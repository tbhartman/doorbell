import doorbell
import doorbell.visitee
import pytest


class TestVisitorDecorator:
    class Value(doorbell.Visitee):
        def __init__(self, value=0):
            self.value = value

        def _accept(self, visitor):
            return visitor.goto_Value

    class Visitor(doorbell.Visitor):
        @doorbell.Visitor.visitor_method
        def goto_Value(self, obj):
            return obj.value

    def test_visitor_method(self):
        v = self.Value(1)
        a = self.Visitor()
        assert v.accept(a) == 1


class TestErrors:
    class MyError(Exception):
        pass

    @doorbell.Visitee.create
    class Value1(object):
        pass

    @doorbell.Visitee.create
    class Value2(object):
        pass

    class Visitor1(doorbell.Visitor):
        def visit_Value1(self, *args, **kwargs):
            raise TestErrors.MyError()

    class Visitor2(Visitor1):
        def onNotImplementedError(self, *args, **kwargs):
            return NotImplemented, args, kwargs

        def onError(self, *args, **kwargs):
            return args, kwargs

    class Value3(doorbell.Visitee):
        def _accept(self, visitor):
            raise AttributeError('')

    def test_attribute_error_during_accept(self):
        a3 = self.Value3()
        v1 = self.Visitor1()
        with pytest.raises(NotImplementedError):
            a3.accept(v1)

    def test_default_onError(self):
        a1 = self.Value1()
        v1 = self.Visitor1()
        with pytest.raises(self.MyError):
            a1.accept(v1)

    def test_default_onNotImplemented(self):
        a2 = self.Value2()
        v1 = self.Visitor1()
        with pytest.raises(NotImplementedError):
            a2.accept(v1)

    def test_custom_onNotImplemented(self):
        a2 = self.Value2()
        v2 = self.Visitor2()

        ret = a2.accept(v2, 1, a=1)
        assert ret[0] == NotImplemented
        assert ret[1][0] == a2
        assert isinstance(ret[1][1], NotImplementedError)
        assert ret[1][2] == 'visit_Value2'
        assert ret[1][3] == 1
        assert ret[2] == {'a': 1}

    def test_custom_onError(self):
        a1 = self.Value1()
        v2 = self.Visitor2()

        ret = a1.accept(v2, 1, a=1)
        assert ret[0][0] == a1
        assert isinstance(ret[0][1], self.MyError)
        assert ret[0][2] == 1
        assert ret[1] == {'a': 1}


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
