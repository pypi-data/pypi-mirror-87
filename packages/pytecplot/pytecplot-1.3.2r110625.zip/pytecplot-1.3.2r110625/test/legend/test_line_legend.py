import os, unittest

import tecplot as tp
from tecplot.constant import *
from tecplot.exception import *

from ..sample_data import sample_data
from .test_legend import TestCategoryLegend


class TestLineLegend(TestCategoryLegend, unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        self.filename, self.dataset = sample_data('2x2x3_overlap')
        frame = tp.active_frame()
        frame.plot_type = PlotType.XYLine
        self.legend = frame.plot(PlotType.XYLine).legend

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)


if __name__ == '__main__':
    from .. import main
    main()
