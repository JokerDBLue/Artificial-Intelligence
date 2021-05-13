import numpy as np

import TSP
import Knapsack


def generate_rnd_population(problem_type: str, problem_size: int, population_size: int, evaluator):
    """
    Returneaza o populatie de marime population_size pentru problema problem_type de marime problem_size
    :param population_size: marimea populatioe
    :param problem_size: marimea pentru solutia problemei
    :param problem_type: poate avea valorile "knapsack" sau "tsp"
    :param evaluator: doar pentru problema rucsacului
    :return population: populatia noua pentru problema specificata
    """
    population = []
    for i in range(population_size):
        if problem_type == "tsp":
            population.append(TSP.rdm_solution(problem_size))
        elif problem_type == "knapsack":
            population.append(Knapsack.generate_valid_solution(problem_size, evaluator[0], evaluator[1]))
    return population


def new_population(problem_type: str, old_population: list, mutated_children: list, evaluator):
    """
    Genereaza o populatie noua dupa urmatoarele reguli:
    -se pastreaza toti copiii obtinuti dupa mutatii(acestia se repara in cazul problemei de tip knapsack)
    -locurile libere din populatie se vor umple cu parintii ramasi
    :param problem_type: poate avea valorile "knapsack" sau "tsp"
    :param old_population: populatia precedenta
    :param mutated_children: copiii obtinuti dupa mutatie
    :param evaluator: in cazul unei probleme de tip Kanpsack va avea contine o lista de obiecte si capacitatea maxima
                    in cazul uneil probleme de tip TSP va contine matricea de distante
    :return population: noua popullatie obtinuta
    """
    population = []
    mc = mutated_children[:]
    if problem_type == "knapsack":
        for i in range(len(mc)):
            if not Knapsack.is_valid(evaluator[0], mc[i], evaluator[1]):
                mc[i] = Knapsack.make_it_valid(evaluator[0], mc[i], evaluator[1])
        population = old_population + mc
        population = sorted(population, key=lambda x: Knapsack.fitness(evaluator[0], x, evaluator[1]), reverse=True)
    elif problem_type == "tsp":
        population = old_population + mc
        population = sorted(population, key=lambda x: TSP.fitness_TSP(x, evaluator), reverse=False)
    population = population[:len(old_population)]
    return population


def evaluate_population(problem_type: str, population: list, population_size: int, evaluator):
    """
    Evaluarea populatiei pentru a obtine best, average si worst
    :param problem_type: poate avea valorile "knapsack" sau "tsp"
    :param population: populatia evaluata
    :param population_size: marimea populatiei
    :param evaluator: in cazul unei probleme de tip Kanpsack va avea contine o lista de obiecte si capacitatea maxima
                    in cazul uneil probleme de tip TSP va contine matricea de distante
    :return best: cel mai bun fitness din populatie
    :return avg: valoare medie pentru fitness-ul populatie
    :return worst: cel mai slab fitness din populatie
    """
    best, avg, worst = 0, 0, 0
    if problem_type == "knapsack":
        eval_population = sorted(population, key=lambda x: Knapsack.fitness(evaluator[0], x, evaluator[1]), reverse=True)
        best = Knapsack.fitness(evaluator[0], eval_population[0], evaluator[1])
        for i in range(population_size):
            avg += Knapsack.fitness(evaluator[0], eval_population[i], evaluator[1])
        avg /= population_size
        worst = Knapsack.fitness(evaluator[0], eval_population[-1], evaluator[1])
    elif problem_type == "tsp":
        eval_population = sorted(population, key=lambda x: TSP.fitness_TSP(x, evaluator), reverse=False)
        best = TSP.fitness_TSP(eval_population[0], evaluator)
        for i in range(population_size):
            avg += TSP.fitness_TSP(eval_population[i], evaluator)
        avg /= population_size
        worst = TSP.fitness_TSP(eval_population[-1], evaluator)
    return best, avg, worst


'''Selection functions'''


