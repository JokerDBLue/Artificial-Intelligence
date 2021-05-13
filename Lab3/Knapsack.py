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


def make_it_valid(objects, solution, max_capacity):
    """
    Transformat o solutie nevalida intr-o solutie valida
    :param objects: lista de obiecte cu valorile sale
    :param solution:
    :param max_capacity:
    :return:
    """
    length = len(solution)
    repaired_solution = solution[:]
    i = 0
    while i < length:
        if repaired_solution[i] == 1:
            repaired_solution[i] = 0
        if is_valid(objects, repaired_solution, max_capacity):
            break
        i += 1
    return repaired_solution
