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
import org.graalvm.nativeimage.ObjectHandles;
import org.graalvm.nativeimage.c.function.CEntryPoint;
import org.graalvm.nativeimage.c.type.CDoublePointer;
import org.graalvm.nativeimage.c.type.CLongPointer;
import org.graalvm.nativeimage.c.type.WordPointer;
import org.jheaps.array.BinaryArrayAddressableHeap;
import org.jheaps.array.BinaryArrayBulkInsertWeakHeap;
import org.jheaps.array.BinaryArrayHeap;
import org.jheaps.array.BinaryArrayWeakHeap;
import org.jheaps.array.DaryArrayAddressableHeap;
import org.jheaps.array.DaryArrayHeap;
import org.jheaps.array.MinMaxBinaryArrayDoubleEndedHeap;
import org.jheaps.capi.Constants;
import org.jheaps.capi.JHeapsContext.HeapType;
import org.jheaps.capi.JHeapsContext.Status;
import org.jheaps.capi.error.StatusReturnExceptionHandler;

/**
 * Heapify heap creation
 */
public class HeapifyCreateApi {

	private static ObjectHandles globalHandles = ObjectHandles.getGlobal();

	@CEntryPoint(name = Constants.LIB_PREFIX + "Heap_D_heapify", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int createHeapWithDoubleHeapify(IsolateThread thread, HeapType heapType, CDoublePointer keys,
			CLongPointer values, int n, WordPointer res) {
		Double[] actualKeys = copyKeys(keys, n);
		Object heap = null;
		switch (heapType) {
		case HEAP_TYPE_BINARY_IMPLICIT:
			heap = BinaryArrayHeap.heapify(actualKeys);
			break;
		case HEAP_TYPE_BINARY_IMPLICIT_WEAK:
			heap = BinaryArrayWeakHeap.heapify(actualKeys);
			break;
		case HEAP_TYPE_BINARY_IMPLICIT_WEAK_BULKINSERT:
			heap = BinaryArrayBulkInsertWeakHeap.heapify(actualKeys);
			break;
		case HEAP_TYPE_DOUBLEENDED_BINARY_IMPLICIT_MINMAX:
			heap = MinMaxBinaryArrayDoubleEndedHeap.heapify(actualKeys);
			break;
		case HEAP_TYPE_ADDRESSABLE_BINARY_IMPLICIT:
			Long[] actualValues = copyValues(values, n);
			heap = BinaryArrayAddressableHeap.heapify(actualKeys, actualValues);
			break;
		default:
			throw new IllegalArgumentException("Illegal heap type requested.");
		}

		if (res.isNonNull()) {
			res.write(globalHandles.create(heap));
		}
		return Status.STATUS_SUCCESS.getCValue();
	}

	@CEntryPoint(name = Constants.LIB_PREFIX + "Heap_L_heapify", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int createHeapWithLongHeapify(IsolateThread thread, HeapType heapType, CLongPointer keys,
			CLongPointer values, int n, WordPointer res) {
		Long[] actualKeys = copyKeys(keys, n);
		Object heap = null;
		switch (heapType) {
		case HEAP_TYPE_BINARY_IMPLICIT:
			heap = BinaryArrayHeap.heapify(actualKeys);
			break;
		case HEAP_TYPE_BINARY_IMPLICIT_WEAK:
			heap = BinaryArrayWeakHeap.heapify(actualKeys);
			break;
		case HEAP_TYPE_BINARY_IMPLICIT_WEAK_BULKINSERT:
			heap = BinaryArrayBulkInsertWeakHeap.heapify(actualKeys);
			break;
		case HEAP_TYPE_DOUBLEENDED_BINARY_IMPLICIT_MINMAX:
			heap = MinMaxBinaryArrayDoubleEndedHeap.heapify(actualKeys);
			break;
		case HEAP_TYPE_ADDRESSABLE_BINARY_IMPLICIT:
			Long[] actualValues = copyValues(values, n);
			heap = BinaryArrayAddressableHeap.heapify(actualKeys, actualValues);
			break;
		default:
			throw new IllegalArgumentException("Illegal heap type requested.");
		}

		if (res.isNonNull()) {
			res.write(globalHandles.create(heap));
		}
		return Status.STATUS_SUCCESS.getCValue();
	}

	@CEntryPoint(name = Constants.LIB_PREFIX
			+ "dary_Heap_D_heapify", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int createDaryHeapWithDoubleHeapify(IsolateThread thread, HeapType heapType, int d,
			CDoublePointer keys, CLongPointer values, int n, WordPointer res) {
		Double[] actualKeys = copyKeys(keys, n);
		Object heap = null;
		switch (heapType) {
		case HEAP_TYPE_DARY_IMPLICIT:
			heap = DaryArrayHeap.heapify(d, actualKeys);
			break;
		case HEAP_TYPE_ADDRESSABLE_DARY_EXPLICIT:
			Long[] actualValues = copyValues(values, n);
			heap = DaryArrayAddressableHeap.heapify(d, actualKeys, actualValues);
			break;
		default:
			throw new IllegalArgumentException("Illegal heap type requested.");
		}

		if (res.isNonNull()) {
			res.write(globalHandles.create(heap));
		}
		return Status.STATUS_SUCCESS.getCValue();
	}

	@CEntryPoint(name = Constants.LIB_PREFIX
			+ "dary_Heap_L_heapify", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int createDaryHeapWithLongHeapify(IsolateThread thread, HeapType heapType, int d, CLongPointer keys,
			CLongPointer values, int n, WordPointer res) {
		Long[] actualKeys = copyKeys(keys, n);
		Object heap = null;
		switch (heapType) {
		case HEAP_TYPE_DARY_IMPLICIT:
			heap = DaryArrayHeap.heapify(d, actualKeys);
			break;
		case HEAP_TYPE_ADDRESSABLE_DARY_EXPLICIT:
			Long[] actualValues = copyValues(values, n);
			heap = DaryArrayAddressableHeap.heapify(d, actualKeys, actualValues);
			break;
		default:
			throw new IllegalArgumentException("Illegal heap type requested.");
		}

		if (res.isNonNull()) {
			res.write(globalHandles.create(heap));
		}
		return Status.STATUS_SUCCESS.getCValue();
	}

	// helper methods

	public static Long[] copyValues(CLongPointer values, int n) {
		if (n <= 0) {
			throw new IllegalArgumentException("Array size must be positive");
		}
		Long[] actualValues = new Long[n];
		if (values.isNull()) {
			for (int i = 0; i < n; i++) {
				actualValues[i] = 0l;
			}
		} else {
			for (int i = 0; i < n; i++) {
				actualValues[i] = values.read(i);
			}
		}
		return actualValues;
	}

	public static Long[] copyKeys(CLongPointer keys, int n) {
		if (n <= 0) {
			throw new IllegalArgumentException("Array size must be positive");
		}
		if (keys.isNull()) {
			throw new IllegalArgumentException("Keys array cannot be null");
		}
		Long[] actualKeys = new Long[n];
		for (int i = 0; i < n; i++) {
			actualKeys[i] = keys.read(i);
		}
		return actualKeys;
	}

	public static Double[] copyKeys(CDoublePointer keys, int n) {
		if (n <= 0) {
			throw new IllegalArgumentException("Array size must be positive");
		}
		if (keys.isNull()) {
			throw new IllegalArgumentException("Keys array cannot be null");
		}
		Double[] actualKeys = new Double[n];
		for (int i = 0; i < n; i++) {
			actualKeys[i] = keys.read(i);
		}
		return actualKeys;
	}

}
