from .. import backend

from ..types import (
    Heap, 
    DoubleEndedHeap,
)
from ._wrappers import _HandleWrapper

from ._utils import (
    _inc_ref,
    _dec_ref_by_id,
    _id_to_obj,
)

class _BaseHeap(_HandleWrapper, Heap): 
    """A Heap. All operations are delegated to the backend.
    """
    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def clear(self):
        backend.jheaps_Heap_clear(self._handle)

    def __len__(self):
        return backend.jheaps_Heap_size(self._handle)

    def is_empty(self):
        return backend.jheaps_Heap_isempty(self._handle)

    def __repr__(self):
        return "_BaseHeap(%r)" % self._handle


class _DoubleHeap(_BaseHeap): 
    """A Heap with floating point keys. All operations are delegated to the backend.
    """
    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def insert(self, key):
        backend.jheaps_Heap_D_insert_key(self._handle, key)

    def find_min(self):
        return backend.jheaps_Heap_D_find_min(self._handle)

    def delete_min(self):
        return backend.jheaps_Heap_D_delete_min(self._handle)

    def __repr__(self):
        return "_DoubleHeap(%r)" % self._handle


class _DoubleEndedDoubleHeap(_DoubleHeap, DoubleEndedHeap): 
    """A double ended heap with floating point keys.
    """
    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def find_max(self):
        return backend.jheaps_DEHeap_D_find_max(self._handle)

    def delete_max(self):
        return backend.jheaps_DEHeap_D_delete_max(self._handle)

    def __repr__(self):
        return "_DoubleEndedDoubleHeap(%r)" % self._handle


class _LongHeap(_BaseHeap): 
    """A Heap with long integer keys. All operations are delegated to the backend.
    """
    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def insert(self, key):
        backend.jheaps_Heap_L_insert_key(self._handle, key)

    def find_min(self):
        return backend.jheaps_Heap_L_find_min(self._handle)

    def delete_min(self):
        return backend.jheaps_Heap_L_delete_min(self._handle)

    def __repr__(self):
        return "_LongHeap(%r)" % self._handle


class _DoubleEndedLongHeap(_LongHeap, DoubleEndedHeap): 
    """A double ended heap with long integer keys.
    """
    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def find_max(self):
        return backend.jheaps_DEHeap_L_find_max(self._handle)

    def delete_max(self):
        return backend.jheaps_DEHeap_L_delete_max(self._handle)

    def __repr__(self):
        return "_DoubleEndedLongHeap(%r)" % self._handle


class _AnyHeap(_BaseHeap): 
    """A Heap with any hashable keys. All operations are delegated to the backend.
    """
    def __init__(self, handle, comparator, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._comparator=comparator

    def insert(self, key):
        _inc_ref(key)
        backend.jheaps_Heap_L_insert_key(self._handle, id(key))

    def find_min(self):
        key_id = backend.jheaps_Heap_L_find_min(self._handle)
        return _id_to_obj(key_id)

    def delete_min(self):
        key_id = backend.jheaps_Heap_L_delete_min(self._handle)
        _dec_ref_by_id(key_id)
        return _id_to_obj(key_id)

    def clear(self):
        # Clean one by one in order to decrease reference counts
        while not self.is_empty():
            key_id = backend.jheaps_Heap_L_delete_min(self._handle)
            _dec_ref_by_id(key_id)

    def __repr__(self):
        return "_AnyHeap(%r)" % self._handle


class _DoubleEndedAnyHeap(_AnyHeap, DoubleEndedHeap): 
    """A double ended heap with any hashable keys.
    """
    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def find_max(self):
        key_id = backend.jheaps_DEHeap_L_find_max(self._handle)
        return _id_to_obj(key_id)

    def delete_max(self):
        key_id = backend.jheaps_DEHeap_L_delete_max(self._handle)
        _dec_ref_by_id(key_id)
        return _id_to_obj(key_id)

    def __repr__(self):
        return "_DoubleEndedAnyHeap(%r)" % self._handle
