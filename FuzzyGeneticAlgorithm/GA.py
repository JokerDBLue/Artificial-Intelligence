import time
import Knapsack as ks
import numpy as np
import random
from FuzzyController import FuzzyController


def initialize_pop(n: int, p: list, w: list, c: list, m: int):
    pop = []
    for i in range(100):
        pop.append(ks.generate_solution(p, w, c, m, n))
    return pop


def hamming_distance(solution1: list, solution2: list, n: int):
    p = [1 for i in range(n) if solution1[i] == solution2[i]]
    hd = sum(p)
    return hd


def sexual_selection(pop: list, p: list, w: list, c: list, g: int, m, n):
    m_pop = [pop[i] for i in range(g % 2, 100, 2)]
    f_pop = [pop[i] for i in range(1 - (g % 2), 100, 2)]
    '''Alegerea primului parinte'''
    k = int(np.random.default_rng().choice(range(1, len(f_pop)), size=1, replace=False))
    sample = np.random.default_rng().choice(len(f_pop), size=k, replace=False)
    possible_parents = [f_pop[s] for s in sample]
    parent = sorted(possible_parents, key=lambda x: ks.fitness(x, p, w, c, m, n), reverse=True)
    parent1 = parent[0][:]
    '''Sfarsit pentru alegerea primului parinte'''

    '''Alegerea celui de al doilea parinte'''
    # Alegerea unui numar k de candidati
    k = int(np.random.default_rng().choice(range(1, len(m_pop)), size=1, replace=False))
    sample = np.random.default_rng().choice(len(m_pop), size=k, replace=False)
    possible_parents = [m_pop[s] for s in sample]
    # Cautarea celor mai potriviti candidati dintre cei k initiali
    hds = [hamming_distance(parent1, possible_parents[i], n) for i in range(k)]
    max_value = max(hds)
    indices = [index for index, value in enumerate(hds) if value == max_value]
    # In cazul in care se gasesc mai multe optiuni se va calcula si fitness-ul
    if len(indices) > 1:
        fs = [ks.fitness(possible_parents[i], p, w, c, m, n) for i in indices]
        possible_parents = [possible_parents[i] for i in indices]
        max_value = max(fs)
        indices = [index for index, value in enumerate(fs) if value == max_value]
        if len(indices) > 1:
            indices = [random.choice(indices)]
    parent2 = possible_parents[indices[0]][:]
    '''Sfarsit pentru alegerea celui de al doilea parinte'''
    return parent1, parent2


'''
Incrucisari
'''


def single_point(parent1: list, parent2: list, problem_size: int):
    c_point = np.random.randint(1, problem_size - 1)
    child1 = parent1[:c_point] + parent2[c_point:]
    child2 = parent2[:c_point] + parent1[c_point:]
    return child1, child2


def k_point(parent1: list, parent2: list, problem_size: int, k=None):
    options = range(1, problem_size - 1)
    if k is None:
        k = int(np.random.default_rng().choice(range(3, problem_size - 1), size=1, replace=False))
    sample = np.random.default_rng().choice(options, size=k, replace=False)
    sample = sorted(sample, reverse=False)
    child1 = parent1[:]
    child2 = parent2[:]
    for i in range(1, len(sample), 2):
        child1[sample[i - 1]:sample[i]] = parent2[sample[i - 1]:sample[i]]
        child1[sample[i - 1]:sample[i]] = parent1[sample[i - 1]:sample[i]]
    return child1, child2


def uniform(parent1: list, parent2: list, problem_size: int):
    mask1 = list(np.random.randint(2, size=problem_size))
    mask2 = list(np.random.randint(2, size=problem_size))
    child1 = parent1[:]
    child2 = parent2[:]
    for i in range(problem_size):
        if mask1[i] != child1[i]:
            child1[i] = mask1[i]
        if mask2[i] != child2[i]:
            child2[i] = mask2[i]
    return child1, child2


