from builtins import int, str, super

import ctypes
import copy
import enum
import logging

from collections.abc import Iterable
from ctypes import (c_char, c_char_p, c_double, c_size_t, c_int64, pointer,
                    POINTER)

import six

from ..tecutil import _tecutil, _tecutil_connector
from ..constant import *
from ..exception import *
from .. import tecutil, version
from ..tecutil import sv


log = logging.getLogger(__name__)


@tecutil.lock(with_recording=False)
def set_style(value, *args, **kwargs):
    if __debug__:
        assert len(args) < 7, ', '.join(args)
        if isinstance(value, int):
            if value < tecutil.minint64 or tecutil.maxuint64 < value:
                raise TecplotOverflowError('Integer outside of valid range.')

        if log.getEffectiveLevel() < logging.INFO:
            msg = 'SetStyle\n'
            msg += '  value: {}\n'.format(value)
            for a in args:
                msg += '  {} {}\n'.format(type(a), a)
            for k, v in kwargs.items():
                msg += '  {} : {} {}\n'.format(k, type(v), v)
            log.debug(msg[:-1])

            _tecutil_connector._style_call_count['SET'][' '.join(args)] += 1

    with tecutil.ArgList() as arglist:

        allocd = []
        try:
            for i, p in enumerate(args):
                arglist[getattr(sv, 'P' + str(i + 1))] = p

            if isinstance(value, enum.Enum):
                arglist[sv.IVALUE] = c_size_t(value.value)
            elif isinstance(value, tecutil.Index):
                arglist[sv.IVALUE] = c_size_t(value + 1)
            elif isinstance(value, (int, bool)):
                arglist[sv.IVALUE] = c_size_t(value)
            elif isinstance(value, float):
                arglist[sv.DVALUE] = value
            elif isinstance(value, six.string_types):
                arglist[sv.STRVALUE] = value
            elif hasattr(value, '__iter__'):
                value_list = list(value)
                if not len(value_list) or isinstance(value_list[0], int):
                    value_obj = tecutil.IndexSet(*value_list)
                    allocd.append(value_obj)
                    arglist[sv.IVALUE] = c_size_t(value_obj.value)
                else:
                    value_obj = tecutil.StringList(*value_list)
                    allocd.append(value_obj)
                    arglist[sv.IVALUE] = c_size_t(ctypes.addressof(
                        ctypes.cast(value_obj, POINTER(c_size_t)).contents))
            elif value is None:
                arglist[sv.IVALUE] = c_size_t(0)
            else:
                raise TecplotTypeError

            for k, v in kwargs.items():
                k = k.upper()
                if k == sv.UNIQUEID:
                    v = c_size_t(v)
                elif k in [sv.OBJECTSET]:
                    v = tecutil.IndexSet(*v)
                    allocd.append(v)
                elif k in [sv.OFFSET1, sv.OFFSET2]:
                    v = v + 1
                arglist[k] = v

            if __debug__:
                if log.getEffectiveLevel() < logging.INFO:
                    msg = 'SetStyle\n'
                    for k, v in arglist.items():
                        msg += '  {}: {}\n'.format(k, v)
                    log.debug(msg[:-1])

            try:
                res = _tecutil.StyleSetLowLevelX(arglist)
                if res not in [SetValueReturnCode.Ok,
                               SetValueReturnCode.DuplicateValue]:
                    if __debug__:
                        msg = 'SetStyle\n'
                        for k, v in arglist.items():
                            msg += '  {}: {}\n'.format(k, v)
                        raise TecplotSystemError(str(res) + '\n' + msg)
                    raise TecplotSystemError(res)
            except TecplotLogicError as e:
                if __debug__:
                    msg = 'SetStyle\n'
                    for k, v in arglist.items():
                        msg += '  {}: {}\n'.format(k, v)
                    raise TecplotLogicError(str(e) + '\n' + msg)
                else:
                    raise

        finally:
            for a in allocd:
                a.dealloc()


