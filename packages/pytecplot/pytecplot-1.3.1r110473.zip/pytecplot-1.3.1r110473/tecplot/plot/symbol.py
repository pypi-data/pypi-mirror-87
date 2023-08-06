from builtins import str, super

from collections.abc import Iterable

from ..constant import *
from ..exception import *
from .. import session, tecutil
from ..tecutil import sv


@tecutil.lock_attributes
class Symbol(object):
    def __init__(self, parent, svarg=sv.SYMBOLSHAPE):
        self.parent = parent
        self._sv = [svarg]

    def _get_style(self, rettype, *svargs):
        return self.parent._get_style(rettype, *(self._sv + list(svargs)))

    def _set_style(self, value, *svargs):
        self.parent._set_style(value, *(self._sv + list(svargs)))

    @property
    def _symbol_type(self):
        _stype = {
            True: SymbolType.Text,
            False: SymbolType.Geometry}
        isascii = self._get_style(bool, sv.ISASCII)
        if isinstance(isascii, Iterable):
            return tuple([_stype[i] for i in isascii])
        else:
            return _stype[isascii]

    @_symbol_type.setter
    def _symbol_type(self, value):
        value = SymbolType(value)
        if value is SymbolType.Text:
            self._set_style(True, sv.ISASCII)
        else:
            self._set_style(False, sv.ISASCII)


class TextSymbol(Symbol):
    """Text character for linemap symbols.

    Only a single character can be used.

    .. code-block:: python
        :emphasize-lines: 23,28

        from os import path
        import tecplot as tp
        from tecplot.constant import PlotType, Color, SymbolType, FillMode

        examples_dir = tp.session.tecplot_examples_directory()
        infile = path.join(examples_dir, 'SimpleData', 'Rainfall.dat')
        dataset = tp.data.load_tecplot(infile)

        frame = tp.active_frame()
        frame.plot_type = PlotType.XYLine
        plot = frame.plot()
        plot.show_symbols = True

        cols = [Color.DeepRed, Color.Blue, Color.Fern]
        chars = ['S','D','M']

        lmaps = plot.linemaps()
        lmaps.show = True
        lmaps.symbols.show = True
        lmaps.symbols.size = 2.5
        lmaps.symbols.color = Color.White
        lmaps.symbols.fill_mode = FillMode.UseSpecificColor
        lmaps.symbols.symbol_type = SymbolType.Text

        for lmap, color, character in zip(lmaps, cols, chars):
            lmap.line.color = color
            lmap.symbols.fill_color = color
            lmap.symbols.symbol().text = character

        plot.view.fit()

        # save image to file
        tp.export.save_png('linemap_symbols_text.png', 600, supersample=3)

    .. figure:: /_static/images/linemap_symbols_text.png
        :width: 300px
        :figwidth: 300px
    """
    def __init__(self, parent, svarg=sv.SYMBOLSHAPE):
        super().__init__(parent, svarg)
        self._sv += [sv.ASCIISHAPE]

    @property
    def text(self):
        """The ASCII character to use as the symbol to show

        .. note:: This is limited to a single character.

        Example usage::

            >>> from tecplot.constant import SymbolType
            >>> symbols = plot.linemap(0).symbols
            >>> symbols.symbol_type = SymbolType.Text
            >>> symbols.symbol().text = 'X'
        """
        return self._get_style(str, sv.ASCIICHAR)

    @text.setter
    def text(self, value):
        self._set_style(str(value)[0], sv.ASCIICHAR)

    @property
    def use_base_font(self):
        """`bool`: Use the base typeface when rendering text-based symbols.

        When `False`, the ``font_override`` attribute takes effect::

            >>> from tecplot.constant import SymbolType, Font
            >>> symbols = plot.linemap(0).symbols
            >>> symbols.symbol_type = SymbolType.Text
            >>> symbols.symbol().use_base_font = False
            >>> symbols.symbol().font_override = Font.Greek
        """
        return self._get_style(bool, sv.USEBASEFONT)

    @use_base_font.setter
    def use_base_font(self, value):
        self._set_style(bool(value), sv.USEBASEFONT)

    @property
    def font_override(self):
        """`constant.Font`: Typeface to use when rendering text-based symbols.

        Possible values: `constant.Font.Greek`, `constant.Font.Math` or
        `constant.Font.UserDefined`.

        The ``use_base_font`` attribute must be set to `False`::

            >>> from tecplot.constant import SymbolType, Font
            >>> symbols = plot.linemap(0).symbols
            >>> symbols.symbol_type = SymbolType.Text
            >>> symbols.symbol().use_base_font = False
            >>> symbols.symbol().font_override = Font.Greek
        """
        return self._get_style(Font, sv.FONTOVERRIDE)

    @font_override.setter
    def font_override(self, value):
        if __debug__:
            valid_typefaces = [Font.Greek, Font.Math, Font.UserDefined]
            if value not in valid_typefaces:
                msg = 'font_override must be one of: '
                msg += ' '.join(str(x) for x in valid_typefaces)
                raise TecplotLogicError(msg)
        self._set_style(Font(value), sv.FONTOVERRIDE)


