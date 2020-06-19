# USGS2TELEMAC

This graphical interface is designed to: 1) ask [USGS NWIS](https://waterdata.usgs.gov/nwis) for flow discharge and gage height data of interested USGS gaging stations and interested period of time, 2) download received data, and 3) prepare the liquid boundary file for [TELEMAC-2D/3D](http://www.opentelemac.org/) modeling usage. It sends on-demand requests to NWIS and receives JSON format data returned from NWIS, with help of the [HydroFunctions](https://github.com/mroberge/hydrofunctions) project. Piecewise linear interpolation is applied when repairing NANs in the raw data and when increasing temporal resolution (for example, in the case that station A has 1-min temporal resolution and station B has 15-min temporal resolution, the data of station B needs to be interpolated to adapt the 1-min resolution of station A).

![](https://github.com/ZhiLiHydro/USGS2TELEMAC/blob/master/img/capture.jpg)

## Prerequisites

* Python 3
* tkinter
* Numpy
* Matplotlib
* Pandas
* hydrofunctions


### Run

```
python usgs2telemac.py
```

Enter station number (8 digits), boundary condition type (flow discharge or gage height) and datum shift (a real number). Datum shift is needed for gage height data because TELEMAC needs a unified datum, no matter it is NGVD 29 or NAVD 88 or an arbitrary one.

Click `Generate stationInfo.csv` button to get a station info file.

Click `Ask USGS` button to send requests to NWIS, receive data from NWIS and make the liquid boundary file for TELEMAC.

### Use it in TELEMAC

Add the following line to the TELEMAC-2D/3D steering file (usually *.cas):

```
LIQUID BOUNDARIES FILE = usgs2telemac_liq_boundary.xls
```
