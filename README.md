doorbell
========

[![Build Status](https://travis-ci.com/tbhartman/doorbell.svg?branch=master)](https://travis-ci.com/tbhartman/doorbell)
[![Coverage Status](https://coveralls.io/repos/github/tbhartman/doorbell/badge.svg)](https://coveralls.io/github/tbhartman/doorbell)
[![Docs Status](https://readthedocs.org/projects/doorbell/badge/?version=latest)](https://readthedocs.org/projects/doorbell)

[![PyPI version](https://badge.fury.io/py/doorbell.svg)](https://pypi.org/project/doorbell)
![Python Version](https://img.shields.io/pypi/pyversions/doorbell.svg)

`doorbell` provides a visitor pattern implementation for Python.

Usage
=====

Define an object that receives a visitor.  For example, in an expression
evaluator, create classes for a value and add and multiply operators:

```python
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
```

Then create a visitor class to evaluate:

```python
class Visitor(doorbell.CascadingVisitor):
    def visit_Value(self, obj, children):
        return obj.value

    def visit_Add(self, obj, children):
        return functools.reduce(operator.add, children, 0)

    def visit_Multiply(self, obj, children):
        return functools.reduce(operator.mul, children, 1)
```

Create an object and visit it:

```python
// (1+1)*(1+1)
one = Value(1)
add = Add()
add.children.extend((one, one))
mult = Mult()
mult.children.extend((add, add))

v = Visitor()
r = mult.accept(v)
assert r == 4
```

Installation
============

`pip install doorbell`

License
=======

`doorbell` is free software and licensed under the MIT License.

