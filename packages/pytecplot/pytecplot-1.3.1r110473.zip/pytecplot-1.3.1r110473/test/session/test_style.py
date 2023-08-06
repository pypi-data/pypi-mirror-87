from builtins import int, str

import ctypes
import numpy as np
import logging
import os
import platform
import sys

from ctypes import *
from contextlib import contextmanager
from enum import Enum
from textwrap import dedent
import unittest
from unittest.mock import patch, Mock, call

from test import patch_tecutil, skip_if_connected

import tecplot as tp
from tecplot import session, tecutil
from tecplot.constant import GetValueReturnCode, SetValueReturnCode, PlotType, SurfacesToPlot, Color
from tecplot.exception import *
from tecplot.tecutil import IndexSet, StringList, sv

from ..sample_data import sample_data


class TestSetStyle(unittest.TestCase):
    def setUp(self):
        self.setx_arglists = []
        def _setx(arglist,self=self):
            d = dict(arglist)
            for k,v in d.items():
                if isinstance(v,IndexSet):
                    d[k] = set(v)
            self.setx_arglists.append(d)
            return SetValueReturnCode.Ok
        self.setx = Mock(side_effect=_setx)
        self.patches = [
            patch.object(tp.tecutil._tecutil, 'StyleSetLowLevelX', self.setx),
        ]
        for p in self.patches:
            p.start()

    def tearDown(self):
        for p in self.patches:
            p.stop()

    @skip_if_connected
    def test_log(self):
        if __debug__:
            loglevel = logging.root.getEffectiveLevel()
            logging.root.setLevel(logging.DEBUG)
            with patch.object(tp.session.style.log, 'debug', Mock()) as log:
                tp.session.set_style('value',str(sv.P1),str(sv.P2),key1=str('key1value'))
                self.assertEqual(log.call_args_list[0][0][0], dedent('''\
                    SetStyle
                      value: value
                      {0} P1
                      {0} P2
                      key1 : {0} key1value'''.format(type(str()))))
                self.assertEqual(log.call_args_list[1][0][0], dedent('''\
                    SetStyle
                      P1: P1
                      P2: P2
                      STRVALUE: value
                      KEY1: key1value'''))
            logging.root.setLevel(loglevel)

    def test_enum(self):
        class MyEnum(Enum):
            Key = 2
        tp.session.set_style(MyEnum.Key)
        self.assertEqual({k:MyEnum(getattr(v, 'value', v))
                          for k, v in self.setx_arglists[-1].items()},
                         {sv.IVALUE:MyEnum.Key})

    def test_index(self):
        i = tp.tecutil.Index(4)
        tp.session.set_style(i)
        arglist = self.setx_arglists[-1]
        self.assertEqual({k:getattr(v, 'value', v) for k, v in arglist.items()},
                         {sv.IVALUE:i+1})

    def test_int(self):
        i = 4
        tp.session.set_style(i)
        arglist = self.setx_arglists[-1]
        self.assertEqual({k:getattr(v, 'value', v) for k, v in arglist.items()},
                         {sv.IVALUE:4})

        if __debug__:
            with self.assertRaises((TecplotOverflowError, TecplotTypeError)):
                tp.session.set_style(2**64 + 1)

    def test_bool(self):
        i = True
        tp.session.set_style(i)
        arglist = self.setx_arglists[-1]
        self.assertEqual({k:getattr(v, 'value', v) for k, v in arglist.items()},
                         {sv.IVALUE:1})

    def test_float(self):
        i = 3.1415
        tp.session.set_style(i)
        arglist = self.setx_arglists[-1]
        self.assertEqual(list(arglist.keys()),[sv.DVALUE])
        self.assertTrue(np.isclose(arglist[sv.DVALUE], 3.1415))

    def test_str(self):
        i = 'test'
        tp.session.set_style(i)
        arglist = self.setx_arglists[-1]
        self.assertEqual(arglist, {sv.STRVALUE:'test'})

    def test_lists(self):

        def _setx(arglist,self=self):
            val = arglist[sv.IVALUE]
            addr = ctypes.c_size_t(getattr(val, 'value', val))
            ptr = ctypes.c_void_p(addr.value)
            iset = ctypes.cast(ptr, IndexSet)
            self.assertEqual(set(iset), {1,2,3})
            return SetValueReturnCode.Ok
        setx = Mock(side_effect=_setx)
        with patch.object(tp.tecutil._tecutil, 'StyleSetLowLevelX', setx):
            tp.session.set_style({1,2,3})

    def test_stringlist(self):
        def _setx(arglist,self=self):
            val = arglist[sv.IVALUE]
            addr = ctypes.c_size_t(getattr(val, 'value', val))
            ptr = ctypes.c_void_p(addr.value)
            iset = ctypes.cast(ptr, StringList)
            self.assertEqual(list(iset), ['aa','bb'])
            return SetValueReturnCode.Ok
        setx = Mock(side_effect=_setx)
        with patch.object(tp.tecutil._tecutil, 'StyleSetLowLevelX', setx):
            tp.session.set_style(['aa','bb'])

    def test_none(self):
        i = None
        tp.session.set_style(i)
        arglist = self.setx_arglists[-1]
        self.assertEqual({k:getattr(v, 'value', v) for k, v in arglist.items()},
                         {sv.IVALUE:0})

    def test_errors(self):
        class UnknownType(object):
            pass
        with self.assertRaises(TecplotTypeError):
            tp.session.set_style(UnknownType())

        def _setx(arglist,self=self):
            return SetValueReturnCode.ValueSyntaxError
        setx = Mock(side_effect=_setx)
        with patch.object(tp.tecutil._tecutil, 'StyleSetLowLevelX', setx):
            with self.assertRaises(TecplotSystemError):
                tp.session.set_style(1)

        with patch_tecutil('StyleSetLowLevelX', side_effect=TecplotLogicError):
            with self.assertRaises(TecplotLogicError):
                tp.session.set_style(1)

    def test_kwargs(self):
        uid = 2
        objset = {3,4}
        off1 = 5
        off2 = 6
        tp.session.set_style(0, **{sv.UNIQUEID:uid, sv.OBJECTSET:objset,
            sv.OFFSET1: off1, sv.OFFSET2: off2})
        al = self.setx_arglists[-1]
        svlist = [sv.UNIQUEID, sv.OBJECTSET, sv.OFFSET1, sv.OFFSET2]
        exlist = [2, {3, 4}, 5 + 1, 6 + 1]
        for s, e in zip(svlist, exlist):
            v = al[s]
            self.assertEqual(getattr(v, 'value', v), e)


