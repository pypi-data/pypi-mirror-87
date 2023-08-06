import pytest

from random import Random

from jheaps import (
    create_addressable_pairing_heap
)


def test_long_heap(): 

    h = create_addressable_pairing_heap(key_type=int)

    h1 = h.insert(5, 15)
    assert h1.key == 5
    assert h1.value == 15
    h1.value=10
    assert h1.value == 10

    h2 = h.insert(6, 20)
    h3 = h.insert(7, 20)
    h4 = h.insert(8, 20)

    h5 = h.find_min()
    assert h5.key == 5
    assert h5.value == 10

    h5.decrease_key(4)
    assert h5.key == 4
    assert h5.value == 10

    assert len(h) == 4

    h5.delete()
    assert len(h) == 3

    # check that handle is still valid even if 
    # removed 
    assert h5.key == 4
    assert h5.value == 10

    # But reusing should throw a value error
    with pytest.raises(ValueError):
        h5.delete()

    h.clear();
    assert len(h) == 0


def test_sort_with_heap():
    rng = Random(17)

    numbers = []
    for i in range(10000):
        numbers.append(rng.randint(0,1000))

    heap = create_addressable_pairing_heap(key_type=int)
    for n in numbers: 
        heap.insert(n, 0)

    sorted_numbers = []
    while len(heap) != 0:
        sorted_numbers.append(heap.delete_min().key)

    assert all(sorted_numbers[i] <= sorted_numbers[i+1] for i in range(len(sorted_numbers)-1))

