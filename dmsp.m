function [dat, time, elev, wavelength] = dmsp(fn)
%% Load digital meridian scanning photometer from Matlab.
% https://www.scivision.co/matlab-python-user-module-import/
%
% fn: DMSP filename to read
%
% example:
% [dat, time, elev, wavelength] = dmsp('~/data/2011-03-01/msp/MSP_2011060.PF');


assert(~verLessThan('matlab', '9.5'), 'Matlab >= R2018b required')

validateattributes(fn, {'char'}, {'scalartext'})

I = py.dmsp.load(fn);

time = datetime2datetime(I{'time'});
elev = double(I{'elevation'}.values);
wavelength = cellfun(@char, cell(py.list(I.data_vars.keys())), 'uniformoutput', false);

dat = nan(length(time), length(elev), length(wavelength));

for i = 1:length(wavelength)
    dat(:, :, i) = xarray2mat(I, char(wavelength{i})); %#ok<AGROW,*NASGU>
end

end


function M = xarray2mat(V, key)
if nargin < 2  % xarray.DataArray
  M = double(py.numpy.asfortranarray(V));
else % xarray.Dataset
  M = double(py.numpy.asfortranarray(V{key}));
end
end


function dt = datetime2datetime(t0)

t0 = t0.values.tolist();

dt = NaT(length(t0), 1);

for i = 1:length(t0)
    t = cellfun(@double, cell(t0{i}.utctimetuple()));
    dt(i) = datetime(t(1), t(2), t(3), t(4), t(5), t(6));
end


end
