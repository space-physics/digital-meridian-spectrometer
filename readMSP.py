#!/usr/bin/env python3
from __future__ import division,absolute_import
from netCDF4 import Dataset
from os.path import expanduser
from numpy import arange
from matplotlib.pyplot import subplots,show
#import seaborn

with Dataset(expanduser('~/data/PKR_SMSP_STD_20130414.NC'),'r') as f:
    secdayutc=f.variables['Time'][:]
    X=f.variables['AnalogData'][:]
    Ipeak=f.variables['PeakIntensity'][:]
    Ibase=f.variables['BaseIntensity'][:]
    wavelen=f.variables['Wavelength'][:]
    elv=arange(181.) #TODO is this right?
#%% plots
fg,ax = subplots(6,1,figsize=(15,5))
for i,(a,l) in enumerate(zip(ax,wavelen)):
    a.pcolormesh(secdayutc,elv,Ipeak[:,i,:].T)
    a.set_title('{:.1f} nm'.format(l))
    a.set_ylabel('elevation [deg.]')
    a.autoscale(True,'x',tight=True)

a.set_xlabel('sec since UTC midnight')



show()