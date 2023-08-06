
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Language](http://img.shields.io/badge/language-java-brightgreen.svg)](https://www.java.com/)

# JHeaps Native Library

This library provides a native C api to the JHeaps library. Since the JHeaps library is written in Java, we
use [GraalVM](https://www.graalvm.org/) in order to build a shared library.

_Important! This is alpha software and the interface many change!_

## Build

We use cmake to build the native library. 

```
mkdir build/
cd build/
cmake ..
make
```
## Installation

Use `make install` to install the library. After a successful installation, you should see the following files: 

```
jheaps_capi.h
jheaps_capi_types.h
jheaps_capi_dynamic.h
graal_isolate.h
graal_isolate_dynamic.h
```

and the shared library `libjheaps_capi.so`.

## Requirements 

The build will succeed only if you have the following piece of software installed:

 * GraalVM 20.0 with Java 11 support
 * Native Image component from GraalVM
 * GNU C compiler or clang
 * glibc-devel, zlib-devel (header files for the C library and zlib)
 * Maven build tool
 * CMake

For Windows you will need Microsoft Visual C++ (MSVC) 2017 15.5.5 or later. Build the 
system using the proper
[Developer Command Prompt](https://docs.microsoft.com/en-us/cpp/build/building-on-the-command-line?view=vs-2019#developer_command_prompt_shortcuts)
for your version of [Visual Studio](https://visualstudio.microsoft.com/vs/). This means 
`x64 Native Tools Command Prompt`. Use Visual Studio 2017 or later.

## License

This library may be used under the terms of the 

 * Apache License Version 2.0
   https://www.apache.org/licenses/LICENSE-2.0

Please note that this library is distributed WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE.

Please refer to the license for details.

SPDX-License-Identifier: Apache-2.0

## Author

(C) Copyright 2020, by Dimitrios Michail


Enjoy!