def selection(problem_type: str, population: list, population_size: int, evaluator):
    """
    Aici se selecteaza un parinte din populatia initiala. Se foloseste selectia turnir de marime 5.
    :param population_size: marimea populatiei
    :param problem_type: poate avea valorile "knapsack" sau "tsp"
    :param population: populatia initiala
    :param evaluator: in cazul unei probleme de tip Kanpsack va avea contine o lista de obiecte si capacitatea maxima
                    in cazul uneil probleme de tip TSP va contine matricea de distante
    :return parent: lista
    """
    parent1, parent2 = [], []
    p = population[:]  # copie a populatiei initiale
    for i in range(2):
        sample = np.random.default_rng().choice(population_size, size=2, replace=False)
        possible_parents = [p[s] for s in sample]
        if sample[0] > sample[1]:
            sample[0], sample[1] = sample[1], sample[0]
        del p[sample[0]]
        del p[sample[1] - 1]
        population_size -= 2
        parent = []
        if problem_type == "knapsack":
            parent = sorted(possible_parents, key=lambda x: Knapsack.fitness(evaluator[0], x, evaluator[1]),
                            reverse=True)
        elif problem_type == "tsp":
            parent = sorted(possible_parents, key=lambda x: TSP.fitness_TSP(x, evaluator), reverse=False)
        if i == 0:
            parent1 = parent[0]
        else:
            parent2 = parent[0]
    return parent1, parent2


'''Crossover functions'''


'''Binary'''


def single_point(parent1: list, parent2: list, problem_size: int):
    """
    Incrucisare printr-un punct de taietura.
    :param parent1: o solutie a problemei data in reprezentare binara
    :param parent2: o solutie a problemei data in reprezentare binara
    :param problem_size: marimea solutiilor problemei
    :return child1: prima solutie copil obtinuta din incrucisare
    :return child2: a doua solutie copil obtinuta din incrucisare
    """
    c_point = np.random.randint(1, problem_size - 1)
    child1 = parent1[:c_point] + parent2[c_point:]
    child2 = parent2[:c_point] + parent1[c_point:]
    return child1, child2


def two_point(parent1: list, parent2: list, problem_size: int):
    """
    Incrucisare prin doua puncte de taietura.
    :param parent1: o solutie a problemei data in reprezentare binara
    :param parent2: o solutie a problemei data in reprezentare binara
    :param problem_size: marimea solutiilor problemei
    :return child1: prima solutie copil obtinuta din incrucisare
    :return child2: a doua solutie copil obtinuta din incrucisare
    """
    options = range(1, problem_size - 1)
    sample = np.random.default_rng().choice(options, size=2, replace=False)
    if sample[0] > sample[1]:
        sample[0], sample[1] = sample[1], sample[0]
    child1 = parent2[:sample[0]] + parent1[sample[0]:sample[1]] + parent2[sample[1]:]
    child2 = parent1[:sample[0]] + parent2[sample[0]:sample[1]] + parent1[sample[1]:]
    return child1, child2


def binary_crossover(problem_type: str, problem_size: int, population_size: int, population: list, crossover_count: int,
                     evaluator, operator: str):
    """
    Aici se executa un crossover in functie de operatorul de crossover dat
    :param operator: operatorul de incrucisare
    :param population_size:
    :param evaluator: in cazul unei probleme de tip Kanpsack va avea contine o lista de obiecte si capacitatea maxima
                    in cazul uneil probleme de tip TSP va contine matricea de distante
    :param crossover_count: marimea populatiei obtinute dupa crossover / 2
    :param problem_type: poate avea valorile "knapsack" sau "tsp"
    :param problem_size: marimea problemei
    :param population: populatia initiala
    :return children: copiii obtinuti dupa crossover
    """
    children = []
    for i in range(crossover_count):
        parent1, parent2 = selection(problem_type, population, population_size, evaluator)
        child1, child2 = [], []
        if operator == "spc":
            child1, child2 = single_point(parent1, parent2, problem_size)
        elif operator == "tpc":
            child1, child2 = two_point(parent1, parent2, problem_size)
        children.append(child1)
        children.append(child2)
    return children


