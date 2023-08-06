from builtins import int, str

import getpass
import logging
import os
import platform
import six
import textwrap
import warnings

from ..tecutil import _tecutil, _tecutil_connector
from ..constant import *
from ..exception import *
from .. import layout, macro, tecutil, version
from ..tecutil import IndexSet, StringList, lock, sv


log = logging.getLogger(__name__)


@lock()
def _tecplot_loader_load_data(arglist,
                              frame,
                              read_data_option=None,
                              reset_style=None,
                              initial_plot_first_zone_only=None,
                              initial_plot_type=None,
                              assign_strand_ids=None,
                              add_zones_to_existing_strands=None):
    frame = frame or layout.active_frame()

    # If read_data_option is append and there is no data, we
    # need to silently change it to "Replace in Active Frame"
    if read_data_option == ReadDataOption.Append and (
                not frame.has_dataset or frame.dataset.num_zones == 0):
        read_data_option = ReadDataOption.ReplaceInActiveFrame
    if read_data_option == ReadDataOption.ReplaceInActiveFrame:
        read_data_option = None  # Replace in active frame is the default

    with frame.activated():
        arglist.update(**{
            sv.READDATAOPTION: read_data_option,
            sv.RESETSTYLE: reset_style,
            sv.INITIALPLOTFIRSTZONEONLY: initial_plot_first_zone_only,
            sv.INITIALPLOTTYPE: initial_plot_type,
            sv.ASSIGNSTRANDIDS: assign_strand_ids,
            sv.ADDZONESTOEXISTINGSTRANDS: add_zones_to_existing_strands})

        if __debug__:
            msg = 'loading data:'
            for k, v in arglist.items():
                if k == sv.FILENAMESORINSTRUCTIONS:
                    msg += '\n    {}:'.format(k)
                    for i in v:
                        msg += '\n        {}'.format(i)
                else:
                    msg += '\n    {}: {}'.format(k, v)
            log.debug(msg)

        if not _tecutil.DataSetReadX(arglist):
            raise TecplotSystemError()

        return frame.dataset


@lock()
def load_converge_hdf5(filenames,
                       frame=None,
                       read_data_option=ReadDataOption.Append,
                       reset_style=None,
                       initial_plot_type=None):
    """Read CONVERGE HDF5 data files.

    Parameters:
        filenames (`str` or `list` of `strings <str>`): CONVERGE HDF5 data
            files to be read. (See note below concerning absolute and relative
            paths.)
        frame (`Frame`, optional): The `Frame` to attach the resulting
            `Dataset`. If `None`, the currently active `Frame` is used and the
            zones are appended by default.
        read_data_option (`ReadDataOption`, optional): Specify how the data
            is loaded into Tecplot. (default: `ReadDataOption.Append`)

            Possible values are:
                * `ReadDataOption.ReplaceInActiveFrame`
                    Remove the dataset from the active frame prior to reading
                    in the new dataset. If other frames use the same `DataSet`
                    in the active frame, they will continue to use the old one.
                * `ReadDataOption.Append`
                    Append to the existing `DataSet`.
                * `ReadDataOption.Replace`
                    Replace the `DataSet` attached to the active frame and to
                    all other frames that use the same `DataSet`.
        reset_style (`bool`, optional): Reset the style for
            destination `Frame`. If `False`, the `Frame`'s current style is
            preserved. (default: `True`)
        initial_plot_type (`PlotType`, optional): Forces a specific type of
            plot upon loading of the data. Only used if *resetstyle* is `True`.
            To have |Tecplot 360| determine the most appropriate plot type
            for the data, use `PlotType.Automatic`. Possible values are:
            `PlotType.Automatic` (default), `Cartesian3D`, `Cartesian2D`,
            `XYLine`, `PlotType.Sketch`, `PolarLine`.

    Returns:
        `Dataset`: The `Dataset` holding the loaded data.

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

    .. versionadded:: 2019.1
        Loading CONVERGE HDF5 data requires Tecplot 360 2019 R1 or later.

    .. versionadded:: 1.2
    """
    if isinstance(filenames, six.string_types):
        filenames = filenames.split(',')

    filenames = [tecutil.normalize_path(f) for f in filenames]

    if not _tecutil_connector.connected \
       or _tecutil_connector.client.host in ['localhost', '127.0.0.1']:
        for f in filenames:
            if not os.path.exists(f):
                raise TecplotOSError('File not found: ' + f)

    with tecutil.StringList('STANDARDSYNTAX', '1.0') as instr:
        with tecutil.ArgList() as arglist:
            arglist[sv.DATASETREADER] = 'CONVERGE HDF5 File Loader'
            instr += ['FILELIST_DATAFILES', str(len(filenames))] + filenames
            arglist[sv.FILENAMESORINSTRUCTIONS] = instr
            return _tecplot_loader_load_data(
                arglist, frame=frame, read_data_option=read_data_option,
                reset_style=reset_style,
                initial_plot_type=initial_plot_type,
                assign_strand_ids=True)


@lock()
def load_converge_output(filenames,
                         frame=None,

                         read_data_option=ReadDataOption.Append,
                         reset_style=None):
    """Read CONVERGE Output data files.

    Parameters:
        filenames (`str` or `list` of `strings <str>`): CONVERGE Output data
            files to be read. (See note below concerning absolute and relative
            paths.)
        frame (`Frame`, optional): The `Frame` to attach the resulting
            `Dataset`. If `None`, the currently active `Frame` is used and the
            zones are appended by default.
        read_data_option (`ReadDataOption`, optional): Specify how the data
            is loaded into Tecplot. (default: `ReadDataOption.Append`)

            Possible values are:
                * `ReadDataOption.ReplaceInActiveFrame`
                    Remove the dataset from the active frame prior to reading
                    in the new dataset. If other frames use the same `DataSet`
                    in the active frame, they will continue to use the old one.
                * `ReadDataOption.Append`
                    Append to the existing `DataSet`.
                * `ReadDataOption.Replace`
                    Replace the `DataSet` attached to the active frame and to
                    all other frames that use the same `DataSet`.
        reset_style (`bool`, optional): Reset the style for
            destination `Frame`. If `False`, the `Frame`'s current style is
            preserved. (default: `True`)

    Returns:
        `Dataset`: The `Dataset` holding the loaded data.

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
    """
    if isinstance(filenames, six.string_types):
        filenames = filenames.split(',')
    with StringList('STANDARDSYNTAX', '1.0') as instr:
        with tecutil.ArgList() as arglist:
            arglist[sv.DATASETREADER] = 'CONVERGE Output File Loader'
            instr += ['FILELIST', str(len(filenames))]
            instr += [tecutil.normalize_path(f) for f in filenames]
            arglist[sv.FILENAMESORINSTRUCTIONS] = instr
            return _tecplot_loader_load_data(
                arglist, frame=frame, read_data_option=read_data_option,
                reset_style=reset_style)


@lock()
def load_fvcom(filenames,

               frame=None,

               read_data_option=ReadDataOption.Append,
               reset_style=None,
               initial_plot_type=None):
    """Read FVCOM netCDF data files.

    Parameters:
        filenames (`str` or `list` of `strings <str>`): FVCOM data
            files to be read. (See note below concerning absolute and relative
            paths.)
        frame (`Frame`, optional): The `Frame` to attach the resulting
            `Dataset`. If `None`, the currently active `Frame` is used and the
            zones are appended by default.
        read_data_option (`ReadDataOption`, optional): Specify how the data
            is loaded into Tecplot. (default: `ReadDataOption.Append`)

            Possible values are:
                * `ReadDataOption.ReplaceInActiveFrame`
                    Remove the dataset from the active frame prior to reading
                    in the new dataset. If other frames use the same `DataSet`
                    in the active frame, they will continue to use the old one.
                * `ReadDataOption.Append`
                    Append to the existing `DataSet`.
                * `ReadDataOption.Replace`
                    Replace the `DataSet` attached to the active frame and to
                    all other frames that use the same `DataSet`.
        reset_style (`bool`, optional): Reset the style for
            destination `Frame`. If `False`, the `Frame`'s current style is
            preserved. (default: `True`)
        initial_plot_type (`PlotType`, optional): Forces a specific type of
            plot upon loading of the data. Only used if *resetstyle* is `True`.
            To have |Tecplot 360| determine the most appropriate plot type
            for the data, use `PlotType.Automatic`. Possible values are:
            `PlotType.Automatic` (default), `Cartesian3D`, `Cartesian2D`,
            `XYLine`, `PlotType.Sketch`, `PolarLine`.

    Returns:
        `Dataset`: The `Dataset` holding the loaded data.

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

    .. versionadded:: 2018.2
        Loading FVCOM data requires Tecplot 360 2018 R2 or later.
    """
    if isinstance(filenames, six.string_types):
        filenames = filenames.split(',')
    with StringList('STANDARDSYNTAX', '1.0') as instr:
        with tecutil.ArgList() as arglist:
            arglist[sv.DATASETREADER] = 'FVCOM netCDF Loader'
            instr += ['FILELIST_DATAFILES', str(len(filenames))]
            instr += [tecutil.normalize_path(f) for f in filenames]
            arglist[sv.FILENAMESORINSTRUCTIONS] = instr
            return _tecplot_loader_load_data(
                arglist, frame=frame, read_data_option=read_data_option,
                reset_style=reset_style,
                initial_plot_type=initial_plot_type,
                assign_strand_ids=True)


