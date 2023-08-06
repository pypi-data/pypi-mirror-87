from builtins import int

from collections.abc import Iterable
from contextlib import contextmanager

from six import string_types

from ..tecutil import _tecutil
from ..constant import *
from ..exception import *
from .. import layout, tecutil
from ..tecutil import IndexSet, Index, flatten_args, sv, optional


@tecutil.lock()
def execute_equation(equation, zones=None, i_range=None, j_range=None,
                     k_range=None, value_location=None, variable_data_type=None,
                     ignore_divide_by_zero=None):
    """The execute_equation function operates on a data set within the
    |Tecplot Engine| using FORTRAN-like equations.

    Parameters:
        equation (`str`): String containing the equation.
            Multiple equations can be processed by separating each equation
            with a newline. See Section 20 - 1 "Data Alteration through
            Equations" in the |Tecplot User's Manual| for more information on
            using equations. Iterable container of `Zone <data_access>` objects
            to operate on. May be a list, set, tuple, or any iterable
            container. If `None`, the equation will be applied to all zones.

            .. note:: In the equation string, variable names should be enclosed
                in curly braces. For example, '{X} = {X} + 1'

        zones: (Iterable container of `Zone <data_access>` objects, optional):
            Iterable container of `Zone <data_access>` objects to operate on.
            May be a list, set, tuple, or any iterable container. If `None`,
            the equation will be applied to all zones.
        i_range (`tuple` of `integers <int>`, optional):
            Tuple of integers for I:  (min, max, step). If `None`, then the
            equation will operate on the entire range.
            Not used for finite element nodal data.
        j_range (`tuple` of `integers <int>`, optional):
            Tuple of integers for J:  (min, max, step). If `None`, then the
            equation will operate on the entire range.
            Not used for finite element nodal data.
        k_range (`tuple` of `integers <int>`, optional):
            Tuple of integers for K:  (min, max, step). If `None`, then the
            equation will operate on the entire range.
            Not used for finite element nodal data.
        value_location (`ValueLocation`, optional):
            Variable `ValueLocation` for the variable on the left hand side.
            This is used only if this variable is being created for the first
            time.
            If `None`, |Tecplot Engine| will choose the location for you.
        variable_data_type (`FieldDataType`, optional):
            Data type for the variable on the left hand side.
            This is used only if this variable is being created for the first
            time.
            If `None`, |Tecplot Engine| will choose the type for you.
        ignore_divide_by_zero (`bool`, optional):
            `bool` value which instructs |Tecplot Engine| to ignore
            divide by zero errors. The result is clamped
            such that 0/0 is clamped to zero and (+/-N)/0
            where N != 0 clamps to +/-maximum value for the given type.

    .. warning:: Zero-based Indexing

        It is important to know that all indexing in |PyTecplot| scripts are
        zero-based. This is a departure from the macro language which is
        one-based. This is to keep with the expectations when working in the
        python language. However, |PyTecplot| does not modify strings that are
        passed to the |Tecplot Engine|. This means that one-based indexing
        should be used when running macro commands from python or when using
        `execute_equation() <tecplot.data.operate.execute_equation>`.

    Add one to variable 'X' for zones 'Rectangular' and 'Circular' for every
    data point:

    >>> dataset = tecplot.active_frame().dataset
    >>> execute_equation('{X} = {X} + 1', zones=[dataset.zone('Rectangular'),
    >>>                  dataset.zone('Circular')])

    Create a new, double precision variable called DIST:

    >>> execute_equation('{DIST} = SQRT({X}**2 + {Y}**2)',
    ...                  variable_data_type=FieldDataType.Double)

    Set a variable called **P** to zero along the boundary of an IJ-ordered
    zone:

    >>> execute_equation('{P} = 0', i_range=(0, -1, 0), j_range=(0, -1, 0))

    Using 1-based indexing in equations and 0-based indexing in parameters.
    Zone 4 is subtracted from zone 3 and the result is placed in zone 2:

    >>> execute_equation('{T} = {T}[3]-{T}[4]', zones=[ds.zone(1)])
    """
    if __debug__:
        if not isinstance(equation, string_types):
            raise TecplotTypeError('Equation must be a string')
        elif len(equation) == 0:
            raise TecplotValueError('Equation can not be empty')
        if not isinstance(value_location, (ValueLocation, type(None))):
            msg = 'value_location must be a ValueLocation'
            raise TecplotTypeError(msg)
        if not isinstance(variable_data_type, (FieldDataType, type(None))):
            msg = 'variable_data_type must be a FieldDataType'
            raise TecplotTypeError(msg)
        if not isinstance(ignore_divide_by_zero, (bool, type(None))):
            raise TecplotTypeError('ignore_divide_by_zero must be a bool')

        # Check that all zones belong to the active dataset
        # (which is currently the only dataset option available)
        if zones:
            try:
                current_dataset = layout.active_frame().dataset
                parent_ids = {U.dataset.uid for U in zones} if isinstance(
                    zones, Iterable) else {zones.dataset.uid}

                if {current_dataset.uid} != parent_ids:
                    raise TecplotValueError(
                        'All zones must have the same parent dataset')
            except AttributeError:
                pass  # integer indices do not care or know about parent dataset

    with tecutil.ArgList() as arglist:
        arglist[sv.EQUATION] = equation
        with optional(IndexSet, zones) as zoneset:
            arglist[sv.ZONESET] = zoneset

            for dim, rng in zip(['I', 'J', 'K'], [i_range, j_range, k_range]):
                if rng is not None:
                    rng = tecutil.IndexRange(*rng)
                    if rng.min is not None:
                        arglist[dim + 'MIN'] = Index(rng.min)
                    if rng.max is not None:
                        arglist[dim + 'MAX'] = Index(rng.max)
                    if rng.step is not None:
                        step = int(rng.step)
                        if step > 0:
                            arglist[dim + 'SKIP'] = step
                        elif step < 0:
                            msg = 'Negative step not supported.'
                            raise TecplotLogicError(msg)

            arglist[sv.VALUELOCATION] = value_location
            arglist[sv.VARDATATYPE] = variable_data_type
            arglist[sv.IGNOREDIVIDEBYZERO] = ignore_divide_by_zero

            if not _tecutil.DataAlterX(arglist):
                raise TecplotSystemError()


