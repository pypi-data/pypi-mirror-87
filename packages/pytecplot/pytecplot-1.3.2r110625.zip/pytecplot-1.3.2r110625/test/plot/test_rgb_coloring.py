import os
import unittest

from unittest.mock import patch, Mock

import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *

from .. import skip_if_sdk_version_before, mocked_sdk_version, mocked_connected
from ..sample_data import sample_data


class TestRGBColoring(unittest.TestCase):
    @skip_if_sdk_version_before(2018, 2)
    def setUp(self):
        tp.new_layout()
        self.filename,self.dataset = sample_data('10x10x10')
        frame = tp.active_frame()
        frame.plot_type = PlotType.Cartesian3D
        plot = frame.plot()
        plot.show_contour = True
        plot.rgb_coloring.red_variable = self.dataset.variable(0)
        plot.rgb_coloring.green_variable = self.dataset.variable(1)
        plot.rgb_coloring.blue_variable = self.dataset.variable(2)

        fmap = plot.fieldmap(0)
        fmap.contour.flood_contour_group = plot.rgb_coloring
        self.rgb_coloring = plot.rgb_coloring

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    def test_eq(self):
        fr = tp.active_frame()
        other = tp.active_page().add_frame().plot(PlotType.Cartesian2D).rgb_coloring
        fr.activate()
        self.assertEqual(self.rgb_coloring, fr.plot().rgb_coloring)
        self.assertNotEqual(self.rgb_coloring, other)
        self.assertTrue(self.rgb_coloring == fr.plot().rgb_coloring)
        self.assertFalse(self.rgb_coloring == other)
        self.assertFalse(self.rgb_coloring != fr.plot().rgb_coloring)
        self.assertTrue(self.rgb_coloring != other)

    def test_index(self):
        self.assertEqual(self.rgb_coloring.index, Color.RGBColor.value)

    def test_legend(self):
        self.assertIsInstance(self.rgb_coloring.legend,
                              tp.legend.RGBColoringLegend)

    def test_mode(self):
        for val in list(RGBMode)[:3]:
            self.rgb_coloring.mode = val
            self.assertEqual(self.rgb_coloring.mode, val)
        with self.assertRaises(ValueError):
            self.rgb_coloring.mode = 0.5
        with self.assertRaises(ValueError):
            self.rgb_coloring.mode = 'badvalue'

    def test_min_intensity(self):
        for val in [-1, -0.5, 0, 0.5, 1, 100]:
            self.rgb_coloring.min_intensity = val
            self.assertAlmostEqual(self.rgb_coloring.min_intensity, val)
        with self.assertRaises(ValueError):
            self.rgb_coloring.min_intensity = 'badvalue'

    def test_max_intensity(self):
        for val in [-1, -0.5, 0, 0.5, 1, 100]:
            self.rgb_coloring.max_intensity = val
            self.assertAlmostEqual(self.rgb_coloring.max_intensity, val)
        with self.assertRaises(ValueError):
            self.rgb_coloring.max_intensity = 'badvalue'

    def test_red_variable(self):
        v0 = self.dataset.variable(0)
        v1 = self.dataset.variable(1)
        self.rgb_coloring.red_variable_index = v0.index
        self.assertEqual(self.rgb_coloring.red_variable_index, v0.index)
        self.assertEqual(self.rgb_coloring.red_variable, v0)
        self.rgb_coloring.red_variable_index = v1.index
        self.assertEqual(self.rgb_coloring.red_variable_index, v1.index)
        self.assertEqual(self.rgb_coloring.red_variable, v1)
        self.rgb_coloring.red_variable = v0
        self.assertEqual(self.rgb_coloring.red_variable_index, v0.index)
        self.assertEqual(self.rgb_coloring.red_variable, v0)

        if __debug__:
            class V:
                index = 0
            with mocked_sdk_version(2018, 1), mocked_connected():
                with self.assertRaises(TecplotOutOfDateEngineError):
                    self.rgb_coloring.red_variable = V()
                with self.assertRaises(TecplotOutOfDateEngineError):
                    self.rgb_coloring.red_variable_index = 0

    def test_green_variable(self):
        v0 = self.dataset.variable(0)
        v1 = self.dataset.variable(1)
        self.rgb_coloring.green_variable_index = v0.index
        self.assertEqual(self.rgb_coloring.green_variable_index, v0.index)
        self.assertEqual(self.rgb_coloring.green_variable, v0)
        self.rgb_coloring.green_variable_index = v1.index
        self.assertEqual(self.rgb_coloring.green_variable_index, v1.index)
        self.assertEqual(self.rgb_coloring.green_variable, v1)
        self.rgb_coloring.green_variable = v0
        self.assertEqual(self.rgb_coloring.green_variable_index, v0.index)
        self.assertEqual(self.rgb_coloring.green_variable, v0)

        if __debug__:
            class V:
                index = 0
            with mocked_sdk_version(2018, 1), mocked_connected():
                with self.assertRaises(TecplotOutOfDateEngineError):
                    self.rgb_coloring.green_variable = V()
                with self.assertRaises(TecplotOutOfDateEngineError):
                    self.rgb_coloring.green_variable_index = 0

    def test_blue_variable(self):
        v0 = self.dataset.variable(0)
        v1 = self.dataset.variable(1)
        self.rgb_coloring.blue_variable_index = v0.index
        self.assertEqual(self.rgb_coloring.blue_variable_index, v0.index)
        self.assertEqual(self.rgb_coloring.blue_variable, v0)
        self.rgb_coloring.blue_variable_index = v1.index
        self.assertEqual(self.rgb_coloring.blue_variable_index, v1.index)
        self.assertEqual(self.rgb_coloring.blue_variable, v1)
        self.rgb_coloring.blue_variable = v0
        self.assertEqual(self.rgb_coloring.blue_variable_index, v0.index)
        self.assertEqual(self.rgb_coloring.blue_variable, v0)

        if __debug__:
            class V:
                index = 0
            with mocked_connected():
                with patch('tecplot.plot.RGBColoring._get_style', Mock(return_value=0)):
                    with patch('tecplot.plot.RGBColoring._set_style', Mock()) as set_style:
                        self.rgb_coloring.blue_variable_index = 0
                        self.assertEqual(set_style.call_count, 1)
                with patch('tecplot.plot.RGBColoring._get_style', Mock(return_value=-1)):
                    with patch('tecplot.plot.RGBColoring._set_style', Mock()) as set_style:
                        self.rgb_coloring.blue_variable_index = 0
                        self.assertEqual(set_style.call_count, 4)
                with mocked_sdk_version(2018, 1):
                    with self.assertRaises(TecplotOutOfDateEngineError):
                        self.rgb_coloring.blue_variable = V()
                    with self.assertRaises(TecplotOutOfDateEngineError):
                        self.rgb_coloring.blue_variable_index = 0


if __name__ == '__main__':
    from .. import main
    main()
