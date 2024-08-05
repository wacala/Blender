import bpy


class CurvePropertiesGroup(bpy.types.PropertyGroup):
    curve_width: bpy.props.FloatProperty(
        name="Curve width",
        default=1.0,
        min=0.0,
        max=2.0,
        step=1,
    )

    curve_length: bpy.props.FloatProperty(
        name="Curve length",
        default=1.0,
        min=0.0,
        max=2.0,
        step=1,
    )

    curve_height: bpy.props.FloatProperty(
        name="Curve height",
        default=1.0,
        min=0.0,
        max=2.0,
        step=1,
    )

    @staticmethod
    def set_curve_properties(prop):
        if isinstance(prop, CurvePropertiesGroup):
            props_names = ["curve_with", "curve_length", "curve_height"]
            for prop_name in props_names:
                setattr(prop, prop_name, 1.0)


class TabiqueCurvesProperties(bpy.types.PropertyGroup):
    raiz: bpy.props.PointerProperty(name="Raiz", type=CurvePropertiesGroup)
    puente: bpy.props.PointerProperty(name="Puente", type=CurvePropertiesGroup)
    dorso: bpy.props.PointerProperty(name="Dorso", type=CurvePropertiesGroup)
    suprapunta: bpy.props.PointerProperty(name="Suprapunta", type=CurvePropertiesGroup)
    punta: bpy.props.PointerProperty(name="Punta", type=CurvePropertiesGroup)
    surco: bpy.props.PointerProperty(name="Surco", type=CurvePropertiesGroup)

    def init_variables(self):
        for prop_name in ['raiz_curve_properties', 'puente_curve_properties', 'dorso_curve_properties',
                          'suprapunta_curve_properties', 'punta_curve_properties', 'surco_curve_properties']:
            prop = getattr(self, prop_name)
            self.set_curve_properties(prop)


class FosasCurvesProperties(bpy.types.PropertyGroup):
    pass


classes = (CurvePropertiesGroup, TabiqueCurvesProperties)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.curve_properties_group = bpy.props.PointerProperty(type=CurvePropertiesGroup)
    bpy.types.Scene.tabique_curves_properties = bpy.props.PointerProperty(type=TabiqueCurvesProperties)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.curve_properties_group
    del bpy.types.Scene.tabique_curves_properties


if __name__ == "__main__":
    register()
