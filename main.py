# добавить обработку запятых

from entities.ArgumentParser import ArgumentParser
from entities.Solver import Solver

if __name__ == '__main__':
    parser = ArgumentParser()
    args = parser.get_arguments()
    solver = Solver(args)
    print(solver.solve())
