import random

import numpy as np
import SchwefelFunction as sf


def generate_rnd_population(problem_size: int, population_size: int):
    """
    Returneaza o populatie de marime population_size pentru problema problem_type de marime problem_size
    :param population_size: marimea populatioe
    :param problem_size: marimea pentru solutia problemei
    :return population: populatia noua pentru problema specificata
    """
    population = []
    for i in range(population_size):
        population.append(sf.generate_solution(problem_size))
    return population


def new_population(problem_size: int, old_population: list, mutated_children: list):
    """
    Genereaza o populatie noua dupa urmatoarele reguli:
    -se pastreaza doar solutiile cele mai bune
    :param problem_size:
    :param old_population: populatia precedenta
    :param mutated_children: copiii obtinuti dupa mutatie
    :return population: noua popullatie obtinuta
    """
    mc = mutated_children[:]
    population = old_population + mc
    population = sorted(population, key=lambda x: sf.schwefel(problem_size, x), reverse=False)
    return population[:len(old_population)]


def evaluate_population(problem_size: int, population: list, population_size: int):
    """
    Evaluarea populatiei pentru a obtine best, average si worst
    :param problem_size:
    :param population: populatia evaluata
    :param population_size: marimea populatiei
    :return best: cel mai bun fitness din populatie
    :return avg: valoare medie pentru fitness-ul populatie
    :return worst: cel mai slab fitness din populatie
    """
    best, avg, worst = 0, 0, 0
    eval_population = sorted(population, key=lambda x: sf.schwefel(problem_size, x), reverse=False)
    best = sf.schwefel(problem_size, eval_population[0])
    for i in range(population_size):
        avg += sf.schwefel(problem_size, eval_population[i])
    avg /= population_size
    worst = sf.schwefel(problem_size, eval_population[-1])
    return best, avg, worst


'''Selection functions'''


def turnir_selection(problem_size: int, population: list, population_size: int, turnir_size: int):
    parent1, parent2 = [], []
    p = population[:]  # copie a populatiei initiale
    for i in range(2):
        sample = list(np.random.default_rng().choice(population_size, size=turnir_size, replace=False))
        possible_parents = [p[s] for s in sample]
        sorted(sample, reverse=False)
        l = len(sample)
        for j in range(l):
            del p[sample[j] - j]
        population_size -= l
        parent = sorted(possible_parents, key=lambda x: sf.schwefel(problem_size, x), reverse=False)
        if i == 0:
            parent1 = parent[0]
        else:
            parent2 = parent[0]
    return parent1, parent2


def rank_selection(problem_size: int, population: list, population_size: int, s: float):
    parent1, parent2 = [], []
    p = population[:]  # copie a populatiei initiale
    for i in range(2):
        p = sorted(p, key=lambda x: sf.schwefel(problem_size, x), reverse=True)
        parent = p[0][:]
        for j in range(population_size):
            prob_i = ((2 - s) / population_size) + (2 * j * (s - 1)) / (population_size - 1)
            if np.random.random() < prob_i:
                parent = p[j][:]
                del p[j]
                break
        population_size -= 1
        if i == 0:
            parent1 = parent
        else:
            parent2 = parent
    return parent1, parent2


'''Crossover functions'''

'''Numeric'''


def numeric_crossover(problem_size: int, population_size: int, population: list, crossover_count: int, operator: str,
                      selection_operator: str, s, p: float):
    children = []
    for i in range(crossover_count):
        if selection_operator == "turnir":
            parent1, parent2 = turnir_selection(problem_size, population, population_size, s)
        else:
            parent1, parent2 = rank_selection(problem_size, population, population_size, s)
        child1, child2 = parent1[:], parent2[:]
        if operator == "avg":
            for j in range(problem_size):
                if np.random.random() < p:
                    m = (parent1[j] + parent2[j]) / 2
                    child1[j], child2[j] = m, m
        elif operator == "discreet":
            for j in range(problem_size):
                if np.random.random() < p:
                    child1[j] = parent2[j]
                    child2[j] = parent1[j]
        children.append(child1)
        children.append(child2)
    return children


'''Mutation functions'''

'''Numeric'''


def numeric_mutation(children: list, problem_size: int, mutation_rate: float, operator: str, p: int, r: float, t: int,
                     t_max: int):
    mutants = []
    for c in children:
        x = c[:]
        for i in range(problem_size):
            if np.random.random() < mutation_rate:
                if operator == "uniform":
                    x[i] = random.uniform(-500, 500)  # Bit flip
                elif operator == "nonuniform":
                    if p == 1:
                        x[i] = x[i] + (500 - x[i])*(1 - r**(1 - t / t_max))
                    elif p == -1:
                        x[i] = x[i] - (x[i] - (-500)) * (1 - r ** (1 - t / t_max))
        mutants.append(x)
    return mutants


'''Evolutionary algorithm'''


def evolutionary_algorithm(problem_size: int, population_size: int, mutation_rate: float, crossover_rate: float,
                           generations: int, crossover_operator: str, mutation_operator: str, selection_operator: str,
                           s, p: float):
    population = generate_rnd_population(problem_size, population_size)
    b, a, w = evaluate_population(problem_size, population, population_size)
    best = [b]
    avg = [a]
    worst = [w]
    crossover_count = int((population_size * crossover_rate / 100) // 2)
    direction = 0  # pentru mutatia neuniforma
    r = 0.0  # pentru mutatia neuniforma
    for i in range(generations):
        if mutation_operator == "nonuniform":
            direction = random.choice([-1, 1])
            r = random.uniform(0, 1)
        children = numeric_crossover(problem_size, population_size, population, crossover_count, crossover_operator,
                                     selection_operator, s, p)
        mutants = numeric_mutation(children, problem_size, mutation_rate, mutation_operator, direction, r, i, generations)
        population = new_population(problem_size, population, mutants)
        b, a, w = evaluate_population(problem_size, population, population_size)
        best.append(b)
        avg.append(a)
        worst.append(w)
    return best, avg, worst
