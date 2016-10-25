from datetime import datetime
from pytz import UTC
from matplotlib.pyplot import subplots,figure
from matplotlib.colors import LogNorm
from matplotlib.dates import DateFormatter
from matplotlib.ticker import LogFormatterMathtext#,ScalarFormatter
#
from isrutils.plots import timeticks

def plotmspspectra(Intensity):
    sfmt = LogFormatterMathtext()
#    sfmt = ScalarFormatter()
#    sfmt.set_powerlimits((-2,2)) #force scientific notation for numbers with 10^a where A<a<B
#    sfmt.set_scientific(True)
#    sfmt.set_useOffset(False)

    wavelen = Intensity.wavelength.values
    Ipeak = Intensity.values
    t = Intensity.time
    #%% plots
    fg,ax = subplots(wavelen.size,1,figsize=(20,12),sharex=True)
    for i,(a,l) in enumerate(zip(ax,wavelen)):
        h=a.pcolormesh(t, Intensity.elevation,
                       Ipeak[:,i,:].T,
                       cmap='cubehelix_r',norm=LogNorm())

        fg.colorbar(h,ax=a,format=sfmt)

        a.set_title('{:.1f} nm'.format(l/10))

        a.invert_yaxis()
        a.autoscale(True,tight=True)


    fg.text(0.88, 0.5, 'Rayleighs', ha='center', va='center', rotation='vertical')
    fg.text(0.01, 0.5, 'elevation from North [deg.]', ha='center', va='center', rotation='vertical')

    tickfix(t,fg,a)


    fg.suptitle(datetime.fromtimestamp(t[0].item()/1e9, tz=UTC).strftime('%Y-%m-%d') +
                '  Meridian Scanning Photometer: Peak Intensity',
                y=0.99)
    fg.tight_layout(pad=1.5)

def plotratio(ratio,wl):
    fg = figure()
    ax = fg.gca()
    hi = ax.pcolormesh(ratio.time,ratio.elevation,
                       ratio.T,
                       cmap='cubehelix_r')

    fg.colorbar(hi,ax=ax).set_label('{} / {}'.format(wl[0],wl[1]))

    ax.set_ylabel('elevation from North [deg.]')

    tickfix(ratio.time,fg,ax)

def tickfix(t,fg,ax):
    majtick,mintick = timeticks(t[-1] - t[0])
    if majtick:
        ax.xaxis.set_major_locator(majtick)
    if mintick:
        ax.xaxis.set_minor_locator(mintick)
    ax.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
    fg.autofmt_xdate()
    ax.set_xlabel('UTC')