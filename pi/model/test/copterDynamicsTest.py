from scipy.linalg import expm3, norm, svd, det
from numpy import *
from math import sqrt, atan2


#all methods will return only translation vector
from model.copterDynamics import rigid_transform_3D


def tt():
    '''
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
    '''
    n = 1
    A=array([[1,0,0]])
    B=array([[0,0,1]])
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
    print ret_R
    print ""

    print "Translation"
    print ret_t
    print ""

    print "RMSE:", rmse
    print "If RMSE is near zero, the function is correct!"



tt()