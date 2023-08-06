import numpy as np


class RD:
    def __init__(self, val):
        self.val = val
        self.grad = 1
        self.children = []

    def __mul__(self, other):
        try:
            val_mul = self.val * other.val
            new_RD = RD(val_mul)
            self.children.append((other.val, new_RD))
            self.grad = None
            other.children.append((self.val, new_RD))
            other.grad = None
        except AttributeError:
            val_mul = self.val * other
            new_RD = RD(val_mul)
            self.children.append((other, new_RD))
            self.grad = None
        return new_RD

    def __add__(self, other):
        try:
            val_add = self.val + other.val
            new_RD = RD(val_add)
            self.children.append((1, new_RD))
            self.grad = None
            other.children.append((1, new_RD))
            other.grad = None
        except AttributeError:
            val_add = self.val + other
            new_RD = RD(val_add)
            self.children.append((1, new_RD))
            self.grad = None
        return new_RD

    def get_gradient(self):
        if self.grad is None:
            grad = 0
            for der, child in self.children:
                grad += der * child.get_gradient()
            self.grad = grad
        return self.grad

    def get_value(self):
        return self.val

    # subtraction
    def __sub__(self, other):
        try:
            val_sub = self.val - other.val
            new_RD = RD(val_sub)
            self.children.append((1, new_RD))
            self.grad = None
            other.children.append((-1, new_RD))
            other.grad = None
        except AttributeError:
            val_sub = self.val - other
            new_RD = RD(val_sub)
            self.children.append((1, new_RD))
            self.grad = None

        return new_RD

    # division
    def __truediv__(self, other):
        try:
            val_div = self.val / other.val
            new_RD = RD(val_div)
            self.children.append(( 1 / other.val, new_RD))
            self.grad = None
            other.children.append(( - self.val / (other.val ** 2) , new_RD))  # need confirmation
            other.grad = None
        except AttributeError:
            val_div = self.val / other
            new_RD = RD(val_div)
            self.children.append(( 1 / other, new_RD))
            self.grad = None

        return new_RD

    # exponential  # need to change to handle all bases
    def __pow__(self, other):
        try:
            if self.val > 0:
                val_div = self.val ** other.val
                # der_div = other.val * self.val**(other.val-1) * self.der + np.log(self.val) * self.val**other.val * other.der
                new_RD = RD(val_div)
                self.children.append((other.val*self.val**(other.val-1), new_RD))
                self.grad = None
                other.children.append(( np.log(self.val) * self.val**other.val , new_RD))
                other.grad = None
            else:
                raise ValueError("Derivative of this power function is a complex number. Sadly our package won't handle complex numbers.")
        except AttributeError:
            val_div = self.val ** other
            new_RD = RD(val_div)
            self.children.append((other*self.val**(other-1), new_RD))
            self.grad = None
        
        return new_RD


    # reverse exponential
    def __rpow__(self, other):
        val_div = other ** self.val
        new_RD = RD(val_div)
        der_div = np.log(other) * (other**self.val)
        self.children.append((der_div, new_RD))
        self.grad = None
        return new_RD
    
    # reverse addition
    def __radd__(self, other):
        return self.__add__(other)

    # reverse multiplication
    def __rmul__(self, other):
        return self.__mul__(other)

    # reverse subtraction
    def __rsub__(self,other):
        val_sub = other - self.val
        new_RD = RD(val_sub)
        self.children.append((-1, new_RD))
        self.grad = None

        return new_RD

    # reverse division
    def __rtruediv__(self, other):
        val_div = other / self.val
        new_RD = RD(val_div)
        self.children.append((-other/self.val**2, new_RD))
        self.grad = None

        return new_RD

    # sine
    def sin(self):
        new_RD = RD(np.sin(self.val))
        self.children.append((np.cos(self.val), new_RD))
        self.grad = None
        return new_RD

    # cosine
    def cos(self):
        val = np.cos(self.val)
        new_RD = RD(val)
        self.children.append((-np.sin(self.val), new_RD))
        self.grad = None
        return new_RD

    # tangent
    def tan(self):
        val = np.tan(self.val)
        new_RD = RD(val)
        self.children.append(( 1/(np.cos(self.val)**2), new_RD)) 
        self.grad = None
        return new_RD

        # arcsine
    def arcsin(self):
        if abs(self.val) >= 1:
            raise ValueError('Arcsin cannot be evaluated at {}.'.format(self.val))
        val = np.arcsin(self.val)
        new_RD = RD(val)
        self.children.append(( 1/np.sqrt(1 - self.val**2), new_RD)) 
        self.grad = None
        return new_RD
    
    # arccosine
    def arccos(self):
        if abs(self.val) >= 1:
            raise ValueError('Arccos cannot be evaluated at {}.'.format(self.val))
        val = np.arccos(self.val)
        new_RD = RD(val)
        self.children.append(( -1/np.sqrt(1 - self.val**2), new_RD)) 
        self.grad = None
        return new_RD
    
    # arctangent
    def arctan(self):
        val = np.arctan(self.val)
        new_RD = RD(val)
        self.children.append((1/(1 + self.val**2), new_RD)) 
        self.grad = None
        return new_RD
        
    # hyperbolic sine
    def sinh(self):
        val = np.sinh(self.val)
        new_RD = RD(val)
        self.children.append((np.cosh(self.val), new_RD))
        self.grad = None
        return new_RD

    # hyperbolic cosine
    def cosh(self):
        val = np.cosh(self.val)
        new_RD = RD(val)
        self.children.append((np.sinh(self.val), new_RD))
        self.grad = None
        return new_RD

    # hyperbolic tangent
    def tanh(self):
        val = np.tanh(self.val)
        new_RD = RD(val)
        self.children.append(( 1/np.cosh(self.val)**2, new_RD))  
        self.grad = None
        return new_RD
    
    # square root
    def sqrt(self):
        val = np.sqrt(self.val)
        new_RD = RD(val)
        self.children.append(( 0.5*self.val**(-0.5), new_RD))  
        self.grad = None
        return new_RD

    # exponential
    def exp(self):
        val = np.exp(self.val)
        new_RD = RD(val)
        self.children.append((np.exp(self.val), new_RD))
        self.grad = None
        return new_RD

    def __neg__(self):
        val = -1 * self.val
        new_RD = RD(val)
        self.children.append((-1, new_RD))
        self.grad = None
        return new_RD
    
    # equal
    def __eq__(self, other):
        try:
            if self.val == other.val and self.get_gradient() == other.get_gradient():
                return True
            else:
                return False
        except:
            return False
        
    # not equal
    def __ne__(self, other):
        try:
            if self.val != other.val or self.get_gradient() != other.get_gradient():
                return True
            else:
                return False
        except:
            return True
    
    # Define the generic log function that the user will use
    def logarithm(self, base):
        val = np.log(self.val)/np.log(base)
        new_RD = RD(val)
        self.children.append((1/(self.val * np.log(base)), new_RD))
        self.grad = None
        return new_RD

    # Define the logistic function that the user will use
    def logistic(self):
        val = 1/(1 + np.exp(1)**(-self.val))
        new_RD = RD(val)
        self.children.append(((np.exp(1)**(self.val))/(1 + np.exp(1)**(self.val)), new_RD))
        self.grad = None
        return new_RD

    def __repr__(self):
        return 'RD({})'.format(self.val)

    def __str__(self):
        return 'RD({})'.format(self.val)
