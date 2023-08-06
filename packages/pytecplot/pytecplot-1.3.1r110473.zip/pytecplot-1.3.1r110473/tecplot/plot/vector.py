from builtins import super

from collections import namedtuple

from ..tecutil import _tecutil
from ..constant import *
from ..exception import *
from .. import session
from ..tecutil import Index, lock, color_spec, sv
from ..text import LabelFormat, Font


class ReferenceVectorLabel(session.Style):
    """Label for the reference vector.

    See the example under `ReferenceVector`.
    """
    def __init__(self, ref_vector):
        self.ref_vector = ref_vector
        super().__init__(ref_vector._sv, sv.MAGNITUDELABEL, **ref_vector._kw)

    @property
    def show(self):
        """`bool`: Print a label next to the reference vector.

        Example usage::

            >>> ref_vector = plot.vector.reference_vector
            >>> ref_vector.show = True
            >>> ref_vector.label.show = True
        """
        return self._get_style(bool, sv.SHOW)

    @show.setter
    def show(self, value):
        self._set_style(bool(value), sv.SHOW)

    @property
    def color(self):
        """`Color`: `Color` of the reference vector label.

        Example usage::

            >>> from tecplot.constant import Color
            >>> ref_vector = plot.vector.reference_vector
            >>> ref_vector.show = True
            >>> ref_vector.label.show = True
            >>> ref_vector.label.color = Color.Red
        """
        return self._get_style(Color, sv.TEXTCOLOR)

    @color.setter
    def color(self, value):
        self._set_style(Color(value), sv.TEXTCOLOR)

    @property
    def offset(self):
        """`float` (percent of frame height): Distance from the reference vector to the associated label.

        Example usage::

            >>> ref_vector = plot.vector.reference_vector
            >>> ref_vector.show = True
            >>> ref_vector.label.show = True
            >>> ref_vector.label.offset = 10
        """
        return self._get_style(float, sv.OFFSET)

    @offset.setter
    def offset(self, value):
        self._set_style(float(value), sv.OFFSET)

    @property
    def font(self):
        """`text.Font`: Typeface of the reference vector label.

        Example usage::

            >>> ref_vector = plot.vector.reference_vector
            >>> ref_vector.show = True
            >>> ref_vector.label.show = True
            >>> ref_vector.label.font.size = 6
        """
        return Font(self)

    @property
    def format(self):
        """`LabelFormat`: Number formatting control for the reference vector label.

        Example usage::

            >>> from tecplot.constant import NumberFormat
            >>> ref_vector = plot.vector.reference_vector
            >>> ref_vector.show = True
            >>> ref_vector.label.show = True
            >>> ref_vector.label.format.format_type = NumberFormat.Exponential
        """
        return LabelFormat(self)


