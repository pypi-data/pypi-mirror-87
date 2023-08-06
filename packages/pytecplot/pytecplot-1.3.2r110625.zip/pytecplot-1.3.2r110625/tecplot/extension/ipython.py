"""
Integration with Jupyter IPython Notebooks
------------------------------------------

The environment variables needed to run and start |PyTecplot| have to be set
when the Jupyter server is started for them to take effect for each notebook
created. This includes ``PATH`` for Windows, ``LD_LIBRARY_PATH`` for Linux
and ``DYLD_LIBRARY_PATH`` for Mac OS X (see `Installation` for details).
Once set, the notebook server can usually be started with the command::

    jupyter notebook

Depending on your configuration, this may bring up your default web browser
showing the jupyter notebook interface.
"""
from __future__ import absolute_import, with_statement

import importlib
import io
import logging
import os
import tempfile
import warnings

from .. import layout, export

log = logging.getLogger(__name__)

def show(frame=None, width=600):
    """Display a `Frame` as an image inline in a notebook.

    Parameters:
        frame (`Frame`, optional): The `Frame` to display. The active `Frame`
            will be used if `None`. (default: `None`)
        width (`int`, optional): Width of the image in pixels.
            (default: 600)

    Example::

        >>> tecplot.load_layout('mylayout.lay')
        >>> tecplot.extension.ipython.show()

    This should put the resulting image just below the current cell in the
    notebook.
    """
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        from PIL import Image
        import IPython

    frame = frame or layout.active_frame()
    f = tempfile.NamedTemporaryFile(prefix=frame.name,
                                    suffix='.png',
                                    delete=False)
    try:
        with frame.activated():
            frame.move_to_top()
            f.close()
            export.save_png(f.name, width)
        with open(f.name, 'rb') as fimg:
            im = Image.open(fimg)
            b = io.BytesIO()
            im.save(b, format='png')
        IPython.display.display(IPython.display.Image(data=b.getvalue()))
    finally:
        try:
            os.remove(f.name)
        except OSError:
            log.warning('could not remove temporary file: {}'.format(f.name))
