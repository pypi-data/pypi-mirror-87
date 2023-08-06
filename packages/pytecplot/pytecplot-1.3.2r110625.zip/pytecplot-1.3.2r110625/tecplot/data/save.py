import logging

from six import string_types

from ..tecutil import _tecutil
from ..constant import *
from ..exception import *
from .. import layout, macro, tecutil
from ..tecutil import IndexSet, lock, sv


log = logging.getLogger(__name__)


@lock()
def _save_tecplot(binary, frame, dataset, filename, include_text, include_geom,
                  include_data, include_data_share_linkage,
                  include_autogen_face_neighbors, use_point_format,
                  associate_with_layout, zones, variables, precision, version):
    if dataset is None:
        if frame is None:
            frame = layout.active_frame()
    elif frame is None:
        frame = dataset.frame
    elif frame.dataset != dataset:
        msg = ('Input dataset must be attached to the input Frame: {} != {}'.
               format(repr(frame.dataset), repr(dataset)))
        raise TecplotValueError(msg)

    with frame.activated():
        with tecutil.ArgList() as arglist:
            alloc_list = []
            arglist[sv.FNAME] = tecutil.normalize_path(filename)
            arglist[sv.BINARY] = binary

            if zones is not None:
                s = IndexSet(zones)
                alloc_list.append(s)
                arglist[sv.ZONELIST] = s

            if variables is not None:
                s = IndexSet(variables)
                alloc_list.append(s)
                arglist[sv.VARLIST] = s

            arglist[sv.INCLUDETEXT] = include_text
            arglist[sv.INCLUDEGEOM] = include_geom
            arglist[sv.INCLUDEDATA] = include_data
            arglist[sv.INCLUDEDATASHARELINKAGE] = include_data_share_linkage
            arglist[sv.INCLUDEAUTOGENFACENEIGHBORS] = \
                include_autogen_face_neighbors
            arglist[sv.ASSOCIATELAYOUTWITHDATAFILE] = associate_with_layout
            if version is not None:
                arglist[sv.TECPLOTVERSIONTOWRITE] = BinaryFileVersion(version)
            arglist[sv.PRECISION] = precision
            arglist[sv.USEPOINTFORMAT] = use_point_format

            try:
                if not _tecutil.DataSetWriteX(arglist):
                    raise TecplotSystemError()
            finally:
                for a in alloc_list:
                    a.dealloc()

        return frame.dataset


def save_tecplot_ascii(filename, frame=None, dataset=None, zones=None,
                       variables=None, include_text=None, precision=None,
                       include_geom=None, include_data=None,
                       include_data_share_linkage=None,
                       include_autogen_face_neighbors=None,
                       use_point_format=None):
    """Write Tecplot ASCII data file.

    Parameters:
        filename (`str`): Name of the data file to write. (See note
            below conerning absolute and relative paths.)
        frame (`Frame`, optional): The `Frame` which holds the `Dataset` to
            be written. If this option and *dataset* are both `None`, the
            currently active `Frame` is used. (default: `None`)
        dataset (`Dataset`, optional): The `Dataset` to write out. If this
            and *frame* are both `None`, the `Dataset` of the currently active
            `Frame` is used. (default: `None`)
        include_text (`bool`, optional): Write out all text,
            geometries and custom labels. (default: `True`)
        include_geom (`bool`, optional): Write out all geometries.
            (default: `True`)
        include_data (`bool`, optional): Write out the data. Set
            this to `False` if you only want to write out annotations.
            (default: `True`)
        include_data_share_linkage (`bool`, optional): Conserve space
            and write the variable and connectivity linkage wherever
            possible. If `False`, this will write out all data, losing the
            connectivity sharing linkage for future dataset reads of the
            file. (default: `True`)
        include_autogen_face_neighbors (`bool`, optional): Save the
            face neighbor connectivity. This may produce very large data
            files. (default: `False`)
        use_point_format (`bool`, optional): Write out point format,
            otherwise use block format.
            (default: `False`)
        zones (`list` of `Zones <data_access>`, optional): `Zones
            <data_access>` to write out. Use `None` to write out all `Zones
            <data_access>`. (default: `None`)
        variables (`list` of `Variables <Variable>`, optional):
            `Variables <Variable>` to write out. Use `None` to write out all
            `Variables <Variable>`. (default: `None`)
        precision (`int`, optional): ASCII decimal precision to use.
            (default: 12)

    Returns:
        `Dataset`: The `Dataset` read from when saving.

    Raises:
        `TecplotSystemError`
        `TecplotLogicError`

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

    Example:
        In this example, we load sample data and save the data in Tecplot ASCII
        format:

		.. code-block:: python
		    :emphasize-lines: 12-14

		    from os import path
		    import tecplot
		    examples_directory = tecplot.session.tecplot_examples_directory()
		    infile = path.join(examples_directory,
		                       'OneraM6wing', 'OneraM6_SU2_RANS.plt')
		    dataset = tecplot.data.load_tecplot(infile)
		    variables_to_save = [dataset.variable(V)
		                         for V in ('x','y','z','Pressure_Coefficient')]

		    zone_to_save = dataset.zone('WingSurface')
		    # write data out to an ascii file
		    tecplot.data.save_tecplot_ascii('wing.dat', dataset=dataset,
		                                    variables=variables_to_save,
		                                    zones=[zone_to_save])
    """
    return _save_tecplot(
        binary=False, frame=frame, dataset=dataset,
        filename=filename, include_text=include_text,
        include_geom=include_geom, include_data=include_data,
        include_data_share_linkage=include_data_share_linkage,
        include_autogen_face_neighbors=include_autogen_face_neighbors,
        use_point_format=use_point_format,
        associate_with_layout=None,
        precision=precision,
        zones=zones, variables=variables,
        version=None)


