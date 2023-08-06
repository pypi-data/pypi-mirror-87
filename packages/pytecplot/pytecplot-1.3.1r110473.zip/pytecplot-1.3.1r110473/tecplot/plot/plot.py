from builtins import super, int

import contextlib
import fnmatch
import re
import six
import warnings

from ..tecutil import _tecutil, _tecutil_connector, sv
from ..constant import *
from ..exception import *
from .. import legend, session, tecutil, text, version
from .axes import (Cartesian2DFieldAxes, Cartesian3DFieldAxes, SketchAxes,
                   PolarLineAxes, XYLineAxes)
from .contour import ContourGroup
from .fieldmap import (Cartesian2DFieldmap, Cartesian2DFieldmapCollection,
                       Cartesian3DFieldmap, Cartesian3DFieldmapCollection,
                       FieldmapCollection)
from .isosurface import IsosurfaceGroup
from .streamtrace import StreamtraceRodRibbon, Streamtraces
from .vector import Vector2D, Vector3D
from . import (blanking, effects, labels, linking, linemap,
               rgb_coloring, scatter, slice, view)


class Plot(session.Style):
    def __init__(self, frame, *svargs):
        self.frame = frame
        super().__init__(*svargs, uniqueid=frame.uid)

    def __eq__(self, that):
        return isinstance(that, type(self)) and self.frame == that.frame

    def __ne__(self, that):
        return not (self == that)

    @contextlib.contextmanager
    def activated(self):
        """Context to ensure this plot is active.

        Example usage::

            >>> from tecplot.constant import PlotType
            >>> frame = tecplot.active_frame()
            >>> frame.plot_type = PlotType.XYLine  # set active plot type
            >>> plot = frame.plot(PlotType.Cartesian3D)  # get inactive plot
            >>> print(frame.plot_type)
            PlotType.XYLine
            >>> with plot.activated():
            ...     print(frame.plot_type)  # 3D plot temporarily active
            PlotType.Cartesian3D
            >>> print(frame.plot_type)  # original plot type restored
            PlotType.XYLine
        """
        with self.frame.activated():
            orig_plot = self.frame.plot()
            try:
                self.activate()
                yield self
            finally:
                orig_plot.activate()


class SketchPlot(Plot):
    """A plot space with no data attached.

    .. code-block:: python
        :emphasize-lines: 5,8-9

        import tecplot as tp
        from tecplot.constant import PlotType

        frame = tp.active_frame()
        plot = frame.plot(PlotType.Sketch)

        frame.add_text('Hello, World!', (36, 50), size=34)
        plot.axes.x_axis.show = True
        plot.axes.y_axis.show = True

        tp.export.save_png('plot_sketch.png', 600, supersample=3)

    ..  figure:: /_static/images/plot_sketch.png
        :width: 300px
        :figwidth: 300px
    """

    def activate(self):
        """Make this the active plot type on the parent frame.

        Example usage::

            >>> from tecplot.constant import PlotType
            >>> plot = frame.plot(PlotType.Sketch)
            >>> plot.activate()
        """
        self.frame.plot_type = PlotType.Sketch

    @property
    def axes(self):
        """`SketchAxes`: Axes (x and y) for the sketch plot.

        Example usage::

            >>> from tecplot.constant import PlotType
            >>> frame.plot_type = PlotType.Sketch
            >>> frame.plot().axes.x_axis.show = True
        """
        return SketchAxes(self)

    @property
    def linking_between_frames(self):
        """`SketchPlotLinkingBetweenFrames`: Style linking between frames.

        Example usage::

            >>> plot.linking_between_frames.group = 1
            >>> plot.linking_between_frames.link_solution_time = True
        """
        return linking.SketchPlotLinkingBetweenFrames(self.frame)

    @property
    def linking_within_frame(self):
        """`LinkingWithinFrame`: Style linking within the frame.

        Example usage::

            >>> plot.linking_within_frame.link_gridline_style = True
        """
        return linking.LinkingWithinFrame(self.frame)


