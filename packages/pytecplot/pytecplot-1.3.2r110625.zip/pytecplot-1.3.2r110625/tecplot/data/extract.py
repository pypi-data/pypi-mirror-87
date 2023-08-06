import ctypes

from ..tecutil import _tecutil
from ..constant import *
from ..exception import *
from .. import layout, macro, tecutil, version
from ..tecutil import sv


@tecutil.lock()
def extract_blanked_zones(*zones, **kwargs):
    """Extract subsets of `Zones`_ based on blanking conditions of the plot.

    Parameters:
        *zones (`Zones`_, required): Set of source zones to extract.

    Keyword Arguments:
        plot (`Cartesian3DFieldPlot` or other data-backed plot type, optional):
            The plot that defines the blanking conditions. By default, the
            active plot will be used.

    Returns:
        `Zones`_: A `list` of the extracted zones.

    A new zone will be created for each zone specified unless blanking dictates
    that all cells and points in the entire zone are blanked. The following
    example extracts all zones in the dataset:

    .. code-block:: python

        import os

        import tecplot as tp
        from tecplot.constant import *

        examples_dir = tp.session.tecplot_examples_directory()
        datafile = os.path.join(examples_dir, 'SimpleData', 'VortexShedding.plt')

        dataset = tp.data.load_tecplot(datafile)

        plot = tp.active_frame().plot()
        plot.show_contour = True

        xax = plot.axes.x_axis
        xax.min = -0.005
        xax.max = 0.015
        yax = plot.axes.y_axis
        yax.min = -0.01
        yax.max = 0.002

        # Setup value blanking
        vblank = plot.value_blanking
        constraint = vblank.constraint(0)
        constraint.variable_index = 1
        constraint.comparison_operator = RelOp.GreaterThan
        constraint.active = True
        vblank.active = True

        # Use list comprehension to get all zones assocaitated with
        # a specific strand, in this case strand 1
        in_zns = [zn for zn in dataset.zones() if zn.strand == 1]

        # Extract all zones assocaitated with strand 1
        ext_zns = tp.data.extract.extract_blanked_zones(in_zns)

        # Place all extracted zones into the same strand
        for zn in ext_zns:
            zn.strand = 2

        # Turn off plotting for the original zone and turn on plotting
        # of the extracted zones.
        plot.fieldmap(0).show = False
        plot.fieldmap(1).show = True

        tp.export.save_time_animation_mpeg4('extract_blanked_zones.mp4',
                                            width=400, end_time=0.0004,
                                            supersample=3)

    .. raw:: html

        <video controls>
            <source src="../_static/videos/extract_blanked_zones.m4v" type="video/mp4">
            I'm sorry; your browser doesn't support HTML5 MPEG4/H.264 video.
        </video>

    .. versionadded:: 2020.1
        Extracting blanked zones requires Tecplot 360 2020 R1 or later.
    """
    if __debug__:
        if version.sdk_version_info < (2020,):
            msg = 'Extracting blanked zones not supported.'
            raise TecplotOutOfDateEngineError((2020,), msg)

    if not zones:
        msg = 'extract_blanked_zones(*zones) requires at least one zone'
        raise TecplotLogicError(msg)
    plot = kwargs.get('plot', None)
    if not plot:
        plot = layout.active_frame().plot()
    dataset = plot.frame.dataset
    num_zones = dataset.num_zones
    with plot.activated():
        zones = tecutil.flatten_args(*zones)
        zone_indices = (getattr(z, 'index', z) for z in zones)
        cmd = 'Zones = [{}]'.format(','.join(str(z + 1) for z in zone_indices))
        macro.execute_extended_command('ExtractBlankedZones', cmd)
    return [dataset.zone(i) for i in range(num_zones, dataset.num_zones)]


