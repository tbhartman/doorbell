import abc
import functools

from . import _version
from . import _six

name = 'doorbell'
__version__ = _version.get_versions()['version']


class Visitee(_six.with_metaclass(abc.ABCMeta, object)):
    @abc.abstractmethod
    def accept(self, visitor):
        """accept a `Visitor`

        Call the appropriate `Visitor.visit_*` method and return the result.

        Args:
            visitor (Visitor): the visitor to accept Returns:
            any value returned by the visitor

        """
        raise NotImplementedError()


class _VisitorMethod(object):
    """a method that is used as a visitor

    Internal type to mark a method as a visitor method.  By default, all
    methods named "visit_*" will be marked as a visitor method.  If `skip` is
    True, this method will *not* be wrapped as a visitor method.

    Attributes:
        function (Callable): the visitor method
        skip (bool): if True, this method is not used as a visitor

    Args:
        function (Callable): the visitor method
        skip (bool): default False

    """
    def __init__(self, function, skip=False):
        self.function = function
        # skip is currently not used, but I can't resist
        self.skip = skip


class _MetaVisitor(type):
    def __init__(cls, name, bases, attrs):
        for k, v in attrs.items():
            if isinstance(v, _VisitorMethod):
                v = v.function
            elif k.startswith('visit_'):
                v = cls.visitor_method(v).function
            attrs[k] = v
            setattr(cls, k, v)
        super(_MetaVisitor, cls).__init__(name, bases, attrs)


class Visitor(_six.with_metaclass(_MetaVisitor, object)):
    """A basic visitor.

    This implementation does nothing special, but provides groundwork for
    child classes.

    Attributes:
        _visiting (bool): whether this is currently visiting a visitee

    """
    def __init__(self, *args, **kwargs):
        super(Visitor, self).__init__(*args, **kwargs)
        self._visiting = False

    @classmethod
    def visitor_method(cls, func):
        """Wrapper to mark non-default method as a visitor method.

        >>> class MyClass(Visitor):
        ...    @Visitor.visitor_method
        ...    def unusual_method_name(self, subject):
        ...        pass

        """
        # wrap func with _visit_wrapper
        wrapper = _six.partialmethod(cls._visit_wrapper, function=func)
        wrapper = functools.wraps(func)(wrapper)
        # mark as a visitor method
        return _VisitorMethod(wrapper)

    @classmethod
    def non_visitor_method(cls, func):
        """Wrapper to mark method as *not* a visitor method.

        >>> class MyClass(Visitor):
        ...    @Visitor.non_visitor_method
        ...    def visit_DontUseThisMethod(self, subject):
        ...        pass

        """
        return _VisitorMethod(func, skip=True)

    def _visit_wrapper(self, *args, **kwargs):
        """Wrapper for visitor methods.

        This method wraps all visitor methods.  This is intended to be
        overridden, and need not be called when overridden.  The wrapped
        method is always passed in as a keyword argument `function`.  This
        must pass all other positional and keyword arguments to that function.

        Args:
            function: the function to wrap; always passed as keyword argument

        """
        return kwargs.pop('function')(self, *args, **kwargs)


class WrappingVisitor(Visitor):
    """A visitor class that wraps each call with pre and post methods.

    """
    def _visit_wrapper(self, *args, **kwargs):
        func = kwargs['function']
        if self._visiting:
            pre = self._wrap_each_pre
            post = self._wrap_each_post
            return post(func(self, *pre(*args)))
        else:
            self._visiting = True
            pre = self._wrap_all_pre
            post = self._wrap_all_post
            try:
                return post(self._visit_wrapper(*pre(*args), **kwargs))
            finally:
                self._visiting = False

    def _wrap_each_pre(self, *args):
        """Method called before each visit.

        Returns:
            all arguments to be passed to visitor method

        """
        return args

    def _wrap_each_post(self, arg):
        """Method called after each visit.

        Returns:
            return value from each visitor method

        """
        return arg

    def _wrap_all_pre(self, *args):
        """Method called before any visit method is called.

        This is the first method called when a visitor method is called.

        Returns:
            arguments passed to :func:`_wrap_each_pre`

        """
        return args

    def _wrap_all_post(self, arg):
        """Method called after all visit methods are called.

        This is the last method called when a visitor method is called.

        Returns:
            final return value from a visitor method call

        """
        return arg


class CascadingVisitor(WrappingVisitor):
    """Visits children first.

    This visitor visits all child nodes of a visitee first, cascading through
    all children.

    Visitor methods are passed the visitee, then a list of return values from
    visiting the children, then all remaining arguments.

    """
    def _gather_children(self, subject):
        """Gather children from a visitee.

        Default implementation simply returns `subject.children`.

        """
        return subject.children

    def _wrap_each_pre(self, subject, *args):
        children = [c.accept(self) for c in self._gather_children(subject)]
        args = list(args)
        args.insert(0, children)
        args.insert(0, subject)
        return args