class FieldPlot(Plot):
    """Plot containing data associated with style through fieldmaps.

    .. code-block:: python

        from os import path
        import tecplot as tp
        from tecplot.constant import PlotType

        examples_dir = tp.session.tecplot_examples_directory()
        infile = path.join(examples_dir, 'SimpleData', 'F18.plt')
        dataset = tp.data.load_tecplot(infile)

        frame = tp.active_frame()
        plot = frame.plot(PlotType.Cartesian3D)
        plot.activate()
        plot.show_contour = True
        plot.use_translucency = True
        plot.contour(0).variable = dataset.variable('S')

        # ensure consistent output between interactive (connected) and batch
        plot.contour(0).levels.reset_to_nice()

        # save image to file
        tp.export.save_png('plot_field.png', 600, supersample=3)

    ..  figure:: /_static/images/plot_field.png
        :width: 300px
        :figwidth: 300px
    """
    def __init__(self, frame):
        super().__init__(frame, sv.FIELDLAYERS)

    def contour(self, index):
        """`ContourGroup`: Plot-local `ContourGroup` style control.

        Example usage::

            >>> contour = frame.plot().contour(0)
            >>> contour.colormap_name = 'Magma'
        """
        return ContourGroup(index, self)

    @property
    def streamtraces(self):
        """`Streamtraces`: Plot-local `streamtrace <Streamtraces>` attributes.

        Example usage::

            >>> streamtraces = frame.plot().streamtraces
            >>> streamtraces.color = Color.Blue
        """
        return Streamtraces(self)

    def slice(self, index):
        tecutil.api_changed('''\
            Access to 3D slice groups from 2D plots has been removed.
            Use frame.plot(PlotType.Cartesian3D).slice() to access
            slice groups.''', '0.13', '2018 R2')

    def isosurface(self, index):
        tecutil.api_changed('''\
            Access to 3D isosurface groups from 2D plots has been removed.
            Use frame.plot(PlotType.Cartesian3D).isosurface() to access
            isosurface groups.''', '0.13', '2018 R2')

    @property
    def rgb_coloring(self):
        """`RGBColoring`: RGB contour flooding style control.

        Example usage::

            >>> plot.rgb_coloring.red_variable = dataset.variable('gas')
            >>> plot.rgb_coloring.green_variable = dataset.variable('oil')
            >>> plot.rgb_coloring.blue_variable = dataset.variable('water')
            >>> plot.show_contour = True
            >>> plot.fieldmaps().contour.flood_contour_group = plot.rgb_coloring
        """
        return rgb_coloring.RGBColoring(self)

    @property
    def scatter(self):
        """`Scatter`: Plot-local `Scatter` style control.

        Example usage::

            >>> scatter = frame.plot().scatter
            >>> scatter.variable = dataset.variable('P')
        """
        return scatter.Scatter(self)

    @property
    def show_contour(self):
        """`bool`: Enable contours for this plot.

        Example usage::

            >>> frame.plot().show_contour = True
        """
        return self._get_style(bool, sv.SHOWCONTOUR)

    @show_contour.setter
    def show_contour(self, show):
        self._set_style(bool(show), sv.SHOWCONTOUR)

    @property
    def show_edge(self):
        """`bool`: Enable zone edge lines for this plot.

        Example usage::

            >>> frame.plot().show_edge = True
        """
        return self._get_style(bool, sv.SHOWEDGE)

    @show_edge.setter
    def show_edge(self, show):
        self._set_style(bool(show), sv.SHOWEDGE)

    @property
    def show_mesh(self):
        """`bool`: Enable mesh lines for this plot.

        Example usage::

            >>> frame.plot().show_mesh = True
        """
        return self._get_style(bool, sv.SHOWMESH)

    @show_mesh.setter
    def show_mesh(self, show):
        self._set_style(bool(show), sv.SHOWMESH)

    @property
    def show_scatter(self):
        """`bool`: Enable scatter symbols for this plot.

        Example usage::

            >>> frame.plot().show_scatter = True
        """
        return self._get_style(bool, sv.SHOWSCATTER)

    @show_scatter.setter
    def show_scatter(self, show):
        self._set_style(bool(show), sv.SHOWSCATTER)

    @property
    def show_shade(self):
        """`bool`: Enable surface shading effect for this plot.

        Example usage::

            >>> frame.plot().show_shade = True
        """
        return self._get_style(bool, sv.SHOWSHADE)

    @show_shade.setter
    def show_shade(self, show):
        self._set_style(bool(show), sv.SHOWSHADE)

    @property
    def show_slices(self):
        """`bool`: Show slices for this plot.

        Example usage::

            >>> frame.plot().show_slices(True)
        """
        with self.frame.activated():
            return session.get_style(bool, sv.SLICELAYERS, sv.SHOW,
                                     uniqueid=self.frame.uid)

    @show_slices.setter
    def show_slices(self, show):
        with self.frame.activated():
            session.set_style(bool(show), sv.SLICELAYERS, sv.SHOW,
                              uniqueid=self.frame.uid)

    @property
    def show_isosurfaces(self):
        """`bool`: Show isosurfaces for this plot.

        Example usage::

            >>> frame.plot().show_isosurfaces(True)
        """
        with self.frame.activated():
            return session.get_style(bool, sv.ISOSURFACELAYERS, sv.SHOW,
                                     uniqueid=self.frame.uid)

    @show_isosurfaces.setter
    def show_isosurfaces(self, show):
        with self.frame.activated():
            session.set_style(bool(show), sv.ISOSURFACELAYERS, sv.SHOW,
                              uniqueid=self.frame.uid)

    @property
    def show_streamtraces(self):
        """`bool`: Enable drawing `Streamtraces` on this plot.

        Example usage::

            >>> frame.plot().show_streamtraces = True
        """
        with self.frame.activated():
            return session.get_style(bool, sv.STREAMTRACELAYERS, sv.SHOW,
                                     uniqueid=self.frame.uid)

    @show_streamtraces.setter
    def show_streamtraces(self, show):
        with self.frame.activated():
            session.set_style(bool(show), sv.STREAMTRACELAYERS, sv.SHOW,
                              uniqueid=self.frame.uid)

    @property
    def show_vector(self):
        """`bool`: Enable drawing of vectors.

        Example usage::

            >>> frame.plot().show_vector = True
        """
        return self._get_style(bool, sv.SHOWVECTOR)

    @show_vector.setter
    def show_vector(self, show):
        self._set_style(bool(show), sv.SHOWVECTOR)

    @property
    def num_fieldmaps(self):
        """`int`: Number of all fieldmaps in this plot.

        Example usage::

            >>> print(frame.plot().num_fieldmaps)
            3
        """
        return _tecutil.FieldMapGetCountForFrame(self.frame.uid)

    def _fieldmap_indices(self, *keys):
        result = set()
        for key in tecutil.flatten_args(*keys):
            if isinstance(key, FieldmapCollection):
                result |= key._indices
            elif isinstance(key, int):
                result.add(key)
            else:
                index = getattr(key, 'index', self.fieldmap_index(key))
                result.add(index)
        return result

    def fieldmap_index(self, zone):
        """The index of the fieldmap associated with a `Zone <data_access>`.

        Parameters:
            zone (`Zone <data_access>`): The `Zone <data_access>` object that
                belongs to the `Dataset` associated with this plot.

        Returns:
            `Index`

        Example usage::

            >>> fmap_index = plot.fieldmap_index(dataset.zone('Zone'))
            >>> plot.fieldmap(fmap_index).show_mesh = True
        """
        with self.frame.activated():
            return tecutil.Index(_tecutil.ZoneGetFieldMap(zone.index + 1) - 1)

    @property
    def active_fieldmap_indices(self):
        """`set`: Set of active fieldmaps by index.

        This example sets the first three fieldmaps active, disabling all
        others. It then turns on scatter symbols for just these three::

            >>> plot.active_fieldmap_indices = [0, 1, 2]
            >>> plot.fieldmaps(0, 1, 2).scatter.show = True
        """
        return session.get_style(set, sv.ACTIVEFIELDMAPS,
                                 uniqueid=self.frame.uid)

    @active_fieldmap_indices.setter
    def active_fieldmap_indices(self, values):
        session.set_style(set(values), sv.ACTIVEFIELDMAPS,
                          uniqueid=self.frame.uid)

    @property
    def num_solution_times(self):
        """`int`: Number of solution times for all active fieldmaps.

        .. note::

            This only returns the number of *active* solution times. When
            assigning strands and solution times to zones, the zones are
            placed into an *inactive* fieldmap that must be subsequently
            activated. See example below.

        .. code-block:: python

            >>> # place all zones into a single fieldmap (strand: 1)
            >>> # with incrementing solution times
            >>> for time, zone in enumerate(dataset.zones()):
            ...     zone.strand = 1
            ...     zone.solution_time = time
            ...
            >>> # We must activate the fieldmap to ensure the plot's
            >>> # solution times have been updated. Since we placed
            >>> # all zones into a single fieldmap, we can assume the
            >>> # first fieldmap (index: 0) is the one we want.
            >>> plot.active_fieldmaps += [0]
            >>>
            >>> # now the plot's solution times are available.
            >>> print(plot.num_solution_times)
            10
            >>> print(plot.solution_times)
            [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]

        .. versionadded:: 2017.2
            Solution time manipulation requires Tecplot 360 2017 R2 or later.
        """
        if __debug__:
            reqver = (2017, 2)
            if version.sdk_version_info < reqver:
                msg = 'Solution time manipulation requires 2017 R2 or later.'
                raise TecplotOutOfDateEngineError(reqver, msg)
        success, result = _tecutil.SolutionTimeGetNumTimeStepsForFrame(
            self.frame.uid)
        if not success:
            raise TecplotSystemError()
        return result

    @property
    def solution_times(self):
        """`list` of `floats <float>`: `List <list>` of active solution times.

        .. note::

            This only returns the list of *active* solution times. When
            assigning strands and solution times to zones, the zones are placed
            into an *inactive* fieldmap that must be subsequently activated.
            See example below.

        Example usage::

            >>> print(plot.solution_times)
            [0.0, 1.0, 2.0]

        .. versionadded:: 2017.2
            Solution time manipulation requires Tecplot 360 2017 R2 or later.
        """
        if __debug__:
            reqver = (2017, 2)
            if version.sdk_version_info < reqver:
                msg = 'Solution time manipulation requires 2017 R2 or later.'
                raise TecplotOutOfDateEngineError(reqver, msg)
        res = _tecutil.SolutionTimeGetSolutionTimesForFrame(self.frame.uid)
        success, ntimes, times = res
        if not success:
            raise TecplotSystemError()
        ret = list(times[:ntimes])
        if not _tecutil_connector.connected:
            _tecutil.ArrayDealloc(times)
        return ret

    @property
    def solution_time(self):
        """`float`: The current solution time.

        Example usage::

            >>> print(plot.solution_times)
            [0.0, 1.0, 2.0]
            >>> plot.solution_time = 1.0

        .. note:: **Possible side-effect when connected to Tecplot 360.**

                Changing the solution times in the dataset or modifying the
                active fieldmaps in a frame may trigger a change in the active
                plot's solution time by the Tecplot 360 interface. This is done
                to keep the GUI controls consistent. In batch mode, no such
                side-effect will take place and the user must take care to set
                the plot's solution time with the `plot.solution_time
                <Cartesian3DFieldPlot.solution_time>` or
                `plot.solution_timestep
                <Cartesian3DFieldPlot.solution_timestep>` properties.

        .. versionadded:: 2017.2
            Solution time manipulation requires Tecplot 360 2017 R2 or later.
        """
        if __debug__:
            reqver = (2017, 2)
            if version.sdk_version_info < reqver:
                msg = 'Solution time manipulation requires 2017 R2 or later.'
                raise TecplotOutOfDateEngineError(reqver, msg)
        return _tecutil.SolutionTimeGetCurrentForFrame(self.frame.uid)

    @solution_time.setter
    @tecutil.lock()
    def solution_time(self, value):
        if __debug__:
            reqver = (2017, 2)
            if version.sdk_version_info < reqver:
                msg = 'Solution time manipulation requires 2017 R2 or later.'
                raise TecplotOutOfDateEngineError(reqver, msg)
        with self.frame.activated():
            res = _tecutil.SolutionTimeSetCurrent(float(value))
            if res not in [SetValueReturnCode.Ok,
                           SetValueReturnCode.DuplicateValue]:
                raise TecplotSystemError()

    @property
    def solution_timestep(self):
        """`int`: The zero-based index of the current solution time.

        A negative index is interpreted as counting from the end of the
        available solution timesteps. Example usage::

            >>> print(plot.solution_times)
            [0.0, 1.0, 2.0]
            >>> print(plot.solution_time)
            0.0
            >>> plot.solution_timestep += 1
            >>> print(plot.solution_time)
            1.0

        .. note:: **Possible side-effect when connected to Tecplot 360.**

                Changing the solution times in the dataset or modifying the
                active fieldmaps in a frame may trigger a change in the active
                plot's solution time by the Tecplot 360 interface. This is done
                to keep the GUI controls consistent. In batch mode, no such
                side-effect will take place and the user must take care to set
                the plot's solution time with the `plot.solution_time
                <Cartesian3DFieldPlot.solution_time>` or
                `plot.solution_timestep
                <Cartesian3DFieldPlot.solution_timestep>` properties.

        .. versionadded:: 2017.2
            Solution time manipulation requires Tecplot 360 2017 R2 or later.
        """
        if __debug__:
            reqver = (2017, 2)
            if version.sdk_version_info < reqver:
                msg = 'Solution time manipulation requires 2017 R2 or later.'
                raise TecplotOutOfDateEngineError(reqver, msg)
        success, result = _tecutil.SolutionTimeGetCurrentTimeStepForFrame(
            self.frame.uid)
        if not success:
            raise TecplotSystemError()
        return result - 1

    @solution_timestep.setter
    def solution_timestep(self, timestep):
        if __debug__:
            reqver = (2017, 2)
            if version.sdk_version_info < reqver:
                msg = 'Solution time manipulation requires 2017 R2 or later.'
                raise TecplotOutOfDateEngineError(reqver, msg)
        timestep = int(timestep)
        if timestep < 0:
            timestep = self.num_solution_times + timestep
        success, time = _tecutil.SolutionTimeGetSolutionTimeAtTimeStepForFrame(
            self.frame.uid, int(timestep) + 1)
        if not success:
            raise TecplotSystemError()
        self.solution_time = time

    @property
    def ijk_blanking(self):
        """`IJKBlanking`: Mask off cells by :math:`(i, j, k)` index.

        Example usage::

            >>> plot.ijk_blanking.min_percent = (50, 50)
            >>> plot.ijk_blanking.active = True
        """
        return blanking.IJKBlanking(self)

    @property
    def data_labels(self):
        """`FieldPlotDataLabels`: Node and cell labels.

        This object controls displaying labels for every node and/or cell in
        the dataset. Example usage::

            >>> plot.data_labels.show_cell_labels = True
            >>> plot.data_labels.step_index = 10
        """
        return labels.FieldPlotDataLabels(self)

    @property
    def linking_within_frame(self):
        """`FieldPlotLinkingWithinFrame`: Style linking within the frame.

        Example usage::

            >>> plot.linking_within_frame.link_gridline_style = True
        """
        return linking.FieldPlotLinkingWithinFrame(self.frame)


