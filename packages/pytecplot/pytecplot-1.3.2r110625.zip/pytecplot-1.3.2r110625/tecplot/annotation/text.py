import collections

from ..tecutil import _tecutil
from .. import constant, tecutil
from ..exception import TecplotSystemError


@tecutil.lock_attributes
class TextFont(object):
    """Typeface and font settings for a `Text` object."""
    def __init__(self, text):
        self.text = text
        self.uid = self.text.uid
        self.frame = self.text.frame

    @property
    def typeface(self):
        """`str`: The font family used by the `Text` object.

        For consistency across various platforms, |Tecplot 360| guarantees that
        the following standard typeface names are available:

            * "Helvetica"
            * "Times"
            * "Courier"
            * "Greek"
            * "Math"
            * "User Defined"

        Other typefaces may or may not be available depending on the TrueType
        fonts available. If the typeface or style is not available, a suitable
        replacement will be selected. This example shows how to set the
        typeface of a `Text` object to 'Times'::

            >>> text = frame.add_text('abc')
            >>> text.font.typeface = 'Times'
        """
        with self.frame.activated():
            return _tecutil.TextGetTypefaceFamily(self.uid)

    @typeface.setter
    @tecutil.lock()
    def typeface(self, value):
        with self.frame.activated():
            _tecutil.TextSetTypeface(self.uid, str(value), self.bold,
                                     self.italic)

    @property
    def bold(self):
        """`bool`: Use bold typeface in the `Text` object.

        Example showing how to set the bold property of a `Text` object::

            >>> text = frame.add_text('abc')
            >>> text.font.bold = True
        """
        with self.frame.activated():
            return _tecutil.TextGetTypefaceIsBold(self.uid)

    @bold.setter
    @tecutil.lock()
    def bold(self, value):
        with self.frame.activated():
            _tecutil.TextSetTypeface(self.uid, self.typeface, bool(value),
                                     self.italic)

    @property
    def italic(self):
        """`bool`: Use italic typeface of the `Text` object.

        Example showing how to set the italic property of a `Text` object::

            >>> text = frame.add_text('abc')
            >>> text.font.italic = True
        """
        with self.frame.activated():
            return _tecutil.TextGetTypefaceIsItalic(self.uid)

    @italic.setter
    @tecutil.lock()
    def italic(self, value):
        with self.frame.activated():
            _tecutil.TextSetTypeface(self.uid, self.typeface, self.bold,
                                     bool(value))

    @property
    def size(self):
        """`int`: The text size in the currently defined text size units.

        Example showing how to set the text size of a `Text` object::

            >>> text = frame.add_text('abc')
            >>> text.font.size_units = tecplot.constant.Units.Point
            >>> text.font.size = 14
        """
        with self.frame.activated():
            return _tecutil.TextGetHeight(self.uid)

    @size.setter
    @tecutil.lock()
    def size(self, value):
        with self.frame.activated():
            _tecutil.TextSetHeight(self.uid, float(value))

    @property
    def size_units(self):
        """`Units`: Units of the text character height.

        `Units` may be one of the following:

            * `Units.Point`: Specify character height in points.
            * `Units.Frame`: Specify character height as a percentage of frame
                height
            * `Units.Grid`: Specify character height in grid units.

        (default = `Units.Point`)

        .. note::
            * One point is 1/72nd of an inch.
            * `Units.Grid` is available only if position_coordinate_system is
                `CoordSys.Grid`
            * The position coordinate system will be changed to `CoordSys.Grid`
                if size units is set to `Units.Grid`

        Example showing how to set the units of the character height for a
        `Text` object::

            >>> from tecplot.constant import CoordSys
            >>> text = frame.add_text("abc")
            >>> text.position_coordinate_system = CoordSys.Grid
            >>> text.font.size_units = Units.Point
        """
        with self.frame.activated():
            return constant.Units(_tecutil.TextGetSizeUnits(self.uid))

    @size_units.setter
    @tecutil.lock()
    def size_units(self, value):
        with self.frame.activated():
            size = self.size
            size_units = constant.Units(value)
            if size_units == constant.Units.Grid:
                # if units == grid, then coord-sys must be grid
                coord_sys = constant.CoordSys.Grid
            else:
                coord_sys = self.text.position_coordinate_system
            _tecutil.TextSetCoordSysAndUnits(self.uid, coord_sys.value,
                                             size_units.value)
            self.size = size


