# diablos_base.py
# 29/06/24
# Walter Rojas <walter.rojas@me.com>
# Clase base de ¡Diablos!


import abc
import bpy


class MiMetaClass(type(abc.ABC), type(bpy.types.Operator)):
    """
    Metaclase que se usa como parámetro en múltiple herencia
    para resolver el conflicto de tipo. El método type(class) devuelve
    el metaclass de class que se pasa como super clase de MiMetaClass
    que la convierte en una clase que construye clases.
    """
    pass


class DiablosBase(abc.ABC, bpy.types.Operator, metaclass=MiMetaClass):
    bl_idname = "object.mi_operator_personalizado"
    bl_label = "Mi Operator personalizado"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def register(cls) -> None:
        print(f"Clase {cls} registrada")

    @classmethod
    def unregister(cls) -> None:
        pass

    # Sobreescritura del método preconstruído __subclasshook__
    # con el que se valida si la subclase pertenece a la clase
    @classmethod
    def __subclasshook__(cls, C):
        if cls is DiablosBase:
            if any("metodo_enganche" in B.__dict__ for B in C.__mro__):
                return True
        return NotImplemented

    # ----- PROPIEDADES

    # posicion: bpy.props.FloatVectorProperty(
    #     name="posicion",
    #     description="Posición del rasgo",
    # )
    #
    # dimensiones: bpy.props.FloatVectorProperty(
    #     name="dimensiones",
    #     description="Dimensiones del rasgo",
    # )
    #
    # def set_posicion(self, valor: bpy.props.FloatVectorProperty):
    #     pass
    #
    # def get_posicion(self) -> bpy.props.FloatVectorProperty:
    #     pass
    #
    # def set_dimensiones(self, valor: bpy.props.FloatVectorProperty):
    #     pass
    #
    # def get_dimensiones(self) -> bpy.props.FloatVectorProperty:
    #     pass

    @staticmethod
    def metodo_estatico(v1, v2):
        return v1 + v2

    @classmethod
    def poll(cls, context):
        print(f"Context: {context.object}")
        return context.object is not None

    # Métodos que deben ser sobre escritos
    # por la clase que hereda de DiablosBase.
    @abc.abstractmethod
    def execute(self, context):
        pass

    @abc.abstractmethod
    def draw(self, context):
        pass

    @abc.abstractmethod
    def invoke(self, context, event):
        pass
