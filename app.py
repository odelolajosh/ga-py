
from genetic_algorithm.selection import RouletteSelection
from genetic_algorithm.crossover import SinglePointCrossover
from genetic_algorithm.mutation import BitFlipMutation
from genetic_algorithm.chromosome_decoder import BinaryChromosomeDecoder
from genetic_algorithm.optimization import Maximization
from genetic_algorithm.termination_criterion import NumberOfGeneration, OrTermination, ThresholdDifference
from ga import GeneticAlgorithm
from genetic_algorithm.callbacks.base import Callback
import matplotlib.pyplot as plt

class PlotFitnessCallback(Callback):
    def __init__(self):
        self.generations = []
        self.best_fitnesses = []

    def on_generation_end(self, generation, population, best_fitness, best_individual):
        self.generations.append(generation)
        self.best_fitnesses.append(best_fitness)

    def on_evolution_end(self, best_fitness, best_individual):
        plt.figure(figsize=(10, 6))
        plt.plot(self.generations, self.best_fitnesses, marker='o')
        plt.title('Fitness vs Generation')
        plt.xlabel('Generation')
        plt.ylabel('Best Fitness')
        plt.grid(True)
        plt.show()


print("Laboratory Exercise 1")
def f(x):
    return 2*x[0]*x[1]*x[2] - 4*x[0]*x[2] - 2*x[1]*x[2] + x[0]**2 + x[1]**2 + x[2]**2 - 2*x[0] - 4*x[1] + 4*x[2]
ga = GeneticAlgorithm(
    population_size=50,
    objective_function=f,
    chromosome_decoder=BinaryChromosomeDecoder(
        number_of_bytes=10,
        number_of_decision_variables=3,
        lower_bounds=[10, 0, -20],
        upper_bounds=[90, 90, 60]
    ),
    termination=OrTermination(
        NumberOfGeneration(50),
        ThresholdDifference(0.05)
    ),
    callbacks=[PlotFitnessCallback()],
    optimization=Maximization(),
    selection=RouletteSelection(),
    crossover=SinglePointCrossover(0.80),
    mutation=BitFlipMutation(0.20),
)
ga.run()
print(ga.result)
