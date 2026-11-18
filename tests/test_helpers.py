
import pytest

from oanda.helpers import side_to_close

def make_position(long_units, short_units):
    return {"long": {"units": long_units}, "short": {"units": short_units}}

def test_long_open():
    assert side_to_close(make_position("100", "0")) == "longUnits"

def test_short_open():
    assert side_to_close(make_position("0", "-100")) == "shortUnits"

def test_nothing_open():
    assert side_to_close(make_position("0", "0")) is None

def test_both_sides_open_raises():
    with pytest.raises(ValueError):
        side_to_close(make_position("100", "-100"))