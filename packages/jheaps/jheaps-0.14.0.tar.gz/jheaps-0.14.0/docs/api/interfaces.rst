
.. _interfaces:

Interfaces
**********

.. currentmodule:: jheaps

AddressableHeap
^^^^^^^^^^^^^^^

The main interface of the library is the :class:`AddressableHeap <jheaps.types.AddressableHeap>`.
Addressable heaps support key-value pairs. After an insertion the user get a handle which she
can later use in order to increase the priority of the element (decrease-key), change the value 
or delete the element completely from the heap.

.. autoclass:: jheaps.types.AddressableHeap
   :inherited-members:
   :members:

.. autoclass:: jheaps.types.AddressableHeapHandle
   :inherited-members:
   :members:

MergeableHeap
^^^^^^^^^^^^^

Most addressable heaps are also mergeable.

.. autoclass:: jheaps.types.MergeableHeap
   :inherited-members:
   :members:

DoubleEndedAddressableHeap
^^^^^^^^^^^^^^^^^^^^^^^^^^

The library also contains a few double ended addressable heaps which are also mergeable.

.. autoclass:: jheaps.types.DoubleEndedAddressableHeap
   :inherited-members:
   :members:

.. autoclass:: jheaps.types.DoubleEndedAddressableHeapHandle
   :inherited-members:
   :members:   

Heap
^^^^

A simpler interface is also supported for heaps which are not addressable. In this simpler 
interface, values are not supported.

.. autoclass:: jheaps.types.Heap
   :inherited-members:
   :members:

DoubleEndedHeap
^^^^^^^^^^^^^^^

Support is also provided for double ended heaps (minmax).

.. autoclass:: jheaps.types.DoubleEndedHeap
   :inherited-members:
   :members:

