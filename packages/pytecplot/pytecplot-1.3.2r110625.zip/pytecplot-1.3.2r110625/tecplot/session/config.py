r"""
.. function:: tecplot.session.configuration()

    Run-time configuration parameters can be accessed and changed through the
    configuration instance returned by ``tecplot.session.configuration()``::

        >>> conf = tecplot.session.configuration()
        >>> print(conf.latex.command)
        pdflatex -interaction=batchmode -output-directory=@OUTDIR @INFILE
        >>> conf.latex.preamble = '\usepackage{amsmath}'

The default settings have been tested with MiKTeX and TeXLive engines and
should work without the need for any changes to the session configuration.
However, you may wish to change the LaTeX packages which are loaded by default
or use a different LaTeX engine. See the Tecplot user manual for guidance in
changing your LaTeX configuration file so changes persist across sessions.

Available configuration parameters:

..  contents::
    :local:
    :depth: 1

``latex.command``
^^^^^^^^^^^^^^^^^

The system command used to compile LaTeX text objects. Parameters ``@OUTDIR``
and ``@INFILE`` are replaced with appropriate strings to coordinate the
creation of the final rendered text.

Type:
    `str`
Default:
    "latex -interaction=batchmode -output-directory=\@OUTDIR @INFILE"

``latex.dvipng_command``
^^^^^^^^^^^^^^^^^^^^^^^^

The system command used to convert the output from the LaTeX command from DVI
to PNG. The parameters ``@DPI``, ``@PAGERANGE``, ``@OUTFILE`` and ``@INFILE``
are replaced with appropriate strings to coordinate the creation fo the final
rendered text.

Type:
    `str`
Default:
    "dvipng -bg Transparent -D @DPI -pp @PAGERANGE -T tight -o @OUTFILE @INFILE"

``latex.preamble``
^^^^^^^^^^^^^^^^^^

Code that will be placed before the ``\begin{document}`` section of the LaTeX
source to be compiled. This primarily used for loading LaTeX packages.

Type:
    `str`
Default:
    "\\usepackage{amsfonts}\\usepackage{amsmath}\\usepackage{amssymb}\\usepackage{amsthm}"

"""
from builtins import str

from ..tecutil import sv
from .style import StyleConfig, style_property


class ConfigLaTeX(StyleConfig):
    command = style_property(str, sv.LATEXCMD)
    preamble = style_property(str, sv.PREAMBLE)
    dvipng_command = style_property(str, sv.DVIPNGCMD)


class ConfigLimits(StyleConfig):
    load_on_demand_threshold_min = style_property(
                                    float, sv.LODTHRESHOLDMINFRACT)
    load_on_demand_threshold_max = style_property(
                                    float, sv.LODTHRESHOLDMAXFRACT)


class ConfigOpenGL(StyleConfig):
    run_display_lists_after_building = style_property(
                                        bool, sv.RUNDISPLAYLISTSAFTERBUILDING)


class ConfigInterface(StyleConfig):
    opengl = ConfigOpenGL('interface.opengl', sv.INTERFACE, sv.OPENGLCONFIG)


class configuration(StyleConfig):
    latex = ConfigLaTeX('latex', sv.LATEX)
    limits = ConfigLimits('limits', sv.LIMITS)
    interface = ConfigInterface('interface', sv.INTERFACE)
