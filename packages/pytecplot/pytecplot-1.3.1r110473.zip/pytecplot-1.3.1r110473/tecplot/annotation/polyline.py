import ctypes

from ..tecutil import _tecutil
from .. import constant, tecutil, version

from . import geometry


class Arrowhead(object):
    """Polyline arrowhead properties.

    .. seealso:: `Frame.add_polyline()`

    .. code-block:: python
        :emphasize-lines: 10-12

        import tecplot as tp
        from tecplot.constant import *

        frame = tp.active_frame()

        line0 = frame.add_polyline([[30,30], [50,60]], coord_sys=CoordSys.Frame)
        line1 = frame.add_polyline([[35,30], [55,60]], coord_sys=CoordSys.Frame)
        line2 = frame.add_polyline([[40,30], [60,60]], coord_sys=CoordSys.Frame)

        line0.arrowhead.attachment = ArrowheadAttachment.AtEnd
        line1.arrowhead.attachment = ArrowheadAttachment.AtEnd
        line2.arrowhead.attachment = ArrowheadAttachment.AtEnd

        line0.line_thickness = 2
        line1.line_thickness = 2
        line2.line_thickness = 2

        tp.export.save_png('arrowhead.png', 600)

    .. figure:: /_static/images/arrowhead.png
        :width: 300px
        :figwidth: 300px
    """
    def __init__(self, polyline):
        self.polyline = polyline
        self.uid = self.polyline.uid
        self.frame = self.polyline.frame

    @property
    def angle(self):
        """`float`: The angle of the arrow lines in degrees.

        This is the angle that one side of the arrowhead makes with the vector,
        i.e. the apex angle is twice the arrowhead angle::

            >>> from tecplot.constant import ArrowheadAttachment
            >>> polyline.arrowhead.attachment = ArrowheadAttachment.AtEnd
            >>> polyline.arrowhead.angle = 45
        """
        with self.frame.activated():
            return _tecutil.GeomArrowheadGetAngle(self.uid)

    @angle.setter
    @tecutil.lock()
    def angle(self, value):
        with self.frame.activated():
            _tecutil.GeomArrowheadSetAngle(self.uid, float(value))

    @property
    def attachment(self):
        """`ArrowheadAttachment`: Location of arrowhead on the polyline.

        Possible values are `ArrowheadAttachment.None_`,
        `ArrowheadAttachment.AtBeginning`, `ArrowheadAttachment.AtEnd` and
        `ArrowheadAttachment.AtBothEnds`::

            >>> from tecplot.constant import ArrowheadAttachment
            >>> polyline.arrowhead.attachment = ArrowheadAttachment.AtEnd
        """
        with self.frame.activated():
            return _tecutil.GeomArrowheadGetAttach(self.uid)

    @attachment.setter
    @tecutil.lock()
    def attachment(self, value):
        attachment = constant.ArrowheadAttachment(value)
        with self.frame.activated():
            _tecutil.GeomArrowheadSetAttach(self.uid, attachment.value)

    @property
    def size(self):
        """`float`: Size of the arrowhead on the polyline.

        This is in the coordinate system specified by the
        `position_coordinate_system <Polyline2D.position_coordinate_system>`
        attribute of the polyline::

            >>> from tecplot.constant import ArrowheadAttachment
            >>> polyline.arrowhead.attachment = ArrowheadAttachment.AtEnd
            >>> polyline.arrowhead.size = 10
        """
        with self.frame.activated():
            return _tecutil.GeomArrowheadGetSize(self.uid)

    @size.setter
    @tecutil.lock()
    def size(self, value):
        with self.frame.activated():
            _tecutil.GeomArrowheadSetSize(self.uid, float(value))

    @property
    def style(self):
        """`ArrowheadStyle`: The style of the arrowhead on the polyline.

        Possible values are `ArrowheadStyle.Plain`, `ArrowheadStyle.Hollow` and
        `ArrowheadStyle.Filled`::

            >>> from tecplot.constant import ArrowheadAttachment, ArrowheadStyle
            >>> polyline.arrowhead.attachment = ArrowheadAttachment.AtEnd
            >>> polyline.arrowhead.style = ArrowheadStyle.Filled
        """
        with self.frame.activated():
            return _tecutil.GeomArrowheadGetStyle(self.uid)

    @style.setter
    @tecutil.lock()
    def style(self, value):
        style = constant.ArrowheadStyle(value)
        with self.frame.activated():
            _tecutil.GeomArrowheadSetStyle(self.uid, style.value)


