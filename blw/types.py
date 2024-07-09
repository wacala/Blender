from enum import Enum


class CurveType(Enum):
    POLY = 'POLY'
    BEZIER = 'BEZIER'
    NURBS = 'NURBS'
    BSPLINE = 'BSPLINE'
    CARDINAL = 'CARDINAL'
