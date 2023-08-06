"""Arith object that contains 5 functions for addition, subtraction, division, multiplication, and factorial
Author: Nicholas Boldery"""


class Arith(object):

    def __init__(self): pass

    def add(x, y):
        """
        >>> Arith.add(5, 2)
        7
        """
        return (x + y)


    def sub(x, y):
        """
        subtracts value x from value y and returns difference
        >>> Arith.sub(20, 5)
        15
        """
        return (x - y)

    def div(x, y):
        """
        divides value y from value x and returns result in double
        >>> Arith.div(30, 15)
        2.0
        """
        return (x / y)

    def mul(x, y):
        """
        multiplies value x by value y and returns product
        >>> Arith.mul(15, 5)
        75
        """
        return (x * y)
    def fact(x):
        """
        recursive factorial, base case 1 to avoid unnecessary computation.
        multiplies value x by recursive call of fact(x-1) until it reaches one and then returns the product
        >>> Arith.fact(5)
        120
        """
        if(x == 1):
            return x
        else:
            return x * Arith.fact(x-1)