@lock()
def load_cgns(filenames,

              frame=None,

              read_data_option=ReadDataOption.Append,
              reset_style=None,
              initial_plot_first_zone_only=None,
              initial_plot_type=None,

              zones=None,
              variables=None,

              load_convergence_history=None,
              combine_fe_sections=None,
              average_to_nodes='Arithmetic',
              uniform_grid=None,
              assign_strand_ids=None,
              add_zones_to_existing_strands=None,

              include_boundary_conditions=True):
    """Read CGNS data files.

    Parameters:
        filenames (`str` or `list` of `strings <str>`): CGNS data
            files to be read. (See note below concerning absolute and relative
            paths.)
        frame (`Frame`, optional): The `Frame` to attach the resulting
            `Dataset`. If `None`, the currently active `Frame` is used and the
            zones are appended by default.
        read_data_option (`ReadDataOption`, optional): Specify how the data
            is loaded into Tecplot. (default: `ReadDataOption.Append`)

            Possible values are:
                * `ReadDataOption.ReplaceInActiveFrame`
                    Remove the dataset from the active frame prior to reading
                    in the new dataset. If other frames use the same `DataSet`
                    in the active frame, they will continue to use the old one.
                * `ReadDataOption.Append`
                    Append to the existing `DataSet`.
                * `ReadDataOption.Replace`
                    Replace the `DataSet` attached to the active frame and to
                    all other frames that use the same `DataSet`.
        reset_style (`bool`, optional): Reset the style for
            destination `Frame`. If `False`, the `Frame`'s current style is
            preserved. (default: `True`)
        initial_plot_first_zone_only (`bool`, optional): Informs
            the |Tecplot Engine| that after the data is loaded it only needs to
            activate the first enabled `Zone <data_access>` for the initial
            plot. This option is particularly useful if you have many `Zones
            <data_access>` and want to get the data into the |Tecplot Engine|
            and the first `Zone <data_access>` drawn as fast as possible. The
            inactive `Zones <data_access>` can always be activated when needed.
            (default: `False`)
        initial_plot_type (`PlotType`, optional): Forces a specific type of
            plot upon loading of the data. Only used if *resetstyle* is `True`.
            To have |Tecplot 360| determine the most appropriate plot type
            for the data, use `PlotType.Automatic`. Possible values are:
            `PlotType.Automatic` (default), `Cartesian3D`, `Cartesian2D`,
            `XYLine`, `PlotType.Sketch`, `PolarLine`.

        zones (`list` of `integers <int>`, optional): List of zone indexes to
            load starting from zero. `None` implies loading all zones.
            (default: `None`)
        variables (`list` of `integers <int>`, optional): List of variable
            indexes, beyond the first coordinate variables, to load starting
            from zero. `None` implies loading all variables. The grid will
            always be loaded and an index of zero indicates the first
            non-coordinate variable. (default: `None`)

        load_convergence_history (`bool`, optional): Load the
            global convergence history rather than any grid or solution data.
            (default: `False`)
        combine_fe_sections (`bool`, optional): Combine all
            finite-element sections with the zone cell-dimension into one
            zone. (default: `False`)
        average_to_nodes (`str`, optional): Average
            cell-centered data to grid nodes using the specified method.
            (Options: `None`, "Arithmetic", "Laplacian", default: "Arithmetic")
        uniform_grid (`bool`, optional): Indicates the grid
            structure is the same for all time steps. (default: `True`)
        assign_strand_ids (`bool`, optional): Assign strand ID's to
            zones that have a strand ID of -1. (default: `True`)
        add_zones_to_existing_strands (`bool`, optional): Add the
            `Zones <data_access>` to matching strands, if they exist.
            Otherwise, if the new data specifies strands, new ones will be
            created beginning after the last strand in the `Dataset`. (default:
            `False`)

        include_boundary_conditions (`bool`, optional): Load the
            boundary conditions along with the data. Upon loading, the
            associated fieldmaps will remain inactive. For unstructured data,
            boundary conditions are always loaded and this option is ignored.
            (default: `True`)

    Returns:
        `Dataset`: The `Dataset` holding the loaded data.

    Raises:
        `TecplotSystemError`: Internal error when loading data.
        `TecplotTypeError`: Invalid input.

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
    """
    if __debug__:
        avg_to_nodes_opts = [None, 'Arithmetic', 'Laplacian']
        if average_to_nodes not in avg_to_nodes_opts:
            msg = 'average_to_nodes must be one of: '
            msg += ', '.join(str(x) for x in avg_to_nodes_opts)
            raise TecplotTypeError(msg)

    with StringList('STANDARDSYNTAX', '1.0') as instr:
        with tecutil.ArgList() as arglist:
            arglist[sv.DATASETREADER] = 'CGNS LOADER'
            instr += ['LoaderVersion', 'V3']

            # We need to add the cgns library version to the arglist,
            # although this setting is not exposed in the API.
            instr += ['CgnsLibraryVersion', '3.1.4']

            if isinstance(filenames, six.string_types):
                filenames = filenames.split(',')
            instr += ['FILELIST_CGNSFILES', str(len(filenames))]
            instr += [tecutil.normalize_path(f) for f in filenames]

            if zones is not None:
                indexes = [str(int(z)) for z in zones]
                instr += ['ZoneList', ','.join(indexes)]
            if variables is not None:
                indexes = [str(int(v)) for v in variables]
                instr += ['VarList', ','.join(indexes)]

            if average_to_nodes is None:
                instr += ['AverageToNodes', 'No']
            elif average_to_nodes != 'Arithmetic':
                # Default for 'AverageToNoes' is 'Yes'
                # Default for AveragingMethods is 'Arithmetic'
                instr += ['AveragingMethod', average_to_nodes]

            if uniform_grid is not None:
                instr += ['UniformGridStructure',
                          'Yes' if uniform_grid else 'No']

            if combine_fe_sections is not None:
                instr += [
                    'SectionLoad', 'SeparateZones'
                    if combine_fe_sections else 'Combine']
            if include_boundary_conditions is not None:
                instr += ['LoadBCs',
                          'Yes' if include_boundary_conditions else 'No']
            if load_convergence_history is not None:
                instr += ['LoadConvergenceHistory',
                          'Yes' if load_convergence_history else 'No']
            if assign_strand_ids is not None:
                instr += ['AssignStrandIDs',
                          'Yes' if assign_strand_ids else 'No']

            arglist[sv.FILENAMESORINSTRUCTIONS] = instr

            return _tecplot_loader_load_data(
                arglist, frame=frame, read_data_option=read_data_option,
                reset_style=reset_style,
                initial_plot_first_zone_only=initial_plot_first_zone_only,
                initial_plot_type=initial_plot_type,
                assign_strand_ids=assign_strand_ids,
                add_zones_to_existing_strands=add_zones_to_existing_strands)


