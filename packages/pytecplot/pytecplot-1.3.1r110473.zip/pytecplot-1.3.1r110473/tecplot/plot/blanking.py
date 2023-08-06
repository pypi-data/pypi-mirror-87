from builtins import super

from ..tecutil import sv
from .. import constant, exception, session, tecutil


class ValueBlankingConstraint(session.Style):
    """Value blanking constraint for cartesian 3D and line plots.

    .. seealso:: `ValueBlankingCartesian3D`
    """
    def __init__(self, blanking, index):
        if __debug__:
            if index < 0 or index > 7:
                raise exception.TecplotIndexError
        self.blanking = blanking
        super().__init__(blanking._sv, sv.CONSTRAINT,
                         offset1=tecutil.Index(index),
                         uniqueid=blanking.plot.frame.uid)

    @property
    def variable_index(self):
        """`Index`: Index of the `Variable` to be blanked.

        Example usage::

            >>> from tecplot.constant import ConstraintOp2Mode
            >>> constraint = plot.value_blanking.constraint(0)
            >>> constraint.compare_by = ConstraintOp2Mode.UseVar
            >>> constraint.variable_index = 1
        """
        return self._get_style(tecutil.Index, sv.VARA)

    @variable_index.setter
    def variable_index(self, value):
        self._set_style(tecutil.Index(value), sv.VARA)

    @property
    def variable(self):
        """`Variable`: The `Variable` to be blanked.

        Example usage::

            >>> from tecplot.constant import ConstraintOp2Mode
            >>> constraint = plot.value_blanking.constraint(0)
            >>> constraint.compare_by = ConstraintOp2Mode.UseVar
            >>> constraint.variable = dataset.variable('s')
        """
        return self.blanking.plot.frame.dataset.variable(self.variable_index)

    @variable.setter
    def variable(self, value):
        self.variable_index = value.index

    @property
    def comparison_value(self):
        """`float`: Constant value for blanking.

        The variable will be blanked according to this constant value, using
        the `comparison_operator` for this constraint, when the `compare_by`
        attribute is set to `ConstraintOp2Mode.UseConstant`::

            >>> from tecplot.constant import ConstraintOp2Mode, RelOp
            >>> constraint = plot.value_blanking.constraint(0)
            >>> constraint.active = True
            >>> constraint.compare_by = ConstraintOp2Mode.UseConstant
            >>> constraint.comparison_operator = RelOp.LessThanOrEqual
            >>> constraint.comparison_value = 3.14
        """
        return self._get_style(float, sv.VALUECUTOFF)

    @comparison_value.setter
    def comparison_value(self, value):
        self._set_style(float(value), sv.VALUECUTOFF)

    @property
    def comparison_variable_index(self):
        """`Index`: `Index` of the `Variable` to determine when to blank.

        The variable will be blanked according to values in this "comparison"
        variable, using the `comparison_operator` for this constraint, when the
        `compare_by` attribute is set to `ConstraintOp2Mode.UseVar`::

            >>> from tecplot.constant import ConstraintOp2Mode, RelOp
            >>> constraint = plot.value_blanking.constraint(0)
            >>> constraint.active = True
            >>> constraint.compare_by = ConstraintOp2Mode.UseVar
            >>> constraint.comparison_operator = RelOp.LessThanOrEqual
            >>> constraint.comparison_variable_index = 2
        """
        return self._get_style(tecutil.Index, sv.VARB)

    @comparison_variable_index.setter
    def comparison_variable_index(self, value):
        self._set_style(tecutil.Index(value), sv.VARB)

    @property
    def comparison_variable(self):
        """`Variable`: The `Variable` to determine when to blank.

        The variable will be blanked according to values in this "comparison"
        variable, using the `comparison_operator` for this constraint, when the
        `compare_by` attribute is set to `ConstraintOp2Mode.UseVar`::

            >>> from tecplot.constant import ConstraintOp2Mode, RelOp
            >>> constraint = plot.value_blanking.constraint(0)
            >>> constraint.active = True
            >>> constraint.compare_by = ConstraintOp2Mode.UseVar
            >>> constraint.comparison_operator = RelOp.LessThanOrEqual
            >>> constraint.comparison_variable = dataset.variable('s')
        """
        return self.blanking.plot.frame.dataset.variable(
            self.comparison_variable_index)

    @comparison_variable.setter
    def comparison_variable(self, value):
        self.comparison_variable_index = value.index

    @property
    def compare_by(self):
        """`ConstraintOp2Mode`: Compare against a constant or `Variable`.

        This controls what is used in the comparison for blanking. Possible
        values are: `ConstraintOp2Mode.UseConstant` and
        `ConstraintOp2Mode.UseVar`::

            >>> from tecplot.constant import ConstraintOp2Mode, RelOp
            >>> constraint = plot.value_blanking.constraint(0)
            >>> constraint.active = True
            >>> constraint.compare_by = ConstraintOp2Mode.UseConstant
            >>> constraint.comparison_operator = RelOp.LessThanOrEqual
            >>> constraint.comparison_value = 3.14
        """
        return self._get_style(constant.ConstraintOp2Mode,
                               sv.CONSTRAINTOP2MODE)

    @compare_by.setter
    def compare_by(self, value):
        self._set_style(constant.ConstraintOp2Mode(value),
                        sv.CONSTRAINTOP2MODE)

    @property
    def comparison_operator(self):
        """`RelOp`: The relationship to use to determine blanking.

        This controls what comparison relation is used for blanking. Possible
        values are `RelOp.LessThanOrEqual`, `RelOp.GreaterThanOrEqual`,
        `RelOp.LessThan`, `RelOp.GreaterThan`, `RelOp.EqualTo` and
        `RelOp.NotEqualTo`::

            >>> from tecplot.constant import ConstraintOp2Mode, RelOp
            >>> constraint = plot.value_blanking.constraint(0)
            >>> constraint.active = True
            >>> constraint.compare_by = ConstraintOp2Mode.UseConstant
            >>> constraint.comparison_operator = RelOp.LessThanOrEqual
            >>> constraint.comparison_value = 3.14
        """
        return self._get_style(constant.RelOp, sv.RELOP)

    @comparison_operator.setter
    def comparison_operator(self, value):
        self._set_style(constant.RelOp(value), sv.RELOP)

    @property
    def active(self):
        """`bool`: Include value blanking.

        Toggle-on to include this constraint for value blanking on the plot::

            >>> plot.value_blanking.constraint(0).active = True
        """
        return self._get_style(bool, sv.INCLUDE)

    @active.setter
    def active(self, value):
        self._set_style(bool(value), sv.INCLUDE)