class Cartesian2DFieldPlot(FieldPlot):
    """2D plot containing field data associated with style through fieldmaps.

    .. code-block:: python
        :emphasize-lines: 10-17,23-24

        from os import path
        import tecplot as tp
        from tecplot.constant import PlotType

        examples_dir = tp.session.tecplot_examples_directory()
        infile = path.join(examples_dir, 'SimpleData', 'HeatExchanger.plt')
        dataset = tp.data.load_tecplot(infile)

        frame = tp.active_frame()
        plot = frame.plot(PlotType.Cartesian2D)
        plot.activate()

        plot.vector.u_variable = dataset.variable('U(M/S)')
        plot.vector.v_variable = dataset.variable('V(M/S)')

        plot.contour(2).variable = dataset.variable('T(K)')
        plot.contour(2).colormap_name = 'Sequential - Yellow/Green/Blue'

        for z in dataset.zones():
            fmap = plot.fieldmap(z)
            fmap.contour.flood_contour_group = plot.contour(2)

        plot.show_contour = True
        plot.show_vector = True

        # ensure consistent output between interactive (connected) and batch
        plot.contour(2).levels.reset_to_nice()

        # save image to file
        tp.export.save_png('plot_field2d.png', 600, supersample=3)

    ..  figure:: /_static/images/plot_field2d.png
        :width: 300px
        :figwidth: 300px
    """

    def activate(self):
        """Make this the active plot type on the parent frame.

        Example usage::

            >>> from tecplot.constant import PlotType
            >>> plot = frame.plot(PlotType.Cartesian2D)
            >>> plot.activate()
        """
        self.frame.plot_type = PlotType.Cartesian2D

    @property
    def axes(self):
        """`Cartesian2DFieldAxes`: Axes style control for this plot.

        Example usage::

            >>> from tecplot.constant import PlotType
            >>> frame.plot_type = PlotType.Cartesian2D
            >>> axes = frame.plot().axes
            >>> axes.x_axis.variable = dataset.variable('U')
            >>> axes.y_axis.variable = dataset.variable('V')
        """
        return Cartesian2DFieldAxes(self)

    def fieldmap(self, key):
        """Returns a `Cartesian2DFieldmap` by `Zone <data_access>` or index.

        Parameters:
            key (`Zone <data_access>` or `int`): The `Zone <data_access>` must
                be in the `Dataset` attached to the associated frame of this
                plot. A negative index is interpreted as counting from the end
                of the available fieldmaps.

        Example usage::

            >>> fmap = plot.fieldmap(dataset.zone(0))
            >>> fmap.scatter.show = True
        """
        if isinstance(key, int):
            index = self.num_fieldmaps + key if key < 0 else key
        else:
            index = self.fieldmap_index(key)
        return Cartesian2DFieldmap(self, index)

    def fieldmaps(self, *keys):
        """`Cartesian2DFieldmapCollection` by `Zones <data_access>` or indices.

        Parameters:
            keys (`list` of `Zones <data_access>` or `ints <int>`): The
                `Zones <data_access>` must be in the `Dataset` attached to the
                associated frame of this plot. Negative indices are interpreted
                as counting from the end of the available fieldmaps.

        Example usage::

            >>> fmaps = plot.fieldmaps(dataset.zone(0), dataset.zone(1))
            >>> fmaps.scatter.show = True

        .. versionchanged:: 0.9
            `fieldmaps` was changed from a property (0.8 and earlier) to a
            method requiring parentheses.
        """
        indices = self._fieldmap_indices(*keys)
        if not indices:
            indices = range(self.num_fieldmaps)
        return Cartesian2DFieldmapCollection(self, *indices)

    @property
    def active_fieldmaps(self):
        """`Cartesian2DFieldmapCollection`: Active fieldmaps in this plot.

        Example usage::

            >>> plot.active_fieldmaps.vector.show = True

        .. note:: **Possible side-effect when connected to Tecplot 360.**

                Changing the solution times in the dataset or modifying the
                active fieldmaps in a frame may trigger a change in the active
                plot's solution time by the Tecplot 360 interface. This is done
                to keep the GUI controls consistent. In batch mode, no such
                side-effect will take place and the user must take care to set
                the plot's solution time with the `plot.solution_time
                <Cartesian3DFieldPlot.solution_time>` or
                `plot.solution_timestep
                <Cartesian3DFieldPlot.solution_timestep>` properties.
        """
        indices = self.active_fieldmap_indices
        return Cartesian2DFieldmapCollection(self, *indices)

    @active_fieldmaps.setter
    def active_fieldmaps(self, fmaps):
        indices = getattr(fmaps, 'fieldmap_indices', fmaps)
        self.active_fieldmap_indices = indices

    @property
    def vector(self):
        """`Vector2D`: Vector variable and style control for this plot.

        Example usage::

            >>> plot.vector.u_variable = dataset.variable('U')
        """
        return Vector2D(self)

    @property
    def draw_order(self):
        """`TwoDDrawOrder`: The order in which objects are drawn to the screen.

        Possible values: `TwoDDrawOrder.ByZone`, `TwoDDrawOrder.ByLayer`.

        The order is either by `Zone <data_access>` or by visual layer
        (contour, mesh, etc.)::

            >>> plot.draw_order = TwoDDrawOrder.ByZone
        """
        return self._get_style(TwoDDrawOrder, sv.TWODDRAWORDER)

    @draw_order.setter
    def draw_order(self, order):
        self._set_style(TwoDDrawOrder(order), sv.TWODDRAWORDER)

    @property
    def view(self):
        """`Cartesian2DFieldView`: Axes orientation and limits adjustments.

        Example usage::

            >>> plot.view.fit()
        """
        return view.Cartesian2DFieldView(self)

    @property
    def value_blanking(self):
        """`ValueBlanking`: Mask off cells by value.

        Example usage::

            >>> plot.value_blanking.constraint(0).comparison_value = 3.14
            >>> plot.value_blanking.constraint(0).active = True
        """
        return blanking.ValueBlankingCartesian2D(self)

    @property
    def linking_between_frames(self):
        """`Cartesian2DPlotLinkingBetweenFrames`: Style linking between frames.

        Example usage::

            >>> plot.linking_between_frames.group = 1
            >>> plot.linking_between_frames.link_solution_time = True
        """
        return linking.Cartesian2DPlotLinkingBetweenFrames(self.frame)


