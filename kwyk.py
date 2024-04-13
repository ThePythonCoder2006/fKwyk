import re
from sympy import Line3D, solve, solveset, simplify, Symbol, S, latex, factor, diff, pprint, srepr, pretty, Rational, exp, symbols, Point3D, Plane
from sympy.calculus.util import continuous_domain
from sympy.geometry.util import intersection

from latex2sympy2 import latex2sympy

from sign_table import print_sign_table

x = Symbol('x')
y = Symbol('y')
h = Symbol('h')

k = Symbol('k')
A = Symbol('A')

a = Symbol('a')
b = Symbol('b')
c = Symbol('c')


def P1(a, b):
    return a*x + b


"""
standart degree 2 polynomial function stuff
"""


def P2(a, b, c):
    return a*x**2 + b*x + c


# returns alpha for P(x) = a*x**2 + b*x + c
def alpha(a, b, c):
    return -b/(2*a)


def beta(a, b, c):
    return (-(Delta(a, b, c))/(4*a))

# returns Delta for P(x) = a*x**2 + b*x + c


def Delta(a, b, c):
    return b**2 - 4*a*c


def canon(a: Rational, b: Rational, c: Rational):
    return (a)*(x - (alpha(a, b, c)))**2 + beta(a, b, c)


def finite_diff(f, a):
    return simplify((f(a + h) - f(a))/h)


# accepts the input in latex and outputs the sympy equivaltent
def inter_inp(inp: str):
    val: str = inp.strip()
    # val: str = inp.replace("\\left", "")
    # val = val.replace("\\right", "")
    val = val.replace("=", "==")
    val = val.replace(r"\lt", "<")
    val = val.replace(r"\gt", ">")
    val = val.replace(r"\operatorname{ln}", r"\ln")
    val = val.replace(r"\operatorname{cos}", r"\cos")
    val = val.replace(r"\operatorname{sin}", r"\sin")
    val = remove_mapsto(val)
    try:
        val = latex2sympy(val)
    except:
        # print(f"something went wrong with : \"{inp}\" (\"{val}\")")
        val = inp
    return val


def sanitize_latex(dirtyLatex: str, useSet: bool = True):
    if not isinstance(dirtyLatex, str):
        return dirtyLatex
    cleanLatex: str = dirtyLatex.replace(r"\ln", "ln")
    cleanLatex = cleanLatex.replace(r"\log", "ln")
    cleanLatex = cleanLatex.replace(r"\sin", "sin")
    cleanLatex = cleanLatex.replace(r"\cos", "cos")
    cleanLatex = cleanLatex.replace(r"\ ", "")

    if useSet:
        cleanLatex = cleanLatex.replace(',', ';')
    return cleanLatex


def remove_mapsto(LatexExpr: str) -> str:
    expr = LatexExpr.strip()
    expr = expr.replace("f: x \\mapsto", "")
    expr = expr.replace("f:x \\mapsto", "")
    expr = expr.replace("f:x\\mapsto", "")
    return expr


def latex_solve_eq(LatexExpr: str, var=x) -> str:
    expr = inter_inp(LatexExpr)
    return sanitize_latex(latex(solve_eq(expr, var)), useSet=True)


def solve_eq(expr, var=x, max_domain=S.Reals):
    domain = continuous_domain(expr, var, domain=max_domain)
    return solveset(expr, var, domain=domain)

# solutions of differential eq of the form y' + ay = b, /w y(IC[0]) = IC[1]


def solve_eq_diff(a, b, IC=None, dummy=k):
    k = dummy
    expr = k * exp(-a * x) + Rational(b, a)
    if IC == None:
        return expr

    # this is (normally) a linear equation so the domain is \R
    k_val = list(solveset(expr.subs(x, IC[0]) - IC[1], k, domain=S.Reals))[0]
    return simplify(expr.subs(k, k_val))


def latex_solve_eq_diff(a, b, IC=None, dummy=k):
    return sanitize_latex(latex(solve_eq_diff(a, b, IC, k)))


def solve_nohomo_eq_diff(a2, f, deg, dummy=k):
    if deg == 1:
        vars = [a, b]
        P = P1
    elif deg == 2:
        vars = [a, b, c]
        P = P2
    else:
        print("only linear and quadratic f are currently supported")

    f0 = P(*vars)
    abcs = solve(diff(f0, x) + a2*f0 - f, vars, domain=S.Reals, dict=False)
    f0 = P(*[abcs[x] for x in vars])
    pprint(f0)

    homo = solve_eq_diff(a2, 0, None, dummy)
    pprint(homo)

    sol = homo + f0
    pprint(sol)

    return [f0, homo, sol]


def latex_solve_nohomo_eq_diff(a2, f, deg, dummy=k):
    return [sanitize_latex(latex(x)) for x in solve_nohomo_eq_diff(a2, f, deg, dummy)]


def plane_eq(A: tuple[float, float, float], B: tuple[float, float, float], C: tuple[float, float, float]):
    a1 = B[0] - A[0]  # x2 - x1
    b1 = B[1] - A[1]  # y2 - y1
    c1 = B[2] - A[2]  # z2 - z1
    a2 = C[0] - A[0]  # x3 - x1
    b2 = C[1] - A[1]  # y3 - y1
    c2 = C[2] - A[2]  # z3 - z1
    a = b1 * c2 - b2 * c1
    b = a2 * c1 - a1 * c2
    c = a1 * b2 - b1 * a2
    d = (- a * A[0] - b * A[1] - c * A[2])
    return (a, b, c, d)


