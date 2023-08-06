from builtins import str, super

from ..constant import *
from ..exception import *
from ..tecutil import sv
from .. import legend, session, tecutil, text
from . import labels, symbol


class PieChartsWedge(session.Style):
    """Individual wedge style control for pie charts.

    .. seealso:: `PieCharts`
    """
    def __init__(self, pie_charts, index):
        self.pie_charts = pie_charts
        self.index = tecutil.Index(index)
        self.plot = pie_charts.scatter.plot
        super().__init__(pie_charts._sv, sv.WEDGE, offset1=self.index,
                         **pie_charts._kw)

    @property
    def show(self):
        """`bool`

        .. note::

            At least one fieldmap must have scatter symbol shape set
            to `GeomShape.PieChart` before setting the show property
            of the wedges to `True`::

                from tecplot.constant import GeomShape
                plot.fieldmap(0).scatter.symbol().shape = GeomShape.PieChart
                plot.scatter.pie_charts.wedge(0).show = True
        """
        return self._get_style(bool, sv.INCLUDE)

    @show.setter
    def show(self, value):
        self._set_style(bool(value), sv.INCLUDE)

    @property
    def show_label(self):
        """`bool`"""
        return self._get_style(bool, sv.SHOWLABEL)

    @show_label.setter
    def show_label(self, value):
        self._set_style(bool(value), sv.SHOWLABEL)

    @property
    def label_text(self):
        """`str`"""
        return self._get_style(str, sv.LABELTEXT)

    @label_text.setter
    def label_text(self, value):
        self._set_style(str(value), sv.LABELTEXT)

    @property
    def color(self):
        """`Color`"""
        return self._get_style(Color, sv.COLOR)

    @color.setter
    def color(self, value):
        self._set_style(Color(value), sv.COLOR)

    @property
    def variable_index(self):
        """`Index`"""
        return self._get_style(tecutil.Index, sv.VAR)

    @variable_index.setter
    def variable_index(self, value):
        self._set_style(tecutil.Index(value), sv.VAR)

    @property
    def variable(self):
        """`Variable`"""
        return self.plot.frame.dataset.variable(self.variable_index)

    @variable.setter
    def variable(self, variable):
        self.variable_index = variable.index


class PieCharts(session.Style):
    """Pie charts displayed at each scatter point.

    .. code-block:: python
        :emphasize-lines: 46-59

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
        plot.show_scatter = True

        plot.axes.x_axis.min = 6
        plot.axes.x_axis.max = 8
        plot.axes.y_axis.min = 1.5
        plot.axes.y_axis.max = 3.0

        # Normalize variables to the range [0, 1]
        normalize_variable(dataset, 'T(K)')
        normalize_variable(dataset, 'P(N)')

        frame.add_text(r'Normalized Temperature in Red', (50, 95), color=Color.Red)
        frame.add_text(r'Normalized Pressure in Blue', (50, 92), color=Color.Blue)

        fmaps = plot.fieldmaps()
        fmaps.scatter.symbol().shape = GeomShape.PieChart
        fmaps.scatter.size = 4.0

        pie_charts = plot.scatter.pie_charts
        pie_charts.wedge(0).show = True
        pie_charts.wedge(0).show_label = False
        pie_charts.wedge(0).variable = dataset.variable('T(K) normalized')
        pie_charts.wedge(0).color = Color.Red

        pie_charts.wedge(1).show = True
        pie_charts.wedge(1).show_label = False
        pie_charts.wedge(1).variable = dataset.variable('P(N) normalized')
        pie_charts.wedge(1).color = Color.Blue

        tp.export.save_png('pie_charts.png')

    .. figure:: /_static/images/pie_charts.png
        :width: 300px
        :figwidth: 300px
    """
    def __init__(self, scatter):
        self.scatter = scatter
        super().__init__(scatter._sv, sv.PIECHARTS, **scatter._kw)

    @property
    def label_offset(self):
        """`float`"""
        return self._get_style(float, sv.LABELOFFSET)

    @label_offset.setter
    def label_offset(self, value):
        self._set_style(float(value), sv.LABELOFFSET)

    @property
    def label_text(self):
        """`str`"""
        return self._get_style(str, sv.LABELTEXT)

    @label_text.setter
    def label_text(self, value):
        self._set_style(str(value), sv.LABELTEXT)

    @property
    def label_color(self):
        """`Color`"""
        return self._get_style(Color, sv.LABELTEXTCOLOR)

    @label_color.setter
    def label_color(self, value):
        self._set_style(Color(value), sv.LABELTEXTCOLOR)

    @property
    def label_font(self):
        """`text.Font`"""
        return text.Font(self, sv.LABELTEXTSHAPE)

    @property
    def show_zero_value_wedge_labels(self):
        """`bool`"""
        return self._get_style(bool, sv.SHOWLABELFORZEROVALUEWEDGES)

    @show_zero_value_wedge_labels.setter
    def show_zero_value_wedge_labels(self, value):
        self._set_style(bool(value), sv.SHOWLABELFORZEROVALUEWEDGES)

    @property
    def start_angle(self):
        """`float`"""
        return self._get_style(float, sv.STARTANGLE)

    @start_angle.setter
    def start_angle(self, value):
        self._set_style(float(value), sv.STARTANGLE)

    def wedge(self, index):
        """`PieChartsWedge`"""
        return PieChartsWedge(self, index)


