from ..tecutil import _tecutil
from .. import constant, tecutil
from . import annotation


class Geometry(annotation.Annotation):
    """Base class for all geometric shape annotations."""
    @property
    def color(self):
        """`Color`: Line `Color`.

        This example shows how to change the edge or line `Color` to red::

            >>> from tecplot.constant import Color, CoordSys
            >>> geom = frame.add_circle((50, 50), 10, CoordSys.Frame)
            >>> geom.color = Color.Red
        """
        return constant.Color(_tecutil.GeomGetColor(self.uid))

    @color.setter
    @tecutil.lock()
    def color(self, value):
        with self.frame.activated():
            _tecutil.GeomSetColor(self.uid, constant.Color(value).value)

    @property
    def fill_color(self):
        """`constant.Color`: Background fill color.

        This example shows how to change the area fill `Color` to red. To turn
        off filling the geometry, set this attribute to `None`::

            >>> from tecplot.constant import Color, CoordSys
            >>> geom = frame.add_circle((50, 50), 10, CoordSys.Frame)
            >>> geom.fill_color = Color.Red
        """
        with self.frame.activated():
            is_filled = _tecutil.GeomGetIsFilled(self.uid)
            if is_filled:
                return constant.Color(_tecutil.GeomGetFillColor(self.uid))

    @fill_color.setter
    @tecutil.lock()
    def fill_color(self, value):
        with self.frame.activated():
            if value is None:
                _tecutil.GeomSetIsFilled(self.uid, False)
            else:
                _tecutil.GeomSetIsFilled(self.uid, True)
                _tecutil.GeomSetFillColor(self.uid, constant.Color(value).value)

    @property
    def line_pattern(self):
        """`LinePattern`: Pattern used for drawing lines or edges.

        This example shows how to change the line pattern::

            >>> from tecplot.constant import CoordSys, LinePattern
            >>> geom = frame.add_circle((50, 50), 10, CoordSys.Frame)
            >>> geom.line_pattern = LinePattern.DashDot
        """
        with self.frame.activated():
            return constant.LinePattern(_tecutil.GeomGetLinePattern(self.uid))

    @line_pattern.setter
    @tecutil.lock()
    def line_pattern(self, value):
        with self.frame.activated():
            line_pattern = constant.LinePattern(value)
            _tecutil.GeomSetLinePattern(self.uid, line_pattern.value)

    @property
    def line_thickness(self):
        """`float`: Thickness of lines or edges.

        This example shows how to change the line thickness::

            >>> from tecplot.constant import CoordSys
            >>> geom = frame.add_circle((50, 50), 10, CoordSys.Frame)
            >>> geom.line_thickness = 4.0
        """
        with self.frame.activated():
            return _tecutil.GeomGetLineThickness(self.uid)

    @line_thickness.setter
    @tecutil.lock()
    def line_thickness(self, value):
        with self.frame.activated():
            _tecutil.GeomSetLineThickness(self.uid, float(value))

    @property
    def pattern_length(self):
        """`float`: Length of the line pattern.

        This example shows how to change the pattern length::

            >>> from tecplot.constant import CoordSys
            >>> geom = frame.add_circle((50, 50), 10, CoordSys.Frame)
            >>> geom.pattern_length = 1.2
        """
        with self.frame.activated():
            return _tecutil.GeomGetPatternLength(self.uid)

    @pattern_length.setter
    @tecutil.lock()
    def pattern_length(self, value):
        with self.frame.activated():
            _tecutil.GeomSetPatternLength(self.uid, float(value))


