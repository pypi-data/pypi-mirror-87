from builtins import int, super

from ..exception import *
from ..tecutil import sv
from .. import session


class SketchPlotLinkingBetweenFrames(session.Style):
    """`SketchPlot` `Frame` style linking control.

    .. seealso:: `Cartesian3DPlotLinkingBetweenFrames` for details on how to
        link style across multiple frames.
    """
    def __init__(self, frame):
        self.frame = frame
        super().__init__(sv.LINKING, sv.BETWEENFRAMES, uniqueid=frame.uid)

    @property
    def group(self):
        """`int`: Group number (1-32).

        Each frame may be a member of a single group and may opt in or out of
        linking each specific style to other frames within this group. Once the
        group is set, the frame may opt in and out of specific attributes::

            >>> frame_linking = plot.linking_between_frames
            >>> frame_linking.group = 5
            >>> frame_linking.link_frame_size_and_position = True
            >>> frame_linking.link_solution_time = True
        """
        return self._get_style(int, sv.LINKGROUP)

    @group.setter
    def group(self, value):
        self._set_style(int(value), sv.LINKGROUP)

    @property
    def link_frame_size_and_position(self):
        """`bool`: Match frame geometry.

        Keeps the same geometry across all frames in the specified `group`.
        Example usage::

            >>> frame_linking = plot.linking_between_frames
            >>> frame_linking.group = 1
            >>> frame_linking.link_frame_size_and_position = True
        """
        return self._get_style(bool, sv.LINKFRAMESIZEANDPOSITION)

    @link_frame_size_and_position.setter
    def link_frame_size_and_position(self, value):
        self._set_style(bool(value), sv.LINKFRAMESIZEANDPOSITION)

    @property
    def link_solution_time(self):
        """`bool`: Match current solution time.

        Keeps the same active solution time across all frames in the specified
        `group`. Example usage::

            >>> frame_linking = plot.linking_between_frames
            >>> frame_linking.group = 1
            >>> frame_linking.link_solution_time = True
        """
        return self._get_style(bool, sv.LINKSOLUTIONTIME)

    @link_solution_time.setter
    def link_solution_time(self, value):
        return self._set_style(bool(value), sv.LINKSOLUTIONTIME)


class DataPlotLinkingBetweenFrames(SketchPlotLinkingBetweenFrames):
    @property
    def link_value_blanking(self):
        """`bool`: Match all value blanking style settings.

        Keeps the same value blanking across all frames in the specified
        `group`. Example usage::

            >>> frame_linking = plot.linking_between_frames
            >>> frame_linking.group = 1
            >>> frame_linking.link_value_blanking = True
        """
        return self._get_style(bool, sv.LINKVALUEBLANKING)

    @link_value_blanking.setter
    def link_value_blanking(self, value):
        self._set_style(bool(value), sv.LINKVALUEBLANKING)


class XYLinePlotLinkingBetweenFrames(DataPlotLinkingBetweenFrames):
    """`XYLinePlot` `Frame` style linking control.

    .. seealso:: `Cartesian3DPlotLinkingBetweenFrames` for details on how to
        link style across multiple frames.
    """

    @property
    def link_x_axis_range(self):
        """`bool`: Match x-axis range.

        Keeps the same x-axis range across all frames in the specified `group`.
        Example usage::

            >>> frame_linking = plot.linking_between_frames
            >>> frame_linking.group = 1
            >>> frame_linking.link_x_axis_range = True
        """
        return self._get_style(bool, sv.LINKXAXISRANGE)

    @link_x_axis_range.setter
    def link_x_axis_range(self, value):
        self._set_style(bool(value), sv.LINKXAXISRANGE)

    @property
    def link_y_axis_range(self):
        """`bool`: Match y-axis range.

        Keeps the same y-axis range across all frames in the specified `group`.
        Example usage::

            >>> frame_linking = plot.linking_between_frames
            >>> frame_linking.group = 1
            >>> frame_linking.link_y_axis_range = True
        """
        return self._get_style(bool, sv.LINKYAXISRANGE)

    @link_y_axis_range.setter
    def link_y_axis_range(self, value):
        self._set_style(bool(value), sv.LINKYAXISRANGE)

    @property
    def link_axis_position(self):
        """`bool`: Match axis position within the frames.

        Keeps the same axis position across all frames in the specified
        `group`. Example usage::

            >>> frame_linking = plot.linking_between_frames
            >>> frame_linking.group = 1
            >>> frame_linking.link_axis_position = True
        """
        return self._get_style(bool, sv.LINKAXISPOSITION)

    @link_axis_position.setter
    def link_axis_position(self, value):
        self._set_style(bool(value), sv.LINKAXISPOSITION)


