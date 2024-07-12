import bpy
import numpy
import time
import mathutils

punto1 = [0, 0, 0]
punto2 = [10, 20, 30]


def dist1(p1, p2):
    start_time = time.time()
    _p1 = mathutils.Vector(p1)
    _p2 = mathutils.Vector(p2)
    dif = _p1 - _p2
    distance = dif.length
    print(f"dist1: {distance}")
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"dist1 execution time in seconds: {execution_time:.6f}")


def dist2(p1, p2):
    start_time = time.time()
    _p1 = numpy.array(p1)
    _p2 = numpy.array(p2)
    distance = numpy.linalg.norm(_p1 - _p2)
    print(f"dist2: {distance}")
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"dist2 execution time in seconds: {execution_time:.6f}")


if __name__ == '__main__':
    dist1(punto1, punto2)
    dist2(punto1, punto2)