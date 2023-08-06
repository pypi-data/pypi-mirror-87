/*
 * (C) Copyright 2020, by Dimitrios Michail.
 *
 * JGraphT C-API
 *
 * See the CONTRIBUTORS.md file distributed with this work for additional
 * information regarding copyright ownership.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License 2.0 which is available at
 * http://www.eclipse.org/legal/epl-2.0, or the
 * GNU Lesser General Public License v2.1 or later
 * which is available at
 * http://www.gnu.org/licenses/old-licenses/lgpl-2.1-standalone.html.
 *
 * SPDX-License-Identifier: EPL-2.0 OR LGPL-2.1-or-later
 */
package org.jheaps.capi.error;

import org.jheaps.capi.JHeapsContext.Status;

/**
 * Convert an exception into an status code.
 */
public class StatusReturnExceptionHandler {

	public static int handle(Throwable e) {
		Status s = Errors.throwableToStatus(e);
		Errors.setError(e);
		return s.getCValue();
	}

}
