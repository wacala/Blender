# test_op.py
# 17/06/24
# WR
# Test

bl_info = {
    "name": "test",
    "author": "wr <walter.rojas@me.com>",
    "version": (1, 0),
    "blender": (4, 1, 0),
    "location": "View3D > Add > Mesh > test",
    "description": "Test",
    "warning": "",
    "doc_url": "",
    "category": "mesh",
}

import bpy
from bpy.types import Operator, Panel
from bpy.props import IntProperty, FloatProperty


class MESH_OT_plantilla(Operator):
    """Test"""
    bl_idname = "mesh.plantilla_operador"
    bl_label = "Test"
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

class VIEW3D_PT_test_op(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_catergory = "Monkeys"
    bl_label = "Grid"

    def draw(self, context):
        pass


def register():
    bpy.utils.register_class(MESH_OT_plantilla)
    bpy.utils.register_class(VIEW3D_PT_test_op)


def unregister():
    bpy.utils.unregister_class(MESH_OT_plantilla)
    bpy.utils.unregister_class(VIEW3D_PT_test_op)


if __name__ == "__main__":
    register()
