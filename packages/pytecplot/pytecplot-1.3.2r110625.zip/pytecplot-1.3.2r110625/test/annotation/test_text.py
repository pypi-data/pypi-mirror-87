from __future__ import unicode_literals

import os, unittest, warnings

import tecplot as tp
from tecplot import annotation, tecutil
from tecplot.constant import *
from tecplot.exception import *

from test import sample_data, patch_tecutil, skip_if_sdk_version_before


class TestTextFont(unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        self.filename, ds = sample_data.sample_data('3x3x3_p')
        self.font = tp.active_frame().add_text('test').font

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    def test_bold(self):
        for val in [True, False, True]:
            self.font.bold = val
            self.assertEqual(self.font.bold, val)

    def test_italic(self):
        for val in [True, False, True]:
            self.font.italic = val
            self.assertEqual(self.font.italic, val)

    def test_size(self):
        self.font.size_units = Units.Frame
        for val in [0, 1, 10, 100, 150]:
            self.font.size = val
            self.assertAlmostEqual(self.font.size, val)
        with self.assertRaises(ValueError):
            self.font.size = 'badvalue'
        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            self.font.size = -1

        self.font.size_units = Units.Point
        self.font.size = 0
        if tp.sdk_version_info < (2018, 2):
            self.assertAlmostEqual(self.font.size, 0.5)
        else:
            self.assertAlmostEqual(self.font.size, 0)
        for val in [1, 10, 100, 150]:
            self.font.size = val
            self.assertAlmostEqual(self.font.size, val)
        with self.assertRaises(ValueError):
            self.font.size = 'badvalue'
        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            self.font.size = -1

    @skip_if_sdk_version_before(2018, 3)
    def test_size_units(self):
        tp.active_frame().plot_type = PlotType.Cartesian3D
        sz = self.font.size
        for val in [Units.Frame, Units.Point, Units.Grid]:
            self.font.size_units = val
            self.assertEqual(self.font.size_units, val)
            self.assertAlmostEqual(self.font.size, sz)
        with self.assertRaises(ValueError):
            self.font.size_units = 0.5
        with self.assertRaises(ValueError):
            self.font.size_units = 'badvalue'
        self.assertAlmostEqual(self.font.size, sz)

    def test_typeface(self):
        for val in ['Times', 'Helvetica', 'Invalid Font Name']:
            self.font.typeface = val
            self.assertEqual(self.font.typeface, val)


class TestTextBox(unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        self.box = tp.active_frame().add_text('test').box

    def test_type(self):
        for val in TextBox:
            self.box.type = val
            self.assertEqual(self.box.type, val)
        with self.assertRaises(ValueError):
            self.box.type = "badtype"

    def test_color(self):
        for val in [Color.Red, Color.Blue]:
            self.box.color = val
            self.assertEqual(self.box.color, val)
        with self.assertRaises(ValueError):
            self.box.color = "badtype"

    def test_fill_color(self):
        for val in [Color.Magenta, Color.Cyan]:
            self.box.fill_color = val
            self.assertEqual(self.box.fill_color, val)
        with self.assertRaises(ValueError):
            self.box.fill_color = "badtype"

    def test_line_thickness(self):
        self.box.line_thickness = 0
        self.assertAlmostEqual(self.box.line_thickness, 0.0001)
        for val in [0.5, 1, 2]:
            self.box.line_thickness = val
            self.assertAlmostEqual(self.box.line_thickness, val)
        with self.assertRaises(ValueError):
            self.box.line_thickness = "badtype"
        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            self.box.line_thickness = -1

    def test_margin(self):
        for val in [0,0.5,1,2]:
            self.box.margin = val
            self.assertEqual(self.box.margin, val)
        with self.assertRaises(ValueError):
            self.box.margin = "badtype"
        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            self.box.margin = -1

    def test_corner_locations(self):
        pos = self.box.corner_locations
        self.assertIsInstance(pos.x1, float)
        self.assertIsInstance(pos.y1, float)
        self.assertIsInstance(pos.x2, float)
        self.assertIsInstance(pos.y2, float)
        self.assertIsInstance(pos.x3, float)
        self.assertIsInstance(pos.y3, float)
        self.assertIsInstance(pos.x4, float)
        self.assertIsInstance(pos.y4, float)

    @skip_if_sdk_version_before(2018, 2)
    def test_deprecated(self):
        with self.assertRaises(TecplotInterfaceChangeError):
            _ = self.box.position


class TestText(unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        self.filename, ds = sample_data.sample_data('3x3x3_p')
        self.text = tp.active_frame().add_text('test')
        self.text3d = tp.active_frame().add_text('test', coord_sys=CoordSys.Grid3D)
        self.text_other = tp.active_frame().add_text('other')

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    def test_str(self):
        self.assertEqual(str(self.text), 'test')

    def test_eq(self):
        self.assertEqual(self.text, next(tp.active_frame().texts()))

    def test_ne(self):
        texts = tp.active_frame().texts()
        next(texts)
        other = next(texts)
        self.assertNotEqual(self.text, other)

    @skip_if_sdk_version_before(2017, 3)
    def test_type(self):
        for val in [TextType.Regular, TextType.LaTeX, TextType.Regular]:
            self.text.type = val
            self.assertEqual(self.text.type, val)
        with self.assertRaises(ValueError):
            self.text.type = 'badvalue'

    def test_box(self):
        self.assertIsInstance(self.text.box, annotation.text.TextBox)

    def test_font(self):
        self.assertIsInstance(self.text.font, annotation.text.TextFont)

    @skip_if_sdk_version_before(2018, 3)
    def test_anchor(self):
        for a in (TextAnchor.MidRight, TextAnchor.HeadLeft, TextAnchor.HeadCenter):
            self.text.anchor = a
            self.assertEqual(self.text.anchor, a)
        with self.assertRaises((TecplotSystemError, TecplotLogicError)):
            self.text.anchor = TextAnchor.OnSide

    def test_angle(self):
        for a in [-30, 0, 90, 0]:
            self.text.angle = a
            self.assertAlmostEqual(self.text.angle, a)
        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            self.text.angle = -400
        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            self.text.angle = 400
        with self.assertRaises(ValueError):
            self.text.angle = 'badvalue'

    @skip_if_sdk_version_before(2018, 3)
    def test_position_coordinate_system(self):
        tp.active_frame().plot_type = PlotType.Cartesian3D
        for cs in [CoordSys.Grid, CoordSys.Frame]:
            self.text.position_coordinate_system = cs
            self.assertEqual(self.text.position_coordinate_system, cs)

        tp.active_frame().plot_type = PlotType.Sketch
        with self.assertRaises((TecplotSystemError, TecplotLogicError)):
            self.text.position_coordinate_system = CoordSys.Grid3D
        with self.assertRaises((TecplotSystemError, TecplotLogicError)):
            self.text3d.position_coordinate_system = CoordSys.Grid

        tp.active_frame().plot_type = PlotType.Cartesian3D

        with self.assertRaises(ValueError):
            self.text.position_coordinate_system = 'badvalue'

        self.text.position_coordinate_system = CoordSys.Grid
        self.text.font.size_units = Units.Grid
        self.assertEqual(self.text.font.size_units, Units.Grid)
        self.assertEqual(self.text.position_coordinate_system, CoordSys.Grid)

        self.text.position_coordinate_system = CoordSys.Frame
        self.assertEqual(self.text.font.size_units, Units.Frame)
        self.assertEqual(self.text.position_coordinate_system, CoordSys.Frame)

    def test_line_spacing(self):
        for val in [0, 0.5, 1, 2]:
            self.text.line_spacing = val
            self.assertEqual(self.text.line_spacing, val)
        with self.assertRaises(ValueError):
            self.text.line_spacing = "badtype"
        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            self.text.line_spacing = -1

    def test_text_string(self):
        self.assertEqual(self.text.text_string, 'test')
        self.text.text_string = 'blah'
        self.assertEqual(self.text.text_string, 'blah')
        self.text.text_string = 'test'
        self.assertEqual(self.text.text_string, 'test')

        with patch_tecutil('TextGetString', return_value=(False, None)):
            with self.assertRaises(TecplotSystemError):
                _ = self.text.text_string

    @skip_if_sdk_version_before(2018, 3)
    def test_position(self):
        tp.active_frame().plot_type = PlotType.Cartesian3D
        self.text3d.position = 1, 2, 3
        self.assertEqual(self.text3d.position, tecutil.XYZ(1, 2, 3))

        self.text.position_coordinate_system = CoordSys.Grid
        self.text.position = 1, 2
        self.assertEqual(self.text.position, tecutil.XY(1, 2))

    def test_scope(self):
        for s in Scope:
            self.text.scope = s
            self.assertEqual(self.text.scope, s)
        with self.assertRaises(ValueError):
            self.text.scope = "badtype"

    def test_attached_map_index(self):
        self.text.attached_map_index = None
        self.assertIsNone(self.text.attached_map_index)
        for i in [0, 1]:
            self.text.attached_map_index = i
            self.assertEqual(self.text.attached_map_index, i)
        self.text.attached_map_index = None
        self.assertIsNone(self.text.attached_map_index)
        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            self.text.attached_map_index = -1

    def test_color(self):
        for val in [Color.Blue, Color.Red, Color.Black]:
            self.text.color = val
            self.assertEqual(self.text.color, val)
        with self.assertRaises(ValueError):
            self.text.color = 'badvalue'
        with self.assertRaises(ValueError):
            self.text.color = 0.5

    def test_clipping(self):
        for c in Clipping:
            self.text.clipping = c
            self.assertEqual(self.text.clipping, c)
        with self.assertRaises(ValueError):
            self.text.clipping = 'badvalue'

    @skip_if_sdk_version_before(2018, 2)
    def test_deprecated(self):
        with self.assertRaises(TecplotInterfaceChangeError):
            _ = self.text.text_box

        with self.assertRaises(TecplotInterfaceChangeError):
            _ = self.text.anchor_position
        with self.assertRaises(TecplotInterfaceChangeError):
            self.text.anchor_position = None

        with self.assertRaises(TecplotInterfaceChangeError):
            _ = self.text.zone_or_map
        with self.assertRaises(TecplotInterfaceChangeError):
            self.text.zone_or_map = None


class TestTextOnOtherFrame(unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        self.frame = tp.active_frame()
        self.text = self.frame.add_text('abc')
        self.active_frame = tp.active_page().add_frame()

    def test_add_text(self):
        self.active_frame.activate()
        text = self.frame.add_text('def')
        self.assertEqual(text.frame, self.frame)
        self.assertEqual(self.active_frame, tp.active_frame())

    def test_size(self):
        self.active_frame.activate()
        self.text.font.size = 10
        self.assertEqual(self.text.font.size, 10)
        self.assertEqual(self.active_frame, tp.active_frame())


if __name__ == '__main__':
    from .. import main
    main()
