from __future__ import print_function, unicode_literals

import os
import platform
import subprocess
import unittest
import io
import time
from tempfile import NamedTemporaryFile
from unittest.mock import *

import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *

from ..sample_data import sample_data
from .. import (patch_tecutil, closed_tempfile, skip_if_sdk_version_before,
                mocked_sdk_version)


def isvideo(cls, filename):
    if tp.version.sdk_version_info < (2018, 2, 1):
        with open(filename, 'rb') as fin:
            return len(fin.read()) > 0
    else:
        # wait for file to show up for at most 15 seconds on windows
        if platform.system() == 'Windows':
            start = time.time()
            while not os.path.exists(filename) and time.time() - start < 15:
                time.sleep(0.3)
            cls.assertTrue(os.path.exists(filename), msg=filename)
        ffmpeg = os.path.join(tp.tecutil._tecutil_connector.tecsdkhome,
                              'MacOS' if platform.system() == 'Darwin' else 'bin',
                              'ffmpeg')
        if not os.path.exists(ffmpeg):
            with open(filename, 'rb') as fin:
                return len(fin.read()) > 0
        cmd = '"{}" -v error -i "{{}}" -dn -f null -'.format(ffmpeg)
        shell = platform.system() in ['Linux', 'Darwin']
        exe = os.environ.get('SHELL', '/bin/bash') if shell else None
        env = os.environ.copy()
        if platform.system() == 'Linux':
            tec360dir = tp.tecutil._tecutil_connector.tecsdkhome
            ldpaths = [os.path.join(tec360dir, 'bin')]
            for p in os.environ.get('LD_LIBRARY_PATH', '').split(os.pathsep):
                p = os.path.abspath(p)
                if not p.startswith(tec360dir):
                    ldpaths.append(p)
            env['LD_LIBRARY_PATH'] = os.pathsep.join(ldpaths)
        proc = subprocess.Popen(cmd.format(filename), env=env, shell=shell,
                                executable=exe, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                universal_newlines=True)
        out, _ = proc.communicate()
        success = len(out) == 0
        if not success:
            print(out)
        return success


class TestAnimation(unittest.TestCase):
    _OPTS = dict(width=32, supersample=1)

    def setUp(self):
        tp.new_layout()
        self.filename,dataset = sample_data('3x3x3_p')
        frame = tp.active_frame()
        self.dataset = frame.dataset

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    def test_animation_avi(self):
        with closed_tempfile('.avi') as fname:
            with tp.export.animation_avi(fname, **TestAnimation._OPTS) as ani:
                ani.export_animation_frame()
                ani.export_animation_frame()
            self.assertTrue(isvideo(self, fname))

    def test_mpeg4_failure_on_out_of_date_engine(self):
        with mocked_sdk_version(2017, 2):
            with closed_tempfile('.avi') as fname:
                with tp.export.animation_avi(fname, **TestAnimation._OPTS) as ani:
                    ani.export_animation_frame()
                    ani.export_animation_frame()
                self.assertTrue(isvideo(self, fname))

            with self.assertRaises(TecplotOutOfDateEngineError):
                with closed_tempfile('.mp4') as fname:
                    with tp.export.animation_mpeg4(fname, **TestAnimation._OPTS) as ani:
                        ani.export_animation_frame()

    @skip_if_sdk_version_before(2017, 3)
    def test_animation_mpeg4_byext(self):
        with closed_tempfile('.mp4') as fname:
            with tp.export.animation(fname, **TestAnimation._OPTS) as ani:
                ani.export_animation_frame()
                ani.export_animation_frame()
            self.assertTrue(isvideo(self, fname))

    @skip_if_sdk_version_before(2017, 3)
    def test_animation_mpeg4(self):
        with closed_tempfile('.mp4') as fname:
            with tp.export.animation_mpeg4(fname, **TestAnimation._OPTS) as ani:
                ani.export_animation_frame()
                ani.export_animation_frame()
            self.assertTrue(isvideo(self, fname))

    @skip_if_sdk_version_before(2017, 3)
    def test_animation_wmv(self):
        with closed_tempfile('.wmv') as fname:
            with tp.export.animation_wmv(fname, **TestAnimation._OPTS) as ani:
                ani.export_animation_frame()
                ani.export_animation_frame()
            self.assertTrue(isvideo(self, fname))

    def test_animation_raster_metafile(self):
        with closed_tempfile('.rm') as fname:
            with tp.export.animation_raster_metafile(fname, **TestAnimation._OPTS) as ani:
                ani.export_animation_frame()
                ani.export_animation_frame()
            # no good way to determine video format for
            # raster metafiles so just check the file size
            with open(fname, 'rb') as fin:
                self.assertGreater(len(fin.read()), 800)

    def test_animation_flash(self):
        with closed_tempfile('.swf') as fname:
            opts = TestAnimation._OPTS.copy()
            opts.update(
                compression = FlashCompressionType.SmallestSize,
                image_type = FlashImageType.Color256
            )
            with tp.export.animation_flash(fname, **opts) as ani:
                ani.export_animation_frame()
                ani.export_animation_frame()
            self.assertTrue(isvideo(self, fname))

    @skip_if_sdk_version_before(2017, 3)
    def test_failures(self):
        with closed_tempfile('.mp4') as fname:
            try:
                with patch_tecutil('ExportStart', return_value=False):
                    with self.assertRaises(TecplotSystemError):
                        with tp.export.animation_mpeg4(fname) as ani:
                            pass

                with patch_tecutil('ExportStart', return_value=True):
                    with patch_tecutil('ExportFinish', return_value=True):
                        with patch_tecutil('ExportNextFrame', return_value=False):
                            with tp.export.animation_mpeg4(fname) as ani:
                                with self.assertRaises(TecplotSystemError):
                                    ani.export_animation_frame()

                    with patch_tecutil('ExportFinish', return_value=False):
                        with self.assertRaises(TecplotSystemError):
                            with tp.export.animation_mpeg4(fname) as ani:
                                pass
            finally:
                # clean up engine export state
                try:
                    with tp.tecutil.lock():
                        tp.tecutil._tecutil.ExportFinish()
                except:
                    pass



if __name__ == '__main__':
    from .. import main
    main()
