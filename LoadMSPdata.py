#!/usr/bin/env python3
from matplotlib.pyplot import show
#
from msp_aurora import readmsp,lineratio
from msp_aurora.plots import plotmspspectra,plotratio
import seaborn as sns
sns.set_context('talk')
sns.set_style('ticks')

"""
Note: elevation from North Horizon, so to get near magnetic zenith at Poker Flat we use elevation angles
    FROM NORTH of 95-110 degrees corresponding to symmetric about 77.5 elevation angle

2007-03-23
./LoadMSPdata.py ~/data/2007-03-23/msp/MSP_2007082.PF -t 2007-03-23T10:30 2007-03-23T12:00Z  -e 90 115 --elfid 98 107

2013-04-11
./LoadMSPdata.py ~/data/2013-04-11/msp/PKR_SMSP_STD_20130411.NC -t 2013-04-11T10:30:00Z 2013-04-11T11:30:00Z  -e 90 115 --elfid 98 107

2013-04-14
./LoadMSPdata.py ~/data/2013-04-14/msp/PKR_SMSP_STD_20130414.NC -t 2013-04-14T08:00:00Z 2013-04-14T09:30:00Z  -e 85 120 --elfid 98 107
"""

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description='reading Poker Flat Research Range Meridian Scanning Photometer')
    p.add_argument('ncfn',help='netCDF data file name to read')
    p.add_argument('-t','--tlim',help='time window to zoom plot in on',nargs=2)
    p.add_argument('-e','--elim',help='elevation limits to plot FROM NORTH HORIZON',nargs=2,type=float)
    p.add_argument('--wl',help='wavelengths to ratio [A]',nargs=2,default=[6300,4278])
    p.add_argument('--elfid',help='elevation angles at which to place fiducials (for other camera)',type=float,nargs=2,default=[])
    p.add_argument('-v','--verbose',action='store_true')
    p = p.parse_args()

    Intensity = readmsp(p.ncfn, p.tlim, p.elim)
    plotmspspectra(Intensity, p.elfid)
#%%
    ratio = lineratio(Intensity,p.wl)
    plotratio(ratio,p.wl, Intensity.sel(wavelength=p.wl), p.elfid, p.verbose)

    show()