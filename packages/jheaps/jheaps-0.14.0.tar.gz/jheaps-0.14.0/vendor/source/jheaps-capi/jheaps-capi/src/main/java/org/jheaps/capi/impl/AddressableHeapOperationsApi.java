/*
 * (C) Copyright 2020-2020, by Dimitrios Michail
 *
 * JHeaps Library
 * 
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * 
 * SPDX-License-Identifier: Apache-2.0
 */
package org.jheaps.capi.impl;

import org.graalvm.nativeimage.IsolateThread;
import org.graalvm.nativeimage.ObjectHandle;
import org.graalvm.nativeimage.ObjectHandles;
import org.graalvm.nativeimage.c.function.CEntryPoint;
import org.graalvm.nativeimage.c.type.CDoublePointer;
import org.graalvm.nativeimage.c.type.CIntPointer;
import org.graalvm.nativeimage.c.type.CLongPointer;
import org.graalvm.nativeimage.c.type.WordPointer;
import org.jheaps.AddressableHeap;
import org.jheaps.AddressableHeap.Handle;
import org.jheaps.capi.Constants;
import org.jheaps.capi.JHeapsContext.Status;
import org.jheaps.capi.error.StatusReturnExceptionHandler;

/**
 * Operations on addressable heaps.
 */
public class AddressableHeapOperationsApi {

	private static ObjectHandles globalHandles = ObjectHandles.getGlobal();

