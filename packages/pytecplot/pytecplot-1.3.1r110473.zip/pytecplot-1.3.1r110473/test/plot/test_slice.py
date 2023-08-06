import os
import unittest

from unittest.mock import ANY

import tecplot as tp
from tecplot.tecutil import sv
from tecplot.exception import *
from tecplot.constant import *
from tecplot.plot import slice

from tecplot.tecutil import Index
from ..property_test import PropertyTest
from test import patch_tecutil
from tecplot.plot import ContourGroup

from test import (assert_style, sample_data, skip_if_sdk_version_before,
                  mocked_sdk_version)


class TestSliceMesh(unittest.TestCase):
    @staticmethod
    def setUpClass():
        sample_data.create_ordered_3d()

    def setUp(self):
        self.plot = tp.active_frame().plot()
        self.mesh = self.plot.slice(0).mesh

    def test_show(self):
        for val in [True, False, True]:
            self.mesh.show = val
            self.assertEqual(self.mesh.show, val)

    def test_color(self):
        for val in [Color.Blue, self.plot.contour(0), Color.Red]:
            self.mesh.color = val
            self.assertEqual(self.mesh.color, val)

    def test_line_thickness(self):
        for val in [0.5, 1, 100]:
            self.mesh.line_thickness = val
            self.assertAlmostEqual(self.mesh.line_thickness, val)
        with self.assertRaises(ValueError):
            self.mesh.line_thickness = 'badvalue'
        with self.assertRaises(TecplotSystemError):
            self.mesh.line_thickness = 0
        with self.assertRaises(TecplotSystemError):
            self.mesh.line_thickness = -1


class TestSliceShade(unittest.TestCase):
    @staticmethod
    def setUpClass():
        sample_data.create_ordered_3d()

    def setUp(self):
        self.shade = tp.active_frame().plot().slice(0).shade

    def test_show(self):
        for val in [True, False, True]:
            self.shade.show = val
            self.assertEqual(self.shade.show, val)

    def test_color(self):
        for val in [Color.Blue, Color.Red]:
            self.shade.color = val
            self.assertEqual(self.shade.color, val)

    def test_use_lighting_effect(self):
        for val in [True, False, True]:
            self.shade.use_lighting_effect = val
            self.assertEqual(self.shade.use_lighting_effect, val)


class TestSliceEffects(unittest.TestCase):
    @staticmethod
    def setUpClass():
        sample_data.create_ordered_3d()

    def setUp(self):
        self.effects = tp.active_frame().plot().slice(0).effects

    def test_lighting_effect(self):
        for val in [LightingEffect.Gouraud, LightingEffect.Paneled]:
            self.effects.lighting_effect = val
            self.assertEqual(self.effects.lighting_effect, val)

    def test_surface_translucency(self):
        for val in [1, 2, 99]:
            self.effects.surface_translucency = val
            self.assertAlmostEqual(self.effects.surface_translucency, val)
        with self.assertRaises(ValueError):
            self.effects.surface_translucency = 'badvalue'
        with self.assertRaises(TecplotSystemError):
            self.effects.surface_translucency = 0
        with self.assertRaises(TecplotSystemError):
            self.effects.surface_translucency = -1
        with self.assertRaises(TecplotSystemError):
            self.effects.surface_translucency = 100

    def test_use_translucency(self):
        for val in [True, False, True]:
            self.effects.use_translucency = val
            self.assertEqual(self.effects.use_translucency, val)


