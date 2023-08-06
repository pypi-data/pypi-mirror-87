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

import java.util.Comparator;

import org.graalvm.nativeimage.IsolateThread;
import org.graalvm.nativeimage.ObjectHandles;
import org.graalvm.nativeimage.c.function.CEntryPoint;
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
import org.jheaps.capi.JHeapsContext.LongComparatorFunctionPointer;
import org.jheaps.capi.JHeapsContext.Status;
import org.jheaps.capi.error.StatusReturnExceptionHandler;

/**
 * Heapify heap creation with comparator.
 */
public class HeapifyCreateWithComparatorApi {

	private static ObjectHandles globalHandles = ObjectHandles.getGlobal();

	@CEntryPoint(name = Constants.LIB_PREFIX
			+ "Heap_L_comparator_heapify", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int createHeapWithLongHeapify(IsolateThread thread, HeapType heapType,
			LongComparatorFunctionPointer comparatorFunctionPointer, CLongPointer keys, CLongPointer values, int n,
			WordPointer res) {

		if (comparatorFunctionPointer.isNull()) {
			throw new IllegalArgumentException("Comparator cannot be null");
		}
		Comparator<Long> comparator = (a, b) -> comparatorFunctionPointer.invoke(a, b);

		Long[] actualKeys = HeapifyCreateApi.copyKeys(keys, n);
		Object heap = null;
		switch (heapType) {
		case HEAP_TYPE_BINARY_IMPLICIT:
			heap = BinaryArrayHeap.heapify(actualKeys, comparator);
			break;
		case HEAP_TYPE_BINARY_IMPLICIT_WEAK:
			heap = BinaryArrayWeakHeap.heapify(actualKeys, comparator);
			break;
		case HEAP_TYPE_BINARY_IMPLICIT_WEAK_BULKINSERT:
			heap = BinaryArrayBulkInsertWeakHeap.heapify(actualKeys, comparator);
			break;
		case HEAP_TYPE_DOUBLEENDED_BINARY_IMPLICIT_MINMAX:
			heap = MinMaxBinaryArrayDoubleEndedHeap.heapify(actualKeys, comparator);
			break;
		case HEAP_TYPE_ADDRESSABLE_BINARY_IMPLICIT:
			Long[] actualValues = HeapifyCreateApi.copyValues(values, n);
			heap = BinaryArrayAddressableHeap.heapify(actualKeys, actualValues, comparator);
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
			+ "dary_Heap_L_comparator_heapify", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int createDaryHeapWithLongHeapify(IsolateThread thread, HeapType heapType,
			LongComparatorFunctionPointer comparatorFunctionPointer, int d, CLongPointer keys, CLongPointer values,
			int n, WordPointer res) {

		if (comparatorFunctionPointer.isNull()) {
			throw new IllegalArgumentException("Comparator cannot be null");
		}
		Comparator<Long> comparator = (a, b) -> comparatorFunctionPointer.invoke(a, b);

		Long[] actualKeys = HeapifyCreateApi.copyKeys(keys, n);
		Object heap = null;
		switch (heapType) {
		case HEAP_TYPE_DARY_IMPLICIT:
			heap = DaryArrayHeap.heapify(d, actualKeys, comparator);
			break;
		case HEAP_TYPE_ADDRESSABLE_DARY_EXPLICIT:
			Long[] actualValues = HeapifyCreateApi.copyValues(values, n);
			heap = DaryArrayAddressableHeap.heapify(d, actualKeys, actualValues, comparator);
			break;
		default:
			throw new IllegalArgumentException("Illegal heap type requested.");
		}

		if (res.isNonNull()) {
			res.write(globalHandles.create(heap));
		}
		return Status.STATUS_SUCCESS.getCValue();
	}

}
