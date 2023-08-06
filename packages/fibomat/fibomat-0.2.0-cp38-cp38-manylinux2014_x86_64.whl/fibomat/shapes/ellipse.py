"""Provides the :class:`Ellipse` class."""
# pylint: disable=too-many-arguments,invalid-name

from __future__ import annotations
from typing import Optional

import numpy as np

from fibomat.shapes.shape import Shape
from fibomat.linalg import VectorArray, VectorLike, Vector, rotate, translate
from fibomat.linalg.boundingbox import BoundingBox
from fibomat.shapes.arc_spline import ArcSpline, ArcSplineCompatible


class Ellipse(Shape, ArcSplineCompatible):
    """2-dim ellipse."""
    def __init__(
        self,
        a: float, b: float, theta: float = 0,
        center: Optional[VectorLike] = None,
        description: Optional[str] = None
    ):
        """

        Args:
            a (float): length of half axis in pos. x-direction (unrotated)
            b (float): length of half axis in pos. y-direction (unrotated)
            theta (float): rotation angle, default to 0
            center (VectorLike, optional): center of circle, default to (0, 0)
            description (str, optional): description
        """
        super().__init__(description)

        assert a > 0.
        assert b > 0.

        # center, axis in pos. x direction, axis in pos. y direction (all unrotated)
        self._axes = VectorArray(
            (float(a), 0.),
            (0., float(b))
        ).rotated(float(theta))

        self._center = Vector(center) if center is not None else Vector()

    def __repr__(self) -> str:
        return '{}(a={!r}, b={!r}, theta={!r}, center={!r})'.format(
            self.__class__.__name__, self.a, self.b, self.theta, self.center)

    def to_arc_spline(self) -> ArcSpline:
        from fibomat.shapes.parametric_curve import ParametricCurve

        from sympy import Curve
        from sympy.abc import t
        from sympy import sin, cos

        ellipse = ParametricCurve.from_sympy_curve(
            Curve([self.a * cos(t), self.b * sin(t)], (t, 0, 2*np.pi)),
            try_length_integration=False
        )

        ellipse_arc_spline = ellipse.to_arc_spline(.01)

        return ellipse_arc_spline.transformed(rotate(self.theta) | translate(self.center))

    @property
    def a(self) -> float:
        """Length of half axis in pos. x-direction (unrotated)

        Access:
            get

        Returns:
            float
        """
        return self._axes[0].length

    @property
    def b(self) -> float:
        """Length of half axis in pos. y-direction (unrotated)

        Access:
            get

        Returns:
            float
        """
        return self._axes[1].length

    @property
    def theta(self) -> float:
        """rotation angle of ellipse.

        Access:
            get

        Returns:
            float
        """
        return self._axes[0].angle_about_x_axis

    @property
    def center(self) -> Vector:
        return self._center

    @property
    def bounding_box(self) -> BoundingBox:
        # TODO: test this carefully!
        # https://stackoverflow.com/questions/87734/how-do-you-calculate-the-axis-aligned-bounding-box-of-an-ellipse
        # https://www.iquilezles.org/www/articles/ellipses/ellipses.htm
        u = np.array(self._axes[0])
        v = np.array(self._axes[1])

        w = np.sqrt(u*u + v*v)
        return BoundingBox.from_points([self._axes[0]+w, self._axes[0]-w])

    @property
    def is_closed(self) -> bool:
        return True

    def _impl_translate(self, trans_vec: VectorLike) -> None:
        self._center += Vector(trans_vec)

    def _impl_rotate(self, theta: float) -> None:
        self._axes = self._axes.rotated(float(theta))

    def _impl_scale(self, fac: float) -> None:
        self._axes *= float(fac)

    def _impl_mirror(self, mirror_axis: VectorLike) -> None:
        self._axes = self._axes.mirrored(mirror_axis)
        self._center = self._center.mirrored(mirror_axis)
