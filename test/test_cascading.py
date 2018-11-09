import doorbell
import functools
import operator


class Value(doorbell.Visitee):
    def __init__(self, value=0):
        self.value = value
        self.children = []

    def accept(self, visitor):
        return visitor.visit_Value(self)


class Add(Value):
    def accept(self, visitor):
        return visitor.visit_Add(self)


class Mult(Add):
    def accept(self, visitor):
        return visitor.visit_Mult(self)


class ManyArgs(Value):
    def accept(self, visitor, *args):
        return visitor.visit_ManyArgs(self, *args)


class Visitor(doorbell.CascadingVisitor):
    def visit_Value(self, obj, children):
        return obj.value

    def visit_Add(self, obj, children):
        return functools.reduce(operator.add, children, 0)

    def visit_Mult(self, obj, children):
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
