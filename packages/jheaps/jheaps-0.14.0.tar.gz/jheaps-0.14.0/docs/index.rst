.. jheaps documentation master file, created by
   sphinx-quickstart on Thu Apr 23 10:34:24 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

The JHeaps library
===================

Release v\ |version|.

Python bindings for the `JHeaps library <https://www.jheaps.org/>`_.

The JHeaps library is a highly efficient Java library, containing state-of-the-art heap 
implementations. The |Bindings| is a pure python/native package having no dependency on the JVM. During the build process the backend JHeaps library is compiled as a shared library and bundled
inside the python package.

Backend version v\ |BackendVersion|.

Development
-----------

Development happens in the following places.

 * https://github.com/d-michail/python-jheaps
 * https://github.com/d-michail/jheaps-capi
 * https://github.com/d-michail/jheaps
 * https://www.jheaps.org


Documentation
-------------

.. toctree::
   :maxdepth: 2
   :caption: JHeaps

   install
   tutorials/index
   api/index
   license
   credits

.. toctree::
   :maxdepth: 2
   :caption: Example galleries

   auto_examples/index


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
