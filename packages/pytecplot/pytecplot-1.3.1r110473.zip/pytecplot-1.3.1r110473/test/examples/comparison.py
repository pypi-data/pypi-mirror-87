# coding: utf-8
from __future__ import division

import datetime
import difflib
import filecmp
import multiprocessing
import os
import re

import numpy as np
from PIL import Image



def filter_paths(dirs, files):
    IGNORE_FILES = ['README.md', 'batch.log']
    dirs[:] = [d for d in dirs if d[0] != '.']
    files = [f for f in files if f[0] != '.' and f not in IGNORE_FILES]
    return sorted(dirs), sorted(files)


class Comparator:
    def __init__(self,
                 test_directory='image_comparisons/test',
                 reference_directory='image_comparisons/reference',
                 diff_directory='image_comparisons/diff',
                 default_tol=0.03):
        self.test_directory = test_directory
        self.reference_directory = reference_directory
        self.diff_directory = diff_directory
        self.tol = {'DEFAULT': default_tol}
        ftol = os.path.join(self.reference_directory, '.tolerance')
        if os.path.exists(ftol):
            ptrn = re.compile(r'^\s*([\d\.eE]+)\s+([\w\./]+)', re.M)
            with open(ftol, 'rt') as fin:
                for tol, fname in ptrn.findall(fin.read()):
                    self.tol[os.path.normpath(fname)] = float(tol)

    @staticmethod
    def _read_image(fpath, dtype=None):
        with Image.open(fpath, 'r') as img:
            data = np.asarray(img.getdata(), dtype=dtype)
            data.shape = (img.height, img.width, -1)
        return data[:, :, :3]

    @staticmethod
    def _image_rms(reference_image, test_image):
        """
            The values in the image are normalized and are assumed to span
            entire range of the type. For example, if the image data is uint8,
            then then maximum value assumed is 255.

            i runs through image pixels for each of R, G, B channels
            N = number of pixels times number of channels (3)

            di = reference_i - test_i
            maxvalue = type(test_i).max
            rms = sqrt( sum( (di / maxvalue)**2 ) / N )

            The resulting value is in the range [0, 1]
        """
        diff = reference_image.astype(np.int16) - test_image.astype(np.int16)
        maxvalue = np.iinfo(test_image.dtype).max
        return np.sqrt(np.sum((diff / maxvalue)**2) / test_image.size)

    @staticmethod
    def _image_diff(reference_image, test_image):
        if reference_image.shape != test_image.shape:
            diff_image = np.average(test_image, axis=2)
        else:
            diff_image = np.abs(reference_image - test_image).sum(2)
        diff_image = diff_image * np.iinfo(test_image.dtype).max / diff_image.max()
        return np.clip(diff_image, 0, 255).astype(np.uint8)

    def compare_image(self, fname):
        tol = self.tol.get(os.path.normpath(fname), self.tol['DEFAULT'])
        reference_fpath = os.path.join(self.reference_directory, fname)
        test_fpath = os.path.join(self.test_directory, fname)
        good_match = False
        rms = None
        if os.path.exists(reference_fpath):
            reference_image = Comparator._read_image(reference_fpath, np.uint8)
            test_image = Comparator._read_image(test_fpath, np.uint8)
            if tol < 0.0:
                good_match = np.array_equal(reference_image, test_image)
            else:
                if reference_image.shape != test_image.shape:
                    good_match = False
                else:
                    rms = Comparator._image_rms(reference_image, test_image)
                    good_match = rms <= tol
            diff_fpath = os.path.join(self.diff_directory, fname)
            if good_match:
                if os.path.exists(diff_fpath):
                    os.remove(diff_fpath)
            else:
                diff_image = Comparator._image_diff(reference_image, test_image)
                with Image.fromarray(diff_image, 'L') as img:
                    diff_fdir = os.path.dirname(diff_fpath)
                    if not os.path.exists(diff_fdir):
                        try:
                            os.makedirs(diff_fdir)
                        except OSError:
                            pass
                    img.save(diff_fpath)
        return good_match, rms

    def compare_file(self, fpath):
        print('.', end='', flush=True)
        reference_fpath = os.path.join(self.reference_directory, fpath)
        test_fpath = os.path.join(self.test_directory, fpath)
        if not os.path.exists(reference_fpath):
            if not os.path.exists(test_fpath):
                return False, 'file not found'
            return False, 'only in test directory'
        elif not os.path.exists(test_fpath):
            return False, 'only in reference directory'
        elif filecmp.cmp(reference_fpath, test_fpath):
            return True, None
        else:
            try:
                return self.compare_image(fpath)
            except OSError:
                diff_fpath = os.path.join(self.diff_directory, fpath)
                diff_fdir = os.path.dirname(diff_fpath)
                if not os.path.exists(diff_fdir):
                    try:
                        os.makedirs(diff_fdir)
                    except OSError:
                        pass
                try:
                    with open(reference_fpath, 'rt') as fin:
                        refdata = fin.read()
                    with open(test_fpath, 'rt') as fin:
                        testdata = fin.read()
                    diff = difflib.unified_diff(refdata.splitlines(keepends=True),
                                                testdata.splitlines(keepends=True))
                    diff = ''.join(diff)
                except:
                    diff = 'binary files differ'
                with open(diff_fpath, 'wt') as fout:
                    fout.write(diff)
                return False, diff

    def compare_files(self):
        success, fail = [], []

        fpaths = []
        for root, dirs, files in os.walk(self.test_directory):
            dirs[:], files = filter_paths(dirs, files)
            subdir = os.path.relpath(root, self.test_directory)
            for f in files:
                fpaths.append(os.path.join(subdir, f))

        pool = multiprocessing.Pool()
        results = pool.map(self.compare_file, fpaths)
        pool.close()
        pool.join()

        print('')

        for fpath, (good_match, diff) in zip(fpaths, results):
            if good_match:
                success.append(fpath)
            else:
                fail.append((fpath, diff))
                if diff:
                    if isinstance(diff, float):
                        print('{diff} RMS difference in {fpath}'.format(**locals()))
                    else:
                        print('difference in {fpath}:'.format(**locals()))
                        print(diff)
                else:
                    print('binary file or image shape mismatch: {fpath}'.format(**locals()))

        for root, dirs, files in os.walk(self.reference_directory):
            dirs[:], files = filter_paths(dirs, files)
            subdir = os.path.relpath(root, self.reference_directory)
            for f in files:
                fpath = os.path.join(subdir, f)
                if not os.path.exists(os.path.join(self.test_directory, fpath)):
                    fail.append((fpath, 'only in reference directory'))

        return success, fail
