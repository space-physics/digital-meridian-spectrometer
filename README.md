[![image](https://zenodo.org/badge/DOI/10.5281/zenodo.167565.svg)](https://doi.org/10.5281/zenodo.167565)
[![image](https://travis-ci.org/scivision/meridian-spectrometer-reader.svg?branch=master)](https://travis-ci.org/scivision/meridian-spectrometer-reader)
[![image](https://coveralls.io/repos/github/scivision/meridian-spectrometer-reader/badge.svg?branch=master)](https://coveralls.io/github/scivision/meridian-spectrometer-reader?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/41995381a6cd84d46cb7/maintainability)](https://codeclimate.com/github/scivision/meridian-spectrometer-reader/maintainability)

## meridian-spectrometer-reader

for Poker Flat Digital Meridian Spectrometer, which uses netCDF

![example of PF-DMSP data](tests/demo.png)


## Data sources

-   [2011-present](ftp://optics.gi.alaska.edu/PKR/DMSP/NCDF/)
-   [1983-2010 (NetCDF 3 .PF files)](http://optics.gi.alaska.edu/realtime/data/msp/pkr)


## Install

    python -m pip install -e .

## Usage examples

see top comments in LoadMSPdata.py, with the data obtained from the URL above.

## Notes

You can also graphically browse the files with the `ncview` program:

    apt install ncview

### Error: libnetcdf.so.7

if you get

> ImportError: libnetcdf.so.7: cannot open shared object file: No such
> file or directory

try:

    apt install libnetcdf-dev
    python -m pip install --upgrade netcdf4
