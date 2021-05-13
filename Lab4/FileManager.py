import numpy as np


def write_to_file_ea(name: str, best: list, avg: list, worst: list, time: list):
    with open(name, 'w') as file:
        line = str(np.average(best)) + " " + str(np.average(avg)) + " " + str(np.average(worst)) + " " + str(
            np.average(time)) + "\n"
        file.write(line)
        line = str(min(best)) + "\n"
        file.write(line)


def write_to_file_pso(name: str, best: list, time: list):
    with open(name, 'w') as file:
        line = str(np.average(best)) + " " + str(np.average(time)) + "\n"
        file.write(line)
        line = str(min(best)) + "\n"
        file.write(line)