class TestGetStyle(unittest.TestCase):
    def setUp(self):
        if tp.tecutil._tecutil_connector.connected:
            raise unittest.SkipTest('batch only tests')

    def test_int(self):
        def modify_arglist(al):
            # print(type(al[sv.IVALUE]), al[sv.IVALUE])
            al[sv.IVALUE][0] = 1
            return GetValueReturnCode.Ok
        with patch_tecutil('StyleGetLowLevelX', side_effect=modify_arglist):
            self.assertEqual(tp.session.get_style(int), 1)

    def test_log(self):
        if __debug__:
            loglevel = logging.root.getEffectiveLevel()
            logging.root.setLevel(logging.DEBUG)
            with patch_tecutil('StyleGetLowLevelX',
                               return_value=GetValueReturnCode.Ok):
                with patch.object(tp.session.style.log, 'debug', Mock()) as log:
                    tp.session.get_style(str,str(sv.P1),str(sv.P2),key1=str('key1value'))
                    self.assertEqual(log.call_args_list[0][0][0], dedent('''\
                        GetStyle
                          {0} P1
                          {0} P2
                          key1 : {0} key1value'''.format(type(str()))))
                    expected = dedent('''\
                        GetStyle
                          P1: P1
                          P2: P2
                          KEY1: key1value
                          IVALUE:''')
                    self.assertEqual(
                        log.call_args_list[1][0][0][:len(expected)],
                        expected)
            logging.root.setLevel(loglevel)

    def test_kwargs(self):
        def fn(al):
            self.assertEqual(al[sv.UNIQUEID], 2)
            self.assertEqual(al[sv.OBJECTSET], {3,4})
            self.assertEqual(al[sv.OFFSET1], 5+1)
            self.assertEqual(al[sv.OFFSET2], 6+1)
            return GetValueReturnCode.Ok
        class UnknownType(object):
            pass
        uid = 2
        objset = {3,4}
        off1 = 5
        off2 = 6
        with patch_tecutil('StyleGetLowLevelX', side_effect=fn):
            with self.assertRaises(TecplotTypeError):
                tp.session.get_style(UnknownType, **{sv.UNIQUEID:uid,
                    sv.OBJECTSET:objset, sv.OFFSET1: off1, sv.OFFSET2: off2})

    def test_float(self):
        v = 3.14
        def modify_arglist(al,v=v):
            al[sv.DVALUE][0] = v
            return GetValueReturnCode.Ok
        with patch_tecutil('StyleGetLowLevelX', side_effect=modify_arglist):
            self.assertEqual(tp.session.get_style(float), v)

    def test_errors(self):
        def fn(al):
            return GetValueReturnCode.SyntaxError
        with patch_tecutil('StyleGetLowLevelX', side_effect=fn):
            with self.assertRaises(TecplotSystemError):
                tp.session.get_style(str)

        with patch_tecutil('StyleGetLowLevelX', side_effect=TecplotLogicError):
            with self.assertRaises(TecplotLogicError):
                tp.session.get_style(int)

    def test_enum(self):
        class MyEnum(Enum):
            A = 0
            B = 1
        v = MyEnum.B
        def modify_arglist(al,v=v):
            al[sv.IVALUE][0] = v.value
            return GetValueReturnCode.Ok
        with patch_tecutil('StyleGetLowLevelX', side_effect=modify_arglist):
            self.assertEqual(tp.session.get_style(MyEnum), v)

    def test_list(self):
        v = [1,2,3]
        def modify_arglist(al,v=v):
            iset = IndexSet(*v)
            al[sv.IVALUE][0] = addressof(cast(iset,POINTER(c_int64)).contents)
            return GetValueReturnCode.Ok
        with patch_tecutil('StyleGetLowLevelX', side_effect=modify_arglist):
            self.assertEqual(tp.session.get_style(list), v)

    def test_bool(self):
        v = False
        def fn(al,v=v):
            al[sv.IVALUE][0] = v
            return GetValueReturnCode.Ok
        with patch_tecutil('StyleGetLowLevelX', side_effect=fn):
            self.assertEqual(tp.session.get_style(bool), v)

        v = True
        def fn(al,v=v):
            al[sv.IVALUE][0] = v
            return GetValueReturnCode.Ok
        with patch_tecutil('StyleGetLowLevelX', side_effect=fn):
            self.assertEqual(tp.session.get_style(bool), v)

    def test_str(self):
        s = c_char_p(b'abc')
        def modify_arglist(al,s=s):
            addr = addressof(cast(s, POINTER(c_char)).contents)
            ptr = pointer(c_int64(addr))
            al[sv.IVALUE][0] = ptr.contents
            return GetValueReturnCode.Ok
        with patch_tecutil('StyleGetLowLevelX', side_effect=modify_arglist):
            self.assertEqual(tp.session.get_style(str), s.value.decode())

        def modify_arglist(al):
            al[sv.IVALUE][0] = c_longlong(0)
            return GetValueReturnCode.Ok
        with patch_tecutil('StyleGetLowLevelX', side_effect=modify_arglist):
            self.assertIsNone(tp.session.get_style(str))


