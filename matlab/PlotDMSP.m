%% example load/plot DMSP via Python dmsp package

cwd = fileparts(mfilename('fullpath'));
fn = fullfile(cwd, 'src/dmsp/tests/PKR_SMSP_STD_20141011.NC');

p = pyenv;
disp("Using Python "+ p.Version + " " + p.Executable)

[dat, time, elev, wavelength] = dmsp(fn);

fg = figure(1);
clf(fg)

Nwl = size(dat,3);
for i = 1:Nwl
    ax = subplot(Nwl, 1, i);
    h = pcolor(ax, time, elev, dat(:, :, i).');
    set(h, 'edgecolor', 'none')
    title(ax, [wavelength{i}, ' \AA'], 'interpreter', 'latex')
    set(ax, 'ytick', 0:45:180, 'ydir', 'reverse')
    hc = colorbar('peer', ax);

    if i < Nwl
        set(ax, 'xtick', [])
    else
        xlabel(ax, 'UTC')
        ylabel(ax, 'elev. from North [deg]')
    end

end

ylabel(hc, 'Rayleighs')
