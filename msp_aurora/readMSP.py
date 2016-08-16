#!/usr/bin/env python
from six import string_types
from netCDF4 import Dataset
from xarray import DataArray
from numpy import arange,array
from datetime import datetime,timedelta
from dateutil.parser import parse
#
from histutils.fortrandates import yd2datetime,forceutc

def readmsp(fn, tlim,elim):
    """
    This function works with 1983-2010 netCDF3 as well as 2011-present netCDF4 files.
    """
#%% date from filename -- only way
    ext = fn.suffix.lower()
    if ext == '.nc':
        d0 = forceutc(datetime.strptime(fn.stem[13:21],'%Y%m%d'))
    elif ext == '.pf':
        d0 = yd2datetime(fn.stem[4:])


    with Dataset(str(fn),'r') as f:
#%% load by time
        secdayutc = f['Time'][:]
        # convert to datetimes -- need as ndarray for next line
        t = array([d0 + timedelta(seconds=int(s)) for s in secdayutc])
        if tlim is not None and len(tlim)==2:
            if isinstance(tlim[0],string_types):
                tlim = [parse(t) for t in tlim]
            tind = (tlim[0] <= t) & (t <= tlim[1])
        else:
            tind = slice(None)
#%% elevation from North horizon
        elv=arange(181.) #TODO is this right?
        if elim is not None and len(elim)==2:
            elind = (elim[0] <= elv) & (elv <= elim[1])
        else:
            elind = slice(None)
#%% wavelength channels
        wavelen = f['Wavelength'][:] # vector of measured wavelengths [nm]
        goodwl = wavelen > 1. #some channels are unused in some files
#%% load the data
#        Analog=f['AnalogData'][tind,:]
#        Ibase=f['BaseIntensity'][tind,goodwl,elind]
        Ipeak = f['PeakIntensity'][tind,goodwl,elind] # time x wavelength x elevation angle
#%% root out bad channels 2011-03-01 for example
        for i in range(wavelen[goodwl].size):
            if (Ipeak[:,i,:]==0).all():
                goodwl[i] = False
        # astype(float) is critical to avoid overflow!
        Ipeak = f['PeakIntensity'][tind,goodwl,elind].astype(float)
#%% filter factor per wavelength Rayleigh/PMT * 128
        filtfact = f['FilterFactor'][goodwl]


    Rayleigh = Ipeak * filtfact[None,:,None].astype(float) / 128.



    R = DataArray(data = Rayleigh,
                  dims = ['time','wavelength','elevation'],
                  coords = {'time':t[tind], 'wavelength':wavelen[goodwl], 'elevation':elv[elind]})

    return R