@contextmanager
def _interpolate_process_args(dest_zone, src_zones, variables, plot):
    if plot is None:
        plot = layout.active_frame().plot()
    if isinstance(dest_zone, int):
        dest_zone = plot.frame.dataset.zone(dest_zone)
    if not isinstance(src_zones, (Iterable, type(None))):
        src_zones = [src_zones]
    if not isinstance(variables, (Iterable, type(None))):
        variables = [variables]

    if __debug__:
        if plot.frame.dataset != dest_zone.dataset:
            msg = 'Plot and destination zone do not share the same dataset.'
            raise TecplotLogicError(msg)
        if src_zones is not None:
            def is_invalid_zone(z):
                if isinstance(z, int):
                    return z >= plot.frame.dataset.num_zones
                else:
                    return plot.frame.dataset != z.dataset
            if any(map(is_invalid_zone, src_zones)):
                msg = 'Source zones are not part of the same dataset.'
                raise TecplotLogicError(msg)
        if variables is not None:
            def is_invalid_variable(v):
                if isinstance(v, int):
                    return v >= plot.frame.dataset.num_variables
                else:
                    return plot.frame.dataset != v.dataset
            if any(map(is_invalid_variable, variables)):
                msg = 'Variables are not part of the same dataset.'
                raise TecplotLogicError(msg)

    with plot.activated():
        with optional(IndexSet, src_zones) as src:
            with optional(IndexSet, variables) as varset:
                dest = dest_zone.index + 1
                yield src, dest, varset


