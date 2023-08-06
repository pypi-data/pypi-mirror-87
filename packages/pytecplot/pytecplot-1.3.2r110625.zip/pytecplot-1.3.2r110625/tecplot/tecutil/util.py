from builtins import int, str, super

import collections
import contextlib
import ctypes
import inspect
import logging
import os
import re
import tempfile
import textwrap
import warnings

from collections.abc import Iterable
from ctypes import cast, c_int, POINTER
from six import string_types

from ..exception import *
from ..constant import Color

log = logging.getLogger(__name__)

maxint64 = 2**(64 - 1) - 1
minint64 = -maxint64 - 1
maxuint64 = 2**64 - 1

IndexRange = collections.namedtuple('IndexRange', 'min max step')
IndexRange.__new__.__defaults__ = (None, None, None)

class Index(int):
    """Position identifier type.

    This type is used internally to represent a position in a list. It is
    used to indicate that a change between zero-based indexing and one-based
    indexing must occur at the TecUtil boundary.

    This type can be treated exactly like a Python native `int` and is only
    meaningful internally to the tecplot Python module.
    """

XY = collections.namedtuple('XY', ('x', 'y'))
XY.__new__.__defaults__ = (None, None)

XYZ = collections.namedtuple('XYZ', ('x', 'y', 'z'))
XYZ.__new__.__defaults__ = (None, None, None)

def flatten_args(*args):
    flatargs = []
    for a in args:
        if isinstance(a, Iterable) and not isinstance(a, string_types):
            flatargs += list(a)
        else:
            flatargs.append(a)
    return tuple(flatargs)


def array_to_enums(array_pointer, array_size, enum_type):
    indexes = cast(array_pointer, POINTER(c_int))
    return tuple(enum_type(indexes[i]) for i in range(array_size))


def inherited_property(cls):
    def _copy_property(prop):
        attr = getattr(cls, prop.__name__)
        return property(attr.fget, attr.fset, attr.fdel, prop.__doc__)
    return _copy_property


def lock_attributes(cls):
    """
    As a decorator of a class, this ensures that no new attributes are created
    after __init__() is called.
    """
    if __debug__:
        def _setattr(self, name, value):
            if not name.startswith('_') and name not in dir(self):
                stacknames = [f[0].f_code.co_name for f in inspect.stack()[:3]]
                if '__init__' not in stacknames:
                    msg = 'No attribute: {}.{}'
                    classname = self.__class__.__name__
                    raise TecplotAttributeError(msg.format(classname, name))
            return super(cls, self).__setattr__(name, value)
        cls.__setattr__ = _setattr
    return cls


_VarInfo = collections.namedtuple('_VarInfo', ('types', 'values', 'names'))


def check_arglist_argtypes(function_name, *args):
    for arg in args:
        vinfo = _VarInfo(*arg)
        for name, value in zip(vinfo.names, vinfo.values):
            if value is not None:
                if not isinstance(value, tuple(vinfo.types)):
                    errfmt = '{}: Type of  parameter {} must be one of: {}'
                    types = ', '.join(t.__name__ for t in vinfo.types)
                    errmsg = errfmt.format(function_name, name, types)
                    raise TecplotTypeError(errmsg)


def color_spec(color, plot=None):
    """
        color_spec(Color.Blue, plot)          --> Color.Blue
        color_spec(Color.MultiColor, plot)    --> plot.contour(0)
        color_spec(Color.MultiColor2, plot)   --> plot.contour(1)
        color_spec(Color.Blue)                --> Color.Blue
        color_spec(plot.contour(0))           --> Color.MultiColor
        color_spec(plot.contour(1))           --> Color.MultiColor2

        color_spec(plot.rgb_coloring)         --> Color.RGBColor
        color_spec(Color.RGBColor, plot)      --> plot.rgb_coloring
    """
    if isinstance(color, Iterable):
        return tuple([color_spec(c, plot) for c in color])
    color_spec._indexes = {
        Color.RGBColor: Index(Color.RGBColor.value),
        Color.MultiColor: Index(0),
        Color.MultiColor2: Index(1),
        Color.MultiColor3: Index(2),
        Color.MultiColor4: Index(3),
        Color.MultiColor5: Index(4),
        Color.MultiColor6: Index(5),
        Color.MultiColor7: Index(6),
        Color.MultiColor8: Index(7)}
    color_spec._multicolors = {v: k for k, v in color_spec._indexes.items()}
    try:
        if plot:
            if color == Color.RGBColor:
                return plot.rgb_coloring
            else:
                return plot.contour(color_spec._indexes[Color(color)])
        else:
            return color_spec._multicolors[Index(color.index)]
    except (AttributeError, KeyError):
        return Color(color)


def filled_slice(slice_, maxlen):
    """Convert start, stop, step in slice to real integers.

    None and negative values are converted to actual default values depending
    on the maxlen given.
    """
    if slice_.start is None:
        start = 0
    elif slice_.start < 0:
        start = maxlen + slice_.start
    else:
        start = slice_.start
    start = min(max(start, 0), maxlen)

    if slice_.stop is None:
        stop = maxlen
    elif slice_.stop < 0:
        stop = maxlen + slice_.stop
    else:
        stop = slice_.stop
    stop = min(max(stop, 0), maxlen)

    if slice_.step is None:
        step = 1
    else:
        step = min(max(slice_.step, 1), maxlen)

    return slice(start, stop, step)


