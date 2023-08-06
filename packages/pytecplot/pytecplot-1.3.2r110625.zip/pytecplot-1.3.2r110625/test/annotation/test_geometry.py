import unittest

import tecplot as tp
from tecplot import annotation
from tecplot.constant import *
from tecplot.exception import *

from .test_annotation import TestFrameAnnotation, TestMovableAnnotation


class TestGeometry(TestFrameAnnotation):
    def test_eq(self):
        self.assertEqual(self.anno, next(self.anno.frame.geometries()))

    def test_ne(self):
        geom = self.anno.frame.add_circle((0,0), 1, CoordSys.Frame)
        self.assertNotEqual(self.anno, geom)

    def test_color(self):
        for val in [Color.Red, Color.Blue]:
            self.geom.color = val
            self.assertEqual(self.geom.color, val)
        with self.assertRaises(ValueError):
            self.geom.color = "badtype"

    def test_fill_color(self):
        for val in [Color.Red, None, Color.Blue]:
            self.geom.fill_color = val
            self.assertEqual(self.geom.fill_color, val)
        with self.assertRaises(ValueError):
            self.geom.fill_color = "badtype"

    def test_line_pattern(self):
        for val in LinePattern:
            self.geom.line_pattern = val
            self.assertEqual(self.geom.line_pattern, val)
        with self.assertRaises(ValueError):
            self.geom.line_pattern = 0.5
        with self.assertRaises(ValueError):
            self.geom.line_pattern = 'badvalue'

    def test_line_thickness(self):
        self.geom.line_thickness = 0
        self.assertAlmostEqual(self.geom.line_thickness, 0.0001)
        for val in [0.5, 1, 2]:
            self.geom.line_thickness = val
            self.assertAlmostEqual(self.geom.line_thickness, val)
        with self.assertRaises(ValueError):
            self.geom.line_thickness = "badtype"
        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            self.geom.line_thickness = -1

    def test_pattern_length(self):
        self.geom.pattern_length = 0
        self.assertAlmostEqual(self.geom.pattern_length, 0.01)
        for val in [0.5, 1, 2]:
            self.geom.pattern_length = val
            self.assertAlmostEqual(self.geom.pattern_length, val)
        with self.assertRaises(ValueError):
            self.geom.pattern_length = "badtype"
        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            self.geom.pattern_length = -1


class TestGeometry2D(TestGeometry, TestMovableAnnotation):
    def test_clipping(self):
        for c in Clipping:
            self.geom.clipping = c
            self.assertEqual(self.geom.clipping, c)
        with self.assertRaises(ValueError):
            self.geom.clipping = 0.5
        with self.assertRaises(ValueError):
            self.geom.clipping = 'badvalue'


class TestCurvedGeometry(TestGeometry2D):
    def test_num_points(self):
        for val in [3, 5, 50]:
            self.geom.num_points = val
            self.assertAlmostEqual(self.geom.num_points, val)
        with self.assertRaises(ValueError):
            self.geom.num_points = "badtype"
        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            self.geom.num_points = 0
        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            self.geom.num_points = 2


class TestCircle(TestCurvedGeometry, unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        fr = tp.active_frame()
        x, y = (0.5, 0.6)
        r = 0.1
        self.geom = fr.add_circle((x, y), r, CoordSys.Frame)
        self.assertAlmostEqual(self.geom.position.x, x)
        self.assertAlmostEqual(self.geom.position.y, y)
        self.assertAlmostEqual(self.geom.radius, r)
        self.anno = self.geom

    def test_type(self):
        self.assertEqual(self.anno.type, GeomType.Circle)

    def test_radius(self):
        for val in [-1, 0.5, 1, 2]:
            self.geom.radius = val
            self.assertAlmostEqual(self.geom.radius, val)
        with self.assertRaises(ValueError):
            self.geom.radius = "badtype"
        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            self.geom.radius = 0


class TestEllipse(TestCurvedGeometry, unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        fr = tp.active_frame()
        x, y = (0.5, 0.6)
        h, v = (0.1, 0.2)
        self.geom = fr.add_ellipse((x, y), (h, v), CoordSys.Frame)
        self.assertAlmostEqual(self.geom.position.x, x)
        self.assertAlmostEqual(self.geom.position.y, y)
        self.assertAlmostEqual(self.geom.size[0], h)
        self.assertAlmostEqual(self.geom.size[1], v)
        self.anno = self.geom

    def test_type(self):
        self.assertEqual(self.anno.type, GeomType.Ellipse)

    def test_size(self):
        for val in [(1, 2), (0.1, 0.3)]:
            self.geom.size = val
            h, v = self.geom.size
            self.assertAlmostEqual(h, val[0])
            self.assertAlmostEqual(v, val[1])
        with self.assertRaises(ValueError):
            self.geom.size = "badtype"
        with self.assertRaises(TypeError):
            self.geom.size = 0
        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            self.geom.size = 0, 0


class TestRectangle(TestGeometry2D, unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        fr = tp.active_frame()
        x, y = (0.5, 0.6)
        w, h = (0.1, 0.2)
        self.geom = fr.add_rectangle((x, y), (w, h), CoordSys.Frame)
        self.assertAlmostEqual(self.geom.position.x, x)
        self.assertAlmostEqual(self.geom.position.y, y)
        self.assertAlmostEqual(self.geom.size[0], w)
        self.assertAlmostEqual(self.geom.size[1], h)
        self.anno = self.geom

    def test_type(self):
        self.assertEqual(self.anno.type, GeomType.Rectangle)

    def test_size(self):
        for val in [(1, 2), (0.1, 0.3)]:
            self.geom.size = val
            h, v = self.geom.size
            self.assertAlmostEqual(h, val[0])
            self.assertAlmostEqual(v, val[1])
        with self.assertRaises(ValueError):
            self.geom.size = "badtype"
        with self.assertRaises(TypeError):
            self.geom.size = 0
        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            self.geom.size = 0, 0


class TestSquare(TestGeometry2D, unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        fr = tp.active_frame()
        x, y = (0.5, 0.6)
        l = 0.1
        self.geom = fr.add_square((x, y), l, CoordSys.Frame)
        self.assertAlmostEqual(self.geom.position.x, x)
        self.assertAlmostEqual(self.geom.position.y, y)
        self.assertAlmostEqual(self.geom.size, l)
        self.anno = self.geom

    def test_type(self):
        self.assertEqual(self.anno.type, GeomType.Square)

    def test_size(self):
        for val in [-1, 0.5, 1, 2]:
            self.geom.size = val
            self.assertAlmostEqual(self.geom.size, val)
        with self.assertRaises(ValueError):
            self.geom.size = "badtype"
        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            self.geom.size = 0


if __name__ == '__main__':
    from .. import main
    main()
