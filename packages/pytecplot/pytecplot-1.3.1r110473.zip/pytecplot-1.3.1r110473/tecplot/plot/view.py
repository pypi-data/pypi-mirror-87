from builtins import super

import itertools
import math

from ..tecutil import _tecutil
from ..constant import *
from ..exception import *
from .. import constant, session, tecutil, version
from ..tecutil import lock, lock_attributes, sv


@lock_attributes
class View(session.Style):
    """View of plot within the frame."""
    def __init__(self, plot, *svargs):
        self.plot = plot
        super().__init__(svargs, uniqueid=plot.frame.uid)

    @lock()
    def _view_action(self, action, consider_blanking=None):
        """Internal implementation for all view actions which take a single
        consider_blanking parameter."""
        with self.plot.frame.activated():
            with tecutil.ArgList() as arglist:
                arglist[sv.VIEWOP] = action
                arglist[sv.CONSIDERBLANKING] = consider_blanking
                if not _tecutil.ViewX(arglist):
                    raise TecplotSystemError()

    @property
    def magnification(self):
        """`float`: Magnification for the data being plotted.

        The ``magnification`` value is a decimal percent and must be greater
        than 0. A ``magnification`` size of 1.0 (100%) will size the plot so
        that it can fit within the grid area.  The following example will scale
        the view to ten percent of the size at which the data would fit the
        full frame::

            >>> view.magnification = 0.10
        """
        with self.plot.frame.activated():
            success, result = _tecutil.ViewGetMagnification()
            if not success:
                raise TecplotSystemError()
            return result

    @magnification.setter
    @lock()
    def magnification(self, value):
        with self.plot.frame.activated():
            if not _tecutil.ViewSetMagnification(float(value)):
                raise TecplotSystemError()

    @lock()
    def translate(self, x=0.0, y=0.0):
        """Shift the data being plotted in the X and/or Y direction.

        .. note:: The amount translated is in frame units.

        Parameters:
            x (`float`, optional): Amount to shift in the X direction
                as a percentage of the frame width. Positive values shift right,
                negative values shift left. (default: 0.0)
            y (`float`, optional): Amount to shift in the Y direction
                as a percentage of the frame height. Positive values shift up,
                negative values shift down. (default: 0.0)

        Translate the view 10 percent of the frame width to the right::

            >>> view.translate(x=10)

        Translate the view 5 percent of the frame width to the right,
        20 of the frame height down::

            >>> view.translate(x=5, y=-20)
        """
        with self.plot.frame.activated():
            if not _tecutil.ViewTranslate(float(x), float(y)):
                raise TecplotSystemError()

    @lock()
    def zoom(self, xmin, ymin, xmax, ymax):
        """Zoom the view to a rectangular region of the plot.

        Change the view by "zooming" into the data. Ranges on the axes are
        adjusted to view the region defined by the rectangle with corners at
        (``xmin``, ``ymin``) and (``xmax``, ``ymax``).

        .. note:: All position values are defined in units of the X- and
            Y- axis (that is, grid coordinates).

        Parameters:
            xmin: (`float`) X min corner of the rectangle to be viewed.
            ymin: (`float`) Y min corner of the rectangle to be viewed.
            xmax: (`float`) X max corner of the rectangle to be viewed.
            ymax: (`float`) Y max corner of the rectangle to be viewed.

        Zoom so the rectangular region with corners at ``(1, 0)`` and ``(7,
        9)`` is in view::

            >>> view.zoom(1, 7, 0, 9)
        """
        with self.plot.frame.activated():
            if not _tecutil.ViewZoom(float(xmin), float(ymin),
                                     float(xmax), float(ymax)):
                raise TecplotSystemError()


class Cartesian2DView(View):
    def adjust_to_nice(self):
        """Shifts axes to make axis-line values "nice"

        Modifies the axis range to fit the minimum and maximum of the
        variable assigned to that axis, then snaps the major tick marks to
        the ends of the axis. If axis dependency is not independent,
        this may affect the range on another axis.

        In other words, given an existing range of values RMin, RMax and an
        initial delta, D (such as axis ranges with grid spacing or
        contour levels), determine a new delta (ND) that:

        * Is 1,2, or 5 times 10 to some power that is the "best"
          alternative to D.
        * Produces new range min and max values that are some multiple of ND
          that are nearest the original RMin and RMax

        Axes are shifted without changing the extents of the window.
        """
        self._view_action(constant.View.MakeCurrentViewNice)

    def fit_to_nice(self):
        """Set axis range to begin/end on major axis increments.

        Changes the view to make the extents of the frame neatly hold the
        plot with integer values for axis labels.
        """
        self._view_action(constant.View.NiceFit)


class FieldView(View):
    def fit(self, consider_blanking=True):
        """Fit the data being plotted within the axis grid area.

        .. note:: This also takes into consideration text and geometries that
            are plotted using the grid coordinate system.

        Parameters:
            consider_blanking (`Boolean <bool>`, optional): If `True` and
                blanking is enabled, the resulting view excludes blanked cells
                at the edges of the plot. If 'False`, then
                the resulting view will ignore blanked cells at the edges of the
                plot. (default: `True`)
        """
        self._view_action(constant.View.Fit, consider_blanking)

    def fit_data(self, consider_blanking=True):
        """Fit data zones or line mappings within the grid area.

        Parameters:
            consider_blanking (`Boolean <bool>`, optional): If `True` and
                blanking is enabled, the resulting view excludes blanked cells
                at the edges of the plot. If 'False`, then
                the resulting view will ignore blanked cells at the edges of the
                plot. (default: `True`)

        .. note:: This does not take into consideration text and geometries that
            are plotted using the grid coordinate system.
        """
        self._view_action(constant.View.DataFit, consider_blanking)

    def center(self, consider_blanking=True):
        """Center the data within the axis grid area.

        Parameters:
            consider_blanking (`Boolean <bool>`, optional): If `True` and
                blanking is enabled, the resulting view excludes blanked cells
                at the edges of the plot. If 'False`, then
                the resulting view will ignore blanked cells at the edges of the
                plot. (default: `True`)
        """
        self._view_action(constant.View.Center, consider_blanking)


class LineView(View):
    def fit(self):
        """Fit the data being plotted within the axis grid area.

        .. note:: This also takes into consideration text and geometries that
            are plotted using the grid coordinate system.
        """
        self._view_action(constant.View.Fit)

    def fit_data(self):
        """Fit data zones or line mappings within the grid area.

        .. note:: This does not take into consideration text and geometries
            that are plotted using the grid coordinate system.
        """
        self._view_action(constant.View.DataFit)

    def center(self):
        """Center the data within the axis grid area.

        Raises:
            `TecplotSystemError`: View could not be centered.
        """
        self._view_action(constant.View.Center)

    @property
    def extents(self):
        """`tuple`: Viewport extents in data units.

        Extents are represented by the `tuple`: ``(x1, y1, x2, y2)`` and
        setting this effectively zooms the view of the data within the
        viewport. The values ``(x1, y1)`` and ``(x2, y2)`` are the lower-left
        and upper-right edges respectively and are in data units. The following
        example will set the bottom and left edges of the viewport to the value
        of ``-3`` and the top and right edges to the value of 5::

            >>> plot.view.extents = -3, -3, 5, 5
        """
        return session.RectPosition(self, sv.EXTENTS)

    @extents.setter
    def extents(self, values):
        session.RectPosition(self, sv.EXTENTS)[:] = values


class XYLineView(LineView, Cartesian2DView):
    """Adjust the way XY Line data is displayed.

    .. code-block:: python
        :emphasize-lines: 20

        import os
        import tecplot
        from tecplot.constant import *

        examples_dir = tecplot.session.tecplot_examples_directory()
        datafile = os.path.join(examples_dir, 'SimpleData', 'Rainfall.dat')
        dataset = tecplot.data.load_tecplot(datafile)

        frame = tecplot.active_frame()
        plot = frame.plot()
        frame.plot_type = tecplot.constant.PlotType.XYLine

        for i in range(3):
            plot.linemap(i).show = True
            plot.linemap(i).line.line_thickness = .4

        y_axis = plot.axes.y_axis(0)
        y_axis.title.title_mode = AxisTitleMode.UseText
        y_axis.title.text = 'Rainfall (in)'
        plot.view.fit_to_nice()

        tecplot.export.save_png('view_line.png', 600, supersample=3)

    .. figure:: /_static/images/view_line.png
        :width: 300px
        :figwidth: 300px
    """
    def __init__(self, plot):
        super().__init__(plot, sv.XYLINEAXIS)


class Cartesian2DFieldView(FieldView, Cartesian2DView):
    """Adjust the way cartesian 2D data is displayed.

    .. code-block:: python
        :emphasize-lines: 16

        from os import path
        import tecplot as tp
        from tecplot.constant import PlotType

        examples_dir = tp.session.tecplot_examples_directory()
        infile = path.join(examples_dir, 'SimpleData', 'HeatExchanger.plt')
        dataset = tp.data.load_tecplot(infile)

        frame = tp.active_frame()
        plot = frame.plot(PlotType.Cartesian2D)
        plot.activate()
        plot.show_contour = True
        plot.contour(0).variable = dataset.variable('P(N)')
        plot.contour(0).colormap_name = 'Sequential - Yellow/Green/Blue'

        plot.view.fit_to_nice()

        # ensure consistent output between interactive (connected) and batch
        plot.contour(0).levels.reset_to_nice()

        tp.export.save_png('view_2D.png', 600, supersample=3)

    .. figure:: /_static/images/view_2D.png
        :width: 300px
        :figwidth: 300px
    """
    def fit_to_nice(self, consider_blanking=True):
        """Set axis range to begin/end on major axis increments.

        Changes the view to make the extents of the frame neatly hold the
        plot with integer values for axis labels.

        Parameters:
            consider_blanking (`Boolean <bool>`, optional): If `True` and
                blanking is enabled, the resulting view excludes blanked cells
                at the edges of the plot. If 'False`, then
                the resulting view will ignore blanked cells at the edges of the
                plot. (default: `True`)
        """
        self._view_action(constant.View.NiceFit, consider_blanking)


