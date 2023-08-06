"""Optional and extended functionality.

This sub-module provides integration with popular third-party libraries
including `NumPy <http://www.numpy.org/>`_ and `IPython
<https://ipython.org/>`_. These will be ignored if the required dependencies
are not installed. To enable extensions, you can install the required
dependencies with pip:

    cd pytecplot
    python -m pip install -U .[extras]

"""
from __future__ import absolute_import

from . import ipython