@lock()
def load_fluent(case_filenames=None,
                data_filenames=None,

                frame=None,

                append=True,
                zones=None,
                variables=None,

                all_poly_zones=None,
                average_to_nodes='Arithmetic',
                time_interval=None,
                assign_strand_ids=True,
                add_zones_to_existing_strands=None,

                include_particle_data=None,
                include_additional_quantities=True,
                save_uncompressed_files=None):
    """Read Fluent data files.

    Parameters:
        case_filenames (`str` or `list` of `strings <str>`, optional):
            Case (*.cas*, *.cas.gz*) files to be read. Compressed files with
            extension *.gz* are supported. (See note below concerning absolute
            and relative paths.)
        data_filenames (`str` or `list` of `strings <str>`, optional):
            Data (*.dat*, *.xml*, *.dat.gz*, *.fdat*, *.fdat.gz*, etc.) files
            to be read. Compressed files with extension *.gz* are supported.
        frame (`Frame`, optional): The `Frame` to attach the resulting
            `Dataset`. If `None`, the currently active `Frame` is used and the
            zones are appended by default.
        append (`bool`, optional): Append the data to the existing
            `Dataset`. If `False`, the existing data attached to the `Frame` is
            deleted and replaced. (default: `True`)

        zones (`str` or `list` of `integers <int>`, optional): List of
            zone indexes (zero-based) to load or string specifying the type of
            zones to load. Possible values are: "CellsAndBoundaries",
            "CellsOnly" and "BoundariesOnly". Specifying one of these options
            is mutually exclusive with the ``variables`` option. (default:
            "CellsAndBoundaries")
        variables (`list` of `strings <str>`, optional): List of variable
            names to load. `None` implies loading all variables. (default:
            `None`)

        all_poly_zones (`bool`, optional): Converts all zones to
            Tecplot polytope (polyhedral or polygonal) zones. (default:
            `False`)
        average_to_nodes (`str`, optional): Average
            cell-centered data to grid nodes using the specified method.
            (Options: `None`, "Arithmetic", "Laplacian", default: "Arithmetic")
        time_interval (`float`, optional): Use a constant time interval between
            each *.dat* file. If `None`, the flow-data parameter of each
            solution *.dat* file is used. (default: `None`)
        assign_strand_ids (`bool`, optional): Assign strand ID's to
            zones that have a strand ID of -1. (default: `True`)

            .. note::
                assign_strand_ids only applies if you have also provided a
                time_interval, otherwise it will be ignored.
        add_zones_to_existing_strands (`bool`, optional): Add the
            `Zones <data_access>` to matching strands, if they exist.
            Otherwise, if the new data specifies strands, new ones will be
            created beginning after the last strand in the `Dataset`. (default:
            `False`)

        include_particle_data (`bool`, optional): Load particle
            data from the *.dat* files. If loading particle data from an XML
            file, the XML file should be included in the ``data_filenames``
            list. (default: `False`)
        include_additional_quantities (`bool`, optional): Load
            quantities that were derived from the FLUENT's standard quantities.
            (default: `True`) *New in Tecplot 360 2017 R2*.
        save_uncompressed_files (`bool`, optional): Save the
            uncompressed files to the compressed files' location.

    Returns:
        `Dataset`: The `Dataset` holding the loaded data.

    Raises:
        `TecplotSystemError`: Internal error when loading data.
        `TecplotTypeError`: In-valid input.

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

    Notes:
        The ``zones`` option takes either a `list` of zone indexes to be
        imported or one of "CellsAndBoundaries", "CellsOnly" or
        "BoundariesOnly" to indicate the type of zones the user wants to load,
        however these options are mutually exclusive with the ``variables``
        option::

            >>> dataset = tecplot.data.load_fluent(['one.cas', 'two.cas'],
            ...     data_filenames=['one.dat', 'two.dat'],
            ...     variables = ['Pressure','Velocity'],
            ...     zones = [0,1,3])
    """
    if isinstance(case_filenames, six.string_types):
        case_filenames = [case_filenames]
    if isinstance(data_filenames, six.string_types):
        data_filenames = [data_filenames]

    if __debug__:
        zone_types_opts = ['CellsAndBoundaries', 'CellsOnly', 'BoundariesOnly']
        avg_to_nodes_opts = [None, 'Arithmetic', 'Laplacian']
        if isinstance(zones, six.string_types):
            if zones not in zone_types_opts:
                msg = 'Zones must be list of indexes or one of: '
                msg += ', '.join(zone_types_opts)
                raise TecplotTypeError(msg)
            if variables is not None:
                msg = 'Loading a subset of variables is allowed only if'
                msg += ' zones is None or a list of zones.'
                raise TecplotTypeError(msg)
        if (case_filenames or data_filenames) is None:
            raise TecplotTypeError('You must specify a case or data file.')
        if (case_filenames is None) and (len(data_filenames) != 1):
            msg = 'Case file is required when loading multiple data files'
            raise TecplotTypeError(msg)
        if average_to_nodes not in avg_to_nodes_opts:
            msg = 'average_to_nodes must be one of: '
            msg += ', '.join(str(x) for x in avg_to_nodes_opts)
            raise TecplotTypeError(msg)

        if include_additional_quantities:
            sdk_required = (2017, 2)
            if version.sdk_version_info < sdk_required:
                def format_msg(msg):
                    """reflow message, adjusting spaces"""
                    msg = textwrap.dedent(' '.join(msg.split()))
                    return textwrap.fill(msg, width=60)
                msg = 'Out-of-date Tecplot 360.\n'
                msg += format_msg('''\
                    Loading of FLUENT's additional quantities requires Tecplot
                    360 version {} R{} or later. Data will be loaded without
                    these additional quantities.'''.format(*sdk_required))
                warnings.warn(msg)

    with StringList('STANDARDSYNTAX', '1.0') as instr:
        with tecutil.ArgList() as arglist:
            arglist[sv.DATASETREADER] = 'Fluent Data Loader'

            if append:
                instr += ['Append', 'Yes']

            if case_filenames is not None:
                if data_filenames is not None:
                    nfiles = len(case_filenames) + len(data_filenames)
                    instr += ['LoadOption', 'MultipleCaseAndData',
                              'FILELIST_Files', str(nfiles)]
                    instr += [tecutil.normalize_path(f)
                              for f in list(case_filenames) +
                              list(data_filenames)]
                else:
                    instr += ['LoadOption', 'MultipleCaseAndData',
                              'FILELIST_Files', str(len(case_filenames))]
                    instr += [tecutil.normalize_path(f)
                              for f in list(case_filenames)]
            else:
                instr += ['LoadOption', 'ResidualsOnly',
                          'FILENAME_DataFile',
                          tecutil.normalize_path(data_filenames[0])]

            if time_interval is not None:
                instr += ["UnsteadyOption", 'ApplyConstantTimeInterval']
                instr += ['TimeInterval', str(float(time_interval))]

            if isinstance(zones, six.string_types):
                instr += ['GridZones', zones]
            elif (zones or variables) is not None:
                instr += ["GridZones", 'SelectedZones']
                if zones is not None:
                    zone_indexes = ','.join(str(int(z) + 1) for z in zones)
                    instr += ['ZoneList', zone_indexes]
                if variables is not None:
                    var_names = '\n'.join(variables)
                    instr += ['VarNameList', var_names]

            if include_particle_data:  # "No" is the default
                instr += ['IncludeParticleData',
                          'Yes']
            if all_poly_zones:  # "No" is the default
                instr += ['AllPolyZones',
                          'Yes']
            if average_to_nodes is None:
                instr += ['AverageToNodes', 'No']
            elif average_to_nodes != 'Arithmetic':
                # Default for 'AverageToNoes' is 'Yes'
                # Default for AveragingMethods is 'Arithmetic'
                instr += ['AveragingMethod', average_to_nodes]

            if assign_strand_ids is not None:
                instr += ['AssignStrandIDs',
                          'Yes' if assign_strand_ids else 'No']
            if add_zones_to_existing_strands is not None:
                instr += ['AddZonesToExistingStrands',
                          'Yes' if add_zones_to_existing_strands else 'No']

            # Always explicitly provide SaveUncompressedFiles
            instr += ['SaveUncompressedFiles',
                      'Yes' if save_uncompressed_files else 'No']

            if version.sdk_version_info >= (2017, 2):
                instr += ['LoadAdditionalQuantities',
                          'Yes' if include_additional_quantities else 'No']

            arglist[sv.FILENAMESORINSTRUCTIONS] = instr

            return _tecplot_loader_load_data(arglist, frame=frame)


