import pytest
from simple_library_01.functions import is_leap


def test_is_leap():
    assert is_leap(2024)
    assert is_leap(2000)
    assert not is_leap(1955)
    assert not is_leap(1900)


def test_is_leap_attribute_error():
    with pytest.raises(AttributeError):
        is_leap(-1488)
