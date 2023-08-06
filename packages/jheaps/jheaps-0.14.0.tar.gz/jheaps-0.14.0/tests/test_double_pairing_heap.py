import pytest

from random import Random

from jheaps import (
    create_doubleended_addressable_pairing_heap
)


def test_long_heap(): 

    h = create_doubleended_addressable_pairing_heap(key_type=int)

    h1 = h.insert(5, 15)
    assert h1.key == 5
    assert h1.value == 15
    h1.value=10
    assert h1.value == 10

    h2 = h.insert(6, 40)
    h3 = h.insert(7, 30)
    h4 = h.insert(8, 20)

    h5 = h.find_min()
    assert h5.key == 5
    assert h5.value == 10

    h5.decrease_key(4)
    assert h5.key == 4
    assert h5.value == 10

    assert len(h) == 4

    h6 = h.find_max()
    assert h6.key == 8
    assert h6.value == 20

    h7 = h.delete_max()
    assert h7.key == 8
    assert h7.value == 20

    h6 = h.find_max()
    assert h6.key == 7
    assert h6.value == 30

    h6.increase_key(9)
    assert h6.key == 9
    assert h6.value == 30


def test_double_heap(): 

    h = create_doubleended_addressable_pairing_heap(key_type=float)

    h1 = h.insert(5.5, 15)
    assert h1.key == 5.5
    assert h1.value == 15
    h1.value=10
    assert h1.value == 10

    h2 = h.insert(6.5, 40)
    h3 = h.insert(7.5, 30)
    h4 = h.insert(8.5, 20)

    h5 = h.find_min()
    assert h5.key == 5.5
    assert h5.value == 10

    h5.decrease_key(4.5)
    assert h5.key == 4.5
    assert h5.value == 10

    assert len(h) == 4

    h6 = h.find_max()
    assert h6.key == 8.5
    assert h6.value == 20

    h7 = h.delete_max()
    assert h7.key == 8.5
    assert h7.value == 20

    h6 = h.find_max()
    assert h6.key == 7.5
    assert h6.value == 30

    h6.increase_key(9.5)
    assert h6.key == 9.5
    assert h6.value == 30


def test_any_heap(): 

    h = create_doubleended_addressable_pairing_heap(key_type=object, value_type=object)

    print(h)

    h1 = h.insert("5.5", "15")
    assert h1.key == "5.5"
    assert h1.value == "15"
    h1.value="10"
    assert h1.value == "10"

    h2 = h.insert("6.5", "40")
    h3 = h.insert("7.5", "30")
    h4 = h.insert("8.5", "20")

    h5 = h.find_min()
    assert h5.key == "5.5"
    assert h5.value == "10"

    h5.decrease_key("4.5")
    assert h5.key == "4.5"
    assert h5.value == "10"

    assert len(h) == 4

    h6 = h.find_max()
    assert h6.key == "8.5"
    assert h6.value == "20"

    h7 = h.delete_max()
    assert h7.key == "8.5"
    assert h7.value == "20"

    h6 = h.find_max()
    assert h6.key == "7.5"
    assert h6.value == "30"

    h6.increase_key("9.5")
    assert h6.key == "9.5"
    assert h6.value == "30"
