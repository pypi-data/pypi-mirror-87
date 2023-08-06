PyTecplot
=========

The pytecplot library is a high level API that connects your Python script
to the power of the |Tecplot 360| visualization engine. It offers line
plotting, 2D and 3D surface plots in a variety of formats, and 3D volumetric
visualization. Familiarity with |Tecplot 360| and the |Tecplot 360|
macro language is helpful, but not required.

Documentation
-------------

The full documentation is here: http://www.tecplot.com/docs/pytecplot

.. note::
	|PyTecplot| supports 64-bit Python 3.7 or later. |PyTecplot| does not
	support 32 bit Python. Please refer to INSTALL.rst for installation
	instructions and environment setup. For the best experience, developers are
	encouraged to use the **latest version of Python**.

Quick Start
-----------

Please refer to the documentation for detailed installation instructions and
environment setup. The short of it is something like this::

    pip install pytecplot

Linux and OSX users may have to set ``LD_LIBRARY_PATH`` or
``DYLD_LIBRARY_PATH`` to the directories containing the |Tecplot 360|
dynamic libraries. Please refer to the documentation at
http://www.tecplot.com/docs/pytecplot for detailed information regarding setup
and use. In addition, the web page
http://www.tecplot.com/support/faqs/pytecplot contains a list of answered
questions you may have about |PyTecplot| in general.

.. |Tecplot 360| replace:: `Tecplot 360 <http://www.tecplot.com/products/tecplot-360/>`__
.. |PyTecplot| replace:: `PyTecplot <http://www.tecplot.com/docs/pytecplot>`__

Change Log
----------

PyTecplot 1.3.1
^^^^^^^^^^^^^^^

Released with Tecplot 360 2020 R2

* New method: ``tp.data.extract.extract_connected_regions()`` to create zones
  from contiguous regions.
* Fixed a crash on exit when running in a MacOS virtual machine.
* Several minor documentation corrections.

PyTecplot 1.3.0
^^^^^^^^^^^^^^^

Released with Tecplot 360 2020 R1

* Fixed ``probe_on_surface()`` tolerance behavior for skewed cells.
* New methods: export of time-series animation videos.
* Current FEA loader version updated to v450.
* Fixed bug around setting axis ranges before data is loaded.

PyTecplot 1.2.0
^^^^^^^^^^^^^^^

* New loader: Converge HDF5 data files.
* New feature: Slice collections class through ``plot.slices()`` which
  simplifies and optimizes manipulating many slice groups at once.
* New method: Slice clipping.
* New methods: Transform array data from spherical or poler to rectagular and
  back.
* New method: ``tp.data.operate.smooth()`` for in-place transformation of field
  data.
* New method: ``tp.data.extract.triangulate()`` for 2D source zones.
* Fixed internal state-change behavior during suspend context.
* Fixed memory leaks around dynamic loading of libraries.
* Renaming and deprecation: ``Fieldmap.show_iso_surface`` has been deprecated
  and renamed to ``Fieldmap.show_isosurface``.
* Deprecated from 2D plot types: properties ``show_slices``,
  ``show_streamtraces`` and ``show_iso_surfaces`` are now only accessible from
  the 3D plot type.
* Several improvements to documentation and installation notes.

These methods and improvements will require either the April 2020 Beta or the
upcoming release of Tecplot 360 2020 R1:

* macOS: PyTecplot in batch mode can now export images with Python as installed
  by Brew or MacPorts.
* New method: ``tp.data.extract.extract_blanked_zones()``.
* Even vector spacing API: ``plot.vector.use_even_spacing``.
* Better API coverage by python recorder.

PyTecplot 1.1.0
^^^^^^^^^^^^^^^

* Officially supported Python versions are now 2.7 and 3.6+.
* Added support for Python 3.8 on all platforms. Windows batch-mode with Python
  3.8+ now requires PyTecplot version 1.1 or later.
* New feature: Fieldmap and Linemap collections classes through
  ``plot.fieldmaps()`` and ``plot.linemaps()`` which simplifies and optimizes
  manipulating many fieldmaps or linemaps at once.
* New option to close (quit) Tecplot 360 on disconnect.
* New position and size parameters for ``add_frame()``.
* New IJK range parameters for ``copy_zones()`` and ``Zone.copy()``.
* Bug fix: tp.data.operate.execute_equation() now uses zero-based indexing for
  IJK range parameters.
* Bug fix: ``IndexRange`` max value of zero is now interpreted as the first
  index in the range instead of the last index.
* Many documentation and example script updates and fixes.

PyTecplot 1.0.0
^^^^^^^^^^^^^^^

Released with Tecplot 360 2019 R1

* This is the first release of a guaranteed-stable interface of PyTecplot.
  Following this, the API will adhere closely to the guidelines enumerated
  by `Semantic Versioning 2.0.0 <https://semver.org>`_.
* Deprecation warnings from previous versions have been elevated to errors.
* Setting field data now unravels multidimensional arrays automatically,
  removing the need for the user to do this in client code.
