import pytest

from random import Random

from jheaps import (
    create_addressable_pairing_heap
)

class MyKey():

    def __init__(self, value):
        self._value = value

    def __lt__(self, o):
        return self._value < o._value

    def __eq__(self, o):
        return self._value == o._value    

    def __str__(self): 
        return '{}'.format(self._value)

class MyValue():
    def __init__(self, value):
        self._value = value

    def __eq__(self, o):
        return self._value == o._value

    def __str__(self): 
        return '{}'.format(self._value)


def test_any_any_addressable_heap(): 

    h = create_addressable_pairing_heap(key_type=object, value_type=object)

    h1 = h.insert(MyKey(5.5), MyValue(15))
    assert h1.key == MyKey(5.5)
    assert h1.value == MyValue(15)
    h1.value = MyValue(10)
    assert h1.value == MyValue(10)

    h.insert(MyKey(6.5), MyValue(20))
    h.insert(MyKey(7.5), MyValue(20))
    h.insert(MyKey(8.5), MyValue(20))

    h5 = h.find_min()
    assert h5.key == MyKey(5.5)
    assert h5.value == MyValue(10)

    h5.decrease_key(MyKey(4.5))
    assert h5.key == MyKey(4.5)
    assert h5.value == MyValue(10)

    assert len(h) == 4

    h5.delete()
    assert len(h) == 3

    # check that handle is still valid even if 
    # removed 
    assert h5.key == MyKey(4.5)
    assert h5.value == MyValue(10)

    # But reusing should throw a value error
    with pytest.raises(ValueError):
        h5.delete()

    h.clear()
    assert len(h) == 0