class TestSliceEdge(unittest.TestCase):
    @staticmethod
    def setUpClass():
        sample_data.create_ordered_3d()

    def setUp(self):
        self.edge = tp.active_frame().plot().slice(0).edge

    def test_show(self):
        for val in [True, False, True]:
            self.edge.show = val
            self.assertEqual(self.edge.show, val)

    def test_edge_type(self):
        for val in [EdgeType.Borders, EdgeType.Creases]:
            self.edge.edge_type = val
            self.assertEqual(self.edge.edge_type, val)
        with self.assertRaises(ValueError):
            self.edge.edge_type = 'badvalue'

    def test_color(self):
        for val in [Color.Blue, Color.Red]:
            self.edge.color = val
            self.assertEqual(self.edge.color, val)

    def test_line_thickness(self):
        for val in [0.5, 1, 100]:
            self.edge.line_thickness = val
            self.assertAlmostEqual(self.edge.line_thickness, val)
        with self.assertRaises(ValueError):
            self.edge.line_thickness = 'badvalue'
        with self.assertRaises(TecplotSystemError):
            self.edge.line_thickness = 0
        with self.assertRaises(TecplotSystemError):
            self.edge.line_thickness = -1
        with self.assertRaises(TecplotSystemError):
            self.edge.line_thickness = 101


class TestSliceVector(unittest.TestCase):
    @staticmethod
    def setUpClass():
        sample_data.create_ordered_3d()

    def setUp(self):
        self.vec = tp.active_frame().plot().slice(0).vector

    def test_show(self):
        for val in [True, False, True]:
            self.vec.show = val
            self.assertEqual(self.vec.show, val)

    def test_is_tangent(self):
        for val in [True, False, True]:
            self.vec.is_tangent = val
            self.assertEqual(self.vec.is_tangent, val)

    def test_color(self):
        for val in [Color.Black, Color.Red, Color.Blue]:
            self.vec.color = val
            self.assertEqual(self.vec.color, val)
        with self.assertRaises(ValueError):
            self.vec.color = 0.5

    def test_line_thickness(self):
        for val in [0.5, 1, 2, 100]:
            self.vec.line_thickness = val
            self.assertAlmostEqual(self.vec.line_thickness, val)
        with self.assertRaises(ValueError):
            self.vec.line_thickness = 'badtype'
        with self.assertRaises(TecplotSystemError):
            self.vec.line_thickness = -1
        with self.assertRaises(TecplotSystemError):
            self.vec.line_thickness = 0
        with self.assertRaises(TecplotSystemError):
            self.vec.line_thickness = 101

    def test_vector_type(self):
        for val in [VectorType.TailAtPoint, VectorType.HeadAtPoint,
                    VectorType.MidAtPoint]:
            self.vec.vector_type = val
            self.assertEqual(self.vec.vector_type, val)
        with self.assertRaises(ValueError):
            self.vec.vector_type = 0.5

    def test_arrowhead_style(self):
        for val in [ArrowheadStyle.Plain, ArrowheadStyle.Filled,
                    ArrowheadStyle.Hollow]:
            self.vec.arrowhead_style = val
            self.assertEqual(self.vec.arrowhead_style, val)
        with self.assertRaises(ValueError):
            self.vec.arrowhead_style = 0.5


