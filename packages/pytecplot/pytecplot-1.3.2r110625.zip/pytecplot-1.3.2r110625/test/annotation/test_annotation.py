from tecplot.constant import *
from tecplot.exception import *

from test import patch_tecutil


class TestAnnotation(object):
    def test_scope(self):
        for s in Scope:
            self.anno.scope = s
            self.assertEqual(self.anno.scope, s)
        with self.assertRaises(ValueError):
            self.anno.scope = 'badvalue'

    def test_eq(self):
        assert False  # derived class must implement this test

    def test_ne(self):
        assert False  # derived class must implement this test

    def test_type(self):
        assert False  # derived class must implement this test


class TestFrameAnnotation(TestAnnotation):
    def test_macro_function(self):
        self.anno.macro_function = 'testing testing'
        self.assertEqual(self.anno.macro_function, 'testing testing')

        with patch_tecutil('GeomSetMacroFunctionCmd', return_value=False):
            with self.assertRaises(TecplotSystemError):
                self.anno.macro_function = 'test'

        with patch_tecutil('GeomGetMacroFunctionCmd', return_value=(False, None)):
            with self.assertRaises(TecplotSystemError):
                _ = self.anno.macro_function

    def test_attached_map_index(self):
        self.anno.attached_map_index = None
        self.assertIsNone(self.anno.attached_map_index)
        for i in [0, 1]:
            self.anno.attached_map_index = i
            self.assertEqual(self.anno.attached_map_index, i)
        self.anno.attached_map_index = None
        self.assertIsNone(self.anno.attached_map_index)
        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            self.anno.attached_map_index = -1


class TestMovableAnnotation(TestFrameAnnotation):
    def test_draw_order(self):
        for c in DrawOrder:
            self.anno.draw_order = c
            self.assertEqual(self.anno.draw_order, c)
        with self.assertRaises(ValueError):
            self.anno.draw_order = 0.5
        with self.assertRaises(ValueError):
            self.anno.draw_order = 'badvalue'

    def test_position(self):
        for p in [(1,2), (0,0)]:
            self.anno.position = p
            pos = self.anno.position
            self.assertAlmostEqual(p[0], pos.x)
            self.assertAlmostEqual(p[1], pos.y)

    def test_position_coordinate_system(self):
        for cs in [CoordSys.Grid, CoordSys.Frame, CoordSys.Grid]:
            self.anno.position_coordinate_system = cs
            self.assertEqual(self.anno.position_coordinate_system, cs)
        with self.assertRaises(ValueError):
            self.anno.position_coordinate_system = 'badvalue'