@lock()
def load_telemac(filenames=None,
                 boundary_filename=None,
                 frame=None,
                 read_data_option=ReadDataOption.Append,
                 reset_style=None,
                 initial_plot_type=None):
    """Read Telemac data files and/or boundary file.

    Parameters:
        filenames (`str` or `list` of `strings <str>`, optional): Telemac data
            file(s) to be read. (See note below concerning absolute and
            relative paths.) Not required if a boundary file is being appended
            to an existing data set.
        boundary_filename (`str`, optional): Boundary file. If loaded with
            multiple Telemac files, will be applied to the first Telemac file.
            If loaded with no Telemac files, must be appended to an existing
            data set (read_data_option must be `ReadDataOption.Append`, the
            default).
        frame (`Frame`, optional): The `Frame` to attach the resulting
            `Dataset`. If `None`, the currently active `Frame` is used and the
            zones are appended by default.
        read_data_option (`ReadDataOption`, optional): Specify how the data
            is loaded into Tecplot. (default: `ReadDataOption.Append`)

            Possible values are:
                * `ReadDataOption.ReplaceInActiveFrame`
                    Remove the dataset from the active frame prior to reading
                    in the new dataset. If other frames use the same `DataSet`
                    in the active frame, they will continue to use the old one.
                * `ReadDataOption.Append`
                    Append to the existing `DataSet`.
                * `ReadDataOption.Replace`
                    Replace the `DataSet` attached to the active frame and to
                    all other frames that use the same `DataSet`.
        reset_style (`bool`, optional): Reset the style for
            destination `Frame`. If `False`, the `Frame`'s current style is
            preserved. (default: `True`)
        initial_plot_type (`PlotType`, optional): Forces a specific type of
            plot upon loading of the data. Only used if *resetstyle* is `True`.
            To have |Tecplot 360| determine the most appropriate plot type for
            the data, use `PlotType.Automatic`. Possible values are:
            `PlotType.Automatic`, `Cartesian3D`, `Cartesian2D`, `XYLine`,
            `PlotType.Sketch`, `PolarLine`. (default: `PlotType.Automatic`)

    Returns:
        `Dataset`: The `Dataset` holding the loaded data.

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

    .. versionadded:: 2019.1
        Loading Telemac data requires Tecplot 360 2019 R1 or later.
    """
    with StringList('STANDARDSYNTAX', '1.0') as instr:
        with tecutil.ArgList() as arglist:
            arglist[sv.DATASETREADER] = 'Telemac Data Loader'

            if filenames is not None:
                if isinstance(filenames, six.string_types):
                    filenames = filenames.split(',')
                instr += ['FILELIST_TELEMAC', str(len(filenames))]
                instr += [tecutil.normalize_path(f) for f in filenames]

            if boundary_filename is not None:
                instr += ['FILENAME_BOUNDARY',
                          tecutil.normalize_path(boundary_filename)]

            arglist[sv.FILENAMESORINSTRUCTIONS] = instr

            return _tecplot_loader_load_data(
                arglist, frame=frame, read_data_option=read_data_option,
                reset_style=reset_style,
                initial_plot_type=initial_plot_type,
                assign_strand_ids=True)


@lock()
def load_plot3d(grid_filenames=None,
                solution_filenames=None,
                function_filenames=None,
                name_filename=None,

                frame=None,

                append=True,
                # setting any of these three implies auto_detect=False
                data_structure=None,  # (1D|2D|3DP|3DW|UNSTRUCTURED)
                is_multi_grid=None,  # (True|False)
                style=None,  # (PLOT2DCLASSIC|PLOT3DFUNCTION|OVERFLOW)

                ascii_is_double=None,  # (True|False)
                ascii_has_blanking=None,  # (True|False)
                uniform_grid=None,  # (True|False)

                assign_strand_ids=True,
                add_zones_to_existing_strands=True,
                append_function_variables=None,  # (True|False)
                include_boundaries=True):
    """Read Plot3D data files.

    Parameters:
        grid_filenames (`list` of `strings <str>`, optional): One or more grid
            file names to be read. (See note below concerning absolute and
            relative paths.)
        solution_filenames (`list` of `strings <str>`, optional): One or more
            solution data file names to be read.
        function_filenames (`list` of `strings <str>`, optional): One or more
            function file names.
        name_filename (`str`, optional): Path to the name file.
        frame (`Frame`, optional): The `Frame` to attach the resulting
            `Dataset`. If `None`, the currently active `Frame` is used and the
            zones are appended by default.
        append (`bool`, optional): Append the data to the existing
            `Dataset`. If `False`, the existing data attached to the `Frame` is
            deleted and replaced. (default: `True`)
        data_structure (`str`, optional): Specifies the data
            structure and overrides the automatic detection. Options are:
            ``1D``, ``2D``, ``3DP``, ``3DW``, ``UNSTRUCTURED``. Setting this
            requires ``is_multi_grid`` and ``style`` to be set as well.
        is_multi_grid (`bool`, optional): Sets data as multi-grid
            and overrides the automatic data structure detection. Setting
            this requires ``data_structure`` and ``style`` to be set as well.
        style (`bool`, optional): Specifies the data style and
            overrides the automatic data structure detection. Options are:
            ``PLOT3DCLASSIC``, ``PLOT3DFUNCTION``, ``OVERFLOW``. Setting this
            requires ``data_structure`` and ``is_multi_grid`` to be set as
            well.

        ascii_is_double (`bool`, optional): Indicates that
            floating-point numbers found in the text data files should be
            store with 64-bit precision. (default: `False`)
        ascii_has_blanking (`bool`, optional): Indicates that the
            text data files contain blanking. (default: `False`)
        uniform_grid (`bool`, optional): Indicates the grid
            structure is the same for all time steps. (default: `True`)

        assign_strand_ids (`bool`, optional): Assign strand ID's to
            zones that have a strand ID of -1. (default: `True`)
        add_zones_to_existing_strands (`bool`, optional): Add the
            `Zones <data_access>` to matching strands, if they exist.
            Otherwise, if the new data specifies strands, new ones will be
            created beginning after the last strand in the `Dataset`. (default:
            `True`)
        append_function_variables (`bool`, optional): Append
            variables in function files to those found in solution files.
            (default: `False`)
        include_boundaries (`bool`, optional): Loads boundary zones
            found in the ".g.fvbnd" file located in the same directory as the
            grid file, if available. (default: `True`)

    Returns:
        `Dataset`: The `Dataset` holding the loaded data.

    Raises:
        `TecplotSystemError`: Internal error when loading data.
        `TecplotValueError`: In-valid input.

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

    .. note:: Data structure is automatically detected by default.

        The options ``data_structure``, ``is_multi_grid`` and ``style``
        must be supplied together or not at all. When all of these are
        `None`, the data structure is automatically detected.

    The variables from the function files can be appended to the dataset
    upon loading::

        >>> dataset = tecplot.data.load_plot3d(
        ...     grid_filenames = 'data.g',
        ...     solution_filenames = ['t0.q', 't1.q'],
        ...     function_filenames = ['t0.f', 't1.f'],
        ...     append_function_variables = True)
    """
    if isinstance(grid_filenames, six.string_types):
        grid_filenames = [grid_filenames]
    if isinstance(solution_filenames, six.string_types):
        solution_filenames = [solution_filenames]
    if isinstance(function_filenames, six.string_types):
        function_filenames = [function_filenames]

    if __debug__:
        data_structure_opts = [None, '1D', '2D', '3DP', '3DW', 'UNSTRUCTURED']
        style_opts = [None, 'PLOT3DCLASSIC', 'PLOT3DFUNCTION', 'OVERFLOW']
        if data_structure not in data_structure_opts:
            msg = 'data_structure must be one of: '
            msg += ', '.join(str(x) for x in data_structure_opts)
            raise TecplotValueError(msg)
        if style not in style_opts:
            msg = 'style must be one of: '
            msg += ', '.join(str(x) for x in style_opts)
            raise TecplotValueError(msg)
        if grid_filenames and solution_filenames:
            if len(grid_filenames) != 1 and \
               len(grid_filenames) != len(solution_filenames):
                raise TecplotValueError(textwrap.dedent('''\
                    You must specify a single grid file or
                    the same number of grid and solution files.'''))
        autodetect_opts = [data_structure, is_multi_grid, style]
        if sum([x is None for x in autodetect_opts]) not in [0, 3]:
            raise TecplotValueError(textwrap.dedent('''\
                The options: data_structure, is_multi_grid and style
                must be supplied all together or not at all.'''))

    frame = frame or layout.active_frame()

    with StringList('STANDARDSYNTAX', '1.0') as instr:
        with tecutil.ArgList() as arglist:
            arglist[sv.DATASETREADER] = 'PLOT3D Loader'

            preexisting_dataset = frame.has_dataset and frame.dataset.num_zones
            if append is not None:
                if append:
                    if preexisting_dataset:
                        instr += ['Append', 'Yes']
                else:
                    instr += ['Append', 'No']

            if grid_filenames is not None:
                instr += ['FILELIST_GRIDFILES', str(len(grid_filenames))]
                instr += [tecutil.normalize_path(f) for f in grid_filenames]
            if solution_filenames is not None:
                instr += ['FILELIST_SOLUTIONFILES',
                          str(len(solution_filenames))]
                instr += [tecutil.normalize_path(f) for f in solution_filenames]
            if function_filenames is not None:
                instr += ['FILELIST_FUNCTIONFILES',
                          str(len(function_filenames))]
                instr += [tecutil.normalize_path(f) for f in function_filenames]
            if name_filename is not None:
                instr += ['FILENAME_NAMEFILE',
                          tecutil.normalize_path(name_filename)]

            if (data_structure or is_multi_grid or style) is None:
                instr += ['AUTODETECT', 'Yes']
            else:
                instr += ['AUTODETECT', 'No']
                instr += ['DATASTRUCTURE', data_structure]
                instr += ['ISMULTIGRID', 'Yes' if is_multi_grid else 'No']
                instr += ['STYLE', style]

            if ascii_is_double is not None:
                instr += ['ASCIIISDOUBLE', 'Yes' if ascii_is_double else 'No']
            if ascii_has_blanking is not None:
                instr += ['ASCIIHASBLANK',
                          'Yes' if ascii_has_blanking else 'No']

            if uniform_grid is not None:
                instr += ['UNIFORMGRIDSTRUCTURE',
                          'Yes' if uniform_grid else 'No']
            if assign_strand_ids is not None:
                instr += ['ASSIGNSTRANDIDS',
                          'Yes' if assign_strand_ids else 'No']
            if add_zones_to_existing_strands is not None:
                if preexisting_dataset:
                    instr += ['ADDTOEXISTINGSTRANDS',
                              'Yes' if add_zones_to_existing_strands else 'No']

            if append_function_variables is not None:
                if solution_filenames or preexisting_dataset:
                    instr += ['APPENDFUNCTIONVARIABLES',
                              'Yes' if append_function_variables else 'No']
            if include_boundaries is not None:
                instr += ['LOADBOUNDARY', 'Yes' if include_boundaries else 'No']

            arglist[sv.FILENAMESORINSTRUCTIONS] = instr

            try:
                return _tecplot_loader_load_data(arglist, frame=frame)
            except TecplotLogicError as e:
                if str(e).startswith('The boundary file does not'):
                    log.warning(e)
                    return layout.active_frame().dataset
                raise


