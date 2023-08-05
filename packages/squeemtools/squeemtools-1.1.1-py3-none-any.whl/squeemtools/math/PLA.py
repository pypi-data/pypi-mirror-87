import numpy as np #arrays as vectors, dot product

#quick fn to check sign of input and classify it based on output
def sign(input):
    '''Gets the sign of the input'''
    if input > 0: return 1
    elif input == 0: return 0
    else: return -1

#PLA function
def PLA(input_list):
    '''Does Perceptron Learning Algorithm  to segment data (input_list) on the hyper plane'''
    size = len(input_list[0])-1
    weights_ = np.zeros(shape=size)
    converge_ = False
    t_ = 0
    iter_ = 0
    wu_ = 0

    while not converge_:
        if sign(input_list[t_][:size].dot(weights_)) != input_list[t_][size]:
            weights_ += input_list[t_][size] * input_list[t_][:size]
            t_ = 0
            wu_ += 1
        else:
            t_ += 1
        if t_ == len(input_list):
            converge_ = True
            print("PLA converged, here are the weights:", weights_)
        iter_ += 1
    print("\nIterations: ",iter_,"Weight Changes: ",wu_)
