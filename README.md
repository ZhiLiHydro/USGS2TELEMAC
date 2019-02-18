# USGS2TELEMAC

This Python code is to prepare the liquid boundary file for [TELEMAC](http://www.opentelemac.org/ "TELEMAC website") modeling usage. It's operating on the raw discharge data or gauge height data downloaded from [USGS Current Water Data](https://waterdata.usgs.gov/nwis/rt "USGS Current Water Data") website. Piecewise linear interpolation is applied to repair missing raw data and interpolate when increasing temporal resolution.

## Required packages

* Numpy
* Matplotlib
* Pandas >= 0.24.0 (otherwise it will raise error at `.to_numpy()`)

## Usage

### Prepare the `*.txt` files

* Navigate to the page for the gauging station of interest.
* Select desired date range and check 'Tab-separated' for output format. 
* Copy and paste the data to a txt file and save it to working directory. It is recommended to name this txt file using the name of the gauging station.
* Repeat to obtain txt files containing data of all gauging stations of interet. Starting date and time should be exactly the same for all stations, but ending date and time does not need to. In the end, `gauge1.txt`, `gauge2.txt`, `gauge3.txt`, etc. should be in the working directory.

### Prepare the `user_input.csv` file
Create the user input file as following example:

|gauge1.txt|gauge2.txt|gauge3.txt|...more...|
|---|---|---|---|
|Q(1)|Q(2)|SL(3)|...more...|
|m3/s|m3/s|m|...more...|
|nan|nan|12.34|...more...|

Notes:
* Line 1: files names. Line 2: boundary types. Line 3: units. Line 4: datum conversion.
* `Q` and `SL` stand for discharge boundary condition and water level boundary condition, respectively.
* Units are not important in the current version of TELEMAC.
* `nan` should be put under all Q boundaries ~~if unit conversion from cfs to cms is not needed. Otherwise, put the unit conversion factor under all Q boundaries, e.g. from cfs to cms, 0.02831684659~~. Now cfs/ft is forced to convert to cms/m by default. The unit of datum conversion should be in m.

### Run

```
python usgs2telemac.py
```


### Use it in TELEMAC

Add this line to the TELEMAC steering file:

```
LIQUID BOUNDARIES FILE = liquid_boundary.xls
```
