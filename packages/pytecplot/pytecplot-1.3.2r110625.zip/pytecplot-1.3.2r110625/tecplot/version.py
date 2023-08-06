"""Version information of the tecplot Python module can be obtained as a `string
<str>` of the form "Major.Minor.Patch"::

    tecplot.__version__

or as a `namedtuple <collections.namedtuple>` with attributes: "major",
"minor", "patch", "build" in that order::

    tecplot.version_info

The underlying |Tecplot 360| installation has its own version which can be
obtained as a `str`::

    tecplot.sdk_version

or as a `namedtuple <collections.namedtuple>`::

    tecplot.sdk_version_info

PyTecplot adheres to the semantic versioning as outlined in `SemVer 2.0.0
<https://semver.org/spec/v2.0.0.html>`__ with regard to backwards compatibility
between releases. For this purpose, the public interface of PyTecplot is
defined as all entities (functions, properties etc.) presented in the `HTML
documentation <https://www.tecplot.com/docs/pytecplot/>`__ and does not include
methods in the code-base which do not show up in the HTML documentation, even
when a docstring is present. In short, we will maintain backwards compatibility
of the public interface between all minor releases of the same major version
with the exception of internal changes that fix incorrect behavior or bugs.
"""
import collections

from .tecutil import _tecutil_connector

Version = collections.namedtuple('V', ['major', 'minor', 'patch', 'build'])

version = '1.3.2'
build = '110625'
version_info = Version(*[int(x) for x in version.split('.')], build=build or 0)

sdk_version_info = _tecutil_connector.sdk_version_info
sdk_version = _tecutil_connector.sdk_version
