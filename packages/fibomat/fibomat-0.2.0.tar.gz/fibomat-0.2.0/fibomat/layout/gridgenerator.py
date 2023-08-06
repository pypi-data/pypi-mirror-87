from typing import TypeVar, Callable, Optional

import numpy as np

from fibomat import linalg
from fibomat.layout import grid


T = TypeVar('T')


# class GridGenerator(grid.Lattice[T]):
#     def __init__(
#             self,
#             generator: Callable[[int, int, linalg.Vector], linalg.Transformable],
#             nu: int, nv: int,
#             du: float, dv: float,
#             alpha: Optional[float] = np.pi / 2,
#             center: Optional[linalg.VectorLike] = None,
#             description: Optional[str] = None
#     ):
#         super().__init__(nu, nv, du, dv, alpha, center, description)
#
#         for iu in range(self._grid_coords.nu):
#             for iv in range(self._grid_coords.nv):
#                 self._elements[iu, iv] = generator(iu, iv, self._grid_coords[iu, iv])
