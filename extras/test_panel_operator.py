import bpy

# Define a PropertyGroup with some properties
class MyProperties(bpy.types.PropertyGroup):
    my_int: bpy.props.IntProperty(
        name="My Integer",
        description="An integer property",
        default=23,
        min=10,
        max=100
    )
    my_float: bpy.props.FloatProperty(
        name="My Float",
        description="A float property",
        default=1.0,
        min=0.0,
        max=10.0
    )
    my_string: bpy.props.StringProperty(
        name="My String",
        description="A string property",
        default="Hello"
    )

# Define an Operator to act as a controller
class MyOperator(bpy.types.Operator):
    bl_idname = "wm.my_operator"
    bl_label = "Print Property Values"

    def execute(self, context):
        my_props = context.scene.my_props
        self.report({'INFO'}, f"Integer: {my_props.my_int}, Float: {my_props.my_float}, String: {my_props.my_string}")
        return {'FINISHED'}

# Define a Panel to display the properties and the operator button
class MyPanel(bpy.types.Panel):
    bl_label = "My Custom Panel"
    bl_idname = "PT_MyPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        my_props = scene.my_props

        layout.prop(my_props, "my_int")
        layout.prop(my_props, "my_float")
        layout.prop(my_props, "my_string")
        layout.operator("PT_MyPanel")

# Register and unregister classes
def register():
    bpy.utils.register_class(MyProperties)
    bpy.types.Scene.my_props = bpy.props.PointerProperty(type=MyProperties)
    bpy.utils.register_class(MyOperator)
    bpy.utils.register_class(MyPanel)

def unregister():
    bpy.utils.unregister_class(MyPanel)
    bpy.utils.unregister_class(MyOperator)
    del bpy.types.Scene.my_props
    bpy.utils.unregister_class(MyProperties)

if __name__ == "__main__":
    register()
