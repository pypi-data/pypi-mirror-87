"""Arith object that contains 5 functions for addition, subtraction, division, multiplication, and factorial
Author: Nicholas Boldery"""


class Arith(object):

    def __init__(self): pass
    #adds values from two inputs and returns sum
    def add(self, x, y): return (x + y)
    #subtracts value x from value y and returns difference
    def sub(self, x, y): return (x - y)
    #divides value y from value x and returns result
    def div(self, x, y): return (x/y)
    #multiplies value x by value y and returns product
    def mul(self, x, y): return(x*y)
    #recursive factorial, base case 1 to avoid unnecessary computation.
    #multiplies value x by recursive call of fact(x-1) until it reaches one and then returns the product
    def fact(self, x):
        if(x == 1):
            return x
        else:
            return x * Arith.fact(self, x-1)


