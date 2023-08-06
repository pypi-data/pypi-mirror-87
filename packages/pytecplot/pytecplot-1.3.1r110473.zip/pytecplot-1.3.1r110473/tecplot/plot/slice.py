from builtins import int, super

import itertools as it

from collections.abc import Iterable

from ..tecutil import _tecutil, sv
from ..constant import *
from ..exception import *
from .. import session, tecutil, version


class SliceMesh(session.SubStyle):
    """Mesh attributes of the slice group.

    .. code-block:: python
        :emphasize-lines: 12

        from os import path
        import tecplot as tp
        from tecplot.constant import SliceSurface, ContourType

        examples_dir = tp.session.tecplot_examples_directory()
        datafile = path.join(examples_dir, 'SimpleData', 'DuctFlow.plt')
        dataset = tp.data.load_tecplot(datafile)
        plot = tp.active_frame().plot()
        plot.show_slices = True
        plot.contour(0).variable = dataset.variable('U(M/S)')

        plot.slice(0).mesh.show = True

        # ensure consistent output between interactive (connected) and batch
        plot.contour(0).levels.reset_to_nice()

        tp.export.save_png('slice_mesh.png', 600, supersample=3)

    .. figure:: /_static/images/slice_mesh.png
        :width: 300px
        :figwidth: 300px
    """
    def __init__(self, slice_group):
        super().__init__(slice_group, sv.MESH)

    @property
    def show(self):
        """`bool`: Show mesh lines.

        Example usage::

            >>> plot.slice(0).mesh.show = True
        """
        return self._get_style(bool, sv.SHOW)

    @show.setter
    def show(self, value):
        self._set_style(bool(value), sv.SHOW)

    @property
    def color(self):
        """`Color` or `ContourGroup`: Slice mesh line Color.

        Slice mesh lines can be a solid color or be colored by a
        `ContourGroup` as obtained through the ``plot.contour`` property.

        Example usage::

            >>> plot.slice(0).mesh.show = True
            >>> plot.slice(0).mesh.color = Color.Green
        """
        return tecutil.color_spec(self._get_style(Color, sv.COLOR),
                                  self.parent.plot)

    @color.setter
    def color(self, value):
        self._set_style(tecutil.color_spec(value), sv.COLOR)

    @property
    def line_thickness(self):
        """`float`: Mesh line thickness.

        The mesh line thickness is specified as a percentage of the frame width.

        Example usage::

            >>> plot.slice(0).mesh.show = True
            >>> plot.slice(0).mesh.line_thickness = 0.8
        """
        return self._get_style(float, sv.LINETHICKNESS)

    @line_thickness.setter
    def line_thickness(self, value):
        self._set_style(float(value), sv.LINETHICKNESS)


class SliceShade(session.SubStyle):
    """Shade attributes of the slice group.

    Show shading on the slice when `SliceContour.show` has not been
    selected or is set to `ContourType.Lines`:

    .. code-block:: python
        :emphasize-lines: 11-14

        from os import path
        import tecplot as tp
        from tecplot.constant import Color

        examples_dir = tp.session.tecplot_examples_directory()
        datafile = path.join(examples_dir, 'SimpleData', 'Pyramid.plt')
        dataset = tp.data.load_tecplot(datafile)

        plot = tp.active_frame().plot()
        plot.show_slices = True
        plot.slice(0).contour.show = False
        shade = plot.slice(0).shade
        shade.show = True
        shade.color = Color.Red  # Slice will be colored solid red.
        tp.export.save_png('slice_shade.png', 600, supersample=3)

    .. figure:: /_static/images/slice_shade.png
        :width: 300px
        :figwidth: 300px
    """

    def __init__(self, slice_group):
        super().__init__(slice_group, sv.SHADE)

    @property
    def show(self):
        """`bool`: Show shade attributes.

        Example usage::

            >>> plot.slice(0).shade.show = True
        """
        return self._get_style(bool, sv.SHOW)

    @show.setter
    def show(self, value):
        self._set_style(bool(value), sv.SHOW)

    @property
    def color(self):
        """`Color`: Shade color.

        `Color.MultiColor` and `Color.RGBColor` coloring are not available.
        Use flooded contours for multi-color or RGB flooding

        Example usage::

            >>> plot.slice(0).shade.show = True
            >>> plot.slice(0).shade.color = Color.Blue
        """
        return self._get_style(Color, sv.COLOR)

    @color.setter
    def color(self, value):
        self._set_style(Color(value), sv.COLOR)

    @property
    def use_lighting_effect(self):
        """`bool`: Use lighting effect.

        When set to `True`, the lighting effect may be selected with the
        `SliceEffects.lighting_effect` attribute.

        .. note::
            Setting `SliceShade.use_lighting_effect` will also set
            the same value for `SliceContour.use_lighting_effect`,
            and vice-versa.

        Example usage::

            >>> plot.slice(0).shade.use_lighting_effect = True
            >>> plot.slice(0).effects.lighting_effect = LightingEffect.Paneled
        """
        return self._get_style(bool, sv.USELIGHTINGEFFECT)

    @use_lighting_effect.setter
    def use_lighting_effect(self, value):
        self._set_style(bool(value), sv.USELIGHTINGEFFECT)


