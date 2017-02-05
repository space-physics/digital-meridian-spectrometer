#!/usr/bin/env python
from setuptools import setup

try:
    import conda.cli
    conda.cli.main('install','--file','requirements.txt')
except Exception as e:
    print(e)
    import pip
    pip.main(['install','-r','requirements.txt'])
    

setup(name='msp_aurora',
      install_requires=['nose','netCDF4','xarray','numpy','matplotlib','python-dateutil','pytz',
        'histutils','isrutils'],
      dependency_links = [
        'https://github.com/scienceopen/histutils/tarball/master#egg=histutils',
        'https://github.com/scienceopen/isrutils/tarball/master#egg=isrutils',],
      packages=['msp_aurora'],
	  )

