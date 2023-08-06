import base64
import os
import tempfile
import unittest

import tecplot as tp
from tecplot.constant import *
from tecplot.exception import *

from test import sample_data, skip_if_sdk_version_before
from .test_annotation import TestMovableAnnotation


class TestImage(TestMovableAnnotation, unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        self.frame = tp.active_frame()

        self.image_ftmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        self.image_ftmp.write(base64.b64decode(sample_data.images['swoosh_png']))
        self.image_ftmp.close()

        self.image = self.frame.add_image(self.image_ftmp.name, (0,0), 10)
        self.anno = self.image

    def tearDown(self):
        tp.new_layout()
        os.remove(self.image_ftmp.name)

    def test_eq(self):
        self.assertEqual(self.anno, next(self.frame.images()))

    def test_ne(self):
        geom = self.frame.add_circle((0,0), 1, CoordSys.Frame)
        self.assertNotEqual(self.anno, geom)

    def test_type(self):
        self.assertEqual(self.anno.type, GeomType.Image)

    def test_filename(self):
        self.assertEqual(self.image.filename, self.image_ftmp.name)

    @skip_if_sdk_version_before(2018, 3)
    def test_height(self):
        self.image.maintain_aspect_ratio = False
        for val in [1, 10, 20]:
            self.image.height = val
            self.assertAlmostEqual(self.image.height, val, places=6)
        with self.assertRaises(ValueError):
            self.image.height = 'badvalue'
        with self.assertRaises(TecplotValueError):
            self.image.height = 0
        with self.assertRaises(TecplotValueError):
            self.image.height = -1

    def test_maintain_aspect_ratio(self):
        for val in [True, False, True]:
            self.image.maintain_aspect_ratio = val
            self.assertEqual(self.image.maintain_aspect_ratio, val)

        self.image.maintain_aspect_ratio = False
        self.image.size = (5,10)
        self.image.maintain_aspect_ratio = True
        self.image.width = 10
        self.assertAlmostEqual(self.image.height, 20, places=6)

    def test_raw_size(self):
        w, h = self.image.raw_size
        self.assertAlmostEqual(w, 10)
        self.assertAlmostEqual(h, 10)

    def test_reset_aspect_ratio(self):
        self.image.maintain_aspect_ratio = False
        self.image.size = (10, 200)
        self.image.reset_aspect_ratio()
        self.assertLess(self.image.height - 10, 3)
        self.assertLess(self.image.width - 10, 3)

    def test_resize_filter(self):
        for val in ImageResizeFilter:
            self.image.resize_filter = val
            self.assertEqual(self.image.resize_filter, val)
        with self.assertRaises(ValueError):
            self.image.resize_filter = 'badvalue'

    @skip_if_sdk_version_before(2018, 3)
    def test_size(self):
        self.image.maintain_aspect_ratio = False
        for val in [(1,1), (1,2), (10,10), (15,20)]:
            self.image.size = val
            w, h = self.image.size
            self.assertAlmostEqual(w, val[0], places=5)
            self.assertAlmostEqual(h, val[1], places=5)
            self.assertAlmostEqual(self.image.width, val[0], places=5)
            self.assertAlmostEqual(self.image.height, val[1], places=5)
        for val in [(0,0), (1,0), (0,1)]:
            with self.assertRaises((TecplotSystemError, TecplotLogicError,
                                    TecplotValueError)):
                self.image.size = val
        self.image.maintain_aspect_ratio = True
        for val in [(10,10), (15,20)]:
            self.image.size = val
            w, h = self.image.size
            self.assertAlmostEqual(w, val[0], places=5)
            self.assertAlmostEqual(h, val[1], places=5)
            self.assertAlmostEqual(self.image.width, val[0], places=5)
            self.assertAlmostEqual(self.image.height, val[1], places=5)
        with self.assertRaises(ValueError):
            self.image.size = 'badvalue'

    @skip_if_sdk_version_before(2018, 3)
    def test_width(self):
        self.image.maintain_aspect_ratio = False
        for val in [1, 10, 20]:
            self.image.width = val
            self.assertAlmostEqual(self.image.width, val, places=6)
        with self.assertRaises(ValueError):
            self.image.width = 'badvalue'
        with self.assertRaises((TecplotSystemError, TecplotLogicError)):
            self.image.width = 0


if __name__ == '__main__':
    from .. import main
    main()