	/**
	 * Insert a double key with a value.
	 *
	 * @param thread     the thread isolate
	 * @param heapHandle the heap
	 * @param key        the key
	 * @param res        the new element handle
	 * @return status
	 */
	@CEntryPoint(name = Constants.LIB_PREFIX
			+ "AHeap_D_insert_key", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int insertDoubleKeyValue(IsolateThread thread, ObjectHandle heapHandle, double key, WordPointer res) {
		AddressableHeap<Double, Long> heap = globalHandles.get(heapHandle);
		Handle<Double, Long> handle = heap.insert(key, 0l);
		if (res.isNonNull()) {
			res.write(globalHandles.create(handle));
		}
		return Status.STATUS_SUCCESS.getCValue();
	}

	/**
	 * Insert a long key with a value.
	 *
	 * @param thread     the thread isolate
	 * @param heapHandle the heap
	 * @param key        the key
	 * @param res        the new element handle
	 * @return status
	 */
	@CEntryPoint(name = Constants.LIB_PREFIX
			+ "AHeap_L_insert_key", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int insertLongKeyValue(IsolateThread thread, ObjectHandle heapHandle, long key, WordPointer res) {
		AddressableHeap<Long, Long> heap = globalHandles.get(heapHandle);
		Handle<Long, Long> handle = heap.insert(key, 0l);
		if (res.isNonNull()) {
			res.write(globalHandles.create(handle));
		}
		return Status.STATUS_SUCCESS.getCValue();
	}

	/**
	 * Insert a double key with a value.
	 *
	 * @param thread     the thread isolate
	 * @param heapHandle the heap
	 * @param key        the key
	 * @param long       the value
	 * @param res        the new element handle
	 * @return status
	 */
	@CEntryPoint(name = Constants.LIB_PREFIX
			+ "AHeap_D_insert_key_value", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int insertDoubleKeyValue(IsolateThread thread, ObjectHandle heapHandle, double key, long value,
			WordPointer res) {
		AddressableHeap<Double, Long> heap = globalHandles.get(heapHandle);
		Handle<Double, ?> handle = heap.insert(key, value);
		if (res.isNonNull()) {
			res.write(globalHandles.create(handle));
		}
		return Status.STATUS_SUCCESS.getCValue();
	}

	/**
	 * Insert a long key with a value.
	 *
	 * @param thread     the thread isolate
	 * @param heapHandle the heap
	 * @param key        the key
	 * @param long       the value
	 * @param res        the new element handle
	 * @return status
	 */
	@CEntryPoint(name = Constants.LIB_PREFIX
			+ "AHeap_L_insert_key_value", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int insertLongKeyValue(IsolateThread thread, ObjectHandle heapHandle, long key, long value,
			WordPointer res) {
		AddressableHeap<Long, Long> heap = globalHandles.get(heapHandle);
		Handle<Long, ?> handle = heap.insert(key, value);
		if (res.isNonNull()) {
			res.write(globalHandles.create(handle));
		}
		return Status.STATUS_SUCCESS.getCValue();
	}

	/**
	 * Find minimum
	 *
	 * @param thread     the thread isolate
	 * @param heapHandle the heap
	 * @param res        the element handle
	 * @return status
	 */
	@CEntryPoint(name = Constants.LIB_PREFIX + "AHeap_find_min", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int findMin(IsolateThread thread, ObjectHandle heapHandle, WordPointer res) {
		AddressableHeap<?, ?> heap = globalHandles.get(heapHandle);
		Handle<?, ?> handle = heap.findMin();
		if (res.isNonNull()) {
			res.write(globalHandles.create(handle));
		}
		return Status.STATUS_SUCCESS.getCValue();
	}

	/**
	 * Delete minimum
	 *
	 * @param thread     the thread isolate
	 * @param heapHandle the heap
	 * @param res        the element handle
	 * @return status
	 */
	@CEntryPoint(name = Constants.LIB_PREFIX
			+ "AHeap_delete_min", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int deleteMin(IsolateThread thread, ObjectHandle heapHandle, WordPointer res) {
		AddressableHeap<?, ?> heap = globalHandles.get(heapHandle);
		Handle<?, ?> handle = heap.deleteMin();
		if (res.isNonNull()) {
			res.write(globalHandles.create(handle));
		}
		return Status.STATUS_SUCCESS.getCValue();
	}

	@CEntryPoint(name = Constants.LIB_PREFIX + "AHeap_size", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int size(IsolateThread thread, ObjectHandle heapHandle, CLongPointer res) {
		AddressableHeap<?, ?> heap = globalHandles.get(heapHandle);
		if (res.isNonNull()) {
			res.write(heap.size());
		}
		return Status.STATUS_SUCCESS.getCValue();
	}

	@CEntryPoint(name = Constants.LIB_PREFIX + "AHeap_isempty", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int isEmpty(IsolateThread thread, ObjectHandle heapHandle, CIntPointer res) {
		AddressableHeap<?, ?> heap = globalHandles.get(heapHandle);
		if (res.isNonNull()) {
			res.write(heap.isEmpty() ? 1 : 0);
		}
		return Status.STATUS_SUCCESS.getCValue();
	}

	@CEntryPoint(name = Constants.LIB_PREFIX + "AHeap_clear", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int clear(IsolateThread thread, ObjectHandle heapHandle) {
		AddressableHeap<?, ?> heap = globalHandles.get(heapHandle);
		heap.clear();
		return Status.STATUS_SUCCESS.getCValue();
	}

	/**
	 * Get a double key from a handle
	 *
	 * @param thread the thread isolate
	 * @param handle the heap handle handle
	 * @param res    the key
	 * @return status
	 */
	@CEntryPoint(name = Constants.LIB_PREFIX
			+ "AHeapHandle_D_get_key", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int handleGetDoubleKey(IsolateThread thread, ObjectHandle handle, CDoublePointer res) {
		AddressableHeap.Handle<Double, ?> h = globalHandles.get(handle);
		if (res.isNonNull()) {
			res.write(h.getKey());
		}
		return Status.STATUS_SUCCESS.getCValue();
	}

	/**
	 * Get a long key from a handle
	 *
	 * @param thread the thread isolate
	 * @param handle the heap handle handle
	 * @param res    the key
	 * @return status
	 */
	@CEntryPoint(name = Constants.LIB_PREFIX
			+ "AHeapHandle_L_get_key", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int handleGetLongKey(IsolateThread thread, ObjectHandle handle, CLongPointer res) {
		AddressableHeap.Handle<Long, ?> h = globalHandles.get(handle);
		if (res.isNonNull()) {
			res.write(h.getKey());
		}
		return Status.STATUS_SUCCESS.getCValue();
	}

	/**
	 * Get the value from a handle
	 *
	 * @param thread the thread isolate
	 * @param handle the heap handle handle
	 * @param res    the value
	 * @return status
	 */
	@CEntryPoint(name = Constants.LIB_PREFIX
			+ "AHeapHandle_get_value", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int handleGetValue(IsolateThread thread, ObjectHandle handle, CLongPointer res) {
		AddressableHeap.Handle<?, Long> h = globalHandles.get(handle);
		if (res.isNonNull()) {
			res.write(h.getValue());
		}
		return Status.STATUS_SUCCESS.getCValue();
	}

	/**
	 * Set the value of a handle
	 *
	 * @param thread the thread isolate
	 * @param handle the heap handle handle
	 * @param value  the new value
	 * @param res    the key
	 * @return status
	 */
	@CEntryPoint(name = Constants.LIB_PREFIX
			+ "AHeapHandle_set_value", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int handleSetValue(IsolateThread thread, ObjectHandle handle, long value) {
		AddressableHeap.Handle<?, Long> h = globalHandles.get(handle);
		h.setValue(value);
		return Status.STATUS_SUCCESS.getCValue();
	}

	/**
	 * Decrease a double key of a handle
	 *
	 * @param thread the thread isolate
	 * @param handle the heap handle handle
	 * @param key    the new key
	 * @return status
	 */
	@CEntryPoint(name = Constants.LIB_PREFIX
			+ "AHeapHandle_D_decrease_key", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int handleDecreaseDoubleKey(IsolateThread thread, ObjectHandle handle, double key) {
		AddressableHeap.Handle<Double, ?> h = globalHandles.get(handle);
		h.decreaseKey(key);
		return Status.STATUS_SUCCESS.getCValue();
	}

	/**
	 * Decrease a long key of a handle
	 *
	 * @param thread the thread isolate
	 * @param handle the heap handle handle
	 * @param key    the new key
	 * @return status
	 */
	@CEntryPoint(name = Constants.LIB_PREFIX
			+ "AHeapHandle_L_decrease_key", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int handleDecreaseLongKey(IsolateThread thread, ObjectHandle handle, long key) {
		AddressableHeap.Handle<Long, ?> h = globalHandles.get(handle);
		h.decreaseKey(key);
		return Status.STATUS_SUCCESS.getCValue();
	}

	/**
	 * Delete an element from the queue
	 *
	 * @param thread the thread isolate
	 * @param handle the heap handle handle
	 * @return status
	 */
	@CEntryPoint(name = Constants.LIB_PREFIX
			+ "AHeapHandle_delete", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int handleDelete(IsolateThread thread, ObjectHandle handle) {
		AddressableHeap.Handle<?, ?> h = globalHandles.get(handle);
		h.delete();
		return Status.STATUS_SUCCESS.getCValue();
	}

}
