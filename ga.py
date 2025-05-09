from typing import Literal
import numpy as np
from numpy.typing import NDArray

from genetic_algorithm.selection import BaseSelection, RouletteSelection
from genetic_algorithm.crossover import BaseCrossover, SinglePointCrossover
from genetic_algorithm.mutation import BaseMutation, BitFlipMutation
from genetic_algorithm.chromosome_decoder import BaseChromosomeDecoder
from genetic_algorithm.termination_criterion import BaseTerminationCriterion
from genetic_algorithm.callbacks.base import Callback

OptimizationSense = Literal["minimize", "maximize"]

def ga(
    population_size: int,
    objective_function,
    number_of_decision_variables,
    lower_bounds: list[int],
    upper_bounds: list[int],
    chromosome_decoder: BaseChromosomeDecoder,
    termination: BaseTerminationCriterion,
    optimization_sense: OptimizationSense = "maximization",
    selection: BaseSelection = RouletteSelection(),
    crossover: BaseCrossover = SinglePointCrossover(0.85),
    mutation: BaseMutation = BitFlipMutation(0.2),
    callbacks: list[Callback] = []
) -> None:
    # chromosome_decoder.lower_bounds = lower_bounds
    # chromosome_decoder.upper_bounds = upper_bounds
    # chromosome_decoder.number_of_decision_variables = number_of_decision_variables

    lower_bounds = np.array(lower_bounds)
    upper_bounds = np.array(upper_bounds)

    number_of_generation = 0
    population: NDArray[np.float64] = np.empty((population_size, number_of_decision_variables))
    optimal_fitness: np.float64 = None
    optimal_chromosome: NDArray[np.float64] = np.empty(number_of_decision_variables)

    # initialize population
    random_matrix = np.random.rand(population_size, number_of_decision_variables)
    population = lower_bounds + (upper_bounds - lower_bounds) * random_matrix

    # while termination criterion is met
    while not termination.should_terminate(number_of_generation, optimal_fitness):
        # Start of generation
        for cb in callbacks:
            cb.on_generation_start(
                number_of_generation,
                float(optimal_fitness) if optimal_fitness else None,
                list(optimal_chromosome),
                list(population),
            )

        # Evaluate population
        population_fitness = np.apply_along_axis(objective_function, axis=1, arr=population)
        best_index = np.argmax(population_fitness) if optimization_sense == "maximize" else np.argmax(population_fitness)
        optimal_chromosome, optimal_fitness = population[best_index], population_fitness[best_index]

        # Do selection
        population = selection.select(population, population_fitness)

        number_of_generation += 1

        new_population = []

        while len(new_population) < population_size:
            # select two different parents, randomly
            i1, i2 = np.random.choice(len(population), size=2, replace=False)
            parent1 = population[i1]
            parent2 = population[i2]

            parent1 = chromosome_decoder.encode(parent1.tolist())
            parent2 = chromosome_decoder.encode(parent2.tolist())

            # crossover
            child1, child2 = crossover.cross(parent1, parent2)

            # mutation
            child1, child2 = mutation.mutate(child1, child2)

            child1 = chromosome_decoder.decode(child1)
            child2 = chromosome_decoder.decode(child2)

            # add the children to the new population
            new_population.append(child1)
            if len(new_population) < population_size:
                new_population.append(child2)

        population = np.array(new_population, dtype=np.float64)

        # End of generation
        for cb in callbacks:
            cb.on_generation_end(
                number_of_generation,
                float(optimal_fitness) if optimal_fitness else None,
                list(optimal_chromosome),
                list(population),
            )

    # End of evolution
    for cb in callbacks:
        cb.on_evolution_end(
            number_of_generation,
            float(optimal_fitness) if optimal_fitness else None,
            list(optimal_chromosome),
            list(population),
        )
    
    return float(optimal_fitness), optimal_chromosome.tolist()
