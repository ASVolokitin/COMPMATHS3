from entities.ArgSet import ArgSet
from entities.SolvingMethod import SolvingMethod
from solvers.rectangle_method import solve_rectangle
from solvers.simpson_method import solve_simpson
from solvers.trapezoid_method import solve_trapezoid


class Solver:
    def __init__(self, argset : ArgSet):
        self.argset = argset

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
        except TypeError as e:
            print("The value of the integral function cannot be determined")
            exit(1)
        except NameError as e:
            print("Error occured while parsing the integral function, check that the functions used are written correctly")
            return