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