class FieldPlotLinkingBetweenFrames(DataPlotLinkingBetweenFrames):
    @property
    def link_contour_levels(self):
        """`bool`: Match all contour levels.

        Keeps the same contour levels across all frames in the specified
        `group`. Example usage::

            >>> frame_linking = plot.linking_between_frames
            >>> frame_linking.group = 1
            >>> frame_linking.link_contour_levels = True
        """
        return self._get_style(bool, sv.LINKCONTOURLEVELS)

    @link_contour_levels.setter
    def link_contour_levels(self, value):
        self._set_style(bool(value), sv.LINKCONTOURLEVELS)


class Cartesian2DPlotLinkingBetweenFrames(FieldPlotLinkingBetweenFrames,
                                          XYLinePlotLinkingBetweenFrames):
    """`Cartesian2DFieldPlot` `Frame` style linking control.

    .. seealso:: `Cartesian3DPlotLinkingBetweenFrames` for details on how to
        link style across multiple frames.
    """

class Cartesian3DPlotLinkingBetweenFrames(FieldPlotLinkingBetweenFrames):
    """`Cartesian3DFieldPlot` `Frame` style linking control.

    The following example shows how to set up a series of transparent overlay
    frames where each overlay shows one component of the :math:`(U, V, W)`
    vector from the `Dataset`. All four frames are linked to each other (group
    1) so they have the same size, position and view.

    .. code-block:: python
        :emphasize-lines: 36-39,62-65,82-83

        import os

        import tecplot as tp
        from tecplot.constant import *

        examples_dir = tp.session.tecplot_examples_directory()
        infile = os.path.join(examples_dir, 'SimpleData', 'DuctFlow.plt')
        dataset = tp.data.load_tecplot(infile)

        # Create a "blank" (zeroed-out) variable to use when plotting
        # only one component of the (U, V, W) vectors
        tp.data.operate.execute_equation(r'{blank} = 0')

        # Setup the background frame and plot style
        frame = tp.active_frame()
        frame.background_color = Color.Black

        plot = frame.plot(PlotType.Cartesian3D)
        plot.activate()

        contour = plot.contour(0)
        contour.variable = dataset.variable('P(N/m2)')
        contour.legend.show = False

        plot.use_translucency = True
        plot.show_contour = True
        plot.show_edge = True
        plot.axes.orientation_axis.color = Color.White
        plot.view.width = 2.43

        fmap = plot.fieldmap(0)
        fmap.edge.edge_type = EdgeType.Creases
        fmap.edge.color = Color.White
        fmap.surfaces.surfaces_to_plot = SurfacesToPlot.BoundaryFaces

        frame_linking = plot.linking_between_frames
        frame_linking.group = 1
        frame_linking.link_view = True
        frame_linking.link_frame_size_and_position = True

        def add_transparent_overlay(frame):
            '''Creates a transparent frame overlay with "blank" vector variables.'''
            overlay_frame = frame.page.add_frame()
            overlay_frame.transparent = True

            plot = overlay_frame.plot(frame.plot_type)
            plot.activate()
            plot.show_shade = False
            plot.axes.orientation_axis.show = False

            blank_var = overlay_frame.dataset.variable('blank')
            plot.vector.u_variable = blank_var
            plot.vector.v_variable = blank_var
            plot.vector.w_variable = blank_var
            plot.show_vector = True

            fmap = plot.fieldmap(0)
            fmap.vector.line_thickness = 0.35
            fmap.points.step = 80
            fmap.points.points_to_plot = PointsToPlot.AllCellCenters

            frame_linking = plot.linking_between_frames
            frame_linking.group = 1
            frame_linking.link_view = True
            frame_linking.link_frame_size_and_position = True

            return plot

        # Create three overlays - one for each vector component we want to show
        u_plot = add_transparent_overlay(frame)
        u_plot.vector.u_variable = dataset.variable('U(M/S)')
        u_plot.fieldmap(0).vector.color = Color.Red

        v_plot = add_transparent_overlay(frame)
        v_plot.vector.v_variable = dataset.variable('V(M/S)')
        v_plot.fieldmap(0).vector.color = Color.Green

        w_plot = add_transparent_overlay(frame)
        w_plot.vector.w_variable = dataset.variable('W(M/S)')
        w_plot.fieldmap(0).vector.color = Color.Blue

        # Now that all plots have been linked,
        # movement in one will affect all three plots.
        u_plot.view.translate(x=5)

        tp.export.save_png('plot3d_linking_between_frames.png')

    ..  figure:: /_static/images/plot3d_linking_between_frames.png
        :width: 300px
        :figwidth: 300px
    """

    @property
    def link_view(self):
        """`bool`: Match the view orientation and position.

        Keeps the same view across all frames in the specified `group`. Example
        usage::

            >>> frame_linking = plot.linking_between_frames
            >>> frame_linking.group = 1
            >>> frame_linking.link_view = True
        """
        return self._get_style(bool, sv.LINK3DVIEW)

    @link_view.setter
    def link_view(self, value):
        self._set_style(bool(value), sv.LINK3DVIEW)

    @property
    def link_slice_positions(self):
        """`bool`: Match slice positions.

        Keeps the same slice positions across all frames in the specified
        `group`. Example usage::

            >>> frame_linking = plot.linking_between_frames
            >>> frame_linking.group = 1
            >>> frame_linking.link_slice_positions = True
        """
        return self._get_style(bool, sv.LINKSLICEPOSITIONS)

    @link_slice_positions.setter
    def link_slice_positions(self, value):
        self._set_style(bool(value), sv.LINKSLICEPOSITIONS)

    @property
    def link_isosurface_values(self):
        """`bool`: Match isosurface values.

        Keeps the same isosurfaces across all frames in the specified `group`.
        Example usage::

            >>> frame_linking = plot.linking_between_frames
            >>> frame_linking.group = 1
            >>> frame_linking.link_isosurface_values = True
        """
        return self._get_style(bool, sv.LINKISOSURFACEVALUES)

    @link_isosurface_values.setter
    def link_isosurface_values(self, value):
        self._set_style(bool(value), sv.LINKISOSURFACEVALUES)


