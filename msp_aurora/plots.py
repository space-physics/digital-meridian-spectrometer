from datetime import datetime
from pytz import UTC
from matplotlib.pyplot import subplots
from matplotlib.colors import LogNorm
from matplotlib.dates import DateFormatter
from matplotlib.ticker import LogFormatterMathtext#,ScalarFormatter

import seaborn as sns
sns.set_context('talk')
sns.set_style('ticks')
#
from isrutils.plots import timeticks

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
    for i,(a,l) in enumerate(zip(ax,wavelen)):
        h=a.pcolormesh(t,elv,Ipeak[:,i,:].T,
                       cmap='cubehelix',norm=LogNorm())
        fg.colorbar(h,ax=a,format=sfmt).set_label('Rayleighs')
        a.set_title('{:.1f} nm'.format(l))

        a.invert_yaxis()
        a.autoscale(True,tight=True)


    a.set_ylabel('elev. North [deg.]')

    majtick,mintick = timeticks(t[-1] -t[0])
    a.xaxis.set_major_locator(majtick)
    a.xaxis.set_minor_locator(mintick)
    a.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
    fg.autofmt_xdate()
    a.set_xlabel('UTC')


    fg.suptitle(datetime.fromtimestamp(t[0].item()/1e9, tz=UTC).strftime('%Y-%m-%d') +
                '  Meridian Scanning Photometer: Peak Intensity',
                y=0.99)
    fg.tight_layout(pad=1.7)
