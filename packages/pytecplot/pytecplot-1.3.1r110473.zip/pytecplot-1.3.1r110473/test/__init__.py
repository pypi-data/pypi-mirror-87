from __future__ import print_function
from builtins import super

import warnings as _warnings
import os as _os

import tempfile

try:
    import collections.abc
except ImportError:  # if sys.version_info < (3,)
    import collections
    import sys
    setattr(collections, 'abc', collections)
    sys.modules['collections.abc'] = collections

import sys

### move mock under unittest like it is in Python version 3.1+
if sys.version_info < (3,1):
    import mock
    import unittest
    sys.modules['unittest.mock'] = mock
    unittest.mock = mock

    def assertIsNone(self, obj):
        return self.assertTrue(obj is None)
    unittest.TestCase.assertIsNone = assertIsNone

    if sys.version_info < (3,3):
        def assertRegex(self, text, regexp, msg=None):
            return self.assertRegexpMatches(text, regexp, msg)
        unittest.TestCase.assertRegex = assertRegex

        def assertRaisesRegex(self, text, regexp, msg=None):
            return self.assertRaisesRegexp(text, regexp, msg)
        unittest.TestCase.assertRaisesRegex = assertRaisesRegex

if sys.version_info < (3, 2):
    # back-port TemporaryDirectory for Python 2.7
    class TemporaryDirectory(object):
        """Create and return a temporary directory.  This has the same
        behavior as mkdtemp but can be used as a context manager.  For
        example:

            with TemporaryDirectory() as tmpdir:
                ...

        Upon exiting the context, the directory and everything contained
        in it are removed.
        """

        def __init__(self, suffix="", prefix="tmp", dir=None):
            self._closed = False
            self.name = None # Handle mkdtemp raising an exception
            self.name = tempfile.mkdtemp(suffix, prefix, dir)

        def __repr__(self):
            return "<{} {!r}>".format(self.__class__.__name__, self.name)

        def __enter__(self):
            return self.name

        def cleanup(self, _warn=False):
            if self.name and not self._closed:
                try:
                    self._rmtree(self.name)
                except (TypeError, AttributeError) as ex:
                    # Issue #10188: Emit a warning on stderr
                    # if the directory could not be cleaned
                    # up due to missing globals
                    if "None" not in str(ex):
                        raise
                    print("ERROR: {!r} while cleaning up {!r}".format(ex, self,),
                          file=_sys.stderr)
                    return
                self._closed = True
                if _warn:
                    self._warn("Implicitly cleaning up {!r}".format(self),
                               ResourceWarning)

        def __exit__(self, exc, value, tb):
            self.cleanup()

        def __del__(self):
            # Issue a ResourceWarning if implicit cleanup needed
            self.cleanup(_warn=True)

        # XXX (ncoghlan): The following code attempts to make
        # this class tolerant of the module nulling out process
        # that happens during CPython interpreter shutdown
        # Alas, it doesn't actually manage it. See issue #10188
        _listdir = staticmethod(_os.listdir)
        _path_join = staticmethod(_os.path.join)
        _isdir = staticmethod(_os.path.isdir)
        _islink = staticmethod(_os.path.islink)
        _remove = staticmethod(_os.remove)
        _rmdir = staticmethod(_os.rmdir)
        _warn = _warnings.warn

        def _rmtree(self, path):
            # Essentially a stripped down version of shutil.rmtree.  We can't
            # use globals because they may be None'ed out at shutdown.
            for name in self._listdir(path):
                fullname = self._path_join(path, name)
                try:
                    isdir = self._isdir(fullname) and not self._islink(fullname)
                except OSError:
                    isdir = False
                if isdir:
                    self._rmtree(fullname)
                else:
                    try:
                        self._remove(fullname)
                    except OSError:
                        pass
            try:
                self._rmdir(path)
            except OSError:
                pass

    tempfile.TemporaryDirectory = TemporaryDirectory


import argparse, collections, functools, logging, os, platform, random, re
import time, unittest, warnings

from argparse import ArgumentParser, SUPPRESS
from contextlib import contextmanager
from os import path
from tempfile import NamedTemporaryFile
from unittest.mock import patch, Mock, PropertyMock

from .hide_modules import hide_modules

logging.basicConfig()

# useful for testing other platforms
#patch('platform.system', Mock(return_value='Windows')).start()

