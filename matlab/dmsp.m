function [dat, time, elev, wavelength] = dmsp(fn)
%% Load digital meridian scanning photometer from Matlab.
% https://www.scivision.dev/matlab-python-user-module-import/
%
% fn: DMSP filename to read
%
% example:
% [dat, time, elev, wavelength] = dmsp('~/data/2011-03-01/msp/MSP_2011060.PF');
arguments
  fn (1,1) string {mustBeFile}
end

I = py.dmsp.load(fn);

time = datetime2datetime(I{'time'});
elev = double(I{'elevation'}.values);
wavelength = string(py.list(I.data_vars.keys()));

dat = nan(length(time), length(elev), length(wavelength));

for i = 1:length(wavelength)
    dat(:, :, i) = xarray2mat(I, char(wavelength{i}));
end

end


function M = xarray2mat(V, key)
arguments
  V
  key string = string.empty
end

if nargin < 2  % xarray.DataArray
  M = double(py.numpy.asfortranarray(V));
else % xarray.Dataset
  M = double(py.numpy.asfortranarray(V{key}));
end

end


function dt = datetime2datetime(t0)

dt = datetime(t0.values.astype("datetime64[ms]").tolist());

end
