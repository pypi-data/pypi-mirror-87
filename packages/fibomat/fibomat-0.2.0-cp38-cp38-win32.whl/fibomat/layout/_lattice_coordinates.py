from __future__ import annotations
from typing import Optional, Tuple

import numpy as np

# from .groupbase import GroupBase
from fibomat.linalg import VectorLike, Vector, Transformable
from fibomat.linalg.boundingbox import BoundingBox


class LatticeCoordinates(Transformable):
    def __init__(
            self,
            nu: int, nv: int,
            du: float, dv: float, alpha: Optional[float] = np.pi / 2,
            center: Optional[VectorLike] = None
    ):
        """

        Args:
            nu (int): elements in `du` direction
            nv (int): elements in `dv` direction
            du (float): length of first grid vector, default to `(1, 0)`
            dv (float): length of second grid vector, default to `(0, 1)`
        """
        super().__init__()

        if nu < 1 or nv < 1:
            raise ValueError('nu and nv must be at least 1.')

        if np.isclose(alpha, 0.) or alpha < 0.:
            raise ValueError('alpha must be greater than 0.')

        self._du: float = float(du)
        self._dv: float = float(dv)

        u: Vector = self._du * Vector(1, -1).rotated(-alpha/2).normalized()
        v: Vector = self._dv * Vector(1, -1).rotated(+alpha/2).normalized()

        self._nu: int = int(nu)
        self._nv: int = int(nv)

        self._center: Vector = Vector(center) if center else Vector()

        shift_u = -1
        shift_v = -1

        pos = -(nu+shift_u)/2 * u - (nv+shift_v)/2 * v + self._center

        self._grid: np.ndarray = np.empty(shape=(nu, nv), dtype=object)
        for iu in range(nu):
            # grid_row = []
            for iv in range(nv):
                self._grid[iu, iv] = pos
                # grid_row.append(pos)
                pos += v
            pos -= nv * v
            pos += u
            # self._grid.append(grid_row)

    @property
    def nu(self) -> int:
        return self._nu

    @property
    def nv(self) -> int:
        return self._nv
    #
    # @property
    # def du(self) -> float:
    #     return self._du
    #
    # @property
    # def dv(self) -> float:
    #     return self._dv
    #
    # @property
    # def u(self) -> linalg.Vector:
    #     return self._u
    #
    # @property
    # def v(self) -> linalg.Vector:
    #     return self._v

    @property
    def grid(self) -> np.ndarray:
        return self._grid

    def __getitem__(self, point: Tuple[int, int]) -> Vector:
        iv, iu = point
        return self._grid[iv][iu]

    @property
    def bounding_box(self) -> BoundingBox:
        """
        :class:`~fibomat.boundingbox.BoundingBox`: bounding box of shape (getter)

        Access:
            get
        """
        raise NotImplementedError

    @property
    def center(self) -> Vector:
        return self._center

    def _impl_translate(self, trans_vec: VectorLike) -> None:
        self._center += trans_vec

        trans_func = np.frompyfunc(lambda vec: vec + trans_vec, 1, 1)
        trans_func(self._grid)

    def _impl_rotate(self, theta: float) -> None:
        # TODO: needed?
        self._center = self._center.rotated(theta)

        rot_func = np.frompyfunc(lambda vec: vec.rotated(theta), 1, 1)
        rot_func(self._grid)

    def _impl_scale(self, fac: float) -> None:
        # TODO: needed?
        self._center = self._center.scaled(fac)

        scale_func = np.frompyfunc(lambda vec: vec * fac, 1, 1)
        scale_func(self._grid)

    def _impl_mirror(self, mirror_axis: VectorLike) -> None:
        self._center = self._center.mirrored(mirror_axis)

        scale_func = np.frompyfunc(lambda vec: vec.mirrored(mirror_axis), 1, 1)
        scale_func(self._grid)

    # def translate(self, trans_vec: linalg.VectorLike) -> _GridCoordinates:
    #     self._center += linalg.Vector(trans_vec)
    #
    #     trans_func = np.frompyfunc(lambda vec: vec + trans_vec, 1, 1)
    #     trans_func(self._grid)
    #     # for element in np.nditer(self._grid, flags=["refs_ok"]):
    #     #     element.translate(trans_vec)
    #
    #     return self
    #
    # def simple_rotate(self, theta: float) -> None:
    #     rot_func = np.frompyfunc(lambda vec: vec.rotated(theta), 1, 1)
    #     rot_func(self._grid)
    #
    # def simple_scale(self, s: float) -> None:
    #     scale_func = np.frompyfunc(lambda vec: vec * s, 1, 1)
    #     scale_func(self._grid)

    # def group_elements(self) -> Iterable[Tuple[int, int, Vector]]:
    #     for iv in range(self._nv):
    #         for iu in range(self._nu):
    #             yield iu, iv, self._grid[iv][iu]
