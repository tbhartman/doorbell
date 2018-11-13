"""A visitor-pattern helper module.

"""
from ._version import get_versions
from .visitee import Visitee
from .visitor import Visitor, WrappingVisitor, CascadingVisitor

__version__ = get_versions()['version']

__all__ = [
    'CascadingVisitor',
    'Visitee',
    'Visitor',
    'WrappingVisitor',
    '__version__',
    ]
