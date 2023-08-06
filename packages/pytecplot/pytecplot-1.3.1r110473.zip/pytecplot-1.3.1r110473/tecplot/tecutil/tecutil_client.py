# coding: utf-8
from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
from builtins import *

import atexit
import contextlib
import logging
import sys
import textwrap
import zmq

from collections.abc import Iterable
from ctypes import *
from enum import Enum
from six import string_types

from . import message_pb2 as tecrpc

from ..constant import *
from ..exception import *
from .tecutil_rpc import TecUtilRPC, ValueType
from .util import Index


log = logging.getLogger(__name__)


def set_arglist_item(item, key, val):
    assert isinstance(key, string_types) or isinstance(key, c_char)

    if isinstance(key, c_char):
        item.key = key.value.decode('utf-8')
    else:
        item.key = key

    if isinstance(val, tecplot.tecutil.StringList):
        addr = getattr(val, 'value', val)
        set_address(item.value, tecrpc.Argument.StringList, addr)
    elif isinstance(val, tecplot.tecutil.IndexSet):
        addr = getattr(val, 'value', val)
        set_address(item.value, tecrpc.Argument.IndexSet, addr)
    elif isinstance(val, string_types):
        set_text(item.value, None, val)
    elif isinstance(val, (float, c_double)):
        set_scalar(item.value, c_double, val)
    elif isinstance(val, Index):
        set_scalar(item.value, c_int64, val+1)

    elif isinstance(val, POINTER(c_double)):  # POSSIBLY IN/OUTPUT
        item.value.type = tecrpc.Argument.Address | tecrpc.Argument.Float64
        item.value.float64 = val[0]

    elif isinstance(val, (int, bool)):
        set_scalar(item.value, c_int64, val)
    elif isinstance(val, Enum):
        set_scalar(item.value, c_int64, val.value)

    elif isinstance(val, c_size_t):  # POSSIBLY IN/OUTPUT
        set_arbparam(item.value, None, val)
    elif isinstance(val, POINTER(c_size_t)):  # POSSIBLY IN/OUTPUT
        ptr = cast(val, c_void_p)
        set_arbparam(item.value, POINTER, ptr.value)
    elif isinstance(val, POINTER(POINTER(c_char))):  # POSSIBLY IN/OUTPUT
        set_arbparam(item.value, POINTER, val.contents)
    elif isinstance(val, POINTER(c_char_p)):  # POSSIBLY IN/OUTPUT
        set_text(item.value, Argument.Address, val)

    else:
        if isinstance(val, Iterable):
            val = list(val)
        if isinstance(val, list):
            if isinstance(val[0], Enum):
                enum_values = [e.value for e in val]
                set_array(item.value, c_int32, enum_values)
            elif isinstance(val[0], float):
                set_array(item.value, c_double, val)
            elif len(val) == 0 or isinstance(val[0], int):
                set_array(item.value, c_int64, val)
            else:
                msg = 'invalid type: {} ({} = {})'
                msg = msg.format(type(val), key, val)
                raise TecplotTypeError(msg)
        else:
            msg = 'invalid type: {} ({} = {})'
            msg = msg.format(type(val), key, val)
            raise TecplotTypeError(msg)


def add_arglist(arg, arglist):
    assert isinstance(arglist, tecplot.tecutil.LocalArgList)
    arg.type = tecrpc.Argument.ArgList
    for key, val in arglist.items():
        item = arg.arglist.items.add()
        set_arglist_item(item, key, val)


def set_address(arg, argtype, value):
    if argtype is c_uint64:
        arg.type = tecrpc.Argument.Address
    else:
        arg.type = argtype | tecrpc.Argument.Address

    if value is None or value == 0:
        arg.type |= tecrpc.Argument.Null
    else:
        arg.uint64 = value


def set_arbparam(arg, argtype, value):
    assert argtype in [None, POINTER, tecrpc.Argument.Address]
    if isinstance(value, POINTER(c_char)):
        value = cast(value, c_char_p).value.decode('utf-8')
    is_addr = argtype is not None and (argtype is POINTER or
                                       argtype & tecrpc.Argument.Address)
    if isinstance(value, string_types):
        arg.type = tecrpc.Argument.ArbParam | tecrpc.Argument.Text
        if is_addr:
            arg.type |= tecrpc.Argument.Address
        arg.text = value or ''
    else:
        if is_addr:
            arg.type = tecrpc.Argument.ArbParam | tecrpc.Argument.Address
            arg.uint64 = value
        elif isinstance(value, Enum):
            arg.type = tecrpc.Argument.ArbParam | tecrpc.Argument.Enum
            arg.int64 = value.value
        else:
            arg.type = tecrpc.Argument.ArbParam
            arg.int64 = c_int64(int(getattr(value, 'value', value))).value


