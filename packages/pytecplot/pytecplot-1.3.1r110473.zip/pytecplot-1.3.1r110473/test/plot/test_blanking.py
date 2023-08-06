import os, unittest

import tecplot as tp
from tecplot.constant import *
from tecplot.exception import *
from tecplot.plot import (ValueBlanking, ValueBlankingCartesian2D,
                          ValueBlankingCartesian3D, ValueBlankingConstraint,
                          ValueBlankingConstraintCartesian2D)
from tecplot.plot import IJKBlanking


from .. import sample_data


class TestValueBlankingConstraint(object):
    def test_variable_index(self):
        for constraint in [self.blanking.constraint(i) for i in range(2)]:
            for val in [1, 2, 0]:
                constraint.variable_index = val
                self.assertEqual(constraint.variable_index, val)
        with self.assertRaises((TecplotSystemError, TecplotLogicError)):
            self.blanking.constraint(0).variable_index = 100
        with self.assertRaises(ValueError):
            self.blanking.constraint(0).variable_index = 'badvalue'

    def test_variable(self):
        for constraint in [self.blanking.constraint(i) for i in range(2)]:
            for i in [1, 2, 0]:
                var = self.dataset.variable(i)
                constraint.variable = var
                self.assertEqual(constraint.variable, var)
        with self.assertRaises(AttributeError):
            self.blanking.constraint(0).variable = 100
        with self.assertRaises(TypeError):
            self.blanking.constraint(0).variable = 'badvalue'

    def test_comparison_value(self):
        for constraint in [self.blanking.constraint(i) for i in range(2)]:
            for val in [-1000, -0.5, 0, 0.5, 100]:
                constraint.comparison_value = val
                self.assertEqual(constraint.comparison_value, val)
        with self.assertRaises(ValueError):
            self.blanking.constraint(0).comparison_value = 'badvalue'

    def test_comparison_variable_index(self):
        for constraint in [self.blanking.constraint(i) for i in range(2)]:
            for val in [1, 2, 0]:
                constraint.comparison_variable_index = val
                self.assertEqual(constraint.comparison_variable_index, val)
        with self.assertRaises((TecplotSystemError, TecplotLogicError)):
            self.blanking.constraint(0).comparison_variable_index = 100
        with self.assertRaises(ValueError):
            self.blanking.constraint(0).comparison_variable_index = 'badvalue'

    def test_comparison_variable(self):
        for constraint in [self.blanking.constraint(i) for i in range(2)]:
            for i in [1, 2, 0]:
                var = self.dataset.variable(i)
                constraint.comparison_variable = var
                self.assertEqual(constraint.comparison_variable, var)
        with self.assertRaises(AttributeError):
            self.blanking.constraint(0).comparison_variable = 100
        with self.assertRaises(ValueError):
            self.blanking.constraint(0).variable_index = 'badvalue'

    def test_compare_by(self):
        for constraint in [self.blanking.constraint(i) for i in range(2)]:
            for mode in ConstraintOp2Mode:
                constraint.compare_by = mode
                self.assertEqual(constraint.compare_by, mode)
        with self.assertRaises(ValueError):
            self.blanking.constraint(0).compare_by = 'badvalue'

    def test_comparison_operator(self):
        for constraint in [self.blanking.constraint(i) for i in range(2)]:
            for op in RelOp:
                constraint.comparison_operator = op
                self.assertEqual(constraint.comparison_operator, op)
        with self.assertRaises(ValueError):
            self.blanking.constraint(0).comparison_operator = 'badvalue'

    def test_active(self):
        for constraint in [self.blanking.constraint(i) for i in range(2)]:
            for val in [True, False, True]:
                constraint.active = val
                self.assertEqual(constraint.active, val)


class TestValueBlankingConstraintCartesian2D(TestValueBlankingConstraint):
    def test_show_line(self):
        for constraint in [self.blanking.constraint(i) for i in range(2)]:
            for val in [True, False, True]:
                constraint.show_line = val
                self.assertEqual(constraint.show_line, val)

    def test_color(self):
        for constraint in [self.blanking.constraint(i) for i in range(2)]:
            for val in [Color.Red, Color.Blue, Color.Black]:
                constraint.color = val
                self.assertEqual(constraint.color, val)
            with self.assertRaises(ValueError):
                constraint.color = 'badvalue'

    def test_line_thickness(self):
        for constraint in [self.blanking.constraint(i) for i in range(2)]:
            for val in [0.5,1,100]:
                constraint.line_thickness = val
                self.assertAlmostEqual(constraint.line_thickness, val)
            with self.assertRaises(ValueError):
                constraint.line_thickness = 'badvalue'
            with self.assertRaises(TecplotSystemError):
                constraint.line_thickness = 0
            with self.assertRaises(TecplotSystemError):
                constraint.line_thickness = -1

    def test_line_pattern(self):
        for constraint in [self.blanking.constraint(i) for i in range(2)]:
            for val in LinePattern:
                constraint.line_pattern = val
                self.assertEqual(constraint.line_pattern, val)
            with self.assertRaises(ValueError):
                constraint.line_pattern = 'badvalue'

    def test_pattern_length(self):
        for constraint in [self.blanking.constraint(i) for i in range(2)]:
            for val in [0.5,1,2]:
                constraint.pattern_length = val
                self.assertEqual(constraint.pattern_length, val)
            with self.assertRaises(ValueError):
                constraint.pattern_length = 'badtype'
            with self.assertRaises(TypeError):
                constraint.pattern_length = None
            with self.assertRaises(TecplotSystemError):
                constraint.pattern_length = -1
            with self.assertRaises(TecplotSystemError):
                constraint.pattern_length = 0


