from builtins import str, super

import copy
import logging

from six import string_types
from ctypes import c_void_p, cast, pointer

from .tecutil_connector import _tecutil_connector, _tecutil
from .util import flatten_args
from .. import constant
from ..exception import TecplotTypeError


log = logging.getLogger(__name__)


class StringList(c_void_p):
    def __init__(self, *strings):
        super().__init__(_tecutil.StringListAlloc())
        self += flatten_args(*filter(lambda x: x, strings))

    @staticmethod
    def _bind_tecutil():
        try:
            _tecutil.handle.tecUtilArgListGetStringListByIndex.restype = StringList
        except AttributeError:
            pass

        if _tecutil_connector.client is not None:
            _ArgListGetStringListByIndex = _tecutil_connector.client.ArgListGetStringListByIndex
            def ArgListGetStringListByIndex(*a, **kw):
                return cast(_ArgListGetStringListByIndex(*a, **kw), StringList)
            _tecutil_connector.client.ArgListGetStringListByIndex = ArgListGetStringListByIndex

        if not hasattr(_tecutil, '_CustomLabelsGet'):
            _tecutil._CustomLabelsGet = _tecutil.CustomLabelsGet
            def CustomLabelsGet(*a, **kw):
                success, ptr = _tecutil._CustomLabelsGet(*a, **kw)
                if not success:
                    raise TecplotSystemError()
                return cast(ptr, StringList)
            _tecutil.CustomLabelsGet = CustomLabelsGet

    # data access
    def __getitem__(self,i):
        return _tecutil.StringListGetRawStringPtr(self, i+1)

    def __len__(self):
        return _tecutil.StringListGetCount(self)

    def __eq__(self, other):
        if len(self) != len(other):
            return False
        for i in self:
            if i not in other:
                return False
        return True

    # string representations
    def __repr__(self):
        return 'StringList({args})'.format(args=', '.join("'{arg}'".format(arg=s) for s in self))

    def __str__(self):
        return str(list(self))

    # iterating
    def __iter__(self):
        obj = copy.copy(self) if hasattr(self, 'current_index') else self
        obj.current_index = -1
        obj.max_index = len(self)
        obj.iter_items = _tecutil.StringListToNLString(obj).split('\n')
        if len(obj.iter_items) != obj.max_index:
            del obj.iter_items
        return obj

    def __next__(self):
        self.current_index += 1
        if self.current_index < self.max_index:
            try:
                return self.iter_items[self.current_index]
            except (AttributeError, IndexError):
                return self.__getitem__(self.current_index)
        else:
            del self.current_index
            del self.max_index
            try:
                delattr(self, 'iter_items')
            except AttributeError:
                pass
            raise StopIteration()

    # context management
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.dealloc()

    # public methods
    def __iadd__(self, string_list):
        for s in string_list:
            self.append(s)
        return self

    def append(self,s):
        if not isinstance(s, string_types):
            raise TecplotTypeError('StringList can only hold strings')
        if hasattr(self, 'current_index'):
            raise TecplotLogicError('Cannot append to StringList while iterating over it')
        _tecutil.StringListAppendString(self, s)

    def clear(self):
        _tecutil.StringListClear(self)

    def dealloc(self):
        _tecutil.StringListDealloc(pointer(self))

    def next(self): # if sys.version_info < (3,)
        return self.__next__()
