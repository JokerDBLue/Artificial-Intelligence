import SchwefelFunction as sf
from Particle import Particle


def generate_rnd_particles(problem_size: int, no_particles: int):
    """
    Returneaza o populatie de marime population_size pentru problema problem_type de marime problem_size
    :param no_particles: marimea populatioe
    :param problem_size: marimea pentru solutia problemei
    :return particles: populatia noua pentru problema specificata
    """
    particles = []
    domain_x = (sf.LOWER_BOUND, sf.UPPER_BOUND)
    domain_v = (int(10 * sf.LOWER_BOUND / 100), int(10 * sf.UPPER_BOUND / 100))
    for i in range(no_particles):
        positions = sf.generate_solution(problem_size)
        velocity = sf.generate_solution(problem_size, domain_v[0], domain_v[1])
        f = sf.schwefel(problem_size, positions)
        particles.append(Particle(problem_size, positions, velocity, f, domain_x, domain_v))
    return particles


def get_global_best(particles: list, problem_size: int, no_particles: int):
    g_best = particles[0].get_p_best()
    for i in range(no_particles):
        if sf.schwefel(problem_size, particles[i].get_p_best()) < sf.schwefel(problem_size, g_best):
            g_best = particles[i].get_p_best()[:]
    return g_best


def pso(problem_size: int, no_particles: int, no_iterations, w: float, c1: float, c2: float):
    particles = generate_rnd_particles(problem_size, no_particles)
    best = []
    g_best = get_global_best(particles, problem_size, no_particles)
    best.append(sf.schwefel(problem_size, g_best))
    for k in range(no_iterations):
        for i in range(no_particles):
            particles[i].update_p_best()
            particles[i].update_velocity(w, c1, c2, g_best)
            particles[i].update_positions()
        g_best = get_global_best(particles, problem_size, no_particles)
        best.append(sf.schwefel(problem_size, g_best))
    return g_best, best
