import doorbell


class TestVisitorDecorator:
    class Value(doorbell.Visitee):
        def __init__(self, value=0):
            self.value = value

        def accept(self, visitor):
            return visitor.goto_Value(self)

    class Visitor(doorbell.Visitor):
        @doorbell.Visitor.visitor_method
        def goto_Value(self, obj):
            return obj.value

    def test_visitor_method(self):
        v = self.Value(1)
        a = self.Visitor()
        assert v.accept(a) == 1


class TestVisiteeCreate:
    @doorbell.Visitee.create
    class Value(object):
        pass

    @doorbell.Visitee.create('Value3')
    class Value2(object):
        pass

    class Visitor(doorbell.Visitor):
        def visit_Value(self, obj):
            return type(obj).__name__

        def visit_Value3(self, obj):
            return type(obj).__name__

    def test_method(self):
        v = self.Value()
        a = self.Visitor()
        assert v.accept(a) == 'Value'

    def test_method2(self):
        v = self.Value2()
        a = self.Visitor()
        assert v.accept(a) == 'Value2'
