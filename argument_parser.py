import argparse

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
        self.setup_basic_subparser(self.trap_parser)
        self.setup_basic_subparser(self.simp_parser)

    def setup_basic_subparser(self, subparser):
        subparser.add_argument("func",
                               metavar="FUNC",
                               choices=["1", "2", "3", "4", "5"],
                               help="Specify the integrand function")
        subparser.add_argument("lower_limit",
                               type=self.uni_float,
                               metavar="LOWER-LIMIT",
                               help="Specify the lower limit of integration")
        subparser.add_argument("upper_limit",
                               metavar="UPPER-LIMIT",
                               type=self.uni_float,
                               help="Specify the upper limit of integration")
        subparser.add_argument("precision",
                               metavar="PRECISION",
                               type=self.uni_float,
                               help="Specify the accuracy of the integral calculation")
        subparser.add_argument("number_of_partitions",
                               metavar="NUMBER-OF-PARTITIONS",
                               type=int,
                               help="Specify the initial number of partition segments to calculate the integral")

    def setup_rect_arguments(self):
        self.rect_parser.add_argument("method",
                                      metavar="METHOD",
                                      choices=["1", "2", "3"],
                                      help="""Specify the method for calculating the integral:
                                         1 - left,
                                         2 - right,
                                         3 - middle""")
        self.setup_basic_subparser(self.rect_parser)

    def uni_float(self, value):
        try:
            return float(value.replace(',', '.'))
        except ValueError:
            return argparse.ArgumentTypeError(' is not a float' % value)

    def validate_arguments(self, args):
        self.validate_borders(args)
        self.validate_precision(args)
        self.validate_partitions(args)

    def validate_borders(self, args):
        if args.lower_limit >= args.upper_limit:
            self.parser.error("The lower limit should be smaller than the upper one")

    def validate_precision(self, args):
        if args.precision < 0 or args.precision > 1:
            self.parser.error("Precision must be between 0 and 1")

    def validate_partitions(self, args):
        if args.number_of_partitions < 0:
            self.parser.error("Number of partitions must be positive")

    def get_arguments(self):
        args = self.parser.parse_args()
        self.validate_arguments(args)
        return args

