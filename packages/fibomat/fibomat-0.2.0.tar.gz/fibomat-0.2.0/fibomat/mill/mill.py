"""Provide the :class:`Mill` class."""
from typing import Optional

from fibomat.units import QuantityType
from fibomat.mill.ionbeam import IonBeam


# def _beam_required(func):
#     def decorator(self, *args, **kwargs):
#         if not self._beam:
#             raise RuntimeError('beam must be specified to access this property.')
#         return func(self, *args, **kwargs)
#     return decorator


class Mill:
    """The `Mill` class is used to specify the, dwell_time per spot and the number of repats for a pattern.

    Optionally, the class can hold an object describing the shape of the ion beam which is needed if any kind of
    optimization is done.
    """
    def __init__(self, dwell_time: QuantityType, repeats: int, beam: Optional[IonBeam] = None, _special_settings=None):
        """
        Args:
            dwell_time (QuantityType): dwell time per spot
            repeats (int): number of repeats
            beam (IonBeam, optional): ion beam describing object
        """
        self._dwell_time = dwell_time
        self._repeats: int = int(repeats)
        self._beam: Optional[IonBeam] = beam
        self._special_settings = _special_settings

    @classmethod
    def special_settings(
        cls,
        dwell_time: QuantityType = None,
        repeats: int = None,
        beam: Optional[IonBeam] = None,
        **kwargs
    ):
        """Create a Mill with special settings which can be used in custom backends.

        Args:
            dwell_time (QuantityType, optional): dwell time per spot
            repeats (int, optional): number of repeats
            beam (IonBeam, optional): ion beam describing object
            \*\*kwargs: other settings

        Returns:
            Mill
        """
        return cls(dwell_time, repeats, beam, kwargs)

    @property
    def dwell_time(self) -> QuantityType:
        """Dwell time per spot.

        Access:
            get

        Returns:
            QuantityType
        """
        return self._dwell_time.to('ms')

    @property
    def repeats(self) -> int:
        """Number of repeats.

        Access:
            get

        Returns:
            int
        """
        return self._repeats

    @property
    def beam_specified(self) -> bool:
        """Check if beam is specified.

        Access:
            get

        Returns:
            bool
        """
        return self._beam is not None

    @property
    def beam(self) -> Optional[IonBeam]:
        """return beam object

        Access:
            get

        Returns:
            Optional[IonBeam]
        """
        return self._beam

    def __repr__(self) -> str:
        return '{}(dwell_time={!r}, repeats={!r}, beam={!r}, _special_settings={!r})'.format(
            self.__class__.__name__, self.dwell_time, self._repeats, self._beam, self._special_settings
        )
