from builtins import super

import os
import unittest

import numpy as np

import tecplot as tp
from tecplot.constant import *
from tecplot.exception import *
from tecplot import constant
from tecplot.plot.axis import Axis
from tecplot.plot.view import Cartesian2DView, Cartesian3DView, PolarView
from tecplot.tecutil import sv, ArgList

from ..property_test import PropertyTest
from ..sample_data import sample_data

from test import patch_tecutil, skip_if_sdk_version_before


class _TestView(object):
    def test_magnification(self):
        for val in [0.5, 1, 100, 200]:
            self.view.magnification = val
            self.assertAlmostEqual(self.view.magnification, val)
        with self.assertRaises(ValueError):
            self.view.magnification = 'badvalue'
        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            self.view.magnification = 0
        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            self.view.magnification = -1

        with patch_tecutil('ViewGetMagnification', return_value=(False, None)):
            with self.assertRaises(TecplotSystemError):
                _ = self.view.magnification

        with patch_tecutil('ViewSetMagnification', return_value=False):
            with self.assertRaises(TecplotSystemError):
                self.view.magnification = 1

    def test_translate(self):
        raise NotImplementedError

    def test_zoom(self):
        raise NotImplementedError


class _TestCartesian2DView(_TestView):
    def test_adjust_to_nice(self):
        self.view.zoom(1.999999, 1.99999, 9.9999999, 9.9999999)
        self.view.adjust_to_nice()
        self.assertAlmostEqual(self.xaxis.min, 2)
        self.assertAlmostEqual(self.yaxis.min, 2)
        self.assertAlmostEqual(self.xaxis.max, 10)
        self.assertAlmostEqual(self.yaxis.max, 10)

    def test_fit_to_nice(self):
        raise NotImplementedError


class _TestFieldView(_TestView):
    def test_center(self):
        raise NotImplementedError

    def test_fit(self):
        raise NotImplementedError

    def test_fit_data(self):
        raise NotImplementedError

    def test_fit_to_nice(self):
        raise NotImplementedError


class _TestLineView(_TestView):
    def test_center(self):
        raise NotImplementedError

    def test_fit(self):
        raise NotImplementedError

    def test_fit_data(self):
        raise NotImplementedError

    def test_extents(self):
        raise NotImplementedError


