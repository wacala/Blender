# diablos_base.py
# 29/06/24
# Walter Rojas <walter.rojas@me.com>
# Clase base de ¡Diablos!


import abc
import bpy


class MyMetaClass(type(abc.ABC), type(bpy.types.Operator)):
    """
    Metaclase que se usa como parámetro en múltiple herencia
    para resolver el conflicto de tipo. El método type(class) devuelve
    el metaclass de class que se pasa como super clase de MiMetaClass
    que la convierte en una clase que construye clases.
    """
    pass


class DiablosBase(abc.ABC, bpy.types.Operator, metaclass=MyMetaClass):
    @classmethod
    def register(cls) -> None:
        print(f"Clase {cls} registered")

    @classmethod
    def unregister(cls) -> None:
        print(f"Clase {cls} unregistered")

    # Sobreescritura del método preconstruído __subclasshook__
    # con el que se valida si la subclase pertenece a la clase
    @classmethod
    def __subclasshook__(cls, C):
        if cls is DiablosBase:
            if any("metodo_enganche" in B.__dict__ for B in C.__mro__):
                return True
        return NotImplemented


    @staticmethod
    def metodo_estatico(v1, v2):
        return v1 + v2

    @classmethod
    @abc.abstractmethod
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
