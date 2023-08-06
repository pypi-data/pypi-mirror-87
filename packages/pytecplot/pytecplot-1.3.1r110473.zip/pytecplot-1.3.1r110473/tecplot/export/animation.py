import os

from ..tecutil import _tecutil
from ..constant import *
from ..exception import *
from .. import tecutil, version

from .export_setup import ExportSetup
from .print_setup import PrintSetup


class animation(object):
    r'''Frame-by-frame animation context.'''
    def __init__(self, filename, width=800, animation_speed=10,
                 region=ExportRegion.AllFrames, supersample=3,
                 compression=None, image_type=None,
                 multiple_color_tables=False, format_options=None,
                 convert_to_256_colors=None, jpeg_encoding=None, quality=None,
                 gray_scale_depth=None, tiff_byte_order=None, format=None):
        if __debug__:
            if (
                compression is not None and
                format not in [ExportFormat.AVI, ExportFormat.Flash]
            ):
                msg = 'Compression only supported for AVI and Flash animations.'
                msg += ' compression: {}   format: {}'.format(compression,
                                                              format)
                raise TecplotLogicError(msg)
            if (
                image_type is not None and
                format != ExportFormat.Flash
            ):
                msg = 'Image-type only supported for Flash animations.'
                raise TecplotLogicError(msg)
        _ext = {
            'avi': ExportFormat.AVI,
            'mp4': ExportFormat.MPEG4,
            'mpeg': ExportFormat.MPEG4,
            'f4v': ExportFormat.Flash,
            'flv': ExportFormat.Flash,
            'swf': ExportFormat.Flash,
            'rm': ExportFormat.RasterMetafile,
            'wmv': ExportFormat.WMV,

            # image formats
            'bmp': ExportFormat.BMP,
            'jpeg': ExportFormat.JPEG,
            'png': ExportFormat.PNG,
            'tiff': ExportFormat.TIFF,
        }
        if format is None:
            format = _ext.get(os.path.splitext(filename)[-1].split('.')[-1],
                              ExportFormat.MPEG4)
        self.format = ExportFormat(format)

        if version.sdk_version_info < (2017, 3):
            if self.format in [ExportFormat.MPEG4, ExportFormat.WMV]:
                msg = 'Animation export using FFmpeg is not supported via' + \
                      ' PyTecplot with Tecplot 360 2017 R2 and earlier.' + \
                      ' Please update your installation of Tecplot 360.'
                raise TecplotOutOfDateEngineError((2017, 3), msg)

        self.filename = filename
        self.width = width
        self.animation_speed = animation_speed
        self.region = region
        self.supersample = supersample
        self.compression = compression
        self.image_type = image_type
        self.multiple_color_tables = multiple_color_tables
        self.format_options = format_options

        # image format options
        self.convert_to_256_colors = convert_to_256_colors
        self.jpeg_encoding = jpeg_encoding
        self.quality = quality
        self.gray_scale_depth = gray_scale_depth
        self.tiff_byte_order = tiff_byte_order

    @tecutil.lock()
    def setup(self):
        export_setup = ExportSetup()
        export_setup.reset()
        export_setup.format = self.format
        export_setup.filename = self.filename
        export_setup.width = self.width
        export_setup.animation_speed = self.animation_speed
        export_setup.region = self.region
        export_setup.supersample = self.supersample
        export_setup.multiple_color_tables = self.multiple_color_tables

        if self.format == ExportFormat.AVI:
            export_setup.avi_compression = self.compression
        elif self.format == ExportFormat.Flash:
            export_setup.flash_compression = self.compression
            export_setup.flash_image_type = self.image_type
        elif self.format == ExportFormat.MPEG4:
            export_setup.mpeg_format_options = self.format_options
        elif self.format == ExportFormat.WMV:
            export_setup.wmv_format_options = self.format_options
        elif self.format in [ExportFormat.BMP, ExportFormat.PNG]:
            export_setup.convert_to_256_colors = self.convert_to_256_colors
        elif self.format == ExportFormat.JPEG:
            export_setup.jpeg_encoding = self.jpeg_encoding
            export_setup.quality = self.quality
        elif self.format == ExportFormat.TIFF:
            export_setup.gray_scale_depth = self.gray_scale_depth
            export_setup.tiff_byte_order = self.tiff_byte_order

    @tecutil.lock()
    def __enter__(self):
        self.setup()
        if not _tecutil.ExportStart():
            raise TecplotSystemError()
        return self

    @tecutil.lock()
    def __exit__(self, *args, **kargs):
        if not _tecutil.ExportFinish():
            raise TecplotSystemError()

    @tecutil.lock()
    def export_animation_frame(self):
        """Append a frame to the current animation.

        This function is available as a method on the object returned by the
        animation contexts:

            * `animation_avi`
            * `animation_flash`
            * `animation_mpeg4`
            * `animation_raster_metafile`
            * `animation_wmv`

        It instructs Tecplot 360 to capture the current state of the plot or
        workspace (see the *region* parameter in the contexts above) as a
        single frame in the resulting animation. Typical usage is to make small
        changes to the plot, calling `animation.export_animation_frame()` after
        each change to create a smooth transition from one view to another. For
        a detailed example, see `animation_mpeg4`. The following example is an
        excerpt from the MPEG-4 example code::

            with tp.export.animation_mpeg4(outfile, **opts) as ani:
                for i in range(args.nframes):
                    view.rotate_axes(5, (1, 0, 0))
                    translate_view(view, 30 / args.nframes)
                    ani.export_animation_frame()
        """
        if not _tecutil.ExportNextFrame():
            raise TecplotSystemError()