class SliceEffects(session.SubStyle):
    """Slice effects for this slice.

    .. code-block:: python
        :emphasize-lines: 16-17

        from os import path
        import tecplot as tp

        examples_dir = tp.session.tecplot_examples_directory()
        datafile = path.join(examples_dir, 'SimpleData', 'DuctFlow.plt')
        dataset = tp.data.load_tecplot(datafile)

        plot = tp.active_frame().plot()

        plot.show_slices = True
        slice_0 = plot.slice(0)

        plot.contour(0).variable = dataset.variable('U(M/S)')
        slice_0.contour.show = True

        slice_0.effects.use_translucency = True
        slice_0.effects.surface_translucency = 70

        # ensure consistent output between interactive (connected) and batch
        plot.contour(0).levels.reset_to_nice()

        tp.export.save_png('slice_effects.png', 600, supersample=3)

    .. figure:: /_static/images/slice_effects.png
        :width: 300px
        :figwidth: 300px
    """
    def __init__(self, slice_group):
        super().__init__(slice_group, sv.EFFECTS)

    @property
    def lighting_effect(self):
        """`LightingEffect`: Surface lighting effect.

        Slice lighting effects must be enabled by setting
        `SliceContour.use_lighting_effect` or
        `SliceShade.use_lighting_effect` to `True` when setting this value.

        There are two types of lighting effects: Paneled and Gouraud:

            * `Paneled`: Within each cell, the color assigned to each area by
                shading or contour flooding is tinted by a shade constant
                across the cell. This shade is based on the orientation
                of the cell relative to your 3D light source.
            * `Gouraud`: This offers smoother, more continuous shading than
                Paneled shading, but it also results in slower plotting and
                larger print files. `Gouraud` shading is not continuous across
                zone boundaries unless face neighbors are specified in the
                data. `Gouraud` shading is not available for finite element
                volume `Zones <data_access>` when blanking is active. The
                zone's lighting effect reverts to `Paneled` shading in this
                case.

        Example usage::

            >>> plot.slice(0).contour.use_lighting_effect = True
            >>> plot.slice(0).effects.lighting_effect = LightingEffect.Paneled
        """
        return self._get_style(LightingEffect, sv.LIGHTINGEFFECT)

    @lighting_effect.setter
    def lighting_effect(self, value):
        self._set_style(LightingEffect(value), sv.LIGHTINGEFFECT)

    @property
    def surface_translucency(self):
        """`int`: Surface translucency of the slice group.

        Slice surface translucency must be enabled by setting
        `SliceEffects.use_translucency` = `True` when setting this value.


        Valid slice translucency values range
        from one (opaque) to 99 (translucent).

        Example usage::

            >>> plot.slice(0).effects.use_translucency = True
            >>> plot.slice(0).effects.surface_translucency = 20
        """
        return self._get_style(int, sv.SURFACETRANSLUCENCY)

    @surface_translucency.setter
    def surface_translucency(self, value):
        self._set_style(int(value), sv.SURFACETRANSLUCENCY)

    @property
    def use_translucency(self):
        """`bool`: Enable surface translucency for this slice group.

        The surface translucency value can be changed by setting
        `SliceEffects.surface_translucency`.

        Example usage::

            >>> plot.slice(0).effects.use_translucency = True
            >>> plot.slice(0).effects.surface_translucency = 20
        """
        return self._get_style(bool, sv.USETRANSLUCENCY)

    @use_translucency.setter
    def use_translucency(self, value):
        self._set_style(bool(value), sv.USETRANSLUCENCY)


class SliceEdge(session.SubStyle):
    """Edge attributes of the slice group.

    When enabled, selected edge lines of all slices in this group will
    be shown:

    .. code-block:: python
        :emphasize-lines: 13-14

        from os import path
        import tecplot as tp

        examples_dir = tp.session.tecplot_examples_directory()
        datafile = path.join(examples_dir, 'SimpleData', 'DuctFlow.plt')
        dataset = tp.data.load_tecplot(datafile)

        plot = tp.active_frame().plot()
        plot.show_slices = True
        plot.contour(0).variable = dataset.variable('U(M/S)')

        slice_0 = plot.slice(0)
        slice_0.edge.show = True
        slice_0.edge.line_thickness = 0.8

        # ensure consistent output between interactive (connected) and batch
        plot.contour(0).levels.reset_to_nice()

        tp.export.save_png('slice_edge.png', 600, supersample=3)

    .. figure:: /_static/images/slice_edge.png
        :width: 300px
        :figwidth: 300px
    """

    def __init__(self, slice_group):
        super().__init__(slice_group, sv.EDGELAYER)

    @property
    def edge_type(self):
        """`EdgeType`: Edge type.

        There are two types of edges in |Tecplot 360|: creases and borders.

        An edge border is the boundary of a `Zone <data_access>`. An edge
        crease appears when the inside angle between two cells is less than a
        user-defined limit. The inside angle can range from 0-180 degrees
        (where 180 degrees indicates coplanar surfaces). The default inside
        angle for determining an edge crease is 135 degrees.

        Example usage::

            >>> plot.slice(0).edge.show = True
            >>> plot.slice(0).edge.edge_type = EdgeType.BordersAndCreases
        """
        return self._get_style(EdgeType, sv.EDGETYPE)

    @edge_type.setter
    def edge_type(self, value):
        self._set_style(EdgeType(value), sv.EDGETYPE)

    @property
    def show(self):
        """`bool`: Show edges.

        This property must be set to `True` to show any of the other edge
        properties.

        Example usage::

            >>> plot.slice(0).edge.show = True
            >>> plot.slice(0).edge.edge_type = EdgeType.BordersAndCreases
        """
        return self._get_style(bool, sv.SHOW)

    @show.setter
    def show(self, value):
        self._set_style(bool(value), sv.SHOW)

    @property
    def color(self):
        """`Color`: Edge color.

        Example usage::

            >>> plot.slice(0).edge.show = True
            >>> plot.slice(0).edge.color = Color.Blue
        """
        return self._get_style(Color, sv.COLOR)

    @color.setter
    def color(self, value):
        self._set_style(Color(value), sv.COLOR)

    @property
    def line_thickness(self):
        """`float`: Edge line thickness as a percentage of frame width.

        Example usage::

            >>> plot.slice(0).edge.show = True
            >>> plot.slice(0).edge.line_thickness = .8
        """
        return self._get_style(float, sv.LINETHICKNESS)

    @line_thickness.setter
    def line_thickness(self, value):
        self._set_style(float(value), sv.LINETHICKNESS)


