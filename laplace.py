from sympy import *

a, b, s = symbols('a b s')

Eq = s**2 + a*s + b**2

pprint(factor(Eq))