class TestStyle(unittest.TestCase):
    def setUp(self):
        self.filename,self.dataset = sample_data('10x10x10')
        frame = tp.active_frame()

        frame.plot_type = PlotType.Cartesian3D
        self.plot = frame.plot()
        contour = self.plot.contour(0)
        contour.variable_index = self.dataset.variable('Z').index
        fieldmap = self.plot.fieldmap(0)
        fieldmap.surfaces.surfaces_to_plot = SurfacesToPlot.BoundaryFaces
        self.plot.show_contour = True

        self.override = frame.plot().contour(0).colormap_filter.override(0)
        self.override_style = session.Style(*self.override._sv,
            offset1=contour.index, offset2=self.override.index)

        self.plot_style = session.Style(*self.plot._sv)

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    def test_nouid_offset1_offset2(self):
        for val in [Color.Red,Color.Blue]:
            self.override_style._set_style(val,sv.COLOR)
            self.assertEqual(self.override_style._get_style(Color,sv.COLOR),
                             self.override.color)
            self.assertEqual(self.override.color, val)

    def test_nouid_nooffset(self):
        for val in [True,False,True]:
            self.plot_style._set_style(val, sv.SHOWCONTOUR)
            self.assertEqual(self.plot_style._get_style(bool, sv.SHOWCONTOUR),
                             self.plot.show_contour)
            self.assertEqual(self.plot.show_contour, val)

    def test_offset1(self):
        y,z = (self.dataset.variable(x) for x in ['Y','Z'])
        ctr = self.plot.fieldmap(0).contour
        ctr.flood_contour_group = self.plot.contour(0)
        ctr.line_group = self.plot.contour(1)
        ctr.flood_contour_group.variable = y
        ctr.line_group.variable = z
        self.assertEqual(ctr.flood_contour_group.variable, y)
        self.assertEqual(ctr.line_group.variable, z)
        ctr.flood_contour_group.variable = z
        ctr.line_group.variable = y
        self.assertEqual(ctr.flood_contour_group.variable, z)
        self.assertEqual(ctr.line_group.variable, y)