class TestSliceContour(unittest.TestCase):
    @staticmethod
    def setUpClass():
        sample_data.create_ordered_3d()

    def setUp(self):
        self.plot = tp.active_frame().plot()
        self.contour = self.plot.slice(0).contour

    def test_show(self):
        for val in [True, False, True]:
            self.contour.show = val
            self.assertEqual(self.contour.show, val)

    def test_contour_type(self):
        for val in [ContourType.AverageCell, ContourType.Flood]:
            self.contour.contour_type = val
            self.assertEqual(self.contour.contour_type, val)
        with self.assertRaises(ValueError):
            self.contour.contour_type = 0.5

    def test_line_color(self):
        for val in [Color.Blue, Color.Azure, Color.Red]:
            self.contour.line_color = val
            self.assertEqual(self.contour.line_color, val)

    def test_line_thickness(self):
        for val in [0.5, 1, 100]:
            self.contour.line_thickness = val
            self.assertAlmostEqual(self.contour.line_thickness, val)
        with self.assertRaises(ValueError):
            self.contour.line_thickness = 'badvalue'
        with self.assertRaises(TecplotSystemError):
            self.contour.line_thickness = 0
        with self.assertRaises(TecplotSystemError):
            self.contour.line_thickness = -1

    def test_flood_contour_group_index(self):
        for val in [0, 1, 3]:
            self.contour.flood_contour_group_index = val
            self.assertAlmostEqual(self.contour.flood_contour_group_index, val)
        with self.assertRaises(ValueError):
            self.contour.flood_contour_group_index = 'badvalue'
        with self.assertRaises(TecplotSystemError):
            self.contour.flood_contour_group_index = -1

    def test_flood_contour_group(self):
        self.contour.line_contour_group = self.plot.contour(1)

        self.contour.flood_contour_group = self.plot.contour(0)
        self.assertEqual(self.contour.flood_contour_group, self.plot.contour(0))
        self.contour.flood_contour_group = self.plot.contour(3)
        self.assertNotEqual(self.contour.flood_contour_group, self.plot.contour(0))
        self.assertEqual(self.contour.flood_contour_group, self.plot.contour(3))
        self.contour.flood_contour_group = self.plot.contour(0)
        self.assertEqual(self.contour.flood_contour_group, self.plot.contour(0))
        self.assertNotEqual(self.contour.flood_contour_group, self.plot.contour(3))

        self.assertEqual(self.contour.line_contour_group, self.plot.contour(1))

    def test_line_contour_group_index(self):
        for val in [0, 1, 3]:
            self.contour.line_contour_group_index = val
            self.assertAlmostEqual(self.contour.line_contour_group_index, val)
        with self.assertRaises(ValueError):
            self.contour.line_contour_group_index = 'badvalue'
        with self.assertRaises(TecplotSystemError):
            self.contour.line_contour_group_index = -1

    def test_line_contour_group(self):
        self.contour.flood_contour_group = self.plot.contour(1)

        self.contour.line_contour_group = self.plot.contour(0)
        self.assertEqual(self.contour.line_contour_group, self.plot.contour(0))
        self.contour.line_contour_group = self.plot.contour(3)
        self.assertNotEqual(self.contour.line_contour_group, self.plot.contour(0))
        self.assertEqual(self.contour.line_contour_group, self.plot.contour(3))
        self.contour.line_contour_group = self.plot.contour(0)
        self.assertEqual(self.contour.line_contour_group, self.plot.contour(0))
        self.assertNotEqual(self.contour.line_contour_group, self.plot.contour(3))

        self.assertEqual(self.contour.flood_contour_group, self.plot.contour(1))

    def test_use_lighting_effect(self):
        for val in [True, False, True]:
            self.contour.use_lighting_effect = val
            self.assertEqual(self.contour.use_lighting_effect, val)


