.. _annotation:

Annotations
===========

..  contents::
    :local:
    :depth: 2


Text
----

..  contents::
    :local:
    :depth: 2

.. py:currentmodule:: tecplot.annotation

Text
^^^^

.. autoclass:: Text

    **Attributes**

    .. autosummary::
        :nosignatures:

        anchor
        angle
        attached_map_index
        box
        clipping
        color
        font
        line_spacing
        position
        position_coordinate_system
        scope
        text_string
        type

.. autoattribute:: Text.anchor
.. autoattribute:: Text.angle
.. autoattribute:: Text.attached_map_index
.. autoattribute:: Text.box
.. autoattribute:: Text.clipping
.. autoattribute:: Text.color
.. autoattribute:: Text.font
.. autoattribute:: Text.line_spacing
.. autoattribute:: Text.position
.. autoattribute:: Text.position_coordinate_system
.. autoattribute:: Text.scope
.. autoattribute:: Text.text_string
.. autoattribute:: Text.type

.. py:currentmodule:: tecplot.annotation

TextBox
^^^^^^^

.. autoclass:: TextBox

    **Attributes**

    .. autosummary::
        :nosignatures:

        color
        corner_locations
        fill_color
        line_thickness
        margin
        type

.. autoattribute:: TextBox.color
.. autoattribute:: TextBox.corner_locations
.. autoattribute:: TextBox.fill_color
.. autoattribute:: TextBox.line_thickness
.. autoattribute:: TextBox.margin
.. autoattribute:: TextBox.type

.. py:currentmodule:: tecplot.annotation

TextFont
^^^^^^^^

.. autoclass:: TextFont

    **Attributes**

    .. autosummary::
        :nosignatures:

        bold
        italic
        size
        size_units
        typeface

.. autoattribute:: TextFont.bold
.. autoattribute:: TextFont.italic
.. autoattribute:: TextFont.size
.. autoattribute:: TextFont.size_units
.. autoattribute:: TextFont.typeface

.. _geometry:

Geometric Shapes
----------------

.. py:currentmodule:: tecplot.annotation

Circle
^^^^^^

.. autoclass:: Circle

    **Attributes**

    .. autosummary::
        :nosignatures:

        attached_map_index
        clipping
        color
        draw_order
        fill_color
        line_pattern
        line_thickness
        macro_function
        num_points
        pattern_length
        position
        position_coordinate_system
        radius
        scope
        type

.. autoattribute:: Circle.attached_map_index
.. autoattribute:: Circle.clipping
.. autoattribute:: Circle.color
.. autoattribute:: Circle.draw_order
.. autoattribute:: Circle.fill_color
.. autoattribute:: Circle.line_pattern
.. autoattribute:: Circle.line_thickness
.. autoattribute:: Circle.macro_function
.. autoattribute:: Circle.num_points
.. autoattribute:: Circle.pattern_length
.. autoattribute:: Circle.position
.. autoattribute:: Circle.position_coordinate_system
.. autoattribute:: Circle.radius
.. autoattribute:: Circle.scope
.. autoattribute:: Circle.type

.. py:currentmodule:: tecplot.annotation

Ellipse
^^^^^^^

.. autoclass:: Ellipse

    **Attributes**

    .. autosummary::
        :nosignatures:

        attached_map_index
        clipping
        color
        draw_order
        fill_color
        line_pattern
        line_thickness
        macro_function
        num_points
        pattern_length
        position
        position_coordinate_system
        scope
        size
        type

.. autoattribute:: Ellipse.attached_map_index
.. autoattribute:: Ellipse.clipping
.. autoattribute:: Ellipse.color
.. autoattribute:: Ellipse.draw_order
.. autoattribute:: Ellipse.fill_color
.. autoattribute:: Ellipse.line_pattern
.. autoattribute:: Ellipse.line_thickness
.. autoattribute:: Ellipse.macro_function
.. autoattribute:: Ellipse.num_points
.. autoattribute:: Ellipse.pattern_length
.. autoattribute:: Ellipse.position
.. autoattribute:: Ellipse.position_coordinate_system
.. autoattribute:: Ellipse.scope
.. autoattribute:: Ellipse.size
.. autoattribute:: Ellipse.type

