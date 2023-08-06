from builtins import int, super

from ..constant import *
from ..exception import *
from ..tecutil import sv
from .. import session, tecutil, text


class DataLabels(session.Style):
    @property
    def show_node_labels(self):
        """`bool`: Display labels at each node.

        Example usage::

            >>> plot.data_labels.show_node_labels = True
        """
        return self._get_style(bool, sv.SHOWNODELABELS)

    @show_node_labels.setter
    def show_node_labels(self, value):
        self._set_style(bool(value), sv.SHOWNODELABELS)

    @property
    def node_label_type(self):
        """`LabelType`: The value to be displayed for node labels.

        Possible values are `LabelType.Index` or `LabelType.VarValue`::

            >>> from tecplot.constant import LabelType
            >>> plot.data_labels.show_node_labels = True
            >>> plot.data_labels.node_label_type = LabelType.VarValue
        """
        return self._get_style(LabelType, sv.NODELABELTYPE)

    @node_label_type.setter
    def node_label_type(self, value):
        self._set_style(LabelType(value), sv.NODELABELTYPE)

    @property
    def index_step(self):
        """`int`: Step interval between labels.

        A value of 1 displays labels on all nodes or cells. Example usage::

            >>> plot.data_labels.show_node_labels = True
            >>> plot.data_labels.index_step = 10

        .. seealso:: `LinePlotDataLabels.step_mode` for line plots.
        """
        return self._get_style(int, sv.INDEXSKIP)

    @index_step.setter
    def index_step(self, value):
        self._set_style(int(value), sv.INDEXSKIP)

    @property
    def color_by_map(self):
        """`bool`: Inherit `Color` from the symbol or scatter mapping style.

        Example usage for linemaps::

            >>> from tecplot.constant import Color
            >>> plot.linemap(0).symbols.color = Color.Blue
            >>> plot.data_labels.show_node_labels = True
            >>> plot.data_labels.color_by_map = True

        Example usage for fieldmaps::

            >>> from tecplot.constant import Color
            >>> plot.fieldmap(0).scatter.color = Color.Yellow
            >>> plot.data_labels.show_node_labels = True
            >>> plot.data_labels.color_by_map = True
        """
        return self._get_style(bool, sv.COLORBYZONEMAP)

    @color_by_map.setter
    def color_by_map(self, value):
        self._set_style(bool(value), sv.COLORBYZONEMAP)

    @property
    def color(self):
        """`Color`: The `Color` of the data labels.

        Example usage::

            >>> from tecplot.constant import Color
            >>> plot.data_labels.show_node_labels = True
            >>> plot.data_labels.color = Color.LightBlue
        """
        return self._get_style(Color, sv.COLOR)

    @color.setter
    def color(self, value):
        self._set_style(Color(value), sv.COLOR)

    @property
    def show_box(self):
        """`bool`: Show a box around each label.

        This is `True` by default. Set to `False` to disable the box::

            >>> plot.data_labels.show_node_labels = True
            >>> plot.data_labels.show_box = False
        """
        return self._get_style(bool, sv.INCLUDEBOX)

    @show_box.setter
    def show_box(self, value):
        self._set_style(bool(value), sv.INCLUDEBOX)

    @property
    def font(self):
        """`text.Font`: Typeface control for all data labels.

        Example usage::

            >>> plot.data_labels.font.typeface = 'Times'
        """
        return text.Font(self)

    @property
    def label_format(self):
        """`text.LabelFormat`: Floating-point number format control.

        Example usage::

            >>> from tecplot.constant import NumberFormat
            >>> labels = plot.data_labels
            >>> labels.label_format.format_type = NumberFormat.Integer
        """
        return text.LabelFormat(self)


