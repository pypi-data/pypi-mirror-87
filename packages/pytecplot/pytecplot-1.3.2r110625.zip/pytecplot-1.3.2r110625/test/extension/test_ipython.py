from __future__ import with_statement

import base64
import os
import unittest
import warnings

from unittest.mock import patch, Mock

import tecplot as tp


def save_png(filename, *args, **kwargs):
    with open(filename, 'wb') as fout:
        # this is a 1-pixel valid png
        fout.write(base64.b64decode('''
iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAACklEQVR4nGMAAQAABQABDQottAAA
AABJRU5ErkJggg==
            '''.strip()))


class TestIPython(unittest.TestCase):

    def setUp(self):
        tp.new_layout()

    def test_show(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            warnings.filterwarnings("ignore", category=PendingDeprecationWarning)
            with patch('IPython.display.display'):
                with patch('tecplot.export.save_png', side_effect=save_png):
                    tp.extension.ipython.show()

                    with patch('os.remove', Mock(side_effect=OSError)) as rm:
                        with patch('tecplot.extension.ipython.log.warning', Mock()) as lg:
                            tp.extension.ipython.show()
                        self.assertEqual(lg.call_count, 1)
            os.remove(rm.call_args[0][0])


if __name__ == '__main__':
    from .. import main
    main()
