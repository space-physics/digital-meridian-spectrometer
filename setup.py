#!/usr/bin/env python
req = ['nose','netCDF4','xarray','numpy','matplotlib','python-dateutil','pytz']
pipreq=['sciencedates',]

import pip
try:
    import conda.cli
    conda.cli.main('install',*req)
except Exception as e:
    pip.main(['install']+req)
pip.main(['install']+pipreq)
# %%
from setuptools import setup

setup(name='msp_aurora',
      packages=['msp_aurora'],
      author='Michael Hirsch, Ph.D.',
      url='https://github.com/scivision/meridian-spectrometer-reader',
      version='0.5',
	  )

