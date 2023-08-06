
.. _introduction:

Introduction
************ 

.. currentmodule:: jheaps
 
The |Project| library is a highly efficient library containing state-of-the-art heap implementations.

The |Bindings| is a pure python/native package having no dependency on the JVM. During the build
process the backend |Project| library is compiled as a shared library and bundled inside the python
package.

Available heaps:

  * Tree-based.

    * Fibonacci mergeable and addressable heaps.

    * Simple Fibonacci heaps.

    * Pairing mergeable and addressable heaps.

    * Costless-meld variant of Pairing heaps.

    * Rank-Pairing (type-1) mergeable and addressable heaps.

    * Leftist mergeable and addressable heaps.

    * Explicit binary tree addressable heaps.

    * Binary tree soft heaps.

    * Skew heaps.

  * Dag-based.

    * Hollow mergeable and addressable heaps.

  * Double-ended mergeable and addressable heaps.

    * Reflected Fibonacci heaps.

    * Reflected Pairing heaps.

  * Array-based.

    * Binary heaps.

    * Binary addressable heaps.

    * D-ary heaps.

    * D-ary addressable heaps.

    * Binary weak heaps.

    * Binary weak heaps supporting bulk insertion.

    * Highly optimized binary heaps for integer keys using the Wegener bottom-up heuristic and sentinel values.

  * Double-ended array-based.

    * Binary MinMax heaps.

  * Monotone heaps.

    * Addressable radix heaps with float and int keys.

    * Non-addressable radix heaps with float and int keys.


   