### Mock out DLL if all we are going to do is list out test cases
parser = ArgumentParser(usage=SUPPRESS, add_help=False)
parser.add_argument('-l', '--list',
    action='store_true',
    default=False,
    help='''just list out the test cases, but do not run them.''')
args,_ = parser.parse_known_args(sys.argv)
if args.list:
    from .mock_tecplot_module import patch_tecplot_module
    patch_tecplot_module()
    sys.modules['numpy'] = Mock()
else:
    # else ensure numpy is available for certain tests which require it
    import numpy

@contextmanager
def closed_tempfile(suffix=''):
    with NamedTemporaryFile(suffix=suffix, delete=False) as fout:
        try:
            fout.close()
            yield fout.name
        finally:
            try:
                #print('removing', fout.name)
                os.remove(fout.name)
            except Exception as e:
                print(e)

### convenience methods for patching tecutil
def patch_tecutil(fn_name, **kwargs):
    import tecplot
    return patch.object(tecplot.tecutil._tecutil, fn_name, Mock(**kwargs))

@contextmanager
def patched_tecutil(fn_name, **kwargs):
    with patch_tecutil(fn_name, **kwargs) as p:
        yield p

@contextmanager
def mocked_sdk_version(*version):
    import tecplot
    _sdk_vinfo = tecplot.version.sdk_version_info
    try:
        if len(version) < 3:
            # extend version tuple to at least three numbers (appending 0's)
            version = tuple(list(version) + [0] * (3 - len(version)))
        tecplot.version.sdk_version_info = version
        yield
    finally:
        tecplot.version.sdk_version_info = _sdk_vinfo

@contextmanager
def mocked_connected():
    import tecplot

    class TecUtilClient(Mock):
        host = 'localhost'

    class LocalStringList(list):
        def __init__(self, *args):
            super().__init__(args)
        def __enter__(self):
            return self
        def __exit__(self, *args):
            pass

    class LocalArgList(collections.OrderedDict):
        def __init__(self, *args):
            super().__init__(args)
        def __enter__(self):
            return self
        def __exit__(self, *args):
            pass

    with patch('tecplot.tecutil.tecutil_connector.TecUtilConnector.connected',
               PropertyMock(return_value=True)):
        _client = tecplot.tecutil._tecutil_connector.client
        _sus = tecplot.tecutil._tecutil_connector.suspended
        _ArgList = tecplot.tecutil.ArgList
        _StringList = tecplot.tecutil.StringList
        try:
            tecplot.tecutil._tecutil_connector.client = TecUtilClient()
            tecplot.tecutil._tecutil_connector.suspended = True
            tecplot.tecutil._tecutil_connector._delete_caches = []
            tecplot.tecutil.ArgList = LocalArgList
            tecplot.tecutil.StringList = LocalStringList
            yield
        finally:
            tecplot.tecutil.StringList = _StringList
            tecplot.tecutil.ArgList = _ArgList
            delattr(tecplot.tecutil._tecutil_connector, '_delete_caches')
            tecplot.tecutil._tecutil_connector.suspended = _sus
            tecplot.tecutil._tecutil_connector.client = _client

@contextmanager
def mocked_tuserver_version(ver):
    import tecplot
    with mocked_connected():
        class C:
            tuserver_version = ver
        _client = tecplot.tecutil._tecutil_connector.client
        tecplot.tecutil._tecutil_connector.client = C()
        try:
            _sus = tecplot.tecutil._tecutil_connector.suspended
            try:
                tecplot.tecutil._tecutil_connector.suspended = False
                yield
            finally:
                tecplot.tecutil._tecutil_connector.suspended = _sus
                pass
        finally:
            tecplot.tecutil._tecutil_connector.client = _client

# This will print out timing information for each TestCase
'''
@classmethod
def setUpClass(cls):
    cls.startTime = time.time()
@classmethod
def tearDownClass(cls):
    print("\n{}.{}: {:.3f}".format(cls.__module__, cls.__name__, time.time() - cls.startTime))
unittest.TestCase.setUpClass = setUpClass
unittest.TestCase.tearDownClass = tearDownClass
'''


import numpy
def assert_allclose(self, actual, expected, rtol=1e-5, atol=1e-7):
    return numpy.testing.assert_allclose(actual, expected, rtol=rtol, atol=atol)
unittest.TestCase.assertAllClose = assert_allclose


LATEST_SDK_VERSION = (2021, 1)


