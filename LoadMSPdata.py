#!/usr/bin/env python3
from __future__ import division,absolute_import
from os.path import basename
from matplotlib.pyplot import show
#
from spectroreader.readMSP import readmsp,plotmspspectra

"""
example:

2013 Apr 13
./LoadMSPdata.py ~/data/2013-04-11/MSP/PKR_SMSP_STD_20130411.NC -t 2013-04-11T10:30:00Z 2013-04-11T11:30:00Z -e 70 85

2013 Apr 14
./LoadMSPdata.py ~/data/2013-04-14/MSP/PKR_SMSP_STD_20130414.NC -t 2013-04-14T08:00:00Z 2013-04-14T09:30:00Z -e 70 85
"""

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description='reading Poker Flat Research Range Meridian Scanning Photometer')
    p.add_argument('ncfn',help='netCDF data file name to read')
    p.add_argument('-t','--tlim',help='time window to zoom plot in on',nargs=2)
    p.add_argument('-e','--elim',help='elevation limits to plot',nargs=2,type=float)
    p = p.parse_args()

    base = basename(p.ncfn)
    date = base[13:21]

    Intensity = readmsp(p.ncfn,date,p.tlim,p.elim)
    plotmspspectra(Intensity,None)

    show()