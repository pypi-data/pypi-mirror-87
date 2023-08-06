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

import java.util.Objects;

import org.graalvm.nativeimage.c.type.CTypeConversion.CCharPointerHolder;
import org.jheaps.capi.StringUtils;
import org.jheaps.capi.JHeapsContext.Status;

public class Error {

	private Status status;
	private String message;
	private CCharPointerHolder messagePin;
	private Throwable throwable;

	public Error(Status status, String message, Throwable throwable) {
		this.status = Objects.requireNonNull(status, "Status cannot be null");
		this.message = Objects.requireNonNull(message, "Message cannot be null");
		this.messagePin = StringUtils.toCStringInUtf8(message);
		this.throwable = throwable;
	}

	public Status getStatus() {
		return status;
	}

	public String getMessage() {
		return message;
	}

	public CCharPointerHolder getMessagePin() {
		return messagePin;
	}

	public Throwable getThrowable() {
		return throwable;
	}

	@Override
	public String toString() {
		return "Error [status=" + status + ", message=" + message + ", messagePin=" + messagePin + ", throwable="
				+ throwable + "]";
	}

}
