import os
import unittest

import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *
from tecplot import text

from .. import sample_data


class TestDataLabels(object):
    def test_index_step(self):
        for val in [1, 2, 10]:
            self.labels.index_step = val
            self.assertEqual(self.labels.index_step, val)
        with self.assertRaises(TecplotSystemError):
            self.labels.index_step = -1
        with self.assertRaises(TecplotSystemError):
            self.labels.index_step = 0
        with self.assertRaises(ValueError):
            self.labels.index_step = 'badvalue'

    def test_show_node_labels(self):
        for val in [True, False, True]:
            self.labels.show_node_labels = val
            self.assertEqual(self.labels.show_node_labels, val)

    def test_node_label_type(self):
        for val in [LabelType.VarValue, LabelType.Index, LabelType.VarValue]:
            self.labels.node_label_type = val
            self.assertEqual(self.labels.node_label_type, val)
        with self.assertRaises(ValueError):
            self.labels.node_label_type = 0.5
        with self.assertRaises(ValueError):
            self.labels.node_label_type = 'badvalue'

    def test_color_by_map(self):
        for val in [True, False, True]:
            self.labels.color_by_map = val
            self.assertEqual(self.labels.color_by_map, val)

    def test_color(self):
        for val in [Color.Red, Color.Blue]:
            self.labels.color = val
            self.assertEqual(self.labels.color, val)
        with self.assertRaises(ValueError):
            self.labels.color = 0.5
        with self.assertRaises(ValueError):
            self.labels.color = 'badvalue'

    def test_show_box(self):
        for val in [True, False, True]:
            self.labels.show_box = val
            self.assertEqual(self.labels.show_box, val)

    def test_font(self):
        self.assertIsInstance(self.labels.font, text.Font)

    def test_label_format(self):
        self.assertIsInstance(self.labels.label_format, text.LabelFormat)


class TestDataLabelsFieldPlot(TestDataLabels, unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        self.filename, self.dataset = sample_data.sample_data('10x10x10')
        frame = tp.active_frame()
        frame.plot_type = PlotType.Cartesian3D
        self.labels = frame.plot().data_labels

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    def test_cell_label_type(self):
        for val in [LabelType.VarValue, LabelType.Index, LabelType.VarValue]:
            self.labels.cell_label_type = val
            self.assertEqual(self.labels.cell_label_type, val)
        with self.assertRaises(ValueError):
            self.labels.cell_label_type = 0.5
        with self.assertRaises(ValueError):
            self.labels.cell_label_type = 'badvalue'

    def test_show_cell_labels(self):
        for val in [True, False, True]:
            self.labels.show_cell_labels = val
            self.assertEqual(self.labels.show_cell_labels, val)

    def test_cell_variable_index(self):
        for v in self.dataset.variables():
            self.labels.cell_variable_index = v.index
            self.assertEqual(self.labels.cell_variable_index, v.index)
            self.assertEqual(self.labels.cell_variable, v)

    def test_cell_variable(self):
        for v in self.dataset.variables():
            self.labels.cell_variable = v
            self.assertEqual(self.labels.cell_variable_index, v.index)
            self.assertEqual(self.labels.cell_variable, v)

    def test_node_variable_index(self):
        for v in self.dataset.variables():
            self.labels.node_variable_index = v.index
            self.assertEqual(self.labels.node_variable_index, v.index)
            self.assertEqual(self.labels.node_variable, v)

    def test_node_variable(self):
        for v in self.dataset.variables():
            self.labels.node_variable = v
            self.assertEqual(self.labels.node_variable_index, v.index)
            self.assertEqual(self.labels.node_variable, v)


class TestDataLabelsLinePlot(TestDataLabels, unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        self.filename, self.dataset = sample_data.sample_data('xylines_poly')
        frame = tp.active_frame()
        frame.plot_type = PlotType.XYLine
        self.labels = frame.plot().data_labels

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    def test_step_mode(self):
        for val in StepMode:
            self.labels.step_mode = val
            self.assertEqual(self.labels.step_mode, val)
        with self.assertRaises(ValueError):
            self.labels.step_mode = 0.5
        with self.assertRaises(ValueError):
            self.labels.step_mode = 'badvalue'

    def test_step_distance(self):
        for val in [0, 1, 3.14, 10]:
            self.labels.step_distance = val
            self.assertAlmostEqual(self.labels.step_distance, val)
        with self.assertRaises(TecplotSystemError):
            self.labels.step_distance = -1
        with self.assertRaises(ValueError):
            self.labels.step_distance = 'badvalue'


if __name__ == '__main__':
    from .. import main
    main()
