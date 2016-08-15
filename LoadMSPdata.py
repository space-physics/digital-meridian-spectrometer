#!/usr/bin/env python3
from __future__ import division
from msp_aurora import Path
from matplotlib.pyplot import show
#
from msp_aurora.readMSP import readmsp,plotmspspectra

"""
Note: elevation from North Horizon, so magnetic zenith ~ 180-77.5 =

2007-03-23
./LoadMSPdata.py ~/data/2007-03-23/msp/MSP_2007082.PF -t 2007-03-23T10:30 2007-03-23T12:00Z  -e 95 110

2013-04-13
./LoadMSPdata.py ~/data/2013-04-11/msp/PKR_SMSP_STD_20130411.NC -t 2013-04-11T10:30:00Z 2013-04-11T11:30:00Z  -e 95 110

2013-04-14
./LoadMSPdata.py ~/data/2013-04-14/msp/PKR_SMSP_STD_20130414.NC -t 2013-04-14T08:00:00Z 2013-04-14T09:30:00Z  -e 95 110
"""

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description='reading Poker Flat Research Range Meridian Scanning Photometer')
    p.add_argument('ncfn',help='netCDF data file name to read')
    p.add_argument('-t','--tlim',help='time window to zoom plot in on',nargs=2)
    p.add_argument('-e','--elim',help='elevation limits to plot FROM NORTH HORIZON',nargs=2,type=float)
    p = p.parse_args()

    fn = Path(p.ncfn).expanduser()

    Intensity = readmsp(fn, p.tlim, p.elim)
    plotmspspectra(Intensity,None)

    show()