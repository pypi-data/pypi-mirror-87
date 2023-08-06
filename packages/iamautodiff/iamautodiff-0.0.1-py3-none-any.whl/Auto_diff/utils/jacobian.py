#!/usr/bin/env python3
import numpy as np
from Auto_diff import FD

# Define a function that produces output that can be used in order to find the Jacobian
def Jacobian(arr):
    # initialize with input value
    num_var = len(arr)
    output = [[] for x in range(num_var)]
    for i in range(num_var):
        for j in range(num_var):
            if i == j:
                output[i].append(FD(arr[i], 1))
            else:
                output[i].append(FD(arr[i], 0))
    return np.array(output)