class Cartesian3DView(FieldView):
    """Adjust the way cartesian 3D data is displayed.

    .. code-block:: python
        :emphasize-lines: 9-13

        import tecplot
        import os
        from tecplot.constant import *
        examples_dir = tecplot.session.tecplot_examples_directory()
        infile = os.path.join(examples_dir, 'SimpleData', 'F18.plt')
        ds = tecplot.data.load_tecplot(infile)
        plot = tecplot.active_frame().plot(PlotType.Cartesian3D)
        plot.activate()
        plot.view.width = 17.5
        plot.view.alpha = 0
        plot.view.theta = 125
        plot.view.psi   = 65
        plot.view.position = (-100, 80, 65)

        tecplot.export.save_jpeg('view_3D.jpeg', 600, supersample=3)

    .. figure:: /_static/images/view_3D.jpeg
        :width: 300px
        :figwidth: 300px
    """
    def __init__(self, plot):
        super().__init__(plot, sv.THREEDVIEW)

    @lock()
    def rotate_to_angles(self, psi, theta, alpha):
        """Rotate the plot to specific angles.

        Parameters:
            psi: (`float`): Tilt, in degrees, of the eye origin ray away from
                the Z-axis.
            theta: (`float`): Rotation, in degrees, of the eye origin ray about
                the Z-axis.
            alpha: (`float`): Twist, in degrees, about the eye origin ray.
        """
        _tecutil.RotateToSpecificAngles(float(psi), float(theta), float(alpha))

    @lock()
    def _rotate(self, angle, normal, origin):
        rotate_axis = RotateAxis.AboutVector
        for i, j in itertools.combinations([0, 1, 2], 2):
            if normal[i] == 0 and normal[j] == 0:
                a = ({0, 1, 2} - {i, j}).pop()
                rotate_axis = {0: RotateAxis.X,
                               1: RotateAxis.Y,
                               2: RotateAxis.Z}[a]
                if normal[a] < 0:
                    angle = -1 * angle
                break
        if not _tecutil.ViewRotate3D(rotate_axis.value, angle, normal[0],
                                     normal[1], normal[2],
                                     RotateOriginLocation(origin).value):
            raise TecplotSystemError()

    @property
    def rotation_origin(self):
        """`tuple`: Center of rotation for `rotate_axes` and `rotate_viewer`.

        Example of rotating 30 degrees about the :math:`y`-axis and around the
        data-position :math:`(x, y, z) = (1, 2, 3)`::

            >>> plot.view.rotation_origin = (1, 2, 3)
            >>> plot.view.rotate_axes(30, (0, 1, 0))
        """
        style = session.Style(sv.GLOBALTHREED, uniqueid=self.plot.frame.uid)
        return session.XYZ(style, sv.ROTATEORIGIN)

    @rotation_origin.setter
    def rotation_origin(self, values):
        style = session.Style(sv.GLOBALTHREED, uniqueid=self.plot.frame.uid)
        session.XYZ(style, sv.ROTATEORIGIN)[:] = values

    def rotate_axes(self, angle, normal=(0, 0, 1)):
        """Adjust the view so the axes are rotated about some normal vector.

        This effectively rotates the axes around the axes origin about some
        **normal** using the right-hand rule by the specified **angle** in
        degrees. The rotation is performed about the position:
        `Cartesian3DView.rotation_origin`.

        Parameters:
            angle (`float`): The angle in degrees to rotate.
            normal (`tuple`, optional): The direction vector :math:`(x, y, z)`
                around which the rotation will be done.
                (default: ``(0, 0, 1)``)

        Example of rotating 30 degrees about the :math:`x`-axis and around the
        data's origin::

            >>> plot.view.rotation_origin = (0, 0, 0)
            >>> plot.view.rotate_axes(30, (1, 0, 0))
        """
        return self._rotate(angle, normal, RotateOriginLocation.DefinedOrigin)

    def rotate_viewer(self, angle, normal=(0, 0, 1)):
        """Rotate the camera or viewer about some normal vector.

        This rotates the viewer about some **normal** using the right-hand rule
        by the specified **angle** in degrees. The rotation is performed about
        the position: `Cartesian3DView.rotation_origin`.

        Parameters:
            angle (`float`): The angle in degrees to rotate.
            normal (`tuple`, optional): The direction vector :math:`(x, y, z)`
                around which the rotation will be done.
                (default: ``(0, 0, 1)``)

        Example of rotating 2 degrees about the :math:`x`-axis and around the
        data's origin::

            >>> plot.view.rotation_origin = (0, 0, 0)
            >>> plot.view.rotate_viewer(2, (1, 0, 0))
        """
        return self._rotate(angle, normal, RotateOriginLocation.Viewer)

    def fit_surfaces(self, consider_blanking=True):
        """Fit 3D plot surfaces to the grid area.

        Parameters:
            consider_blanking (`bool`, optional): If `True` and blanking is
                enabled, the resulting view excludes blanked cells at the edges
                of the plot. If 'False`, then the resulting view will ignore
                blanked cells at the edges of the plot. (default: `True`)

        .. note:: 3D volume zones are excluded when `surfaces_to_plot` is
            `SurfacesToPlot.None_`.
        """
        self._view_action(constant.View.FitSurfaces, consider_blanking)

    @property
    def _draw_in_perspective(self):
        # DRAWINPERSPECTIVE is deprecated, but we use it privately for backward
        # compatibility if PROJECTION is not available.
        return self._get_style(bool, sv.DRAWINPERSPECTIVE)

    @property
    def field_of_view(self):
        """`float`: Amount of the plot which is displayed.

        Get or set the amount of the plot (in terms of spherical arc) in front
        of the viewer that may be seen.

        .. warning:: ``field_of_view`` cannot be set if `projection`
            is `Projection.Orthographic`.

        Example usage::

            >>> from tecplot.constant import Projection
            >>> plot.view.projection = Projection.Perspective
            >>> plot.view.field_of_view = 9.6
        """
        return self._get_style(float, sv.FIELDOFVIEW)

    @field_of_view.setter
    def field_of_view(self, value):
        if __debug__:
            if not self._draw_in_perspective:
                raise TecplotValueError('Cannot set field_of_view if not '
                                        'using perspective.')
        self._set_style(float(value), sv.FIELDOFVIEW)

    @staticmethod
    def _check_projection_supported():
        if __debug__:
            sdk_version_required = (2017, 2, 0, 78708)
            if version.sdk_version_info < sdk_version_required:
                raise TecplotOutOfDateEngineError(
                    sdk_version_required,
                    'Cartesian3DView.projection() is not supported.')

    @property
    def projection(self):
        """`Projection`: Projection type (`Perspective` or `Orthographic`).

        When set to `Perspective`, Tecplot 360 draws the plot in perspective.
        When set to `Orthographic`, the plot is drawn with orthographic
        projection where the shape of the object does not change with distance.

        .. note:: Requires Tecplot version 2017.2 or later.

        Example usage::

            >>> from tecplot.constant import Projection
            >>> plot.view.projection = Projection.Orthographic
        """
        self._check_projection_supported()
        return self._get_style(Projection, sv.PROJECTION)

    @projection.setter
    def projection(self, value):
        self._check_projection_supported()
        self._set_style(Projection(value), sv.PROJECTION)

    @property
    def psi(self):
        """`float`: Eye origin view Psi angle in degrees.

        The Psi angle is the tilt of the eye origin ray away from the Z-axis::

            >>> plot.view.psi = 90.0
        """
        return self._get_style(float, sv.PSIANGLE)

    @psi.setter
    def psi(self, angle):
        self._set_style(math.fmod(float(angle), 360.0), sv.PSIANGLE)

    @property
    def theta(self):
        """`float`: Eye origin view Theta angle in degrees.

        The Theta angle is the rotation of the eye origin ray about the
        Z-axis::

            >>> plot.view.theta = 24.3
        """
        return self._get_style(float, sv.THETAANGLE)

    @theta.setter
    def theta(self, angle):
        self._set_style(math.fmod(float(angle), 360.0), sv.THETAANGLE)

    @property
    def alpha(self):
        """`float`: Eye origin view Alpha angle in degrees.

        The Alpha angle is the twist about the eye origin ray::

            >>> plot.view.alpha = 95.0
        """
        return self._get_style(float, sv.ALPHAANGLE)

    @alpha.setter
    def alpha(self, angle):
        self._set_style(math.fmod(float(angle), 360.0), sv.ALPHAANGLE)

    @property
    def position(self):
        """`tuple`: 3D viewer position.

        The viewer position is the viewer's relation to the image::

            >>> plot.view.position
            (1.25, 3.2, 0.74)
            >>> plot.view.position.x
            1.25
            >>> plot.view.position = (2.5, 0.0, 1.0)
            >>> plot.view.position.y
            0.0
            >>> plot.view.position.z
            1.0

        .. seealso:: `distance`
        """
        return session.XYZ(self, sv.VIEWERPOSITION)

    @position.setter
    def position(self, pos):
        session.XYZ(self, sv.VIEWERPOSITION)[:] = pos

    @property
    def width(self):
        """`float`: 3D view width.

        The 3D view width is the amount of the plot (in X-axis units) in front
        of the viewer that may be seen.

        .. warning:: `width` cannot be set if `projection` is `Perspective`.

        Example usage::

            >>> plot.view.width = 1.5
        """
        return self._get_style(float, sv.VIEWWIDTH)

    @width.setter
    def width(self, value):
        if __debug__:
            if self._draw_in_perspective:
                raise TecplotValueError('view width cannot be set if drawing '
                                        'in perspective.')
        self._set_style(float(value), sv.VIEWWIDTH)

    @property
    def distance(self):
        """`float`: Get or set the view distance.

        The view distance is the distance from the viewer to the plane that is
        parallel to the screen and passes through the 3-D rotation origin.

        .. note:: Changing this value will also change the viewer `position`.

        .. seealso:: `position`

        Example usage::

            >>> plot.view.distance
            13.5
            >>> plot.view.distance = 10.0
            >>> plot.view.distance
            10.0
        """
        return _tecutil.ThreeDViewGetDistanceToRotateOriginPlane()

    @distance.setter
    @lock()
    def distance(self, value):
        if not _tecutil.Set3DEyeDistance(float(value)):
            raise TecplotSystemError()