class animation_avi(animation):
    r'''Frame-by-frame AVI animation context.

    Parameters:
        filename (`str`): The resulting video file name or path, relative to
            Python's current working directory.
        width (`int`, optional): The width of the video in pixels. (default:
            800)
        animation_speed (`int`, optional): The frame-rate of the video in
            frames per second. (default: 10)
        region (`Frame` or `ExportRegion`, optional): The rectangular area to
            be exported. This can be a specific `Frame` object or one of
            `ExportRegion.CurrentFrame`, `ExportRegion.AllFrames` (default) or
            `ExportRegion.WorkArea`.
        supersample (`int`, optional): Controls the amount of anti-aliasing
            used in each frame. Valid values are 1-16. A value of **1**
            indicates that no antialiasing will be used. Antialiasing smooths
            jagged edges on text, lines, and edges of the video output by the
            process of supersampling. *Some graphics cards* can cause Tecplot
            360 to crash when larger anti-aliasing values are used. If this
            occurs on your machine, try updating your graphics driver or using
            a lower anti-aliasing value. (default: **3**)
        compression (`AVICompression`, optional): The compression scheme to use
            when creating the video stream. Options are:
            `AVICompression.ColorPreserving` (default on Windows),
            `AVICompression.LinePreserving` or
            `AVICompression.LosslessUncompressed` (default on Linux and MacOS).
        multiple_color_tables (`bool`, optional): Create a color table for each
            frame of the animation. If `False` (default), the whole animation
            will be scanned in an attempt to create a single table of 256
            colors.

    This is a `context manager
    <https://docs.python.org/3/reference/datamodel.html#context-managers>`_ and
    must be invoked using the `with
    <https://docs.python.org/3/reference/compound_stmts.html#with>`_ statement.
    The returned object of the context manager is used to control when each
    frame of the video is captured. This is done using the context method
    `animation.export_animation_frame()` as shown in the example below, at
    which point the specified region or plot is rendered. The actual video file
    is produced upon exit of the context.

    Typical code looks like the following (see the example under
    `animation_mpeg4` for a complete working example)::

        >>> with tp.export.animation_avi('output.avi') as ani:
        ...     # make some view changes here
        ...     ani.export_animation_frame()
    '''
    def __init__(self, filename, width=800, animation_speed=10,
                 region=ExportRegion.AllFrames, supersample=3,
                 compression=None, multiple_color_tables=False):
        animation.__init__(self, filename=filename, width=width,
                           animation_speed=animation_speed, region=region,
                           supersample=supersample, compression=compression,
                           multiple_color_tables=multiple_color_tables,
                           format=ExportFormat.AVI)