class TestValueBlanking(TestValueBlankingConstraint):
    def test_active(self):
        for val in [True, False, True]:
            self.blanking.active = val
            self.assertEqual(self.blanking.active, val)

    def test_constraint(self):
        for constraint in [self.blanking.constraint(i) for i in range(8)]:
            self.assertIsInstance(constraint, ValueBlankingConstraint)
        if __debug__:
            with self.assertRaises(TecplotIndexError):
                _ = self.blanking.constraint(8)
            with self.assertRaises(TecplotIndexError):
                _ = self.blanking.constraint(-1)

class TestValueBlankingXYPlot(unittest.TestCase, TestValueBlanking):
    def setUp(self):
        self.ftmp, self.dataset = sample_data.sample_data('xylines_poly')
        plot = tp.active_frame().plot(PlotType.XYLine)
        plot.activate()
        self.blanking = plot.value_blanking

    def tearDown(self):
        tp.new_layout()
        os.remove(self.ftmp)


class TestValueBlankingPolarPlot(unittest.TestCase, TestValueBlanking):
    def setUp(self):
        self.ftmp, self.dataset = sample_data.sample_data('xylines_poly')
        plot = tp.active_frame().plot(PlotType.PolarLine)
        plot.activate()
        self.blanking = plot.value_blanking

    def tearDown(self):
        tp.new_layout()
        os.remove(self.ftmp)


class TestValueBlankingCartesian2D(unittest.TestCase, TestValueBlankingConstraintCartesian2D):
    def setUp(self):
        self.ftmp, self.dataset = sample_data.sample_data('10x10x10')
        plot = tp.active_frame().plot(PlotType.Cartesian2D)
        plot.activate()
        self.blanking = plot.value_blanking

    def tearDown(self):
        tp.new_layout()
        os.remove(self.ftmp)

    def test_constraint(self):
        for constraint in [self.blanking.constraint(i) for i in range(8)]:
            self.assertIsInstance(constraint, ValueBlankingConstraintCartesian2D)
        if __debug__:
            with self.assertRaises(TecplotIndexError):
                _ = self.blanking.constraint(8)
            with self.assertRaises(TecplotIndexError):
                _ = self.blanking.constraint(-1)

    def test_cell_mode(self):
        for mode in ValueBlankCellMode:
            self.blanking.cell_mode = mode
            self.assertEqual(self.blanking.cell_mode, mode)
        with self.assertRaises(ValueError):
            self.blanking.cell_mode = 'badvalue'


class TestValueBlankingCartesian3D(unittest.TestCase, TestValueBlanking):
    def setUp(self):
        self.ftmp, self.dataset = sample_data.sample_data('10x10x10')
        plot = tp.active_frame().plot(PlotType.Cartesian3D)
        plot.activate()
        self.blanking = plot.value_blanking

    def tearDown(self):
        tp.new_layout()
        os.remove(self.ftmp)

    def test_cell_mode(self):
        for mode in [ValueBlankCellMode.AllCorners,
                     ValueBlankCellMode.AnyCorner,
                     ValueBlankCellMode.PrimaryValue]:
            self.blanking.cell_mode = mode
            self.assertEqual(self.blanking.cell_mode, mode)
        with self.assertRaises(ValueError):
            self.blanking.cell_mode = 'badvalue'
        with self.assertRaises(TecplotLogicError):
            self.blanking.cell_mode = ValueBlankCellMode.TrimCells