class SliceVector(session.SubStyle):
    """Vector attributes of the slice group.

    .. code-block:: python
        :emphasize-lines: 22-25

        from os import path
        import tecplot as tp
        from tecplot.constant import *

        examples_dir = tp.session.tecplot_examples_directory()
        datafile = path.join(examples_dir, 'SimpleData', 'DuctFlow.plt')
        dataset = tp.data.load_tecplot(datafile)

        plot = tp.active_frame().plot()

        plot.show_slices = True
        slice_0 = plot.slice(0)

        plot.contour(0).variable = dataset.variable('T(K)')

        # Vector variables must be assigned before displaying
        vectors = plot.vector
        vectors.u_variable = dataset.variable('U(M/S)')
        vectors.v_variable = dataset.variable('V(M/S)')
        vectors.w_variable = dataset.variable('W(M/S)')

        slice_vector = plot.slice(0).vector
        slice_vector.show = True
        slice_vector.vector_type = VectorType.MidAtPoint
        slice_vector.color = Color.BluePurple

        slice_0.effects.use_translucency = True
        slice_0.effects.surface_translucency = 30

        # ensure consistent output between interactive (connected) and batch
        plot.contour(0).levels.reset_to_nice()

        tp.export.save_png('slice_vector.png', 600, supersample=3)

    .. figure:: /_static/images/slice_vector.png
        :width: 300px
        :figwidth: 300px
    """

    def __init__(self, slice_group):
        super().__init__(slice_group, sv.VECTOR)

    @property
    def show(self):
        """`bool`: Show vectors on slices.

        Example usage::

            >>> plot.slice(0).vector.show = True
        """
        return self._get_style(bool, sv.SHOW)

    @show.setter
    def show(self, value):
        self._set_style(bool(value), sv.SHOW)

    @property
    def color(self):
        """`Color`: Set slice vector color.

        Example usage::

            >>> plot.slice(0).vector.show = True
            >>> plot.slice(0).vector.color = Color.Red
        """
        return self._get_style(Color, sv.COLOR)

    @color.setter
    def color(self, value):
        self._set_style(Color(value), sv.COLOR)

    @property
    def is_tangent(self):
        """`bool`: Use tangent vectors for slices.

        Example usage::

            >>> plot.slice(0).vector.show = True
            >>> plot.slice(0).vector.is_tangent = True
        """
        return self._get_style(bool, sv.ISTANGENT)

    @is_tangent.setter
    def is_tangent(self, value):
        self._set_style(bool(value), sv.ISTANGENT)

    @property
    def line_thickness(self):
        """`float`: Vector line thickness as a percentage of the frame height.

        Typical values are .02, .1, .4, .8, 1.5

        Example usage::

            >>> plot.slice(0).vector.show = True
            >>> plot.slice(0).vector.line_thickness = .1
        """
        return self._get_style(float, sv.LINETHICKNESS)

    @line_thickness.setter
    def line_thickness(self, value):
        self._set_style(float(value), sv.LINETHICKNESS)

    @property
    def vector_type(self):
        """`VectorType`: Type of vector for slices in this slice group.

        Example usage::

            >>> plot.slice(0).vector.show = True
            >>> plot.slice(0).vector.vector_type = VectorType.MidAtPoint
        """
        return self._get_style(VectorType, sv.VECTORTYPE)

    @vector_type.setter
    def vector_type(self, value):
        self._set_style(VectorType(value), sv.VECTORTYPE)

    @property
    def arrowhead_style(self):
        """`ArrowheadStyle`: Arrowhead style of slice vectors.

        Example usage::

            >>> plot.slice(0).vector.show = True
            >>> plot.slice(0).vector.arrowhead_style = ArrowheadStyle.Hollow
        """
        return self._get_style(ArrowheadStyle, sv.ARROWHEADSTYLE)

    @arrowhead_style.setter
    def arrowhead_style(self, value):
        self._set_style(ArrowheadStyle(value), sv.ARROWHEADSTYLE)


