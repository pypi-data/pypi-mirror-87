import os, unittest

import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *

from test import sample_data


class TestFont(unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        plot = tp.active_frame().plot(PlotType.Sketch)
        self.font = plot.axes.x_axis.title.font

    def test_bold(self):
        for val in [True,False,True]:
            self.font.bold = val
            self.assertEqual(self.font.bold, val)

    def test_italic(self):
        for val in [True,False,True]:
            self.font.italic = val
            self.assertEqual(self.font.italic, val)

    def test_size(self):
        self.font.size_units = Units.Frame
        for val in [1,10,100,150]:
            self.font.size = val
            self.assertEqual(self.font.size, val)
        with self.assertRaises(ValueError):
            self.font.size = 'badvalue'
        with self.assertRaises(TecplotSystemError):
            self.font.size = -1
        with self.assertRaises(TecplotSystemError):
            self.font.size = 0

        self.font.size_units = Units.Point
        for val in [1,10,100,150]:
            self.font.size = val
            self.assertEqual(self.font.size, val)
        with self.assertRaises(ValueError):
            self.font.size = 'badvalue'
        with self.assertRaises(TecplotSystemError):
            self.font.size = -1
        with self.assertRaises(TecplotSystemError):
            self.font.size = 0

    def test_size_units(self):
        sz = self.font.size
        for val in [Units.Frame, Units.Point, Units.Frame]:
            self.font.size_units = val
            self.assertEqual(self.font.size_units, val)
            self.assertEqual(self.font.size, sz)
        with self.assertRaises(ValueError):
            self.font.size_units = 0.5
        self.assertEqual(self.font.size, sz)

    def test_typeface(self):
        for val in ['Times', 'Helvetica', 'Invalid Font Name']:
            self.font.typeface = val
            self.assertEqual(self.font.typeface, val)


class TestLineLegendFont(unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        self.filename, self.dataset = sample_data.sample_data('2x2x3_overlap')
        frame = tp.active_frame()
        frame.plot_type = PlotType.XYLine
        self.legend = frame.plot(PlotType.XYLine).legend

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    def test_bold(self):
        for val in [True, False, True]:
            self.legend.font.bold = val
            self.assertEqual(self.legend.font.bold, val)

    def test_italic(self):
        for val in [True, False, True]:
            self.legend.font.italic = val
            self.assertEqual(self.legend.font.italic, val)

    def test_size(self):
        for val in [1, 100]:
            self.legend.font.size = val
            self.assertEqual(self.legend.font.size, val)
        with self.assertRaises(ValueError):
            self.legend.font.size = 'badtype'
        with self.assertRaises(TecplotSystemError):
            self.legend.font.size = 0

    def test_size_units(self):
        for val in [Units.Point, Units.Frame, Units.Point]:
            self.legend.font.size_units = val
            self.assertEqual(self.legend.font.size_units, val)
        with self.assertRaises((TecplotValueError, TecplotSystemError)):
            self.legend.font.size_units = Units.Grid

    def test_typeface(self):
        for val in ['Arial']:
            self.legend.font.typeface = val
            self.assertEqual(self.legend.font.typeface, val)


class TestContourLegendFont(unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        self.filename, self.dataset = sample_data.sample_data('2x2x3_overlap')
        frame = tp.active_frame()

        plot = frame.plot(PlotType.Cartesian3D)
        plot.vector.u_variable_index = 0
        plot.vector.v_variable_index = 1
        plot.vector.w_variable_index = 2
        self.legend = plot.contour(0).legend

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    def test_bold(self):
        for val in [True, False, True]:
            self.legend.header_font.bold = val
            self.assertEqual(self.legend.header_font.bold, val)

            self.legend.number_font.bold = val
            self.assertEqual(self.legend.number_font.bold, val)

    def test_italic(self):
        for val in [True, False, True]:
            self.legend.header_font.italic = val
            self.assertEqual(self.legend.header_font.italic, val)
            self.legend.number_font.italic = val
            self.assertEqual(self.legend.number_font.italic, val)

    def test_size(self):
        for val in [1, 100]:
            self.legend.header_font.size = val
            self.assertEqual(self.legend.header_font.size, val)
            self.legend.number_font.size = val
            self.assertEqual(self.legend.number_font.size, val)
        with self.assertRaises(ValueError):
            self.legend.number_font.size = 'badtype'
        with self.assertRaises(TecplotSystemError):
            self.legend.number_font.size = 0

    def test_size_units(self):
        for val in [Units.Point, Units.Frame, Units.Point]:
            self.legend.header_font.size_units = val
            self.assertEqual(self.legend.header_font.size_units, val)
        with self.assertRaises((TecplotValueError, TecplotSystemError)):
            self.legend.header_font.size_units = Units.Grid

        for val in [Units.Point, Units.Frame, Units.Point]:
            self.legend.number_font.size_units = val
            self.assertEqual(self.legend.number_font.size_units, val)
        with self.assertRaises((TecplotValueError, TecplotSystemError)):
            self.legend.number_font.size_units = Units.Grid

    def test_typeface(self):
        for val in ['Arial']:
            self.legend.header_font.typeface = val
            self.assertEqual(self.legend.header_font.typeface, val)
            self.legend.number_font.typeface = val
            self.assertEqual(self.legend.number_font.typeface, val)


class TestBaseFont(object):
    def test_typeface(self):
        for val in ['Times', 'Helvetica']:
            self.font.typeface = val
            self.assertEqual(self.font.typeface, val)

    def test_bold(self):
        for val in [True, False, True]:
            self.font.bold = val
            self.assertEqual(self.font.bold, val)

    def test_italic(self):
        for val in [True, False, True]:
            self.font.italic = val
            self.assertEqual(self.font.italic, val)


class TestScatterBaseFont(TestBaseFont, unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        self.filename,dataset = sample_data.sample_data('10x10x10')
        plot = tp.active_frame().plot(PlotType.Cartesian3D)
        plot.activate()
        self.font = plot.scatter.base_font

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)


class TestLinePlotBaseFont(TestBaseFont, unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        self.filename,dataset = sample_data.sample_data('xylines_poly')
        frame = tp.active_frame()
        self.font = frame.plot(PlotType.XYLine).base_font

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)


if __name__ == '__main__':
    from .. import main
    main()
