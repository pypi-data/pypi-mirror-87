from .. import backend

from ..types import (
    HeapType as _HeapType,
)

from ._heaps import (
    _DoubleHeap,
    _LongHeap,
    _AnyHeap,
    _DoubleEndedDoubleHeap,
    _DoubleEndedLongHeap,
    _DoubleEndedAnyHeap,
)

from ._addressable_heaps import (
    _DoubleLongAddressableHeap,
    _DoubleEndedDoubleLongAddressableHeap,
    _DoubleLongMergeableAddressableHeap,
    _DoubleEndedDoubleLongMergeableAddressableHeap,
    _LongLongAddressableHeap,
    _DoubleEndedLongLongAddressableHeap,
    _LongLongMergeableAddressableHeap,
    _DoubleEndedLongLongMergeableAddressableHeap,
)

from ._addressable_any_heaps import (
    _DoubleAnyAddressableHeap,
    _DoubleEndedDoubleAnyAddressableHeap,
    _DoubleAnyMergeableAddressableHeap,
    _DoubleEndedDoubleAnyMergeableAddressableHeap,
    _LongAnyAddressableHeap,
    _DoubleEndedLongAnyAddressableHeap,
    _LongAnyMergeableAddressableHeap,
    _DoubleEndedLongAnyMergeableAddressableHeap,
    _AnyLongAddressableHeap,
    _DoubleEndedAnyLongAddressableHeap,
    _AnyLongMergeableAddressableHeap,
    _DoubleEndedAnyLongMergeableAddressableHeap,
    _AnyAnyAddressableHeap,
    _DoubleEndedAnyAnyAddressableHeap,
    _AnyAnyMergeableAddressableHeap,
    _DoubleEndedAnyAnyMergeableAddressableHeap,
)

from ._utils import (
    _id_comparator,
    _create_wrapped_id_comparator_callback,
)

import ctypes


def _wrap_heap(
    handle,
    key_type=float,
    value_type=int,
    comparator=None,
    addressable=True,
    mergeable=False,
    double_ended=False,
):
    if addressable:
        if double_ended:
            if mergeable:
                if key_type == float:
                    if value_type == int:
                        return _DoubleEndedDoubleLongMergeableAddressableHeap(handle)
                    else:
                        return _DoubleEndedDoubleAnyMergeableAddressableHeap(handle)
                elif key_type == int:
                    if value_type == int:
                        return _DoubleEndedLongLongMergeableAddressableHeap(handle)
                    else:
                        return _DoubleEndedLongAnyMergeableAddressableHeap(handle)
                else:
                    if value_type == int:
                        return _DoubleEndedAnyLongMergeableAddressableHeap(
                            handle, comparator=comparator
                        )
                    else:
                        return _DoubleEndedAnyAnyMergeableAddressableHeap(
                            handle, comparator=comparator
                        )
            else:
                if key_type == float:
                    if value_type == int:
                        return _DoubleEndedDoubleLongAddressableHeap(handle)
                    else:
                        return _DoubleEndedDoubleAnyAddressableHeap(handle)
                elif key_type == int:
                    if value_type == int:
                        return _DoubleEndedLongLongAddressableHeap(handle)
                    else:
                        return _DoubleEndedLongAnyAddressableHeap(handle)
                else:
                    if value_type == int:
                        return _DoubleEndedAnyLongAddressableHeap(
                            handle, comparator=comparator
                        )
                    else:
                        return _DoubleEndedAnyAnyAddressableHeap(
                            handle, comparator=comparator
                        )
        else:
            if mergeable:
                if key_type == float:
                    if value_type == int:
                        return _DoubleLongMergeableAddressableHeap(handle)
                    else:
                        return _DoubleAnyMergeableAddressableHeap(handle)
                elif key_type == int:
                    if value_type == int:
                        return _LongLongMergeableAddressableHeap(handle)
                    else:
                        return _LongAnyMergeableAddressableHeap(handle)
                else:
                    if value_type == int:
                        return _AnyLongMergeableAddressableHeap(
                            handle, comparator=comparator
                        )
                    else:
                        return _AnyAnyMergeableAddressableHeap(
                            handle, comparator=comparator
                        )
            else:
                if key_type == float:
                    if value_type == int:
                        return _DoubleLongAddressableHeap(handle)
                    else:
                        return _DoubleAnyAddressableHeap(handle)
                elif key_type == int:
                    if value_type == int:
                        return _LongLongAddressableHeap(handle)
                    else:
                        return _LongAnyAddressableHeap(handle)
                else:
                    if value_type == int:
                        return _AnyLongAddressableHeap(handle, comparator=comparator)
                    else:
                        return _AnyAnyAddressableHeap(handle, comparator=comparator)
    else:
        if double_ended:
            if key_type == float:
                return _DoubleEndedDoubleHeap(handle)
            elif key_type == int:
                return _DoubleEndedLongHeap(handle)
            else:
                return _DoubleEndedAnyHeap(handle, comparator=comparator)
        else:
            if key_type == float:
                return _DoubleHeap(handle)
            elif key_type == int:
                return _LongHeap(handle)
            else:
                return _AnyHeap(handle, comparator=comparator)


def _create_and_wrap_heap(
    heap_type, key_type, value_type, addressable, mergeable, double_ended
):
    if key_type != int and key_type != float:
        f_ptr, f = _create_wrapped_id_comparator_callback(_id_comparator)
        handle = backend.jheaps_Heap_comparator_create(heap_type.value, f_ptr)
        return _wrap_heap(
            handle,
            key_type,
            value_type,
            comparator=f,
            addressable=addressable,
            mergeable=mergeable,
            double_ended=double_ended,
        )
    else:
        handle = backend.jheaps_Heap_create(heap_type.value)
        return _wrap_heap(
            handle,
            key_type,
            value_type,
            addressable=addressable,
            mergeable=mergeable,
            double_ended=double_ended,
        )


def _create_and_wrap_dary_heap(
    heap_type, d, key_type, value_type, addressable, mergeable, double_ended
):
    if key_type != int and key_type != float:
        f_ptr, f = _create_wrapped_id_comparator_callback(_id_comparator)
        handle = backend.jheaps_dary_Heap_comparator_create(heap_type.value, f_ptr, d)
        return _wrap_heap(
            handle,
            key_type,
            value_type,
            comparator=f,
            addressable=addressable,
            mergeable=mergeable,
            double_ended=double_ended,
        )
    else:
        handle = backend.jheaps_dary_Heap_create(heap_type.value, d)
        return _wrap_heap(
            handle,
            key_type,
            value_type,
            addressable=addressable,
            mergeable=mergeable,
            double_ended=double_ended,
        )


def _create_and_wrap_radix_heap(
    heap_type, min, max, key_type, value_type, addressable, mergeable, double_ended
):
    if key_type == float:
        handle = backend.jheaps_double_radix_Heap_create(heap_type, min, max)
        return _wrap_heap(
            handle,
            key_type,
            value_type,
            addressable=addressable,
            mergeable=mergeable,
            double_ended=double_ended,
        )
    elif key_type == int:
        handle = backend.jheaps_long_radix_Heap_create(heap_type, min, max)
        return _wrap_heap(
            handle,
            key_type,
            value_type,
            addressable=addressable,
            mergeable=mergeable,
            double_ended=double_ended,
        )
    else:
        raise ValueError("Key type can only be float or int")
