from entities.ArgSet import ArgSet
from entities.SolvingMethod import SolvingMethod
from solvers.rectangle_method import solve_rectangle
from solvers.simpson_method import solve_simpson
from solvers.trapezoid_method import solve_trapezoid


class Solver:
    def __init__(self, argset : ArgSet):
        self.argset = argset
        # self.method = argset.method
        # self.func = argset.func
        # self.lower_limit = argset.lower_limit
        # self.upper_limit = argset.upper_limit
        # self.precision = argset.precision
        # self.number_of_partitions = argset.number_of_partitions

    def solve(self):
        try:
            if self.argset.method == SolvingMethod.RECT_LEFT or self.argset.method == SolvingMethod.RECT_RIGHT or self.argset.method == SolvingMethod.RECT_MIDDLE:
                return solve_rectangle(self.argset)
            elif self.argset.method == SolvingMethod.TRAP:
                return solve_trapezoid(self.argset)
            elif self.argset.method == SolvingMethod.SIMP:
                return solve_simpson(self.argset)
        except ValueError as e:
                print(e)
                exit(1)