class TestSliceGroupCollection(unittest.TestCase):
    @staticmethod
    def setUpClass():
        plot = sample_data.create_ordered_3d()
        sample_data.create_ordered_3d(frame=plot.frame)

    def setUp(self):
        frame = tp.active_frame()
        self.dataset = frame.dataset
        self.plot = frame.plot()
        self.slices = self.plot.slices(0, 1)

    def test_indices(self):
        self.assertEqual(self.slices.indices, [0, 1])
        self.assertEqual(self.plot.slices().indices, list(range(8)))

    def test_eq(self):
        self.assertTrue(self.slices == self.plot.slices(0, 1))
        self.assertTrue(self.slices != self.plot.slices(1))
        self.assertFalse(self.slices == self.plot.slices(1))
        self.assertFalse(self.slices != self.plot.slices(0, 1))

    def test_iter(self):
        for i, slc in enumerate(self.slices):
            self.assertEqual(self.plot.slice(i), slc)

    @skip_if_sdk_version_before(2017, 3)
    def test_extract(self):
        nzones = self.dataset.num_zones
        new_zones = list(self.slices.extract())
        self.assertIsInstance(new_zones[0], tp.data.zone.Zone)
        self.assertEqual(self.dataset.num_zones, nzones + 2)

        nzones = self.dataset.num_zones
        new_zones = self.slices.extract(
            mode=ExtractMode.OneZonePerConnectedRegion,
            assign_strand_ids=False,
            resulting_1d_zone_type=Resulting1DZoneType.FELineSegment)
        new_zones = list(new_zones)
        self.assertGreater(len(new_zones), 0)
        self.assertIsInstance(new_zones[0], tp.data.zone.Zone)
        self.assertEqual(self.dataset.num_zones, nzones + len(new_zones))

        with patch_tecutil('ExtractSlicesX', return_value=False):
            with self.assertRaises((TecplotSystemError, TecplotLogicError)):
                self.slices.extract()

        if __debug__:
            with mocked_sdk_version(2017, 2):
                with self.assertRaises(TecplotOutOfDateEngineError):
                    self.slices.extract()
        if __debug__:
            with mocked_sdk_version(2018, 2):
                with patch_tecutil('ExtractSlicesX', return_value=False):
                    with self.assertRaises((TecplotSystemError, TecplotLogicError)):
                        self.slices.extract()

    @skip_if_sdk_version_before(2019, 1)
    def test_extract_transient(self):
        self.dataset.zone(0).strand = 1
        self.dataset.zone(0).solution_time = 1.0
        self.dataset.zone(1).strand = 1
        self.dataset.zone(1).solution_time = 2.0
        self.plot.active_fieldmap_indices = [0, 1]
        self.plot.solution_time = 1.0

        z = self.slices.extract(
            transient_mode=TransientOperationMode.AllSolutionTimes)
        z = list(z)
        self.assertGreater(len(z), 1)

    def test_subclasses(self):
        self.assertIsInstance(self.slices.vector, slice.SliceVector)
        self.assertIsInstance(self.slices.mesh, slice.SliceMesh)
        self.assertIsInstance(self.slices.effects, slice.SliceEffects)
        self.assertIsInstance(self.slices.shade, slice.SliceShade)
        self.assertIsInstance(self.slices.edge, slice.SliceEdge)
        self.assertIsInstance(self.slices.contour, slice.SliceContour)
        with self.assertRaises(AttributeError):
            self.slices.contour = None
        with self.assertRaises(AttributeError):
            self.slices.mesh = None
        with self.assertRaises(AttributeError):
            self.slices.effects = None
        with self.assertRaises(AttributeError):
            self.slices.edge = None
        with self.assertRaises(AttributeError):
            self.slices.shade = None
        with self.assertRaises(AttributeError):
            self.slices.vector = None

    def test_show(self):
        for val in [True, False, True]:
            self.slices.show = val
            self.assertEqual(self.slices.show, tuple([val] * 2))

    def test_orientation(self):
        for val in [SliceSurface.Arbitrary, SliceSurface.IPlanes,
                    SliceSurface.YPlanes]:
            self.slices.orientation = val
            self.assertEqual(self.slices.orientation, tuple([val] * 2))

    def test_start_position(self):
        self.slices.orientation = SliceSurface.IPlanes
        self.slices.start_position = (0, 1, 2)
        self.assertAllClose(self.slices.start_position, ((0,0),(1,1),(2,2)))

        self.slices.start_position = (3, 5, 7)
        self.assertAllClose(self.slices.start_position, ((3,3),(5,5),(7,7)))

        self.slices.start_position.i = 2
        self.slices.start_position.j = 3
        self.slices.start_position.k = 4
        self.assertEqual(self.slices.start_position.i, (2,2))
        self.assertEqual(self.slices.start_position.j, (3,3))
        self.assertEqual(self.slices.start_position.k, (4,4))

        self.slices.orientation = SliceSurface.Arbitrary
        self.slices.start_position = (0, 1, 2)
        self.assertAllClose(self.slices.start_position, ((0,0),(1,1),(2,2)))

        self.slices.start_position = (3, 5, 7)
        self.assertAllClose(self.slices.start_position, ((3,3),(5,5),(7,7)))

        self.slices.start_position.x = 2
        self.slices.start_position.y = 3
        self.slices.start_position.z = 4
        self.assertAlmostEqual(self.slices.start_position.x, (2,2))
        self.assertAlmostEqual(self.slices.start_position.y, (3,3))
        self.assertAlmostEqual(self.slices.start_position.z, (4,4))

        self.plot.slice(0).orientation = SliceSurface.IPlanes
        with self.assertRaises(TecplotLogicError):
            _ = self.slices.start_position

    def test_contour_flood_group(self):
        slice_contour = self.slices.contour
        cont2 = self.plot.contour(2)
        cont3 = self.plot.contour(3)
        cont4 = self.plot.contour(4)

        slice_contour.line_contour_group = cont2
        self.assertEqual(slice_contour.line_contour_group_index, (2, 2))
        self.assertEqual(slice_contour.line_contour_group, tuple([cont2] * 2))

        slice_contour.flood_contour_group = cont4
        self.assertEqual(slice_contour.flood_contour_group, tuple([cont4] * 2))

        slice_contour.flood_contour_group = cont3
        self.assertEqual(slice_contour.flood_contour_group, tuple([cont3] * 2))

        slice_contour.flood_contour_group_index = 4
        self.assertEqual(slice_contour.flood_contour_group_index, (4, 4))
        self.assertEqual(slice_contour.flood_contour_group, tuple([cont4] * 2))

        self.assertEqual(slice_contour.line_contour_group_index, (2, 2))
        self.assertEqual(slice_contour.line_contour_group, tuple([cont2] * 2))

    def test_num_intermediate_slices(self):
        for val in [1, 2]:
            self.slices.num_intermediate_slices = val
            self.assertEqual(self.slices.num_intermediate_slices, tuple([val] * 2))

    @skip_if_sdk_version_before(2017, 3)
    def test_fallback_extraction(self):
        with mocked_sdk_version(2018, 2):
            z = self.slices.extract()
            z = list(z)
            self.assertGreater(len(z), 1)

    def test_use_slice_clipping(self):
        for val in [True, False, True]:
            self.slices.use_slice_clipping = val
            self.assertEqual(self.slices.use_slice_clipping, tuple([val] * 2))
        with assert_style(True, sv.SLICEATTRIBUTES, sv.OBEYCLIPPLANES,
                          once=False, OFFSET1=ANY, **self.slices._style_attrs):
            self.slices.use_slice_clipping = True
            _ = self.slices.use_slice_clipping

    def test_clip(self):
        for val in [ClipPlane.AbovePrimarySlice,
                    ClipPlane.BelowPrimarySlice,
                    ClipPlane.None_]:
            self.slices.clip = val
            self.assertEqual(self.slices.clip, tuple([val] * 2))
        with self.assertRaises(ValueError):
            self.slices.clip = 0.5


