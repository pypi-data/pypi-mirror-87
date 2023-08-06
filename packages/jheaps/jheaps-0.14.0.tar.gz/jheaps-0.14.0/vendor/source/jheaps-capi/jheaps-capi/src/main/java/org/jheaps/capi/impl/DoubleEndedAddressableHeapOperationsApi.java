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
import org.graalvm.nativeimage.c.type.WordPointer;
import org.jheaps.DoubleEndedAddressableHeap;
import org.jheaps.DoubleEndedAddressableHeap.Handle;
import org.jheaps.capi.Constants;
import org.jheaps.capi.JHeapsContext.Status;
import org.jheaps.capi.error.StatusReturnExceptionHandler;

/**
 * Operations on double ended addressable heaps.
 */
public class DoubleEndedAddressableHeapOperationsApi {

	private static ObjectHandles globalHandles = ObjectHandles.getGlobal();

	/**
	 * Find maximum
	 *
	 * @param thread     the thread isolate
	 * @param heapHandle the heap
	 * @param res        the element handle
	 * @return status
	 */
	@CEntryPoint(name = Constants.LIB_PREFIX
			+ "DEAHeap_find_max", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int findMax(IsolateThread thread, ObjectHandle heapHandle, WordPointer res) {
		DoubleEndedAddressableHeap<?, ?> heap = globalHandles.get(heapHandle);
		Handle<?, ?> handle = heap.findMax();
		if (res.isNonNull()) {
			res.write(globalHandles.create(handle));
		}
		return Status.STATUS_SUCCESS.getCValue();
	}

	/**
	 * Delete maximum
	 *
	 * @param thread     the thread isolate
	 * @param heapHandle the heap
	 * @param res        the element handle
	 * @return status
	 */
	@CEntryPoint(name = Constants.LIB_PREFIX
			+ "DEAHeap_delete_max", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int deleteMax(IsolateThread thread, ObjectHandle heapHandle, WordPointer res) {
		DoubleEndedAddressableHeap<?, ?> heap = globalHandles.get(heapHandle);
		Handle<?, ?> handle = heap.deleteMax();
		if (res.isNonNull()) {
			res.write(globalHandles.create(handle));
		}
		return Status.STATUS_SUCCESS.getCValue();
	}

	/**
	 * Increase a double key of a handle
	 *
	 * @param thread the thread isolate
	 * @param handle the heap handle handle
	 * @param key    the new key
	 * @return status
	 */
	@CEntryPoint(name = Constants.LIB_PREFIX
			+ "DEAHeapHandle_D_increase_key", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int handleIncreaseDoubleKey(IsolateThread thread, ObjectHandle handle, double key) {
		Handle<Double, ?> h = globalHandles.get(handle);
		h.increaseKey(key);
		return Status.STATUS_SUCCESS.getCValue();
	}

	/**
	 * Increase a long key of a handle
	 *
	 * @param thread the thread isolate
	 * @param handle the heap handle handle
	 * @param key    the new key
	 * @return status
	 */
	@CEntryPoint(name = Constants.LIB_PREFIX
			+ "DEAHeapHandle_L_increase_key", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int handleIncreaseLongKey(IsolateThread thread, ObjectHandle handle, long key) {
		Handle<Long, ?> h = globalHandles.get(handle);
		h.increaseKey(key);
		return Status.STATUS_SUCCESS.getCValue();
	}
}