class PolarPlotLinkingBetweenFrames(DataPlotLinkingBetweenFrames):
    """`PolarLinePlot` `Frame` style linking control.

    .. seealso:: `Cartesian3DPlotLinkingBetweenFrames` for details on how to
        link style across multiple frames.
    """

    @property
    def link_view(self):
        """`bool`: Match polar view settings.

        Keeps the same view across all frames in the specified `group` showing
        a polar plot. Example usage::

            >>> frame_linking = plot.linking_between_frames
            >>> frame_linking.group = 1
            >>> frame_linking.link_view = True
        """
        return self._get_style(bool, sv.LINKPOLARVIEW)

    @link_view.setter
    def link_view(self, value):
        self._set_style(bool(value), sv.LINKPOLARVIEW)


class LinkingWithinFrame(session.Style):
    """`SketchPlot` style linking control within a `Frame`.

    .. seealso:: `FieldPlotLinkingWithinFrame` for details on how to setup
        style linking within a `Frame`.

    .. seealso:: `Cartesian3DPlotLinkingBetweenFrames` for details on how to
        link style across multiple frames.
    """
    def __init__(self, frame):
        self.frame = frame
        super().__init__(sv.LINKING, sv.WITHINFRAME, uniqueid=frame.uid)

    @property
    def link_axis_style(self):
        """`bool`: Match axis style.

        Keeps the same axis style across all axes within the `Frame`.

            >>> frame_linking = plot.linking_within_frame
            >>> frame_linking.link_axis_style = True
        """
        return self._get_style(bool, sv.LINKAXISSTYLE)

    @link_axis_style.setter
    def link_axis_style(self, value):
        self._set_style(bool(value), sv.LINKAXISSTYLE)

    @property
    def link_gridline_style(self):
        """`bool`: Match gridline style.

        Keeps the same style gridlines across all axes within the `Frame`.

            >>> frame_linking = plot.linking_within_frame
            >>> frame_linking.link_gridline_style = True
        """
        return self._get_style(bool, sv.LINKGRIDLINESTYLE)

    @link_gridline_style.setter
    def link_gridline_style(self, value):
        self._set_style(bool(value), sv.LINKGRIDLINESTYLE)


