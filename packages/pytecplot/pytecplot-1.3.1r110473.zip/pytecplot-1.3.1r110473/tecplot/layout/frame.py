from builtins import str

import contextlib, ctypes, logging, numbers, six

from ..tecutil import _tecutil, sv
from ..constant import *
from ..exception import *
from .. import annotation, constant, plot, session, tecutil


log = logging.getLogger(__name__)


class Frame(session.Style):
    """`Frame` object within a `Page`, holding onto a `Dataset` and a `Plot`.

    Parameters:
        uid (`int`, optional): This must be a *valid* unique ID
            number pointing internally to a Frame object or `None`. A new
            `Frame` is created if set to `None`. (default: `None`)
        page (`Page`, optional): The destination `Page` of this newly
            created `Frame`. If `None`, the currently active `Page` is used.
            (default: `None`)

    Warning:
        Though it is possible to create a `Frame` object using the
        constructor, it is usually sufficient to obtain a frame through
        `tecplot.active_frame()` or `Page.frame()`. One can also create a
        `Frame` using a `Page` handle with `Page.add_frame()`.

    The concept of the `Frame` is central to understanding the
    |Tecplot Engine|. The `Frame` is what connects a `Dataset` to a `Plot`
    handle from which one manipulates the desired image as well as accessing
    the attached data:

    .. code-block:: python

        import tecplot

        frame = tecplot.active_frame()

        # will print: 'Frame "Frame 001"'
        print(frame)
    """

    page = None
    """The `Page` containing this Frame.

    This provides access to the parent `Page`:

    .. code-block:: python

        import tecplot

        frame = tecplot.active_frame()
        page = frame.page

        # Will print: "Page 001"
        print(page.name)
    """

    def __init__(self, uid, page):
        self.page = page
        self.uid = uid
        """The internal unique ID number of this Frame."""
        super().__init__(sv.FRAMELAYOUT, uniqueid=self.uid)

    def __str__(self):
        """Brief string representation.

        Returns:
            `str`: Brief representation of this `Frame`.

        Example:

        .. code-block:: python

            import tecplot
            frame = tecplot.active_frame()

            # will print: 'Frame: "Frame 001"'
            print(frame)
        """
        return 'Frame: "{name}"'.format(name=self.name)

    def __repr__(self):
        """Executable string representation.

        Returns:
            `str`: Internal representation of this `Frame`.

        The string returned can be executed to generate an identical
        copy of this `Frame` object:

        .. code-block:: python

            import tecplot
            from tecplot.layout import Frame, Page

            frame = tecplot.active_frame()

            '''
            The "repr" string of the Frame is executable code.
            The following will print: "Frame(uid=11, page=Page(uid=1))"
            '''
            print(repr(frame))

            frame2 = None
            exec('frame2 = '+repr(frame))

            '''
            At this point, frame2 is just another handle to
            the exact same frame object in the Tecplot Engine
            '''
            assert frame2 == frame
        """
        return 'Frame(uid={uid}, page={page})'.format(uid=self.uid,
                                                      page=repr(self.page))

    def __eq__(self, other):
        """Checks for `Frame` equality in the |Tecplot Engine|.

        Returns:
            `bool`: `True` if the unique ID numbers are the same for both
            `Frames <Frame>`.

        Example:

        .. code-block:: python

            import tecplot

            page = tecplot.active_page()
            frame1 = page.active_frame()
            frame2 = page.add_frame()

            assert not (frame1 == frame2)
            assert page.active_frame() == frame2
        """
        return self.uid == other.uid

    @property
    def position(self):
        """`tuple`: ``(x,y)`` position of the `Frame` in inches.

        The `Frame` x position is relative to the left side of the paper.
        The `Frame` y position is relative to the top of the paper.

        If x is `None`, the `Frame` x position is not changed.
        If y is `None`, the `Frame` y position is not changed.

        Set `Frame` position 1 inch from the left side of the paper
        and two inches from the top of the paper::

            >>> tp.active_frame().position=(1.0, 2.0)

        Move the active `Frame` one inch to the right::

            >>> tp.active_frame().position=(tp.active_frame().position.x+1, None)
        """
        return session.XY(self, sv.XYPOS)

    @position.setter
    def position(self, pos):
        session.XY(self, sv.XYPOS)[:] = pos

    @property
    def aux_data(self):
        """Auxiliary data for this frame.

        Returns:
            `AuxData`

        This is the auxiliary data attached to the frame. Such data is written
        to the layout file by default and can be retrieved later. Example
        usage::

            >>> aux = tp.active_frame().aux_data
            >>> aux['Result'] = '3.14159'
            >>> print(aux['Result'])
            3.14159
        """
        return session.AuxData(self, AuxDataObjectType.Frame)

    def texts(self):
        """Get an iterator for all `Text` objects in the frame.

        This example shows how to obtain a list of all red `Text` objects::

            >>> from tecplot.constant import Color
            >>> all_red_text_objects = [T for T in tp.active_frame().texts()
            ...                         if T.color == Color.Red]
        """
        return annotation.TextIterator(self)

    def geometries(self):
        """Get an iterator for all geometry objects in the frame.

        This method provides access to all geometric shape instances attached
        to this `Frame`. This includes `Circle`, `Polyline2D`, `Polyline3D` and
        all similar objects::

            >>> for geom in frame.geometries():
            ...     print(type(geom))
            <class 'tecplot.annotation.geometry.Circle'>
            <class 'tecplot.annotation.polyline.Polyline2D'>
        """
        shapefilter = annotation.GeometryIterator.ShapeFilter
        return annotation.GeometryIterator(shapefilter, self)

    def images(self):
        """Get an iterator for all image objects in the frame.

        This method provides access to all `Image` and `GeoreferencedImage`
        instances attached to this `Frame`::

            >>> for image in frame.images():
            ...     print(image.filename)
            image1.png
            image2.png
        """
        imagefilter = annotation.GeometryIterator.ImageFilter
        return annotation.GeometryIterator(imagefilter, self)

    @contextlib.contextmanager
    def activated(self):
        """Context for temporarily activating this `Frame`.

        Example:

        .. code-block:: python

            import tecplot

            page = tecplot.active_page()
            frame1 = page.active_frame()
            frame2 = page.add_frame()

            assert frame2.active

            with frame1.activated():
                # frame1 is active only during this context
                assert frame1.active
                # there is only one frame active at a time
                assert not frame2.active

            assert frame2.active
        """
        frame_uid = _tecutil.FrameGetActiveID()
        if self.uid == frame_uid:
            yield
        else:
            page_uid = _tecutil.PageGetUniqueID()
            self.activate()
            try:
                yield
            finally:
                with tecutil.lock():
                    if _tecutil.PageGetUniqueID() != page_uid:
                        _tecutil.PageSetCurrentByUniqueID(page_uid)
                    _tecutil.FrameActivateByUniqueID(frame_uid)

    @tecutil.lock()
    def load_stylesheet(self, filename, plot_style=True, text=True, geom=True,
                        streams=True, contours=True, frame_geom=False,
                        merge=False):
        """Apply a stylesheet settings file to this frame.

        Parameters:
            filename (`str`): The path to a stylesheet file. (See note
                below conerning absolute and relative paths.)
            plot_style (`bool`, optional): Apply the stylesheet's
                plot style. (default: `True`)
            text (`bool`, optional): Include the stylesheet's text
                objects. (default: `True`)
            geom (`bool`, optional): Include the stylesheet's
                geometry objects. (default: `True`)
            streams (`bool`, optional): Include the stylesheet's
                stream traces. (default: `True`)
            contours (`bool`, optional): Include the stylesheet's
                contour levels. (default: `True`)
            frame_geom (`bool`, optional): Apply the stylesheet's
                frame position and size. (default: `False`)
            merge (`bool`, optional): Merge with the frame's current
                style. (default: `False`)

        .. note:: **Absolute and relative paths with PyTecplot**

            Relative paths, when used within the PyTecplot API are always from
            Python's current working directory which can be obtained by calling
            :func:`os.getcwd()`. This is true for batch and `connected
            <tecplot.session.connect()>` modes. One exception to this is paths
            within a macro command or file which will be relative to the
            |Tecplot Engine|'s home directory, which is typically the |Tecplot
            360| installation directory. Finally, when connected to a remote
            (non-local) instance of Tecplot 360, only absolute paths are
            allowed.

            Note that backslashes must be escaped which is especially important
            for windows paths such as ``"C:\\\\Users"`` or
            ``"\\\\\\\\server\\\\path"`` which will resolve to ``"C:\\Users"``
            and ``"\\\\server\\path"`` respectively. Alternatively, one may use
            Python's raw strings: ``r"C:\\Users"`` and ``r"\\\\server\\path"``

        Example usage::

            >>> frame = tecplot.active_frame()
            >>> frame.load_stylesheet('my_style.sty')
        """
        filepath = tecutil.normalize_path(filename)
        with self.activated():
            log.debug('Applying style from {} to frame'.format(filepath))
            if not _tecutil.ReadStylesheet(filepath, plot_style, text, geom,
                                           streams, contours, merge,
                                           frame_geom):
                raise TecplotSystemError()

    @tecutil.lock()
    def save_stylesheet(self, filename, plot_style=True, aux_data=True,
                        text=True, geom=True, streams=True, contours=True,
                        defaults=False, relative_paths=True, compress=False):
        """Save the frame's current style to a file.

        Parameters:
            filename (`str`): The path to a stylesheet file. (See note
                below conerning absolute and relative paths.)
            plot_style (`bool`, optional): Include the frame's plot
                style. (default: `True`)
            aux_data (`bool`, optional): Include auxiliary data.
                (default: `True`)
            text (`bool`, optional): Include text objects. (default:
                `True`)
            geom (`bool`, optional): Include geometry objects.
                (default: `True`)
            streams (`bool`, optional): Include  stream traces.
                (default: `True`)
            contours (`bool`, optional): Include contour levels.
                (default: `True`)
            defaults (`bool`, optional): Include all factory defaults
                used by the current style. (default: `False`)
            relative_paths (`bool`, optional): Use relative paths.
                (default: `True`)
            compress (`bool`, optional): Compress the output of the
                style. (default: `False`)

        .. note:: **Absolute and relative paths with PyTecplot**

            Relative paths, when used within the PyTecplot API are always from
            Python's current working directory which can be obtained by calling
            :func:`os.getcwd()`. This is true for batch and `connected
            <tecplot.session.connect()>` modes. One exception to this is paths
            within a macro command or file which will be relative to the
            |Tecplot Engine|'s home directory, which is typically the |Tecplot
            360| installation directory. Finally, when connected to a remote
            (non-local) instance of Tecplot 360, only absolute paths are
            allowed.

            Note that backslashes must be escaped which is especially important
            for windows paths such as ``"C:\\\\Users"`` or
            ``"\\\\\\\\server\\\\path"`` which will resolve to ``"C:\\Users"``
            and ``"\\\\server\\path"`` respectively. Alternatively, one may use
            Python's raw strings: ``r"C:\\Users"`` and ``r"\\\\server\\path"``

        Example usage::

            >>> frame = tecplot.active_frame()
            >>> frame.save_stylesheet('my_style.sty')
        """
        filepath = tecutil.normalize_path(filename)
        with self.activated():
            with tecutil.ArgList() as arglist:
                arglist.update((
                    (sv.FNAME, str(filepath)),
                    (sv.INCLUDEPLOTSTYLE, bool(plot_style)),
                    (sv.INCLUDEAUXDATA, bool(aux_data)),
                    (sv.INCLUDETEXT, bool(text)),
                    (sv.INCLUDEGEOM, bool(geom)),
                    (sv.INCLUDESTREAMPOSITIONS, bool(streams)),
                    (sv.INCLUDECONTOURLEVELS, bool(contours)),
                    (sv.INCLUDEFACTORYDEFAULTS, bool(defaults)),
                    (sv.USERELATIVEPATHS, bool(relative_paths)),
                    (sv.COMPRESS, bool(compress))))
                if not _tecutil.WriteStylesheetX(arglist):
                    raise TecplotSystemError()

    @property
    def name(self):
        """`str`: Returns or sets the name.

        This is the name used when searching for `Frame` objects in
        `Page.frames` and `Page.frame`. It does not have to be unique,
        even for multiple frames in a single `Page`:

        .. code-block:: python

            import tecplot

            frame = tecplot.active_frame()
            frame.name = '3D Data View'

            # will print: "this frame: 3D Data View"
            print('this frame:', frame.name)
        """
        with self.activated():
            return _tecutil.FrameGetName()[1]

    @name.setter
    @tecutil.lock()
    def name(self, name):
        with self.activated():
            _tecutil.FrameSetName(name)

    @property
    def active(self):
        """Checks if this `Frame` is active.

        Returns:
            `bool`: `True` if this `Frame` is the active `Frame`.
        """
        return self.uid == _tecutil.FrameGetActiveID()

    @property
    def current(self):
        return self.uid == _tecutil.FrameGetUniqueID()

    @tecutil.lock()
    def activate(self):
        """Causes this `Frame` to become active.

        The parent `Page` is implicitly "activated" as a side-effect of this
        operation:

        .. code-block:: python

            import tecplot

            page1 = tecplot.active_page()
            frame1 = page1.active_frame()
            page2 = tecplot.add_page()
            frame2 = page2.active_frame()
            assert not (frame1.active and page1.active)
            assert frame2.active and page2.active

            frame1.activate()
            assert not (frame2.active or page2.active)
            assert frame1.active and page1.active
        """
        if not self.active:
            if self.page is not None:
                self.page.activate()
            if not _tecutil.FrameActivateByUniqueID(self.uid):
                err = 'could not activate frame with uid {0}'.format(self.uid)
                raise TecplotSystemError(err)

    @property
    def plot_type(self):
        """`constant.PlotType`: Returns or sets the current plot type.

        A `Frame` can have only one active plot type at any given time. The
        types are enumerated by `constant.PlotType`:

        .. code-block:: python

            import os
            import tecplot
            from tecplot.constant import PlotType

            frame = tecplot.active_frame()
            assert frame.plot_type is PlotType.Sketch

            install_dir = tecplot.session.tecplot_install_directory()
            infile = os.path.join(install_dir, 'examples', 'SimpleData', 'SpaceShip.lpk')
            tecplot.load_layout(infile)

            frame = tecplot.active_frame()
            assert frame.plot_type is PlotType.Cartesian3D

            frame.plot_type = PlotType.Cartesian2D
            assert frame.plot_type is PlotType.Cartesian2D

        .. note:: Plot type cannot be set to `constant.PlotType.Automatic`.
        """
        return _tecutil.FrameGetPlotTypeForFrame(self.uid)

    @plot_type.setter
    @tecutil.lock()
    def plot_type(self, plot_type):
        with self.activated():
            try:
                res = _tecutil.FrameSetPlotType(plot_type.value)
            except TecplotSystemError as err:
                if not self.has_dataset:
                    res = SetValueReturnCode.ContextError1
                else:
                    raise err
            if res not in [SetValueReturnCode.Ok,
                           SetValueReturnCode.DuplicateValue]:
                if res is SetValueReturnCode.ContextError1:
                    raise TecplotSystemError('no dataset attached to frame')
                raise TecplotSystemError(res)

    def plot(self, plot_type=PlotType.Active):
        """The primary `Plot` style-control object.

        Returns:
            `Plot`:
                One of the possible `Plot` subclasses, depending on the
                ``plot_type`` specified. By default, the active plot
                type, obtained from `Frame.plot_type`, is used.

        The `Plot` object is the handle through which one can manipulate the
        style and visual representation of the `Dataset`. Possible return types
        are: `SketchPlot`, `Cartesian2DFieldPlot`, `Cartesian3DFieldPlot`,
        `PolarLinePlot` and `XYLinePlot`. Each of these have their own specific
        set of attributes and methods:

        .. code-block:: python

            import os
            import tecplot
            from tecplot.constant import PlotType

            install_dir = tecplot.session.tecplot_install_directory()
            infile = os.path.join(install_dir, 'examples', 'SimpleData', 'SpaceShip.lpk')
            tecplot.load_layout(infile)

            frame = tecplot.active_frame()
            assert frame.plot_type is PlotType.Cartesian3D

            plot3d = frame.plot()
            plot3d.show_contour = True
        """
        if plot_type is PlotType.Active:
            plot_type = None
        _dispatch = {
            PlotType.Cartesian2D: plot.Cartesian2DFieldPlot,
            PlotType.Cartesian3D: plot.Cartesian3DFieldPlot,
            PlotType.XYLine: plot.XYLinePlot,
            PlotType.PolarLine: plot.PolarLinePlot,
            PlotType.Sketch: plot.SketchPlot}
        return _dispatch[plot_type or self.plot_type](self)

    @tecutil.lock()
    def move_to_bottom(self):
        """Moves `Frame` behind all others in `Page`.
        """
        _tecutil.FrameMoveToBottomByUniqueID(self.uid)

    @tecutil.lock()
    def move_to_top(self):
        """Moves `Frame` in front of all others in `Page`.
        """
        _tecutil.FrameMoveToTopByUniqueID(self.uid)

    @tecutil.lock()
    def active_zones(self, *zones):
        """Returns or sets the active `Zones <data_access>`.

        Parameters:
            zones (`Zones <data_access>`, optional): The `Zone <data_access>`
                objects, which must be in the `Dataset` attached to this
                `Frame`, that will be activated. All other `Zones
                <data_access>` will be deactivated.

        Returns:
            `Zones <data_access>`:
                This will return a generator of active `Zones <data_access>` in
                this `Frame`.

        This should only be used on frames with an active plot type that
        contains a dataset with at least one zone.
        """
        if __debug__:
            if self.plot_type is PlotType.Sketch:
                err = 'Active plot type is Sketch which has no active zones.'
                raise TecplotLogicError(err)
            if not self.has_dataset:
                raise TecplotLogicError('Frame has no dataset.')
            if self.dataset.num_zones == 0:
                raise TecplotLogicError('Dataset has no zones.')

        with self.activated():
            if zones:
                with tecutil.IndexSet(*zones) as zoneset:
                    _tecutil.ZoneSetActive(zoneset, AssignOp.Equals.value)
            else:
                zoneset = _tecutil.ZoneGetActiveForFrame(self.uid)
                zones = [self.dataset.zone(i) for i in zoneset]
                zoneset.dealloc()
            return zones

    @tecutil.lock()
    def delete_geometry(self, geom):
        """Delete a geometry or image annotation object from the `Frame`.

        Parameters:
            geom (`Circle`, `Image` or similar instance): The annotation
                instance to be removed from the `Frame`.

        .. warning::
            After the annotation is deleted, all handles to it will no longer
            be valid and all accessing any properties of the object will result
            in a `TecplotLogicError` being raised.

        Example usage:

        .. code-block:: python
            :emphasize-lines: 6

            import tecplot
            from tecplot.constant import CoordSys

            frame = tecplot.active_frame()
            rectangle = frame.add_rectangle((0.5, 0.5), (0.1, 0.2), CoordSys.Frame)
            frame.delete_geometry(rectangle)
        """
        with self.activated():
            _tecutil.GeomDelete(geom.uid)

    @tecutil.lock()
    def delete_image(self, img):
        """Delete an image annotation object from the `Frame`.

        Parameters:
            img (`Image` or `GeoreferencedImage`): The annotation instance to
                be removed from the `Frame`.

        .. warning::
            After the annotation is deleted, all handles to it will no longer
            be valid and all accessing any properties of the object will result
            in a `TecplotLogicError` being raised.

        .. seealso:: `delete_geometry()`
        """
        return self.delete_geometry(img)

    @tecutil.lock()
    def delete_text(self, text):
        """Delete a `text <annotation.Text>` object from a frame.

        When deleted, the text object is no longer displayed in the frame and is
        permanently invalid. To display the text in the frame again,
        a new text object must be created by calling `add_text`.

        .. warning::
            Use this method with care.
            After a text object has been deleted by calling this method,
            it is no longer valid, and all properties of the deleted text
            object will throw `TecplotLogicError` when accessed.

        Example usage:

        .. code-block:: python

            import tecplot as tp

            text = tp.active_frame().add_text("abc")
            tp.active_frame().delete_text(text)

            # The text object is no longer valid.
            # Any property access will throw TecplotLogicError
            try:
                print(text.text_string)
            except tp.exception.TecplotLogicError as e:
                print(e)

        .. seealso:: `add_text`
        """
        with self.activated():
            _tecutil.TextDelete(text.uid)

    @tecutil.lock()
    def add_image(self, filename, position, height):
        """Add an image to the `Frame`.

        Parameters:
            filename (`str`): The image source file. The format of this file
                must be Microsoft Windows Bitmap (*.bmp), JPEG (*.jpg or
                *.jpeg) or Portable Network Graphics (*.png).
            position (`tuple` of `floats <float>`): Position :math:`(x, y)` of
                the image in percentage frame coordinates.
            height (`float`): The initial size, or height, of the image in
                percentage frame units. The initial width in frame units is set
                automatically based on the width to height aspect ratio of the
                image.

        Returns:
            `annotation.Image`

        This example adds an image to the upper left quadrant of the frame::

            >>> frame = tp.active_frame()
            >>> img = frame.add_image('myimage.png', (0, 50), 50)
        """
        x, y = (float(p) for p in position)
        gid = _tecutil.GeomImageCreate(filename, x, y, height)
        if not gid:
            raise TecplotSystemError()
        return annotation.Image(gid, self)

    @tecutil.lock()
    def add_georeferenced_image(self, image_filename, world_filename):
        """Add a geographic reference image and world file to the `Frame`.

        Parameters:
            image_filename (`str`): The image source file.
            world_filename (`str`): The world file associated with the image.

        Returns:
            `annotation.GeoreferencedImage`

        Example usage::

            >>> frame = tp.active_frame()
            >>> imgfile = 'region.png'
            >>> worldfile = 'region.pgw'
            >>> geoimg = frame.add_georeferenced_image(imgfile, worldfile)
        """
        gid = _tecutil.GeoRefImageCreate(image_filename, world_filename)
        if not gid:
            raise TecplotSystemError()
        return annotation.GeoreferencedImage(gid, self)

    @tecutil.lock()
    def add_circle(self, center, radius, coord_sys):
        """Place a circle annotation on the `Frame`.

        Parameters:
            center (`tuple` of `floats <float>`): Position :math:`(x, y)` of
                the center of the circle in the coordinates specified by
                **coord_sys**.
            radius (`float`): The size of the radius in the coordinates
                specified by **coord_sys**.
            coord_sys (`CoordSys`): The coordinate system to use for position
                and size of this annotation.

        Returns:
            `annotation.Circle`

        Example usage:

        .. code-block:: python

            import tecplot
            from tecplot.constant import CoordSys

            frame = tecplot.active_frame()
            circle = frame.add_circle((0.2, 0.2), 0.1, CoordSys.Frame)

        .. seealso:: `add_ellipse`, `add_rectangle`, `add_square`,
            `add_polyline`
        """
        x, y = (float(i) for i in center)
        coord_sys = constant.CoordSys(coord_sys)
        gid = _tecutil.GeomCircleCreate(coord_sys.value, x, y, float(radius))
        if not gid:
            raise TecplotSystemError()
        return annotation.Circle(gid, self)

    @tecutil.lock()
    def add_ellipse(self, center, size, coord_sys):
        """Place an ellipse annotation on the `Frame`.

        Parameters:
            center (`tuple` of `floats <float>`): Position :math:`(x, y)` of
                the ellipse in the coordinates specified by **coord_sys**.
            size (`tuple` of `floats <float>`): Lengths :math:`(h_{axis},
                v_{axis})` of the horizontal and vertical axes in the
                coordinates specified by **coord_sys**. Both lengths must be
                non-zero.
            coord_sys (`CoordSys`): The coordinate system to use for position
                and size of this annotation.

        Returns:
            `annotation.Ellipse`

        Example usage:

        .. code-block:: python

            import tecplot
            from tecplot.constant import CoordSys

            frame = tecplot.active_frame()
            ellipse = frame.add_ellipse((0.5, 0.5), (0.1, 0.2), CoordSys.Frame)

        .. seealso:: `add_circle`, `add_rectangle`, `add_square`,
            `add_polyline`
        """
        x, y = (float(i) for i in center)
        haxis, vaxis = (float(i) for i in size)
        coord_sys = constant.CoordSys(coord_sys)
        gid = _tecutil.GeomEllipseCreate(coord_sys.value, x, y, haxis, vaxis)
        if not gid:
            raise TecplotSystemError()
        return annotation.Ellipse(gid, self)

    @tecutil.lock()
    def add_rectangle(self, corner, size, coord_sys):
        """Place a rectangle annotation on the `Frame`.

        Parameters:
            center (`tuple` of `floats <float>`): Position :math:`(x, y)` of
                the rectangle in the coordinates specified by **coord_sys**.
            size (`tuple` of `floats <float>`): Size :math:`(width, height)` of
                the rectangle in the coordinates specified by **coord_sys**.
            coord_sys (`CoordSys`): The coordinate system to use for position
                and size of this annotation.

        Returns:
            `annotation.Rectangle`

        Example usage:

        .. code-block:: python

            import tecplot
            from tecplot.constant import CoordSys

            frame = tecplot.active_frame()
            rectangle = frame.add_rectangle((0.5, 0.5), (0.1, 0.2), CoordSys.Frame)

        .. seealso:: `add_circle`, `add_ellipse`, `add_square`,
            `add_polyline`
        """
        x, y = (float(i) for i in corner)
        w, h = (float(i) for i in size)
        coord_sys = constant.CoordSys(coord_sys)
        gid = _tecutil.GeomRectangleCreate(coord_sys.value, x, y, w, h)
        if not gid:
            raise TecplotSystemError()
        return annotation.Rectangle(gid, self)

    @tecutil.lock()
    def add_square(self, corner, size, coord_sys):
        """Place a square annotation on the `Frame`.

        Parameters:
            corner (`tuple` of `floats <float>`): Position :math:`(x, y)` of
                the lower-left corner of the square in the coordinates
                specified by **coord_sys**.
            size (`float`): Side-length of the square in the coordinates
                specified by **coord_sys**.
            coord_sys (`CoordSys`): The coordinate system to use for position
                and size of this annotation.

        Returns:
            `annotation.Square`

        Example usage:

        .. code-block:: python

            import tecplot
            from tecplot.constant import CoordSys

            frame = tecplot.active_frame()
            square = frame.add_square((0.2, 0.2), 0.1, CoordSys.Frame)

        .. seealso:: `add_circle`, `add_ellipse`, `add_rectangle`,
            `add_polyline`
        """
        x, y = (float(i) for i in corner)
        coord_sys = constant.CoordSys(coord_sys)
        gid = _tecutil.GeomSquareCreate(coord_sys.value, x, y, float(size))
        if not gid:
            raise TecplotSystemError()
        return annotation.Square(gid, self)

    @tecutil.lock()
    def add_polyline(self, *points, **kwargs):
        """Create a polyline annotation on this `Frame`.

        Parameters:
            *points (`lists <list>` of points): Arrays of :math:`(x, y)` or
                :math:`(x, y, z)` positions of the points along this polyline
                in the coordinate system specified by **coord_sys**. If
                multiple lists are provided, they must be of the same dimension
                (2D or 3D), though they may be of different lengths.

        Keyword Parameters:
            coord_sys (`CoordSys`, optional): The coordinate system to use for
                the positions of this annotation. Only 2D polylines may use a
                coordinate system other than the data-coordinates ("grid").
                (default: `CoordSys.Grid`)

        Returns:
            One of `annotation.Polyline2D`, `annotation.Polyline3D`,
            `annotation.MultiPolyline2D` or `annotation.MultiPolyline3D`.

        Example usage:

        .. code-block:: python

            import tecplot

            points = [ [1, 2,  3],
                       [2, 4,  9],
                       [3, 8, 27], ]

            frame = tecplot.active_frame()
            polyline = frame.add_polyline(points)

        .. seealso:: `add_circle`, `add_ellipse`, `add_rectangle`, `add_square`
        """
        coord_sys = kwargs.get('coord_sys', constant.CoordSys.Grid)
        coord_sys = constant.CoordSys(coord_sys)
        num_lines = len(points)
        dims = [len(l[0]) for l in points]
        if any(d != dims[0] for d in dims):
            msg = 'dimensions of all polylines must be the same'
            raise TecplotLogicError(msg)
        lengths = (ctypes.c_int64 * num_lines)(*[len(l) for l in points])

        if dims[0] == 3:
            if __debug__:
                if coord_sys not in [constant.CoordSys.Grid,
                                     constant.CoordSys.Grid3D]:
                    msg = '3D polylines must be in "Grid" coordinates'
                    raise TecplotLogicError(msg)
            gid = _tecutil.Geom3DMPolyCreate(num_lines, lengths)
            if not gid:
                raise TecplotSystemError()
            polyline = annotation.MultiPolyline3D(gid, self)
        else:
            gid = _tecutil.Geom2DMPolyCreate(coord_sys.value, num_lines, lengths)
            if not gid:
                raise TecplotSystemError()
            polyline = annotation.MultiPolyline2D(gid, self)

        for l, p in zip(polyline, points):
            l[:] = p

        if num_lines == 1:
            if dims[0] == 3:
                polyline = annotation.Polyline3D(0, polyline)
            else:
                polyline = annotation.Polyline2D(0, polyline)

        return polyline

    @tecutil.lock()
    def add_text(self, text, position=None, coord_sys=None, text_type=None,
                 typeface=None, bold=None, italic=None, size_units=None,
                 size=None, color=None, angle=None, line_spacing=None,
                 anchor=None, box_type=None, line_thickness=None,
                 box_color=None, fill_color=None, margin=None, zone=None):
        """Adds a `text <annotation.Text>` to a `Frame`.

        Parameters:
            text (`str`): The text to add to the `Frame`.
                The text string must have a non-zero length.
            position (`tuple` of `floats <float>` (x,y), optional): The
                position of the anchor as a percentage of the
                specified coordinates. (default: (0,0))
            coord_sys (`CoordSys`, optional): Coordinate system used to
                position the anchor of the text object. The possible values
                are: `CoordSys.Grid` or `CoordSys.Frame`. (default:
                `CoordSys.Frame`)
            text_type (`TextType`, optional): Type of text object to create.
                Options are `TextType.Regular` (default) and `TextType.LaTeX`.
                If set to `TextType.LaTeX`, most style-related options will be
                saved but ignored when the text is rendered. These options will
                only be used if the type of the text object is later changed to
                `TextType.Regular`.
            typeface (`str`, optional): The typeface name. For
                consistency across various platforms, Tecplot guarantees that
                the following standard typeface names are available:
                "Helvetica", "Times", "Courier", "Greek", "Math", and "User
                Defined". Other typefaces may or may not be available depending
                on the TrueType fonts available. If the typeface name or style
                is not available, a suitable replacement will be selected.
                (default: "Helvetica")
            bold (`bool`, optional): Use the bold variation of the
                specified typeface. (default: `True`)
            italic (`bool`, optional): Use the italic variation of
                the specified typeface. (default: `False`)
            size_units (`Units`, optional): Text sizing units. Possible
                values are: `Units.Grid`, `Units.Frame` or `Units.Point`.
                (default: `Units.Point`)
            size (`float`, optional): Text height in the specified units.
                (default: 14)
            color (`Color`, optional): Color of the text
                   (default: `Color.Black`)
            angle (`float`, optional): Angle of the text baseline in degrees
                from -360 to 360. (default: 0)
            line_spacing (`float`, optional): Line spacing in units of line
                size. Can take values from 0 to 50. (default: 1)
            anchor (`TextAnchor`, optional): Anchor position with respect to
                the text box. Possible values are: `TextAnchor.Left`,
                `TextAnchor.Center`, `TextAnchor.Right`,
                `TextAnchor.MidLeft`, `TextAnchor.MidCenter`,
                `TextAnchor.MidRight`, `TextAnchor.HeadLeft`,
                `TextAnchor.HeadCenter`, `TextAnchor.HeadRight`,
                `TextAnchor.OnSide` (default: `TextAnchor.Left`)
            box_type (`constant.TextBox`, optional): Type of text box can be one
                of: `constant.TextBox.None_`, `constant.TextBox.Filled` or `constant.TextBox.Hollow`.
                (default: `constant.TextBox.None_`)
            line_thickness (`float`, optional): Text box boarder line
                thickness may be a value in the range from 0.0001 to 100.
                (default: 0.1)
            box_color (`Color`, optional): Text box border line color. See
                `Color` for possible values. (default: `Color.Black`)
            fill_color (`Color`, optional): Text box fill color. See `Color`
                for possible values. (default: `White`)
            margin (`float`, optional): Margin between the text and text
                box. May be in the range from 0 to 2000. (default: 20)
            zone (`Zone <data_access>`, optional): `Zone <data_access>` or
                `XYLinemap` to which the text will be attached. (default: None)

        Returns:
            `annotation.Text`: The resulting `text box <annotation.Text>`
            object.

        Example:

        .. code-block:: python
            :emphasize-lines: 5-6

            import tecplot
            from tecplot.constant import Color

            frame = tecplot.active_frame()
            frame.add_text('Hello, World!', position=(35, 50),
                           bold=True, italic=False, color=Color.Blue)

        .. seealso:: `add_latex`, `delete_text`
        """
        if __debug__:
            tecutil.check_arglist_argtypes(
                'frame.add_text',
                ([tuple], [position], ['position']),
                ([CoordSys], [coord_sys], ['coord_sys']),
                (six.string_types, [typeface, text], ['typeface', 'text']),
                ([bool], [bold, italic], ['bold', 'italic']),
                ([Units], [size_units], ['size_units']),
                ([numbers.Number], [size, angle, line_thickness, margin,
                            line_spacing],
                    ['size', 'angle', 'line_thickness', 'margin',
                     'line_spacing']),
                ([Color], [color, box_color, fill_color],
                    ['color', 'text_color', 'fill_color']),
                ([TextAnchor], [anchor], ['anchor']),
                ([TextBox], [box_type], ['box_type']),
            )

        with tecutil.ArgList() as arglist:
            if zone is not None:
                arglist[sv.ATTACHTOZONE] = True
                arglist[sv.ZONE] = zone.index + 1

            def optional(type_, value):
                return type_(value) if value is not None else None

            # Note that TecUtil calls SV_TEXTCOLOR the color of the text,
            # and SV_COLOR as the text *box* color. These names correspond
            # to the 'color' and 'box_color' parameters.
            arglist.update((
                (sv.TEXT, text),
                (sv.POSITIONCOORDSYS, coord_sys),
                (sv.ISBOLD, bold),
                (sv.ISITALIC, italic),
                (sv.SIZEUNITS, size_units),
                (sv.ANCHOR, anchor),
                (sv.COLOR, box_color),
                (sv.TEXTCOLOR, color),
                (sv.FILLCOLOR, fill_color),
                (sv.BOXTYPE, box_type)))
            arglist[sv.TEXTTYPE] = optional(TextType, text_type)
            if position is not None:
                arglist[sv.XPOS] = optional(float, position[0])
                arglist[sv.YPOS] = optional(float, position[1])

            arglist[sv.HEIGHT] = optional(float, size)
            arglist[sv.ANGLE] = optional(float, angle)
            arglist[sv.LINETHICKNESS] = optional(float, line_thickness)
            arglist[sv.MARGIN] = optional(float, margin)
            arglist[sv.LINESPACING] = optional(float, line_spacing)

            tid = _tecutil.TextCreateX(arglist)
            if tid == 0:
                raise TecplotSystemError()
            return annotation.Text(tid, self)

    def add_latex(self, text, position=None, coord_sys=None, size_units=None,
                  size=None, anchor=None, zone=None):
        r"""Adds a `LaTeX text  <annotation.Text>` annotation to the Frame.

        LaTeX is a computer language designed for typesetting. The most popular
        use of LaTeX is math and Greek fonts for technical purposes. See the
        User Manual for instruction on how to setup LaTeX for use with Tecplot
        360. Once LaTeX is configured for the GUI version of Tecplot 360 no
        additional changes are needed for PyTecplot.

        Parameters:
            text (`str`): The text to add to the `Frame`.
                The text string must have a non-zero length.
            position (`tuple` of `floats <float>` (x,y), optional): The
                position of the anchor as a percentage of the
                specified coordinates. (default: (0,0))
            coord_sys (`CoordSys`, optional): Coordinate system used to
                position the anchor of the text object. The possible values
                are: `CoordSys.Grid` or `CoordSys.Frame`. (default:
                `CoordSys.Frame`)
            size_units (`Units`, optional): Text sizing units. Possible
                values are: `Units.Grid`, `Units.Frame` or `Units.Point`.
                (default: `Units.Point`)
            size (`float`, optional): Text height in the specified units.
                (default: 14)
            anchor (`TextAnchor`, optional): Anchor position with respect to
                the text box. Possible values are: `TextAnchor.Left`,
                `TextAnchor.Center`, `TextAnchor.Right`,
                `TextAnchor.MidLeft`, `TextAnchor.MidCenter`,
                `TextAnchor.MidRight`, `TextAnchor.HeadLeft`,
                `TextAnchor.HeadCenter`, `TextAnchor.HeadRight`,
                `TextAnchor.OnSide` (default: `TextAnchor.Left`)
            zone (`Zone <data_access>`, optional): `Zone <data_access>` or
                `XYLinemap` to which the text will be attached. (default: None)

        Returns:
            `annotation.Text`: The resulting `text box <annotation.Text>`
            object.

        Example:
            .. code-block:: python
                :emphasize-lines: 5-6

                import tecplot as tp
                from tecplot.constant import TextAnchor

                frame = tp.active_frame()
                frame.add_latex(r'$$\zeta(s) = \sum_{n=1}^\infty\frac{1}{n^s}$$',
                                (50,50), size=64, anchor=TextAnchor.Center)

            .. figure:: /_static/images/frame_add_latex.png
                :width: 300px
                :figwidth: 300px

        .. seealso:: `add_text`, `delete_text`
        """
        return self.add_text(text, position=position, coord_sys=coord_sys,
                             size_units=size_units, size=size, anchor=anchor,
                             zone=zone, text_type=TextType.LaTeX)

    @tecutil.lock()
    def create_dataset(self, name, var_names=None, reset_style=True):
        """Create an empty `Dataset`.

        This will create a new `Dataset` and replace the existing one,
        destroying all data associated with it.

        Parameters:
            name (`str`): Title of the new `Dataset`. This does not
                have to be unique.
            var_names (`list` of `strings <str>`, optional): `Variable`
                names. This only sets the names and not the data type or
                location. See `add_variable`. (default: `None`)
            reset_style (`bool`): Reset style of the active `Frame`
                before loading the `Dataset`. (default: `True`)

        Returns:
            `Dataset`: The newly created `Dataset`.

        .. note:: Relationships between `Frame` and `Dataset`

            A `Frame` may only hold a single `Dataset`, though this `Dataset`
            may be shared between several `Frames <Frame>`. Therefore, this
            method will only *replace* the current dataset when **reset_style**
            is set to `True` and will fail otherwise. If this `Frame` already
            has a `Dataset`, it may be more efficient to do one of the following
            instead:

                * Add a new (blank) frame with `Page.add_frame()` and create
                  a `Dataset` for this.
                * Add new zones to the existing `Dataset` with
                  `Dataset.add_ordered_zone()`, `Dataset.add_fe_zone()` or
                  `Dataset.add_poly_zone()`.
                * Change the existing data `in-place <Array>`.

        .. note:: **Performance considerations for data manipulations.**

            When performing many data-manipulation operations including adding
            zones, adding variables, modifying field data or connectivity, and
            especially in connected mode, it is recommended to do this all with
            the `tecplot.session.suspend()`. This will prevent the Tecplot
            engine from trying to "keep up" with the changes. Tecplot will be
            notified of all changes made upon exit of this context. This may
            result in significant performance gains for long operations.

        """
        with self.activated():
            if var_names is not None:
                var_names = tecutil.StringList(*var_names)
            try:
                if not _tecutil.DataSetCreate(name, var_names, reset_style):
                    raise TecplotSystemError()
            finally:
                if var_names is not None:
                    var_names.dealloc()
            return self.dataset

    @property
    def background_color(self):
        """`Color`: Color of the background."""
        return self._get_style(constant.Color, sv.BACKGROUNDCOLOR)

    @background_color.setter
    def background_color(self, value):
        self._set_style(constant.Color(value), sv.BACKGROUNDCOLOR)

    @property
    def border_thickness(self):
        """`float`: The border thickness in units of `Frame.size_pos_units`."""
        return self._get_style(float, sv.BORDERTHICKNESS)

    @border_thickness.setter
    def border_thickness(self, value):
        self._set_style(float(value), sv.BORDERTHICKNESS)

    @property
    def height(self):
        """`float`: The height in units of `Frame.size_pos_units`."""
        return self._get_style(float, sv.HEIGHT)

    @height.setter
    def height(self, value):
        self._set_style(float(value), sv.HEIGHT)

    @property
    def show_border(self):
        """`bool`: Show or hide the `Frame`'s border."""
        return self._get_style(bool, sv.SHOWBORDER)

    @show_border.setter
    def show_border(self, value):
        self._set_style(bool(value), sv.SHOWBORDER)

    @property
    def show_header(self):
        """`bool`: Show or hide the `Frame`'s header in the border."""
        return self._get_style(bool, sv.SHOWHEADER)

    @show_header.setter
    def show_header(self, value):
        self._set_style(bool(value), sv.SHOWHEADER)

    @property
    def header_background_color(self):
        """`Color`: The header's background color."""
        return self._get_style(constant.Color, sv.HEADERCOLOR)

    @header_background_color.setter
    def header_background_color(self, value):
        self._set_style(constant.Color(value), sv.HEADERCOLOR)

    @property
    def size_pos_units(self):
        """`FrameSizePosUnits`: The units used for size properties.

        Possible values: `Paper`, `Workspace <FrameSizePosUnits.Workspace>`.
        """
        return self._get_style(constant.FrameSizePosUnits, sv.FRAMESIZEPOSUNITS)

    @size_pos_units.setter
    def size_pos_units(self, value):
        self._set_style(constant.FrameSizePosUnits(value), sv.FRAMESIZEPOSUNITS)

    @property
    def transparent(self):
        """`bool`: Use transparency within this `Frame`."""
        return self._get_style(bool, sv.ISTRANSPARENT)

    @transparent.setter
    def transparent(self, value):
        self._set_style(bool(value), sv.ISTRANSPARENT)

    @property
    def width(self):
        """`float`: The width in units of `Frame.size_pos_units`."""
        return self._get_style(float, sv.WIDTH)

    @width.setter
    def width(self, value):
        self._set_style(float(value), sv.WIDTH)
