"""
Provides the :class:`Site` class.
"""
from __future__ import annotations

from typing import Optional, List, Tuple, Union
from copy import deepcopy

import numpy as np

from fibomat.linalg.boundingbox import BoundingBox
from fibomat.linalg import VectorLike, Vector, DimTransformable, DimVectorLike, DimVector, Transformable
from fibomat.units import LengthUnit, UnitType, scale_factor
from fibomat.raster_styles import RasterStyle
from fibomat.mill import Mill
from fibomat import layout
from fibomat.pattern import Pattern

from fibomat.dimensioned_object import DimObj, DimObjLike


class Site(DimTransformable):
    """
    The `Site` class is used to collect shapes with its patterning settings.

    .. note:: All shape positions added to each site are interpreted relative to the site's position!

    .. note:: If fov is not passed, it will be determined by the bounding box of the added patterns.

    Args:
        position (VectorLike):
            Center coordinate of the site.
        unit(UnitType):
            length unit to be used for positioning of the site
        fov (VectorLike, optional):
            the fov (field of view) to be used
        description (str, optional):
            description of the layer

    """
    def __init__(
            self,
            dim_position: DimVectorLike,
            dim_fov: Optional[DimVectorLike] = None,
            description: Optional[str] = None
    ):
        super().__init__(description=description)

        dim_position = DimVector.create(dim_position)
        dim_fov = DimVector.create(dim_fov)

        self._center = Vector(dim_position.vector)
        # if position_unit.dimensionality != '[length]':
        #     raise ValueError('position_unit must have dimension [length]')
        self._position_unit = dim_position.unit
        self._fov = Vector(dim_fov.vector) if dim_fov is not None else None
        self._fov_unit = dim_fov.unit if dim_fov is not None else None
        # self._description: Optional[str] = str(description) if description else None

        self._patterns: List[Pattern] = []

    @property
    def center(self) -> DimVector:
        """
        :class:`~fibomat.linalg.linalg.Vector`: site's center

        Access: get
        """
        return DimVector(self._center, self._position_unit)

    @property
    def fov(self) -> DimVector:
        """
        :class:`~fibomat.linalg.linalg.Vector`: fov

        Access: get
        """
        if self._fov:
            return DimVector(self._fov, self._fov_unit)
        else:
            raise NotImplementedError
            # TODO: what todo if self.empty ?
            # bbox = self.bounding_box
            # ll = bbox.lower_left
            # up = bbox.upper_right
            #
            # bbox.extend(2*self._center - ll)
            # bbox.extend(2*self._center - up)
            #
            # scale_fac = units.scale_factor(self._fov_unit, self._)
            #
            # return linalg.Vector(bbox.width, bbox.height), self._fov_unit

    @property
    def fov_unit(self) -> LengthUnit:
        return self._fov_unit

    @property
    def squrare_fov(self) -> DimVector:
        """
        :class:`~fibomat.linalg.linalg.Vector`: fov

        Access: get
        """
        fov = self._fov
        return DimVector(Vector(fov.x, fov.x) if fov.x > fov.y else Vector(fov.y, fov.y), self._fov_unit)

    @property
    def unit(self) -> UnitType:
        """
        UnitType: length unit to be used for positioning of the site

        Access: get
        """
        return self._position_unit

    @property
    def empty(self) -> bool:
        """
        bool: True if site does not contain any pattern

        Access: get
        """
        return not bool(self._patterns)

    @property
    def bounding_box(self) -> Optional[BoundingBox]:
        """
        Optional[BoundingBox]: bounding box of the added shapes, not of the site.

        Access: get
        """
        raise NotImplementedError

        # # TODO: account for shape units
        # if self._patterns:
        #     bbox: BoundingBox = self._patterns[0].shape.bounding_box
        #     for pattern in self._patterns:
        #         bbox.extend(pattern.shape.bounding_box)
        #     return bbox
        # else:
        #     return None

    @property
    def patterns(self):
        """
        List[patterns]: contained patterns in site

        Access: get
        """
        return self._patterns

    def create_pattern(
        self,
        dim_shape: DimObjLike[Transformable, LengthUnit],
        mill: Mill,
        raster_style: RasterStyle,
        description: Optional[str] = None,
        **kwargs
    ) -> Pattern:
        pattern = Pattern(dim_shape, mill, raster_style, description=description, **kwargs)
        self.add_pattern(pattern)
        return pattern

    def add_pattern(self, ptn: Union[Pattern, layout.LayoutBase]) -> None:
        """
        Adds a :class:`fibomat.pattern.Pattern` to the site.

        Args:
            ptn (Pattern):
                new pattern
            copy (bool):
                if pattern is deep copied

        Returns:
            None
        """
        if isinstance(ptn, layout.LayoutBase):
            for extracted_pattern in ptn.layout_elements():
                self._patterns.append(extracted_pattern)
        else:
            self._patterns.append(ptn)

    def __iadd__(self, ptn:  Union[Pattern, layout.LayoutBase]) -> Site:
        """
        Adds a :class:`fibomat.pattern.Pattern` to the site.
        `ohter` is deep copied.

        Args:
            ptn: new pattern

        Returns:
            None
        """
        self.add_pattern(ptn)
        return self

    def _impl_translate(self, trans_vec: DimVectorLike) -> None:
        trans_vec = DimVector.create(trans_vec)
        self._center += scale_factor(self._position_unit, trans_vec.unit) * trans_vec.vector

        # for ptn in self._patterns:
        #     ptn._impl_translate(trans_vec)

    def _impl_rotate(self, theta: float) -> None:
        if not np.isclose(np.mod(theta, np.pi/2), 0.):
            raise ValueError('Sites can only be rotated by multiples of pi/2')

        self._center = self._center.rotated(theta)

        if not np.isclose(np.mod(theta, np.pi), 0.):
            self._fov = Vector(self._fov.y, self._fov.x)

        for ptn in self._patterns:
            ptn._impl_rotate(theta)

    def _impl_scale(self, fac: float) -> None:
        self._fov *= float(fac)

        for ptn in self._patterns:
            ptn._impl_scale(fac)

    def _impl_mirror(self, mirror_axis: DimVectorLike) -> None:
        mirror_axis = DimVector.create(mirror_axis)

        if not np.isclose(np.mod(mirror_axis.vector.angle_about_x_axis, np.pi/2), 0.):
            raise ValueError(
                'Sites can only be mirrored on an axis which has and angle of a multiple of pi/2 measured to the axes.'
            )

        self._center = self._center.mirrored(mirror_axis.vector)

        if not np.isclose(np.mod(mirror_axis.vector.angle_about_x_axis, np.pi), 0.):
            self._fov = Vector(self._fov.y, self._fov.x)

        for ptn in self._patterns:
            ptn._impl_mirror(mirror_axis)