class ReferenceVector(session.Style):
    """Vector field reference vector.

    The reference vector is a single arrow with an optional label indicating
    the value of the shown reference length:

    .. code-block:: python
        :emphasize-lines: 34-41

        from os import path
        import tecplot as tp
        from tecplot.constant import *

        examples_dir = tp.session.tecplot_examples_directory()
        infile = path.join(examples_dir, 'SimpleData', 'VortexShedding.plt')
        tp.data.load_tecplot(infile)

        frame = tp.active_frame()
        dataset = frame.dataset
        plot = frame.plot(PlotType.Cartesian2D)

        for txt in frame.texts():
            frame.delete_text(txt)

        vector_contour = plot.contour(0)
        vector_contour.variable = dataset.variable('T(K)')
        vector_contour.colormap_name = 'Magma'
        vector_contour.colormap_filter.reversed = True
        vector_contour.legend.show = False
        base_contour = plot.contour(1)
        base_contour.variable = dataset.variable('P(N/M2)')
        base_contour.colormap_name = 'GrayScale'
        base_contour.colormap_filter.reversed = True
        base_contour.legend.show = False

        vector = plot.vector
        vector.u_variable = dataset.variable('U(M/S)')
        vector.v_variable = dataset.variable('V(M/S)')
        vector.relative_length = 1E-5
        vector.arrowhead_size = 0.2
        vector.arrowhead_angle = 16

        ref_vector = vector.reference_vector
        ref_vector.show = True
        ref_vector.position = 50, 95
        ref_vector.line_thickness = 0.4
        ref_vector.label.show = True
        ref_vector.label.format.format_type = NumberFormat.FixedFloat
        ref_vector.label.format.precision = 1
        ref_vector.magnitude = 100

        fmap = plot.fieldmap(0)
        fmap.contour.flood_contour_group = base_contour
        fmap.vector.color = vector_contour
        fmap.vector.line_thickness = 0.4

        plot.show_contour = True
        plot.show_streamtraces = False
        plot.show_vector = True

        plot.axes.y_axis.min = -0.005
        plot.axes.y_axis.max = 0.005
        plot.axes.x_axis.min = -0.002
        plot.axes.x_axis.max = 0.008

        tp.export.save_png('vector2d_reference.png', 600, supersample=3)

    ..  figure:: /_static/images/vector2d_reference.png
        :width: 300px
        :figwidth: 300px
    """
    def __init__(self, vector):
        self.vector = vector
        super().__init__(vector._sv, sv.REFVECTOR, **vector._kw)

    @property
    def show(self):
        """`bool`: Draw the reference vector.

        Example usage::

            >>> plot.vector.reference_vector.show = True
        """
        return self._get_style(bool, sv.SHOW)

    @show.setter
    def show(self, value):
        self._set_style(bool(value), sv.SHOW)

    @property
    def color(self):
        """`Color`: `Color` of the reference vector.

        Example usage::

            >>> from tecplot.constant import Color
            >>> ref_vector = plot.vector.reference_vector
            >>> ref_vector.show = True
            >>> ref_vector.color = Color.Red
        """
        return self._get_style(Color, sv.COLOR)

    @color.setter
    def color(self, value):
        self._set_style(Color(value), sv.COLOR)

    @property
    def position(self):
        """`tuple`: :math:`(x,y)` of the reference vector in percent of frame height.

        Example usage::

            >>> ref_vector = plot.vector.reference_vector
            >>> ref_vector.show = True
            >>> ref_vector.position = (50, 5)  # bottom, center
        """
        return session.XY(self, sv.XYPOS)

    @position.setter
    def position(self, pos):
        session.XY(self, sv.XYPOS)[:] = pos

    @property
    def magnitude(self):
        """`float` (data units): Length of the reference vector.

        Example usage::

            >>> ref_vector = plot.vector.reference_vector
            >>> ref_vector.show = True
            >>> ref_vector.magnitude = 2
        """
        return self._get_style(float, sv.MAGNITUDE)

    @magnitude.setter
    def magnitude(self, value):
        self._set_style(float(value), sv.MAGNITUDE)

    @property
    def angle(self):
        """`float` (degrees): Degrees counter-clockwise to rotate the reference vector.

        Example usage::

            >>> ref_vector = plot.vector.reference_vector
            >>> ref_vector.show = True
            >>> ref_vector.angle = 90  # vertical, up
        """
        return self._get_style(float, sv.ANGLE)

    @angle.setter
    def angle(self, value):
        self._set_style(float(value), sv.ANGLE)

    @property
    def line_thickness(self):
        """`float` (percentage of frame height): reference vector line thickness.

        Example usage::

            >>> ref_vector = plot.vector.reference_vector
            >>> ref_vector.show = True
            >>> ref_vector.line_thickness = 0.3
        """
        return self._get_style(float, sv.LINETHICKNESS)

    @line_thickness.setter
    def line_thickness(self, value):
        self._set_style(float(value), sv.LINETHICKNESS)

    @property
    def label(self):
        """`ReferenceVectorLabel`: reference vector label style control.

        Example usage::

            >>> ref_vector = plot.vector.reference_vector
            >>> ref_vector.show = True
            >>> ref_vector.label.show = True
        """
        return ReferenceVectorLabel(self)


