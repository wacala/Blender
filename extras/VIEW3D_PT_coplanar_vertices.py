# https://b3d.interplanety.org/en/calling-functions-by-pressing-buttons-in-blender-custom-ui/

import bpy
from bpy.props import EnumProperty
from bpy.types import Operator, Panel
from bpy.utils import register_class, unregister_class

from skspatial.objects import Points
from skspatial.objects import Plane


class VIEW3D_PT_coplanar_vertices(Panel):
    bl_idname = "VIEW3D_PT_coplanar_vertices"
    bl_label = "Label"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Category"

    def draw(self, context):
        layout = self.layout
        layout.operator("OBJECT_OT_coplanar_vertices", text="Clear scene").accion = "CLEAR"
        layout.operator("OBJECT_OT_coplanar_vertices", text="Add cube").accion = "ADD_CUBE"
        layout.operator("OBJECT_OT_coplanar_vertices", text="Add sphere").accion = "ADD_SPHERE"


class OBJECT_OT_coplanar_vertices(Operator):
    # Se usa el "." como una regla
    # que respeta el espacio de nombres
    bl_idname = "object.coplanar_vertices"
    bl_label = "Label"
    bl_description = "This is a custom operator"
    bl_options = {"REGISTER", "UNDO"}

    action: EnumProperty(
        items=[
            ("CLEAR", "clear scene", "clear scene"),
            ("ADD_CUBE", "add cube", "add cube"),
            ("ADD_SPHERE", "add sphere", "add sphere")
        ]
    )

    def execute(self, context):
        if self.action == "CLEAR":
            self.clear_scene(context=context)
        elif self.action == "ADD_CUBE":
            self.add_cube(context=context)
        elif self.action == "ADD_SPHERE":
            self.add_sphere(context=context)
        return {"FINISHED"}

    @staticmethod
    def clear_scene(context):
        for obj in bpy.data.objects:
            bpy.data.objects.remove(obj)

    @staticmethod
    def add_cube(context):
        bpy.ops.mesh.primitive_cube_add()

    @staticmethod
    def add_sphere(context):
        bpy.ops.mesh.primitive_uv_sphere_add()


def register():
    register_class(OBJECT_OT_coplanar_vertices)
    register_class(VIEW3D_PT_coplanar_vertices)


def unregister():
    unregister_class(OBJECT_OT_coplanar_vertices)
    unregister_class(VIEW3D_PT_coplanar_vertices)


def sel_valida(s):
    obj = bpy.context.active_object
    for v in s:
        assert isinstance(v, object)
        print(v)
    return True


def num_vertices():
    pass


def construye_plano(p1, p2, p3):
    _p1, _p2, _p3 = p1, p2, p3
    pl = Plane.from_points(_p1, _p2, _p3)
    return pl


if __name__ == "__main__":
    Points([[1, 2], [9, -18], [12, 4], [2, 1]]).are_coplanar()
    register()