def are_coplanar_points(A: tuple[float, float, float], B: tuple[float, float, float], C: tuple[float, float, float], D: tuple[float, float, float]):
    a, b, c, d = plane_eq(A, B, C)

    # equation of plane is: a*x + b*y + c*z = 0
    return (a * D[0] + b * D[1] + c * D[2] + d == 0)


def points_are_coplanar_from_paste():
    return are_coplanar_points(*triplet_from_paste(input()))


def find_coplanar_point(A: tuple[float, float, float], B: tuple[float, float, float], C: tuple[float, float, float], Dx=None, Dy=None, Dz=None):
    num_set = float(Dx != None) + float(Dy != None) + float(Dz != None)

    if (num_set == 3):
        return (Dx, Dy, Dz)

    if (num_set < 2):
        print("[ERROR] multiple solutions is not (yet) implemented !!")
        return None

    a, b, c, d = plane_eq(A, B, C)

    if (Dx == None):
        x = Rational(-1, a) * (b * Dy + c * Dz + d)
        return (x, Dy, Dz)
    if (Dy == None):
        y = Rational(-1, b) * (a * Dx + c*Dz + d)
        return (Dx, y, Dz)
    if (Dz == None):
        z = Rational(-1/c) * (a * Dx + b*Dy + d)
        return (Dx, Dy, z)


def vecs_are_colinear(A: tuple[float, float, float], B: tuple[float, float, float]):
    x = A[1] * B[2] - A[2] * B[1]

    y = A[2] * B[0] - A[0] * B[2]

    z = A[0] * B[1] - A[1] * B[0]

    return (x == 0 and y == 0 and z == 0)


def lines_are_parral(u, v):
    return vecs_are_colinear(u, v)


def lines_are_identical(A: tuple[float, float, float], u: tuple[float, float, float], B: tuple[float, float, float], v: tuple[float, float, float]):
    if (not vecs_are_colinear(u, v)):
        return False

    t = Symbol('t')
    return (solve([-B[i] + A[i] + v[i] * t for i in range(3)], t) != [])


def lines_intersect_vec(A, u, B, v):
    A_ = [A[i] + u[i] for i in range(3)]
    B_ = [B[i] + v[i] for i in range(3)]

    return lines_intersect_pt(A, A_, B, B_)


def lines_intersect_pt(A, B, C, D):

    L1 = Line3D(A, B)
    L2 = Line3D(C, D)

    # if (Line3D.is_parallel(L1, L2)):
    #     return False

    return intersection(L1, L2)[0].coordinates


def sympy_plane_from_eq(a, b, c, d):
    # z = (ax + bz + d)/c

    z1 = (a * 0 + b * 0 + d)/c
    z2 = (a * 1 + b * 0 + d)/c
    z3 = (a * 0 + b * 1 + d)/c

    return Plane(Point3D(0, 0, z1), Point3D(1, 0, z2), Point3D(0, 1, z3))


def vecs_are_coplanar(u, v, w):
    # 0·4·8 + 1·5·6 + 2·3·7 - 2·4·6 - 1·3·8 - 0·5·7
    triple_prod = u[0]*v[1]*w[2] + u[1]*v[2]*w[0] + u[2]*v[0] * \
        w[1] - u[2]*v[1]*w[0] - u[1]*v[0]*w[2] - u[0]*v[2]*w[1]
    return triple_prod == 0


def triplet_from_paste(str: str):
    str = str.replace("−", "-")  # warning not identical !!
    matches = re.findall(
        r".*?\(([\d\-]+);([\d\-]+);([\d\-]+).*?\)", str)

    triplets = [(int(match[0]), int(match[1]), int(match[2]))
                for match in matches]

    return tuple(triplets)


def line_from_paste(str: str):
    str = str.replace("−", "-")
    str = str.replace(" ", "")
    str = str.replace("+t", "+1t")
    str = str.replace("-t", "-1t")
    matches = re.findall(r"[xyz].*?=.*?([\d\-]+).*?([+\-].*?\d+)t", str)
    A = (int(matches[0][0]), int(matches[1][0]), int(matches[2][0]))
    u = (int(matches[0][1]), int(matches[1][1]), int(matches[2][1]))

    return A, u


def line_plane_relationship(A, B, a, b, c, d):
    # x, y, z : ax + by + cz = 0
    z1 = Rational(-1, c) * (a*0 + b*1)
    z2 = Rational(-1, c) * (a*1 + b*0)

    AB = [B[i] - A[i] for i in range(3)]
    u = (0, 1, z1)
    v = (1, 0, z2)

    if (not vecs_are_coplanar(AB, u, v)):
        print("the plane and line intersect on a point")
    elif (a*A[0] + b*A[1] + c*A[2] + d == 0):  # A \in P
        print("the line is included in the plane")
    else:
        print("the line and plane are stricly parrallel")

    return


class Solver:
    def __init__(self,
                 standart_output_func, n_standart_outputs=1,
                 special_output_funcs=None, n_special_outputs=0,
                 special_input_funcs=None, n_special_inputs=0,
                 is_katex=True, has_std_input=True,
                 std_input_exclude=[]):
        self.standart_output_func = standart_output_func
        self.n_standart_outputs = n_standart_outputs

        self.special_output_funcs = special_output_funcs
        self.n_special_outputs = n_special_outputs

        self.special_input_funcs = special_input_funcs
        self.n_special_inputs = n_special_inputs

        self.is_katex = is_katex
        self.has_std_input = has_std_input
        self.std_input_exclude = std_input_exclude


if __name__ == "__main__":
    # print_sign_table((exp(x) - 6)/(exp(x) - 1))
    print_sign_table(1/(Rational(1, 5)*x**5 - Rational(1, 3)*x**3))
    print("\n")
