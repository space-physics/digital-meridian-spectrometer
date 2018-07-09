#!/usr/bin/env python
from pathlib import Path
from numpy.testing import run_module_suite
from msp_aurora import readmsp
#
fn = Path(__file__).parent / 'PKR_SMSP_STD_20141011.NC'


def test_load():
    Intensity = readmsp(fn)
    print(Intensity)


if __name__ == '__main__':
    run_module_suite()
