from __future__ import unicode_literals, with_statement

import ctypes
import numpy as np
import os
import platform
import re
import sys

from contextlib import contextmanager
from tempfile import NamedTemporaryFile
from textwrap import dedent

import unittest
from unittest.mock import patch, Mock, PropertyMock

from test import LATEST_SDK_VERSION, patch_tecutil

import tecplot as tp

class TestVersion(unittest.TestCase):
    def test_version(self):
        self.assertIsInstance(tp.version_info, tp.version.Version)
        self.assertRegex(tp.__version__, r'\d+\.\d+\.\d+')

    def test_sdk_version(self):
        self.assertIsInstance(tp.sdk_version_info,
                              tp.tecutil.tecutil_connector.SDKVersion)
        self.assertRegex(tp.sdk_version, r'\d+\.\d+-\d+-\d+')

    def test_sdk_latest(self):
        sdkver = tp.sdk_version_info[:2]
        self.assertLessEqual(sdkver, LATEST_SDK_VERSION,
            '\nUpdate LATEST_SDK_VERSION in test/__init__.py to {}'.format(sdkver))


if __name__ == '__main__':
    from . import main
    main()
