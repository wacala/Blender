# view3d_ot_rasgo_facial_abc.py
# 28/06/24
# Walter Rojas <walter.rojas@me.com>
# Clase abstracta base para rasgos faciales
import abc
import bpy


class VIEW3D_OT_rasgo_facial_abc(bpy.types.Operator, abc.ABC):
    __slots__ = ('__dictionary__', 'posicion_rasgo_x', 'posicion_rasgo_y',
                 'posicion_rasgo_z', 'ancho', 'largo', 'alto')
    bl_idname = "view3d.rasgos_faciales_abc"
    bl_label = "Rasgos faciales"
    bl_description = "Clase base abstracta para rasgos faciales"
    bl_options = {'REGISTER', 'UNDO'}

    action: bpy.types.EnumProperty(
        items=[
            ("CLEAR", "clear scene", "clear scene"),
            ("ADD_CUBE", "add cube", "add cube"),
            ("ADD_SPHERE", "add sphere", "add sphere")
        ]
    )

    posicion_rasgo_x: bpy.types.FloatProperty(
        name="Posición en x",
        description="Coordenada en x del rasgo",
    )

    posicion_rasgo_y: bpy.types.FloatProperty(
        name="Posición en y",
        description="Coordenada en y del rasgo",
    )

    posicion_rasgo_z: bpy.types.FloatProperty(
        name="Posición en z",
        description="Coordenada en z del rasgo",
    )

    ancho: bpy.types.FloatProperty(
        name="Ancho del rasgo",
        description="Ancho del rasgo",
    )

    largo: bpy.types.FloatProperty(
        name="Largo del rasgo",
        description="Largo del rasgo",
    )

    alto: bpy.types.FloatProperty(
        name="Altura del rasgo",
        description="Altura del rasgo",
    )

    @classmethod
    def poll(cls, context):
        pass

    @abc.abstractmethod
    def draw(self, context):
        pass

    @abc.abstractmethod
    def execute(self, context):
        pass

    def invoke(self, context, event):
        pass

    def modal(self, context, event):
        pass

    def clear_scene(self, context):
        for obj in bpy.data.objects:
            bpy.data.objects.remove(obj)

    def add_cube(self, context):
        bpy.ops.mesh.primitive_cube_add()

    def add_sphere(self, context):
        bpy.ops.mesh.primitive_uv_sphere_add()
