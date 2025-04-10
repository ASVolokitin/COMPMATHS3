from decimal import Decimal
import sympy as sp

from entities.ArgSet import ArgSet
from utils import get_h, MAX_NUMBER_OF_PARTITIONS, round_result, runge_iterator, TRAP_K


def calculate_iteration(argset : ArgSet):
    h = get_h(argset)
    x = argset.lower_limit + h
    res = 0
    for _ in range(argset.number_of_partitions - 1):
        res += argset.get_fx(x)
        x += h
    res += sp.Float(argset.get_fx(argset.lower_limit) + argset.get_fx(argset.upper_limit)) / 2
    res *= h
    return sp.Float(res)

def solve_trapezoid(argset : ArgSet):
    return runge_iterator(argset, calculate_iteration, TRAP_K)