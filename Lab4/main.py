import time
import matplotlib.pyplot as plt  # to plot :)

from FileManager import *
from Evolutionary import evolutionary_algorithm
from PSO import pso


def options_solutions():
    print("Alegeti una dintre urmatoarele optiuni:\n"
          "1. Algoritm evolutiv\n"
          "2. PSO\n"
          "Orice alt numar BACK")


def see_evolution(best, avg, worst):
    plt.figure()
    plt.title("Evolutia algoritmului")
    plt.plot(worst, 'r')
    plt.plot(avg, 'b')
    plt.plot(best, 'g')
    plt.legend(["worst", "avg", "best"], loc="upper right")
    plt.show()


def menu_solver():
    while True:
        options_solutions()
        i = int(input("\nOptiunea dorita: "))
        new_file = ""
        if i == 1:
            n = int(input("Marimea problemei: "))
            p_size = int(input("Marimea populatie: "))
            c_rate = int(input("Rata de incrucisare: "))
            m_rate = float(input("Rata de mutatie: "))
            nr_gen = int(input("Numarul de generatii: "))
            j = int(input("Alege operatorul de incrucisare:\n1.avg\n2.discreet\nAlegerea ta: "))
            if j == 1:
                op_c = "avg"
            else:
                op_c = "discreet"
            p = float(input("Probabilitatea: "))
            j = int(input("Alege operatorul de mutatie:\n1.uniform\n2.nonuniform\nAlegerea ta: "))
            if j == 1:
                op_m = "uniform"
            else:
                op_m = "nonuniform"
            j = int(input("Alege operatorul de selectie:\n1.turnir\n2.rank\nAlegerea ta: "))
            if j == 1:
                op_s = "turnir"
                s = int(input("Marimea turneului: "))
            else:
                op_s = "rank"
                s = float(input("Alegeti presiunea de selectie(un numar intre 1 si 2): "))

            nr_exec = int(input("De cate ori sa se execute algoritmul: "))
            new_file += "GA_{0}_{1}_{2}_{3}_{4}_{5}_{6}_{7}_{8}_{9}.txt".format(str(p_size), str(c_rate), str(m_rate),
                                                                                str(nr_gen), str(nr_exec), op_c, str(p),
                                                                                op_m, op_s, str(s))
            bests, averages, worsts, times = [], [], [], []
            for i in range(nr_exec):
                start_time = time.time()
                best, avg, worst = evolutionary_algorithm(n, p_size, m_rate, c_rate, nr_gen, op_c, op_m, op_s, s, p)
                start_time = time.time() - start_time
                bests.append(best[-1])
                averages.append(avg[-1])
                worsts.append(worst[-1])
                times.append(start_time)
                see_evolution(best, avg, worst)
            write_to_file_ea(new_file, bests, averages, worsts, times)
        elif i == 2:
            n = int(input("Marimea problemei: "))
            no_p = int(input("Numarul de particule: "))
            no_i = int(input("Numarul de iteratii: "))
            w = float(input("Factorul de inertie: "))
            c1 = float(input("Factorul de invatare cognitiv: "))
            c2 = float(input("Factorul de invatare social: "))
            nr_exec = int(input("De cate ori sa se execute algoritmul: "))
            new_file += "PSO_{0}_{1}_{2}_{3}_{4}_{5}_{6}.txt".format(str(n), str(no_p), str(no_i), str(w), str(c1),
                                                                     str(c2), str(nr_exec))
            bests, times = [], []
            for i in range(nr_exec):
                start_time = time.time()
                g_best, best = pso(n, no_p, no_i, w, c1, c2)
                start_time = time.time() - start_time
                times.append(start_time)
                bests.append(best[-1])
                see_evolution(best, [], [])
                print(g_best, " ", best[-1])
            write_to_file_pso(new_file, bests, times)
        else:
            break


if __name__ == "__main__":
    menu_solver()
