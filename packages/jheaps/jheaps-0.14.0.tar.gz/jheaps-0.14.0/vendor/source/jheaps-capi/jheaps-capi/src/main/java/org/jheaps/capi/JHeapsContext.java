/*
 * (C) Copyright 2014-2020, by Dimitrios Michail
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
package org.jheaps.capi;

import org.graalvm.nativeimage.c.CContext;
import org.graalvm.nativeimage.c.constant.CEnum;
import org.graalvm.nativeimage.c.constant.CEnumLookup;
import org.graalvm.nativeimage.c.constant.CEnumValue;
import org.graalvm.nativeimage.c.function.CFunctionPointer;
import org.graalvm.nativeimage.c.function.InvokeCFunctionPointer;

@CContext(JHeapsDirectives.class)
public class JHeapsContext {

	@CEnum("status_t")
	public enum Status {

		// @formatter:off
		STATUS_SUCCESS, 
		STATUS_ERROR,
		STATUS_ILLEGAL_ARGUMENT,
		STATUS_UNSUPPORTED_OPERATION,
		STATUS_INDEX_OUT_OF_BOUNDS,
		STATUS_NO_SUCH_ELEMENT,
		STATUS_NULL_POINTER,
		STATUS_CLASS_CAST,
		STATUS_IO_ERROR,
		STATUS_ILLEGAL_STATE,
		;
		// @formatter:on

		@CEnumValue
		public native int getCValue();

		@CEnumLookup
		public static native Status fromCValue(int value);

	}

	@CEnum("heap_type_t")
	public enum HeapType {

		// @formatter:off
		HEAP_TYPE_MERGEABLE_ADDRESSABLE_FIBONACCI,
		HEAP_TYPE_MERGEABLE_ADDRESSABLE_FIBONACCI_SIMPLE,
	    HEAP_TYPE_MERGEABLE_ADDRESSABLE_PAIRING,
	    HEAP_TYPE_MERGEABLE_ADDRESSABLE_PAIRING_RANK,
	    HEAP_TYPE_MERGEABLE_ADDRESSABLE_PAIRING_COSTLESSMELD,
	    HEAP_TYPE_MERGEABLE_ADDRESSABLE_HOLLOW,
	    HEAP_TYPE_MERGEABLE_ADDRESSABLE_LEFTIST,
	    HEAP_TYPE_MERGEABLE_ADDRESSABLE_SKEW,
	    
	    HEAP_TYPE_BINARY_IMPLICIT,
	    HEAP_TYPE_BINARY_IMPLICIT_WEAK,
	    HEAP_TYPE_BINARY_IMPLICIT_WEAK_BULKINSERT,
	    HEAP_TYPE_ADDRESSABLE_BINARY_IMPLICIT,
	    HEAP_TYPE_ADDRESSABLE_BINARY_EXPLICIT,
	    
	    HEAP_TYPE_DARY_IMPLICIT,
	    HEAP_TYPE_ADDRESSABLE_DARY_IMPLICIT,
	    HEAP_TYPE_ADDRESSABLE_DARY_EXPLICIT,
	    
	    HEAP_TYPE_MERGEABLE_ADDRESSABLE_BINARY_EXPLICIT_SOFT,
	    
	    HEAP_TYPE_DOUBLEENDED_BINARY_IMPLICIT_MINMAX,
	    HEAP_TYPE_DOUBLEENDED_MERGEABLE_ADDRESSABLE_FIBONACCI_REFLECTED,
	    HEAP_TYPE_DOUBLEENDED_MERGEABLE_ADDRESSABLE_PAIRING_REFLECTED,
	    
	    HEAP_TYPE_MONOTONE_LONG_RADIX,
	    HEAP_TYPE_MONOTONE_ADDRESSABLE_LONG_RADIX,
	    HEAP_TYPE_MONOTONE_DOUBLE_RADIX,
	    HEAP_TYPE_MONOTONE_ADDRESSABLE_DOUBLE_RADIX,
		;
		// @formatter:on

		@CEnumValue
		public native int toCEnum();

		@CEnumLookup
		public static native HeapType toJavaEnum(int value);

	}

	/*
     * Function pointer for a comparator with long identifiers (indirect reference). 
     */
    public interface LongComparatorFunctionPointer extends CFunctionPointer {

            @InvokeCFunctionPointer
            int invoke(long a, long b);
            
    }

}
