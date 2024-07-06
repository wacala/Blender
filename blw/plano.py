# plano.py
# 24/06/24
# Walter Rojas <walter.rojas@me.com>
# Constructor de planos

bl_info = {
    "name": "plano",
    "author": "Walter Rojas <walter.rojas@me.com>",
    "version": (1, 0),
    "blender": (4, 1, 0),
    "location": "View3D > Add > Mesh > plano",
    "description": "Constructor de planos",
    "warning": "",
    "doc_url": "",
    "category": "Mesh",
}

import bpy
import mathutils
import os
import sys
import importlib

ruta_excepciones = "/Users/walter/Programación/Blender/blw/excepciones.py"

blend_dir = os.path.dirname(ruta_excepciones)
if blend_dir not in sys.path:
    sys.path.append(blend_dir)

ruta_utils = "/Users/walter/Programación/Blender/blw/utils.py"

blend_dir = os.path.dirname(ruta_utils)
if blend_dir not in sys.path:
    sys.path.append(blend_dir)

import utils
import excepciones
importlib.reload(utils)
importlib.reload(excepciones)


class MESH_OT_plano(bpy.types.Operator):
    """Constructor de planos"""
    bl_idname = "mesh.plano"
    bl_label = "Plano"
    bl_options = {'REGISTER', 'UNDO'}

    x: bpy.props.FloatProperty(
        name="x",
        description="Coordenada en x del punto del plano",
    )

    y: bpy.props.FloatProperty(
        name="y",
        description="Coordenada en y del punto del plano",
    )

    z: bpy.props.FloatProperty(
        name="z",
        description="Coordenada en z del punto del plano",
    )

    x_normal: bpy.props.FloatProperty(
        name="x_normal",
        description="Coordenada en x de la normal",
    )

    y_normal: bpy.props.FloatProperty(
        name="y_normal",
        description="Coordenada en y de la normal",
    )

    z_normal: bpy.props.FloatProperty(
        name="z_normal",
        description="Coordenada en z de la normal",
    )

    pos_x: bpy.props.FloatProperty(
        name="pos_x",
        description="Coordenada en x del plano",
    )

    pos_y: bpy.props.FloatProperty(
        name="pos_y",
        description="Coordenada en y del plano",
    )

    pos_z: bpy.props.FloatProperty(
        name="pos_z",
        description="Coordenada en z del plano",
    )

    rotacion_x: bpy.props.FloatProperty(
        name="rotacion_x",
        description="Rotación del plano en el eje x",
    )

    rotacion_y: bpy.props.FloatProperty(
        name="rotacion_y",
        description="Rotación del plano en el eje y",
    )

    rotacion_z: bpy.props.FloatProperty(
        name="rotacion_z",
        description="Rotación del plano en el eje z",
    )

    # @classmethod
    # def poll(cls, context):
    #     modo_actual = context.active_object.mode
    #     if modo_actual != 'EDIT':
    #         raise excepciones.ExcepcionModo

    def execute(self, context: object):
        try:
            bpy.ops.mesh.primitive_plane_add()
            plano_nuevo = bpy.context.selected_objects[0]
            plano_nuevo.rotation_euler = (self.rotacion_x, self.rotacion_y, self.rotacion_z)
            utils.Utils.mueve_bmesh(plano_nuevo, [self.pos_x, self.pos_y, self.pos_z])
            print(f"Plano: {plano_nuevo}")
            return {'FINISHED'}
        except Exception as e:
            print(e)

    def draw(self, context):
        """

        Args:
            context:
        """
        layout = self.layout
        layout.label(text="Punto y normal del plano")
        row = layout.row(heading="Punto")
        row.prop(self, "x")
        row.prop(self, "y")
        row.prop(self, "z")
        row = layout.row(heading="Normal")
        row.prop(self, "x_normal")
        row.prop(self, "y_normal")
        row.prop(self, "z_normal")
        row = layout.row(heading="Posición")
        row.prop(self, "pos_x")
        row.prop(self, "pos_y")
        row.prop(self, "pos_z")
        row = layout.row(heading="Rotación")
        row.prop(self, "rotacion_x")
        row.prop(self, "rotacion_y")
        row.prop(self, "rotacion_z")


def register():
    bpy.utils.register_class(MESH_OT_plano)


def unregister():
    bpy.utils.unregister_class(MESH_OT_plano)


if __name__ == "__main__":
    register()
