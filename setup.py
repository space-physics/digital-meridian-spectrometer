#!/usr/bin/env python
from setuptools import setup

req = ['sciencedates',
       'nose','netCDF4','xarray','numpy','matplotlib','python-dateutil','pytz']

setup(name='msp_aurora',
      packages=['msp_aurora'],
      author='Michael Hirsch, Ph.D.',
      url='https://github.com/scivision/meridian-spectrometer-reader',
      version='0.5',
      install_requires=req,
	  )

