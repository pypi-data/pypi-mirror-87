from builtins import super

from ..constant import *
from ..exception import *
from ..tecutil import _tecutil_connector, sv
from .. import legend, session, tecutil, version


class RGBColoring(session.Style):
    """RGB coloring (multivariate contour) style control.

    .. code-block:: python
        :emphasize-lines: 39-53

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
        plot.rgb_coloring.legend.use_variable_for_green_label = False
        plot.rgb_coloring.legend.green_label = 'Pressure'
        plot.rgb_coloring.legend.use_variable_for_blue_label = False
        plot.rgb_coloring.legend.blue_label = 'Temperature'

        plot.fieldmaps().contour.flood_contour_group = plot.rgb_coloring

        tp.export.save_png('rgb_coloring.png')

    .. figure:: /_static/images/rgb_coloring.png
        :width: 300px
        :figwidth: 300px
    """
    def __init__(self, plot):
        self.plot = plot
        super().__init__(sv.GLOBALRGB, **plot._kw)

    def __eq__(self, other):
        return self.plot == other.plot

    def __ne__(self, other):
        return not (self == other)

    @property
    def index(self):
        """`Index`: Color `Index` for RGB Coloring.

        This property is used internally to identify it as a contour flooding
        option.
        """
        return tecutil.Index(Color.RGBColor.value)

    @property
    def legend(self):
        """`RGBColoringLegend`: Legend placement and style control.

        Example usage::

            >>> plot.rgb_coloring.legend.show = True
        """
        return legend.RGBColoringLegend(self)

    @property
    def mode(self):
        """`RGBMode`: Which channels to use for RGB coloring.

        Example usage::

            >>> from tecplot.constant import RGBMode
            >>> plot.rgb_coloring.mode = RGBMode.SpecifyRB
        """
        return self._get_style(RGBMode, sv.RGBMODE)

    @mode.setter
    def mode(self, value):
        self._set_style(RGBMode(value), sv.RGBMODE)

    @property
    def min_intensity(self):
        """`float`: `Variable` value at minimum intensity for each channel.

        This should typically be set to the minimum value of the data being
        plotted::

            >>> plot.rgb_coloring.min_intensity = dataset.variable('P').min()
        """
        return self._get_style(float, sv.RANGEMIN)

    @min_intensity.setter
    def min_intensity(self, value):
        self._set_style(float(value), sv.RANGEMIN)

    @property
    def max_intensity(self):
        """`float`: `Variable` value at maximum intensity for each channel.

        This should typically be set to the maximum value of the data being
        plotted::

            >>> plot.rgb_coloring.max_intensity = dataset.variable('P').max()
        """
        return self._get_style(float, sv.RANGEMAX)

    @max_intensity.setter
    def max_intensity(self, value):
        self._set_style(float(value), sv.RANGEMAX)

    def _ensure_valid_rgb_variables(self, index):
        """
            Note: this is essentially a work-around for behavior in the Tecplot
            engine where setting a single RGB channel would be reverted when
            the engine goes to an on-idle state. The engine was changed to
            allow setting a single channel in 2018 R3 but this function remains
            so that setting RGB channel variables still work with 2018 R2.
            However, it requires the suspend context which was not available
            in 2018 R1.
        """
        if _tecutil_connector.connected:
            if version.sdk_version_info < (2018, 2):
                msg = '''\
                    Setting RGB coloring variables
                    not supported in connected mode.'''
                raise TecplotOutOfDateEngineError((2018, 2), msg)
            r = self.red_variable_index
            g = self.green_variable_index
            b = self.blue_variable_index
            if any(x < 0 for x in (r, g, b)):
                r = tecutil.Index(index if r < 0 else r)
                g = tecutil.Index(index if g < 0 else g)
                b = tecutil.Index(index if b < 0 else b)
                with session.suspend():
                    self._set_style(r, sv.REDCHANNELVAR)
                    self._set_style(g, sv.GREENCHANNELVAR)
                    self._set_style(b, sv.BLUECHANNELVAR)

    @property
    def red_variable_index(self):
        """`Index`: `Variable` `Index` to use for the red channel.

        Example usage::

            >>> plot.rgb_coloring.red_variable_index = 5

        .. note::
            In connected mode, setting this property requires Tecplot 360
            version 2018 R2 or later.
        """
        return self._get_style(tecutil.Index, sv.REDCHANNELVAR)

    @red_variable_index.setter
    def red_variable_index(self, value):
        self._ensure_valid_rgb_variables(value)
        self._set_style(tecutil.Index(value), sv.REDCHANNELVAR)

    @property
    def red_variable(self):
        """`Variable`: `Variable` to use for the red channel.

        Example usage::

            >>> plot.rgb_coloring.red_variable = dataset.variable('Gas')

        .. note::
            In connected mode, setting this property requires Tecplot 360
            version 2018 R2 or later.
        """
        return self.plot.frame.dataset.variable(self.red_variable_index)

    @red_variable.setter
    def red_variable(self, variable):
        self.red_variable_index = variable.index

    @property
    def green_variable_index(self):
        """`Index`: `Variable` `Index` to use for the green channel.

        Example usage::

            >>> plot.rgb_coloring.green_variable_index = 3

        .. note::
            In connected mode, setting this property requires Tecplot 360
            version 2018 R2 or later.
        """
        return self._get_style(tecutil.Index, sv.GREENCHANNELVAR)

    @green_variable_index.setter
    def green_variable_index(self, value):
        self._ensure_valid_rgb_variables(value)
        self._set_style(tecutil.Index(value), sv.GREENCHANNELVAR)

    @property
    def green_variable(self):
        """`Variable`: `Variable` to use for the green channel.

        Example usage::

            >>> plot.rgb_coloring.green_variable = dataset.variable('Oil')

        .. note::
            In connected mode, setting this property requires Tecplot 360
            version 2018 R2 or later.
        """
        return self.plot.frame.dataset.variable(self.green_variable_index)

    @green_variable.setter
    def green_variable(self, variable):
        self.green_variable_index = variable.index

    @property
    def blue_variable_index(self):
        """`Index`: `Variable` `Index` to use for the blue channel.

        Example usage::

            >>> plot.rgb_coloring.blue_variable_index = 4

        .. note::
            In connected mode, setting this property requires Tecplot 360
            version 2018 R2 or later.
        """
        return self._get_style(tecutil.Index, sv.BLUECHANNELVAR)

    @blue_variable_index.setter
    def blue_variable_index(self, value):
        self._ensure_valid_rgb_variables(value)
        self._set_style(tecutil.Index(value), sv.BLUECHANNELVAR)

    @property
    def blue_variable(self):
        """`Variable`: `Variable` to use for the blue channel.

        Example usage::

            >>> plot.rgb_coloring.blue_variable = dataset.variable('Water')

        .. note::
            In connected mode, setting this property requires Tecplot 360
            version 2018 R2 or later.
        """
        return self.plot.frame.dataset.variable(self.blue_variable_index)

    @blue_variable.setter
    def blue_variable(self, variable):
        self.blue_variable_index = variable.index