class Cartesian3DFieldPlot(FieldPlot):
    """3D plot containing field data associated with style through fieldmaps.

    .. code-block:: python
        :emphasize-lines: 10-14

        from os import path
        import tecplot as tp
        from tecplot.constant import PlotType

        examples_dir = tp.session.tecplot_examples_directory()
        infile = path.join(examples_dir, 'SimpleData', 'SpaceShip.lpk')
        dataset = tp.load_layout(infile)

        frame = tp.active_frame()
        plot = frame.plot(PlotType.Cartesian3D)
        plot.activate()
        plot.use_lighting_effect = False
        plot.show_streamtraces = False
        plot.use_translucency = True

        # ensure consistent output between interactive (connected) and batch
        plot.contour(0).levels.reset_to_nice()

        # save image to file
        tp.export.save_png('plot_field3d.png', 600, supersample=3)

    ..  figure:: /_static/images/plot_field3d.png
        :width: 300px
        :figwidth: 300px
    """

    def activate(self):
        """Make this the active plot type on the parent frame.

        Example usage::

            >>> from tecplot.constant import PlotType
            >>> plot = frame.plot(PlotType.Cartesian3D)
            >>> plot.activate()
        """
        self.frame.plot_type = PlotType.Cartesian3D

    @property
    def axes(self):
        """`Cartesian3DFieldAxes`: Axes style control for this plot.

        Example usage::

            >>> from tecplot.constant import PlotType
            >>> frame.plot_type = PlotType.Cartesian3D
            >>> axes = frame.plot().axes
            >>> axes.x_axis.variable = dataset.variable('U')
            >>> axes.y_axis.variable = dataset.variable('V')
            >>> axes.z_axis.variable = dataset.variable('W')
        """
        return Cartesian3DFieldAxes(self)

    def fieldmap(self, key):
        """Returns a `Cartesian3DFieldmap` by `Zone <data_access>` or index.

        Parameters:
            key (`Zone <data_access>` or `int`): The `Zone
                <data_access>` must be in the `Dataset` attached to the
                associated frame of this plot. A negative index is interpreted
                as counting from the end of the available fieldmaps.

        Example usage::

            >>> fmap = plot.fieldmap(dataset.zone(0))
            >>> fmap.scatter.show = True
        """
        if isinstance(key, int):
            index = self.num_fieldmaps + key if key < 0 else key
        else:
            index = self.fieldmap_index(key)
        return Cartesian3DFieldmap(self, index)

    def fieldmaps(self, *keys):
        """`Cartesian3DFieldmapCollection` by `Zones <data_access>` or indices.

        Parameters:
            keys (`list` of `Zones <data_access>` or `integers <int>`): The
                `Zones <data_access>` must be in the `Dataset` attached to the
                associated frame of this plot. Negative indices are interpreted
                as counting from the end of the available fieldmaps.

        Example usage::

            >>> fmaps = plot.fieldmaps(dataset.zone(0), dataset.zone(1))
            >>> fmaps.scatter.show = True

        .. versionchanged:: 0.9
            `fieldmaps` was changed from a property (0.8 and earlier) to a
            method requiring parentheses.
        """
        indices = self._fieldmap_indices(*keys)
        if not indices:
            indices = range(self.num_fieldmaps)
        return Cartesian3DFieldmapCollection(self, *indices)

    @property
    def active_fieldmaps(self):
        """`Cartesian3DFieldmapCollection`: Active fieldmaps in this plot.

        Example usage::

            >>> plot.active_fieldmaps.vector.show = True

        .. note:: **Possible side-effect when connected to Tecplot 360.**

                Changing the solution times in the dataset or modifying the
                active fieldmaps in a frame may trigger a change in the active
                plot's solution time by the Tecplot 360 interface. This is done
                to keep the GUI controls consistent. In batch mode, no such
                side-effect will take place and the user must take care to set
                the plot's solution time with the `plot.solution_time
                <Cartesian3DFieldPlot.solution_time>` or
                `plot.solution_timestep
                <Cartesian3DFieldPlot.solution_timestep>` properties.
        """
        indices = self.active_fieldmap_indices
        return Cartesian3DFieldmapCollection(self, *indices)

    @active_fieldmaps.setter
    def active_fieldmaps(self, fmaps):
        indices = getattr(fmaps, 'fieldmap_indices',
                          [getattr(fmap, 'index', fmap) for fmap in fmaps])
        self.active_fieldmap_indices = indices

    def slice(self, index):
        """`SliceGroup`: Plot-local `slice <SliceGroup>` style control.

        Example usage::

            >>> from tecplot.constant import Color
            >>> slice0 = frame.plot().slice(0)
            >>> slice0.mesh.show = True
            >>> slice0.mesh.color = Color.Blue
        """
        return slice.SliceGroup(self, index)

    def slices(self, *indices):
        """`SliceGroupCollection`: Plot-local slice style control.

        Example setting setting mesh color of all slices to blue::

            >>> from tecplot.constant import Color
            >>> slices = frame.plot().slices()
            >>> slices.mesh.show = True
            >>> slices.mesh.color = Color.Blue

        Example turning on the first two slice's contour layer::

            >>> slices = frame.plot().slices(0, 1)
            >>> slices.contour.show = True
        """
        return slice.SliceGroupCollection(self, *indices)

    def isosurface(self, index):
        """`IsosurfaceGroup`: Plot-local `isosurface <IsosurfaceGroup>` settings.

        Example usage::

            >>> isosurface_0 = frame.plot().isosurface(0)
            >>> isosurface_0.mesh.color = Color.Blue
        """
        return IsosurfaceGroup(index, self)

    @property
    def vector(self):
        """`Vector3D`: Vector variable and style control for this plot.

        Example usage::

            >>> plot.vector.u_variable = dataset.variable('U')
        """
        return Vector3D(self)

    @property
    def view(self):
        """`Cartesian3DView`: Viewport, axes orientation and limits adjustments.

        Example usage::

            >>> plot.view.fit()
        """
        return view.Cartesian3DView(self)

    @property
    def use_lighting_effect(self):
        """`bool`: Enable lighting effect for all objects within this plot.

        Example usage::

            >>> frame.plot().use_lighting_effect = True
        """
        return self._get_style(bool, sv.USELIGHTINGEFFECT)

    @use_lighting_effect.setter
    def use_lighting_effect(self, value):
        self._set_style(bool(value), sv.USELIGHTINGEFFECT)

    @property
    def use_translucency(self):
        """`bool`: Enable translucent effect for all objects within this plot.

        Example usage::

            >>> frame.plot().use_translucency = True
        """
        return self._get_style(bool, sv.USETRANSLUCENCY)

    @use_translucency.setter
    def use_translucency(self, show):
        self._set_style(bool(show), sv.USETRANSLUCENCY)

    @property
    def light_source(self):
        """`LightSource`: Control the direction and effects of lighting.

        Example usage::

            >>> plot.light_source.intensity = 70.0
        """
        return effects.LightSource(self)

    @property
    def value_blanking(self):
        """`ValueBlanking`: Mask off cells by value.

        Example usage::

            >>> plot.value_blanking.constraint(0).comparison_value = 3.14
            >>> plot.value_blanking.constraint(0).active = True
        """
        return blanking.ValueBlankingCartesian3D(self)

    @property
    def line_lift_fraction(self):
        """`float`: Lift lines above plot by percentage distance to the eye.

        Example usage::

            >>> plot.line_lift_fraction = 0.6
        """
        style = session.Style(sv.GLOBALTHREED, **self._kw)
        return style._get_style(float, sv.LINELIFTFRACTION)

    @line_lift_fraction.setter
    def line_lift_fraction(self, value):
        style = session.Style(sv.GLOBALTHREED, **self._kw)
        style._set_style(float(value), sv.LINELIFTFRACTION)

    @property
    def near_plane_fraction(self):
        """`float`: position of the "near plane".

        In a 3D plot, the "near plane" acts as a windshield. Anything in front
        of this plane does not display. Example usage::

            >>> plot.near_plane_fraction = 0.1
        """
        style = session.Style(sv.GLOBALTHREED, **self._kw)
        return style._get_style(float, sv.NEARPLANEFRACTION)

    @near_plane_fraction.setter
    def near_plane_fraction(self, value):
        style = session.Style(sv.GLOBALTHREED, **self._kw)
        style._set_style(float(value), sv.NEARPLANEFRACTION)

    @property
    def perform_extra_sorting(self):
        """`bool`: Use a more robust depth sorting algorithm for display.

        When printing 3D plots in a vector graphics format, Tecplot 360 must
        sort the objects so that it can draw those farthest from the screen
        first and those closest to the screen last. By default, Tecplot 360
        uses a quick sorting algorithm. This is not always accurate and does
        not detect problems such as intersecting objects. When
        ``perform_extra_sorting`` set to `True`, Tecplot 360 uses a slower,
        more accurate approach that detects and resolves such problems. Example
        usage::

            >>> plot.perform_extra_sorting = True
        """
        style = session.Style(sv.GLOBALTHREED, **self._kw)
        return style._get_style(bool, sv.PERFORMEXTRA3DSORTING)

    @perform_extra_sorting.setter
    def perform_extra_sorting(self, value):
        style = session.Style(sv.GLOBALTHREED, **self._kw)
        style._set_style(bool(value), sv.PERFORMEXTRA3DSORTING)

    @property
    def symbol_lift_fraction(self):
        """`float`: Lift symbols above plot by percentage distance to the eye.

        Example usage::

            >>> plot.symbol_lift_fraction = 0.6
        """
        style = session.Style(sv.GLOBALTHREED, **self._kw)
        return style._get_style(float, sv.SYMBOLLIFTFRACTION)

    @symbol_lift_fraction.setter
    def symbol_lift_fraction(self, value):
        style = session.Style(sv.GLOBALTHREED, **self._kw)
        style._set_style(float(value), sv.SYMBOLLIFTFRACTION)

    @property
    def vector_lift_fraction(self):
        """`float`: Lift vectors above plot by percentage distance to the eye.

        Example usage::

            >>> plot.vector_lift_fraction = 0.6
        """
        style = session.Style(sv.GLOBALTHREED, **self._kw)
        return style._get_style(float, sv.VECTORLIFTFRACTION)

    @vector_lift_fraction.setter
    def vector_lift_fraction(self, value):
        style = session.Style(sv.GLOBALTHREED, **self._kw)
        style._set_style(float(value), sv.VECTORLIFTFRACTION)

    @property
    def linking_between_frames(self):
        """`Cartesian3DPlotLinkingBetweenFrames`: Style linking between frames.

        Example usage::

            >>> plot.linking_between_frames.group = 1
            >>> plot.linking_between_frames.link_solution_time = True
        """
        return linking.Cartesian3DPlotLinkingBetweenFrames(self.frame)