class FieldPlotDataLabels(DataLabels):
    """Node and cell labels for field plots.

    .. code-block:: python
        :emphasize-lines: 20-25

        from os import path
        import tecplot as tp
        from tecplot.constant import LabelType, NumberFormat, PlotType

        examples_dir = tp.session.tecplot_examples_directory()
        infile = path.join(examples_dir, 'SimpleData', 'RainierElevation.plt')
        dataset = tp.data.load_tecplot(infile)

        frame = tp.active_frame()
        plot = frame.plot(PlotType.Cartesian2D)
        plot.activate()
        plot.show_contour = True
        plot.contour(0).legend.show = False

        plot.axes.x_axis.min = -8500
        plot.axes.x_axis.max = 8200
        plot.axes.y_axis.min = -400
        plot.axes.y_axis.max = -150

        plot.data_labels.show_node_labels = True
        plot.data_labels.node_label_type = LabelType.VarValue
        plot.data_labels.node_variable = dataset.variable('E')
        plot.data_labels.index_step = 4
        plot.data_labels.label_format.format_type = NumberFormat.Integer
        plot.data_labels.show_box = False

        tp.export.save_png('field_plot_data_labels.png')

    ..  figure:: /_static/images/field_plot_data_labels.png
        :width: 300px
        :figwidth: 300px
    """
    def __init__(self, plot):
        self.plot = plot
        super().__init__(sv.GLOBALSCATTER, sv.DATALABELS, **plot._kw)

    @property
    def show_cell_labels(self):
        """`bool`: Display labels at each cell.

        Example usage::

            >>> plot.data_labels.show_cell_labels = True
        """
        return self._get_style(bool, sv.SHOWCELLLABELS)

    @show_cell_labels.setter
    def show_cell_labels(self, value):
        self._set_style(bool(value), sv.SHOWCELLLABELS)

    @property
    def cell_label_type(self):
        """`LabelType`: The value to be displayed for cell labels.

        Possible values are `LabelType.Index` or `LabelType.VarValue`::

            >>> plot.data_labels.show_cell_labels = True
            >>> plot.data_labels.cell_label_type = LabelType.VarValue
        """
        return self._get_style(LabelType, sv.CELLLABELTYPE)

    @cell_label_type.setter
    def cell_label_type(self, value):
        self._set_style(LabelType(value), sv.CELLLABELTYPE)

    @property
    def cell_variable_index(self):
        """`Index`: `Index` of the variable to use for cell labels.

        Example usage::

            >>> from tecplot.constant import LabelType
            >>> plot.data_labels.show_cell_labels = True
            >>> plot.data_labels.cell_label_type = LabelType.VarValue
            >>> plot.data_labels.cell_variable_index = 3
        """
        return self._get_style(tecutil.Index, sv.CELLLABELVAR)

    @cell_variable_index.setter
    def cell_variable_index(self, value):
        self._set_style(tecutil.Index(value), sv.CELLLABELVAR)

    @property
    def cell_variable(self):
        """`Variable`: `Variable` to use for cell labels.

        Example usage::

            >>> from tecplot.constant import LabelType
            >>> plot.data_labels.show_cell_labels = True
            >>> plot.data_labels.cell_label_type = LabelType.VarValue
            >>> plot.data_labels.cell_variable = dataset.variable('E')
        """
        i = self.cell_variable_index
        return self.plot.frame.dataset.variable(i)

    @cell_variable.setter
    def cell_variable(self, value):
        self.cell_variable_index = value.index

    @property
    def node_variable_index(self):
        """`Index`: `Index` of the variable to use for node labels.

        Example usage::

            >>> from tecplot.constant import LabelType
            >>> plot.data_labels.show_node_labels = True
            >>> plot.data_labels.node_label_type = LabelType.VarValue
            >>> plot.data_labels.node_variable_index = 3
        """
        return self._get_style(tecutil.Index, sv.NODELABELVAR)

    @node_variable_index.setter
    def node_variable_index(self, value):
        self._set_style(tecutil.Index(value), sv.NODELABELVAR)

    @property
    def node_variable(self):
        """`Variable`: `Variable` to use for node labels.

        Example usage::

            >>> from tecplot.constant import LabelType
            >>> plot.data_labels.show_node_labels = True
            >>> plot.data_labels.node_label_type = LabelType.VarValue
            >>> plot.data_labels.node_variable = dataset.variable('E')
        """
        i = self.node_variable_index
        return self.plot.frame.dataset.variable(i)

    @node_variable.setter
    def node_variable(self, value):
        self.node_variable_index = value.index


class LinePlotDataLabels(DataLabels):
    """Node labels for line plots.

    .. code-block:: python
        :emphasize-lines: 12-13

        from os import path
        import tecplot as tp
        from tecplot.constant import PlotType

        examples_dir = tp.session.tecplot_examples_directory()
        infile = path.join(examples_dir, 'SimpleData', 'SunSpots.plt')
        dataset = tp.data.load_tecplot(infile)

        frame = tp.active_frame()
        plot = frame.plot(PlotType.XYLine)
        plot.activate()
        plot.data_labels.show_node_labels = True
        plot.data_labels.index_step = 3

        tp.export.save_png('line_plot_data_labels.png')

    ..  figure:: /_static/images/line_plot_data_labels.png
        :width: 300px
        :figwidth: 300px
    """
    def __init__(self, plot):
        self.plot = plot
        super().__init__(sv.GLOBALLINEPLOT, sv.DATALABELS, **plot._kw)

    @property
    def step_mode(self):
        """`StepMode`: The scale to use when stepping through elements.

        Possible values are: `StepMode.ByIndex` and `StepMode.ByFrameUnits`.
        Example usage::

            >>> plot.data_labels.show_node_labels = True
            >>> plot.data_labels.step_mode = StepMode.ByFrameUnits
            >>> plot.data_labels.step_distance = 10.0
        """
        return self._get_style(StepMode, sv.SKIPMODE)

    @step_mode.setter
    def step_mode(self, value):
        self._set_style(StepMode(value), sv.SKIPMODE)

    @property
    def step_distance(self):
        """`float`: Distance between labels when stepping by frame units.

        Example usage::

            >>> plot.data_labels.show_node_labels = True
            >>> plot.data_labels.step_mode = StepMode.ByFrameUnits
            >>> plot.data_labels.step_distance = 10.0
        """
        return self._get_style(float, sv.DISTANCESKIP)

    @step_distance.setter
    def step_distance(self, value):
        self._set_style(float(value), sv.DISTANCESKIP)
