import base64, os, tempfile, textwrap
import unittest

import tecplot as tp

from test import sample_data


class TestGeoreferencedImage(unittest.TestCase):
    def setUp(self):
        if tp.sdk_version_info < (2018, 3):
            raise unittest.SkipTest('Added to SDK in 2018.3')

        tp.new_layout()

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

        fr = tp.active_frame()
        self.geom = fr.add_georeferenced_image(self.image_ftmp.name,
                                               self.world_ftmp.name)

    def tearDown(self):
        tp.new_layout()
        os.remove(self.image_ftmp.name)
        os.remove(self.world_ftmp.name)

    def test_z(self):
        for z in [-1, 0., 0.5, 10000]:
            self.geom.z = z
            self.assertEqual(self.geom.z, z)
        with self.assertRaises(ValueError):
            self.geom.z = 'badvalue'


if __name__ == '__main__':
    from .. import main
    main()