def array_to_str(arr, maxlen=10):
    try:
        itr = iter(arr)
        item = next(itr)
        ret = '[' + str(item)
        for i, item in enumerate(itr, start=2):
            if i > maxlen:
                ret += ' ...'
                break
            ret += ', {}'.format(item)
        return ret + ']'
    except StopIteration:
        return '[]'
    except TypeError:
        return str(arr)


class ListWrapper(object):
    """Converts a list to a wrapped paragraph of items.

    Unlike textwrap.TextWrapper, items in the list are not broken over
    multiple lines even if they contain spaces.
    """
    def __init__(self, initial_indent='', subsequent_indent='    ',
                 initial_width=70, subsequent_width=70, delim=',',
                 prefix='', suffix=''):
        assert (len(prefix) + len(initial_indent)) < initial_width
        assert (len(suffix) + len(subsequent_indent)) < subsequent_width
        self.initial_indent = initial_indent
        self.subsequent_indent = subsequent_indent
        self.initial_width = initial_width
        self.subsequent_width = subsequent_width
        self.delim = delim
        self.prefix = prefix
        self.suffix = suffix

    def wrap(self, str_list):
        ret = []
        max_space = self.subsequent_width - len(self.subsequent_indent)

        line = "{}{}".format(self.prefix, self.initial_indent)

        itr = iter(str_list)
        try:
            item = next(itr)
            line += "'{}'".format(item)
        except StopIteration:
            pass  # no items in list

        space_left = self.initial_width - len(line)

        for item in itr:
            s = "{} '{}'".format(self.delim, str(item))
            if len(s) < space_left or max_space <= space_left:
                line += s
                space_left -= len(s)
            else:
                ret.append(line + self.delim)
                line = "{}'{}'".format(self.subsequent_indent, item)
                space_left = self.subsequent_width - len(line)

        if len(self.suffix) <= space_left:
            ret.append(line + self.suffix)
        else:
            ret.append(line)
            ret.append("{}{}".format(self.subsequent_indent, self.suffix))
        return ret

    def fill(self, str_list):
        return '\n'.join(self.wrap(str_list))


@contextlib.contextmanager
def optional(cls, args):
    """Context for optional arguments that can be None.

    In this example, variables is an optional parameter. If not `None`, then
    ``varset`` will be the result of ``IndexSet(*variables)``, if `None`, then
    ``varset`` will be `None`::

        def fn(variables=None):
            with optional(IndexSet, variables) as varset:
                _tecutil.Fn(varset)

    The ``cls`` parameter must be a class and must have the ``__enter__`` and
    ``__exit__`` methods implemented.
    """
    if args is None:
        yield None
    else:
        with cls(*flatten_args(args)) as obj:
            yield obj


def split_macro(source):
    """Split macro code into a list of commands."""
    comments = re.compile(r'(?<!\\)(\".*?\"|\'.*?\')|(#[^\r\n]*$)', re.MULTILINE)
    pattern = re.compile(r'(\$!.*?)(?=\$!)|(\$!.*)', re.MULTILINE | re.DOTALL)
    source = comments.sub(lambda m: m.group(1) or '', source)
    for match in pattern.finditer(source):
        yield (match.group(1) or match.group(2)).strip()


def normalize_path(nodepath):
    """Convert relative paths to absolute and normalize.

    Always use Python's current working directory to convert to absolute paths.
    However, relative paths are disallowed when connected to a non-local
    instance of the TecUtil Server.
    """
    if nodepath is not None:
        nodepath = str(nodepath)
        from tecplot.tecutil import _tecutil_connector
        if _tecutil_connector.connected:
            if _tecutil_connector.client.host not in ['localhost', '127.0.0.1']:
                if not os.path.isabs(nodepath):
                    msg = 'paths must be absolute when connected to Tecplot 360'
                    raise TecplotLogicError(msg)
        return os.path.abspath(nodepath)


@contextlib.contextmanager
def temporary_closed_file(suffix=None):
    """A named temporary file that has been created and closed.

    The file will be removed on exit of the context.
    """
    ftmp = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
    try:
        ftmp.close()
        yield ftmp.name
    finally:
        try:
            os.remove(ftmp.name)
        except OSError as e:
            msg = 'Temp file I/O error: {}'.format(e)
            warnings.warn(msg)


def api_changed(msg, version_changed, sdk_version_changed, warning=False):
    msg = textwrap.dedent('''\
    PyTecplot API Change (version {})
    Tecplot 360 version: {}
    {}
    ''').format(version_changed, sdk_version_changed, textwrap.fill(msg))
    if warning:
        if __debug__:
            msg += 'Please update your code as the legacy interface will\n' \
                +  'be removed in the next major release of PyTecplot.'
            warnings.warn(msg, TecplotFutureWarning)
    else:
        raise TecplotInterfaceChangeError(msg)


def api_moved(old, new, version_changed, sdk_version_changed, warning=False):
    msg = textwrap.dedent('''\
    PyTecplot API Change (version {})
    Tecplot 360 version: {}
        {} has been moved to {}
    ''').format(version_changed, sdk_version_changed, old, new)
    if warning:
        if __debug__:
            msg += 'Please update your code as the legacy interface will\n' \
                +  'be removed in the next major release of PyTecplot.'
            warnings.warn(msg, TecplotFutureWarning)
    else:
        raise TecplotInterfaceChangeError(msg)
