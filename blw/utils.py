# utils.py
# 21/05/24
# Walter Rojas
# Colección de métodos para operaciones diversas

import blw.excepciones
import os
import sys
import time
import orjson
import logging
import importlib
from typing import Optional
from typing import List
from typing import Any
from typing import Tuple
import bpy
import math
import bmesh
import mathutils
from pprint import pprint
from skspatial import objects
from unidecode import unidecode

import numpy
import blw.types

ruta_excepciones = "/Users/walter/Programación/Blender/blw/excepciones.py"

blend_dir = os.path.dirname(ruta_excepciones)
if blend_dir not in sys.path:
    sys.path.append(blend_dir)

importlib.reload(blw.excepciones)


class Utils:
    vertices_seleccionados: List[Any] = []
    indices_vertices_seleccionados: List[int] = []
    mi_malla: bmesh.types.BMesh

    @staticmethod
    def obtiene_vertices_seleccionados() -> Optional[List[bmesh.types.BMesh | List]]:
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
        objetos_seleccionados = Utils.get_selected_objects()
        data_objeto = objetos_seleccionados[0].data
        mi_malla = bmesh.from_edit_mesh(data_objeto)
        vertices_seleccionados = [
            vert for vert in mi_malla.verts if vert.select]
        if not vertices_seleccionados:
            raise blw.excepciones.ExcepcionNoSeleccion()
        indices_vertices_seleccionados = [
            vert.index for vert in vertices_seleccionados]
        return mi_malla, vertices_seleccionados, indices_vertices_seleccionados

    @staticmethod
    def get_selected_objects() -> List:
        objetos_seleccionados = bpy.context.selected_objects
        if objetos_seleccionados[0].type != 'MESH':
            raise blw.excepciones.ExcepcionMalla(objetos_seleccionados)
        return objetos_seleccionados

    @staticmethod
    def mueve_vertices(desfase: List):
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
    def mueve_bmesh(malla_b: bmesh.types.BMesh, coordenadas: List[float]):
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
    def obtiene_puntos_proyectados(points: objects.Points,
                                   plane: objects.Plane) -> objects.Points:
        """
        Calcula los puntos pruyectados en un plano.

        Args:
            points (List[float]): Los puntos a proyectarse en el plano.
            plane (objects.Plane): El plano sobre el que se proyectarán los puntos.

        Returns:
            puntos_proyectados: Los puntos proyectados.
        """
        puntos_proyectados = plane.project_points(points)
        return puntos_proyectados

    @staticmethod
    def proyecta_vertices_a_plano():
        vertices_seleccionados = Utils.obtiene_vertices_seleccionados()
        return True

    @staticmethod
    def crea_plano(punto: List[float],
                   normal: List[float]) -> Optional[objects.Plane | None]:
        """
        Construye un plano con un punto y una normal
        Args:
            punto: Lista de 3 elementos que representan la
            posición del punto en el espacio
            normal: Lista de 3 elementos que representan
            lo componentes de la normal en el espacio*

        Returns:
            nuevo_plano:
        """
        if all(value == 0 for value in normal):
            raise blw.excepciones.ExcepcionNormal(normal)
        try:
            nuevo_plano = objects.Plane(punto, normal)
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
    def calcula_distancia_con_mathutils(pos1: Optional[List[float] | tuple],
                                        pos2: Optional[List[float] | tuple]) -> float:
        """
        Calcula la distancia con mathutils entre dos Listas
        que representan coordenadas x, y, z. Más rápido
        para pocos cálculos.

        Args:
            pos1: Lista de coordenadas 1.
            pos2: Lista de coordenadas 2.

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
    def calcula_distancia_con_numpy(pos1: Optional[List[float] | tuple],
                                    pos2: Optional[List[float] | tuple]) -> float:
        """
        Calcula la distancia con numpy entre dos Listas
        que representan coordenadas x, y, z. Más rápido
        para volumen alto de cálculos.

        Args:
            pos1: Lista de coordenadas 1.
            pos2: Lista de coordenadas 2.

        Returns:
            La distancia.
        """
        if pos1 and pos2:
            if len(pos1) != len(pos2):
                raise ValueError(
                    "Las Listas de entrada no son de la misma longitud")
            array_pos1 = numpy.asarray(pos1)
            array_pos2 = numpy.asarray(pos2)
            distance = numpy.linalg.norm(array_pos1 - array_pos2)
            return distance
        else:
            raise blw.excepciones.ExcepcionValorNulo()

    @staticmethod
    def make_3d_curve(coordinates: List[tuple[float, float, float]],
                      curve_name: str = 'curve_name',
                      curve_type: str = 'NURBS',
                      resolution: int = 3,
                      close: bool = False) -> bpy.types.Object:
        """
        Construye una curva a partir de sus coordenadas, nombre y
         tipo:
        'POLY', 'BEZIER', 'NURBS', 'BSPLINE', 'CARDINAL'
        Args:
            coordinates: Lista de tuples de 3 dimensiones
            curve_name: Nombre de la curva para su identificación
            curve_type: Tipo de la curva: 'POLY', 'BEZIER', 'NURBS', 'BSPLINE', 'CARDINAL'
            resolution: Resolución de la curva en número de puntos de control
            close: Curva cerrada o abierta

        Returns:
            Objeto de referencia a la curva
        """
        try:
            if not all(isinstance(coord, tuple) and len(coord) == 3 for coord in coordinates):
                raise ValueError(
                    "Coordenadas con formato inválido. Se esperan listas de tuples de 3 dimensiones.")
            if curve_type not in blw.types.CurveType.__members__:
                raise ValueError(
                    "Tipo de curva inválido. Se espera 'POLY', 'BEZIER', 'NURBS', 'BSPLINE' o 'CARDINAL'.")
            curve_data_block = bpy.data.curves.new(curve_name, type='CURVE')
            curve_data_block.dimensions = '3D'
            curve_data_block.resolution_u = resolution
            spline = curve_data_block.splines.new(curve_type)
            if close:
                spline.use_cyclic_u = True
                spline.use_cyclic_v = True
            for i, coord in enumerate(coordinates):
                x, y, z = coord
                if curve_type == 'BEZIER':
                    spline.bezier_points.add(len(coordinates) - 1)
                    spline.bezier_points[i].co = (x, y, z)
                else:
                    spline.points.add(len(coordinates) - 1)
                    spline.points[i].co = (x, y, z, 1)
            curve_object = bpy.data.objects.new(curve_name, curve_data_block)
            return curve_object
        except blw.excepciones.ExcepcionErrorCreandoCurva as e:
            logging.error(e)
            return None

    @staticmethod
    def distribute_objects(objects_to_distribute: List[bpy.types.Object],
                           axis: str,
                           offset: float = 1) -> bool:
        """
            Distribute objects along an axis.

            Args:
                objects_to_distribute: The objects to be moved. The first and the last are the limits.
                axis: Orientation of the final arrange.
                offset: The space between objects.

            Returns:
                True if the move was successful.
        """
        try:
            if not objects_to_distribute:
                raise ValueError("objects_to_distribute list is empty")
            if not all(isinstance(obj, bpy.types.Object) for obj in objects_to_distribute):
                raise TypeError(
                    "objects_to_distribute must be a list of bpy.types.Object")
            if not blw.types.Axis.is_valid_axis(axis):
                raise ValueError(f"Error: invalid axis value {axis}")
            if offset <= 0:
                raise ValueError("Offset value must be positive")
            distance = 0
            axis_mapping = {'X': 'x', 'Y': 'y', 'Z': 'z'}
            for obj in reversed(objects_to_distribute):
                setattr(obj.location, axis_mapping[axis], distance)
                distance += offset
            return True
        except blw.excepciones.ExcepcionDistribuyendoObjeto() as e:
            logging.error(e)
            return False

    @staticmethod
    def convert_curves_to_meshes(curves: Optional[List[bpy.types.Curve] |
                                                  List]) -> Optional[List[bpy.types.Mesh] | List]:
        """Convert a list of curves to meshes

        Args:
            curves (Optional[List[bpy.types.Curve]  |  List]): _description_

        Returns:
            Optional[List[bpy.types.Mesh] | List]: _description_
        """
        converted_meshes = [
            bpy.data.objects.new(curve.name, bpy.data.meshes.new_from_object(curve)) for curve in
            curves]
        for index, new_curve_mesh in enumerate(converted_meshes):
            new_curve_mesh.data.name = curves[index].name
            new_curve_mesh.matrix_world = curves[index].matrix_world
        return converted_meshes

    @staticmethod
    def build_polygon_mesh_from_points(input_points: List[List[float]]) -> List[bpy.types.Mesh]:
        """Builds a mesh from a list of points

        Args:
            input_points (List[List[float]]): List of points to convert

        Returns:
            bpy.types.Mesh: Mesh from input points
        """
        mesh = bpy.data.meshes.new(name="PolygonMesh")
        return mesh

    @staticmethod
    def link_objects_on_collection(objects_to_be_linked: List[bpy.types.Object]) -> List[bpy.types.Object]:
        """Links the objects of the list to the scene

        Args:
            objects_to_be_linked: list of objects to be linked to the scene.

        Returns:
            linked_objects: objects linked.
        """
        try:
            linked_objects = [bpy.context.collection.objects.link(object_to_be_linked) for
                              object_to_be_linked in objects_to_be_linked]
            return linked_objects
        except blw.excepciones.ExcepcionObjetosLigados() as e:
            logging.error(f"{e}")

    @staticmethod
    def deselect_all():
        for obj in bpy.data.objects:
            obj.select_set(False)

    @staticmethod
    def select_objects(objects_to_select: List[bpy.types.Object]):
        Utils.deselect_all()
        if not all(isinstance(obj, bpy.types.Object) for obj in objects_to_select):
            raise TypeError(
                "objects_to_select must be a list of bpy.types.Object")
        for obj in objects_to_select:
            obj.select_set(True)

    @staticmethod
    def join_objects_in_list(object_list: List[bpy.types.Object]) -> bpy.types.Object:
        Utils.select_objects(object_list)
        bpy.context.view_layer.objects.active = object_list[0]
        bpy.ops.object.join()
        return bpy.context.selected_objects

    @staticmethod
    def join_objects_in_list_bmesh(object_list: List[bpy.types.Object]):
        Utils.select_objects(object_list)
        bm = bmesh.new()
        for obj in object_list:
            bm.from_mesh(obj.data)
        mesh = bpy.data.meshes.new('JoinedMesh')
        bm.to_mesh(mesh)
        mesh.update()
        obj = bpy.data.objects.new('JoinedObject', mesh)
        bpy.context.collection.objects.link(obj)

    @staticmethod
    def select_object_by_name(object_name: str):
        bpy.ops.object.select_all(action='DESELECT')
        obj = bpy.context.scene.objects.get(object_name)
        if obj:
            obj.select_set(True)

    @staticmethod
    def get_vertices_from_mesh(mesh_object: bpy.types.Mesh) -> List[tuple]:
        if mesh_object.mode == 'EDIT':
            # This works only in edit mode
            bm = bmesh.from_edit_mesh(mesh_object.data)
            vertices = [vert.co for vert in bm.verts]
        else:
            # This works only in object mode
            vertices = [vert.co for vert in mesh_object.data.vertices]
        # Coordinates as tuples
        plain_vertices = [vert.to_tuple() for vert in vertices]
        return plain_vertices

    @staticmethod
    def make_vertices_groups_from_meshes(meshes: List[bpy.types.Mesh]) -> List[bpy.types.VertexGroups]:
        vertex_groups = []
        all_vertices = [Utils.get_vertices_from_mesh(mesh) for mesh in meshes]
        for mesh_object, vertices in zip(meshes, all_vertices):
            actual_group = Utils.make_vertices_group_from_mesh(mesh=mesh_object,
                                                               group_name=f"{mesh_object.data.name}_group")
            vertex_groups.append(actual_group)
        return vertex_groups

    @staticmethod
    def make_vertices_group_from_mesh(mesh: bpy.types.Mesh,
                                      group_name: str = "Group_name") -> bpy.types.VertexGroups:
        """
        Make vertices group from a list of vertices and the object associated with it.
        Args:
            mesh: The object which the group is going to be attached to.
            group_name: Name of the group.
        """
        if not Utils.is_mesh(mesh):
            raise TypeError("mesh must be an instance of bpy.types.Mesh")
        new_vertex_group = mesh.vertex_groups.new(name=group_name)
        indexes = range(len(mesh.data.vertices))
        new_vertex_group.add(indexes, 1.0, 'REPLACE')
        return new_vertex_group

    @staticmethod
    def add_faces_to_mesh_vertices(mesh: bpy.types.Mesh):
        if not Utils.is_mesh(mesh):
            raise ValueError(f"ValueError: {mesh} type is not bpy.types.Mesh")
        list_of_vertices_indexes_by_group = list(
            Utils.get_indexes_vertices_from_mesh_by_group(mesh, index)
            for index in
            range(len(mesh.vertex_groups)))
        all_n_vertices = list(zip(*list_of_vertices_indexes_by_group))
        all_vertices_paired = Utils.convert_n_to_pairs_list(
            all_n_vertices)
        bpy.ops.object.mode_set(mode='EDIT')
        bmesh_data = bmesh.from_edit_mesh(mesh.data)
        Utils.deselect_all()
        bmesh_data.verts.ensure_lookup_table()
        for index_pair in all_vertices_paired:
            v1, v2 = index_pair
            bmesh.ops.contextual_create(
                bmesh_data, geom=[bmesh_data.verts[v1], bmesh_data.verts[v2]])
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.edge_face_add()
        return bpy.context.active_object

    @staticmethod
    def get_vertices_from_mesh_by_index_group(mesh: bpy.types.Mesh,
                                              index_of_group: int) -> List[bpy.types.MeshVertex]:
        vs = [v for v in mesh.data.vertices if index_of_group in [
            vg.group for vg in v.groups]]
        return vs

    @staticmethod
    def get_indexes_vertices_from_mesh_by_group(mesh: bpy.types.Mesh,
                                                index_of_group: int) -> List[bpy.types.MeshVertex]:
        vs = [v.index for v in mesh.data.vertices if index_of_group in [
            vg.group for vg in v.groups]]
        return vs

    @staticmethod
    def make_surface_from_mesh_curves():
        bpy.ops.object.mode_set(mode='EDIT')

    @staticmethod
    def convert_n_to_pairs_list(input_list: List[List[Any]]) -> List[Tuple[Any, Any]]:
        """
        Convert a list of trios to pairs.

        Args:
            input_list: The list of trios to convert.

        Returns:
            List of pairs.
        """
        if not input_list:
            return []
        return list((sublist[i], sublist[i + 1]) for sublist in input_list for i in range(len(sublist) - 1))

    @staticmethod
    def select_all_mesh_vertices(mesh: bpy.types.Mesh):
        if Utils.is_mesh(mesh):
            bmesh_data = mesh.data
            bm = bmesh.from_edit_mesh(bmesh_data)
            bm.select_mode = {'VERT'}
            for v in bm.verts:
                v.select = True

    @staticmethod
    def deselect_all_mesh_vertices(mesh: bpy.types.Mesh):
        if Utils.is_mesh(mesh):
            bmesh_data = mesh.data
            bm = bmesh.from_edit_mesh(bmesh_data)
            bm.select_mode = {'VERT'}
            for v in bm.verts:
                v.select = False

    @staticmethod
    def is_mesh(obj):
        return obj.type == 'MESH'

    @staticmethod
    def read_json(path_to_json):
        with open(path_to_json, "rb") as f:
            json_data = f.read()
        data = orjson.loads(json_data)
        return data

    @staticmethod
    def convert_list_to_tuple(input_list: List) -> tuple:
        if input_list is None:
            return ()
        return tuple(input_list)

    @staticmethod
    def remove_double_vertices(mesh):
        # obj = bpy.context.object
        # mesh = obj.data

        # Set the merge threshold (e.g., 0.001 for small distances)
        merge_threshold = 0.001

        # Merge vertices within the threshold
        mesh.vertices.foreach_set("select", [False] * len(mesh.vertices))
        for v in mesh.vertices:
            if not v.select:
                v.select = True
                bpy.ops.mesh.merge(type="DISTANCE")
                v.select = False

    @staticmethod
    def replace_accented_chars(strings: List[str]) -> List[str]:
        """_summary_

        Args:
            strings (List[str]): _description_

        Returns:
            List[str]: _description_
        """
        return [unidecode(s) for s in strings]

    @staticmethod
    def lowercase_string_list(lower_case_strings: List[str]) -> List[str]:
        """_summary_

        Args:
            lower_case_strings (List[str]): _description_

        Returns:
            List[str]: _description_
        """
        return [word.lower() for word in lower_case_strings]

    @staticmethod
    def convert_zip_in_list(zip_object: zip) -> List[list]:
        """ Converts input zip_object into a list with error handling"""
        try:
            return list(map(list, zip_object))
        except Exception as e:
            print(f"Error occurred during conversion: {e}")

    @staticmethod
    def mesh_from_curves(input_curves: List[bpy.types.Curve],
                         curves_offset: float = 1,
                         curves_axis: str = "Z") -> bpy.types.Mesh:
        """Constructs a mesh from a list of curves.

        Args:
            input_curves (List[bpy.types.Curve]): Curves to construct mesh from.
            curves_offset (float, optional): Curves offset. Defaults to 1.
            curves_axis (str, optional): Distribution axis. Defaults to "Z".

        Returns:
            bpy.types.Mesh: Mesh normalized.
        """
        meshes_from_curves = Utils.convert_curves_to_meshes(
            curves=input_curves)
        Utils.make_vertices_groups_from_meshes(meshes=meshes_from_curves)
        Utils.distribute_objects(
            objects_to_distribute=meshes_from_curves, axis=curves_axis, offset=curves_offset)
        Utils.link_objects_on_collection(
            objects_to_be_linked=meshes_from_curves)
        joined_object = Utils.join_objects_in_list(
            object_list=meshes_from_curves)
        return Utils.add_faces_to_mesh_vertices(joined_object[0])

    @staticmethod
    def mesh_from_points(mesh_input_points: List[list[float]],
                         polygon_offset: float = 1,
                         curves_axis: str = "Z") -> bpy.types.Mesh:
        polygon_mesh_from_points = Utils.build_polygon_mesh_from_points(
            input_points=mesh_input_points)
        return polygon_mesh_from_points

    @staticmethod
    def create_verts_faces_sphere(radius=10, segments=32, rings=16):
        """Creates a sphere

        Args:
            radius (int, optional): Radius of the sphere. Defaults to 10.
            segments (int, optional): Segments of the sphere. Defaults to 32.
            rings (int, optional): Rings of the sphere. Defaults to 16.

        Returns:
            _type_: _description_
        """
        vertices = []
        faces = []

        for i in range(rings + 1):
            lat = math.pi * i / rings
            for j in range(segments):
                lon = 2 * math.pi * j / segments
                x = radius * math.sin(lat) * math.cos(lon)
                y = radius * math.sin(lat) * math.sin(lon)
                z = radius * math.cos(lat)
                vertices.append((x, y, z))

        for i in range(rings):
            for j in range(segments):
                next_i = i + 1
                next_j = (j + 1) % segments
                faces.append((i * segments + j, i * segments + next_j,
                             next_i * segments + next_j, next_i * segments + j))

        return vertices, faces

    @staticmethod
    def create_verts_faces_half_sphere(radius=10, segments=32, rings=16):
        """Create a half-sphere

        Args:
            radius (int, optional): Radius of the half-sphere. Defaults to 10.
            segments (int, optional): Segments of the half-sphere. Defaults to 32.
            rings (int, optional): Rings of the half-sphere. Defaults to 16.
        """
        vertices = []
        faces = []

        # Create vertices
        for i in range(rings + 1):
            theta = math.pi * i / rings / 2  # Only half-sphere
            for j in range(segments):
                phi = 2 * math.pi * j / segments
                x = radius * math.sin(theta) * math.cos(phi)
                y = radius * math.sin(theta) * math.sin(phi)
                z = radius * math.cos(theta)
                vertices.append((x, y, z))

        # Create faces
        for i in range(rings):
            for j in range(segments):
                next_i = i + 1
                next_j = (j + 1) % segments
                faces.append((i * segments + j, next_i * segments + j,
                             next_i * segments + next_j, i * segments + next_j))

        return vertices, faces

    @staticmethod
    def create_sphere(radius: int = 10, segments: int = 32, rings: int = 16) -> bpy.types.Object:
        """Builds a sphere from a given radius, segments, and rings.

        Args:
            radius (int, optional): Radius of the sphere. Defaults to 10.
            segments (int, optional): Horizontal segments of the sphere. Defaults to 32.
            rings (int, optional): Vertical rings of the sphere. Defaults to 16.

        Returns:
            mesh (bpy.types.Mesh): Sphere object.
        """
        vertices, faces = Utils.create_verts_faces_sphere(
            radius, segments, rings)
        mesh_data = bpy.data.meshes.new("sphere_mesh_data")
        mesh_data.from_pydata(vertices, [], faces)
        mesh_data.update()
        obj = bpy.data.objects.new("My_Sphere", mesh_data)
        scene = bpy.context.scene
        scene.collection.objects.link(obj)
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj  # Set object as active
        return obj

    @staticmethod
    def create_half_sphere(radius: int = 10, 
                           segments: int = 32, 
                           rings: int = 16, 
                           name="Half_Sphere",
                           location=(0.0, 0.0, 0.0)) -> bpy.types.Object:
        """Builds a half-sphere from a given radius, segments, rings and name.

        Args:
            radius (int, optional): _description_. Defaults to 10.
            segments (int, optional): _description_. Defaults to 32.
            rings (int, optional): _description_. Defaults to 16.
            name (string, optional): _description_. Defaults to "Half_Sphere".

        Returns:
            bpy.types.Object: Half-sphere object.
        """
        vertices, faces = Utils.create_verts_faces_half_sphere(
            radius, segments, rings)
        mesh_data = bpy.data.meshes.new("sphere_mesh_data")
        mesh_data.from_pydata(vertices, [], faces)
        mesh_data.update()
        obj = bpy.data.objects.new(name, mesh_data)
        scene = bpy.context.scene
        scene.collection.objects.link(obj)
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj  # Set object as active
        obj.location = location
        return obj

    @staticmethod
    def set_dimensions(obj, width, height, length):
        obj.scale = (width, height, length)

    @staticmethod
    def correct_mesh_normals(obj):
        if obj and obj.type == 'MESH':
            # Create a BMesh from the object's mesh data
            bm = bmesh.new()
            bm.from_mesh(obj.data)
            
            # Recalculate normals
            bm.normal_update()
            
            # Update the mesh with the new normals
            # bpy.ops.object.mode_set(mode='OBJECT')
            bm.to_mesh(obj.data)
            # bpy.ops.object.mode_set(mode='EDIT')
            bm.free()
            
            print("Normals have been corrected.")
        else:
            print("Active object is not a mesh.")

    @staticmethod
    def clean_geometry(obj_name):
        # Select the object
        obj = bpy.data.objects[obj_name]
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)

        # Switch to EDIT mode
        bpy.ops.object.mode_set(mode='EDIT')

        # Remove doubles
        bpy.ops.mesh.remove_doubles()

        # Recalculate normals
        bpy.ops.mesh.normals_make_consistent(inside=False)

        # Convert tris to quads
        bpy.ops.mesh.tris_convert_to_quads()

        # Switch back to OBJECT mode
        bpy.ops.object.mode_set(mode='OBJECT')

    @staticmethod
    def add_thickness(obj_name: str, thickness: float):
        """Adds thickness to the object with name 'obj_name'.

        Args:
            obj_name (str): _description_
            thickness (float): _description_
        """
        obj = bpy.data.objects[obj_name]
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)

        solidify_modifier = obj.modifiers.new(name="Solidify", type='SOLIDIFY')
        solidify_modifier.thickness = thickness

        bpy.ops.object.modifier_apply(modifier=solidify_modifier.name)