#!/usr/bin/env python
install_requires = ['netCDF4','xarray','numpy','python-dateutil','pytz',
       'sciencedates']
tests_require=['nose','coveralls']

from setuptools import setup,find_packages

setup(name='msp_aurora',
      packages=find_packages(),
      author='Michael Hirsch, Ph.D.',
      url='https://github.com/scivision/meridian-spectrometer-reader',
      description="Load and plot UAF Geophysical Institute Digital Meridian Spectrometer data",
      version='0.5.1',
      classifiers=[
      'Intended Audience :: Science/Research',
      'Development Status :: 4 - Beta',
      'License :: OSI Approved :: MIT License',
      'Topic :: Scientific/Engineering :: Atmospheric Science',
      'Programming Language :: Python :: 3',
      ],
      install_requires=install_requires,
      python_requires='>=3.6',
      extras_require={'plot':['matplotlib',],
                      'tests':tests_require},
      tests_require=tests_require,
	  )

