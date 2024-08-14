import os
import sys
import bpy
from typing import Dict, Any, List
import importlib
import logging
from pprint import pprint

ruta_utils = "/Users/walter/Programación/Blender/blw/utils"
blend_dir = os.path.dirname(ruta_utils)
if blend_dir not in sys.path:
    sys.path.append(blend_dir)

ruta_utils = "/Users/walter/Programación/Blender/diablos"
blend_dir = os.path.dirname(ruta_utils)
if blend_dir not in sys.path:
    sys.path.append(blend_dir)

import blw.utils
import blw.types
import diablos.props

importlib.reload(blw.utils)
importlib.reload(blw.types)
importlib.reload(diablos.props)


class Fosa(object):
    @property
    def fosa_curves_data(self):
        return self._fosa_curves_data

    @fosa_curves_data.setter
    def fosa_curves_data(self, value):
        self._fosa_curves_data = value

    # fosa_properties_group = bpy.props.PointerProperty(type=diablos.props.fosaCurvesProperties)

    @property
    def fosa_curves(self):
        return self._fosa_curves

    @fosa_curves.setter
    def fosa_curves(self, value):
        self._fosa_curves = value

    def __init__(self) -> None:
        self._fosa_curves: List[Any] = []
        self._fosa_curves_data: List[Any] = []
        self._curve_data: List[Any] = []
        self._json_curves_data = blw.utils.Utils.read_json(
            "/Users/walter/Programación/Blender/diablos/cabeza/cara/nariz/data.json")
        self._fosa_curves_data = self._json_curves_data["fosas_curves_data"]
        self._curve_data = ({"coordinates": [tuple(coord) for coord in curves_dictionary["coordinates"]],
                             "curve_name": curves_dictionary["curve_name"]} for
                            curves_dictionary in self._fosa_curves_data)
        self._fosa_curves = [blw.utils.Utils.make_3d_curve(coordinates=elem["coordinates"],
                                                              curve_name=elem["curve_name"],
                                                              close=True) for elem in self._curve_data]


if __name__ == "__main__":
    t = Fosa()
