import numpy as np
import random

UPPER_BOUND = 500
LOWER_BOUND = -500


def schwefel(n, x):
    f = 0
    for i in range(n):
        f += x[i] * np.sin(np.sqrt(abs(x[i])))
    return -f


def in_bounds(xi):
    return LOWER_BOUND <= xi <= UPPER_BOUND


def generate_solution(n, x_min=LOWER_BOUND, x_max=UPPER_BOUND):
    x = []
    for i in range(n):
        x.append(random.uniform(x_min, x_max))
    return x
