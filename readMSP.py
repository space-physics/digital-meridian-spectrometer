#!/usr/bin/env python3
from __future__ import division,absolute_import
from netCDF4 import Dataset
from pandas import Panel
from os.path import expanduser
from numpy import arange
from matplotlib.pyplot import subplots,show
#import seaborn

def readmsp(fn):
    with Dataset(expanduser(fn),'r') as f:
        secdayutc=f.variables['Time'][:]
        Analog=f.variables['AnalogData'][:]

        Ipeak=f.variables['PeakIntensity'][:]
        Ibase=f.variables['BaseIntensity'][:]

        wavelen=f.variables['Wavelength'][:]
        elv=arange(181.) #TODO is this right?

        Intensity = Panel(items=secdayutc,major_axis=wavelen,minor_axis=elv,data=Ipeak)
        return Intensity

def plotmspspectra(Intensity):
    #unpack Panel
    wavelen=Intensity.major_axis.values
    elv = Intensity.minor_axis.values
    secdayutc=Intensity.items.values
    Ipeak = Intensity.values
    #%% plots
    fg,ax = subplots(6,1,figsize=(15,5))
    for i,(a,l) in enumerate(zip(ax,wavelen)):
        a.pcolormesh(secdayutc,elv,Ipeak[:,i,:].T,cmap='cubehelix')
        a.set_title('{:.1f} nm'.format(l))
        a.set_ylabel('elevation [deg.]')
        a.autoscale(True,'x',tight=True)

    a.set_xlabel('sec since UTC midnight')

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description='reading Poker Flat Research Range Meridian Scanning Photometer')
    p.add_argument('ncfn',help='netCDF data file name to read')
    p = p.parse_args()

    Intensity = readmsp(p.ncfn)
    plotmspspectra(Intensity)

    show()