class LinePlot(Plot):
    """Plot with line data and associated style through linemaps.

    .. code-block:: python

        from os import path
        import tecplot as tp
        from tecplot.constant import PlotType, Color, LinePattern

        examples_dir = tp.session.tecplot_examples_directory()
        infile = path.join(examples_dir, 'SimpleData', 'Rainfall.dat')
        dataset = tp.data.load_tecplot(infile)

        frame = tp.active_frame()
        frame.plot_type = PlotType.XYLine
        plot = frame.plot()
        plot.show_symbols = True

        # save image to file
        tp.export.save_png('plot_line.png', 600, supersample=3)

    ..  figure:: /_static/images/plot_line.png
        :width: 300px
        :figwidth: 300px
    """

    def __init__(self, frame):
        super().__init__(frame, sv.LINEPLOTLAYERS)

    @tecutil.lock()
    def delete_linemaps(self, *linemaps):
        r"""Clear all linemaps within this plot.

        Parameters:
            \*linemaps (:ref:`Linemap`, `int` or `str`):
                One or more of the following: :ref:`Linemap` objects, linemap
                indices (zero-based) or linemap names. If none are given, all
                linemaps will be deleted.

        Example usage::

            >>> plot.delete_linemaps()
            >>> print(plot.num_linemaps)
            0
        """
        if not linemaps:
            return _tecutil.LineMapDelete(None)
        with tecutil.IndexSet() as indices:
            for lmap in tecutil.flatten_args(*linemaps):
                try:
                    # try as a Linemap object
                    indices.append(lmap.index)
                except (AttributeError, TypeError):
                    try:
                        # try as a linemap index
                        indices.append(lmap)
                    except TypeError:
                        # assume name pattern
                        for submap in self.linemaps(lmap):
                            indices.append(submap.index)
            return _tecutil.LineMapDelete(indices)

    @property
    def num_linemaps(self):
        """`int`: Number of linemaps held by this plot.

        Example usage::

            >>> print(plot.num_linemaps)
            3
        """
        return _tecutil.LineMapGetCountForFrame(self.frame.uid)

    def _linemap_indices_by_name(self, pattern):
        pattern_type = getattr(re, 'Pattern', getattr(re, '_pattern_type', None))
        if not isinstance(pattern, pattern_type):
            regex = re.compile(fnmatch.translate(pattern), re.IGNORECASE)
        else:
            regex = pattern

        indices = set()
        with self.frame.activated():
            found = False
            for i in range(self.num_linemaps):
                try:
                    _, name = _tecutil.LineMapGetName(i + 1)
                    name = name or ''
                except (AttributeError, TecplotSystemError):
                    name = ''
                if regex.match(name):
                    found = True
                    indices.add(i)
            if __debug__:
                if (
                    not found and
                    isinstance(pattern, six.string_types) and
                    any(c in pattern for c in '*?[]')
                ):
                    msg = 'no linemaps found matching: "{}"'.format(pattern)
                    warning = TecplotPatternMatchWarning(pattern, msg)
                    warnings.warn(warning)
        return indices

    def _linemap_indices(self, *keys):
        """
        convert keys to a set of indices where keys are:
            * int: get one linemap index (converting negative values)
            * regex pattern: match by name
            * glob-style string: match by name
        if no keys are given, get all linemaps indices
        """
        indices = set()
        if keys:
            for key in keys:
                if isinstance(key, int):
                    index = key + self.num_linemaps if key < 0 else key
                    if index >= self.num_linemaps:
                        msg = 'linemap index out of range: ' + str(index)
                        raise TecplotIndexError(msg)
                    indices.add(index)
                else:
                    indices |= self._linemap_indices_by_name(key)
        else:
            indices |= set(range(self.num_linemaps))
        return indices

    @tecutil.lock()
    def _add_linemap(self, name, zone, show=True):
        with self.frame.activated():
            new_linemap_index = self.num_linemaps
            if not _tecutil.LineMapCreate():
                raise TecplotSystemError()
            linemap = self.linemap(new_linemap_index)
            if name is not None:
                linemap.name = name
            if zone is not None:
                linemap.zone_index = getattr(zone, 'index', zone)
            if show is not None:
                linemap.show = show
            return linemap

    @property
    def legend(self):
        """`LineLegend`: Line plot legend style and placement control.

        Example usage::

            >>> plot.legend.show = True
        """
        return legend.LineLegend(self)

    @property
    def active_linemap_indices(self):
        """`set` of `integers <int>`: `set` of all active linemaps by index.

        Numbers are zero-based indices to the linemaps::

            >>> active_indices = plot.active_linemap_indices
            >>> active_lmaps = [plot.linemap(i) for i in active_indices]
        """
        return session.get_style(set, sv.ACTIVELINEMAPS,
                                 uniqueid=self.frame.uid)

    @property
    def show_lines(self):
        """`bool`: Enable lines for this plot.

        Example usage::

            >>> plot.show_lines = True
        """
        return self._get_style(bool, sv.SHOWLINES)

    @show_lines.setter
    def show_lines(self, value):
        self._set_style(bool(value), sv.SHOWLINES)

    @property
    def show_symbols(self):
        """`bool`: Enable symbols at line vertices for this plot.

        Example usage::

            >>> plot.show_symbols = True
        """
        return self._get_style(bool, sv.SHOWSYMBOLS)

    @show_symbols.setter
    def show_symbols(self, value):
        self._set_style(bool(value), sv.SHOWSYMBOLS)

    @property
    def value_blanking(self):
        """`ValueBlanking`: Mask off points by value.

        Example usage::

            >>> plot.value_blanking.constraint(0).comparison_value = 3.14
            >>> plot.value_blanking.constraint(0).active = True
        """
        return blanking.ValueBlanking(self)

    @property
    def base_font(self):
        """`BaseFont`: Default typeface style control.

        Example usage::

            >>> plot.base_font.typeface = 'Times'
        """
        return text.BaseFont(sv.GLOBALLINEPLOT, **self._kw)

    @property
    def data_labels(self):
        """`LinePlotDataLabels`: Node and cell labels.

        This object controls displaying labels for every node and/or cell in
        the dataset. Example usage::

            >>> plot.data_labels.show_node_labels = True
            >>> plot.data_labels.step_index = 10
        """
        return labels.LinePlotDataLabels(self)

    @property
    def linking_within_frame(self):
        """`DataPlotLinkingWithinFrame`: Style linking within the frame.

        Example usage::

            >>> plot.linking_within_frame.link_gridline_style = True
        """
        return linking.DataPlotLinkingWithinFrame(self.frame)