class animation_flash(animation):
    r'''Frame-by-frame Flash animation context.

    Parameters:
        filename (`str`): The resulting video file name or path, relative to
            Python's current working directory.
        width (`int`, optional): The width of the video in pixels. (default:
            800)
        animation_speed (`int`, optional): The frame-rate of the video in
            frames per second. (default: 10)
        region (`Frame` or `ExportRegion`, optional): The rectangular area to
            be exported. This can be a specific `Frame` object or one of
            `ExportRegion.CurrentFrame`, `ExportRegion.AllFrames` (default) or
            `ExportRegion.WorkArea`.
        supersample (`int`, optional): Controls the amount of anti-aliasing
            used in each frame. Valid values are 1-16. A value of **1**
            indicates that no antialiasing will be used. Antialiasing smooths
            jagged edges on text, lines, and edges of the video output by the
            process of supersampling. *Some graphics cards* can cause Tecplot
            360 to crash when larger anti-aliasing values are used. If this
            occurs on your machine, try updating your graphics driver or using
            a lower anti-aliasing value. (default: **3**)
        compression (`FlashCompressionType`, optional): The compression scheme
            to use when creating the video stream. Options are:
            `FlashCompressionType.BestSpeed` (default) and
            `FlashCompressionType.SmallestSize`.
        image_type (`FlashImageType`, optional): The type of images to generate
            for each frame of the animation. Options are:
            `FlashImageType.Color256`, `FlashImageType.JPEG` and
            `FlashImageType.Lossless` (default).

    This is a `context manager
    <https://docs.python.org/3/reference/datamodel.html#context-managers>`_ and
    must be invoked using the `with
    <https://docs.python.org/3/reference/compound_stmts.html#with>`_ statement.
    The returned object of the context manager is used to control when each
    frame of the video is captured. This is done using the context method
    `animation.export_animation_frame()` as shown in the example below, at
    which point the specified region or plot is rendered. The actual video file
    is produced upon exit of the context.

    Typical code looks like the following (see the example under
    `animation_mpeg4` for a complete working example)::

        >>> with tp.export.animation_flash('output.flv') as ani:
        ...     # make some view changes here
        ...     ani.export_animation_frame()
    '''
    def __init__(self, filename, width=800, animation_speed=10,
                 region=ExportRegion.AllFrames, supersample=3,
                 compression=None, image_type=FlashImageType.Lossless):
        animation.__init__(self, filename=filename, width=width,
                           animation_speed=animation_speed, region=region,
                           supersample=supersample, compression=compression,
                           image_type=image_type, format=ExportFormat.Flash)


