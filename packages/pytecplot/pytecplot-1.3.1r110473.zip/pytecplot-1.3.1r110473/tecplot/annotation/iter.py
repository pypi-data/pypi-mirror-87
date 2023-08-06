from ..tecutil import _tecutil
from .. import constant
from .annotation import Annotation, MovableAnnotation
from .geometry import Circle, Ellipse, Rectangle, Square
from .georeference import GeoreferencedImage
from .image import Image
from .polyline import MultiPolyline2D, MultiPolyline3D, Polyline2D, Polyline3D
from .text import Text

class GeometryIterator(object):
    """
        type_filter is a function that takes a Geometry object and returns one
        of the concrete geometry objects: Circle, Square, Polyline3D,
        MultiPolyline2D, Image, etc. or None if the object is to be filtered
        out. For convenience, this class provides static methods for geometric
        shape and image filtering.
    """
    def __init__(self, type_filter, frame):
        self.type_filter = type_filter
        self.frame = frame

    def __iter__(self):
        self.current_item = None
        return self

    @staticmethod
    def ShapeFilter(anno):
        geom_type = anno.type
        if geom_type == constant.GeomType.LineSegs:
            anno = MovableAnnotation(anno.uid, anno.frame)
            if anno.position_coordinate_system == constant.CoordSys.Grid3D:
                mpolyline = MultiPolyline3D(anno.uid, anno.frame)
                if len(mpolyline) == 1:
                    return Polyline3D(0, mpolyline)
                else:
                    return mpolyline
            else:
                mpolyline = MultiPolyline2D(anno.uid, anno.frame)
                if len(mpolyline) == 1:
                    return Polyline2D(0, mpolyline)
                else:
                    return mpolyline
        else:
            try:
                ShapeTypes = {
                    constant.GeomType.Circle: Circle,
                    constant.GeomType.Ellipse: Ellipse,
                    constant.GeomType.Rectangle: Rectangle,
                    constant.GeomType.Square: Square,
                }
                return ShapeTypes[geom_type](anno.uid, anno.frame)
            except KeyError:
                return

    @staticmethod
    def ImageFilter(anno):
        if anno.type == constant.GeomType.Image:
            anno = MovableAnnotation(anno.uid, anno.frame)
            if anno.position_coordinate_system == constant.CoordSys.Grid3D:
                return GeoreferencedImage(anno.uid, anno.frame)
            else:
                return Image(anno.uid, anno.frame)

    def __next__(self):
        with self.frame.activated():
            while True:
                if getattr(self, 'current_item', None) is None:
                    uid = _tecutil.GeomGetBase()
                else:
                    uid = _tecutil.GeomGetNext(self.current_item.uid)
                if not uid:
                    break
                self.current_item = Annotation(uid, self.frame)
                obj = self.type_filter(self.current_item)
                if obj is None:
                    continue
                self.current_item = obj
                return self.current_item
        raise StopIteration

    def next(self):
        return self.__next__()


class TextIterator(object):
    def __init__(self, frame):
        self.frame = frame

    def __iter__(self):
        self.current_item = None
        return self

    def __next__(self):
        with self.frame.activated():
            if getattr(self, 'current_item', None) is None:
                uid = _tecutil.TextGetBase()
            else:
                uid = _tecutil.TextGetNext(self.current_item.uid)
        if not uid:
            raise StopIteration
        self.current_item = Text(uid, self.frame)
        return self.current_item

    def next(self):
        return self.__next__()
