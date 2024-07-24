import os
import sys
from typing import Dict, Any
import importlib
import logging
from pprint import pprint

ruta_utils = "/Users/walter/Programación/Blender/blw/utils.py"
blend_dir = os.path.dirname(ruta_utils)
if blend_dir not in sys.path:
    sys.path.append(blend_dir)
import blw.utils
import blw.types

importlib.reload(blw.utils)


class Tabique(object):

    @property
    def tabique_curves_data(self):
        return self._tabique_curves_data

    @tabique_curves_data.setter
    def tabique_curves_data(self, value):
        self._tabique_curves_data = value

    @property
    def tabique_curves(self):
        return self._tabique_curves

    @tabique_curves.setter
    def tabique_curves(self, value):
        self._tabique_curves = value

    def __init__(self) -> None:
        self._tabique_curves = []
        self._json_curves_data = blw.utils.Utils.read_json(
            "/Users/walter/Programación/Blender/diablos/cabeza/cara/nariz/data.json")
        # self._tabique_curves_data = [{"curve_name": "raiz",
        #                               "coordinates": [(-0.01, 0, 0),
        #                                               (-0.005, 0.001, 0),
        #                                               (0, 0.003, 0),
        #                                               (0.005, 0.001, 0),
        #                                               (0.01, 0, 0)]},
        #                              {"curve_name": "puente",
        #                               "coordinates": [(-0.02, 0, 0),
        #                                               (-0.003, 0.02, 0),
        #                                               (0, 0.028, 0),
        #                                               (0.003, 0.02, 0),
        #                                               (0.02, 0, 0)]},
        #                              {"curve_name": "dorso",
        #                               "coordinates": [(-0.025, 0, 0),
        #                                               (-0.02, 0.02, 0),
        #                                               (0, 0.040, 0),
        #                                               (0.02, 0.02, 0),
        #                                               (0.025, 0, 0)]},
        #                              {"curve_name": "suprapunta",
        #                               "coordinates": [(-0.024, 0, 0),
        #                                               (-0.02, 0.022, 0),
        #                                               (0, 0.042, 0),
        #                                               (0.02, 0.022, 0),
        #                                               (0.024, 0, 0)]},
        #                              {"curve_name": "punta_nasal",
        #                               "coordinates": [(-0.03, 0, 0),
        #                                               (-0.017, 0.025, 0.003),
        #                                               (0, 0.07, 0.006),
        #                                               (0.017, 0.025, 0.003),
        #                                               (0.03, 0, 0)]},
        #                              {"curve_name": "surco",
        #                               "coordinates": [(-0.01, 0, 0),
        #                                               (-0.003, 0.002, 0),
        #                                               (0, 0.02, 0),
        #                                               (0.003, 0.002, 0),
        #                                               (0.01, 0, 0)]}]
        self._tabique_curves_data = self._json_curves_data["tabique_curves_data"]
        self._curve_data = [{"coordinates": [tuple(coord) for coord in curves_dictionary["coordinates"]],
                            "curve_name": curves_dictionary["curve_name"]} for
                           curves_dictionary in self._tabique_curves_data]
        self._tabique_curves = [blw.utils.Utils.make_3d_curve(coordinates=elem["coordinates"],
                                                             curve_name=elem["curve_name"],
                                                             close=True) for elem in self._curve_data]


if __name__ == "__main__":
    t = Tabique()
    print(t.tabique_curves)
