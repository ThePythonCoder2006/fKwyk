from sympy import solve, Symbol, S, latex, factor, diff,  symbols, Interval, oo, simplify, is_decreasing, EmptySet, Union, solveset, pprint
from sympy.calculus.util import continuous_domain
from latex2sympy2 import latex2sympy
from sympy.series.sequences import RecursiveSeq
from sympy import Function


from kwyk import inter_inp, sanitize_latex, remove_mapsto, Solver, print_sign_table, Rational
from selenium_interact_layer import *

from sign_table import pad, print_sign_table, str_sign_table

import re

x = Symbol('x')
u = Function('u')
n = Symbol('n')

expr_ = r"\left(\dfrac{1}{2}x + \dfrac{1}{4}\right) \ln\left(- \dfrac{1}{3}x + \dfrac{5}{6}\right) "

expr = latex2sympy(expr_)
print(expr)

print(latex(simplify(diff(expr))))
