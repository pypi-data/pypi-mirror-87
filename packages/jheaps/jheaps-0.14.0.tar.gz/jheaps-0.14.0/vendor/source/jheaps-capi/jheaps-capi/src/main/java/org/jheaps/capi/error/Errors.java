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
package org.jheaps.capi.error;

import java.io.IOException;
import java.util.NoSuchElementException;
import java.util.Optional;

import org.graalvm.nativeimage.c.type.CCharPointer;
import org.jheaps.capi.JHeapsContext.Status;

/**
 * Error handling
 */
public class Errors {

	public static final String NO_MESSAGE = "";

	/**
	 * The actual error, one per thread.
	 */
	private static ThreadLocal<Error> errorThreadLocal = ThreadLocal
			.withInitial(() -> new Error(Status.STATUS_SUCCESS, NO_MESSAGE, null));

	public static Status getErrorStatus() {
		return errorThreadLocal.get().getStatus();
	}

	public static String getErrorMessage() {
		return errorThreadLocal.get().getMessage();
	}

	public static CCharPointer getMessageCCharPointer() {
		Error error = errorThreadLocal.get();
		return error.getMessagePin().get();
	}

	public static Optional<Throwable> getErrorThrowable() {
		return Optional.ofNullable(errorThreadLocal.get().getThrowable());
	}

	public static void clearError() {
		errorThreadLocal.set(new Error(Status.STATUS_SUCCESS, NO_MESSAGE, null));
	}

	public static void setError(Throwable e) {
		Status status = throwableToStatus(e);
		String message = e.getMessage();
		if (message == null) {
			StringBuilder sb = new StringBuilder();
			sb.append("Error");
			String exceptionClassName = e.getClass().getSimpleName();
			if (exceptionClassName != null) {
				sb.append(" (");
				sb.append(exceptionClassName);
				sb.append(")");
			}
			message = sb.toString();
		}
		errorThreadLocal.set(new Error(status, message, e));
	}

	public static Status throwableToStatus(Throwable e) {
		if (e instanceof IllegalArgumentException) {
			return Status.STATUS_ILLEGAL_ARGUMENT;
		} else if (e instanceof UnsupportedOperationException) {
			return Status.STATUS_UNSUPPORTED_OPERATION;
		} else if (e instanceof IndexOutOfBoundsException) {
			return Status.STATUS_INDEX_OUT_OF_BOUNDS;
		} else if (e instanceof NoSuchElementException) {
			return Status.STATUS_NO_SUCH_ELEMENT;
		} else if (e instanceof NullPointerException) {
			return Status.STATUS_NULL_POINTER;
		} else if (e instanceof ClassCastException) {
			return Status.STATUS_CLASS_CAST;
		} else if (e instanceof IOException) {
			return Status.STATUS_IO_ERROR;
		} else if (e instanceof IllegalStateException) {
			return Status.STATUS_ILLEGAL_STATE;
		} else {
			return Status.STATUS_ERROR;
		}
	}

}
