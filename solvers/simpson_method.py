from decimal import Decimal

from entities.ArgSet import ArgSet
from utils import MAX_NUMBER_OF_PARTITIONS, round_result, runge_iterator, SIMP_K


def simpson_iteration(argset : ArgSet):
    h = (argset.upper_limit - argset.lower_limit) / argset.number_of_partitions
    res = 0
    res += (argset.get_fx(argset.lower_limit) + argset.get_fx(argset.upper_limit))
    x = argset.lower_limit
    for i in range(argset.number_of_partitions - 1):
        if i % 2 == 0:
            res += 2 * argset.get_fx(x)
        else:
            res += 4 * argset.get_fx(x)
        x += h
    res *= h / 3
    return res

def solve_simpson(argset : ArgSet):
    return runge_iterator(argset, simpson_iteration, SIMP_K)