class Geometry2D(Geometry, annotation.MovableAnnotation):
    @property
    def clipping(self):
        """`Clipping`: Clip geometry to the axes or frame for 2D plots.

        Clipping refers to displaying only that portion of an object that falls
        within a specified clipping region of the plot. If you have specified
        the position in the Frame coordinate system, the `Annotation` will be
        clipped to the frame. Default: `Clipping.ClipToViewport`.

        If you have specified the Grid coordinate system, you can choose to
        clip your `Annotation` to the frame or the viewport. The size of the
        viewport depends on the plot type as follows:

            * 3D Cartesian - The viewport is the same as the frame, so viewport
                clipping is the same as frame clipping.
            * 2D Cartesian/XY Line - The viewport is defined by the extents of
                the X and Y axes.
            * Polar Line/Sketch - By default, the viewport is the same as the
                frame.

        .. warning::

            For 3D and line plots the viewport is the same as the frame and so
            clipping to the viewport or the frame will have no apparent affect.
            In cartesian 2D plots, clipping to the axes
            (`Clipping.ClipToViewport`) is only available when the position
            coordinate system is `CoordSys.Grid`.

        Example of clipping a circle to the frame::

            >>> from tecplot.constant import Clipping, CoordSys
            >>> geom = frame.add_circle((0.5, 0.5), 0.55, CoordSys.Grid)
            >>> geom.clipping = Clipping.ClipToFrame
        """
        with self.frame.activated():
            return constant.Clipping(_tecutil.GeomGetClipping(self.uid))

    @clipping.setter
    @tecutil.lock()
    def clipping(self, value):
        with self.frame.activated():
            _tecutil.GeomSetClipping(self.uid, constant.Clipping(value).value)


class CurvedGeometry(Geometry2D):
    @property
    def num_points(self):
        """`int`: Number of points to use when creating the curved shape.

        This is the number of segments along the edge plus one. Example usage::

            >>> from tecplot.constant import CoordSys
            >>> geom = frame.add_circle((50, 50), 10, CoordSys.Frame)
            >>> geom.num_points = 300
        """
        with self.frame.activated():
            return _tecutil.GeomEllipseGetNumPoints(self.uid)

    @num_points.setter
    @tecutil.lock()
    def num_points(self, value):
        _tecutil.GeomEllipseSetNumPoints(self.uid, int(value))


class Circle(CurvedGeometry):
    """A circle annotation attached to a `Frame`.

    .. seealso:: `Frame.add_circle()`

    .. code-block:: python

        import tecplot as tp
        from tecplot.constant import *

        frame = tp.active_frame()

        circle0 = frame.add_circle((40, 50), 12, CoordSys.Frame)
        circle1 = frame.add_circle((50, 50), 12, CoordSys.Frame)
        circle2 = frame.add_circle((60, 50), 12, CoordSys.Frame)

        circle0.fill_color = Color.Magenta
        circle1.fill_color = Color.Yellow
        circle2.fill_color = Color.Cyan

        tp.export.save_png('circle.png', 600)

    .. figure:: /_static/images/circle.png
        :width: 300px
        :figwidth: 300px
    """
    @property
    def radius(self):
        """`float`: Length of the radius.

        This will be in the coordinate system specified by
        `Circle.position_coordinate_system`. This example creates a circle of
        radius 5 and then doubles it to 10 later::

            >>> from tecplot.constant import CoordSys
            >>> geom = frame.add_circle((20, 30), 5, CoordSys.Frame)
            >>> geom.radius = 10
        """
        with self.frame.activated():
            return _tecutil.GeomCircleGetRadius(self.uid)

    @radius.setter
    @tecutil.lock()
    def radius(self, value):
        with self.frame.activated():
            _tecutil.GeomCircleSetRadius(self.uid, float(value))


