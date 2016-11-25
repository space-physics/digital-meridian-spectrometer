.. image:: https://travis-ci.org/scienceopen/meridian-spectrometer-reader.svg?branch=master
    :target: https://travis-ci.org/scienceopen/meridian-spectrometer-reader

============================
meridian-spectrometer-reader
============================
for Poker Flat Digital Meridian Spectrometer, which uses netCDF

.. image:: tests/demo.png
    :alt: example of PF-DMSP data

.. contents::



Data sources
============
* 2011-present ftp://optics.gi.alaska.edu/PKR/DMSP/NCDF/
* 1983-2010 (NetCDF 3 .PF files)  http://optics.gi.alaska.edu/realtime/data/msp/pkr

install
=======
::

    python setup.py develop

examples
========
see top comments in LoadMSPdata.py, with the data obtained from the URL above.

Notes
=====
You can also graphically browse the files with the ``ncview`` program::

    apt-get install ncview

Error: libnetcdf.so.7
=====================
if you get::

    ImportError: libnetcdf.so.7: cannot open shared object file: No such file or directory

try::

    sudo apt install libnetcdf-dev
    pip install --upgrade netcdf4