@tecutil.lock()
def interpolate_linear(destination_zone, source_zones=None, variables=None,
                       fill_value=None, plot=None):
    """Linear interpolation onto a destination zone.

    Parameters:
        destination_zone (`zone <data_access>` or `int`): The
            destination zone (or zone index) for interpolation.
        source_zones (`zones <data_access>` or `integers <int>`, optional):
            Zones (or zone indices) used to obtain the field values for
            interpolation. By default, all zones except the *destination_zone*
            will be used. All source zones must be FE-Tetra, FE-Brick or be
            IJK-ordered when doing linear interpolation in 3D.
        variables (`variables <Variable>` or `integers <int>`, optional):
            Variables (or variable indices) to interpolate. By default, all
            variables except those assigned to the axes will be used and is in
            general dependent on the active plot type of the frame.
        fill_value (`float`, optional): Constant value to which all points
            outside the data field are set. By default, the values outside
            the field are preserved.
        plot (:ref:`plot`, optional): The plot to use when interpolating which
            determines the dimensionality and spatial variables. By default,
            the active plot on the active frame will be used.

    .. note:: Cartesian 2D and 3D plots only.

        This interpolation method relies on the coordinates, :math:`(x, y)` for
        2D or :math:`(x, y, z)` for 3D, set for the active (or given) plot
        which must be either Cartesian2D or Cartesian3D.

    The following example loads a 2D dataset and uses interpolation to merge
    information from two independent zones:

    .. code-block:: python

        import os
        import numpy as np
        import tecplot as tp
        from tecplot.constant import *

        # Use interpolation to merge information from two independent zones
        examples_dir = tp.session.tecplot_examples_directory()
        datafile = os.path.join(examples_dir, 'SimpleData', 'RainierElevation.plt')
        dataset = tp.data.load_tecplot(datafile)
        # Get list of source zones to use later
        srczones = list(dataset.zones())

        fr = tp.active_frame()
        plot = fr.plot(PlotType.Cartesian2D)
        plot.activate()
        plot.show_contour = True
        plot.show_edge = True

        # Show two section of the plot independently
        plot.contour(0).legend.show = False
        plot.contour(1).legend.show = False
        plot.contour(1).colormap_name = 'Diverging - Blue/Red'
        for scrzone in srczones:
            plot.fieldmap(scrzone).edge.line_thickness = 0.4
        plot.fieldmap(0).contour.flood_contour_group = plot.contour(1)

        # export image of original data
        tp.export.save_png('interpolate_2d_source.png', 600, supersample=3)

        # use the first zone as the source, and get the range of (x, y)
        xvar = plot.axes.x_axis.variable
        yvar = plot.axes.y_axis.variable
        ymin, xmin = 99999,99999
        ymax, xmax = -99999,-99999
        for scrzone in srczones:
            curxmin, curxmax = scrzone.values(xvar.index).minmax()
            curymin, curymax = scrzone.values(yvar.index).minmax()
            ymin = min(curymin,ymin)
            ymax = max(curymax,ymax)
            xmin = min(curxmin,xmin)
            xmax = max(curxmax,xmax)

        # create new zone with a coarse grid
        # onto which we will interpolate from the source zone
        xpoints = 40
        ypoints = 40
        newzone = dataset.add_ordered_zone('Interpolated', (xpoints, ypoints))

        # setup the (x, y) positions of the new grid
        xx = np.linspace(xmin, xmax, xpoints)
        yy = np.linspace(ymin, ymax, ypoints)
        YY, XX = np.meshgrid(yy, xx, indexing='ij')
        newzone.values(xvar.index)[:] = XX.ravel()
        newzone.values(yvar.index)[:] = YY.ravel()

        # perform linear interpolation from the source to the new zone
        tp.data.operate.interpolate_linear(newzone, source_zones=srczones)

        # show the new zone's data, hide the source
        plot.fieldmap(newzone).show = True
        plot.fieldmap(newzone).contour.show = True
        plot.fieldmap(newzone).contour.flood_contour_group = plot.contour(0)
        plot.fieldmap(newzone).edge.show = True
        plot.fieldmap(newzone).edge.line_thickness = .4
        plot.fieldmap(newzone).edge.color = Color.Orange

        for scrzone in srczones:
            plot.fieldmap(scrzone).show = False

        # export image of interpolated data
        tp.export.save_png('interpolate_linear_2d_dest.png', 600, supersample=3)

    .. figure:: /_static/images/interpolate_2d_source.png
        :width: 300px
        :figwidth: 300px

        Source data.

    .. figure:: /_static/images/interpolate_linear_2d_dest.png
        :width: 300px
        :figwidth: 300px

        Interpolated data.

    """
    with _interpolate_process_args(destination_zone, source_zones, variables,
                                   plot) as (src, dest, varset):
        if fill_value is None:
            interp_const = 0.0
            interp_mode = LinearInterpMode.DontChange
        else:
            interp_const = float(fill_value)
            interp_mode = LinearInterpMode.SetToConst
        if not _tecutil.LinearInterpolate(src, dest, varset, interp_const,
                                          interp_mode.value):
            raise TecplotSystemError()


