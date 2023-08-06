# coding: utf-8
from __future__ import unicode_literals

import base64, itertools as it, os, platform, sys, unittest, zlib

import numpy as np
from numpy import random as rand

from ctypes import *
from tempfile import NamedTemporaryFile
from unittest.mock import patch, Mock, PropertyMock

import tecplot as tp
from tecplot import session
from tecplot.constant import *
from tecplot.exception import *

from test import patch_tecutil, skip_if_sdk_version_before, mocked_sdk_version

from .. import sample_data
from ..sample_data import sample_data_file


class TestExtractBlankedZones(unittest.TestCase):
    @skip_if_sdk_version_before(2020, 0)
    def setUp(self):
        tp.new_layout()
        self.plot = sample_data.create_ordered_3d()
        frame = self.plot.frame
        self.plot = sample_data.create_ordered_3d(frame=frame)
        self.ds = self.plot.frame.dataset

        self.plot.value_blanking.active = True
        constraint = self.plot.value_blanking.constraint(0)
        constraint.active = True
        constraint.compare_by = ConstraintOp2Mode.UseConstant
        constraint.comparison_operator = RelOp.LessThanOrEqual
        constraint.comparison_value = 1
        constraint.variable = self.ds.variable('s')

    def test_outside_blanked_region(self):
        self.plot.value_blanking.active = True
        self.plot.value_blanking.constraint(0).comparison_value = 10
        new_zones = tp.data.extract.extract_blanked_zones(*self.ds.zones())
        self.assertEqual(len(new_zones), 0)

    def test_inactive_blanking(self):
        self.plot.value_blanking.active = False
        self.plot.value_blanking.constraint(0).comparison_value = 1
        new_zones = tp.data.extract.extract_blanked_zones(self.ds.zone(0),
                                                          plot=self.plot)
        self.assertEqual(len(new_zones), 1)

    def test_extract_blanked_zones(self):
        self.plot.value_blanking.active = True
        self.plot.value_blanking.constraint(0).comparison_value = 1
        n = self.ds.num_zones
        new_zones = tp.data.extract.extract_blanked_zones(self.ds.zones())
        self.assertEqual(len(new_zones), n)

    def test_failures(self):
        with self.assertRaises(TecplotLogicError):
            _ = tp.data.extract.extract_blanked_zones()

        if __debug__:
            with mocked_sdk_version(2019, 1):
                with self.assertRaises(TecplotOutOfDateEngineError):
                    _ = tp.data.extract.extract_blanked_zones(self.ds.zones())


class TestExtractConnectedRegions(unittest.TestCase):
    @skip_if_sdk_version_before(2020, 2)
    def test_extract_connected_regions(self):
        tp.new_layout()
        tp.macro.execute_command('$!CreateRectangularZone IMax = 4 JMax = 4 KMax = 4')
        self.frame = tp.active_frame()
        self.plot = self.frame.plot()
        self.ds = self.frame.dataset
        tp.data.operate.execute_equation(equation='{P}=(X+Y+Z) * (3-X-Y-Z) / 2.25')
        self.plot.value_blanking.constraint(0).comparison_operator=RelOp.GreaterThan
        self.plot.value_blanking.constraint(0).active=True
        self.plot.value_blanking.cell_mode=ValueBlankCellMode.AllCorners
        self.plot.value_blanking.constraint(0).variable_index=3
        self.plot.value_blanking.active=True
        tp.data.extract.extract_blanked_zones(self.ds.zone(0), plot=self.plot)
        self.ds.delete_zones([0])

        new_zones = tp.data.extract.extract_connected_regions([0])
        self.assertEqual(len(new_zones), 2)

    @skip_if_sdk_version_before(2020, 2)
    def test_failures(self):
        tp.new_layout()
        with self.assertRaises(TecplotLogicError):
            _ = tp.data.extract.extract_connected_regions()

        if __debug__:
            with self.assertRaises(TecplotLogicError):
                _ = tp.data.extract.extract_connected_regions([0],
                    frame=tp.active_frame(), dataset='no dataset')

            with mocked_sdk_version(2020, 1):
                with self.assertRaises(TecplotOutOfDateEngineError):
                    _ = tp.data.extract.extract_connected_regions()


