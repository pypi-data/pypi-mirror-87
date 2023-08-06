Session and Top-Level Functionality
===================================

..  contents::
    :local:
    :depth: 1

tecplot
-------

.. automodule:: tecplot


Version Information
-------------------

tecplot.version
^^^^^^^^^^^^^^^

.. automodule:: tecplot.version


Session
-------

..  contents::
    :local:
    :depth: 1

tecplot.session
^^^^^^^^^^^^^^^

.. automodule:: tecplot.session

session.suspend()
^^^^^^^^^^^^^^^^^

.. autofunction:: tecplot.session.suspend

session.suspend_enter()
^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: tecplot.session.suspend_enter

session.suspend_exit()
^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: tecplot.session.suspend_exit

session.clear_suspend()
^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: tecplot.session.clear_suspend

session.connect()
^^^^^^^^^^^^^^^^^

.. autofunction:: tecplot.session.connect

session.connected()
^^^^^^^^^^^^^^^^^^^

.. autofunction:: tecplot.session.connected

session.disconnect()
^^^^^^^^^^^^^^^^^^^^

.. autofunction:: tecplot.session.disconnect

session.stop()
^^^^^^^^^^^^^^

.. autofunction:: tecplot.session.stop

session.acquire_license()
^^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: tecplot.session.acquire_license

session.release_license()
^^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: tecplot.session.release_license

session.start_roaming()
^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: tecplot.session.start_roaming

session.stop_roaming()
^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: tecplot.session.stop_roaming

session.license_expiration()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: tecplot.session.license_expiration

session.tecplot_install_directory()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: tecplot.session.tecplot_install_directory

session.tecplot_examples_directory()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: tecplot.session.tecplot_examples_directory


Configuration
-------------


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


Miscellaneous
-------------

..  contents::
    :local:
    :depth: 1

.. autoclass:: tecplot.tecutil.Index
.. autoclass:: tecplot.session.IndexRange