class Vector(session.Style):
    def __init__(self, plot, *svargs):
        self.plot = plot
        super().__init__(*svargs, uniqueid=self.plot.frame.uid)

    @property
    def arrowhead_angle(self):
        """`float` (degrees): Angle between the vector body and the head line.

        Example usage::

            >>> plot.vector.arrowhead_angle = 10
        """
        return self._get_style(float, sv.ARROWHEADANGLE)

    @arrowhead_angle.setter
    def arrowhead_angle(self, value):
        self._set_style(float(value), sv.ARROWHEADANGLE)

    @property
    def arrowhead_fraction(self):
        """`float` (ratio): Size of the arrowhead when sizing by fraction.

        The ``size_arrowhead_by_fraction`` property must be set to `True` for
        this to take effect::

            >>> plot.vector.size_arrowhead_by_fraction = True
            >>> plot.vector.arrowhead_fraction = 0.4
        """
        return self._get_style(float, sv.HEADSIZEASFRACTION)

    @arrowhead_fraction.setter
    def arrowhead_fraction(self, value):
        self._set_style(float(value), sv.HEADSIZEASFRACTION)

    @property
    def arrowhead_size(self):
        """`float` (percent of frame height): Size of arrowhead when sizing by frame height.

        The ``size_arrowhead_by_fraction`` property must be set to `False` for
        this to take effect::

            >>> plot.vector.size_arrowhead_by_fraction = False
            >>> plot.vector.arrowhead_size = 4
        """
        return self._get_style(float, sv.HEADSIZEINFRAMEUNITS)

    @arrowhead_size.setter
    def arrowhead_size(self, value):
        self._set_style(float(value), sv.HEADSIZEINFRAMEUNITS)

    @property
    def relative_length(self):
        """`float` (grid units or cm per magnitude): Magnitude-varying length of the vector line.

        When ``use_relative`` is `True`, the length of the vectors will be
        relative to the magnitude of the velocity vector values in the data
        field, scaled by this parameter which is either grid-units or
        centimeters per unit magnitude depending on the value of
        ``use_grid_units``::

            >>> plot.vector.use_relative = True
            >>> plot.vector.use_grid_units = True
            >>> plot.vector.relative_length = 0.003
        """
        with self.plot.activated():
            return self._get_style(float, sv.RELATIVELENGTH)

    @relative_length.setter
    def relative_length(self, value):
        self._set_style(float(value), sv.RELATIVELENGTH)

    @property
    def use_even_spacing(self):
        """`bool`: Use even spacing for vectors.   
        
        When `True` this will selectively remove vectors from the plot to 
        approximately enforce the display intervals specified by ``even_spacing``.

        Turn on even spacing::

            >>> plot.vector.use_even_spacing = True
        """
        return self._get_style(bool, sv.USEEVENSPACING)

    @use_even_spacing.setter
    def use_even_spacing(self, value):
        self._set_style(bool(value), sv.USEEVENSPACING)

    @property
    def use_grid_units(self):
        """`bool`: Use grid-units when determining the relative length.

        This takes effect only if ``use_relative`` is `True`. If `False`,
        ``relative_length`` will be in cm per magnitude::

            >>> plot.vector.use_relative = True
            >>> plot.vector.use_grid_units = False
            >>> plot.vector.relative_length = 0.010
        """
        return self._get_style(bool, sv.RELATIVELENGTHINGRIDUNITS)

    @use_grid_units.setter
    def use_grid_units(self, value):
        self._set_style(bool(value), sv.RELATIVELENGTHINGRIDUNITS)

    @property
    def size_arrowhead_by_fraction(self):
        """`bool`: Base arrowhead size on length of vector line.

        Example usage::

            >>> plot.vector.size_arrowhead_by_fraction = True
            >>> plot.vector.relative_length = 0.1
        """
        return self._get_style(bool, sv.SIZEHEADBYFRACTION)

    @size_arrowhead_by_fraction.setter
    def size_arrowhead_by_fraction(self, value):
        self._set_style(bool(value), sv.SIZEHEADBYFRACTION)

    @property
    def length(self):
        """`float` (percent of plot height): Length of all vectors when not using relative sizing.

        Example usage::

            >>> plot.vector.use_relative = False
            >>> plot.vector.length = 5
        """
        return self._get_style(float, sv.UNIFORMLENGTH)

    @length.setter
    def length(self, value):
        self._set_style(float(value), sv.UNIFORMLENGTH)

    @property
    def use_relative(self):
        """`bool`: Use relative sizing for vector lines.

        This determines whether ``length`` or ``relative_length`` are used to
        size the arrow lines. Example usage::

            >>> plot.vector.use_relative = False
            >>> plot.vector.relative_length = 0.5
        """
        return self._get_style(bool, sv.USERELATIVE)

    @use_relative.setter
    def use_relative(self, value):
        self._set_style(bool(value), sv.USERELATIVE)

    @property
    def reference_vector(self):
        """`ReferenceVector`: Vector field reference vector.

        Example usage::

            >>> plot.vector.reference_vector.show = True
        """
        return ReferenceVector(self)

    @property
    def u_variable_index(self):
        """`int` (Zero-based index): :math:`U`-component `Variable` index of the plotted vectors.

        Vectors are plotted as :math:`(u,v,w)`. Example usage::

            >>> plot.vector.u_variable_index = 3
        """
        return self._get_style(Index, sv.UVAR)

    @u_variable_index.setter
    def u_variable_index(self, index):
        self._set_style(Index(index), sv.UVAR)

    @property
    def u_variable(self):
        """`Variable`: :math:`U`-component `Variable` of the plotted vectors.

        Vectors are plotted as :math:`(u,v,w)`. Example usage::

            >>> plot.vector.u_variable = dataset.variable('Pressure X')
        """
        return self.plot.frame.dataset.variable(self.u_variable_index)

    @u_variable.setter
    def u_variable(self, variable):
        self.u_variable_index = variable.index

    @property
    def v_variable_index(self):
        """`int` (Zero-based index): :math:`V`-component `Variable` index of the plotted vectors.

        Vectors are plotted as :math:`(u,v,w)`. Example usage::

            >>> plot.vector.v_variable_index = 4
        """
        return self._get_style(Index, sv.VVAR)

    @v_variable_index.setter
    def v_variable_index(self, index):
        self._set_style(Index(index), sv.VVAR)

    @property
    def v_variable(self):
        """`Variable`: :math:`V`-component `Variable` of the plotted vectors.

        Vectors are plotted as :math:`(u,v,w)`. Example usage::

            >>> plot.vector.v_variable = dataset.variable('Pressure Y')
        """
        return self.plot.frame.dataset.variable(self.v_variable_index)

    @v_variable.setter
    def v_variable(self, variable):
        self.v_variable_index = variable.index

    @lock()
    def reset_even_spacing(self):
        """Reset the even vector spacing.

        Example usage::

           >>> plot.vector.reset_even_spacing()
        """
        with self.plot.frame.activated():
            if not _tecutil.ResetVectorSpacing():
                raise TecplotSystemError()

    @lock()
    def reset_length(self):
        """Reset the vector length.

        Example usage::

           >>> plot.vector.reset_length()
        """
        with self.plot.frame.activated():
            if not _tecutil.ResetVectorLength():
                raise TecplotSystemError()