@tecutil.lock()
def extract_line(points, num_points=None, frame=None, dataset=None):
    """Create new zone from a line in the dataset.

    Parameters:
        points (``2D numeric array``): The points defining the line in two or
            three dimensions. This array must be of the shape *(N, D)* where
            *N* is the number points and *D* is the number of dimensions. That
            is, it must take the form ``[(x0, y0, z0), (x1, y1, z1) ...]``.
            Points that do not lie within the dataset volume will be removed
            from the resulting zone.
        num_points (`int`, optional): The number of points to evenly
            distribute along the polyline. (default: length of *points* or *N*)
        frame (`Frame`, optional): A `Frame` that holds the `Dataset` to
            operate on which must match *dataset* if given. (default: currently
            active `Frame`)
        dataset (`Dataset`, optional): The `Dataset` to operate on which must
            be attached to *frame* if given. (default: currently active
            `Dataset`)

    Returns:
        A 1D `OrderedZone` representing a line through the data. Points outside
        of the dataset will be removed from the extracted zone resulting in
        fewer points than input.

    .. warning::

        Line extraction is only available when the plot type is set to
        `Cartesian2D` or `Cartesian3D`::

            >>> from tecplot.constant import PlotType
            >>> frame.plot_type = PlotType.Cartesian3D

    This example shows how to extract a zone along a line, overlaying the
    result in a new frame:

    .. code-block:: python
        :emphasize-lines: 26

        import numpy as np
        from os import path

        import tecplot as tp
        from tecplot.constant import *

        examples_dir = tp.session.tecplot_examples_directory()
        datafile = path.join(examples_dir, 'SimpleData', 'VortexShedding.plt')
        dataset = tp.data.load_tecplot(datafile)

        frame = tp.active_frame()
        frame.activate()
        plot = frame.plot()
        plot.contour(0).variable = dataset.variable("P(N/M2)")
        plot.show_contour = True
        plot.contour(0).levels.reset(num_levels=11)
        plot.contour(0).colormap_name = 'Sequential - Yellow/Green/Blue'

        plot.axes.y_axis.min = -0.01
        plot.axes.y_axis.max = 0.01
        plot.axes.x_axis.min = -0.005
        plot.axes.x_axis.max = 0.015

        xx = np.linspace(0, 0.01, 100)
        yy = np.zeros(100)
        line = tp.data.extract.extract_line(zip(xx, yy))

        plot.show_mesh = True
        plot.fieldmap(0).mesh.show = False

        frame = tp.active_page().add_frame()
        frame.position = (3.0, 0.5)
        frame.height = 2
        frame.width = 4
        plot = tp.active_frame().plot(PlotType.XYLine)
        plot.activate()

        plot.delete_linemaps()
        lmap = plot.add_linemap('data', line, x=dataset.variable('P(N/M2)'),
                                y=dataset.variable('T(K)'))
        lmap.line.line_thickness = 2.0
        plot.axes.x_axis(0).title.font.size = 10
        plot.axes.y_axis(0).title.font.size = 10
        plot.axes.viewport.left = 20
        plot.axes.viewport.bottom = 20
        plot.view.fit()

        tp.export.save_png("extract_line.png", region=ExportRegion.AllFrames,
                           width=600, supersample=3)

    .. figure:: /_static/images/extract_line.png
        :width: 300px
        :figwidth: 300px
    """
    if dataset is None:
        if frame is None:
            frame = layout.active_frame()
        dataset = frame.dataset
    elif frame is None:
        frame = dataset.frame

    if __debug__:
        if frame.plot_type not in [PlotType.Cartesian2D, PlotType.Cartesian3D]:
            msg = 'must be in a cartesian plot type to extract a line'
            raise TecplotLogicError(msg)
        if dataset != frame.dataset:
            msg = 'dataset is not attached to given frame'
            raise TecplotLogicError(msg)

    new_zone_index = dataset.num_zones

    try:
        _ = points[0]
    except TypeError:
        points = list(points)

    ndim = len(points[0])
    if num_points is None:
        num_points = len(points)

    n = len(points)
    xx = (ctypes.c_double * n)(*(float(p[0]) for p in points))
    yy = (ctypes.c_double * n)(*(float(p[1]) for p in points))
    zz = (ctypes.c_double * n)(*([0.]*len(xx)
                                 if ndim < 3
                                 else (float(p[2]) for p in points)))

    extract_through_volume = ndim == 3
    only_points_on_line = num_points == len(points)
    include_distance = False
    to_file = False
    filename = None

    try:
        if not _tecutil.ExtractFromPolyline(xx, yy, zz, len(xx),
                                            extract_through_volume,
                                            only_points_on_line,
                                            include_distance, num_points,
                                            to_file, filename):
            raise TecplotSystemError()
    except TecplotLogicError as e:
        # If some of the points are outside of the data, the zone
        # is still extracted and this exception is not technically
        # an error. A different message is generated if all of the
        # points are outside of the data which is re-raised.
        if 'Probe Position is outside of the data' not in str(e):
            raise

    return dataset.zone(new_zone_index)


