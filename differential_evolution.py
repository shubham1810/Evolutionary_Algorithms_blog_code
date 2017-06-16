__author__ = 'Shubham Dokania'

import copy
import random
import time

from helpers.population import Population
from helpers import get_best_point
from helpers.test_functions import Function

from matplotlib import pyplot as plt
import seaborn as sns


class DifferentialEvolution(object):
    def __init__(self, num_iterations=10, CR=0.4, F=0.48, dim=2, population_size=10, print_status=False, visualize=False, func=None):
        random.seed()
        self.print_status = print_status
        self.visualize = visualize
        self.num_iterations = num_iterations
        self.iteration = 0
        self.CR = CR
        self.F = F
        self.population_size = population_size
        self.func = Function(func=func)
        self.population = Population(dim=dim, num_points=self.population_size, objective=self.func)

    def iterate(self):
        for ix in xrange(self.population.num_points):
            x = self.population.points[ix]
            [a, b, c] = random.sample(self.population.points, 3)
            while x == a or x == b or x == c:
                [a, b, c] = random.sample(self.population.points, 3)

            R = random.random() * x.dim
            y = copy.deepcopy(x)

            for iy in xrange(x.dim):
                ri = random.random()

                if ri < self.CR or iy == R:
                    y.coords[iy] = a.coords[iy] + self.F * (b.coords[iy] - c.coords[iy])

            y.evaluate_point()
            if y.z < x.z:
                self.population.points[ix] = y
        self.iteration += 1

    def simulate(self):
        all_vals = []
        avg_vals = []
        pnt = get_best_point(self.population.points)
        all_vals.append(pnt.z)
        avg_vals.append(self.population.get_average_objective())
        print("Initial best value: " + str(pnt.z))
        while self.iteration < self.num_iterations:
            if self.print_status == True and self.iteration%50 == 0:
                pnt = get_best_point(self.population.points)
                print pnt.z, self.population.get_average_objective()
            self.iterate()
            all_vals.append(get_best_point(self.population.points).z)
            avg_vals.append(self.population.get_average_objective())
            if self.visualize == True and self.iteration%2==0:
                self.population.get_visualization()
        # sns.figure(0)
        plt.plot(all_vals, 'r', label='Best')
        plt.plot(avg_vals, 'g', label='Average')
        plt.legend()
        plt.xlabel('Iterations')
        plt.ylabel('Objective Function Value')
        plt.title(self.func.func_name + ', ' + str(self.population.dim) + '-D')
        plt.show()
        pnt = get_best_point(self.population.points)
        print("Final best value: " + str(pnt.z))
        return pnt.z


if __name__ == '__main__':
    number_of_runs = 1
    val = 0
    print_time = True

    for i in xrange(number_of_runs):
        start = time.clock()
        de = DifferentialEvolution(num_iterations=500, dim=50, CR=0.4, F=0.48, population_size=75, print_status=False, func='rastrigin')
        val += de.simulate()
        if print_time:
            print("")
            print(time.clock() - start)

    print("Final average of all runs: "), (val / number_of_runs)

