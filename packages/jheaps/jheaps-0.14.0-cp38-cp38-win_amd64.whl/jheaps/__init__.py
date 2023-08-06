"""
Python-JHeaps Library
~~~~~~~~~~~~~~~~~~~~~

JHeaps is a library providing state-of-the-art heap data structures.

See https://github.com/d-michail/python-jheaps for more details.
"""

from .__version__ import __title__, __description__, __url__
from .__version__ import __version__, __backend_version__
from .__version__ import __author__, __author_email__, __license__
from .__version__ import __copyright__

# Initialize with backend and setup module cleanup
from . import backend
import atexit

backend.jheaps_init()
del backend


def _module_cleanup_function():
    from . import backend

    backend.jheaps_cleanup()


atexit.register(_module_cleanup_function)
del atexit

# Set default logging handler to avoid "No handler found" warnings.
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())

from . import (
    types,
)

from ._internals._factories import (
    _HeapType,
    _create_and_wrap_heap,
    _create_and_wrap_dary_heap,
    _create_and_wrap_radix_heap,
)


def create_addressable_dary_heap(key_type=float, value_type=int, d=4, explicit=False):
    """Create an addressable d-ary heap.

    :param key_type: the key type
    :type key_type: float, int or object
    :param value_type: the value type
    :type value_type: float, int or object
    :param d: the degree of the d-ary heap
    :type d: int
    :param explicit: if True the heap is an actual tree, otherwise is it stored as an array
    :type explicit: boolean
    :returns: the heap
    :rtype: :py:class:`.AddressableHeap`
    """
    if explicit:
        heap_type = _HeapType.HEAP_TYPE_ADDRESSABLE_DARY_IMPLICIT
    else:
        heap_type = _HeapType.HEAP_TYPE_ADDRESSABLE_DARY_IMPLICIT

    return _create_and_wrap_dary_heap(
        heap_type,
        d,
        key_type,
        value_type=value_type,
        addressable=True,
        mergeable=False,
        double_ended=False,
    )


def create_implicit_dary_heap(key_type=float, d=4):
    """Create an implicit (array-based) d-ary heap.

    :param key_type: the key type
    :type key_type: float, int or object
    :param d: the degree of the d-ary heap
    :type d: int
    :returns: the heap
    :rtype: :py:class:`.Heap`
    """
    heap_type = _HeapType.HEAP_TYPE_DARY_IMPLICIT

    return _create_and_wrap_dary_heap(
        heap_type,
        d,
        key_type,
        value_type=None,
        addressable=False,
        mergeable=False,
        double_ended=False,
    )

def create_implicit_weak_binary_heap(key_type=float, bulk_insert=False):
    """Create an implicit (array-based) weak binary heap.

    :param key_type: the key type
    :type key_type: float, int or object
    :param bulk_insert: whether to use the variant which supports bulk insertion
    :type bulk_insert: boolean
    :returns: the heap
    :rtype: :py:class:`.Heap`
    """
    if bulk_insert:
        heap_type = _HeapType.HEAP_TYPE_BINARY_IMPLICIT_WEAK_BULKINSERT
    else:
        heap_type = _HeapType.HEAP_TYPE_BINARY_IMPLICIT_WEAK

    return _create_and_wrap_heap(
        heap_type,
        key_type,
        value_type=None,
        addressable=False,
        mergeable=False,
        double_ended=False,
    )


def create_implicit_binary_heap(key_type=float):
    """Create an implicit (array-based) binary heap.

    :param key_type: the key type
    :type key_type: float, int or object
    :returns: the heap
    :rtype: :py:class:`.Heap`
    """
    heap_type = _HeapType.HEAP_TYPE_BINARY_IMPLICIT

    return _create_and_wrap_heap(
        heap_type,
        key_type,
        value_type=None,
        addressable=False,
        mergeable=False,
        double_ended=False,
    )


def create_doublended_implicit_binary_heap(key_type=float): 
    """Create an implicit (array-based) binary MinMax heap.

    :param key_type: the key type
    :type key_type: float, int or object
    :returns: the heap
    :rtype: :py:class:`.DoubleEndedHeap`
    """
    heap_type = _HeapType.HEAP_TYPE_DOUBLEENDED_BINARY_IMPLICIT_MINMAX

    return _create_and_wrap_heap(
        heap_type,
        key_type,
        value_type=None,
        addressable=False,
        mergeable=False,
        double_ended=True,
    )


