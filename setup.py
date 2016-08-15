#!/usr/bin/env python
import subprocess
from setuptools import setup

try:
    subprocess.call(['conda','install','--file','requirements.txt'])
except Exception:
    pass


setup(name='spectroreader',
	  description='Spectrometer Reader netCDF4',
	  author='Michael Hirsch',
	  url='https://github.com/scienceopen/meridian-spectrometer-reader',
   install_requires=['pathlib2'],
      packages=['spectroreader'],
	  )