def set_array(arg, argtype, value):
    _types = {
        c_bool: tecrpc.Argument.Bool,
        c_uint8: tecrpc.Argument.UInt8,
        c_uint32: tecrpc.Argument.UInt32,
        c_uint64: tecrpc.Argument.UInt64,
        c_int32: tecrpc.Argument.Int32,
        c_int64: tecrpc.Argument.Int64,
        c_float: tecrpc.Argument.Float32,
        c_double: tecrpc.Argument.Float64}
    if value is None:
        arg.type = tecrpc.Argument.Unspecified if argtype is None else _types[argtype]
        arg.type |= tecrpc.Argument.Array | tecrpc.Argument.Null
    else:
        if argtype is None:
            arg.type = tecrpc.Argument.Array
            try:
                arg.type |= _types[value._type_]
            except KeyError:
                arg.type |= tecrpc.Argument.Unspecified
            arg.uint64 = len(value)
        else:
            arg.type = tecrpc.Argument.Array | _types[argtype]
            if isinstance(value, Array):
                # ctypes arrays are reinterpreted
                if value._type_ != argtype:
                    n, r = divmod(len(value) * sizeof(value._type_), sizeof(argtype))
                    if r:
                        raise TypeError('could not cast array to the requested type')
                    p = cast(value, POINTER(argtype))
                    a = (argtype * n).from_address(addressof(p.contents))
                    arg.buffer = bytes(bytearray(a))
                else:
                    arg.buffer = bytes(bytearray(value))
            else:
                # all other array types are cast to type argtype
                try:
                    import numpy as np
                    arr = np.array(value, dtype=argtype)
                    try:
                        arg.buffer = arr.tobytes()
                    except AttributeError:
                        # numpy.ndarray.tobytes() added in 1.9.0
                        arg.buffer = bytes(arr.tostring())
                except ImportError:
                    value = (argtype * len(value))(*value)
                    arg.buffer = bytes(bytearray(value))


def set_scalar(arg, argtype, value):
    _types = {
        c_bool: tecrpc.Argument.Bool,
        c_uint8: tecrpc.Argument.UInt8,
        c_uint32: tecrpc.Argument.UInt32,
        c_uint64: tecrpc.Argument.UInt64,
        c_int32: tecrpc.Argument.Int32,
        c_int64: tecrpc.Argument.Int64,
        c_float: tecrpc.Argument.Float32,
        c_double: tecrpc.Argument.Float64, }
    arg.type = _types[argtype]
    if arg.type == tecrpc.Argument.Bool:
        arg.boolean = value
    elif arg.type in [tecrpc.Argument.UInt8, tecrpc.Argument.UInt32]:
        arg.uint32 = value
    elif arg.type == tecrpc.Argument.UInt64:
        arg.uint64 = value
    elif arg.type == tecrpc.Argument.Int32:
        arg.int32 = value
    elif arg.type == tecrpc.Argument.Int64:
        arg.int64 = value
    elif arg.type == tecrpc.Argument.Float32:
        arg.float32 = value
    elif arg.type == tecrpc.Argument.Float64:
        arg.float64 = value
    else:
        raise TecplotNotImplementedError('cannot add scalar: {}'.format(type(value)))


def set_text(arg, argtype, value):
    assert argtype in [None, tecrpc.Argument.Address]
    if isinstance(value, c_char):
        value = value.value.decode('utf-8')
    arg.type = tecrpc.Argument.Text
    if argtype is not None and argtype & tecrpc.Argument.Address:
        arg.type |= tecrpc.Argument.Address
    if value is None:
        arg.type |= tecrpc.Argument.Null
    else:
        arg.text = value or ''


def add_args(request, *args):
    _dispatch = {
        ValueType.Address: set_address,
        ValueType.ArbParam: set_arbparam,
        ValueType.Array: set_array,
        ValueType.Scalar: set_scalar,
        ValueType.Text: set_text, }
    for valtype, argtype, value in args:
        arg = request.args.add()
        if isinstance(value, tecplot.tecutil.LocalArgList):
            assert argtype is c_uint64
            add_arglist(arg, value)
        else:
            _dispatch[valtype](arg, argtype, value)


def build_tecutil_request(request, tecutil_command, *args, **kwargs):
    request.operation = tecutil_command
    request.type = tecrpc.Request.TecUtil
    if any(isinstance(a[2], tecplot.tecutil.LocalArgList) for a in args):
        request.type |= tecrpc.Request.TecUtilX
    if kwargs.pop('lock', True):
        request.type |= tecrpc.Request.LockRequired
    add_args(request, *args)
    return request.type