@tecutil.lock()
def interpolate_kriging(destination_zone, source_zones=None, variables=None,
                        krig_range=0.3, zero_value=0.0, drift=Drift.Linear,
                        point_selection=PtSelection.OctantN, num_points=8,
                        plot=None):
    """Kriging interpolation onto a destination zone.

    Parameters:
        destination_zone (`zone <data_access>` or `int`): The
            destination zone (or zone index) for interpolation.
        source_zones (`zones <data_access>` or `integers <int>`, optional):
            Zones (or zone indices) used to obtain the field values for
            interpolation. By default, all zones except the *destination_zone*
            will be used. All source zones must be FE-Tetra, FE-Brick or
            IJK-ordered when doing kriging interpolation in 3D.
        variables (`variables <Variable>` or `integers <int>`, optional):
            Variables (or variable indices) to interpolate. By default, all
            variables except those assigned to the axes will be used and is in
            general dependent on the active plot type of the frame.
        krig_range (`float`, optional): Distance beyond which source points
            become insignificant. Must be between zero and one, inclusive.
            (default: 0.3)
        zero_value (`float`, optional): Semi-variance at each source data point
            on a normalized scale from zero to one. (default: 0.0)
        drift (`Drift`, optional): Overall trend for the data. Possible values:
            `Drift.None_` no trend, `Drift.Linear` (default) linear trend,
            `Drift.Quad` quadratic trend.
        point_selection (`PtSelection`, optional): Method for determining which
            source points to consider for each destination data point. Possible
            values: `PtSelection.OctantN` (default) closest *num_points*
            selected by coordinate-system octants, `PtSelection.NearestN`
            closest *num_points* to the destination point, `PtSelection.All`
            all points in the source zone.
        num_points (`int`, optional): Number of source points to
            consider for each destination data point if *point_selection* is
            `PtSelection.OctantN` or `PtSelection.NearestN`. (default: 8)
        plot (:ref:`plot`, optional): The plot to use when interpolating which
            determines the dimensionality and spatial variables. By default,
            the active plot on the active frame will be used.

    .. note:: Cartesian 2D and 3D plots only.

        This interpolation method relies on the coordinates, :math:`(x, y)` for
        2D or :math:`(x, y, z)` for 3D, set for the active (or given) plot
        which must be either Cartesian2D or Cartesian3D.

    The following example loads a 2D dataset and interpolates the first zone to
    a new one with a larger grid spacing:

    .. code-block:: python
        :emphasize-lines: 58-59

        import os
        import numpy as np
        import tecplot as tp
        from tecplot.constant import *

        # Use interpolation to merge information from two independent zones
        examples_dir = tp.session.tecplot_examples_directory()
        datafile = os.path.join(examples_dir, 'SimpleData',
                                'RainierElevation.plt')
        dataset = tp.data.load_tecplot(datafile)
        # Get list of source zones to use later
        srczones = list(dataset.zones())

        fr = tp.active_frame()
        plot = fr.plot(PlotType.Cartesian2D)
        plot.activate()
        plot.show_contour = True
        plot.show_edge = True

        # Show two section of the plot independently
        plot.contour(0).legend.show = False
        plot.contour(1).legend.show = False
        plot.contour(1).colormap_name = 'Diverging - Blue/Red'
        for scrzone in srczones:
            plot.fieldmap(scrzone).edge.line_thickness = 0.4
        plot.fieldmap(0).contour.flood_contour_group = plot.contour(1)

        # export image of original data
        tp.export.save_png('interpolate_2d_source.png', 600, supersample=3)

        # use the first zone as the source, and get the range of (x, y)
        xvar = plot.axes.x_axis.variable
        yvar = plot.axes.y_axis.variable
        ymin, xmin = 99999,99999
        ymax, xmax = -99999,-99999
        for scrzone in srczones:
            curxmin, curxmax = scrzone.values(xvar.index).minmax()
            curymin, curymax = scrzone.values(yvar.index).minmax()
            ymin = min(curymin,ymin)
            ymax = max(curymax,ymax)
            xmin = min(curxmin,xmin)
            xmax = max(curxmax,xmax)

        # create new zone with a coarse grid
        # onto which we will interpolate from the source zone
        xpoints = 20
        ypoints = 20
        newzone = dataset.add_ordered_zone('Interpolated', (xpoints, ypoints))

        # setup the (x, y) positions of the new grid
        xx = np.linspace(xmin, xmax, xpoints)
        yy = np.linspace(ymin, ymax, ypoints)
        YY, XX = np.meshgrid(yy, xx, indexing='ij')
        newzone.values(xvar.index)[:] = XX.ravel()
        newzone.values(yvar.index)[:] = YY.ravel()

        # perform linear interpolation from the source to the new zone
        tp.data.operate.interpolate_kriging(newzone, source_zones=srczones,
                                            drift=Drift.None_, num_points=1)

        # show the new zone's data, hide the source
        plot.fieldmap(newzone).show = True
        plot.fieldmap(newzone).contour.show = True
        plot.fieldmap(newzone).contour.flood_contour_group = plot.contour(0)
        plot.fieldmap(newzone).edge.show = True
        plot.fieldmap(newzone).edge.line_thickness = .4
        plot.fieldmap(newzone).edge.color = Color.Orange

        for scrzone in srczones:
            plot.fieldmap(scrzone).show = False

        # export image of interpolated data
        tp.export.save_png('interpolate_krig_2d_dest.png', 600, supersample=3)

    .. figure:: /_static/images/interpolate_2d_source.png
        :width: 300px
        :figwidth: 300px

        Source data.

    .. figure:: /_static/images/interpolate_krig_2d_dest.png
        :width: 300px
        :figwidth: 300px

        Interpolated data.
    """
    with _interpolate_process_args(destination_zone, source_zones, variables,
                                   plot) as (src, dest, varset):
        if not _tecutil.Krig(
            src, dest, varset, krig_range, zero_value, Drift(drift).value,
                PtSelection(point_selection).value, num_points):
            raise TecplotSystemError()