'''Permutation'''


def complete_child(child: list, parent: list):
    """
    Completeaza solutia copil cu valorile din solutia parinte.
    O pozitie e libera daca e egala cu -1.
    :param child: o solutie a problemei cu valorile -1 in locurile libere
    :param parent: o solutie completa pentru problema, sub forma unei permutari
    :return child: solutia copil completata
    """
    index = 0
    for i in range(len(parent)):
        if parent[i] not in child:
            while child[index] != -1 and index < len(child):
                index += 1
            child[index] = parent[i]
    return child


def cycle_crossover(parent1: list, parent2: list):
    """
    Aceasta functie executa un crossover de tip ciclic intre cei doi parinti primiti la intrare
    :param parent1: primul parinte(o solutie a problemeie)
    :param parent2: al doilea parint(o solutie a problemeie)
    :return child: un copilul obtinut dupa un crossover ciclic(o noua solutie pentru problema)
    """
    child = [-1] * len(parent1)
    index = 0
    while child[index] == -1:
        child[index] = parent1[index]
        value = parent2[index]
        index = parent1.index(value)
    child = complete_child(child, parent2)
    return child


def order_crossover(parent1: list, parent2: list, problem_size: int):
    """
    Se executa o incrucisare ordonata
    :param parent1: o solutie parinte pt problema, reprezentata printr-o permutare
    :param parent2: o solutie parinte pt problema, reprezentata printr-o permutare
    :param problem_size: marimea solutiilor obtinute si primite ca parametri
    :return child1: prima solutie copil obtinuta din incrucisare
    :return child2: a doua solutie copil obtinuta din incrucisare
    """
    child1 = [-1] * len(parent1)
    child2 = [-1] * len(parent2)
    options = range(1, problem_size)
    sample = np.random.default_rng().choice(options, size=2, replace=False)
    if sample[0] > sample[1]:
        sample[0], sample[1] = sample[1], sample[0]
    child1[sample[0]:sample[1]] = parent1[sample[0]:sample[1]]
    child2[sample[0]:sample[1]] = parent2[sample[0]:sample[1]]
    child1 = complete_child(child1, parent2)
    child2 = complete_child(child2, parent1)
    return child1, child2


def permutation_crossover(problem_type: str, problem_size: int, population_size: int, population: list,
                          crossover_count: int, evaluator, operator: str):
    """
    Aici se face un crossover pentru solutii de tip permutare.
    :param problem_size: marimea solutiilor obtinute si primite ca parametri
    :param operator: operatorul de incrucisare
    :param problem_type: poate avea valorile "knapsack" sau "tsp"
    :param population_size: marimea problemei
    :param population: populatia initiala
    :param crossover_count: marimea populatiei obtinute dupa crossover / 2
    :param evaluator: in cazul unei probleme de tip Kanpsack va avea contine o lista de obiecte si capacitatea maxima
                    in cazul uneil probleme de tip TSP va contine matricea de distante
    :return children: toti copiii obtinuti dupa crossover
    """
    children = []
    for i in range(crossover_count):
        parent1, parent2 = selection(problem_type, population, population_size, evaluator)
        child1, child2 = [], []
        if operator == "cx":
            child1 = cycle_crossover(parent1, parent2)
            child2 = cycle_crossover(parent2, parent1)
        elif operator == "ox":
            child1, child2 = order_crossover(parent1, parent2, problem_size)
        children.append(child1)
        children.append(child2)
    return children


'''Mutation functions'''


'''Binary'''


def binary_mutation(children: list, problem_size: int, mutation_rate: float, operator: str):
    """
    Creeaza mutatii copiiilor obtinuti dupa crossover pentru solutii cu reprezentare binara.
    :param operator: operatorul de mutatie. Poate avea valorile "hard" si "weak"
    :param problem_size: marimea problemei pentru care se cauta solutia
    :param children: Lista formata din copiii obtinuti dupa crossover
    :param mutation_rate: rata de mutatie pentru care se va face bit flip
    :return mutants: o lista formata dupa mutatia copiiilor
    """
    mutants = []
    for c in children:
        mutant_child = c[:]
        for i in range(problem_size):
            if np.random.random() < mutation_rate:
                if operator == "hard":  # mutatie tare
                    mutant_child[i] = 1 - mutant_child[i]  # Bit flip
                elif operator == "weak":  # mutatie slaba
                    mutant_child[i] = np.random.randint(2)
        mutants.append(mutant_child)
    return mutants


