# coding: utf-8
from __future__ import unicode_literals
from builtins import range

import ctypes, os, platform, sys, unittest, six, warnings
import numpy as np

from collections import namedtuple
from contextlib import contextmanager
from ctypes import *
from os import path
from textwrap import dedent
from unittest.mock import patch, Mock, PropertyMock

import tecplot as tp
from tecplot import session
from tecplot.constant import *
from tecplot.exception import *
from tecplot.tecutil import _tecutil_connector

from test import (patch_tecutil, hide_modules, mocked_connected,
                  skip_if_connected, skip_if_sdk_version_before)


class TestArray(unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        self.ds = tp.active_frame().create_dataset('D', ['x'])
        self.ds.add_ordered_zone('Z0', (3,))
        self.ds.add_ordered_zone('Z1', (3,3))
        self.ds.add_ordered_zone('Z2', (3,3,3))
        self.ds.add_ordered_zone('Z3', (1,1,3))
        self.ds.add_fe_zone(ZoneType.FEQuad, 'Z4', 8, 3)
        self.ds.add_poly_zone(ZoneType.FEPolyhedron, 'Z5', 8, 1, 12)
        self.ds.add_variable('n', FieldDataType.Double,
                             locations=ValueLocation.Nodal)
        self.ds.add_variable('c', FieldDataType.Int32,
                             locations=ValueLocation.CellCentered)

    def test_native_ref(self):
        rref = self.ds.zone(0).values(0)._native_reference(False)
        self.assertIsInstance(rref, six.integer_types)
        wref = self.ds.zone(0).values(0)._native_reference(True)
        self.assertIsInstance(wref, six.integer_types)
        self.assertEqual(rref, wref)
        self.assertEqual(self.ds.zone(0).values(0)._native_reference(), rref)

    def test_raw_pointer(self):
        if _tecutil_connector.connected:
            with self.assertRaises(TecplotLogicError):
                rptr = self.ds.zone(0).values(0)._raw_pointer(False)
        else:
            rptr = self.ds.zone(0).values(0)._raw_pointer(False)
            self.assertIsInstance(rptr, ctypes.POINTER(ctypes.c_float))
            wptr = self.ds.zone(0).values(0)._raw_pointer(True)
            self.assertIsInstance(wptr, ctypes.POINTER(ctypes.c_float))
            self.assertEqual(rptr[0], wptr[0])

            ptr = self.ds.zone(0).values(1)._raw_pointer()
            self.assertIsInstance(ptr, ctypes.POINTER(ctypes.c_double))

            ptr = self.ds.zone(0).values(2)._raw_pointer()
            self.assertIsInstance(ptr, ctypes.POINTER(ctypes.c_int32))

        arr = self.ds.zone(0).values(0)
        with mocked_connected():
            with self.assertRaises(TecplotLogicError):
                rptr = arr._raw_pointer(False)
            with self.assertRaises(TecplotLogicError):
                wptr = arr._raw_pointer(True)

    def test_eq(self):
        x = self.ds.zone(0).values(0)
        n = self.ds.zone(0).values(1)
        self.assertTrue (x == self.ds.zone(0).values(0))
        self.assertFalse(x != self.ds.zone(0).values(0))
        self.assertFalse(n == x)
        self.assertTrue (n != x)

    def test_len(self):
        self.assertEqual(len(self.ds.zone(0).values(0)), 3)
        self.assertEqual(len(self.ds.zone(0).values(1)), 3)
        self.assertEqual(len(self.ds.zone(0).values(2)), 2)
        self.assertEqual(len(self.ds.zone(2).values(0)), 3*3*3)
        self.assertEqual(len(self.ds.zone(2).values(1)), 3*3*3)
        self.assertEqual(len(self.ds.zone(2).values(2)), 2*3*3)

    def test_shape(self):
        self.assertEqual(self.ds.zone(0).values(0).shape, (3,))
        self.assertEqual(self.ds.zone(0).values(1).shape, (3,))
        self.assertEqual(self.ds.zone(0).values(2).shape, (2,))
        self.assertEqual(self.ds.zone(2).values(0).shape, (3,3,3))
        self.assertEqual(self.ds.zone(2).values(1).shape, (3,3,3))
        self.assertEqual(self.ds.zone(2).values(2).shape, (2,2,2))
        self.assertEqual(self.ds.zone(3).values(0).shape, (3,))
        self.assertEqual(self.ds.zone(3).values(2).shape, (2,))

        self.assertEqual(self.ds.zone(4).values(0).shape, (8,))
        self.assertEqual(self.ds.zone(4).values(2).shape, (7,))
        self.assertEqual(self.ds.zone(5).values(0).shape, (8,))
        self.assertEqual(self.ds.zone(5).values(2).shape, (7,))

        small_zone = self.ds.add_ordered_zone('small zone', (1,))
        self.assertEqual(small_zone.values(0).shape, (1,))

    def test_c_type(self):
        self.assertEqual(self.ds.zone(0).values(0).c_type, ctypes.c_float)
        self.assertEqual(self.ds.zone(0).values(1).c_type, ctypes.c_double)
        self.assertEqual(self.ds.zone(0).values(2).c_type, ctypes.c_int32)
        self.assertEqual(self.ds.zone(1).values(0).c_type, ctypes.c_float)
        self.assertEqual(self.ds.zone(1).values(1).c_type, ctypes.c_double)
        self.assertEqual(self.ds.zone(1).values(2).c_type, ctypes.c_int32)
        self.assertEqual(self.ds.zone(2).values(0).c_type, ctypes.c_float)
        self.assertEqual(self.ds.zone(2).values(1).c_type, ctypes.c_double)
        self.assertEqual(self.ds.zone(2).values(2).c_type, ctypes.c_int32)

    def test_data_type(self):
        self.assertEqual(self.ds.zone(0).values(0).data_type, FieldDataType.Float)
        self.assertEqual(self.ds.zone(1).values(0).data_type, FieldDataType.Float)
        self.assertEqual(self.ds.zone(2).values(0).data_type, FieldDataType.Float)
        self.assertEqual(self.ds.zone(0).values(1).data_type, FieldDataType.Double)
        self.assertEqual(self.ds.zone(1).values(1).data_type, FieldDataType.Double)
        self.assertEqual(self.ds.zone(2).values(1).data_type, FieldDataType.Double)
        self.assertEqual(self.ds.zone(0).values(2).data_type, FieldDataType.Int32)
        self.assertEqual(self.ds.zone(1).values(2).data_type, FieldDataType.Int32)
        self.assertEqual(self.ds.zone(2).values(2).data_type, FieldDataType.Int32)

    def test_copy(self):
        x = self.ds.zone(0).values(0)
        x[0] = 3.1415
        xcopy = x.copy()
        self.assertAlmostEqual(x[0], xcopy[0])
        xcopy[0] = 6.283
        self.assertNotAlmostEqual(x[0], xcopy[0])

    @skip_if_connected
    def test_as_ctypes_array(self):
        x = self.ds.zone(0).values(0)
        size = len(x)
        with mocked_connected(), \
             patch_tecutil('DataValueGetCountByRef', return_value=size), \
             patch('tecplot.data.array.Array.c_type',
                   PropertyMock(return_value=ctypes.c_float)):
            with self.assertRaises(TecplotLogicError):
                _ = x.as_ctypes_array(copy=False)
        data = x.as_ctypes_array(copy=False)
        np.testing.assert_allclose(x[:], data[:])

        data = x.as_ctypes_array(offset=1, copy=False)
        np.testing.assert_allclose(x[1:], data[:])
        self.assertEqual(len(data), size - 1)

        data = x.as_ctypes_array(size=2, copy=False)
        np.testing.assert_allclose(x[:2], data[:])
        self.assertEqual(len(data), 2)

    def test_slice_range(self):
        x = self.ds.zone(0).values(0)
        self.assertEqual(list(x._slice_range(slice(len(x)))),
                         list(range(0,len(x),1)))
        self.assertEqual(list(x._slice_range(slice(1))),
                         list(range(0,1,1)))
        self.assertEqual(list(x._slice_range(slice(0,2))),
                         list(range(0,2,1)))
        self.assertEqual(list(x._slice_range(slice(None,None,2))),
                         list(range(0,len(x),2)))

        with self.assertRaises((TecplotIndexError, TecplotSystemError)):
            x[:4096] = np.zeros(len(x))

    def test_get_set_item(self):
        x = self.ds.zone(2).values(0)
        x[0] = 3.1415
        self.assertAlmostEqual(x[0], 3.1415)
        x[:2] = [5,6]
        self.assertAlmostEqual(x[0], 5)
        self.assertAlmostEqual(x[1], 6)
        x[:3:2] = [8,9]
        self.assertAlmostEqual(x[0], 8)
        self.assertAlmostEqual(x[2], 9)
        arr = x[:3:2]
        self.assertAlmostEqual(arr[0], 8)
        self.assertAlmostEqual(arr[1], 9)

        c_carr = x.as_ctypes_array()
        self.assertAlmostEqual(c_carr[0], 8)
        self.assertAlmostEqual(c_carr[1], 6)

        c_narr = x.as_numpy_array()
        self.assertAlmostEqual(c_narr[0], 8)
        self.assertAlmostEqual(c_narr[1], 6)

        with patch('tecplot.session.state_changed._state_changed', Mock()) as schg:
            x = self.ds.zone(2).values(0)
            _ = x[5]
            schg.assert_not_called()

    def test_get_set_item_connected(self):
        x = self.ds.zone(2).values(0)
        with mocked_connected(), \
             patch('tecplot.session.data_altered'):
            with patch('tecplot.data.array.Array._cache', Mock(return_value=False)), \
                 patch('tecplot.data.array.Array.copy', Mock(return_value=[1,2,3])), \
                 patch_tecutil('DataValueGetByRef', return_value=1), \
                 patch_tecutil('DataValueGetCountByRef', return_value=3):
                self.assertEqual(x[:], [1,2,3])
                self.assertEqual(x[0], 1)
                self.assertEqual(x[::2], [1,1])
            with patch('tecplot.data.array.Array._native_reference', Mock(return_value=None)), \
                 patch('tecplot.data.array.Array.c_type', PropertyMock(return_value=ctypes.c_double)), \
                 patch_tecutil('DataValueArraySetByRef', return_value=1) as arrset, \
                 patch_tecutil('DataValueSetByRef', return_value=2) as valset:
                x[0] = 3.1415
                valset.assert_called_once_with(None, 1, 3.1415)
                arrset.assert_not_called()
                with patch('tecplot.data.array.Array._slice_range', Mock(return_value=range(0, 3, 1))):
                    valset.reset_mock()
                    arrset.reset_mock()
                    x[:] = np.array([1.,2.,3.], dtype=np.float64)
                    valset.assert_not_called()
                    self.assertEqual(arrset.call_count, 1)
                    self.assertIsNone(arrset.call_args[0][0])
                    self.assertEqual(arrset.call_args[0][1], 1)
                    self.assertEqual(arrset.call_args[0][2], 3)
                    self.assertEqual(type(arrset.call_args[0][3]), (ctypes.c_double * 3))
                with patch('tecplot.data.array.Array._slice_range', Mock(return_value=range(0, 3, 2))):
                    valset.reset_mock()
                    arrset.reset_mock()
                    x[:] = np.array([1.,2.], dtype=np.float64)
                    valset.assert_called_with(None, 3, 2.0)
                    arrset.assert_not_called()

    def test_iter(self):
        x = self.ds.zone(2).values(0)
        data = list(range(len(x)))
        x[:] = data
        for i,d in zip(x,data):
            self.assertAlmostEqual(i,d)

    def test_limits(self):
        x = self.ds.zone(2).values(0)
        data = list(range(len(x)))
        x[:] = data
        self.assertAlmostEqual(x.min(), 0)
        self.assertAlmostEqual(x.max(), len(x)-1)
        self.assertAlmostEqual(x.minmax()[0], 0)
        self.assertAlmostEqual(x.minmax()[1], len(x)-1)

        x[3] = -3.14
        x[5] = 4096
        self.assertAlmostEqual(x.min(), -3.14, 6)
        self.assertAlmostEqual(x.max(), 4096, 6)

    def test_shared_zones(self):
        z = self.ds.zone(0)
        z2 = z.copy(True)
        self.assertEqual(z.values(0).shared_zones, [z,z2])
        self.assertEqual(z.values(0), z2.values(0))

    @skip_if_sdk_version_before(2019, 1)
    def test_passiveness(self):
        z = self.ds.add_ordered_zone('Z1', (3,))
        zcopy1 = z.copy(True)
        self.ds.branch_variables(z, 0, copy_data=False)
        self.assertEqual(z.values(0).shared_zones, [])
        self.assertEqual(z.values(0).passive, True)

    def test_cache(self):
        arr = self.ds.zone(0).values(0)
        self.assertFalse(arr._cache)
        with tp.session.suspend():
            self.assertTrue(arr._cache)

            nrref = arr._native_reference()
            self.assertEqual(id(nrref), id(arr._native_reference()))
            nwref = arr._native_reference(writable=True)
            self.assertEqual(id(nwref), id(arr._native_reference(writable=True)))

            if not tp.session.connected():
                rptr = arr._raw_pointer(False)
                self.assertEqual(id(rptr), id(arr._raw_pointer(False)))
                wptr = arr._raw_pointer(True)
                self.assertEqual(id(wptr), id(arr._raw_pointer(True)))

                l = len(arr)
                self.assertEqual(id(l), id(len(arr)))
                l = arr.location
                self.assertEqual(id(l), id(arr.location))

    def test_array_assignment(self):
        zn = self.ds.zone(2)
        xarr = zn.values(0)
        yarr = zn.values(1)
        x =  np.linspace(0, 1, 27)
        y =  np.linspace(10, 100, 27)
        xarr[:] = x
        yarr[:] = y
        np.testing.assert_allclose(xarr[:], x)
        np.testing.assert_allclose(yarr[:], y)
        xarr[:] = yarr
        np.testing.assert_allclose(xarr[:], yarr[:])

        # self assignment
        xarr[:] = zn.values(0)

        # array copy from zone to zone
        zn0 = self.ds.zone(0)
        zn3 = self.ds.zone(3)
        with patch_tecutil('DataValueCopy', return_value=True) as dvcpy:
            zn0.values(0)[:] = zn3.values(0)
            self.assertEqual(dvcpy.call_count, 1)
        with patch_tecutil('DataValueCopy', return_value=False):
            with self.assertRaises((TecplotLogicError, TecplotSystemError)):
                zn0.values(0)[:] = zn3.values(0)

        # sub-array copy from zone to zone
        x0 = self.ds.zone(0).values(0)
        x1 = self.ds.zone(1).values(0)
        self.assertEqual(len(x0), 3)
        self.assertEqual(len(x1), 9)
        x0[:] = np.full(len(x0), 0)

        x1[:] = np.full(len(x1), -1000)
        x1[:3] = x0
        np.testing.assert_allclose(x1[:3], x0[:])

        x1[:] = np.full(len(x1), -1000)
        x1[3:6] = x0
        np.testing.assert_allclose(x1[3:6], x0[:])

        x1[:] = np.full(len(x1), -1000)
        x1[3:-3] = x0
        np.testing.assert_allclose(x1[3:-3], x0[:])

        x1[:] = np.full(len(x1), -1000)
        x1[-3:] = x0
        np.testing.assert_allclose(x1[-3:], x0[:])

    def test_ravel_on_assignment(self):
        x = self.ds.zone(2).values(0)
        xx = np.linspace(0, 1, 27).reshape((3,3,3))
        x[:] = xx
        np.testing.assert_allclose(x[:], xx.ravel())


class TestArrayWithoutNumpy(unittest.TestCase):
    '''
    This test case focuses on data array operations where we have fall-back
    behavior when numpy is not installed.
    '''
    @hide_modules(['numpy'])
    def setUp(self):
        tp.new_layout()
        self.ds = tp.active_frame().create_dataset('D', ['x'])
        self.ds.add_ordered_zone('Z0', (3,))
        self.ds.add_ordered_zone('Z1', (3,3))
        self.ds.add_ordered_zone('Z2', (3,3,3))
        self.ds.add_ordered_zone('Z3', (1,1,3))
        self.ds.add_fe_zone(ZoneType.FEQuad, 'Z4', 8, 3)
        self.ds.add_poly_zone(ZoneType.FEPolyhedron, 'Z5', 8, 1, 12)
        self.ds.add_variable('n', FieldDataType.Double,
                             locations=ValueLocation.Nodal)
        self.ds.add_variable('c', FieldDataType.Int32,
                             locations=ValueLocation.CellCentered)

    @hide_modules(['numpy'])
    def test_limits(self):
        x = self.ds.zone(2).values(0)
        data = list(range(len(x)))
        x[:] = data
        self.assertAlmostEqual(x.min(), 0)
        self.assertAlmostEqual(x.max(), len(x)-1)
        self.assertAlmostEqual(x.minmax()[0], 0)
        self.assertAlmostEqual(x.minmax()[1], len(x)-1)

        x[3] = -3.14
        x[5] = 4096
        self.assertAlmostEqual(x.min(), -3.14, 6)
        self.assertAlmostEqual(x.max(), 4096, 6)

    @hide_modules(['numpy'])
    def test_data(self):
        x = self.ds.zone(2).values(0)
        with patch('logging.Logger.warning') as log:
            data = x.copy()
            for i in range(len(x)):
                self.assertEqual(x[i], data[i])
            self.assertEqual(log.call_count, 1)
            self.assertRegex(str(log.call_args_list[0]), r'.*Numpy.*')

    @hide_modules(['numpy'])
    def test_get_set_item_connected(self):
        x = self.ds.zone(2).values(0)
        with mocked_connected(), \
             patch('tecplot.session.data_altered'):
            with patch('tecplot.data.array.Array._native_reference', Mock(return_value=None)), \
                 patch('tecplot.data.array.Array.c_type', PropertyMock(return_value=ctypes.c_double)), \
                 patch_tecutil('DataValueArraySetByRef', return_value=1) as arrset, \
                 patch_tecutil('DataValueSetByRef', return_value=2) as valset:
                with patch('tecplot.data.array.Array._slice_range', Mock(return_value=range(0, 3, 1))):
                    x[:] = np.array([1.,2.,3.], dtype=np.float64)
                    valset.assert_not_called()
                    self.assertEqual(arrset.call_count, 1)
                    self.assertIsNone(arrset.call_args[0][0])
                    self.assertEqual(arrset.call_args[0][1], 1)
                    self.assertEqual(arrset.call_args[0][2], 3)
                    self.assertEqual(type(arrset.call_args[0][3]), (ctypes.c_double * 3))


if __name__ == '__main__':
    from .. import main
    main()
