from __future__ import division, print_function, absolute_import

import fnmatch
import logging
import re
import six
import warnings

from os import path

from ..tecutil import _tecutil
from ..constant import *
from ..exception import *
from .. import session, tecutil
from ..tecutil import sv
from .page import Page


log = logging.getLogger(__name__)


@tecutil.lock()
def new_layout():
    """Clears the current layout and creates a blank frame.

    This will invalidate any object instances previously obtained:

    .. code-block:: python
        :emphasize-lines: 4

        import tecplot

        frame = tecplot.active_frame()
        tecplot.new_layout()

        # frame object is no longer usable.
        # the following will print:
        #       <class 'ValueError'> 255 is not a valid PlotType
        try:
            frame.plot_type
        except Exception as e:
            print(type(e),e)
    """
    _tecutil.NewLayout()


@tecutil.lock()
def load_layout(filename):
    """Reads a layout file and replaces the active frame.

    Parameters:
        filename (`str`): The file name of the layout to be loaded.
            (See note below conerning absolute and relative paths.)

    Raises:
        `TecplotOSError`: If file can not be found.
        `TecplotSystemError`: If the file could not be loaded.

    .. note:: **Absolute and relative paths with PyTecplot**

        Relative paths, when used within the PyTecplot API are always from
        Python's current working directory which can be obtained by calling
        :func:`os.getcwd()`. This is true for batch and `connected
        <tecplot.session.connect()>` modes. One exception to this is paths
        within a macro command or file which will be relative to the |Tecplot
        Engine|'s home directory, which is typically the |Tecplot 360|
        installation directory. Finally, when connected to a remote (non-local)
        instance of Tecplot 360, only absolute paths are allowed.

        Note that backslashes must be escaped which is especially important for
        windows paths such as ``"C:\\\\Users"`` or ``"\\\\\\\\server\\\\path"``
        which will resolve to ``"C:\\Users"`` and ``"\\\\server\\path"``
        respectively. Alternatively, one may use Python's raw strings:
        ``r"C:\\Users"`` and ``r"\\\\server\\path"``

    This will replace the current layout and therefore will invalidate any
    object instances previously obtained:

    .. code-block:: python
        :emphasize-lines: 8

        import os
        import tecplot as tp

        frame = tp.active_frame()

        examples = tp.session.tecplot_examples_directory()
        layoutfile = os.path.join(examples, 'SimpleData', 'F18.lay')
        tp.load_layout(layoutfile)

        # frame object is no longer usable.
        # the following will print:
        #       <class 'ValueError'> 255 is not a valid PlotType
        try:
            frame.plot_type
        except Exception as e:
            print(type(e),e)
    """
    filepath = tecutil.normalize_path(filename)
    with tecutil.ArgList(FNAME=filepath) as arglist:
        if not _tecutil.OpenLayoutX(arglist):
            raise TecplotSystemError(filepath)


