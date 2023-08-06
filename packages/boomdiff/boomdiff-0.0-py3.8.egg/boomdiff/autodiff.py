import numpy as np

class AD():

    def __init__(self, eval_pt, der_dict={'x1':1}):
        """Initializes class structure

        Parameters
        ----------
        eval_pt : float
            Value of the current function/variable
        der_dict : dict
            derivative value dictionary of all variables

        Returns
        -------
        None.

        Examples
        --------
        >>> x1 = AD(3.6, {'x1':1})
        >>> x1.func_val
        3.6
        >>> x1.partial_dict
        {'x1': 1}
        """

        # Set function string
        self.func_string = ''
        self.func_val = eval_pt

        # Set partial derivative dictionary
        # Will assume form of x_1, ..., x_n
        self.partial_dict = der_dict

    def set_params(self, params):
        pass # TODO

    def __add__(self, other):
        """Overload addition operation '+'

        Parameters
        ----------
        other : AD class instance or float
            Elements to be added from self. Can be a AD class instance, which
            will update function value and partial derivative dictionary; Or a con-
            -stant, which will only update function value.

        Returns
        -------
        A new AD class instance with updated information

        Examples
        --------
        >>> x1 = AD(3.6, {'x1': 1})
        >>> print(x1.func_val, x1.partial_dict)
        3.6 {'x1': 1}
        >>> f1 = x1 + 10
        >>> print(f1.func_val, f1.partial_dict)
        13.6 {'x1': 1}
        >>> x2 = AD(2.0, {'x1': 3.4})
        >>> f2 = x1 + x2
        >>> print(f2.func_val, f2.partial_dict)
        5.6 {'x1': 4.4}
        """

        try:
            # First try as other is an AD class instance
            # Give the variable list for self object
            self_var_keys = list(self.partial_dict.keys())
            # Give the variable list for other object
            other_var_keys = list(other.partial_dict.keys())
            # At this moment, we assume all have one variable, need to be fixed, TODO
            new_der_dict = {self_var_keys[0]: self.partial_dict[self_var_keys[0]] + other.partial_dict[self_var_keys[0]]}
            return AD(self.func_val+other.func_val, new_der_dict)
        except AttributeError:
            # If other is not an AD class instance, treat as a constant
            return AD(self.func_val+other, self.partial_dict)

    def __radd__(self, other):
        """Overload to make sure commutativity of addition '+'

        Parameters
        ----------
        other : AD class instance or float
            Elements to be subtracted on the left, from self. Can be a AD class instance, which
            will update function value and partial derivative dictionary; Or a con-
            -stant, which will only update function value.

        Returns
        -------
        A new AD class instance with updated information

        Examples
        --------
        >>> x1 = AD(3.6, {'x1': 1})
        >>> f1 = 10 + x1
        >>> print(f1.func_val, f1.partial_dict)
        13.6 {'x1': 1}
        """
        if isinstance(other, AD):
            # First try as other is an AD class instance
            return other.__add__(self)
        else:
            # If other is not an AD class instance, treat as a constant
            self_var_keys = list(self.partial_dict.keys())
            # At this moment, we assume all have one variable, need to be fixed, TODO
            new_der_dict = {self_var_keys[0]: self.partial_dict[self_var_keys[0]]}
            return AD(other+self.func_val, new_der_dict)


    def __sub__(self, other):
        """Overload subtraction operation '-'

        Parameters
        ----------
        other : AD class instance or float
            Elements to be subtracted from self. Can be a AD class instance, which
            will update function value and partial derivative dictionary; Or a con-
            -stant, which will only update function value.

        Returns
        -------
        A new AD class instance with updated information

        Examples
        --------
        >>> x1 = AD(3.6, {'x1': 1})
        >>> print(x1.func_val, x1.partial_dict)
        3.6 {'x1': 1}
        >>> f1 = x1 - 10
        >>> print(f1.func_val, f1.partial_dict)
        -6.4 {'x1': 1}
        >>> x2 = AD(2.0, {'x1': 3.4})
        >>> f2 = x1 - x2
        >>> print(f2.func_val, f2.partial_dict)
        1.6 {'x1': -2.4}
        """
        try:
            # First try as other is an AD class instance
            # Give the variable list for self object
            self_var_keys = list(self.partial_dict.keys())
            # Give the variable list for other object
            other_var_keys = list(other.partial_dict.keys())
            # At this moment, we assume all have one variable, need to be fixed, TODO
            new_der_dict = {self_var_keys[0]: self.partial_dict[self_var_keys[0]] - other.partial_dict[self_var_keys[0]]}
            return AD(self.func_val-other.func_val, new_der_dict)
        except AttributeError:
            # If other is not an AD class instance, treat as a constant
            return AD(self.func_val-other, self.partial_dict)

    def __rsub__(self, other):
        """Overload to make sure commutativity of subtraction '-'

        Parameters
        ----------
        other : AD class instance or float
            Elements to be subtracted on the left, from self. Can be a AD class instance, which
            will update function value and partial derivative dictionary; Or a con-
            -stant, which will only update function value.

        Returns
        -------
        A new AD class instance with updated information

        Examples
        --------
        >>> x1 = AD(3.6, {'x1': 1})
        >>> f1 = 10 - x1
        >>> print(f1.func_val, f1.partial_dict)
        6.4 {'x1': -1}
        """
        if isinstance(other, AD):
            # First try as other is an AD class instance
            return other.__sub__(self)
        else:
            # If other is not an AD class instance, treat as a constant
            self_var_keys = list(self.partial_dict.keys())
            # At this moment, we assume all have one variable, need to be fixed, TODO
            new_der_dict = {self_var_keys[0]: -self.partial_dict[self_var_keys[0]]}
            return AD(other-self.func_val, new_der_dict)

    def __mul__(self, other):
        """Overload multiplication operation '*'

        Parameters
        ----------
        other : AD class instance or float
            Elements to be multiplied to self. Can be a AD class instance, which
            will update function value and partial derivative dictionary; Or a con-
            -stant, which will only update function value.

        Returns
        -------
        A new AD class instance with updated information

        Examples
        --------
        >>> x1 = AD(1, {'x1': 1})
        >>> f1 = x1*10.0
        >>> print(f1.func_val, f1.partial_dict)
        10.0 {'x1': 10.0}
        >>> x2 = x1*3.4 - 1.4
        >>> print(x2.func_val, x2.partial_dict)
        2.0 {'x1': 3.4}
        >>> f2 = f1 * x2
        >>> print(f2.func_val, f2.partial_dict)
        20.0 {'x1': 54.0}
        """
        try:
            # First try as other is an AD class instance
            # Give the variable list for self object
            self_var_keys = list(self.partial_dict.keys())
            # Give the variable list for other object
            other_var_keys = list(other.partial_dict.keys())
            # At this moment, we assume all have one variable, need to be fixed, TODO
            new_der_dict = {self_var_keys[0]: self.partial_dict[self_var_keys[0]]*other.func_val + self.func_val*other.partial_dict[self_var_keys[0]]}
            return AD(self.func_val*other.func_val, new_der_dict)
        except AttributeError:
            # If other is not an AD class instance, treat as a constant
            self_var_keys = list(self.partial_dict.keys())
            # At this moment, we assume all have one variable, need to be fixed, TODO
            new_der_dict = {self_var_keys[0]: self.partial_dict[self_var_keys[0]]*other}
            return AD(self.func_val*other, new_der_dict)

    def __rmul__(self, other):
        """Overload to make sure commutativity of operation '*'

        Parameters
        ----------
        other : AD class instance or float
            Elements to be multiplied to self. Can be a AD class instance, which
            will update function value and partial derivative dictionary; Or a con-
            -stant, which will only update function value.

        Returns
        -------
        A new AD class instance with updated information

        Examples
        --------
        >>> x1 = AD(1, {'x1': 1})
        >>> f1 = 10.0*x1
        >>> print(f1.func_val, f1.partial_dict)
        10.0 {'x1': 10.0}
        >>> x2 = 3.4*x1 - 1.4
        >>> print(x2.func_val, x2.partial_dict)
        2.0 {'x1': 3.4}
        >>> f2 = f1 * x2
        >>> print(f2.func_val, f2.partial_dict)
        20.0 {'x1': 54.0}
        """
        if isinstance(other, AD):
            # First try as other is an AD class instance
            return other.__mul__(self)
        else:
            # if other is not an AD class instance, treat as a constant
            self_var_keys = list(self.partial_dict.keys())
            # At this moment, we assume all have one variable, need to be fixed, TODO
            new_der_dict = {self_var_keys[0]: other*self.partial_dict[self_var_keys[0]]}
            return AD(other*self.func_val, new_der_dict)

    def __truediv__(self, other):
        """Overload division operation '/'

        Parameters
        ----------
        other: AD class instance or float
            Elements to be divided from self. Can be an AD class instance, which
            will update function value and partial derivative dictionary; Or a con-
            -stant, which will only update function value.

        Returns
        -------
        A new AD class instance with updated information

        Examples
        --------
        >>> x1 = AD(1., {'x1':1})
        >>> f1 = x1/10.
        >>> print(f1.func_val, f1.partial_dict)
        0.1 {'x1': 0.1}
        >>> x2 = 3.4*x1
        >>> f2 = x2/x1
        >>> print(f2.func_val, f2.partial_dict)
        3.4 {'x1': 0.0}
        """
        try:
            # First try as other is an AD class instance
            # Give the variable list for self object
            self_var_keys = list(self.partial_dict.keys())
            # Give the variable list for other object
            other_var_keys = list(other.partial_dict.keys())
            # At this moment, we assume all have one variable, need to be fixed, TODO
            new_der_value = (self.partial_dict[self_var_keys[0]]*other.func_val - other.partial_dict[self_var_keys[0]]*self.func_val)/(other.func_val**2)
            new_der_dict = {self_var_keys[0]: new_der_value} 
            return AD(self.func_val/other.func_val, new_der_dict)
        except AttributeError:
            # If other is not an AD class instance, treat as a constant
            self_var_keys = list(self.partial_dict.keys())
            # At this moment, we assume all have one variable, need to be fixed, TODO
            new_der_dict = {self_var_keys[0]: self.partial_dict[self_var_keys[0]]/other}
            return AD(self.func_val/other, new_der_dict)

    def __rtruediv__(self, other):
        """Overload to make right version of operation '/' works

        Parameters
        ----------
        other : AD class instance or float
            Elements to be multiplied to self. Can be a AD class instance, which 
            will update function value and partial derivative dictionary; Or a con-
            -stant, which will only update function value.
        
        Returns
        -------
        A new AD class instance with updated information

        Examples
        --------
        >>> x1 = AD(1., {'x1':1})
        >>> f1 = 10.0/x1
        >>> print(f1.func_val, f1.partial_dict)
        10.0 {'x1': -10.0}
        >>> x2 = 3.4*x1 - 1.4
        >>> f2 = x2/x1
        >>> print(f2.func_val, f2.partial_dict)
        2.0 {'x1': 1.4}
        """
        if isinstance(other, AD):
            # First try as other is an AD class instance
            return other.__truediv__(self)
        else:
            # if other is not an AD class instance, treat as a constant
            self_var_keys = list(self.partial_dict.keys())
            # At this moment, we assume all have one variable, need to be fixed, TODO
            new_der_value = -other*self.partial_dict[self_var_keys[0]]/(self.func_val**2)
            new_der_dict = {self_var_keys[0]: new_der_value}
            return AD(other/self.func_val, new_der_dict)

    def __pow__(self, other):
        pass # TODO

    def __rpow__(self, other):
        pass # TODO

    @staticmethod
    def sin(x):
        """A static method to calculate the sine function of a AD instance, or a float
        Parameters
        ----------
        x: AD class instance or float, in radians
           Elements to be operated a sin operator. Can be an AD class instance, whichi
           will update function value and partial derivative dictionary; or a constant, whi-
           -ch will give a constant output
        Returns
        -------
        A new AD class with updated information
        Examples
        --------
        >>> x1 = AD(np.pi/2, {'x1': 1.})
        >>> f1 = AD.sin(x1)
        >>> print(f1.func_val, f1.partial_dict)
        1.0 {'x1': 6.123233995736766e-17}
        >>> x2 = AD.sin(np.pi)
        >>> print(x2)
        1.2246467991473532e-16
        """
        try:
            # First try as x is an AD instance
            new_der_dict = x.partial_dict.copy()
            for var in new_der_dict.keys():
                new_der_dict[var] = np.cos(x.func_val)*new_der_dict[var]
            return AD(np.sin(x.func_val), new_der_dict)
        except AttributeError:
            # if x is not an AD class instance, treat as a constant
            return np.sin(x)

        try:
            # First try as x is an AD instance
            new_der_dict = x.partial_dict.copy()
            for var in new_der_dict.keys():
                new_der_dict[var] = np.cos(x.func_val)*new_der_dict[var]
            return AD(np.sin(x.func_val), new_der_dict)
        except AttributeError:
            # if x is not an AD class instance, treat as a constant
            return np.sin(x)


    @staticmethod
    def cos(x):
        """A static method to calculate the cosine function of a AD instance, or a float

        Parameters
        ----------
        x: AD class instance or float, in radians
           Elements to be operated a consine operator. Can be an AD class instance, whichi
           will update function value and partial derivative dictionary; or a constant, whi-
           -ch will give a constant output

        Returns
        ------- 
        A new AD class with updated information

        Examples
        --------
        >>> x1 = AD(np.pi/2, {'x1': 1.})
        >>> f1 = AD.cos(x1)
        >>> print(f1.func_val.round(1), f1.partial_dict)
        0.0 {'x1': -1.0}
        >>> x2 = AD.cos(np.pi)
        >>> print(x2)
        -1.0
        """
        try:
            # First try as x is an AD instance
            new_der_dict = x.partial_dict.copy()
            for var in new_der_dict.keys():
                new_der_dict[var] = -np.sin(x.func_val)*new_der_dict[var]
            return AD(np.cos(x.func_val), new_der_dict)
        except AttributeError:
            # if x is not an AD class instance, treat as a constant
            return np.cos(x)

    @staticmethod
    def tan(x):
        """A static method to calculate the tangent function of a AD instance, or a float

        Parameters
        ----------
        x: AD class instance or float, in radians
           Elements to be operated a tangent operator. Can be an AD class instance, which
           will update function value and partial derivative dictionary; or a constant, whi-
           -ch will give a constant output

        Returns
        ------- 
        A new AD class with updated information

        Examples
        --------
        >>> x1 = AD(np.pi, {'x1': 1.})
        >>> f1 = AD.tan(x1)
        >>> print(f1.func_val.round(1), f1.partial_dict)
        -0.0 {'x1': 1.0}
        >>> x2 = AD.tan(np.pi)
        >>> print(x2.round(1))
        -0.0
        """
        try:
            # First try as x is an AD instance
            new_der_dict = x.partial_dict.copy()
            for var in new_der_dict.keys():
                new_der_dict[var] = new_der_dict[var]/(np.cos(x.func_val)**2)
            return AD(np.tan(x.func_val), new_der_dict)
        except AttributeError:
            # if x is not an AD class instance, treat as a constant
            return np.tan(x)

    @staticmethod
    def log(x):
        """A static method to calculate the natrual logrithm function of a AD instance, or a float

        Parameters
        ----------
        x: AD class instance or float, in radians
           Elements to be operated a natural logrithm. Can be an AD class instance, which
           will update function value and partial derivative dictionary; or a constant, whi-
           -ch will give a constant output

        Returns
        ------- 
        A new AD class with updated information

        Examples
        --------
        >>> x1 = AD(np.e**2, {'x1': 1.})
        >>> f1 = AD.log(x1)
        >>> print(f1.func_val.round(1), f1.partial_dict)
        2.0 {'x1': 0.1353352832366127}
        >>> x2 = AD.log(np.e)
        >>> print(x2)
        1.0
        """
        try:
            # First try as x is an AD instance
            new_der_dict = x.partial_dict.copy()
            for var in new_der_dict.keys():
                new_der_dict[var] = new_der_dict[var]/x.func_val
            return AD(np.log(x.func_val), new_der_dict)
        except AttributeError:
            # if x is not an AD class instance, treat as a constant
            return np.log(x)
        
if __name__ == '__main__':
    import doctest
    doctest.testmod()