@tecutil.lock()
def interpolate_inverse_distance(destination_zone, source_zones=None,
                                 variables=None, exponent=3.5, min_radius=0.0,
                                 point_selection=PtSelection.OctantN,
                                 num_points=8, plot=None):
    """Inverse-Distance interpolation onto a destination zone.

    Parameters:
        destination_zone (`zone <data_access>` or `int`): The
            destination zone (or zone index) for interpolation.
        source_zones (`zones <data_access>` or `integers <int>`, optional):
            Zones (or zone indices) used to obtain the field values for
            interpolation. By default, all zones except the *destination_zone*
            will be used. All source zones must be FE-Tetra, FE-Brick or be
            IJK-ordered when doing linear interpolation in 3D.
        variables (`variables <Variable>` or `integers <int>`, optional):
            Variables (or variable indices) to interpolate. By default, all
            variables except those assigned to the axes will be used and is in
            general dependent on the active plot type of the frame.
        exponent (`float`, optional): Exponent for the inverse-distance
            weighting. (default: 3.5)
        min_radius (`float`, optional): Minimum distance used for the
            inverse-distance weighting. (default: 0.0)
        point_selection (`PtSelection`, optional): Method for determining which
            source points to consider for each destination data point. Possible
            values: `PtSelection.OctantN` (default) closest *num_points*
            selected by coordinate-system octants, `PtSelection.NearestN`
            closest *num_points* to the destination point, `PtSelection.All`
            all points in the source zone.
        num_points (`int`, optional): Number of source points to
            consider for each destination data point if *point_selection* is
            `PtSelection.OctantN` or `PtSelection.NearestN`. (default: 8)
        plot (:ref:`plot`, optional): The plot to use when interpolating which
            determines the dimensionality and spatial variables. By default,
            the active plot on the active frame will be used.

    .. note:: Cartesian 2D and 3D plots only.

        This interpolation method relies on the coordinates, :math:`(x, y)` for
        2D or :math:`(x, y, z)` for 3D, set for the active (or given) plot
        which must be either Cartesian2D or Cartesian3D.

    The following example loads a 2D dataset and interpolates the first zone to
    a new one with a larger grid spacing:

    .. code-block:: python
        :emphasize-lines: 57

        import os
        import numpy as np
        import tecplot as tp
        from tecplot.constant import *

        # Use interpolation to merge information from two independent zones
        examples_dir = tp.session.tecplot_examples_directory()
        datafile = os.path.join(examples_dir, 'SimpleData', 'RainierElevation.plt')
        dataset = tp.data.load_tecplot(datafile)
        # Get list of source zones to use later
        srczones = list(dataset.zones())

        fr = tp.active_frame()
        plot = fr.plot(PlotType.Cartesian2D)
        plot.activate()
        plot.show_contour = True
        plot.show_edge = True

        # Show two section of the plot independently
        plot.contour(0).legend.show = False
        plot.contour(1).legend.show = False
        plot.contour(1).colormap_name = 'Diverging - Blue/Red'
        for scrzone in srczones:
            plot.fieldmap(scrzone).edge.line_thickness = 0.4
        plot.fieldmap(0).contour.flood_contour_group = plot.contour(1)

        # export image of original data
        tp.export.save_png('interpolate_2d_source.png', 600, supersample=3)

        # use the first zone as the source, and get the range of (x, y)
        xvar = plot.axes.x_axis.variable
        yvar = plot.axes.y_axis.variable
        ymin, xmin = 99999,99999
        ymax, xmax = -99999,-99999
        for scrzone in srczones:
            curxmin, curxmax = scrzone.values(xvar.index).minmax()
            curymin, curymax = scrzone.values(yvar.index).minmax()
            ymin = min(curymin,ymin)
            ymax = max(curymax,ymax)
            xmin = min(curxmin,xmin)
            xmax = max(curxmax,xmax)

        # create new zone with a coarse grid
        # onto which we will interpolate from the source zone
        xpoints = 40
        ypoints = 40
        newzone = dataset.add_ordered_zone('Interpolated', (xpoints, ypoints))

        # setup the (x, y) positions of the new grid
        xx = np.linspace(xmin, xmax, xpoints)
        yy = np.linspace(ymin, ymax, ypoints)
        YY, XX = np.meshgrid(yy, xx, indexing='ij')
        newzone.values(xvar.index)[:] = XX.ravel()
        newzone.values(yvar.index)[:] = YY.ravel()

        # perform linear interpolation from the source to the new zone
        tp.data.operate.interpolate_inverse_distance(newzone, source_zones=srczones)

        # show the new zone's data, hide the source
        plot.fieldmap(newzone).show = True
        plot.fieldmap(newzone).contour.show = True
        plot.fieldmap(newzone).contour.flood_contour_group = plot.contour(0)
        plot.fieldmap(newzone).edge.show = True
        plot.fieldmap(newzone).edge.line_thickness = .4
        plot.fieldmap(newzone).edge.color = Color.Orange

        for scrzone in srczones:
            plot.fieldmap(scrzone).show = False

        # export image of interpolated data
        tp.export.save_png('interpolate_invdst_2d_dest.png', 600, supersample=3)

    .. figure:: /_static/images/interpolate_2d_source.png
        :width: 300px
        :figwidth: 300px

        Source data.

    .. figure:: /_static/images/interpolate_invdst_2d_dest.png
        :width: 300px
        :figwidth: 300px

        Interpolated data.
    """
    with _interpolate_process_args(destination_zone, source_zones, variables,
                                   plot) as (src, dest, varset):
        if not _tecutil.InverseDistInterpolation(
            src, dest, varset, exponent, min_radius,
                PtSelection(point_selection).value, num_points):
            raise TecplotSystemError()


