import os, unittest, warnings

import tecplot as tp
from tecplot.constant import *
from tecplot.exception import *

from ..sample_data import sample_data
from .test_legend import TestTabularLegend


class TestContourLegend(TestTabularLegend, unittest.TestCase):
    def setUp(self):
        warnings.simplefilter("always")

        tp.new_layout()
        self.filename, self.dataset = sample_data('2x2x3_overlap')
        frame = tp.active_frame()

        plot = frame.plot(PlotType.Cartesian3D)
        plot.vector.u_variable_index = 0
        plot.vector.v_variable_index = 1
        plot.vector.w_variable_index = 2
        self.legend = plot.contour(0).legend

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    def test_auto_resize(self):
        for val in [True, False, True]:
            self.legend.auto_resize = val
            self.assertEqual(self.legend.auto_resize, val)

    def test_header_font(self):
        self.assertIsInstance(self.legend.header_font, tp.text.LegendFont)

    def test_number_font(self):
        self.assertIsInstance(self.legend.number_font, tp.text.LegendFont)

    def test_show_cutoff_levels(self):
        for val in [True, False, True]:
            self.legend.show_cutoff_levels = val
            self.assertEqual(self.legend.show_cutoff_levels, val)

        with self.assertRaises(TecplotInterfaceChangeError):
            _ = self.legend.include_cutoff_levels
        with self.assertRaises(TecplotInterfaceChangeError):
            self.legend.include_cutoff_levels = None

    def test_vertical(self):
        for val in [True, False, True]:
            self.legend.vertical = val
            self.assertEqual(self.legend.vertical, val)

    def test_label_increment(self):
        for i in [.5, 1, 1000]:
            self.legend.label_increment = i
            self.assertAlmostEqual(self.legend.label_increment, i)
        with self.assertRaises((TecplotSystemError, TecplotLogicError)):
            self.legend.label_increment = -1
        with self.assertRaises((TecplotSystemError, TecplotLogicError)):
            self.legend.label_increment = 0
        with self.assertRaises(ValueError):
            self.legend.label_increment = 'badvalue'

    def test_label_location(self):
        for val in ContLegendLabelLocation:
            self.legend.label_location = val
            self.assertEqual(self.legend.label_location, val)
        with self.assertRaises(ValueError):
            self.legend.label_location = 0.5
        with self.assertRaises(ValueError):
            self.legend.label_location = 'badvalue'

    def test_overlay_bar_grid(self):
        for val in [True, False, True]:
            self.legend.overlay_bar_grid = val
            self.assertEqual(self.legend.overlay_bar_grid, val)

    def test_show_header(self):
        for val in [True, False, True]:
            self.legend.show_header = val
            self.assertEqual(self.legend.show_header, val)

    def test_label_step(self):
        contour_labels = self.legend.contour.labels
        for val in [1, 2, 3.14, 10]:
            self.legend.label_step = val
            self.assertEqual(self.legend.label_step, int(val))
            self.assertEqual(contour_labels.step, int(val))
        with self.assertRaises(ValueError):
            self.legend.label_step = 'badtype'
        with self.assertRaises(TypeError):
            self.legend.label_step = None
        with self.assertRaises(TecplotSystemError):
            self.legend.label_step = -1
        with self.assertRaises(TecplotSystemError):
            self.legend.label_step = 0

    def test_label_format(self):
        fmt = self.legend.label_format
        fmt_alt = self.legend.contour.labels.format
        for val in [1,2,10]:
            fmt.precision = val
            self.assertAlmostEqual(fmt.precision, val)
            self.assertAlmostEqual(fmt.precision, fmt_alt.precision)
        with self.assertRaises(ValueError):
            fmt.precision = 'badvalue'
        with self.assertRaises(TecplotSystemError):
            fmt.precision = -1
        with self.assertRaises(TecplotSystemError):
            fmt.precision = 0


if __name__ == '__main__':
    from .. import main
    main()

