# TODO: codecs not needed after Python 2.7 is dropped completely
import codecs
import os
import re
import sys


def long_description():
    here = os.path.abspath(os.path.dirname(__file__))
    readmefile = os.path.join(here, 'README.rst')
    with codecs.open(readmefile, encoding='utf-8') as f:
        return f.read()


def read_version():
    here = os.path.abspath(os.path.dirname(__file__))
    versionfile = os.path.join(here, 'tecplot', 'version.py')
    with codecs.open(versionfile, encoding='utf-8') as f:
        m = re.search(r"version = '(.*?)'", f.read(), re.M)
        return m.group(1)


def install_requires():
    if sys.version_info < (3, 0):
        return [
            'contextlib2==0.6.0.post1',
            'enum34==1.1.6',
            'flatbuffers==1.11',
            'future==0.18.2',
            'protobuf==3.11.2',
            'pyzmq==18.1.1',
            'six==1.13.0',
        ]
    elif sys.version_info < (3, 4):
        return ['enum34', 'flatbuffers', 'protobuf', 'pyzmq', 'six']
    else:
        return ['flatbuffers', 'protobuf', 'pyzmq', 'six']


def extra_requires():
    if sys.version_info < (3, 0):
        return ['ipython==5.8.0', 'numpy==1.16.6', 'pillow==6.2.1']
    else:
        return ['ipython', 'numpy', 'pillow']


def test_requires():
    reqs = extra_requires()
    if sys.version_info < (3, 0):
        reqs += [
            'coverage==5.0.3',
            'mock==3.0.5',
            'scipy==1.2.3',
            'tox==3.14.3',
        ]
    elif sys.version_info < (3, 3):
        reqs += ['coverage', 'mock', 'scipy', 'tox']
    else:
        reqs += ['coverage', 'scipy', 'tox']
    return sorted(set(reqs))


def doc_requires():
    return ['sphinx', 'pyyaml']


def setup_opts():
    from setuptools import find_packages
    opts = dict(
        name='pytecplot',
        version=read_version(),
        description='A python interface to Tecplot 360',
        long_description=long_description(),
        url='http://www.tecplot.com/docs/pytecplot',
        author='Tecplot, Inc.',
        author_email='support@tecplot.com',
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'Intended Audience :: Education',
            'Intended Audience :: End Users/Desktop',
            'Intended Audience :: Science/Research',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Topic :: Education',
            'Topic :: Multimedia :: Graphics :: 3D Rendering',
            'Topic :: Multimedia :: Graphics :: Presentation',
            'Topic :: Multimedia :: Graphics :: Viewers',
            'Topic :: Scientific/Engineering',
            'Topic :: Scientific/Engineering :: Information Analysis',
            'Topic :: Scientific/Engineering :: Mathematics',
            'Topic :: Scientific/Engineering :: Physics',
            'Topic :: Scientific/Engineering :: Visualization',
            'Topic :: Software Development :: Libraries',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'License :: Other/Proprietary License',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
        ],
        keywords=[
            'tecplot',
            'cfd',
            'data analysis',
            'scientific',
            'scientific computing',
            'statistics',
            'visualization',
            'numerical simulation',
            'aerospace',
        ],
        packages=find_packages(exclude=['test', 'test*']),
        install_requires=install_requires(),
        extras_require={
            'extras': extra_requires(),
            'doc': doc_requires(),
            'test': test_requires(),
            'all': sorted(set(extra_requires() +
                              test_requires() +
                              doc_requires())),
        },
    )
    return opts


if __name__ == '__main__':
    import setuptools
    import struct

    if sys.version_info[:2] < (2, 7):
        raise Exception('PyTecplot only supports Python 3.7 or later')

    pointer_size = struct.calcsize('P')
    if pointer_size != 8:
        err = '{} bit architecture detected.\n'.format(pointer_size * 8)
        err += 'PyTecplot must be used with a 64-bit version of Python.'
        raise Exception(err)

    setuptools.setup(**setup_opts())
