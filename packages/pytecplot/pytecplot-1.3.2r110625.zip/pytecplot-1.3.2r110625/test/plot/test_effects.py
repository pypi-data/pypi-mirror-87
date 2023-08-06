import os
import unittest

import numpy as np

import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *
from tecplot import text

from .. import sample_data


class TestLightSource(unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        self.filename, dataset = sample_data.sample_data('10x10x10')
        frame = tp.active_frame()
        frame.plot_type = PlotType.Cartesian3D
        self.lightsource = frame.plot().light_source

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    def test_background_light(self):
        for val in [0, 0.5, 1, 100]:
            self.lightsource.background_light = val
            self.assertAlmostEqual(self.lightsource.background_light, val)
        with self.assertRaises(TecplotSystemError):
            self.lightsource.background_light = -1
        with self.assertRaises(TecplotSystemError):
            self.lightsource.background_light = 101
        with self.assertRaises(ValueError):
            self.lightsource.background_light = 'badvalue'

    def test_intensity(self):
        for val in [0, 0.5, 1, 100]:
            self.lightsource.intensity = val
            self.assertAlmostEqual(self.lightsource.intensity, val)
        with self.assertRaises(TecplotSystemError):
            self.lightsource.intensity = -1
        with self.assertRaises(TecplotSystemError):
            self.lightsource.intensity = 101
        with self.assertRaises(ValueError):
            self.lightsource.intensity = 'badvalue'

    def test_specular_intensity(self):
        for val in [0, 0.5, 1, 100]:
            self.lightsource.specular_intensity = val
            self.assertAlmostEqual(self.lightsource.specular_intensity, val)
        with self.assertRaises(TecplotSystemError):
            self.lightsource.specular_intensity = -1
        with self.assertRaises(TecplotSystemError):
            self.lightsource.specular_intensity = 101
        with self.assertRaises(ValueError):
            self.lightsource.specular_intensity = 'badvalue'

    def test_specular_shininess(self):
        for val in [0, 0.5, 1, 100]:
            self.lightsource.specular_shininess = val
            self.assertAlmostEqual(self.lightsource.specular_shininess, val)
        with self.assertRaises(TecplotSystemError):
            self.lightsource.specular_shininess = -1
        with self.assertRaises(TecplotSystemError):
            self.lightsource.specular_shininess = 101
        with self.assertRaises(ValueError):
            self.lightsource.specular_shininess = 'badvalue'

    def test_surface_color_contrast(self):
        for val in [0, 0.5, 1, 100]:
            self.lightsource.surface_color_contrast = val
            self.assertAlmostEqual(self.lightsource.surface_color_contrast, val)
        with self.assertRaises(TecplotSystemError):
            self.lightsource.surface_color_contrast = -1
        with self.assertRaises(TecplotSystemError):
            self.lightsource.surface_color_contrast = 101
        with self.assertRaises(ValueError):
            self.lightsource.surface_color_contrast = 'badvalue'

    def test_direction(self):
        self.lightsource.direction = (0, 0, 0)
        np.testing.assert_array_almost_equal(self.lightsource.direction, (0, 0, 0))
        self.lightsource.direction = (1, 2, 3)
        np.testing.assert_array_almost_equal(self.lightsource.direction, (1, 2, 3))

    def test_force_gouraud_for_contour_flood(self):
        for val in [True, False, True]:
            self.lightsource.force_gouraud_for_contour_flood = val
            self.assertEqual(self.lightsource.force_gouraud_for_contour_flood, val)

    def test_force_paneled_for_cell_flood(self):
        for val in [True, False, True]:
            self.lightsource.force_paneled_for_cell_flood = val
            self.assertEqual(self.lightsource.force_paneled_for_cell_flood, val)


if __name__ == '__main__':
    from .. import main
    main()
