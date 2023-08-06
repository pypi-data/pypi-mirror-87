from ..tecutil import _tecutil
from ..exception import *
from .. import tecutil
from . import annotation


class GeoreferencedImage(annotation.Annotation):
    """A Geographic reference image.

    A georeferenced can be added to a plot with a call to
    `Frame.add_georeferenced_image()`. Placement of the image is controlled by
    the :math:`(x, y)` variables of the `Frame` and the `GeoreferencedImage`
    object's :math:`z` parameter.
    """
    @property
    def z(self):
        """`float`: :math:`z`-position of the georeferenced image.

        This is the :math:`z` position (typically elevation) of the
        georeferenced image with respect to the :math:`(x, y, z)` variables set
        in the `Frame`. Example usage::

            >>> georefimg.z = 100
        """
        with self.frame.activated():
            pos = _tecutil.GeomGetAnchorPos(self.uid)
            return tecutil.XYZ(*pos).z

    @z.setter
    @tecutil.lock()
    def z(self, value):
        with self.frame.activated():
            _tecutil.GeomSetAnchorPos(self.uid, 0, 0, float(value))