def create_addressable_binary_heap(key_type=float, value_type=int, explicit=False):
    """Create an addressable binary heap.

    :param key_type: the key type
    :type key_type: float, int or object
    :param value_type: the value type
    :type value_type: float, int or object
    :param explicit: if True the heap is an actual tree, otherwise is it stored as an array
    :type explicit: boolean
    :returns: the heap
    :rtype: :py:class:`.AddressableHeap`
    """
    if explicit:
        heap_type = _HeapType.HEAP_TYPE_ADDRESSABLE_BINARY_EXPLICIT
    else:
        heap_type = _HeapType.HEAP_TYPE_ADDRESSABLE_BINARY_IMPLICIT

    return _create_and_wrap_heap(
        heap_type,
        key_type,
        value_type,
        addressable=True,
        mergeable=False,
        double_ended=False,
    )


def create_doubleended_addressable_fibonacci_heap(key_type=float, value_type=int):
    """Create a double-ended Fibonacci heap using the reflected heaps technique.

    :param key_type: the key type
    :type key_type: float, int or object
    :param value_type: the value type
    :type value_type: float, int or object
    :returns: the heap
    :rtype: :py:class:`.DoubleEndedAddressableHeap` and :py:class:`.MergeableHeap`
    """
    heap_type = (
        _HeapType.HEAP_TYPE_DOUBLEENDED_MERGEABLE_ADDRESSABLE_FIBONACCI_REFLECTED
    )

    return _create_and_wrap_heap(
        heap_type,
        key_type,
        value_type,
        addressable=True,
        mergeable=True,
        double_ended=True,
    )
    pass


def create_addressable_fibonacci_heap(
    key_type=float,
    value_type=int,
    simple=False,
):
    """Create an addressable Fibonacci heap.

    :param key_type: the key type
    :type key_type: float, int or object
    :param value_type: the value type
    :type value_type: float, int or object
    :param simple: if true then the simple variant is returned, otherwise the classic
    :type simple: boolean
    :returns: the heap
    :rtype: :py:class:`.AddressableHeap` and :py:class:`.MergeableHeap`
    """
    heap_type = (
        _HeapType.HEAP_TYPE_MERGEABLE_ADDRESSABLE_FIBONACCI_SIMPLE
        if simple
        else _HeapType.HEAP_TYPE_MERGEABLE_ADDRESSABLE_FIBONACCI
    )

    return _create_and_wrap_heap(
        heap_type,
        key_type,
        value_type,
        addressable=True,
        mergeable=True,
        double_ended=False,
    )


def create_doubleended_addressable_pairing_heap(
    key_type=float, value_type=int, 
):
    """Create a double-ended pairing heap using the reflected heaps technique.

    :param key_type: the key type
    :type key_type: float, int or object
    :param value_type: the value type
    :type value_type: float, int or object
    :returns: the heap
    :rtype: :py:class:`.DoubleEndedAddressableHeap` and :py:class:`.MergeableHeap`    
    """
    heap_type = _HeapType.HEAP_TYPE_DOUBLEENDED_MERGEABLE_ADDRESSABLE_PAIRING_REFLECTED

    return _create_and_wrap_heap(
        heap_type,
        key_type,
        value_type,
        addressable=True,
        mergeable=True,
        double_ended=True,
    )


def create_addressable_pairing_heap(
    key_type=float, value_type=int, type=None, 
):
    """Create an addressable pairing heap. Different pairing heap 
    variants can be constructed using the parameter `type`. 

    :param key_type: the key type
    :type key_type: float, int or object
    :param value_type: the value type
    :type value_type: float, int or object
    :param type: the type of pairing heap to create
    :type type: None, 'rank' or 'costless_meld'
    :returns: the heap
    :rtype: :py:class:`.AddressableHeap` and :py:class:`.MergeableHeap`
    """
    if type == 'rank':
        heap_type = _HeapType.HEAP_TYPE_MERGEABLE_ADDRESSABLE_PAIRING_RANK
    elif type == 'costless_meld':
        heap_type = _HeapType.HEAP_TYPE_MERGEABLE_ADDRESSABLE_PAIRING_COSTLESSMELD
    else:
        heap_type = _HeapType.HEAP_TYPE_MERGEABLE_ADDRESSABLE_PAIRING

    return _create_and_wrap_heap(
        heap_type,
        key_type,
        value_type,
        addressable=True,
        mergeable=True,
        double_ended=False,
    )