class SliceContour(session.SubStyle):
    """Contour attributes of the slice group.

    .. code-block:: python
        :emphasize-lines: 18-21

        from os import path
        import tecplot as tp
        from tecplot.constant import SliceSurface, ContourType

        examples_dir = tp.session.tecplot_examples_directory()
        datafile = path.join(examples_dir, 'SimpleData', 'DuctFlow.plt')
        dataset = tp.data.load_tecplot(datafile)

        plot = tp.active_frame().plot()

        plot.show_slices = True
        slice_0 = plot.slice(0)

        # Use contour(0) for Flooding and contour(2) for Lines
        plot.contour(0).variable = dataset.variable('P(N/m2)')
        plot.contour(2).variable = dataset.variable('T(K)')
        plot.contour(2).legend.show = False
        slice_0.contour.show = True
        slice_0.contour.flood_contour_group = plot.contour(0)
        slice_0.contour.line_contour_group = plot.contour(2)
        slice_0.contour.contour_type = ContourType.Overlay  # AKA "Both lines and flood"

        slice_0.show_primary_slice = False
        slice_0.show_start_and_end_slices = True
        slice_0.show_intermediate_slices = True
        slice_0.start_position = (-.21, .05, .025)
        slice_0.end_position = (1.342, .95, .475)
        slice_0.num_intermediate_slices = 3

        # ensure consistent output between interactive (connected) and batch
        slice_0.contour.flood_contour_group.levels.reset_to_nice()
        slice_0.contour.line_contour_group.levels.reset_to_nice()

        tp.export.save_png('slice_contour.png', 600, supersample=3)

    .. figure:: /_static/images/slice_contour.png
        :width: 300px
        :figwidth: 300px
    """
    def __init__(self, slice_group):
        super().__init__(slice_group, sv.CONTOUR)
        self.plot = slice_group.plot

    @property
    def show(self):
        """`bool`: Show contours on the slice.

        Example usage::

            >>> plot.show_slices = True
            >>> plot.slice(1).contour.show = True
        """
        return self._get_style(bool, sv.SHOW)

    @show.setter
    def show(self, value):
        self._set_style(bool(value), sv.SHOW)

    @property
    def contour_type(self):
        """`ContourType`: Contour type for the slice contours.

        Example usage::

            >>> plot.show_slices = True
            >>> plot.slice(0).contour.contour_type = ContourType.AverageCell
        """
        return self._get_style(ContourType, sv.CONTOURTYPE)

    @contour_type.setter
    def contour_type(self, value):
        self._set_style(ContourType(value), sv.CONTOURTYPE)

    @property
    def line_color(self):
        """`Color`: `Color` of contour lines.

        Selecting `Color.MultiColor` will color the slice contour lines
        based on the `contour group <tecplot.plot.ContourGroup>` variable.

        Example usage::

            >>> plot.show_slices = True
            >>> plot.slice(0).contour.line_color = Color.Blue
        """
        return self._get_style(Color, sv.COLOR)

    @line_color.setter
    def line_color(self, value):
        self._set_style(Color(value), sv.COLOR)

    @property
    def line_thickness(self):
        """`float`: Contour line thickness as a percentage of frame width.

        Suggested values are one of: **.02, .1, .4, .8, 1.5**

        Example usage::

            >>> plot.show_slices = True
            >>> plot.slice(0).contour.line_thickness = .4
        """
        return self._get_style(float, sv.LINETHICKNESS)

    @line_thickness.setter
    def line_thickness(self, value):
        self._set_style(float(value), sv.LINETHICKNESS)

    @property
    def flood_contour_group_index(self):
        """`Index`: Zero-based `Index` of the flodding `ContourGroup`.

        This property sets and gets, by `Index`, the `ContourGroup` used for
        flooding. Changing style on this `ContourGroup` will affect all
        fieldmaps on the same `Frame` that use it.

        Example usage::

            >>> plot.show_slices = True
            >>> contour = plot.slice(0).contour
            >>> contour.flood_contour_group_index = 1
        """
        return self._get_style(tecutil.Index, sv.FLOODCOLORING)

    @flood_contour_group_index.setter
    def flood_contour_group_index(self, index):
        self._set_style(tecutil.Index(index), sv.FLOODCOLORING)

    @property
    def flood_contour_group(self):
        """`ContourGroup`: Contour group to use for flooding.

        Changing style on this `ContourGroup` will affect all
        fieldmaps on the same `Frame` that use it.

        Example usage::

            >>> group = plot.contour(1)
            >>> contour = plot.slice(1).contour
            >>> contour.flood_contour_group = group
        """
        indices = self.flood_contour_group_index
        if isinstance(indices, Iterable):
            return tuple([self.plot.contour(i) for i in indices])
        else:
            return self.plot.contour(indices)

    @flood_contour_group.setter
    def flood_contour_group(self, flood_contour_group):
        self.flood_contour_group_index = flood_contour_group.index

    @property
    def line_contour_group_index(self):
        """`int`: Zero-based `Index` of the `ContourGroup` for contour lines.

        This property sets and gets, by `Index`, the `ContourGroup` used for
        line placement. Although all properties of the `ContourGroup` can be
        manipulated through this object, many of them (i.e., color) will not
        affect the lines unless the `FieldmapContour.line_color` is set to the
        same `ContourGroup`. Note that changing style on this `ContourGroup`
        will affect all other fieldmaps on the same `Frame` that use it.

        Example usage::

            >>> plot.show_slices = True
            >>> contour = plot.slice(0).contour
            >>> contour.line_contour_group_index = 2
        """
        return self._get_style(tecutil.Index, sv.LINECONTOURGROUP)

    @line_contour_group_index.setter
    def line_contour_group_index(self, index):
        self._set_style(tecutil.Index(index), sv.LINECONTOURGROUP)

    @property
    def line_contour_group(self):
        """`ContourGroup`: Contour group to use for contour lines.

        Changing style on this `ContourGroup` will affect all
        fieldmaps on the same `Frame` that use it.

        Example usage::

            >>> group = plot.contour(1)
            >>> contour = plot.slice(1).contour
            >>> contour.line_contour_group = group
        """
        indices = self.line_contour_group_index
        if isinstance(indices, Iterable):
            return tuple([self.plot.contour(i) for i in indices])
        else:
            return self.plot.contour(indices)

    @line_contour_group.setter
    def line_contour_group(self, line_contour_group):
        self.line_contour_group_index = line_contour_group.index

    @property
    def use_lighting_effect(self):
        """`bool`; Enable lighting effect.

        .. note::
            Setting `SliceContour.use_lighting_effect` will also set
            the same value for `SliceShade.use_lighting_effect`,
            and vice-versa.

        The lighting effect is set with `SliceEffects.lighting_effect`, and may
        be one of `LightingEffect.Gouraud` or `LightingEffect.Paneled`.

        Example usage::

            >>> plot.show_slices = True
            >>> contour = plot.slice(0).contour
            >>> contour.use_lighting_effect = True
            >>> plot.slice(0).effects.lighting_effect = LightingEffect.Paneled
        """
        return self._get_style(bool, sv.USELIGHTINGEFFECT)

    @use_lighting_effect.setter
    def use_lighting_effect(self, value):
        self._set_style(bool(value), sv.USELIGHTINGEFFECT)


