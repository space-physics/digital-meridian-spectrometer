from __future__ import annotations
from pathlib import Path
import typing

from netCDF4 import Dataset
import xarray
import numpy as np
from datetime import datetime, timedelta
from dateutil.parser import parse


def load(
    fn: Path,
    tlim: tuple[datetime, datetime] | None = None,
    elevlim: tuple[float, float] | None = None,
) -> xarray.Dataset:
    """
    This function works with 1983-2010 netCDF3 as well as 2011-present netCDF4 files.
    """
    fn = Path(fn).expanduser()
    # %% date from filename -- only way
    ext = fn.suffix.lower()
    if ext == ".nc":
        d0 = datetime.strptime(fn.stem[13:21], "%Y%m%d")
    elif ext == ".pf":
        year = int(fn.stem[4:8])
        days = int(fn.stem[8:11])
        d0 = datetime(year, 1, 1) + timedelta(days=days - 1)

    with Dataset(fn, "r") as f:
        # %% load by time
        secdayutc = f["Time"][:]
        # convert to datetimes -- need as ndarray for next line
        t = np.array([d0 + timedelta(seconds=int(s)) for s in secdayutc])

        tind: typing.Any
        if tlim is not None and len(tlim) == 2:
            if isinstance(tlim[0], str):
                tlim = [parse(t) for t in tlim]
            tind = (tlim[0] <= t) & (t <= tlim[1])
        else:
            tind = slice(None)
        # %% elevation from North horizon
        """
        elevation is not stored anywhere in the data files...
        """
        elv = np.arange(181.0)
        elind: typing.Any
        if elevlim is not None and len(elevlim) == 2:
            elind = (elevlim[0] <= elv) & (elv <= elevlim[1])
        else:
            elind = slice(None)
        # %% wavelength channels
        wavelen = (f["Wavelength"][:] * 10).astype(int)
        goodwl = wavelen > 1  # some channels are unused in some files
        # %% load the data
        #        Analog=f['AnalogData'][tind,:]
        #        Ibase=f['BaseIntensity'][tind,goodwl,elind]
        Ipeak = f["PeakIntensity"][tind, :, elind]  # time x wavelength x elevation angle
        if Ipeak.shape[1] != wavelen.size:
            wavelen = wavelen[goodwl]
        # %% root out bad channels 2011-03-01 for example
        goodwl &= ~(Ipeak == 0).all(axis=(0, 2))
        wavelen = wavelen[goodwl]
        """
        astype(float) is critical to avoid overflow of int16 dtype!
        """
        Ipeak = f["PeakIntensity"][tind, goodwl, elind].astype(float)
        # %% filter factor per wavelength Rayleigh/PMT * 128
        filtfact = f["FilterFactor"][goodwl]
    # %% assemble output
    R = xarray.Dataset(coords={"time": t[tind], "elevation": elv[elind]})

    for i, w in enumerate(wavelen.astype(str)):
        R[w] = (("time", "elevation"), Ipeak[:, i, :] * filtfact[i].astype(float) / 128.0)

    return R
