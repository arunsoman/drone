from matplotlib.pyplot import plot
from pyquaternion import Quaternion
import numpy
numpy.set_printoptions(suppress=True) # Suppress insignificant values for clarity
v = numpy.array([0., 0., 1.]) # Unit vector in the +z direction
q0 = Quaternion(axis=[1, 1, 1], angle=0.0) # Rotate 0 about x=y=z
q1 = Quaternion(axis=[1, 1, 1], angle=2 * 3.14159265 / 3) # Rotate 120 about x=y=z

print(q0.vector)
print(q1.vector)
for q in Quaternion.intermediates(q0, q1, 8, include_endpoints=True):
    v_prime = q.rotate(v)
    print(v_prime)

class Earth(object):
    def __init__(self):
        self.g = 9.8
        self.liftConstant = 1
        self.airDensity
        self.currentAirVelocity
