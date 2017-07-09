import model.copterDynamics as cd
import unittest
import numpy as np
from math import sqrt, atan2
from scipy.linalg import expm3, norm, svd, det

class testcopterDynamics(unittest.TestCase):
    def test_Transformation(self):
        n = 1
        A = np.array([[1, 0, 0]])
        B = np.array([[0, 0, 1]])
        # recover the transformation
        R, t = cd.get_transformation(A, B)
        print (R, t)

    def tt(self):
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
        A = np.array([[1, 0, 0]])
        B = np.array([[0, 0, 1]])
        # recover the transformation
        ret_R, ret_t = cd.get_transformation(A, B)

        A2 = (ret_R * A.T) + tile(ret_t, (1, n))
        A2 = A2.T

        # Find the error
        err = A2 - B

        err = multiply(err, err)
        err = sum(err)
        rmse = sqrt(err / n)

        print("Points A", A)

        print("Points B", B)

        print ("Rotation", ret_R)

        print ("Translation", ret_t)

        print ("RMSE:", rmse)
        print ("If RMSE is near zero, the function is correct!")
