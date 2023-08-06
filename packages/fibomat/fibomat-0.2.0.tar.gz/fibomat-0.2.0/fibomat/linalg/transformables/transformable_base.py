"""
Provides the :class:`TransformableBase` class.
"""
from __future__ import annotations
from typing import Optional, Union, Callable, TypeVar, Any
import abc

from fibomat.linalg.vector import Vector, VectorLike
from fibomat.describable import Describable
from fibomat.linalg.transformables.transformation_builder import (
    _TransformationBuilder, _TranslationBuilder, _RotationBuilder, _ScaleBuilder, _MirrorBuilder
)
from fibomat.linalg.boundingbox import BoundingBox


T = TypeVar('T', bound='TransformableBase')  # pylint: disable=invalid-name


class TransformableBase(Describable, abc.ABC):
    """
    :class:`Transformable` is a base class providing the translate, rotate and uniform scale
    transformations.

    In order to use this mixin in a child class, the following methods and properties must be implemented:
        * :attr:`Transformable.center`
        * :meth:`Transformable.translate`
        * :meth:`Transformable.simple_rotate`
        * :meth:`Transformable.simple_scale`

    """

    def __init__(self, description: Optional[str] = None):
        """
        Args:
            pivot (VectorLike, optional): if set, the :attr:`Transformable.pivot` is set to `pivot`. If not set,
                                           :attr:`Transformable.center` is used as default.

            description (str, optional): optional description
        """
        super().__init__(description)

        self._pivot = None

    @property
    @abc.abstractmethod
    def center(self) -> Any:
        """center of the (geometric) object

        Access:
            get

        Returns:
            Any
        """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def pivot(self) -> Any:
        """Origin of the (geometric) object. If origin is set to `None`, :attr:`Transformable.center` will be
        returned.

        Pivot must be set to a callable function without parameters. ::

            transformable_obj = ...
            transformable_obj.pivot = lambda: return Vector(1, 2)
            print(transformable_obj.pivot)  # will print Vector(1, 2)

        Access:
            get/set

        Returns:
            Vector
        """
        # if self._pivot is not None:
        #     return Vector(self._pivot(self))
        # return self.center
        raise NotImplementedError

    # @pivot.setter
    # def pivot(self, value: Any):
    #     self._pivot = value

    @property
    @abc.abstractmethod
    def bounding_box(self) -> Any:
        """
        :class:`~fibomat.boundingbox.BoundingBox`: bounding box of transformable

        Access:
            get
        """
        raise NotImplementedError

    @abc.abstractmethod
    def _impl_translate(self, trans_vec: Any) -> None:
        """Translate the object by `trans_vec`.

        Args:
            trans_vec (VectorLike): translation linalg

        Returns:
            T: self
        """
        raise NotImplementedError

    @abc.abstractmethod
    def _impl_rotate(self, theta: float) -> None:
        """Rotate the object by theta.

        Args:
            theta: rotation angle

        Returns:
            None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def _impl_scale(self, fac: float) -> None:
        """Scale the object by fac.

        Args:
            fac: scale factor

        Returns:
            None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def _impl_mirror(self, mirror_axis: VectorLike) -> None:
        """Mirror the object at mirror_axis.

        Args:
            mirror_axis (VectorLike): mirror_plane

        Returns:
            None
        """
        raise NotImplementedError

    # def _apply_shifted_trafo(
    #     self: T,
    #     trafo: Callable[[float], None],
    #     arg: float,
    #     origin: Optional[Union[VectorLike, str]] = None
    # ) -> T:
    #     if origin:
    #         if isinstance(origin, str):
    #             if origin == 'center':
    #                 origin = self.center
    #             elif origin == 'pivot':
    #                 origin = self.pivot
    #             else:
    #                 raise ValueError(f'Unknown origin `{origin}`')
    #         else:
    #             origin = Vector(origin)
    #
    #         self._impl_translate(-origin)  # pylint: disable=invalid-unary-operand-type
    #         trafo(float(arg))
    #         self._impl_translate(origin)
    #     else:
    #         trafo(float(arg))
    #
    #     return self

    def translated(self: T, trans_vec: Any) -> T:
        """Return a translated copy of the object by `trans_vec`.

        Args:
            trans_vec (VectorLike): translation vector

        Returns:
            Transformable
        """
        # pylint: disable=protected-access
        clone: T = self.clone()
        clone._impl_translate(trans_vec)
        return clone

    def rotated(self: T, theta: float, origin: Optional[Union[Any, str]] = None) -> T:
        """Return a rotated copy around `origin` with angle `theta` in math. positive direction (counterclockwise).

        Args:
            theta (float): rotation angle in rad
            origin (Optional[Union[linalg.VectorLike, str]], optional):
                origin of rotation. If not set, (0,0) is used as
                origin. If origin == 'center', the
                :attr:`Transformable.center` of the object will
                be used. The same applies for the case that
                origin == 'origin' with the
                :attr:`Transformable.origin` property. Default
                to None.

        Returns:
            Transformable
        """
        # pylint: disable=protected-access
        clone: T = self.clone()
        clone._apply_shifted_trafo(clone._impl_rotate, theta, origin)
        return clone

    def scaled(self: T, fac: float, origin: Optional[Union[Any, str]] = None) -> T:
        """Return a scale object homogeneously about `origin` with factor `s`.

        Args:
            fac (float): rotation angle in rad
            origin (Optional[Union[linalg.VectorLike, str]], optional):
                origin of rotation. If not set, (0,0) is used as
                origin. If origin == 'center', the
                :attr:`Transformable.center` of the object will
                be used. The same applies for the case that
                origin == 'origin' with the
                :attr:`Transformable.origin` property. Default
                to None.

        Returns:
            Transformable
        """
        clone: T = self.clone()
        clone._apply_shifted_trafo(clone._impl_scale, fac, origin)  # pylint: disable=protected-access
        return clone

    def mirrored(self: T, mirror_plane: Any) -> T:
        """Return a mirrored object mirrored about `mirror_plane`.

        Args:
            mirror_plane (VectorLike): mirror plane to be used.

        Returns:
            Transformable
        """
        clone: T = self.clone()
        clone._impl_mirror(mirror_plane)  # pylint: disable=protected-access
        return clone

    def transformed(self: T, transformations: _TransformationBuilder) -> T:
        """Return a transformed object. the transformation can be build by the following functions:
            - :func:`~fibomat.linalg.transformation_builder.translate`
            - :func:`~fibomat.linalg.transformation_builder.rotate`
            - :func:`~fibomat.linalg.transformation_builder.scale`
            - :func:`~fibomat.linalg.transformation_builder.mirror`

        E.g. ::

            transformable_obj.transform(translate([1, 2]) | rotate(np.pi/3) | mirror([3,4])

        Args:
            transformations (_TransformationBuilder): transformation

        Returns:
            Transformable
        """
        # pylint: disable=protected-access
        clone: T = self.clone()
        for trafo in transformations.transformations:
            if isinstance(trafo, _TranslationBuilder):
                clone._impl_translate(trafo.trans_vec)
            elif isinstance(trafo, _RotationBuilder):
                clone._apply_shifted_trafo(clone._impl_rotate, trafo.theta, trafo.origin)
            elif isinstance(trafo, _ScaleBuilder):
                clone._apply_shifted_trafo(clone._impl_scale, trafo.fac, trafo.origin)
            elif isinstance(trafo, _MirrorBuilder):
                clone._impl_mirror(trafo.mirror_plane)
            else:
                raise ValueError(f'{trafo.__class__} is an unknown transforamtion.')

        return clone
