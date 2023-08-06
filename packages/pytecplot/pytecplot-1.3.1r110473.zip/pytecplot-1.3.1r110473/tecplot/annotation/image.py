from ..tecutil import _tecutil
from ..exception import *
from .. import constant, tecutil

from .annotation import MovableAnnotation


class Image(MovableAnnotation):
    """Image annotation.

    This example shows creating an image from a 2D plot and overlaying it on
    the 3D plot of the same data.

    .. code-block:: python
        :emphasize-lines: 22

        import os

        import tecplot as tp
        from tecplot.constant import PlotType

        examples_dir = tp.session.tecplot_examples_directory()
        datafile = os.path.join(examples_dir, 'SimpleData', 'F18.plt')
        dataset = tp.data.load_tecplot(datafile)

        frame = tp.active_frame()

        plot2d = frame.plot(PlotType.Cartesian2D)
        plot2d.activate()
        plot2d.show_contour = True
        plot2d.contour(0).colormap_name = 'Sequential - Blue'
        plot2d.contour(0).variable = dataset.variable('S')
        tp.export.save_png('embedded_image.png')

        plot3d = frame.plot(PlotType.Cartesian3D)
        plot3d.activate()
        plot3d.show_contour = True
        frame.add_image('embedded_image.png', (5, 55), 40)

        tp.export.save_png('image.png')

    .. figure:: /_static/images/image.png
        :width: 300px
        :figwidth: 300px
    """
    @property
    def filename(self):
        """`str`: Source file (read-only).

        Example usage::

            >>> image = frame.add_imge('my_image.png', (20, 20), 40)
            >>> print(image.filename)
            my_image.png
        """
        with self.frame.activated():
            return _tecutil.GeomImageGetFileName(self.uid)

    @property
    def height(self):
        """`float`: Displayed image height in the coordinate system specified.

        The units for height are determined by the `position_coordinate_system`
        of the image. This example sets the height to 40% of the `Frame`::

            >>> from tecplot.constant import CoordSys
            >>> image.position_coordinate_system = CoordSys.Frame
            >>> image.height = 40
        """
        return self.size[1]

    @height.setter
    @tecutil.lock()
    def height(self, value):
        value = float(value)
        if value <= 0.0:
            msg = 'Annotation image height must be greater than 0'
            raise TecplotValueError(msg)
        with self.frame.activated():
            _tecutil.GeomImageSetHeight(self.uid, value)

    @property
    def maintain_aspect_ratio(self):
        """`bool`: Keep aspect ratio on width or height change.

        Example usage::

            >>> image.maintain_aspect_ratio = True
        """
        with self.frame.activated():
            return _tecutil.GeomImageGetUseRatio(self.uid)

    @maintain_aspect_ratio.setter
    @tecutil.lock()
    def maintain_aspect_ratio(self, value):
        with self.frame.activated():
            _tecutil.GeomImageSetUseRatio(self.uid, bool(value))

    @property
    def raw_size(self):
        """:math:`(width, height)`: Original image size in pixels (read-only).

        Example usage::

            >>> print(image.raw_size)
            (600, 400)
        """
        return _tecutil.GeomImageGetRawSize(self.uid)

    @tecutil.lock()
    def reset_aspect_ratio(self):
        """Restore the aspect ratio to that of the original image.

        Example usage::

            >>> image.reset_aspect_ratio()
        """
        _tecutil.GeomImageResetAspectRatio(self.uid)

    @property
    def resize_filter(self):
        """`ImageResizeFilter`: Smoothing filter.

        Possible values are `ImageResizeFilter.Texture`,
        `ImageResizeFilter.Box`, `ImageResizeFilter.Lanczos2`,
        `ImageResizeFilter.Lanczos3`, `ImageResizeFilter.Triangle`,
        `ImageResizeFilter.Bell`, `ImageResizeFilter.BSpline`,
        `ImageResizeFilter.Cubic`, `ImageResizeFilter.Mitchell`,
        `ImageResizeFilter.Gaussian`. Example usage::

            >>> from tecplot.constant import ImageResizeFilter
            >>> image.resize_filter = ImageResizeFilter.BSpline
        """
        imgrf = _tecutil.GeomImageGetResizeFilter(self.uid)
        with self.frame.activated():
            return constant.ImageResizeFilter(imgrf)

    @resize_filter.setter
    @tecutil.lock()
    def resize_filter(self, value):
        imgrf = constant.ImageResizeFilter(value)
        with self.frame.activated():
            _tecutil.GeomImageSetResizeFilter(self.uid, imgrf.value)

    @property
    def size(self):
        """:math:`(width, height)`: Displayed image size.

        This will be in the coordinates specified by
        `Image.position_coordinate_system`. Example usage::

            >>> image.size = (40, 20)
        """
        with self.frame.activated():
            return _tecutil.GeomImageGetSize(self.uid)

    @size.setter
    def size(self, values):
        width, height = (float(v) for v in values)
        _maintain_aspect = self.maintain_aspect_ratio
        if _maintain_aspect:
            self.maintain_aspect_ratio = False
        self.width = width
        self.height = height
        if _maintain_aspect:
            self.maintain_aspect_ratio = _maintain_aspect

    @property
    def width(self):
        """`float`: Displayed image width in the coordinate system specified.

        The units for width are determined by the `position_coordinate_system`
        of the image. This example sets the width to 40% of the `Frame`::

            >>> from tecplot.constant import CoordSys
            >>> image.position_coordinate_system = CoordSys.Frame
            >>> image.width = 0.4
        """
        return self.size[0]

    @width.setter
    @tecutil.lock()
    def width(self, value):
        with self.frame.activated():
            _tecutil.GeomImageSetWidth(self.uid, float(value))
