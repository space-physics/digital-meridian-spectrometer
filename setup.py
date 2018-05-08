#!/usr/bin/env python
install_requires = ['netCDF4','xarray','numpy','python-dateutil','pytz',
       'sciencedates']
tests_require=['pytest','nose','coveralls']

from setuptools import setup,find_packages

setup(name='msp_aurora',
      packages=find_packages(),
      author='Michael Hirsch, Ph.D.',
      url='https://github.com/scivision/meridian-spectrometer-reader',
      description="Load and plot UAF Geophysical Institute Digital Meridian Spectrometer data",
      version='0.5.2',
      classifiers=[
      'Development Status :: 4 - Beta',
      'Intended Audience :: Science/Research',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 3.6',
      'Programming Language :: Python :: 3.7',
      'Topic :: Scientific/Engineering :: Atmospheric Science',
      ],
      install_requires=install_requires,
      python_requires='>=3.6',
      extras_require={'plot':['matplotlib',],
                      'tests':tests_require},
      tests_require=tests_require,
      scripts=['LoadMSPdata.py'],
	  )

