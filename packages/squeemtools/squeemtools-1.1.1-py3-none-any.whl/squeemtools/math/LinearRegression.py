import numpy as np
from Helpers import Augment

def LinearRegression(X,Y,verbose=False):
    '''X is the input, Y is the output'''
    # Homogeneous coordinates
    newX = Augment(X)

    # Compute matrices and calculate the weights
    xt_x = newX.T @ newX             # X transpose * X
    xt_y = newX.T @ Y                # X transpose * Y
    A = np.linalg.inv(xt_x) @ newX.T # Matrix A which is (X transpose)^-1 * X transpose
    w = np.linalg.inv(xt_x) @ xt_y   # w = (X transpose * X)^-1 * (X transpose * Y)
    if verbose:
        return w, newX, xt_x, xt_y
    else:
        return w
