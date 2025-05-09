import argparse
import sympy as sp

from entities.ArgSet import ArgSet
from entities.SolvingMethod import SolvingMethod
from utils import sympify_func, uni_float, MAX_NUMBER_OF_PARTITIONS, MAX_PRECISION, parse_func, check_singularities, lambdify_func


class ArgumentParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog="cm3", description="And here's the third one")
        self.subparsers = self.parser.add_subparsers(dest="solving_method", required=True, title="Solving Method", description="Methods of solving integrals")
        self.rect_parser = self.subparsers.add_parser("rect", help="Rectangular (right, left or middle) method")
        self.trap_parser = self.subparsers.add_parser("trap", help="Trapezoidal method")
        self.simp_parser = self.subparsers.add_parser("simp", help="Simpson method")
        self.setup_subparsers()

    def setup_subparsers(self):
        self.setup_rect_arguments()
        self.setup_trap_arguments()
        self.setup_simp_arguments()
        # self.setup_basic_subparser(self.rect_parser)
        # self.setup_basic_subparser(self.trap_parser)
        # self.setup_basic_subparser(self.simp_parser)

    def setup_basic_subparser(self, subparser):
        subparser.add_argument("--func",
                               required=True,
                               metavar="FUNC",
                               help="Specify the integrand function")
        subparser.add_argument("--ll",
                               required=True,
                               type=uni_float,
                               metavar="LOWER-LIMIT",
                               help="Specify the lower limit of integration")
        subparser.add_argument("--ul",
                               required=True,
                               metavar="UPPER-LIMIT",
                               type=uni_float,
                               help="Specify the upper limit of integration")
        subparser.add_argument("--npart",
                               required=True,
                               metavar="NUMBER-OF-PARTITIONS",
                               type=int,
                               help="Specify the initial number of partition segments to calculate the integral")
        subparser.add_argument("--pr",
                               required=True,
                               metavar="PRECISION",
                               type=int,
                               help="Specify the accuracy of the integral calculation (number of decimal places)")
        subparser.add_argument("--of",
                               required=False,
                               metavar="OUTPUT-FILE",
                               help="(optional) Specify the name of the output file if needed")


    def setup_rect_arguments(self):
        self.rect_parser.add_argument("--recmet",
                                      required=True,
                                      metavar="RECT-METHOD",
                                      choices=["left", "right", "middle"],
                                      help="Specify the method for calculating the integral (right, left, middle)")
        self.setup_basic_subparser(self.rect_parser)

    def setup_trap_arguments(self):
        self.setup_basic_subparser(self.trap_parser)


    def setup_simp_arguments(self):
        self.setup_basic_subparser(self.simp_parser)

    def validate_arguments(self, args):
        res = self.validate_function(args)
        res = self.validate_borders(args) and res
        res = self.validate_precision(args) and res
        res = self.validate_partitions(args) and res

        return res

    def validate_function(self, args):
        try:
            args.func_text = args.func.replace("^", "**")
            singularities = check_singularities(sympify_func(args.func))
            for singularity in singularities:
                if args.ll <= singularity <= args.ul:
                    self.parser.error(f"The integral function has a singularity on the integration segment (x = {singularity}). Integral diverges")
            args.func = parse_func(args.func)
            if args.func is None:
                print("Error occured while parsing function")
                return False
            if args.func.has(sp.zoo):
                self.parser.error("The integral function is not defined over the entire interval")
            args.func = lambdify_func(args.func)
        except TypeError as e:
            self.parser.error(str(e))

    def validate_borders(self, args):
        if args.ll >= args.ul:
            self.parser.error("The lower limit should be smaller than the upper one")

    def validate_precision(self, args):
        if args.pr <= 0:
            self.parser.error("Precision must be positive")
        if args.pr > MAX_PRECISION:
            self.parser.error(f"The selected accuracy is too high, the maximum allowed value is {MAX_PRECISION}")

    def validate_partitions(self, args):
        if args.npart <= 0:
            self.parser.error("Number of partitions must be positive")
        if args.npart > MAX_NUMBER_OF_PARTITIONS:
            self.parser.error("Number of partitions is too big")

    def get_method(self, args):
        method = None
        if args.solving_method == "rect":
            if args.recmet == "left":
                method = SolvingMethod.RECT_LEFT
            elif args.recmet == "right":
                method = SolvingMethod.RECT_RIGHT
            elif args.recmet == "middle":
                method = SolvingMethod.RECT_MIDDLE
        elif args.solving_method == "trap":
            method = SolvingMethod.TRAP
        elif args.solving_method == "simp":
            method = SolvingMethod.SIMP

        return method

    def get_arguments(self):
        args = self.parser.parse_args()
        if self.validate_arguments(args) == False:
            print("Erorr occured while validating arguments")
            return
        method = self.get_method(args)
        if method is not None: return ArgSet(method, args)
        else: self.parser.error("Solving method is not set properly")
