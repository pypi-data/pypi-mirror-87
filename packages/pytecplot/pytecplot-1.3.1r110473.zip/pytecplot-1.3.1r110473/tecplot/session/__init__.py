"""|Tecplot Engine| State and |Tecplot License| Management

The `session` module contains methods used to manipulate the |Tecplot Engine|
such as notification of a `state change` that was done such as adding or
modifying data. It also contains methods for acquiring and releasing the
|Tecplot License|.

.. _state change:

State Changes
-------------

State changes are the method for propagating information when an event occurs.
A state change can be triggered by many events. Examples include: loading a
data file, changing the color of a mesh plot, creating a new zone, or changing
the plot type.

In general, state changes are already handled internally after each call to the
PyTecplot API. This can cause a script that performs many operations,
especially those that alter data, to run slowly since the |Tecplot Engine| must
update it's internal state every time a state change is received. To speed up
such scripts, it may be necessary to use the `tecplot.session.suspend()`
context. This will collect state changes for any operation performed and will
emit the required state changes only upon exit of the context.

Using the `tecplot.session.suspend()` context in combination with Python's
"-OO" flag which removes many run-time checks in the PyTecplot API is the
recommended way to run a PyTecplot script which requires faster execution
time. The user should be aware that, when using the "-OO" flag, errors may
not be recoverable by the |Tecplot Engine|.

"""

from .aux_data import AuxData
from .config import configuration
from .session import (acquire_license, clear_suspend, connect, connected,
                      disconnect, license_expiration, release_license,
                      start_roaming, stop, stop_roaming, suspend,
                      suspend_enter, suspend_exit)
from .state_changed import connectivity_altered, data_altered, zone_added
from .style import (Style, SubStyle, get_style, set_style,
                    IJK, IJKMaxFract, IJKMinFract, IndependentVariableLimits,
                    Limits, IndexIJK, IndexRange, RectPosition, RectSize,
                    SplineDerivativeAtEnds, XY, XYZ)

import os
import platform
from ..tecutil import _tecutil_connector


def tecplot_install_directory():
    """|Tecplot 360| installation directory.

    Top-level installation directory for |Tecplot 360|. This will
    typically contain configuration files and the examples directory.

    This directory is platform-dependent and will contain configuration files
    and the examples directory:

    .. code-block:: python
        :emphasize-lines: 4

        import os
        import tecplot

        install_dir = tecplot.session.tecplot_install_directory()
        infile = os.path.join(install_dir, 'examples', 'SimpleData', 'SpaceShip.lpk')

        tecplot.load_layout(infile)
        tecplot.export.save_png('spaceship.png', 600, supersample=3)

    .. figure:: /_static/images/spaceship.png
        :width: 300px
        :figwidth: 300px
    """
    if not _tecutil_connector.connected:
        _tecutil_connector.start()
    d = _tecutil_connector.tecsdkhome
    if d:
        if platform.system() in ['Darwin', 'Mac']:
            d = os.path.normpath(os.path.join(d, '..', '..'))
        return d


def tecplot_examples_directory():
    """|Tecplot 360| examples directory.

    Examples directory that is typically installed with |Tecplot 360|.
    This may be overridden with the TECPLOT_EXAMPLES environment variable.

    This directory is platform-dependent and by default contains the various
    examples shipped with |Tecplot 360|:

    .. code-block:: python
        :emphasize-lines: 4

        import os
        import tecplot

        examples_dir = tecplot.session.tecplot_examples_directory()
        infile = os.path.join(examples_dir, 'SimpleData', 'F18.lay')

        tecplot.load_layout(infile)
        tecplot.export.save_png('load_example.png', 600, supersample=3)

    .. figure:: /_static/images/load_example.png
        :width: 300px
        :figwidth: 300px
    """
    d = tecplot_install_directory()
    if d:
        return os.environ.get('TECPLOT_EXAMPLES', os.path.join(d, 'examples'))
