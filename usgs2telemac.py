# coding: utf-8
"""
USGS2TELEMAC
MIT License
Author: Zhi Li, Univ. of Illinois Urbana-Champaign
Contact: zhil2[at]illinois[dot]edu

"""

import sys
import platform
import webbrowser
from urllib import request, error
from base64 import encodebytes
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import hydrofunctions as hf

plt.rcParams['font.family'] = 'Times New Roman'

def main():
    root = tk.Tk()
    root.title('USGS2TELEMAC')
    root.resizable(0, 0)
    
    if platform.system() == 'Darwin':
        w = 4
    else:
        w = 2
        
    msg = tk.Message(
        root,
        text='Setup',
        bg='light cyan',
        font='System 12 bold',
        width=500,
        relief='raised')
    msg.pack()

    row = tk.Frame(root)
    row.pack(side='top')


    unitvar = tk.IntVar()
    unit = tk.Radiobutton(
        row,
        text='m, m3/s',
        width=10,
        font='System 10',
        variable=unitvar,
        value=1)
    unit.pack(side='left') 
    unit.select()
    unit = tk.Radiobutton(
        row,
        text='ft, ft3/s',
        width=10,
        font='System 10',
        variable=unitvar,
        value=0)
    unit.pack(side='left')


    row = tk.Frame(root)
    row.pack(side='top')

    pvar= tk.IntVar()
    p = tk.Radiobutton(
        row,
        text='Days from now',
        width=15,
        font='System 10',
        variable=pvar,
        value=1)
    p.pack(side='left') 
    p.select()

    periodvar = tk.StringVar()
    period = ttk.Combobox(
        row,
        font='System 10',
        width=3,
        textvariable=periodvar)
    period['values'] = ('14', '30', '365')
    period.set('7')
    period.pack(side='left')

    row = tk.Frame(root)
    row.pack(side='top')
    
    p = tk.Radiobutton(
        row,
        text='Begin and End',
        width=15,
        font='System 10',
        variable=pvar,
        value=0)
    p.pack(side='left')

    row = tk.Frame(root)
    row.pack(side='top')
    
    row = tk.Frame(root)
    row.pack(side='top')

    tk.Label(
        row,
        text='Begin (YYYY-MM-DD):',
        width=20,
        font='System 10',
        anchor='w').pack(side='left')
    
    beginvar = tk.StringVar()
    begin = ttk.Combobox(
        row,
        font='System 10',
        width=10,
        textvariable=beginvar)
    begin.set('2020-05-01')
    begin.pack(side='left')

    row = tk.Frame(root)
    row.pack(side='top')

    tk.Label(
        row,
        text='End (YYYY-MM-DD):',
        width=20,
        font='System 10',
        anchor='w').pack(side='left')
    
    endvar = tk.StringVar()
    end = ttk.Combobox(
        row,
        font='System 10',
        width=10,
        textvariable=endvar)
    end.set('2020-06-01')
    end.pack(side='left')
    

    stationvar = []
    bcvar = []
    shiftvar = []
    presetstations = ['05536085','05536580','05536500','05536340','05536290','04087440','05536995']

    msg = tk.Message(
        root,
        text='Station Info',
        bg='light cyan',
        font='System 12 bold',
        width=500,
        relief='raised')
    msg.pack()

    for i in range(16):
        row = tk.Frame(root)
        row.pack(side='top', padx=20)
        
        tk.Label(
            row,
            text=str(i+1).zfill(2)+' Station Number:',
            width=17,
            font='System 10',
            anchor='w').pack(side='left')
        
        stationvar.append(tk.StringVar())
        station = ttk.Combobox(
            row,
            font='System 10',
            width=9,
            textvariable=stationvar[i])
        station.set(presetstations[i] if i < len(presetstations) else 0)
        station.pack(side='left')
        
        tk.Label(
            row,
            text='      '+str(i+1).zfill(2)+' BC Type:',
            width=13,
            font='System 10',
            anchor='w').pack(side='left')

        bcvar.append(tk.StringVar())
        BC = tk.Radiobutton(
            row,
            text='Q',
            width=w,
            font='System 10',
            variable=bcvar[i],
            value='Q')
        BC.pack(side='left') 
        BC.select()
        BC = tk.Radiobutton(
            row,
            text='H',
            width=w,
            font='System 10',
            variable=bcvar[i],
            value='H')
        BC.pack(side='left')


        tk.Label(
            row,
            text='      '+str(i+1).zfill(2)+' Datum Shift:',
            width=17,
            font='System 10',
            anchor='w').pack(side='left')
        
        shiftvar.append(tk.DoubleVar())
        shift = ttk.Combobox(
            row,
            font='System 10',
            width=8,
            textvariable=shiftvar[i])
        shift.set('0')
        shift.pack(side='left')

        row = tk.Frame(root)
        row.pack(side='top')
        