@lock()
def load_cfx(filename,
             frame=None,
             append=True,
             assign_strand_ids=True,
             add_zones_to_existing_strands=True,
             initial_plot_type=PlotType.Automatic):
    """Read an ANSYS CFX data file.

    Parameters:
        filename (`str`): The data file to be read. (See note below concerning
            absolute and relative paths.)
        frame (`Frame`, optional): The `Frame` to attach the resulting
            `Dataset`. If `None`, the currently active `Frame` is used and the
            zones are appended by default.
        append (`bool`, optional): Append the data to the existing
            `Dataset`. If `False`, the existing data attached to the `Frame` is
            deleted and replaced. (default: `True`)
        assign_strand_ids (`bool`, optional): Assign strand ID's to
            zones that have a strand ID of -1. (default: `True`)
        add_zones_to_existing_strands (`bool`, optional): Add the
            `Zones <data_access>` to matching strands, if they exist.
            Otherwise, if the new data specifies strands, new ones will be
            created beginning after the last strand in the `Dataset`. (default:
            `True`)
        initial_plot_type (`PlotType`, optional): Set the initial plot type
            upon loading of the data. Must be one of `PlotType.Automatic`
            (default), `PlotType.Cartesian3D` or `PlotType.Cartesian2D`.

    Returns:
        `Dataset`: The `Dataset` holding the loaded data.

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
        The CFX loader is not available on macOS.
    """
    if platform.system() == 'Darwin':
        msg = 'CFX data loader is not available on macOS'
        raise TecplotNotImplementedError(msg)
    with StringList('STANDARDSYNTAX', '1.0') as instr:
        with tecutil.ArgList() as arglist:
            arglist[sv.DATASETREADER] = 'ANSYS CFX (FEA)'
            instr += ['FEALoaderVersion', FEALoaderVersion.Current.value]
            instr += ['FILENAME_File', tecutil.normalize_path(filename)]

            frame = frame or layout.active_frame()
            preexisting_dataset = frame.has_dataset and frame.dataset.num_zones
            if preexisting_dataset:
                instr += ['Append', 'Yes' if append else 'No']
                instr += ['AddToExistingStrands',
                          'Yes' if add_zones_to_existing_strands else 'No']

            instr += ['AutoAssignStrandIDs',
                      'Yes' if assign_strand_ids else 'No']
            initplottype = PlotType(initial_plot_type)
            if initplottype != PlotType.Automatic:
                instr += ['InitialPlotType', initplottype.name]

            arglist[sv.FILENAMESORINSTRUCTIONS] = instr
            return _tecplot_loader_load_data(arglist, frame=frame)


@lock()
def load_ensight(filename,
                 frame=None,
                 read_data_option=ReadDataOption.Append,
                 reset_style=None,
                 initial_plot_first_zone_only=None,
                 initial_plot_type=None,
                 assign_strand_ids=True,
                 add_zones_to_existing_strands=None):
    """Read Ensight data files and/or boundary file.

    Parameters:
        filename (`str`): The case file to be read. (See note below concerning
            absolute and relative paths.)
        frame (`Frame`, optional): The `Frame` to attach the resulting
            `Dataset`. If `None`, the currently active `Frame` is used and the
            zones are appended by default.
        read_data_option (`ReadDataOption`, optional): Specify how the data
            is loaded into Tecplot. (default: `ReadDataOption.Append`)

            Possible values are:
                * `ReadDataOption.ReplaceInActiveFrame`
                    Remove the dataset from the active frame prior to reading
                    in the new dataset. If other frames use the same `DataSet`
                    in the active frame, they will continue to use the old one.
                * `ReadDataOption.Append`
                    Append to the existing `DataSet`.
                * `ReadDataOption.Replace`
                    Replace the `DataSet` attached to the active frame and to
                    all other frames that use the same `DataSet`.
        reset_style (`bool`, optional): Reset the style for
            destination `Frame`. If `False`, the `Frame`'s current style is
            preserved. (default: `True`)
        initial_plot_type (`PlotType`, optional): Forces a specific type of
            plot upon loading of the data. Only used if *resetstyle* is `True`.
            To have |Tecplot 360| determine the most appropriate plot type for
            the data, use `PlotType.Automatic`. Possible values are:
            `PlotType.Automatic`, `Cartesian3D`, `Cartesian2D`, `XYLine`,
            `PlotType.Sketch`, `PolarLine`. (default: `PlotType.Automatic`)
        assign_strand_ids (`bool`, optional): Assign strand ID's to
            zones that have a strand ID of -1. (default: `True`)
        add_zones_to_existing_strands (`bool`, optional): Add the
            `Zones <data_access>` to matching strands, if they exist.
            Otherwise, if the new data specifies strands, new ones will be
            created beginning after the last strand in the `Dataset`. (default:
            `True`)

    Returns:
        `Dataset`: The `Dataset` holding the loaded data.

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
    """
    with StringList('STANDARDSYNTAX', '1.0') as instr:
        with tecutil.ArgList() as arglist:
            arglist[sv.DATASETREADER] = 'EnSight Loader'
            instr += ['FILENAME_CASEFILE', tecutil.normalize_path(filename)]
            arglist[sv.FILENAMESORINSTRUCTIONS] = instr
            return _tecplot_loader_load_data(
                arglist, frame=frame, read_data_option=read_data_option,
                reset_style=reset_style,
                initial_plot_first_zone_only=initial_plot_first_zone_only,
                initial_plot_type=initial_plot_type,
                assign_strand_ids=assign_strand_ids,
                add_zones_to_existing_strands=add_zones_to_existing_strands)