@tecutil.lock()
def extract_slice(origin=(0, 0, 0), normal=(0, 0, 1), source=None,
                  mode=ExtractMode.SingleZone, copy_cell_centers=None,
                  assign_strand_ids=None,
                  transient_mode=TransientOperationMode.SingleSolutionTime,
                  frame=None, dataset=None, **kw):
    """Create new zone from a plane in the dataset.

    Parameters:
        origin (array of three `floats <float>`): Point in space,
            :math:`(x, y, z)`, that lies on the slice plane.
        normal (array of three `floats <float>`): Vector direction,
            :math:`(x, y, z)`, indicating the normal of the slice plane.
        source (`SliceSource`): Source zone types to consider when extracting
            the slice. Possible values: `SliceSource.LinearZones`,
            `SliceSource.SurfaceZones`, `SliceSource.SurfacesOfVolumeZones`,
            `SliceSource.VolumeZones` (default).
        mode (`ExtractMode`): Controls how many zones are created. Possible
            values are: `ExtractMode.SingleZone` (default),
            `ExtractMode.OneZonePerConnectedRegion` and
            `ExtractMode.OneZonePerSourceZone`.
        copy_cell_centers (`bool`): If `True`, cell-center
            values will be copied when possible to the extracted slice plane.
            Cell-centers are copied when a variable is cell-centered for all
            the source zones through which the slice passes. Otherwise,
            extracted planes use node-centered data, which is calculated by
            interpolation. (default: `False`)
        assign_strand_ids (`bool`): Automatically assign strand IDs
            to the data extracted from transient sources. This is only
            available if *multiple_zones* is `False`. (default: `True`)
        transient_mode (`TransientOperationMode`): Determines which solution
            times are used to extract slices when transient data is available
            in the dataset. Possible values are
            `TransientOperationMode.SingleSolutionTime` (default) or
            `TransientOperationMode.AllSolutionTimes`.
        frame (`Frame`, optional): A `Frame` that holds the `Dataset` to
            operate on which must match *dataset* if given. (default: currently
            active `Frame`)
        dataset (`Dataset`, optional): The `Dataset` to operate on which must
            be attached to *frame* if given. (default: currently active
            `Dataset`)

    Returns:
        One or a `list` of `Zones <data_access>` representing a planar slice.

    .. warning::

        Slicing is only available when the plot type is set to 3D::

            >>> from tecplot.constant import PlotType
            >>> frame.plot_type = PlotType.Cartesian3D

    .. note::

        The extracted zone is returned if **mode** is `ExtractMode.SingleZone`
        and **transient_mode** is `TransientOperationMode.SingleSolutionTime`,
        otherwise a `generator <https://docs.python.org/3/reference/expressions.html#generator-expressions>`_
        of the extracted zones.

    .. seealso:: `tecplot.plot.SliceGroup.extract()`

    This example shows extracting a slice zone from the surface a wing:

    .. code-block:: python
        :emphasize-lines: 16-20

        import os
        import tecplot as tp
        from tecplot.constant import PlotType, SliceSource

        examples_dir = tp.session.tecplot_examples_directory()
        datafile = os.path.join(examples_dir, 'OneraM6wing',
                                'OneraM6_SU2_RANS.plt')
        dataset = tp.data.load_tecplot(datafile)

        frame = tp.active_frame()
        frame.plot_type = PlotType.Cartesian3D

        # set active plot to 3D and extract
        # an arbitrary slice from the surface
        # data on the wing
        extracted_slice = tp.data.extract.extract_slice(
            origin=(0, 0.25, 0),
            normal=(0, 1, 0),
            source=SliceSource.SurfaceZones,
            dataset=dataset)

        # switch plot type in current frame, clear plot
        plot = frame.plot(PlotType.XYLine)
        plot.activate()
        plot.delete_linemaps()

        # create line plot from extracted zone data
        cp_linemap = plot.add_linemap(
            name='Quarter-chord C_p',
            zone=extracted_slice,
            x=dataset.variable('x'),
            y=dataset.variable('Pressure_Coefficient'))

        # set style of linemap plot and
        # update axes limits to show data
        cp_linemap.line.color = tp.constant.Color.Blue
        cp_linemap.line.line_thickness = 0.8
        cp_linemap.y_axis.reverse = True
        plot.view.fit()

        # export image of pressure coefficient as a function of x
        tp.export.save_png('wing_slice_pressure_coeff.png', 600, supersample=3)

    .. figure:: /_static/images/wing_slice_pressure_coeff.png
        :width: 300px
        :figwidth: 300px
    """
    if 'multiple_zones' in kw:
        tecutil.api_changed('''\
            "multiple_zones" has been removed, please use "mode" instead.''',
            '0.13', '2018 R2')

    if dataset is None:
        if frame is None:
            frame = layout.active_frame()
        dataset = frame.dataset
    elif frame is None:
        frame = dataset.frame

    mode = ExtractMode(mode)
    transient_mode = TransientOperationMode(transient_mode)

    if __debug__:
        if frame.dataset != dataset:
            raise TecplotLogicError('Dataset is not attached to frame.')
        if frame.plot_type is not PlotType.Cartesian3D:
            msg = 'Plot Type must be Cartesian3D to create a slice.'
            raise TecplotLogicError(msg)
        if mode != ExtractMode.SingleZone:
            if version.sdk_version_info < (2017, 3):
                msg = '"mode" parameter not supported.'
                raise TecplotOutOfDateEngineError((2017, 3), msg)
        if transient_mode != TransientOperationMode.SingleSolutionTime:
            if version.sdk_version_info < (2019, 1):
                msg = 'Slice over all solution times not supported'
                raise TecplotOutOfDateEngineError((2019, 1), msg)

    with frame.activated():
        nzones = dataset.num_zones
        with tecutil.ArgList() as arglist:
            arglist[sv.ORIGINX] = float(origin[0])
            arglist[sv.ORIGINY] = float(origin[1])
            arglist[sv.ORIGINZ] = float(origin[2])
            arglist[sv.NORMALX] = float(normal[0])
            arglist[sv.NORMALY] = float(normal[1])
            arglist[sv.NORMALZ] = float(normal[2])
            if source is not None:
                arglist[sv.SLICESOURCE] = SliceSource(source)
            if mode != ExtractMode.SingleZone:
                arglist[sv.EXTRACTMODE] = mode
            arglist[sv.COPYCELLCENTEREDVALUES] = copy_cell_centers
            if assign_strand_ids is not None:
                arglist[sv.AUTOSTRANDTRANSIENTDATA] = bool(assign_strand_ids)
            if transient_mode != TransientOperationMode.SingleSolutionTime:
                arglist[sv.TRANSIENTOPERATIONMODE] = transient_mode
            if not _tecutil.CreateSliceZoneFromPlneX(arglist):
                raise TecplotSystemError()
            if dataset.num_zones == nzones:
                raise TecplotLogicError('No zones found when extracting slice')

        if (
            mode == ExtractMode.SingleZone and
            transient_mode == TransientOperationMode.SingleSolutionTime
        ):
            return dataset.zone(nzones)
        else:
            return (dataset.zone(i) for i in range(nzones, dataset.num_zones))


