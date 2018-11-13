import doorbell
import pytest


def test_create_accept_invalid():
    with pytest.raises(ValueError):
        doorbell._create_accept("123")


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


class TestNoVisitorMethod:
    @doorbell.Visitee.create
    class Value(object):
        pass

    class Visitor(doorbell.Visitor):
        pass

    def test_it(self):
        a = self.Value()
        v = self.Visitor()

        with pytest.raises(AttributeError):
            a.accept(v)


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


class TestVisiteeAutoCreate:
    @doorbell.Visitee.auto_create
    class Value(object):
        pass

    class Value2(Value):
        pass

    class Visitor(doorbell.Visitor):
        def visit_Value(self, obj):
            return type(obj).__name__

        def visit_Value2(self, obj):
            return type(obj).__name__

    def test_method(self):
        v = self.Value()
        a = self.Visitor()
        assert v.accept(a) == 'Value'

    def test_method2(self):
        v = self.Value2()
        a = self.Visitor()
        assert v.accept(a) == 'Value2'


class TestVisiteeAutoCreateWithFunction:
    @doorbell.Visitee.auto_create(lambda i: i.upper())
    class Value(object):
        pass

    class Value2(Value):
        pass

    class Visitor(doorbell.Visitor):
        def visit_VALUE(self, obj):
            return type(obj).__name__

        def visit_VALUE2(self, obj):
            return type(obj).__name__

    def test_method(self):
        v = self.Value()
        a = self.Visitor()
        assert v.accept(a) == 'Value'

    def test_method2(self):
        v = self.Value2()
        a = self.Visitor()
        assert v.accept(a) == 'Value2'

    def test_invalid_function(self):
        with pytest.raises(ValueError):
            @doorbell.Visitee.auto_create(1)
            class Value(object):
                pass


class TestVisiteeMultipleAutoCreate:
    class ValueNonAuto(doorbell.Visitee):
        pass

    @doorbell.Visitee.auto_create
    class Value(object):
        pass

    @doorbell.Visitee.auto_create(lambda i: i.upper())
    class ValueUpper(Value):
        pass

    class ValueUpper2(ValueUpper):
        pass

    @doorbell.Visitee.auto_create
    class ValueNoMoreUpper(ValueUpper2):
        pass

    class Value2(Value):
        pass

    @doorbell.Visitee.auto_create
    class ValueAutoRepeat(Value):
        pass

    @doorbell.Visitee.stop_auto_create
    class ValueAutoStop(Value):
        pass

    @doorbell.Visitee.stop_auto_create
    class ValueAutoStop2(ValueAutoStop):
        pass

    class Visitor(doorbell.Visitor):
        def _get(self, obj):
            return type(obj).__name__

        def visit_Value(self, obj):
            return 'Value', self._get(obj)

        def visit_Value2(self, obj):
            return self._get(obj)

        def visit_ValueAutoRepeat(self, obj):
            return self._get(obj)

        def visit_ValueNoMoreUpper(self, obj):
            return self._get(obj)

        def visit_VALUEUPPER(self, obj):
            return self._get(obj)

        def visit_VALUEUPPER2(self, obj):
            return self._get(obj)

    def test_auto_repeat(self):
        a = self.Value()
        b = self.ValueAutoRepeat()
        v = self.Visitor()

        assert a.accept(v) == ('Value', 'Value')
        assert b.accept(v) == 'ValueAutoRepeat'

    def test_change_function(self):
        a = self.Value()
        b = self.Value2()
        c = self.ValueUpper()
        d = self.ValueUpper2()
        v = self.Visitor()

        assert a.accept(v) == ('Value', 'Value')
        assert b.accept(v) == 'Value2'
        assert c.accept(v) == 'ValueUpper'
        assert d.accept(v) == 'ValueUpper2'

    def test_reset_auto(self):
        a = self.Value()
        b = self.ValueNoMoreUpper()
        v = self.Visitor()

        assert a.accept(v) == ('Value', 'Value')
        assert b.accept(v) == 'ValueNoMoreUpper'

    def test_stop_auto(self):
        b = self.ValueAutoStop()
        v = self.Visitor()

        assert b.accept(v) == ('Value', 'ValueAutoStop')

    def test_stop_auto_without_auto_create(self):

        with pytest.raises(ValueError):
            @doorbell.Visitee.stop_auto_create
            class ClassStopAutoNonAuto(self.ValueNonAuto):
                pass