.. py:currentmodule:: tecplot.annotation

Rectangle
^^^^^^^^^

.. autoclass:: Rectangle

    **Attributes**

    .. autosummary::
        :nosignatures:

        attached_map_index
        clipping
        color
        draw_order
        fill_color
        line_pattern
        line_thickness
        macro_function
        pattern_length
        position
        position_coordinate_system
        scope
        size
        type

.. autoattribute:: Rectangle.attached_map_index
.. autoattribute:: Rectangle.clipping
.. autoattribute:: Rectangle.color
.. autoattribute:: Rectangle.draw_order
.. autoattribute:: Rectangle.fill_color
.. autoattribute:: Rectangle.line_pattern
.. autoattribute:: Rectangle.line_thickness
.. autoattribute:: Rectangle.macro_function
.. autoattribute:: Rectangle.pattern_length
.. autoattribute:: Rectangle.position
.. autoattribute:: Rectangle.position_coordinate_system
.. autoattribute:: Rectangle.scope
.. autoattribute:: Rectangle.size
.. autoattribute:: Rectangle.type

.. py:currentmodule:: tecplot.annotation

Square
^^^^^^

.. autoclass:: Square

    **Attributes**

    .. autosummary::
        :nosignatures:

        attached_map_index
        clipping
        color
        draw_order
        fill_color
        line_pattern
        line_thickness
        macro_function
        pattern_length
        position
        position_coordinate_system
        scope
        size
        type

.. autoattribute:: Square.attached_map_index
.. autoattribute:: Square.clipping
.. autoattribute:: Square.color
.. autoattribute:: Square.draw_order
.. autoattribute:: Square.fill_color
.. autoattribute:: Square.line_pattern
.. autoattribute:: Square.line_thickness
.. autoattribute:: Square.macro_function
.. autoattribute:: Square.pattern_length
.. autoattribute:: Square.position
.. autoattribute:: Square.position_coordinate_system
.. autoattribute:: Square.scope
.. autoattribute:: Square.size
.. autoattribute:: Square.type

.. py:currentmodule:: tecplot.annotation

Polyline2D
^^^^^^^^^^

.. autoclass:: Polyline2D

    **Attributes**

    .. autosummary::
        :nosignatures:

        arrowhead
        attached_map_index
        clipping
        color
        draw_order
        fill_color
        line_pattern
        line_thickness
        macro_function
        pattern_length
        position
        position_coordinate_system
        scope
        type

.. autoattribute:: Polyline2D.arrowhead
.. autoattribute:: Polyline2D.attached_map_index
.. autoattribute:: Polyline2D.clipping
.. autoattribute:: Polyline2D.color
.. autoattribute:: Polyline2D.draw_order
.. autoattribute:: Polyline2D.fill_color
.. autoattribute:: Polyline2D.line_pattern
.. autoattribute:: Polyline2D.line_thickness
.. autoattribute:: Polyline2D.macro_function
.. autoattribute:: Polyline2D.pattern_length
.. autoattribute:: Polyline2D.position
.. autoattribute:: Polyline2D.position_coordinate_system
.. autoattribute:: Polyline2D.scope
.. autoattribute:: Polyline2D.type

.. py:currentmodule:: tecplot.annotation

Polyline3D
^^^^^^^^^^

.. autoclass:: Polyline3D

    **Attributes**

    .. autosummary::
        :nosignatures:

        attached_map_index
        color
        fill_color
        line_pattern
        line_thickness
        macro_function
        pattern_length
        scope
        type

.. autoattribute:: Polyline3D.attached_map_index
.. autoattribute:: Polyline3D.color
.. autoattribute:: Polyline3D.fill_color
.. autoattribute:: Polyline3D.line_pattern
.. autoattribute:: Polyline3D.line_thickness
.. autoattribute:: Polyline3D.macro_function
.. autoattribute:: Polyline3D.pattern_length
.. autoattribute:: Polyline3D.scope
.. autoattribute:: Polyline3D.type

.. py:currentmodule:: tecplot.annotation

MultiPolyline2D
^^^^^^^^^^^^^^^

