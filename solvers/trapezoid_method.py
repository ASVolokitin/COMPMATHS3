from decimal import Decimal

from entities.ArgSet import ArgSet
from utils import get_h, MAX_NUMBER_OF_PARTITIONS, round_result


def calculate_iteration(argset : ArgSet):
    h = get_h(argset)
    x = argset.lower_limit + h
    res = Decimal(0)
    for _ in range(argset.number_of_partitions - 1):
        res += argset.func(x)
        x += h
    res += Decimal(argset.func(argset.lower_limit) + argset.func(argset.upper_limit)) / 2
    res *= h
    return res

def solve_trapezoid(argset : ArgSet):
    prev = calculate_iteration(argset)
    argset.number_of_partitions *= 2
    cur = calculate_iteration(argset)
    while abs(cur - prev) / 3 >= 0.1 ** argset.precision:
        argset.number_of_partitions *= 2
        if argset.number_of_partitions > MAX_NUMBER_OF_PARTITIONS:
            raise ValueError(
                "The specified accuracy will take too long to calculate, reduce it or the length of the interval")
        prev = cur
        cur = calculate_iteration(argset)

    return round_result(cur, argset.precision), argset