"""Provides the `class:`Shape` class."""
from __future__ import annotations
from typing import Optional
import abc

from fibomat.linalg import Transformable
from fibomat.linalg.boundingbox import BoundingBox


class Shape(Transformable, abc.ABC):
    """Baseclass for all shapes in the library which defines the basic interface."""

    def __init__(self, description: Optional[str] = None):
        """
        Args:
            description (str, optional): description
        """
        super().__init__(description=description)

    @abc.abstractmethod
    def __repr__(self) -> str:
        """str: repr of class"""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def is_closed(self) -> bool:
        """
        bool: True if shape is closes. This property should not be defined for 0-dim shapes

        Access:
            get
        """
        raise NotImplementedError