class PolarView(LineView):
    """Adjust the way polar data is displayed.

    .. code-block:: python
        :emphasize-lines: 27

        import numpy as np
        import tecplot as tp
        from tecplot.constant import PlotType, ThetaMode

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

        plot.axes.r_axis.max = np.max(r)
        plot.axes.theta_axis.mode = ThetaMode.Radians

        plot.delete_linemaps()
        lmap = plot.add_linemap('Linemap', zone, dataset.variable('R'),
                                dataset.variable('Theta'))
        lmap.line.line_thickness = 0.8

        plot.view.fit()

        tp.export.save_png('view_polar.png', 600, supersample=3)

    .. figure:: /_static/images/view_polar.png
        :width: 300px
        :figwidth: 300px
    """
    def __init__(self, plot):
        super().__init__(plot, sv.POLARVIEW)

    @property
    def extents(self):
        """`tuple`: Viewport extents in radial data units.

        Extents are represented by the `tuple`: ``(x1, y1, x2, y2)`` and
        setting this effectively zooms the view of the data within the
        viewport. The values ``(x1, y1)`` and ``(x2, y2)`` are the lower-left
        and upper-right edges respectively and are in radial (data) units. The
        following example will set the bottom and left edges of the viewport to
        the radial value of ``-3`` and the top and right edges to the radial
        value of 5::

            >>> plot.view.extents = -3, -3, 5, 5
        """
        return session.RectPosition(self, sv.EXTENTS)

    @extents.setter
    def extents(self, values):
        session.RectPosition(self, sv.EXTENTS)[:] = values


