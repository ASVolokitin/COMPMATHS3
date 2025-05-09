from entities.ArgumentParser import ArgumentParser
from entities.Solver import Solver
from utils import print_result, save_result

if __name__ == '__main__':
    parser = ArgumentParser()
    args = parser.get_arguments()
    if args is None: exit(1)
    solver = Solver(args)
    solution = solver.solve()
    print_result(solution)
    save_result(args.output_file, solution)