@tecutil.lock()
def save_layout(filename, include_data=None, include_preview=None,
                use_relative_paths=None, post_layout_commands=None,
                pages=None):
    """Writes the current layout to a file.

    Parameters:
        filename (`str`): The path to the output filename. (See note
            below conerning absolute and relative paths.)
        include_data (`bool`, optional): Associated value indicates
            if the layout should be saved as a layout package where the data
            is included with the style information or if it should reference
            linked data. If 'include_data' is None and the filename ends
            with '.lpk', then the file will be saved as a layout package file.
            (default: None)
        include_preview (`bool`, optional): Associated value
            indicates if the layout package should also include a preview
            image. This argument only applies if the include data option is
            True. (default: `True`)
        use_relative_paths (`bool`, optional): Associated value
            indicates if the layout should be saved using relative paths.
            This argument only applies if the include data option is `False`.
            (default: `False`)
        post_layout_commands (`str`, optional): A character string
            containing a set of Tecplot macro commands that are appended to
            the layout or layout package file. These can be almost anything
            and are generally used to store add-on specific state
            information using ``$!EXTENDEDCOMMAND`` commands. (default:
            `None`)
        pages (`list` of `Page` objects, optional): If `None`, all pages
            are written to the layout, otherwise the specified subset of pages
            are written. (default: `None`)

    .. note:: **Absolute and relative paths with PyTecplot**

        Relative paths, when used within the PyTecplot API are always from
        Python's current working directory which can be obtained by calling
        :func:`os.getcwd()`. This is true for batch and `connected
        <tecplot.session.connect()>` modes. One exception to this is paths
        within a macro command or file which will be relative to the |Tecplot
        Engine|'s home directory, which is typically the |Tecplot 360|
        installation directory. Finally, when connected to a remote (non-local)
        instance of Tecplot 360, only absolute paths are allowed.

        Note that backslashes must be escaped which is especially important for
        windows paths such as ``"C:\\\\Users"`` or ``"\\\\\\\\server\\\\path"``
        which will resolve to ``"C:\\Users"`` and ``"\\\\server\\path"``
        respectively. Alternatively, one may use Python's raw strings:
        ``r"C:\\Users"`` and ``r"\\\\server\\path"``

    .. note::

        If you receive an exception with the error message "Journal should be
        valid in all frames", then you must save a data file using
        `save_tecplot_ascii` or `save_tecplot_plt` before saving the layout.

    In this example, we load an example layout file and then save it as a
    packaged layout file:

    .. code-block:: python
        :emphasize-lines: 8

        import os
        import tecplot

        examples_dir = tecplot.session.tecplot_examples_directory()
        infile = os.path.join(examples_dir, 'SimpleData', 'F18.lay')

        tecplot.load_layout(infile)
        tecplot.save_layout('output.lpk')
    """
    if include_data is None and filename.lower().endswith('.lpk'):
        include_data = True

    with tecutil.ArgList() as arglist:
        arglist[sv.FNAME] = tecutil.normalize_path(filename)

        for arg, svarg in [(include_data, sv.INCLUDEDATA),
                           (include_preview, sv.INCLUDEPREVIEW),
                           (use_relative_paths, sv.USERELATIVEPATHS),
                           (post_layout_commands, sv.POSTLAYOUTCOMMANDS)]:
            if arg is not None:
                arglist[svarg] = arg

        if pages is not None:
            # Allow either an int array or page object array
            if isinstance(pages[0], int):
                arglist[sv.PAGELIST] = tecutil.IndexSet(P for P in pages)
            else:
                arglist[sv.PAGELIST] = tecutil.IndexSet(P.position
                                                        for P in pages)

        if not _tecutil.SaveLayoutX(arglist):
            raise TecplotSystemError()


def active_page():
    """Returns the currently active page.

    Returns:
        `Page`: The currently active page.

    Only one `Page` can be active at any given time. As long as the page is not
    deleted (through a call to `new_layout` or `load_layout` for example) this
    can be used to bring it back to the active state:

    .. code-block:: python
        :emphasize-lines: 3

        import tecplot

        page1 = tecplot.active_page()
        page2 = tecplot.add_page()

        # page2 is now active
        assert page2.active

        # we can bring page1 back to the front:
        page1.activate()
        assert page1.active
    """
    return Page(_tecutil.PageGetUniqueID())


def num_pages():
    """Returns the number of pages in the layout.

    Returns: `int`

    Example usage::

        >>> print(tecplot.layout.num_pages())
        1
    """
    return _tecutil.PageGetCount()


@tecutil.lock()
def add_page():
    """Adds a `Page` to the layout.

    Returns:
        `Page`: The newly created page.

    This will implicitly activate the newly created page:

    .. code-block:: python
        :emphasize-lines: 3

        import tecplot
        page1 = tecplot.active_page()
        page2 = tecplot.add_page()
        # page2 is now active
        assert page2.active
    """
    if _tecutil.PageCreateNew():
        return Page(_tecutil.PageGetUniqueID())
    else:
        raise TecplotSystemError('could not add-create-new page')


@tecutil.lock()
def delete_page(page_to_delete):
    """Removes a `Page` from the layout.

    This will render any `Page` object pointing to the deleted `Page` useless.
    The unique ID will not be used again in the active session and it is up
    to the user to clear the python object using `del`:

    .. code-block:: python
        :emphasize-lines: 5

        import tecplot as tp
        from tecplot.exception import TecplotRuntimeError

        page = tp.add_page()
        tp.delete_page(page)

        next_page = tp.active_page()

        assert page != next_page
        assert not page.active

        try:
            # the page is gone so activating
            # will produce an exception
            page.activate()
        except TecplotRuntimeError as e:
            print(e)

        del page # clear the python object
    """
    page_to_delete.activate()
    _tecutil.PageDelete()


@tecutil.lock()
def next_page():
    """Activates and returns the next page.

    Returns:
        `layout.Page`: The next page in the layout.

    `Page` objects are stored in an ordered stack in the |Tecplot Engine|. This
    method rotates the stack and returns the resulting active `Page`:

    .. code-block:: python
        :emphasize-lines: 6

        import tecplot
        from tecplot.layout import next_page

        page1 = tecplot.active_page()
        page2 = tecplot.add_page()
        page3 = next_page()

        # page1 is now the active page
        # and is the same as page3
        assert page1.active
        assert page3 == page1
    """
    _tecutil.PageSetCurrentToNext()
    return active_page()


