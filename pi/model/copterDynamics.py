from scipy.linalg import expm3, norm, svd, det
from numpy import *
from math import sqrt

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


def rigid_transform_3D(A, B):
    assert len(A) == len(B)

    N = A.shape[0]; # total points

    centroid_A = mean(A, axis=0)
    centroid_B = mean(B, axis=0)

    # centre the points
    AA = A - tile(centroid_A, (N, 1))
    BB = B - tile(centroid_B, (N, 1))

    # dot is matrix multiplication for array
    H = transpose(AA) * BB

    U, S, Vt = linalg.svd(H)

    R = Vt.T * U.T

    # special reflection case
    if linalg.det(R) < 0:
       print "Reflection detected"
       Vt[2,:] *= -1
       R = Vt.T * U.T

    t = -R*centroid_A.T + centroid_B.T

    print t
    rotationMatrixToEulerAngles(R)
    return R, t

def tt():
    # Random rotation and translation
    R = mat(random.rand(3, 3))
    t = mat(random.rand(3, 1))

    # make R a proper rotation matrix, force orthonormal
    U, S, Vt = linalg.svd(R)
    R = U * Vt

    # remove reflection
    if linalg.det(R) < 0:
        Vt[2, :] *= -1
        R = U * Vt

    # number of points
    n = 1

    A = mat(random.rand(n, 3))
    B = R * A.T + tile(t, (1, n))
    B = B.T

    # recover the transformation
    ret_R, ret_t = rigid_transform_3D(A, B)

    A2 = (ret_R * A.T) + tile(ret_t, (1, n))
    A2 = A2.T

    # Find the error
    err = A2 - B

    err = multiply(err, err)
    err = sum(err)
    rmse = sqrt(err / n);

    print "Points A"
    print A
    print ""

    print "Points B"
    print B
    print ""

    print "Rotation"
    print R
    print ""

    print "Translation"
    print t
    print ""

    print "RMSE:", rmse
    print "If RMSE is near zero, the function is correct!"


# Calculates rotation matrix to euler angles
# The result is the same as MATLAB except the order
# of the euler angles ( x and z are swapped ).
def rotationMatrixToEulerAngles(R):

    sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])

    singular = sy < 1e-6

    if not singular:
        x = math.atan2(R[2, 1], R[2, 2])
        y = math.atan2(-R[2, 0], sy)
        z = math.atan2(R[1, 0], R[0, 0])
    else:
        x = math.atan2(-R[1, 2], R[1, 1])
        y = math.atan2(-R[2, 0], sy)
        z = 0
    print("x,y,z");print(x,y,z)
    return array([x, y, z])

def rotateT():
    v, axis, theta = [3, 5, 0], [4, 4, 1], 1.2
    M0 = rotate(v, axis, theta)
    print("rotatation M"); print( M0)
    #print("dotProduct", dot(M0, v))

tt()