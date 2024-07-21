import os
import sys
from typing import Dict, Any
import importlib
import logging
from pprint import pprint

import blw.types

ruta_utils = "/Users/walter/Programación/Blender/blw/utils.py"
blend_dir = os.path.dirname(ruta_utils)
if blend_dir not in sys.path:
    sys.path.append(blend_dir)
import blw.utils

importlib.reload(blw.utils)


class Tabique(object):

    def __init__(self, tabique_curves: Dict[str, Any]) -> None:
        if "tabique_curves_data" not in tabique_curves or not isinstance(tabique_curves["tabique_curves_data"], list):
            raise ValueError("`tabique_curves` must contain a list under key 'tabique_curves_data'")
        for elem in tabique_curves["tabique_curves_data"]:
            try:
                coordinates_tuples = [tuple(coor_list) for coor_list in elem["coordinates"]]
                blw.utils.Utils.make_3d_curve(coordinates=coordinates_tuples,
                                              curve_name=elem["curve_name"],
                                              close=True)
            except Exception as e:
                logging.error(f"Error: {e}")


if __name__ == "__main__":
    actual_data = blw.utils.Utils.read_json("/Users/walter/Programación/Blender/diablos/cabeza/cara/nariz/data.json")
    t = Tabique(tabique_curves=actual_data)