class ValueBlankingConstraintCartesian2D(ValueBlankingConstraint):
    """Value blanking constraint for cartesian 2D plots.

    .. seealso:: `ValueBlankingCartesian2D`
    """
    @property
    def show_line(self):
        """`bool`: Show constraint boundary.

        Toggle-on to display a line that separates the region of your data that
        is blanked from the region which is not blanked::

            >>> plot.value_blanking.constraint(0).show_line = True
        """
        return self._get_style(bool, sv.SHOW)

    @show_line.setter
    def show_line(self, value):
        self._set_style(bool(value), sv.SHOW)

    @property
    def color(self):
        """`Color`: `Color` of the constraint boundary line.

        Example usage::

            >>> from tecplot.constant import Color
            >>> plot.value_blanking.constraint(0).show_line = True
            >>> plot.value_blanking.constraint(0).color = Color.Red
        """
        return self._get_style(constant.Color, sv.COLOR)

    @color.setter
    def color(self, value):
        self._set_style(constant.Color(value), sv.COLOR)

    @property
    def line_thickness(self):
        """`float`: Width of the constraint boundary line.

        Example usage::

            >>> plot.value_blanking.constraint(0).show_line = True
            >>> plot.value_blanking.constraint(0).line_thickness = 1.5
        """
        return self._get_style(float, sv.LINETHICKNESS)

    @line_thickness.setter
    def line_thickness(self, value):
        self._set_style(float(value), sv.LINETHICKNESS)

    @property
    def line_pattern(self):
        """`LinePattern`: Dash pattern of the constraint boundary line.

        Example usage::

            >>> from tecplot.constant import LinePattern
            >>> constraint = plot.value_blanking.constraint(0)
            >>> constraint.show_line = True
            >>> constraint.line_pattern = LinePattern.Dashed
        """
        return self._get_style(constant.LinePattern, sv.LINEPATTERN)

    @line_pattern.setter
    def line_pattern(self, value):
        self._set_style(constant.LinePattern(value), sv.LINEPATTERN)

    @property
    def pattern_length(self):
        """`float`: Length of the dash pattern for the boundary line.
        Example usage::

            >>> from tecplot.constant import LinePattern
            >>> constraint = plot.value_blanking.constraint(0)
            >>> constraint.show_line = True
            >>> constraint.line_pattern = LinePattern.Dashed
            >>> constraint.pattern_length = 1.5
        """
        return self._get_style(float, sv.PATTERNLENGTH)

    @pattern_length.setter
    def pattern_length(self, value):
        self._set_style(float(value), sv.PATTERNLENGTH)


