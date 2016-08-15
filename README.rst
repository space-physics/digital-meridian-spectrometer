============================
meridian-spectrometer-reader
============================
for Poker Flat Digital Meridian Spectrometer, which uses netCDF

.. contents::

.. image:: tests/demo.png
    :alt: example of MSP data



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
