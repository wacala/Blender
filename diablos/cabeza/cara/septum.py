import diablos.props
import blw.types
import blw.utils
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


importlib.reload(blw.utils)
importlib.reload(blw.types)
importlib.reload(diablos.props)


class Septum(object):
    @property
    def septum_curves_data(self) -> List[Any]:
        return self._septum_curves_data

    @septum_curves_data.setter
    def septum_curves_data(self, value):
        self._septum_curves_data = value

    @property
    def septum_curves(self) -> List[Any]:
        return self._septum_curves

    @septum_curves.setter
    def septum_curves(self, value):
        self._septum_curves = value

    def __init__(self) -> None:
        self.septum_curves = []
        self.septum_curves_data= []
        self.septum_coordinates = []
        self.curve_data: List[Any] = []
        self.json_curves_data = blw.utils.Utils.read_json_2("diablos/data/face.json", "septum_curves_data")
        self.curve_data = ({"coordinates": [tuple(coord) for coord in curves_dictionary["coordinates"]],
                            "curve_name": curves_dictionary["curve_name"]} for
                            curves_dictionary in self.json_curves_data)
        self.septum_coordinates = blw.utils.Utils.get_coordinates(self.json_curves_data)
        print(f"self.septum_coordinates: {self.septum_coordinates}")
        self.septum_curves = [blw.utils.Utils.make_3d_curve(coordinates=elem["coordinates"],
                                                            curve_name=elem["curve_name"],
                                                            close=True) for elem in self.curve_data]


if __name__ == "__main__":
    t = Septum()
