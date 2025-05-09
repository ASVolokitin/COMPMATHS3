import argparse
import json
import re

import sympy as sp
from sympy.parsing.sympy_parser import parse_expr
from sympy import symbols, log, lambdify

from entities.ArgSet import ArgSet

MAX_NUMBER_OF_PARTITIONS = 1e6
MAX_PRECISION = 50
RECT_K = 2
TRAP_K = 2
SIMP_K = 4

def replace_decimal_commas(expr_str):
    return re.sub(r'(?<=\d),(?=\d)', '.', expr_str)

def sympify_func(func_str):
    func_str = replace_decimal_commas(func_str.strip())
    try:
        expr = sp.sympify(func_str, rational=True)
        variables = expr.free_symbols
        if not variables.issubset({sp.Symbol('x')}):
            raise TypeError("The function should contain only the variable x.")
        return expr
    except KeyError as e:
        print("Function feels like far too weird ...")
        exit(1)
    except AttributeError as e:
        print("Function format is unacceptable")
        return
    except sp.SympifyError as e:
        print(e)
        return

def parse_func(func_str):
    func_str = replace_decimal_commas(func_str.strip())
    try:
        expr = parse_expr(func_str)
        variables = expr.free_symbols
        if not variables.issubset({sp.Symbol('x')}):
            raise TypeError("The function should contain only the variable x.")
        return expr
    except KeyError as e:
        print("Function feels like far too weird ...")
        exit(1)
    # except AttributeError as e:
    #     print("Function format is unacceptable")
    #     return
    except sp.SympifyError as e:
        print(e)
        return

def lambdify_func(expr):
    return sp.lambdify(sp.symbols('x'), expr, "math")

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
    if result_tuple is None:
        print("Program finished with no result")
        return
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

def save_result(outut_filename, solution):
    if outut_filename is not None and outut_filename != "":
        try:
            if not isinstance(outut_filename, str):
                raise TypeError("The file name must be a string")

            try:
                to_json_data = solution[1].to_json()
                to_json_data['result'] = float(solution[0])
                json_data = json.dumps(to_json_data, indent=4)
            except TypeError as e:
                print(f"The object is not serializable in JSON: {e}")
                return

            try:
                with open(outut_filename, "w", encoding="utf-8") as f:
                    f.write(json_data)
            except PermissionError as e:
                print(f"Permission denied: {e}")
                return
            except IOError as e:
                print(f"Error writing to a file {outut_filename}: {e}")
                return

        except Exception as e:
            print(f"Couldn't save the object to {outut_filename}: {e}")
            return


def runge_iterator(argset : ArgSet, calculate_iteration, k):
    prev = calculate_iteration(argset)
    if prev is None:
        raise ValueError
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
            raise ValueError("During the devision, a transition was made to the complex plane, the result cannot be interpreted meaningfully.")
        cur = calculate_iteration(argset)

    return round_result(cur, argset.precision), argset

def is_complex(value):
    if isinstance(value, (sp.Add, sp.Mul)):
        return any(sp.I in arg.atoms() for arg in value.args)
    return sp.I in value.atoms() if hasattr(value, 'atoms') else isinstance(value, complex)