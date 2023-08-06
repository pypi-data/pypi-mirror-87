import os
import unittest

import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *

from .. import sample_data



class TestPieChartsWedge(unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        self.filename, self.dataset = sample_data.sample_data('10x10x10')
        frame = tp.active_frame()
        frame.plot_type = PlotType.Cartesian3D
        frame.plot().fieldmap(0).scatter.symbol().shape = GeomShape.PieChart
        self.wedge = frame.plot().scatter.pie_charts.wedge(0)
        self.wedge.variable = self.dataset.variable(0)

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    def test_show(self):
        for val in [True, False, True]:
            self.wedge.show = val
            self.assertEqual(self.wedge.show, val)

    def test_show_label(self):
        for val in [True, False, True]:
            self.wedge.show_label = val
            self.assertEqual(self.wedge.show_label, val)

    def test_label_text(self):
        for val in ['aa', '0', 0, 3.14, None]:
            self.wedge.label_text = val
            self.assertEqual(self.wedge.label_text, str(val))

    def test_color(self):
        for val in [Color.Red, Color.Blue]:
            self.wedge.color = val
            self.assertEqual(self.wedge.color, val)
        with self.assertRaises(ValueError):
            self.wedge.color = 0.5
        with self.assertRaises(ValueError):
            self.wedge.color = 'badvalue'

    def test_variable(self):
        for v in self.dataset.variables():
            self.wedge.variable = v
            self.assertEqual(self.wedge.variable, v)
            self.assertEqual(self.wedge.variable_index, v.index)

    def test_variable_index(self):
        for v in self.dataset.variables():
            self.wedge.variable_index = v.index
            self.assertEqual(self.wedge.variable, v)
            self.assertEqual(self.wedge.variable_index, v.index)


class TestPieCharts(unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        self.filename, dataset = sample_data.sample_data('10x10x10')
        frame = tp.active_frame()
        frame.plot_type = PlotType.Cartesian3D
        self.piecharts = frame.plot().scatter.pie_charts

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    def test_label_offset(self):
        for val in [0, 0.5, 1, 100]:
            self.piecharts.label_offset = val
            self.assertAlmostEqual(self.piecharts.label_offset, val)
        with self.assertRaises(TecplotSystemError):
            self.piecharts.label_offset = -1
        with self.assertRaises(ValueError):
            self.piecharts.label_offset = 'badvalue'

    def test_label_text(self):
        for val in ['aa', '0', 0, 3.14, None]:
            self.piecharts.label_text = val
            self.assertEqual(self.piecharts.label_text, str(val))

    def test_label_color(self):
        for val in [Color.Red, Color.Blue]:
            self.piecharts.label_color = val
            self.assertEqual(self.piecharts.label_color, val)
        with self.assertRaises(ValueError):
            self.piecharts.label_color = 0.5
        with self.assertRaises(ValueError):
            self.piecharts.label_color = 'badvalue'

    def test_label_font(self):
        self.assertIsInstance(self.piecharts.label_font, tp.text.Font)

    def test_show_zero_value_wedge_labels(self):
        for val in [True, False, True]:
            self.piecharts.show_zero_value_wedge_labels = val
            self.assertEqual(self.piecharts.show_zero_value_wedge_labels, val)

    def test_start_angle(self):
        for val in [0, 0.5, 1, 100]:
            self.piecharts.start_angle = val
            self.assertAlmostEqual(self.piecharts.start_angle, val)
        with self.assertRaises(TecplotSystemError):
            self.piecharts.start_angle = -1
        with self.assertRaises(ValueError):
            self.piecharts.start_angle = 'badvalue'

    def test_wedge(self):
        self.assertIsInstance(self.piecharts.wedge(0), tp.plot.PieChartsWedge)
        self.assertIsInstance(self.piecharts.wedge(1), tp.plot.PieChartsWedge)


class TestScatter(unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        self.filename,self.dataset = sample_data.sample_data('10x10x10')
        frame = tp.active_frame()
        frame.plot_type = PlotType.Cartesian3D
        self.scatter = frame.plot().scatter

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    def test_base_font(self):
        self.assertIsInstance(self.scatter.base_font, tp.text.BaseFont)

    def test_legend(self):
        self.assertIsInstance(self.scatter.legend, tp.legend.ScatterLegend)

    def test_pie_charts(self):
        self.assertIsInstance(self.scatter.pie_charts, tp.plot.PieCharts)

    def test_reference_symbol(self):
        self.assertIsInstance(self.scatter.reference_symbol,
                              tp.plot.ScatterReferenceSymbol)

    def test_relative_size(self):
        for val in [0, 0.5, 1, 100]:
            self.scatter.relative_size = val
            self.assertAlmostEqual(self.scatter.relative_size, val)
        with self.assertRaises(TecplotSystemError):
            self.scatter.relative_size = -1
        with self.assertRaises(ValueError):
            self.scatter.relative_size = 'badvalue'

    def test_relative_size_units(self):
        for val in [RelativeSizeUnits.Grid, RelativeSizeUnits.Page,
                    RelativeSizeUnits.Grid]:
            self.scatter.relative_size_units = val
            self.assertEqual(self.scatter.relative_size_units, val)
        with self.assertRaises(ValueError):
            self.scatter.relative_size_units = 'badvalue'

    def test_sphere_render_quality(self):
        for val in SphereScatterRenderQuality:
            self.scatter.sphere_render_quality = val
            self.assertEqual(self.scatter.sphere_render_quality, val)
        with self.assertRaises(ValueError):
            self.scatter.sphere_render_quality = 0.5
        with self.assertRaises(ValueError):
            self.scatter.sphere_render_quality = 'badvalue'

    def test_variable(self):
        for v in self.dataset.variables():
            self.scatter.variable = v
            self.assertEqual(self.scatter.variable, v)
            self.assertEqual(self.scatter.variable_index, v.index)

    def test_variable_index(self):
        for v in self.dataset.variables():
            self.scatter.variable_index = v.index
            self.assertEqual(self.scatter.variable, v)
            self.assertEqual(self.scatter.variable_index, v.index)


if __name__ == '__main__':
    from .. import main
    main()
