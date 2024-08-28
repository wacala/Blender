import diablos.props
import blw.types
import blw.utils
import os
import sys
from typing import Dict, Any, List
import importlib

paths = ["/Users/walter/Programación/Blender/blw",
         "/Users/walter/Programación/Blender/diablos"]

for path in paths:
    path_dir: str = os.path.dirname(path)
    if path_dir not in sys.path:
        sys.path.insert(0, str(path_dir))


importlib.reload(blw.utils)


class Nostrils(object):
    def __init__(self) -> None:
        self.left_nostril = blw.utils.Utils.create_half_sphere(
            radius=0.013,
            segments=20,
            rings=15,
            name="Left_Nostril",
            location=(-0.02, 0, 0),
            )
        self.right_nostril = blw.utils.Utils.create_half_sphere(
            radius=0.013,
            segments=20,
            rings=15,
            name="Right_Nostril",
            location=(0.02, 0, 0),
            )


class Nostril:
    @property
    def nostril_width(self):
        return self.nostril_width

    @nostril_width.setter
    def nostril_width(self, value):
        self.nostril_width = value

    @property
    def nostril_height(self):
        return self.nostril_height

    @nostril_height.setter
    def nostril_height(self, value):
        self.nostril_height = value

    @property
    def nostril_length(self):
        return self.nostril_length

    @nostril_length.setter
    def nostril_length(self, value):
        self.nostril_length = value


if __name__ == "__main__":
    t = Nostrils()
