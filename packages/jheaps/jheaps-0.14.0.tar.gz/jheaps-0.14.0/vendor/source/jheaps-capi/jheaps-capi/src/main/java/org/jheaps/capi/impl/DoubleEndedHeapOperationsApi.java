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
import org.graalvm.nativeimage.c.type.CLongPointer;
import org.jheaps.DoubleEndedHeap;
import org.jheaps.capi.Constants;
import org.jheaps.capi.JHeapsContext.Status;
import org.jheaps.capi.error.StatusReturnExceptionHandler;

/**
 * Operations on double ended heaps.
 */
public class DoubleEndedHeapOperationsApi {

	private static ObjectHandles globalHandles = ObjectHandles.getGlobal();

	/**
	 * Find maximum
	 *
	 * @param thread     the thread isolate
	 * @param heapHandle the heap
	 * @param res        the element
	 * @return status
	 */
	@CEntryPoint(name = Constants.LIB_PREFIX
			+ "DEHeap_D_find_max", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int findDoubleMax(IsolateThread thread, ObjectHandle heapHandle, CDoublePointer res) {
		DoubleEndedHeap<Double> heap = globalHandles.get(heapHandle);
		if (res.isNonNull()) {
			res.write(heap.findMax());
		}
		return Status.STATUS_SUCCESS.getCValue();
	}

	/**
	 * Find maximum
	 *
	 * @param thread     the thread isolate
	 * @param heapHandle the heap
	 * @param res        the element
	 * @return status
	 */
	@CEntryPoint(name = Constants.LIB_PREFIX
			+ "DEHeap_L_find_max", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int findLongMax(IsolateThread thread, ObjectHandle heapHandle, CLongPointer res) {
		DoubleEndedHeap<Long> heap = globalHandles.get(heapHandle);
		if (res.isNonNull()) {
			res.write(heap.findMax());
		}
		return Status.STATUS_SUCCESS.getCValue();
	}

	/**
	 * Delete maximum
	 *
	 * @param thread     the thread isolate
	 * @param heapHandle the heap
	 * @param res        the element
	 * @return status
	 */
	@CEntryPoint(name = Constants.LIB_PREFIX
			+ "DEHeap_D_delete_max", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int deleteDoubleMax(IsolateThread thread, ObjectHandle heapHandle, CDoublePointer res) {
		DoubleEndedHeap<Double> heap = globalHandles.get(heapHandle);
		if (res.isNonNull()) {
			res.write(heap.deleteMax());
		}
		return Status.STATUS_SUCCESS.getCValue();
	}

	/**
	 * Delete maximum
	 *
	 * @param thread     the thread isolate
	 * @param heapHandle the heap
	 * @param res        the element
	 * @return status
	 */
	@CEntryPoint(name = Constants.LIB_PREFIX
			+ "DEHeap_L_delete_max", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int deleteLongMax(IsolateThread thread, ObjectHandle heapHandle, CLongPointer res) {
		DoubleEndedHeap<Long> heap = globalHandles.get(heapHandle);
		if (res.isNonNull()) {
			res.write(heap.deleteMax());
		}
		return Status.STATUS_SUCCESS.getCValue();
	}

}