class TestXYLineView(_TestLineView, _TestCartesian2DView, unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        self.filename, ds = sample_data('xylines_poly')
        fr = tp.active_frame()
        plot = fr.plot(PlotType.XYLine)
        plot.activate()
        self.xaxis = plot.axes.x_axis(0)
        self.yaxis = plot.axes.y_axis(0)
        self.view = plot.view

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    def test_translate(self):
        self.xaxis.min = 0
        self.yaxis.min = 0
        self.xaxis.max = 10
        self.yaxis.max = 10
        self.view.translate(3, 3)
        self.assertAlmostEqual(self.xaxis.min, -0.4)
        self.assertAlmostEqual(self.yaxis.min, -0.3896103896)
        self.assertAlmostEqual(self.xaxis.max, 9.6)
        self.assertAlmostEqual(self.yaxis.max, 9.6103896103896)

    def test_zoom(self):
        self.xaxis.min = 0
        self.yaxis.min = 0
        self.xaxis.max = 10
        self.yaxis.max = 10
        self.view.zoom(1, 1, 9, 9)
        self.assertAlmostEqual(self.xaxis.min, 1)
        self.assertAlmostEqual(self.yaxis.min, 1)
        self.assertAlmostEqual(self.xaxis.max, 9)
        self.assertAlmostEqual(self.yaxis.max, 9)

    def test_center(self):
        self.view.fit()
        self.view.translate(50, 50)
        self.view.center()
        self.xaxis.adjust_range_to_nice()
        self.yaxis.adjust_range_to_nice()
        self.assertAlmostEqual(-10.0, self.xaxis.min)
        self.assertAlmostEqual( -0.6, self.yaxis.min)
        self.assertAlmostEqual( 10.0, self.xaxis.max)
        self.assertAlmostEqual(  0.4, self.yaxis.max)

    def test_fit(self):
        self.view.fit()
        self.view.translate(50, 50)
        self.assertNotEqual(-10.0, self.xaxis.min)
        self.assertNotEqual( -0.6, self.yaxis.min)
        self.assertNotEqual( 10.0, self.xaxis.max)
        self.assertNotEqual(  0.4, self.yaxis.max)
        self.view.fit()
        self.xaxis.adjust_range_to_nice()
        self.yaxis.adjust_range_to_nice()
        self.assertAlmostEqual(-10.0, self.xaxis.min)
        self.assertAlmostEqual( -0.6, self.yaxis.min)
        self.assertAlmostEqual( 10.0, self.xaxis.max)
        self.assertAlmostEqual(  0.4, self.yaxis.max)

    def test_fit_data(self):
        self.view.fit()
        self.view.translate(50, 50)
        self.assertNotEqual(-10.0, self.xaxis.min)
        self.assertNotEqual( -0.5, self.yaxis.min)
        self.assertNotEqual( 10.0, self.xaxis.max)
        self.assertNotEqual(  0.5, self.yaxis.max)
        self.view.fit_data()
        self.assertAlmostEqual(-10.0, self.xaxis.min, places=2)
        self.assertAlmostEqual( -0.5, self.yaxis.min, places=2)
        self.assertAlmostEqual( 10.0, self.xaxis.max, places=2)
        self.assertAlmostEqual(  0.5, self.yaxis.max, places=2)

    def test_fit_to_nice(self):
        self.view.fit()
        self.view.translate(50, 50)
        self.assertNotEqual(-15.0, self.xaxis.min)
        self.assertNotEqual( -0.8, self.yaxis.min)
        self.assertNotEqual( 15.0, self.xaxis.max)
        self.assertNotEqual(  0.6, self.yaxis.max)
        self.view.fit_to_nice()
        self.assertAlmostEqual(-15.0, self.xaxis.min, places=2)
        self.assertAlmostEqual( -0.8, self.yaxis.min, places=2)
        self.assertAlmostEqual( 15.0, self.xaxis.max, places=2)
        self.assertAlmostEqual(  0.6, self.yaxis.max, places=2)
        #print(self.xaxis.min, self.yaxis.min, self.xaxis.max, self.yaxis.max)

    def test_extents(self):
        if not __debug__:
            '''
            The following test asserts in SDK debug build.
            Possibly an overzealous check in the SDK

            Assertion: (!(!IsProcessingMacroCommand && !IsAddOnProcessingDisruptiveTecUtilFunction()))
            Tecplot version: 2018.3.1.97683
            File Name: sdk/trunk/libs/engine/src/sv_frame.cpp
            Line Number: 3444
            python3: sdk/trunk/libs/engine/src/sv_frame.cpp:3444:
                void __linuxassertproxy(const char*, const char*, int):
                    Assertion `(!(!IsProcessingMacroCommand && !IsAddOnProcessingDisruptiveTecUtilFunction()))' failed.
            lib/libexception.so(_ZN7tecplot15GetCurBacktraceB5cxx11Ei+0x8a)
            lib/libexception.so(_ZN7tecplot17PrintCurBacktraceEP8_IO_FILEi+0x75)
            lib/libtpsdkbase.so(+0x625cc5) [0x7fda505eccc5]
            lib/libtpsdkbase.so(TecUtilStyleSetLowLevelX+0xc04)
            lib/libtecutilchecked.so(tecUtilStyleSetLowLevelX+0x1f)
            '''
            self.view.fit()
            extents = self.view.extents
            self.view.extents = 1, 1, 9, 9
            np.testing.assert_array_almost_equal(self.view.extents,
                (1, 1, 9, 9))

    def test_view_action_failure(self):
        with patch_tecutil('ViewX', return_value=False):
            with self.assertRaises(TecplotSystemError):
                self.view.fit_to_nice()


class TestPolarView(_TestLineView, unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        self.filename, ds = sample_data('xylines_poly')
        fr = tp.active_frame()
        plot = fr.plot(PlotType.PolarLine)
        plot.activate()
        self.view = plot.view

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    def test_translate(self):
        self.view.fit()
        np.testing.assert_array_almost_equal(self.view.extents,
            (-0.648855, -0.576759999999, 0.648855, 0.576759999999))
        self.view.translate(10, 10)
        np.testing.assert_array_almost_equal(self.view.extents,
            (-0.7786259999999, -0.692112, 0.519084, 0.4614079999999))

    def test_zoom(self):
        self.view.fit()
        np.testing.assert_array_almost_equal(self.view.extents,
            (-0.648855, -0.576759999999, 0.648855, 0.576759999999))
        self.view.zoom(1, 1, 9, 9)
        np.testing.assert_array_almost_equal(self.view.extents,
            (0.5, 1, 9.5, 9))

    def test_center(self):
        self.view.fit()
        self.view.translate(50, 50)
        self.view.center()
        np.testing.assert_array_almost_equal(self.view.extents,
            (-0.648855, -0.57676, 0.648855, 0.57676))

    def test_fit(self):
        self.view.fit()
        self.view.translate(50, 50)
        self.view.fit()
        np.testing.assert_array_almost_equal(self.view.extents,
            (-0.648855, -0.57676, 0.648855, 0.57676))

    def test_fit_data(self):
        self.view.fit()
        self.view.translate(50, 50)
        self.view.fit_data()
        np.testing.assert_array_almost_equal(self.view.extents,
            (-0.562612, -0.5001, 0.562612, 0.5001))

    def test_extents(self):
        self.view.fit()
        self.view.extents = -1, -1, 1, 1
        self.assertAlmostEqual(self.view.extents.x1, -1)
        self.assertAlmostEqual(self.view.extents.x2, 1)

        self.view.extents[0] = -1.2
        self.assertAlmostEqual(self.view.extents[0], -1.2)
        self.view.extents.x1 = -1.1
        self.assertAlmostEqual(self.view.extents.x1, -1.1)

        self.view.extents[2] = 1.2
        self.assertAlmostEqual(self.view.extents[2], 1.2)
        self.view.extents.x2 = 1.1
        self.assertAlmostEqual(self.view.extents.x2, 1.1)

        # while x1, x2 can be set to specific values, setting y1, y2
        # is just a suggestion and the engine only tries to get close
        # but sometimes it doesn't change much at all
        self.view.extents.y1 = -1.2
        y1 = self.view.extents.y1
        self.view.extents[1] = -1.0
        self.assertNotAlmostEqual(self.view.extents[1], y1)
        self.assertNotAlmostEqual(self.view.extents.y1, y1)

        self.view.extents.y2 = -1.2
        y2 = self.view.extents.y2
        self.view.extents[3] = -1.0
        self.assertNotAlmostEqual(self.view.extents[3], y2)
        self.assertNotAlmostEqual(self.view.extents.y2, y2)

        self.view.fit()
        np.testing.assert_array_almost_equal(self.view.extents,
            (-0.648855, -0.57676 ,  0.648855,  0.57676))

    def test_moved_attribute(self):
        with self.assertRaises(AttributeError):
            self.view.reset_to_entire_circle()


class TestCartesian2DFieldView(_TestFieldView, _TestCartesian2DView,
                               unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        self.filename,ds = sample_data('10x10x10')
        fr = tp.active_frame()
        plot = fr.plot(PlotType.Cartesian2D)
        plot.activate()
        self.xaxis = plot.axes.x_axis
        self.yaxis = plot.axes.y_axis
        self.view = plot.view

        # show some surfaces so we can have blanking
        plot.show_contour = True
        plot.fieldmap(0).surfaces.surfaces_to_plot = SurfacesToPlot.BoundaryFaces
        tp.macro.execute_command('''
            $!Blanking Value{Include = Yes}
            $!Blanking Value{Constraint 1 {VarA = 1}}
            $!Blanking Value{Constraint 1 {Include = Yes}}
            $!Blanking Value{Constraint 1 {ValueCutoff = 0.5}}
            $!Blanking Value{Constraint 2 {VarA = 2}}
            $!Blanking Value{Constraint 2 {Include = Yes}}
            $!Blanking Value{Constraint 2 {ValueCutoff = 0.5}}
            $!Blanking Value{Constraint 3 {VarA = 3}}
            $!Blanking Value{Constraint 3 {Include = Yes}}
            $!Blanking Value{Constraint 3 {ValueCutoff = 0.5}}
        ''')

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    def test_translate(self):
        self.xaxis.min = 0
        self.yaxis.min = 0
        self.xaxis.max = 10
        self.yaxis.max = 10
        self.view.translate(3, 3)
        self.assertAlmostEqual(self.xaxis.min, -0.4383116883116883)
        self.assertAlmostEqual(self.yaxis.min, -0.3896103896103896)
        self.assertAlmostEqual(self.xaxis.max, 10.519480519480519)
        self.assertAlmostEqual(self.yaxis.max, 9.6103896103896)

        with patch_tecutil('ViewTranslate', return_value=False):
            with self.assertRaises(TecplotSystemError):
                self.view.translate(3, 3)

    def test_zoom(self):
        self.xaxis.min = 0
        self.yaxis.min = 0
        self.xaxis.max = 10
        self.yaxis.max = 10
        self.view.zoom(1, 1, 9, 9)
        self.assertAlmostEqual(self.xaxis.min, 1)
        self.assertAlmostEqual(self.yaxis.min, 1)
        self.assertAlmostEqual(self.xaxis.max, 9.766233766233766)
        self.assertAlmostEqual(self.yaxis.max, 9)

        with patch_tecutil('ViewZoom', return_value=False):
            with self.assertRaises(TecplotSystemError):
                self.view.zoom(1, 1, 9, 9)

    def test_center(self):
        #print(self.xaxis.min, self.yaxis.min, self.xaxis.max, self.yaxis.max)
        self.view.fit()
        self.view.translate(50, 50)
        self.view.center(False)
        np.testing.assert_array_almost_equal(
            (self.xaxis.min, self.yaxis.min, self.xaxis.max, self.yaxis.max),
            (0.256469, 0.277756, 0.743531, 0.722244))
        self.view.center()
        np.testing.assert_array_almost_equal(
            (self.xaxis.min, self.yaxis.min, self.xaxis.max, self.yaxis.max),
            (0.534247, 0.555533, 1.021309, 1.000022))

    def test_fit(self):
        self.view.fit()
        self.view.translate(50, 50)
        self.view.fit(False)
        np.testing.assert_array_almost_equal(
            (self.xaxis.min, self.yaxis.min, self.xaxis.max, self.yaxis.max),
            (0.      , 0.      , 1.095889, 1.0001))
        self.view.fit()
        np.testing.assert_array_almost_equal(
            (self.xaxis.min, self.yaxis.min, self.xaxis.max, self.yaxis.max),
            (0.555556, 0.555556, 1.042617, 1.000044))

    def test_fit_data(self):
        self.view.fit()
        self.view.translate(50, 50)
        self.view.fit_data(False)
        np.testing.assert_array_almost_equal(
            (self.xaxis.min, self.yaxis.min, self.xaxis.max, self.yaxis.max),
            (0.      , 0.      , 1.095889, 1.0001))
        self.view.fit_data()
        np.testing.assert_array_almost_equal(
            (self.xaxis.min, self.yaxis.min, self.xaxis.max, self.yaxis.max),
            (0.555556, 0.555556, 1.042617, 1.000044))

    def test_fit_to_nice(self):
        self.view.fit()
        self.view.translate(50, 50)
        self.view.fit_to_nice(False)
        np.testing.assert_array_almost_equal(
            (self.xaxis.min, self.yaxis.min, self.xaxis.max, self.yaxis.max),
            (-0.2, -0.2,  1.2,  1.))
        self.view.fit_to_nice()
        np.testing.assert_array_almost_equal(
            (self.xaxis.min, self.yaxis.min, self.xaxis.max, self.yaxis.max),
            (0.2, 0.4, 1.2, 1.3))


class TestCartesian3DView(_TestFieldView, unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        self.filename, ds = sample_data('10x10x10')
        fr = tp.active_frame()
        plot = fr.plot(PlotType.Cartesian3D)
        plot.activate()
        self.view = plot.view

        # show some surfaces so we can have blanking
        plot.show_contour = True
        plot.fieldmap(0).surfaces.surfaces_to_plot = SurfacesToPlot.BoundaryFaces
        tp.macro.execute_command('''
            $!Blanking Value{Include = Yes}
            $!Blanking Value{Constraint 1 {VarA = 1}}
            $!Blanking Value{Constraint 1 {Include = Yes}}
            $!Blanking Value{Constraint 1 {ValueCutoff = 0.5}}
            $!Blanking Value{Constraint 2 {VarA = 2}}
            $!Blanking Value{Constraint 2 {Include = Yes}}
            $!Blanking Value{Constraint 2 {ValueCutoff = 0.5}}
            $!Blanking Value{Constraint 3 {VarA = 3}}
            $!Blanking Value{Constraint 3 {Include = Yes}}
            $!Blanking Value{Constraint 3 {ValueCutoff = 0.5}}
        ''')

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    def test_translate(self):
        self.view.fit()
        self.view.position = 8, 5, 6
        self.view.translate(10, 10)
        np.testing.assert_array_almost_equal(
            self.view.position,
            (8.068537, 4.950136, 5.940377))

    def test_zoom(self):
        self.view.fit()
        self.view.position = 8, 5, 6
        self.view.zoom(1, 1, 9, 9)
        np.testing.assert_array_almost_equal(
            self.view.position,
            (3.5776043594251394, 8.05035839726953, 9.991905598179686))

    def test_center(self):
        self.view.fit()
        self.view.translate(50, 50)
        self.view.center(False)
        np.testing.assert_array_almost_equal(
            self.view.position,
            (8.073557, 4.872595, 5.549038))
        self.view.center()
        np.testing.assert_array_almost_equal(
            self.view.position,
            (8.000707, 4.947938, 5.593064))

    def test_fit(self):
        self.view.fit()
        self.view.translate(50, 50)
        self.view.fit(False)
        np.testing.assert_array_almost_equal(
            self.view.position,
            (8.073557, 4.872595, 5.549038))
        self.view.fit()
        np.testing.assert_array_almost_equal(
            self.view.position,
            (8.000707, 4.947938, 5.593064))

    def test_fit_data(self):
        self.view.fit()
        self.view.translate(50, 50)
        self.view.fit_data(False)
        np.testing.assert_array_almost_equal(
            self.view.position,
            (8.073557, 4.872595, 5.549038))
        self.view.fit_data()
        np.testing.assert_array_almost_equal(
            self.view.position,
            (8.000707, 4.947938, 5.593064))

    def test_fit_to_nice(self):
        with self.assertRaises(AttributeError):
            self.view.fit_to_nice()

    def test_fit_surfaces(self):
        self.view.fit()
        self.view.translate(50, 50)
        self.view.fit_surfaces(False)
        np.testing.assert_array_almost_equal(
            self.view.position,
            (8.073557, 4.872595, 5.549038))
        self.view.fit_surfaces()
        np.testing.assert_array_almost_equal(
            self.view.position,
            (8.000707, 4.947938, 5.593064))

    def test_rotation_origin(self):
        with self.assertRaises((TecplotSystemError, TecplotLogicError)):
            self.view.rotation_origin = -100, 0, 0

        with self.assertRaises((TecplotSystemError, TecplotLogicError)):
            self.view.rotation_origin = 0, 0, 100

        self.view.rotation_origin = 0, 0, 0
        np.testing.assert_array_almost_equal(
            self.view.rotation_origin, (0, 0, 0))

        self.view.rotation_origin = 1, 2, 3
        np.testing.assert_array_almost_equal(
            self.view.rotation_origin, (1, 2, 3))

    def test_rotate_failure(self):
        with patch_tecutil('ViewRotate3D', return_value=False):
            with self.assertRaises(TecplotSystemError):
                self.view.rotate_axes(5)

    def test_rotate_axes(self):
        self.view.position = 0, 0, 1
        self.view.rotation_origin = (0, 0, 0)
        self.view.rotate_to_angles(0, 0, 0)

        self.view.rotate_axes(180)
        np.testing.assert_array_almost_equal(
            self.view.position, (0, -0.866025, 0.5))
        np.testing.assert_array_almost_equal(
            (self.view.psi, self.view.theta, self.view.alpha),
            (0, 180, 0))

        self.view.rotate_axes(180, (0, 1, 0))
        np.testing.assert_array_almost_equal(
            (self.view.psi, self.view.theta, self.view.alpha),
            (180, 0, 0))

        self.view.rotate_axes(180, (-1, 0, 0))
        np.testing.assert_array_almost_equal(
            (self.view.psi, self.view.theta, self.view.alpha),
            (0, 0, 0))

        self.view.rotate_axes(90, (-1, 1, 0))
        np.testing.assert_array_almost_equal(
            (self.view.psi, self.view.theta, self.view.alpha),
            (90, 45, -45))

        self.view.position = 5, 6, 7
        self.view.rotation_origin = (5, 4, 3)
        self.view.rotate_to_angles(0, 0, 0)
        self.view.rotate_axes(180)
        np.testing.assert_array_almost_equal(
            self.view.position, (3.171573, 0.171573, 1.585786))
        np.testing.assert_array_almost_equal(
            (self.view.psi, self.view.theta, self.view.alpha),
            (0, 180, 0))

    def test_rotate_to_angles(self):
        self.view.rotate_to_angles(1, 2, 3)
        np.testing.assert_array_almost_equal(
            (self.view.psi, self.view.theta, self.view.alpha),
            (1, 2, 3))
        self.view.rotate_to_angles(2, 3, 4)
        np.testing.assert_array_almost_equal(
            (self.view.psi, self.view.theta, self.view.alpha),
            (2, 3, 4))

    def test_rotate_viewer(self):
        self.view.position = 0, 0, 1
        self.view.rotation_origin = (0, 0, 0)
        self.view.rotate_to_angles(0, 0, 0)

        self.view.rotate_viewer(180)
        np.testing.assert_array_almost_equal(
            self.view.position, (0, 0.866025, 0.5))
        np.testing.assert_array_almost_equal(
            (self.view.psi, self.view.theta, self.view.alpha),
            (0, 180, 0))

        self.view.rotate_viewer(180, (0, 1, 0))
        np.testing.assert_array_almost_equal(
            (self.view.psi, self.view.theta, self.view.alpha),
            (180, 0, 0))

        self.view.rotate_viewer(180, (1, 0, 0))
        np.testing.assert_array_almost_equal(
            (self.view.psi, self.view.theta, self.view.alpha),
            (0, 0, 0))

        self.view.rotate_viewer(90, (-1, 1, 0))
        np.testing.assert_array_almost_equal(
            (self.view.psi, self.view.theta, self.view.alpha),
            (90, 45, -45))

    def test_alpha(self):
        for val in [-1, 0, 0.5, 1, 100]:
            self.view.alpha = val
            self.assertAlmostEqual(self.view.alpha, val)
        self.view.alpha = 30 + 360
        self.assertAlmostEqual(self.view.alpha, 30)
        with self.assertRaises(ValueError):
            self.view.alpha = 'badvalue'

    def test_distance(self):
        for val in [-1, 0, 0.5, 1, 100]:
            self.view.distance = val
            self.assertAlmostEqual(self.view.distance, val)
        with self.assertRaises(ValueError):
            self.view.distance = 'badvalue'

        with patch_tecutil('Set3DEyeDistance', return_value=False):
            with self.assertRaises(TecplotSystemError):
                self.view.distance = 1

    @skip_if_sdk_version_before(2017, 2)
    def test_field_of_view(self):
        self.view.projection = Projection.Perspective
        for val in [0.5, 1, 100]:
            self.view.field_of_view = val
            self.assertAlmostEqual(self.view.field_of_view, val)
        with self.assertRaises(ValueError):
            self.view.field_of_view = 'badvalue'
        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            self.view.field_of_view = 0
        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            self.view.field_of_view = -1

        self.view.projection = Projection.Orthographic
        with self.assertRaises((TecplotValueError, TecplotSystemError)):
            self.view.field_of_view = 10.0

    def test_position(self):
        self.view.position = (0, 0, 0)
        np.testing.assert_array_almost_equal(self.view.position, (0, 0, 0))
        self.view.position = (1, 2, 3)
        np.testing.assert_array_almost_equal(self.view.position, (1, 2, 3))

    @skip_if_sdk_version_before(2017, 2)
    def test_projection(self):
        for val in [Projection.Orthographic, Projection.Perspective,
                    Projection.Orthographic]:
            self.view.projection = val
            self.assertEqual(self.view.projection, val)
        with self.assertRaises(ValueError):
            self.view.projection = 'badvalue'

    def test_psi(self):
        for val in [-1, 0, 0.5, 1, 100]:
            self.view.psi = val
            self.assertAlmostEqual(self.view.psi, val)
        self.view.psi = 30 + 360
        self.assertAlmostEqual(self.view.psi, 30)
        with self.assertRaises(ValueError):
            self.view.psi = 'badvalue'

    def test_theta(self):
        for val in [-1, 0, 0.5, 1, 100]:
            self.view.theta = val
            self.assertAlmostEqual(self.view.theta, val)
        self.view.theta = 30 + 360
        self.assertAlmostEqual(self.view.theta, 30)
        with self.assertRaises(ValueError):
            self.view.theta = 'badvalue'

    def test_width(self):
        for val in [0.5, 1, 100]:
            self.view.width = val
            self.assertAlmostEqual(self.view.width, val)
        with self.assertRaises(ValueError):
            self.view.width = 'badvalue'
        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            self.view.width = 0
        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            self.view.width = -1


class TestReadOnlyViewport(unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        self.filename, ds = sample_data('10x10x10')
        fr = tp.active_frame()
        plot = fr.plot(PlotType.Cartesian3D)
        plot.activate()
        self.viewport = plot.axes.viewport

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    def test_bottom(self):
        self.assertAlmostEqual(self.viewport.bottom, 0)

    def test_left(self):
        self.assertAlmostEqual(self.viewport.left, 0)

    def test_right(self):
        self.assertAlmostEqual(self.viewport.right, 100)

    def test_top(self):
        self.assertAlmostEqual(self.viewport.top, 100)


class _TestViewport(object):
    def test_bottom(self):
        self.viewport.bottom = 0
        self.viewport.left = 0
        self.viewport.right = 100
        self.viewport.top = 100

        for val in [0, 0.5, 1, 95]:
            self.viewport.bottom = val
            self.assertAlmostEqual(self.viewport.bottom, val)

        self.viewport.bottom = 100
        self.assertAlmostEqual(self.viewport.bottom, 95)

        with self.assertRaises(ValueError):
            self.viewport.bottom = 'badvalue'
        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            self.viewport.bottom = -1
        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            self.viewport.bottom = 101

    def test_left(self):
        self.viewport.bottom = 0
        self.viewport.left = 0
        self.viewport.right = 100
        self.viewport.top = 100

        for val in [0, 0.5, 1, 95]:
            self.viewport.left = val
            self.assertAlmostEqual(self.viewport.left, val)

        self.viewport.left = 100
        self.assertAlmostEqual(self.viewport.left, 95)

        with self.assertRaises(ValueError):
            self.viewport.left = 'badvalue'
        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            self.viewport.left = -1
        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            self.viewport.left = 101

    def test_right(self):
        self.viewport.bottom = 0
        self.viewport.left = 0
        self.viewport.right = 100
        self.viewport.top = 100

        for val in [5, 50, 99.5, 100]:
            self.viewport.right = val
            self.assertAlmostEqual(self.viewport.right, val)

        self.viewport.right = 0
        self.assertAlmostEqual(self.viewport.right, 5)

        with self.assertRaises(ValueError):
            self.viewport.right = 'badvalue'
        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            self.viewport.right = -1
        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            self.viewport.right = 101

    def test_top(self):
        self.viewport.bottom = 0
        self.viewport.left = 0
        self.viewport.right = 100
        self.viewport.top = 100

        for val in [5, 50, 99.5, 100]:
            self.viewport.top = val
            self.assertAlmostEqual(self.viewport.top, val)

        self.viewport.top = 0
        self.assertAlmostEqual(self.viewport.top, 5)

        with self.assertRaises(ValueError):
            self.viewport.top = 'badvalue'
        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            self.viewport.top = -1
        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            self.viewport.top = 101


class TestCartesian2DViewport(_TestViewport, unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        self.filename, ds = sample_data('10x10x10')
        fr = tp.active_frame()
        plot = fr.plot(PlotType.Cartesian2D)
        plot.activate()
        self.viewport = plot.axes.viewport

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    def test_nice_fit_buffer(self):
        for val in [0, 0.5, 1, 100]:
            self.viewport.nice_fit_buffer = val
            self.assertAlmostEqual(self.viewport.nice_fit_buffer, val)
        with self.assertRaises(ValueError):
            self.viewport.nice_fit_buffer = 'badvalue'
        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            self.viewport.nice_fit_buffer = -1

    def test_top_snap_target(self):
        for val in [0, 0.5, 1, 100]:
            self.viewport.top_snap_target = val
            self.assertAlmostEqual(self.viewport.top_snap_target, val)
        with self.assertRaises(ValueError):
            self.viewport.top_snap_target = 'badvalue'
        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            self.viewport.top_snap_target = -1

    def test_top_snap_tolerance(self):
        for val in [0, 0.5, 1, 100]:
            self.viewport.top_snap_tolerance = val
            self.assertAlmostEqual(self.viewport.top_snap_tolerance, val)
        with self.assertRaises(ValueError):
            self.viewport.top_snap_tolerance = 'badvalue'
        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            self.viewport.top_snap_tolerance = -1


class TestPolarViewport(_TestViewport, unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        self.filename, ds = sample_data('xylines_poly')
        fr = tp.active_frame()
        plot = fr.plot(PlotType.PolarLine)
        plot.activate()
        self.viewport = plot.axes.viewport

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    def test_fill_color(self):
        for val in [Color.Black, None, Color.Red, Color.White]:
            self.viewport.fill_color = val
            self.assertEqual(self.viewport.fill_color, val)
        with self.assertRaises(ValueError):
            self.viewport.fill_color = 0.5

    def test_show_border(self):
        for val in [True, False, True]:
            self.viewport.show_border = val
            self.assertEqual(self.viewport.show_border, val)

    def test_border_thickness(self):
        for val in [0.5, 1, 100]:
            self.viewport.border_thickness = val
            self.assertAlmostEqual(self.viewport.border_thickness, val)
        with self.assertRaises(ValueError):
            self.viewport.border_thickness = 'badvalue'
        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            self.viewport.border_thickness = 0

    def test_border_color(self):
        for val in [Color.Black, Color.Red, Color.White]:
            self.viewport.border_color = val
            self.assertEqual(self.viewport.border_color, val)
        with self.assertRaises(ValueError):
            self.viewport.border_color = 0.5


if __name__ == '__main__':
    from .. import main
    main()
