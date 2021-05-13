import numpy as np


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


def best_non_tabu_neighbor(c, memory, objects, max_capacity):
    best_x = c[:]
    non_tabu = False
    index = -1
    for i in range(len(memory)):
        if memory[i] == 0 and not non_tabu:
            best_x[i] = 1 - best_x[i]
            index = i
            non_tabu = True
        elif memory[i] == 0 and non_tabu:
            x = c[:]
            x[i] = 1 - x[i]
            if fitness(objects, x, max_capacity) > fitness(objects, best_x, max_capacity):
                best_x = x[:]
                index = i
    return best_x, index


def update_memory(memory, index, p):
    for i in range(len(memory)):
        if i == index:
            memory[i] = p
        elif memory[i] > 0:
            memory[i] -= 1
    return memory


def tabu_search(k, p, objects, max_capacity):
    c = generate_valid_solution(len(objects), objects, max_capacity)
    memory = [0] * len(objects)
    best = c[:]
    while k > 0:
        x, index = best_non_tabu_neighbor(c, memory, objects, max_capacity)
        c = x[:]
        memory = update_memory(memory, index, p)
        if fitness(objects, c, max_capacity) > fitness(objects, best, max_capacity):
            best = c[:]
        k -= 1

    return best, fitness(objects, best, max_capacity), get_weight(objects, best)
