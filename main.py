from tkinter import W
from weakref import finalize
from includes import *
from selenium.webdriver.remote.webelement import WebElement
from kwyk import latex_solve_eq, sanitize_latex
from sympy.sets.sets import Interval
from sympy import pi

from selenium_interact_layer import finish, write_output

import traceback

x = Symbol('x')
y = Symbol('y')
h = Symbol('h')

k = Symbol('k')
A = Symbol('A')

trig_int = Interval.Lopen(-pi, pi)
wtrig_int = Interval(-pi, pi)


def main_fn():
    def evalc(txt):
        try:
            return eval(txt, {__builtins__: None},
                        {'e': e, 'se': se, 'c': c, 'x': x, 'k': k, 'A': A, 'pi': pi,
                         'trig_int': trig_int,
                         'wtrig_int': wtrig_int,
                         'diff': diff,
                         'latex': latex,
                         'latex_solve_eq': latex_solve_eq, 'solve_eq': solve_eq,
                         'solve_eq_diff': solve_eq_diff, 'latex_solve_eq_diff': latex_solve_eq_diff,
                         'solve_nohomo_eq_diff': solve_nohomo_eq_diff, 'latex_solve_nohomo_eq_diff': latex_solve_nohomo_eq_diff,
                         'Interval': Interval,
                         'sign_table': print_sign_table,
                         'are_coplanar_points': are_coplanar_points,
                         'find_coplanar_point': find_coplanar_point,
                         'triplet_from_paste': triplet_from_paste,
                         'vecs_are_coplanar': vecs_are_coplanar,
                         'pts_cpl_paste': points_are_coplanar_from_paste,
                         'plane_eq': plane_eq,
                         'lines_are_parral': lines_are_parral,
                         'lines_are_identical': lines_are_identical,
                         'lines_intersect_vec': lines_intersect_vec,
                         'lines_intersect_pt': lines_intersect_pt,
                         'line_from_paste': line_from_paste,
                         'sympy_plane_from_eq': sympy_plane_from_eq})

        except Exception as ex:
            print("something went wrong with your code, please check it !!")
            traceback.print_exception(ex)
            return None

    driver, wait = setup("https://www.monbureaunumerique.fr/")
    login(driver, wait)

    input("appuie sur <enter> quand tu es sur la page de la question.")

    e = get_exprs(driver, wait)
    print(e)
    se = [inter_inp(x) for x in e]
    print(se)

    c = None
    quit: bool = False
    while not quit:
        usr_txt = input(">> ")
        if (len(usr_txt) == 0):
            continue

        if (usr_txt[0] == '$'):
            match usr_txt[1]:
                case 'w':
                    print("writing output to Kwyk !")
                    argv = get_arg(usr_txt, 1)
                    if argv == None:
                        continue
                    arg = evalc(argv[1])
                    if arg == None:
                        continue

                    if not isinstance(arg, list):
                        # print("not list")
                        arg = [sanitize_latex(arg)]
                    else:
                        # print("list")
                        arg = [sanitize_latex(x) for x in arg]
                    print(arg)
                    write_output(driver, wait, arg)
                case 'g':
                    print("(re)getting the math from question")
                    e = get_exprs(driver, wait)
                    print(e)
                    se = [inter_inp(x) for x in e]
                    print(se)
                case 's':
                    print("solving equation")
                    argv = get_arg(usr_txt, 1)
                    if argv == None:
                        continue
                    c = solve_eq(evalc(argv[1]))
                    print("c = ", c)
                case 'l':
                    print("transforming to latex !")
                    argv = get_arg(usr_txt, 1)
                    if argv == None:
                        continue
                    c = sanitize_latex(latex(evalc(argv[1])), useSet=True)
                    print("c = \'", c, "\'")
                case 'q':
                    print("cya !!")
                    quit = True
                case 'e':
                    print(e)
                    print(se)
                    print(c)
        else:
            c = evalc(usr_txt)
            print(f"c = \'{c}\'")

    finish(driver, wait)


katex_css_selector = ".katex-mathml annotation"
MathJax_css_selector = "script[id^=MathJax-Element-]"


def get_exprs(driver, wait):
    web_eles: list[WebElement] = []
    try:
        web_eles += driver.find_elements(
            By.CSS_SELECTOR, katex_css_selector)
    except Exception as e1:
        pass

    try:
        web_eles += driver.find_elements(
            By.CSS_SELECTOR, MathJax_css_selector)
    except Exception as e2:
        pass

    exprs = [x.get_attribute("textContent") for x in web_eles]
    return exprs


def get_arg(txt, argc=1):
    argv = txt.split(' ', argc)
    if (len(argv) < argc + 1):
        print("you must provide an expression to solve as an argument !")
        return None
    return argv


if __name__ == '__main__':
    main_fn()
