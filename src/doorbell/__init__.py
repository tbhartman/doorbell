"""A visitor-pattern helper module.

"""
import abc
import collections
import functools
import inspect
import re
import textwrap

from . import _version
from . import _six

name = 'doorbell'
__version__ = _version.get_versions()['version']


def _create_accept(name):
    """create an accept method from visitor method name

    The created method calls the visitor method named
    "visit_<name>".

    Args:
        name (str): visitor method suffix

    Raises:
        ValueError: if name is invalid.  name must be a string with only
                    alphanumeric characters or an underscore

    """
    name = str(name)

    accept_definition = textwrap.dedent("""
        def accept(self, visitor):
            return visitor.visit_{0!s}(self)
        """.format(name))

    # check string before eval
    basic = "[A-Za-z_][A-Za-z0-9_]*"
    name_re = re.compile('^' + basic + '$')
    name_match = name_re.match(name)
    accept_re = re.compile(
        r'^ *return visitor.' + basic + r'\(self\)$',
        re.MULTILINE)
    accept_match = accept_re.search(accept_definition)
    if name_match is None or accept_match is None:
        raise ValueError('Invalid visitor method name ' + name)

    locals_ = {}
    globals_ = {}
    exec(accept_definition, globals_, locals_)
    locals_['accept']._autocreate = name
    return locals_['accept']


class _MetaVisitee(abc.ABCMeta):
    def __new__(cls, *args, **kwargs):
        name, bases, attrs = args[:3]
        if 'accept' not in attrs:
            has_auto = [hasattr(i, '_visitee_auto_names') for i in bases]
            if any(has_auto):
                parent = bases[has_auto.index(True)]
                if parent._visitee_auto_function is None:
                    # auto_create has been stopped
                    pass
                else:
                    accept_name = parent._visitee_auto_function(name)
                    parent._visitee_auto_names[accept_name] += 1
                    if parent._visitee_auto_names[accept_name] > 1:
                        msg = ("Visitor method name already used: " +
                               accept_name)
                        raise ValueError(msg)
                    accept = _create_accept(accept_name)
                    attrs['accept'] = accept
        return super(_MetaVisitee, cls).__new__(cls, *args, **kwargs)


class Visitee(_six.with_metaclass(_MetaVisitee, object)):
    """a visited object"""
    @staticmethod
    def stop_auto_create(arg):
        """Stop auto-creating accept methods

        Raises:
            ValueError: if auto_create was not used on a parent class

        """
        return Visitee.auto_create(arg, stop=True)

    @staticmethod
    def auto_create(arg, function=None, stop=False):
        """Decorator to automatically create accept methods on subclasses

        Also creates on the current class.  Single argument can be a callable
        (see :func:`Visitee.create`).  The argument *cannot* be a string.

        Args:
            arg (callable): optional argument
            function: *internal use*
            stop: *internal use*

        Raises:
            ValueError: if a subclass creates an accept method that uses
                        an already used visitor method name
            ValueError: if the function to generate a name creates an invalid
                        name

        >>> @Visitee.auto_create(lambda i: i.upper())
        ... class MyClass:
        ...     pass
        >>> class MyClAsS(MyClass):
        ...     pass
        Traceback (most recent call last):
        ...
        ValueError: Visitor method name already used: MYCLASS

        """
        if inspect.isclass(arg):
            if callable(function):
                name = function(arg.__name__)
            elif function is None:
                def function(i):
                    return i
                name = arg.__name__
            else:
                raise ValueError('Invalid argument ' + repr(function))

            attr = {}

            if stop:
                function = None
                if not (issubclass(arg, Visitee)
                        and hasattr(arg, '_visitee_auto_names')):
                    raise ValueError('auto_create not yet applied')
                else:
                    accept = arg.__dict__.get('accept')
                    if accept and getattr(accept, '_autocreate') is not None:
                        # need to remove auto-created-name
                        arg._visitee_auto_names[accept._autocreate] -= 1
                    # create a super method
                    locals_ = {}
                    globals_ = {
                        'SuperClass': arg,
                        }
                    accept_definition = textwrap.dedent("""
                        def accept(self, visitor):
                            return super(SuperClass, self).accept(visitor)
                        """)
                    exec(accept_definition, globals_, locals_)
                    attr['accept'] = locals_['accept']
                    attr['accept']._autocreate = None
            else:
                attr['accept'] = _create_accept(name)

            attr['_visitee_auto_function'] = staticmethod(function)

            if not (issubclass(arg, Visitee)
                    and hasattr(arg, '_visitee_auto_names')):
                # auto_create has not yet been applied
                bases = (arg, Visitee)
                attr['_visitee_auto_names'] = collections.Counter((name,))
            else:
                # if else, this is overriding a previous auto_create
                bases = (arg, )
            return type(arg.__name__, bases, attr)
        else:
            return functools.partial(Visitee.auto_create, function=arg)

    @staticmethod
    def create(arg, name=None):
        """Decorator to create accept method on class

        Pass a string as the argument so that the accept method calls
        `visit_<arg>` on the visitor:

        >>> @Visitee.create('Person')
        ... class Tom:
        ...    # def accept(self, visitor):
        ...    #     return visitor.visit_Person(self)
        ...    pass

        Pass a callable to name the visitor method as a function of the
        decorated class's name.  The class name is passed to the callable; the
        result is used to name the method as `visit_<result>`:

        >>> @Visitee.create(lambda i: i.upper())
        ... class Richard:
        ...    # def accept(self, visitor):
        ...    #     return visitor.visit_RICHARD(self)
        ...    pass

        Use the decorator directly:

        >>> @Visitee.create
        ... class Bob:
        ...    # def accept(self, visitor):
        ...    #     return visitor.visit_Bob(self)
        ...    pass

        Args:
            arg (callable|str): optional argument
            name: *internal use*

        """
        if inspect.isclass(arg):
            if callable(name):
                name = name(arg.__name__)
            elif name is None:
                name = arg.__name__

            if issubclass(arg, Visitee):
                bases = (arg,)
            else:
                bases = (arg, Visitee)

            accept = _create_accept(name)
            return type(arg.__name__, bases, {'accept': accept})
        else:
            return functools.partial(Visitee.create, name=arg)

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
