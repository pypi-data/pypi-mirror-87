# -*- coding: utf-8 -*-

"""
Fibonacci Heap
==============

In this example we create a Fibonacci heap.
"""

# %%
# Start by importing the package.

import jheaps

# %%
# Create the pairing heap using the following factory method. By default all
# addressable heaps have `float` keys and `int` values. This can be adjusted by 
# parameters `key_type` and `value_type` in the factory method which can take 
# values `float`, `int`, `object`.

heap = jheaps.create_addressable_fibonacci_heap()

# %%
# Adding elements can be performed using insert. We next add an element with key 
# equal to 3.14 and value 100. Moreover, we add a few more elements.

heap.insert(3.14, 100)

for i in range(1, 100):
    heap.insert(i, 1000+i)

# %%
# Now our heap has 100 elements.

print ('Total elements so far: {}'.format(len(heap)))


# %%
# If we never need to refer to that element, except from possible accessing it when 
# its key is minimum in the heap, we are done. Otherwise, when inserting an element we 
# are presented with a `handle` which we can later use to refer to that particular element.

handle1 = heap.insert(15.3, 200)

# %% 
# Using the handle we can print the key and value of the element

print('key: {}, value: {}'.format(handle1.key, handle1.value))

# %%
# We can also adjust its value

handle1.value = 250
print('key: {}, value: {}'.format(handle1.key, handle1.value))

# %%
# Adjusting the key is more limited as we can only increase an element's priority, thus decrease
# its key. We next find the minimum element in the heap and make the element referred by 
# `handle1` as the new minimum.

cur_min_key = heap.find_min().key
handle1.decrease_key(cur_min_key - 1.0)
print('key: {}, value: {}'.format(handle1.key, handle1.value))

# %%
# Method `find_min` returns a handle to the current minimum element. 

handle2 = heap.find_min()
print('key: {}, value: {}'.format(handle2.key, handle2.value))

# %%
# Method `delete_min` deletes the minimum element and returns a handle. Be 
# careful with that handle as it allows you to read the key and read/write the
# value but calling any other method (such as `decrease_key` or `delete`) on that handle
# will raise an error.

handle3 = heap.delete_min()
print('key: {}, value: {}'.format(handle3.key, handle3.value))

# %% 
# Except from decreasing the key, handles are also useful when we want to delete an element 
# which is not the element with the minimum key. We next insert an element and then remove it.
# 

print('Size of heap before insertion: {}'.format(len(heap)))
handle4 = heap.insert(50.5, 103)
print('Size of heap after insertion: {}'.format(len(heap)))
handle4.delete()
print('Size of heap after deletion: {}'.format(len(heap)))

# %% 
# Clearing the heap can be done using method `clear`.

heap.clear()

print('Size of heap: {}'.format(len(heap)))
print('Heap is empty: {}'.format(heap.is_empty()))
