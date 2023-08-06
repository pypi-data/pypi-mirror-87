from decimal import Decimal, ROUND_HALF_UP


def round(f):
    return Decimal(f'{f}').quantize(0, ROUND_HALF_UP).__int__()
