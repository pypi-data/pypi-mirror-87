import pytest

from random import Random

from jheaps import (
    create_addressable_pairing_heap
)


def test_double_any_value_heap(): 

    h = create_addressable_pairing_heap(key_type=float, value_type=object)

    h1 = h.insert(5.5, "15")
    assert h1.key == 5.5
    assert h1.value == "15"
    h1.value="10"
    assert h1.value == "10"

    h.insert(6.5, "20")
    h.insert(7.5, "20")
    h.insert(8.5, "20")

    h5 = h.find_min()
    assert h5.key == 5.5
    assert h5.value == "10"

    h5.decrease_key(4.5)
    assert h5.key == 4.5
    assert h5.value == "10"

    assert len(h) == 4

    h5.delete()
    assert len(h) == 3

    # check that handle is still valid even if 
    # removed 
    assert h5.key == 4.5
    assert h5.value == "10"

    # But reusing should throw a value error
    with pytest.raises(ValueError):
        h5.delete()

    h.clear()
    assert len(h) == 0