def skip_windows():
    def decorator(test_item):
        @functools.wraps(test_item)
        def skip_wrapper(*args, **kwargs):
            if platform.system() != 'Windows':
                test_item(*args, **kwargs)
        return skip_wrapper
    return decorator


def skip_on(*ex):
    """
    Unconditionally skip a test on specfic exceptions
    """
    def decorator(test_item):
        @functools.wraps(test_item)
        def skip_wrapper(*args, **kwargs):
            if __debug__:
                try:
                    warnings.simplefilter('ignore')
                    test_item(*args, **kwargs)
                except ex:
                    raise unittest.SkipTest(str(ex[0]))
                finally:
                    warnings.simplefilter('default')
            else:
                import tecplot
                if tecplot.sdk_version_info < LATEST_SDK_VERSION:
                    raise unittest.SkipTest(str(ex[0]))
                else:
                    test_item(*args, **kwargs)
        return skip_wrapper
    return decorator


def skip_if_sdk_version_before(*ver, **kwargs):
    msg = kwargs.pop('msg', 'Added to SDK in {}')
    def decorator(test_item):
        @functools.wraps(test_item)
        def skip_wrapper(*args, **kwargs):
            import tecplot
            if tecplot.sdk_version_info < ver:
                raise unittest.SkipTest(msg.format('.'.join(str(x) for x in ver)))
            else:
                test_item(*args, **kwargs)
        return skip_wrapper
    return decorator


def skip_if_tuserver_version_before(ver, **kwargs):
    msg = kwargs.pop('msg', 'Added to TecUtil Server in version {}')
    def decorator(test_item):
        @functools.wraps(test_item)
        def skip_wrapper(*args, **kwargs):
            from tecplot.tecutil import _tecutil_connector
            if (
                _tecutil_connector.connected and
                _tecutil_connector.client.tuserver_version < ver
            ):
                raise unittest.SkipTest(msg.format(ver))
            else:
                test_item(*args, **kwargs)
        return skip_wrapper
    return decorator

def skip_if_connected(test_item):
    @functools.wraps(test_item)
    def skip_wrapper(*args, **kwargs):
        import tecplot
        if tecplot.tecutil._tecutil_connector.connected:
            raise unittest.SkipTest('Batch only')
        else:
            test_item(*args, **kwargs)
    return skip_wrapper

@contextmanager
def assert_style(value, *svargs, **kwargs):
    once = kwargs.pop('once', True)
    with patch('tecplot.session.style.get_style', Mock()) as g, \
         patch('tecplot.session.style.set_style', Mock()) as s:
        yield
    if once:
        g.assert_called_once_with(type(value), *svargs, **kwargs)
        s.assert_called_once_with(value, *svargs, **kwargs)
    else:
        g.assert_called_with(type(value), *svargs, **kwargs)
        s.assert_called_with(value, *svargs, **kwargs)

