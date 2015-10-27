#!/usr/bin/env python3
from __future__ import division,absolute_import
from netCDF4 import Dataset
from pandas import Panel
from os.path import expanduser
from numpy import arange,ndarray,asarray
from datetime import datetime,timedelta
from dateutil.parser import parse
from pytz import UTC
from matplotlib.pyplot import subplots
from matplotlib.colors import LogNorm
from matplotlib.ticker import LogFormatterMathtext,ScalarFormatter
import seaborn as sns
sns.set_context('talk')

def readmsp(fn,date,tlim,elim):
    with Dataset(expanduser(fn),'r') as f:
#%% load by time
        d0 = datetime.strptime(date,'%Y%m%d').replace(tzinfo=UTC)
        secdayutc=f.variables['Time'][:]
        t = asarray([d0 + timedelta(seconds=int(s)) for s in secdayutc])
        if isinstance(tlim,(list,tuple,ndarray)) and len(tlim)==2:
            tind = (parse(tlim[0]) <= t) & (t <= parse(tlim[1]))
        else:
            tind = range(t.size) #instead of [:], which also grabs all values
#%% load by elevation
        elv=arange(181.) #TODO is this right?
        if isinstance(elim,(list,tuple,ndarray)) and len(elim)==2:
            elind = (elim[0] <=elv) & (elv <= elim[1])
        else:
            elind = range(elv.size)
#%% load the rest, assemble into Panel
#        Analog=f.variables['AnalogData'][tind,:]

        Ipeak=f.variables['PeakIntensity'][tind,:,elind]
#        Ibase=f.variables['BaseIntensity'][tind,:,elind]

        wavelen=f.variables['Wavelength'][:]

        Intensity = Panel(items=t[tind],major_axis=wavelen,minor_axis=elv[elind],data=Ipeak)
        return Intensity

def plotmspspectra(Intensity,tlim):
    sfmt = LogFormatterMathtext()
#    sfmt = ScalarFormatter()
#    sfmt.set_powerlimits((-2,2)) #force scientific notation for numbers with 10^a where A<a<B
#    sfmt.set_scientific(True)
#    sfmt.set_useOffset(False)

    #unpack Panel
    wavelen=Intensity.major_axis.values
    elv = Intensity.minor_axis.values
    t=Intensity.items.to_pydatetime()
    Ipeak = Intensity.values
    #%% plots
    fg,ax = subplots(6,1,figsize=(20,12),sharex=True)
    fg.suptitle(t[0].strftime('%Y-%m-%d  Meridian Scanning Photometer: Peak Intensity'),fontsize='large')
    for i,(a,l) in enumerate(zip(ax,wavelen)):
        h=a.pcolormesh(t,elv,Ipeak[:,i,:].T,
                       cmap='cubehelix',norm=LogNorm())
        fg.colorbar(h,ax=a,format=sfmt)
        a.set_title('{:.1f} nm'.format(l))
        a.set_ylabel('elevation [deg.]')
        a.autoscale(True,tight=True)
        if tlim:
            xlim = [parse(l) for l in tlim]
            a.set_xlim(xlim)

    a.set_xlabel('UTC')