@tecutil.lock()
def extract_connected_regions(*zones, **kwargs):
    """Create new zones from regions of connected cells.

    Parameters:
        *zones (`Zones`_, required): Source zones from which to extract
            connected regions. All source zones must be finite-element
            zones, either classic FE or polygonal/polyhedral.

    Keyword Arguments:
        assign_strand_ids (`bool`, optional): Automatically assign strand IDs
            to the zones extracted from transient sources.  If True the
            resulting zones will be all be assigned to the same newly created
            strand id. (default: `True`)
        frame (`Frame`, optional): A `Frame` that holds the `Dataset` to
            operate on which must match *dataset* if given. (default: currently
            active `Frame`)
        dataset (`Dataset`, optional): The `Dataset` to operate on which must
            be attached to *frame* if given. (default: currently active
            `Dataset`)

    Returns:
        A `list` of the extracted `Zones <data_access>`.

    .. versionadded:: 2020.2
        Extracting connected regions requires Tecplot 360 2020 R2 or later.
    """
    if __debug__:
        if version.sdk_version_info < (2020, 2):
            msg = 'Extracting connected regions not supported.'
            raise TecplotOutOfDateEngineError((2020, 2), msg)

    if not zones:
        msg = 'extract_connected_regions(*zones) requires at least one zone'
        raise TecplotLogicError(msg)
    assign_strand_ids = kwargs.get('assign_strand_ids', True)
    frame = kwargs.get('frame', None)
    dataset = kwargs.get('dataset', None)

    if dataset is None:
        if frame is None:
            frame = layout.active_frame()
        dataset = frame.dataset
    elif frame is None:
        frame = dataset.frame

    if __debug__:
        if not frame.has_dataset:
            msg = 'The specified frame (or active frame if no frame is ' + \
                  'specified) must have a data set.'
            raise TecplotLogicError(msg)

    nzones = dataset.num_zones

    zone_tuple = tecutil.flatten_args(*zones)
    with frame.activated():
        with tecutil.ArgList() as arglist, \
            tecutil.IndexSet(zone_tuple) as zone_set:
            arglist[sv.SOURCEZONES] = zone_set
            arglist[sv.FRAME] = frame.uid
            arglist[sv.AUTOSTRANDTRANSIENTDATA] = assign_strand_ids
            if not _tecutil.ExtractConnectedRegionsX(arglist):
                raise TecplotSystemError()
        return [dataset.zone(i) for i in range(nzones, dataset.num_zones)]