@lock_attributes
class ReadOnlyViewport(session.Style):
    def __init__(self, axes):
        kw = dict(uniqueid=axes.plot.frame.uid)
        super().__init__(*axes._sv, **kw)

    @property
    def bottom(self):
        """`float` in percentage of frame height from the bottom of frame

        Example usage::

            >>> print(plot.axes.viewport.bottom)
            10.0
        """
        return self._get_style(float, sv.VIEWPORTPOSITION, sv.Y1)

    @property
    def left(self):
        """`float` in percentage of frame width from the left of the frame.

        Example usage::

            >>> print(plot.axes.viewport.left)
            10.0
        """
        return self._get_style(float, sv.VIEWPORTPOSITION, sv.X1)

    @property
    def right(self):
        """`float` in percentage of frame width from the left of the frame.

        Example usage::

            >>> print(plot.axes.viewport.right)
            90.0
        """
        return self._get_style(float, sv.VIEWPORTPOSITION, sv.X2)

    @property
    def top(self):
        """`float` in percentage of frame height from the bottom of the frame.

        Example usage::

            >>> print(plot.axes.viewport.top)
            90.0
        """
        return self._get_style(float, sv.VIEWPORTPOSITION, sv.Y2)


class Viewport(ReadOnlyViewport):
    bottom = ReadOnlyViewport.bottom
    left   = ReadOnlyViewport.left
    right  = ReadOnlyViewport.right
    top    = ReadOnlyViewport.top

    @bottom.setter
    def bottom(self, value):
        self._set_style(float(value), sv.VIEWPORTPOSITION, sv.Y1)

    @left.setter
    def left(self, value):
        self._set_style(float(value), sv.VIEWPORTPOSITION, sv.X1)

    @right.setter
    def right(self, value):
        self._set_style(float(value), sv.VIEWPORTPOSITION, sv.X2)

    @top.setter
    def top(self, value):
        self._set_style(float(value), sv.VIEWPORTPOSITION, sv.Y2)


