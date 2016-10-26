from datetime import datetime
from pytz import UTC
import numpy as np
from matplotlib.pyplot import subplots,figure
from matplotlib.colors import LogNorm
from matplotlib.dates import DateFormatter
from matplotlib.ticker import LogFormatterMathtext#,ScalarFormatter
import matplotlib.colors as colors
#
from isrutils.plots import timeticks

sfmt = LogFormatterMathtext()
#    sfmt = ScalarFormatter()
#    sfmt.set_powerlimits((-2,2)) #force scientific notation for numbers with 10^a where A<a<B
#    sfmt.set_scientific(True)
#    sfmt.set_useOffset(False)

def plotmspspectra(I):
    wl = I.wavelength.values
    #%% plots
    fg,ax = subplots(wl.size,1,figsize=(20,12),sharex=True)

    spectrasubplot(wl,I,fg,ax)
    tickfix(I.time, fg, fg.gca())

    fg.text(0.88, 0.5, 'Rayleighs', ha='center', va='center', rotation='vertical')
    fg.text(0.01, 0.5, 'elevation from North [deg.]', ha='center', va='center', rotation='vertical')

    fg.suptitle(datetime.fromtimestamp(I.time[0].item()/1e9, tz=UTC).strftime('%Y-%m-%d') +
                '  Meridian Scanning Photometer: Peak Intensity',
                y=0.99)
    fg.tight_layout(pad=1.5)

def spectrasubplot(wl,I,fg,ax,indlbl=False,clim=(None,None)):
    for i,(a,l) in enumerate(zip(ax,wl)):
        h=a.pcolormesh(I.time, I.elevation,
                       I[:,i,:].T,
                       cmap='cubehelix_r',norm=LogNorm(),
                       vmin=clim[0],vmax=clim[1])

        hc = fg.colorbar(h,ax=a,format=sfmt)
        if indlbl:
            hc.set_label('Rayleighs')

        a.set_title('{:.1f} nm'.format(l/10))

        a.invert_yaxis()
        a.autoscale(True,tight=True)

def plotratio(ratio,wl,I):
    fg,ax = subplots(3,1,figsize=(20,12),sharex=True)

    spectrasubplot(wl,I,fg,ax[:2],True,(1e3,1e4))

    hi = ax[2].pcolormesh(ratio.time,ratio.elevation,
                          ratio.T,
                          cmap='bwr',
                          norm=MidpointNormalize(midpoint=1.))
    ax[2].autoscale(True,tight=True)

    fg.colorbar(hi,ax=ax[2]).set_label('{} / {}'.format(wl[0],wl[1]))

    fg.text(0.085, 0.5, 'elevation from North [deg.]', ha='center', va='center', rotation='vertical')

    fg.suptitle(datetime.fromtimestamp(I.time[0].item()/1e9, tz=UTC).strftime('%Y-%m-%d') +
                '  Meridian Scanning Photometer: {} / {} Intensity Ratio'.format(wl[0],wl[1]))
               # y=0.99)

    tickfix(ratio.time,fg,ax[2])


def tickfix(t,fg,ax):
    majtick,mintick = timeticks(t[-1] - t[0])
    if majtick:
        ax.xaxis.set_major_locator(majtick)
    if mintick:
        ax.xaxis.set_minor_locator(mintick)
    ax.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
    fg.autofmt_xdate()
    ax.set_xlabel('UTC')

class MidpointNormalize(colors.Normalize):
    """
    http://matplotlib.org/users/colormapnorms.html
    may appear in a future version of Matplotlib
    """
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        # I'm ignoring masked values and all kinds of edge cases to make a
        # simple example...
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y))