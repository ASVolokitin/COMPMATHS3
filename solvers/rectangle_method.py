from decimal import Decimal

from entities.ArgSet import ArgSet
from entities.SolvingMethod import SolvingMethod
from utils import get_h, MAX_NUMBER_OF_PARTITIONS, round_result


def get_starting_point(argset : ArgSet):
    if argset.method == SolvingMethod.RECT_RIGHT:
        return Decimal(argset.lower_limit)
    elif argset.method == SolvingMethod.RECT_LEFT:
        return Decimal(argset.lower_limit + get_h(argset))
    elif argset.method == SolvingMethod.RECT_MIDDLE:
        return Decimal(argset.lower_limit + get_h(argset) / 2)
    else:
        raise ValueError(f'Unknown method: {argset.method}')

def calculate_iteration(argset : ArgSet):
    res = 0
    x = get_starting_point(argset)
    h = get_h(argset)
    for _ in range(argset.number_of_partitions):
        res += Decimal(argset.func(x) * get_h(argset))
        x += h
    return res


def solve_rectangle(argset : ArgSet):
    prev = calculate_iteration(argset)
    argset.number_of_partitions *= 2
    cur = calculate_iteration(argset)
    while abs(cur - prev) / 3 >= 0.1**argset.precision:
        argset.number_of_partitions *= 2
        if argset.number_of_partitions > MAX_NUMBER_OF_PARTITIONS:
            raise ValueError("The specified accuracy will take too long to calculate, reduce it or the length of the interval")
        prev = cur
        cur = calculate_iteration(argset)

    return round_result(cur, argset.precision), argset


