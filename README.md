# USGS2TELEMAC

This Python code is a graphical user interface to prepare the liquid boundary file for [TELEMAC](http://www.opentelemac.org/ "TELEMAC website") modeling usage. It gets data from JSON format data returned from on-demand requests to NWIS. Piecewise linear interpolation is applied to repair missing raw data and interpolate when increasing temporal resolution.

![](https://github.com/ZhiLiHydro/USGS2TELEMAC/blob/master/capture.jpg)

## Required packages

* Numpy
* Matplotlib
* Pandas
* tkinter
* hydrofunctions

## Usage

coming soon...

### Run

```
python usgs2telemac.py
```


### Use it in TELEMAC

Add this line to the TELEMAC steering file:

```
LIQUID BOUNDARIES FILE = usgs2telemac_liq_boundary
```
