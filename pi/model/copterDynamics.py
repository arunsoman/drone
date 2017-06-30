import numpy as py
from numpy import cross, eye, dot
from scipy.linalg import expm3, norm

#all methods will return only translation vector

def moveTo(a,b):
    if a.x is b.x and a.y is b.y:
        #perform vertical motion
        return [0,0,b.z - a.z]

    if a.z is b.z:
        #perform horizontal motion
        return [b.x - a.x, b.y - a.y, 0]
    return

def rotate(a, axis, theta):
    return dot(expm3(cross(eye(3), axis/norm(axis)*theta)),a)

def rotateT():
    v, axis, theta = [3, 5, 0], [4, 4, 1], 1.2
    M0 = rotate(v, axis, theta)
    print("rotatation M"); print( M0)
    #print("dotProduct", dot(M0, v))

rotateT()