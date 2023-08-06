import pytest

from random import Random

from jheaps import create_implicit_binary_heap

from jheaps._internals._utils import _ref_count


class MyKey:
    def __init__(self, value):
        self._value = value

    def __lt__(self, o):
        return self._value < o._value

    def __eq__(self, o):
        return self._value == o._value

    def __str__(self):
        return "{}".format(self._value)


def test_any_heap():

    # Create an implicit non-addressable heap
    h = create_implicit_binary_heap(key_type=object)

    h.insert(MyKey(5.5))

    h.insert(MyKey(6.5))
    h.insert(MyKey(7.5))
    h.insert(MyKey(8.5))

    h5 = h.find_min()
    assert h5 == MyKey(5.5)

    assert len(h) == 4

    h6 = h.delete_min()
    assert h6 == MyKey(5.5)
    assert len(h) == 3

    assert h.find_min() == MyKey(6.5)

    h.clear()
    assert len(h) == 0


def test_any_heap_ref_counts():

    h = create_implicit_binary_heap(key_type=object)

    allobjects = []
    for i in range(10):
        allobjects.append(object())

    for o in allobjects:
        pre_ref_count = _ref_count(o)
        h.insert(o)
        post_ref_count = _ref_count(o)
        assert pre_ref_count + 1 == post_ref_count