class TestExtract(unittest.TestCase):
    def setUp(self):
        self.filenames = [
            sample_data_file('10x10x10'),
            sample_data_file('3x3_2x2')]

    def tearDown(self):
        tp.new_layout()
        for f in self.filenames:
            os.remove(f)

    @skip_if_sdk_version_before(2017, 3)
    def test_extract_default_args(self):
        tp.new_layout()
        ds = tp.data.load_tecplot(self.filenames[0])
        fr = tp.active_frame()
        fr.plot_type = PlotType.Cartesian3D

        z = tp.data.extract.extract_slice(origin=(.5,.5,0), normal=(0,1,0),
            source=SliceSource.VolumeZones, mode=ExtractMode.SingleZone,
            copy_cell_centers=False, assign_strand_ids=False, frame=None,
            dataset=None)

        self.assertIsInstance(z, tp.data.ClassicFEZone)

        if __debug__:
            with mocked_sdk_version(2017, 2):
                with self.assertRaises(TecplotOutOfDateEngineError):
                    z = tp.data.extract.extract_slice(origin=(.5,.5,0),
                        normal=(0,1,0), mode=ExtractMode.OneZonePerConnectedRegion)

    @skip_if_sdk_version_before(2017, 3)
    def test_extract_nondefault_args(self):
        tp.new_layout()
        ds = tp.data.load_tecplot(self.filenames[0])
        fr = tp.active_frame()
        fr.plot_type = PlotType.Cartesian3D

        z = tp.data.extract.extract_slice(origin=(.5,.5,0), normal=(0,1,0),
            source=SliceSource.VolumeZones,
            mode=ExtractMode.OneZonePerConnectedRegion, copy_cell_centers=True,
            assign_strand_ids=True, frame=fr, dataset=None)
        z = list(z)
        self.assertEqual(len(z), 1)

        with self.assertRaises(TecplotInterfaceChangeError):
            z = tp.data.extract.extract_slice((0,0,0), (0,0,1),
                                              multiple_zones=True)

    def test_dataset_frame_mismatch(self):
        tp.new_layout()
        ds = tp.data.load_tecplot(self.filenames[0])
        fr = tp.active_frame()
        fr.plot_type = PlotType.Cartesian3D

        newfr = tp.active_page().add_frame()
        newfr.create_dataset('D', ['x','y'])

        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            z = tp.data.extract.extract_slice(dataset=ds, frame=newfr)

    @skip_if_sdk_version_before(2017, 3)
    def test_interpolate_linear(self):
        tp.new_layout()
        ds = tp.data.load_tecplot(self.filenames[0])

        fr = tp.active_frame()
        fr.plot_type = PlotType.Cartesian3D

        z = tp.data.extract.extract_slice(origin=(0.5,0.5,0), normal=(0,1,0),
            source=SliceSource.VolumeZones, dataset=ds)
        self.assertIn(z, ds)
        self.assertTrue(z.name.startswith('Slice:'))

    def test_interpolate_linear_failures(self):
        tp.new_layout()
        ds = tp.data.load_tecplot(self.filenames[0])

        fr = tp.active_frame()
        fr.plot_type = PlotType.Cartesian3D

        with patch_tecutil('CreateSliceZoneFromPlneX', return_value=False):
            with self.assertRaises(TecplotSystemError):
                tp.data.extract.extract_slice((0.5,0.5,0), (0,1,0))

        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            tp.data.extract.extract_slice((0.5,0.5,100), (0,0,1))

        if __debug__:
            tp.new_layout()
            ds = tp.data.load_tecplot(self.filenames[1])

            fr = tp.active_frame()
            fr.plot_type = PlotType.Cartesian2D
            with self.assertRaises(TecplotLogicError):
                tp.data.extract.extract_slice((0.5,0.5,0), (0,1,0))

        tp.new_layout()
        ds = tp.data.load_tecplot(self.filenames[1])

        fr = tp.active_frame()
        fr.plot_type = PlotType.Cartesian3D
        with self.assertRaises(TecplotLogicError):
            tp.data.extract.extract_slice((0.5,0.5,0), (0,1,0))

    def test_extract_line_3d(self):
        tp.new_layout()
        ds = tp.data.load_tecplot(self.filenames[0])
        fr = tp.active_frame()
        fr.plot_type = PlotType.Cartesian3D

        pts = [
            (.5, .5, .5),
            (.8, .8, .8),
            (1., 1., 1.)]
        z = tp.data.extract.extract_line(pts)
        self.assertIsInstance(z, tp.data.OrderedZone)
        self.assertEqual(z.values(0).shape, (3,))

        pts = [
            (.5, .5, .5),
            (.8, .8, .8),
            (1., 1., 1.)]
        z = tp.data.extract.extract_line(pts, num_points=10)
        self.assertIsInstance(z, tp.data.OrderedZone)
        self.assertEqual(z.values(0).shape, (10,))

        def pts():
            for p in ((.5, .5, .5), (.8, .8, .8), (1., 1., 1.)):
                yield p
        z = tp.data.extract.extract_line(pts())
        self.assertIsInstance(z, tp.data.OrderedZone)
        self.assertEqual(z.values(0).shape, (3,))

        pts = [
            (.5, .5, .5),
            (.8, .8, .8),
            (1.1, 1.1, 1.1)]
        z = tp.data.extract.extract_line(pts)
        self.assertIsInstance(z, tp.data.OrderedZone)
        self.assertEqual(z.values(0).shape, (2,))

        pts = [(1.1, 1.1, 1.1)]
        nzones = ds.num_zones
        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            z = tp.data.extract.extract_line(pts)
        self.assertEqual(nzones, ds.num_zones)

    def test_extract_line_2d(self):
        tp.new_layout()
        ds = tp.data.load_tecplot(self.filenames[0])
        fr = tp.active_frame()
        fr.plot_type = PlotType.Cartesian2D
        fr.plot().fieldmap(0).surfaces.surfaces_to_plot = SurfacesToPlot.KPlanes

        pts = [
            (.5, .5),
            (.8, .8),
            (1., 1.)]
        z = tp.data.extract.extract_line(pts, frame=fr)
        self.assertIsInstance(z, tp.data.OrderedZone)
        self.assertEqual(z.values(0).shape, (3,))

        pts = [
            (.5, .5),
            (.8, .8),
            (1.1, 1.1)]
        z = tp.data.extract.extract_line(pts, dataset=ds)
        self.assertIsInstance(z, tp.data.OrderedZone)
        self.assertEqual(z.values(0).shape, (2,))

        pts = [(1.1, 1.1)]
        nzones = ds.num_zones
        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            z = tp.data.extract.extract_line(pts, frame=fr, dataset=ds)
        self.assertEqual(nzones, ds.num_zones)

    def test_extract_line_failures(self):
        if __debug__:
            tp.new_layout()
            ds = tp.data.load_tecplot(self.filenames[0])
            fr = tp.active_frame()

            pts = [
                (.5, .5, .5),
                (.8, .8, .8),
                (1., 1., 1.)]

            fr.plot_type = PlotType.Sketch

            with self.assertRaises(TecplotLogicError):
                z = tp.data.extract.extract_line(pts)

            fr.plot_type = PlotType.Cartesian3D
            fr2 = tp.active_page().add_frame()
            ds2 = tp.data.load_tecplot(self.filenames[0])
            with self.assertRaises(TecplotLogicError):
                z = tp.data.extract.extract_line(pts, frame=fr, dataset=ds2)

    @skip_if_sdk_version_before(2017, 3)
    def test_extract_modes(self):
        rand.seed(1)
        tp.new_layout()
        fr = tp.active_frame()
        ds = fr.create_dataset('D', ['x', 'y', 'z', 's'])

        # Create a single FE Brick zone with two disconnected regions
        x = np.linspace(-1, 1, 3)
        y = np.linspace(-1, 1, 4)
        z = np.linspace(-1, 1, 5)
        nodes = list(it.product(x, y, z))
        shape = (len(x), len(y), len(z))
        cells = []
        for i, j, k in it.product(*[range(s - 1) for s in shape]):
            cell = []
            for ii, jj in it.product([i, i+1], [j, j+1]):
                for kk in [k, k+1] if jj == j else [k+1, k]:
                    cell.append(ii * len(y) * len(z) + jj * len(z) + kk)
            cells.append(cell)

        z = np.linspace(2, 4, 5)
        node_offset = len(nodes)
        nodes.extend(list(it.product(x, y, z)))
        shape = (len(x), len(y), len(z))
        for i, j, k in it.product(*[range(s - 1) for s in shape]):
            cell = []
            for ii, jj in it.product([i, i+1], [j, j+1]):
                for kk in [k, k+1] if jj == j else [k+1, k]:
                    cell.append(ii * len(y) * len(z) + jj * len(z) + kk + node_offset)
            cells.append(cell)

        zn = ds.add_fe_zone(ZoneType.FEBrick, 'Z', num_points=len(nodes),
                            num_elements=len(cells))

        zn.values('x')[:] = [n[0] for n in nodes]
        zn.values('y')[:] = [n[1] for n in nodes]
        zn.values('z')[:] = [n[2] for n in nodes]
        zn.values('s')[:] = rand.uniform(-10, 10, len(nodes))

        zn.nodemap[:] = cells

        fr.plot_type = PlotType.Cartesian3D

        self.assertEqual(ds.num_zones, 1)
        zn = tp.data.extract.extract_slice((0.25,0.25,0), (1,1,0),
            mode=ExtractMode.SingleZone)
        self.assertIsInstance(zn, tp.data.zone.Zone)
        self.assertEqual(ds.num_zones, 2)
        zns = tp.data.extract.extract_slice((0.25,0.25,0), (1,1,0),
            mode=ExtractMode.OneZonePerSourceZone)
        zns = list(zns)
        self.assertEqual(len(zns), 1)
        self.assertIsInstance(zns[0], tp.data.zone.Zone)
        self.assertEqual(ds.num_zones, 3)
        zns = tp.data.extract.extract_slice((0.25,0.25,0), (1,1,0),
            mode=ExtractMode.OneZonePerConnectedRegion)
        zns = list(zns)
        self.assertEqual(ds.num_zones, 5)
        self.assertEqual(len(zns), 2)
        self.assertIsInstance(zns[0], tp.data.zone.Zone)
        self.assertIsInstance(zns[1], tp.data.zone.Zone)

    @skip_if_sdk_version_before(2019, 1)
    def test_extract_transient_modes(self):
        tp.new_layout()
        ds = tp.data.load_tecplot(self.filenames[0])
        ds.copy_zones(ds.zone(0))
        fr = tp.active_frame()
        plot = fr.plot(PlotType.Cartesian3D)
        plot.activate()
        ds.zone(0).strand = 1
        ds.zone(0).solution_time = 1.0
        ds.zone(1).strand = 1
        ds.zone(1).solution_time = 2.0
        plot.active_fieldmap_indices = [0, 1]
        plot.solution_time = 1.0

        z = tp.data.extract.extract_slice(origin=(.5,.5,1), normal=(0,1,0),
                transient_mode=TransientOperationMode.AllSolutionTimes)
        z = list(z)
        self.assertEqual(len(z), 2)

        self.assertTrue(tp.tecutil._tecutil.DataSetJournalIsValid())


