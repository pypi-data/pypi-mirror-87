from __future__ import annotations
from typing import TypeVar, Tuple, Union
from dataclasses import dataclass

from fibomat.linalg.vector import Vector, VectorLike
from fibomat.units import LengthUnit, has_length_dim


DimVectorT = TypeVar('DimVectorT', bound='DimensionedObj')


@dataclass(frozen=True)
class DimVector:
    vector: Vector
    unit: LengthUnit

    @classmethod
    def create(cls, dim_vector: Union[DimVectorT, Tuple[VectorLike, LengthUnit]]) -> DimVector:
        """Parse a object and create a :class:`DimensionedObj` from a tuple or class instance.

        No checks are performed at the arguments.

        Args:
            dim_vector: Union[DimVectorT, Tuple[VectorLike, LengthUnit]]: dimensioned vector

        Returns:
            DimVector

        Raises:
            TypeError: Raised if `DimVector` cannot be parsed.
        """
        # https://stackoverflow.com/a/390885
        def _count_iterable(i):
            return sum(1 for e in i)

        if isinstance(dim_vector, cls):
            return dim_vector

        if isinstance(dim_vector, tuple):
            error = 'dim_vector must be tuple of a Vector and a length unit. Maybe you forgot to pass a unit?'
            if len(dim_vector) != 2:
                raise TypeError(error + ' (len(dim_vector) != 2)')
            if sum(1 for _ in dim_vector[0]) != 2:
                raise TypeError(error + ' (length of vector != 2)')
            if len(dim_vector[0]) != 2 or not has_length_dim(dim_vector[1]):
                raise TypeError(error + ' (len(dim_vector[0]) != 2 or not has_length_dim(dim_vector[1]))')
            return cls(Vector(dim_vector[0]), dim_vector[1])

        raise TypeError('Cannot understand passed "dim_vector". Maybe you forgot to pass a unit?')


DimVectorLike = Union[DimVector, Tuple[VectorLike, LengthUnit]]
