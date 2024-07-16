import sys
import os
import importlib
import bpy

ruta_1: str = "/Users/walter/Programación/Blender/diablos"
ruta_1_dir: str = os.path.dirname(ruta_1)
if ruta_1_dir not in sys.path:
    sys.path.insert(0, str(ruta_1_dir))
import diablos.diablos_base

ruta_2: str = "/Users/walter/Programación/Blender/blw"
ruta_2_dir: str = os.path.dirname(ruta_2)
if ruta_2_dir not in sys.path:
    sys.path.insert(0, str(ruta_2_dir))
import blw
import blw.types
import blw.utils

importlib.reload(diablos.diablos_base)
importlib.reload(blw.types)
importlib.reload(blw.utils)

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
        default=0.04,
        min=0.005,
        max=0.05,
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
        default=-0.04,
        min=-0.025,
        max=-0.005,
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

    are_groups_created: bpy.props.BoolProperty(default=False)

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
        min=0.0012,
        max=0.04,
        default=0.009,
        step=1,
        precision=3,
    )

    def __init__(self):
        self.fosa_derecha = None
        self.fosa_izquierda = None

    @classmethod
    def poll(cls, context):
        return bpy.context.area.type == 'VIEW_3D'

    def execute(self, context):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1)
        self.fosa_derecha = context.object
        self.fosa_derecha.scale = (self.ancho_fosa_derecha, self.largo_fosa_derecha, self.alto_fosa_derecha)
        self.fosa_derecha.location = (self.distancia_entre_fosas/2, self.y_fosa_derecha, self.z_fosa_derecha)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1)
        self.fosa_izquierda = context.object
        self.fosa_izquierda.scale = (self.ancho_fosa_izquierda, self.largo_fosa_izquierda, self.alto_fosa_izquierda)
        self.fosa_izquierda.location = (-self.distancia_entre_fosas/2, self.y_fosa_izquierda, self.z_fosa_izquierda)
        self.distancia_entre_fosas = blw.utils.Utils.calcula_distancia_con_numpy(
            self.fosa_izquierda.location,
            self.fosa_derecha.location
        )
        self.tabique()
        bpy.context.view_layer.update()
        return {'FINISHED'}

    def draw(self, context):
        self.fosas()

    def invoke(self, context, event):
        return self.execute(context)

    @staticmethod
    def tabique():
        # Requiere de tres curvas
        # Raíz
        # Punta nasal
        # Surco
        curva_surco = blw.utils.Utils.make_3d_curve(
            coordinates=[(-0.01, 0, 0),
                         (-0.007, 0.018, 0),
                         (0, 0.03, 0),
                         (0.007, 0.018, 0),
                         (0.01, 0, 0)],
            curve_name="surco",
            close=True
        )
        curva_punta_nasal = blw.utils.Utils.make_3d_curve(
            coordinates=[(-0.02, 0, 0),
                         (-0.017, 0.025, 0),
                         (0, 0.065, 0),
                         (0.017, 0.025, 0),
                         (0.02, 0, 0)],
            curve_name="punta_nasal",
            close=True
        )
        curva_raiz = blw.utils.Utils.make_3d_curve(
            coordinates=[(-0.04, 0, 0),
                         (-0.03, 0.035, 0),
                         (0, 0.075, 0),
                         (0.03, 0.035, 0),
                         (0.04, 0, 0)],
            curve_name="raíz",
            close=True
        )
        nose_curves = [curva_raiz, curva_punta_nasal, curva_surco]
        meshes_from_curves = blw.utils.Utils.convert_curves_to_meshes(curves=nose_curves)
        blw.utils.Utils.make_vertices_groups_from_meshes(meshes=meshes_from_curves)
        blw.utils.Utils.distribute_objects(objects=meshes_from_curves, axis='Z', offset=0.035)
        blw.utils.Utils.link_objects_on_collection(objects_to_be_linked=meshes_from_curves)
        joined_object = blw.utils.Utils.join_objects_in_list(object_list=meshes_from_curves)
        print(f"add_faces_to_mesh_vertices: {blw.utils.Utils.add_faces_to_mesh_vertices(joined_object[0])}")

    def fosas(self):
        layout = self.layout
        col = layout.column()
        col.label(text="Fosa derecha")
        col.prop(self, "ancho_fosa_derecha")
        col.prop(self, "largo_fosa_derecha")
        col.prop(self, "alto_fosa_derecha")
        col.prop(self, "y_fosa_derecha")
        col.prop(self, "z_fosa_derecha")
        col.label(text="Fosa izquierda")
        col.prop(self, "ancho_fosa_izquierda")
        col.prop(self, "largo_fosa_izquierda")
        col.prop(self, "alto_fosa_izquierda")
        col.prop(self, "y_fosa_izquierda")
        col.prop(self, "z_fosa_izquierda")
        col.label(text="Fosas")
        col.prop(self, "distancia_entre_fosas")


def register():
    bpy.utils.register_class(OBJECT_OT_nariz)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_nariz)

