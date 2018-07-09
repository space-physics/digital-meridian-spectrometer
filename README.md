[![image](https://zenodo.org/badge/DOI/10.5281/zenodo.167565.svg)](https://doi.org/10.5281/zenodo.167565)
[![image](https://travis-ci.org/scivision/digital-meridian-spectrometer.svg?branch=master)](https://travis-ci.org/scivision/digital-meridian-spectrometer)
[![Coverage Status](https://coveralls.io/repos/github/scivision/digital-meridian-spectrometer/badge.svg?branch=master)](https://coveralls.io/github/scivision/digital-meridian-spectrometer?branch=master)
[![Build status](https://ci.appveyor.com/api/projects/status/r7044ijm5pgmawwg?svg=true)](https://ci.appveyor.com/project/scivision/digital-meridian-spectrometer)


## Digital Meridian Spectrometer

For Geophysical Institute's Poker Flat Digital Meridian Spectrometer, which uses netCDF

![example of PF-DMSP data](tests/demo.png)

This library is also usable from Matlab, as seen in `dmsp.m`.


## Data sources

* 2011-present: ftp://optics.gi.alaska.edu/PKR/DMSP/NCDF/
* [1983-2010 (NetCDF 3 .PF files)](http://optics.gi.alaska.edu/realtime/data/msp/pkr)
* [other dates](http://optics.gi.alaska.edu/realtime/data/archive/PKR_MSP_X/)


## Install

    python -m pip install -e .

## Usage examples

see top comments in LoadMSPdata.py, with the data obtained from the URL above.

## Notes

You can also graphically browse the files with the `ncview` program:
```sh
apt install ncview
```

### Error: libnetcdf.so.7

if you get

> ImportError: libnetcdf.so.7: cannot open shared object file: No such file or directory

try:
```sh
apt install libnetcdf-dev
python -m pip install netcdf4
```
or
```sh
conda install netcdf4
```
