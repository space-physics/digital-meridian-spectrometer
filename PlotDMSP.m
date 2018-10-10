%% example load/plot DMSP via Python dmsp package

[dat, time, elev, wavelength] = dmsp('~/data/2007-03-23/msp/MSP_2007082.PF');

fg = figure(1);
clf(fg)

Nwl = size(dat,3);
for i = 1:Nwl
    ax = subplot(Nwl, 1, i);
    h = pcolor(ax, datenum(time), elev, dat(:, :, i).');
    set(h, 'edgecolor', 'none')
    title(ax, [wavelength{i}, ' \AA'], 'interpreter', 'latex')
    set(ax, 'ytick', 0:45:180, 'ydir', 'reverse')
    hc = colorbar('peer', ax);
    
    if i < Nwl
        set(ax, 'xtick', [])
    else
        datetick(ax, 'x', 'HH:MM:ss',  'keepticks')
        xlabel(ax, 'UTC')
        ylabel(ax, 'elev. from North [deg]')
    end
    
end

ttxt = char(time(1));
sgtitle(fg, ttxt(1:11))
ylabel(hc, 'Rayleighs')