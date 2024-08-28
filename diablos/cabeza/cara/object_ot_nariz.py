import importlib
import bpy
import os
import sys

paths = ["/Users/walter/Programación/Blender/blw",
         "/Users/walter/Programación/Blender/diablos"]

for path in paths:
    path_dir: str = os.path.dirname(path)
    if path_dir not in sys.path:
        sys.path.insert(0, str(path_dir))

import blw
import diablos.diablos_base
import diablos.cabeza.cara.septum
import diablos.cabeza.cara.nostrils
import diablos.props
import blw.utils

importlib.reload(blw)
importlib.reload(blw.utils)
importlib.reload(diablos)
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
    bl_idname = "object_ot.nariz"
    bl_label = "Nariz paramétrica para ¡Diablos!"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return bpy.context.area.type == 'VIEW_3D'

    def execute(self, context):
        my_props = context.scene.props
        self.septum_curves_properties = context.scene.septum_curves_properties
        self.creates_septum()
        self.creates_nostrils()
        return {'FINISHED'}

    def invoke(self, context, event):
        return self.execute(context)

    def creates_septum(self) -> diablos.cabeza.cara.septum.Septum:
        septum = diablos.cabeza.cara.septum.Septum()
        septum_mesh = blw.utils.Utils.mesh_from_curves(
            input_curves=septum.septum_curves,
            curves_axis="Z",
            curves_offset=0.02)
        blw.utils.Utils.clean_geometry(septum_mesh.name)
        return septum_mesh

    def septum_layout(self, context):
        layout = self.layout
        col = layout.column()
        col.prop(self, "test_int")

        self.septum_curves_properties = context.scene.septum_curves_properties
        prop_objects = [self.septum_curves_properties.raiz,
                        self.septum_curves_properties.puente,
                        self.septum_curves_properties.dorso,
                        self.septum_curves_properties.suprapunta,
                        self.septum_curves_properties.punta,
                        self.septum_curves_properties.surco
                        ]
        septum_curves_titles = ["Raíz", "Puente",
                                "Dorso", "Suprapunta", "Punta", "Surco"]
        objects_and_curves_titles = blw.utils.Utils.convert_zip_in_list(
            zip(prop_objects, septum_curves_titles))
        layout = self.layout
        layout.label(text="Curvas septum")
        for object_and_curve_title in objects_and_curves_titles:
            layout.label(text=object_and_curve_title[1])
            row = layout.row()
            col_width = row.column()
            col_length = row.column()
            col_width.prop(object_and_curve_title[0], "curve_width")
            col_length.prop(object_and_curve_title[0], "curve_length")

    def creates_nostrils(self):
        self.nostrils = diablos.cabeza.cara.nostrils.Nostrils()
        blw.utils.Utils.add_thickness(self.nostrils.left_nostril.name, .002)
        blw.utils.Utils.add_thickness(self.nostrils.right_nostril.name, .002)

    def nostrils_layout(self, context):
        layout = self.layout
        col = layout.column()
        scene = context.scene
        my_props = scene.props

        props_names = ["location", "width", "height", "length"]

        col.label(text="Left nostril")
        for prop_name in props_names:
            col.prop(my_props, prop_name)

        col.label(text="Right nostril")
        for prop_name in props_names:
            col.prop(my_props, prop_name)

        col.prop(self, "distancia_entre_fosas")


# Define a Panel to display the properties
class PANEL_PT_nariz(bpy.types.Panel):
    bl_label = "Panel Nariz Diablos"
    bl_idname = "PANEL_PT_nariz"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout
        layout.operator("object_ot.nariz", text="Run Nariz")


classes = [OBJECT_OT_nariz,
           PANEL_PT_nariz,
           diablos.props.CurvePropertiesGroup,
           diablos.props.SeptumCurvesProperties,
           diablos.props.Props,
           ]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.septum_curves_properties = bpy.props.PointerProperty(
        type=diablos.props.SeptumCurvesProperties)
    bpy.types.Scene.props = bpy.props.PointerProperty(
        type=diablos.props.Props)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.septum_curves_properties
    del bpy.types.Scene.props