class TestIJKBlanking(object):
    def test_active(self):
        for val in [True, False, True]:
            self.blanking.active = val
            self.assertEqual(self.blanking.active, val)

    def test_zone_index(self):
        for val in [1, 0]:
            self.blanking.zone_index = val
            self.assertEqual(self.blanking.zone_index, val)
        with self.assertRaises((TecplotSystemError, TecplotLogicError)):
            self.blanking.zone_index = 100
        with self.assertRaises(ValueError):
            self.blanking.zone_index = 'badvalue'

    def test_zone(self):
        for i in [1, 0]:
            zone = self.dataset.zone(i)
            self.blanking.zone = zone
            self.assertEqual(self.blanking.zone, zone)
        with self.assertRaises(AttributeError):
            self.blanking.zone = 100
        with self.assertRaises(TypeError):
            self.blanking.zone = 'badvalue'

    def test_mode(self):
        for val in [IJKBlankMode.BlankExterior, IJKBlankMode.BlankInterior,
                    IJKBlankMode.BlankExterior]:
            self.blanking.mode = val
            self.assertEqual(self.blanking.mode, val)
        with self.assertRaises(ValueError):
            self.blanking.mode = 'badvalue'

    def test_min_percent(self):
        self.blanking.max_percent = 100, 100, 100
        for val in [(0,0,0), (10,20,30), (0,50,100)]:
            self.blanking.min_percent = val
            minpct = self.blanking.min_percent
            self.assertAlmostEqual(minpct[0], val[0])
            self.assertAlmostEqual(minpct[1], val[1])
            self.assertAlmostEqual(minpct[2], val[2])

        self.blanking.min_percent = 0, 0, 0
        minpct = self.blanking.min_percent
        self.assertAlmostEqual(minpct[0], 0)
        self.assertAlmostEqual(minpct[1], 0)
        self.assertAlmostEqual(minpct[2], 0)

        self.blanking.min_percent = (10, )
        minpct = self.blanking.min_percent
        self.assertAlmostEqual(minpct[0], 10)
        self.assertAlmostEqual(minpct[1], 0)
        self.assertAlmostEqual(minpct[2], 0)

        self.blanking.min_percent = (20, 30)
        minpct = self.blanking.min_percent
        self.assertAlmostEqual(minpct[0], 20)
        self.assertAlmostEqual(minpct[1], 30)
        self.assertAlmostEqual(minpct[2], 0)

        self.blanking.min_percent.i = 5
        self.blanking.min_percent.j = 10
        self.blanking.min_percent.k = 15
        minpct = self.blanking.min_percent
        self.assertAlmostEqual(minpct.i, 5)
        self.assertAlmostEqual(minpct.j, 10)
        self.assertAlmostEqual(minpct.k, 15)

        with self.assertRaises(ValueError):
            self.blanking.min_percent = 'badvalue'

    def test_max_percent(self):
        self.blanking.min_percent = 0, 0, 0
        for val in [(0,0,0), (10,20,30), (0,50,100)]:
            self.blanking.max_percent = val
            maxpct = self.blanking.max_percent
            self.assertAlmostEqual(maxpct[0], val[0])
            self.assertAlmostEqual(maxpct[1], val[1])
            self.assertAlmostEqual(maxpct[2], val[2])

        self.blanking.max_percent = 0, 0, 0
        maxpct = self.blanking.max_percent
        self.assertAlmostEqual(maxpct[0], 0)
        self.assertAlmostEqual(maxpct[1], 0)
        self.assertAlmostEqual(maxpct[2], 0)

        self.blanking.max_percent = (10, )
        maxpct = self.blanking.max_percent
        self.assertAlmostEqual(maxpct[0], 10)
        self.assertAlmostEqual(maxpct[1], 0)
        self.assertAlmostEqual(maxpct[2], 0)

        self.blanking.max_percent = (20, 30)
        maxpct = self.blanking.max_percent
        self.assertAlmostEqual(maxpct[0], 20)
        self.assertAlmostEqual(maxpct[1], 30)
        self.assertAlmostEqual(maxpct[2], 0)

        self.blanking.max_percent.i = 5
        self.blanking.max_percent.j = 10
        self.blanking.max_percent.k = 15
        maxpct = self.blanking.max_percent
        self.assertAlmostEqual(maxpct.i, 5)
        self.assertAlmostEqual(maxpct.j, 10)
        self.assertAlmostEqual(maxpct.k, 15)

        with self.assertRaises(ValueError):
            self.blanking.max_percent = 'badvalue'


class TestIJKBlankingCartesian2D(unittest.TestCase, TestIJKBlanking):
    def setUp(self):
        self.ftmp, self.dataset = sample_data.sample_data('2x2x3_overlap')
        plot = tp.active_frame().plot(PlotType.Cartesian2D)
        plot.activate()
        self.blanking = plot.ijk_blanking

    def tearDown(self):
        tp.new_layout()
        os.remove(self.ftmp)


class TestIJKBlankingCartesian3D(unittest.TestCase, TestIJKBlanking):
    def setUp(self):
        self.ftmp, self.dataset = sample_data.sample_data('2x2x3_overlap')
        plot = tp.active_frame().plot(PlotType.Cartesian3D)
        plot.activate()
        self.blanking = plot.ijk_blanking

    def tearDown(self):
        tp.new_layout()
        os.remove(self.ftmp)


if __name__ == '__main__':
    from .. import main
    main()