class TestSubStyle(unittest.TestCase):
    def test_init(self):
        class Parent(Mock):
            pass
        parent = Parent()
        sty = session.SubStyle(parent, 'TEST')
        self.assertEqual(sty.parent, parent)
        self.assertEqual(sty._svargs, ['TEST'])

    def test_eq(self):
        class Parent:
            def __init__(self, uid):
                self.uid = uid
            def __eq__(self, other):
                return self.uid == other.uid

        sty0 = session.SubStyle(Parent(0), 'TEST')
        sty1 = session.SubStyle(Parent(0), 'BLAH')
        self.assertFalse(sty0 == sty1)
        self.assertTrue(sty0 != sty1)
        sty2 = session.SubStyle(Parent(1), 'TEST')
        self.assertFalse(sty0 == sty2)
        self.assertTrue(sty0 != sty2)
        sty3 = session.SubStyle(Parent(0), 'TEST')
        self.assertTrue(sty0 == sty3)
        self.assertFalse(sty0 != sty3)

    def test_style(self):
        class Parent:
            def __init__(self, uid):
                self.uid = uid
            def __eq__(self, other):
                return self.uid == other.uid
            def _get_style(self, *a, **kw):
                pass
            def _set_style(self, *a, **kw):
                pass
        parent = Parent(0)
        with patch.object(parent, '_get_style') as sget:
            with patch.object(parent, '_set_style') as sset:
                sty = session.SubStyle(parent, 'TEST')
                sty._get_style(int, 'ONE', test=1)
                sget.assert_called_with(int, 'TEST', 'ONE', test=1)
                sset.assert_not_called()

                sget.reset_mock()
                sty._set_style(int(1), 'ONE', test=1)
                sget.assert_not_called()
                sset.assert_called_with(1, 'TEST', 'ONE', test=1)


class TestStyleConfig(unittest.TestCase):
    def setUp(self):
        self.get = []
        self.set = []

        class CaptureGetSetStyle:
            def _get_style(cls, value_type, svargs):
                self.get.append((value_type, svargs))
                return (value_type.__name__, svargs)

            def _set_style(cls, value, svargs):
                self.set.append((value, svargs))

        class ConfigB(CaptureGetSetStyle, tp.session.style.StyleConfig):
            prop = tp.session.style.style_property(int, 'PROP')

        class ConfigA(CaptureGetSetStyle, tp.session.style.StyleConfig):
            b = ConfigB('a.b', 'B')
            prop = tp.session.style.style_property(bool, 'TEST')

        class configuration(CaptureGetSetStyle, tp.session.style.StyleConfig):
            a = ConfigA('a', 'A')

        self.conf = configuration()

    def test_config(self):
        self.assertEqual(self.conf.a.prop, (bool.__name__, 'TEST'))
        self.assertEqual(self.conf.a.b.prop, (int.__name__, 'PROP'))
        self.conf.a.prop = True
        self.assertEqual(self.set[-1], (True, 'TEST'))
        self.conf.a.b.prop = 5
        self.assertEqual(self.set[-1], (5, 'PROP'))
        self.conf.a.b.prop = 6
        self.assertEqual(self.set[-1], (6, 'PROP'))

    def test_str(self):
        exp = "a.prop = ('{}', 'TEST')\na.b.prop = ('{}', 'PROP')"
        exp = exp.format(bool.__name__, int.__name__)
        res = str(self.conf)
        self.assertEqual(res, exp)

        # some state is cached first time so call it again
        res = str(self.conf)
        self.assertEqual(res, exp)

    def test_lock_attrs(self):
        with self.assertRaises(TecplotAttributeError):
            self.conf.a.no_property = 'test'

        # some state is cached first time so call it again
        with self.assertRaises(TecplotAttributeError):
            self.conf.a.no_property = 'test'


class TestStyleProperty(unittest.TestCase):
    def test_properties(self):
        class A(object):
            def _get_style(self, *a, **kw):
                pass
            def _set_style(self, *a, **kw):
                pass
            x = tp.session.style.style_property(int, 'X')
            y = tp.session.style.style_property(float, 'Y', lambda x: float((x or 0) + 1))
            z = tp.session.style.style_property(float, 'Z', lambda x: x)

        a = A()
        with patch.object(a, '_get_style') as sget:
            with patch.object(a, '_set_style') as sset:
                _ = a.x
                sget.assert_called_with(int, 'X')
                sset.assert_not_called()
                sget.reset_mock()
                a.x = 2
                sget.assert_not_called()
                sset.assert_called_with(2, 'X')
                sset.reset_mock()

                _ = a.y
                sget.assert_called_with(float, 'Y')
                sset.assert_not_called()
                sget.reset_mock()
                a.y = 2
                sget.assert_not_called()
                sset.assert_called_with(float(2 + 1), 'Y')
                sset.reset_mock()

                a.x = None
                sget.assert_not_called()
                sset.assert_not_called()

                a.y = None
                sget.assert_not_called()
                sset.assert_called_with(float(float(0) + 1), 'Y')
                sset.reset_mock()

                a.z = None
                sget.assert_not_called()
                sset.assert_not_called()