def save_tecplot_plt(filename, frame=None, dataset=None, zones=None,
                        variables=None, version=None, include_text=None,
                        include_geom=None, include_data=None,
                        include_data_share_linkage=None,
                        include_autogen_face_neighbors=None,
                        associate_with_layout=None):
    """Write Tecplot binary PLT data file.

    Parameters:
        filename (`str`): Name of the data file to write. (See note
            below conerning absolute and relative paths.)
        frame (`Frame`, optional): The `Frame` which holds the `Dataset` to
            be written. If this option and *dataset* are both `None`, the
            currently active `Frame` is used. (default: `None`)
        dataset (`Dataset`, optional): The `Dataset` to write out. If this
            and *frame* are both `None`, the `Dataset` of the currently active
            `Frame` is used. (default: `None`)
        zones (`list` of `Zones <data_access>`, optional): `Zones
            <data_access>` to write out. If `None`, all `Zones <data_access>`
            will be saved.
        variables (`list` of `Variables <Variable>`, optional):
            `Variables <Variable>` to write out. If `None`, all `Variables
            <Variable>` will be saved.
        include_text (`bool`, optional): Write out all text,
            geometries and custom labels. (default: `True`)
        include_geom (`bool`, optional): Write out all geometries.
            (default: `True`)
        include_data (`bool`, optional): Write out the data. Set
            this to `False` if you only want to write out annotations.
            (default: `True`)
        include_data_share_linkage (`bool`, optional): Conserve space
            and write the variable and connectivity linkage wherever
            possible. If `False`, this will write out all data, losing the
            connectivity sharing linkage for future dataset reads of the
            file. (default: `True`)
        include_autogen_face_neighbors (`bool`, optional): Save the
            face neighbor connectivity. This may produce very large data
            files. (default: `False`)
        associate_with_layout (`bool`, optional): Associate this
            data file with the current layout. Set to `False` to write the
            datafile without modifying Tecplot's current data file to layout
            association. If *version* is set to anything other than
            `BinaryFileVersion.Current`, this association is not possible,
            and this parameter will be ignored. (default: `True`)
        version (`BinaryFileVersion`, optional): Specifies the
            file version to write. Note that some data may be excluded from
            the file if it cannot be supported in the specified version.
            Possible values are: `Tecplot2006`, `Tecplot2008`, `Tecplot2009`
            and `BinaryFileVersion.Current`. (default:
            `BinaryFileVersion.Current`)

    Returns:
        `Dataset`: The `Dataset` read from when saving.

    Raises:
        `TecplotSystemError`
        `TecplotLogicError`

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

    Example:
        In this example, we load sample data and save the data in Tecplot
        binary PLT format:

		.. code-block:: python
		    :emphasize-lines: 13-15

		    from os import path
		    import tecplot
		    examples_directory = tecplot.session.tecplot_examples_directory()
		    infile = path.join(examples_directory,
		                       'OneraM6wing', 'OneraM6_SU2_RANS.plt')
		    dataset = tecplot.data.load_tecplot(infile)
		    variables_to_save = [dataset.variable(V)
		                         for V in ('x', 'y', 'z',
		                                   'Pressure_Coefficient')]

		    zone_to_save = dataset.zone('WingSurface')
		    # write data out to a binary file
		    tecplot.data.save_tecplot_plt('wing.plt', dataset=dataset,
		                                    variables=variables_to_save,
		                                    zones=[zone_to_save])
    """
    return _save_tecplot(
        binary=True, frame=frame, dataset=dataset,
        filename=filename, include_text=include_text,
        include_geom=include_geom, include_data=include_data,
        include_data_share_linkage=include_data_share_linkage,
        include_autogen_face_neighbors=include_autogen_face_neighbors,
        use_point_format=None,
        associate_with_layout=associate_with_layout,
        precision=None,
        zones=zones, variables=variables,
        version=version)


def save_tecplot_szl(filename, frame=None, dataset=None):
    """Write Tecplot SZL data file.

    Parameters:
        filename (`str`): Name of the data file to write. (See note
            below conerning absolute and relative paths.)
        frame (`Frame`, optional): The `Frame` which holds the `Dataset` to
            be written. If this option and *dataset* are both `None`, the
            currently active `Frame` is used. (default: `None`)
        dataset (`Dataset`, optional): The `Dataset` to write out. If this
            and *frame* are both `None`, the `Dataset` of the currently active
            `Frame` is used. (default: `None`)

    Returns:
        `Dataset`: The `Dataset` read from when saving.

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

    Example:
        In this example, we load sample data and save it in Tecplot SZL
        format:

        .. code-block:: python
            :emphasize-lines: 7

            from os import path
            import tecplot
            examples_directory = tecplot.session.tecplot_examples_directory()
            infile = path.join(examples_directory,
                               'OneraM6wing', 'OneraM6_SU2_RANS.plt')
            dataset = tecplot.data.load_tecplot(infile)
            tecplot.data.save_tecplot_szl('wing.szplt')
    """
    if dataset is None:
        if frame is None:
            frame = layout.active_frame()
    elif frame is None:
        frame = dataset.frame
    elif frame.dataset != dataset:
        msg = ('Input dataset must be attached to the input Frame: {} != {}'.
               format(repr(frame.dataset), repr(dataset)))
        raise TecplotValueError(msg)

    filepath = tecutil.normalize_path(filename)
    with frame.activated():
        macro.execute_extended_command(
            'Tecplot Subzone Data Tools',
            'WRITEDATASET FILENAME="{}"'.format(filepath))
        return frame.dataset
