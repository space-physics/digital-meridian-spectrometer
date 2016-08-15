#!/usr/bin/env python
from six import string_types
from netCDF4 import Dataset
from xarray import DataArray
from numpy import arange,array
from datetime import datetime,timedelta
from dateutil.parser import parse
from pytz import UTC
from matplotlib.pyplot import subplots
from matplotlib.colors import LogNorm
from matplotlib.dates import DateFormatter
from matplotlib.ticker import LogFormatterMathtext#,ScalarFormatter
import seaborn as sns
sns.set_context('talk')
sns.set_style('ticks')
#
from histutils.fortrandates import yd2datetime

def readmsp(fn, tlim,elim):
    """
    This function works with 1983-2010 netCDF3 as well as 2011-present netCDF4 files.
    """
#%% date from filename -- only way
    ext = fn.suffix.lower()
    if ext == '.nc':
        d0 = datetime.strptime(fn.stem[13:21],'%Y%m%d')
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
        goodwl = wavelen > 0 #some channels are unused in some files
#%% filter factor per wavelength Rayleigh/PMT * 128
        filtfact = f['FilterFactor'][goodwl]
#%% load the data
#        Analog=f['AnalogData'][tind,:]
#        Ibase=f['BaseIntensity'][tind,goodwl,elind]

        # astype(float) is critical to avoid overflow!
        Ipeak = f['PeakIntensity'][tind,goodwl,elind].astype(float)  # time x wavelength x elevation angle
    Ipeak = Ipeak * filtfact[None,:,None].astype(float) / 128.

    assert (Ipeak>=0).all(),'did you forget to cast to float before math ops?'


    I = DataArray(data = Ipeak,
                  dims = ['time','wavelength','elevation'],
                  coords = {'time':t[tind], 'wavelength':wavelen[goodwl], 'elevation':elv[elind]})

    return I

def plotmspspectra(Intensity):
    sfmt = LogFormatterMathtext()
#    sfmt = ScalarFormatter()
#    sfmt.set_powerlimits((-2,2)) #force scientific notation for numbers with 10^a where A<a<B
#    sfmt.set_scientific(True)
#    sfmt.set_useOffset(False)

    wavelen = Intensity.wavelength.values
    elv = Intensity.elevation
    t=Intensity.time  #str(datetime.fromtimestamp(t.item()/1e9, tz=UTC))[:-6]
    Ipeak = Intensity.values
    #%% plots
    fg,ax = subplots(wavelen.size,1,figsize=(20,12),sharex=True)
    fg.suptitle(datetime.fromtimestamp(t[0].item()/1e9, tz=UTC).strftime('%Y-%m-%d') +
                '  Meridian Scanning Photometer: Peak Intensity')
    for i,(a,l) in enumerate(zip(ax,wavelen)):
        h=a.pcolormesh(t,elv,Ipeak[:,i,:].T,
                       cmap='cubehelix',norm=LogNorm())
        fg.colorbar(h,ax=a,format=sfmt).set_label('Rayleighs')
        a.set_title('{:.1f} nm'.format(l))
        a.set_ylabel('elev. from North [deg.]')
        a.autoscale(True,tight=True)



    a.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
    fg.autofmt_xdate()
    a.set_xlabel('UTC')

    #fg.tight_layout(pad=1.7)