class Scatter(session.Style):
    """Plot-local scatter style settings.

    This class controls the style of drawn scatter points on a specific plot.

    .. code-block:: python
        :emphasize-lines: 15

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

        for z in dataset.zones():
            scatter = plot.fieldmap(z).scatter
            scatter.symbol_type = SymbolType.Geometry
            scatter.symbol().shape = GeomShape.Circle
            scatter.fill_mode = FillMode.UseSpecificColor
            scatter.fill_color = plot.contour(0)
            scatter.color = plot.contour(0)
            scatter.size_by_variable = True

        frame.add_text('Size of dots indicate relative pressure', (20, 80))

        # ensure consistent output between interactive (connected) and batch
        plot.contour(0).levels.reset_to_nice()

        tp.export.save_png('scatter.png')

    .. figure:: /_static/images/scatter.png
        :width: 300px
        :figwidth: 300px
    """
    def __init__(self, plot):
        self.plot = plot
        super().__init__(sv.GLOBALSCATTER, uniqueid=self.plot.frame.uid)

    @property
    def base_font(self):
        """`BaseFont`: Default typeface to use for text scatter symbols.

        Example usage::

            >>> plot.scatter.base_font.typeface = 'Times'
        """
        return text.BaseFont(*self._sv, **self._kw)

    @property
    def legend(self):
        """`ScatterLegend`: Scatter symbol legend.

        Example usage::

            >>> plot.scatter.legend.show = True
        """
        return legend.ScatterLegend(self)

    @property
    def pie_charts(self):
        return PieCharts(self)

    @property
    def reference_symbol(self):
        """`ScatterReferenceSymbol`: Reference symbol for scatter plots.

        The reference scatter symbol is only shown when the scatter symbols are
        sized by a `Variable` in the `Dataset`. Example::

            >>> plot.fieldmap(0).scatter.size_by_variable = True
            >>> plot.scatter.variable = dataset.variable('s')
            >>> plot.scatter.reference_symbol.show = True
        """
        return symbol.ScatterReferenceSymbol(self)

    @property
    def relative_size(self):
        """`float`: Relative size of the reference symbol.

        Relative size will be in ``cm`` when units are set to
        `RelativeSizeUnits.Page`. Example usage::

            >>> plot.scatter.relative_size = 20
        """
        return self._get_style(float, sv.RELATIVESIZE)

    @relative_size.setter
    def relative_size(self, value):
        self._set_style(float(value), sv.RELATIVESIZE)

    @property
    def relative_size_units(self):
        """`RelativeSizeUnits`: Use grid or page units for relative size.

        Relative size will be in ``cm`` when units are set to
        `RelativeSizeUnits.Page`. Example usage::

            >>> from tecplot.constant import RelativeSizeUnits
            >>> plot.scatter.relative_size_units = RelativeSizeUnits.Grid
            >>> plot.scatter.relative_size = 2.0
        """
        if self._get_style(bool, sv.RELATIVESIZEINGRIDUNITS):
            return RelativeSizeUnits.Grid
        else:
            return RelativeSizeUnits.Page

    @relative_size_units.setter
    def relative_size_units(self, value):
        value = RelativeSizeUnits(value) == RelativeSizeUnits.Grid
        self._set_style(value, sv.RELATIVESIZEINGRIDUNITS)

    @property
    def sphere_render_quality(self):
        """`SphereScatterRenderQuality`: render quality of spheres

        Example usage::

            >>> from tecplot.constant import *
            >>> plot.fieldmap(0).scatter.symbol().shape = GeomShape.Sphere
            >>> scatter = plot.scatter
            >>> scatter.sphere_render_quality = SphereScatterRenderQuality.Low
        """
        return self._get_style(SphereScatterRenderQuality,
                               sv.SPHERESCATTERRENDERQUALITY)

    @sphere_render_quality.setter
    def sphere_render_quality(self, value):
        self._set_style(SphereScatterRenderQuality(value),
                        sv.SPHERESCATTERRENDERQUALITY)

    @property
    def variable_index(self):
        """Zero-based index of the `Variable` used for size of scatter symbols.

        .. code-block:: python

            >>> plot.scatter.variable_index = dataset.variable('P').index
            >>> plot.fieldmap(0).scatter.size_by_variable = True

        The `Dataset` attached to this contour group's `Frame` is used, and
        the variable itself can be obtained through it::

            >>> scatter = plot.scatter
            >>> scatter_var = dataset.variable(scatter.variable_index)
            >>> scatter_var.index == scatter.variable_index
            True
        """
        return self._get_style(tecutil.Index, sv.VAR)

    @variable_index.setter
    def variable_index(self, index):
        self._set_style(tecutil.Index(index), sv.VAR)

    @property
    def variable(self):
        """The `Variable` to be used when sizing scatter symbols.

        The variable must belong to the `Dataset` attached to the `Frame`
        that holds this `ContourGroup`. Example usage::

            >>> plot.scatter.variable = dataset.variable('P')
            >>> plot.fieldmap(0).scatter.size_by_variable = True
        """
        return self.plot.frame.dataset.variable(self.variable_index)

    @variable.setter
    def variable(self, variable):
        self.variable_index = variable.index