'''
@lock()
def load_kiva(filenames,
              frame=None,
              is_double=True,
              load_particle_data=True,
              velocity_vector='u_vel',
              dataset_title=None):
    """Read Kiva/GMV data files.

    Parameters:
        filenames (`str` or `list` of `strings <str>`): The data file(s) to be
            read. (See note below concerning absolute and relative paths.)
        frame (`Frame`, optional): The `Frame` to attach the resulting
            `Dataset`. If `None`, the currently active `Frame` is used and the
            zones are appended by default.
        is_double (`bool`, optional): Allows greater precision for your data
            values. (default: `True`)
        load_particle_data (`bool`, optional): Adds a zone for any files
            containing particle data. (default: `True`)
        velocity_vector (`str`, optional): Identify the naming convention for
            your velocity vectors. This is the name of the first component (u)
            and is typically one of: "u_vel" (default), "u-vel" or "u".
        dataset_title (`str`, optional): The name of the resulting `Dataset` in
            Tecplot. (default: `None`)

    Returns:
        `Dataset`: The `Dataset` holding the loaded data.

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
    """
    if isinstance(filenames, six.string_types):
        filenames = [filenames]
    with StringList('STANDARDSYNTAX', '1.0') as instr:
        with tecutil.ArgList() as arglist:
            arglist[sv.DATASETREADER] = 'Kiva Loader'
            instr += ['FILELIST_DataFiles', str(len(filenames))]
            instr += [tecutil.normalize_path(f) for f in filenames]
            instr += ['ISDOUBLE', 'YES' if is_double else 'No']
            instr += ['LOADPARTICLEDATA', 'YES' if load_particle_data else 'No']
            instr += ['VELVECTOR', str(velocity_vector)]
            if dataset_title:
                instr += ['DATASETTITLE', str(dataset_title)]
            arglist[sv.FILENAMESORINSTRUCTIONS] = instr
            return _tecplot_loader_load_data(arglist, frame)
'''


@lock()
def load_openfoam(
    filename,
    frame=None,
    append=True,
    boundary_zone_construction=None,
    assign_strand_ids=True,
    add_zones_to_existing_strands=True,
    initial_plot_type=PlotType.Automatic,
    initial_plot_first_zone_only=False
):
    """Read an OpenFOAM data file.

    Parameters:
        filename (`str`): The data file to be read. (See note below concerning
            absolute and relative paths.)
        frame (`Frame`, optional): The `Frame` to attach the resulting
            `Dataset`. If `None`, the currently active `Frame` is used and the
            zones are appended by default.
        append (`bool`, optional): Append the data to the existing
            `Dataset`. If `False`, the existing data attached to the `Frame` is
            deleted and replaced. (default: `True`)
        boundary_zone_construction (`BoundaryZoneConstruction`, optional): Set
            how the boundary zones are constructed. This may be either
            `BoundaryZoneConstruction.Reconstructed` (default) or
            `BoundaryZoneConstruction.Decomposed`. This option requires Tecplot
            360 2019 R1 or later.
        assign_strand_ids (`bool`, optional): Assign strand ID's to
            zones that have a strand ID of -1. (default: `True`)
        add_zones_to_existing_strands (`bool`, optional): Add the
            `Zones <data_access>` to matching strands, if they exist.
            Otherwise, if the new data specifies strands, new ones will be
            created beginning after the last strand in the `Dataset`. (default:
            `True`)
        initial_plot_type (`PlotType`, optional): Set the initial plot type
            upon loading of the data. Must be one of `PlotType.Automatic`
            (default), `PlotType.Cartesian3D` or `PlotType.Cartesian2D`.
        initial_plot_first_zone_only (`bool`, optional): Informs
            the |Tecplot Engine| that after the data is loaded it only needs to
            activate the first enabled `Zone <data_access>` for the initial
            plot. This option is particularly useful if you have many `Zones
            <data_access>` and want to get the data into the |Tecplot Engine|
            and the first `Zone <data_access>` drawn as fast as possible. The
            inactive `Zones <data_access>` can always be activated when needed.
            (default: `False`)

    Returns:
        `Dataset`: The `Dataset` holding the loaded data.

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

    .. warning:: **Zone and variable ordering may change between releases**

        Due to possible changes in data loaders or data formats over time, the
        ordering of zones and variables may be different between versions of
        Tecplot 360. Therefore it is recommended to always reference zones and
        variables **by name** instead of by index.
    """
    if __debug__:
        if (
            boundary_zone_construction is not None and
            version.sdk_version_info < (2018, 3)
        ):
            msg = 'boundary_zone_construction' + \
                  ' requires Tecplot 360 2019 R1 or later'
            raise TecplotOutOfDateEngineError((2019, 1), msg)

    with StringList('STANDARDSYNTAX', '1.0') as instr:
        with tecutil.ArgList() as arglist:
            arglist[sv.DATASETREADER] = 'OpenFOAM (FEA)'

            instr += ['FEALoaderVersion', FEALoaderVersion.Current.value]
            instr += ['FILENAME_File', tecutil.normalize_path(filename)]

            frame = frame or layout.active_frame()
            preexisting_dataset = frame.has_dataset and frame.dataset.num_zones
            if preexisting_dataset:
                instr += ['Append', 'Yes' if append else 'No']
                instr += ['AddToExistingStrands',
                          'Yes' if add_zones_to_existing_strands else 'No']

            instr += ['AutoAssignStrandIDs',
                      'Yes' if assign_strand_ids else 'No']
            initplottype = PlotType(initial_plot_type)
            if initplottype != PlotType.Automatic:
                instr += ['InitialPlotType', initplottype.name]
            instr += ['ShowFirstZoneOnly',
                      'Yes' if initial_plot_first_zone_only else 'No']

            if version.sdk_version_info >= (2018, 3):
                if boundary_zone_construction is None:
                    bzcon = BoundaryZoneConstruction.Reconstructed
                else:
                    bzcon = BoundaryZoneConstruction(boundary_zone_construction)
                instr += ['BoundaryZoneConstruction', bzcon.value]

            arglist[sv.FILENAMESORINSTRUCTIONS] = instr
            return _tecplot_loader_load_data(arglist, frame=frame)


@lock()
def load_stl(filename,
             frame=None,
             append=True,
             subdivide_zones=SubdivideZones.DoNotSubdivide,
             assign_strand_ids=True,
             add_zones_to_existing_strands=True,
             initial_plot_type=PlotType.Automatic,
             initial_plot_first_zone_only=False):
    """Read a 3D Systems STL data file.

    Parameters:
        filename (`str`): The data file to be read. (See note below concerning
            absolute and relative paths.)
        frame (`Frame`, optional): The `Frame` to attach the resulting
            `Dataset`. If `None`, the currently active `Frame` is used and the
            zones are appended by default.
        append (`bool`, optional): Append the data to the existing
            `Dataset`. If `False`, the existing data attached to the `Frame` is
            deleted and replaced. (default: `True`)
        subdivide_zones (`SubdivideZones`, optional): Specify method of zone
            division. Possible values are: `SubdivideZones.DoNotSubdivide`
            (default), `SubdivideZones.ByComponent` and
            `SubdivideZones.ByElementType`.
        assign_strand_ids (`bool`, optional): Assign strand ID's to
            zones that have a strand ID of -1. (default: `True`)
        add_zones_to_existing_strands (`bool`, optional): Add the
            `Zones <data_access>` to matching strands, if they exist.
            Otherwise, if the new data specifies strands, new ones will be
            created beginning after the last strand in the `Dataset`. (default:
            `True`)
        initial_plot_type (`PlotType`, optional): Set the initial plot type
            upon loading of the data. Must be one of `PlotType.Automatic`
            (default), `PlotType.Cartesian3D` or `PlotType.Cartesian2D`.
        initial_plot_first_zone_only (`bool`, optional): Informs
            the |Tecplot Engine| that after the data is loaded it only needs to
            activate the first enabled `Zone <data_access>` for the initial
            plot. This option is particularly useful if you have many `Zones
            <data_access>` and want to get the data into the |Tecplot Engine|
            and the first `Zone <data_access>` drawn as fast as possible. The
            inactive `Zones <data_access>` can always be activated when needed.
            (default: `False`)

    Returns:
        `Dataset`: The `Dataset` holding the loaded data.

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
    """
    with StringList('STANDARDSYNTAX', '1.0') as instr:
        with tecutil.ArgList() as arglist:
            arglist[sv.DATASETREADER] = '3D Systems STL (FEA)'
            instr += ['FEALoaderVersion', FEALoaderVersion.Current.value]
            instr += ['FILENAME_File', tecutil.normalize_path(filename)]

            frame = frame or layout.active_frame()
            preexisting_dataset = frame.has_dataset and frame.dataset.num_zones
            if preexisting_dataset:
                instr += ['Append', 'Yes' if append else 'No']
                instr += ['AddToExistingStrands',
                          'Yes' if add_zones_to_existing_strands else 'No']

            subdiv = SubdivideZones(subdivide_zones)
            if subdiv != SubdivideZones.DoNotSubdivide:
                instr += ['SubdivideZonesBy', subdiv.value]
            instr += ['AutoAssignStrandIDs',
                      'Yes' if assign_strand_ids else 'No']
            initplottype = PlotType(initial_plot_type)
            if initplottype != PlotType.Automatic:
                instr += ['InitialPlotType', initplottype.name]
            instr += ['ShowFirstZoneOnly',
                      'Yes' if initial_plot_first_zone_only else 'No']

            arglist[sv.FILENAMESORINSTRUCTIONS] = instr
            return _tecplot_loader_load_data(arglist, frame=frame)