* New methods for exporting to BMP and EPS image formats.
* New interfaces for linking style between and within frames.
* New method for mirroring zones: ``Dataset.mirror_zones()``.
* Telemac data loader: tp.data.load_telemac(), requires Tecplot 360 2019 R1 or
  later.
* New loader interfaces for CFX, Ensight, OpenFOAM, STL and VTK.
* SZL Server loader: tp.data.load_tecplot_szl() now fully supports SZL server.
* Several documentation and example script updates and fixes.

PyTecplot 0.14.0
^^^^^^^^^^^^^^^^

* New annotation objects: geometric shapes, poly-lines, images, georeferenced
  images and LaTeX.
* New interface for value blanking.
* New interface for scatter symbols, RGB coloring, data labels and light source.
* New animation export defaults: all frames, width: 800 px, supersample: 3.
* Reverse indexing (negative indices counting from the end) for linemap,
  fieldmap and solution_timestep.
* Regex pattern search for pages, frames, linemaps, zones and variables.
* Interface change: getting a single page, frame, linemap, zone or variable
  by name no longer raises and exception if no match is found. Instead the
  methods emit a warning and return None.
* Setting array data from Python into PyTecplot now orders of magnitude faster
  if Numpy is installed for batch-mode.
* New property: ``Variable.lock_mode`` to get lock status of the variable.
* New multiprocessing examples.
* Several documentation corrections and minor fixes.
* Removed: slice and isosurface properties are 3D only and have now been
  removed from the Cartesian2DFieldPlot class.

PyTecplot 0.12.0
^^^^^^^^^^^^^^^^

Released with Tecplot 360 2018 R2.1

* New: direct support for frame-by-frame and transient (solution time-based) animations.
* Bug fix: Dataset.copy_zones() now copies all zones by default.
* Better PyTecplot Connections exception handling.
* Updated installation documentation addressing differences between batch and connected modes.
* Removed from API: ``PolarView.reset_to_entire_circle()``. Scripts should use
  ``PolarLineAxis.reset_to_entire_circle()`` instead.
* Fixed recording of PyTecplot copy/paste frame.
* Added ability for PyTecplot to subsequently acquire a license if the first attempt
  failed due to contention.

PyTecplot 0.11.0
^^^^^^^^^^^^^^^^

Released with Tecplot 360 2018 R2

* FVCOM data loader: tp.data.load_fvcom(), requires Tecplot 360 2018 R2 and later.
* New properties of the Dataset: ``zone_names`` and ``variable_names`` returning lists of names.
* Performance: tp.session.suspend() context now delays GUI updates during complex operations. This
  is now fully supported with Tecplot 360 2018 R2 and later.
* Performance: The underlying protocol for connect mode has changed to "Protocol Buffers" by
  Google. PyTecplot is still backwards compatible with the previous versions of the TecUtil Server,
  but newer versions of Tecplot 360 will now require PyTecplot 0.11 or later.
* Import of the ``tecplot`` Python module is now "on-demand" and should be faster for most users.

PyTecplot 0.10.4
^^^^^^^^^^^^^^^^

* Bug fix: state changes now successfully emitted on exit from suspend context

PyTecplot 0.10.3
^^^^^^^^^^^^^^^^

* New extract line method: tp.data.extract.extract_line()
* All file operations are now always relative to Python's current working directory
* When connected to a non-local Tecplot 360 instance, paths must be absolute
* Faster import of the tecplot module by dynamic loading
* Several additions to documentation
* Bug fix: macro error messages are now included in the TecplotMacroError exception

PyTecplot 0.10.0
^^^^^^^^^^^^^^^^

* Preliminary support for Python 3.7
    * Tested with Python version 3.7.0b5
    * Python 3.7 PyZMQ pre-compiled wheels were not avaiable at the time of publishing 0.10.0 to install PyTecplot you must either:
        * Run pip with ``--no-deps`` for batch mode only.
        * Install Windows Visual Studio 2015 build tools for installing pyzmq until a wheel is avaiable.
* New: tecplot.session.suspend() context manager
* PyTecplot now uses Numpy (when installed) for increased performance during
  data transfers between Python and the Tecplot 360 Engine
* Many internal performance enhancements

PyTecplot 0.9.5
^^^^^^^^^^^^^^^

Released with Tecplot 360 2018 R1 March Maintenance Release

* Edge case fixes for tp.data.query.probe_on_surface()

PyTecplot 0.9.4
^^^^^^^^^^^^^^^

Released with Tecplot 360 2018 R1

* New feature: tp.data.query.probe_on_surface()
* Dataset.add_poly_zone() now requires the num_faces parameter (was optional).
* More efficient and reliable array handling when connected to running 360
* Minor documentation updates

PyTecplot 0.9.3
^^^^^^^^^^^^^^^

* Added IsosurfaceVector style access
* probe_at_position() now returns None when the point is outside the data volume
* Added tp.layout.num_pages() to get the number pages in a layout
* Bug fix: DataSet.add_zone() family of functions now obeys the strand argument
* Several documentation corrections

