from Auto_diff import FD
import numpy as np
 
def test_basic_addition_v():
    x = FD(3, 1)
    y = FD(2, 0)
    derivative = x + y
    assert (float(derivative.get_value()) == 5.0) & (float(derivative.get_derivative()) == 1.0), Exception(f'test_basic_addition_c() has error.')
    
def test_basic_addition_c():
    x = FD(3, 1)
    derivative = x + 2
    assert (float(derivative.val) == 5.0) & (float(derivative.der) == 1.0), Exception(f'test_basic_addition_c() has error.')

def test_basic_subtraction_v():
    x = FD(3, 1)
    y = FD(2, 0)
    derivative = x - y
    assert ((float(derivative.val)) == 1.0) & (float(derivative.der) == 1.0), Exception(f'test_basic_subtraction_v() has error.')

def test_basic_subtraction_c():
    x = FD(3, 1)
    derivative = x - 2
    assert ((float(derivative.val)) == 1.0) & (float(derivative.der) == 1.0), Exception(f'test_basic_subtraction_c() has error.')

def test_basic_multiplication_v():
    x = FD(3, 1)
    y = FD(2, 0)
    derivative = x * y
    assert ((float(derivative.val) == 6.0) & (float(derivative.der) == 2.0)), Exception(f'test_basic_multiplication_v() has error.')

def test_basic_multiplication_c():
    x = FD(3, 1)
    derivative = x * 2
    assert ((float(derivative.val) == 6.0)  & (float(derivative.der) == 2.0)), Exception(f'test_basic_multiplication_c() has error.')

def test_basic_div_v():
    x = FD(3, 1)
    y = FD(2, 0)
    derivative = x / y
    assert ((float(derivative.val) == 1.50)  & (float(derivative.der) == 0.5)), Exception(f'test_basic_div_v() has error.')

def test_basic_div_c():
    x = FD(3, 1)
    derivative = x / 2
    assert ((float(derivative.val) == 1.50) & (float(derivative.der) == 0.5)), Exception(f'test_basic_div_c() has error.')

def test_basic_power_v():
    x = FD(3, 1)
    y = FD(2, 0)
    derivative = x ** y
    assert ((float(derivative.val) == 9.0) & (float(derivative.der) == 6.0)), Exception(f'test_basic_power_v() has error.')

def test_basic_power_c1():
    x = FD(3, 1)
    derivative = x ** 2
    assert ((float(derivative.val) == 9.0) & (float(derivative.der) == 6.0)), Exception(f'test_basic_power_c() has error.')

def test_basic_power_c2():
    x = FD(-1, 1)
    derivative = x ** 2
    assert ((float(derivative.val) == 1) & (float(derivative.der) == -2)), Exception(f'test_basic_power_c() has error.')

def test_basic_exponential_v():
    x = FD(3, 1)
    derivative = np.exp(x)
    assert ((float(derivative.val) == np.exp(3)) & (float(derivative.der) == np.exp(3))), Exception(f'test_basic_exponential_v() has error.')

def test_basic_radd_v():
    x = FD(3, 1)
    y = FD(2, 0)
    derivative = y + x
    assert ((float(derivative.val) == 5.0) & (float(derivative.der) == 1.0)), Exception(f'test_basic_radd_v() has error.')

def test_basic_radd_c():
    x = FD(3, 1)
    derivative = 2 + x
    assert ((float(derivative.val)) == 5.0)  & (float(derivative.der) == 1.0), Exception(f'test_basic_radd_c() has error.')

def test_basic_rmul_v():
    x = FD(3, 1)
    y = FD(2, 0)
    derivative = y * x
    assert ((float(derivative.val) == 6.0) & (float(derivative.der) == 2.0)), Exception(f'test_basic_rmul_v() has error.')

def test_basic_rmul_c():
    x = FD(3, 1)
    derivative = 2 * x
    assert ((float(derivative.val) == 6.0) & (float(derivative.der) == 2.0)), Exception(f'test_basic_rmul_c() has error.')

def test_basic_rsub_v():
    x = FD(3, 1)
    y = FD(2, 0)
    derivative = y-x
    assert ((float(derivative.val) == -1.0) & (float(derivative.der) == -1.0)), Exception(f'test_basic_rsub_v() has error.')

def test_basic_rsub_c():
    x = FD(3, 1)
    derivative = 2-x
    assert (float(derivative.val) == -1.0) & (float(derivative.der) == -1.0), Exception(f'test_basic_rsub_c() has error.')