@tecutil.lock()
def triangulate(*zones, **kwargs):
    """Create a new zone by forming triangles from points in 2D zones.

    Arguments:
        *zones (`Zones`_): Set of 2-dimensional source zones to triangulate.

    Keyword Arguments:
        boundary_zones (`list` of :math:`I`-Ordered `Zones`_, optional): Set
            of :math:`I`-ordered zones that define the boundaries across which
            no triangles can be created. (default: `None`)
        include_boundary_points (`bool`, optional): If `True`, boundary points
            will be used to create triangles. (default: `False`)
        keep_factor (`float` in the range [0.0, 0.5], optional): The smaller
            the number, the more likely it will be that highly obtuse triangles
            will be created opening toward the outside of the triangulated
            zone.
        plot (`Cartesian2DFieldPlot`, optional): The plot defining the
            :math:`(x, y)` variables in the dataset. If not set, the active
            plot will be used which must be of type `Cartesian2DFieldPlot`.

    Returns:
        `ClassicFEZone`: The resulting triangulated zone.

    The active plot or the plot specified must be of type
    `Cartesian2DFieldPlot` and the boundary zones, if supplied, may only be
    :math:`I`-ordered zones. This example creates a new zone by triangulating
    data points from two other `Zones`_::

        >>> zone0 = dataset.zone('Zone 0')
        >>> zone1 = dataset.zone('Zone 1')
        >>> new_zone = tp.data.extract.triangulate(zone0, zone1)
    """
    boundary_zones = kwargs.get('boundary_zones', None)
    include_boundary_points = bool(kwargs.get('include_boundary_points', False))
    keep_factor = float(kwargs.get('keep_factor', 0.25))
    plot = kwargs.get('plot', None)
    if not plot:
        plot = layout.active_frame().plot()

    with plot.activated():
        zones = tecutil.flatten_args(*zones)
        dataset = zones[0].dataset
        num_zones = dataset.num_zones
        with tecutil.optional(tecutil.IndexSet, zones) as zones:
            with tecutil.optional(tecutil.IndexSet, boundary_zones) as bzones:
                res = _tecutil.Triangulate(zones, bool(bzones), bzones,
                                           include_boundary_points, keep_factor)
                success, num_coincident_points = res
                if not success:
                    raise TecplotSystemError()
                return dataset.zone(num_zones)
