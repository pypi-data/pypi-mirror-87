import pytest

from random import Random

from jheaps import (
    create_addressable_pairing_heap, 
    create_doubleended_addressable_pairing_heap,
)


def test_long_mergeable_heap(): 

    h1 = create_addressable_pairing_heap(key_type=int)
    h2 = create_addressable_pairing_heap(key_type=int)

    for i in range(100):
        h1.insert(i, i+1)

    assert len(h1) == 100

    for i in range(100, 200):
        h2.insert(i, i+1)

    assert len(h2) == 100

    h1.meld(h2)

    assert len(h1) == 200
    assert len(h2) == 0

    expected = 0
    while len(h1) > 0: 
        cur = h1.delete_min()
        assert cur.key == expected
        assert cur.value == expected+1
        expected += 1


def test_double_mergeable_heap(): 

    h1 = create_addressable_pairing_heap(key_type=float)
    h2 = create_addressable_pairing_heap(key_type=float)

    for i in range(100):
        h1.insert(i, i+1)

    assert len(h1) == 100

    for i in range(100, 200):
        h2.insert(i, i+1)

    assert len(h2) == 100

    h1.meld(h2)

    assert len(h1) == 200
    assert len(h2) == 0

    expected = 0
    while len(h1) > 0: 
        cur = h1.delete_min()
        assert cur.key == expected
        assert cur.value == expected+1
        expected += 1




def test_long_mergeable_heap_invalid_second_heap(): 

    h1 = create_addressable_pairing_heap(key_type=int)
    h2 = create_addressable_pairing_heap(key_type=int)

    h1.insert(1,1)
    h1.insert(2,1)
    h1.insert(3,1)
    h1.insert(4,1)
    h1.insert(5,1)

    h2.insert(1,1)
    handle1 = h2.insert(2,2)
    h2.insert(3,3)
    h2.insert(4,4)
    h2.insert(5,5)

    h1.meld(h2)
    
    assert len(h1) == 10
    assert len(h2) == 0

    assert handle1.key == 2
    assert handle1.value == 2

    # cannot insert after a meld
    with pytest.raises(ValueError):
        h2.insert(6,6)


def test_longlong_mergeable_doubleended_heap(): 

    h1 = create_doubleended_addressable_pairing_heap(key_type=int)
    h2 = create_doubleended_addressable_pairing_heap(key_type=int)

    for i in range(100):
        h1.insert(i, i+1)

    for i in range(100):
        h2.insert(100+i, 100+i+1)    

    assert len(h1) == 100
    assert len(h2) == 100

    h1.meld(h2)

    assert len(h1) == 200
    assert len(h2) == 0

    expected = 0
    while len(h1) > 100: 
        cur = h1.delete_min()
        assert cur.key == expected
        assert cur.value == expected+1
        expected += 1

    expected = 199
    while len(h1) > 0: 
        cur = h1.delete_max()
        assert cur.key == expected
        assert cur.value == expected+1
        expected -= 1
    
