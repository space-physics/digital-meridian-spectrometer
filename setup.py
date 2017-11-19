#!/usr/bin/env python
req = ['nose','netCDF4','xarray','numpy','python-dateutil','pytz',
       'sciencedates']

from setuptools import setup,find_packages

setup(name='msp_aurora',
      packages=find_packages(),
      author='Michael Hirsch, Ph.D.',
      url='https://github.com/scivision/meridian-spectrometer-reader',
      description="Load and plot UAF Geophysical Institute Digital Meridian Spectrometer data",
      version='0.5.0',
      classifiers=[
      'Intended Audience :: Science/Research',
      'Development Status :: 4 - Beta',
      'License :: OSI Approved :: MIT License',
      'Topic :: Scientific/Engineering :: Atmospheric Science',
      'Programming Language :: Python :: 3',
      ],
      install_requires=req,
      python_requires='>=3.6',
      extras_require={'plot':['matplotlib',]},
	  )