.. autoclass:: MultiPolyline2D

    **Attributes**

    .. autosummary::
        :nosignatures:

        arrowhead
        attached_map_index
        clipping
        color
        draw_order
        fill_color
        line_pattern
        line_thickness
        macro_function
        pattern_length
        position
        position_coordinate_system
        scope
        type

.. autoattribute:: MultiPolyline2D.arrowhead
.. autoattribute:: MultiPolyline2D.attached_map_index
.. autoattribute:: MultiPolyline2D.clipping
.. autoattribute:: MultiPolyline2D.color
.. autoattribute:: MultiPolyline2D.draw_order
.. autoattribute:: MultiPolyline2D.fill_color
.. autoattribute:: MultiPolyline2D.line_pattern
.. autoattribute:: MultiPolyline2D.line_thickness
.. autoattribute:: MultiPolyline2D.macro_function
.. autoattribute:: MultiPolyline2D.pattern_length
.. autoattribute:: MultiPolyline2D.position
.. autoattribute:: MultiPolyline2D.position_coordinate_system
.. autoattribute:: MultiPolyline2D.scope
.. autoattribute:: MultiPolyline2D.type

.. py:currentmodule:: tecplot.annotation

MultiPolyline3D
^^^^^^^^^^^^^^^

.. autoclass:: MultiPolyline3D

    **Attributes**

    .. autosummary::
        :nosignatures:

        attached_map_index
        color
        fill_color
        line_pattern
        line_thickness
        macro_function
        pattern_length
        scope
        type

.. autoattribute:: MultiPolyline3D.attached_map_index
.. autoattribute:: MultiPolyline3D.color
.. autoattribute:: MultiPolyline3D.fill_color
.. autoattribute:: MultiPolyline3D.line_pattern
.. autoattribute:: MultiPolyline3D.line_thickness
.. autoattribute:: MultiPolyline3D.macro_function
.. autoattribute:: MultiPolyline3D.pattern_length
.. autoattribute:: MultiPolyline3D.scope
.. autoattribute:: MultiPolyline3D.type

.. py:currentmodule:: tecplot.annotation

Arrowhead
^^^^^^^^^

.. autoclass:: Arrowhead

    **Attributes**

    .. autosummary::
        :nosignatures:

        angle
        attachment
        size
        style

.. autoattribute:: Arrowhead.angle
.. autoattribute:: Arrowhead.attachment
.. autoattribute:: Arrowhead.size
.. autoattribute:: Arrowhead.style

Images
------

.. py:currentmodule:: tecplot.annotation

Image
^^^^^

.. autoclass:: Image

    **Attributes**

    .. autosummary::
        :nosignatures:

        attached_map_index
        draw_order
        filename
        height
        macro_function
        maintain_aspect_ratio
        position
        position_coordinate_system
        raw_size
        resize_filter
        scope
        size
        type
        width

    **Methods**

    .. autosummary::

        reset_aspect_ratio

.. autoattribute:: Image.attached_map_index
.. autoattribute:: Image.draw_order
.. autoattribute:: Image.filename
.. autoattribute:: Image.height
.. autoattribute:: Image.macro_function
.. autoattribute:: Image.maintain_aspect_ratio
.. autoattribute:: Image.position
.. autoattribute:: Image.position_coordinate_system
.. autoattribute:: Image.raw_size
.. automethod:: Image.reset_aspect_ratio
.. autoattribute:: Image.resize_filter
.. autoattribute:: Image.scope
.. autoattribute:: Image.size
.. autoattribute:: Image.type
.. autoattribute:: Image.width

.. py:currentmodule:: tecplot.annotation

GeoreferencedImage
^^^^^^^^^^^^^^^^^^

.. autoclass:: GeoreferencedImage

    **Attributes**

    .. autosummary::
        :nosignatures:

        attached_map_index
        macro_function
        scope
        type
        z

.. autoattribute:: GeoreferencedImage.attached_map_index
.. autoattribute:: GeoreferencedImage.macro_function
.. autoattribute:: GeoreferencedImage.scope
.. autoattribute:: GeoreferencedImage.type
.. autoattribute:: GeoreferencedImage.z