class SliceGroupCollection(session.Style):
    """Change attributes associated with multiple slices.

    Slices can include lighting effects, contours, meshes, and more. To
    customize these and other attributes of slices, use this object. It
    controls the style for specific slice groups within a `Frame`. Slice
    `contour <SliceGroup.contour>`, vector, edge, effects, mesh, visibility and
    position information are accessed through this class:

    .. code-block:: python
        :emphasize-lines: 12-29

        from os import path
        import tecplot as tp
        from tecplot.constant import *

        examples_dir = tp.session.tecplot_examples_directory()
        datafile = path.join(examples_dir, 'SimpleData', 'DuctFlow.plt')
        dataset = tp.data.load_tecplot(datafile)

        plot = tp.active_frame().plot()
        plot.contour(0).variable = dataset.variable('U(M/S)')

        plot.show_slices = True
        slices = plot.slices(0, 1, 2)
        slices.show = True

        slices.contour.show = True
        slices.contour.contour_type = ContourType.Overlay
        slices.effects.use_translucency = True
        slices.effects.surface_translucency = 70

        # Show arbitrary slices
        slices.orientation = SliceSurface.Arbitrary
        slices.origin = (0.1, 0.2, 0)
        slices[0].arbitrary_normal = (1, 0.5, 0)
        slices[1].arbitrary_normal = (0.2, 1, 0)
        slices[2].arbitrary_normal = (0, 0, 1)

        slices.edge.show = True
        slices.edge.line_thickness = 0.4

        plot.contour(0).levels.reset_to_nice()
        plot.contour(0).legend.show = False

        tp.export.save_png('slice_collection.png')

    .. figure:: /_static/images/slice_collection.png
        :width: 300px
        :figwidth: 300px

    Up to eight different slice groups can be set and each slice group can use
    different slice planes or different ranges for the same slice plane.

    This class behaves like `SliceGroup` except that setting any underlying
    style will do so for all of the represented slice groups. The style
    properties are then always returned as a `tuple` of properties, one for
    each group, ordered by index number. This means there is an asymmetry
    between setting and getting any property under this object, illustrated by
    the following example::

        >>> slices = plot.slices(0, 1, 2)
        >>> slices.show = True
        >>> print(slices.show)
        (True, True, True)

    All examples that set style on a single slice like the following::

        >>> plot.slice(0).contour.show = True

    may be converted to setting the same style on all slice groups like so::

        >>> plot.slices().contour.show = True

    .. seealso:: `SliceGroup`

    .. versionadded:: 1.2
        Slice collection objects.
    """
    def __init__(self, plot, *indices):
        if __debug__:
            assert all(0 <= i < 8 for i in indices), \
                'Slice index out of range (must be in the range: [0,7])'
        if indices:
            self._indices = set([tecutil.Index(i) for i in indices])
        else:
            self._indices = set(range(8))
        self.plot = plot
        super().__init__(sv.SLICEATTRIBUTES, uniqueid=self.plot.frame.uid)

    @property
    def indices(self):
        return sorted(self._indices)

    def __getitem__(self, index):
        return SliceGroup(self.plot, self.indices[index])

    def __iter__(self):
        self._current_index = -1
        self._max_index = len(self._indices)
        return self

    def __next__(self):
        self._current_index += 1
        if self._current_index < self._max_index:
            return self[self._current_index]
        raise StopIteration

    def next(self):  # if sys.version_info < (3,)
        return self.__next__()

    def __eq__(self, other):
        return (self.indices == other.indices) and (self.plot == other.plot)

    def __ne__(self, other):
        return not self.__eq__(other)

    def _get_style(self, rettype, *svargs, **kwargs):
        res = []
        for index in self.indices:
            kwargs.update(**{sv.OFFSET1: index})
            res.append(super()._get_style(rettype, *svargs, **kwargs))
        return tuple(res)

    def _set_style(self, value, *svargs, **kwargs):
        for index in self.indices:
            kwargs.update(**{sv.OFFSET1: index})
            super()._set_style(value, *svargs, **kwargs)

    @tecutil.lock()
    def extract(self, mode=ExtractMode.SingleZone, assign_strand_ids=True,
                resulting_1d_zone_type=Resulting1DZoneType.IOrderedIfPossible,
                transient_mode=TransientOperationMode.SingleSolutionTime):
        """Create new zones from this slice collection.

        Extracts the current slices represented by this group to the
        `Dataset` as one or more zones.

        Parameters:
            mode (`ExtractMode`, optional): Determines how many zones are
                created upon extraction. Possible values are:
                `ExtractMode.SingleZone` (default) and
                `ExtractMode.OneZonePerConnectedRegion`.
            assign_strand_ids (`bool`, optional): Automatically assign strand
                ID's to the created zones. (default: `True`)
            resulting_1d_zone_type (`Resulting1DZoneType`, optional): The type
                of zone to create when the result is one-dimensional. Possible
                values are: `Resulting1DZoneType.IOrderedIfPossible` (default)
                and `Resulting1DZoneType.FELineSegment`.
            transient_mode (`TransientOperationMode`): Determines which
                solution times are used to extract slices when transient data
                is available in the dataset. Possible values are
                `TransientOperationMode.SingleSolutionTime` (default) or
                `TransientOperationMode.AllSolutionTimes`.

        Returns:

            generator_ of the extracted zones.

        .. seealso:: `tecplot.data.extract.extract_slice()`

        Example usage showing how to convert the resulting generator into a
        reusable list object of zones::

            >>> slice_zones = list(plot.slices(0, 1).extract())

        .. _generator: https://docs.python.org/3/reference/expressions.html#generator-expressions
        """
        transient_mode = TransientOperationMode(transient_mode)

        if __debug__:
            if version.sdk_version_info < (2017, 3):
                msg = 'Slice extraction not supported'
                raise TecplotOutOfDateEngineError((2017, 3), msg)
            if transient_mode != TransientOperationMode.SingleSolutionTime:
                if version.sdk_version_info < (2019, 1):
                    msg = 'Slice over all solution times not supported'
                    raise TecplotOutOfDateEngineError((2019, 1), msg)

        dataset = self.plot.frame.dataset
        mode = ExtractMode(mode)
        nzones = dataset.num_zones
        with self.plot.frame.activated(), \
             tecutil.ArgList() as arglist:

            arglist[sv.EXTRACTMODE] = mode
            arglist[sv.AUTOSTRANDTRANSIENTDATA] = bool(assign_strand_ids)
            zone_type = Resulting1DZoneType(resulting_1d_zone_type)
            arglist[sv.RESULTING1DZONETYPE] = zone_type
            if transient_mode != TransientOperationMode.SingleSolutionTime:
                arglist[sv.TRANSIENTOPERATIONMODE] = transient_mode

            if version.sdk_version_info < (2019, 1):
                opts = dict(arglist)
                for group in self.indices:
                    arglist.clear()
                    arglist.update(**opts)
                    arglist[sv.GROUP] = group
                    if not _tecutil.ExtractSlicesX(arglist):
                        raise TecplotSystemError()
            else:
                with tecutil.IndexSet(*self._indices) as groups:
                    arglist[sv.GROUPS] = groups
                    if not _tecutil.ExtractSlicesX(arglist):
                        raise TecplotSystemError()

        return (dataset.zone(i) for i in range(nzones, dataset.num_zones))

    @property
    def vector(self):
        """`SliceVector`: Vector attributes for this slice group.

        Example usage::

            >>> plot.slice(0).vector.show = True
        """
        return SliceVector(self)

    @property
    def edge(self):
        """`SliceEdge`: Edge attributes for this slice group.

        Example usage::

            >>> plot.slice(0).edge.show = True
        """
        return SliceEdge(self)

    @property
    def effects(self):
        """`SliceEffects`: Effects attributes for this slice group.

            Example usage::

                >>> plot.slice(0).effects.use_translucency = True
        """
        return SliceEffects(self)

    @property
    def shade(self):
        """`SliceShade`: Shade attributes for this slice group.

        Example usage::

            >>> plot.slice(0).shade.show = True
        """
        return SliceShade(self)

    @property
    def mesh(self):
        """`SliceMesh`: Mesh attributes for this slice group.

        Example usage::

            >>> plot.slice(0).mesh.show = True
        """
        return SliceMesh(self)

    @property
    def show(self):
        """`bool`: Show slices for this slice group.

        Example usage::

            >>> plot.slice(0).show = True
        """
        return self._get_style(bool, sv.SHOWGROUP)

    @show.setter
    def show(self, value):
        self._set_style(bool(value), sv.SHOWGROUP)

    @property
    def show_primary_slice(self):
        """`bool`; Include the primary slice (first slice placed) in the `Plot`.

        Example usage::

            >>> plot.slice(0).show = True
            >>> plot.slice(0).show_primary_slice = True

        """
        return self._get_style(bool, sv.SHOWPRIMARYSLICE)

    @show_primary_slice.setter
    def show_primary_slice(self, value):
            self._set_style(bool(value), sv.SHOWPRIMARYSLICE)

    @property
    def contour(self):
        """`SliceContour`: Contour attributes for the slice group.

        Example usage::

            >>> plot.slice(0).contour.show = True
        """
        return SliceContour(self)

    @property
    def orientation(self):
        """`SliceSurface`: Select on which plane the slice is drawn.

        You may also choose `SliceSurface.Arbitrary` to place the
        slice on an arbitrary plane.

        To orient slices in an arbitrary direction,
        choose `SliceSurface.Arbitrary`.
        As with other slices, you may specify origin points for a primary
        slice and/or for start and end slices. Slices pass through the
        indicated origin point(s), so you can easily align the edge of a
        slice or group of slices along some other feature of the plot,
        such as an axis. If intermediate slices are activated,
        they are drawn equally spaced between the slices
        defined by the start and end origins.

        Example usage::

            >>> plot.slice(0).orientation = SliceSurface.XPlanes
        """
        return self._get_style(SliceSurface, sv.SLICESURFACE)

    @orientation.setter
    def orientation(self, value):
        self._set_style(SliceSurface(value), sv.SLICESURFACE)

    @property
    def arbitrary_normal(self):
        """`tuple`: Normal for arbitrary slices.

        Example usage::

            >>> plot.slice(0).orientation = SliceSurface.Arbitrary
            >>> plot.slice(0).arbitrary_normal = (0.1, 0.2, 0.3)
            >>> plot.slice(0).arbitrary_normal.x
            0.1
            >>> plot.slice(0).arbitrary_normal.y
            0.2
            >>> plot.slice(0).arbitrary_normal.z
            0.3
        """
        return session.XYZ(self, sv.NORMAL)

    @arbitrary_normal.setter
    def arbitrary_normal(self, values):
        session.XYZ(self, sv.NORMAL)[:] = values

    def _position(self, svarg):
        index_orientations = (SliceSurface.IPlanes,
                              SliceSurface.JPlanes,
                              SliceSurface.KPlanes)
        spatial = [o not in index_orientations for o in self.orientation]
        if all(spatial):
            return session.XYZ(self, svarg)
        elif any(spatial):
            msg = 'all slices must have the same type of orientation'
            raise TecplotLogicError(msg)
        else:
            return session.IndexIJK(self, svarg)

    @property
    def origin(self):
        """`tuple` or `int`: Origin of the slice.

        This will be a 3-`tuple` of `float` if `orientation` is ``X,Y,Z`` or
        zero-based `int` if `orientation` is ``I,J,K``. For arbitrary slice
        orientation, the origin can be any location. For axis orientations
        (`XPlanes`, `YPlanes`, etc.) two of the three components are not used.

        Example usage::

            >>> slice_0 = plot.slice(0)
            >>> slice_0.orientation = SliceSurface.IPlanes
            >>> slice_0.origin = (1, 0, 0)
            >>> dx = (1, 1, 1)
            >>> slice_0.origin += dx
            >>> slice_0.origin.i
            2
            >>> slice_0.origin.j
            1
            >>> slice_0.origin.k
            1

            >>> slice_0.orientation = SliceSurface.Arbitrary
            >>> slice_0.origin = (.5, .1, .1)
            >>> slice_0.origin += dx
            >>> slice_0.origin.x
            1.5
            >>> slice_0.origin.y
            .1
            >>> slice_0.origin.z
            .1
        """
        return self._position(sv.PRIMARYPOSITION)

    @origin.setter
    def origin(self, values):
        self._position(sv.PRIMARYPOSITION)[:] = values

    @property
    def end_position(self):
        """`tuple` or `int`: Position of the end slice.

        `SliceGroup.show_start_and_end_slices` must be `True` to show the end
        slice. This will be a 3-`tuple` of `float` if `orientation` is
        ``X,Y,Z`` or zero-based `int` if `orientation` is ``I,J,K``.

        Example usage::

            >>> plot.slice(0).show_start_and_end_slices = True
            >>> plot.slice(0).end_position = (1, 1, 1)
            >>> plot.slice(0).end_position.i
            1
        """
        return self._position(sv.ENDPOSITION)

    @end_position.setter
    def end_position(self, values):
        self._position(sv.ENDPOSITION)[:] = values

    @property
    def start_position(self):
        """`tuple` or `int`: Position of the start slice.

        `SliceGroup.show_start_and_end_slices` must be `True` to show the start
        slice. This will be a 3-`tuple` of `float` if `orientation` is
        ``X,Y,Z`` or zero-based `int` if `orientation` is ``I,J,K``.

        Example usage::

            >>> plot.slice(0).show_start_and_end_slices = True
            >>> plot.slice(0).start_position = (1, 1, 1)
            >>> plot.slice(0).start_position.i
            1
        """
        return self._position(sv.STARTPOSITION)

    @start_position.setter
    def start_position(self, values):
        self._position(sv.STARTPOSITION)[:] = values

    @property
    def num_intermediate_slices(self):
        """`int`: Number of intermediate slicing planes.

        You may specify between 1 and 5,000 intermediate slices.

        Example usage::

            >>> # Show 2 intermediate slices
            >>> plot.slice(0).num_intermediate_slices = 2
        """
        return self._get_style(int, sv.NUMINTERMEDIATESLICES)

    @num_intermediate_slices.setter
    def num_intermediate_slices(self, value):
        self._set_style(int(value), sv.NUMINTERMEDIATESLICES)

    @property
    def show_intermediate_slices(self):
        """Show intermediate slices.

        Intermediate slices are evenly distributed between the start and end
        slices.

        Example usage::

            >>> plot.slice(0).show_intermediate_slices = True
        """
        return self._get_style(bool, sv.SHOWINTERMEDIATESLICES)

    @show_intermediate_slices.setter
    def show_intermediate_slices(self, value):
        self._set_style(bool(value), sv.SHOWINTERMEDIATESLICES)

    @property
    def obey_source_zone_blanking(self):
        """`bool`: Obey source zone blanking.

        When set to `True`, slices are subject to any blanking used for
        the data. When set to `False`, slices are generated for blanked
        and unblanked regions.

        Example usage::

            >>> plot.slice(0).obey_source_zone_blanking = True
        """
        return self._get_style(bool, sv.OBEYSOURCEZONEBLANKING)

    @obey_source_zone_blanking.setter
    def obey_source_zone_blanking(self, value):
        self._set_style(bool(value), sv.OBEYSOURCEZONEBLANKING)

    @property
    def slice_source(self):
        """`SliceSource`: `Zones <data_access>` to slice through.

        Choose to slice through volume `Zones <data_access>`, surface `Zones
        <data_access>`, or the surfaces of volume `Zones <data_access>`.

        Example usage::

            >>> plot.slice(0).slice_source = SliceSource.SurfaceZones
        """
        return self._get_style(SliceSource, sv.SLICESOURCE)

    @slice_source.setter
    def slice_source(self, value):
        self._set_style(SliceSource(value), sv.SLICESOURCE)

    @property
    def show_start_and_end_slices(self):
        """`bool`: Include start and end slices.

        Example usage::

            >>> plot.slice(0).show_start_and_end_slices = True
        """
        return self._get_style(bool, sv.SHOWSTARTENDSLICE)

    @show_start_and_end_slices.setter
    def show_start_and_end_slices(self, value):
        self._set_style(bool(value), sv.SHOWSTARTENDSLICE)

    @property
    def surface_generation_method(self):
        """`SurfaceGenerationMethod`: Determines how the surface is generated.

        May be one of:

        * `SurfaceGenerationMethod.Auto`:
            Selects one of the surface generation algorithms best suited for
            the zones participating in the slice generation. "All polygons" is
            used if one or more of the participating zones is polytope,
            otherwise "allow quads" is used.
        * `SurfaceGenerationMethod.AllPolygons`:
            Similar to the "All triangles" method except that all interior
            faces generated as a result of triangulation that are not part of
            the original mesh are eliminated. This preserves the original mesh
            of the source zones on the resulting slice.
        * `SurfaceGenerationMethod.AllTriangles`:
            An advanced algorithm that can handle complex saddle issues and
            guarantees that there will be no holes in the final surface. As the
            surface is composed entirely of triangles, it can be delivered more
            efficiently to the graphics hardware.
        * `SurfaceGenerationMethod.AllowQuads`:
            Produces quads or triangles, and the resulting surface more closely
            resembles the shape of the volume cells from the source zone. Since
            the quads are not arbitrarily divided into triangles, no biases are
            introduced, and the resulting surface may appear smoother. This
            method is preferred when the source zone is FE-Brick or IJK-Ordered
            and the surface is aligned with the source cells.

        Example usage::

            >>> from tecplot.constant import SurfaceGenerationMethod
            >>> plot.slice(0).surface_generation_method = \
            ... SurfaceGenerationMethod.AllowQuads
        """
        return self._get_style(SurfaceGenerationMethod,
                               sv.SURFACEGENERATIONMETHOD)

    @surface_generation_method.setter
    def surface_generation_method(self, value):
        if __debug__:
            if version.sdk_version_info < (2017, 2):
                msg = 'setting surface generation method requires' \
                      ' Tecplot 360 2017 R2 or later.'
                raise TecplotOutOfDateEngineError((2017, 2), msg)
            elif version.sdk_version_info < (2018, 1):
                if SurfaceGenerationMethod(value) in [
                        SurfaceGenerationMethod.AllPolygons,
                        SurfaceGenerationMethod.Auto]:
                    msg = 'This surface generation method requires' \
                          ' Tecplot 360 2018 R1 or later.'
                    raise TecplotOutOfDateEngineError((2018, 1), msg)
        self._set_style(SurfaceGenerationMethod(value),
                        sv.SURFACEGENERATIONMETHOD)

    @property
    def clip(self):
        """`ClipPlane`: Orientation of data clipping for this slice group.

        Clipping the field data, isosurfaces, streamtraces or other plot
        objects using slices requires setting the ``clip`` property of the
        slice as well as adding the slice group to the ``clip_planes`` property
        on the fieldmap effects. Only slice groups 0 to 5 are available for
        clipping in this framework::

            >>> from tecplot.constant import *
            >>> # setup slice and clipping orientation
            >>> slice = plot.slice(0)
            >>> slice.origin = (7, 0, 0)
            >>> slice.clip = ClipPlane.AbovePrimarySlice
            >>> # add slice group to the fieldmap clip planes
            >>> plot.fieldmap(0).effects.clip_planes = [slice]
            >>> # turn on and set value of isosurface
            >>> # and enforce slice clipping
            >>> isosurf = plot.isosurface(0)
            >>> isosurf.isosurface_values = 3
            >>> isosurf.use_slice_clipping = True
            >>> # turn on isosurfaces and slices
            >>> pt.show_isosurfaces = True
            >>> pt.show_slices = True

        .. warning:: **Slice clipping is only supported for X, Y and Z-planes.**

            Slice clipping has no effect for slices that have an orientation of
            `SliceSurface.Arbitrary`, `SliceSurface.IPlanes`,
            `SliceSurface.JPlanes` or , `SliceSurface.KPlanes`. That is, the
            orientation must be one of: `SliceSurface.XPlanes`,
            `SliceSurface.YPlanes` or `SliceSurface.ZPlanes`.
        """
        return self._get_style(ClipPlane, sv.CLIPPLANE)

    @clip.setter
    def clip(self, value):
        self._set_style(ClipPlane(value), sv.CLIPPLANE)

    @property
    def use_slice_clipping(self):
        """`bool`: Clip this slice by any intersecting slices.

        Example usage::

            >>> from tecplot.constant import ClipPlane
            >>> slice = plot.slice(0)
            >>> slice.clip = ClipPlane.AbovePrimarySlice
            >>> plot.fieldmap(0).effects.clip_planes = slice
            >>> plot.slice(1).use_slice_clipping = True

        .. seealso:: `SliceGroup.clip`
        """
        return self._get_style(bool, sv.OBEYCLIPPLANES)

    @use_slice_clipping.setter
    def use_slice_clipping(self, value):
        self._set_style(bool(value), sv.OBEYCLIPPLANES)


