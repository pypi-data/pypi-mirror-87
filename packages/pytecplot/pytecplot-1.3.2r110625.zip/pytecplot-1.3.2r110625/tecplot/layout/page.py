import fnmatch
import logging
import re
import six
import warnings

from contextlib import contextmanager

from ..tecutil import _tecutil
from ..constant import *
from ..exception import *
from .. import macro, session, tecutil
from ..tecutil import Index, lock, lock_attributes, sv
from .frame import Frame


log = logging.getLogger(__name__)


@lock_attributes
class Page(object):
    """`Page` object within a layout, holding onto one or more `Frames <Frame>`.

    Parameters:
        uid (`int`, optional): This must be a *valid* unique ID
            number pointing internally to a `Page` object or `None`. A new
            `Page` is created if set to `None`. (default: `None`)

    Warning:
        Though it is possible to create a `Page` object using the
        constructor, it is usually sufficient to obtain a page through
        `tecplot.add_page`,  `tecplot.active_page`, `tecplot.page` or
        `tecplot.pages`.

    A `Page` can be thought of like a canvas onto which one or more
    `Frames <Frame>` can be laid out. The engine guarantees there will
    always be at least one `Page` in the layout which can be accessed
    via `tecplot.active_page`:

    .. code-block:: python

        import tecplot

        page = tecplot.active_page()
        page.name = 'Page 001'

        # prints: "Page 001"
        print(page.name)

        # prints: "Frame 001"
        for frame in page.frames():
            print(frame.name)
    """
    def __init__(self, uid):
        self.uid = uid
        self.framelist = None
        """The unique ID number of this Page, internal to the |Tecplot Engine|."""
        self._sv = [sv.PAGE]

    def __str__(self):
        """Brief string representation.

        Returns:
            `str`: Brief representation of this `Page`.

        Example:

        .. code-block:: python

            import tecplot
            page = tecplot.active_page()
            page.name = 'Page 001'

            # will print: 'Page: "Page 001"'
            print(page)
        """
        return 'Page: "{name}"'.format(name=self.name)

    def __repr__(self):
        """Executable string representation.

        Returns:
            `str`: Internal representation of this `Page`.

        The string returned can be executed to generate an identical
        copy of this `Page` object:

        .. code-block:: python

            import tecplot
            from tecplot.layout import Page

            page = tecplot.active_page()

            '''
            The "repr" string of the Page is executable code.
            The following will print: "Page(uid=1)"
            '''
            print(repr(page))

            page2 = None
            exec('page2 = '+repr(page))

            '''
            At this point, page2 is just another handle to
            the exact same page object in the Tecplot Engine
            '''
            assert page2 == page
        """
        return 'Page(uid={uid})'.format(uid=self.uid)

    def __eq__(self, other):
        """Checks for `Page` equality in the |Tecplot Engine|.

        Returns:
            `bool`: `True` if the unique ID numbers are the same for both `Pages <Page>`.

        Example:

        .. code-block:: python

            import tecplot

            page1 = tecplot.active_page()
            page2 = tecplot.add_page()

            assert page1 != page2
            assert tecplot.active_page() == page2
        """
        return self.uid == other.uid

    @lock()
    def __contains__(self, frame):
        with self.activated():
            result = False
            if _tecutil.FrameGetCount():
                with session.suspend():
                    _tecutil.FrameLightweightLoopStart()
                    try:
                        while True:
                            if frame.uid == _tecutil.FrameGetUniqueID():
                                result = True
                                break
                            if not _tecutil.FrameLightweightLoopNext():
                                break
                    finally:
                        _tecutil.FrameLightweightLoopEnd()
            return result

    def __getitem__(self, pattern):
        return self.frame(pattern)

    def __iter__(self):
        self.framelist = list(self.frames())
        return self

    def __next__(self):
        try:
            return self.framelist.pop(0)
        except (KeyError, IndexError):
            raise StopIteration

    def next(self):  # if sys.version_info < (3,)
        return self.__next__()

    @property
    def aux_data(self):
        """Auxiliary data for this page.

        Returns: `AuxData`

        This is the auxiliary data attached to the page. Such data is written
        to the layout file by default and can be retrieved later. Example
        usage::

            >>> aux = tp.active_page().aux_data
            >>> aux['Result'] = '3.14159'
            >>> print(aux['Result'])
            3.14159
        """
        return session.AuxData(self, AuxDataObjectType.Page)

    @property
    def position(self):
        """`Index`: Index of the Page

        The page positions are 0 based positions relative to the current page,
        where the current page has a position value of 0, the next page 1,
        the page after that 2, and so on.
        """
        return Index(_tecutil.PageGetPosByUniqueID(self.uid) - 1)

    @property
    def name(self):
        """`str`: Name of the page.

        This is the name used when searching for `Page` objects in
        `tecplot.pages` and `tecplot.page`. It does not have to be unique.

        Example:

        .. code-block:: python

            import tecplot

            page = tecplot.active_page()
            page.name = 'My Data'

            # prints: "this page: My Data"
            print('this page:', page.name)
        """
        with self.activated():
            return _tecutil.PageGetName()[1]

    @name.setter
    @lock()
    def name(self, name):
        with self.activated():
            if not _tecutil.PageSetName(name):
                raise TecplotSystemError()

    @property
    def paper(self):
        """`Paper`: The `Paper` defined in this `Page`.

        Every `Page` has the concept of a workspace which includes
        all `Frames <Frame>` as well as a sub-area of the workspace
        called the `Paper`. The limits of the `Paper` with respect to
        the placement of `Frames <Frame>` is used when exporting
        certain image formats.
        """
        return Paper(self)

    @property
    def active(self):
        """Checks if this `Page` is active.

        Returns:
            `bool`: `True` if active.
        """
        return self.uid == _tecutil.PageGetUniqueID()

    @lock()
    def activate(self):
        """Activates the `Page`.

        Raises:
            `TecplotRuntimeError`: Page does not exist.
            `TecplotSystemError`: Could not activate the page.
        """
        if not self.active:
            if not self.exists:
                raise TecplotRuntimeError('page does not exists')
            elif not _tecutil.PageSetCurrentByUniqueID(self.uid):
                raise TecplotSystemError('could not activate page')

    @contextmanager
    def activated(self):
        current_page = Page(_tecutil.PageGetUniqueID())
        if self == current_page:
            yield
        else:
            self.activate()
            try:
                yield
            finally:
                current_page.activate()

    def active_frame(self):
        """Returns the active `Frame`.

        Returns:
            `Frame`: The active `Frame`.

        This implicitly activates this `Page` and returns the active
        `Frame` attached to it.
        """
        self.activate()
        if _tecutil.FrameGetCount():
            return Frame(_tecutil.FrameGetActiveID(), self)

    @lock()
    def add_frame(self, position=None, size=None):
        """Creates a new `Frame` in this `Page`.

        Parameters:
            position (`tuple` of `floats <float>` (x,y), optional): The
                position (in inches) of the frame relative to the top left
                corner of the paper. If supplied, size must also be supplied.
            size (`tuple` of `floats <float>` (width,height), optional): The
                size (in inches) of the frame. If supplied, position must also
                be supplied.

        Returns:
            `Frame`: The newly created and activated `Frame`.

        This implicitly activates the `Page` and creates and activates
        a new `Frame`.

        .. code-block:: python

            import tecplot as tp

            frame = tp.active_page().add_frame(position=(1, 0.25), size=(8, 9))
        """
        supplied_frame_size = bool(position or size)

        if __debug__:
            if bool(position) ^ bool(size):
                raise TecplotValueError('must supply position and size')
            msg = 'position and size must be 2-tuple'
            if supplied_frame_size:
                if hasattr(position, '__iter__') and hasattr(size, '__iter__'):
                    if len(position) != 2 or len(size) != 2:
                        raise TecplotValueError(msg)
                else:
                    raise TecplotTypeError(msg)

        pos = tecutil.XY(*(position or (0, 0)))
        size = tecutil.XY(*(size or (0, 0)))

        self.activate()
        if not _tecutil.FrameCreateNew(supplied_frame_size, pos.x, pos.y, size.x, size.y):
            raise TecplotSystemError('could not create new frame')
        else:
            uid = _tecutil.FrameGetActiveID()
            if uid > 0:
                return Frame(uid, self)
            else:
                raise TecplotRuntimeError('could not get id of newly created active frame')

    @lock()
    def delete_frame(self, frame):
        """Removes the frame from this `Page`.

        Raises:
            `TecplotRuntimeError`: If `Frame` is not in this `Page`.
            `TecplotSystemError`: Could not delete the frame.
        """
        if frame not in self:
            raise TecplotRuntimeError('frame is not in this page')
        else:
            with frame.activated():
                if not _tecutil.FrameDeleteActive():
                    raise TecplotSystemError()

    @lock()
    def frame(self, pattern):
        """Returns the `Frame` by name.

        Parameters:
            pattern (`str` or `re.Pattern <re.compile>`): Case-insensitive
                `glob-style pattern string <fnmatch.fnmatch>` or a compiled
                `regex pattern instance <re.compile>` used to match the frame
                by name.

        Returns:
            `Frame`: The first `Frame` identified by *pattern*.

        .. note::
            A `Page` can contain `Frames <Frame>` with identical names and only
            the first match found is returned. This is not guaranteed to be
            deterministic and care should be taken to have only `Frames
            <Frame>` with unique names when this feature is used.

        Example:

        .. code-block:: python
            :emphasize-lines: 11

            import tecplot
            page = tecplot.active_page()

            frameA = page.add_frame()
            frameA.name = 'A'

            frameB = page.add_frame()
            frameB.name = 'B'

            assert frameB.active
            assert frameA == page.frame('A')
        """
        pattern_type = getattr(re, 'Pattern', getattr(re, '_pattern_type', None))
        if not isinstance(pattern, pattern_type):
            regex = re.compile(fnmatch.translate(pattern), re.IGNORECASE)
        else:
            regex = pattern

        with self.activated():
            frame = None
            if _tecutil.FrameGetCount():
                with session.suspend():
                    _tecutil.FrameLightweightLoopStart()
                    try:
                        while True:
                            if regex.match(_tecutil.FrameGetName()[1]):
                                frame = Frame(_tecutil.FrameGetUniqueID(), self)
                                break
                            if not _tecutil.FrameLightweightLoopNext():
                                break
                    finally:
                        _tecutil.FrameLightweightLoopEnd()
            if __debug__:
                if (
                    frame is None and
                    isinstance(pattern, six.string_types) and
                    any(c in pattern for c in '*?[]')
                ):
                    msg = 'no frame found matching: "{}"'.format(pattern)
                    warning = TecplotPatternMatchWarning(pattern, msg, 'glob')
                    warnings.warn(warning)
            return frame

    @lock()
    def frames(self, pattern=None):
        """Returns a `list` of `Frames <Frame>` matching the specified pattern.

        Parameters:
            pattern (`str` or `re.Pattern <re.compile>`, optional):
                Case-insensitive `glob-style pattern string <fnmatch.fnmatch>`
                or a compiled `regex pattern instance <re.compile>` used to
                match frame names.

        Returns:
            `list`: `Frames <Frame>` identified by *pattern* or all frames if
            no *pattern* is specified.

        Example:

        .. code-block:: python

            import tecplot

            page = tecplot.active_page()
            page.add_frame()  # create a second frame

            # iterate over all frames and print their names
            for frame in page.frames():
                print(frame.name)

            # store a persistent list of frames
            frames = page.frames()

            # prints: ['Frame 001', 'Frame 002']
            print([f.name for f in frames])
        """
        if pattern:
            pattern_type = getattr(re, 'Pattern', getattr(re, '_pattern_type', None))
            if not isinstance(pattern, pattern_type):
                regex = re.compile(fnmatch.translate(pattern), re.IGNORECASE)
            else:
                regex = pattern

        with self.activated():
            framelist = []
            if _tecutil.FrameGetCount():
                with session.suspend():
                    _tecutil.FrameLightweightLoopStart()
                    try:
                        while True:
                            success, name = _tecutil.FrameGetName()
                            if success:
                                if pattern is None or regex.match(name):
                                    framelist.append(Frame(_tecutil.FrameGetUniqueID(), self))
                            if not _tecutil.FrameLightweightLoopNext():
                                break
                    finally:
                        _tecutil.FrameLightweightLoopEnd()
            if __debug__:
                if (
                    not framelist and
                    pattern is not None and
                    isinstance(pattern, six.string_types) and
                    any(c in pattern for c in '*?[]')
                ):
                    msg = 'no frames found matching: "{}"'.format(pattern)
                    warning = TecplotPatternMatchWarning(pattern, msg, 'glob')
                    warnings.warn(warning)
            return framelist

    @property
    @lock()
    def exists(self):
        """Checks if the `Page` exists in the current layout.

        This will return `False` after the `Page` has been deleted:

        .. code-block:: python

            import tecplot as tp
            page = tp.add_page()
            assert page.exists
            tp.delete_page(page)
            assert not page.exists
        """
        current_page = _tecutil.PageGetUniqueID()
        try:
            for _ in range(_tecutil.PageGetCount()):
                _tecutil.PageSetCurrentToNext()
                if self.uid == _tecutil.PageGetUniqueID():
                    return True
            return False
        finally:
            if current_page != _tecutil.PageGetUniqueID():
                _tecutil.PageSetCurrentByUniqueID(current_page)

    @lock()
    def tile_frames(self, mode=TileMode.Grid):
        """Tile frames based on a certain mode.

        Parameters:
            mode (`TileMode`, optional): Direction and layout mode for tiling
                frames. Possible values: `TileMode.Grid` (default),
                `TileMode.Columns`, `TileMode.Rows`, `TileMode.Wrap`.

        Example usage::

            >>> from tecplot.constant import TileMode
            >>> page.tile_frame(TileMode.Wrap)
        """
        with self.activated():
            macro.execute_extended_command('Multi Frame Manager', mode.value)


@lock_attributes
class Paper(object):
    """The `Paper` boundary defined on a workspace.

    This is the area used for certain image output formats. It
    is defined for a specific `Page`. `Frames <Frame>` can be
    laid out in reference to this sub-area of the workspace.
    """
    def __init__(self, page):
        self.page = page
        self._sv = page._sv + [sv.PAPER]

    @property
    def dimensions(self):
        """Width and height (read-only).

        the dimensions, *(width, height)* in inches, of the
        currently defined paper in the Tecplot workspace.
        """
        with self.page.activated():
            return _tecutil.PaperGetDimensions()