@tecutil.lock_attributes
class TextBox(object):
    """The box surrounding a `Text` object."""
    def __init__(self, text):
        self.text = text
        self.uid = self.text.uid
        self.frame = self.text.frame

    @property
    def line_thickness(self):
        """`float`: Border line thickness.

        Must be  greater than 0, default: ``0.1``. Example showing how to set
        the line thickness of the `text box <annotation.TextBox>`::

            >>> text = frame.add_text("abc")
            >>> text.box.line_thickness = 0.5
        """
        with self.frame.activated():
            return _tecutil.TextBoxGetLineThickness(self.uid)

    @line_thickness.setter
    @tecutil.lock()
    def line_thickness(self, value):
        with self.frame.activated():
            _tecutil.TextBoxSetLineThickness(self.uid, float(value))

    @property
    def margin(self):
        """`float`: Margin between the text and the surrounding border.

        Specify the margin as a percentage of the text character height. Margin
        must be greater than or equal to 0.0, and may be greater than 100.
        (default = 20.0)

        Example showing how to set the margin of the `text box <TextBox>` for a
        `Text` object::

            >>> text = frame.add_text("abc")
            >>> text.box.type = tecplot.constant.TextBox.Filled
            >>> text.box.margin = 0.5
        """
        with self.frame.activated():
            return _tecutil.TextBoxGetMargin(self.uid)

    @margin.setter
    @tecutil.lock()
    def margin(self, margin):
        with self.frame.activated():
            _tecutil.TextBoxSetMargin(self.uid, float(margin))

    @property
    def fill_color(self):
        """`Color`: Background fill color of the text box.

        Example showing how to set the fill color of the `text box <TextBox>`
        for a `Text` object::

            >>> text = frame.add_text("abc")
            >>> text.box.type = TextBox.Filled
            >>> text.box.fill_color = tecplot.constant.Color.Blue
        """
        return constant.Color(_tecutil.TextBoxGetFillColor(self.uid))

    @fill_color.setter
    @tecutil.lock()
    def fill_color(self, color):
        with self.frame.activated():
            _tecutil.TextBoxSetFillColor(self.uid, constant.Color(color).value)

    @property
    def color(self):
        """`Color`: Border line color of the text box.

        Default: `Color.Black`. Example showing how to set the outline color of
        the `text box <TextBox>` for a `Text` object::

            >>> from tecplot.constant import Color, TextBox
            >>> text = frame.add_text("abc")
            >>> text.box.type = TextBox.Filled
            >>> text.box.color = Color.Blue
        """
        return constant.Color(_tecutil.TextBoxGetColor(self.uid))

    @color.setter
    @tecutil.lock()
    def color(self, color):
        with self.frame.activated():
            _tecutil.TextBoxSetColor(self.uid, constant.Color(color).value)

    _Pos = collections.namedtuple('TextBoxPos', 'x1 y1 x2 y2 x3 y3 x4 y4')

    @property
    def corner_locations(self):
        """`tuple`: Position of the four corners of the `text box <TextBox>`.

        **Note:** This property is read-only.

        The tuple consists of 8 `floats <float>`:

            * x1: X-Coordinate for bottom left corner
            * y1: Y-Coordinate for bottom left corner
            * x2: X-Coordinate for bottom right corner
            * y2: Y-Coordinate for bottom right corner
            * x3: X-Coordinate for upper right corner
            * y3: Y-Coordinate for upper right corner
            * x4: X-Coordinate for upper left corner
            * y4: Y-Coordinate for upper left corner

        There is no default, position will vary with text box properties.
        Example showing how to query position of the `text box <TextBox>` for a
        `Text` object. The values ``x1, ..., y4``` contain the corners
        of the text box::

            >>> text = frame.add_text("abc")
            >>> text.box.type = tecplot.constant.TextBox.Filled
            >>> x1,y1,x2,y2,x3,y3,x4,y4 = text.box.corner_locations
        """
        with self.frame.activated():
            return TextBox._Pos(*_tecutil.TextBoxGetPosition(self.uid))

    @property
    def position(self):
        tecutil.api_moved('TextBox.position', 'TextBox.corner_locations',
                          '0.13', '2018 R2')

    @property
    def type(self):
        """`constant.TextBox`: Style of the text box fill area and border.

        The text box type can be set to the following:

            * None\_ - (default) No box is drawn around the text.
            * Filled - A filled box around the text which is opaque. if you
                place it over another |Tecplot 360| object, the underlying
                object cannot be seen.
            * Hollow - A plain box around the text.

        Example showing how to set the type of the text box for a `TextBox`
        object::

            >>> text = frame.add_text("abc")
            >>> text.box.type = tecplot.constant.TextBox.Filled
        """
        return constant.TextBox(_tecutil.TextBoxGetType(self.uid))

    @type.setter
    @tecutil.lock()
    def type(self, value):
        _tecutil.TextBoxSetType(self.uid, constant.TextBox(value).value)


