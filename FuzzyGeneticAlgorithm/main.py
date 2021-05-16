import FileManager as fm
import Knapsack as ks
import GA as genetic


def runner(m, n, alpha, b):
    s = 0
    f_name = "{0}_{1}_{2}_{3}.txt".format(str(m), str(n), str(alpha), str(b))
    for i in range(1):
        w, c, p = ks.generate_knapsack(m, n, alpha)
        for j in range(10):
            print(m, " ", n, " ", alpha, " ", b, " ", i, " ", j, end=" ")
            r = genetic.fga(n, p, w, c, m)
            pd = abs(b - r) / b
            print(pd)
            s += pd
    avg_pd = s / 10
    fm.write_to_file(f_name, avg_pd)


def test():
    m = (5, 10, 30)
    n = (100, 250, 500)
    alpha = (0.25, 0.50, 0.75)
    b = [((24197.20, 43252.90, 60471.00), (60409.70, 109284.60, 151555.90), (120615.50, 219503.10, 302354.90)),
         ((22601.90, 45659.10, 59555.60), (58993.90, 108706.40, 151330.40), (118565.50, 217274.60, 302556.00)),
         ((21654.60, 41431.30, 59199.10), (56875.90, 106673.70, 150443.50), (115473.50, 216156.90, 302353.40))]
    for i in range(len(m)):
        for j in range(len(n)):
            for k in range(len(alpha)):
                runner(m[i], n[j], alpha[k], b[i][j][k])


if __name__ == "__main__":
    test()
