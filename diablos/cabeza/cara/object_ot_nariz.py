import sys
import os
import bpy
import importlib

ruta: str = "/Users/walter/Programación/Blender/blw"
ruta_dir: str = os.path.dirname(ruta)
if ruta_dir not in sys.path:
    sys.path.insert(0, str(ruta_dir))

ruta: str = "/Users/walter/Programación/Blender/diablos"
ruta_dir: str = os.path.dirname(ruta)
if ruta_dir not in sys.path:
    sys.path.insert(0, str(ruta_dir))

ruta: str = "/Users/walter/Programación/Blender/blw"
ruta_dir: str = os.path.dirname(ruta)
if ruta_dir not in sys.path:
    sys.path.insert(0, str(ruta_dir))

import blw.utils
import diablos
import diablos.diablos_base
import diablos.cabeza.cara.tabique
import diablos.props

importlib.reload(blw.utils)
importlib.reload(diablos.diablos_base)
importlib.reload(diablos.cabeza.cara.tabique)
importlib.reload(diablos.props)

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
        min=0.0017,
        max=0.04,
        default=0.011,
        step=1,
        precision=3,
    )

    # raiz: bpy.props.PointerProperty(
    #     type=diablos.props.TabiqueCurvesProperties.raiz
    # )

    def __init__(self):
        self.fosa_derecha = None
        self.fosa_izquierda = None
        self.tabique_curves_properties = None

    @classmethod
    def poll(cls, context):
        return bpy.context.area.type == 'VIEW_3D'

    def execute(self, context):
        self.tabique_curves_properties = context.scene.tabique_curves_properties
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1)
        self.fosa_derecha = context.object
        self.fosa_derecha.scale = (self.ancho_fosa_derecha,
                                   self.largo_fosa_derecha,
                                   self.alto_fosa_derecha)
        self.fosa_derecha.location = (self.distancia_entre_fosas / 2,
                                      self.y_fosa_derecha,
                                      self.z_fosa_derecha)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1)
        self.fosa_izquierda = context.object
        self.fosa_izquierda.scale = (self.ancho_fosa_izquierda,
                                     self.largo_fosa_izquierda,
                                     self.alto_fosa_izquierda)
        self.fosa_izquierda.location = (-self.distancia_entre_fosas / 2,
                                        self.y_fosa_izquierda,
                                        self.z_fosa_izquierda)
        self.distancia_entre_fosas = blw.utils.Utils.calcula_distancia_con_numpy(
            self.fosa_izquierda.location,
            self.fosa_derecha.location
        )
        self.makes_tabique()
        context.view_layer.update()
        return {'FINISHED'}

    def draw(self, context):
        self.fosas()
        self.tabique(context)

    def invoke(self, context, event):
        return self.execute(context)

    @staticmethod
    def makes_tabique():
        tabique = diablos.cabeza.cara.tabique.Tabique()
        meshes_from_curves = blw.utils.Utils.convert_curves_to_meshes(curves=tabique.tabique_curves)
        blw.utils.Utils.make_vertices_groups_from_meshes(meshes=meshes_from_curves)
        blw.utils.Utils.distribute_objects(objects_to_distribute=meshes_from_curves, axis='Z', offset=0.02)
        blw.utils.Utils.link_objects_on_collection(objects_to_be_linked=meshes_from_curves)
        joined_object = blw.utils.Utils.join_objects_in_list(object_list=meshes_from_curves)
        blw.utils.Utils.add_faces_to_mesh_vertices(joined_object[0])

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

    def tabique(self, context):
        self.tabique_curves_properties = context.scene.tabique_curves_properties
        prop_objects = [self.tabique_curves_properties.raiz,
                        self.tabique_curves_properties.puente,
                        self.tabique_curves_properties.dorso,
                        self.tabique_curves_properties.suprapunta,
                        self.tabique_curves_properties.punta,
                        self.tabique_curves_properties.surco
                        ]
        tabique_curves_titles = ["Raíz", "Puente", "Dorso", "Suprapunta", "Punta", "Surco"]
        objects_and_curves_titles = blw.utils.Utils.convert_zip_in_list(zip(prop_objects, tabique_curves_titles))
        print(f"objects_and_curves_titles: {objects_and_curves_titles}")
        layout = self.layout
        layout.label(text="Curvas Tabique")
        for object_and_curve_title in objects_and_curves_titles:
            layout.label(text=object_and_curve_title[1])
            print(object_and_curve_title[0])
            row = layout.row()
            col_width = row.column()
            col_length = row.column()
            col_width.prop(object_and_curve_title[0], "curve_width")
            col_length.prop(object_and_curve_title[0], "curve_length")


classes = [OBJECT_OT_nariz,
           diablos.props.CurvePropertiesGroup,
           diablos.props.TabiqueCurvesProperties]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.tabique_curves_properties = bpy.props.PointerProperty(
        type=diablos.props.TabiqueCurvesProperties)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.tabique_curves_properties
