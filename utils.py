import argparse

import sympy as sp

from entities.ArgSet import ArgSet

MAX_NUMBER_OF_PARTITIONS = 1e6
MAX_PRECISION = 50
RECT_K = 2
TRAP_K = 2
SIMP_K = 4

def parse_func(func_str):
    func_str = func_str.strip().replace(",", ".")
    try:
        expr = sp.sympify(func_str)
        variables = expr.free_symbols
        if not variables.issubset({sp.Symbol('x')}):
            raise TypeError("The function should contain only the variable x.")
        # for atom in expr.atoms():
        #     print(atom)
        #     if atom == sp.zoo or atom == sp.nan or atom == sp.oo:
        #         raise ValueError("Function feels like far too weird ...")
        # f = sp.lambdify(sp.symbols('x'), expr, 'sympy')
        return expr
    # except (sp.SympifyError, NameError, AttributeError) as e:
    #     print("Syntax of the function does not match the format")
    #     exit(1)
    except KeyError as e:
        print("Function feels like far too weird ...")
        exit(1)

def lambdify_func(expr):
    return sp.lambdify(sp.symbols('x'), expr, 'sympy')

def check_singularities(f):
    return sp.singularities(f, sp.symbols('x'))

def uni_float(value):
    try:
        return sp.Float(value.replace(',', '.'))
    except ValueError:
        return argparse.ArgumentTypeError(' is not a float' % value)

def get_h(argset : ArgSet):
    return sp.Float((argset.upper_limit - argset.lower_limit) / argset.number_of_partitions)

def round_result(result, precision):
    # return round(result, len(str(precision).split('.')[1])
    return round(result, precision)

def print_result(result_tuple):
    if is_complex(result_tuple[0]):
        print("During the decision, a transition was made to the complex plane, the result cannot be interpreted meaningfully.")
        return
    print(f"""\nRESULT:
    function: {result_tuple[1].func_text}
    lower limit: {result_tuple[1].lower_limit}
    upper limit: {result_tuple[1].upper_limit}
    method: {result_tuple[1].method.name}
    result: {result_tuple[0]}
    precision: {"±0." + "0" * (result_tuple[1].precision - 1) + "1"}
    number of partitions: {result_tuple[1].number_of_partitions}
    """)

def runge_iterator(argset : ArgSet, calculate_iteration, k):
    prev = calculate_iteration(argset)
    argset.number_of_partitions *= 2
    cur = calculate_iteration(argset)
    while abs(cur - prev) / (2**k - 1) >= 0.1 ** argset.precision:
        argset.number_of_partitions *= 2
        print(f"Current number of partitions: {argset.number_of_partitions}")
        if argset.number_of_partitions > MAX_NUMBER_OF_PARTITIONS:
            raise ValueError(
                "The specified accuracy will take too long to calculate, reduce it or the length of the interval")
        prev = cur
        if is_complex(cur):
            raise ValueError("During the decision, a transition was made to the complex plane, the result cannot be interpreted meaningfully.")
        cur = calculate_iteration(argset)
        print(prev, cur)

    return round_result(cur, argset.precision), argset

def is_complex(value):
    if isinstance(value, (sp.Add, sp.Mul)):
        return any(sp.I in arg.atoms() for arg in value.args)
    return sp.I in value.atoms() if hasattr(value, 'atoms') else isinstance(value, complex)