More Collections
================

Some useful data structures for collections of data

Class ``Index``
~~~~~~~~~~~~~~~

Provide indexing for a list. Inner properties can be used for keys, and
keys can be tuples of properties.

Class ``UniqueIndex``
~~~~~~~~~~~~~~~~~~~~~

Same as Index, but includes checks and optimization to ensure members'
keys are unique.

Class ``Queue``
~~~~~~~~~~~~~~~

A ``Queue`` is a list, with ``add()`` and ``pop()``. It ensures members
in the queue are not duplicated by not adding the ones already found in
the queue.

Class ``Matrix``
~~~~~~~~~~~~~~~~

A multidimensional grid of values that can be used like a ``Mapping``
from a-tuple-of-coordinates to the value at that coordinate. Plus a few
other convenience methods.

This is a naive implementation. The hope it is a simple facade to a
faster implementation.

Class ``Relation``
~~~~~~~~~~~~~~~~~~

Store the many-to-many relations between two domains