class TestSliceGroup(unittest.TestCase):
    @staticmethod
    def setUpClass():
        plot = sample_data.create_ordered_3d()
        sample_data.create_ordered_3d(frame=plot.frame)

    def setUp(self):
        fr = tp.active_frame()
        self.dataset = fr.dataset
        self.plot = fr.plot()
        self.slice = self.plot.slice(0)

    @skip_if_sdk_version_before(2017, 3)
    def test_extract(self):
        nzones = self.dataset.num_zones
        new_zone = self.slice.extract()
        self.assertIsInstance(new_zone, tp.data.zone.Zone)
        self.assertEqual(self.dataset.num_zones, nzones + 1)

        nzones = self.dataset.num_zones
        new_zones = self.slice.extract(
            mode=ExtractMode.OneZonePerConnectedRegion,
            assign_strand_ids=False,
            resulting_1d_zone_type=Resulting1DZoneType.FELineSegment)
        new_zones = list(new_zones)
        self.assertGreater(len(new_zones), 0)
        self.assertIsInstance(new_zones[0], tp.data.zone.Zone)
        self.assertEqual(self.dataset.num_zones, nzones + len(new_zones))

        with patch_tecutil('ExtractSlicesX', return_value=False):
            with self.assertRaises((TecplotSystemError, TecplotLogicError)):
                self.slice.extract()

        if __debug__:
            with mocked_sdk_version(2017, 2):
                with self.assertRaises(TecplotOutOfDateEngineError):
                    self.slice.extract()

    @skip_if_sdk_version_before(2019, 1)
    def test_extract_transient(self):
        self.dataset.zone(0).strand = 1
        self.dataset.zone(0).solution_time = 1.0
        self.dataset.zone(1).strand = 1
        self.dataset.zone(1).solution_time = 2.0
        self.plot.active_fieldmap_indices = [0, 1]
        self.plot.solution_time = 1.0

        z = self.slice.extract(
            transient_mode=TransientOperationMode.AllSolutionTimes)
        z = list(z)
        self.assertGreater(len(z), 1)

    def test_eq(self):
        self.assertTrue(self.slice == self.plot.slice(0))
        self.assertTrue(self.slice != self.plot.slice(1))
        self.assertFalse(self.slice == self.plot.slice(1))
        self.assertFalse(self.slice != self.plot.slice(0))

    def test_show(self):
        for val in [True, False, True]:
            self.slice.show = val
            self.assertEqual(self.slice.show, val)

    def test_show_primary_slice(self):
        for val in [True, False, True]:
            self.slice.show_primary_slice = val
            self.assertEqual(self.slice.show_primary_slice, val)

    def test_arbitrary_normal(self):
        p1 = (1, 2, 3)
        p2 = (4, 5, 6)
        p3 = (.7, .8, .9)

        self.plot.show_slices = True
        self.slice.orientation = SliceSurface.Arbitrary
        self.slice.set_arbitrary_from_points(p1, p2, p3)

        self.assertAlmostEqual(self.slice.arbitrary_normal[0], -2.7)
        self.assertAlmostEqual(self.slice.arbitrary_normal[1], 5.4)
        self.assertAlmostEqual(self.slice.arbitrary_normal[2], -2.7)
        self.assertEqual(self.slice.origin, (.7, .8, .9))

        with patch_tecutil('SliceSetArbitraryUsingThreePoints') as set_arb:
            set_arb.return_value = False
            with self.assertRaises(TecplotSystemError):
                p1 = (1, 2, 3)
                p2 = (4, 5, 6)
                p3 = (.7, .8, .9)
                self.slice.set_arbitrary_from_points(p1, p2, p3)

        self.slice.arbitrary_normal = (1, 2, 3)
        self.assertAllClose(self.slice.arbitrary_normal, (1, 2, 3))

    def test_start_position(self):
        self.slice.orientation = SliceSurface.IPlanes
        self.slice.start_position = (0, 1, 2)
        self.assertAllClose(self.slice.start_position, (0, 1, 2))

        self.slice.start_position = (3, 5, 7)
        self.assertAllClose(self.slice.start_position, (3, 5, 7))

        self.slice.start_position.i = 2
        self.slice.start_position.j = 3
        self.slice.start_position.k = 4
        self.assertEqual(self.slice.start_position.i, 2)
        self.assertEqual(self.slice.start_position.j, 3)
        self.assertEqual(self.slice.start_position.k, 4)

        self.slice.orientation = SliceSurface.Arbitrary
        self.slice.start_position = (0, 1, 2)
        self.assertAllClose(self.slice.start_position, (0, 1, 2))

        self.slice.start_position = (3, 5, 7)
        self.assertAllClose(self.slice.start_position, (3, 5, 7))

        self.slice.start_position.x = 2
        self.slice.start_position.y = 3
        self.slice.start_position.z = 4
        self.assertAlmostEqual(self.slice.start_position.x, 2)
        self.assertAlmostEqual(self.slice.start_position.y, 3)
        self.assertAlmostEqual(self.slice.start_position.z, 4)

    def test_end_position(self):
        self.slice.orientation = SliceSurface.IPlanes
        self.slice.end_position = (0, 1, 2)
        self.assertAllClose(self.slice.end_position, (0, 1, 2))

        self.slice.end_position = (3, 5, 7)
        self.assertAllClose(self.slice.end_position, (3, 5, 7))

        self.slice.end_position.i = 2
        self.slice.end_position.j = 3
        self.slice.end_position.k = 4
        self.assertEqual(self.slice.end_position.i, 2)
        self.assertEqual(self.slice.end_position.j, 3)
        self.assertEqual(self.slice.end_position.k, 4)

        self.slice.orientation = SliceSurface.Arbitrary
        self.slice.end_position = (0, 1, 2)
        self.assertAllClose(self.slice.end_position, (0, 1, 2))

        self.slice.end_position = (3, 5, 7)
        self.assertAllClose(self.slice.end_position, (3, 5, 7))

        self.slice.end_position.x = 2
        self.slice.end_position.y = 3
        self.slice.end_position.z = 4
        self.assertAlmostEqual(self.slice.end_position.x, 2)
        self.assertAlmostEqual(self.slice.end_position.y, 3)
        self.assertAlmostEqual(self.slice.end_position.z, 4)

    @skip_if_sdk_version_before(2018, 1)
    def test_surface_generation_method(self):
        if __debug__:
            with mocked_sdk_version(2017, 2):
                with self.assertRaises(TecplotOutOfDateEngineError):
                    self.slice.surface_generation_method = \
                        SurfaceGenerationMethod.AllPolygons

                for val in [SurfaceGenerationMethod.AllowQuads,
                            SurfaceGenerationMethod.AllTriangles]:
                    self.slice.surface_generation_method = val
                    self.assertEqual(self.slice.surface_generation_method, val)

        for val in SurfaceGenerationMethod:
            self.slice.surface_generation_method = val
            self.assertEqual(self.slice.surface_generation_method, val)

    def test_ijk_position(self):
        for slice_surface in (SliceSurface.IPlanes,
                              SliceSurface.JPlanes,
                              SliceSurface.KPlanes):

            self.slice.orientation = slice_surface
            self.slice.origin = (1, 2, 3)
            self.assertEqual(self.slice.origin.i, 1)
            self.assertEqual(self.slice.origin.j, 2)
            self.assertEqual(self.slice.origin.k, 3)

            if __debug__:
                for bad_attribute in ('x', 'y', 'z'):
                    with self.assertRaises(AttributeError):
                        getattr(self.slice.origin, bad_attribute)

            self.slice.origin += (1, 1, 1)
            self.assertEqual(self.slice.origin, (2, 3, 4))

            self.slice.origin -= (1, 1, 1)
            self.assertEqual(self.slice.origin, (1, 2, 3))

            with self.assertRaises(TecplotSystemError):
                self.slice.origin = -self.slice.origin

            slice_1 = self.plot.slice(1)  # type: SliceGroup
            slice_1.orientation = slice_surface
            slice_1.origin = (1, 2, 3)
            self.slice.origin = slice_1.origin
            self.assertEqual(self.slice.origin.i, 1)
            self.assertEqual(self.slice.origin.j, 2)
            self.assertEqual(self.slice.origin.k, 3)

            self.slice.origin += slice_1.origin
            self.assertEqual(self.slice.origin, (2, 4, 6))

            self.slice.origin -= slice_1.origin
            self.assertEqual(self.slice.origin, (1, 2, 3))

            self.slice.origin[0] = 1
            self.assertEqual(self.slice.origin.i, 1)

            with self.assertRaises(IndexError):
                self.slice.origin[4]

            self.slice.origin = (0, 1, 2)
            self.assertEqual('(0, 1, 2)', str(self.slice.origin))

            with self.assertRaises(TypeError):
                self.slice.origin = 1

            with self.assertRaises(TypeError):
                self.slice.origin += 2

    def test_xyz_position(self):
        for slice_surface in (SliceSurface.XPlanes,
                              SliceSurface.YPlanes,
                              SliceSurface.ZPlanes):

            self.slice.orientation = slice_surface
            self.slice.origin = (1.1, 2, 3)
            self.assertEqual(self.slice.origin.x, 1.1)
            self.assertEqual(self.slice.origin.y, 2.0)
            self.assertEqual(self.slice.origin.z, 3.0)

            if __debug__:
                for bad_attribute in ('i', 'j', 'k'):
                    with self.assertRaises(AttributeError):
                        getattr(self.slice.origin, bad_attribute)

            self.slice.origin += (1, 2, 3)
            self.assertEqual(self.slice.origin, (2.1, 4.0, 6.0))

            self.slice.origin -= (1, 2, 3)
            self.assertEqual(self.slice.origin, (1.1, 2.0, 3.0))

            self.slice.origin = -self.slice.origin
            self.assertEqual(self.slice.origin, (-1.1, -2.0, -3.0))

            slice_1 = self.plot.slice(1)  # type: SliceGroup
            slice_1.orientation = slice_surface
            slice_1.origin = (1.1, 2, 3)
            self.slice.origin = slice_1.origin
            self.assertEqual(self.slice.origin.x, 1.1)
            self.assertEqual(self.slice.origin.y, 2.0)
            self.assertEqual(self.slice.origin.z, 3.0)

            self.slice.origin += slice_1.origin
            self.assertEqual(self.slice.origin, (2.2, 4, 6))

            self.slice.origin -= slice_1.origin
            self.assertEqual(self.slice.origin, (1.1, 2.0, 3.0))

            self.slice.origin = -self.slice.origin
            self.assertEqual(self.slice.origin, (-1.1, -2.0, -3.0))

            with self.assertRaises(TypeError):
                self.slice.origin = 1

            with self.assertRaises(TypeError):
                self.slice.origin += 2

    def test_num_intermediate_slices(self):
        for val in [1, 2]:
            self.slice.num_intermediate_slices = val
            self.assertEqual(self.slice.num_intermediate_slices, val)

    def test_show_intermediate_slices(self):
        for val in [True, False, True]:
            self.slice.show_intermediate_slices = val
            self.assertEqual(self.slice.show_intermediate_slices, val)

    def test_obey_source_zone_blanking(self):
        for val in [True, False, True]:
            self.slice.obey_source_zone_blanking = val
            self.assertEqual(self.slice.obey_source_zone_blanking, val)

    def test_slice_source(self):
        for val in [SliceSource.LinearZones, SliceSource.SurfaceZones]:
            self.slice.slice_source = val
            self.assertEqual(self.slice.slice_source, val)

    def test_show_start_and_end_slices(self):
        for val in [True, False, True]:
            self.slice.show_start_and_end_slices = val
            self.assertEqual(self.slice.show_start_and_end_slices, val)

    def test_use_slice_clipping(self):
        for val in [True, False, True]:
            self.slice.use_slice_clipping = val
            self.assertEqual(self.slice.use_slice_clipping, val)
        with assert_style(True, sv.SLICEATTRIBUTES, sv.OBEYCLIPPLANES,
                          OFFSET1=self.slice.index, **self.slice._style_attrs):
            self.slice.use_slice_clipping = True
            _ = self.slice.use_slice_clipping

    def test_clip(self):
        for val in [ClipPlane.AbovePrimarySlice,
                    ClipPlane.BelowPrimarySlice,
                    ClipPlane.None_]:
            self.slice.clip = val
            self.assertEqual(self.slice.clip, val)
        with self.assertRaises(ValueError):
            self.slice.clip = 0.5


class TestExtractTransientJournalValidity(unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        self.filename, self.dataset = sample_data.sample_data('2x2x3_overlap')
        frame = tp.active_frame()
        self.frame = frame

        frame.plot_type = PlotType.Cartesian3D
        self.plot = frame.plot()
        self.slice = self.plot.slice(0)

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    @skip_if_sdk_version_before(2019, 1)
    def test_extract_transient(self):
        self.dataset.zone(0).strand = 1
        self.dataset.zone(0).solution_time = 1.0
        self.dataset.zone(1).strand = 1
        self.dataset.zone(1).solution_time = 2.0
        self.plot.active_fieldmap_indices = [0, 1]
        self.plot.solution_time = 1.0

        z = self.slice.extract(
            transient_mode=TransientOperationMode.AllSolutionTimes)

        self.assertTrue(tp.tecutil._tecutil.DataSetJournalIsValid())


if __name__ == '__main__':
    from .. import main
    main()