'''Permutation'''


def perMutation(children: list, problem_size: int, mutation_rate: float, operator: str):
    """
    Creeaza mutatii copiiilor obtinuti dupa crossover pentru solutii cu reprezentare sub form de permutari.
    :param operator: operatorul de mutatie, Poate avea valorile "invs" si "swap"
    :param children: Lista formata din copiii obtinuti dupa crossover
    :param problem_size: marimea problemei pentru care se cauta solutia
    :param mutation_rate: rata de mutatie pentru care se vor face transformari asupra unei solutii
    :return mutants: o lista formata dupa mutatia copiiilor
    """
    mutants = []
    for c in children:
        mutant_child = c[:]
        if np.random.random() < mutation_rate:
            sample = np.random.default_rng().choice(problem_size, size=2, replace=False)
            if operator == "invs":  # mutatie prin inversiune
                if sample[0] > sample[1]:
                    sample[0], sample[1] = sample[1], sample[0]
                mutant_child[sample[0]:sample[1] + 1] = reversed(mutant_child[sample[0]:sample[1] + 1])
            elif operator == "swap":  # mutatie prin interschimbare
                mutant_child[sample[0]], mutant_child[sample[1]] = mutant_child[sample[1]], mutant_child[sample[0]]
        mutants.append(mutant_child)
    return mutants


'''Evolutionary algorithm'''


def evolutionary_algorithm(problem_type, problem_size, population_size, mutation_rate, crossover_rate,
                           generations, evaluator, crossover_operator: str, mutation_operator: str):
    """
    Aceasta functie executa un algoritm evolutiv
    :param problem_type: poate avea valorile "knapsack" sau "tsp"
    :param problem_size: marimea problemei(adica cat de lungi o sa fie solutiile obtinute)
    :param population_size: marimea populatiei pe parcursul problemei
    :param mutation_rate: rata de mutatie(sansele de a face mutatii asupra unei solutii)
    :param crossover_rate: rata populatiei obtinute din crossover(nu va afecta obtinerea populatiei initiale)
    :param generations: numarul de generatii parcurse de algoritm pana la stop
    :param evaluator: in cazul unei probleme de tip Kanpsack va avea contine o lista de obiecte si capacitatea maxima
                    in cazul uneil probleme de tip TSP va contine matricea de distante
    :param crossover_operator: operatorul de crossover
    :param mutation_operator: operatorul de mutatie
    :return best: cele mai bune fitness-uri din populatie
    :return avg: valoarile medii pentru fitness-urile populatie
    :return worst: cele mai slabe fitness-uri din populatie
    """
    population = generate_rnd_population(problem_type, problem_size, population_size, evaluator)
    b, a, w = evaluate_population(problem_type, population, population_size, evaluator)
    best = [b]
    avg = [a]
    worst = [w]
    crossover_count = int((population_size * crossover_rate / 100) // 2)
    for i in range(generations):
        mutants = []
        if problem_type == "knapsack":
            children = binary_crossover(problem_type, problem_size, population_size, population, crossover_count,
                                        evaluator, crossover_operator)
            mutants = binary_mutation(children, problem_size, mutation_rate, mutation_operator)
        elif problem_type == "tsp":
            children = permutation_crossover(problem_type, problem_size, population_size, population, crossover_count,
                                             evaluator, crossover_operator)
            mutants = perMutation(children, problem_size, mutation_rate, mutation_operator)
        population = new_population(problem_type, population, mutants, evaluator)
        b, a, w = evaluate_population(problem_type, population, population_size, evaluator)
        best.append(b)
        avg.append(a)
        worst.append(w)
    return best, avg, worst