class DataPlotLinkingWithinFrame(LinkingWithinFrame):
    """`XYLinePlot` and `PolarLinePlot` style linking control within a `Frame`.

    .. seealso:: `FieldPlotLinkingWithinFrame` for details on how to setup
        style linking within a `Frame`.

    .. seealso:: `Cartesian3DPlotLinkingBetweenFrames` for details on how to
        link style across multiple frames.
    """

    @property
    def link_layer_line_color(self):
        """`bool`: Match line colors.

        Keeps the same line colors across all layers within the `Frame`.

            >>> frame_linking = plot.linking_within_frame
            >>> frame_linking.link_layer_line_color = True
        """
        return self._get_style(bool, sv.LINKLAYERLINECOLOR)

    @link_layer_line_color.setter
    def link_layer_line_color(self, value):
        self._set_style(bool(value), sv.LINKLAYERLINECOLOR)


class FieldPlotLinkingWithinFrame(DataPlotLinkingWithinFrame):
    """2D and 3D cartesian plot style linking control within a `Frame`.

    .. seealso:: `Cartesian3DPlotLinkingBetweenFrames` for details on how to
        link style across multiple frames.

    .. code-block:: python
        :emphasize-lines: 13-15,20-21

        import os
        import tecplot as tp
        from tecplot.constant import *

        examples_dir = tp.session.tecplot_examples_directory()
        infile = os.path.join(examples_dir, 'SimpleData', 'Sphere.lpk')
        tp.load_layout(infile)

        dataset = tp.active_frame().dataset
        frame = tp.active_frame()
        plot = frame.plot()

        frame_linking = plot.linking_within_frame
        frame_linking.link_gridline_style = True
        frame_linking.link_axis_style = True

        plot.axes.grid_area.fill_color = Color.Mahogany
        plot.axes.grid_area.use_lighting_effect = False

        # With linked axis style, we only need to modify
        # one axis and all others will get the same.
        axis = plot.axes.x_axis
        axis.show = True
        axis.grid_lines.line_thickness = 0.2
        axis.title.color = Color.Green
        axis.ticks.show_on_opposite_edge = True
        axis.minor_grid_lines.show = True
        axis.minor_grid_lines.line_pattern = LinePattern.Dotted
        axis.minor_grid_lines.color = Color.Cyan
        axis.line.line_thickness = 0.2

        plot.view.fit()

        tp.export.save_png('field_plot_link_within_frame.png')

    ..  figure:: /_static/images/field_plot_linking_within_frame.png
        :width: 300px
        :figwidth: 300px
    """

    @property
    def link_layer_line_pattern(self):
        """`bool`: Match line pattern.

        Keeps the same pattern across lines within the `Frame`.

            >>> frame_linking = plot.linking_within_frame
            >>> frame_linking.link_layer_line_pattern = True
        """
        return self._get_style(bool, sv.LINKLAYERLINEPATTERN)

    @link_layer_line_pattern.setter
    def link_layer_line_pattern(self, value):
        self._set_style(bool(value), sv.LINKLAYERLINEPATTERN)
