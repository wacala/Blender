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
    def left_nostril(self):
        return self._half_sphere
    
    @left_nostril.setter
    def left_nostril(self, value):
        self._left_nostril = value

    @property
    def right_nostril(self):
        return self._half_sphere
    
    @right_nostril.setter
    def right_nostril(self, value):
        self._right_nostril = value

    def __init__(self) -> None:
        self.left_nostril = blw.utils.Utils.create_half_sphere(radius=0.01, segments=20, rings=15)
        self.right_nostril = blw.utils.Utils.create_half_sphere(radius=0.01, segments=20, rings=15)


if __name__ == "__main__":
    t = Fosa()
