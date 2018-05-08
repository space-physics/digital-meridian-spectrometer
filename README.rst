.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.167565.svg
   :target: https://doi.org/10.5281/zenodo.167565

.. image:: https://travis-ci.org/scivision/meridian-spectrometer-reader.svg?branch=master
    :target: https://travis-ci.org/scivision/meridian-spectrometer-reader

.. image:: https://coveralls.io/repos/github/scivision/meridian-spectrometer-reader/badge.svg?branch=master
    :target: https://coveralls.io/github/scivision/meridian-spectrometer-reader?branch=master

.. image:: https://api.codeclimate.com/v1/badges/41995381a6cd84d46cb7/maintainability
   :target: https://codeclimate.com/github/scivision/meridian-spectrometer-reader/maintainability
   :alt: Maintainability

============================
meridian-spectrometer-reader
============================
for Poker Flat Digital Meridian Spectrometer, which uses netCDF

.. image:: tests/demo.png
    :alt: example of PF-DMSP data

.. contents::



Data sources
============
* `2011-present <ftp://optics.gi.alaska.edu/PKR/DMSP/NCDF/>`_
* `1983-2010 (NetCDF 3 .PF files)  <http://optics.gi.alaska.edu/realtime/data/msp/pkr>`_

install
=======
::

    python -m pip install -e .

examples
========
see top comments in LoadMSPdata.py, with the data obtained from the URL above.

Notes
=====
You can also graphically browse the files with the ``ncview`` program::

    apt install ncview

Error: libnetcdf.so.7
=====================
if you get

    ImportError: libnetcdf.so.7: cannot open shared object file: No such file or directory

try::

    apt install libnetcdf-dev
    python -m pip install --upgrade netcdf4
