# cabeza_diablos.py
# 27/06/24
# Walter Rojas <walter.rojas@me.com>
# Clase asbtracta que describe la cabeza de diablo


from abc import ABCMeta
from abc import abstractmethod

import bpy
from blw import excepciones


class CabezaDiablo(metaclass=ABCMeta, bpy.types.Operator):

    def __init__(self, ojo_der, ojo_izq, nariz, boca):
        self.ojo_der = ojo_der
        self.ojo_izq = ojo_izq
        self.nariz = nariz
        self.boca = boca

    # ----- PROPIEDADES

    @property
    def ojo_der(self):
        return self._ojo_der

    @ojo_der.setter
    def ojo_der(self, v):
        # Ejemplo de validación 
        # para casos con propiedades 
        # con restricción
        if v != '':
            self._ojo_der = v
        else:
            raise ValueError('Propiedad ojo_der no indicada')

    @ojo_der.deleter
    def ojo_der(self):
        del self._ojo_der

    @property
    def ojo_izq(self):
        return self._ojo_izq

    @ojo_izq.setter
    def ojo_izq(self, v):
        self._ojo_izq = v

    @ojo_izq.deleter
    def ojo_izq(self):
        del self._ojo_izq

    @property
    def nariz(self):
        return self._nariz

    @nariz.setter
    def nariz(self, v):
        self._nariz = v

    @nariz.deleter
    def nariz(self):
        del self._nariz

    @property
    def boca(self):
        return self._boca

    @boca.setter
    def boca(self, v):
        self._boca = v

    @boca.deleter
    def boca(self):
        del self._boca

    # ----- MÉTODOS

    # Métodos asociados a la clase
    # que no requieren una instancia
    # para ser invocados. Reciben un parámetro 'cls'
    # que es una referencia a la clase. Se llaman
    # usando la forma CabezaDiablo.fabrica_ojo_der()
    # Son muy útiles para instanciar objetos de la clase CabezaDiablo
    # y con el truco a continuación, se evitaría tener que cambiar
    # el nombre del constructor en cada método fabricante caso de renombrarla
    # y una innecesaria repetición.

    @classmethod
    # Múltiples métodos fabricantes para 
    # construir diferentes variantes de la misma clase, por
    # ejemplo si la clase fuera Pizza podríamos
    # tener un método fabricante margarita() y otro vegetariana()
    def fabrica_cabeza(cls, ojo_izq: object, ojo_der: object, nariz: object, boca: object) -> object:
        return cls(ojo_izq, ojo_der, nariz, boca)

    # Métodos que cuando se invocan
    # no requieren una instancia,
    # no reciben un parámetro
    # implícito y no modifican el estado mismo de la clase.
    # Se usan como métodos utilería que toman valores e ignoran
    # atributos de clase. Se llaman de la forma CabezaDiablo.metodo_estatico()
    @staticmethod
    def metodo_estatico(v1, v2):
        return v1 + v2

    # Sobreescritura del método preconstruído __subclasshook__
    # con el que se valida si la subclase pertenece a la clase
    @classmethod
    def __subclasshook__(cls, C):
        if cls is CabezaDiablo:
            if any("hook_method" in B.__dict__ for B in C.__mro__):
                return True
        return NotImplemented

    @classmethod
    def poll(cls, context):
        pass

    @abstractmethod
    def excecute(self, context):
        pass

    @abstractmethod
    def draw(self, context):
        pass
