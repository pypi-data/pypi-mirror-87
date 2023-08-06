from __future__ import unicode_literals
from builtins import str

import contextlib
import io
import logging
import os
import re
import textwrap
import sys

import six

from .tecutil import _tecutil, _tecutil_connector
from .exception import TecplotLogicError, TecplotSystemError, TecplotMacroError
from . import tecutil

log = logging.getLogger(__name__)


if not hasattr(contextlib, 'nullcontext'):
    @contextlib.contextmanager
    def nullcontext(result=None):
        yield result
    contextlib.nullcontext = nullcontext


@tecutil.lock()
def execute_function(name, parameters=None):
    """Runs a macro function.

    Parameters:
        name: (`str`): Name of the macro function to run. This name
            is not case sensitive. Must be a non-zero length `str`.

        parameters: (`str`): Any parameters which the quick macro
            requires. Pass `None` (default) for macro functions which require no
            parameters. The parameters are passed as a string which includes
            the parenthesis. For example, if the macro function takes a
            string parameter and int parameter, pass
            **'("string_parameter_name", 2)'** Default: `None`

    Macro functions must be defined before they are used. Typically they
    are defined in the 'tecplot.mcr' configuration file which is read
    when |Tecplot Engine| is initialized. Macro functions
    may also be available in the Quick Macro Panel when the Tecplot 360 GUI
    is running.

    .. note::
        See the |Tecplot Macro Scripting Guide| for more information about
        macro functions.

    Run the "Tile Frames" macro functions. This macro function is defined in
    the file "tecplot.mcr", which is located in the Tecplot 360
    installation directory::

        >>> tecplot.macro.execute_function('Tile Frames')

    Run a macro function named "Calculate" which takes no parameters and
    another macro function called "Display" which takes the name of a
    layout file and an integer as parameters::

        >>> tp.macro.execute_function('Calculate')
        >>> tp.macro.execute_function('Display', '("contour.lay", 2)')
    """
    try:
        if not _tecutil.MacroRunFunction(
                name.strip(),
                parameters.strip() if parameters else None):
            raise TecplotMacroError(name)
    except (TecplotLogicError, TecplotSystemError) as e:
        raise TecplotMacroError(str(e))


@tecutil.lock()
def execute_command(command):
    """Runs a series of tecplot macro commands.

    Parameters:
        command (`str`): The macro commands to be run.

    .. warning:: Zero-based Indexing

        It is important to know that all indexing in |PyTecplot| scripts are
        zero-based. This is a departure from the macro language which is
        one-based. This is to keep with the expectations when working in the
        python language. However, |PyTecplot| does not modify strings that are
        passed to the |Tecplot Engine|. This means that one-based indexing
        should be used when running macro commands from python or when using
        `execute_equation() <tecplot.data.operate.execute_equation>`.

    This command splits the input into individual commands and runs them one
    at a time. See the |Tecplot Macro Scripting Guide| for details about
    |Tecplot 360|'s macro language.

    .. warning::
        The $!VARSET command is not supported. Tecplot Macro variables should be
        converted to Python variables.

    .. warning::
        Intrinsic variables (that is, variables with pipes such as
        ``|DATASETFNAME|``) are not supported. If you need to use an intrinsic
        variable in the macro command, add the macro command to a text file and
        call `execute_file`.

    See the |Tecplot Macro Scripting Guide| for more information about raw data
    and intrinsic variables.

    The following command will perform the same operations as the
    `Hello, World! example <hello_world>`::

        >>> tecplot.macro.execute_command(r'''
        ...   $!ATTACHTEXT
        ...     ANCHORPOS { X = 35 Y = 50 }
        ...     TEXTSHAPE { HEIGHT = 35 }
        ...     TEXT = 'Hello, World!'
        ...   $!EXPORTSETUP EXPORTFNAME = 'hello_world.png'
        ...   $!EXPORT
        ...     EXPORTREGION = CURRENTFRAME
        ... ''')
    """
    varset = re.compile(r'\$!VARSET.*', re.IGNORECASE)
    for c in tecutil.split_macro(command):
        if __debug__:
            if varset.match(c):
                msg = ('The $!VARSET command is not supported in\n'
                       'execute_macro(). Python variables should be used\n'
                       'instead of macro variables. Alternatively, you can\n'
                       'execute a macro in a file with '
                       'macro.execute_file().\n'
                       '$!VARSET is supported in execute_file()')
                raise TecplotMacroError(c + '\n' + msg)
            log.debug('executing command:\n' + c)
        try:
            if not _tecutil.MacroExecuteCommand(c):
                raise TecplotMacroError(c)
        except (TecplotLogicError, TecplotSystemError) as e:
            raise TecplotMacroError(str(e))


