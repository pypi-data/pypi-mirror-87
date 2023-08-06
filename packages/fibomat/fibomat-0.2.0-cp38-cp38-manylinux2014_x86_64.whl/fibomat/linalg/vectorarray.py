"""
Provides the :class:`VectorArray` class.
"""

from __future__ import annotations
from typing import Optional, Iterable, Union, Iterator, overload
import collections.abc

import numpy as np

from fibomat.linalg.vector import Vector, VectorValueError, VectorLike


class VectorArrayValueError(ValueError):
    """
    Exception of this type is raised if any non supported value type is passed to VectorArray.__init__
    """


class VectorArray(collections.abc.Iterable):
    """Class represents immutable list of vectors."""

    def __init__(self, *args):
        """
        Possible `Vector` initializations:
        * `VectorArray([[x1, y1], [x2, y2], ...])`
        * `VectorArray([x1, y1], [x2, y2], ...)`
        * `VectorArray(Vector([x1, y1]), (x2, y2), ...)`
        * `VectorArray([Vector([x1, y1]), (x2, y2), ...])`

        Args:
            *args: arguments

        Raises:
            VectorArrayValueError: Raised if parameters are not understood.
        """

        if not args:
            raise VectorArrayValueError('Cannot construct empty vector array.')

        if isinstance(args[0], self.__class__):
            self._vs = np.asarray(args[0])
        elif isinstance(args[0], np.ndarray):
            self._vs = np.array(args[0], dtype=float)
            if len(self._vs.shape) != 2:
                raise VectorArrayValueError(
                    f'Input array has wrong number dimensions. It should be 2 but got {len(self._vs.shape)}'
                )
            if self._vs.shape[1] != 2:
                raise VectorArrayValueError(
                    f'Input array has wrong dimension. It should be (N, 2) but got {self._vs.shape}'
                )
        else:
            array = []
            try:
                for vec in args:
                    array.append(np.asarray(Vector(vec)))
            except VectorValueError:
                array = []
                try:
                    for vec in args[0]:
                        array.append(np.asarray(Vector(vec)))
                except VectorValueError as vec_val_error:
                    raise VectorArrayValueError('Cannot understand args for VectorArray') from vec_val_error

            self._vs = np.asarray(array)

    def __array__(self):
        """Helper to allow conversion to numpy array.

        ::

            np_array = np.asarray(VectorArray([1, 2], [3, 4]))

        Returns:
            numpy.ndarray
        """
        return self._vs.copy()

    def __len__(self) -> int:
        """Number of individual vectors in array.

        Returns:
            int
        """
        return len(self._vs)

    @property
    def n_vectors(self) -> int:
        """Number of individual vectors in array.

        Access:
            get

        Returns:
            int
        """
        return len(self._vs)

    def iter(self) -> Iterator[Vector]:
        """Return iterable to individual vectors in the array.

        Yields:
            Iterable[Vector]
        """
        for vec in self._vs:
            yield Vector(vec)

    def __iter__(self) -> Iterator[Vector]:
        return self.iter()

    @property
    def x(self) -> np.ndarray:  # pylint: disable=invalid-name
        """X components of vectors

        Access:
            get

        Returns:
            np.ndarray: read-only view
        """
        view = self._vs[:, 0]
        view.flags.writeable = False
        return view

    @property
    def y(self) -> np.ndarray:  # pylint: disable=invalid-name
        """Y components of vectors

        Access:
            get

        Returns:
            np.ndarray: read-only view
        """
        view = self._vs[:, 1]
        view.flags.writeable = False
        return view

    @overload
    def __getitem__(self, index: int) -> Vector: ...

    @overload
    def __getitem__(self, index: slice) -> VectorArray: ...

    def __getitem__(self, index: Union[int, slice]) -> Union[VectorArray, Vector]:
        if isinstance(index, slice):
            return self.__class__(self._vs[index].copy())

        if isinstance(index, int):
            return Vector(self._vs[index])

        raise TypeError('Cannot understand index')

    @property
    def lengths(self) -> np.ndarray:
        """Lengths (norms) of individual vectors.

       Access:
           get

       Returns:
           np.ndarray
       """
        return np.sqrt((self._vs*self._vs).sum(axis=1))

    @property
    def center(self) -> Vector:
        """Mean vector.

        Access:
            get

        Returns:
            np.ndarray
        """
        return Vector(np.mean(self._vs, axis=0))

    def rotated(self, theta: float, origin: Optional[VectorLike] = None) -> VectorArray:
        """Return rotated copy around `center` with angle `theta` in math. positive direction.

        Args:
            theta (float): rotation angle in rad
            origin (VectorLike, optional): rotation center, default to [0., 0.]

        Returns:
            (vector.Vector): self
        """
        theta = float(theta)
        rot_matrix = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])

        rotated_va = np.asarray(self)

        if origin is not None:
            origin = Vector(origin)
            rotated_va -= origin
            # rotated_va = rotated_va @ m.T
            rotated_va = rot_matrix.dot(rotated_va.T).T
            rotated_va += origin
        else:
            # rotated_va = rotated_va @ m.T
            rotated_va = rot_matrix.dot(rotated_va.T).T

        return self.__class__(rotated_va)

    def mirrored(self, mirror_axis: VectorLike) -> VectorArray:
        """Return mirrored copy about `mirror_axis`.

        Args:
            mirror_axis (VectorLike): mirror axis

        Returns:
            VectorArray
        """
        # pylint: disable=invalid-name
        mirror_axis = Vector(mirror_axis)

        lx, ly = mirror_axis
        mirror_matrix = np.array([[lx*lx - ly*ly, 2*lx*ly], [2*lx*ly, ly*ly - lx*lx]]) / mirror_axis.length

        return self.__class__(mirror_matrix.dot(self._vs.T).T)

    def __repr__(self):
        return f"{self.__class__.__name__}({self._vs})"

    def __add__(self, other: VectorLike) -> VectorArray:
        """Add operation: self + other.

        Args:
            other (VectorLike): summand

        Returns:
            VectorArray
        """
        other = Vector(other)

        return self.__class__(self._vs + np.array(other))

    def __radd__(self, other: VectorLike) -> VectorArray:
        """Add operation: other + self.

        Args:
            other (VectorLike): summand

        Returns:
            VectorArray
        """
        return self.__add__(other)

    def __sub__(self, other: VectorLike) -> VectorArray:
        """Subtraction operation: self - other.

        Args:
            other (VectorLike): subtrahend

        Returns:
            VectorArray
        """
        other = Vector(other)

        return self.__class__(self._vs - np.array(other))

    def __rsub__(self, other: VectorLike) -> VectorArray:
        """Subtraction operation: other - self.

        Args:
            other (VectorLike): minuend

        Returns:
            VectorArray
        """
        other = Vector(other)

        return self.__class__(np.array(other) - self._vs)

    def __mul__(self, other: float) -> VectorArray:
        """Scalar multiplication: self * other.

        Args:
            other (float): multiplicand

        Returns:
            VectorArray
        """
        return self.__class__(self._vs * float(other))

    def __rmul__(self, other: float) -> VectorArray:
        """Scalar multiplication: other * self.

        Args:
            other (float): multiplicand

        Returns:
            VectorArray
        """
        return self.__mul__(other)

    def __truediv__(self, other: float) -> VectorArray:
        """Scalar division: self / other.

        Args:
            other (float): divisor

        Returns:
            VectorArray
        """
        return self.__class__(self._vs / float(other))

    def __neg__(self) -> VectorArray:
        """Negation: -vector.

        Returns:
            VectorArray
        """
        return self.__class__(-self._vs)


VectorArrayLike = Union[
    np.ndarray,
    Iterable[VectorLike]
]
"""vectorarray-like objects for type hints"""