def create_addressable_hollow_heap(key_type=float, value_type=int):
    """Create an addressable hollow heap.

    :param key_type: the key type
    :type key_type: float, int or object
    :param value_type: the value type
    :type value_type: float, int or object
    :returns: the heap
    :rtype: :py:class:`.AddressableHeap` and :py:class:`.MergeableHeap`
    """
    heap_type = _HeapType.HEAP_TYPE_MERGEABLE_ADDRESSABLE_HOLLOW

    return _create_and_wrap_heap(
        heap_type,
        key_type,
        value_type,
        addressable=True,
        mergeable=True,
        double_ended=False,
    )


def create_addressable_leftist_heap(key_type=float, value_type=int):
    """Create an addressable leftist heap.

    :param key_type: the key type
    :type key_type: float, int or object
    :param value_type: the value type
    :type value_type: float, int or object
    :returns: the heap
    :rtype: :py:class:`.AddressableHeap` and :py:class:`.MergeableHeap`
    """
    heap_type = _HeapType.HEAP_TYPE_MERGEABLE_ADDRESSABLE_LEFTIST

    return _create_and_wrap_heap(
        heap_type,
        key_type,
        value_type,
        addressable=True,
        mergeable=True,
        double_ended=False,
    )


def create_addressable_skew_heap(key_type=float, value_type=int):
    """Create an addressable skew heap.

    :param key_type: the key type
    :type key_type: float, int or object
    :param value_type: the value type
    :type value_type: float, int or object
    :returns: the heap
    :rtype: :py:class:`.AddressableHeap` and :py:class:`.MergeableHeap`
    """
    heap_type = _HeapType.HEAP_TYPE_MERGEABLE_ADDRESSABLE_SKEW

    return _create_and_wrap_heap(
        heap_type,
        key_type,
        value_type,
        addressable=True,
        mergeable=True,
        double_ended=False,
    )


def create_addressable_radix_heap(key_type=float, value_type=int, min=None, max=None):
    """Create an addressable radix heap. Radix heaps are monotone heaps
    stored using buckets. The key type can only be float or int. The number of
    buckets depends on the difference between the min and max values provided.

    :param key_type: the key type
    :type key_type: float or int
    :param value_type: the value type
    :type value_type: float, int or object
    :param min: minimum key value
    :type min: float or int depending on key_type
    :param max: maximum key value
    :type max: float or int depending on key_type
    :returns: the heap
    :rtype: :py:class:`.AddressableHeap`
    """
    if key_type == float:
        heap_type = _HeapType.HEAP_TYPE_MONOTONE_ADDRESSABLE_DOUBLE_RADIX
    elif key_type == int:
        heap_type = _HeapType.HEAP_TYPE_MONOTONE_ADDRESSABLE_LONG_RADIX
    else:
        raise ValueError("Radix heaps support float or int keys")

    if min is None:
        min = key_type()
    if not isinstance(min, key_type):
        raise TypeError("Min value not valid")

    if max is None:
        if key_type == float:
            max = float("0x1.fffffffffffffP+1023")
        elif key_type == int:
            max = int("0x7fffffff")
    if not isinstance(max, key_type):
        raise TypeError("Max value not valid")

    return _create_and_wrap_radix_heap(
        heap_type,
        min,
        max,
        key_type,
        value_type,
        addressable=True,
        mergeable=False,
        double_ended=False,
    )


def create_radix_heap(key_type=float, min=None, max=None):
    """Create a radix heap. Radix heaps are monotone heaps
    stored using buckets. The key type can only be float or int. The number of
    buckets depends on the difference between the min and max values provided.

    :param key_type: the key type
    :type key_type: float or int
    :param value_type: the value type
    :type value_type: float, int or object
    :param min: minimum key value
    :type min: float or int depending on key_type
    :param max: maximum key value
    :type max: float or int depending on key_type
    :returns: the heap
    :rtype: :py:class:`.Heap`
    """
    if key_type == float:
        heap_type = _HeapType.HEAP_TYPE_MONOTONE_DOUBLE_RADIX
    elif key_type == int:
        heap_type = _HeapType.HEAP_TYPE_MONOTONE_LONG_RADIX

    if min is None:
        min = key_type()
    if not isinstance(min, key_type):
        raise TypeError("Min value not valid")

    if max is None:
        if key_type == float:
            max = float("0x1.fffffffffffffP+1023")
        elif key_type == int:
            max = int("0x7fffffff")
    if not isinstance(max, key_type):
        raise TypeError("Max value not valid")

    return _create_and_wrap_radix_heap(
        heap_type,
        min,
        max,
        key_type,
        value_type=None,
        addressable=False,
        mergeable=False,
        double_ended=False,
    )
