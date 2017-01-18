#!/usr/bin/env python
import subprocess
from setuptools import setup

try:
    subprocess.call(['conda','install','--file','requirements.txt'])
except Exception:
    pass


setup(name='msp_aurora',
	  description='MSP Aurora Spectrometer Reader netCDF4 / netCDF3',
	  author='Michael Hirsch',
	  url='https://github.com/scienceopen/meridian-spectrometer-reader',
      install_requires=['histutils','isrutils'],
      dependency_links = [
        'https://github.com/scienceopen/histutils/tarball/master#egg=histutils',
        'https://github.com/scienceopen/isrutils/tarball/master#egg=isrutils',],
      packages=['msp_aurora'],
	  )