class TextScatterSymbol(TextSymbol):
    """Text character for scatter plots.

    Only a single character can be used.

    .. code-block:: python
        :emphasize-lines: 14,23-26,29-30

        from os import path
        import tecplot as tp
        from tecplot.constant import (Color, PlotType, PointsToPlot, SymbolType,
                                          GeomShape, FillMode)

        examples_dir = tp.session.tecplot_examples_directory()
        infile = path.join(examples_dir, 'SimpleData', 'HeatExchanger.plt')
        dataset = tp.data.load_tecplot(infile)

        frame = tp.active_frame()
        frame.plot_type = PlotType.Cartesian2D
        plot = frame.plot()
        plot.show_shade = True
        plot.show_scatter = True

        # get handle to a collection of all fieldmaps
        fmaps = plot.fieldmaps()

        fmaps.points.points_to_plot = PointsToPlot.SurfaceCellCenters
        fmaps.points.step = (4,4)
        fmaps.shade.color = Color.LightBlue

        fmaps.scatter.fill_mode = FillMode.UseSpecificColor
        fmaps.scatter.fill_color = Color.Yellow
        fmaps.scatter.size = 3
        fmaps.scatter.symbol_type = SymbolType.Text

        for i, fmap in enumerate(fmaps):
            fmap.scatter.color = Color((i % 4) + 13)
            fmap.scatter.symbol().text = hex(i)[-1]

        tp.export.save_png('fieldmap_scatter_text.png', 600, supersample=3)

    .. figure:: /_static/images/fieldmap_scatter_text.png
        :width: 300px
        :figwidth: 300px
    """

    @tecutil.inherited_property(TextSymbol)
    def text(self):
        """The ASCII character to use as the symbol to show

        .. note:: This is limited to a single character.

        Example usage::

            >>> from tecplot.constant import SymbolType
            >>> scatter = plot.fieldmap(0).scatter
            >>> scatter.symbol_type = SymbolType.Text
            >>> scatter.symbol().text = 'X'
        """

    @tecutil.inherited_property(TextSymbol)
    def use_base_font(self):
        """`bool`: Use the base typeface when rendering text-based scatter.

        When `False`, the ``font_override`` attribute takes effect::

            >>> from tecplot.constant import SymbolType, Font
            >>> scatter = plot.fieldmap(0).scatter
            >>> scatter.symbol_type = SymbolType.Text
            >>> scatter.symbol().use_base_font = False
            >>> scatter.symbol().font_override = Font.Greek
        """

    @tecutil.inherited_property(TextSymbol)
    def font_override(self):
        """`constant.Font`: Typeface to use when rendering text-based scatter.

        Possible values: `constant.Font.Greek`, `constant.Font.Math` or
        `constant.Font.UserDefined`.

        The ``use_base_font`` attribute must be set to `False`::

            >>> from tecplot.constant import SymbolType, Font
            >>> scatter = plot.fieldmap(0).scatter
            >>> scatter.symbol_type = SymbolType.Text
            >>> scatter.symbol().use_base_font = False
            >>> scatter.symbol().font_override = Font.Math
        """


