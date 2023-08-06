from builtins import int

import os, unittest

from unittest.mock import patch, Mock, ANY

import tecplot as tp
from tecplot.constant import *
from tecplot.exception import *
from tecplot.tecutil import sv

from .. import assert_style, sample_data


class TestLinkingBetweenFrames(unittest.TestCase):
    def setUp(self):
        plot = tp.active_frame().plot(PlotType.Sketch)
        self.linking = plot.linking_between_frames

    def test_group(self):
        for i in range(1, 33):
            self.linking.group = i
            self.assertEqual(self.linking.group, i)
        with self.assertRaises((TecplotSystemError, TecplotLogicError)):
            self.linking.group = -1
        with self.assertRaises((TecplotSystemError, TecplotLogicError)):
            self.linking.group = 0
        with self.assertRaises((TecplotSystemError, TecplotLogicError)):
            self.linking.group = 33

        with assert_style(int(1), sv.LINKING, sv.BETWEENFRAMES,
                          sv.LINKGROUP, UNIQUEID=ANY):
            _ = self.linking.group
            self.linking.group = int(1)

    def test_link_frame_size_and_position(self):
        for val in [True, False, True]:
            self.linking.link_frame_size_and_position = val
            self.assertEqual(self.linking.link_frame_size_and_position, val)

        with assert_style(True, sv.LINKING, sv.BETWEENFRAMES,
                          sv.LINKFRAMESIZEANDPOSITION, UNIQUEID=ANY):
            _ = self.linking.link_frame_size_and_position
            self.linking.link_frame_size_and_position = True

    def test_link_solution_time(self):
        for val in [True, False, True]:
            self.linking.link_solution_time = val
            self.assertEqual(self.linking.link_solution_time, val)

        with assert_style(True, sv.LINKING, sv.BETWEENFRAMES,
                          sv.LINKSOLUTIONTIME, UNIQUEID=ANY):
            _ = self.linking.link_solution_time
            self.linking.link_solution_time = True


class TestDataPlotLinkingBetweenFrames:
    def test_link_value_blanking(self):
        for val in [True, False, True]:
            self.linking.link_value_blanking = val
            self.assertEqual(self.linking.link_value_blanking, val)

        with assert_style(True, sv.LINKING, sv.BETWEENFRAMES,
                          sv.LINKVALUEBLANKING, UNIQUEID=ANY):
            _ = self.linking.link_value_blanking
            self.linking.link_value_blanking = True


class TestPlot2DLinkingBetweenFrames(TestDataPlotLinkingBetweenFrames,
                                     TestLinkingBetweenFrames):
    def setUp(self):
        self.ftmp, dataset = sample_data.sample_data('xylines_poly')
        plot = tp.active_frame().plot(PlotType.XYLine)
        plot.activate()
        self.linking = plot.linking_between_frames

    def tearDown(self):
        tp.new_layout()
        os.remove(self.ftmp)

    def test_link_x_axis_range(self):
        for val in [True, False, True]:
            self.linking.link_x_axis_range = val
            self.assertEqual(self.linking.link_x_axis_range, val)

        with assert_style(True, sv.LINKING, sv.BETWEENFRAMES,
                          sv.LINKXAXISRANGE, UNIQUEID=ANY):
            _ = self.linking.link_x_axis_range
            self.linking.link_x_axis_range = True

    def test_link_y_axis_range(self):
        for val in [True, False, True]:
            self.linking.link_y_axis_range = val
            self.assertEqual(self.linking.link_y_axis_range, val)

        with assert_style(True, sv.LINKING, sv.BETWEENFRAMES,
                          sv.LINKYAXISRANGE, UNIQUEID=ANY):
            _ = self.linking.link_y_axis_range
            self.linking.link_y_axis_range = True

    def test_link_axis_position(self):
        for val in [True, False, True]:
            self.linking.link_axis_position = val
            self.assertEqual(self.linking.link_axis_position, val)

        with assert_style(True, sv.LINKING, sv.BETWEENFRAMES,
                          sv.LINKAXISPOSITION, UNIQUEID=ANY):
            _ = self.linking.link_axis_position
            self.linking.link_axis_position = True


class TestFieldPlotLinkingBetweenFrames:
    def test_link_contour_levels(self):
        for val in [True, False, True]:
            self.linking.link_contour_levels = val
            self.assertEqual(self.linking.link_contour_levels, val)

        with assert_style(True, sv.LINKING, sv.BETWEENFRAMES,
                          sv.LINKCONTOURLEVELS, UNIQUEID=ANY):
            _ = self.linking.link_contour_levels
            self.linking.link_contour_levels = True


class TestCartesian2DPlotLinkingBetweenFrames(TestFieldPlotLinkingBetweenFrames,
                                              TestPlot2DLinkingBetweenFrames):
    def setUp(self):
        self.ftmp, dataset = sample_data.sample_data('3x3x3_p')
        plot = tp.active_frame().plot(PlotType.Cartesian2D)
        plot.activate()
        self.linking = plot.linking_between_frames

    def tearDown(self):
        tp.new_layout()
        os.remove(self.ftmp)