@lock()
def load_vtk(filenames,
             frame=None,
             read_data_option=ReadDataOption.Append,
             reset_style=True,
             initial_plot_type=PlotType.Automatic,
             assign_strand_ids=True,
             add_zones_to_existing_strands=False,
             solution_time_source=SolutionTimeSource.Auto):
    """Read VTK data files.

    Parameters:
        filenames (`str` or `list` of `strings <str>`): The data file(s) to be
            read. (See note below concerning absolute and relative paths.)
        frame (`Frame`, optional): The `Frame` to attach the resulting
            `Dataset`. If `None`, the currently active `Frame` is used and the
            zones are appended by default.
        read_data_option (`ReadDataOption`, optional): Specify how the data
            is loaded into Tecplot. (default: `ReadDataOption.Append`)

            Possible values are:
                * `ReadDataOption.ReplaceInActiveFrame`
                    The `DataSet` in the active frame is replaced by the new
                    `DataSet`. If other frames were using the same `DataSet`
                    originally in the active frame, they will continue to use
                    it.
                * `ReadDataOption.Append`
                    Append to the existing `DataSet`.
                * `ReadDataOption.Replace`
                    Replace the `DataSet` attached to the active frame, and to
                    all other frames that use the same `DataSet`.

                Default: `ReadDataOption.Append`
        reset_style (`bool`, optional): Reset the style for
            destination `Frame`. If `False`, the `Frame`'s current style is
            preserved. (default: `True`)
        initial_plot_type (`PlotType`, optional): Forces a specific type of
            plot upon loading of the data. Only used if *resetstyle* is `True`.
            To have |Tecplot 360| determine the most appropriate plot type
            for the data, use `PlotType.Automatic`. Possible values are:
            `PlotType.Automatic` (default), `Cartesian3D`, `Cartesian2D`,
            `XYLine`, `PlotType.Sketch`, `PolarLine`.
        assign_strand_ids (`bool`, optional): Assign strand ID's to
            zones that have a strand ID of -1. (default: `True`)
        add_zones_to_existing_strands (`bool`, optional): Add the
            `Zones <data_access>` to matching strands, if they exist.
            Otherwise, if the new data specifies strands, new ones will be
            created beginning after the last strand in the `Dataset`. (default:
            `False`)

        solution_time_source (`SolutionTimeSource`, optional): Assign the
            solution times of the zones based on the specified criteria.
            Possible values are: `SolutionTimeSource.Auto` (default) which
            favors the "time" scalar over the numbers embedded in the file
            names, `SolutionTimeSource.None_` which does not assign solutions
            times or strands, `SolutionTimeSource.FromFieldData` which uses the
            "time" scalar and `SolutionTimeSource.FromFilename` which uses the
            solution time embedded in the file names.

    Returns:
        `Dataset`: The `Dataset` holding the loaded data.

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
    """
    if isinstance(filenames, six.string_types):
        filenames = [filenames]
    with StringList('STANDARDSYNTAX', '1.0') as instr:
        with tecutil.ArgList() as arglist:
            arglist[sv.DATASETREADER] = 'VTK Data Loader'
            instr += ['FILELIST_DATAFILES', str(len(filenames))]
            instr += [tecutil.normalize_path(f) for f in filenames]
            instr += ['SOLUTIONTIMESOURCE',
                      SolutionTimeSource(solution_time_source).value]
            arglist[sv.FILENAMESORINSTRUCTIONS] = instr
            return _tecplot_loader_load_data(
                arglist, frame=frame, read_data_option=read_data_option,
                reset_style=reset_style, initial_plot_type=initial_plot_type,
                assign_strand_ids=assign_strand_ids,
                add_zones_to_existing_strands=add_zones_to_existing_strands)


@lock()
def load_tecplot(filenames,

                 frame=None,

                 read_data_option=ReadDataOption.Append,
                 reset_style=None,
                 initial_plot_first_zone_only=None,
                 initial_plot_type=None,

                 zones=None,
                 variables=None,

                 collapse=None,
                 skip=None,
                 assign_strand_ids=True,
                 add_zones_to_existing_strands=None,

                 include_text=None,
                 include_geom=None,
                 include_custom_labels=None,
                 include_data=None):
    """Read a tecplot data file.

    Parameters:
        filenames (`str` or `list` of `strings <str>`): Files to be
            read. (See note below concerning absolute and relative paths.)
        frame (`Frame`, optional): The `Frame` to attach the resulting
            `Dataset`. If `None`, the currently active `Frame` is used and the
            zones are appended by default.
        read_data_option (`ReadDataOption`, optional): Specify how the data
            is loaded into Tecplot. (default: `ReadDataOption.Append`)

            Possible values are:
                * `ReadDataOption.ReplaceInActiveFrame`
                    The `DataSet` in the active frame is replaced by the new
                    `DataSet`. If other frames were using the same `DataSet`
                    originally in the active frame, they will continue to use
                    it.
                * `ReadDataOption.Append`
                    Append to the existing `DataSet`.
                * `ReadDataOption.Replace`
                    Replace the `DataSet` attached to the active frame, and to
                    all other frames that use the same `DataSet`.

                Default: `ReadDataOption.Append`
        reset_style (`bool`, optional): Reset the style for
            destination `Frame`. If `False`, the `Frame`'s current style is
            preserved. (default: `True`)
        initial_plot_first_zone_only (`bool`, optional): Informs
            the |Tecplot Engine| that after the data is loaded it only needs to
            activate the first enabled `Zone <data_access>` for the initial
            plot. This option is particularly useful if you have many `Zones
            <data_access>` and want to get the data into the |Tecplot Engine|
            and the first `Zone <data_access>` drawn as fast as possible. The
            inactive `Zones <data_access>` can always be activated when needed.
            (default: `False`)
        initial_plot_type (`PlotType`, optional): Forces a specific type of
            plot upon loading of the data. Only used if *resetstyle* is `True`.
            To have |Tecplot 360| determine the most appropriate plot type
            for the data, use `PlotType.Automatic`. Possible values are:
            `PlotType.Automatic` (default), `Cartesian3D`, `Cartesian2D`,
            `XYLine`, `PlotType.Sketch`, `PolarLine`.

        zones (`set` of `integers <int>`, optional): Set of `Zones
            <data_access>` to load. Use `None` to load all zones. (default:
            `None`)
        variables (`set` of `strings <str>` or `integers <int>`, optional):
            Set of `Variables <Variable>` to load. Use `None` to load all
            variables. (default: `None`)

        collapse (`bool`, optional): Reindex `Zones <data_access>` and
            `Variables <Variable>` if any are disabled. (default: `False`)
        skip: (3-`tuple` of `integers <int>`, optional) The *ijk*-skip. A value
            of (1,1,1) loads every data point in the *(i,j,k)* directions. A
            value of (2,2,2) loads every other data point and so forth. This
            only applies to ordered data. (default: (1,1,1))
        assign_strand_ids (`bool`, optional): Assign strand ID's to
            zones that have a strand ID of -1. (default: `True`)
        add_zones_to_existing_strands (`bool`, optional): Add the
            `Zones <data_access>` to matching strands, if they exist.
            Otherwise, if the new data specifies strands, new ones will be
            created beginning after the last strand in the `Dataset`. (default:
            `False`)

        include_text (`bool`, optional): Load any text, geometries, or
            custom labels (default: `True`)
        include_geom (`bool`, optional): Load geometries. (default:
            `True`)
        include_custom_labels (`bool`, optional):  (default: `True`)
        include_data (`bool`, optional): Load data. Set this to
            `False` if you only want annotations such as text or geometries.
            (default: `True`)

    Returns:
        `Dataset`: The `Dataset` holding the loaded data.

    Raises:
        `TecplotSystemError`: Internal error when loading data.
        `TecplotTypeError`: In-valid input.

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
    """
    if isinstance(filenames, six.string_types):
        filenames = [filenames]
    with StringList(tecutil.normalize_path(f) for f in filenames) as fnames:
        with tecutil.ArgList() as arglist:
            allocd = []

            arglist.update(**{
                sv.DATASETREADER: 'TECPLOT',
                sv.FILENAMESORINSTRUCTIONS: fnames,
                sv.INCLUDETEXT: include_text,
                sv.INCLUDEGEOM: include_geom,
                sv.INCLUDECUSTOMLABELS: include_custom_labels,
                sv.INCLUDEDATA: include_data,
                sv.COLLAPSEZONESANDVARS: collapse})

            if zones is not None:
                zoneset = IndexSet(zones)
                allocd.append(zoneset)
                arglist[sv.ZONELIST] = zoneset

            if variables is None:
                arglist[sv.VARLOADMODE] = VarLoadMode.ByName

            else:
                if isinstance(variables[0], int):
                    arglist[sv.VARLOADMODE] = VarLoadMode.ByPosition
                    varset = IndexSet(*variables)
                    allocd.append(varset)
                    arglist[sv.VARPOSITIONLIST] = varset
                elif isinstance(variables[0], six.string_types):
                    arglist[sv.VARLOADMODE] = VarLoadMode.ByName
                    var_string_list = StringList(*variables)
                    allocd.append(var_string_list)
                    arglist[sv.VARNAMELIST] = var_string_list
                else:
                    err = 'unknown type for variables: {}'
                    raise TecplotTypeError(err.format(type(variables)))
            if skip is not None:
                i, j, k = skip
                arglist[sv.ISKIP] = i
                arglist[sv.JSKIP] = j
                arglist[sv.KSKIP] = k

            try:
                return _tecplot_loader_load_data(
                    arglist, frame=frame, read_data_option=read_data_option,
                    reset_style=reset_style,
                    initial_plot_first_zone_only=initial_plot_first_zone_only,
                    initial_plot_type=initial_plot_type,
                    assign_strand_ids=assign_strand_ids,
                    add_zones_to_existing_strands=add_zones_to_existing_strands)
            finally:
                for a in allocd:
                    a.dealloc()


