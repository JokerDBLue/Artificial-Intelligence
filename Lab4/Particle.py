import SchwefelFunction as sf
import numpy as np


class Particle:
    def __init__(self, n: int, positions: list, velocity: list, fitness: float, domain_x: tuple, domain_v: tuple):
        self.n = n
        self.positions = positions
        self.velocity = velocity
        self.fitness = fitness
        self.p_best = self.positions[:]
        self.domain_x = domain_x
        self.domain_v = domain_v

    def update_velocity(self, w: float, c1: float, c2: float, g_best: list):
        v = self.velocity[:]
        for i in range(self.n):
            v[i] = w * v[i] + c1 * np.random.random() * (
                    self.p_best[i] - self.positions[i]) + c2 * np.random.random() * (g_best[i] - self.positions[i])
            if self.domain_v[0] <= v[i] <= self.domain_v[1]:
                self.velocity[i] = v[i]

    def update_positions(self):
        for i in range(self.n):
            if self.domain_x[0] <= self.positions[i] + self.velocity[i] <= self.domain_x[1]:
                self.positions[i] += self.velocity[i]
        self.fitness = sf.schwefel(self.n, self.positions)

    def update_p_best(self):
        if sf.schwefel(self.n, self.positions) < sf.schwefel(self.n, self.p_best):
            self.p_best = self.positions[:]

    def get_p_best(self):
        return self.p_best

    def get_position(self):
        return self.positions

    def __str__(self):
        s = "Coordonate: {0}\nViteza: {1}\nFitness: {2}\nPersonal best: {3}\n".format(self.positions, self.velocity,
                                                                                      self.fitness, self.p_best)
        return s
