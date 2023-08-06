from builtins import int

import logging

from six import string_types
from textwrap import dedent

from ..tecutil import _tecutil, _tecutil_connector
from ..constant import *
from ..exception import *
from .. import layout, session, tecutil
from . import array

log = logging.getLogger(__name__)


@tecutil.lock_attributes
class Variable(object):
    """Key value for a data array within a `Dataset`.

    `Variables <Variable>` can be identified (uniquely) by the index within
    their parent `Dataset` or (non-uniquely) by name. In general, a `Zone
    <data_access>` must also be selected to access the underlying data array.
    This object is used by several style controlling classes such as contours
    and vectors. The following example sets the contour variable for the first
    contour group to the first variable named 'S'::

        >>> plot.contour(0).variable = dataset.variable('S')
    """
    def __init__(self, uid, dataset):
        self.uid = uid
        self.dataset = dataset

    @property
    def _cache(self):
        if _tecutil_connector.suspended:
            _tecutil_connector._delete_caches.append(self._delete_cache)
            return True
        else:
            return False

    def _delete_cache(self):
        attrs = ['_index']
        for attr in attrs:
            try:
                delattr(self, attr)
            except AttributeError:
                pass

    def __str__(self):
        """Brief string representation.

        Returns:
            `str`: Brief representation of this `Variable`, showing
            `Zones <data_access>`.

        Example::

            >>> p = dataset.variable('Pressure')
            >>> print(p)
            Pressure
        """
        return self.name

    def __repr__(self):
        """Executable string representation.

        Returns:
            `str`: Internal representation of this `Variable`.

        The string returned can be executed to generate a
        clone of this `Variable` object::

            >>> x = dataset.variable('x')
            >>> print(repr(x))
            Variable(uid=41, Dataset(uid=21, frame=Frame(uid=11,
            page=Page(uid=1)))
            >>> exec('x_clone = '+repr(x))
            >>> x_clone
            Variable(uid=41, Dataset(uid=21, frame=Frame(uid=11,
            page=Page(uid=1)))
            >>> x == x_clone
            True
        """
        return 'Variable(uid={uid}, dataset={dataset})'.format(
            uid=self.uid, dataset=repr(self.dataset))

    def __eq__(self, other):
        """Checks for equality in the |Tecplot Engine|.

        Returns:
            `bool`: `True` if the unique ID numbers are the same for both
            `Variables <Variable>`.
        """
        return self.uid == other.uid

    def __ne__(self, other):
        return not (self == other)

    @property
    def aux_data(self):
        """Auxiliary data for this variable.

        Returns:
            `AuxData`

        This is the auxiliary data attached to the variable. Such data is
        written to the layout file by default and can be retrieved later.
        Example usage::

            >>> frame = tp.active_frame()
            >>> aux = frame.dataset.variable('X').aux_data
            >>> aux['X_weighted_avg'] = '3.14159'
            >>> print(aux['X_weighted_avg'])
            3.14159
        """
        return session.AuxData(self.dataset.frame, AuxDataObjectType.Variable,
                               self.index)

    @property
    def index(self):
        """`Index`: Zero-based position within the parent `Dataset`.

        Example usage::

            >>> plot.contour(0).variable_index = dataset.variable('S').index
        """
        if self._cache:
            if not hasattr(self, '_index'):
                num = _tecutil.VarGetNumByUniqueID(self.uid)
                self._index = tecutil.Index(num - 1)
            return self._index
        else:
            return tecutil.Index(_tecutil.VarGetNumByUniqueID(self.uid) - 1)

    @property
    def lock_mode(self):
        """`VarLockMode`: Type of lock or `None` (read-only).

        Variables may be locked as a result of other operations, typically
        through the use of the CFD Analyzer. This read-only property returns
        `None` if the variable is not locked, `VarLockMode.ValueChange` if the
        variable may not be modified or `VarLockMode.Delete` if the variable
        may not be deleted.

        This example modifies variable ``s`` only if it is not locked::

            >>> variable_s = dataset.variable('s')
            >>> if variable_s.lock_mode is None:
            ...     tp.data.operate.execute_equation('{s} = {p}**2')

        .. versionadded:: 2019.1
            Variable lock mode property requires Tecplot 360 2019 R1 or later.
        """
        if __debug__:
            if (
                _tecutil_connector.connected and
                _tecutil_connector.client.tuserver_version < 5
            ):
                raise TecplotOutOfDateEngineError((2018, 3))
        with self.dataset.frame.activated():
            _, mode, _ = _tecutil.VariableIsLocked(self.index + 1)
            return mode

    def minmax(self):
        """Limits of the values stored in this variable across all zones.

        :rtype: 2-tuple of `floats <float>`

        This always returns `floats <float>` regardless of the underlying data
        type::

            >>> print(dataset.variable('x').minmax())
            (0, 10)
        """
        with self.dataset.frame.activated():
            success, vmin, vmax = _tecutil.VarGetMinMax(self.index + 1)
            if not success:
                raise TecplotSystemError()
            return vmin, vmax

    def min(self):
        """Lower bound of the values stored in this variable across all zones.

        :rtype: `float`

        This always returns a `float` regardless of the underlying data type::

            >>> print(dataset.variable('x').min())
            0
        """
        return self.minmax()[0]

    def max(self):
        """Upper bound of the values stored in this variable across all zones.

        :rtype: `float`

        This always returns a `float` regardless of the underlying data type::

            >>> print(dataset.variable('x').max())
            10
        """
        return self.minmax()[1]

    @property
    def name(self):
        """Returns or sets the name.

        :rtype: `string <str>`

        .. warning:: **Newlines in string identifiers may affect performance.**

            When iterating over many items by name, such as must be done when
            fetching an item via pattern matching, PyTecplot will optimize the
            search only if there are no newline characters in the searched
            items. Iterating over strings that contain newlines will be slower
            and therefore, it is best to avoid using newlines in string
            identifiers or names of objects such as `Zones <data_access>` or
            `Variables <Variable>`.

        Example usage::

            >>> print(dataset.variable(0).name)
            X
        """
        res, var_name = _tecutil.VarGetNameByDataSetID(self.dataset.uid,
                                                       self.index + 1)
        if not res:
            raise TecplotSystemError()
        return var_name

    @name.setter
    @tecutil.lock()
    def name(self, name):
        _tecutil.VarRenameByDataSetID(self.dataset.uid, self.index + 1, name)

    @property
    def num_zones(self):
        """`int`: Number of `Zones <data_access>` in the parent `Dataset`.

        Example usage, looping over all zones by index::

            >>> for zindex in range(dataset.num_zones):
            ...     zone = dataset.zone(zindex)
        """
        return self.dataset.num_zones

    def values(self, pattern):
        """Returns `Array` by index or string pattern.

        Parameters:
            pattern (`int`, `str` or `Zone <data_access>`):  Zero-based index
                or `glob-style pattern <fnmatch.fnmatch>` in which case, the
                first match is returned, or a `Zone <data_access>` object.

        .. note:: **Data operations can make use of Numpy when installed.**

            When doing large data transfers into and out of Tecplot using
            PyTecplot, it is recommended to install the Python array-processing
            module `Numpy <https://scipy.org>`_. PyTecplot will automatically
            use this to optimize data transfers which may result in significant
            performance gains.

        The `Zone.name <OrderedZone.name>` attribute is used to match the
        *pattern* to the desired `Array` though this is not necessarily
        unique::

            >>> ds = frame.dataset
            >>> print(ds)
            Dataset:
              Zones: 'Rectangular zone'
              Variables: 'x', 'y', 'z'
            >>> x = ds.variable('x')
            >>> rectzone = x.values('Rectangular zone')
            >>> rectzone == x.values(0)
            True

        .. warning:: **Zone and variable ordering may change between releases**

            Due to possible changes in data loaders or data formats over time,
            the ordering of zones and variables may be different between
            versions of Tecplot 360. Therefore it is recommended to always
            reference zones and variables **by name** instead of by index.
        """
        if isinstance(pattern, (string_types, int)):
            zone = self.dataset.zone(pattern)
        else:
            zone = pattern
        return array.Array(zone, self)
