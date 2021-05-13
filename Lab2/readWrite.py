import numpy as np


def get_mean(elements: list):
    return np.average(elements)


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


def write_to_file_rucsac(name: str, solution_list: list, value_list: list, weight_list: list, times: list):
    with open(name, 'w') as file:
        for i in range(len(solution_list)):
            line = str(solution_list[i]) + " " + str(value_list[i]) + " " + str(weight_list[i]) + " " + str(
                times[i]) + "\n"
            file.write(line)
        line = str(get_mean(value_list)) + " " + str(get_mean(weight_list)) + " " + str(get_mean(times))
        file.write(line)


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


def read_from_file_TSPOpt(name: str):
    solution = []
    dimension = 0
    with open(name, 'r') as file:
        for i in range(5):
            line = file.readline()
            line = line.replace("\n", "")
            line = line.split(" ")
            if len(line) == 3 and line[0] == "DIMENSION":
                dimension = int(line[2])
        for i in range(dimension):
            line = file.readline()
            line = line.replace("\n", "")
            solution.append(int(line) - 1)
    return solution


def write_to_file_TSP(name: str, solution_list: list, distance_list: list, times: list):
    with open(name, 'w') as file:
        for i in range(len(solution_list)):
            line = str(solution_list[i]) + " " + str(distance_list[i]) + " " + str(times[i]) + "\n"
            file.write(line)
        line = str(get_mean(distance_list)) + " " + str(get_mean(times))
        file.write(line)
