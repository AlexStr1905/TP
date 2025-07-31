import pytest
from simple_library_01.functions import get_month_days


def test_get_month_days():
    assert get_month_days(2000, 2) == 29
    assert get_month_days(2025, 2) == 28
    assert get_month_days(2013, 1) == 31
    assert get_month_days(1945, 4) == 30
    assert get_month_days(1930, 1) == 30


def test_get_month_days_invalid_month():
    with pytest.raises(AttributeError):
        get_month_days(2025, 13)
    with pytest.raises(AttributeError):
        get_month_days(2025, 0)