class Polyline(geometry.Geometry):
    def __init__(self, index, mpolyline):
        self.index = tecutil.Index(index)
        self.mpolyline = mpolyline
        self.uid = self.mpolyline.uid
        self.frame = self.mpolyline.frame

    def __len__(self):
        with self.frame.activated():
            return _tecutil.GeomMPolyGetPointCount(self.uid, self.index + 1)


class Polyline2D(Polyline, geometry.Geometry2D):
    """A series of connected points in 2D.

    .. seealso:: `Frame.add_polyline()`

    .. code-block:: python
        :emphasize-lines: 14-16

        from __future__ import division
        import math

        import tecplot as tp
        from tecplot.constant import *

        # create sine-wave in frame % coordinates
        xx = list(range(10, 90))
        yy = [10 * math.sin(x / 5) + 50 for x in xx]
        points = [(x, y) for x, y in zip(xx, yy)]

        frame = tp.active_frame()

        line = frame.add_polyline(points, coord_sys=CoordSys.Frame)
        line.line_thickness = 2
        line.color = Color.Blue

        tp.export.save_png('polyline2d.png', 600)

    .. figure:: /_static/images/polyline2d.png
        :width: 300px
        :figwidth: 300px
    """
    @property
    def arrowhead(self):
        """`Arrowhead`: Style control for arrowheads.

        Example usage::

            >>> from tecplot.constant import ArrowheadAttachment, ArrowheadStyle
            >>> polyline.arrowhead.attachment = ArrowheadAttachment.AtEnd
            >>> polyline.arrowhead.style = ArrowheadStyle.Filled
        """
        return Arrowhead(self)

    def __getitem__(self, i):
        if __debug__:
            if i >= len(self):
                raise IndexError
        with self.frame.activated():
            pos = _tecutil.Geom2DMPolyGetPoint(self.uid, self.index + 1, i + 1)
            return tecutil.XY(*pos)

    @tecutil.lock()
    def __setitem__(self, i, values):
        if isinstance(i, slice):
            num_points = len(self)
            if i == slice(None, None, None):
                x = (ctypes.c_double * num_points)(*[v[0] for v in values])
                y = (ctypes.c_double * num_points)(*[v[1] for v in values])
            else:
                x = (ctypes.c_double * num_points)()
                y = (ctypes.c_double * num_points)()
                for j in range(len(self)):
                    x[j], y[j] = self[j]
                x[i] = [v[0] for v in values]
                y[i] = [v[1] for v in values]
        else:
            x, y = (float(v) for v in values)
        with self.frame.activated():
            if isinstance(x, ctypes.Array):
                if version.sdk_version_info < (2018, 3, 1) and self.index > 0:
                    for j, (xx, yy) in enumerate(zip(x, y)):
                        _tecutil.Geom2DMPolySetPoint(self.uid, self.index + 1, j + 1, xx, yy)
                else:
                    _tecutil.Geom2DMPolySetPolyline(self.uid, self.index + 1, x, y)
            else:
                _tecutil.Geom2DMPolySetPoint(self.uid, self.index + 1, i + 1, x, y)


class Polyline3D(Polyline):
    """A series of connected points in 3D.

    .. seealso:: `Frame.add_polyline()`

    .. code-block:: python
        :emphasize-lines: 19-21

        from __future__ import division
        import math

        import tecplot as tp
        from tecplot.constant import *

        # create helix polyline in data coordinates
        zz = [z / 2000 for z in range(1000)]
        xx = [0.5 * math.cos(z * 50) for z in zz]
        yy = [0.5 * math.sin(z * 50) for z in zz]
        points = [(x, y, z) for x, y, z in zip(xx, yy, zz)]

        frame = tp.active_frame()
        dataset = frame.create_dataset('Dataset Name', ['x', 'y', 'z'])
        dataset.add_ordered_zone('Zone Name', (10, 10, 10))
        plot = frame.plot(PlotType.Cartesian3D)
        plot.activate()

        line = frame.add_polyline(points)
        line.line_thickness = 2
        line.color = Color.Chartreuse

        tp.export.save_png('polyline3d.png', 600)

    .. figure:: /_static/images/polyline3d.png
        :width: 300px
        :figwidth: 300px
    """
    def __getitem__(self, i):
        if __debug__:
            if i >= len(self):
                raise IndexError
        with self.frame.activated():
            pos = _tecutil.Geom3DMPolyGetPoint(self.uid, self.index + 1, i + 1)
            return tecutil.XYZ(*pos)

    @tecutil.lock()
    def __setitem__(self, i, values):
        if isinstance(i, slice):
            num_points = len(self)
            if i == slice(None, None, None):
                x = (ctypes.c_double * num_points)(*[v[0] for v in values])
                y = (ctypes.c_double * num_points)(*[v[1] for v in values])
                z = (ctypes.c_double * num_points)(*[v[2] for v in values])
            else:
                x = (ctypes.c_double * num_points)()
                y = (ctypes.c_double * num_points)()
                z = (ctypes.c_double * num_points)()
                for j in range(len(self)):
                    x[j], y[j], z[j] = self[j]
                x[i] = [v[0] for v in values]
                y[i] = [v[1] for v in values]
                z[i] = [v[2] for v in values]
        else:
            x, y, z = (float(v) for v in values)
        with self.frame.activated():
            if isinstance(x, ctypes.Array):
                if version.sdk_version_info < (2018, 3, 1) and self.index > 0:
                    for j, (xx, yy, zz) in enumerate(zip(x, y, z)):
                        _tecutil.Geom3DMPolySetPoint(self.uid, self.index + 1, j + 1, xx, yy, zz)
                else:
                    _tecutil.Geom3DMPolySetPolyline(self.uid, self.index + 1, x, y, z)
            else:
                _tecutil.Geom3DMPolySetPoint(self.uid, self.index + 1, i + 1, x, y, z)