def segregation(parent1: list, parent2: list, problem_size: int):
    options = range(1, problem_size - 1)
    sample1 = np.random.default_rng().choice(options, size=2, replace=False)
    sample2 = np.random.default_rng().choice(options, size=2, replace=False)
    sample1 = sorted(sample1, reverse=False)
    sample2 = sorted(sample2, reverse=False)
    child1 = parent1[:]
    child2 = parent2[:]
    child1[sample1[0]:sample1[1]] = parent2[sample1[0]:sample1[1]]
    child1[sample2[0]:sample2[1]] = parent1[sample2[0]:sample2[1]]
    return child1, child2


def inversion(parent1: list, parent2: list, problem_size: int):
    options = range(1, problem_size - 1)
    sample1 = np.random.default_rng().choice(options, size=2, replace=False)
    sample2 = np.random.default_rng().choice(options, size=2, replace=False)
    sample1 = sorted(sample1, reverse=False)
    sample2 = sorted(sample2, reverse=False)
    child1 = parent1[:]
    child2 = parent2[:]
    child1[sample1[0]:sample1[1]] = reversed(parent2[sample1[0]:sample1[1]])
    child1[sample2[0]:sample2[1]] = reversed(parent1[sample2[0]:sample2[1]])
    return child1, child2


def crossover(n: int, m: int, pop: list, crossover_count: int, p: list, w: list, c: list, g: int, op_c="single-point"):
    children = []
    for i in range(crossover_count):
        parent1, parent2 = sexual_selection(pop, p, w, c, g, m, n)
        child1, child2 = parent1, parent2
        if op_c == "single-point":
            child1, child2 = single_point(parent1, parent2, n)
        elif op_c == "2-point":
            child1, child2 = k_point(parent1, parent2, n, 2)
        elif op_c == "k-point":
            k = random.choice(range(1, n // 2))
            child1, child2 = k_point(parent1, parent2, n, k)
        elif op_c == "segregation":
            child1, child2 = segregation(parent1, parent2, n)
        else:
            child1, child2 = inversion(parent1, parent2, n)
        children.append(child1)
        children.append(child2)
    return children


'''
Mutatii
'''


def binary_m(mutant: list, problem_size: int):
    for i in range(problem_size):
        mutant[i] = 1 - mutant[i]
    return mutant


def interchanging(mutant: list, problem_size: int):
    options = range(1, problem_size - 1)
    sample = np.random.default_rng().choice(options, size=2, replace=False)
    mutant[sample[0]], mutant[sample[1]] = mutant[sample[1]], mutant[sample[0]]
    return mutant


def revers(mutant: list, problem_size: int):
    options = range(1, problem_size - 2)
    sample = int(np.random.default_rng().choice(options, size=1, replace=False))
    mutant[sample + 1], mutant[sample - 1] = mutant[sample - 1], mutant[sample + 1]
    return mutant


def parity(mutant: list, problem_size: int):
    for i in range(1, problem_size):
        if mutant[i] + mutant[i - 1] > 1:
            mutant[i] = 0
        else:
            mutant[i] = mutant[i] + mutant[i - 1]
    return mutant


def mutation(children: list, n: int, pm: float, op_m="binary_m"):
    mutants = []
    for c in children:
        mutant_child = c[:]
        if np.random.random() < pm:
            if op_m == "interchanging":
                mutant_child = interchanging(mutant_child, n)
            elif op_m == "revers":
                mutant_child = revers(mutant_child, n)
            elif op_m == "binary_m":
                mutant_child = binary_m(mutant_child, n)
            else:
                mutant_child = parity(mutant_child, n)
        mutants.append(mutant_child)
    return mutants


'''
Generatia urmatoare
'''


def nex_generation(mutants: list, old_pop: list, p: list, w: list, c: list, m: int, n: int, g=0):
    rm = mutants[:]
    for i in range(len(mutants)):
        if not ks.is_valid(mutants[i], w, c, m, n):
            rm[i] = ks.make_valid(rm[i], w, c, m, n)
    new_pop = old_pop + rm[:]
    new_pop = sorted(new_pop, key=lambda x: ks.fitness(x, p, w, c, m, n), reverse=True)
    new_pop = new_pop[:100]
    new_pop_set = set(tuple(x) for x in new_pop)
    if len(new_pop_set) <= 90 * len(new_pop) / 100 and g % 10 == 0:
        for i in range(1, len(new_pop) - 1):
            if new_pop[i] == new_pop[i - 1] or new_pop[i] == new_pop[i + 1]:
                new_pop[i] = ks.generate_solution(p, w, c, m, n)
    return new_pop


def evaluate_pop(pop: list, n: int, p: list, w: list, c: list, m: int):
    fs = [ks.fitness(pop[i], p, w, c, m, n) for i in range(100)]
    return max(fs), min(fs), np.average(fs)


'''
Versiune proprie pt algoritm
'''


def ga(n: int, p: list, w: list, c: list, m: int):
    pc = 70
    pm = 1 / n
    pop = initialize_pop(n, p, w, c, m)
    best, worst, avg = evaluate_pop(pop, n, p, w, c, m)
    g = 0
    last_improvement = g  # generatia in care a avut loc ultima imbunatatire pentru fitness-ul maxim
    max_generations = 10**6  # numarul maxim de generatii
    crossover_count = int((100 * pc / 100) // 2)
    t = time.time()

    while (g - last_improvement < 100) and (g < max_generations) and (time.time() - t <= 250):
        children = crossover(n, m, pop, crossover_count, p, w, c, g)
        mutants = mutation(children, n, pm)
        pop = nex_generation(mutants, pop, p, w, c, m, n).copy()
        new_best, worst, avg = evaluate_pop(pop, n, p, w, c, m)
        if new_best > best:
            last_improvement = g
            best = new_best
        # print(g - last_improvement, " ", g, " ", time.time() - t, " ", best)
        g += 1

    return best


'''
Article version forthe algorithm |
                                 |
                                 V
'''


def fuzzy_side(n: int, p: list, w: list, c: list, m: int, best: float, worst: float, avg: float, pop: list,
               fc: FuzzyController):
    fs = set([ks.fitness(pop[i], p, w, c, m, n) for i in range(100)])
    pop_size = 100
    '''Determinarea T1, T2, T3'''
    t1 = len(fs) / pop_size
    t2 = (best - avg) / best
    sorted_pop = sorted(pop, key=lambda x: ks.fitness(x, p, w, c, m, n), reverse=True)
    best_sol = sorted_pop[0]
    worst_sol = sorted_pop[-1]
    t3 = hamming_distance(best_sol, worst_sol, n) / n
    rc, pc, rm, pm = fc.apply_rules(t1, t2, t3)
    if rc == "low":
        op_c = "2-point"
    elif rc == "medium":
        op_c = random.choice(["k-point", "uniform"])
    else:
        op_c = random.choice(["segregation", "inversion"])

    if rm == "low":
        op_m = random.choice(["interchanging", "revers"])
    elif rc == "medium":
        op_m = "binary_m"
    else:
        op_m = "parity"

    return op_c, pc, op_m, pm


def fga(n: int, p: list, w: list, c: list, m: int):
    pop = initialize_pop(n, p, w, c, m)
    best, worst, avg = evaluate_pop(pop, n, p, w, c, m)
    g = 0
    last_improvement = g
    max_generations = 10 ** 6  # numarul maxim de generatii
    t = time.time()
    fc = FuzzyController(n)
    while (g - last_improvement < 100) and (g < max_generations) and (time.time() - t <= 250):
        op_c, pc, op_m, pm = fuzzy_side(n, p, w, c, m, best, worst, avg, pop, fc)
        # print(op_c, " ", op_m)
        crossover_count = int((100 * pc) // 2)
        children = crossover(n, m, pop, crossover_count, p, w, c, g, op_c)
        mutants = mutation(children, n, pm, op_m)
        pop = nex_generation(mutants, pop, p, w, c, m, n, g).copy()
        new_best, worst, avg = evaluate_pop(pop, n, p, w, c, m)
        if new_best > best:
            last_improvement = g
            best = new_best
        g += 1
    return best
