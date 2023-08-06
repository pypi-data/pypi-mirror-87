from builtins import super

from ..tecutil import sv
from .. import session


class LightSource(session.Style):
    """Three-dimensional light source style control.

    The light source is a point of light infinitely far from the drawing area.

    .. code-block:: python
        :emphasize-lines: 13-16

        from os import path
        import tecplot as tp
        from tecplot.constant import PlotType, Color

        examples_dir = tp.session.tecplot_examples_directory()
        infile = path.join(examples_dir, 'SimpleData', 'F18.plt')
        dataset = tp.data.load_tecplot(infile)

        frame = tp.active_frame()
        plot = frame.plot(PlotType.Cartesian3D)
        plot.activate()

        plot.light_source.direction = (0., -0.7, 0.9)
        plot.light_source.intensity = 70
        plot.light_source.specular_intensity = 80
        plot.light_source.specular_shininess = 50

        tp.export.save_png('light_source.png')

    ..  figure:: /_static/images/light_source.png
        :width: 300px
        :figwidth: 300px
    """
    def __init__(self, plot):
        self.plot = plot
        super().__init__(sv.GLOBALTHREED, sv.LIGHTSOURCE,
                         uniqueid=self.plot.frame.uid)

    @property
    def background_light(self):
        """`float`: Percentage intensity of the omni-directional fill light.

        Example usage::

            >>> plot.light_source.background_light = 70.0
        """
        return self._get_style(float, sv.BACKGROUNDLIGHT)

    @background_light.setter
    def background_light(self, value):
        self._set_style(float(value), sv.BACKGROUNDLIGHT)

    @property
    def intensity(self):
        """`float`: Percentage intensity of the light source.

        Example usage::

            >>> plot.light_source.intensity = 50.0
        """
        return self._get_style(float, sv.INTENSITY)

    @intensity.setter
    def intensity(self, value):
        self._set_style(float(value), sv.INTENSITY)

    @property
    def specular_intensity(self):
        """`float`: Percentage intensity of specular highlights.

        Set this to zero to turn off specular effects::

            >>> plot.light_source.specular_intensity = 0
        """
        if self._get_style(bool, sv.INCLUDESPECULAR):
            return self._get_style(float, sv.SPECULARINTENSITY)
        else:
            return 0

    @specular_intensity.setter
    def specular_intensity(self, value):
        if not value:
            self._set_style(False, sv.INCLUDESPECULAR)
        else:
            self._set_style(True, sv.INCLUDESPECULAR)
            self._set_style(float(value), sv.SPECULARINTENSITY)

    @property
    def specular_shininess(self):
        """`float`: Percentage of shininess for specular highlights.

        Example usage::

            >>> plot.light_source.specular_shininess = 80.0
        """
        return self._get_style(float, sv.SPECULARSHININESS)

    @specular_shininess.setter
    def specular_shininess(self, value):
        self._set_style(float(value), sv.SPECULARSHININESS)

    @property
    def surface_color_contrast(self):
        """`float`: Percentage of contrast for surface colors.

        Example usage::

            >>> plot.light_source.surface_color_contrast = 80.0
        """
        return self._get_style(float, sv.SURFACECOLORCONTRAST)

    @surface_color_contrast.setter
    def surface_color_contrast(self, value):
        self._set_style(float(value), sv.SURFACECOLORCONTRAST)

    @property
    def direction(self):
        """`tuple`: :math:`(x, y, z)` direction of the light rays.

        The direction is in the view coordinate system where :math:`z` goes
        into the page and the origin of :math:`(x, y)` is in the lower left
        corner. The default is :math:`(-0.2, -0.2, 0.959)`::

            >>> plot.light_source.direction = (0, -0.7, 0.9)
        """
        return session.XYZ(self, sv.XYZDIRECTION)

    @direction.setter
    def direction(self, values):
        session.XYZ(self, sv.XYZDIRECTION)[:] = values

    @property
    def force_gouraud_for_contour_flood(self):
        """`bool`: Force gouraud effects for shaded continuous flooding.

        Example usage::

            >>> plot.light_source.force_gouraud_for_contour_flood = True
        """
        return self._get_style(bool, sv.FORCEGOURAUDFOR3DCONTFLOOD)

    @force_gouraud_for_contour_flood.setter
    def force_gouraud_for_contour_flood(self, value):
        self._set_style(bool(value), sv.FORCEGOURAUDFOR3DCONTFLOOD)

    @property
    def force_paneled_for_cell_flood(self):
        """`bool`: Force paneled effects for shaded cell flooding.

        Example usage::

            >>> plot.light_source.force_paneled_for_cell_flood = True
        """
        return self._get_style(bool, sv.FORCEPANELEDFOR3DCELLFLOOD)

    @force_paneled_for_cell_flood.setter
    def force_paneled_for_cell_flood(self, value):
        self._set_style(bool(value), sv.FORCEPANELEDFOR3DCELLFLOOD)