def get_style(return_type, *args, **kwargs):
    if __debug__:
        assert len(args) < 7

        if log.getEffectiveLevel() < logging.INFO:
            msg = 'GetStyle\n'
            for a in args:
                msg += '  {} {}\n'.format(type(a), a)
            for k, v in kwargs.items():
                msg += '  {} : {} {}\n'.format(k, type(v), v)
            log.debug(msg[:-1])

            _tecutil_connector._style_call_count['GET'][' '.join(args)] += 1

    with tecutil.ArgList() as arglist:

        allocd = []
        try:

            for i, p in enumerate(args):
                arglist[getattr(sv, 'P' + str(i + 1))] = p

            for k, v in kwargs.items():
                k = k.upper()
                if k == sv.UNIQUEID:
                    v = c_size_t(v)
                elif k in [sv.OBJECTSET]:
                    v = tecutil.IndexSet(*v)
                    allocd.append(v)
                elif k in [sv.OFFSET1, sv.OFFSET2]:
                    v = v + 1
                arglist[k] = v

            if (return_type in [int, bool, tecutil.Index, list, set] or
                    issubclass(return_type, enum.Enum)):
                arglist[sv.IVALUE] = pointer(c_size_t())
            elif return_type in [str]:
                arglist[sv.IVALUE] = pointer(pointer(c_char()))
            elif return_type in [float]:
                arglist[sv.DVALUE] = pointer(c_double())
            else:
                raise TecplotTypeError('unknown return_type: {}'.format(return_type))

            if __debug__:
                if log.getEffectiveLevel() < logging.INFO:
                    msg = 'GetStyle\n'
                    for k, v in arglist.items():
                        msg += '  {}: {}\n'.format(k, v)
                    log.debug(msg[:-1])

            try:
                res = _tecutil.StyleGetLowLevelX(arglist)
                if res is not GetValueReturnCode.Ok:
                    raise TecplotSystemError(res)
            except TecplotLogicError as e:
                if __debug__:
                    msg = 'GetStyle\n'
                    for k, v in arglist.items():
                        msg += '  {}: {}\n'.format(k, v)
                    raise TecplotLogicError(str(e) + '\n' + msg)
                else:
                    raise

            if return_type in [str]:
                ivalue = ctypes.cast(arglist[sv.IVALUE], POINTER(c_char_p))
                result = ivalue.contents.value
                if result not in [None, '']:
                    result = result.decode('utf-8')
            elif issubclass(return_type, enum.Enum):
                ival = arglist[sv.IVALUE]
                val = ctypes.cast(ival, POINTER(c_int64)).contents.value
                result = return_type(int(val))
            elif return_type in [tecutil.Index]:
                ival = arglist[sv.IVALUE]
                val = ctypes.cast(ival, POINTER(c_int64)).contents.value
                result = return_type(int(val) - 1)
            elif return_type in [list, set]:
                ptr = ctypes.cast(arglist[sv.IVALUE], POINTER(tecutil.IndexSet))
                iset = ptr.contents
                result = return_type(iset)
                iset.dealloc()
            elif return_type in [int, bool]:
                result = return_type(arglist[sv.IVALUE].contents.value)
            else:  # if return_type in [float]:
                result = return_type(arglist[sv.DVALUE].contents.value)

            if __debug__:
                if log.getEffectiveLevel() < logging.INFO:
                    log.debug('GetStyle result: {}'.format(result))

            return result

        finally:
            for a in allocd:
                a.dealloc()


@tecutil.lock_attributes
class Style(object):
    def __init__(self, *svargs, **kwargs):
        self._sv = list(tecutil.flatten_args(*svargs))
        uniqueid = kwargs.pop('uniqueid', None)
        offset1 = kwargs.pop('offset1', None)
        offset2 = kwargs.pop('offset2', None)
        objectset = kwargs.pop('objectset', None)

        assert not (offset1 and objectset), \
            'offset1 and objectset are mutually exclusive'
        assert not (offset2 and not (offset1 or objectset)), \
            'offset2 requires offset1 or objectset to also be specified'

        self._style_attrs = {}
        if uniqueid is not None:
            self._style_attrs[sv.UNIQUEID] = int(uniqueid)
        if offset1 is not None:
            self._style_attrs[sv.OFFSET1] = tecutil.Index(offset1)
        if offset2 is not None:
            self._style_attrs[sv.OFFSET2] = tecutil.Index(offset2)
        if objectset is not None:
            self._style_attrs[sv.OBJECTSET] = set(objectset)

    @property
    def _kw(self):
        return {k.lower(): v for k, v in self._style_attrs.items()}

    def _get_style(self, rettype, *svargs, **kwargs):
        svargs = self._sv + list(svargs)
        kw = self._style_attrs.copy()
        kw.update(**kwargs)
        if sv.OBJECTSET in kw:
            objectset = kw.pop(sv.OBJECTSET)
            result = []
            for offset1 in sorted(objectset):
                kw[sv.OFFSET1] = tecutil.Index(offset1)
                result.append(get_style(rettype, *svargs, **kw))
            return tuple(result)
        else:
            return get_style(rettype, *svargs, **kw)

    def _set_style(self, value, *svargs, **kwargs):
        svargs = self._sv + list(svargs)
        kw = self._style_attrs.copy()
        kw.update(**kwargs)
        set_style(value, *svargs, **kw)