def main():
    parser = ArgumentParser(usage=SUPPRESS)
    parser.add_argument('-r', '--random',
        action='store_true',
        default=False,
        help='''randomize ordering of test cases and further randomize
                test methods within each test case''')
    parser.add_argument('-d', '--debug',
        action='store_true',
        default=False,
        help='''Set logging output to DEBUG''')
    parser.add_argument('-i', '--info',
        action='store_true',
        default=False,
        help='''Print DEBUG logging output only during initial import of tecplot''')
    parser.add_argument('-l', '--list',
        action='store_true',
        default=False,
        help='''just list out the test cases, but do not run them.''')
    parser.add_argument('-c', '--connect',
        action='store_true',
        default=False,
        help='''connect to a running instance of Tecplot 360.''')
    parser.add_argument('-p', '--port',
        type=int, default=7600,
        help='''port to use when connecting to the TecUtil Server.''')

    def print_help():
        try:
            unittest.main(argv=[sys.argv[0], '--help'])
        except SystemExit:
            parser._print_help()
            sys.exit(0)
    parser._print_help = parser.print_help
    parser.print_help = print_help
    args,unknown_args = parser.parse_known_args(sys.argv)

    if args.debug:
        logging.root.handlers[0].stream = sys.stdout
        logging.root.setLevel(logging.DEBUG)
    else:
        logging.root.handlers[0].stream = open(os.devnull, 'w')

    if args.list:

        def list_of_tests(tests):
            if unittest.suite._isnotsuite(tests):
                yield tests
            else:
                for test in tests._tests:
                    for t in list_of_tests(test):
                        yield t

        here = os.path.abspath(os.path.realpath(os.path.dirname(__file__)))
        tests = unittest.defaultTestLoader.discover('test',
            top_level_dir=os.path.dirname(here))

        tests = sorted(set([str(t) for t in list_of_tests(tests)]))
        tests = [str(t).replace(' (','-').replace(')','') for t in tests]

        for test in tests:
            fnname, namespace = test.split('-')
            if re.search(r'test\.examples\.', namespace):
                continue
            if platform.system() == 'Windows':
                if re.search(r'captured_output', namespace):
                    continue
            print(test)

    else:
        if args.info and not args.debug:
            logging.root.handlers[0].stream = sys.stdout
            logging.root.setLevel(logging.DEBUG)

        logging.debug('PATH:')
        for p in os.environ['PATH'].split(os.pathsep):
            logging.debug('    ' + p)

        if platform.system() == 'Linux':
            logging.debug('LD_LIBRARY_PATH:')
            for p in os.environ.get('LD_LIBRARY_PATH', '').split(os.pathsep):
                logging.debug('    ' + p)
        elif platform.system() == 'Darwin':
            logging.debug('DYLD_LIBRARY_PATH:')
            for p in os.environ.get('DYLD_LIBRARY_PATH', '').split(os.pathsep):
                logging.debug('    ' + p)

        import tecplot as tp
        if args.connect:
            tp.session.connect(port=args.port, timeout=600, quiet=True)
            tp.new_layout()
        else:
            tp.session._tecutil_connector.start()

        if args.info and not args.debug:
            logging.root.handlers[0].stream = open(os.devnull, 'w')
            logging.root.setLevel(logging.WARNING)

        try:
            if args.random:
                unittest.defaultTestLoader.sortTestMethodsUsing = \
                    lambda *a: random.choice((-1,1))
                def suite_init(self,tests=()):
                    self._tests = []
                    self._removed_tests = 0
                    if isinstance(tests, list):
                        random.shuffle(tests)
                    self.addTests(tests)
                unittest.defaultTestLoader.suiteClass.__init__ = suite_init

            from unittest.runner import TextTestResult

            class TimeLoggingTestResult(TextTestResult):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.test_timings = []

                def startTest(self, test):
                    self._test_started_at = time.time()
                    super().startTest(test)

                def addSuccess(self, test):
                    elapsed = time.time() - self._test_started_at
                    num = len(self.test_timings)
                    name = self.getDescription(test)
                    self.test_timings.append((num, name, elapsed))
                    super().addSuccess(test)

            if __debug__:
                SLOW_TEST_THRESHOLD = 5 if args.connect else 1
            else:
                SLOW_TEST_THRESHOLD = 1 if args.connect else 0.5

            class TimeLoggingTestRunner(unittest.TextTestRunner):
                def __init__(self, slow_test_threshold=SLOW_TEST_THRESHOLD,
                             *args, **kwargs):
                    self.slow_test_threshold = slow_test_threshold
                    return super().__init__(resultclass=TimeLoggingTestResult,
                                            *args, **kwargs)

                def run(self, test):
                    result = super().run(test)
                    timings = list(filter(lambda item: item[2] > self.slow_test_threshold,
                                          result.test_timings))
                    if timings:
                        self.stream.writeln(
                            "\nSlow Tests (>{:.03f}s):".format(
                                self.slow_test_threshold))
                        for num, name, elapsed in timings:
                            if elapsed > self.slow_test_threshold:
                                self.stream.writeln(
                                    "({:.03f}s) {} {}".format(
                                        elapsed, num, name))
                    else:
                        self.stream.writeln(
                            '\nAll tests ran within {:.03f} s'.format(
                                self.slow_test_threshold))
                    return result

            # ensure we exit with the status of the tests and avoid failing
            # if the SDK crashed on exit (which happens in macos VMs)
            if platform.system() == 'Darwin':
                try:
                    # unittest.main() got exit=False option in python 3.1
                    # we use try/except here to allow for python 2.7
                    unittest.main(argv=unknown_args, testRunner=TimeLoggingTestRunner)
                except SystemExit as e:
                    os._exit(e.code)
            else:
                unittest.main(argv=unknown_args, testRunner=TimeLoggingTestRunner)

        finally:
            if args.connect:
                tp.session.disconnect()
            if platform.system() != 'Darwin':
                tp.session.stop()
