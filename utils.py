import argparse
from argparse import ArgumentError

import sympy as sp

from decimal import Decimal
from entities.ArgSet import ArgSet

MAX_NUMBER_OF_PARTITIONS = 1e6 * 3
MAX_PRECISION = 50

def parse_func(func_str):
    func_str = func_str.strip().replace(",", ".")
    try:
        expr = sp.sympify(func_str)
        variables = expr.free_symbols
        if not variables.issubset({sp.Symbol('x')}):
            raise TypeError("The function should contain only the variable x.")
        if str(expr) == "zoo":
            raise TypeError("The entered expression is an ambiguity")
        return sp.lambdify(sp.symbols('x'), expr, 'numpy')
    except (sp.SympifyError, NameError, AttributeError) as e:
        print("The syntax of the function does not match the format")
        exit(1)


def uni_float(value):
    try:
        print(value)
        return Decimal(value.replace(',', '.'))
    except ValueError:
        return argparse.ArgumentTypeError(' is not a float' % value)

def get_h(argset : ArgSet):
    return Decimal((argset.upper_limit - argset.lower_limit) / argset.number_of_partitions)

def round_result(result, precision):
    # return round(result, len(str(precision).split('.')[1])
    return round(result, precision)

def print_result(result_tuple):
    print(f"""\nRESULT:
    function: {result_tuple[1].func}
    lower limit: {result_tuple[1].lower_limit}
    upper limit: {result_tuple[1].upper_limit}
    method: {result_tuple[1].method.name}
    result: {result_tuple[0]}
    precision: {result_tuple[1].precision}
    number of partitions: {result_tuple[1].number_of_partitions}
    """)