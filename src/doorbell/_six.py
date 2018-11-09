# various 2to3 fixes
import functools

class partialmethod(object):
    def __init__(self, wrapped_function, *args, **kwargs):
        self.function = wrapped_function
        self.args = args
        self.kwargs = kwargs
    def __get__(self, instance, *args, **kwargs):
        if instance is None:
            return self
        else:
            return functools.partial(self.function, instance, *self.args, **self.kwargs)

# borrowed from six.py:
# Copyright (c) 2010-2018 Benjamin Peterson
# https://github.com/benjaminp/six
# commit: a611f60
def with_metaclass(meta, *bases):
    class metaclass(type):
        def __new__(cls, name, this_bases, d):
            return meta(name, bases, d)
        @classmethod
        def __prepare__(cls, name, this_bases):
            return meta.__prepare__(name, bases)
    return type.__new__(metaclass, 'temporary_class', (), {})
