from Auto_diff import RD
import numpy as np


def test_basic_addition_v():
    x = RD(3)
    y = RD(2)
    derivative = x + y
    assert (float(derivative.get_value()) == 5.0) & (float(x.get_gradient()) == 1.0) & (float(y.get_gradient()) == 1.0), Exception(f'test_basic_addition_c() has error.')

def test_basic_addition_c():
    x = RD(3)
    derivative = x + 2
    assert (float(derivative.val) == 5.0) & (float(x.get_gradient()) == 1.0), Exception(f'test_basic_addition_c() has error.')

def test_basic_subtraction_v():
    x = RD(3)
    y = RD(2)
    derivative = x - y
    assert ((float(derivative.get_value())) == 1.0) & (float(x.get_gradient()) == 1.0) & (float(y.get_gradient()) == -1.0), Exception(f'test_basic_subtraction_v() has error.')

def test_basic_subtraction_c():
    x = RD(3)
    derivative = x - 2
    assert ((float(derivative.get_value())) == 1.0) & (float(x.get_gradient()) == 1.0), Exception(f'test_basic_subtraction_c() has error.')

def test_basic_multiplication_v():
    x = RD(3)
    y = RD(2)
    derivative = x * y
    assert (float(derivative.val) == 6.0) & (float(x.get_gradient()) == 2.0) & (float(y.get_gradient()) == 3.0), Exception(f'test_basic_multiplication_v() has error.')

def test_basic_multiplication_c():
    x = RD(3)
    derivative = x * 2
    assert (float(derivative.val) == 6.0)  & (float(x.get_gradient()) == 2.0), Exception(f'test_basic_multiplication_c() has error.')

def test_basic_div_v():
    x = RD(3)
    y = RD(2)
    derivative = x / y
    assert (float(derivative.val) == 1.50)  & (float(x.get_gradient()) == 0.5) & (float(y.get_gradient()) == -0.75), Exception(f'test_basic_div_v() has error.')

def test_basic_div_c():
    x = RD(3)
    derivative = x / 2
    assert (float(derivative.get_value()) == 1.50) & (float(x.get_gradient()) == 0.5), Exception(f'test_basic_div_c() has error.')

def test_basic_power_v():
    x = RD(3)
    y = RD(2)
    derivative = x ** y
    assert (float(derivative.get_value()) == 9.0) & (float(x.get_gradient()) == 6) & (float(y.get_gradient()) == np.log(3)*9), Exception(f'test_basic_power_v() has error.')

def test_basic_power_c():
    x = RD(3)
    derivative = x ** 2
    assert (float(derivative.get_value()) == 9.0) & (float(x.get_gradient()) == 6), Exception(f'test_basic_power_c() has error.')

def test_basic_exponential_v():
    x = RD(3)
    derivative = np.exp(x)
    assert ((float(derivative.val) == np.exp(3)) & (float(x.get_gradient()) == np.exp(3))), Exception(f'test_basic_exponential_v() has error.')

def test_basic_radd_c():
    x = RD(3)
    derivative = 2 + x
    assert ((float(derivative.val)) == 5.0)  & (float(x.get_gradient()) == 1.0), Exception(f'test_basic_radd_c() has error.')

def test_basic_rmul_c():
    x = RD(3)
    derivative = 2 * x
    assert ((float(derivative.val) == 6.0) & (float(x.get_gradient()) == 2.0)), Exception(f'test_basic_rmul_c() has error.')

def test_basic_rsub_c():
    x = RD(3)
    derivative = 2-x
    assert (float(derivative.val) == -1.0) & (float(x.get_gradient()) == -1.0), Exception(f'test_basic_rsub_c() has error.')

def test_basic_rdiv_c(): # Account for when the divisor is 0
    x = RD(3)
    derivative = 2/x
    assert (float(derivative.val) == (2/3)) & (float(x.get_gradient()) == -(2/9)), Exception(f'test_basic_rdiv_c() has error.')

def test_basic_rpow_c(): 
    x = RD(3)
    derivative = 2 ** x
    assert (float(derivative.get_value()) == 8.0) & (float(x.get_gradient()) == 8*np.log(2)), Exception(f'test_basic_rpow_c() has error.')

