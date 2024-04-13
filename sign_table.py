from sympy.sets.sets import EmptySet, Interval, FiniteSet, Union, SetKind
from sympy.core.singleton import S
from sympy import oo, limit, sqrt, pprint
from sympy.calculus.singularities import is_decreasing
from sympy import pretty, nsimplify, diff, solveset, simplify
from sympy.calculus.util import continuous_domain
from sympy.abc import x

import traceback


def pad(count: int, ch: str = " "):
    string = ""
    i = 0
    while i < count:
        string += ch
        i += 1
    return string


def mstr(expr):
    return str(expr).replace("log", "ln")


def subs_root(f, root):
    return simplify(f.subs(x, nsimplify(root, rational=True, full=True)))


def str_sign_table(f, use_unicode: bool = True, max_domain=Interval(-oo, oo), cols: list[str] = ["x", "f'(x)", "f(x)"], print_third_line=True):
    def add_padding(i: int, ch: str = " "):
        string = ch*2
        string += pad(max_width(i), ch)
        string += ch*2
        return string

    def max_width(i: int):
        return max(first_line_spacings[i], second_line_spacings[i], third_line_spacings[i])

    def text_add(text, i: int, line: list):
        string = "  "
        string += text
        string += pad(max_width(i) - line[i])
        string += "  "
        return string

    def print_sep():
        string = hline*(init_max_width + 1) + crossing
        string += pad(max_width(0), hline)
        for i in range(len(roots_of_f_prime)):
            string += add_padding(2*i + 1, hline)

            string += hline * 2
            if illegal_values.contains(roots_of_f_prime[i]):
                string += v_double
                string += pad(max_width(2*i + 2) -
                              len(v_double_h_single), hline)
            else:
                string += pad(max_width(2*i + 2), hline)
            string += hline * 2
        string += add_padding(2*n_roots + 1, hline)
        string += add_padding(2*n_roots + 2, hline)
        return string

    def get_spacings(before: list, loop: list, after: list):
        spacings = []
        for beforeVal in before:
            spacings.append(beforeVal)

        for root in roots_of_f_prime:
            for insideLoop in loop:
                spacings.append(insideLoop(root))

        for afterVal in after:
            spacings.append(afterVal)

        return spacings

    try:
        f_domain = continuous_domain(f, x, domain=max_domain)
        illegal_values = f_domain.complement(max_domain)
        if type(illegal_values) != FiniteSet and type(illegal_values) != EmptySet:
            print("[ERROR] having illegal values not be finite is not implemented")

        f_prime = diff(f, x)
        roots_of_f_prime = list(
            Union(solveset(f_prime, x, domain=max_domain), illegal_values))
        roots_of_f_prime = list(map(lambda root: nsimplify(
            root, full=True, rational=True), roots_of_f_prime))
        roots_of_f_prime.sort()
        n_roots = len(roots_of_f_prime)

        sets = []

        hline = "\u2500" if use_unicode else "-"
        vline = "\u2502" if use_unicode else "|"
        crossing = "\u253c" if use_unicode else "|"
        v_double = "\u2551" if use_unicode else "||"
        v_double_h_single = "\u256c" if use_unicode else "||"
        up_arrow = "\u2197" if use_unicode else " "
        down_arrow = "\u2198" if use_unicode else " "

        first_line_spacings = get_spacings(
            [len(str(max_domain.start)), 0], [lambda x:len(mstr(x)), lambda _:0], [2])

        second_line_spacings = get_spacings(
            [0], [lambda _:1, lambda x: len("0") if not illegal_values.contains(x) else len(v_double)], [1, 0])

        third_line_spacings = get_spacings([len(str(limit(f, x, max_domain.start)))], [lambda _: 1, lambda root:len(
            mstr(subs_root(f, root))) if not illegal_values.contains(root) else len(v_double)], [1, len(str(limit(f, x, max_domain.end)))])

        # print(first_line_spacings)
        # print(second_line_spacings)
        # print(third_line_spacings)

        init_max_width = max(len(cols[0]), len(cols[1]), len(cols[2]))

        first_line = cols[0] + pad(init_max_width - len(cols[0]) + 1) + vline
        second_line = cols[1] + pad(init_max_width - len(cols[1]) + 1) + vline
        third_line = cols[2] + pad(init_max_width - len(cols[2]) + 1) + vline

        bef = "" if use_unicode else " "

        first_line += bef + str(max_domain.start) + \
            pad(max_width(0) - len(str(max_domain.start))) + "  "

        second_line += bef + pad(max_width(0)) + "  "
        prev = max_domain.start

        third_line += bef + \
            str(limit(f, x, max_domain.start)) + pad(max_width(0) -
                                                     len(str(limit(f, x, max_domain.start)))) + "  "

        for i in range(n_roots):
            root = roots_of_f_prime[i]

            # first line
            first_line += add_padding(2*i + 1)  # aligns with the +/-
            first_line += text_add(mstr(root), 2*i + 2, first_line_spacings)

            # second line
            curr = root
            curr_set = Interval(prev, curr, True, True)
            sets.append(curr_set)
            is_going_down = is_decreasing(
                f, interval=curr_set)
            second_line += text_add('-' if is_going_down else '+',
                                    2 * i + 1, second_line_spacings)
            second_line += text_add("0" if not illegal_values.contains(root)
                                    else v_double, 2*i + 2, second_line_spacings)
            prev = curr

            # third line
            third_line += text_add(down_arrow if is_going_down else up_arrow,
                                   2*i + 1, third_line_spacings)
            text_value = mstr(subs_root(f, root))
            # illegal values should be marked with "||"
            if illegal_values.contains(root):
                text_value = v_double
            third_line += text_add(text_value, 2*i + 2, third_line_spacings)

        first_line += add_padding(2 * n_roots + 1)
        first_line += "  " + \
            pad(max_width(2*n_roots + 2) - len(str(max_domain.end))) + \
            str(max_domain.end)

        curr_set = Interval(prev, max_domain.end, True, True)
        sets.append(curr_set)
        is_going_down = is_decreasing(
            f, interval=curr_set)
        second_line += text_add('-' if is_going_down else '+',
                                2 * n_roots + 1, second_line_spacings)
        second_line += add_padding(2*n_roots + 2)

        # third_line += #add_padding(2 * n_roots + 1)
        third_line += text_add(down_arrow if is_going_down else up_arrow,
                               2*n_roots + 1, third_line_spacings)
        third_line += "  " + pad(max_width(2*n_roots + 2) - len(
            str(limit(f, x, max_domain.end)))) + str(limit(f, x, max_domain.end))

        out = first_line + '\n'
        out += print_sep() + '\n'
        out += second_line + '\n'
        if print_third_line:
            out += print_sep() + '\n'
            out += third_line + '\n'
    except KeyboardInterrupt:
        raise KeyboardInterrupt
    except Exception as e:
        traceback.print_exception(e)
    return out, sets


def print_sign_table(f, use_unicode: bool = True, max_domain: Interval = Interval(-oo, oo), cols: list[str] = ["x", "f'(x)", "f(x)"], print_third_line: bool = True):
    text, sets = str_sign_table(
        f, use_unicode, max_domain, cols, print_third_line)
    print(text)
    return sets


if __name__ == "__main__":
    print_sign_table(sqrt(x)*(x**2 - 2*x + 1),
                     max_domain=Interval(0, +oo))