@tecutil.lock_attributes
class SubStyle(object):
    def __init__(self, parent, *svargs):
        self.parent = parent
        self._svargs = list(tecutil.flatten_args(*svargs))

    def __eq__(self, that):
        return (isinstance(that, type(self))
                and self.parent == that.parent
                and self._svargs == that._svargs)

    def __ne__(self, that):
        return not (self == that)

    def _get_style(self, rettype, *svargs, **kwargs):
        svargs = self._svargs + list(tecutil.flatten_args(*svargs))
        return self.parent._get_style(rettype, *svargs, **kwargs)

    def _set_style(self, value, *svargs, **kwargs):
        svargs = self._svargs + list(tecutil.flatten_args(*svargs))
        self.parent._set_style(value, *svargs, **kwargs)


class StyleConfig(Style):
    """Runtime Configuration Control Base Class."""
    def __init__(self, name=None, *svargs):
        if svargs:
            Style.__init__(self, *svargs)
        self._ns = name.split('.') if name else []

    def __setattr__(self, name, value):
        if not name.startswith('_'):
            if not hasattr(self, '_keys'):
                self._keys = list(filter(lambda x: not x.startswith('_'), dir(self)))
            if name not in self._keys:
                msg = 'No configuration found: '
                raise TecplotAttributeError(msg + '.'.join(self._ns + [name]))
        super().__setattr__(name, value)

    @property
    def _opts(self):
        if not hasattr(self, '_attrs'):
            configs, props = [], []
            for key in filter(lambda x: not x.startswith('_'), dir(self)):
                value = getattr(self, key)
                if isinstance(value, StyleConfig):
                    configs.append((key, value))
                else:
                    props.append(key)
            self._attrs = (sorted(configs), sorted(props))
        return self._attrs

    def __str__(self):
        configs, props = self._opts
        lines = []
        for keyname in props:
            key = '.'.join(self._ns + [keyname])
            lines.append('{} = {}'.format(key, getattr(self, keyname)))
        for _, value in configs:
            lines.append(str(value))
        return '\n'.join(lines)


def style_property(value_type, svarg, value_cast=None):
    def getter(self):
        return self._get_style(value_type, svarg)

    if value_cast:
        def setter(self, val):
            val = value_cast(val)
            if val is not None:
                self._set_style(val, svarg)
    else:
        def setter(self, val):
            if val is not None:
                self._set_style(value_type(val), svarg)

    return property(getter, setter)


class NamedTupleStyle(SubStyle, Iterable):
    def __len__(self):
        return len(self._keys)

    def __getitem__(self, index):
        if isinstance(index, slice):
            rng = range(index.start or 0,
                        index.stop or len(self),
                        index.step or 1)
            return tuple([self[x] for x in rng])
        else:
            return getattr(self, self._keys[index])

    def __setitem__(self, index, value):
        if isinstance(index, slice):
            for i in range(index.start or 0,
                           index.stop or len(self),
                           index.step or 1):
                self[i] = value[i] if i < len(value) else None
        else:
            setattr(self, self._keys[index], value)

    def __iter__(self):
        self._current_index = -1
        return self

    def __next__(self):
        self._current_index += 1
        if self._current_index < len(self):
            return self.__getitem__(self._current_index)
        else:
            del self._current_index
            raise StopIteration()

    def next(self): # if sys.version_info < (3,)
        return self.__next__()

    def __str__(self):
        return '({})'.format(', '.join(str(x) for x in self))

    def __eq__(self, other):
        return (len(self) == len(other)
                and all(a == b for a, b in zip(self, other)))


