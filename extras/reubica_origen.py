import bpy


class VIEW3D_PT_reubica_origen(bpy.types.Panel):
    '''Clase que hereda la clase Panel del UI de Blender'''
    # Dónde poner el panel en la UI
    '''Area del Viewport listadas aquí 3D
    https://docs.blender.org/api/current/bpy_types_enum_items/space_type_items.html#rna-enum-space-type-items'''
    bl_space_type = "VIEW_3D"
    '''Región del área lateral listadas aquí 
    https://docs.blender.org/api/current/bpy_types_enum_items/region_type_items.html#rna-enum-region-type-items'''
    bl_region_type = "UI"

    # Agregar etiquetas
    bl_category = "Categoría"
    bl_label = "Etiqueta"

    def draw(self, context):
        '''Definir el acomodo del panel'''


# Registrar el panel en Blender
# print(Points([[1, 2], [9, -18], [12, 4], [2, 1]]).are_coplanar())
def register():
    bpy.utils.register_class(VIEW3D_PT_reubica_origen)


def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_reubica_origen)


if __name__ == "__main__":
    register()
