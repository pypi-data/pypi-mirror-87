from __future__ import unicode_literals

import atexit
import datetime
import os
import platform
import sys
import unittest
import warnings

from contextlib import contextmanager
from datetime import date
from unittest.mock import patch, Mock, PropertyMock

from tecplot.exception import *
import tecplot as tp

from test import LATEST_SDK_VERSION, skip_if_sdk_version_before, skip_if_connected, mocked_connected


@contextmanager
def patch_env(key, val=None):
    saved_val = os.environ.get(key, None)
    try:
        try:
            del os.environ[key]
        except KeyError:
            pass
        if val is not None:
            os.environ[key] = val
        yield
    finally:
        if saved_val is None:
            try:
                del os.environ['HOME']
            except KeyError:
                pass
        else:
            os.environ[key] = saved_val


class TestSession(unittest.TestCase):
    @skip_if_connected
    def test_tecplot_directories(self):
        with patch('tecplot.tecutil.tecutil_connector.TecUtilConnector.tecsdkhome',
                   PropertyMock(return_value='/path/to/tec360')):
            with patch('tecplot.tecutil.tecutil_connector.TecUtilConnector.start', Mock()) as start:
                self.assertTrue(tp.session.tecplot_install_directory().startswith('/path'))
                self.assertTrue(tp.session.tecplot_examples_directory().startswith(
                                    tp.session.tecplot_install_directory()))
                self.assertEqual(start.call_count, 3)

            with patch('tecplot.tecutil.tecutil_connector.TecUtilConnector.start', Mock()) as start:
                with patch('tecplot.tecutil.tecutil_connector.TecUtilConnector.connected',
                           PropertyMock(return_value=True)):
                    self.assertTrue(tp.session.tecplot_install_directory().startswith('/path'))
                    self.assertTrue(tp.session.tecplot_examples_directory().startswith(
                                    tp.session.tecplot_install_directory()))
                    self.assertEqual(start.call_count, 0)

        with patch('tecplot.tecutil.tecutil_connector.TecUtilConnector.tecsdkhome',
                   PropertyMock(return_value=None)):
            self.assertIsNone(tp.session.tecplot_install_directory())
            self.assertIsNone(tp.session.tecplot_examples_directory())

    def test_stop(self):
        with patch('tecplot.tecutil.tecutil_connector.TecUtilConnector.stop',
                   Mock(return_value=True)) as stop:
            self.assertIsNone(tp.session.stop())
            stop.assert_called_once()

    def test_acquire_license(self):
        with patch('tecplot.tecutil.tecutil_connector.TecUtilConnector.acquire_license',
                   Mock(return_value=True)) as acquire:
            self.assertIsNone(tp.acquire_license())
            acquire.assert_called_once()

    def test_release_license(self):
        with patch(
                'tecplot.tecutil.tecutil_connector.TecUtilConnector.release_license',
                Mock(return_value=True)) as release:
            self.assertIsNone(tp.release_license())
            release.assert_called_once()

    @skip_if_connected
    @skip_if_sdk_version_before(2017, 3)
    def test_roaming(self):
        def LicenseStartRoaming(ndays):
            return True
        _LicenseStartRoaming = tp.tecutil._tecutil_connector.handle.LicenseStartRoaming
        tp.tecutil._tecutil_connector.handle.LicenseStartRoaming = LicenseStartRoaming
        try:
            warnings.simplefilter('ignore')
            with patch('tecplot.tecutil.tecutil_connector.TecUtilConnector.connected',
                       PropertyMock(return_value=True)):
                with self.assertRaises(TecplotLogicError):
                    tp.session.start_roaming(10)
                with self.assertRaises(TecplotLogicError):
                    tp.session.stop_roaming()

            tp.session.start_roaming(10)
            tp.session.stop_roaming()
        finally:
            tp.tecutil._tecutil_connector.handle.LicenseStartRoaming = _LicenseStartRoaming

    def test_expiration_date(self):
        if tp.tecutil._tecutil_connector.handle is not None:
            expdate = None
            def LicenseExpirationDate():
                return expdate
            _LicenseExpirationDate = tp.tecutil._tecutil_connector.handle.LicenseExpirationDate
            tp.tecutil._tecutil_connector.handle.LicenseExpirationDate = LicenseExpirationDate
            try:
                expdate = b'2020-01-01'
                self.assertEqual(tp.session.license_expiration(), datetime.date(year=2020, month=1, day=1))
                expdate = b'unknown'
                self.assertIsNone(tp.session.license_expiration())
            finally:
                tp.tecutil._tecutil_connector.handle.LicenseExpirationDate = _LicenseExpirationDate

    @skip_if_connected
    @skip_if_sdk_version_before(2018, 2)
    def test_connect(self):
        connected_fn = 'tecplot.tecutil.tecutil_connector.TecUtilConnector.connected'

        if tp.tecutil._tecutil_connector.client is None:
            import warnings
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                from tecplot.tecutil.tecutil_client import TecUtilClient
            tp.tecutil._tecutil_connector.client = TecUtilClient()
            is_listening_fn = 'tecplot.tecutil.tecutil_client.TecUtilClient.is_server_listening'
        elif tp.tecutil._tecutil_connector.client.tuserver_version < 3:
            is_listening_fn = 'tecplot.tecutil.tecutil_flatbuffers.tecutil_client.TecUtilClient.is_server_listening'
        else:
            is_listening_fn = 'tecplot.tecutil.tecutil_client.TecUtilClient.is_server_listening'

        with patch(connected_fn, PropertyMock(return_value=False)):
            self.assertFalse(tp.session.connected())

        with patch(connected_fn, PropertyMock(return_value=True)):
            with patch(is_listening_fn, Mock(return_value=True)):
                self.assertTrue(tp.session.connected())
            with patch(is_listening_fn, Mock(return_value=False)):
                self.assertFalse(tp.session.connected())

        if not tp.session.connected():
            with self.assertRaises(TecplotTimeoutError):
                tp.session.connect(port=1, timeout=0.1, quiet=True)

        with patch('tecplot.tecutil.tecutil_connector.TecUtilConnector.disconnect',
                   Mock(return_value=None)):
            self.assertIsNone(tp.session.disconnect())

    def test_suspend(self):
        tp.new_layout()
        with tp.session.suspend():
            with tp.session.suspend():
                ds = tp.active_frame().create_dataset('D', ['x', 'y'])
                zn = ds.add_ordered_zone('Z', (1,))
        self.assertEqual(zn.values(0).shape, (1,))

    def test_suspend_enter_exit(self):
        tp.new_layout()
        try:
            tp.session.suspend_enter()
            ds = tp.active_frame().create_dataset('D', ['x', 'y'])
            zn = ds.add_ordered_zone('Z', (1,))
        finally:
            tp.session.suspend_exit()
        self.assertEqual(zn.values(0).shape, (1,))

    @skip_if_connected
    @skip_if_sdk_version_before(2018, 2)
    def test_disconnect(self):
        class Client(Mock):
            def quit():
                pass
        with patch('tecplot.session.session.connected', Mock(return_value=True)) as conn:
            with patch.object(tp.session.session, '_tecutil_connector') as TUConnMock:
                TUConnMock.client = Client
                def disconnect(self):
                    pass
                TUConnMock.disconnect = disconnect
                with patch.object(TUConnMock, 'disconnect') as disconn:
                    with patch.object(Client, 'quit') as quit:
                        tp.session.disconnect()
                        self.assertGreater(conn.call_count, 0)
                        self.assertGreater(disconn.call_count, 0)
                        quit.assert_not_called()
                        conn.reset_mock()
                        disconn.reset_mock()

                        tp.session.disconnect(True)
                        self.assertGreater(conn.call_count, 0)
                        self.assertGreater(disconn.call_count, 0)
                        self.assertGreater(quit.call_count, 0)
                        conn.reset_mock()
                        disconn.reset_mock()

                        tp.session.disconnect(quit=True)
                        self.assertGreater(conn.call_count, 0)
                        self.assertGreater(disconn.call_count, 0)
                        self.assertGreater(quit.call_count, 0)

    def test_atexit(self):
        try:
            connected = tp.tecutil._tecutil_connector.connected
            if connected:
                if sys.version_info < (3,):
                    handlers_to_delete = []
                    for i in range(0, len(atexit._exithandlers)):
                        if (
                            len(atexit._exithandlers[i]) and
                            atexit._exithandlers[i][0] == tp.tecutil._tecutil_connector.client.disconnect
                        ):
                            handlers_to_delete.append(i)
                    for i in reversed(sorted(handlers_to_delete)):
                        del atexit._exithandlers[i]
                else:
                    atexit.unregister(tp.tecutil._tecutil_connector.client.disconnect)
            with patch.object(tp.tecutil._tecutil_connector, 'stop') as stop:
                with patch.object(tp.tecutil._tecutil_connector, 'release_license') as release_license:
                    atexit._run_exitfuncs()
                    if platform.system() == 'Darwin':
                        self.assertEqual(stop.call_count, 0)
                        self.assertEqual(release_license.call_count, 1)
                    else:
                        self.assertEqual(stop.call_count, 1)
        finally:
            if connected:
                atexit.register(tp.tecutil._tecutil_connector.client.disconnect)


if __name__ == '__main__':
    from .. import main
    main()
