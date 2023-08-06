import unittest

import tecplot as tp
from tecplot.constant import *
from tecplot.exception import *
from tecplot import annotation

from .test_geometry import TestGeometry, TestGeometry2D

from test import mocked_sdk_version


class TestArrowhead(unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        fr = tp.active_frame()
        self.points = [[0.1,0.1], [.2,.4], [.3,.9]]
        self.polyline = fr.add_polyline(self.points)
        self.mpolyline = fr.add_polyline(self.points, self.points)

    def test_angle(self):
        for a in [1, 45, 90]:
            self.polyline.arrowhead.angle = a
            self.assertAlmostEqual(self.polyline.arrowhead.angle, a)
        self.polyline.arrowhead.angle = -400
        self.assertAlmostEqual(self.polyline.arrowhead.angle, 1)
        self.polyline.arrowhead.angle = 400
        self.assertAlmostEqual(self.polyline.arrowhead.angle, 90)
        with self.assertRaises(ValueError):
            self.polyline.arrowhead.angle = 'badvalue'

        for a in [1, 45, 90]:
            self.mpolyline.arrowhead.angle = a
            self.assertAlmostEqual(self.mpolyline.arrowhead.angle, a)
        self.mpolyline.arrowhead.angle = -400
        self.assertAlmostEqual(self.mpolyline.arrowhead.angle, 1)
        self.mpolyline.arrowhead.angle = 400
        self.assertAlmostEqual(self.mpolyline.arrowhead.angle, 90)
        with self.assertRaises(ValueError):
            self.mpolyline.arrowhead.angle = 'badvalue'

    def test_attachment(self):
        for val in ArrowheadAttachment:
            self.polyline.arrowhead.attachment = val
            self.assertEqual(self.polyline.arrowhead.attachment, val)
        with self.assertRaises(ValueError):
            self.polyline.arrowhead.attachment = 'badvalue'

        for val in ArrowheadAttachment:
            self.mpolyline.arrowhead.attachment = val
            self.assertEqual(self.mpolyline.arrowhead.attachment, val)
        with self.assertRaises(ValueError):
            self.mpolyline.arrowhead.attachment = 'badvalue'

    def test_size(self):
        for val in [0,0.5,1,2]:
            self.polyline.arrowhead.size = val
            self.assertEqual(self.polyline.arrowhead.size, val)
        with self.assertRaises(ValueError):
            self.polyline.arrowhead.size = "badtype"
        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            self.polyline.arrowhead.size = -1

        for val in [0,0.5,1,2]:
            self.mpolyline.arrowhead.size = val
            self.assertEqual(self.mpolyline.arrowhead.size, val)
        with self.assertRaises(ValueError):
            self.mpolyline.arrowhead.size = "badtype"
        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            self.mpolyline.arrowhead.size = -1

    def test_style(self):
        for val in ArrowheadStyle:
            self.polyline.arrowhead.style = val
            self.assertEqual(self.polyline.arrowhead.style, val)
        with self.assertRaises(ValueError):
            self.polyline.arrowhead.style = 'badvalue'

        for val in ArrowheadStyle:
            self.mpolyline.arrowhead.style = val
            self.assertEqual(self.mpolyline.arrowhead.style, val)
        with self.assertRaises(ValueError):
            self.mpolyline.arrowhead.style = 'badvalue'


class TestPolyline(TestGeometry):
    def test_type(self):
        self.assertEqual(self.geom.type, GeomType.LineSegs)

    def test_len(self):
        self.assertEqual(len(self.geom), len(self.points))


class TestPolyline2D(TestPolyline, TestGeometry2D, unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        fr = tp.active_frame()
        self.points = [[0.1,0.1], [.2,.4], [.3,.9]]
        self.geom = fr.add_polyline(self.points)
        self.anno = self.geom

    def test_arrowhead(self):
        self.assertIsInstance(self.geom.arrowhead, annotation.Arrowhead)

    def test_getset(self):
        self.geom[:] = self.points
        for i, (x, y) in enumerate(self.points):
            p = self.geom[i]
            self.assertAlmostEqual(x, p.x)
            self.assertAlmostEqual(y, p.y)

        points = [[0.2,0.3], [1.0,0.4], [.2,.3]]
        self.geom[:] = points
        for i, (x, y) in enumerate(points):
            p = self.geom[i]
            self.assertAlmostEqual(x, p.x)
            self.assertAlmostEqual(y, p.y)

        points = [[2,3], [4,5]]
        self.geom[::2] = points
        for i, (x, y) in enumerate([[2,3], [1.0,0.4], [4,5]]):
            p = self.geom[i]
            self.assertAlmostEqual(x, p.x)
            self.assertAlmostEqual(y, p.y)

        self.geom[1] = 6,7
        for i, (x, y) in enumerate([[2,3], [6,7], [4,5]]):
            p = self.geom[i]
            self.assertAlmostEqual(x, p.x)
            self.assertAlmostEqual(y, p.y)

        with mocked_sdk_version(2018, 2):
            points = [[0.2,0.3], [1.0,0.4], [.2,.3]]
            self.geom[:] = points
            for i, (x, y) in enumerate(points):
                p = self.geom[i]
                self.assertAlmostEqual(x, p.x)
                self.assertAlmostEqual(y, p.y)


class TestPolyline3D(TestPolyline, unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        fr = tp.active_frame()
        self.points = [[.1,.1,.1], [.1,.2,.4], [.3,.4,.9]]
        self.geom = fr.add_polyline(self.points)
        self.anno = self.geom

    def test_getset(self):
        self.geom[:] = self.points
        for i, (x, y, z) in enumerate(self.points):
            p = self.geom[i]
            self.assertAlmostEqual(x, p.x)
            self.assertAlmostEqual(y, p.y)
            self.assertAlmostEqual(z, p.z)

        points = [[.2,.3,.7], [1.0,.4,4], [.02,.2,.3]]
        self.geom[:] = points
        for i, (x, y, z) in enumerate(points):
            p = self.geom[i]
            self.assertAlmostEqual(x, p.x)
            self.assertAlmostEqual(y, p.y)
            self.assertAlmostEqual(z, p.z, places=6)

        points = [[2,3,7], [0,1,2]]
        self.geom[::2] = points
        for i, (x, y, z) in enumerate([[2,3,7], [1.0,.4,4], [0,1,2]]):
            p = self.geom[i]
            self.assertAlmostEqual(x, p.x)
            self.assertAlmostEqual(y, p.y)
            self.assertAlmostEqual(z, p.z)

        self.geom[1] = 6,7,8
        for i, (x, y, z) in enumerate([[2,3,7], [6,7,8], [0,1,2]]):
            p = self.geom[i]
            self.assertAlmostEqual(x, p.x)
            self.assertAlmostEqual(y, p.y)
            self.assertAlmostEqual(z, p.z)

        with mocked_sdk_version(2018, 2):
            points = [[.2,.3,.7], [1.0,.4,4], [.02,.2,.3]]
            self.geom[:] = points
            for i, (x, y, z) in enumerate(points):
                p = self.geom[i]
                self.assertAlmostEqual(x, p.x)
                self.assertAlmostEqual(y, p.y)
                self.assertAlmostEqual(z, p.z, places=6)


class TestMultiPolyline(TestPolyline):
    def test_points(self):
        for exline, line in zip(self.points, self.geom):
            for expt, pt in zip(exline, line):
                for exval, val in zip(expt, pt):
                    self.assertAlmostEqual(exval, val)


class TestMultiPolyline2D(TestMultiPolyline, TestGeometry2D, unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        fr = tp.active_frame()
        self.points = [
            [[.1,.1], [.1,.2], [.3,.4]],
            [[2,3], [5,6], [8,9]],
            [[-10,5], [-1000,1000], [5,6]],
        ]
        self.geom = fr.add_polyline(*self.points)
        self.anno = self.geom

    def test_arrowhead(self):
        self.assertIsInstance(self.geom.arrowhead, annotation.Arrowhead)

    def test_get(self):
        self.assertIsInstance(self.geom[0], annotation.Polyline2D)
        self.assertIsInstance(self.geom[1], annotation.Polyline2D)
        self.assertIsInstance(self.geom[2], annotation.Polyline2D)
        if __debug__:
            with self.assertRaises(IndexError):
                _ = self.geom[3]

    def test_set(self):
        for line_num in range(len(self.geom)):
            points = [[.2,.3], [1.0,.4], [.02,.2,]]
            self.geom[line_num][:] = points
            for i, (x, y) in enumerate(points):
                p = self.geom[line_num][i]
                self.assertAlmostEqual(x, p.x)
                self.assertAlmostEqual(y, p.y)

            with mocked_sdk_version(2018, 2):
                points = [[.2,.3], [1.0,.4], [.02,.2]]
                self.geom[line_num][:] = points
                for i, (x, y) in enumerate(points):
                    p = self.geom[line_num][i]
                    self.assertAlmostEqual(x, p.x)
                    self.assertAlmostEqual(y, p.y)


class TestMultiPolyline3D(TestMultiPolyline, unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        fr = tp.active_frame()
        self.points = [
            [[.1,.1,.1], [.1,.2,.4], [.3,.4,.9]],
            [[2,3,4], [5,6,7], [8,9,10]],
            [[-10,5,0], [-1000,1000,10000], [5,6,7]],
        ]
        self.geom = fr.add_polyline(*self.points)
        self.anno = self.geom

    def test_get(self):
        self.assertIsInstance(self.geom[0], annotation.Polyline3D)
        self.assertIsInstance(self.geom[1], annotation.Polyline3D)
        self.assertIsInstance(self.geom[2], annotation.Polyline3D)
        if __debug__:
            with self.assertRaises(IndexError):
                _ = self.geom[3]

    def test_set(self):
        for line_num in range(len(self.geom)):
            points = [[.2,.3,.7], [1.0,.4,4], [.02,.2,.3]]
            self.geom[line_num][:] = points
            for i, (x, y, z) in enumerate(points):
                p = self.geom[line_num][i]
                self.assertAlmostEqual(x, p.x)
                self.assertAlmostEqual(y, p.y)
                self.assertAlmostEqual(z, p.z, places=6)

            with mocked_sdk_version(2018, 2):
                points = [[.2,.3,.7], [1.0,.4,4], [.02,.2,.3]]
                self.geom[line_num][:] = points
                for i, (x, y, z) in enumerate(points):
                    p = self.geom[line_num][i]
                    self.assertAlmostEqual(x, p.x)
                    self.assertAlmostEqual(y, p.y)
                    self.assertAlmostEqual(z, p.z, places=6)


if __name__ == '__main__':
    from .. import main
    main()
