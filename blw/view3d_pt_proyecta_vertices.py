# view3d_pt_proyecta_vertices.py
# 18/06/24
# Walter Rojas <walter.rojas@me.com>
# Proyecta vértices
# Versión de desarrollo de Proyecta Vértices
import bpy
from bpy.types import Operator, Panel
from bpy.props import EnumProperty, FloatProperty

import os
import sys

import time
time_start = time.time()

ruta_utils = "/Users/walter/Programación/Blender/blw/utils.py"

blend_dir = os.path.dirname(ruta_utils)
if blend_dir not in sys.path:
    sys.path.append(blend_dir)

from utils import Utils

bl_info = {
    "name": "Proyecta vértices a un plano",
    "author": "Walter Rojas <walter.rojas@me.com>",
    "version": (1, 0),
    "blender": (4, 1, 0),
    "location": "View3D > Add > Mesh > Proyecta",
    "description": "Proyecta vértices seleccionados a un plano",
    "warning": "",
    "doc_url": "",
    "category": "",
}


class VIEW3D_PT_ProyectaVertices(Panel):
    """Proyecta los vértices seleccionados a un plano"""
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Mesh"
    bl_label = "Proyecta vértices"

    @classmethod
    def poll(cls, context):
        return context.object

    def draw(self, context):
        layout = self.layout
        layout.operator("view3d.plantilla_operador",
                        text="Proyecta",
                        icon="META_CUBE").accion = 'PROYECTA_VERTICES'


class VIEW3D_OT_ProyectaVertices(Operator):
    """Operador de Proyecta Vértices"""
    bl_idname = "view3d.plantilla_operador"
    bl_label = "Proyecta vértices"
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
        name="x",
        description="Coordenada en x del punto del plano",
    )

    y_normal: bpy.props.FloatProperty(
        name="y",
        description="Coordenada en y del punto del plano",
    )

    z_normal: bpy.props.FloatProperty(
        name="z",
        description="Coordenada en z del punto del plano",
    )

    accion: bpy.props.EnumProperty(
        items=[
            ("PROYECTA_VERTICES", "Proyecta vertices", "proyecta vertices")
        ]
    )

    @classmethod
    def poll(cls, context):
        objeto_activo = context.active_object
        return objeto_activo is not None

    def execute(self, context):
        if self.accion == "PROYECTA_VERTICES":
            Utils.obtiene_vertices_seleccionados()
            Utils.mueve_vertices([0, 1, 0])
            bpy.ops.mesh.primitive_plane_add()
            Utils.crea_plano([self.x, self.y, self.z], [self.x_normal, self.y_normal, self.z_normal])
        return {'FINISHED'}

    def draw(self, context):
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



def register():
    bpy.utils.register_class(VIEW3D_PT_ProyectaVertices)
    bpy.utils.register_class(VIEW3D_OT_ProyectaVertices)


def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_ProyectaVertices)
    bpy.utils.unregister_class(VIEW3D_OT_ProyectaVertices)


if __name__ == "__main__":
    register()


print("Concluyó la ejecución: %.4f sec" % (time.time() - time_start))