def test_basic_rdiv_c(): # Account for when the divisor is 0
    x = FD(3, 1)
    derivative = 2/x
    assert (float(derivative.val) == (2/3)) & (float(derivative.der) == -(2/9)), Exception(f'test_basic_rdiv_c() has error.')

def test_basic_rpow_c():
    x = FD(3, 1)
    derivative = 2 ** x
    assert (float(derivative.val) == 8.0) & (float(derivative.der) == 8*np.log(2)), Exception(f'test_basic_rpow_c() has error.')

def test_basic_neg_v(): 
    x = FD(3, 1)
    derivative = -x
    assert (float(derivative.val) == -3.0) & (float(derivative.der) == -1.0), Exception(f'test_basic_neg_v() has error.')

def test_basic_sin_v(): 
    x = FD(3, 1)
    derivative = FD.sin(x)
    assert (float(derivative.val) == np.sin(3)) & (float(derivative.der) == np.cos(3)), Exception(f'test_basic_sin_v() has error.')

def test_basic_cos_v(): 
    x = FD(3, 1)
    derivative = FD.cos(x)
    assert (float(derivative.val) == np.cos(3)) & (float(derivative.der) == -np.sin(3)), Exception(f'test_basic_cos_v() has error.')

def test_basic_tan_v():
    x = FD(3, 1)
    derivative = FD.tan(x)
    assert (float(derivative.val) == np.tan(3)) & (float(derivative.der) == 1/(np.cos(3))**2), Exception(f'test_basic_tan_v() has error.')

def test_basic_arcsin_v():
    x = FD(0.5,1)
    derivative = FD.arcsin(x)
    assert (float(derivative.val) == np.arcsin(0.5)) & (float(derivative.der) == 1/np.sqrt(1-0.5**2)), Exception(f'test_basic_arcsin_v() has error.')

def test_basic_arccos_v():
    x = FD(0.5,1)
    derivative = FD.arccos(x)
    assert (float(derivative.val) == np.arccos(0.5)) & (float(derivative.der) == -1/np.sqrt(1 - 0.5**2)), Exception(f'test_basic_arccos_v() has error.')

def test_basic_arctan_v():
    x = FD(3, 1)
    derivative = FD.arctan(x)
    assert (float(derivative.val) == np.arctan(3)) & (float(derivative.der) == 1/(1 + 3**2)), Exception(f'test_basic_arctan_v() has error.')

def test_basic_sinh_v():
    x = FD(3, 1)
    derivative = FD.sinh(x)
    assert (float(derivative.val) == np.sinh(3)) & (float(derivative.der) == np.cosh(3)), Exception(f'test_basic_sinh_v() has error.')

def test_basic_cosh_v():
    x = FD(3, 1)
    derivative = FD.cosh(x)
    assert (float(derivative.val) == np.cosh(3)) & (float(derivative.der) == np.sinh(3)), Exception(f'test_basic_cosh_v() has error.')

def test_basic_tanh_v():
    x = FD(3, 1)
    derivative = FD.tanh(x)
    assert (float(derivative.val) == np.tanh(3)) & (float(derivative.der) == 1/np.cosh(3)**2), Exception(f'test_basic_tanh_v() has error.')

def test_basic_sqrt_v():
    x = FD(3, 1)
    derivative = FD.sqrt(x)
    assert (float(derivative.val) == np.sqrt(3)) & (float(derivative.der) == 0.5*3**(-0.5)), Exception(f'test_basic_sqrt_v() has error.')

def test_basic_eq_v():
    x = FD(3, 1)
    v = FD(3,1)
    assert x == v, Exception(f'test_basic_eq_v() has error.')

def test_basic_ne_v():
    x = FD(3, 1)
    y = FD(2, 0)
    assert x != y, Exception(f'test_basic_ne_v() has error.')

def test_basic_logarithm_v():
    x = FD(3, 1)
    derivative = FD.logarithm(x, np.e)
    assert (float(derivative.val) == np.log(3)) & (float(derivative.der) == 1/3), Exception(f'test_basic_logarithm_v() has error.')

def test_basic_logistic_v():
    x = FD(3, 1)
    derivative = FD.logistic(x)
    assert (float(derivative.val) == 1/(1 + np.e**(-3))) & (float(derivative.der) == (np.e**(3))/(1 + np.e**(3))**2), Exception(f'test_basic_logistic_v() has error.')
    # Define the logistic function that the user will use

def test_basic_repr():
    x = FD(3, 1)
    assert repr(x) == 'FD(3, 1)'

def test_basic_str():
    x = FD(3, 1)
    assert str(x) == 'FD(3, 1)'
