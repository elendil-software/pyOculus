import pytest
from mock import patch
from snapper import rise_set, set_exposure, set_location, DAY_EXP, NIGHT_EXP
from datetime import datetime, timedelta
from astropy.time import Time
import numpy as np

class TestCalculations:

    def test_sunset_sunrise(self):
        OBSERVATORY = set_location()
        now = datetime(2016,4,6,12,10,0)
        sunset = datetime(2016,4,6,18,57)
        sunrise = datetime(2016,4,6,5,37)
        calc_sunrise, calc_sunset = rise_set(OBSERVATORY, now)
        assert np.abs(sunset - calc_sunset) < timedelta(seconds=600)
        assert np.abs(sunrise - calc_sunrise) < timedelta(seconds=600)


    def test_twilight_exposure(self):
        OBSERVATORY = set_location()
        now = datetime(2016,4,6,19,0)
        exposure = set_exposure(OBSERVATORY, now)
        assert exposure == DAY_EXP

    def test_twilight_exposur2(self):
        OBSERVATORY = set_location()
        now = datetime(2016,4,6,19,20)
        exposure = set_exposure(OBSERVATORY, now)
        assert exposure == NIGHT_EXP/10.
