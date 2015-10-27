#!/usr/bin/env python3

from setuptools import setup

with open('README.rst','r') as f:
	long_description = f.read()

setup(name='spectroreader',
      version='0.1',
	  description='Spectrometer Reader netCDF4',
	  long_description=long_description,
	  author='Michael Hirsch',
	  url='https://github.com/scienceopen/meridian-spectrometer-reader',
   install_requires=['netCDF4','pytz','six','nose'],
      packages=['spectroreader'],
	  )