class ValueBlanking(session.Style):
    """Value blanking for line plots.

    .. code-block:: python
        :emphasize-lines: 21-27

        from os import path
        import tecplot as tp
        from tecplot.constant import *

        examples_dir = tp.session.tecplot_examples_directory()
        infile = path.join(examples_dir, 'SimpleData', 'Rainfall.dat')
        dataset = tp.data.load_tecplot(infile)

        frame = tp.active_frame()
        frame.plot_type = PlotType.XYLine
        plot = frame.plot()

        lmap = plot.linemap(0)

        line = lmap.line
        line.color = Color.Blue
        line.line_thickness = 1
        line.line_pattern = LinePattern.LongDash
        line.pattern_length = 2

        plot.value_blanking.active = True
        constraint = plot.value_blanking.constraint(0)
        constraint.active = True
        constraint.compare_by = ConstraintOp2Mode.UseConstant
        constraint.comparison_operator = RelOp.LessThanOrEqual
        constraint.comparison_value = 6
        constraint.variable = dataset.variable('Month')

        tp.export.save_png('value_blanking_line.png', 600)

    .. figure:: /_static/images/value_blanking_line.png
        :width: 300px
        :figwidth: 300px
    """
    def __init__(self, plot):
        self.plot = plot
        super().__init__(sv.BLANKING, sv.VALUE, uniqueid=plot.frame.uid)

    @property
    def active(self):
        """`bool`: Include value blanking.

        Set to `True` to include value blanking. The individual constraints
        must be activated as well::

            >>> plot.value_blanking.active = True
            >>> constraint = plot.value_blanking.constraint(0)
            >>> constraint.active = True
        """
        return self._get_style(bool, sv.INCLUDE)

    @active.setter
    def active(self, value):
        self._set_style(bool(value), sv.INCLUDE)

    def constraint(self, index):
        """One of the eight availble value-blanking constraints.

        Parameters:
            index (`Index`): Integer from 0 to 7 inclusive for the eight
                possible value-blanking constraints.

        Returns:
            `ValueBlankingConstraint`

        There are total of eight value blanking constraints that can be
        independendly activated and adjusted. Example usage::

            >>> plot.value_blanking.constraint(4).active = True
        """
        return ValueBlankingConstraint(self, index)


