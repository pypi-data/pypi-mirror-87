import unittest

import tecplot as tp
from tecplot.constant import *
from tecplot.exception import *


class TestLegend(object):
    def test_box(self):
        self.assertIsInstance(self.legend.box, tp.text.TextBox)

    def test_show(self):
        for val in [True, False, True]:
            self.legend.show = val
            self.assertEqual(self.legend.show, val)

    def test_anchor_alignment(self):
        for val in AnchorAlignment:
            self.legend.anchor_alignment = val
            self.assertEqual(self.legend.anchor_alignment, val)
        with self.assertRaises(ValueError):
            self.legend.anchor_alignment = 0.5
        with self.assertRaises(ValueError):
            self.legend.anchor_alignment = 'badvalue'

    def test_text_color(self):
        for val in [Color.Red, Color.Blue]:
            self.legend.text_color = val
            self.assertEqual(self.legend.text_color, val)
        with self.assertRaises(ValueError):
            self.legend.text_color = 0.5
        with self.assertRaises(ValueError):
            self.legend.text_color = 'badvalue'

    def test_position(self):
        for pos in [(0,0), (20,20), (30,30)]:
            self.legend.position = pos
            self.assertAlmostEqual(self.legend.position[0], pos[0])
            self.assertAlmostEqual(self.legend.position[1], pos[1])
        with self.assertRaises(TypeError):
            self.legend.position = 4
        with self.assertRaises(ValueError):
            self.legend.position = 'badvalue'


class TestTabularLegend(TestLegend):
    def test_row_spacing(self):
        for val in [0.5, 1, 2]:
            self.legend.row_spacing = val
            self.assertAlmostEqual(self.legend.row_spacing, val)
        with self.assertRaises((TecplotSystemError, TecplotLogicError)):
            self.legend.row_spacing = -1
        with self.assertRaises((TecplotSystemError, TecplotLogicError)):
            self.legend.row_spacing = 0
        with self.assertRaises(ValueError):
            self.legend.row_spacing = 'badvalue'


class TestCategoryLegend(TestTabularLegend):
    def test_show_text(self):
        for val in [True, False, True]:
            self.legend.show_text = val
            self.assertEqual(self.legend.show_text, val)

    def test_font(self):
        self.assertIsInstance(self.legend.font, tp.text.Font)
