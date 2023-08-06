from typing import Tuple, Sequence

import numpy as np

from fibomat.rasterizedpattern import RasterizedPattern
from fibomat.raster_styles.rasterstyle import RasterStyle
from fibomat.units import LengthUnit, TimeUnit, scale_to, scale_factor
from fibomat.dimensioned_object import DimObjLike, DimObj
from fibomat.shapes import Spot
from fibomat.mill import Mill


class SingleSpot(RasterStyle):
    def __init__(self):
        super().__init__()

    def __repr__(self) -> str:
        return '{}()'.format(self.__class__.__name__)

    @property
    def dimension(self) -> int:
        return 0

    def rasterize(
        self,
        dim_shape: DimObjLike[Spot, LengthUnit],
        mill: Mill,
        out_length_unit: LengthUnit,
        out_time_unit: TimeUnit
    ) -> RasterizedPattern:

        dim_shape = DimObj.create(dim_shape)

        if not isinstance(dim_shape.obj, Spot):
            raise RuntimeError('Only `shapes.Spot`s can have `SpotStyle` as raster style.')

        spot = dim_shape.obj
        dwell_point = [
            *(spot.position * scale_factor(out_length_unit, dim_shape.unit)),
            scale_to(out_time_unit, mill.dwell_time)
        ]

        # return RasterizedPoints(np.array([dwell_point]*mill.repeats), False)
        return RasterizedPattern(np.array([dwell_point]*mill.repeats), out_length_unit, out_time_unit)