@tecutil.lock()
def smooth(array, num_passes=1, weight=0.8,
           boundary_condition=BoundaryCondition.Fixed, frame=None):
    """Smooth a field data `Array` in the dataset.

    Parameters:
        array (`Array`): The field data to smooth.
        num_passes (`int`, optional): The number of smoothing passes to
            perform. (default: 1)
        weight (`float`, optional):  The relaxation factor for each pass of
            smoothing. Must be a number between zero and one exclusively.
            Higher numbers indicate a greater smoothing effect. (default: 0.8)
        boundary_condition (`BoundaryCondition`, optional): The boundary
            condition by which to smooth. Possible values are
            `BoundaryCondition.Fixed` (default),
            `BoundaryCondition.ZeroGradient` and `BoundaryCondition.Zero2nd`.
        frame (`Frame`, optional): The `Frame` that specifies the spatial
            variables to smooth over via the active plot. By default, the frame
            associated with the input `Array` object will be used.

    The data will be smoothed over the spatial variables set by the plot and is
    dependent on the active plot type of the associated `Frame` (`Cartesian2D`
    or `Cartesian3D`). Example usage::

        >>> tp.data.operate.smooth(dataset.zone('Zone').values('Pressure'))
    """
    frame = frame or array.zone.dataset.frame
    with frame.activated():
        if not _tecutil.Smooth(array.zone.index + 1, array.variable.index + 1,
                               int(num_passes), float(weight),
                               BoundaryCondition(boundary_condition).value):
            raise TecplotSystemError()


def _dataset(*objlists):
    for objs in objlists:
        if objs:
            for obj in objs:
                if obj and hasattr(obj, 'dataset'):
                    return obj.dataset
    return layout.active_frame().dataset


@tecutil.lock()
def transform_polar_to_rectangular(r, theta, x=None, y=None,
                                   angle_units=AngleUnits.Radians, zones=None):
    """Transform all points from polar to rectangular coordinates.

    Parameters:
        r (`Variable`): The radial input variable.
        theta (`Variable`): The angular input variable in **angle_units** from
            the :math:`x`-axis.
        x (`Variable`, optional): The rectangular output :math:`x` variable. By
            default, a new variable will be created. Both **x** and **y** must
            be specified together as either existing variables or as `None`.
        y (`Variable`, optional): The rectangular output :math:`y` variable. By
            default, a new variable will be created. Both **x** and **y** must
            be specified together as either existing variables or as `None`.
        angle_units (`AngleUnits`, optional): The units of the angular
            variables. This may be either `AngleUnits.Radians` (default) or
            `AngleUnits.Degrees`.
        zones (`list` of `Zones <data_access>`, optional): Specific zones to
            transform. By default, all zones are transformed.

    This example will create two new variables in the dataset corresponding to
    the :math:`x` and :math:`y` equivalents of the :math:`r` and :math:`theta`
    variables::

        >>> dataset = tp.active_frame().dataset
        >>> r = dataset.variable('R (m)')
        >>> theta = dataset.variable('Theta (rad)')
        >>> tp.data.operate.transform_polar_to_rectangular(r, theta)
        >>> x, y = dataset.variable(-2), dataset.variable(-1)

    .. warning:: **Source variables must have the same location as the
        destination variables.**

        The variables involved with this transformation must all be either
        nodal or cell-centered.
    """
    dataset = _dataset((r, theta, x, y), zones)
    with tecutil.ArgList() as arglist:
        arglist[sv.TRANSFORMATION] = Transform.PolarToRect
        arglist[sv.RVAR] = dataset.variable(r).index
        arglist[sv.THETAVAR] = dataset.variable(theta).index
        if all(v is None for v in (x, y)):
            arglist[sv.CREATENEWVARIABLES] = True
            arglist[sv.XVAR] = 1
            arglist[sv.YVAR] = 1
        elif all(v is not None for v in (x, y)):
            arglist[sv.CREATENEWVARIABLES] = False
            arglist[sv.XVAR] = dataset.variable(x).index
            arglist[sv.YVAR] = dataset.variable(y).index
        else:
            msg = 'All destination variables must be specified or None.'
            raise TecplotLogicError(msg)
        arglist[sv.ANGLESPEC] = AngleUnits(angle_units)
        with tecutil.optional(tecutil.IndexSet, zones) as zones:
            arglist[sv.ZONELIST] = zones
            if not _tecutil.TransformCoordinatesX(arglist):
                raise TecplotSystemError()