class TecUtilClient(TecUtilRPC):
    def __init__(self):
        self.socket = None
        self.tuserver_version = 0
        self.sdk_version_info = (0, 0, 0, 0)
        self.suspended = False
        self.state_changes = {}

    def connect(self, host='localhost', port=7600, timeout=10, quiet=False):
        # Prepare the ZeroMQ context
        self._context = zmq.Context()

        # Setup the request server socket
        self.socket = self._context.socket(zmq.REQ)

        # Set high water mark for out-going messages.
        # This is the maximum number of messages to
        # store in the out-going queue - send() will
        # block until the HWM is below this limit.
        self.socket.setsockopt(zmq.SNDHWM, 10)

        # Do not linger once socket is closed.
        # Send messages immediately, and possibly
        # fail, but do not attempt to recover.
        self.socket.setsockopt(zmq.LINGER, 0)

        # Connect requester to the reply sever
        self.host = host
        self.endpoint = "tcp://{host}:{port}".format(host=host, port=port)
        self.socket.connect(self.endpoint)

        self.wait_for_connection(timeout, quiet)

        if self.connected:
            atexit.register(self.disconnect)

        # Bring in tecplot module only on connection to avoid circular deps
        import tecplot
        globals()['tecplot'] = tecplot

    def wait_for_connection(self, timeout=10, quiet=False):

        def post_message(msg, quiet=quiet):
            if not quiet:
                if log.getEffectiveLevel() <= logging.INFO:
                    log.info(msg)
                else:
                    print(msg)

        post_message(
            'Connecting to Tecplot 360 TecUtil Server on:\n    {}'.format(
                self.endpoint))

        if not self.is_server_listening(timeout):
            self.disconnect()
            raise TecplotTimeoutError('Failed to connect to TecUtil Server.')

        post_message('Connection established.')

    def is_server_listening(self, timeout=10):
        if self.socket is None:
            raise TecplotLogicError('Not connected to Tecplot 360.')

        # raw messages must be 255 characters or less
        RAWMSG = 0b00001010
        HANDSHAKE = b'UTHR?'
        buf = bytes([RAWMSG, len(HANDSHAKE)] + list(HANDSHAKE))
        self.socket.send(buf)

        poller = zmq.Poller()
        poller.register(self.socket, zmq.POLLIN)
        if poller.poll(timeout * 1000):
            ERRMSG = 'Could not perform handshake with preferred method'

            msg = bytes(self.socket.recv())

            if len(msg) < 10:
                raise TecplotInvalidMessage(ERRMSG + ' (response too small')
            if msg[0] != RAWMSG:
                raise TecplotInvalidMessage(ERRMSG + ' (not a raw message)')

            n = int(msg[1])
            msg = bytes(msg[2:2+n]).decode('utf-8').split(':')

            if msg[0] != 'YA':
                raise TecplotInvalidMessage(ERRMSG + ' (unrecognized response)')
            if len(msg) != 6:
                raise TecplotInvalidMessage(ERRMSG + ' (invalid response length)')

            try:
                self.tuserver_version = int(msg[1])
                self.sdk_version_info = tuple([int(x) for x in msg[2:2+4]])
            except Exception as e:
                self.tuserver_version = 0
                self.sdk_version_info = (0, 0, 0, 0)
                raise TecplotInvalidMessage(ERRMSG + '\n' + str(e))

            return True

        return False

    @property
    def connected(self):
        return self.socket is not None

    def disconnect(self):
        if self.socket:
            if sys.version_info >= (3,):
                atexit.unregister(self.disconnect)
            self.socket.disconnect(self.endpoint)
            self.socket = None
            self.tuserver_version = 0
            self.sdk_version_info = (0, 0, 0, 0)

    def sndrcv(self, tecutil_command, *args, **kwargs):
        request = tecrpc.Request()
        optype = build_tecutil_request(request, tecutil_command, *args, **kwargs)
        request_buffer = request.SerializeToString()
        self.socket.send(request_buffer)

        reply = tecrpc.Reply()
        reply_buffer = self.socket.recv()
        reply.ParseFromString(reply_buffer)

        if optype & tecrpc.Request.TecUtilX:
            reply = self.read_tecutilx_reply(args, reply)

        return reply

    def chk(self, reply):
        if reply.status != tecrpc.Reply.Success:
            errmsg = reply.log
            if not isinstance(errmsg, string_types):
                errmsg = errmsg.decode('utf-8')
            raise TecplotSystemError(errmsg)

    def read_arbparam(self, arg):
        if arg.type & tecrpc.Argument.Null:
            return None
        elif arg.type & tecrpc.Argument.Text:
            txt = arg.text
            if isinstance(txt, string_types):
                ctxt = c_char_p(bytes(txt, encoding='utf-8'))
                txt = cast(ctxt, POINTER(c_char))
            else:
                txt = cast(pointer(create_string_buffer(txt)), POINTER(c_char))
            return txt
        if (arg.type == tecrpc.Argument.Unspecified or
                (arg.type & tecrpc.Argument.Address)):
            return arg.int64
        else:
            TecplotNotImplementedError

    def read_text(self, arg):
        if (arg.type == tecrpc.Argument.Unspecified or
                (arg.type & tecrpc.Argument.Text)):
            return arg.text
        elif arg.type & tecrpc.Argument.Null:
            return None
        else:
            TecplotNotImplementedError

    def read_enum_array(self, arg, argtype):
        n, r = divmod(len(arg.buffer), sizeof(c_int32))
        if r:
            raise Exception('could not read array of specified type')
        arr = (c_int32 * n).from_buffer_copy(arg.buffer)
        return [argtype(i) for i in arr]

    def read_array(self, arg, argtype):
        n, r = divmod(len(arg.buffer), sizeof(argtype))
        if r:
            raise Exception('could not read array of specified type')
        return (argtype * n).from_buffer_copy(arg.buffer)

    def read_tecutilx_reply(self, args, reply):
        for valtype, argtype, arg in args:
            if isinstance(arg, tecplot.tecutil.LocalArgList):
                for reparg in reply.args:
                    if reparg.type & tecrpc.Argument.ArgList:
                        for item in reparg.arglist.items:
                            key, value = item.key, item.value
                            if value.type & tecrpc.Argument.Float64:
                                arg[key][0] = value.float64
                            elif value.type & tecrpc.Argument.ArbParam:
                                arg[key][0] = self.read_arbparam(value)
                            elif value.type & Argument.Text:
                                arg[key] = self.read_text(value)
                            else:
                                raise TecplotValueError(key)
        return reply

    def _send_suspend_interface(self, suspend=True):
        if self.tuserver_version < 3:
            log.info(MESSAGES.PERFORMANCE_IMPROVEMENTS)
        request = tecrpc.Request()
        request.version = 1
        request.type = tecrpc.Request.Server
        request.operation = 'Suspend Interface'
        arg = request.args.add()
        arg.boolean = suspend

        request_buffer = request.SerializeToString()
        self.socket.send(request_buffer)

        reply = tecrpc.Reply()
        reply_buffer = self.socket.recv()
        reply.ParseFromString(reply_buffer)
        self.chk(reply)

    @contextlib.contextmanager
    def suspend_interface(self):
        assert self.socket is not None

        if self.tuserver_version < 2:
            log.warn('This version of the TecUtil Server addon does not'
                     ' support the suspended interface context. Please update'
                     ' to the newest version of Tecplot 360.')
            yield
        else:
            if self.suspended:
                yield
            else:
                try:
                    self._send_suspend_interface(True)
                    self.suspended = True
                    yield
                finally:
                    self.suspended = False
                    self._send_suspend_interface(False)

    def clear_suspend_interface(self):
        self._send_suspend_interface(False)

    @property
    def processing_mode(self):
        raise TecplotNotImplementedError

    @processing_mode.setter
    def processing_mode(self, mode):
        if self.tuserver_version < 6:
            log.warn('This version of the TecUtil Server addon does not'
                     ' support different processing modes. Please update'
                     ' to the newest version of Tecplot 360.')
            return

        request = tecrpc.Request()
        request.version = 1
        request.type = tecrpc.Request.Server
        request.operation = 'Set Processing Mode'
        arg = request.args.add()
        arg.uint32 = TecUtilServerProcessingMode(mode).value

        request_buffer = request.SerializeToString()
        self.socket.send(request_buffer)

        reply = tecrpc.Reply()
        reply_buffer = self.socket.recv()
        reply.ParseFromString(reply_buffer)
        self.chk(reply)

    @property
    def logging_level(self):
        raise TecplotNotImplementedError

    @logging_level.setter
    def logging_level(self, level):
        if self.tuserver_version < 6:
            log.warn('This version of the TecUtil Server addon does not'
                     ' support adjusting the logging level. Please update'
                     ' to the newest version of Tecplot 360.')
            return

        request = tecrpc.Request()
        request.version = 1
        request.type = tecrpc.Request.Server
        request.operation = 'Set Logging Level'
        arg = request.args.add()
        arg.int32 = level

        request_buffer = request.SerializeToString()
        self.socket.send(request_buffer)

        reply = tecrpc.Reply()
        reply_buffer = self.socket.recv()
        reply.ParseFromString(reply_buffer)
        self.chk(reply)

    def quit(self):
        if self.tuserver_version < 7:
            try:
                self.Quit()
            except TecplotSystemError as err:
                if str(err) != 'Tecplot quitting...':
                    raise
        else:
            request = tecrpc.Request()
            request.version = 1
            request.type = tecrpc.Request.Server
            request.operation = 'Quit'

            request_buffer = request.SerializeToString()
            self.socket.send(request_buffer)

            reply = tecrpc.Reply()
            reply_buffer = self.socket.recv()
            reply.ParseFromString(reply_buffer)
            self.chk(reply)