class TestTriangulate(unittest.TestCase):
    def test_triangulate(self):
        tp.new_layout()
        plot = sample_data.create_ordered_2d()
        sample_data.create_ordered_2d(frame=plot.frame)
        sample_data.create_i_ordered(frame=plot.frame)
        ds = plot.frame.dataset
        zn0 = ds.zone(0)
        zn1 = ds.zone(1)
        zn2 = ds.zone(2)
        zn1.values('x')[:] = zn1.values('x')[:] + 1.0
        zn1.values('y')[:] = zn1.values('y')[:] + 1.0

        z = tp.data.extract.triangulate(zn0, zn1)
        self.assertIsInstance(z, tp.data.zone.Zone)
        z = tp.data.extract.triangulate(zn0, zn1,
            boundary_zones=[zn2], include_boundary_points=True,
            keep_factor=0.3)
        self.assertIsInstance(z, tp.data.zone.Zone)

    def test_failure(self):
        tp.new_layout()
        plot = sample_data.create_ordered_2d()
        sample_data.create_ordered_2d(frame=plot.frame)
        ds = plot.frame.dataset
        with patch_tecutil('Triangulate', return_value=(False,None)):
            with self.assertRaises(TecplotSystemError):
                z = tp.data.extract.triangulate(ds.zone(0), ds.zone(1))

    def test_non_active_plot(self):
        tp.new_layout()
        plot = sample_data.create_ordered_2d()
        sample_data.create_ordered_2d(frame=plot.frame)
        ds = plot.frame.dataset
        zn0 = ds.zone(0)
        zn1 = ds.zone(1)
        zn1.values('x')[:] = zn1.values('x')[:] + 1.0
        zn1.values('y')[:] = zn1.values('y')[:] + 1.0

        plot.frame.plot_type = PlotType.Cartesian3D
        with self.assertRaises((TecplotSystemError, TecplotLogicError)):
            _ = tp.data.extract.triangulate(zn0, zn1)
        z = tp.data.extract.triangulate(zn0, zn1, plot=plot)
        self.assertIsInstance(z, tp.data.zone.Zone)


if __name__ == '__main__':
    from .. import main
    main()