class Vector2D(Vector):
    """Vector field style control for Cartesian 2D plots.

    This object controls the style of the vectors that are plotted according to
    the vector properties under fieldmaps. The :math:`(u,v)` components are
    set using this class as well as attributes such as length, arrow-head size
    and the reference vector. This example shows how to show the vector field,
    adjusting the arrows color and thickness:

    .. code-block:: python
        :emphasize-lines: 22-28

        from os import path
        import tecplot as tp
        from tecplot.constant import *

        examples_dir = tp.session.tecplot_examples_directory()
        infile = path.join(examples_dir, 'SimpleData', '3ElementWing.lpk')
        tp.load_layout(infile)

        frame = tp.active_frame()
        dataset = frame.dataset
        plot = frame.plot(PlotType.Cartesian2D)

        frame.background_color = Color.Black
        for axis in plot.axes:
            axis.show = False

        plot.axes.x_axis.min = -0.2
        plot.axes.x_axis.max = 0.3
        plot.axes.y_axis.min = -0.2
        plot.axes.y_axis.max = 0.15

        vect = plot.vector
        vect.u_variable = dataset.variable('U(M/S)')
        vect.v_variable = dataset.variable('V(M/S)')
        vect.relative_length = 0.00025
        vect.size_arrowhead_by_fraction = False
        vect.arrowhead_size = 4
        vect.arrowhead_angle = 10

        plot.show_contour = False
        plot.show_streamtraces = False
        plot.show_edge = True
        plot.show_vector = True

        cont = plot.contour(0)
        cont.variable = dataset.variable('P(N/M2)')
        cont.colormap_name = 'Diverging - Blue/Yellow/Red'
        cont.levels.reset_levels(80000, 90000, 100000, 110000, 120000)

        plot.fieldmaps().show = False

        fmap = plot.fieldmap(3)
        fmap.show = True
        fmap.edge.color = Color.White
        fmap.edge.line_thickness = 1
        fmap.points.step = 5
        fmap.vector.color = cont
        fmap.vector.line_thickness = 0.5

        tp.export.save_png('vector2d.png', 600, supersample=3)

    ..  figure:: /_static/images/vector2d.png
        :width: 300px
        :figwidth: 300px
    """
    def __init__(self, plot):
        super().__init__(plot, sv.GLOBALTWODVECTOR)

    @property
    def even_spacing(self):
        """`tuple`: Spacing for even vectors.

        Set the spacing values in axial directions for even spaced vectors.
        When ``use_even_spacing`` is turned on this will selectively remove 
        vectors so that only one vector occupies each grid region defined 
        by the spacing.  Spacing is aligned with the X and Y axes.

        Example of setting spacing in X to 0.1 and Y to 0.2::

            >>> plot.vector.use_even_spacing = True
            >>> plot.vector.even_spacing = (0.1, 0.2)
        """
        style = session.Style(sv.GLOBALTWODVECTOR, uniqueid=self.plot.frame.uid)
        return session.XY(style, sv.EVENSPACING)

    @even_spacing.setter
    def even_spacing(self, values):
        style = session.Style(sv.GLOBALTWODVECTOR, uniqueid=self.plot.frame.uid)
        session.XY(style, sv.EVENSPACING)[:] = values


