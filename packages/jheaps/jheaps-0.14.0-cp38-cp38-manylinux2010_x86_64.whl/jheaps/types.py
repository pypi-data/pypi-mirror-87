from abc import ABC, abstractmethod
from collections.abc import Mapping

from .backend import HeapType


class AddressableHeapHandle(ABC):
    """Interface for an addressable heap handle."""

    @property
    @abstractmethod
    def key(self):
        """Get the key

        :returns: the key
        """
        pass

    @property
    @abstractmethod
    def value(self):
        """Get the value

        :returns: the value
        """
        pass

    @value.setter
    @abstractmethod
    def value(self, v):
        """Set the value

        :param v: the new value
        """
        pass

    @abstractmethod
    def decrease_key(self, key):
        """Decrease the key of the element represented by
        this handle.

        :param key: the new key
        """
        pass

    @abstractmethod
    def delete(self):
        """Delete an element."""
        pass


class AddressableHeap(ABC):
    """Interface for an addressable heap."""

    @abstractmethod
    def find_min(self):
        """Return a handle for the minimum element.

        :rtype: :class:`.AddressableHeapHandle`
        """
        pass

    @abstractmethod
    def delete_min(self):
        """Delete the minimum element and return a
        handle. The handle can be used to access the key
        or value but not to perform any other operation.

        :rtype: :class:`.AddressableHeapHandle`
        """
        pass

    @abstractmethod
    def is_empty(self):
        """Check if the heap is empty.

        :returns: whether the heap is empty or not
        :rtype: boolean
        """
        pass

    @abstractmethod
    def clear(self):
        """Clear the heap"""
        pass

    @abstractmethod
    def __len__(self):
        """Return the number of elements in the heap.
        :returns: the number of elements in the heap
        :rtype: long integer
        """
        pass

    @abstractmethod
    def insert(self, key, value):
        """Insert a new element.

        :param key: the key
        :param value: the value
        :type value: long integer
        :returns: a handle for the new element
        :rtype: :class:`.AddressableHeapHandle`
        """
        pass


class DoubleEndedAddressableHeapHandle(AddressableHeapHandle):
    """Interface for a double ended addressable heap handle."""

    @abstractmethod
    def increase_key(self, key):
        """Increase the key of the element represented by
        this handle.

        :param key: the new key
        """
        pass


class DoubleEndedAddressableHeap(AddressableHeap):
    """Interface for an double ended addressable heap."""
    
    @abstractmethod
    def find_min(self):
        """Return a handle for the minimum element.

        :rtype: :py:class:`.DoubleEndedAddressableHeapHandle`
        """
        pass

    @abstractmethod
    def delete_min(self):
        """Delete the minimum element and return a
        handle. The handle can be used to access the key
        or value but not to perform any other operation.

        :rtype: :class:`.DoubleEndedAddressableHeapHandle`
        """
        pass

    @abstractmethod
    def insert(self, key, value):
        """Insert a new element.

        :param key: the key
        :param value: the value
        :type value: long integer
        :returns: a handle for the new element
        :rtype: :class:`.DoubleEndedAddressableHeapHandle`
        """
        pass

    @abstractmethod
    def find_max(self):
        """Return a handle for the maximum element.

        :rtype: :class:`.DoubleEndedAddressableHeapHandle`
        """
        pass

    @abstractmethod
    def delete_max(self):
        """Delete the minimum element and return a
        handle. The handle can be used to access the key
        or value but not to perform any other operation.

        :rtype: :class:`.DoubledEndedAddressableHeapHandle`
        """
        pass


class MergeableHeap(ABC):
    """Interface for a mergeable heap."""

    @abstractmethod
    def meld(self, other):
        """Meld heap other into the current heap. After the meld
        operation the heap `other` is not usable.
        """
        pass


class Heap(ABC):
    """Interface for a heap."""

    @abstractmethod
    def find_min(self):
        """Return the minimum key."""
        pass

    @abstractmethod
    def delete_min(self):
        """Delete the minimum element and return its key."""
        pass

    @abstractmethod
    def is_empty(self):
        """Check if the heap is empty.

        :returns: whether the heap is empty or not
        :rtype: boolean
        """
        pass

    @abstractmethod
    def clear(self):
        """Clear the heap"""
        pass

    @abstractmethod
    def __len__(self):
        """Return the number of elements in the heap.

        :returns: the number of elements in the heap
        :rtype: long integer
        """
        pass

    @abstractmethod
    def insert(self, key):
        """Insert a new element.

        :param key: the key
        """
        pass


class DoubleEndedHeap(Heap):
    """Interface for a double ended heap."""

    @abstractmethod
    def find_max(self):
        """Return the maximum key."""
        pass

    @abstractmethod
    def delete_max(self):
        """Delete the maximum element and return its key."""
        pass
