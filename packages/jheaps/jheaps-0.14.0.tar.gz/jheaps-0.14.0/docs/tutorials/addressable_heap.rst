.. _tutorials/addressable_heap:

.. currentmodule:: jheaps

Addressable Heap
================

The most classic addressable heap is the Fibonacci, so let us create one.

Creating an addressable heap
----------------------------

If not explicitly provided otherwise the heap will have `float` keys and `int` values.

.. nbplot::

  >>> import jheaps
  >>> fibo = jheaps.create_addressable_fibonacci_heap()

Inserting Elements
------------------

Now that we have a new heap we can start adding elements. When inserting an element 
in an addressable heap, you get back a handle which can later be used in order to 
perform operations on the element, such as decreasing the key (increasing the 
priority of the element) or deleting it from the heap.

.. nbplot::

  >>> handle1 = fibo.insert(5.5, 1)
  >>> handle2 = fibo.insert(100.5, 2)
  >>> handle3 = fibo.insert(3.3, 3)
  >>> handle4 = fibo.insert(52.3, 4)
  >>> handle5 = fibo.insert(30.0, 5)

Element key-value
-----------------

The key and the value can be read directly using properties 
:py:attr:`.AddressableHeapHandle.key` and :py:attr:`.AddressableHeapHandle.value`
from the handle. 

.. nbplot::

  >>> print('Key: {}'.format(handle1.key))
  >>> print('Value: {}'.format(handle1.value))

Values can also directly be changed. 

.. nbplot::

  >>> handle1.value = 15

As keys can only be decreased, we provide a dedicated method for this,  
:py:meth:`.AddressableHeapHandle.decrease_key`. 

.. nbplot::

  >>> handle1.decrease_key(4.5)

Inspecting the size of the heap
-------------------------------

The number of elements in the heap can be found using: 

.. nbplot::

  >>> print(len(fibo))

Method :py:meth:`.AddressableHeap.is_empty` can be used to check if the heap is 
empty.

.. nbplot::

  >>> fibo.is_empty()

Finding the element with the minimum key
----------------------------------------

A handle to the element with the minimum key can be acquired using:

.. nbplot::

  >>> handle6 = fibo.find_min()

Deleting the element with the minimum key
-----------------------------------------

The element with the minimum key can be removed from the heap using:

.. nbplot::

  >>> handle7 = fibo.delete_min()

The returned handle can only be used for accessing the properties 
:py:attr:`.AddressableHeapHandle.key` and :py:attr:`.AddressableHeapHandle.value`. 
Calling any other method on the handle will raise an exception.

Deleting elements
-----------------

Searching in heaps is not possible, but elements can be deleted from corresponding
handle. Thus, the user can use some external indexing mechanism in order to keep 
track of handles. Given a handle use 

.. nbplot::

  >>> handle4.delete()

to delete the element from the heap. Again after deletion you can only access the 
key and value from the handle, but all other methods raise exceptions.


Increasing the priority of an element
-------------------------------------

Sometimes we want to increase the priority of an element in the heap (recall how 
Dijkstra's algorithm works). This can be performed using the handle by calling 
method :py:meth:`.AddressableHeapHandle.decrease_key`. 

.. nbplot::

  >>> handle2.decrease_key(1.5)

Clearing the heap
-----------------

All elements of the heap can be removed by using method :py:meth:`.AddressableHeap.clear`.

.. nbplot::

  >>> fibo.clear()

