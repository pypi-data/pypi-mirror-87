import unittest
import sys

from unittest.mock import patch, Mock

import tecplot as tp
from tecplot.tecutil import sv
from tecplot.constant import *
from tecplot.exception import *

from tecplot.session import state_changed

from test import sample_data, patch_tecutil


class TestStateChanged(unittest.TestCase):
    @staticmethod
    def setUpClass():
        tp.new_layout()
        fr = tp.active_frame()
        fr.name = 'B'
        sample_data.create_ordered_3d(frame=fr)
        sample_data.create_ordered_3d(frame=fr)
        fr = tp.active_page().add_frame()
        fr.name = 'A'
        sample_data.create_ordered_3d(frame=fr)
        sample_data.create_ordered_3d(frame=fr)

    def test_default_params(self):
        def check_arglist(arglist, self=self):
            self.assertEqual(len(arglist), 1)
            self.assertEqual(StateChange(arglist[sv.STATECHANGE]), StateChange.Text)

        with patch_tecutil('StateChangedX', side_effect=check_arglist):
            state_changed._state_changed(StateChange.Text)

    def test_params(self):
        def check_arglist(arglist, self=self):
            self.assertEqual(len(arglist), 6)
            self.assertEqual(StateChange(arglist[sv.STATECHANGE]),
                             StateChange.VarsAltered)
            self.assertEqual(arglist[sv.ZONELIST], set([5, 6]))
            self.assertEqual(arglist[sv.VARLIST], set([7, 8]))
            self.assertEqual(arglist[sv.INDEX], 10)
            if tp.sdk_version_info >= (2018, 2) and tp.session.connected():
                self.assertEqual(arglist[sv.UNIQUEID].value, 3)
                self.assertEqual(arglist[sv.DATASETUNIQUEID].value, 4)
            else:
                self.assertEqual(arglist[sv.UNIQUEID], 3)
                self.assertEqual(arglist[sv.DATASETUNIQUEID], 4)

        with patch_tecutil('StateChangedX', side_effect=check_arglist):
            state_changed._state_changed(
                StateChange.VarsAltered,
                uniqueid=3,
                dataset=4,
                zones=[5, 6],
                variables=[7, 8],
                index=9)

    def test_zone_added(self):
        with patch('tecplot.session.state_changed._state_changed') as schg:
            ds = tp.active_frame().dataset
            zn = ds.zone(0)
            state_changed.zone_added(zn)
            schg.assert_called_once_with(
                StateChange.ZonesAdded, dataset=ds.uid, zones=set([zn.index]))

    def test_state_changes(self):
        # exercise the state_changed() method to ensure it doesn't throw
        with patch('tecplot.session.state_changed._state_changed') as schg:
            ds = tp.active_page().frame('A').dataset
            state_changed.connectivity_altered(ds.zone(0))
            state_changed.connectivity_altered(ds.zone(1))
            state_changed.data_altered(ds.zone(0), ds.variable(0), index=5)
            state_changed.data_altered(ds.zone(0), ds.variable(0), index=6)
            state_changed.data_altered(ds.zone(0), ds.variable(1), index=7)
            state_changed.data_altered(ds.zone(1), ds.variable(2))
            state_changed.zone_added(ds.zone(0))

            ds1 = tp.active_page().frame('B').dataset
            state_changed.connectivity_altered(ds1.zone(0))
            state_changed.connectivity_altered(ds1.zone(1))
            state_changed.data_altered(ds1.zone(0), ds1.variable(0), index=5)
            state_changed.data_altered(ds1.zone(0), ds1.variable(0), index=6)
            state_changed.data_altered(ds1.zone(0), ds1.variable(1), index=7)
            state_changed.data_altered(ds1.zone(1), ds1.variable(2))
            state_changed.zone_added(ds1.zone(0))
            state_changed.zone_added(ds1.zone(1))

    def test_state_changes_suspended(self):
        # exercise the state_changed() method to ensure it doesn't throw
        with tp.session.suspend():
            with patch('tecplot.session.state_changed._state_changed') as schg:
                ds = tp.active_page().frame('A').dataset
                ds1 = tp.active_page().frame('B').dataset

                state_changed.connectivity_altered(ds.zone(0))
                state_changed.connectivity_altered(ds1.zone(0))

                state_changed.connectivity_altered(ds.zone(1))
                state_changed.connectivity_altered(ds1.zone(1))

                state_changed.data_altered(ds.zone(0), ds.variable(0), index=5)
                state_changed.data_altered(ds.zone(0), ds.variable(0), index=6)
                state_changed.data_altered(ds.zone(0), ds.variable(1), index=7)
                state_changed.data_altered(ds.zone(1), ds.variable(2))

                state_changed.data_altered(ds1.zone(0), ds1.variable(0), index=5)
                state_changed.data_altered(ds1.zone(0), ds1.variable(0), index=6)
                state_changed.data_altered(ds1.zone(0), ds1.variable(1), index=7)
                state_changed.data_altered(ds1.zone(1), ds1.variable(2))

                state_changed.zone_added(ds.zone(0))
                state_changed.zone_added(ds1.zone(0))
                state_changed.zone_added(ds1.zone(1))

                state_changed.data_altered(ds.zone(0), ds.variable(0))

                if __debug__:
                    with self.assertRaises(TecplotLogicError):
                        state_changed.data_altered(ds.zone(0), ds1.variable(0))

    def test_state_changes_suspended_duplicates(self):
        # exercise the state_changed() method to ensure it doesn't throw
        with tp.session.suspend():
            with patch('tecplot.session.state_changed._state_changed') as schg:
                ds = tp.active_page().frame('A').dataset
                state_changed.zone_added(ds.zone(1))
                state_changed.data_altered(ds.zone(0), ds.variable(0), index=1)
                state_changed.data_altered(ds.zone(0), ds.variable(0))
                state_changed.data_altered(ds.zone(0), ds.variable(0))

                state_changed.connectivity_altered(ds.zone(0))

                state_changed.zone_added(ds.zone(0))
                state_changed.connectivity_altered(ds.zone(0))

        with tp.session.suspend():
            with patch('tecplot.session.state_changed._state_changed') as schg:
                ds = tp.active_page().frame('A').dataset
                state_changed.data_altered(ds.zone(0), ds.variable(0), index=1)

    def test_emit_state_changes_unknown(self):
        # the internal method _emit_state_changes currently ignores
        # state changes it does not know about
        state_changed._emit_state_changes({StateChange.AnimationEnd:None})


if __name__ == '__main__':
    from .. import main
    main()