class MultiPolyline(geometry.Geometry):
    def __len__(self):
        with self.frame.activated():
            return _tecutil.GeomMPolyGetPolylineCnt(self.uid)


class MultiPolyline2D(MultiPolyline, geometry.Geometry2D):
    """A collection of `Polyline2D` objects.

    .. seealso:: `Frame.add_polyline()`

    .. code-block:: python
        :emphasize-lines: 17-19

        from __future__ import division
        import math

        import tecplot as tp
        from tecplot.constant import *

        # create sine-wave in frame % coordinates
        xx = list(range(10, 90))
        yy = [10 * math.sin(x / 5) + 50 for x in xx]
        points = [(x, y) for x, y in zip(xx, yy)]

        # create new line with points shifted up and to the left
        shifted_points = [(x + 5, y + 5) for x, y in points]

        frame = tp.active_frame()

        multi_line = frame.add_polyline(points, shifted_points, coord_sys=CoordSys.Frame)
        multi_line.line_thickness = 2
        multi_line.color = Color.Blue

        tp.export.save_png('multipolyline2d.png', 600)

    .. figure:: /_static/images/multipolyline2d.png
        :width: 300px
        :figwidth: 300px
    """
    @property
    def arrowhead(self):
        """`Arrowhead`: Style control for arrowheads.

        Example usage::

            >>> from tecplot.constant import ArrowheadAttachment, ArrowheadStyle
            >>> multi_polyline.arrowhead.attachment = ArrowheadAttachment.AtEnd
            >>> multi_polyline.arrowhead.style = ArrowheadStyle.Filled
        """
        return Arrowhead(self)

    def __getitem__(self, i):
        if __debug__:
            if i >= len(self):
                raise IndexError
        return Polyline2D(i, self)


class MultiPolyline3D(MultiPolyline):
    """A collection of `Polyline3D` objects.

    .. seealso:: `Frame.add_polyline()`

    .. code-block:: python
        :emphasize-lines: 20-22

        from __future__ import division
        import math

        import tecplot as tp
        from tecplot.constant import *

        # create double-helix multi-polyline in data coordinates
        zz = [z / 2000 for z in range(1000)]
        xx = [0.5 * math.cos(z * 50) for z in zz]
        yy = [0.5 * math.sin(z * 50) for z in zz]
        points = [(x, y, z) for x, y, z in zip(xx, yy, zz)]
        points_shifted = [(x, y, z + 0.02) for x, y, z in zip(xx, yy, zz)]

        frame = tp.active_frame()
        dataset = frame.create_dataset('Dataset Name', ['x', 'y', 'z'])
        dataset.add_ordered_zone('Zone Name', (10, 10, 10))
        plot = frame.plot(PlotType.Cartesian3D)
        plot.activate()

        line = frame.add_polyline(points, points_shifted)
        line.line_thickness = 2
        line.color = Color.Turquoise

        tp.export.save_png('multipolyline3d.png', 600)

    .. figure:: /_static/images/multipolyline3d.png
        :width: 300px
        :figwidth: 300px
    """
    def __getitem__(self, i):
        if __debug__:
            if i >= len(self):
                raise IndexError
        return Polyline3D(i, self)
