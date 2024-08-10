import bpy


class CurvePropertiesGroup(bpy.types.PropertyGroup):
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    curve_width: bpy.props.FloatProperty(
        name="Curve width",
        description="Holds the curve scale value in X",
        default=1.0,
        min=0.5,
        max=4.0,
    ) # type: ignore

    curve_length: bpy.props.FloatProperty(
        name="Curve length",
        description="Holds the curve scale value in Y",
        default=1.0,
        min=0.5,
        max=4.0,
    ) # type: ignore


class TabiqueCurvesProperties(bpy.types.PropertyGroup):
    scale: bpy.props.PointerProperty(name="scale", type=CurvePropertiesGroup) # type: ignore
    puente: bpy.props.PointerProperty(name="Puente", type=CurvePropertiesGroup) # type: ignore
    dorso: bpy.props.PointerProperty(name="Dorso", type=CurvePropertiesGroup) # type: ignore
    suprapunta: bpy.props.PointerProperty(name="Suprapunta", type=CurvePropertiesGroup) # type: ignore
    punta: bpy.props.PointerProperty(name="Punta", type=CurvePropertiesGroup) # type: ignore
    surco: bpy.props.PointerProperty(name="Surco", type=CurvePropertiesGroup) # type: ignore


class FosasCurvesProperties(bpy.types.PropertyGroup):
    pass