@lock()
def load_tecplot_szl(filenames,

                     frame=None,

                     read_data_option=ReadDataOption.Append,
                     reset_style=None,
                     initial_plot_first_zone_only=None,
                     initial_plot_type=None,
                     assign_strand_ids=True,
                     add_zones_to_existing_strands=None,

                     server=None,
                     connection_method=None,
                     user=None,
                     authentication_method=None,
                     ssh_private_keyfile=None,
                     szlserver_path=None):
    """Read tecplot SZL data file.

    Parameters:
        filenames (`str` or `list` of `strings <str>`): Files to be
            read. (See note below concerning absolute and relative paths.)
        frame (`Frame`, optional): The `Frame` to attach the resulting
            `Dataset`. If `None`, the currently active `Frame` is used and the
            zones are appended by default.
        read_data_option (`ReadDataOption`, optional): Specify how the data
            is loaded into Tecplot. (default: `ReadDataOption.Append`)

            Possible values are:
                * `ReadDataOption.ReplaceInActiveFrame`
                    Remove the dataset from the active frame prior to reading
                    in the new dataset. If other frames use the same `DataSet`
                    in the active frame, they will continue to use the old one.
                * `ReadDataOption.Append`
                    Append to the existing `DataSet`.
                * `ReadDataOption.Replace`
                    Replace the `DataSet` attached to the active frame and to
                    all other frames that use the same `DataSet`.
        reset_style (`bool`, optional): Reset the style for
            destination `Frame`. If `False`, the `Frame`'s current style is
            preserved. (default: `True`)
        initial_plot_first_zone_only (`bool`, optional): Informs
            the |Tecplot Engine| that after the data is loaded it only needs to
            activate the first enabled `Zone <data_access>` for the initial
            plot. This option is particularly useful if you have many `Zones
            <data_access>` and want to get the data into the |Tecplot Engine|
            and the first `Zone <data_access>` drawn as fast as possible. The
            inactive `Zones <data_access>` can always be activated when needed.
            (default: `False`)
        initial_plot_type (`PlotType`, optional): Forces a specific type of
            plot upon loading of the data. Only used if *resetstyle* is `True`.
            To have |Tecplot 360| determine the most appropriate plot type
            for the data, use `PlotType.Automatic`. Possible values are:
            `PlotType.Automatic` (default), `Cartesian3D`, `Cartesian2D`,
            `XYLine`, `PlotType.Sketch`, `PolarLine`.

        assign_strand_ids (`bool`, optional): Assign strand ID's to
            zones that have a strand ID of -1. (default: `True`)
        add_zones_to_existing_strands (`bool`, optional): Add the
            `Zones <data_access>` to matching strands, if they exist.
            Otherwise, if the new data specifies strands, new ones will be
            created beginning after the last strand in the `Dataset`. (default:
            `False`)

        server (`str`, optional): Load the data remotely from this
            server address. When provided, file paths will be relative to the
            SZL server's working directory. (default: `None`)
        connection_method (`RemoteConnectionMethod`, optional): When *server*
            is given, this specifies the type of connection to be made.
            Possible values are: `RemoteConnectionMethod.Tunneled` (default),
            `RemoteConnectionMethod.Direct`, `RemoteConnectionMethod.Manual`.
        user (`str`, optional): When *server* is given and *connection_method* is
            `RemoteConnectionMethod.Tunneled` or
            `RemoteConnectionMethod.Direct`, this specifies the username to use
            when logging into the server. This will default to the client
            host's user name.
        authentication_method (`RemoteAuthenticationMethod`, optional): The
            authentication method to use when connecting to the remote server
            when *connection_method* is `RemoteConnectionMethod.Tunneled` or
            `RemoteConnectionMethod.Direct`. Possible values are
            `RemoteAuthenticationMethod.SSHAgent`,
            `RemoteAuthenticationMethod.SSHPrivateKey` (default) which uses the
            file specified by *ssh_private_keyfile* or
            `RemoteAuthenticationMethod.Password` which will prompt the user
            for the remote login password in the console.
        ssh_private_keyfile (`str`, optional): When *server* is specified and
            *connection_method* is set to `RemoteConnectionMethod.Tunneled` or
            `RemoteConnectionMethod.Direct` and when *authentication_method* is
            set to `RemoteAuthenticationMethod.SSHPrivateKey`, this specifies
            the full path to the private SSH keyfile. This parameter defaults
            to ``~/.ssh/id_rsa`` where ``~`` expands out to the local user's
            home directory.

    Returns:
        `Dataset`: The `Dataset` holding the loaded data.

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

    """
    if isinstance(filenames, six.string_types):
        filenames = [filenames]
    if server is not None:
        if connection_method is None:
            connection_method = RemoteConnectionMethod.Tunneled
        else:
            connection_method = RemoteConnectionMethod(connection_method)

        if (
            not _tecutil_connector.connected and
            connection_method == RemoteConnectionMethod.Manual
        ):
            msg = 'Manual connection to SZL server not supported in batch mode'
            raise TecplotLogicError(msg)

    with tecutil.ArgList() as arglist:
        if server is None:
            instr = ['STANDARDSYNTAX', '1.0']
            instr += ['FILELIST_DATAFILES', str(len(filenames))]
            instr += [tecutil.normalize_path(f) for f in filenames]

            arglist['DATASETREADER'] = 'Tecplot Subzone Data Loader'
        else:
            if user is None:
                user = getpass.getuser()

            instr = ['Connection Method', connection_method.value,
                     'MACHINE', server]

            if connection_method in [RemoteConnectionMethod.Tunneled,
                                     RemoteConnectionMethod.Direct]:
                if authentication_method is None:
                    auth = RemoteAuthenticationMethod.SSHPrivateKey
                else:
                    auth = RemoteAuthenticationMethod(authentication_method)

                instr += ['USER', user, 'SSH Authentication Option', auth.value]

                if auth == RemoteAuthenticationMethod.SSHPrivateKey:
                    if ssh_private_keyfile is None:
                        homedir = os.path.expanduser('~')
                        keyfile = os.path.join(homedir, '.ssh', 'id_rsa')
                    else:
                        keyfile = os.path.expanduser(ssh_private_keyfile)
                    instr += ['Key Path', str(keyfile)]

                if szlserver_path is not None:
                    instr += ['Server Executable Path', str(szlserver_path)]

            instr += ['FILELIST_DATAFILES', str(len(filenames))]
            instr += filenames

            arglist[sv.DATASETREADER] = 'SZL Remote Loader'

        with tecutil.StringList(*instr) as instr:
            arglist['FILENAMESORINSTRUCTIONS'] = instr
            return _tecplot_loader_load_data(
                arglist, frame=frame, read_data_option=read_data_option,
                reset_style=reset_style,
                initial_plot_first_zone_only=initial_plot_first_zone_only,
                initial_plot_type=initial_plot_type,
                assign_strand_ids=assign_strand_ids,
                add_zones_to_existing_strands=add_zones_to_existing_strands)