class Vector3D(Vector):
    """Vector field style control for Cartesian 3D plots.

    This object controls the style of the vectors that are plotted according to
    the vector properties under fieldmaps. The :math:`(u,v,w)` components are
    set using this class as well as attributes such as length, arrow-head size
    and the reference vector. See the `example for 2D vector plots <Vector2D>`.
    """
    def __init__(self, plot):
        super().__init__(plot, sv.GLOBALTHREEDVECTOR)

    @property
    def w_variable_index(self):
        """`int` (Zero-based index): :math:`W`-component `Variable` index of the plotted vectors.

        Vectors are plotted as :math:`(u,v,w)`. Example usage::

            >>> plot.vector.w_variable_index = 5
        """
        return self._get_style(Index, sv.WVAR)

    @w_variable_index.setter
    def w_variable_index(self, index):
        self._set_style(Index(index), sv.WVAR)

    @property
    def w_variable(self):
        """`Variable`: :math:`W`-component `Variable` of the plotted vectors.

        Vectors are plotted as :math:`(u,v,w)`. Example usage::

            >>> plot.vector.w_variable = dataset.variable('Pressure Z')
        """
        return self.plot.frame.dataset.variable(self.w_variable_index)

    @w_variable.setter
    def w_variable(self, variable):
        self.w_variable_index = variable.index

    @property
    def even_spacing(self):
        """`tuple`: Spacing for even vectors.

        Set the spacing values in axial directions for even spaced vectors.
        When ``use_even_spacing`` is turned on this will selectively remove 
        vectors so that only one vector occupies each grid region defined 
        by the spacing.  Spacing is aligned with the X, Y, and Z axes.

        Example of setting spacing in X to 0.1, Y to 0.2 and Z to 0.3::

            >>> plot.vector.use_even_spacing = True
            >>> plot.vector.even_spacing = (0.1, 0.2, 0.3)
        """
        style = session.Style(sv.GLOBALTHREEDVECTOR, uniqueid=self.plot.frame.uid)
        return session.XYZ(style, sv.EVENSPACING)

    @even_spacing.setter
    def even_spacing(self, values):
        style = session.Style(sv.GLOBALTHREEDVECTOR, uniqueid=self.plot.frame.uid)
        session.XYZ(style, sv.EVENSPACING)[:] = values
