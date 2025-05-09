
from genetic_algorithm.selection import RouletteSelection
from genetic_algorithm.crossover import SinglePointCrossover
from genetic_algorithm.mutation import BitFlipMutation
from genetic_algorithm.chromosome_decoder import BinaryChromosomeDecoder, DenaryChromosomeDecoder
from genetic_algorithm.termination_criterion import NumberOfGeneration, OrTermination, ThresholdDifference
from ga import ga
from genetic_algorithm.callbacks.base import Callback
import matplotlib.pyplot as plt

class PlotFitnessCallback(Callback):
    def __init__(self):
        self.generations = []
        self.best_fitnesses = []

    def on_generation_end(self, generation: int, best_fitness: float, best_individual: list[float], population: list[list[int]]):
        self.generations.append(generation)
        self.best_fitnesses.append(best_fitness)

    def on_evolution_end(self, generation: int, best_fitness: float, best_individual: list[float], population: list[list[int]]):
        plt.figure(figsize=(10, 6))
        plt.plot(self.generations, self.best_fitnesses, marker='o')
        plt.title('Fitness vs Generation')
        plt.xlabel('Generation')
        plt.ylabel('Best Fitness')
        plt.grid(True)
        plt.show()


# Solving a basic optimization problem
# print(f"Solving a basic f(x1, x2) = x1^2 x2 + 2x1 - x2")

# result1 = ga(
#     population_size=100,
#     objective_function=lambda x: (x[0]**2)*x[1] + 2*x[0] - x[1],
#     number_of_decision_variables=2,
#     lower_bounds=[2, -1],
#     upper_bounds=[6, 4],
#     chromosome_decoder=BinaryChromosomeDecoder(
#         number_of_bytes=6,
#         number_of_decision_variables=2,
#         lower_bounds=[2, -1],
#         upper_bounds=[6, 4]
#     ),
#     termination=OrTermination(
#         NumberOfGeneration(100),
#         ThresholdDifference(0.05)
#     ),
#     callbacks=[PlotFitnessCallback()],
#     selection=RouletteSelection(),
#     crossover=SinglePointCrossover(0.85),
#     mutation=BitFlipMutation(0.20),
# )
# print(result1)

print("Laboratory Exercise 1")
def f(x):
    return 2*x[0]*x[1]*x[2] - 4*x[0]*x[2] - 2*x[1]*x[2] + x[0]**2 + x[1]**2 + x[2]**2 - 2*x[0] - 4*x[1] + 4*x[2]
result = ga(
    population_size=50,
    objective_function=f,
    number_of_decision_variables=3,
    lower_bounds=[10, 0, -20],
    upper_bounds=[90, 90, 60],
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
    # callbacks=[PlotFitnessCallback()],
    optimization_sense="maximize",
    selection=RouletteSelection(),
    crossover=SinglePointCrossover(0.80),
    mutation=BitFlipMutation(0.20),
)
print(result)

print("Laboratory Exercise 2")
def f(x):
    return 2*x[0]*x[1]*x[2] - 4*x[0]*x[2] - 2*x[1]*x[2] + x[0]**2 + x[1]**2 + x[2]**2 - 2*x[0] - 4*x[1] + 4*x[2]
result = ga(
    population_size=10,
    objective_function=f,
    number_of_decision_variables=3,
    lower_bounds=[10, 0, -20],
    upper_bounds=[90, 90, 60],
    chromosome_decoder=DenaryChromosomeDecoder(
        number_of_bytes=5,
        number_of_decision_variables=3,
        lower_bounds=[10, 0, -20],
        upper_bounds=[90, 90, 60],
        dp=3,
    ),
    termination=OrTermination(
        NumberOfGeneration(100),
        ThresholdDifference(0.05)
    ),
    # callbacks=[PlotFitnessCallback()],
    optimization_sense="maximize",
    selection=RouletteSelection(),
    crossover=SinglePointCrossover(0.80),
    mutation=BitFlipMutation(0.20),
)
print(result)
