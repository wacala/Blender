import bpy


class TestProps(bpy.types.PropertyGroup):
    propertyDisplayTarget: bpy.props.PointerProperty(name="Object", type=bpy.types.Object)
    propertyDisplayUseActiveObject: bpy.props.BoolProperty(name="Use Active")


class TEST_OT_setPropertyDisplayTargetToActive(bpy.types.Operator):
    """Set property display target object to active"""
    bl_idname = "object.setpropertydisplaytargettoactive"
    bl_label = "Set to active"
    bl_context = "object"

    @classmethod
    def poll(cls, context):
        return bpy.context.active_object != None

    def execute(self, context):
        TestProps = context.scene.TestProps
        TestProps.propertyDisplayTarget = bpy.context.active_object
        print("#" * 7, "set to", TestProps.propertyDisplayTarget)  # for testing purposes
        return {'FINISHED'}


class TEST_PT_propertiesPanel(bpy.types.Panel):
    """Shows properties of specified object"""
    bl_label = "Object/Bone Properties"
    bl_idname = "SCENE_PT_properties"
    bl_space_type = 'VIEW_3D'
    bl_category = 'Testing'
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        scene = bpy.context.scene
        obj = context.active_object
        row = layout.row()
        row.label(text="Test panel")
        row = layout.row()
        if scene.TestProps.propertyDisplayTarget:
            row.label(text="Target name is " + scene.TestProps.propertyDisplayTarget.name)
        else:
            row.label(text="Target name is ")
        row = layout.row()
        row.prop(scene.TestProps, "propertyDisplayTarget")
        row = layout.row()
        row.operator('object.setpropertydisplaytargettoactive')


classes = (TestProps,
           TEST_OT_setPropertyDisplayTargetToActive,
           TEST_PT_propertiesPanel
           )


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.TestProps = bpy.props.PointerProperty(type=TestProps)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.TestProps


if __name__ == "__main__":
    register()