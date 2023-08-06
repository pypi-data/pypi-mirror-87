import os
import unittest

import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *

from ..sample_data import sample_data


class TestTextSymbol(unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        self.filename,dataset = sample_data('xylines_poly')
        frame = tp.active_frame()
        frame.plot_type = PlotType.XYLine
        plot = frame.plot()
        zone = dataset.zone(0)
        x = dataset.variable('X')
        plot.add_linemap('p', zone, x, dataset.variable('P'))
        sym = frame.plot().linemap(0).symbols
        sym.symbol_type = SymbolType.Text
        self.symbol = sym.symbol()

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    def test_text(self):
        for c in ['a','1',1,0,True,False,'abc']:
            self.symbol.text = c
            self.assertEqual(self.symbol.text, str(c)[0])
        with self.assertRaises(IndexError):
            self.symbol.text = ''

    def test_typeface(self):
        for val in [True, False, True]:
            self.symbol.use_base_font = val
            self.assertEqual(self.symbol.use_base_font, val)

        for c in [tp.constant.Font.Greek, tp.constant.Font.Math,
                  tp.constant.Font.UserDefined]:
            self.symbol.font_override = c
            self.assertEqual(self.symbol.font_override, c)
        if __debug__:
            with self.assertRaises(TecplotLogicError):
                self.symbol.font_override = 0.5
            with self.assertRaises(TecplotLogicError):
                self.symbol.font_override = tp.constant.Font.Helvetica
        else:
            with self.assertRaises(ValueError):
                self.symbol.font_override = 0.5


class TestGeometrySymbol(unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        self.filename,dataset = sample_data('xylines_poly')
        frame = tp.active_frame()
        frame.plot_type = PlotType.XYLine
        plot = frame.plot()
        zone = dataset.zone(0)
        x = dataset.variable('X')
        plot.add_linemap('p', zone, x, dataset.variable('P'))
        sym = frame.plot().linemap(0).symbols
        sym.symbol_type = SymbolType.Geometry
        self.symbol = sym.symbol()

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    def test_shape(self):
        for c in [GeomShape.Circle, GeomShape.Square]:
            self.symbol.shape = c
            self.assertEqual(self.symbol.shape, c)
        with self.assertRaises(ValueError):
            self.symbol.shape = 0.5


class TestTextScatterSymbol(unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        self.filename,dataset = sample_data('10x10x10')
        frame = tp.active_frame()
        frame.plot_type = PlotType.Cartesian3D
        self.plot = frame.plot()
        fmap = self.plot.fieldmap(0)
        fmap.scatter.symbol_type = SymbolType.Text
        self.symbol = fmap.scatter.symbol()

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    def test_text(self):
        for c in ['a','1',1,0,True,False,'abc']:
            self.symbol.text = c
            self.assertEqual(self.symbol.text, str(c)[0])
        with self.assertRaises(IndexError):
            self.symbol.text = ''

    def test_typeface(self):
        for val in [True, False, True]:
            self.symbol.use_base_font = val
            self.assertEqual(self.symbol.use_base_font, val)

        for c in [tp.constant.Font.Greek, tp.constant.Font.Math,
                  tp.constant.Font.UserDefined]:
            self.symbol.font_override = c
            self.assertEqual(self.symbol.font_override, c)
        if __debug__:
            with self.assertRaises(TecplotLogicError):
                self.symbol.font_override = 0.5
            with self.assertRaises(TecplotLogicError):
                self.symbol.font_override = tp.constant.Font.Helvetica
        else:
            with self.assertRaises(ValueError):
                self.symbol.font_override = 0.5


class TestGeometryScatterSymbol(unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        self.filename,dataset = sample_data('10x10x10')
        frame = tp.active_frame()
        frame.plot_type = PlotType.Cartesian3D
        self.plot = frame.plot()
        fmap = self.plot.fieldmap(0)
        fmap.scatter.symbol_type = SymbolType.Geometry
        self.symbol = fmap.scatter.symbol()

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    def test_shape(self):
        for c in [GeomShape.Circle, GeomShape.Square]:
            self.symbol.shape = c
            self.assertEqual(self.symbol.shape, c)
        with self.assertRaises(ValueError):
            self.symbol.shape = 0.5
        with self.assertRaises(ValueError):
            self.symbol.shape = 'badvalue'


class TestScatterReferenceSymbol(unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        self.filename,dataset = sample_data('10x10x10')
        frame = tp.active_frame()
        frame.plot_type = PlotType.Cartesian3D
        self.plot = frame.plot()
        self.symbol = self.plot.scatter.reference_symbol

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    def test_show(self):
        for val in [True, False, True]:
            self.symbol.show = val
            self.assertEqual(self.symbol.show, val)

    def test_color(self):
        for val in [Color.Red, Color.Blue]:
            self.symbol.color = val
            self.assertEqual(self.symbol.color, val)
        with self.assertRaises(ValueError):
            self.symbol.color = 0.5
        with self.assertRaises(ValueError):
            self.symbol.color = 'badvalue'

    def test_filled(self):
        for val in [True, False, True]:
            self.symbol.filled = val
            self.assertEqual(self.symbol.filled, val)

    def test_fill_color(self):
        for val in [Color.Red, Color.Blue]:
            self.symbol.fill_color = val
            self.assertEqual(self.symbol.fill_color, val)
        with self.assertRaises(ValueError):
            self.symbol.fill_color = 0.5
        with self.assertRaises(ValueError):
            self.symbol.fill_color = 'badvalue'

    def test_position(self):
        for val in [(0,0), (10,10)]:
            self.symbol.position = val
            self.assertAlmostEqual(self.symbol.position.x, val[0])
            self.assertAlmostEqual(self.symbol.position.y, val[1])
        with self.assertRaises(TypeError):
            self.symbol.position = 3.14
        with self.assertRaises(ValueError):
            self.symbol.position = 'badvalue'

    def test_magnitude(self):
        for val in [0.5, 1, 10.]:
            self.symbol.magnitude = val
            self.assertAlmostEqual(self.symbol.magnitude, val)
        with self.assertRaises(ValueError):
            self.symbol.magnitude = 'badvalue'
        with self.assertRaises(TecplotSystemError):
            self.symbol.magnitude = -1
        with self.assertRaises(TecplotSystemError):
            self.symbol.magnitude = 0

    def test_line_thickness(self):
        for val in [0.5, 1, 10.]:
            self.symbol.line_thickness = val
            self.assertAlmostEqual(self.symbol.line_thickness, val)
        with self.assertRaises(ValueError):
            self.symbol.line_thickness = 'badvalue'
        with self.assertRaises(TecplotSystemError):
            self.symbol.line_thickness = -1
        with self.assertRaises(TecplotSystemError):
            self.symbol.line_thickness = 0

    def test_symbol_type(self):
        for val in [SymbolType.Text, SymbolType.Geometry, SymbolType.Text]:
            self.symbol.symbol_type = val
            self.assertEqual(self.symbol.symbol_type, val)
        with self.assertRaises(ValueError):
            self.symbol.symbol_type = 0.5
        with self.assertRaises(ValueError):
            self.symbol.symbol_type = 'badvalue'

    def test_symbol(self):
        self.symbol.symbol_type = SymbolType.Text
        self.assertIsInstance(self.symbol.symbol(), tp.plot.symbol.TextSymbol)
        self.assertIsInstance(self.symbol.symbol(SymbolType.Geometry),
                              tp.plot.symbol.GeometrySymbol)
        self.symbol.symbol_type = SymbolType.Geometry
        self.assertIsInstance(self.symbol.symbol(), tp.plot.symbol.GeometrySymbol)
        self.assertIsInstance(self.symbol.symbol(SymbolType.Text),
                              tp.plot.symbol.TextSymbol)


if __name__ == '__main__':
    from .. import main
    main()
