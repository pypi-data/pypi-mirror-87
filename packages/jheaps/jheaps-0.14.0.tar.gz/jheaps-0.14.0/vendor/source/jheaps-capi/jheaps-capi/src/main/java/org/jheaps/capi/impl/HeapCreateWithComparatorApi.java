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
import org.jheaps.dag.HollowHeap;
import org.jheaps.tree.BinaryTreeAddressableHeap;
import org.jheaps.tree.BinaryTreeSoftAddressableHeap;
import org.jheaps.tree.CostlessMeldPairingHeap;
import org.jheaps.tree.DaryTreeAddressableHeap;
import org.jheaps.tree.FibonacciHeap;
import org.jheaps.tree.LeftistHeap;
import org.jheaps.tree.PairingHeap;
import org.jheaps.tree.RankPairingHeap;
import org.jheaps.tree.ReflectedFibonacciHeap;
import org.jheaps.tree.ReflectedPairingHeap;
import org.jheaps.tree.SimpleFibonacciHeap;
import org.jheaps.tree.SkewHeap;

/**
 * Heaps with comparator.
 */
public class HeapCreateWithComparatorApi {

	private static ObjectHandles globalHandles = ObjectHandles.getGlobal();

	/**
	 * Create a heap and return its handle.
	 *
	 * @param thread the thread isolate
	 * @return the heap handle
	 */
	@CEntryPoint(name = Constants.LIB_PREFIX
			+ "Heap_comparator_create", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int createHeap(IsolateThread thread, HeapType heapType,
			LongComparatorFunctionPointer comparatorFunctionPointer, WordPointer res) {

		if (comparatorFunctionPointer.isNull()) {
			throw new IllegalArgumentException("Comparator cannot be null");
		}
		Comparator<Long> comparator = (a, b) -> comparatorFunctionPointer.invoke(a, b);

		Object heap = null;
		switch (heapType) {
		case HEAP_TYPE_MERGEABLE_ADDRESSABLE_FIBONACCI:
			heap = new FibonacciHeap<>(comparator);
			break;
		case HEAP_TYPE_MERGEABLE_ADDRESSABLE_FIBONACCI_SIMPLE:
			heap = new SimpleFibonacciHeap<>(comparator);
			break;
		case HEAP_TYPE_MERGEABLE_ADDRESSABLE_PAIRING:
			heap = new PairingHeap<>(comparator);
			break;
		case HEAP_TYPE_MERGEABLE_ADDRESSABLE_PAIRING_RANK:
			heap = new RankPairingHeap<>(comparator);
			break;
		case HEAP_TYPE_MERGEABLE_ADDRESSABLE_PAIRING_COSTLESSMELD:
			heap = new CostlessMeldPairingHeap<>(comparator);
			break;
		case HEAP_TYPE_MERGEABLE_ADDRESSABLE_HOLLOW:
			heap = new HollowHeap<>(comparator);
			break;
		case HEAP_TYPE_MERGEABLE_ADDRESSABLE_LEFTIST:
			heap = new LeftistHeap<>(comparator);
			break;
		case HEAP_TYPE_MERGEABLE_ADDRESSABLE_SKEW:
			heap = new SkewHeap<>(comparator);
			break;
		case HEAP_TYPE_BINARY_IMPLICIT:
			heap = new BinaryArrayHeap<>(comparator);
			break;
		case HEAP_TYPE_BINARY_IMPLICIT_WEAK:
			heap = new BinaryArrayWeakHeap<>(comparator);
			break;
		case HEAP_TYPE_BINARY_IMPLICIT_WEAK_BULKINSERT:
			heap = new BinaryArrayBulkInsertWeakHeap<>(comparator);
			break;
		case HEAP_TYPE_ADDRESSABLE_BINARY_IMPLICIT:
			heap = new BinaryArrayAddressableHeap<>(comparator);
			break;
		case HEAP_TYPE_ADDRESSABLE_BINARY_EXPLICIT:
			heap = new BinaryTreeAddressableHeap<>(comparator);
			break;
		case HEAP_TYPE_DOUBLEENDED_BINARY_IMPLICIT_MINMAX:
			heap = new MinMaxBinaryArrayDoubleEndedHeap<>(comparator);
			break;
		case HEAP_TYPE_DOUBLEENDED_MERGEABLE_ADDRESSABLE_FIBONACCI_REFLECTED:
			heap = new ReflectedFibonacciHeap<>(comparator);
			break;
		case HEAP_TYPE_DOUBLEENDED_MERGEABLE_ADDRESSABLE_PAIRING_REFLECTED:
			heap = new ReflectedPairingHeap<>(comparator);
			break;
		default:
			throw new IllegalArgumentException("Illegal heap type requested.");
		}
		if (res.isNonNull()) {
			res.write(globalHandles.create(heap));
		}
		return Status.STATUS_SUCCESS.getCValue();
	}

	/**
	 * Create a heap and return its handle.
	 *
	 * @param thread the thread isolate
	 * @return the heap handle
	 */
	@CEntryPoint(name = Constants.LIB_PREFIX
			+ "dary_Heap_comparator_create", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int createDaryHeap(IsolateThread thread, HeapType heapType,
			LongComparatorFunctionPointer comparatorFunctionPointer, int d, WordPointer res) {

		if (comparatorFunctionPointer.isNull()) {
			throw new IllegalArgumentException("Comparator cannot be null");
		}
		Comparator<Long> comparator = (a, b) -> comparatorFunctionPointer.invoke(a, b);

		Object heap = null;
		switch (heapType) {
		case HEAP_TYPE_DARY_IMPLICIT:
			heap = new DaryArrayHeap<>(d, comparator);
			break;
		case HEAP_TYPE_ADDRESSABLE_DARY_IMPLICIT:
			heap = new DaryArrayAddressableHeap<>(d, comparator);
			break;
		case HEAP_TYPE_ADDRESSABLE_DARY_EXPLICIT:
			heap = new DaryTreeAddressableHeap<>(d, comparator);
			break;
		default:
			throw new IllegalArgumentException("Illegal heap type requested.");
		}
		if (res.isNonNull()) {
			res.write(globalHandles.create(heap));
		}
		return Status.STATUS_SUCCESS.getCValue();
	}

	/**
	 * Create a heap and return its handle.
	 *
	 * @param thread the thread isolate
	 * @return the heap handle
	 */
	@CEntryPoint(name = Constants.LIB_PREFIX
			+ "soft_Heap_comparator_create", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int createSoftHeap(IsolateThread thread, HeapType heapType,
			LongComparatorFunctionPointer comparatorFunctionPointer, double errorRate, WordPointer res) {

		if (comparatorFunctionPointer.isNull()) {
			throw new IllegalArgumentException("Comparator cannot be null");
		}
		Comparator<Long> comparator = (a, b) -> comparatorFunctionPointer.invoke(a, b);

		Object heap = null;
		switch (heapType) {
		case HEAP_TYPE_MERGEABLE_ADDRESSABLE_BINARY_EXPLICIT_SOFT:
			heap = new BinaryTreeSoftAddressableHeap<>(errorRate, comparator);
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
