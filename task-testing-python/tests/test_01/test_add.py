from simple_library_01.functions import add


def test_add():
    assert add(1, 3) == 4
    assert add(-1488, 1488) == 0
    assert add(-3, 53) == 50
    assert add(0, 0) == 0
