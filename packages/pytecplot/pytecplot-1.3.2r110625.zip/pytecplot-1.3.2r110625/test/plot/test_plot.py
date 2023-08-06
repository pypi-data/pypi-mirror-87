import numpy as np
import os
import platform
import random
import re
import sys
import unittest
import warnings

from os import path
from unittest.mock import patch, Mock, PropertyMock

from test import patch_tecutil

import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *
from tecplot.data.operate import execute_equation
from tecplot import text
from tecplot.plot import *
from tecplot.legend import ContourLegend, LineLegend
from tecplot.session import IndexRange

from test import skip_if_sdk_version_before
from ..sample_data import sample_data


class TestPlot(unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        self.filename,dataset = sample_data('10x10x10')

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    def test_eq(self):
        fr0 = tp.active_frame()
        fr1 = tp.active_page().add_frame()
        self.assertNotEqual(fr0, fr1)
        self.assertTrue(fr0.plot(PlotType.Sketch) != fr1.plot(PlotType.Sketch))
        self.assertTrue(fr0.plot(PlotType.Sketch) != fr0.plot(PlotType.Cartesian3D))
        self.assertTrue(fr0.plot(PlotType.Sketch) == fr0.plot(PlotType.Sketch))
        self.assertTrue(fr0.plot(PlotType.Sketch) == fr0.plot(PlotType.Sketch))

    def test_activated(self):
        fr0 = tp.active_frame()
        fr0.plot_type = PlotType.Cartesian2D
        plot3d = fr0.plot(PlotType.Cartesian3D)
        self.assertEqual(fr0.plot_type, PlotType.Cartesian2D)
        with plot3d.activated():
            self.assertEqual(fr0.plot_type,  PlotType.Cartesian3D)
        self.assertEqual(fr0.plot_type, PlotType.Cartesian2D)

        fr1 = tp.active_page().add_frame()
        fr1.plot_type = PlotType.XYLine
        self.assertTrue(fr1.active)
        self.assertEqual(fr1.plot_type, PlotType.XYLine)
        with plot3d.activated():
            self.assertEqual(tp.active_frame(), fr0)
            self.assertEqual(fr0.plot_type, PlotType.Cartesian3D)
        self.assertTrue(fr1.active)
        self.assertEqual(fr1.plot_type, PlotType.XYLine)


class TestSketchPlot(unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        self.filename,dataset = sample_data('10x10x10')
        self.frame = tp.active_frame()
        self.sketch_plot = self.frame.plot(PlotType.Sketch)

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    def test_activate(self):
        self.frame.plot_type = PlotType.Cartesian3D
        self.sketch_plot.activate()
        self.assertEqual(self.frame.plot_type, PlotType.Sketch)

    def test_axes(self):
        self.assertIsInstance(self.sketch_plot.axes, SketchAxes)

    def test_linking(self):
        self.assertIsInstance(self.sketch_plot.linking_between_frames,
            linking.SketchPlotLinkingBetweenFrames)
        self.assertIsInstance(self.sketch_plot.linking_within_frame,
            linking.LinkingWithinFrame)


class TestFieldPlot(unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        self.filename,self.dataset = sample_data('2x2x3_overlap')
        frame = tp.active_frame()
        self.plot2d = frame.plot(PlotType.Cartesian2D)
        self.plot3d = frame.plot(PlotType.Cartesian3D)
        self.plot3d.vector.u_variable_index = 0
        self.plot3d.vector.v_variable_index = 1
        self.plot3d.vector.w_variable_index = 2

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    def test_contour(self):
        self.assertIsInstance(self.plot2d.contour(0), ContourGroup)
        self.assertIsInstance(self.plot3d.contour(1), ContourGroup)

    def test_data_labels(self):
        self.assertIsInstance(self.plot2d.data_labels, labels.FieldPlotDataLabels)
        self.assertIsInstance(self.plot3d.data_labels, labels.FieldPlotDataLabels)

    def test_rgb_coloring(self):
        self.assertIsInstance(self.plot2d.rgb_coloring, RGBColoring)
        self.assertIsInstance(self.plot3d.rgb_coloring, RGBColoring)

    def test_scatter(self):
        self.assertIsInstance(self.plot2d.scatter, Scatter)
        self.assertIsInstance(self.plot3d.scatter, Scatter)

    def test_slice(self):
        with self.assertRaises(TecplotInterfaceChangeError):
            self.assertIsInstance(self.plot2d.slice(0), SliceGroup)
            self.assertIsInstance(self.plot2d.slices(), SliceGroupCollection)
        self.assertIsInstance(self.plot3d.slice(0), SliceGroup)
        self.assertIsInstance(self.plot3d.slices(), SliceGroupCollection)
        slices = self.plot3d.slices()
        self.assertEqual(slices._indices, set(range(8)))
        slices = self.plot3d.slices(0, 1)
        self.assertEqual(slices._indices, set([0, 1]))

    def test_isosurface(self):
        with self.assertRaises(TecplotInterfaceChangeError):
            self.assertIsInstance(self.plot2d.isosurface(0), IsosurfaceGroup)
        self.assertIsInstance(self.plot3d.isosurface(0), IsosurfaceGroup)

    def test_streamtraces(self):
        self.assertIsInstance(self.plot2d.streamtraces, Streamtraces)
        self.assertIsInstance(self.plot3d.streamtraces, Streamtraces)

    def test_show_contour(self):
        for val in [True,False,True]:
            for plot in [self.plot2d,self.plot3d]:
                plot.show_contour = val
                self.assertEqual(plot.show_contour,val)

    def test_show_edge(self):
        for val in [True,False,True]:
            for plot in [self.plot2d,self.plot3d]:
                plot.show_edge = val
                self.assertEqual(plot.show_edge,val)

    def test_show_mesh(self):
        for val in [True,False,True]:
            for plot in [self.plot2d,self.plot3d]:
                plot.show_mesh = val
                self.assertEqual(plot.show_mesh,val)

    def test_show_scatter(self):
        for val in [True,False,True]:
            for plot in [self.plot2d,self.plot3d]:
                plot.show_scatter = val
                self.assertEqual(plot.show_scatter,val)

    def test_show_shade(self):
        for val in [True,False,True]:
            for plot in [self.plot2d,self.plot3d]:
                plot.show_shade = val
                self.assertEqual(plot.show_shade,val)

    def test_show_streamtraces(self):
        for val in [True,False,True]:
            for plot in [self.plot2d,self.plot3d]:
                plot.show_streamtraces = val
                self.assertEqual(plot.show_streamtraces,val)

    def test_show_slices(self):
        for val in [True, False, True]:
            for current_plot in [self.plot2d, self.plot3d]:
                current_plot.show_slices = val
                self.assertEqual(current_plot.show_slices, val)

    def test_show_isosurfaces(self):
        for val in [True, False, True]:
            for current_plot in [self.plot2d, self.plot3d]:
                current_plot.show_isosurfaces = val
                self.assertEqual(current_plot.show_isosurfaces, val)

    def test_show_vector(self):
        for val in [True,False,True]:
            for plot in [self.plot2d,self.plot3d]:
                plot.show_vector = val
                self.assertEqual(plot.show_vector,val)

    def test_num_fieldmaps(self):
        self.assertEqual(self.plot2d.num_fieldmaps, 2)
        self.assertEqual(self.plot3d.num_fieldmaps, 2)

    def test_fieldmaps(self):
        self.assertEqual(len(list(self.plot2d.fieldmaps())), 2)
        self.assertEqual(len(list(self.plot3d.fieldmaps())), 2)

        self.assertEqual(len(list(self.plot2d.fieldmaps(0, self.dataset.zone(1)))), 2)
        self.assertEqual(len(list(self.plot3d.fieldmaps(1))), 1)
        self.assertEqual(len(list(self.plot3d.fieldmaps(self.dataset.zone(1)))), 1)

        self.assertIsInstance(self.plot2d.fieldmaps(), Cartesian2DFieldmapCollection)
        self.assertIsInstance(self.plot3d.fieldmaps(), Cartesian3DFieldmapCollection)

        for fmap in self.plot3d.fieldmaps():
            self.assertIsInstance(fmap, Cartesian3DFieldmap)
        for fmap in self.plot2d.fieldmaps():
            self.assertIsInstance(fmap, Cartesian2DFieldmap)

        indices = self.plot3d._fieldmap_indices(self.plot3d.fieldmaps())
        self.assertEqual(indices, set(range(self.plot3d.num_fieldmaps)))

    def test_active_fieldmap_indices(self):
        self.assertEqual(self.plot2d.active_fieldmap_indices, {0,1})
        self.assertEqual(self.plot3d.active_fieldmap_indices, {0,1})

    def test_active_fieldmaps(self):
        self.assertIsInstance(self.plot2d.active_fieldmaps, Cartesian2DFieldmapCollection)
        self.assertIsInstance(self.plot3d.active_fieldmaps, Cartesian3DFieldmapCollection)

        self.plot2d.active_fieldmaps = [0, 1]
        self.plot2d.active_fieldmaps = self.plot2d.fieldmaps()
        self.assertEqual(len(self.plot2d.active_fieldmaps.fieldmap_indices), 2)
        self.plot2d.active_fieldmaps -= [0]
        self.assertEqual(len(self.plot2d.active_fieldmaps.fieldmap_indices), 1)
        self.plot2d.active_fieldmaps += [0]
        self.assertEqual(len(self.plot2d.active_fieldmaps.fieldmap_indices), 2)
        self.plot2d.active_fieldmaps = [1]
        self.assertEqual(len(self.plot2d.active_fieldmaps.fieldmap_indices), 1)

        self.plot3d.active_fieldmaps = [0, 1]
        self.plot3d.active_fieldmaps = self.plot3d.fieldmaps()
        self.assertEqual(len(self.plot3d.active_fieldmaps.fieldmap_indices), 2)
        self.plot3d.active_fieldmaps += [0]
        self.assertEqual(len(self.plot3d.active_fieldmaps.fieldmap_indices), 2)
        self.plot3d.active_fieldmaps -= [0]
        self.assertEqual(len(self.plot3d.active_fieldmaps.fieldmap_indices), 1)
        self.plot3d.active_fieldmaps = [1]
        self.assertEqual(len(self.plot3d.active_fieldmaps.fieldmap_indices), 1)

        self.plot3d.active_fieldmaps = []
        self.assertEqual(len(self.plot3d.active_fieldmaps.fieldmap_indices), 0)
        self.plot3d.active_fieldmaps = self.plot3d.fieldmaps()
        self.assertEqual(len(self.plot3d.active_fieldmaps.fieldmap_indices),
                         self.plot3d.num_fieldmaps)

        self.plot3d.active_fieldmaps = []
        self.assertEqual(len(self.plot3d.active_fieldmaps.fieldmap_indices), 0)
        self.plot3d.active_fieldmaps = list(self.plot3d.fieldmaps())
        self.assertEqual(len(self.plot3d.active_fieldmaps.fieldmap_indices),
                         self.plot3d.num_fieldmaps)

        for fmap in self.plot3d.active_fieldmaps:
            self.assertIsInstance(fmap, Cartesian3DFieldmap)
        for fmap in self.plot2d.active_fieldmaps:
            self.assertIsInstance(fmap, Cartesian2DFieldmap)

    def test_fieldmap_index(self):
        self.assertEqual(self.plot2d.fieldmap_index(self.dataset.zone(0)), 0)
        self.assertEqual(self.plot2d.fieldmap_index(self.dataset.zone(1)), 1)
        self.assertEqual(self.plot3d.fieldmap_index(self.dataset.zone(0)), 0)
        self.assertEqual(self.plot3d.fieldmap_index(self.dataset.zone(1)), 1)

    @skip_if_sdk_version_before(2017, 2)
    def test_solution_times(self):
        self.assertEqual(self.plot3d.solution_time, 0)
        self.assertEqual(self.plot3d.num_solution_times, 0)
        self.assertEqual(self.plot3d.solution_times, [])

        for z in self.dataset.zones():
            z.strand = 1
            z.solution_time = 1

        # strand and solution set, but fieldmap not active yet
        self.assertEqual(self.plot3d.solution_time, 0)
        self.assertEqual(self.plot3d.num_solution_times, 0)
        self.assertEqual(self.plot3d.solution_times, [])

        # activate the fieldmap
        self.plot3d.active_fieldmaps += [0]

        # solution time will have been set to 1 by GUI/360
        self.plot3d.solution_time = 1.0

        self.assertAlmostEqual(self.plot3d.solution_time, 1)
        self.assertEqual(self.plot3d.num_solution_times, 1)
        self.assertEqual(self.plot3d.solution_times, [1])

        self.dataset.zone(1).solution_time = 2

        self.assertEqual(self.plot3d.num_solution_times, 2)
        self.assertEqual(self.plot3d.solution_times, [1,2])

        self.assertEqual(self.plot3d.solution_time, 1)
        self.assertEqual(self.plot3d.solution_timestep, 0)
        self.plot3d.solution_timestep += 1
        self.assertEqual(self.plot3d.solution_time, 2)
        self.assertEqual(self.plot3d.solution_timestep, 1)

        self.plot3d.solution_timestep = -2
        self.assertEqual(self.plot3d.solution_time, 1)
        self.assertEqual(self.plot3d.solution_timestep, 0)

        self.plot3d.solution_timestep = -1
        self.assertEqual(self.plot3d.solution_time, 2)
        self.assertEqual(self.plot3d.solution_timestep, 1)

        # ensure no dealloc call when connected
        with patch_tecutil('SolutionTimeGetSolutionTimesForFrame',
                           return_value=(True,None,[])):
            with patch('tecplot.tecutil.tecutil_connector.TecUtilConnector.connected',
                       PropertyMock(return_value=True)):
                with patch_tecutil('ArrayDealloc') as dealloc_fn:
                    _ = self.plot3d.solution_times
                    self.assertEqual(dealloc_fn.call_count, 0)

    @skip_if_sdk_version_before(2017, 3)
    def test_solution_time_failures(self):
        ds = self.dataset
        for t, z in enumerate(ds.zones()):
            z.strand = 1
            z.solution_time = t

        plt = self.plot3d
        plt.active_fieldmaps += [0]

        with patch_tecutil('SolutionTimeGetNumTimeStepsForFrame',
                           return_value=(False,0)):
            with self.assertRaises(TecplotSystemError):
                n = plt.num_solution_times

        with patch_tecutil('SolutionTimeGetSolutionTimesForFrame',
                           return_value=(False,0,0)):
            with patch_tecutil('ArrayDealloc'):
                with self.assertRaises(TecplotSystemError):
                    n = plt.solution_times

        with patch_tecutil('SolutionTimeSetCurrent',
                           return_value=SetValueReturnCode.ValueRangeError):
            with self.assertRaises(TecplotSystemError):
                plt.solution_time = -1.0

        with patch_tecutil('SolutionTimeGetCurrentTimeStepForFrame',
                           return_value=(False, 0.0)):
            with self.assertRaises(TecplotSystemError):
                x = plt.solution_timestep

        with patch_tecutil('SolutionTimeGetSolutionTimeAtTimeStepForFrame',
                           return_value=(False, 0.0)):
            with self.assertRaises(TecplotSystemError):
                plt.solution_timestep = 2

    def test_out_of_date_sdk(self):
        if __debug__:
            oldver = tp.tecutil.tecutil_connector.SDKVersion(0,0,0,0)
            sdkver = tp.version.sdk_version_info
            try:
                tp.version.sdk_version_info = oldver

                ds = self.dataset
                for t, z in enumerate(ds.zones()):
                    z.strand = 1
                    z.solution_time = t
                plt = self.plot3d
                plt.active_fieldmaps += [0]

                with self.assertRaises(TecplotOutOfDateEngineError):
                    n = plt.num_solution_times
                with self.assertRaises(TecplotOutOfDateEngineError):
                    x = plt.solution_times
                with self.assertRaises(TecplotOutOfDateEngineError):
                    x = plt.solution_time
                with self.assertRaises(TecplotOutOfDateEngineError):
                    plt.solution_time = 0
                with self.assertRaises(TecplotOutOfDateEngineError):
                    x = plt.solution_timestep
                with self.assertRaises(TecplotOutOfDateEngineError):
                    plt.solution_timestep = 0

            finally:
                tp.version.sdk_version_info = sdkver

    def test_ijk_blanking(self):
        self.assertIsInstance(self.plot3d.ijk_blanking, IJKBlanking)
        self.assertIsInstance(self.plot2d.ijk_blanking, IJKBlanking)


class TestCartesian2DFieldPlot(unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        self.filename, self.dataset = sample_data('10x10x10')
        self.frame = tp.active_frame()
        self.frame.plot_type = PlotType.Cartesian2D
        self.plot = self.frame.plot()
        self.plot.vector.u_variable_index = 0
        self.plot.vector.v_variable_index = 1

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    def test_activate(self):
        self.frame.plot_type = PlotType.Sketch
        self.plot.activate()
        self.assertEqual(self.frame.plot_type, PlotType.Cartesian2D)

    def test_axes(self):
        self.assertIsInstance(self.plot.axes, Cartesian2DFieldAxes)

    def test_fieldmap(self):
        self.assertIsInstance(self.plot.fieldmap(0), Cartesian2DFieldmap)
        self.assertIsInstance(self.plot.fieldmap(self.dataset.zone(0)),
                                                 Cartesian2DFieldmap)
        self.assertEqual(self.plot.fieldmap(-1),
                         self.plot.fieldmap(self.dataset.num_zones - 1))

    def test_vector(self):
        self.assertIsInstance(self.plot.vector, Vector2D)

    def test_draw_order(self):
        for val in [TwoDDrawOrder.ByZone, TwoDDrawOrder.ByLayer,
                    TwoDDrawOrder.ByZone]:
            self.plot.draw_order = val
            self.assertEqual(self.plot.draw_order, val)
        with self.assertRaises(ValueError):
            self.plot.draw_order = 0.5

    def test_view(self):
        self.assertIsInstance(self.plot.view, Cartesian2DFieldView)

    def test_value_blanking(self):
        self.assertIsInstance(self.plot.value_blanking, ValueBlankingCartesian2D)

    def test_linking(self):
        self.assertIsInstance(self.plot.linking_between_frames,
            linking.Cartesian2DPlotLinkingBetweenFrames)
        self.assertIsInstance(self.plot.linking_within_frame,
            linking.FieldPlotLinkingWithinFrame)

class TestCartesian3DFieldPlot(unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        self.filename, self.dataset = sample_data('10x10x10')
        self.frame = tp.active_frame()
        self.frame.plot_type = PlotType.Cartesian3D
        self.plot = self.frame.plot()
        self.plot.vector.u_variable_index = 0
        self.plot.vector.v_variable_index = 1
        self.plot.vector.w_variable_index = 1

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    def test_activate(self):
        self.frame.plot_type = PlotType.Sketch
        self.plot.activate()
        self.assertEqual(self.frame.plot_type, PlotType.Cartesian3D)

    def test_slice(self):
        self.assertIsInstance(self.plot.slice(0), SliceGroup)

    def test_isosurface(self):
        self.assertIsInstance(self.plot.isosurface(0), IsosurfaceGroup)

    def test_axes(self):
        self.assertIsInstance(self.plot.axes, Cartesian3DFieldAxes)

    def test_fieldmap(self):
        self.assertIsInstance(self.plot.fieldmap(0), Cartesian3DFieldmap)
        self.assertIsInstance(self.plot.fieldmap(self.dataset.zone(0)),
                                                 Cartesian3DFieldmap)
        self.assertEqual(self.plot.fieldmap(-1),
                         self.plot.fieldmap(self.dataset.num_zones - 1))

    def test_vector(self):
        self.assertIsInstance(self.plot.vector, Vector3D)

    def test_view(self):
        self.assertIsInstance(self.plot.view, Cartesian3DView)

    def test_light_source(self):
        self.assertIsInstance(self.plot.light_source, tp.plot.effects.LightSource)

    def test_use_lighting_effect(self):
        for val in [True,False,True]:
            self.plot.use_lighting_effect = val
            self.assertEqual(self.plot.use_lighting_effect,val)

    def test_use_translucency(self):
        for val in [True,False,True]:
            self.plot.use_translucency = val
            self.assertEqual(self.plot.use_translucency,val)

    def test_value_blanking(self):
        self.assertIsInstance(self.plot.value_blanking, ValueBlankingCartesian3D)

    def test_line_lift_fraction(self):
        for val in [-1, -0.5, 0, 0.5, 1, 100]:
            self.plot.line_lift_fraction = val
            self.assertAlmostEqual(self.plot.line_lift_fraction, val)
        with self.assertRaises((TecplotSystemError, TecplotLogicError)):
            self.plot.line_lift_fraction = 101
        with self.assertRaises(ValueError):
            self.plot.line_lift_fraction = 'badvalue'

    def test_near_plane_fraction(self):
        for val in [0, 0.5, 1, 100]:
            self.plot.near_plane_fraction = val
            self.assertAlmostEqual(self.plot.near_plane_fraction, val)
        with self.assertRaises((TecplotSystemError, TecplotLogicError)):
            self.plot.near_plane_fraction = -1
        with self.assertRaises((TecplotSystemError, TecplotLogicError)):
            self.plot.near_plane_fraction = 101
        with self.assertRaises(ValueError):
            self.plot.near_plane_fraction = 'badvalue'

    def test_perform_extra_sorting(self):
        for val in [True,False,True]:
            self.plot.perform_extra_sorting = val
            self.assertEqual(self.plot.perform_extra_sorting,val)

    def test_symbol_lift_fraction(self):
        for val in [-1, -0.5, 0, 0.5, 1, 100]:
            self.plot.symbol_lift_fraction = val
            self.assertAlmostEqual(self.plot.symbol_lift_fraction, val)
        with self.assertRaises((TecplotSystemError, TecplotLogicError)):
            self.plot.symbol_lift_fraction = 101
        with self.assertRaises(ValueError):
            self.plot.symbol_lift_fraction = 'badvalue'

    def test_vector_lift_fraction(self):
        for val in [-1, -0.5, 0, 0.5, 1, 100]:
            self.plot.vector_lift_fraction = val
            self.assertAlmostEqual(self.plot.vector_lift_fraction, val)
        with self.assertRaises((TecplotSystemError, TecplotLogicError)):
            self.plot.vector_lift_fraction = 101
        with self.assertRaises(ValueError):
            self.plot.vector_lift_fraction = 'badvalue'

    def test_linking(self):
        self.assertIsInstance(self.plot.linking_between_frames,
            linking.Cartesian3DPlotLinkingBetweenFrames)
        self.assertIsInstance(self.plot.linking_within_frame,
            linking.FieldPlotLinkingWithinFrame)


class TestLinePlot(unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        self.filename,self.dataset = sample_data('xylines_poly')
        frame = tp.active_frame()
        self.xyplot = frame.plot(PlotType.XYLine)
        self.polarplot = frame.plot(PlotType.PolarLine)
        warnings.simplefilter('always')

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    def test_add_delete_linemaps(self):
        ds = self.dataset

        self.xyplot.delete_linemaps()
        self.assertEqual(self.xyplot.num_linemaps, 0)
        self.assertEqual(self.polarplot.num_linemaps, 0)

        self.xyplot.add_linemap('lmap1',ds.zone(0),ds.variable(0),ds.variable(1))
        self.assertEqual(self.xyplot.num_linemaps, 1)
        self.assertEqual(self.polarplot.num_linemaps, 1)

        self.xyplot.add_linemap('lmap2',ds.zone(0),ds.variable(1),ds.variable(0))
        self.assertEqual(self.xyplot.num_linemaps, 2)
        self.assertEqual(self.polarplot.num_linemaps, 2)

        self.polarplot.delete_linemaps(0)
        self.assertEqual(self.xyplot.num_linemaps, 1)
        self.assertEqual(self.polarplot.num_linemaps, 1)
        self.assertEqual(self.xyplot.linemap(0).name, 'lmap2')

        self.xyplot.delete_linemaps()
        lmap0 = self.xyplot.add_linemap('lmap0',ds.zone(0),ds.variable(0),
                                        ds.variable(1))
        self.xyplot.add_linemap('lmap1',ds.zone(0),ds.variable(1),
                                ds.variable(0))
        self.xyplot.add_linemap('a',ds.zone(0),ds.variable(1),ds.variable(2))
        self.xyplot.delete_linemaps('lmap*')
        self.assertEqual(self.xyplot.num_linemaps, 1)
        self.assertEqual(self.polarplot.num_linemaps, 1)
        self.assertEqual(self.polarplot.linemap(0).name, 'a')

        self.xyplot.delete_linemaps()
        lmap0 = self.xyplot.add_linemap('lmap0',ds.zone(0),ds.variable(0),
                                        ds.variable(1))
        self.xyplot.add_linemap('lmap1',ds.zone(0),ds.variable(1),
                                ds.variable(0))
        self.xyplot.add_linemap('a',ds.zone(0),ds.variable(1),ds.variable(2))
        self.xyplot.add_linemap('b',ds.zone(0),ds.variable(1),ds.variable(2))
        self.polarplot.delete_linemaps([lmap0, 'a', 3])
        self.assertEqual(self.xyplot.num_linemaps, 1)
        self.assertEqual(self.polarplot.num_linemaps, 1)
        self.assertEqual(self.polarplot.linemap(0).name, 'lmap1')

    def test_add_linemap_failure(self):
        ds = self.dataset
        self.xyplot.frame.plot_type = PlotType.Cartesian2D
        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            self.xyplot.add_linemap('b', ds.zone(0), ds.variable(1),
                                    ds.variable(1))
        self.xyplot.frame.plot_type = PlotType.XYLine
        with patch('tecplot.tecutil.tecutil.TecUtil.LineMapCreate',
                   Mock(return_value=False)):
            with self.assertRaises(TecplotSystemError):
                self.xyplot.add_linemap('b', ds.zone(0), ds.variable(1),
                                        ds.variable(1))

    @skip_if_sdk_version_before(2018, 3)
    def test_add_linemap(self):
        ds = self.dataset
        self.xyplot.delete_linemaps()

        self.xyplot.add_linemap('c', show=None)
        self.assertIsNotNone(self.xyplot.linemap('c'))

        n = len(list(self.xyplot.linemaps()))
        self.xyplot.add_linemap()
        self.assertEqual(len(list(self.xyplot.linemaps())), n + 1)

        self.assertEqual(len(list(self.xyplot.linemaps('*'))), n + 1)
        self.assertEqual(len(list(self.xyplot.linemaps('c'))), 1)

    def test_legend(self):
        self.assertIsInstance(self.xyplot.legend, LineLegend)
        self.assertIsInstance(self.polarplot.legend, LineLegend)

    def test_active_linemaps(self):
        ds = self.dataset
        self.xyplot.delete_linemaps()

        self.xyplot.add_linemap('lmap0',ds.zone(0),ds.variable(0),ds.variable(1))
        self.xyplot.add_linemap('lmap1',ds.zone(0),ds.variable(1),ds.variable(1))
        self.xyplot.add_linemap('lmap2',ds.zone(0),ds.variable(1),ds.variable(0))

        with warnings.catch_warnings(record=True) as w:
            self.xyplot.linemap('X')
            self.assertEqual(len(w), 0)
            self.xyplot.linemap('X?')
            if __debug__:
                self.assertEqual(len(w), 1)
                self.assertEqual(w[-1].category, TecplotPatternMatchWarning)
            else:
                self.assertEqual(len(w), 0)

        self.assertEqual(self.xyplot.active_linemap_indices, {0,1,2})
        for i,lmap in enumerate(self.xyplot.active_linemaps):
            self.assertEqual(self.xyplot.linemap(i), lmap)

        self.xyplot.linemap(1).show = False

        indices = self.xyplot.active_linemap_indices
        self.assertEqual(indices, {0,2})
        for i,lmap in zip(indices, self.xyplot.active_linemaps):
            self.assertEqual(self.xyplot.linemap(i), lmap)

    def test_linemaps(self):
        ds = self.dataset
        self.xyplot.delete_linemaps()
        self.xyplot.add_linemap('aa',ds.zone(0),ds.variable(0),ds.variable(1))
        self.xyplot.add_linemap('AB',ds.zone(0),ds.variable(1),ds.variable(1))
        self.xyplot.add_linemap('bb',ds.zone(0),ds.variable(1),ds.variable(0))
        self.assertEqual(len(list(self.xyplot.linemaps('a*'))), 2)
        self.assertEqual(len(list(self.xyplot.linemaps('b*'))), 1)
        self.assertEqual(len(list(self.xyplot.linemaps('A*'))), 2)
        self.assertEqual(len(list(self.xyplot.linemaps(re.compile('a.*')))), 1)
        self.assertEqual(len(list(self.xyplot.linemaps(re.compile('XX.*')))), 0)

        with patch_tecutil('LineMapGetName', side_effect=TecplotSystemError):
            self.assertEqual(len(list(self.xyplot.linemaps('*'))), 3)

    def test_value_blanking(self):
        self.assertIsInstance(self.xyplot.value_blanking, ValueBlanking)
        self.assertIsInstance(self.polarplot.value_blanking, ValueBlanking)

    def test_base_font(self):
        self.assertIsInstance(self.xyplot.base_font, text.BaseFont)
        self.assertIsInstance(self.polarplot.base_font, text.BaseFont)

    def test_data_labels(self):
        self.assertIsInstance(self.xyplot.data_labels, labels.LinePlotDataLabels)
        self.assertIsInstance(self.polarplot.data_labels, labels.LinePlotDataLabels)


class TestXYLinePlot(unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        self.filename,self.dataset = sample_data('xylines_poly')
        frame = tp.active_frame()
        frame.plot_type = PlotType.XYLine
        self.plot = frame.plot()

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    def test_activate(self):
        self.plot.frame.plot_type = PlotType.Sketch
        self.plot.activate()
        self.assertEqual(self.plot.frame.plot_type, PlotType.XYLine)

    def test_linemap(self):
        ds = self.dataset
        self.plot.delete_linemaps()
        lmap0 = self.plot.add_linemap('lmap0',ds.zone(0),ds.variable(0),ds.variable(1))
        lmap1 = self.plot.add_linemap('lmap1',ds.zone(0),ds.variable(1),ds.variable(1))
        lmap2 = self.plot.add_linemap('lmap2',ds.zone(0),ds.variable(1),ds.variable(0))
        self.assertEqual(lmap0, self.plot.linemap(0))
        self.assertEqual(lmap1, self.plot.linemap('lmap1'))
        with self.assertRaises(TecplotIndexError):
            self.plot.linemap(3)

        self.assertEqual(lmap2, self.plot.linemap(-1))
        self.assertEqual(lmap1, self.plot.linemap(-2))

    def test_axes(self):
        self.assertIsInstance(self.plot.axes, XYLineAxes)

    def test_show_bars(self):
        for val in [True,False,True]:
            self.plot.show_bars = val
            self.assertEqual(self.plot.show_bars,val)

    def test_show_error_bars(self):
        ds = self.dataset
        lmap = self.plot.add_linemap('lmap0',ds.zone(0),ds.variable(0),ds.variable(1))
        lmap.error_bars.variable_index = 0
        for val in [True,False,True]:
            self.plot.show_error_bars = val
            self.assertEqual(self.plot.show_error_bars,val)

    def test_show_lines(self):
        for val in [True,False,True]:
            self.plot.show_lines = val
            self.assertEqual(self.plot.show_lines,val)

    def test_show_symbols(self):
        for val in [True,False,True]:
            self.plot.show_symbols = val
            self.assertEqual(self.plot.show_symbols,val)

    def test_view(self):
        self.assertIsInstance(self.plot.view, XYLineView)

    def test_linking(self):
        self.assertIsInstance(self.plot.linking_between_frames,
            linking.XYLinePlotLinkingBetweenFrames)
        self.assertIsInstance(self.plot.linking_within_frame,
            linking.DataPlotLinkingWithinFrame)


class TestPolarLinePlot(unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        self.filename,self.dataset = sample_data('xylines_poly')
        frame = tp.active_frame()
        frame.plot_type = PlotType.PolarLine
        self.plot = frame.plot()
        warnings.simplefilter('always')

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    def test_activate(self):
        self.plot.frame.plot_type = PlotType.Sketch
        self.plot.activate()
        self.assertEqual(self.plot.frame.plot_type, PlotType.PolarLine)

    def test_active_linemaps(self):
        self.plot.linemaps().show = True
        for i, lmap in enumerate(self.plot.active_linemaps):
            self.assertEqual(self.plot.linemap(i), lmap)

    def test_view(self):
        self.assertIsInstance(self.plot.view, PolarView)

    def test_linemap(self):
        ds = self.dataset
        self.plot.delete_linemaps()
        lmap0 = self.plot.add_linemap('lmap0',ds.zone(0),ds.variable(0),ds.variable(1))
        lmap1 = self.plot.add_linemap('lmap1',ds.zone(0),ds.variable(1),ds.variable(1))
        lmap2 = self.plot.add_linemap('lmap2',ds.zone(0),ds.variable(1),ds.variable(0))
        self.assertEqual(lmap0, self.plot.linemap(0))
        self.assertEqual(lmap1, self.plot.linemap('lmap1'))
        with self.assertRaises(TecplotIndexError):
            self.plot.linemap(self.plot.num_linemaps)
        with warnings.catch_warnings(record=True) as w:
            self.assertIsNone(self.plot.linemap('No Linemap'))
            self.assertEqual(len(w), 0)
            self.assertIsNone(self.plot.linemap('No Linemap?'))
            if __debug__:
                self.assertEqual(len(w), 1)
                self.assertEqual(w[-1].category, TecplotPatternMatchWarning)
            else:
                self.assertEqual(len(w), 0)

        self.assertEqual(lmap2, self.plot.linemap(-1))
        self.assertEqual(lmap1, self.plot.linemap(-2))

    @skip_if_sdk_version_before(2018, 3)
    def test_linemaps(self):
        ds = self.dataset
        self.plot.delete_linemaps()
        self.plot.add_linemap('aa',ds.zone(0),ds.variable(0),ds.variable(1))
        self.plot.add_linemap('AB',ds.zone(0),ds.variable(1),ds.variable(1))
        self.plot.add_linemap('bb',ds.zone(0),ds.variable(1),ds.variable(0))
        self.assertEqual(len(list(self.plot.linemaps('a*'))), 2)
        self.assertEqual(len(list(self.plot.linemaps('b*'))), 1)
        self.assertEqual(len(list(self.plot.linemaps('A*'))), 2)
        self.assertEqual(len(list(self.plot.linemaps(re.compile('a.*')))), 1)
        self.assertEqual(len(list(self.plot.linemaps(re.compile('XX.*')))), 0)

        n = self.plot.num_linemaps
        self.plot.add_linemap()
        self.assertEqual(self.plot.num_linemaps, n + 1)

        with warnings.catch_warnings(record=True) as w:
            self.assertEqual(list(self.plot.linemaps('No Linemap')), [])
            self.assertEqual(len(w), 0)
            self.assertEqual(list(self.plot.linemaps('No Linemap?')), [])
            if __debug__:
                self.assertEqual(len(w), 1)
                self.assertEqual(w[-1].category, TecplotPatternMatchWarning)
            else:
                self.assertEqual(len(w), 0)

    def test_axes(self):
        self.assertIsInstance(self.plot.axes, PolarLineAxes)

    def test_linking(self):
        self.assertIsInstance(self.plot.linking_between_frames,
            linking.PolarPlotLinkingBetweenFrames)
        self.assertIsInstance(self.plot.linking_within_frame,
            linking.DataPlotLinkingWithinFrame)


if __name__ == '__main__':
    from .. import main
    main()
