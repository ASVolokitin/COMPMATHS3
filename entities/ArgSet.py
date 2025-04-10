class ArgSet:
    def __init__(self, method, args):
        self.method = method
        self.func = args.func
        self.func_text = args.func_text
        self.lower_limit = args.ll
        self.upper_limit = args.ul
        self.precision = args.pr
        self.number_of_partitions = args.npart

    def get_fx(self, x):
        try:
            return self.func(x)
        except ValueError:
            print(f"Couldn't calculate the value of the function at point x = {x}")
            exit(1)
        except ZeroDivisionError:
            print(f"Couldn't calculate the value of the function at point x = {x} (zero division)")
            exit(1)