import math


def time_based_sinus(minute, lower, upper, multiplier=6):
    delta = upper - lower
    middle = lower + delta / 2

    return round(middle + math.sin(math.radians(minute * multiplier)) * (delta / 2), 2)