class animation_mpeg4(animation):
    r'''Frame-by-frame MPEG4 animation context.

    Parameters:
        filename (`str`): The resulting video file name or path, relative to
            Python's current working directory.
        width (`int`, optional): The width of the video in pixels. (default:
            800)
        animation_speed (`int`, optional): The frame-rate of the video in
            frames per second. (default: 10)
        region (`Frame` or `ExportRegion`, optional): The rectangular area to
            be exported. This can be a specific `Frame` object or one of
            `ExportRegion.CurrentFrame`, `ExportRegion.AllFrames` (default) or
            `ExportRegion.WorkArea`.
        supersample (`int`, optional): Controls the amount of anti-aliasing
            used in each frame. Valid values are 1-16. A value of **1**
            indicates that no antialiasing will be used. Antialiasing smooths
            jagged edges on text, lines, and edges of the video output by the
            process of supersampling. *Some graphics cards* can cause Tecplot
            360 to crash when larger anti-aliasing values are used. If this
            occurs on your machine, try updating your graphics driver or using
            a lower anti-aliasing value. (default: **3**)
        format_options (`str`, optional): A string of options passed directly
            to the underlying application `FFmpeg <https://www.ffmpeg.org/>`_.
            By default, this will be "-c:v libx264 -profile:v high -crf 20
            -pix_fmt yuv420p".

    This is a `context manager
    <https://docs.python.org/3/reference/datamodel.html#context-managers>`_ and
    must be invoked using the `with
    <https://docs.python.org/3/reference/compound_stmts.html#with>`_ statement.
    The returned object of the context manager is used to control when each
    frame of the video is captured. This is done using the context method
    `animation.export_animation_frame()` as shown in the example below, at
    which point the specified region or plot is rendered. The actual video file
    is produced upon exit of the context.

    Example usage:

    .. code-block:: python
        :emphasize-lines: 64,68

        import argparse, os

        import tecplot as tp
        from tecplot.constant import *

        def parse_args():
            """
            This script is to be run from the command line and accepts the
            following command line arguments. Run this script with "--help"
            to see usage and help information.
            """
            parser = argparse.ArgumentParser()
            parser.add_argument('-c', '--connect', action='store_true',
                                help='connect to TecUtil Server')
            parser.add_argument('-p', '--port', type=int, default=7600,
                                help='port to use when connecting to TecUtil Server')
            parser.add_argument('-n', '--nframes', type=int, default=360,
                                help='number of frames to produce in video')
            parser.add_argument('outfile', nargs='?', default='aileron_roll.mp4',
                                help='output file name')
            return parser.parse_args()

        def setup_plot():
            """
            Load the F-18 dataset from Tecplot 360's examples and show the
            jet surface in 3D.
            """
            tp.new_layout()
            exdir = tp.session.tecplot_examples_directory()
            datafile = os.path.join(exdir, 'SimpleData', 'F18.plt')
            ds = tp.data.load_tecplot(datafile)

            frame = tp.active_frame()
            frame.show_border = False
            plot = frame.plot(PlotType.Cartesian3D)
            plot.activate()

            plot.contour(0).variable = ds.variable('S')
            plot.show_contour = True
            return plot

        def translate_view(view, x=0, y=0, z=0):
            """
            Translate the viewer with respect to the data.
            """
            p = view.position
            view.position = p.x + x, p.y + y, p.z + z

        def create_animation(outfile, plot, nframes):
            """
            Using the tp.export.animation_mpeg4() context manager, the F-18 is
            recorded doing an "aileron roll" by rotating and translating the
            viewer with respect to the data by a small amount and capturing
            each frame of the animation with a call to ani.export_animation_frame()
            """
            with tp.session.suspend():
                opts = dict(
                    width=400,
                    animation_speed=30,
                    supersample=3,
                )
                view = plot.view
                translate_view(view, -15)
                with tp.export.animation_mpeg4(outfile, **opts) as ani:
                  for i in range(args.nframes):
                    view.rotate_axes(5, (1, 0, 0))
                    translate_view(view, 30 / args.nframes)
                    ani.export_animation_frame()

        """
        This script is meant to run on the command line. Run with "--help" to see
        usage and help information about the options it understands. It loads
        the F-18 dataset from Tecplot 360's examples directory and produces a
        video of the model doing an "aileron roll" by manipulating the viewer
        position.
        """
        args = parse_args()
        if args.connect:
            tp.session.connect(port=args.port)
        plot = setup_plot()
        create_animation(args.outfile, plot, args.nframes)
        print('video file created:', args.outfile)

    .. raw:: html

        <video controls>
            <source src="../_static/videos/aileron_roll.m4v" type="video/mp4">
            I'm sorry; your browser doesn't support HTML5 MPEG4/H.264 video.
        </video>
    '''
    def __init__(self, filename, width=800, animation_speed=10,
                 region=ExportRegion.AllFrames, supersample=3,
                 format_options=None):
        animation.__init__(self, filename=filename, width=width,
                           animation_speed=animation_speed, region=region,
                           supersample=supersample,
                           format_options=format_options,
                           format=ExportFormat.MPEG4)


