from builtins import super

from ..constant import *
from ..exception import *
from ..tecutil import  sv
from .. import session, tecutil, text


class Legend(session.Style):
    @property
    def box(self):
        """`text.TextBox`: Legend box attributes.

        Example usage::

            >>> from tecplot.constant import PlotType, Color
            >>> plot = frame.plot(PlotType.XYLine)
            >>> plot.legend.box.color = Color.Blue
        """
        return text.TextBox(self)

    @property
    def show(self):
        """`bool`: Show or hide the legend.

        Example usage::

            >>> from tecplot.constant import PlotType
            >>> legend = frame.plot(PlotType.XYLine).legend
            >>> legend.show = True
        """
        return self._get_style(bool, sv.SHOW)

    @show.setter
    def show(self, value):
        self._set_style(bool(value), sv.SHOW)

    @property
    def anchor_alignment(self):
        """`AnchorAlignment`: Anchor location of the legend.

        Example usage::

            >>> from tecplot.constant import AnchorAlignment, PlotType
            >>> legend = frame.plot(PlotType.XYLine).legend
            >>> legend.anchor_alignment = AnchorAlignment.BottomCenter
        """
        return self._get_style(AnchorAlignment, sv.ANCHORALIGNMENT)

    @anchor_alignment.setter
    def anchor_alignment(self, value):
        self._set_style(AnchorAlignment(value), sv.ANCHORALIGNMENT)

    @property
    def text_color(self):
        """`Color`: Color of legend text.

        Example usage::

            >>> from tecplot.constant import PlotType, Color
            >>> legend = frame.plot(PlotType.XYLine).legend
            >>> legend.text_color = Color.Blue
        """
        return self._get_style(Color, sv.TEXTCOLOR)

    @text_color.setter
    def text_color(self, value):
        self._set_style(Color(value), sv.TEXTCOLOR)

    @property
    def position(self):
        """`tuple`: Position as a percentage of frame width/height.

        The legend is automatically placed for you. You may specify the
        :math:`(x,y)` position of the legend by setting this value, where
        :math:`x` is the percentage of frame width, and :math:`y` is a
        percentage of frame height.

        Example usage::

            >>> from tecplot.constant import PlotType
            >>> legend = frame.plot(PlotType.XYLine).legend
            >>> legend.position = (10, 30)
        """
        return session.XY(self, sv.XYPOS)

    @position.setter
    def position(self, pos):
        session.XY(self, sv.XYPOS)[:] = pos


class TabularLegend(Legend):
    @property
    def row_spacing(self):
        """`float`: Spacing between rows in the legend.

        Example usage::

            >>> from tecplot.constant import PlotType
            >>> legend = frame.plot(PlotType.XYLine).legend
            >>> legend.row_spacing = 1.5
        """
        return self._get_style(float, sv.ROWSPACING)

    @row_spacing.setter
    def row_spacing(self, value):
        self._set_style(float(value), sv.ROWSPACING)


class CategoryLegend(TabularLegend):
    @property
    def show_text(self):
        """`bool`: Show/hide mapping names in the legend.

        Example usage::

            >>> from tecplot.constant import PlotType
            >>> plot = frame.plot(PlotType.XYLine)
            >>> plot.legend.show_text = True
        """
        return self._get_style(bool, sv.SHOWTEXT)

    @show_text.setter
    def show_text(self, value):
        self._set_style(bool(value), sv.SHOWTEXT)

    @property
    def font(self):
        """`text.Font`: Legend font attributes.

        .. note::
            The font `size_units <tecplot.text.Font.size_units>` property
            may only be set to `Units.Frame` or `Units.Point`.

        Example usage::

            >>> from tecplot.constant import PlotType
            >>> plot = frame.plot(PlotType.XYLine)
            >>> plot.legend.font.italic = True
        """
        return text.LegendFont(self)