class Cartesian2DViewport(Viewport):
    @property
    def nice_fit_buffer(self):
        """`float`: Tolerance for viewport/frame fit niceness.

        Example usage::

            >>> plot.axes.viewport.nice_fit_buffer = 20
        """
        return self._get_style(float, sv.VIEWPORTNICEFITBUFFER)

    @nice_fit_buffer.setter
    def nice_fit_buffer(self, value):
        self._set_style(float(value), sv.VIEWPORTNICEFITBUFFER)

    @property
    def top_snap_target(self):
        """`float`: Target value for top when being adjusted or dragged.

        Example usage::

            >>> plot.axes.viewport.top_snap_target = 90
        """
        return self._get_style(float, sv.VIEWPORTTOPSNAPTARGET)

    @top_snap_target.setter
    def top_snap_target(self, value):
        self._set_style(float(value), sv.VIEWPORTTOPSNAPTARGET)

    @property
    def top_snap_tolerance(self):
        """`float`: Tolerance for snapping to target value for top.

        Example usage::

            >>> plot.axes.viewport.top_snap_tolerance = 8
        """
        return self._get_style(float, sv.VIEWPORTTOPSNAPTOLERANCE)

    @top_snap_tolerance.setter
    def top_snap_tolerance(self, value):
        self._set_style(float(value), sv.VIEWPORTTOPSNAPTOLERANCE)


class PolarViewport(Viewport):
    @property
    def fill_color(self):
        """`Color`: Background fill color of the entire viewport.

        Example usage::

            >>> from tecplot.constant import Color
            >>> plot.axes.viewport.fill_color = Color.Blue
        """
        if self._get_style(bool, sv.VIEWPORTSTYLE, sv.ISFILLED):
            return self._get_style(Color, sv.VIEWPORTSTYLE, sv.FILLCOLOR)

    @fill_color.setter
    def fill_color(self, value):
        if value is None:
            self._set_style(False, sv.VIEWPORTSTYLE, sv.ISFILLED)
        else:
            self._set_style(True, sv.VIEWPORTSTYLE, sv.ISFILLED)
            self._set_style(Color(value), sv.VIEWPORTSTYLE, sv.FILLCOLOR)

    @property
    def show_border(self):
        """`bool`: Draw a border line around the viewport.

        Example usage::

            >>> plot.axes.viewport.show_border = True
        """
        return self._get_style(bool, sv.VIEWPORTSTYLE, sv.DRAWBORDER)

    @show_border.setter
    def show_border(self, value):
        self._set_style(bool(value), sv.VIEWPORTSTYLE, sv.DRAWBORDER)

    @property
    def border_thickness(self):
        """`float`: Border line thickness around the viewport.

        Example usage::

            >>> plot.axes.viewport.show_border = True
            >>> plot.axes.viewport.border_thickness = 0.8
        """
        return self._get_style(float, sv.VIEWPORTSTYLE, sv.LINETHICKNESS)

    @border_thickness.setter
    def border_thickness(self, value):
        self._set_style(float(value), sv.VIEWPORTSTYLE, sv.LINETHICKNESS)

    @property
    def border_color(self):
        """`Color`: Border line color around the viewport.

        Example usage::

            >>> from tecplot.constant import Color
            >>> plot.axes.viewport.show_border = True
            >>> plot.axes.viewport.border_thickness = 0.8
            >>> plot.axes.viewport.border_color = Color.Red
        """
        return self._get_style(Color, sv.VIEWPORTSTYLE, sv.COLOR)

    @border_color.setter
    def border_color(self, value):
        self._set_style(Color(value), sv.VIEWPORTSTYLE, sv.COLOR)