def page(pattern):
    """Returns the page by name.

    Parameters:
        pattern (`str` or `re.Pattern <re.compile>`): Case-insensitive
            `glob-style pattern string <fnmatch.fnmatch>` or a compiled
            `regex pattern instance <re.compile>` used to match the page by
            name.

    Returns:
        `Page`: The first page identified by *pattern*.

    .. note::

        A layout can contain `pages <Page>` with identical names and only the
        first match found is returned. This is not guaranteed to be
        deterministic and care should be taken to have only `pages <Page>` with
        unique names when this feature is used.

    Example:

    .. code-block:: python
        :emphasize-lines: 6

        import tecplot
        page11 = tecplot.add_page()
        page11.name = 'Page 11'
        page12 = tecplot.add_page()
        page12.name = 'Page 12'
        assert page12 == tecplot.page('Page 1*')
    """
    return next(pages(pattern), None)


def pages(pattern=None):
    """Yields pages matching a specified pattern.

    Parameters:
        pattern (`str` or `re.Pattern <re.compile>`, optional):
            Case-insensitive `glob-style pattern string <fnmatch.fnmatch>` or a
            compiled `regex pattern instance <re.compile>` used to match page
            names.

    Returns:
        `Page`: Generator of pages identified by *pattern* or all pages if
        no *pattern* is specified.

    This function returns a generator which can only be iterated over once.
    It can be converted to a `list` for persistence:

    .. code-block:: python

        import tecplot

        # iterate over all frames in
        # all pages and print their names
        for page in tecplot.pages():
            for frame in page.frames():
                print(frame.name)

        # store a persistent list of pages
        pages = list(tecplot.pages())
    """
    if pattern:
        pattern_type = getattr(re, 'Pattern', getattr(re, '_pattern_type', None))
        if not isinstance(pattern, pattern_type):
            regex = re.compile(fnmatch.translate(pattern), re.IGNORECASE)
        else:
            regex = pattern

    if __debug__:
        found = False
    for i in range(num_pages()):
        current_page = Page(_tecutil.PageGetUniqueID())
        if pattern is None or regex.match(current_page.name):
            if __debug__:
                found = True
            yield current_page
        next_page()

    if __debug__:
        if (
            not found and
            pattern is not None and
            isinstance(pattern, six.string_types) and
            any(c in pattern for c in '*?[]')
        ):
            msg = 'no pages found matching: "{}"'.format(pattern)
            warning = TecplotPatternMatchWarning(pattern, msg, 'glob')
            warnings.warn(warning)


def active_frame():
    """Returns the active frame.

    Returns:
        `Frame`: Currently active frame.
    """
    return active_page().active_frame()


def frames(frame_pattern=None, page_pattern=None):
    """Returns a generator of frames matching the specified pattern.

    Parameters:
        frame_pattern (`str` or `re.Pattern <re.compile>`): Case-insensitive
            `glob-style pattern string <fnmatch.fnmatch>` or a compiled
            `regex pattern instance <re.compile>` used to match the frame by
            name. All frames are returned if no pattern is specified.
        page_pattern (`str` or `re.Pattern <re.compile>`): Case-insensitive
            `glob-style pattern string <fnmatch.fnmatch>` or a compiled
            `regex pattern instance <re.compile>` used to match the page by
            name. All pages are included if no pattern is specified.

    Returns:
        `Frame`: Generator of frames identified by name patterns.

    .. code-block:: python

        import tecplot

        # print name of all frames on all pages
        for frame in tecplot.frames():
            print(frame.name)
    """
    for page in pages(page_pattern):
        for frame in page.frames(frame_pattern):
            yield frame

def aux_data():
    """Auxiliary data for the current layout.

    Returns:
        `AuxData`

    This is the auxiliary data attached to the entire layout containing all
    frames and datasets currently held by the Tecplot Engine. Such data is
    written to the layout file by default and can be retrieved later. Example
    usage:

    .. code-block:: python

        import tecplot as tp

        aux = tp.layout.aux_data()
        aux['info'] = '''\
        This layout contains a lot of things:
            1. Something
            2. Something else
            3. Also this'''

        '''
        The following will print (including newlines):
            This layout contains a lot of things:
                1. Something
                2. Something else
                3. Also this
        '''
        print(aux['info'])
    """
    return session.AuxData(None, AuxDataObjectType.Layout)
