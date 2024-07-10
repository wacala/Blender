# utils.py
# 21/05/24
# Walter Rojas
# Colección de métodos para operaciones diversas

import os
import sys
import time
import logging
import importlib
import typing

import bmesh
import bpy
import skspatial
import mathutils
import numpy
import pydantic

import blw.excepciones
import blw.types

ruta_excepciones = "/Users/walter/Programación/Blender/blw/excepciones.py"

blend_dir = os.path.dirname(ruta_excepciones)
if blend_dir not in sys.path:
    sys.path.append(blend_dir)

import blw.excepciones
importlib.reload(blw.excepciones)


class Utils:
    vertices_seleccionados: list[typing.Any] = []
    indices_vertices_seleccionados: list[int] = []
    mi_malla: bmesh.types.BMesh

    @staticmethod
    def obtiene_vertices_seleccionados() -> typing.Optional[typing.List[bmesh.types.BMesh | list]]:
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
    def mueve_bmesh(malla_b: bmesh.types.BMesh, coordenadas: typing.List[float]):
        try:
            vector_desplazamiento = mathutils.Vector(coordenadas)
            matriz_mundo_inversa = malla_b.matrix_world.copy()
            matriz_mundo_inversa.invert()
            vector_aplicado = vector_desplazamiento @ matriz_mundo_inversa
            malla_b.location += vector_aplicado
            # Si coordenadas locales...
            # Si coordenadas globales...
            return True
        except Exception as e:
            print(e)

    @staticmethod
    def obtiene_puntos_proyectados(points: skspatial.objects.Points,
                                   plane: skspatial.objects.Plane) -> skspatial.objects.Points:
        """
        Calcula los puntos pruyectados en un plano.

        Args:
            points (typing.List[float]): Los puntos a proyectarse en el plano.
            plane (skspatial.objects.Plane): El plano sobre el que se proyectarán los puntos.

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
    def crea_plano(punto: typing.List[float],
                   normal: typing.List[float]) -> typing.Optional[skspatial.objects.Plane | None]:
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
            nuevo_plano = skspatial.Plane(punto, normal)
            print(f"Plano nuevo: {nuevo_plano}")
            return nuevo_plano
        except Exception as e:
            print(f"Error: se generó un error creando el plano: {e}")

    @staticmethod
    def crea_plano_con_un_punto_y_normal(puntos: typing.List[float], normal: typing.List[float]):
        malla = bpy.data.meshes.new("")
        malla.to_mesh()
        pass

    @staticmethod
    def calcula_distancia_con_mathutils(pos1: typing.Optional[list[float] | tuple],
                                        pos2: typing.Optional[list[float] | tuple]) -> float:
        """
        Calcula la distancia con mathutils entre dos listas
        que representan coordenadas x, y, z. Más rápido
        para pocos cálculos.

        Args:
            pos1: typing.Lista de coordenadas 1.
            pos2: typing.Lista de coordenadas 2.

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
    def calcula_distancia_con_numpy(pos1: typing.Optional[list[float] | tuple],
                                    pos2: typing.Optional[list[float] | tuple]) -> float:
        """
        Calcula la distancia con numpy entre dos listas
        que representan coordenadas x, y, z. Más rápido
        para volumen alto de cálculos.

        Args:
            pos1: typing.Lista de coordenadas 1.
            pos2: typing.Lista de coordenadas 2.

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

    @staticmethod
    def construye_curva(coordinates: list[tuple[float, float, float]],
                        curve_name: str = 'curve_name',
                        curve_type: str = 'NURBS',
                        resolution: int = 3,
                        close: bool = False) -> bpy.types.Object:
        """
        Construye una curva a partir de sus coordenadas, nombre y tipo:
        'POLY', 'BEZIER', 'NURBS', 'BSPLINE', 'CARDINAL'
        Args:
            coordinates: typing.Lista de tuples de 3 dimensiones
            curve_name: Nombre de la curva para su identificación
            curve_type: Tipo de la curva: 'POLY', 'BEZIER', 'NURBS', 'BSPLINE', 'CARDINAL'
            resolution: Resolución de la curva en número de puntos de control
            close: Curva cerrada o abierta

        Returns:
            Objeto de referencia a la curva
        """
        # Crea el bloque de Datos de la Curva
        try:
            # Valida los parámetros de entrada
            if not all(isinstance(coord, tuple) and len(coord) == 3 for coord in coordinates):
                raise ValueError("Coordenadas con formato inválido. Se esperan listas de tuples de 3 dimensiones.")
            if curve_type not in blw.types.CurveType.__members__:
                raise ValueError("Tipo de curva inválido. Se espera 'POLY', 'BEZIER', 'NURBS', 'BSPLINE' o 'CARDINAL'.")
            curve_data_block = bpy.data.curves.new(curve_name, type='CURVE')
            curve_data_block.dimensions = '3D'
            curve_data_block.resolution_u = resolution

            # Mapea las coordenadas al spline
            spline = curve_data_block.splines.new(curve_type)
            if close:
                spline.use_cyclic_u = True
                spline.use_cyclic_v = True
            for i, coord in enumerate(coordinates):
                x, y, z = coord
                if curve_type == 'BEZIER':
                    spline.bezier_points.add(len(coordinates)-1)
                    spline.bezier_points[i].co = (x, y, z)
                else:
                    spline.points.add(len(coordinates)-1)
                    spline.points[i].co = (x, y, z, 1)
            # Crea el objeto
            curve_object = bpy.data.objects.new(curve_name, curve_data_block)

            # Liga el objeto y lo activa
            bpy.context.collection.objects.link(curve_object)
            bpy.context.view_layer.objects.active = curve_object
            return curve_object
        except blw.excepciones.ExcepcionErrorCreandoCurva as e:
            logging.error(e)
            return None

    @staticmethod
    def reubica_curva(spline: bpy.types.Object, new_location: typing.List[float]) -> bool:
        """
            Reubicates a curve to a new location.

            Args:
                spline: The curve to be reubicated.
                new_location: The new location for the curve.

            Returns:
                True if the reubication was successful.
            """
        try:
            if not all([isinstance(coordinate, float) for coordinate in new_location]):
                raise ValueError("Error: las coordenadas de la nueva posición deben ser números.")
            if not len(new_location) == 3:
                raise  ValueError("Error: la dimensión de la nueva ubicación debe ser 3.")
            print(f"spline {spline}")
            print(f"new_location {new_location}")
            print(f"spline.location {spline.location}")
            spline.location = new_location
            return True
        except blw.excepciones.ExcepcionReubicandoCurva as e:
            logging.error(e)
            return  False
