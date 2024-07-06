# object_ot_ojo.py
# 27/06/24
# Walter Rojas
# Constructor de un ojo parametrizable para Diablos

bl_info = {
    "name": "ojo",
    "author": "Walter Rojas <walter.rojas@me.com>",
    "version": (1, 0),
    "blender": (4, 1, 0),
    "location": "View3D > Add > Mesh > ojo",
    "description": "Constructor de un ojo parametrizable para Diablos",
    "warning": "",
    "doc_url": "",
    "category": "Object",
}

from abc import ABCMeta
from abc import abstractmethod

import bpy
from bpy.types import Operator
from bpy.props import IntProperty, FloatProperty

import os
import sys

# Técnica para importar con la ruta
# absoluta.
ruta_excepciones = "/Users/walter/Programación/Blender/blw/excepciones.py"

blend_dir = os.path.dirname(ruta_excepciones)
if blend_dir not in sys.path:
    sys.path.append(blend_dir)

import excepciones


class OBJECT_OT_ojo(metaclass=ABCMeta, Operator):
    # Antes del punto la categoría y después el id en minúsculas
    # o arroja un error de nombre
    bl_idname = "object.object_ot_ojo.py"
    bl_label = "Ojo de Diablo"
    bl_options = {'REGISTER', 'UNDO'}

    count_x: IntProperty(
        name="X",
        description="Número de Suzanes en la dirección X",
        default=2,
        min=1, soft_max=10,
    )

    count_y: IntProperty(
        name="Y",
        description="Número de Suzanes en la dirección Y",
        default=5,
        min=1, soft_max=10,
    )

    size: FloatProperty(
        name="Size",
        description="Tamaño de cada Suzane",
        default=0.5,
        min=0, soft_max=1,
    )

    # Método para validar si la operación es posible
    # según el contexto. Ej. la actual operación
    # debe hacerse en VIEW_3D de otra forma
    # el operador no debe estar disponible con F3
    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    # Donde se define la funcionalidad
    @abstractmethod
    def execute(self, context):
        # Código ejemplo transcrito del tutorial:
        # https://youtu.be/xscQ9tcN4GI?si=q_grNtGonlEZ1Xsr
        for idx in range(self.count_x * self.count_y):
            x = idx % self.count_x
            y = idx // self.count_x
            bpy.ops.mesh.primitive_monkey_add(
                size=self.size,
                location=(x, y, 1)
            )
        return {'FINISHED'}

    @abstractmethod
    def draw(self, context):
        pass


def register():
    bpy.utils.register_class(OBJECT_OT_ojo)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_ojo)


if __name__ == "__main__":
    register()
