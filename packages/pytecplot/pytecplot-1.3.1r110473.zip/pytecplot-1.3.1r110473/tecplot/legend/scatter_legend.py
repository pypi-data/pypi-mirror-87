from builtins import super

from ..tecutil import sv
from .. import session, tecutil
from . import legend


class ScatterLegend(legend.CategoryLegend):
    """Legend style for scatter plots.

    .. code-block:: python
        :emphasize-lines: 27-28

        from os import path
        import tecplot as tp
        from tecplot.constant import *

        examples_dir = tp.session.tecplot_examples_directory()
        infile = path.join(examples_dir, 'SimpleData', 'HeatExchanger.plt')
        dataset = tp.data.load_tecplot(infile)

        frame = tp.active_frame()
        frame.plot_type = PlotType.Cartesian2D
        plot = frame.plot()
        plot.show_scatter = True

        # make space for the legend
        plot.axes.viewport.right = 70
        plot.axes.x_axis.min = 4
        plot.axes.x_axis.max = 7

        # assign some shape and color to each fieldmap
        for i, fmap in enumerate(plot.fieldmaps()):
            for zone in fmap.zones:
                zone.name = 'Zone {}'.format(i)
            fmap.scatter.symbol().shape = GeomShape(i % 7)
            fmap.scatter.fill_mode = FillMode.UseSpecificColor
            fmap.scatter.fill_color = Color(i % 7)

        plot.scatter.legend.show = True
        plot.scatter.legend.row_spacing = 0.95

        tp.export.save_png('scatter_legend.png')

    .. figure:: /_static/images/scatter_legend.png
        :width: 300px
        :figwidth: 300px
    """
    def __init__(self, scatter):
        self.scatter = scatter
        super().__init__(scatter._sv, sv.LEGEND, **scatter._kw)

    @tecutil.inherited_property(legend.CategoryLegend)
    def box(self):
        """`text.TextBox`: Legend box attributes.

        Example usage::

            >>> from tecplot.constant import PlotType, Color
            >>> plot.scatter.legend.box.color = Color.Blue
        """

    @tecutil.inherited_property(legend.CategoryLegend)
    def show(self):
        """`bool`: Show or hide the legend.

        Example usage::

            >>> plot.scatter.legend.show = True
        """

    @tecutil.inherited_property(legend.CategoryLegend)
    def anchor_alignment(self):
        """`AnchorAlignment`: Anchor location of the legend.

        Example usage::

            >>> from tecplot.constant import AnchorAlignment
            >>> legend = plot.scatter.legend
            >>> legend.anchor_alignment = AnchorAlignment.BottomCenter
        """

    @tecutil.inherited_property(legend.CategoryLegend)
    def row_spacing(self):
        """`float`: Spacing between rows in the legend.

        Example usage::

            >>> plot.scatter.legend.row_spacing = 1.5
        """

    @tecutil.inherited_property(legend.CategoryLegend)
    def text_color(self):
        """`Color`: Color of legend text.

        Example usage::

            >>> from tecplot.constant import Color
            >>> plot.scatter.legend.text_color = Color.Blue
        """

    @tecutil.inherited_property(legend.CategoryLegend)
    def position(self):
        """`tuple`: Position as a percentage of frame width/height.

        The legend is automatically placed for you. You may specify the
        :math:`(x,y)` position of the legend by setting this value, where
        :math:`x` is the percentage of frame width, and :math:`y` is a
        percentage of frame height.

        Example usage::

            >>> plot.scatter.legend.position = (10, 30)
        """

    @tecutil.inherited_property(legend.CategoryLegend)
    def show_text(self):
        """`bool`: Show/hide mapping names in the legend.

        Example usage::

            >>> plot.scatter.legend.show_text = True
        """

    @tecutil.inherited_property(legend.CategoryLegend)
    def font(self):
        """`text.Font`: Legend font attributes.

        .. note::
            The font `size_units <tecplot.text.Font.size_units>` property
            may only be set to `Units.Frame` or `Units.Point`.

        Example usage::

            >>> plot.scatter.legend.font.italic = True
        """