def test_basic_neg_v(): 
    x = RD(3)
    derivative = -x
    assert (float(derivative.get_value()) == -3.0) & (float(x.get_gradient()) == -1.0), Exception(f'test_basic_neg_v() has error.')

def test_basic_sin_v():
    x = RD(3) 
    derivative = np.sin(x)
    assert (float(derivative.val) == np.sin(3)) & (float(x.get_gradient()) == np.cos(3)), Exception(f'test_basic_sin_v() has error.')

def test_basic_cos_v(): 
    x = RD(3) 
    derivative = np.cos(x)
    assert (float(derivative.val) == np.cos(3)) & (float(x.get_gradient()) == -np.sin(3)), Exception(f'test_basic_cos_v() has error.')

def test_basic_tan_v():
    x = RD(3) 
    derivative = np.tan(x)
    assert (float(derivative.val) == np.tan(3)) & (float(x.get_gradient()) == 1/(np.cos(3))**2), Exception(f'test_basic_tan_v() has error.')

def test_basic_arcsin_v():
    x = RD(0.5) 
    derivative = np.arcsin(x)
    assert (float(derivative.val) == np.arcsin(0.5)) & (float(x.get_gradient()) == 1/np.sqrt(1-0.25)), Exception(f'test_basic_arcsin_v() has error.')

def test_basic_arccos_v(): 
    x = RD(0.5) 
    derivative = np.arccos(x)
    assert (float(derivative.val) == np.arccos(0.5)) & (float(x.get_gradient()) == -1/np.sqrt(1-0.25)), Exception(f'test_basic_arccos_v() has error.')

def test_basic_arctan_v():
    x = RD(3) 
    derivative = np.arctan(x)
    assert (float(derivative.val) == np.arctan(3)) & (float(x.get_gradient()) == 1/(1+9)), Exception(f'test_basic_arctan_v() has error.')

def test_basic_sinh_v():
    x = RD(3) 
    derivative = np.sinh(x)
    assert (float(derivative.val) == np.sinh(3)) & (float(x.get_gradient()) == np.cosh(3)), Exception(f'test_basic_sinh_v() has error.')

def test_basic_cosh_v(): 
    x = RD(3) 
    derivative = np.cosh(x)
    assert (float(derivative.val) == np.cosh(3)) & (float(x.get_gradient()) == np.sinh(3)), Exception(f'test_basic_cosh_v() has error.')

def test_basic_tanh_v():
    x = RD(3) 
    derivative = np.tanh(x)
    assert (float(derivative.val) == np.tanh(3)) & (float(x.get_gradient()) == 1/(np.cosh(3)**2)), Exception(f'test_basic_tanh_v() has error.')

def test_basic_sqrt_v():
    x = RD(3) 
    derivative = np.sqrt(x)
    assert (float(derivative.val) == np.sqrt(3)) & (float(x.get_gradient()) == 0.5*3**(-0.5)), Exception(f'test_basic_sqrt_v() has error.')

def test_basic_log_v():
    x = RD(3) 
    derivative = RD.logarithm(x, 10)
    assert (float(derivative.val) == np.log10(3)) & (float(x.get_gradient()) == 1/(np.log(10)*3)), Exception(f'test_basic_log_v() has error.')

def test_basic_logistic_v():
    x = RD(3) 
    derivative = RD.logistic(x)
    assert (float(derivative.val) == 1/(1 + np.e**(-3))) & (float(x.get_gradient()) == (np.e**(3))/(1 + np.e**3)), Exception(f'test_basic_logistic_v() has error.')

def test_basic_eq_v():
    x = RD.logistic(RD(3))
    v = RD.logistic(RD(3))
    assert x==v, Exception(f'test_basic_eq_v() has error.')

def test_basic_ne_v():
    x = RD.logistic(RD(3))
    v = RD.logarithm(RD.logistic(RD(3)), np.e)
    assert x!=v, Exception(f'test_basic_ne_v() has error.')

def test_basic_repr():
    x = RD(3)
    assert repr(x) == 'RD(3)'

def test_basic_str():
    x = RD(3)
    assert str(x) == 'RD(3)'