class XYLinePlot(LinePlot):
    """Cartesian plot with line data and associated style through linemaps.

    .. code-block:: python
        :emphasize-lines: 10-14

        from os import path
        import tecplot as tp
        from tecplot.constant import PlotType, FillMode

        examples_dir = tp.session.tecplot_examples_directory()
        infile = path.join(examples_dir, 'SimpleData', 'SunSpots.plt')
        dataset = tp.data.load_tecplot(infile)

        frame = tp.active_frame()
        plot = frame.plot(PlotType.XYLine)
        plot.activate()
        plot.show_symbols = True
        plot.linemap(0).symbols.fill_mode = FillMode.UseLineColor
        plot.linemap(0).symbols.size = 1

        tp.export.save_png('plot_xyline.png', 600, supersample=3)

    ..  figure:: /_static/images/plot_xyline.png
        :width: 300px
        :figwidth: 300px
    """

    def activate(self):
        """Make this the active plot type on the parent frame.

        Example usage::

            >>> from tecplot.constant import PlotType
            >>> plot = frame.plot(PlotType.XYLine)
            >>> plot.activate()
        """
        self.frame.plot_type = PlotType.XYLine

    def linemaps(self, *keys):
        """`XYLinemapCollection` by index or name.

        Parameters:
            keys (`int`, `str` or `re.Pattern <re.compile>`): Zero-based
                index, case-insensitive `glob-style pattern string
                <fnmatch.fnmatch>` or a compiled `regex pattern instance
                <re.compile>` used to match the linemaps by name. A negative
                index is interpreted as counting from the end of the available
                linemaps.

        Example usage, adjusting the line thickness for all lines in the plot::

            >>> plot.linemaps().line.line_thickness = 1.4
        """
        indices = self._linemap_indices(*keys)
        return linemap.XYLinemapCollection(self, *indices)

    def linemap(self, pattern):
        """Returns a specific linemap within this plot.

        Parameters:
            pattern (`int`, `str` or `re.Pattern <re.compile>`): Zero-based
                index, case-insensitive
                `glob-style pattern string <fnmatch.fnmatch>` or a compiled
                `regex pattern instance <re.compile>` used to match the
                linemaps by name. A negative index is interpreted as counting
                from the end of the available linemaps.

        Returns:
            `XYLinemap` corresponding to *pattern* or `None` if *pattern* was
            passed in as a `str` or `regex pattern instance <re.compile>` and
            no matching linemap was found.

        .. note::

            Plots can contain linemaps with identical names and only the first
            match found is returned. This is not guaranteed to be deterministic
            and care should be taken to have only linemaps with unique names
            when this feature is used.

        Example usage::

            >>> plot.linemap(0).error_bar.show = True
        """
        try:
            return next(iter(self.linemaps(pattern)))
        except StopIteration:
            pass

    @property
    def active_linemaps(self):
        """`XYLinemapCollection`: Active linemaps in this plot.

        Example usage::

            >>> plot.active_linemaps.show_symbols = True
        """
        indices = self.active_linemap_indices
        return linemap.XYLinemapCollection(self, *indices)

    def add_linemap(self, name=None, zone=None, x=None, y=None, show=True):
        """Add a linemap using the specified zone and variables.

        Parameters:

            name (`str`): Name of the linemap which can be used for
                retrieving with `XYLinePlot.linemap`. If `None`, then the
                linemap will not have a name. Default: `None`.
            zone (`Zone <data_access>`): The data to be used when drawing this
                linemap. If `None`, then |Tecplot Engine| will select a zone.
                Default: `None`.
            x (`Variable`): The ``x`` variable which must be from the same
                `Dataset` as ``y`` and ``zone``. If `None`, then
                |Tecplot Engine| will select an x variable. Default: `None`.
            y (`Variable`): The ``y`` variable which must be from the same
                `Dataset` as ``x`` and ``zone``. If `None`, then
                |Tecplot Engine| will select a ``y`` variable. Default: `None`.
            show (`bool`, optional): Enable this linemap as soon as
                it's added. (default: `True`). If `None`, then |Tecplot Engine|
                will determine if the linemap should be enabled.

        Returns:
            `XYLinemap`

        Example usage::

            >>> lmap = plot.add_linemap('Line 1', dataset.zone('Zone'),
            ...                         dataset.variable('X'),
            ...                         dataset.variable('Y'))
            >>> lmap.line.line_thickness = 0.8
        """
        lmap = self._add_linemap(name, zone, show)
        if x is not None:
            lmap.x_variable = x
        if y is not None:
            lmap.y_variable = y
        return lmap

    @property
    def axes(self):
        """`XYLineAxes`: Axes style control for this plot.

        Example usage::

            >>> from tecplot.constant import PlotType, AxisMode
            >>> frame.plot_type = PlotType.XYLine
            >>> axes = frame.plot().axes
            >>> axes.axis_mode = AxisMode.XYDependent
            >>> axes.xy_ratio = 2
        """
        return XYLineAxes(self)

    @property
    def show_bars(self):
        """`bool`: Enable bar chart drawing mode for this plot.

        Example usage::

            >>> plot.show_bars = True
        """
        return self._get_style(bool, sv.SHOWBARCHARTS)

    @show_bars.setter
    def show_bars(self, value):
        self._set_style(bool(value), sv.SHOWBARCHARTS)

    @property
    def show_error_bars(self):
        """`bool`: Enable error bars for this plot.

        The variable to be used for error bars must be set first on at least
        one linemap within this plot::

            >>> plot.linemap(0).error_bars.variable = dataset.variable('E')
            >>> plot.show_error_bars = True
        """
        return self._get_style(bool, sv.SHOWERRORBARS)

    @show_error_bars.setter
    def show_error_bars(self, value):
        self._set_style(bool(value), sv.SHOWERRORBARS)

    @property
    def view(self):
        """`XYLineView`: View control of the plot relative to the frame.

        Example usage::

            >>> plot.view.fit()
        """
        return view.XYLineView(self)

    @property
    def linking_between_frames(self):
        """`XYLinePlotLinkingBetweenFrames`: Style linking between frames.

        Example usage::

            >>> plot.linking_between_frames.group = 1
            >>> plot.linking_between_frames.link_solution_time = True
        """
        return linking.XYLinePlotLinkingBetweenFrames(self.frame)


