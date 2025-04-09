from entities.ArgSet import ArgSet
from entities.SolvingMethod import SolvingMethod

import numpy as np

def get_h(argset : ArgSet):
    return (argset.upper_limit - argset.lower_limit) / argset.number_of_partitions

def get_starting_point(argset : ArgSet):
    if argset.method == SolvingMethod.RECT_RIGHT:
        return argset.lower_limit
    elif argset.method == SolvingMethod.RECT_LEFT:
        return argset.lower_limit + get_h(argset)
    elif argset.method == SolvingMethod.RECT_MIDDLE:
        return argset.lower_limit + get_h(argset) / 2

def solve_rectangle(argset : ArgSet):
    res = 0
    x = get_starting_point(argset)
    h = get_h(argset)
    for _ in range(argset.number_of_partitions):
        res += argset.func(x) * get_h(argset)
        x += h
    return res
