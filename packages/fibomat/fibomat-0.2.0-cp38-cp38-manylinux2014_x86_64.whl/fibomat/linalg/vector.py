"""Provide the :class:`Vector` class."""

from __future__ import annotations
from typing import Optional, Union, Iterable, overload
import collections.abc

import numpy as np


class VectorValueError(ValueError):
    """Exception of this type is raised if any non supported value type is passed to Vector.__init__."""


class Vector(collections.abc.Sequence):
    """An immutable 2d-vector class.

    .. note:: To create an `numpy.ndarray` use `numpy.asarray(my_vector)` where `my_vector` is a :class:`Vector` object.

    Some parts taken from: https://pypi.org/project/vec/
    """

    @staticmethod
    def _from_polar(r: Optional[float], phi: Optional[float]):  # pylint: disable=invalid-name
        array = np.empty(shape=(2,), dtype=float)

        if r is not None:
            if phi is not None:
                array[0] = r * np.cos(phi)
                array[1] = r * np.sin(phi)
            else:
                raise VectorValueError('If r is defined, theta must be defined, too.')
        else:
            if phi is not None:
                raise VectorValueError('If phi is defined, r must be defined, too.')

        return array

    @staticmethod
    def _from_iterable_or_vector(x: Union[Vector, Iterable[float]]):  # pylint: disable=invalid-name
        array = np.empty(shape=(2,), dtype=float)

        if isinstance(x, Vector):
            array[:] = np.asarray(x)
        # elif hasattr(x, 'x') and hasattr(x, 'y'):
        #     array[0] = x.y
        #     array[1] = x.x
        else:
            if not hasattr(x, "__iter__"):
                raise VectorValueError("x must be int, float, Vector, object with .x and .y, or iterable")
            i = iter(x)
            try:
                array[0] = next(i)
                array[1] = next(i)
            except ValueError as value_error:
                raise VectorValueError("Elements of iterable must be compatible with floats.") from value_error
            try:
                next(i)
                raise VectorValueError("if x is an iterable, it must contain exactly 2 items")
            except StopIteration:
                pass

        return array

    def __init__(
        self,
        x: Optional[Union[float, Vector, Iterable[float]]] = None,
        y: Optional[float] = None,
        r: Optional[float] = None,
        phi: Optional[float] = None
    ):
        """:class:`Vector` can be constructed by:s
            - `Vector()` creating a null vector (x=0, y=0)
            - `Vector(other_vector)` creating a copy of other_vector
            - `Vector(x=1, y=2)` creating a vector with x=1, y=2 components
            - `Vector([1, 2])` creating a vector with x=1, y=2 components
            - `Vector(np.array([1, 2])` creating a vector with x=1, y=2 components
            - `Vector(r=1, phi=np.pi)` creating a vector with x=r*cos(phi), y=r*sin(phi) components

        Args:
            x (float, Vector, Iterable[float], optional):
                x component of vector, :class:`Vector` or Iterable[float] with two components
            y (float, optional): y component of vector
            r (float, optional): radial component of vector
            phi (float, optional): angular component of vector

        Raises:
            VectorValueError: Raised if parameters are not understood.
        """
        array = np.full(shape=(2,), fill_value=0., dtype=float)

        if x is None and y is None and r is None and phi is None:
            pass
        elif x is not None:
            if isinstance(x, (int, float)):  # x and y are float-like
                if (r is not None) or (phi is not None):
                    raise VectorValueError("Define (x, y) or (r, theta) but not both.")

                if y is not None and isinstance(y, (int, float)):
                    array[0] = x
                    array[1] = y
                else:
                    raise VectorValueError('if x is int or float, y must be defined and must have the same type.')
            else:  # x is some kind of list, tuple, Vector, np.ndarray, ...
                if (y is not None) or (r is not None) or (phi is not None):
                    raise VectorValueError("when x is an object, you must not specify y, r, or theta")

                array = self._from_iterable_or_vector(x)
        elif r is not None and phi is not None:  # polar case, r and theta should be defined.
            if y is not None:
                raise VectorValueError("Define (x, y) or (r, theta) but not both.")

            array = self._from_polar(r, phi)
        else:
            raise VectorValueError

        self._v = array

    def __array__(self, dtype=None) -> np.ndarray:
        """Helper to allow conversion to numpy array.

        ::

            np_array = np.asarray(Vector(1, 2))

        Returns:
            numpy.ndarray
        """
        if dtype:
            return np.array(self._v, dtype=dtype)
        return self._v.copy()

    def __len__(self) -> int:
        """Length of vector.

        Returns:
            int: 2
        """
        return 2

    @property
    def x(self) -> float:  # pylint: disable=invalid-name
        """X component the vector

        Access:
            get

        Returns:
            float
        """
        return self._v[0]

    @property
    def y(self) -> float:  # pylint: disable=invalid-name
        """Y component the vector

        Access:
            get

        Returns:
            float
        """
        return self._v[1]

    @property
    def r(self) -> float:  # pylint: disable=invalid-name
        """Radial component the vector.

        Access:
            get

        Returns:
            float
        """
        return self.length

    @property
    def phi(self):
        """Angular component of vector (angle between linalg and x axis in radiant between -pi and pi).

        Access:
            get

        Returns:
            float
        """
        return np.arctan2(self._v[1], self._v[0])

    @overload
    def __getitem__(self, index: int) -> float: ...

    @overload
    def __getitem__(self, index: slice) -> np.ndarray: ...

    def __getitem__(self, index: Union[int, slice]) -> Union[float, np.ndarray]:
        """Getter for vector components.

        Args:
            index(int, slice): index/indices

        Returns:
            float, np.ndarray: float is returned if index is of type `int` and np.ndarray otherwise.
        """
        if isinstance(index, slice):
            view = self._v[index]
            view.flags.writeable = False
            return view

        return self._v[index]

    # def __iter__(self) -> Iterable[float]:
    #     for comp in self._v:
    #         yield comp

    @property
    def length(self) -> float:
        """Length (magnitude) of vector.

        Access:
            get

        Returns:
            float
        """
        return np.sqrt((self._v*self._v).sum())

    @property
    def angle_about_x_axis(self):
        """Angle between vector and positive x axis (angle will be in [0, 2pi]).

        Access:
            get

        Returns:
            float

        Raises:
            RuntimeError: Raised if self is null vector.
        """
        if np.allclose(self, 0.):
            raise RuntimeError('Cannot calculate angle of null vector')

        angle = self.phi
        while angle < 0.:
            angle += 2 * np.pi

        assert np.isclose(np.clip(angle, 0., 2 * np.pi), angle)
        return np.clip(angle, 0., 2 * np.pi)

    def close_to(self, other: Union[Vector, Iterable[float]]) -> bool:
        """Checks if `other` is close to `self` component wise.

        Args:
            other (Vector, Iterable[float]): other vector(like)

        Returns:
            bool
        """
        return np.allclose(self._v, Vector(other))

    def __eq__(self, other: object):
        """Use internally :meth:`Vector.close_to`.

        Args:
            other (object): other vector(like)

        Returns:
            bool

        Raises:
            NotImplementedError: Raised if `other` has incompatible type.
        """
        try:
            other_vec: Vector = Vector(other)  # type: ignore
        except VectorValueError as vec_va_error:
            raise NotImplementedError(f'Cannot compare {other.__class__.__name__} with vector.') from vec_va_error

        return self.close_to(other_vec)

    def normalized(self) -> Vector:
        """Create a new vector with same :attr:`Vector.phi` but :attr:`Vector.r` = 1.

        Returns:
            Vector
        """
        return self.__class__(self._v / np.linalg.norm(self._v))

    def normalized_to(self, length: float):
        """ Create a new vector :attr:`Vector.phi` but :attr:`Vector.r` = length.

        Args:
            length (float): new length of vector

        Returns:
            Vector
        """
        return self.__class__(length * self._v / np.linalg.norm(self._v))

    def rotated(self, theta: float, origin: Optional[VectorLike] = None) -> Vector:
        """Return a rotated copy the vector around `center` with angle `theta` in math. positive direction.

        Args:
            theta (float): rotation angle in rad
            origin (VectorLike): rotation center, default to [0., 0.]

        Returns:
            Vector
        """
        theta = float(theta)
        cos = np.cos(theta)
        sin = np.sin(theta)

        # m = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])

        rotated_vec = np.asarray(self)

        if origin is not None:
            origin_array = Vector(origin)

            rotated_vec -= origin_array
            rotated_vec[:] = (rotated_vec[0]*cos - rotated_vec[1]*sin, rotated_vec[1]*cos + rotated_vec[0]*sin)
            rotated_vec += origin_array
        else:
            rotated_vec[:] = (rotated_vec[0]*cos - rotated_vec[1]*sin, rotated_vec[1]*cos + rotated_vec[0]*sin)

        return self.__class__(rotated_vec)

    def mirrored(self, mirror_axis: VectorLike) -> Vector:
        """Return a mirrored version of the vector.

        Args:
            mirror_axis (VectorLike): mirror axis

        Returns:
            Vector
        """
        # pylint: disable=invalid-name
        mirror_axis = Vector(mirror_axis)

        lx, ly = mirror_axis
        mirror_matrix = np.array([[lx*lx - ly*ly, 2*lx*ly], [2*lx*ly, ly*ly - lx*lx]]) / mirror_axis.length

        return mirror_matrix @ self._v

    def dot(self, other: VectorLike):
        """Calculate dto product with other vector.

        Args:
            other(VectorLike): other vector

        Returns:
            float
        """
        # pylint: disable=protected-access
        other = Vector(other)

        return np.dot(self._v, other._v)

    def __repr__(self):
        return f"{self.__class__.__name__}({self._v[0]}, {self._v[1]})"

    def __add__(self, other: VectorLike) -> Vector:
        """Add operation: self + other.

        Args:
            other (VectorLike): summand

        Returns:
            Vector
        """
        return self.__class__(self._v + Vector(other)._v)

    def __radd__(self, other: VectorLike) -> Vector:
        """Add operation: other + self.

        Args:
            other (VectorLike): summand

        Returns:
            Vector
        """
        return self.__add__(other)

    def __sub__(self, other: VectorLike) -> Vector:
        """Subtraction operation: self - other.

        Args:
            other (VectorLike): subtrahend

        Returns:
            Vector
        """
        return self.__class__(self._v - Vector(other)._v)

    def __rsub__(self, other: VectorLike) -> Vector:
        """Subtraction operation: other - self.

        Args:
            other (VectorLike): minuend

        Returns:
            Vector
        """
        return self.__class__(Vector(other)._v - self._v)

    def __mul__(self, other: float) -> Vector:
        """Scalar multiplication: self * other.

        Args:
            other (float): multiplicand

        Returns:
            Vector
        """
        return self.__class__(self._v * float(other))

    def __rmul__(self, other: float) -> Vector:
        """Scalar multiplication: other * self.

        Args:
            other (float): multiplicand

        Returns:
            Vector
        """
        return self.__mul__(other)

    def __truediv__(self, other: float) -> Vector:
        """Scalar division: self / other.

        Args:
            other (float): divisor

        Returns:
            Vector
        """
        return self.__class__(self._v / float(other))

    def __neg__(self) -> Vector:
        """Negation: -vector.

        Returns:
            Vector
        """
        return self.__class__(-self._v)


VectorLike = Union[
    Vector,
    np.ndarray,
    Iterable[float]
]
"""vector-like objects for type hints"""


def angle_between(vec_1: VectorLike, vec_2: VectorLike) -> float:
    """Returns the the angle between two vectors.

    Args:
        vec_1 (VectorLike): first vector
        vec_2 (VectorLike): second vector

    Returns:
        float
    """
    vec_1 = Vector(vec_1)
    vec_2 = Vector(vec_2)

    return np.arccos(vec_1.dot(vec_2) / (vec_1.length * vec_2.length))
