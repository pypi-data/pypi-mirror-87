import base64, tempfile, textwrap, os, unittest

import tecplot as tp
from tecplot.constant import *

from test import sample_data, skip_if_sdk_version_before


class TestGeometryIteratorNoItems(unittest.TestCase):
    def setUp(self):
        tp.new_layout()

    def test_iter_no_items(self):
        self.assertEqual(list(tp.active_frame().geometries()), [])
        self.assertEqual(list(tp.active_frame().images()), [])


class TestGeometryIterator(unittest.TestCase):
    @skip_if_sdk_version_before(2018, 2, msg='georef images added to SDK in 2018.2')
    def setUp(self):
        tp.new_layout()
        self.fr = tp.active_frame()

        self.image_ftmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        self.image_ftmp.write(base64.b64decode(sample_data.images['swoosh_png']))
        self.image_ftmp.close()

        self.world_ftmp = tempfile.NamedTemporaryFile(suffix='.pgw', mode='w+t', delete=False)
        # example world file numbers taken from
        # http://webhelp.esri.com/arcims/9.3/General/topics/author_world_files.htm
        self.world_ftmp.write(textwrap.dedent(r'''
            20.17541308822119
            0.00000000000000
            0.00000000000000
            -20.17541308822119
            424178.11472601280548
            4313415.90726399607956
        '''))
        self.world_ftmp.close()

        self.images = [
            self.fr.add_georeferenced_image(self.image_ftmp.name,
                                            self.world_ftmp.name),
            self.fr.add_image(self.image_ftmp.name, (0,0), 10),
            self.fr.add_image(self.image_ftmp.name, (1,1), 5),
        ]

        self.geoms = [
            self.fr.add_circle((0,0), 1, CoordSys.Grid),
            self.fr.add_ellipse((0,0), (1,1), CoordSys.Grid),
            self.fr.add_rectangle((0,0), (1,1), CoordSys.Frame),
            self.fr.add_square((0,0), 1, CoordSys.Frame),
            self.fr.add_polyline([[0,0], [1,2], [3,4]]),
            self.fr.add_polyline([[0,0,1], [1,2,3], [2,3,4]]),
            self.fr.add_polyline([[0,0], [1,2], [3,4]],
                            [[0,0], [1,2], [3,4]],
                            coord_sys=CoordSys.Frame),
            self.fr.add_polyline([[0,0,1], [1,2,3], [2,3,4]],
                            [[0,0,1], [1,2,3], [2,3,4]]),
        ]

    def tearDown(self):
        tp.new_layout()
        os.remove(self.image_ftmp.name)
        os.remove(self.world_ftmp.name)

    def test_iter_shapes(self):
        geoms = self.fr.geometries()
        for expected, item in zip(self.geoms, geoms):
            self.assertEqual(expected, item)

        with self.assertRaises(StopIteration):
            _ = next(geoms)

    def test_iter_images(self):
        images = self.fr.images()
        for expected, item in zip(self.images, images):
            self.assertEqual(expected, item)

        with self.assertRaises(StopIteration):
            _ = next(images)

    def test_next(self):
        geoms = self.fr.geometries()
        self.assertEqual(self.geoms[0], next(geoms))
        self.assertEqual(self.geoms[1], geoms.next())


class TestTextIteratorNoItems(unittest.TestCase):
    def setUp(self):
        tp.new_layout()

    def test_iter_no_items(self):
        self.assertEqual(list(tp.active_frame().texts()), [])


class TestTextIterator(unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        self.fr = tp.active_frame()
        self.texts = [
            self.fr.add_text('test1', (0,0)),
            self.fr.add_text('test2', (0,0)),
            self.fr.add_text('test3', (0,0)),
        ]

    def test_iter(self):
        for expected, item in zip(self.texts, self.fr.texts()):
            self.assertEqual(expected, item)

    def test_next(self):
        texts = self.fr.texts()
        self.assertEqual(self.texts[0], next(texts))
        self.assertEqual(self.texts[1], texts.next())


if __name__ == '__main__':
    from .. import main
    main()
