import numpy as np
def Augment(X):
    '''Takes in n-dimensional X and returns n+1-dimensional (augmented) X'''
    try:
        return np.concatenate((np.ones((X.shape[0], 1)), X), axis=1)
    except:
        return np.hstack(([1],X))

def UndoAugment(X):
    '''Takes in n-dimensional X and returns n-1-dimensional (de-augmented) X'''
    if len(X.shape) == 1:
        return X[1:]
    else:
        return np.delete(X,0,1)