PyTecplot 0.9.1
^^^^^^^^^^^^^^^

Released with Tecplot 360 2017 R3 December Maintenance Release

* Recording of save layout, data and stylesheet commands

PyTecplot 0.9.0
^^^^^^^^^^^^^^^

Released with Tecplot 360 2017 R3

* TecUtil Server (PyTecplot Connections) stability and performance enhancements
* PyTecplot script recording via 360
* Added vector image export methods: save_ps(), save_wmf()
* pyzmq and flatbuffers are now installed by default when installing PyTecplot
  with pip
* Macro execute extended command
* Several documentation enhancements and internal bug fixes
* Dataset solution time access now requires Tecplot 2017.3 or later due to bug
  in engine
* Plot.fieldmaps() became function requiring parentheses
* New methods: Variable min(), max() and minmax()
* Zone min(), max() and minmax() became functions requiring parentheses
* When exporting images: width now defaults to 800, super sample defaults to 3
* Streamtrace.add_on_zone_surface() now uses the active zones by default
* CGNS loader will load boundary conditions by default
* Localization fix for roaming using non-en_US license servers
* Rename: axes.edge_auto_reset to axes.auto_edge_assignment
* Fixed exporting mpeg4 animations via macro language

PyTecplot 0.8.2
^^^^^^^^^^^^^^^

* Several bug fixes for 3rd party data loaders
* Connect to TecUtilServer (RPC) substantially more capable
* Aux data can now be cleared with AuxData.clear()
* Lots of documentation updates
* Can now control frame position and dimensions
* Sharing and branching variables and connectivity across zones has been added
* Passiveness for Arrays was added.
* Added support for RAWDATA when executing macro commands from python
* ``Array.__len__()`` now returning the length of the flattened array
* Data loaders now use ReadDataOption instead of the boolean append parameter
* Saving layout with '.lpk' extension implicitly includes data now
* Setting contour variable now implicitly resets the contour levels to nice
* More information is given on start-up errors

PyTecplot 0.8.1
^^^^^^^^^^^^^^^

Released with Tecplot 360 2017 R2

* Defaults change: allowing interpolation using all source zones by default
* Documentation fixes
* Unittests now handle out-of-date SDK with Python optimization
* Documentation text replacement tags now available

PyTecplot 0.8.0
^^^^^^^^^^^^^^^

* Interpolation methods: linear, inverse distance and krigging
* "Additional Quantities" loadable from Fluent data
* Legend style control
* Vector in 2D and 3D plot styles
* Reference vector
* Subzone load-on-demand (SZL) file loader
* rename: save_tecplot_binary() -> save_tecplot_plt()
* Aux data now accessible
* View and zooming control for 3D plots
* rename: tecinterprocess -> tecutil_connector
* Slice zone extraction from arbitrary point and normal
* Solution time and strand accessors for plots and datasets
* Orientation reference axis style and placement control
* More examples
* Lots of documentation added
* Many bug fixes

PyTecplot 0.7.0
^^^^^^^^^^^^^^^

* FaceNeighbors, Facemap and Nodemap.
* Streamlines
* Many doc updates and fixes.
* Streamtrace examples updates.
* "Working with datasets" examples.
* Streamtrace add functions.
* Continuous colormap min/max properties.
* Can now delete text annotations with Frame.delete_text()
* New script for 360 distribution: tec3560-env for easy setup of pytecplot.

PyTecplot 0.6.1
^^^^^^^^^^^^^^^

Released with Tecplot 360 2017 R1

* Better roaming, licensing and exception handling.
* Many documentation updates.
* Many minor bug fixes.
* Fluent loader.
* Reworked installation instructions.
* Better CGNS support.
* Zone.rank/dimensions rework.
* Zone class split into OrderedZone, ClassicFEZone and PolyFEZone.
* rename: font_family --> typeface.

PyTecplot 0.3.4
^^^^^^^^^^^^^^^

* Isosurface style control.
* Slice style control.
* Actions for Axes and Axis.
* Dataset, Zone, Variable and Array fully documented and unittested.
* Many internal bug fixes.
* rename in API: Zone.variable() --> Zone.values()
* rename in API: Variable.zone() --> variable.values()
* Minor bug fixes for Mac

PyTecplot 0.3.2
^^^^^^^^^^^^^^^

* Lots of bug fixes, both internal and external.
* Mostly internal testing and packaging updates.

PyTecplot 0.3.1
^^^^^^^^^^^^^^^

* First public release of PyTecplot
* Tecplot exceptions have been reworked and extended.
* tecplot.data.load_tecplot() fully implemented and now supports multiple input
  files in both binary and ASCII.
* Axis classes have been reworked and cleaned up along with examples and
  unittests.
* User's get "tecplot 360 out-of-date" error if tecinterprocess.so can't be
  loaded.
* Lot's of internal consistency testing.
* Text annotations.
* Fieldmap accessed by zone.
* Plot-level style control.
