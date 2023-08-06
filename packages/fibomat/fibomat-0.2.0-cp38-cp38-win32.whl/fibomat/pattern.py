"""
Provides the :class:`Pattern` class.
"""
# pylint: disable=protected-access
from __future__ import annotations
from typing import Generic, TypeVar, Optional

from fibomat.mill import Mill
from fibomat.units import LengthUnit, scale_factor
from fibomat.linalg.boundingbox import BoundingBox
from fibomat.linalg import VectorLike, DimTransformable, Vector, DimVector, DimVectorLike
from fibomat.raster_styles import RasterStyle
from fibomat.dimensioned_object import DimObj, DimObjLike


T = TypeVar('T', bound=DimTransformable)


class Pattern(DimTransformable, Generic[T]):
    """
    Class is used to collect a shape with a length unit,  mill settings and optional settings.
    """

    def __init__(
        self,
        dim_shape: DimObjLike[T, LengthUnit],
        mill: Mill,
        raster_style: RasterStyle,
        description: Optional[str] = None,
        **kwargs
    ):
        """

        Args:
            dim_shape (Tuple[ShapeType, units.LengthUnit]):
                tuple of a shape type and its length unit. ShapeType can be any transformable, e.g. a layout.Group or
                shapes.Line, ...
            mill (Mill): mill object
            **kwargs: additional args
        """
        super().__init__(description=description)

        self._dim_shape = DimObj.create(dim_shape)
        self._mill = mill
        self._raster_style = raster_style
        self._kwargs = kwargs

    @property
    def dim_shape(self) -> DimObj[T, LengthUnit]:
        return self._dim_shape

    @property
    def mill(self) -> Mill:
        return self._mill

    @property
    def raster_style(self) -> RasterStyle:
        return self._raster_style

    @property
    def bounding_box(self) -> BoundingBox:
        raise NotImplementedError
        # return self.dim_shape.obj.bounding_box

    @property
    def center(self) -> DimVector:
        return DimVector(self._dim_shape.obj.center, self._dim_shape.unit)

    @property
    def kwargs(self):
        return self._kwargs

    def _impl_translate(self, trans_vec: DimVectorLike) -> None:
        self._dim_shape._impl_translate(DimVector.create(trans_vec))

    def _impl_rotate(self, theta: float) -> None:
        self._dim_shape._impl_rotate(theta)

    def _impl_scale(self, fac: float) -> None:
        self._dim_shape._impl_rotate(fac)

    def _impl_mirror(self, mirror_axis: DimVectorLike) -> None:
        self._dim_shape._impl_mirror(DimVector.create(mirror_axis))
