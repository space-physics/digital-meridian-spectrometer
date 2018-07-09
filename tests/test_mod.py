#!/usr/bin/env python
from pathlib import Path
import pytest
from datetime import datetime
import dmsp
#
fn = Path(__file__).parent / 'PKR_SMSP_STD_20141011.NC'


def test_load():
    I0 = dmsp.load(fn)

    t0 = I0.time[0].values.astype('datetime64[us]').astype(datetime)
    assert t0 == datetime(2014, 10, 11, 3, 33, 10)

    wavelength = list(I0.data_vars.keys())
    assert wavelength == ['4278', '4861', '5200', '5577', '6300', '6700']


if __name__ == '__main__':
    pytest.main(['-x', __file__])
