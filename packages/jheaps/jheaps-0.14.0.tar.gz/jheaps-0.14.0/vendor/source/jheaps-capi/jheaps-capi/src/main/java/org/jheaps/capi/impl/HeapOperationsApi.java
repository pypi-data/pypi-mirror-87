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
import org.jheaps.Heap;
import org.jheaps.capi.Constants;
import org.jheaps.capi.JHeapsContext.Status;
import org.jheaps.capi.error.StatusReturnExceptionHandler;

/**
 * Operations on addressable heaps.
 */
public class HeapOperationsApi {

	private static ObjectHandles globalHandles = ObjectHandles.getGlobal();

	/**
	 * Insert a double key with a value.
	 *
	 * @param thread     the thread isolate
	 * @param heapHandle the heap
	 * @param key        the key
	 * @return status
	 */
	@CEntryPoint(name = Constants.LIB_PREFIX
			+ "Heap_D_insert_key", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int insertDouble(IsolateThread thread, ObjectHandle heapHandle, double key) {
		Heap<Double> heap = globalHandles.get(heapHandle);
		heap.insert(key);
		return Status.STATUS_SUCCESS.getCValue();
	}

	/**
	 * Insert a long key with a value.
	 *
	 * @param thread     the thread isolate
	 * @param heapHandle the heap
	 * @param key        the key
	 * @return status
	 */
	@CEntryPoint(name = Constants.LIB_PREFIX
			+ "Heap_L_insert_key", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int insertLong(IsolateThread thread, ObjectHandle heapHandle, long key) {
		Heap<Long> heap = globalHandles.get(heapHandle);
		heap.insert(key);
		return Status.STATUS_SUCCESS.getCValue();
	}

	/**
	 * Find minimum
	 *
	 * @param thread     the thread isolate
	 * @param heapHandle the heap
	 * @param res        the element
	 * @return status
	 */
	@CEntryPoint(name = Constants.LIB_PREFIX + "Heap_D_find_min", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int findDoubleMin(IsolateThread thread, ObjectHandle heapHandle, CDoublePointer res) {
		Heap<Double> heap = globalHandles.get(heapHandle);
		if (res.isNonNull()) {
			res.write(heap.findMin());
		}
		return Status.STATUS_SUCCESS.getCValue();
	}

	/**
	 * Find minimum
	 *
	 * @param thread     the thread isolate
	 * @param heapHandle the heap
	 * @param res        the element
	 * @return status
	 */
	@CEntryPoint(name = Constants.LIB_PREFIX + "Heap_L_find_min", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int findLongMin(IsolateThread thread, ObjectHandle heapHandle, CLongPointer res) {
		Heap<Long> heap = globalHandles.get(heapHandle);
		if (res.isNonNull()) {
			res.write(heap.findMin());
		}
		return Status.STATUS_SUCCESS.getCValue();
	}

	/**
	 * Delete minimum
	 *
	 * @param thread     the thread isolate
	 * @param heapHandle the heap
	 * @param res        the element
	 * @return status
	 */
	@CEntryPoint(name = Constants.LIB_PREFIX
			+ "Heap_D_delete_min", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int deleteDoubleMin(IsolateThread thread, ObjectHandle heapHandle, CDoublePointer res) {
		Heap<Double> heap = globalHandles.get(heapHandle);
		if (res.isNonNull()) {
			res.write(heap.deleteMin());
		}
		return Status.STATUS_SUCCESS.getCValue();
	}

	/**
	 * Delete minimum
	 *
	 * @param thread     the thread isolate
	 * @param heapHandle the heap
	 * @param res        the element
	 * @return status
	 */
	@CEntryPoint(name = Constants.LIB_PREFIX
			+ "Heap_L_delete_min", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int deleteLongMin(IsolateThread thread, ObjectHandle heapHandle, CLongPointer res) {
		Heap<Long> heap = globalHandles.get(heapHandle);
		if (res.isNonNull()) {
			res.write(heap.deleteMin());
		}
		return Status.STATUS_SUCCESS.getCValue();
	}

	@CEntryPoint(name = Constants.LIB_PREFIX + "Heap_size", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int size(IsolateThread thread, ObjectHandle heapHandle, CLongPointer res) {
		Heap<?> heap = globalHandles.get(heapHandle);
		if (res.isNonNull()) {
			res.write(heap.size());
		}
		return Status.STATUS_SUCCESS.getCValue();
	}

	@CEntryPoint(name = Constants.LIB_PREFIX + "Heap_isempty", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int isEmpty(IsolateThread thread, ObjectHandle heapHandle, CIntPointer res) {
		Heap<?> heap = globalHandles.get(heapHandle);
		if (res.isNonNull()) {
			res.write(heap.isEmpty() ? 1 : 0);
		}
		return Status.STATUS_SUCCESS.getCValue();
	}

	@CEntryPoint(name = Constants.LIB_PREFIX + "Heap_clear", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int clear(IsolateThread thread, ObjectHandle heapHandle) {
		Heap<?> heap = globalHandles.get(heapHandle);
		heap.clear();
		return Status.STATUS_SUCCESS.getCValue();
	}

}