################ BUTTONS ################ 
    row = tk.Frame(root)
    row.pack(side='top',pady=3)
    
    row = tk.Frame(root)
    row.pack(side='top')


    tk.Label(
        row,
        text='Step 1: ',
        width=6,
        font='System 10',
        anchor='w').pack(side='left')


    def gen():
        stationVar = [station.get() for station in stationvar]
        bcVar = [bc.get() for bc in bcvar]
        shiftVar = [shift.get() for shift in shiftvar]
        info = pd.DataFrame(data={'stationVar': stationVar, 'bcVar': bcVar, 'shiftVar': shiftVar})
        info = info[info.stationVar != '0']
        print(info)
        info.to_csv('stationInfo.csv',index=False)
        messagebox.showinfo(
            message='\'stationInfo.csv\' has been generated',
            icon='info')

    tk.Button(
            row, 
            text='Generate stationInfo.csv', 
            font='System 11 bold', 
            command=gen,
            padx=6,
            pady=1).pack(side='left',padx=6,pady=1)


    row = tk.Frame(root)
    row.pack(side='top')

    tk.Label(
        row,
        text='Step 2: ',
        width=6,
        font='System 10',
        anchor='w').pack(side='left')


    def run():
        if pvar.get():
            messagebox.showinfo(
                message='Going to ask USGS for '+periodvar.get()+'-day data... May take some time...',
                icon='info')
        else:
            messagebox.showinfo(
                message='Going to ask USGS for data from '+beginvar.get()+' to '+endvar.get()+'... May take some time...',
                icon='info')
        info = pd.read_csv('stationInfo.csv', dtype={'stationVar':str, 'bcVar':str, 'shiftVar':np.float64})
        q = info[info.bcVar == 'Q']
        h = info[info.bcVar == 'H']
        print('='*30)
        print(q)
        print('='*30)
        print(h)
        print('='*30)
        print('Contacting USGS...')
        if pvar.get():
            dfq = hf.NWIS(q.stationVar.tolist(), 'iv', period='P'+periodvar.get()+'D', parameterCd='00060').df()
            dfh = hf.NWIS(h.stationVar.tolist(), 'iv', period='P'+periodvar.get()+'D', parameterCd='00065').df()
        else:
            dfq = hf.NWIS(q.stationVar.tolist(), 'iv', beginvar.get(), endvar.get(), parameterCd='00060').df()
            dfh = hf.NWIS(h.stationVar.tolist(), 'iv', beginvar.get(), endvar.get(), parameterCd='00065').df()
        for i, station in enumerate(q.stationVar.tolist()):
            dfq.drop(dfq.columns[2*(len(q.stationVar)-i)-1], axis=1, inplace=True)
        for i, station in enumerate(h.stationVar.tolist()):
            dfh.drop(dfh.columns[2*(len(h.stationVar)-i)-1], axis=1, inplace=True)
        if unitvar.get():
            dfq *= 0.3048**3
            dfh *= 0.3048
        for i, shift in enumerate(h.shiftVar.tolist()):
            if shift != 0:
                dfh['USGS:'+h.stationVar.tolist()[i]+':00065:00000'] += shift
        df = dfq.merge(dfh,left_index=True,right_index=True,how='outer')
        df.to_csv('usgs2telemac_raw_data.xls', sep='\t', float_format='%.6f', na_rep='nan')
        
        ax = dfh.interpolate(limit_direction='both').plot(linewidth=.75, marker='o', markersize=.75)
        ax.grid(color='grey', linestyle=':')
        
        if unitvar.get():
            plt.ylabel('Gage height, meter')
        else:
            plt.ylabel('Gage height, feet')
        plt.savefig('H.png',dpi=150)
        plt.close()
        
        ax = dfq.interpolate(limit_direction='both').plot(linewidth=.75, marker='o', markersize=.75)
        ax.grid(color='grey', linestyle=':')
        
        if unitvar.get():
            plt.ylabel('Discharge, cubic meter per second')
        else:
            plt.ylabel('Discharge, cubic feet per second')
        plt.savefig('Q.png',dpi=150)
        plt.close()
        
        t_in_seconds = np.zeros(len(df))
        for i in range(1, len(df)):
            dt = df.index.array[i] - df.index.array[i-1]
            t_in_seconds[i] = t_in_seconds[i-1] + dt.total_seconds()
        df.set_index(t_in_seconds, inplace=True)
        df.interpolate(limit_direction='both', inplace=True)
        head = '#\nT\t'+'\t'.join(['Q('+str(index+1)+')' for index in q.index.values])+'\t'
        head += '\t'.join(['SL('+str(index+1)+')' for index in h.index.values])+'\n'
        if unitvar.get():
            head += 's\t'+'m3/s\t'*len(q)+'m\t'*len(h)+'\n'
        else:
            head += 's\t'+'ft3/s\t'*len(q)+'ft\t'*len(h)+'\n'
        with open('usgs2telemac_liq_boundary.xls', 'w') as f: 
            f.write(head)
        df.to_csv('usgs2telemac_liq_boundary.xls', mode='a', sep='\t', header=False, float_format='%.6f', na_rep='nan')
        print('Done')
        messagebox.showinfo(
            message='job done\n\n\'usgs2telemac_raw_data.xls\' and \'usgs2telemac_liq_boundary.xls\' have been written',
            icon='info')

    tk.Button(
        row,
        text='Ask USGS for data & Generate TELEMAC liquid boundary file',
        font='System 11 bold',
        command=run,
        padx=5,
        pady=1,
        wraplength=150).pack(side='left',padx=6,pady=1)

    row = tk.Frame(root)
    row.pack(side='top')

            
    tk.Button(
        row, 
        text='Quit', 
        font='System 11 bold', 
        command=lambda:root.destroy(),
        padx=10,
        pady=1).pack(side='left',padx=6,pady=1)

    row = tk.Frame(root)
    row.pack(side='top')
 
    def open_github(): 
        webbrowser.open('https://github.com/ZhiLiHydro/USGS2TELEMAC')

    tk.Label(
        row,
        text='visit',
        width=5,
        font='System 10',
        anchor='e').pack(side='left')

    urlok = True
    try:
        u = request.urlopen('https://github.githubassets.com/images/modules/logos_page/GitHub-Logo.png')
    except error.URLError:
        urlok = False
    if urlok:
        icon = u.read()
        u.close()
        icon = tk.PhotoImage(data=encodebytes(icon)).subsample(15, 15)
        tk.Button(
            row,
            font='System 11 bold', 
            command=open_github,
            width=60,
            height=25,
            image=icon).pack(side='left')
    else:      
        tk.Button(
            row,
            text='GitHub',
            font='System 11 bold', 
            command=open_github,
            padx=15,
            pady=1).pack(side='left',padx=3,pady=1)

    tk.Label(
        row,
        text='for README',
        width=10,
        font='System 10',
        anchor='w').pack(side='left')
    
    root.mainloop()

if __name__ == '__main__':
    main()
    
