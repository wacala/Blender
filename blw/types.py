from enum import Enum


class CurveType(Enum):
    """
    Enum representing different curve types.
    """
    POLY: str = 'POLY'
    BEZIER: str = 'BEZIER'
    NURBS: str = 'NURBS'
    BSPLINE: str = 'BSPLINE'
    CARDINAL: str = 'CARDINAL'

    @classmethod
    def is_valid_curve_type(cls, value) -> bool:
        return value in {curvetype.value for curvetype in cls}


class Axis(Enum):
    """
    Enum representing different axes.
    """
    X: str = 'X'
    Y: str = 'Y'
    Z: str = 'Z'

    @classmethod
    def is_valid_axis(cls, value) -> bool:
        return value in {axis.value for axis in cls}
