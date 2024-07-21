from enum import Enum


class CurveType(Enum):
    """
    Enum representing different curve types.
    """
    POLY = 'POLY'
    BEZIER = 'BEZIER'
    NURBS = 'NURBS'
    BSPLINE = 'BSPLINE'
    CARDINAL = 'CARDINAL'

    @classmethod
    def is_valid_curve_type(cls, value) -> bool:
        return value in cls._value2member_map_

    def __str__(self) -> str:
        return f"{self.value}"


class Axis(Enum):
    """
    Enum representing different axes.
    """
    X = 'X'
    Y = 'Y'
    Z = 'Z'

    @classmethod
    def is_valid_axis(cls, value) -> bool:
        return value in {axis.value for axis in cls}

    def __str__(self) -> str:
        """
        Return the string representation of the Axis.
        """
        return f"{self.value}"
