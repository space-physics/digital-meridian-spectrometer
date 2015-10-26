#!/usr/bin/env python3
from __future__ import division,absolute_import
from netCDF4 import Dataset
from pandas import Panel
from os.path import expanduser
from numpy import arange
from matplotlib.pyplot import subplots,show
from datetime import datetime,timedelta
from dateutil.parser import parse
#import seaborn

def readmsp(fn,date):
    with Dataset(expanduser(fn),'r') as f:
        secdayutc=f.variables['Time'][:]
        t = [parse(date)+ timedelta(seconds=int(s)) for s in secdayutc]


        Analog=f.variables['AnalogData'][:]

        Ipeak=f.variables['PeakIntensity'][:]
        Ibase=f.variables['BaseIntensity'][:]

        wavelen=f.variables['Wavelength'][:]
        elv=arange(181.) #TODO is this right?

        Intensity = Panel(items=t,major_axis=wavelen,minor_axis=elv,data=Ipeak)
        return Intensity

def plotmspspectra(Intensity,tlim):
    #unpack Panel
    wavelen=Intensity.major_axis.values
    elv = Intensity.minor_axis.values
    t=Intensity.items.to_pydatetime()
    Ipeak = Intensity.values
    #%% plots
    fg,ax = subplots(6,1,figsize=(20,12))
    fg.suptitle(t[0].strftime('%Y-%m-%d'))
    for i,(a,l) in enumerate(zip(ax,wavelen)):
        h=a.pcolormesh(t,elv,Ipeak[:,i,:].T,cmap='cubehelix')
        fg.colorbar(h,ax=a)
        a.set_title('{:.1f} nm'.format(l))
        a.set_ylabel('elevation [deg.]')
        a.autoscale(True,'x',tight=True)
        if tlim:
            xlim = [parse(l) for l in tlim]
            a.set_xlim(xlim)

    a.set_xlabel('UTC')


if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description='reading Poker Flat Research Range Meridian Scanning Photometer')
    p.add_argument('ncfn',help='netCDF data file name to read')
    p.add_argument('date',help='date of file YYYYMMDD') #FIXME: regexp filename
    p.add_argument('--tlim',help='time window to zoom plot in on',nargs=2)
    p = p.parse_args()

    Intensity = readmsp(p.ncfn,p.date)
    plotmspspectra(Intensity,None)
    if p.tlim:
        plotmspspectra(Intensity,p.tlim) #zoom

    show()