class SliceGroup(SliceGroupCollection):
    """Change attributes associated with a specific slice group.

    Slices can include lighting effects, contours, meshes, and more.
    To customize these and other attributes of slices, use this object.

    This object controls the style for a specific slice group within a `Frame`.
    Slice `contour <SliceGroup.contour>`, vector, edge, effects, mesh,
    visibility and position information are accessed through this class:

    .. code-block:: python
        :emphasize-lines: 19-40

        from os import path
        import tecplot as tp
        from tecplot.constant import *

        examples_dir = tp.session.tecplot_examples_directory()
        datafile = path.join(examples_dir, 'SimpleData', 'DuctFlow.plt')
        dataset = tp.data.load_tecplot(datafile)

        plot = tp.active_frame().plot()
        plot.contour(0).variable = dataset.variable('U(M/S)')
        plot.show_edge = True
        plot.fieldmap(0).edge.edge_type = EdgeType.Creases

        vectors = plot.vector
        vectors.u_variable = dataset.variable('U(M/S)')
        vectors.v_variable = dataset.variable('V(M/S)')
        vectors.w_variable = dataset.variable('W(M/S)')

        plot.show_slices = True
        slice_0 = plot.slice(0)

        slice_0.contour.show = True
        slice_0.contour.contour_type = ContourType.Overlay  # AKA "Both lines and flood"

        slice_0.effects.use_translucency = True
        slice_0.effects.surface_translucency = 30

        # Show an arbitrary slice
        slice_0.orientation = SliceSurface.Arbitrary
        slice_0.arbitrary_normal = (1, .5, 0)

        slice_0.show_primary_slice = False
        slice_0.show_start_and_end_slices = True
        slice_0.start_position = (-.21, .05, .025)
        slice_0.end_position = (1.342, .95, .475)
        slice_0.show_intermediate_slices = True
        slice_0.num_intermediate_slices = 3

        slice_0.edge.show = True
        slice_0.edge.line_thickness = 0.4

        # ensure consistent output between interactive (connected) and batch
        plot.contour(0).levels.reset_to_nice()

        tp.export.save_png('slice_group.png', 600, supersample=3)

    .. figure:: /_static/images/slice_group.png
        :width: 300px
        :figwidth: 300px

    Up to eight different slice groups can be set. Each slice group can use
    different slice planes or different ranges for the same slice plane.

        >>> slice_3 = plot.slice(3)
        >>> slice_3.contour.show = True

    .. seealso:: `SliceGroupCollection`
    """
    def __init__(self, plot, index):
        self.index = index
        super().__init__(plot, index)

    def _get_style(self, rettype, *svargs, **kwargs):
        return super()._get_style(rettype, *svargs, **kwargs)[0]

    def _position(self, svarg):
        if self.orientation in (SliceSurface.IPlanes,
                                SliceSurface.JPlanes,
                                SliceSurface.KPlanes):
            return session.IndexIJK(self, svarg)
        else:
            return session.XYZ(self, svarg)

    @tecutil.lock()
    def set_arbitrary_from_points(self, p1, p2, p3):
        """Set an arbitrary slice from 3 points.

        Set the normal and origin of an arbitrary slice using three points.
        The origin will be set to the 3rd point.

        The three points must not be coincident or collinear.
        The slice's origin is set to the third point and its normal
        is recalculated such that the cutting plane passes through all three
        points.

        Parameters:
            p1:  3-`tuple` of floats ``(x, y, z)``
            p2:  3-`tuple` of floats ``(x, y, z)``
            p3:  3-`tuple` of floats ``(x, y, z)``

        Example usage::

            >>> slice0 = plot.slice(0)
            >>> slice0.set_arbitrary_from_points((0.0, 0.0, 0.0),
            ...                                  (0.1, 0.2, 0.3),
            ...                                  (0.1, 0.1, 0.1))
        """
        uid = self._style_attrs[sv.UNIQUEID]
        points = list(it.chain(p1, p2, p3))
        if not _tecutil.SliceSetArbitraryUsingThreePoints(
                uid, self.index + 1, *points):
            msg = 'Error creating arbitrary slice from three points'
            raise TecplotSystemError(msg)

    def extract(self, mode=ExtractMode.SingleZone, assign_strand_ids=True,
                resulting_1d_zone_type=Resulting1DZoneType.IOrderedIfPossible,
                transient_mode=TransientOperationMode.SingleSolutionTime):
        """Create new zones from this slice.

        Extracts the current slices represented by this group to the
        `Dataset` as one or more zones.

        Parameters:
            mode (`ExtractMode`, optional): Determines how many zones are
                created upon extraction. Possible values are:
                `ExtractMode.SingleZone` (default) and
                `ExtractMode.OneZonePerConnectedRegion`.
            assign_strand_ids (`bool`, optional): Automatically assign strand
                ID's to the created zones. (default: `True`)
            resulting_1d_zone_type (`Resulting1DZoneType`, optional): The type
                of zone to create when the result is one-dimensional. Possible
                values are: `Resulting1DZoneType.IOrderedIfPossible` (default)
                and `Resulting1DZoneType.FELineSegment`.
            transient_mode (`TransientOperationMode`): Determines which
                solution times are used to extract slices when transient data
                is available in the dataset. Possible values are
                `TransientOperationMode.SingleSolutionTime` (default) or
                `TransientOperationMode.AllSolutionTimes`.

        Returns:

            The extracted zone is returned if **mode** is
            `ExtractMode.SingleZone` and **transient_mode** is
            `TransientOperationMode.SingleSolutionTime`, otherwise a generator_
            of the extracted zones.

        .. seealso:: `tecplot.data.extract.extract_slice()`

        Example usage::

            >>> slice_zone = plot.slice(0).extract()
        """
        result = super().extract(mode, assign_strand_ids,
                                 resulting_1d_zone_type, transient_mode)
        if (
            mode == ExtractMode.SingleZone and
            transient_mode == TransientOperationMode.SingleSolutionTime
        ):
            return list(result)[0]
        else:
            return result