@tecutil.lock_attributes
class Text(object):
    """Text annotation."""
    def __init__(self, uid, frame):
        self.uid = uid
        self.frame = frame

    def __str__(self):
        """String representation of the text.

        Example::

            >>> print(frame.add_text('Orange'))
            Orange
        """
        return self.text_string

    def __eq__(self, other):
        """Checks for `Text` equality in the |Tecplot Engine|.

        Returns:
            `bool`: `True` if the unique ID numbers are the same for both
            `Text objects <Text>`.

        This example shows how the literal strings that the `Text` objects hold
        are equal, but the `Text` objects themselves are different::

            >>> text1 = frame.add_text('Orange')
            >>> text2 = frame.add_text('Orange')
            >>> text1.text_string == text2.text_string
            True
            >>> text1 == text2
            False
        """
        return self.uid == other.uid

    def __ne__(self, other):
        """Checks for `Text` inequality in the |Tecplot Engine|.

        Returns:
            `bool`: `True` if the unique ID numbers are not the same for both
            `Text objects <Text>`

        This example shows how the literal strings that the `Text` objects hold
        are equal, but the `Text` objects themselves are different::

            >>> text1 = frame.add_text('Orange')
            >>> text2 = frame.add_text('Orange')
            >>> text1.text_string != text2.text_string
            False
            >>> text1 != text2
            True
        """
        return self.uid != other.uid

    @property
    def type(self):
        r"""`TextType`: Normal or LaTeX text type setting.

        Possible values are `TextType.Regular` or `TextType.LaTeX`::

            >>> text = frame.add_text(r'\alpha')
            >>> text.type = TextType.LaTeX
        """
        return _tecutil.TextGetType(self.uid)

    @type.setter
    @tecutil.lock()
    def type(self, value):
        _tecutil.TextSetType(self.uid, constant.TextType(value).value)

    @property
    def box(self):
        """`annotation.TextBox`: The frame and area around this `Text` object.

        The text box is a rectangular frame drawn around the text. Note that in
        order to show the text box, you must set TextBox.type to a value other
        than `constant.TextBox.None_`.

       Example showing how to enable the text box for a `Text` object::

            >>> text = frame.add_text("abc")
            >>> text.box.type = tecplot.constant.TextBox.Filled
        """
        return TextBox(self)

    @property
    def text_box(self):
        tecutil.api_moved('Text.text_box', 'Text.box', '0.13', '2018 R2')

    @property
    def font(self):
        """`TextFont`: Typeface properties for a `Text` object.

        Example usage::

            >>> text = frame.add_text('abc')
            >>> text.font.typeface = 'Times'
        """
        return TextFont(self)

    @property
    def anchor(self):
        """`TextAnchor`: Anchor location of this `Text` object.

        Specify the anchor point, or fixed point, for the text object.
        As the text object grows or shrinks, the anchor location is fixed,
        while the rest of the box adjusts to accommodate the new size.
        (default = `TextAnchor.Left`)

        There are nine possible anchor position points, corresponding to the
        left, right, and center positions on the headline, midline,
        and baseline of the text box.

        Example showing how to set the anchor of a `Text` object::

            >>> text = frame.add_text('abc')
            >>> text.anchor = tecplot.constant.TextAnchor.Center

        .. seealso:: `Text.position`
        """
        with self.frame.activated():
            return _tecutil.TextGetAnchor(self.uid)

    @anchor.setter
    @tecutil.lock()
    def anchor(self, value):
        with self.frame.activated():
            _tecutil.TextSetAnchor(self.uid, constant.TextAnchor(value).value)

    @property
    def angle(self):
        """`float` (degrees counter-clockwise): Angle of the text box in degrees.

        The text angle is the orientation of the text relative to the axis.
        The angle is measured in degrees counter-clockwise from horizontal.
        Horizontal text is at zero degrees; vertical text is at 90 degrees.

        Example showing how to set the angle of a `Text` object::

            >>> text = frame.add_text('abc')
            >>> text.angle = 45
        """
        with self.frame.activated():
            return _tecutil.TextGetAngle(self.uid)

    @angle.setter
    @tecutil.lock()
    def angle(self, value):
        with self.frame.activated():
            _tecutil.TextSetAngle(self.uid, float(value))

    @property
    def position_coordinate_system(self):
        """`CoordSys`: Position coordinate system of the `Text` object.

        The text object may be positioned using either the grid coordinate
        system or the frame coordinate system and must be one of
        `CoordSys.Frame` or `CoordSys.Grid`

        If the position_coordinate_system is `CoordSys.Frame`, then the
        size_units property must be `Units.Frame` or `Units.Point`.

        The text object's position and text height are adjusted so that it
        remains identical to its visual appearance in the original
        coordinate and unit system.

        If the size units are `Units.Grid` and the position coordinate system
        is changed to `CoordSys.Frame`, then the size units will be changed
        to `Units.Frame`. (default = CoordSys.Frame)

        Example showing how to set the position coordinate system
        for a `Text` object::

            >>> from tecplot.constant import CoordSys
            >>> text = frame.add_text("abc")
            >>> text.position_coordinate_system = CoordSys.Grid

        Example showing side effect if size units are `CoordSys.Grid` and
        the coordinate system is changed to `CoordSys.Frame`::

            >>> from tecplot.constant import CoordSys, Units
            >>> text = frame.add_text("abc")
            >>> text.font.size_units = Units.Grid
            >>> text.position_coordinate_system = CoordSys.Frame
            >>> text.position_coordinate_system
            CoordSys.Frame
            >>> text.font.size_units
            Units.Frame
        """
        with self.frame.activated():
            result = _tecutil.TextGetPositionCoordSys(self.uid)
            return constant.CoordSys(result)

    @position_coordinate_system.setter
    @tecutil.lock()
    def position_coordinate_system(self, value):
        with self.frame.activated():
            coord_sys = constant.CoordSys(value)
            size_units = self.font.size_units
            if (
                coord_sys == constant.CoordSys.Frame and
                size_units == constant.Units.Grid
            ):
                # if coord-sys is frame, then units can not be grid
                size_units = constant.Units.Frame
            _tecutil.TextSetCoordSysAndUnits(self.uid, coord_sys.value,
                                             size_units.value)

    @property
    def line_spacing(self):
        """`float` (default = 1.0): Spacing between lines in the text box.

        Line spacing is dependent on the height of the text and the size unit
        system in which it is drawn. This example shows how to set the line
        spacing of a `Text` object::

            >>> text = frame.add_text('abc')
            >>> text.line_spacing = 4
        """
        with self.frame.activated():
            return _tecutil.TextGetLineSpacing(self.uid)

    @line_spacing.setter
    @tecutil.lock()
    def line_spacing(self, line_spacing):
        with self.frame.activated():
            _tecutil.TextSetLineSpacing(self.uid, float(line_spacing))

    @property
    def text_string(self):
        """`str`: The text to be displayed in a text box.

        You can embed Greek, Math, and User-defined characters into
        English-font strings by enclosing them with text formatting tags,
        together with the keyboard characters.

        The text formatting tags and their effects are as follows. Format tags
        are not case sensitive and may be either upper or lower case:

            * <b>...</b> - Boldface
            * <i>...</i> - Italic
            * <verbatim>...</verbatim> - Verbatim
            * <sub>...</sub> - Subscripts
            * <sup>...</sup> - Superscripts
            * <greek>...</greek> - Greek font.
            * <math>...</math> - Math font.
            * <userdef>...</userdef> - User-defined font.
            * <helvetica>...</helvetica> - Helvetica font.
            * <times>...</times> - Times font.
            * <courier>...</courier> - Courier font.

        Not all fonts have Bold and/or Italic variants. For fonts that do not
        have these styles, the <b> and/or <i> tags may have no effect.

        Embedding and escaping special characters work only in English-font
        text; they have no effect in text created in Greek, Math, or
        User-defined character sets.

        You can produce subscripts or superscripts by enclosing any characters
        with <sub>...</sub> or <sup>...</sup>, respectively. |Tecplot 360| has
        only one level of superscripts and subscripts. Expressions requiring
        additional levels must be created by hand using multiple text objects.
        If you alternate subscripts and superscripts, |Tecplot 360| positions
        the superscript directly above the subscript. To produce consecutive
        superscripts, enclose all superscript characters in a single pair of
        tags.

        To insert a tag into text literally, precede the first angle bracket
        with a backslash ("\"). To insert a backslash in the text, just type
        two backslashes ("\\"). This example shows how to set the text string
        of a `Text` object::

            >>> text = frame.add_text('abc')
            >>> text.text_string
            'abc'
            >>> text.text_string ='def'
            >>> text.text_string
            'def'
        """
        with self.frame.activated():
            success, text_string = _tecutil.TextGetString(self.uid)
            if not success:
                raise TecplotSystemError()
            return text_string

    @text_string.setter
    @tecutil.lock()
    def text_string(self, value):
        with self.frame.activated():
            _tecutil.TextSetString(self.uid, str(value))

    @property
    @tecutil.lock()
    def position(self):
        r"""`tuple`: Anchor position of the `Text`.

        This is the position of the `Text` on the `Frame` and will be
        :math:`(x,y)` or :math:`(\theta,r)` depending on the plot type
        (Cartesian or polar). This example shows how to set the anchor position
        of a `Text` object::

            >>> text = frame.add_text("abc")
            >>> text.position = (1.0, 2.0)

        .. seealso:: `Text.anchor`
        """
        with self.frame.activated():
            pos = _tecutil.TextGetAnchorPos(self.uid)
            if self.position_coordinate_system == constant.CoordSys.Grid3D:
                return tecutil.XYZ(*pos)
            else:
                return tecutil.XY(*pos[:2])

    @position.setter
    @tecutil.lock()
    def position(self, values):
        pos = tecutil.XYZ(*[float(x) for x in values])
        with self.frame.activated():
            _tecutil.TextSetAnchorPos(self.uid, pos.x or 0., pos.y or 0.,
                                      pos.z or 0.)

    @property
    def anchor_position(self):
        tecutil.api_moved('Text.anchor_position', 'Text.position',
                          '0.13', '2018 R2')

    @anchor_position.setter
    def anchor_position(self, values):
        tecutil.api_moved('Text.anchor_position', 'Text.position',
                          '0.13', '2018 R2')

    @property
    def scope(self):
        """`Scope`: The `Scope` (local or global) of the `Text`.

        `Annotations <Annotation>` with local scope are displayed only in the
        `frame <Frame>` in which they are created. If the `annotation
        <Annotation>` is defined as having `global <Scope.Global>` scope, it
        will appear in all "like" `frames <Frame>`. That is, those frames using
        the same data set as the one in which the `annotation <Annotation>` was
        created. (default: `Scope.Local`)

        Example showing how to set the scope of a `Text` object::

            >>> text = frame.add_text("abc")
            >>> text.scope = tecplot.constant.Scope.Global
        """
        return constant.Scope(_tecutil.TextGetScope(self.uid))

    @scope.setter
    @tecutil.lock()
    def scope(self, scope):
            _tecutil.TextSetScope(self.uid, constant.Scope(scope).value)

    @property
    def attached_map_index(self):
        """`Index` or `None`: Index of the attached fieldmap or linemap.

        Example showing how to set the attached object `Index` of a `Text`
        object::

            >>> text = frame.add_text("abc")
            >>> text.attached_map_index = 1
        """
        with self.frame.activated():
            if _tecutil.TextIsAttached(self.uid):
                return tecutil.Index(_tecutil.TextGetZoneOrMap(self.uid) - 1)

    @attached_map_index.setter
    @tecutil.lock()
    def attached_map_index(self, value):
        with self.frame.activated():
            if value is None:
                _tecutil.TextSetAttached(self.uid, False)
            else:
                _tecutil.TextSetAttached(self.uid, True)
                _tecutil.TextSetZoneOrMap(self.uid, tecutil.Index(value) + 1)

    @property
    def zone_or_map(self):
        tecutil.api_moved('Text.zone_or_map', 'Text.attached_map_index',
                          '0.13', '2018 R2')

    @zone_or_map.setter
    def zone_or_map(self, value):
        tecutil.api_moved('Text.zone_or_map', 'Text.attached_map_index',
                          '0.13', '2018 R2')

    @property
    def color(self):
        """`Color`: `Color` of the `Text` object.

        Default: `Color.Black`. Example showing how to set the `Color` of a
        `Text` object::

            >>> text = frame.add_text("abc")
            >>> text.color = tecplot.constant.Color.Blue
        """
        return constant.Color(_tecutil.TextGetColor(self.uid))

    @color.setter
    @tecutil.lock()
    def color(self, color):
        with self.frame.activated():
            _tecutil.TextSetColor(self.uid, constant.Color(color).value)

    @property
    def clipping(self):
        """`Clipping`: `Clipping` properties of the `Text`

        Clipping refers to displaying only that portion of an object that falls
        within a specified clipping region of the plot. If you have specified
        your text position in the Frame coordinate system, the `Text`
        will be clipped to the frame. Default: `Clipping.ClipToViewport`.

        If you have specified the Grid coordinate system, you can choose to
        clip your `Text` to the frame or the viewport. The size of the
        viewport depends on the plot type as follows:

            * 3D Cartesian - The viewport is the same as the frame, so viewport
                clipping is the same as frame clipping.
            * 2D Cartesian/XY Line - The viewport is defined by the extents of
                the X and Y axes.
            * Polar Line/Sketch - By default, the viewport is the same as the
                frame.

        Example showing how to set the clipping of a `Text`::

            >>> text = frame.add_text('abc')
            >>> text.clipping = tecplot.constant.Clipping.ClipToFrame
        """
        with self.frame.activated():
            return constant.Clipping(_tecutil.TextGetClipping(self.uid))

    @clipping.setter
    @tecutil.lock()
    def clipping(self, clipping):
        with self.frame.activated():
            _tecutil.TextSetClipping(self.uid,
                                     constant.Clipping(clipping).value)
