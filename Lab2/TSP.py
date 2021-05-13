import numpy as np


def distance_matrix(locations: list):
    length = len(locations)
    dm = np.zeros([length, length], dtype=int)
    for i in range(length):
        for j in range(i + 1, length):
            xd = locations[i][1] - locations[j][1]
            yd = locations[i][2] - locations[j][2]
            dm[i][j] = int(round(np.sqrt(xd * xd + yd * yd)))
            dm[j][i] = dm[i][j]
    return dm


def rdm_solution(dimension: int):
    return list(np.random.permutation(dimension))


def fitness_TSP(solution: list, dm):
    distance = 0
    for i in range(len(solution)):
        if i != len(solution) - 1:
            distance += dm[solution[i]][solution[i + 1]]
        else:
            distance += dm[solution[i]][solution[0]]
    return distance


def two_opt(solution: list, i: int, j: int):
    x = solution.copy()
    index = 0
    while i + index < j - index:
        x[i + index], x[j - index] = x[j - index], x[i + index]
        index += 1
    return x


def neighbor(solution: list, dimension: int):
    sample = np.random.default_rng().choice(dimension, size=2, replace=False)
    if sample[0] > sample[1]:
        sample[0], sample[1] = sample[1], sample[0]
    x = two_opt(solution, sample[0], sample[1])
    return x


def simulated_annealing(t: float, alpha: float, t_min: float, max_iterations: int, dm, dimension: int):
    c = rdm_solution(dimension)
    distances = [fitness_TSP(c, dm)]
    while t > t_min:
        k = 0
        while k < max_iterations:
            x = neighbor(c, dimension)
            delta = fitness_TSP(x, dm) - fitness_TSP(c, dm)
            if delta < 0:
                c = x[:]
                distances.append(fitness_TSP(c, dm))
            elif np.random.random() < np.exp(-delta/t):
                c = x[:]
                distances.append(fitness_TSP(c, dm))
            k += 1
        t = alpha * t
    return c, fitness_TSP(c, dm), distances
