from decimal import Decimal

from entities.ArgSet import ArgSet
from utils import MAX_NUMBER_OF_PARTITIONS, round_result


def calculate_iteration(argset : ArgSet):
    h = (argset.upper_limit - argset.lower_limit) / argset.number_of_partitions
    res = Decimal(0)
    res += argset.func(argset.lower_limit) + argset.func(argset.upper_limit)
    x = argset.lower_limit
    for i in range(argset.number_of_partitions - 1):
        if i % 2 == 0:
            res += 2 * argset.func(x)
        else:
            res += 4 * argset.func(x)
        x += h
    res *= h / 3
    return res

def solve_simpson(argset : ArgSet):
    prev = calculate_iteration(argset)
    argset.number_of_partitions *= 2
    cur = calculate_iteration(argset)
    while abs(cur - prev) / 15 >= 0.1**argset.precision:
        argset.number_of_partitions *= 2
        if argset.number_of_partitions >= MAX_NUMBER_OF_PARTITIONS:
            raise ValueError("The specified accuracy will take too long to calculate, reduce it or the length of the interval")
        prev = cur
        cur = calculate_iteration(argset)

    return round_result(cur, argset.precision), argset
