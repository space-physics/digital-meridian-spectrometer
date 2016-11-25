from datetime import datetime
from pytz import UTC
import numpy as np
from matplotlib.pyplot import subplots
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

vlims = {4278:[500,15000], 4861:[100,1000], 5200:[100,2000], 6700:[100,2000],
         5577:[4e3,1e5],6300:[1000,20000]}

chem = {4278: r'$N_{2}^{+}$ 1N', 4861: r'H$_\beta$', 5200:'[NI]', 6700:r'N$_2$ 1P',
         5577:'[OI]32', 6300:'[OI]21'}

def plotmspspectra(I,elfid):
    wl = I.wavelength.values
    #%% plots
    fg,ax = subplots(wl.size,1,figsize=(20,12),sharex=True)

    spectrasubplot(wl,I,fg,ax,elfid,False,vlims)
    tickfix(I.time, fg, fg.gca())

    fg.text(0.89, 0.5, 'Rayleighs', ha='center', va='center', rotation='vertical')
    fg.text(0.01, 0.5, 'elevation from North [deg.]', ha='center', va='center', rotation='vertical')

    fg.suptitle(datetime.fromtimestamp(I.time[0].item()/1e9, tz=UTC).strftime('%Y-%m-%d') +
                '  Meridian Scanning Photometer: Peak Intensity',
                y=0.99)
    fg.tight_layout(pad=1.1)

def spectrasubplot(wl,I,fg,ax,elfid,indlbl=False,clim=None):
    assert isinstance(indlbl,bool)

    for a,l in zip(ax,wl):
        if clim is None:
            c=(None,None)
        elif isinstance(clim,dict) and l in vlims:
                c = vlims[l]
        elif len(clim)==2:
            c=(None,None)
        else:
            raise TypeError('not sure what clim you are setting with {}'.format(clim))

        h=a.pcolormesh(I.time, I.elevation,
                       I.sel(wavelength=l).values.T,
                       cmap='cubehelix_r',norm=LogNorm(),
                       vmin=c[0],vmax=c[1])

        hc = fg.colorbar(h,ax=a,format=sfmt)
        if indlbl:
            hc.set_label('Rayleighs')

        for f in elfid:
            a.axhline(f,color='gold',alpha=0.8,linestyle='--')

        a.set_title('{:.1f} nm  '.format(l/10) + chem[l])

        a.invert_yaxis()
        a.autoscale(True,tight=True)

def plotratio(ratio,wl,I, elfid, ratlim,verbose):
    if ratio is None:
        return

    ratio = ratio.T
    fg,ax = subplots(3,1,figsize=(20,12),sharex=True)

    spectrasubplot(wl,I,fg,ax[:2],elfid,True,[1e3,1e4]) #FIXME make ratlim based

    hi = ax[2].pcolormesh(ratio.time,ratio.elevation,
                          ratio.values,
                          cmap='bwr',
                          norm=MidpointNormalize(midpoint=ratlim[1]),
                          vmin=ratlim[0], vmax=ratlim[2])

    for f in elfid:
        ax[2].axhline(f,color='gold',alpha=0.85,linestyle='--')

    ax[2].invert_yaxis()
    ax[2].autoscale(True,tight=True)

    fg.colorbar(hi,ax=ax[2]).set_label('{} / {}'.format(wl[0],wl[1]))

    fg.text(0.085, 0.5, 'elevation from North [deg.]', ha='center', va='center', rotation='vertical')

    fg.suptitle(datetime.fromtimestamp(I.time[0].item()/1e9, tz=UTC).strftime('%Y-%m-%d') +
                '  Meridian Scanning Photometer: {} / {} Intensity Ratio'.format(wl[0],wl[1]))
               # y=0.99)

    tickfix(ratio.time,fg,ax[2])
#%% make lots of line subplots
    if verbose:
        nsub = ratio.time.size
        ncol = 4
        nrow = nsub//ncol
        fg,axs = subplots(nrow,ncol,sharey=True,sharex=True)
        for i,ax in enumerate(axs.ravel()):
            if i==nsub:
                break
            ax.plot(ratio[:,i],ratio.elevation)
            ax.set_title(datetime.fromtimestamp(ratio.time[i].item()/1e9, tz=UTC).strftime('%H:%M:%S'))

            for f in elfid:
                ax.axhline(f,color='gold',alpha=0.85,linestyle='--')

        ax.invert_yaxis()

        fg.text(0.05, 0.5, 'elevation from North [deg.]', ha='center', va='center', rotation='vertical')
        fg.text(0.5, 0.02, 'Intensity ratio: {} / {}'.format(wl[0],wl[1]), ha='center', va='center')

        fg.suptitle(datetime.fromtimestamp(I.time[0].item()/1e9, tz=UTC).strftime('%Y-%m-%d') +
                '  Meridian Scanning Photometer: {} / {} Intensity Ratio'.format(wl[0],wl[1]))



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