@tecutil.lock()
def transform_rectangular_to_polar(x, y, r=None, theta=None,
                                   angle_units=AngleUnits.Radians, zones=None):
    """Transform all points from rectangular to polar coordinates.

    Parameters:
        x (`Variable`): The rectangular input :math:`x` variable.
        y (`Variable`): The rectangular input :math:`y` variable.
        r (`Variable`, optional): The radial output :math:`r` variable. By
            default, a new variable will be created. Both **r** and **theta**
            must be specified together as either existing variables or as
            `None`.
        theta (`Variable`, optional): The angular output :math:`theta`
            variable. By default, a new variable will be created. Both **r**
            and **theta** must be specified together as either existing
            variables or as `None`.
        angle_units (`AngleUnits`, optional): The units of the angular
            variables. This may be either `AngleUnits.Radians` (default) or
            `AngleUnits.Degrees`.
        zones (`list` of `Zones <data_access>`, optional): Specific zones to
            transform. By default, all zones are transformed.

    This example will create two new variables in the dataset corresponding to
    the :math:`r` and :math:`theta` equivalents of the :math:`x` and :math:`y`
    variables::

        >>> dataset = tp.active_frame().dataset
        >>> x = dataset.variable('X (m)')
        >>> y = dataset.variable('Y (m)')
        >>> tp.data.operate.transform_rectangular_to_polar(x, y)
        >>> theta, r = dataset.variable(-2), dataset.variable(-1)

    .. warning:: **Source variables must have the same location as the
        destination variables.**

        The variables involved with this transformation must all be either
        nodal or cell-centered.
    """
    dataset = _dataset((x, y, r, theta), zones)
    with tecutil.ArgList() as arglist:
        arglist[sv.TRANSFORMATION] = Transform.RectToPolar
        # (x, y) are switched in the SDK for this polar transformation
        arglist[sv.XVAR] = dataset.variable(y).index
        arglist[sv.YVAR] = dataset.variable(x).index
        if all(v is None for v in (r, theta)):
            arglist[sv.CREATENEWVARIABLES] = True
            arglist[sv.RVAR] = 1
            arglist[sv.THETAVAR] = 1
        elif all(v is not None for v in (r, theta)):
            arglist[sv.CREATENEWVARIABLES] = False
            arglist[sv.RVAR] = dataset.variable(r).index
            arglist[sv.THETAVAR] = dataset.variable(theta).index
        else:
            msg = 'All destination variables must be specified or None.'
            raise TecplotLogicError(msg)
        arglist[sv.ANGLESPEC] = AngleUnits(angle_units)
        with tecutil.optional(tecutil.IndexSet, zones) as zones:
            arglist[sv.ZONELIST] = zones
            if not _tecutil.TransformCoordinatesX(arglist):
                raise TecplotSystemError()


@tecutil.lock()
def transform_spherical_to_rectangular(r, theta, psi, x=None, y=None, z=None,
                                   angle_units=AngleUnits.Radians, zones=None):
    """Transform all points from spherical to rectangular coordinates.

    Parameters:
        r (`Variable`): The radial input variable.
        theta (`Variable`): The angular input variable in **angle_units** from
            the :math:`x`-axis.
        psi (`Variable`): The angular input variable in **angle_units** from
            the :math:`z`-axis.
        x (`Variable`, optional): The rectangular output :math:`x` variable. By
            default, a new variable will be created. All of **x**, **y** and
            **z** must be specified together as either existing variables or as
            `None`.
        y (`Variable`, optional): The rectangular output :math:`y` variable. By
            default, a new variable will be created. All of **x**, **y** and
            **z** must be specified together as either existing variables or as
            `None`.
        z (`Variable`, optional): The rectangular output :math:`z` variable. By
            default, a new variable will be created. All of **x**, **y** and
            **z** must be specified together as either existing variables or as
            `None`.
        angle_units (`AngleUnits`, optional): The units of the angular
            variables. This may be either `AngleUnits.Radians` (default) or
            `AngleUnits.Degrees`.
        zones (`list` of `Zones <data_access>`, optional): Specific zones to
            transform. By default, all zones are transformed.

    This example will create three new variables in the dataset corresponding
    to the :math:`(x, y, z)` equivalents of the :math:`(r, theta, psi)`
    variables::

        >>> dataset = tp.active_frame().dataset
        >>> r = dataset.variable('R (m)')
        >>> theta = dataset.variable('Theta (rad)')
        >>> psi = dataset.variable('Psi (rad)')
        >>> tp.data.operate.transform_spherical_to_rectangular(r, theta, psi)
        >>> x = dataset.variable(-3)
        >>> y = dataset.variable(-2)
        >>> z = dataset.variable(-1)

    .. warning:: **Source variables must have the same location as the
        destination variables.**

        The variables involved with this transformation must all be either
        nodal or cell-centered.
    """
    dataset = _dataset((r, theta, psi, x, y, z), zones)
    with tecutil.ArgList() as arglist:
        arglist[sv.TRANSFORMATION] = Transform.SphericalToRect
        arglist[sv.RVAR] = dataset.variable(r).index
        arglist[sv.THETAVAR] = dataset.variable(theta).index
        arglist[sv.PSIVAR] = dataset.variable(psi).index
        if all(v is None for v in (x, y, z)):
            arglist[sv.CREATENEWVARIABLES] = True
            arglist[sv.XVAR] = 1
            arglist[sv.YVAR] = 1
            arglist[sv.ZVAR] = 1
        elif all(v is not None for v in (x, y, z)):
            arglist[sv.CREATENEWVARIABLES] = False
            arglist[sv.XVAR] = dataset.variable(x).index
            arglist[sv.YVAR] = dataset.variable(y).index
            arglist[sv.ZVAR] = dataset.variable(z).index
        else:
            msg = 'All destination variables must be specified or None.'
            raise TecplotLogicError(msg)
        arglist[sv.ANGLESPEC] = AngleUnits(angle_units)
        with tecutil.optional(tecutil.IndexSet, zones) as zones:
            arglist[sv.ZONELIST] = zones
            if not _tecutil.TransformCoordinatesX(arglist):
                raise TecplotSystemError()


