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

import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;

import org.graalvm.nativeimage.ImageSingletons;
import org.graalvm.nativeimage.PinnedObject;
import org.graalvm.nativeimage.c.type.CCharPointer;
import org.graalvm.nativeimage.c.type.CTypeConversion.CCharPointerHolder;
import org.graalvm.nativeimage.impl.CTypeConversionSupport;

import com.oracle.svm.core.SubstrateUtil;

public class StringUtils {

	public static String toJavaString(CCharPointer cString, Charset charset) {
		if (cString.isNull()) {
			return null;
		}
		CTypeConversionSupport support = ImageSingletons.lookup(CTypeConversionSupport.class);
		return support.toJavaString(cString, SubstrateUtil.strlen(cString), charset);
	}

	public static String toJavaStringFromUtf8(CCharPointer cString) {
		return toJavaString(cString, StandardCharsets.UTF_8);
	}

	public static CCharPointerHolder toCString(CharSequence javaString, Charset charset) {
		return new CCharPointerCharsetHolderImpl(javaString, charset);
	}

	public static CCharPointerHolder toCString(byte[] bytes) {
		return new CCharPointerCharsetHolderImpl(bytes);
	}

	public static CCharPointerHolder toCStringInUtf8(CharSequence javaString) {
		return toCString(javaString, StandardCharsets.UTF_8);
	}

	/**
	 * Custom implementation of CCharPointerHolder which supports adjusting the
	 * charset.
	 */
	static class CCharPointerCharsetHolderImpl implements CCharPointerHolder {

		private final PinnedObject cstring;

		CCharPointerCharsetHolderImpl(CharSequence javaString, Charset charset) {
			byte[] bytes = javaString.toString().getBytes(charset);
			/* Append the terminating 0. */
			bytes = Arrays.copyOf(bytes, bytes.length + 1);
			cstring = PinnedObject.create(bytes);
		}

		CCharPointerCharsetHolderImpl(byte[] bytes) {
			/* Append the terminating 0. */
			bytes = Arrays.copyOf(bytes, bytes.length + 1);
			cstring = PinnedObject.create(bytes);
		}

		@Override
		public CCharPointer get() {
			return cstring.addressOfArrayElement(0);
		}

		@Override
		public void close() {
			cstring.close();
		}
	}

}
