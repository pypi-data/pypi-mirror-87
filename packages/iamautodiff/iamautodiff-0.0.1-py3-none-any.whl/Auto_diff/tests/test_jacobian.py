import numpy as np
from Auto_diff import FD, Jacobian

def test_function_jacobian():
    x = Jacobian([1, 3, 4])
    fun = np.sin(3*x[0] + 2*x[1] - x[2])
    assert isinstance(fun[0], FD), AssertionError('Not an instance of AD.')
    assert isinstance(fun[0].val, int) or isinstance(fun[0].val, float), AssertionError('Value is not a number.')
    assert isinstance(fun[0].der, int) or isinstance(fun[0].der, float), AssertionError('Derivative is not a number.')
    jacob = FD.get_derivatives(fun)
    values = FD.get_values(fun)
    assert isinstance(jacob[0], np.ndarray), AssertionError("get_derivatives method doesn't return numpy ndarray")
    assert isinstance(values[0], np.ndarray), AssertionError("get_values method doesn't return numpy ndarray")

def test_multiple_functions_jacobian():
    x = Jacobian([1, 3, 4])
    fun = [np.sin(3*x[0] + 2*x[1] - x[2]), x[0]**x[1]-x[2]]
    assert len(fun) == 2, AssertionError("Didn't return correct number of functions.")
    assert len(fun[0]) == 3, AssertionError("Didn't return correct number of variables.")
    assert isinstance(fun[0][0], FD), AssertionError('Not an instance of AD.')
    assert isinstance(fun[0][0].val, int) or isinstance(fun[0][0].val, float), AssertionError('Value is not a number.')
    assert isinstance(fun[0][0].der, int) or isinstance(fun[0][0].der, float), AssertionError('Derivative is not a number.')
    jacob = FD.get_derivatives(fun)
    values = FD.get_values(fun)
    assert jacob.shape == (2,3), AssertionError("Jacobian Matrix doesn't have correct dimensions")
    assert values.shape == (2,3), AssertionError("Values Matrix doesn't have correct dimensions")
    assert isinstance(jacob[0], np.ndarray), AssertionError("get_derivatives method doesn't return numpy ndarray")
    assert isinstance(values[0], np.ndarray), AssertionError("get_values method doesn't return numpy ndarray")

test_function_jacobian()
test_multiple_functions_jacobian()