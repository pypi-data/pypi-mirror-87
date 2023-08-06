"""
Provides the :class:`BoundingBox` class.
"""
from __future__ import annotations
from typing import Optional, Union
from copy import deepcopy
import collections.abc

import numpy as np

from fibomat.linalg.vector import Vector, VectorLike
from fibomat.linalg.vectorarray import VectorArrayLike, VectorArray
from fibomat.describable import Describable


class BoundingBox(Describable):
    """
    Class represents rectangular bounding box by its lower left and upper right corners.
    """

    def __init__(self, lower_left: VectorLike, upper_right: VectorLike, description: Optional[str] = None):
        """
        Args:
            lower_left (VectorLike): lower left coordinate of box
            upper_right (VectorLike): upper right coordinate of box
            description (str, optional): description
        """
        super().__init__(description)
        self._lower_left: Vector = Vector(lower_left)
        self._upper_right: Vector = Vector(upper_right)
        self._is_valid()

    @classmethod
    def from_points(cls, points: VectorArrayLike, description: Optional[str] = None) -> BoundingBox:
        """
        Constructs rectangular bounding box containing all `points`

        Args:
            points (VectorArrayLike): points which should be included in bounding box
            description (str, optional): description

        Returns:
            (BoundingBox): new `BoundingBox`
        """

        points = np.asarray(VectorArray(points))

        return BoundingBox(
            # [np.min(points[:, 0]), np.min(points[:, 1])],
            # [np.max(points[:, 0]), np.max(points[:, 1])],
            np.min(points, axis=0),
            np.max(points, axis=0),
            description
        )

    def _is_valid(self):
        if self._lower_left.x > self._upper_right.x \
           or self._lower_left.y > self._upper_right.y:
            raise ValueError('Invalid coordinates for bounding box')

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BoundingBox):
            raise NotImplementedError
        return self._lower_left.close_to(other._lower_left) and self._upper_right.close_to(other._upper_right)

    def __repr__(self):
        return '<BoundingBox(lower_left=({}, {}), upper_right=({}, {})>'.format(
            self._lower_left.x, self._lower_left.y, self._upper_right.x, self._upper_right.y
        )

    @property
    def lower_left(self):
        """
        Vector: lower left coordinate

        Access:
            get
        """
        return self._lower_left

    @property
    def upper_right(self):
        """
        Vector: upper richt coordinate

        Access:
            get
        """
        return self._upper_right

    @property
    def width(self) -> float:
        """
        float: with of bounding box

        Access:
            get
        """
        return self._upper_right[0] - self._lower_left[0]

    @property
    def height(self) -> float:
        """
        float: with of bounding box

        Access:
            get
        """
        return self._upper_right[1] - self._lower_left[1]

    @property
    def center(self) -> Vector:
        """
        Vector: center bounding box

        Access:
            get
        """
        return (self._upper_right + self._lower_left) / 2

    def clone(self) -> BoundingBox:
        """
        Clones the bounding box

        Returns:
            (BoundingBox): cloned box
        """
        return deepcopy(self)

    def scaled(self, val: float):
        """
        Return a scaled version of the `BoundingBox`.

        Args:
            val: scale factor

        Returns:
            BoundingBox
        """
        val = float(val)

        return BoundingBox(self._lower_left * val, self._upper_right * val)

    def contains(self, other: BoundingBox) -> bool:
        """
        Checks if this bounding box contains other. Alternatively, you can use `in` syntax. Note, that a box is contains
        always itself. ::

            box_1 = BoundingBox([1, 2], [3, 4])
            box_2 = BoundingBox([1, 3], [0, 4])

            print(box_1.contains(box_2)
            # or
            print(box_2 in box_1)

        Args:
            other (BoundingBox): other box

        Returns:
            (bool): True if `self` contains `other`
        """
        if not isinstance(other, self.__class__):
            raise TypeError('other must be a instance of BoundingBox.')

        if self._lower_left.x <= other._lower_left.x \
           and self._lower_left.y <= other._lower_left.y \
           and self._upper_right.x >= other._upper_right.x \
           and self._upper_right.y >= other._upper_right.y:
            return True
        return False

    def __contains__(self, other: BoundingBox) -> bool:
        return self.contains(other)

    # TODO: allow list of vectors here.
    def extended(self, other: Union[BoundingBox, VectorLike]) -> BoundingBox:
        """
        Return a extended bounding box so that `self` and other are contained

        Args:
            other (BoundingBox): other box
        """

        clone = self.clone()

        if isinstance(other, self.__class__):
            if other not in clone:
                if other._lower_left.x < clone._lower_left.x:
                    clone._lower_left = Vector(other._lower_left.x, clone._lower_left.y)
                if other._lower_left.y < clone._lower_left.y:
                    clone._lower_left = Vector(clone._lower_left.x, other._lower_left.y)
                if other._upper_right.x > clone._upper_right.x:
                    clone._upper_right = Vector(other._upper_right.x, clone._upper_right.y)
                if other._upper_right.y > clone._upper_right.y:
                    clone._upper_right = Vector(clone._upper_right.x, other._upper_right.y)
        elif isinstance(other, Vector) or isinstance(other, collections.abc.Iterable):
            other = Vector(other)
            if other.x < clone._lower_left.x:
                clone._lower_left = Vector(other.x, clone._lower_left.y)
            if other.x > clone._upper_right.x:
                clone._upper_right = Vector(other.x, clone._upper_right.y)
            if other.y < clone._lower_left.y:
                clone._lower_left = Vector(clone._lower_left.y, other.y)
            if other.y > clone._upper_right.y:
                clone._upper_right = Vector(clone._upper_right.x, other.y)
        else:
            raise TypeError('other must be BoundingBox, Vector or Iterable[float],')

        return clone
