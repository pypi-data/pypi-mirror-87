import pytest

from jheaps import (
    create_doublended_implicit_binary_heap
)


def test_minmax_any_heap(): 

    h = create_doublended_implicit_binary_heap(key_type=object)

    h.insert("1")
    h.insert("2")
    h.insert("3")
    h.insert("4")
    h.insert("5")

    assert "1".__lt__("5")

    assert "1" == h.find_min()
    assert "5" == h.find_max()

    assert "5" == h.delete_max()
    assert "4" == h.find_max()

    assert "1" == h.delete_min()
    assert "2" == h.find_min()


def test_minmax_double_heap(): 

    h = create_doublended_implicit_binary_heap(key_type=float)

    h.insert(1.0)
    h.insert(2.1)
    h.insert(3.2)
    h.insert(4.3)
    h.insert(5.4)

    assert 1.0 == h.find_min()
    assert 5.4 == h.find_max()

    assert 5.4 == h.delete_max()
    assert 4.3 == h.find_max()

    assert 1.0 == h.delete_min()
    assert 2.1 == h.find_min()
