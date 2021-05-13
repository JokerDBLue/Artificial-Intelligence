from logic import *
import time


def options_solutions():
    print("Alegeti una dintre urmatoarele optiuni:\n"
          "1. Generarea unei solutii si verificarea acesteia\n"
          "2. Generarea de k solutii si gasirea celei mai bune solutii\n"
          "3. Random Hill Climbing\n"
          "Orice alt numar BACK")


def options_reading():
    print("Alegeti una dintre urmatoarele optiuni:\n"
          "1. Citeste datele din fisier\n"
          "2. Citeste datele de la tastatura\n"
          "3. Optiune predefinita\n "
          "Orice alt numar EXIT")


def read_from_file(name: str):
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


def write_to_file(name: str, solution_list: list, value_list: list, weight_list: list, times: list):
    with open(name, 'w') as file:
        for i in range(len(solution_list)):
            line = str(solution_list[i]) + " " + str(value_list[i]) + " " + str(weight_list[i]) + " " + str(
                times[i]) + "\n"
            file.write(line)
        line = str(get_mean(value_list)) + " " + str(get_mean(weight_list)) + " " + str(get_mean(times))
        file.write(line)


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
            solutions = generate_solution(len(objects))
            print("Solutia generata: ", solutions)
            print("Validitatea solutiei: ", is_valid(objects, solutions, max_capacity))
            print("Valoarea solutiei e: ", fitness(objects, solutions, max_capacity))
        elif i == 2:
            k = int(input("Cate solutii doriti sa se genereze: "))
            execution_nr = int(input("De cate ori sa se execute algoritmul: "))
            nfn += "RS_" + str(k) + "_" + str(execution_nr) + ".txt"
            for i in range(execution_nr):
                start_time = time.time()
                solutions = generate_k_solutions(len(objects), k, objects, max_capacity)
                best_sol, value, weight = best_solution(objects, solutions, max_capacity)
                times.append(time.time() - start_time)
                best_solutions.append(best_sol)
                values.append(value)
                weights.append(weight)
                print("Cea mai buna solutie este: ", best_sol)
                print("Cu valoarea: ", value)
                print("Cu greutatea de: ", weight)
            write_to_file(nfn, best_solutions, values, weights, times)
        elif i == 3:
            k = int(input("Numar de iteratii dorite: "))
            p = int(input("Numarul de iteratii pana la restart: "))
            execution_nr = int(input("De cate ori sa se execute algoritmul: "))
            nfn += "RHC_" + str(k) + "_" + str(p) + "_" + str(execution_nr) + ".txt"
            for i in range(execution_nr):
                start_time = time.time()
                best_sol, value, weight = random_hill_climbing(k, p, objects, max_capacity)
                times.append(time.time() - start_time)
                best_solutions.append(best_sol)
                values.append(value)
                weights.append(weight)
                print("Cea mai buna solutie obtinuta in urma algoritmului RHC: ", best_sol)
                print("Cu valoarea de: ", value)
                print("Cu greutatea de: ", weight)
            write_to_file(nfn, best_solutions, values, weights, times)
        else:
            break


def menu():
    while True:
        objects = []

        options_reading()
        i = int(input("Optiunea dorita este: "))
        if i == 1:
            file_name = input("Dati numele fisierului: ")
            objects, max_capacity = read_from_file(file_name)
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


if __name__ == "__main__":
    menu()