@tecutil.lock()
def transform_rectangular_to_spherical(x, y, z, r=None, theta=None, psi=None,
                                   angle_units=AngleUnits.Radians, zones=None):
    """Transform all points from rectangular to spherical coordinates.

    Parameters:
        x (`Variable`): The rectangular input :math:`x` variable.
        y (`Variable`): The rectangular input :math:`y` variable.
        z (`Variable`): The rectangular input :math:`z` variable.
        r (`Variable`, optional): The radial output :math:`r` variable. By
            default, a new variable will be created. All of **r**, **theta**
            and **psi** must be specified together as either existing variables
            or as `None`.
        theta (`Variable`, optional): The angular output :math:`theta` variable
            from the :math:`x`-axis. By default, a new variable will be
            created. All of **r**, **theta** and **psi** must be specified
            together as either existing variables or as `None`.
        psi (`Variable`, optional): The angular output :math:`psi` variable
            from the :math:`z`-axis. By default, a new variable will be
            created. All of **r**, **theta** and **psi** must be specified
            together as either existing variables or as `None`.
        angle_units (`AngleUnits`, optional): The units of the angular
            variables. This may be either `AngleUnits.Radians` (default) or
            `AngleUnits.Degrees`.
        zones (`list` of `Zones <data_access>`, optional): Specific zones to
            transform. By default, all zones are transformed.

    This example will create three new variables in the dataset corresponding
    to the :math:`(r, theta, psi)` equivalents of the :math:`(x, y, z)`
    variables::

        >>> dataset = tp.active_frame().dataset
        >>> x = dataset.variable('X (m)')
        >>> y = dataset.variable('Y (m)')
        >>> z = dataset.variable('Z (m)')
        >>> tp.data.operate.transform_rectangular_to_spherical(x, y, z)
        >>> theta = dataset.variable(-3)
        >>> r = dataset.variable(-2)
        >>> psi = dataset.variable(-1)

    .. warning:: **Source variables must have the same location as the
        destination variables.**

        The variables involved with this transformation must all be either
        nodal or cell-centered.
    """
    dataset = _dataset((x, y, z, r, theta, psi), zones)
    with tecutil.ArgList() as arglist:
        arglist[sv.TRANSFORMATION] = Transform.RectToSpherical
        arglist[sv.XVAR] = dataset.variable(x).index
        arglist[sv.YVAR] = dataset.variable(y).index
        arglist[sv.ZVAR] = dataset.variable(z).index
        if all(v is None for v in (r, theta, psi)):
            arglist[sv.CREATENEWVARIABLES] = True
            arglist[sv.RVAR] = 1
            arglist[sv.THETAVAR] = 1
            arglist[sv.PSIVAR] = 1
        elif all(v is not None for v in (r, theta, psi)):
            arglist[sv.CREATENEWVARIABLES] = False
            arglist[sv.RVAR] = dataset.variable(r).index
            arglist[sv.THETAVAR] = dataset.variable(theta).index
            arglist[sv.PSIVAR] = dataset.variable(psi).index
        else:
            msg = 'All destination variables must be specified or None.'
            raise TecplotLogicError(msg)
        arglist[sv.ANGLESPEC] = AngleUnits(angle_units)
        with tecutil.optional(tecutil.IndexSet, zones) as zones:
            arglist[sv.ZONELIST] = zones
            if not _tecutil.TransformCoordinatesX(arglist):
                raise TecplotSystemError()
