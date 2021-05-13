import numpy as np


def get_mean(elements: list):
    return np.mean(elements)


def is_valid(objects, sol, max_capacity):
    """
        Verifica validitatea unei solutii
    """
    weight = 0
    i = 0
    while i < len(sol) and weight <= max_capacity:
        weight += objects[i][1] * sol[i]
        i += 1
    return weight <= max_capacity


def generate_solution(n: int):
    """
        Genereaza o solutie aleatoare
    """
    return list(np.random.randint(2, size=n))


def generate_valid_solution(n: int, objects, max_capacity):
    stop = False
    sol = []
    while not stop:
        sol = generate_solution(n)
        if is_valid(objects, sol, max_capacity):
            stop = True
    return sol


def generate_k_solutions(n: int, k: int, objects, max_capacity):
    solution_list = []
    while k > 0:
        sol = generate_valid_solution(n, objects, max_capacity)
        solution_list.append(sol)
        k -= 1
    return solution_list


def fitness(objects, sol, max_capacity):
    value = 0
    if is_valid(objects, sol, max_capacity):
        for i in range(len(sol)):
            value += objects[i][0] * sol[i]
    else:
        value = -1
    return value


def get_weight(objects, solution):
    weight = 0
    for i in range(len(solution)):
        weight += objects[i][1] * solution[i]
    return weight


def best_solution(objects, solutions, max_capacity):
    best = []
    value = 0
    weight = 0
    for i in range(len(solutions)):
        new_value = fitness(objects, solutions[i], max_capacity)
        if new_value > value:
            value = new_value
            weight = get_weight(objects, solutions[i])
            best = solutions[i][:]
    return best, value, weight


def random_neighbor(sol):
    x = sol[:]
    index = np.random.randint(len(sol))
    if x[index] == 0:
        x[index] = 1
    else:
        x[index] = 0
    return x


def random_hill_climbing(k: int, restart: int, objects: list, max_capacity: int):
    found_solutions = []
    while k > 0:
        c = generate_valid_solution(len(objects), objects, max_capacity)
        p = restart
        while p > 0 and k > 0:
            x = random_neighbor(c)
            if fitness(objects, x, max_capacity) > fitness(objects, c, max_capacity):
                c = x[:]
                p = restart
            else:
                p -= 1
            k -= 1
        found_solutions.append(list(c))
    return best_solution(objects, found_solutions, max_capacity)