class TestNamedTupleStyle(unittest.TestCase):
    class Parent:
        def __init__(self, uid):
            self.uid = uid
        def __eq__(self, other):
            return self.uid == other.uid
        def _get_style(self, *a, **kw):
            pass
        def _set_style(self, *a, **kw):
            pass

    class IJK(tp.session.style.NamedTupleStyle):
        _keys = ('i', 'j', 'k')
        i = tp.session.style.style_property(int, sv.I)
        j = tp.session.style.style_property(int, sv.J)
        k = tp.session.style.style_property(int, sv.K)

    def setUp(self):
        self.parent = TestNamedTupleStyle.Parent(0)
        self.ijk = TestNamedTupleStyle.IJK(self.parent, 'TEST')

    def test_len(self):
        self.assertEqual(len(self.ijk), 3)

    def test_getitem(self):
        with patch.object(self.parent, '_get_style', Mock(return_value=1)) as sget:
            _ = tuple(self.ijk)
            self.assertEqual(sget.call_count, 3)
            sget.assert_has_calls((
                call(int, 'TEST', 'I'),
                call(int, 'TEST', 'J'),
                call(int, 'TEST', 'K')))
            self.assertEqual(self.ijk[1:], (1,1))
            self.assertEqual(self.ijk[:1], (1,))
            self.assertEqual(self.ijk[::3], (1,))

    def test_setitem(self):
        with patch.object(self.parent, '_set_style') as sset:
            self.ijk[:] = (1, 2, 3)
            self.assertEqual(sset.call_count, 3)
            sset.assert_has_calls((
                call(1, 'TEST', 'I'),
                call(2, 'TEST', 'J'),
                call(3, 'TEST', 'K')))
            sset.reset_mock()
            self.ijk.j = 4
            self.assertEqual(sset.call_count, 1)
            sset.assert_called_with(4, 'TEST', 'J')

    def test_iter(self):
        with patch.object(self.parent, '_get_style', Mock(return_value=1)) as sget:
            for i, val in enumerate(self.ijk):
                self.assertEqual(val, 1)
            self.assertEqual(i, 2)

    def test_str(self):
        with patch.object(self.parent, '_get_style', Mock(return_value=1)) as sget:
            self.assertEqual(str(self.ijk), '(1, 1, 1)')

    def test_eq(self):
        parent0 = TestNamedTupleStyle.Parent(0)
        parent1 = TestNamedTupleStyle.Parent(1)
        ijk0 = TestNamedTupleStyle.IJK(parent0, 'TEST')
        ijk0_blah = TestNamedTupleStyle.IJK(parent0, 'BLAH')
        ijk1 = TestNamedTupleStyle.IJK(parent1, 'TEST')
        self.assertTrue(ijk0 == self.ijk)
        self.assertFalse(ijk0 != self.ijk)
        self.assertTrue(ijk0_blah == self.ijk)
        self.assertFalse(ijk0_blah != self.ijk)
        self.assertTrue(ijk1 == self.ijk)
        self.assertFalse(ijk1 != self.ijk)


class TestIndexRange(unittest.TestCase):
    class Parent:
        def __init__(self, uid):
            self.uid = uid
            self._values = {}
        def __eq__(self, other):
            return self.uid == other.uid
        def _get_style(self, rettype, *a, **kw):
            return rettype(self._values[a])
        def _set_style(self, value, *a, **kw):
            self._values[a] = value

    def setUp(self):
        self.parent = TestIndexRange.Parent(0)
        self.rng = tp.session.IndexRange(self.parent, 'TEST')
        self.rng[:] = (1,1,1)

    def test_setget(self):
        self.rng[:] = (1,1,1)
        self.assertEqual(tuple(self.rng), (1,1,1))

        self.rng[:] = (2,3,4)
        self.assertEqual(tuple(self.rng), (2,3,4))

        self.rng[:] = (None, None, None)
        self.assertEqual(tuple(self.rng), (0, -1, 1))

        self.rng[:] = (None, 0, 1)
        self.assertEqual(tuple(self.rng), (0, 0, 1))


if __name__ == '__main__':
    from .. import main
    main()
