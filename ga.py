import random

from genetic_algorithm.type import Individual
from genetic_algorithm.selection import BaseSelection, RouletteSelection
from genetic_algorithm.crossover import BaseCrossover, SinglePointCrossover
from genetic_algorithm.mutation import BaseMutation, BitFlipMutation
from genetic_algorithm.chromosome_decoder import BaseChromosomeDecoder
from genetic_algorithm.optimization import BaseOptimization, Maximization
from genetic_algorithm.termination_criterion import BaseTerminationCriterion
from genetic_algorithm.callbacks.base import Callback


class GeneticAlgorithm:
    def __init__(
        self,
        population_size: int,
        objective_function,
        chromosome_decoder: BaseChromosomeDecoder,
        termination: BaseTerminationCriterion,
        optimization: BaseOptimization = Maximization(),
        selection: BaseSelection = RouletteSelection(),
        crossover: BaseCrossover = SinglePointCrossover(0.85),
        mutation: BaseMutation = BitFlipMutation(0.2),
        callbacks: list[Callback] = []
    ) -> None:
        self.population_size = population_size
        self.optimization = optimization
        self.chromosome_decoder = chromosome_decoder
        self.selector = selection
        self.crossover_strategy = crossover
        self.mutation_strategy = mutation
        self.terminator = termination
        self.objective_function = objective_function
        self.callbacks = callbacks

        self.lower_bounds = chromosome_decoder.lower_bounds
        self.upper_bounds = chromosome_decoder.upper_bounds
        self.number_of_decision_variables = chromosome_decoder.number_of_decision_variables

        self.number_of_generation = 0
        self.population: list[Individual] = []
        self.optimal_fitness: float = None
        self.optimal_individual: Individual = None
    
    def run(self):
        # initialize population
        self.population = []
        for _ in range(self.population_size):
            individual = [random.uniform(self.lower_bounds[i], self.upper_bounds[i]) for i in range(self.number_of_decision_variables)]
            self.population.append(individual)

        # while termination criterion is met
        while not self.terminator.should_terminate(self.number_of_generation, self.optimal_fitness):
            # Start of generation
            for cb in self.callbacks:
                cb.on_generation_start(
                    self.number_of_generation,
                    self.optimal_fitness,
                    self.optimal_individual,
                    self.population
                )

            # Evaluate population
            population_fitness = []
            best_individual = None
            best_fitness = None
            
            for chromosome in self.population:
                fitness = self.objective_function(chromosome)
                population_fitness.append(fitness)

                # Update the optimal fitness chromosome
                if self.optimization.is_optimal(fitness, best_fitness):
                    best_fitness = fitness
                    best_individual = chromosome
            
            self.optimal_fitness = best_fitness
            self.optimal_individual = best_individual

            # Do selection
            self.population = self.selector.select(self.population, population_fitness)

            self.number_of_generation += 1

            new_population = []
            while len(new_population) < self.population_size:
                # select two different parents, randomly
                parent1 = random.choice(self.population)
                parent2 = random.choice(self.population)

                parent1 = self.chromosome_decoder.encode(parent1)
                parent2 = self.chromosome_decoder.encode(parent2)

                # crossover
                child1, child2 = self.crossover_strategy.cross(parent1, parent2)

                # mutation
                child1, child2 = self.mutation_strategy.mutate(child1, child2)

                child1 = self.chromosome_decoder.decode(child1)
                child2 = self.chromosome_decoder.decode(child2)

                # add the children to the new population
                new_population.append(child1)

                if len(new_population) < self.population_size:
                    new_population.append(child2)

            self.population = new_population

            # End of generation
            for cb in self.callbacks:
                cb.on_generation_end(
                    self.number_of_generation,
                    self.optimal_fitness,
                    self.optimal_individual,
                    self.population
                )

        # End of evolution
        for cb in self.callbacks:
            cb.on_evolution_end(
                self.number_of_generation,
                self.optimal_fitness,
                self.optimal_individual,
                self.population
            )

    @property
    def result(self):
        if not self.optimal_individual:
            print("(Warning) Genetic Algorithm has not been run yet. Call run() method first")
        return self.optimal_fitness, self.optimal_individual
