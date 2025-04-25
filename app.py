
from components.selection import RouletteSelection
from components.crossover import SinglePointCrossover
from components.mutation import BitFlipMutation
from components.chromosome_decoder import BinaryChromosomeDecoder
from components.optimization import Maximization
from components.termination_criterion import NumberOfGeneration, OrTermination, ThresholdDifference
from ga import GeneticAlgorithm

if __name__ == "__main__":
    # print(f"Solving a basic f(x1, x2) = x1^2 x2 + 2x1 - x2")
    # ga = GeneticAlgorithm(
    #     population_size=100,
    #     objective_function=lambda x: (x[0]**2)*x[1] + 2*x[0] - x[1],
    #     chromosome_decoder=BinaryChromosomeDecoder(
    #         number_of_bytes=6,
    #         number_of_decision_variables=2,
    #         lower_bounds=[2, -1],
    #         upper_bounds=[6, 4]
    #     ),
    #     termination=OrTermination(
    #         NumberOfGeneration(20),
    #         ThresholdDifference(0.05)
    #     ),
    #     optimization=Maximization(),
    #     selection=RouletteSelection(),
    #     crossover=SinglePointCrossover(0.85),
    #     mutation=BitFlipMutation(0.2),
    # )
    # ga.run()
    # print(ga.result)

    print(f"Laboratory Exercise 1")
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
        optimization=Maximization(),
        selection=RouletteSelection(),
        crossover=SinglePointCrossover(0.80),
        mutation=BitFlipMutation(0.20),
    )
    ga.run()
    print(ga.result)
