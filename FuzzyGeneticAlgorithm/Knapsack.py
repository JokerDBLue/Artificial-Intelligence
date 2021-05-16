import numpy as np


def generate_knapsack(m: int, n: int, a: float):
    w = []
    c = []
    p = []
    # generare greutati si capacitati maxime
    for i in range(m):
        w.append(list(np.random.uniform(0, 1000, n)))
        capacity = a * sum(w[i])
        c.append(capacity)
    # generarea valorilor pentru produse
    for j in range(n):
        e = float(np.random.uniform(0, 1))
        value = sum([w[i][j] for i in range(m)]) / m + 500 * e
        p.append(value)
    return w, c, p


def make_valid(x: list, w: list, c: list, m: int, n: int):
    r = []
    for i in range(m):
        r.append(sum([w[i][j] * x[j] for j in range(n)]))
    for j in range(n - 1, -1, -1):
        if x[j] == 1 and np.any([r[i] > c[i] for i in range(m)]):
            x[j] = 0
            for i in range(m):
                r[i] = r[i] - w[i][j]
    for j in range(n):
        if x[j] == 0 and np.all([r[i] + w[i][j] <= c[i] for i in range(m)]):
            x[j] = 1
            for i in range(m):
                r[i] = r[i] + w[i][j]
    return x[:]


def is_valid(x: list, w: list, c: list, m: int, n: int):
    for i in range(m):
        if sum([w[i][j] * x[j] for j in range(n)]) > c[i]:
            return False
    return True


def generate_solution(p: list, w: list, c: list, m: int, n: int):
    """
    Genereaza o solutie aleatoare
    """
    x = list(np.random.randint(2, size=n))
    if not is_valid(x, w, c, m, n):
        x = make_valid(x, w, c, m, n)
    return x


def fitness(x: list, p: list, w: list, c: list, m: int, n: int):
    if is_valid(x, w, c, m, n):
        return sum([p[j] * x[j] for j in range(n)])
    else:
        return -1