class Ellipse(CurvedGeometry):
    """An ellipse annotation attached to a `Frame`.

    .. seealso:: `Frame.add_ellipse()`

    .. code-block:: python

        import tecplot as tp
        from tecplot.constant import *

        frame = tp.active_frame()

        ellipse0 = frame.add_ellipse((40, 45), (10, 12), CoordSys.Frame)
        ellipse1 = frame.add_ellipse((50, 50), (10, 16), CoordSys.Frame)
        ellipse2 = frame.add_ellipse((60, 55), (10, 20), CoordSys.Frame)

        ellipse0.fill_color = Color.Magenta
        ellipse1.fill_color = Color.Yellow
        ellipse2.fill_color = Color.Cyan

        tp.export.save_png('ellipse.png', 600)

    .. figure:: /_static/images/ellipse.png
        :width: 300px
        :figwidth: 300px
    """
    @property
    def size(self):
        """`tuple`: Size :math:`(h_{axis}, v_{axis})` of the ellipse.

        This is the horizontal and vertical axis lengths of the ellipse and
        will be in the coordinate system specified by
        `Ellipse.position_coordinate_system`. This example creates an ellipse
        with :math:`(h_{axis}, v_{axis})` of :math:`(5, 10)` and changes it to
        :math:`(10, 20)` later::

            >>> from tecplot.constant import CoordSys
            >>> geom = frame.add_ellipse((50, 50), (5, 10), CoordSys.Frame)
            >>> geom.size = (10, 20)
        """
        with self.frame.activated():
            return _tecutil.GeomEllipseGetSize(self.uid)

    @size.setter
    @tecutil.lock()
    def size(self, values):
        haxis, vaxis = (float(v) for v in values)
        _tecutil.GeomEllipseSetSize(self.uid, haxis, vaxis)


class Rectangle(Geometry2D):
    """A rectangle annotation attached to a `Frame`.

    .. seealso:: `Frame.add_rectangle()`

    .. code-block:: python

        import tecplot as tp
        from tecplot.constant import *

        frame = tp.active_frame()

        rectangle0 = frame.add_rectangle((40, 45), (20, 12), CoordSys.Frame)
        rectangle1 = frame.add_rectangle((50, 50), (20, 16), CoordSys.Frame)
        rectangle2 = frame.add_rectangle((60, 55), (20, 20), CoordSys.Frame)

        rectangle0.fill_color = Color.Magenta
        rectangle1.fill_color = Color.Yellow
        rectangle2.fill_color = Color.Cyan

        tp.export.save_png('rectangle.png', 600)

    .. figure:: /_static/images/rectangle.png
        :width: 300px
        :figwidth: 300px
    """
    @property
    def size(self):
        """`tuple`: Size :math:`(width, height)` of the rectangle.

        This is the width and height of the rectangle and will be in the
        coordinate system specified by `Rectangle.position_coordinate_system`.
        This example creates a rectangle with :math:`(width, height)` of
        :math:`(5, 10)` and changes it to :math:`(10, 20)` later::

            >>> from tecplot.constant import CoordSys
            >>> geom = frame.add_rectangle((50, 50), (5, 10), CoordSys.Frame)
            >>> geom.size = (10, 20)
        """
        with self.frame.activated():
            return _tecutil.GeomRectangleGetSize(self.uid)

    @size.setter
    @tecutil.lock()
    def size(self, values):
        width, height = (float(v) for v in values)
        with self.frame.activated():
            _tecutil.GeomRectangleSetSize(self.uid, width, height)


class Square(Geometry2D):
    """A square annotation attached to a `Frame`.

    .. seealso:: `Frame.add_square()`

    .. code-block:: python

        import tecplot as tp
        from tecplot.constant import *

        frame = tp.active_frame()

        square0 = frame.add_square((40, 40), 15, CoordSys.Frame)
        square1 = frame.add_square((50, 50), 15, CoordSys.Frame)
        square2 = frame.add_square((60, 60), 15, CoordSys.Frame)

        square0.fill_color = Color.Magenta
        square1.fill_color = Color.Yellow
        square2.fill_color = Color.Cyan

        tp.export.save_png('square.png', 600)

    .. figure:: /_static/images/square.png
        :width: 300px
        :figwidth: 300px
    """
    @property
    def size(self):
        """`float`: Length of one side of the square.

        This will be in the coordinate system specified by
        `Square.position_coordinate_system`. This example creates a square of
        side-length 5 and then doubles it to 10 later::

            >>> from tecplot.constant import CoordSys
            >>> geom = frame.add_square((50, 50), 5, CoordSys.Frame)
            >>> geom.radius = 10
        """
        with self.frame.activated():
            return _tecutil.GeomSquareGetSize(self.uid)

    @size.setter
    @tecutil.lock()
    def size(self, value):
        with self.frame.activated():
            _tecutil.GeomSquareSetSize(self.uid, float(value))
