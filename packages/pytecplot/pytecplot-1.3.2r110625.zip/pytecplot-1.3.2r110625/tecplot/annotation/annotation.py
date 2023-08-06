from builtins import super

import collections
import ctypes

from ..tecutil import _tecutil
from .. import constant, tecutil
from ..exception import *


@tecutil.lock_attributes
class Annotation(object):
    """Base-class for all geometry and image annotations."""
    def __init__(self, uid, frame):
        self.uid = uid
        self.frame = frame

    def __eq__(self, other):
        return self.uid == other.uid

    def __ne__(self, other):
        return self.uid != other.uid

    @property
    def scope(self):
        """`Scope`: Display annotation in all frames with the same data.

        Annotations with local scope are displayed only in the `Frame` in which
        they are created. If it is defined as having `global <Scope.Global>`
        scope, it will appear in all "like" `frames <Frame>`. That is, those
        frames using the same data set as the one in which the annotation was
        created. (default: `Scope.Local`)

        Example usage assuming an annotation variable ``anno``::

            >>> from tecplot.constant import Scope
            >>> anno.scope = Scope.Global
        """
        with self.frame.activated():
            return constant.Scope(_tecutil.GeomGetScope(self.uid))

    @scope.setter
    @tecutil.lock()
    def scope(self, scope):
        with self.frame.activated():
            _tecutil.GeomSetScope(self.uid, constant.Scope(scope).value)

    @property
    def type(self):
        """`GeomType`: The type of this annotation (read-only).

        This is the generic type information for geometry and image
        annotations. This is a read-only parameter and is used, in combination
        with *position_coordinate_system* to determine the actual return types
        of the iterators `Frame.geometries()` and `Frame.images()`::

            >>> frame.add_image('image.png', (1, 1), 5)
            >>> frame.add_circle((0,0), 1, CoordSys.Grid)
            >>> frame.add_square((0,0), 1, CoordSys.Grid)
            >>> for anno in frame.images():
            ...     print(anno.type)
            ...
            GeomType.Image
            >>> for anno in frame.geometries():
            ...     print(anno.type)
            ...
            GeomType.Circle
            GeomType.Square
        """
        with self.frame.activated():
            return constant.GeomType(_tecutil.GeomGetType(self.uid).value)

    @property
    def macro_function(self):
        """`str`: An associated macro function.

        All geometry or image annotations may be linked to a macro function.
        This macro function is called when you hold down the Control key
        (Command key on Mac OS X) and click the right mouse button on the text,
        geometry or image in the frame.

        In order to be attached to a text or geometry object, the macro
        function must be a "retained" macro function. A macro function is
        "retained" via either of the following scenarios:

        * running a macro file that contains the required macro functions
        * including it in your tecplot.mcr file (which is run at start up,
          making it a special case of the preceding scenario)

        In both cases, the macro function is defined using the $!MACROFUNCTION
        macro command. Refer to "$!MACROFUNCTION...$!ENDMACROFUNCTION" on page
        157 in the |Tecplot Macro Scripting Guide| for additional information.

        Example usage assuming an annotation variable ``anno``::

            >>> anno.macro_function = 'MYMACROFUNCTION'

        To run this function from PyTecplot it is neccessary to pass the
        function to a call to `macro.execute_function()`::

            >>> tecplot.macro.execute_function(anno.macro_function)
        """
        with self.frame.activated():
            success, cmd = _tecutil.GeomGetMacroFunctionCmd(self.uid)
            if not success:
                raise TecplotSystemError()
            return cmd

    @macro_function.setter
    @tecutil.lock()
    def macro_function(self, value):
        with self.frame.activated():
            success = _tecutil.GeomSetMacroFunctionCmd(self.uid, str(value))
            if not success:
                raise TecplotSystemError()

    @property
    def attached_map_index(self):
        """`Index` or `None`: Index to the associated fieldmap or linemap.

        This property allows an annotation to follow the same active/inactive
        state as another plot object so their visibility can be changed
        together. Attach this annotation to a fieldmap or linemap using the
        object's index property. Geometries and images that are attached to an
        inactive or non-existent zone are not displayed. Example usage assuming
        an annotation variable ``anno``::

            >>> anno.attached_map_index = plot.fieldmap(2).index
        """
        with self.frame.activated():
            if _tecutil.GeomIsAttached(self.uid):
                return tecutil.Index(_tecutil.GeomGetZoneOrMap(self.uid) - 1)

    @attached_map_index.setter
    @tecutil.lock()
    def attached_map_index(self, value):
        with self.frame.activated():
            if value is None:
                _tecutil.GeomSetAttached(self.uid, False)
            else:
                _tecutil.GeomSetAttached(self.uid, True)
                _tecutil.GeomSetZoneOrMap(self.uid, tecutil.Index(value) + 1)


class MovableAnnotation(Annotation):
    @property
    def draw_order(self):
        """`constant.DrawOrder`: Draw before or after the data.

        Annotations can be drawn either before or after the data. If a geometry
        or image is drawn before the data, the plot layers, such as mesh,
        contour lines, etc. will be drawn on top of the geometry. Otherwise,
        the annotation will be drawn last, potentially obscuring the data.

        .. note::
            Tecplot 360 draws all geometries and images first, in the order
            they were added, then all text.

        Example usage assuming an annotation variable ``anno``::

            >>> from tecplot.constant import DrawOrder
            >>> anno.draw_order = DrawOrder.BeforeData
        """
        with self.frame.activated():
            return constant.DrawOrder(_tecutil.GeomGetDrawOrder(self.uid))

    @draw_order.setter
    @tecutil.lock()
    def draw_order(self, value):
        with self.frame.activated():
            _tecutil.GeomSetDrawOrder(self.uid, constant.DrawOrder(value).value)

    @property
    def position(self):
        r"""`tuple`: Location on the `Frame`.

        This is the origin of the annotation and will be :math:`(x,y)` or
        :math:`(\theta,r)` depending on the plot type. Example usage assuming
        an annotation variable ``anno``::

            >>> anno.position = (3, 4)
        """
        with self.frame.activated():
            pos = _tecutil.GeomGetAnchorPos(self.uid)
            return tecutil.XY(*pos[:2])

    @position.setter
    @tecutil.lock()
    def position(self, values):
        pos = tecutil.XY(*[float(x) for x in values])
        with self.frame.activated():
            _tecutil.GeomSetAnchorPos(self.uid, pos.x, pos.y, 0)

    @property
    def position_coordinate_system(self):
        """`CoordSys`: Position coordinate system.

        The object may be positioned using either the grid coordinate system or
        the frame coordinate system and must be one of `CoordSys.Frame` or
        `CoordSys.Grid`:

            * `CoordSys.Frame`: The geometry is always displayed at constant
              size and position when you zoom in or out of the plot.
            * `CoordSys.Grid`: The geometry resizes and moves with the data
              grid. However, the geometry remains fixed when you rotate the
              plot. Changing the center of rotation may cause the geometry to
              move.

        Example usage assuming an annotation variable ``anno``::

            >>> from tecplot.constant import CoordSys
            >>> anno.position_coordinate_system = CoordSys.Frame
        """
        with self.frame.activated():
            result = _tecutil.GeomGetPositionCoordSys(self.uid)
            return constant.CoordSys(result)

    @position_coordinate_system.setter
    @tecutil.lock()
    def position_coordinate_system(self, value):
        with self.frame.activated():
            coord_sys = constant.CoordSys(value)
            _tecutil.GeomSetPositionCoordSys(self.uid, coord_sys.value)
