from typing import Optional


class ExceptionsBPY(Exception):

    def __init__(self, generador_error: Optional[object] = None):
        self._generador_error = generador_error
        super().__init__(generador_error)


class ExcepcionModo(ExceptionsBPY):
    """Excepción que ocurre cuando el modo es inválido según la operación"""

    def __str__(self):
        return f"Error: modo {self._generador_error} inválido, requiere EDIT"


class ExcepcionObjeto(ExceptionsBPY):
    """Excepcion que ocurre cuando el generador_error que se suministra es nulo o es de un tipo inválido"""

    def __str__(self):
        return (f"Error: el generador_error de tipo {type(self._generador_error).__name__} es inválido: "
                f"{self._generador_error}")


class ExcepcionObjetoInvalido(ExceptionsBPY):
    def __str__(self):
        return "Error: objeto inválido"


class ExcepcionMalla(ExceptionsBPY):
    """Excepción que ocurre cuando el generador_error suministrado no es una malla"""

    def __str__(self):
        return (f"Error: el generador_error del tipo {type(self._generador_error).__name__}"
                f"es inválido, se requiere MESH")


class ExcepcionPunto(ExceptionsBPY):
    """Excepción que ocurre cuando el generador_error suministrado no es un punto"""

    def __str__(self):
        return f"Error: el generador_error del tipo {type(self._generador_error).__name__} es inválido, se requiere ls"


class ExcepcionPlano(ExceptionsBPY):
    """Excepción que ocurre cuando el generador_error suministrado no es un plano"""

    def __str__(self):
        return f"Error: el generador_error del tipo {type(self._generador_error).__name__} es inválido, se requiere Plane"


class ExcepcionNoSeleccion(ExceptionsBPY):
    """Excepción que ocurre cuando no se selecciona vértice alguno"""

    def __str__(self):
        return "Error: no hay vértices seleccionados"


class ExcepcionNoLocal(ExceptionsBPY):
    """Excepción que ocurre cuando las coordenadas no son locales"""

    def __str__(self):
        return "Error: las coordenadas deben ser locales"


class ExcepcionNoGlobal(ExceptionsBPY):
    """Excepción lanzada cuando las coordenadas no son globales"""

    def __str__(self):
        return "Error: las coordenadas deben ser globales"


class ExcepcionNormal(ExceptionsBPY):
    """Excepción lanzada cuando las coordenadas no son globales"""

    def __str__(self):
        return f"Error: la longitud de la normal no debe ser cero, {self._generador_error}"


class ExcepcionCreacionPlano(ExceptionsBPY):
    """Excepción lanzada si algo sale mal en la creación del plano"""

    def __str__(self):
        return "Error: el plano no pudo crearse"


class ExcepcionValorNulo(ExceptionsBPY):
    """Excepción lanzada si el valor es nulo"""

    def __str__(self):
        return "Error: alguna de las variables es nula"


class ExcepcionErrorCreandoCurva(ExceptionsBPY):
    """Excepción lanzada si hay error en la construcción de una curva"""

    def __str__(self):
        return f"Error: la curva no pudo crearse {self._generador_error}"


class ExcepcionDistribuyendoObjeto(ExceptionsBPY):
    """Excepción lanzada si hay error reubicando una curva"""

    def __str__(self):
        return f"Error: no pudieron distribuirse los objetos {self._generador_error}"


class ExcepcionObjetosLigados(ExceptionsBPY):
    """Excepción lanzada si hay error ligando objetos a la escena"""
    def __str__(self):
        return "Error: los objetos no pudieron ligarse a la escena"
