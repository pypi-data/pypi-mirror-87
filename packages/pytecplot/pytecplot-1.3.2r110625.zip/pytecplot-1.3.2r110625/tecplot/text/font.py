from builtins import str, super

from ..exception import *
from .. import constant, session
from ..tecutil import sv


class Font(session.Style):
    """Style of text objects such as titles and labels.

    This class controls the typeface and size of various text objects found
    in plots and axes:

    .. code-block:: python
        :emphasize-lines: 26-30

        from os import path
        import tecplot as tp
        from tecplot.constant import PlotType, Units, AxisTitleMode

        examples_dir = tp.session.tecplot_examples_directory()
        infile = path.join(examples_dir, 'OneraM6wing', 'OneraM6_SU2_RANS.plt')
        dataset = tp.data.load_tecplot(infile)

        frame = tp.active_frame()
        plot = frame.plot(PlotType.Cartesian2D)
        plot.activate()

        plot.show_contour = True

        xaxis = plot.axes.x_axis
        xaxis.title.title_mode = AxisTitleMode.UseText
        xaxis.title.text = 'Longitudinal (m)'
        xaxis.min, xaxis.max = 0, 1.2

        yaxis = plot.axes.y_axis
        yaxis.title.title_mode = AxisTitleMode.UseText
        yaxis.title.text = 'Transverse (m)'
        yaxis.min, yaxis.max = 0, 1.3

        for ax in [xaxis, yaxis]:
            ax.title.font.typeface = 'Times'
            ax.title.font.bold = False
            ax.title.font.italic = True
            ax.title.font.size_units = Units.Frame
            ax.title.font.size = 7

        # ensure consistent output between interactive (connected) and batch
        plot.contour(0).levels.reset_to_nice()

        tp.export.save_png('font.png', 600, supersample=3)

    ..  figure:: /_static/images/font.png
        :width: 300px
        :figwidth: 300px
    """
    def __init__(self, parent, sv_textshape=sv.TEXTSHAPE):
        self.parent = parent
        super().__init__(parent._sv, sv_textshape, **parent._kw)

    @property
    def bold(self):
        """`bool`: Use the bold version of the current typeface.

        Example::

            >>> axis.title.font.bold = True
        """
        return self._get_style(bool, sv.ISBOLD)

    @bold.setter
    def bold(self, value):
        self._set_style(bool(value), sv.ISBOLD)

    @property
    def italic(self):
        """`bool`: Use the italic version of the current typeface.

        Example::

            >>> axis.title.font.italic = True
        """
        return self._get_style(bool, sv.ISITALIC)

    @italic.setter
    def italic(self, value):
        self._set_style(bool(value), sv.ISITALIC)

    @property
    def size(self):
        """`float`: Height of the font. in units of `Font.size_units`.

        Example usage::

            >>> axis.title.font.size = 10
        """
        return self._get_style(float, sv.HEIGHT)

    @size.setter
    def size(self, value):
        self._set_style(float(value), sv.HEIGHT)

    @property
    def size_units(self):
        """`constant.Units`: Used by the size attribute.

        Possible values: `Units.Point`, `Units.Frame` (percentage of frame
        height). This example sets the axis title to 10% of the frame height::

            >>> from tecplot.constant import Units
            >>> axis.title.font.size_units = Units.Frame
            >>> axis.title.font.size = 10
        """
        return self._get_style(constant.Units, sv.SIZEUNITS)

    @size_units.setter
    def size_units(self, value):
        size = self.size
        self._set_style(constant.Units(value), sv.SIZEUNITS)
        self.size = size

    @property
    def typeface(self):
        """`str`: Specific font (or typeface) to use for text.

        This can be any font installed on the current system. If the font is
        not found, Times or Helvetica will be used when rendering the text.
        Example usage::

            >>> axis.title.font.typeface = 'Times'
        """
        return self._get_style(str, sv.FONTFAMILY)

    @typeface.setter
    def typeface(self, value):
        self._set_style(str(value), sv.FONTFAMILY)


class BaseFont(session.Style):
    """Plot-level or scatter font style fall-back settings.

    .. note::
        Base fonts are accessible directly from line plots
        (`XYLinePlot.base_font`, `PolarLinePlot.base_font`)::

            >>> frame.plot(PlotType.XYLine).base_font

        and the scatter style of field plots (`Scatter.base_font`)::

            >>> frame.plot(PlotType.Cartesian3D).scatter.base_font
    """
    @property
    def typeface(self):
        """`str`: Specific font (or typeface) to use for text.

        This can be any font installed on the current system. If the font is
        not found, Times or Helvetica will be used when rendering the text.
        Example usage::

            >>> line_plot.base_font.typeface = 'Times'
            >>> field_plot.scatter.base_font.typeface = 'Times'
        """
        return self._get_style(str, sv.BASEFONTFAMILY)

    @typeface.setter
    def typeface(self, value):
        self._set_style(str(value), sv.BASEFONTFAMILY)

    @property
    def bold(self):
        """`bool`: Use the bold version of the current typeface.

        Example::

            >>> line_plot.base_font.bold = True
            >>> field_plot.scatter.base_font.bold = True
        """
        return self._get_style(bool, sv.BASEFONTISBOLD)

    @bold.setter
    def bold(self, value):
        self._set_style(bool(value), sv.BASEFONTISBOLD)

    @property
    def italic(self):
        """`bool`: Use the italic version of the current typeface.

        Example::

            >>> line_plot.base_font.italic = True
            >>> field_plot.scatter.base_font.italic = True
        """
        return self._get_style(bool, sv.BASEFONTISITALIC)

    @italic.setter
    def italic(self, value):
        self._set_style(bool(value), sv.BASEFONTISITALIC)


class LegendFont(Font):
    """`LegendFont` is a font that restricts the setting of size_units."""

    @property
    def size_units(self):
        """`Units <constant.Units>`: Units used by the size attribute.

        Possible values: `Units.Point`, `Units.Frame` (percentage of frame
        height). This example sets the axis title to 10% of the frame height::

            >>> legend.font.size_units = Units.Frame
            >>> legend.font.size = 10
        """
        return self._get_style(constant.Units, sv.SIZEUNITS)

    @size_units.setter
    def size_units(self, value):
        value = constant.Units(value)
        if __debug__:
            if value not in (constant.Units.Frame, constant.Units.Point):
                msg = '''\
                    Legend font size units must be one of:
                    Units.Frame, Units.Point'''
                raise TecplotValueError(msg)
        self._set_style(value, sv.SIZEUNITS)