class PolarLinePlot(LinePlot):
    """Polar plot with line data and associated style through linemaps.

    .. code-block:: python
        :emphasize-lines: 16-22

        import numpy as np
        import tecplot as tp
        from tecplot.constant import *

        frame = tp.active_frame()

        npoints = 300
        r = np.linspace(0, 2000, npoints)
        theta = np.linspace(0, 10, npoints)

        dataset = frame.create_dataset('Data', ['R', 'Theta'])
        zone = dataset.add_ordered_zone('Zone', (300,))
        zone.values('R')[:] = r
        zone.values('Theta')[:] = theta

        plot = frame.plot(PlotType.PolarLine)
        plot.activate()
        plot.axes.r_axis.max = r.max()
        plot.axes.theta_axis.mode = ThetaMode.Radians
        plot.delete_linemaps()
        lmap = plot.add_linemap('Linemap', zone, dataset.variable('R'),
                                    dataset.variable('Theta'))
        lmap.line.line_thickness = 0.8
        lmap.line.color = Color.Green

        plot.view.fit()

        tp.export.save_png('plot_polar.png', 600, supersample=3)

    ..  figure:: /_static/images/plot_polar.png
        :width: 300px
        :figwidth: 300px
    """

    def activate(self):
        """Make this the active plot type on the parent frame.

        Example usage::

            >>> from tecplot.constant import PlotType
            >>> plot = frame.plot(PlotType.PolarLine)
            >>> plot.activate()
        """
        self.frame.plot_type = PlotType.PolarLine

    @property
    def axes(self):
        """`PolarLineAxes`: Axes style control for this plot.

        Example usage::

            >>> from tecplot.constant import PlotType, ThetaMode
            >>> frame.plot_type = PlotType.PolarLine
            >>> axes = frame.plot().axes
            >>> axes.theta_mode = ThetaMode.Radians
        """
        return PolarLineAxes(self)

    @property
    def view(self):
        """`PolarView`: View control of the plot relative to the frame.

        Example usage::

            >>> plot.view.fit()
        """
        return view.PolarView(self)

    def add_linemap(self, name=None, zone=None, r=None, theta=None, show=True):
        """Add a linemap using the specified zone and variables.

        Parameters:
            name (`str`): Name of the linemap which can be used for
                retrieving with `PolarLinePlot.linemap`. If `None`, then the
                linemap will not have a name. Default: `None`.
            zone (`Zone <data_access>`): The data to be used when drawing this
                linemap. If `None`, then |Tecplot Engine| will select a
                `Zone <data_access>`.
                Default: `None`.
            r (`Variable`): The ``r`` variable which must be from the same
                `Dataset` as ``theta`` and ``zone``. If `None`, then
                |Tecplot Engine| will select a variable. Default: `None`.
            theta (`Variable`): The ``theta`` variable which must be from the
                same `Dataset` as ``r`` and ``zone``. If `None`, then
                |Tecplot Engine| will select a variable. Default: `None`.
            show (`bool`, optional): Enable this linemap as soon as
                it's added. (default: `True`)

        Returns:
            `PolarLinemap`

        Example usage::

            >>> lmap = plot.add_linemap('Line 1', dataset.zone('Zone'),
            ...                         dataset.variable('R'),
            ...                         dataset.variable('Theta'))
            >>> lmap.line.line_thickness = 0.8
        """
        lmap = self._add_linemap(name, zone, show)
        if r is not None:
            lmap.r_variable = r
        if theta is not None:
            lmap.theta_variable = theta
        return lmap

    def linemaps(self, *keys):
        """`PolarLinemapCollection` by index or name.

        Parameters:
            keys (`int`, `str` or `re.Pattern <re.compile>`): Zero-based
                index, case-insensitive `glob-style pattern string
                <fnmatch.fnmatch>` or a compiled `regex pattern instance
                <re.compile>` used to match the linemaps by name. A negative
                index is interpreted as counting from the end of the available
                linemaps.

        Example usage, adjusting the line thickness for all lines in the plot::

            >>> plot.linemaps().line.line_thickness = 1.4
        """
        indices = self._linemap_indices(*keys)
        return linemap.PolarLinemapCollection(self, *indices)

    def linemap(self, pattern):
        """Returns a specific linemap within this plot.

        Parameters:
            pattern (`int`, `str` or `re.Pattern <re.compile>`): Zero-based
                index, case-insensitive
                `glob-style pattern string <fnmatch.fnmatch>` or a compiled
                `regex pattern instance <re.compile>` used to match the
                linemaps by name. A negative index is interpreted as counting
                from the end of the available linemaps.

        Returns:
            `PolarLinemap` corresponding to *pattern* or `None` if *pattern*
            was passed in as a `str` or `regex pattern instance <re.compile>`
            and no matching linemap was found.

        .. note::

            Plots can contain linemaps with identical names and only the first
            match found is returned. This is not guaranteed to be deterministic
            and care should be taken to have only linemaps with unique names
            when this feature is used.

        Example usage::

            >>> plot.linemap(0).error_bar.show = True
        """
        try:
            return next(iter(self.linemaps(pattern)))
        except StopIteration:
            pass

    @property
    def active_linemaps(self):
        """`PolarLinemapCollection`: Active linemaps in this plot.

        Example usage::

            >>> plot.active_linemaps.show_symbols = True
        """
        indices = self.active_linemap_indices
        return linemap.PolarLinemapCollection(self, *indices)

    @property
    def linking_between_frames(self):
        """`PolarPlotLinkingBetweenFrames`: Style linking between frames.

        Example usage::

            >>> plot.linking_between_frames.group = 1
            >>> plot.linking_between_frames.link_solution_time = True
        """
        return linking.PolarPlotLinkingBetweenFrames(self.frame)

