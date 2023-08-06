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
import org.jheaps.MergeableDoubleEndedAddressableHeap;
import org.jheaps.capi.Constants;
import org.jheaps.capi.JHeapsContext.Status;
import org.jheaps.capi.error.StatusReturnExceptionHandler;

/**
 * Operations on mergeable addressable heaps.
 */
public class MergeableDoubleEndedAddressableHeapOperationsApi {

	private static ObjectHandles globalHandles = ObjectHandles.getGlobal();

	/**
	 * Meld two heaps with double keys. After the operation the second heap will be
	 * empty and not usable anymore.
	 *
	 * @param thread      the thread isolate
	 * @param heap1Handle the heap1
	 * @param heap2Handle the heap2
	 * @return status
	 */
	@CEntryPoint(name = Constants.LIB_PREFIX + "MDEAHeap_D_meld", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int meldDoubleKeyedHeaps(IsolateThread thread, ObjectHandle heap1Handle, ObjectHandle heap2Handle) {
		MergeableDoubleEndedAddressableHeap<Double, Long> heap1 = globalHandles.get(heap1Handle);
		MergeableDoubleEndedAddressableHeap<Double, Long> heap2 = globalHandles.get(heap2Handle);
		heap1.meld(heap2);
		return Status.STATUS_SUCCESS.getCValue();
	}

	/**
	 * Meld two heaps with long keys. After the operation the second heap will be
	 * empty and not usable anymore.
	 *
	 * @param thread      the thread isolate
	 * @param heap1Handle the heap1
	 * @param heap2Handle the heap2
	 * @return status
	 */
	@CEntryPoint(name = Constants.LIB_PREFIX + "MDEAHeap_L_meld", exceptionHandler = StatusReturnExceptionHandler.class)
	public static int meldLongKeyedHeaps(IsolateThread thread, ObjectHandle heap1Handle, ObjectHandle heap2Handle) {
		MergeableDoubleEndedAddressableHeap<Long, Long> heap1 = globalHandles.get(heap1Handle);
		MergeableDoubleEndedAddressableHeap<Long, Long> heap2 = globalHandles.get(heap2Handle);
		heap1.meld(heap2);
		return Status.STATUS_SUCCESS.getCValue();
	}

}
