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
      packages=['msp_aurora'],
      author='Michael Hirsch, Ph.D.',
      url='https://github.com/scienceopen/meridian-spectrometer-reader',
      version='0.5',
      install_requires=['sciencedates',
                        'isrutils'],
      dependency_links = [
        'https://github.com/scienceopen/isrutils/tarball/master#egg=isrutils',],

	  )

