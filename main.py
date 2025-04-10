# добавить в print result описание функции

from entities.ArgumentParser import ArgumentParser
from entities.Solver import Solver
from utils import print_result

if __name__ == '__main__':
    parser = ArgumentParser()
    args = parser.get_arguments()
    solver = Solver(args)
    print_result(solver.solve())