class ValueBlankingCartesian2D(ValueBlanking):
    """Value blanking for cartesian 2D plots.

    .. code-block:: python
        :emphasize-lines: 14-21

        from os import path
        import tecplot as tp
        from tecplot.constant import *

        examples_dir = tp.session.tecplot_examples_directory()
        infile = path.join(examples_dir, 'SimpleData', 'HeatExchanger.plt')
        dataset = tp.data.load_tecplot(infile)

        frame = tp.active_frame()
        plot = frame.plot(PlotType.Cartesian2D)

        plot.show_contour = True

        plot.value_blanking.active = True
        plot.value_blanking.cell_mode = ValueBlankCellMode.AnyCorner
        constraint = plot.value_blanking.constraint(0)
        constraint.active = True
        constraint.compare_by = ConstraintOp2Mode.UseConstant
        constraint.comparison_operator = RelOp.LessThanOrEqual
        constraint.comparison_value = 5
        constraint.variable = dataset.variable('X(M)')

        # ensure consistent output between interactive (connected) and batch
        plot.contour(0).levels.reset_to_nice()

        tp.export.save_png('value_blanking_2d.png', 600)

    .. figure:: /_static/images/value_blanking_2d.png
        :width: 300px
        :figwidth: 300px
    """
    def constraint(self, index):
        """One of the eight availble value-blanking constraints.

        Parameters:
            index (`Index`): Integer from 0 to 7 inclusive for the eight
                possible value-blanking constraints.

        Returns:
            `ValueBlankingConstraintCartesian2D`

        There are total of eight value blanking constraints that can be
        independendly activated and adjusted. Example usage::

            >>> plot.value_blanking.constraint(4).active = True
        """
        return ValueBlankingConstraintCartesian2D(self, index)

    @property
    def cell_mode(self):
        """`ValueBlankCellMode`: Determine which cells to blank.

        This property controls which value is used when determining if a cell
        should be blanked. It also allows for trimming cells precisely.
        Possible values are: `ValueBlankCellMode.AllCorners`,
        `ValueBlankCellMode.AnyCorner`,  `ValueBlankCellMode.PrimaryValue` and
        `ValueBlankCellMode.TrimCells`. This affects all value-blanking
        constraints on the plot::

            >>> from tecplot.constant import ValueBlankCellMode
            >>> plot.value_blanking.cell_mode = ValueBlankCellMode.TrimCells
        """
        if self._get_style(bool, sv.BLANKENTIRECELL):
            return self._get_style(constant.ValueBlankCellMode,
                                   sv.VALUEBLANKCELLMODE)
        else:
            return constant.ValueBlankCellMode.TrimCells

    @cell_mode.setter
    def cell_mode(self, value):
        value = constant.ValueBlankCellMode(value)
        if value == constant.ValueBlankCellMode.TrimCells:
            self._set_style(False, sv.BLANKENTIRECELL)
        else:
            self._set_style(True, sv.BLANKENTIRECELL)
            self._set_style(value, sv.VALUEBLANKCELLMODE)


class ValueBlankingCartesian3D(ValueBlanking):
    """Value blanking for cartesian 3D plots.

    .. code-block:: python
        :emphasize-lines: 12-19

        from os import path
        import tecplot as tp
        from tecplot.constant import *

        examples_dir = tp.session.tecplot_examples_directory()
        infile = path.join(examples_dir, 'SimpleData', 'Sphere.lpk')
        tp.load_layout(infile)

        frame = tp.active_frame()
        plot = frame.plot()

        plot.value_blanking.active = True
        plot.value_blanking.cell_mode = ValueBlankCellMode.AnyCorner
        constraint = plot.value_blanking.constraint(0)
        constraint.active = True
        constraint.compare_by = ConstraintOp2Mode.UseConstant
        constraint.comparison_operator = RelOp.GreaterThan
        constraint.comparison_value = 0
        constraint.variable = frame.dataset.variable('X')

        # ensure consistent output between interactive (connected) and batch
        plot.contour(0).levels.reset_to_nice()

        tp.export.save_png('value_blanking_3d.png', 600)

    .. figure:: /_static/images/value_blanking_3d.png
        :width: 300px
        :figwidth: 300px
    """
    @property
    def cell_mode(self):
        """`ValueBlankCellMode`: Determine which cells to blank.

        This property controls which value is used when determining if a cell
        should be blanked. Possible values are:
        `ValueBlankCellMode.AllCorners`, `ValueBlankCellMode.AnyCorner` and
        `ValueBlankCellMode.PrimaryValue`. This affects all value-blanking
        constraints on the plot::

            >>> from tecplot.constant import ValueBlankCellMode
            >>> plot.value_blanking.cell_mode = ValueBlankCellMode.AnyCorner
        """
        return self._get_style(constant.ValueBlankCellMode,
                               sv.VALUEBLANKCELLMODE)

    @cell_mode.setter
    def cell_mode(self, value):
        value = constant.ValueBlankCellMode(value)
        if value == constant.ValueBlankCellMode.TrimCells:
            msg = 'trim cells mode not available in this plot type'
            raise exception.TecplotLogicError(msg)
        self._set_style(value, sv.VALUEBLANKCELLMODE)