class GeometrySymbol(Symbol):
    """Geometric shape for linemap symbols.

    .. code-block:: python
        :emphasize-lines: 24,30

        from os import path
        import tecplot as tp
        from tecplot.constant import (PlotType, Color, GeomShape, SymbolType,
                                      FillMode)

        examples_dir = tp.session.tecplot_examples_directory()
        infile = path.join(examples_dir, 'SimpleData', 'Rainfall.dat')
        dataset = tp.data.load_tecplot(infile)

        frame = tp.active_frame()
        frame.plot_type = PlotType.XYLine
        plot = frame.plot()
        plot.show_symbols = True

        cols = [Color.DeepRed, Color.Blue, Color.Fern]
        shapes = [GeomShape.Square, GeomShape.Circle, GeomShape.Del]

        lmaps = plot.linemaps()

        lmaps.show = True
        lmaps.symbols.show = True
        lmaps.symbols.size = 4.5
        lmaps.symbols.fill_mode = FillMode.UseSpecificColor
        lmaps.symbols.symbol_type = SymbolType.Geometry

        for lmap, color, shape in zip(lmaps, cols, shapes):
            lmap.line.color = color
            lmap.symbols.color = color
            lmap.symbols.fill_color = color
            lmap.symbols.symbol().shape = shape

        plot.view.fit()

        # save image to file
        tp.export.save_png('linemap_symbols_geometry.png', 600, supersample=3)

    .. figure:: /_static/images/linemap_symbols_geometry.png
        :width: 300px
        :figwidth: 300px
    """

    @property
    def shape(self):
        """`GeomShape`: Geometric shape to use when plotting linemap symbols.

        Possible values: `Square <GeomShape.Square>`, `Del`, `Grad`, `RTri`,
        `LTri`, `Diamond`, `Circle <GeomShape.Circle>`, `Cube`, `Sphere`,
        `Octahedron`, `Point <GeomShape.Point>`.

        Example usage::

            >>> from tecplot.constant import SymbolType, GeomShape
            >>> symbols = plot.linemap(0).symbols
            >>> symbols.symbol_type = SymbolType.Geometry
            >>> symbols.symbol().shape = GeomShape.Diamond
        """
        return self._get_style(GeomShape, sv.GEOMSHAPE)

    @shape.setter
    def shape(self, value):
        self._set_style(GeomShape(value), sv.GEOMSHAPE)


class GeometryScatterSymbol(GeometrySymbol):
    """Geometric shape for scatter plots.

    .. code-block:: python
        :emphasize-lines: 13,22-26,29-31

        from os import path
        import tecplot as tp
        from tecplot.constant import (Color, PlotType, PointsToPlot, SymbolType,
                                      GeomShape, FillMode)

        examples_dir = tp.session.tecplot_examples_directory()
        infile = path.join(examples_dir, 'SimpleData', 'HeatExchanger.plt')
        dataset = tp.data.load_tecplot(infile)

        frame = tp.active_frame()
        frame.plot_type = PlotType.Cartesian2D
        plot = frame.plot()
        plot.show_scatter = True

        # get handle to a collection of all fieldmaps
        fmaps = plot.fieldmaps()

        points = fmaps.points
        points.points_to_plot = PointsToPlot.SurfaceCellCenters
        points.step = (2,2)

        scatter = fmaps.scatter
        scatter.fill_mode = FillMode.UseSpecificColor
        scatter.size = 2
        scatter.line_thickness = 0.5
        scatter.symbol_type = SymbolType.Geometry

        for i, fmap in enumerate(fmaps):
            fmap.scatter.symbol().shape = GeomShape(i%7)
            fmap.scatter.color = Color(i)
            fmap.scatter.fill_color = Color(i + plot.num_fieldmaps)

        tp.export.save_png('fieldmap_scatter_geometry.png', 600, supersample=3)

    .. figure:: /_static/images/fieldmap_scatter_geometry.png
        :width: 300px
        :figwidth: 300px
    """

    @tecutil.inherited_property(GeometrySymbol)
    def shape(self):
        """`GeomShape`: Geometric shape to use when plotting scatter points.

        Possible values: `Square <GeomShape.Square>`, `Del`, `Grad`, `RTri`,
        `LTri`, `Diamond`, `Circle <GeomShape.Circle>`, `Cube`, `Sphere`,
        `Octahedron`, `Point <GeomShape.Point>`.

        Example usage::

            >>> from tecplot.constant import SymbolType, GeomShape
            >>> scatter = plot.fieldmap(0).scatter
            >>> scatter.symbol_type = SymbolType.Geometry
            >>> scatter.symbol().shape = GeomShape.Diamond
        """


