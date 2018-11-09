import doorbell


class TestNonVisitorDecorator:
    class Value(doorbell.Visitee):
        def __init__(self, value=0):
            self.value = value

        def accept(self, visitor):
            return visitor.visit_Value(self)

    class Visitor(doorbell.WrappingVisitor):
        def _wrap_each_pre(*args, **kwargs):
            raise NotImplementedError()

        @doorbell.Visitor.non_visitor_method
        def visit_Value(self, obj):
            return obj.value

    def test_visitor_method(self):
        v = self.Value(1)
        a = self.Visitor()
        assert v.accept(a) == 1


class TestBasicWrapping:
    class Value(doorbell.Visitee):
        def __init__(self, value=0):
            self.value = value

        def accept(self, visitor):
            return visitor.visit_Value(self)

    class Visitor(doorbell.WrappingVisitor):
        def visit_Value(self, obj):
            return obj.value

    def test_visitor_method(self):
        v = self.Value(1)
        a = self.Visitor()
        assert v.accept(a) == 1