class IJKBlanking(session.Style):
    """IJK blanking for cartesian 2D and 3D plots.
    """
    def __init__(self, plot):
        self.plot = plot
        super().__init__(sv.BLANKING, sv.IJK, uniqueid=plot.frame.uid)

    @property
    def active(self):
        """`bool`: Include :math:`(i, j, k)` blanking.

        Set to `True` to include :math:`(i, j, k)` blanking::

            >>> plot.ijk_blanking.active = True
        """
        return self._get_style(bool, sv.INCLUDE)

    @active.setter
    def active(self, value):
        self._set_style(bool(value), sv.INCLUDE)

    @property
    def zone_index(self):
        """`Index`: `Index` of the `Zone <data_access>` to be blanked.

        Example usage::

            >>> plot.ijk_blanking.zone_index = 1
        """
        return self._get_style(tecutil.Index, sv.ZONE)

    @zone_index.setter
    def zone_index(self, value):
        self._set_style(tecutil.Index(value), sv.ZONE)

    @property
    def zone(self):
        """`Zone <data_access>`: The `Zone <data_access>` to be blanked.

        Example usage::

            >>> plot.ijk_blanking.zone = dataset.zone('Zone Name')
        """
        return self.plot.frame.dataset.zone(self.zone_index)

    @zone.setter
    def zone(self, value):
        self.zone_index = value.index

    @property
    def mode(self):
        """`IJKBlankMode`: Blank the interior or exterior of the region.

        Possible values are `IJKBlankMode.BlankInterior` and
        `IJKBlankMode.BlankExterior` and are a reference to the region between
        `IJKBlanking.min_percent` and `IJKBlanking.max_percent`::

            >>> from tecplot.constant import IJKBlankMode
            >>> plot.ijk_blanking.mode = IJKBlankMode.BlankExterior
        """
        return self._get_style(constant.IJKBlankMode, sv.IJKBLANKMODE)

    @mode.setter
    def mode(self, value):
        self._set_style(constant.IJKBlankMode(value), sv.IJKBLANKMODE)

    @property
    def min_percent(self):
        """`tuple`: Minimum :math:`(i, j, k)` values in percent.

        The percentage is of the total range of the dataset in each dimension.
        This example sets the minimum to 50\% in each of the :math:`(i, j, k)`
        dimensions::

            >>> plot.ijk_blanking.min_percent = (50, 50, 50)
        """
        return session.IJKMinFract(self)

    @min_percent.setter
    def min_percent(self, values):
        session.IJKMinFract(self)[:] = values

    @property
    def max_percent(self):
        """`tuple`: Maximum :math:`(i, j, k)` values in percent.

        The percentage is of the total range of the dataset in each dimension.
        This example sets the maximum to 90\% in each of the :math:`(i, j, k)`
        dimensions::

            >>> plot.ijk_blanking.max_percent = (90, 90, 90)
        """
        return session.IJKMaxFract(self)

    @max_percent.setter
    def max_percent(self, values):
        session.IJKMaxFract(self)[:] = values