@tecutil.lock()
def execute_extended_command(command_processor_id, command, raw_data=None):
    """Runs a tecplot macro command defined in an addon.

    Parameters:
        command_processor_id (`str`):  A unique string used to
            determine the API to call when an extended macro command is
            processed. API's are provided by add-ons or applications
            that extend the Tecplot macro language.

            Typically this will be the name of an add-on or application,
            followed by a version number. For example: 'CFDAnalyzer4'.

            Each application or add-on may provide one or more unique
            command processor ID strings corresponding to different API's,
            or different versions of an API.

            For example, a file converter add-on responsible
            for converting DXF files for Tecplot might provide two versions
            of an API:
            "DXFCONVERTTOOL-1.2", and "DXFCONVERTTOOL-2.0".
            In that case either of these strings would be passed in the
            *command_processor_id* parameter to indicate the version of the
            API to use.

        command (`str`): The command to run.
        raw_data (`str`): Raw data required for the command, if any
            (default: `None`).

    .. warning:: Zero-based Indexing

        It is important to know that all indexing in |PyTecplot| scripts are
        zero-based. This is a departure from the macro language which is
        one-based. This is to keep with the expectations when working in the
        python language. However, |PyTecplot| does not modify strings that are
        passed to the |Tecplot Engine|. This means that one-based indexing
        should be used when running macro commands from python or when using
        `execute_equation() <tecplot.data.operate.execute_equation>`.

    In general, the command string is formatted prior to being fed into the
    |Tecplot Engine| so liberal use of whitespace, including new-lines, are
    acceptable.

    Example::

        >>> tecplot.macro.execute_extended_command(
        ...     'Multi Frame Manager',
        ...     'TILEFRAMESSQUARE')
    """
    try:
        if not _tecutil.MacroExecuteExtendedCommand(
                command_processor_id, command.replace('\n', ' '), raw_data):
            raise TecplotMacroError(command)
    except AttributeError:
        command = textwrap.dedent('''
                $!EXTENDEDCOMMAND
                  COMMANDPROCESSORID = '{procid}'
                  COMMAND = '{cmd}'
            '''.format(procid=command_processor_id,
                       cmd=' '.join(command. split()).replace(r"'", r"\'")))
        execute_command(command)
    except TecplotLogicError:
        raise TecplotMacroError()


@tecutil.lock()
def execute_file(filename):
    """Run a macro file.

    Parameters:
        filename (`str`): The file to be run. (See note
            below concerning absolute and relative paths.)

    .. warning:: Zero-based Indexing

        It is important to know that all indexing in |PyTecplot| scripts are
        zero-based. This is a departure from the macro language which is
        one-based. This is to keep with the expectations when working in the
        python language. However, |PyTecplot| does not modify strings that are
        passed to the |Tecplot Engine|. This means that one-based indexing
        should be used when running macro commands from python or when using
        `execute_equation() <tecplot.data.operate.execute_equation>`.

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

    Example::

        >>> tecplot.macro.execute_file('/path/to/macro_file.mcr')
    """
    try:
        filepath = tecutil.normalize_path(filename)
        if not _tecutil.MacroRunFile(filepath):
            raise TecplotMacroError(filepath)
    except (TecplotLogicError, TecplotSystemError) as e:
        raise TecplotMacroError(str(e))


@contextlib.contextmanager
def record(out=None, header=None):
    """Record a block of python code as a macro.

    Parameters:
        out (`str` filename, output stream object or `None`): Output file
            name of the resulting macro or a text buffer object that
            implements write() and flush() methods. If `None`, then a
            `io.StringIO()` object is yielded and can be used to get the
            string after exiting the context.
        header (`str`, optional): String to prepend to the output. This will
            default to "#!MC 1410\n" for a macro file, but be empty when output
            to a buffer. Set this to an empty string to elide the header when
            writing to a file.

    Example output to a file::

        import tecplot as tp
        with tp.macro.record('recording.mcr'):
            tp.active_frame().plot().show_contour = True

    The resulting contents of the recording.mcr::

        $!FieldLayers ShowContour = Yes

    Example output to a string buffer::

        import io
        import tecplot as tp
        with io.StringIO() as buf:
            with tp.macro.record(buf):
                tp.active_frame().plot().show_contour = True
            mcr = buf.getvalue()
        print(mcr)

    Example output to a new string buffer (setting out to `None`). This
    will produce the same string as the string buffer example above::

        import tecplot as tp
        with tp.macro.record() as buf:
            tp.active_frame().plot().show_contour = True
        mcr = buf.getvalue()
        print(mcr)
    """
    suffix = '.mcr'
    if isinstance(out, six.string_types):
        if out.endswith('.py'):
            suffix = '.py'
        ctx = contextlib.closing(open(out, 'w'))
        header = '#!MC 1410\n' if header is None else header
    elif out is None:
        ctx = contextlib.nullcontext(io.StringIO())
    else:
        ctx = contextlib.nullcontext(out)

    with ctx as ostream:
        with tecutil.temporary_closed_file(suffix=suffix) as ftmp:
            _tecutil_connector.macro_record_start(ftmp)
            try:
                with tecutil.force_recording():
                    yield ostream
            finally:
                _tecutil_connector.macro_record_end()

            with open(ftmp, 'r') as fin:
                src = fin.read().strip()
                src = src.decode('utf-8') if six.PY2 else src
                if header is not None:
                    header = header.decode('utf-8') if six.PY2 else header
                    ostream.write(header)
                    if suffix == '.mcr':
                        src = src[src.find('$!'):]
                ostream.write(src)
                ostream.flush()


def translate(source):
    """Translate macro source code into Python.

    Parameters:
        source (`str`): A multiline string containing the macro commands to be
            translated.

    If no translation is available or the translation fails, the
    `tp.macro.execute_command()` method will be used as a fall-back. No import
    statements are included, and the following header is assumed::

        import tecplot as tp
        from tecplot.constant import *
    """
    result = []
    for command in tecutil.split_macro(source):
        result.append(_tecutil_connector.translate_macro_to_python(command))
    return '\n'.join(result)
