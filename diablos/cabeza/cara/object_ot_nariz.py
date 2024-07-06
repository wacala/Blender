import sys
import os
import time
import importlib
import bpy

ruta_1: str = "/Users/walter/Programación/Blender/diablos"
ruta_1_dir: str = os.path.dirname(ruta_1)
if ruta_1_dir not in sys.path:
    # Para insertar la ruta al principio
    # y evitar posibles conflictos
    sys.path.insert(0, str(ruta_1_dir))
import diablos.diablos_base

importlib.reload(diablos.diablos_base)

time_start = time.time()

bl_info = {
    "name": "Nariz paramétrica para ¡Diablos!",
    "author": "Walter Rojas <walter.rojas@me.com>",
    "version": (1, 0),
    "blender": (4, 1, 0),
    "location": "View3D > Add > Mesh > Nariz paramétrica",
    "description": "Clase para crear una nariz paramétrica.",
    "warning": "",
    "doc_url": "",
    "category": "Object",
}


class OBJECT_OT_nariz(diablos.diablos_base.DiablosBase):
    bl_idname = "object.nariz"
    bl_label = "Nariz paramétrica para ¡Diablos!"

    x_fosa_derecha: bpy.props.FloatProperty(
        name="X",
        description="Coordenada en x de la fosa derecha",
    )

    y_fosa_derecha: bpy.props.FloatProperty(
        name="Y",
        description="Coordenada en y de la fosa derecha",
    )

    z_fosa_derecha: bpy.props.FloatProperty(
        name="Z",
        description="Coordenada en z de la fosa derecha",
    )

    x_fosa_izquierda: bpy.props.FloatProperty(
        name="X",
        description="Coordenada en x de la fosa izquierda",
    )

    y_fosa_izquierda: bpy.props.FloatProperty(
        name="Y",
        description="Coordenada en y de la fosa izquierda",
    )

    z_fosa_izquierda: bpy.props.FloatProperty(
        name="Z",
        description="Coordenada en z de la fosa izquierda",
    )

    ancho_fosa_derecha: bpy.props.FloatProperty(
        name="Ancho",
        description="Ancho de la fosa derecha",
        min=0.1,
        default=0.1,
    )

    largo_fosa_derecha: bpy.props.FloatProperty(
        name="Largo",
        description="Largo de la fosa derecha",
        min=0.1,
        default=0.1,
    )

    alto_fosa_derecha: bpy.props.FloatProperty(
        name="Alto",
        description="Alto de la fosa derecha",
        min=0.1,
        default=0.1,
    )

    ancho_fosa_izquierda: bpy.props.FloatProperty(
        name="Ancho",
        description="Ancho de la fosa izquierda",
        min=0.1,
        default=0.1,
    )

    largo_fosa_izquierda: bpy.props.FloatProperty(
        name="Largo",
        description="Largo de la fosa izquierda",
        min=0.1,
        default=0.1,
    )

    alto_fosa_izquierda: bpy.props.FloatProperty(
        name="Alto",
        description="Alto de la fosa izquierda",
        min=0.1,
        default=0.1,
    )

    distancia_entre_fosas: bpy.props.FloatProperty(
        name="Dist. ÷ fosas",
        description="Distancia entre fosas",
        min=0.001,
        default=0.008,
        step=1,
        precision=3,
    )

    def execute(self, context):
        # Dos esferas para las fosas nasales
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1)
        fosa_derecha = context.object
        fosa_derecha.scale = (self.ancho_fosa_derecha, self.largo_fosa_derecha, self.alto_fosa_derecha)
        fosa_derecha.location = (self.x_fosa_derecha, self.y_fosa_derecha, self.z_fosa_derecha)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1)
        fosa_izquierda = context.object
        fosa_izquierda.scale = (self.ancho_fosa_izquierda, self.largo_fosa_izquierda, self.alto_fosa_izquierda)
        fosa_izquierda.location = (self.x_fosa_izquierda, self.y_fosa_izquierda, self.z_fosa_izquierda)
        bpy.context.view_layer.update()
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.label(text="")
        col = layout.column()
        col.label(text="Fosa derecha")
        col.prop(self, "ancho_fosa_derecha")
        col.prop(self, "largo_fosa_derecha")
        col.prop(self, "alto_fosa_derecha")
        col.prop(self, "x_fosa_derecha")
        col.prop(self, "y_fosa_derecha")
        col.prop(self, "z_fosa_derecha")
        col.label(text="Fosa izquierda")
        col.prop(self, "ancho_fosa_izquierda")
        col.prop(self, "largo_fosa_izquierda")
        col.prop(self, "alto_fosa_izquierda")
        col.prop(self, "x_fosa_izquierda")
        col.prop(self, "y_fosa_izquierda")
        col.prop(self, "z_fosa_izquierda")
        col.label(text="Fosas")
        col.prop(self, "distancia_entre_fosas")

    def invoke(self, context, event):
        return self.execute(context)


def register():
    print("En método register()")
    bpy.utils.register_class(OBJECT_OT_nariz)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_nariz)


print("Terminó ejecución: %.4f sec" % (time.time() - time_start))