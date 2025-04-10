import sympy as sp

from entities.ArgSet import ArgSet
from entities.SolvingMethod import SolvingMethod
from utils import get_h, MAX_NUMBER_OF_PARTITIONS, round_result, runge_iterator, RECT_K


def get_starting_point(argset : ArgSet):
    if argset.method == SolvingMethod.RECT_RIGHT:
        return sp.Float(argset.lower_limit)
    elif argset.method == SolvingMethod.RECT_LEFT:
        return sp.Float(argset.lower_limit + get_h(argset))
    elif argset.method == SolvingMethod.RECT_MIDDLE:
        return sp.Float(argset.lower_limit + get_h(argset) / 2)
    else:
        raise ValueError(f'Unknown method: {argset.method}')

def rectangle_iteration(argset : ArgSet):
    try:
        res = 0
        x = get_starting_point(argset)
        h = get_h(argset)
        for _ in range(argset.number_of_partitions):
            res += sp.Float(argset.get_fx(x) * get_h(argset))
            x += h
        return sp.Float(res)
    except TypeError:
        print("Error occured while calculating function value")


def solve_rectangle(argset : ArgSet):
    return runge_iterator(argset, rectangle_iteration, RECT_K)


