"""
Author: Z. Li
License: MIT License
"""
from __future__ import division
from __future__ import print_function
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import threading
import itertools
import datetime
import time
import sys
import os


def woking_animate():
    """
    Manage loading wheel.

    """
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            sys.stdout.flush()
            break
        sys.stdout.write('\rWorking ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rDone!    ')


def num_non_data_lines(fname):
    """
    Count the number of non-data lines in the beginning of data file.

    Parameters
    ----------
    fname : str
        The file name of one gauging station.

    Returns
    -------
    i : non-negative integer
        The number of non-data lines.
    """
    with open(fname, 'r') as f:
        lines = f.readlines()
        i = 0
        for each_line in lines:
            if each_line[0] == '#':
                i = i + 1
            else:
                break
    i = i + 2  # USGS writes 2 lines after # lines and data lines
    return i


def find_longest(fnames):
    """
    Find the largest number of rows among all gauging stations.

    Parameters
    ----------
    fnames : list
        The file names of all gauging stations.

    Returns
    -------
    lg : non-negative integer
        The largest number of rows.
    """
    l = np.zeros(len(fnames))
    i = 0
    for fname in fnames:
        n = num_non_data_lines(fname)
        df = pd.read_csv(fname, sep='\t', skiprows=n, header=None)
        l[i] = len(df[0])
        i = i + 1
    lg = int(np.max(l))
    return lg


def extract_time_series(fname, col_time, col_data):
    """
    Extract the time series of discharge data
    or gauge height data from one file.

    Parameters
    ----------
    fname : str
        The file name of one gauging station.
    col_time : non-negative integer, optional
        The column number of date time data.
    col_data : non-negative integer, optional
        The column number of discharge data or gauge height data.

    Returns
    -------
    t_in_seconds : 1d numpy array
        The time series in seconds converted from date and time data.
    d : 1d numpy array
        The time series of discharge data or gauge height data.
    """
    n = num_non_data_lines(fname)
    df = pd.read_csv(fname, sep='\t', skiprows=n, header=None)
    t_in_seconds = np.zeros(len(df[col_time]))
    for i in range(1, len(df[col_time])):
        s1 = datetime.datetime.strptime(df[col_time][i - 1], '%Y-%m-%d %H:%M')
        s2 = datetime.datetime.strptime(df[col_time][i], '%Y-%m-%d %H:%M')
        dt = s2 - s1
        t_in_seconds[i] = t_in_seconds[i - 1] + dt.total_seconds()
    d = df[col_data].to_numpy()
    return t_in_seconds, d


def generate_A(fnames, col_num, types, datum):
    """
    Generate the matrix before interpolation.

    Parameters
    ----------
    fnames : list
        The file names of all gauging stations.
    datum : 1d numpy array
        The datum conversions of all gauging stations
        (only for gauge height data).

    Returns
    -------
    A : 2d numpy array
        The matrix before interpolation.
    """
    L = find_longest(fnames)
    A = np.full((L, len(fnames) * 2), np.nan)
    i = 0
    for fname in fnames:
        t, d = extract_time_series(fname, 2, col_num[i])
        if types[i + 1][0] == 'Q':
            d = d * 0.3048**3  # convert from cfs to cms
        elif types[i + 1][0] == 'S':
            d = d * 0.3048  # convert from ft to m
        if np.isnan(datum[i]) == False:
            d = d + datum[i]
        A[:len(t), i * 2] = t
        A[:len(t), i * 2 + 1] = d
        i = i + 1
    return A


def interpol(v):
    """
    Interpolte data to higher temporal resolution.

    Parameters
    ----------
    v : 1d numpy array
        The data before interpolation.

    Returns
    -------
    A : 2d numpy array
        The data after interpolation.
    """
    j = 0
    index = np.zeros(sum(~np.isnan(v)))
    index = index.astype(int)
    for i in range(np.size(v)):
        if np.isnan(v[i]) == False:
            index[j] = i
            j = j + 1
    for i in range(1, j):
        a = v[index[i - 1]]
        b = v[index[i]]
        m = 1
        for k in range(index[i - 1] + 1, index[i]):
            v[k] = a + (b - a) * m / (index[i] - index[i - 1])
            m = m + 1
    for i in range(np.size(v)):
        if np.isnan(v[i]):
            v[i] = v[i - 1]
    return v


