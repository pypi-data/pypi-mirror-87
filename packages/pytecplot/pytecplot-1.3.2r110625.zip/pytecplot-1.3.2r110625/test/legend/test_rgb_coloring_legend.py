import os, unittest

import tecplot as tp
from tecplot.constant import *
from tecplot.exception import *

from .. import skip_if_sdk_version_before
from ..sample_data import sample_data
from .test_legend import TestLegend


class TestRGBColoringLegend(TestLegend, unittest.TestCase):
    @skip_if_sdk_version_before(2018, 2)
    def setUp(self):
        tp.new_layout()
        self.filename,self.dataset = sample_data('10x10x10')
        frame = tp.active_frame()
        frame.plot_type = PlotType.Cartesian3D
        plot = frame.plot()
        plot.show_contour = True
        with tp.session.suspend():
            plot.rgb_coloring.red_variable = self.dataset.variable(0)
            plot.rgb_coloring.green_variable = self.dataset.variable(1)
            plot.rgb_coloring.blue_variable = self.dataset.variable(2)

        fmap = plot.fieldmap(0)
        fmap.contour.flood_contour_group = plot.rgb_coloring
        self.legend = plot.rgb_coloring.legend

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    def test_font(self):
        self.assertIsInstance(self.legend.font, tp.text.Font)

    def test_show_labels(self):
        for val in [True, False, True]:
            self.legend.show_labels = val
            self.assertEqual(self.legend.show_labels, val)

    def test_height(self):
        for val in [0.5, 1, 2]:
            self.legend.height = val
            self.assertAlmostEqual(self.legend.height, val)
        with self.assertRaises((TecplotSystemError, TecplotLogicError)):
            self.legend.height = -1
        with self.assertRaises((TecplotSystemError, TecplotLogicError)):
            self.legend.height = 0
        with self.assertRaises(ValueError):
            self.legend.height = 'badvalue'

    def test_orientation(self):
        for val in RGBLegendOrientation:
            self.legend.orientation = val
            self.assertEqual(self.legend.orientation, val)
        with self.assertRaises(ValueError):
            self.legend.orientation = 'badvalue'

    def test_red_label(self):
        for val in ['aa', 'bb', '', 0, 3.14]:
            self.legend.red_label = val
            self.assertEqual(self.legend.red_label, str(val))

    def test_green_label(self):
        for val in ['aa', 'bb', '', 0, 3.14]:
            self.legend.green_label = val
            self.assertEqual(self.legend.green_label, str(val))

    def test_blue_label(self):
        for val in ['aa', 'bb', '', 0, 3.14]:
            self.legend.blue_label = val
            self.assertEqual(self.legend.blue_label, str(val))

    def test_use_variable_for_red_label(self):
        for val in [True, False, True]:
            self.legend.use_variable_for_red_label = val
            self.assertEqual(self.legend.use_variable_for_red_label, val)

    def test_use_variable_for_green_label(self):
        for val in [True, False, True]:
            self.legend.use_variable_for_green_label = val
            self.assertEqual(self.legend.use_variable_for_green_label, val)

    def test_use_variable_for_blue_label(self):
        for val in [True, False, True]:
            self.legend.use_variable_for_blue_label = val
            self.assertEqual(self.legend.use_variable_for_blue_label, val)


if __name__ == '__main__':
    from .. import main
    main()
