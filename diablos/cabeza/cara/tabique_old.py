import os
import sys
from typing import Dict, Any, List
import importlib

ruta_utils = "/Users/walter/Programación/Blender/blw"
blend_dir = os.path.dirname(ruta_utils)
if blend_dir not in sys.path:
    sys.path.append(blend_dir)

ruta_utils = "/Users/walter/Programación/Blender/diablos"
blend_dir = os.path.dirname(ruta_utils)
if blend_dir not in sys.path:
    sys.path.append(blend_dir)

import blw
from blw import singleton

import blw.utils
import blw.types
import blw.singleton
import diablos.props

importlib.reload(blw.utils)
importlib.reload(blw.types)
importlib.reload(blw.singleton)
importlib.reload(diablos.props)


class Tabique():

    @property
    def tabique_curves(self):
        return self._tabique_curves

    @tabique_curves.setter
    def tabique_curves(self, value):
        self._tabique_curves = value

    def __init__(self) -> None:
        self._tabique_curves: List[Any] = []
        self._tabique_curves_data: List[Any] = []
        self._curve_data: List[Any] = []
        self._json_curves_data = blw.utils.Utils.read_json(
            "/Users/walter/Programación/Blender/diablos/cabeza/cara/nariz/data.json")
        self._tabique_curves_data = self._json_curves_data["tabique_curves_data"]
        self._curve_data = ({"coordinates": [tuple(coord) for coord in curves_dictionary["coordinates"]],
                             "curve_name": curves_dictionary["curve_name"]} for
                            curves_dictionary in self._tabique_curves_data)
        self._tabique_curves = [blw.utils.Utils.make_3d_curve(coordinates=elem["coordinates"],
                                                              curve_name=elem["curve_name"],
                                                              close=True) for elem in self._curve_data]



if __name__ == "__main__":
    t = Tabique()
