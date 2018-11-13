import doorbell
import functools
import operator


@doorbell.Visitee.create
class Value(object):
    def __init__(self, value=0):
        self.value = value
        self.children = []


@doorbell.Visitee.create
class Add(Value):
    pass


@doorbell.Visitee.create('Multiply')
class Mult(Add):
    pass


class ManyArgs(Value):
    def accept(self, visitor, *args):
        return visitor.visit_ManyArgs(self, *args)


class Visitor(doorbell.CascadingVisitor):
    def visit_Value(self, obj, children):
        return obj.value

    def visit_Add(self, obj, children):
        return functools.reduce(operator.add, children, 0)

    def visit_Multiply(self, obj, children):
        return functools.reduce(operator.mul, children, 1)

    def visit_ManyArgs(self, obj, children, *args):
        return len(args)


class TestVisitee:
    def test_add(self):
        one = Value(1)
        add = Add()
        add.children.append(one)
        add.children.append(one)
        v = Visitor()
        r = add.accept(v)
        assert r == 2

    def test_multiply(self):
        one = Value(1)
        mult = Mult()
        mult.children.append(one)
        mult.children.append(one)
        v = Visitor()
        r = mult.accept(v)
        assert r == 1

    def test_combined(self):
        one = Value(1)
        add = Add()
        add.children.extend((one, one))
        mult = Mult()
        mult.children.extend((add, add))
        v = Visitor()
        r = mult.accept(v)
        assert r == 4

    def test_many_arguments(self):
        """visitor method should receive all additional arguments"""
        m = ManyArgs()
        v = Visitor()
        assert m.accept(v, 1, 2, 3) == 3
