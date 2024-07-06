# view3d_ot_proyecta_vertices.py
# 18/06/24
# Walter Rojas <walter.rojas@me.com>
# Proyecta vértices
# Versión de desarrollo para un operador que proyecta vértices
# a un plano

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

import bpy
from utils import Utils


class VIEW3D_OT_proyecta_vertices(bpy.types.Operator):
    """Operador de Proyecta Vértices"""
    # Antes del punto la categoría y después el id en minúsculas
    # o arroja un error de nombre
    bl_idname = "view3d.plantilla_operador"
    bl_label = "Test operator"
    bl_options = {'REGISTER', 'UNDO'}

    action: bpy.types.EnumProperty(
        items=[
            ("PROYECTA_VERTICES", "proyecta vertices", "proyecta vertices")
        ]
    )

    # Método para validar si la operación es posible
    # según el contexto. Ej. la actual operación
    # debe hacerse en VIEW_3D de otra forma
    # el operador no debe estar disponible con F3
    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    def execute(self, context):
        if self.action == "PROYECTA_VERTICES":
            Utils.obtiene_vertices_seleccionados()
        return {'FINISHED'}

def register():
    bpy.utils.register_class(VIEW3D_OT_proyecta_vertices)

def unregister():
    bpy.utils.unregister_class(VIEW3D_OT_proyecta_vertices)

if __name__ == "__main__":
    register()
