.. _usage:

Usage
=====

.. currentmodule:: doorbell

The Visitee
-----------

|project_name| provides :class:`Visitee`, an `abstract base class
<ABC_>`_ with a single method, :func:`Visitee.accept`.
Implementations of :func:`Visitee.accept` typically only consist of a
single line:

.. code-block:: python

    def accept(self, visitor):
       return visitor.visit_MyType(self)

where `visit_MyType` is the method on the visitor which applies to this
particular object.  Typically, only the object (`self`) is passed, although
any arguments will be passed along to the visitor's method.

The Visitor
-----------

The base :class:`Visitor` class and its children are the main
products of |project_name|.  Your visitor class inherits from
:class:`Visitor` or its children, and implements a set of methods
which are called from a :func:`Visitee.accpet`.  By default, any
method whose name begins `visit_` is considered a visitor method.  However,
the decorators:

  * :func:`~Visitor.visitor_method`
  * :func:`~Visitor.non_visitor_method`

override this default.  Any method decorated with
:func:`~Visitor.visitor_method` will be considered a visitor method,
while any method decorated with :func:`~Visitor.non_visitor_method`
will *not* be considered a visitor method.  All visitor methods are wrapped by
:func:`Visitor._visit_method`.

The following visitor classes are provided:


.. autosummary::
    :nosignatures:

    ~Visitor
    ~CascadingVisitor
    ~WrappingVisitor


.. _ABC: https://docs.python.org/3/library/abc.html