class ScatterReferenceSymbol(session.Style):
    """Reference symbol for scatter plots.

    .. note::
        The reference scatter symbol is only shown when the scatter symbols are
        sized by a `Variable` in the `Dataset`.

    .. code-block:: python
        :emphasize-lines: 17-22

        from os import path
        import tecplot as tp
        from tecplot.constant import *

        examples_dir = tp.session.tecplot_examples_directory()
        infile = path.join(examples_dir, 'SimpleData', 'HeatExchanger.plt')
        dataset = tp.data.load_tecplot(infile)

        frame = tp.active_frame()
        frame.plot_type = PlotType.Cartesian2D
        plot = frame.plot()
        plot.contour(0).variable = dataset.variable('T(K)')
        plot.show_scatter = True

        plot.scatter.variable = dataset.variable('P(N)')

        plot.scatter.reference_symbol.show = True
        plot.scatter.reference_symbol.symbol().shape = GeomShape.Circle
        plot.scatter.reference_symbol.magnitude = plot.scatter.variable.max()
        plot.scatter.reference_symbol.color = Color.Green
        plot.scatter.reference_symbol.fill_color = Color.Green
        plot.scatter.reference_symbol.position = (20, 81)

        frame.add_text('Size of dots indicate relative pressure', (23, 80))

        for z in dataset.zones():
            scatter = plot.fieldmap(z).scatter
            scatter.symbol_type = SymbolType.Geometry
            scatter.symbol().shape = GeomShape.Circle
            scatter.fill_mode = FillMode.UseSpecificColor
            scatter.fill_color = plot.contour(0)
            scatter.color = plot.contour(0)
            scatter.size_by_variable = True

        # ensure consistent output between interactive (connected) and batch
        plot.contour(0).levels.reset_to_nice()

        tp.export.save_png('scatter_reference_symbol.png')

    .. figure:: /_static/images/scatter_reference_symbol.png
        :width: 300px
        :figwidth: 300px
    """
    def __init__(self, scatter):
        self.scatter = scatter
        super().__init__(scatter._sv, sv.REFSCATSYMBOL, **scatter._kw)

    @property
    def show(self):
        """`bool`: Display a reference scatter symbol on the plot.

        Example usage::

            >>> plot.fieldmap(0).scatter.size_by_variable = True
            >>> plot.scatter.variable = dataset.variable('s')
            >>> plot.scatter.reference_symbol.show = True
        """
        return self._get_style(bool, sv.SHOW)

    @show.setter
    def show(self, value):
        self._set_style(bool(value), sv.SHOW)

    @property
    def color(self):
        """`Color`: The `Color` of the reference symbol.

        Example usage::

            >>> from tecplot.constant import Color
            >>> plot.scatter.reference_symbol.color = Color.Blue
        """
        return self._get_style(Color, sv.COLOR)

    @color.setter
    def color(self, value):
        self._set_style(Color(value), sv.COLOR)

    @property
    def filled(self):
        """`bool`: Fill the background area behind the reference symbol.

        The background can be filled with a color or disabled (made
        transparent) by setting this property to `False`::

            >>> plot.scatter.reference_symbol.filled = True
        """
        return self._get_style(bool, sv.ISFILLED)

    @filled.setter
    def filled(self, value):
        self._set_style(bool(value), sv.ISFILLED)

    @property
    def fill_color(self):
        """`Color`: The fill `Color` of the reference symbol.

        Example usage::

            >>> from tecplot.constant import Color
            >>> plot.scatter.reference_symbol.fill_color = Color.Blue
        """
        return self._get_style(Color, sv.FILLCOLOR)

    @fill_color.setter
    def fill_color(self, value):
        self._set_style(Color(value), sv.FILLCOLOR)

    @property
    def position(self):
        """`tuple`: The :math:`(x, y)` position of the reference symbol.

        This position is in `Frame` percentage units::

            >>> plot.scatter.reference_symbol.position = (50, 50)
        """
        return session.XY(self, sv.XYPOS)

    @position.setter
    def position(self, values):
        session.XY(self, sv.XYPOS)[:] = values

    @property
    def magnitude(self):
        """`float`: Symbol size relative to data variable ranges.

        Example usage::

            >>> plot.scatter.reference_symbol.magnitude = 10.0
        """
        return self._get_style(float, sv.MAGNITUDE)

    @magnitude.setter
    def magnitude(self, value):
        self._set_style(float(value), sv.MAGNITUDE)

    @property
    def line_thickness(self):
        """`float`: Edge line thickness for geometry reference symbols.

        Example usage::

            >>> plot.scatter.reference_symbol.line_thickness = 2.5
        """
        return self._get_style(float, sv.LINETHICKNESS)

    @line_thickness.setter
    def line_thickness(self, value):
        self._set_style(float(value), sv.LINETHICKNESS)

    @property
    def symbol_type(self):
        """`SymbolType`: The type of symbol to display.

        Example usage::

            >>> from tecplot.constant import SymbolType
            >>> reference_symbol = plot.scatter.reference_symbol
            >>> reference_symbol.symbol_type = SymbolType.Text
        """
        return Symbol(self)._symbol_type

    @symbol_type.setter
    def symbol_type(self, value):
        Symbol(self)._symbol_type = value

    def symbol(self, symbol_type=None):
        """`TextSymbol` or `GeometrySymbol`: Style control the displayed symbol.

        Example usage::

            >>> from tecplot.constant import GeomShape
            >>> reference_symbol = plot.scatter.reference_symbol
            >>> reference_symbol.symbol = GeomShape.Sphere
        """
        _dispatch = {
            SymbolType.Text: TextSymbol,
            SymbolType.Geometry: GeometrySymbol}
        return _dispatch[symbol_type or self.symbol_type](self)
