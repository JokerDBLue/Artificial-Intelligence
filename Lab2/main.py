import time
import matplotlib.pyplot as plt  # to plot :)

from readWrite import *
from Rucsac import *
from TSP import *


def options_solutions():
    print("Alegeti una dintre urmatoarele optiuni:\n"
          "1. Tabu search\n"
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
          "Orice alt numar EXIST")


def options_TSP():
    print("Alegeti una dintre urmatoarele optiuni:\n"
          "1. Simulated Annealing\n"
          "Orice alt numar BACK")


def menu_solver(objects: list, max_capacity: int, file_name: str):
    while True:
        options_solutions()
        i = int(input("\nOptiunea dorita: "))
        best_solutions = []
        values = []
        weights = []
        times = []
        nfn = file_name
        if i == 1:
            k = int(input("Numar de iteratii dorite: "))
            p = int(input("Numarul de iteratii tabu: "))
            execution_nr = int(input("De cate ori sa se execute algoritmul: "))
            nfn += "TS_" + str(k) + "_" + str(p) + "_" + str(execution_nr) + ".txt"
            for i in range(execution_nr):
                start_time = time.time()
                best_sol, value, weight = tabu_search(k, p, objects, max_capacity)
                times.append(time.time() - start_time)
                best_solutions.append(best_sol)
                values.append(value)
                weights.append(weight)
                print("Cea mai buna solutie obtinuta in urma algoritmului TS: ", best_sol)
                print("Cu valoarea de: ", value)
                print("Cu greutatea de: ", weight)
            write_to_file_rucsac(nfn, best_solutions, values, weights, times)
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


def see_annealing(states):
    plt.figure()
    plt.title("Evolutia algoritmului")
    plt.plot(states, 'r')
    plt.show()


def menu_tsp():
    locations, dimension = read_from_file_TSP("kroC100.tsp")
    dm = distance_matrix(locations)
    print("Valoare optima:", fitness_TSP(read_from_file_TSPOpt("kroC100.opt.tour"), dm))
    while True:
        options_TSP()
        i = int(input("Optiunea dorita este: "))
        if i == 1:
            t = float(input("Temperatura: "))
            alpha = float(input("Valoarea de racire: "))
            t_min = float(input("Valoarea minima pentru temperatura: "))
            k = int(input("Numar iteratii: "))
            nr_exec = int(input("Numar executii: "))
            file_name = "TSP_" + str(t) + "_" + str(alpha) + "_" + str(t_min) + "_" + str(k) + "_" + str(nr_exec) \
                        + ".txt"
            times = []
            c = []
            d = []
            while nr_exec > 0:
                start_time = time.time()
                final_sol = simulated_annealing(t, alpha, t_min, k, dm, dimension)
                times.append(time.time() - start_time)
                c.append(final_sol[0])
                d.append(final_sol[1])
                print(final_sol[0], " ", final_sol[1])
                nr_exec -= 1
                see_annealing(final_sol[2])
            write_to_file_TSP(file_name, c, d, times)
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
