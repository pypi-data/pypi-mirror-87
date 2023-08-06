import pytest

from random import Random

from jheaps import (
    create_implicit_dary_heap,
    create_addressable_dary_heap
)

def test_double_dary_heap_implicit(): 

    h = create_implicit_dary_heap(key_type=float, d=4)

    h.insert(5.5)
    h.insert(6.5)
    h.insert(7.5)
    h.insert(8.5)

    h5 = h.find_min()
    assert h5 == 5.5

    assert len(h) == 4

    h.delete_min()
    assert 6.5 == h.find_min()
    assert len(h) == 3

    assert 6.5 == h.delete_min()
    assert 7.5 == h.find_min()

    h.clear()
    assert len(h) == 0


def test_long_dary_heap_implicit(): 

    h = create_implicit_dary_heap(key_type=int, d=8)

    for i in range(100):
        h.insert(i)    

    last = None
    while len(h) != 0: 
        cur = h.delete_min()
        if last is not None: 
            assert last < cur
        last = cur

    assert len(h) == 0
