# https://docs.blender.org/api/current/info_tips_and_tricks.html#executing-modules

import sys
import os
import bpy

path_utils_blender = "/Users/walter/Programación/Blender/blw/blw_utils.py"
path_proyecta_blender = "/blw/op_proyecta_vertices_a_plano_temp.py"

blend_dir = os.path.dirname(path_utils_blender)
if blend_dir not in sys.path:
   sys.path.append(blend_dir)
   
if path_coplanar_blender not in sys.path:
   sys.path.append(path_proyecta_blender)

import blw_utils
import exc_blw
import importlib
importlib.reload(utils)
importlib.reload(exc_blw)

class Exec():
    def exec_cmd(self):
        utils.Utils.mueve_vertices([1, -1, 0])
        # Invocar método blw_utils.Utils.proyecta(pts, plano_proy)
        # que debe tomar los puntos seleccionados
        # y solicitar un plano para proyectarlos
        points = Points([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        plane = Plane(point=[0, 0, 0], normal=[0, 0, 1])
        pp= blw_utils.Utils.obtiene_puntos_proyectados(points, plane)

ex = Exec()
ex.exec_cmd()