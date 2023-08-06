"""Provide the :class:`Group` class."""
# pylint: disable=protected-access
from __future__ import annotations
from typing import Optional, List, Iterator, Any, TypeVar, Generic
import abc

from fibomat.layout.layoutbase import LayoutBase
from fibomat.linalg import Vector, DimVector, TransformableBase, DimTransformable, Transformable, BoundingBox
from fibomat.units import LengthUnit, scale_factor
from fibomat.layout.utils import _have_same_type


T = TypeVar('T', bound=TransformableBase)


class GroupBase(LayoutBase, abc.ABC):
    def __init__(
        self,
        elements: List[TransformableBase],
        description: Optional[str] = None
    ):
        if not elements:
            raise ValueError('Length if elements must not be zero.')

        if not _have_same_type(elements):
            raise TypeError('Elements in a layout must have same (base) type.')

        self._elements: List[TransformableBase] = elements

        super().__init__(description=description)

    def _layout_elements(self) -> Iterator[TransformableBase]:
        for element in self._elements:
            yield element

    def _impl_translate(self, trans_vec: Any) -> None:
        for element in self._elements:
            element._impl_translate(trans_vec)

    def _impl_rotate(self, theta: float) -> None:
        for element in self._elements:
            element._impl_rotate(theta)

    def _impl_scale(self, fac: float) -> None:
        for element in self._elements:
            element._impl_scale(fac)

    def _impl_mirror(self, mirror_axis: Any) -> None:
        for element in self._elements:
            element._impl_mirror(mirror_axis)


class Group(GroupBase, Transformable):
    def __init__(
        self,
        elements: List[Transformable],
        description: Optional[str] = None
    ):
        super().__init__(elements=elements, description=description)

    @property
    def bounding_box(self) -> BoundingBox:
        raise NotImplementedError

    @property
    def center(self) -> Vector:
        if not self._elements:
            raise RuntimeError('Cannot calculate center of empty Group.')

        center = self._elements[0].center
        for element in self._elements[1:]:
            center += element.center
        return center / len(self._elements)


class DimGroup(GroupBase, DimTransformable):
    def __init__(
        self,
        elements: List[DimTransformable],
        description: Optional[str] = None
    ):
        super().__init__(elements=elements, description=description)

    @property
    def bounding_box(self) -> 'DimObj[BoundingBox, LengthUnit]':
        raise NotImplementedError

    @property
    def center(self) -> Any:
        if not self._elements:
            raise RuntimeError('Cannot calculate center of empty Group.')

        center = self._elements[0].center.vector
        unit = self._elements[0].center.unit
        for element in self._elements[1:]:
            center += scale_factor(unit, element.center.unit) * element.center.vector
        return DimVector(center / len(self._elements), unit)

# class Group(LayoutBase):
#     """Class to group Transformable objects together."""
#     def __init__(
#         self,
#     ):
#         if not elements:
#             raise ValueError('Length if elements must not be zero.')
#
#         if not _have_same_type(elements):
#             raise TypeError('Elements in a layout must have same (base) type.')
#
#         self._elements: List[TransformableBase] = elements
#
#         super().__init__(is_dimensioned=isinstance(self._elements[0], DimTransformable), description=description)