class animation_raster_metafile(animation):
    r'''Frame-by-frame Raster Metafile animation context.

    Parameters:
        filename (`str`): The resulting video file name or path, relative to
            Python's current working directory.
        width (`int`, optional): The width of the video in pixels. (default:
            800)
        animation_speed (`int`, optional): The frame-rate of the video in
            frames per second. (default: 10)
        region (`Frame` or `ExportRegion`, optional): The rectangular area to
            be exported. This can be a specific `Frame` object or one of
            `ExportRegion.CurrentFrame`, `ExportRegion.AllFrames` (default) or
            `ExportRegion.WorkArea`.
        supersample (`int`, optional): Controls the amount of anti-aliasing
            used in each frame. Valid values are 1-16. A value of **1**
            indicates that no antialiasing will be used. Antialiasing smooths
            jagged edges on text, lines, and edges of the video output by the
            process of supersampling. *Some graphics cards* can cause Tecplot
            360 to crash when larger anti-aliasing values are used. If this
            occurs on your machine, try updating your graphics driver or using
            a lower anti-aliasing value. (default: **3**)
        multiple_color_tables (`bool`, optional): Create a color table for each
            frame of the animation. If `False` (default), the whole animation
            will be scanned in an attempt to create a single table of 256
            colors.

    This is a `context manager
    <https://docs.python.org/3/reference/datamodel.html#context-managers>`_ and
    must be invoked using the `with
    <https://docs.python.org/3/reference/compound_stmts.html#with>`_ statement.
    The returned object of the context manager is used to control when each
    frame of the video is captured. This is done using the context method
    `animation.export_animation_frame()` as shown in the example below, at
    which point the specified region or plot is rendered. The actual video file
    is produced upon exit of the context.

    Typical code looks like the following (see the example under
    `animation_mpeg4` for a complete working example)::

        >>> with tp.export.animation_raster_metafile('output.rm') as ani:
        ...     # make some view changes here
        ...     ani.export_animation_frame()
    '''
    def __init__(self, filename, width=800, animation_speed=10,
                 region=ExportRegion.AllFrames, supersample=3,
                 multiple_color_tables=False):
        animation.__init__(self, filename=filename, width=width,
                           animation_speed=animation_speed, region=region,
                           supersample=supersample,
                           multiple_color_tables=multiple_color_tables,
                           format=ExportFormat.RasterMetafile)


class animation_wmv(animation):
    r'''Frame-by-frame WMV animation context.

    Parameters:
        filename (`str`): The resulting video file name or path, relative to
            Python's current working directory.
        width (`int`, optional): The width of the video in pixels. (default:
            800)
        animation_speed (`int`, optional): The frame-rate of the video in
            frames per second. (default: 10)
        region (`Frame` or `ExportRegion`, optional): The rectangular area to
            be exported. This can be a specific `Frame` object or one of
            `ExportRegion.CurrentFrame`, `ExportRegion.AllFrames` (default) or
            `ExportRegion.WorkArea`.
        supersample (`int`, optional): Controls the amount of anti-aliasing
            used in each frame. Valid values are 1-16. A value of **1**
            indicates that no antialiasing will be used. Antialiasing smooths
            jagged edges on text, lines, and edges of the video output by the
            process of supersampling. *Some graphics cards* can cause Tecplot
            360 to crash when larger anti-aliasing values are used. If this
            occurs on your machine, try updating your graphics driver or using
            a lower anti-aliasing value. (default: **3**)
        format_options (`str`, optional): A string of options passed directly
            to the underlying application `FFmpeg <https://www.ffmpeg.org/>`_.
            By default, this will be "-qscale 4".

    This is a `context manager
    <https://docs.python.org/3/reference/datamodel.html#context-managers>`_ and
    must be invoked using the `with
    <https://docs.python.org/3/reference/compound_stmts.html#with>`_ statement.
    The returned object of the context manager is used to control when each
    frame of the video is captured. This is done using the context method
    `animation.export_animation_frame()` as shown in the example below, at
    which point the specified region or plot is rendered. The actual video file
    is produced upon exit of the context.

    Typical code looks like the following (see the example under
    `animation_mpeg4` for a complete working example)::

        >>> with tp.export.animation_wmv('output.wmv') as ani:
        ...     # make some view changes here
        ...     ani.export_animation_frame()
    '''
    def __init__(self, filename, width=800, animation_speed=10,
                 region=ExportRegion.AllFrames, supersample=3,
                 format_options=None):
        animation.__init__(self, filename=filename, width=width,
                           animation_speed=animation_speed, region=region,
                           supersample=supersample,
                           format_options=format_options,
                           format=ExportFormat.WMV)
