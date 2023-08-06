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
import org.jheaps.dag.HollowHeap;
import org.jheaps.monotone.DoubleRadixAddressableHeap;
import org.jheaps.monotone.DoubleRadixHeap;
import org.jheaps.monotone.LongRadixAddressableHeap;
import org.jheaps.monotone.LongRadixHeap;
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
 * Heap creation
 */
public class HeapCreateApi {

	private static ObjectHandles globalHandles = ObjectHandles.getGlobal();

	/**
	 * Create a heap and return its handle.
	 *
	 * @param thread the thread isolate
	 * @return the heap handle
	 */
	@CEntryPoint(name = Constants.LIB_PREFIX + "Heap_create", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int createHeap(IsolateThread thread, HeapType heapType, WordPointer res) {
		Object heap = null;
		switch (heapType) {
		case HEAP_TYPE_MERGEABLE_ADDRESSABLE_FIBONACCI:
			heap = new FibonacciHeap<>();
			break;
		case HEAP_TYPE_MERGEABLE_ADDRESSABLE_FIBONACCI_SIMPLE:
			heap = new SimpleFibonacciHeap<>();
			break;
		case HEAP_TYPE_MERGEABLE_ADDRESSABLE_PAIRING:
			heap = new PairingHeap<>();
			break;
		case HEAP_TYPE_MERGEABLE_ADDRESSABLE_PAIRING_RANK:
			heap = new RankPairingHeap<>();
			break;
		case HEAP_TYPE_MERGEABLE_ADDRESSABLE_PAIRING_COSTLESSMELD:
			heap = new CostlessMeldPairingHeap<>();
			break;
		case HEAP_TYPE_MERGEABLE_ADDRESSABLE_HOLLOW:
			heap = new HollowHeap<>();
			break;
		case HEAP_TYPE_MERGEABLE_ADDRESSABLE_LEFTIST:
			heap = new LeftistHeap<>();
			break;
		case HEAP_TYPE_MERGEABLE_ADDRESSABLE_SKEW:
			heap = new SkewHeap<>();
			break;
		case HEAP_TYPE_BINARY_IMPLICIT:
			heap = new BinaryArrayHeap<>();
			break;
		case HEAP_TYPE_BINARY_IMPLICIT_WEAK:
			heap = new BinaryArrayWeakHeap<>();
			break;
		case HEAP_TYPE_BINARY_IMPLICIT_WEAK_BULKINSERT:
			heap = new BinaryArrayBulkInsertWeakHeap<>();
			break;
		case HEAP_TYPE_ADDRESSABLE_BINARY_IMPLICIT:
			heap = new BinaryArrayAddressableHeap<>();
			break;
		case HEAP_TYPE_ADDRESSABLE_BINARY_EXPLICIT:
			heap = new BinaryTreeAddressableHeap<>();
			break;
		case HEAP_TYPE_DOUBLEENDED_BINARY_IMPLICIT_MINMAX:
			heap = new MinMaxBinaryArrayDoubleEndedHeap<>();
			break;
		case HEAP_TYPE_DOUBLEENDED_MERGEABLE_ADDRESSABLE_FIBONACCI_REFLECTED:
			heap = new ReflectedFibonacciHeap<>();
			break;
		case HEAP_TYPE_DOUBLEENDED_MERGEABLE_ADDRESSABLE_PAIRING_REFLECTED:
			heap = new ReflectedPairingHeap<>();
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
			+ "dary_Heap_create", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int createDaryHeap(IsolateThread thread, HeapType heapType, int d, WordPointer res) {
		Object heap = null;
		switch (heapType) {
		case HEAP_TYPE_DARY_IMPLICIT:
			heap = new DaryArrayHeap<>(d);
			break;
		case HEAP_TYPE_ADDRESSABLE_DARY_IMPLICIT:
			heap = new DaryArrayAddressableHeap<>(d);
			break;
		case HEAP_TYPE_ADDRESSABLE_DARY_EXPLICIT:
			heap = new DaryTreeAddressableHeap<>(d);
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
			+ "soft_Heap_create", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int createSoftHeap(IsolateThread thread, HeapType heapType, double errorRate, WordPointer res) {
		Object heap = null;
		switch (heapType) {
		case HEAP_TYPE_MERGEABLE_ADDRESSABLE_BINARY_EXPLICIT_SOFT:
			heap = new BinaryTreeSoftAddressableHeap<>(errorRate);
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
			+ "double_radix_Heap_create", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int createDoubleRadixHeap(IsolateThread thread, HeapType heapType, double min, double max,
			WordPointer res) {
		Object heap = null;
		switch (heapType) {
		case HEAP_TYPE_MONOTONE_DOUBLE_RADIX:
			heap = new DoubleRadixHeap(min, max);
			break;
		case HEAP_TYPE_MONOTONE_ADDRESSABLE_DOUBLE_RADIX:
			heap = new DoubleRadixAddressableHeap<>(min, max);
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
			+ "long_radix_Heap_create", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int createLongRadixHeap(IsolateThread thread, HeapType heapType, long min, long max,
			WordPointer res) {
		Object heap = null;
		switch (heapType) {
		case HEAP_TYPE_MONOTONE_LONG_RADIX:
			heap = new LongRadixHeap(min, max);
			break;
		case HEAP_TYPE_MONOTONE_ADDRESSABLE_LONG_RADIX:
			heap = new LongRadixAddressableHeap<>(min, max);
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
