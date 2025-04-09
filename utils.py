import argparse
from decimal import Decimal


def uni_float(value):
    try:
        return Decimal(value.replace(',', '.'))
    except ValueError:
        return argparse.ArgumentTypeError(' is not a float' % value)