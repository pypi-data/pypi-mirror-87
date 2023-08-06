
.. _heap_factories:

Heap Factories
**************

.. currentmodule:: jheaps

Creating heaps can be accomplished using factory methods. Heaps are based on two main 
categories depending on whether they are addressable or not. Addressable heaps follow the
:py:class:`.AddressableHeap` interface and support the addition of key-value pairs 
while classic heaps use the :py:class:`.Heap` interface and support only keys.

Both keys and values (when applicable) can have different types. Native support and therefore 
better performance is provided for `float` and `int` keys or values. All other types are 
represented using `object` and thus entail additional overhead. When keys are objects, comparisons 
are performed using `__lt__` and `__eq__`.  Note that `float` and `int` are translated to 
`double` and `long long` in the backend which means that they do not use arbitrary precision
arithmetic. Use `object` in order to handle arbitrary keys and values.

Additionally several addressable heaps are also mergeable heaps following the 
:py:class:`.Mergeable` interface and thus efficiently support melding with another heap. Note, however,
that after a meld one of the two heaps becomes unusable. Finally, performing cascading melds 
although efficient due to the use of union-find with path compression, invalidates the claimed bounds.

AddressableHeaps
^^^^^^^^^^^^^^^^

Depending on the given parameters different types of heaps can be represented. All heaps
returned by the following functions are instances of :py:class:`.AddressableHeap`.

.. autofunction:: jheaps.create_addressable_dary_heap

.. autofunction:: jheaps.create_addressable_binary_heap

.. autofunction:: jheaps.create_addressable_fibonacci_heap

.. autofunction:: jheaps.create_addressable_pairing_heap

.. autofunction:: jheaps.create_addressable_hollow_heap

.. autofunction:: create_addressable_radix_heap

Heaps
^^^^^

Depending on the given parameters different types of heaps can be represented. All heaps
returned by the following functions are instances of :py:class:`.Heap`.

.. autofunction:: jheaps.create_implicit_dary_heap

.. autofunction:: jheaps.create_implicit_weak_binary_heap

.. autofunction:: jheaps.create_implicit_binary_heap

.. autofunction:: jheaps.create_radix_heap