class NamedVectorStyle(NamedTupleStyle):
    def __neg__(self):
        return tuple([-v for v in self])

    def __add__(self, other):
        return tuple([a - b for a, b in zip(self, other)])

    def __sub__(self, other):
        return tuple([a - b for a, b in zip(self, other)])

    def __iadd__(self, other):
        for k, v in zip(self._keys, other):
            setattr(self, k, getattr(self, k) + v)
        return self

    def __isub__(self, other):
        for k, v in zip(self._keys, other):
            setattr(self, k, getattr(self, k) - v)
        return self


class IndependentVariableLimits(NamedTupleStyle):
    _keys = ('min', 'max')
    min = style_property(float, sv.INDVARMIN)
    max = style_property(float, sv.INDVARMAX)


class IJK(NamedVectorStyle):
    _keys = ('i', 'j', 'k')
    i = style_property(int, sv.I)
    j = style_property(int, sv.J)
    k = style_property(int, sv.K)


class IJKMaxFract(NamedTupleStyle):
    _keys = ('i', 'j', 'k')
    i = style_property(float, sv.IMAXFRACT)
    j = style_property(float, sv.JMAXFRACT)
    k = style_property(float, sv.KMAXFRACT)


class IJKMinFract(NamedTupleStyle):
    _keys = ('i', 'j', 'k')
    i = style_property(float, sv.IMINFRACT)
    j = style_property(float, sv.JMINFRACT)
    k = style_property(float, sv.KMINFRACT)


class Limits(NamedTupleStyle):
    _keys = ('min', 'max')
    min = style_property(float, sv.MIN)
    max = style_property(float, sv.MAX)


class IndexIJK(NamedVectorStyle):
    _keys = ('i', 'j', 'k')
    i = style_property(tecutil.Index, sv.I)
    j = style_property(tecutil.Index, sv.J)
    k = style_property(tecutil.Index, sv.K)


class IndexRange(NamedTupleStyle):
    """Index range specification along some axis.

    This is similar to Python's :class:`slice` object except that ``max`` is
    included in the evaluated indexes. Here are some things to note:

        * All indices start with 0 and go to some maximum index ``m``.
        * Negative values represent the indexes starting with the maximum at -1
          and continuing back to the beginning of the range.
        * A step of `None`, 0 and 1 are all equivalent and mean that no elements
          are skipped.
        * A negative step indicates a skip less than the maximum.


    .. versionchanged:: 1.1
        **(Bug fix)** ``IndexRange`` max value of zero is now interpreted as
        the first index in the range instead of the last index. Prior to
        version 1.1, the ``max`` parameter interpreted zero to be the end of
        the range instead of the first element. This meant that an
        ``IndexRange`` of ``(0, 0, 1)`` would represent the whole range instead
        of just the first item. The standard way to represent the entire index
    """
    _keys = ('min', 'max', 'step')
    min = style_property(tecutil.Index, sv.MIN,
                         lambda x: tecutil.Index(x or 0))
    max = style_property(tecutil.Index, sv.MAX,
                         lambda x: tecutil.Index(-1 if x is None else x))
    step = style_property(int, sv.SKIP, lambda x: int(x or 1))


class RectPosition(NamedTupleStyle):
    _keys = ('x1', 'y1', 'x2', 'y2')
    x1 = style_property(float, sv.X1)
    y1 = style_property(float, sv.Y1)
    x2 = style_property(float, sv.X2)
    y2 = style_property(float, sv.Y2)


class RectSize(NamedTupleStyle):
    _keys = ('width', 'height')
    width = style_property(float, sv.WIDTH)
    height = style_property(float, sv.HEIGHT)


class SplineDerivativeAtEnds(NamedTupleStyle):
    _keys = ('start', 'end')
    start = style_property(float, sv.SPLINEDERIVATIVEATSTART)
    end = style_property(float, sv.SPLINEDERIVATIVEATEND)


class XY(NamedVectorStyle):
    _keys = ('x', 'y')
    x = style_property(float, sv.X)
    y = style_property(float, sv.Y)


class XYZ(NamedVectorStyle):
    _keys = ('x', 'y', 'z')
    x = style_property(float, sv.X)
    y = style_property(float, sv.Y)
    z = style_property(float, sv.Z)
