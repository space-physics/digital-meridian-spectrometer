#!/usr/bin/env python
from matplotlib.pyplot import show
from argparse import ArgumentParser
import dmsp
import dmsp.plots as dmp

try:
    import seaborn as sns

    sns.set_context("talk", font_scale=1.25)
    sns.set_style("ticks")
except ImportError:
    pass

"""
Note: elevation from North Horizon, so to get near magnetic zenith at Poker Flat we use elevation angles
    FROM NORTH of 95-110 degrees corresponding to symmetric about 77.5 elevation angle

2007-03-23T1120
./LoadMSPdata.py ~/data/2007-03-23/msp/MSP_2007082.PF -t 2007-03-23T10:30 2007-03-23T12:00 -e 85 120 --elfid 98 107 -v
./LoadMSPdata.py ~/data/2007-03-23/msp/MSP_2007082.PF -t 2007-03-23T11:17 2007-03-23T11:28 -e 85 120 --elfid 98 107 -r 0.2 1 2 -v
./LoadMSPdata.py ~/data/2007-03-23/msp/MSP_2007082.PF -t 2007-03-23T11:17 2007-03-23T11:28 -e 85 120 --elfid 98 107 --wl 5577 4278 -r 0.7 1 3 -v

2011-03-01T1000
./LoadMSPdata.py ~/data/2011-03-01/msp/MSP_2011060.PF -t 2011-03-01T10:02 2011-03-01T10:20 -e 75 125 --elfid 82 118 --wl 5577 4278 -r 1 2 3
./LoadMSPdata.py ~/data/2011-03-01/msp/MSP_2011060.PF -t 2011-03-01T10:05 2011-03-01T10:07 -e 75 125 --elfid 82 118 --wl 5577 4278 -r 1 2 3 -v

2013-04-11T1030
./LoadMSPdata.py ~/data/2013-04-11/msp/PKR_SMSP_STD_20130411.NC -t 2013-04-11T10:30:00 2013-04-11T11:30:00  -e 90 115 --elfid 98 107
#
2013-04-14T0854
./LoadMSPdata.py ~/data/2013-04-14/msp/PKR_SMSP_STD_20130414.NC -t 2013-04-14T08:51:00 2013-04-14T08:58:00  -e 85 120 --elfid 98 107 -v
2013-04-14T0826
./LoadMSPdata.py ~/data/2013-04-14/msp/PKR_SMSP_STD_20130414.NC -t 2013-04-14T08:25:00 2013-04-14T08:27:00  -e 85 120 --elfid 98 107 -v
-r   1 2 3 is a starting point for 5577/4278 ratio
-r 0.5 1 3 is a starting point for 6300/4278 ratio
"""


def main():
    p = ArgumentParser(
        description="reading Poker Flat Research Range Meridian Scanning Photometer"
    )
    p.add_argument("ncfn", help="netCDF data file name to read")
    p.add_argument("-t", "--tlim", help="time window to zoom plot in on", nargs=2)
    p.add_argument(
        "-e", "--elim", help="elevation limits to plot FROM NORTH HORIZON", nargs=2, type=float
    )
    p.add_argument(
        "-r",
        "--ratlim",
        help="min,mid,max of ratio plot colormap",
        nargs=3,
        type=float,
        default=[0.5, 1, 3],
    )
    p.add_argument("--wl", help="wavelengths to ratio [A]", nargs=2)
    p.add_argument(
        "--elfid",
        help="elevation angles at which to place fiducials (for other camera)",
        type=float,
        nargs=2,
        default=[],
    )
    p.add_argument("-v", "--verbose", action="store_true")
    p = p.parse_args()

    Intensity = dmsp.load(p.ncfn, p.tlim, p.elim)
    dmp.plotmspspectra(Intensity, p.elfid)
    # %% ratios
    if p.wl:
        ratio = Intensity[p.wl[0]] / Intensity[p.wl[1]]
        dmp.plotratio(ratio, p.wl, Intensity, p.elfid, p.ratlim, p.verbose)

    show()


if __name__ == "__main__":
    main()
