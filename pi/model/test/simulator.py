import numpy
from pyquaternion import Quaternion

numpy.set_printoptions(suppress=True)

class Rotor(object):
    def rotateX(self, point, degrees):
        return Quaternion(axis=[1,0,0], degrees=degrees).rotate(point)

    def rotateY(self, point, degrees):
        return Quaternion(axis=[0,1,0], degrees=degrees).rotate(point)

    def rotateZ(self, point, degrees):
        return Quaternion(axis=[0,0,1], degrees=degrees).rotate(point)

    def rotateAtAxis(self, axis, point, degrees):
        return Quaternion(axis=axis, degrees=degrees).rotate(point)

r = Rotor()
print r.rotateX(numpy.array([1,0,1]), 180)