doorbell
========

*You have a visitor.*

.. image:: https://travis-ci.com/tbhartman/doorbell.svg?branch=master
   :target: https://travis-ci.com/tbhartman/doorbell
   :alt: Build Status

.. image:: https://coveralls.io/repos/github/tbhartman/doorbell/badge.svg
   :target: https://coveralls.io/github/tbhartman/doorbell
   :alt: Coverage Status

.. image:: https://readthedocs.org/projects/doorbell/badge/?version=latest
   :target: https://readthedocs.org/projects/doorbell
   :alt: Docs Status


.. image:: https://badge.fury.io/py/doorbell.svg
   :target: https://pypi.org/project/doorbell
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/doorbell.svg
   :alt: Python Version

``doorbell`` provides a visitor pattern implementation for Python.

Usage
=====

Define an object that receives a visitor.  For example, in an expression
evaluator, create classes for a value and add and multiply operators:

.. code:: python

    @doorbell.Visitee.create
    class Value:
        def __init__(self, value=0):
            self.value = value
            self.children = []


    @doorbell.Visitee.create
    class Add(Value):
        pass


    @doorbell.Visitee.create('Multiply')
    class Mult(Add):
        pass

Then create a visitor class to evaluate:

.. code:: python

    class Visitor(doorbell.CascadingVisitor):
        def visit_Value(self, obj, children):
            return obj.value

        def visit_Add(self, obj, children):
            return functools.reduce(operator.add, children, 0)

        def visit_Multiply(self, obj, children):
            return functools.reduce(operator.mul, children, 1)

Create an object and visit it:

.. code:: python

    # (1+1)*(1+1)
    one = Value(1)
    add = Add()
    add.children.extend((one, one))
    mult = Mult()
    mult.children.extend((add, add))

    v = Visitor()
    r = mult.accept(v)
    assert r == 4

Installation
============

``pip install doorbell``

License
=======

``doorbell`` is free software and licensed under the MIT License.

