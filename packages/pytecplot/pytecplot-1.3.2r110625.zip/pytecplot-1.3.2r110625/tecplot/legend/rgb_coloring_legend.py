from builtins import str, super

from ..constant import *
from ..tecutil import sv
from .. import tecutil
from . import legend


class RGBColoringLegend(legend.Legend):
    """Legend for RGB coloring (multivariate contour) plots.

    .. note::
        The RGB coloring legend will only show when an active fieldmap's
        contour is being flooded by RGB.

    .. code-block:: python
        :emphasize-lines: 46-48

        import os
        import numpy as np

        import tecplot as tp
        from tecplot.constant import *

        def normalize_variable(dataset, varname, nsigma=2):
            '''
            Normalize a variable such that the specified number of standard deviations
            are within the range [0.5, 1] and the mean is transformed to 0.5. The
            new variable will append " normalized" to the original variable's name.
            '''
            with tp.session.suspend():
                newvarname = varname + ' normalized'
                dataset.add_variable(newvarname)
                data = np.concatenate([z.values(varname).as_numpy_array()
                                       for z in dataset.zones()])
                vmin = data.mean() - nsigma * data.std()
                vmax = data.mean() + nsigma * data.std()
                for z in dataset.zones():
                    arr = z.values(varname).as_numpy_array()
                    z.values(newvarname)[:] = (arr - vmin) / (vmax - vmin)


        examples_dir = tp.session.tecplot_examples_directory()
        infile = os.path.join(examples_dir, 'SimpleData', 'HeatExchanger.plt')
        dataset = tp.data.load_tecplot(infile)

        frame = tp.active_frame()
        plot = frame.plot(PlotType.Cartesian2D)
        plot.show_contour = True

        # Variables must be normalized relative to each other
        # to make effective use of RGB coloring.
        normalize_variable(dataset, 'T(K)')
        normalize_variable(dataset, 'P(N)')

        plot.rgb_coloring.mode = RGBMode.SpecifyGB

        # all three channel variables must be set even if
        # we are only contouring on two of them.
        plot.rgb_coloring.red_variable = dataset.variable(0)
        plot.rgb_coloring.green_variable = dataset.variable('P(N) normalized')
        plot.rgb_coloring.blue_variable = dataset.variable('T(K) normalized')

        plot.rgb_coloring.legend.show = True
        plot.rgb_coloring.legend.green_label = 'Pressure'
        plot.rgb_coloring.legend.blue_label = 'Temperature'

        plot.fieldmaps().contour.flood_contour_group = plot.rgb_coloring

        tp.export.save_png('rgb_coloring_legend.png')

    .. figure:: /_static/images/rgb_coloring_legend.png
        :width: 300px
        :figwidth: 300px
    """
    def __init__(self, rgb_coloring):
        self.rgb_coloring = rgb_coloring
        super().__init__(rgb_coloring._sv, sv.LEGEND, **rgb_coloring._kw)

    @tecutil.inherited_property(legend.CategoryLegend)
    def box(self):
        """`text.TextBox`: Legend box attributes.

        Example usage::

            >>> from tecplot.constant import Color
            >>> plot.rgb_coloring.legend.box.fill_color = Color.Yellow
        """

    @tecutil.inherited_property(legend.CategoryLegend)
    def show(self):
        """`bool`: Display the RGB coloring legend.

        Example usage::

            >>> plot.rgb_coloring.legend.show = True
        """

    @tecutil.inherited_property(legend.CategoryLegend)
    def anchor_alignment(self):
        """`AnchorAlignment`: Anchor location of the legend.

        Example usage::

            >>> from tecplot.constant import AnchorAlignment
            >>> legend = plot.rgb_coloring.legend
            >>> legend.anchor_alignment = AnchorAlignment.BottomCenter
        """

    @tecutil.inherited_property(legend.CategoryLegend)
    def text_color(self):
        """`Color`: Color of legend text.

        Example usage::

            >>> from tecplot.constant import Color
            >>> legend = plot.rgb_coloring.legend
            >>> legend.text_color = Color.Blue
        """

    @tecutil.inherited_property(legend.CategoryLegend)
    def position(self):
        """`tuple`: Position as a percentage of frame width/height.

        The legend is automatically placed for you. You may specify the
        :math:`(x,y)` position of the legend by setting this value, where
        :math:`x` is the percentage of frame width, and :math:`y` is a
        percentage of frame height.

        Example usage::

            >>> plot.rgb_coloring.legend.position = (20, 80)
        """

    @tecutil.inherited_property(legend.CategoryLegend)
    def font(self):
        """`text.Font`: Legend font attributes.

        .. note::
            The font `size_units <tecplot.text.Font.size_units>` property
            may only be set to `Units.Frame` or `Units.Point`.

        Example usage::

            >>> plot.rgb_coloring.legend.font.italic = True
        """

    @property
    def show_labels(self):
        """`bool`: Show the RGB channel labels.

        Example usage::

            >>> legend = plot.rgb_coloring.legend
            >>> legend.show_labels = True
            >>> legend.red_label = 'Variable A'
            >>> legend.green_label = 'Variable B'
            >>> legend.blue_label = 'Variable C'
        """
        return self._get_style(bool, sv.SHOWLABELS)

    @show_labels.setter
    def show_labels(self, value):
        self._set_style(bool(value), sv.SHOWLABELS)

    @property
    def height(self):
        """`float`: Size of RGB coloring legend

        Example usage::

            >>> plot.rgb_coloring.legend.height = 20
        """
        return self._get_style(float, sv.HEIGHT)

    @height.setter
    def height(self, value):
        self._set_style(float(value), sv.HEIGHT)

    @property
    def orientation(self):
        """`RGBLegendOrientation`: Placement of the RGB channels on the legend.

        The first color is on the bottom left, the second is on the bottom
        right, and the third is on top. Example usage::

            >>> from tecplot.constant import RGBLegendOrientation
            >>> legend = plot.rgb_coloring.legend
            >>> legend.orientation = RGBLegendOrientation.RBG
        """
        return self._get_style(RGBLegendOrientation, sv.RGBLEGENDORIENTATION)

    @orientation.setter
    def orientation(self, value):
        self._set_style(RGBLegendOrientation(value), sv.RGBLEGENDORIENTATION)

    @property
    def use_variable_for_red_label(self):
        """`bool`: Use the `Variable` name for the red channel.

        Example usage::

            >>> plot.rgb_coloring.legend.use_variable_for_red_label = False
            >>> plot.rgb_coloring.legend.red_label = 'gas'
        """
        return self._get_style(bool, sv.USEREDVARNAME)

    @use_variable_for_red_label.setter
    def use_variable_for_red_label(self, value):
        self._set_style(bool(value), sv.USEREDVARNAME)

    @property
    def red_label(self):
        """`str`: Label to use for the red channel.

        This can be set to a string (which may be empty) but the
        `use_variable_for_red_label` property must be set to `False` for this
        label to be shown::

            >>> plot.rgb_coloring.legend.use_variable_for_red_label = False
            >>> plot.rgb_coloring.legend.red_label = 'gas'
        """
        return self._get_style(str, sv.REDCHANNELLABEL)

    @red_label.setter
    def red_label(self, value):
        self._set_style(str(value), sv.REDCHANNELLABEL)

    @property
    def use_variable_for_green_label(self):
        """`bool`: Use the `Variable` name for the green channel.

        Example usage::

            >>> plot.rgb_coloring.legend.use_variable_for_green_label = False
            >>> plot.rgb_coloring.legend.green_label = 'gas'
        """
        return self._get_style(bool, sv.USEGREENVARNAME)

    @use_variable_for_green_label.setter
    def use_variable_for_green_label(self, value):
        self._set_style(bool(value), sv.USEGREENVARNAME)

    @property
    def green_label(self):
        """`str`: Label to use for the green channel.

        This can be set to a string (which may be empty) but the
        `use_variable_for_green_label` property must be set to `False` for this
        label to be shown::

            >>> plot.rgb_coloring.legend.use_variable_for_green_label = False
            >>> plot.rgb_coloring.legend.green_label = 'oil'
        """
        return self._get_style(str, sv.GREENCHANNELLABEL)

    @green_label.setter
    def green_label(self, value):
        self._set_style(str(value), sv.GREENCHANNELLABEL)

    @property
    def use_variable_for_blue_label(self):
        """`bool`: Use the `Variable` name for the blue channel.

        Example usage::

            >>> plot.rgb_coloring.legend.use_variable_for_blue_label = False
            >>> plot.rgb_coloring.legend.blue_label = 'gas'
        """
        return self._get_style(bool, sv.USEBLUEVARNAME)

    @use_variable_for_blue_label.setter
    def use_variable_for_blue_label(self, value):
        self._set_style(bool(value), sv.USEBLUEVARNAME)

    @property
    def blue_label(self):
        """`str`: Label to use for the blue channel.

        This can be set to a string (which may be empty) but the
        `use_variable_for_blue_label` property must be set to `False` for this
        label to be shown::

            >>> plot.rgb_coloring.legend.use_variable_for_blue_label = False
            >>> plot.rgb_coloring.legend.blue_label = 'water'
        """
        return self._get_style(str, sv.BLUECHANNELLABEL)

    @blue_label.setter
    def blue_label(self, value):
        self._set_style(str(value), sv.BLUECHANNELLABEL)
