import argparse

from argument_parser import ArgumentParser

if __name__ == '__main__':
    parser = ArgumentParser()
    args = parser.get_arguments()
    print(args.solving_method)