class TestCartesian3DPlotLinkingBetweenFrames(TestFieldPlotLinkingBetweenFrames,
                                              TestDataPlotLinkingBetweenFrames,
                                              TestLinkingBetweenFrames):
    def setUp(self):
        self.ftmp, dataset = sample_data.sample_data('3x3x3_p')
        plot = tp.active_frame().plot(PlotType.Cartesian3D)
        plot.activate()
        self.linking = plot.linking_between_frames

    def tearDown(self):
        tp.new_layout()
        os.remove(self.ftmp)

    def test_link_view(self):
        for val in [True, False, True]:
            self.linking.link_view = val
            self.assertEqual(self.linking.link_view, val)

        with assert_style(True, sv.LINKING, sv.BETWEENFRAMES,
                          sv.LINK3DVIEW, UNIQUEID=ANY):
            _ = self.linking.link_view
            self.linking.link_view = True

    def test_link_slice_positions(self):
        for val in [True, False, True]:
            self.linking.link_slice_positions = val
            self.assertEqual(self.linking.link_slice_positions, val)

        with assert_style(True, sv.LINKING, sv.BETWEENFRAMES,
                          sv.LINKSLICEPOSITIONS, UNIQUEID=ANY):
            _ = self.linking.link_slice_positions
            self.linking.link_slice_positions = True

    def test_link_isosurface_values(self):
        for val in [True, False, True]:
            self.linking.link_isosurface_values = val
            self.assertEqual(self.linking.link_isosurface_values, val)

        with assert_style(True, sv.LINKING, sv.BETWEENFRAMES,
                          sv.LINKISOSURFACEVALUES, UNIQUEID=ANY):
            _ = self.linking.link_isosurface_values
            self.linking.link_isosurface_values = True


class TestPolarPlotLinkingBetweenFrames(TestDataPlotLinkingBetweenFrames,
                                        TestLinkingBetweenFrames):
    def setUp(self):
        self.ftmp, dataset = sample_data.sample_data('xylines_poly')
        plot = tp.active_frame().plot(PlotType.PolarLine)
        plot.activate()
        self.linking = plot.linking_between_frames

    def tearDown(self):
        tp.new_layout()
        os.remove(self.ftmp)

    def test_link_view(self):
        for val in [True, False, True]:
            self.linking.link_view = val
            self.assertEqual(self.linking.link_view, val)

        with assert_style(True, sv.LINKING, sv.BETWEENFRAMES,
                          sv.LINKPOLARVIEW, UNIQUEID=ANY):
            _ = self.linking.link_view
            self.linking.link_view = True


class TestLinkingWithinFrame(unittest.TestCase):
    def setUp(self):
        plot = tp.active_frame().plot(PlotType.Sketch)
        self.linkings = [plot.linking_within_frame]

    def test_link_axis_style(self):
        for linking in self.linkings:
            for val in [True, False, True]:
                linking.link_axis_style = val
                self.assertEqual(linking.link_axis_style, val)

            with assert_style(True, sv.LINKING, sv.WITHINFRAME,
                              sv.LINKAXISSTYLE, UNIQUEID=ANY):
                _ = linking.link_axis_style
                linking.link_axis_style = True


    def test_link_gridline_style(self):
        for linking in self.linkings:
            for val in [True, False, True]:
                linking.link_gridline_style = val
                self.assertEqual(linking.link_gridline_style, val)

            with assert_style(True, sv.LINKING, sv.WITHINFRAME,
                              sv.LINKGRIDLINESTYLE, UNIQUEID=ANY):
                _ = linking.link_gridline_style
                linking.link_gridline_style = True


class TestDataPlotLinkingWithinFrame(TestLinkingWithinFrame):
    def setUp(self):
        xyplot = tp.active_frame().plot(PlotType.XYLine)
        polarplot = tp.active_frame().plot(PlotType.PolarLine)
        self.linkings = (xyplot.linking_within_frame,
                        polarplot.linking_within_frame)

    def test_link_layer_line_color(self):
        for linking in self.linkings:
            for val in [True, False, True]:
                linking.link_layer_line_color = val
                self.assertEqual(linking.link_layer_line_color, val)

            with assert_style(True, sv.LINKING, sv.WITHINFRAME,
                              sv.LINKLAYERLINECOLOR, UNIQUEID=ANY):
                _ = linking.link_layer_line_color
                linking.link_layer_line_color = True


class TestFieldPlotLinkingWithinFrame(TestDataPlotLinkingWithinFrame):
    def setUp(self):
        plot2d = tp.active_frame().plot(PlotType.Cartesian2D)
        plot3d = tp.active_frame().plot(PlotType.Cartesian3D)
        self.linkings = (plot2d.linking_within_frame,
                         plot3d.linking_within_frame)

    def test_link_layer_line_pattern(self):
        for linking in self.linkings:
            for val in [True, False, True]:
                linking.link_layer_line_pattern = val
                self.assertEqual(linking.link_layer_line_pattern, val)

            with assert_style(True, sv.LINKING, sv.WITHINFRAME,
                              sv.LINKLAYERLINEPATTERN, UNIQUEID=ANY):
                _ = linking.link_layer_line_pattern
                linking.link_layer_line_pattern = True



if __name__ == '__main__':
    from .. import main
    main()