def generate_R(A):
    """
    Generate the final output matrix ready for TELEMAC.

    Parameters
    ----------
    A : 2d numpy array
        The matrix before interpolation.

    Returns
    -------
    R : 2d numpy array
        The matrix after interpolation and ready for TELEMAC.
    """
    col = int(np.size(A[0, :]) / 2) + 1
    row = np.size(A[:, 0])
    R = np.full((row, col), np.nan)
    for i in range(np.size(A[-1, :])):
        if np.isnan(A[-1, i]) == False:
            break
    R[:, 0] = np.copy(A[:, i])
    R[:, int(i / 2) + 1] = np.copy(A[:, i + 1])
    for j in range(1, col):
        if np.isnan(R[0, j]):
            for i in range(row):
                if np.isnan(A[i, (j - 1) * 2]):
                    break
                else:
                    index = np.searchsorted(R[:, 0], A[i, (j - 1) * 2])
                    R[index, j] = A[i, j * 2 - 1]
            R[:, j] = interpol(R[:, j])
        else:
            continue
    return R


def load_user_input():
    """
    Load gauging station names, types (Q or H), units and
    datum conversions from user input file.

    """
    with open('user_input.csv', 'r') as f:
        lines = f.readlines()
        fnames = lines[0].replace('\n', '').split(',')
        col_num = np.asarray(lines[1].split(','), dtype=np.int)
        types = lines[2].replace('\n', '').split(',')
        units = lines[3].replace('\n', '').split(',')
        datum = np.asarray(lines[4].split(','), dtype=np.float)
        types.insert(0, 'T')
        units.insert(0, 's')
    return fnames, col_num, types, units, datum


def plot(R, fnames, types):
    """
    Plot all (divided into H and Q two categories).

    """
    plt.figure(figsize=(10, 8))
    plt.subplot(2, 1, 1)
    le = []
    for i in range(len(fnames)):
        if types[i + 1][0] == 'S':
            plt.plot(R[:, 0], R[:, i + 1])
            le.append(fnames[i])
    plt.xlabel('Time [s]')
    plt.ylabel('Water level [m]')
    plt.grid()
    plt.legend(le)
    plt.title('Water levels')
    plt.subplot(2, 1, 2)
    le = []
    for i in range(len(fnames)):
        if types[i + 1][0] == 'Q':
            plt.plot(R[:, 0], R[:, i + 1])
            le.append(fnames[i])
    plt.xlabel('Time [s]')
    plt.ylabel('Discharge [cms]')
    plt.grid()
    plt.legend(le)
    plt.title('Discharges')
    plt.tight_layout()
    plt.show()


def main():
    try:
        os.remove('liquid_boundary.xls')
        print('\rPrevious output file deleted!')
    except FileNotFoundError:
        pass
    global done
    done = False
    t = threading.Thread(target=woking_animate)
    t.start()
    try:
        fnames, col_num, types, units, datum = load_user_input()
        A = generate_A(fnames, col_num, types, datum)
        R = generate_R(A)
        h = '#\n' + '\t'.join(types) + '\n' + '\t'.join(units)
        np.savetxt('liquid_boundary.xls', R, delimiter='\t',
                   fmt='%.4f', header=h, comments='')
    except TypeError:
        print('\rFound TypeError!')
    except FileNotFoundError:
        print('\rFound FileNotFoundError!')
    except OSError:
        print('\rFound other type of OSError!')
    except BaseException:
        print('\rFound other type of error!')
    done = True
    plot(R, fnames, types)


if __name__ == "__main__":
    main()
