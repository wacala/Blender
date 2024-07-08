# utils.py
# 21/05/24
# Walter Rojas
# Colección de métodos para operaciones diversas

import os
import sys
import time
from typing import Optional, List, Any

import bmesh
import bpy
from bmesh.types import BMesh
from skspatial.objects import Points, Plane
import mathutils
import numpy

ruta_excepciones = "/Users/walter/Programación/Blender/blw/excepciones.py"

blend_dir = os.path.dirname(ruta_excepciones)
if blend_dir not in sys.path:
    sys.path.append(blend_dir)

import blw.excepciones


class Utils:
    vertices_seleccionados: list[Any] = []
    indices_vertices_seleccionados: list[int] = []
    mi_malla: BMesh

    @staticmethod
    def obtiene_vertices_seleccionados() -> Optional[List[BMesh | list]]:
        """
        Obtiene los puntos seleccionados de la malla.

        Returns:
        vertices_seleccionados
        """
        try:
            Utils.valida_modo()
            Utils.mi_malla, Utils.vertices_seleccionados, \
                Utils.indices_vertices_seleccionados = Utils.valida_vertices_seleccionados()
            return Utils.vertices_seleccionados
        except Exception as e:
            print(e)

    @staticmethod
    def valida_modo() -> object:
        modo_actual = bpy.context.object.mode
        if modo_actual != 'EDIT':
            raise blw.excepciones.ExcepcionModo()
        return modo_actual

    @staticmethod
    def valida_vertices_seleccionados() -> tuple:
        """
            Valida los vértices seleccionados
        Returns:
            mi_malla
        """
        objetos_seleccionados = Utils.obtiene_obj_seleccionado()
        data_objeto = objetos_seleccionados[0].data
        mi_malla = bmesh.from_edit_mesh(data_objeto)
        vertices_seleccionados = [vert for vert in mi_malla.verts if vert.select]
        if not vertices_seleccionados:
            raise blw.excepciones.ExcepcionNoSeleccion()
        indices_vertices_seleccionados = [vert.index for vert in vertices_seleccionados]
        return mi_malla, vertices_seleccionados, indices_vertices_seleccionados

    @staticmethod
    def obtiene_obj_seleccionado() -> list:
        objetos_seleccionados = bpy.context.selected_objects
        if objetos_seleccionados[0].type != 'MESH':
            raise blw.excepciones.ExcepcionMalla(objetos_seleccionados)
        return objetos_seleccionados

    @staticmethod
    def mueve_vertices(desfase: list):
        try:
            obj = bpy.context.edit_object
            me = obj.data
            mis_vertices = Utils.mi_malla.verts
            for vert in mis_vertices:
                if vert.index in Utils.indices_vertices_seleccionados:
                    nueva_ubicacion = vert.co
                    nueva_ubicacion[0] += desfase[0]
                    nueva_ubicacion[1] += desfase[1]
                    nueva_ubicacion[2] += desfase[2]
                    vert.co = nueva_ubicacion
            bmesh.update_edit_mesh(me, loop_triangles=True)
        except Exception as e:
            print(f"Error: {e}")

    @staticmethod
    def mueve_bmesh(malla_b: BMesh, coordenadas: List[float]):
        try:
            vector_desplazamiento = mathutils.Vector(coordenadas)
            print(f"vector_desplazamiento: {vector_desplazamiento}")
            matriz_mundo_inversa = malla_b.matrix_world.copy()
            matriz_mundo_inversa.invert()
            print(f"Matriz mundo: {matriz_mundo_inversa}")
            vector_aplicado = vector_desplazamiento @ matriz_mundo_inversa
            malla_b.location += vector_aplicado
            # Si coordenadas locales...
            # Si coordenadas globales...
            return True
        except Exception as e:
            print(e)

    @staticmethod
    def obtiene_puntos_proyectados(points: Points, plane: Plane) -> Points:
        """
        Calcula los puntos pruyectados en un plano.

        Args:
            points (List[float]): Los puntos a proyectarse en el plano.
            plane (Plane): El plano sobre el que se proyectarán los puntos.

        Returns:
            puntos_proyectados: Los puntos proyectados.
        """
        puntos_proyectados = plane.project_points(points)
        return puntos_proyectados

    @staticmethod
    def proyecta_vertices_a_plano():
        vertices_seleccionados = Utils.obtiene_vertices_seleccionados()
        print(f"Vértices seleccionados: {vertices_seleccionados}")
        return True

    @staticmethod
    def crea_plano(punto: List[float], normal: List[float]) -> Optional[Plane | None]:
        """
        Construye un plano con un punto y una normal
        Args:
            punto: lista de 3 elementos que representan la
            posición del punto en el espacio
            normal: lista de 3 elementos que representan
            lo componentes de la normal en el espacio

        Returns:
            nuevo_plano:
        """
        if all(value == 0 for value in normal):
            raise blw.excepciones.ExcepcionNormal(normal)
        try:
            nuevo_plano = Plane(punto, normal)
            print(f"Plano nuevo: {nuevo_plano}")
            return nuevo_plano
        except Exception as e:
            print(f"Error: se generó un error creando el plano: {e}")

    @staticmethod
    def crea_plano_con_un_punto_y_normal(puntos: List[float], normal: List[float]):
        malla = bpy.data.meshes.new("")
        malla.to_mesh()
        pass

    @staticmethod
    def calcula_distancia_con_mathutils(pos1: list[float], pos2: list[float]) -> float:
        """
        Calcula la distancia con mathutils entre dos listas
        que representan coordenadas x, y, z. Más rápido
        para pocos cálculos.

        Args:
            pos1: Lista de corrdenadas 1.
            pos2: Lista de corrdenadas 2.

        Returns:
            La distancia.
        """
        if pos1 and pos2:
            array_pos1 = mathutils.Vector(pos1)
            array_pos2 = mathutils.Vector(pos2)
            dif = array_pos1 - array_pos2
            distance = dif.length
            return distance
        else:
            raise blw.excepciones.ExcepcionValorNulo()

    @staticmethod
    def calcula_distancia_con_numpy(pos1: list[float], pos2: list[float]) -> float:
        """
        Calcula la distancia con numpy entre dos listas
        que representan coordenadas x, y, z. Más rápido
        para muchos cálculos.

        Args:
            pos1: Lista de corrdenadas 1.
            pos2: Lista de corrdenadas 2.

        Returns:
            La distancia.
        """
        if pos1 and pos2:
            if len(pos1) != len(pos2):
                raise ValueError("Las listas de entrada no son de la misma longitud")
            array_pos1 = numpy.asarray(pos1)
            array_pos2 = numpy.asarray(pos2)
            distance = numpy.linalg.norm(array_pos1 - array_pos2)
            return distance
        else:
            raise blw.excepciones.ExcepcionValorNulo()
