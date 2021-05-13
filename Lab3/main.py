import time
import matplotlib.pyplot as plt  # to plot :)

from FileManager import *
from TSP import distance_matrix
from Evolutionary import evolutionary_algorithm


def options_solutions():
    print("Alegeti una dintre urmatoarele optiuni:\n"
          "1. Algoritm evolutiv\n"
          "Orice alt numar BACK")


def options_reading():
    print("Alegeti una dintre urmatoarele optiuni:\n"
          "1. Citeste datele din fisier\n"
          "2. Citeste datele de la tastatura\n"
          "3. Optiune predefinita\n "
          "Orice alt numar BACK")


def options_problem():
    print("Alegeti una dintre urmatoarele optiuni:\n"
          "1. Rezolva Rucsac\n"
          "2. Rezolva TSP\n"
          "Orice alt numar EXIT")


def menu_solver(objects: list, max_capacity: int, file_name: str):
    while True:
        options_solutions()
        i = int(input("\nOptiunea dorita: "))
        new_file = file_name
        if i == 1:
            p_size = int(input("Marimea populatie: "))
            c_rate = int(input("Rata de incrucisare: "))
            m_rate = float(input("Rata de mutatie: "))
            nr_gen = int(input("Numarul de generatii: "))
            j = int(input("Alege operatorul de incrucisare:\n1.Cu o taietura\n2.Cu doua taieturi\nAlegerea ta: "))
            if j == 1:
                op_c = "spc"
            else:
                op_c = "tpc"
            j = int(input("Alege operatorul de mutatie:\n1.Tare\n2.Slaba\nAlegerea ta: "))
            if j == 1:
                op_m = "hard"
            else:
                op_m = "weak"
            evaluator = [objects, max_capacity]
            dimension = len(objects)
            nr_exec = int(input("De cate ori sa se execute algoritmul: "))
            new_file += str(p_size) + "_" + str(c_rate) + "_" + str(m_rate) + "_" + str(nr_gen) + "_" + str(
                nr_exec) + "_" + op_c + "_" + op_m + ".txt"
            bests, averages, worsts, times = [], [], [], []
            for i in range(nr_exec):
                start_time = time.time()
                best, avg, worst = evolutionary_algorithm("knapsack", dimension, p_size, m_rate, c_rate, nr_gen,
                                                          evaluator, op_c, op_m)
                start_time = time.time() - start_time
                bests.append(best[-1])
                averages.append(avg[-1])
                worsts.append(worst[-1])
                times.append(start_time)
                see_evolution(best, avg, worst)
            write_to_file(new_file, bests, averages, worsts, times, "knapsack")
        else:
            break


def menu_knapsack():
    while True:
        objects = []

        options_reading()
        i = int(input("Optiunea dorita este: "))
        if i == 1:
            file_name = input("Dati numele fisierului: ")
            objects, max_capacity = read_from_file_knapsack(file_name)
        elif i == 2:
            file_name = "UI_"
            nr_obj = int(input("\nNumarul de obiecte dorite: "))
            for i in range(nr_obj):
                objects.append(tuple(int(x) for x in input("valoare,greutate: ").split(",")))
            max_capacity = int(input("Capacitate maxima: "))
        elif i == 3:
            file_name = "PI_"
            objects = [(5, 60), (60, 5), (80, 10), (60, 10), (60, 20)]
            max_capacity = 65
        else:
            print("La revedere")
            break

        print("\nObiectele citite sunt: ", objects, "\nCapacitatea maxima este: ", max_capacity, "\n")
        menu_solver(objects, max_capacity, file_name)


def see_evolution(best, avg, worst):
    plt.figure()
    plt.title("Evolutia algoritmului")
    plt.plot(best, 'g')
    plt.plot(avg, 'b')
    plt.plot(worst, 'r')
    plt.show()


def menu_tsp():
    locations, dimension = read_from_file_TSP("kroC100.tsp")
    dm = distance_matrix(locations)
    while True:
        options_solutions()
        i = int(input("Optiunea dorita este: "))
        if i == 1:
            p_size = int(input("Marimea populatie: "))
            c_rate = int(input("Rata de incrucisare: "))
            m_rate = float(input("Rata de mutatie: "))
            nr_gen = int(input("Numarul de generatii: "))
            j = int(input("Alege operatorul de incrucisare:\n1.Ciclica\n2.Ordonata\nAlegerea ta: "))
            if j == 1:
                op_c = "cx"
            else:
                op_c = "ox"
            j = int(input("Alege operatorul de mutatie:\n1.Inversiune\n2.Interschimbare\nAlegerea ta: "))
            if j == 1:
                op_m = "invs"
            else:
                op_m = "swap"
            nr_exec = int(input("Numar executii: "))
            new_file = "{0}_{1}_{2}_{3}_{4}_{5}_{6}.txt".format(str(p_size), str(c_rate), str(m_rate), str(nr_gen), str(
                nr_exec), op_c, op_m)
            bests, averages, worsts, times = [], [], [], []
            while nr_exec > 0:
                start_time = time.time()
                best, avg, worst = evolutionary_algorithm("tsp", dimension, p_size, m_rate, c_rate, nr_gen, dm,
                                                          op_c, op_m)
                start_time = time.time() - start_time
                bests.append(best[-1])
                averages.append(avg[-1])
                worsts.append(worst[-1])
                times.append(start_time)
                see_evolution(best, avg, worst)
                nr_exec -= 1
            write_to_file(new_file, bests, averages, worsts, times, "tsp")
        else:
            break


def menu():
    while True:
        options_problem()
        i = int(input("Optiunea dorita este: "))
        if i == 1:
            menu_knapsack()
        elif i == 2:
            menu_tsp()
        else:
            print("La revedere")
            break


if __name__ == "__main__":
    menu()
