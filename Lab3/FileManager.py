import numpy as np


def read_from_file_knapsack(name: str):
    objects = []
    with open(name, 'r') as file:
        nr_obj = int(file.readline())
        for i in range(nr_obj):
            line = file.readline()
            line = line.split(" ")
            line = [x for x in line if x != ""]
            objects.append(tuple(int(x) for x in line[1:]))
        max_capacity = int(file.readline())
    return objects, max_capacity


def read_from_file_TSP(name: str):
    locations = []
    dimension = 0
    with open(name, 'r') as file:
        for i in range(6):
            line = file.readline()
            line = line.replace("\n", "")
            line = line.split(" ")
            if len(line) == 2 and line[0] == "DIMENSION:":
                dimension = int(line[1])
        for i in range(dimension):
            line = file.readline()
            line = line.replace("\n", "")
            line = line.split(" ")
            line = [x for x in line if x != ""]
            locations.append(tuple(int(x) for x in line[:]))
    return locations, dimension


def write_to_file(name: str, best: list, avg: list, worst: list, time: list, problem_type: str):
    with open(name, 'w') as file:
        line = str(np.average(best)) + " " + str(np.average(avg)) + " " + str(np.average(worst)) + " " + str(
            np.average(time)) + "\n"
        file.write(line)
        if problem_type == "tsp":
            line = str(min(best)) + "\n"
        elif problem_type == "knapsack":
            line = str(max(best)) + "\n"
        file.write(line)
