class ArgSet:
    def __init__(self, method, args):
        self.method = method
        self.func = args.func
        self.lower_limit = args.lower_limit
        self.upper_limit = args.upper_limit
        self.precision = args.precision
        self.number_of_partitions = args.number_of_partitions