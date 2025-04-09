class ArgSet:
    def __init__(self, method, args):
        self.method = method
        self.func = args.func
        # self.func = lambda x: x*x + 2 * x
        self.lower_limit = args.ll
        self.upper_limit = args.ul
        self.precision = args.pr
        self.number_of_partitions = args.npart