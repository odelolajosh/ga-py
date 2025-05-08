import random

from genetic_algorithm.type import Chromosome
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

        self.number_of_generation = 0
        self.population: list[Chromosome] = []
        self.optimal_fitness: float = None
        self.optimal_chromosome: Chromosome = None
    
    def run(self):
        # initialize population
        self.population = []
        for _ in range(self.population_size):
            random_chromosome = self.chromosome_decoder.random_chromosome()
            self.population.append(random_chromosome)

        # while termination criterion is met
        while not self.terminator.should_terminate(self.number_of_generation, self.optimal_fitness):
            # Start of generation
            for cb in self.callbacks:
                cb.on_generation_start(self.number_of_generation, self.population)

            # Evaluate population
            population_fitness = []
            best_chromosome = None
            best_fitness = None
            
            for chromosome in self.population:
                # Decode each chromosome
                values = self.chromosome_decoder.decode(chromosome)
                # Get fitness for each chromosome
                fitness = self.objective_function(values)
                population_fitness.append(fitness)

                # Update the optimal fitness chromosome
                if self.optimization.is_optimal(fitness, best_fitness):
                    best_fitness = fitness
                    best_chromosome = chromosome
            
            self.optimal_fitness = best_fitness
            self.optimal_chromosome = best_chromosome

            # Do selection
            self.population = self.selector.select(self.population, population_fitness)

            self.number_of_generation += 1

            new_population = []
            while len(new_population) < self.population_size:
                # select two different parents, randomly
                parent1 = random.choice(self.population)
                parent2 = random.choice(self.population)

                # crossover
                child1, child2 = self.crossover_strategy.cross(parent1, parent2)

                # mutation
                child1, child2 = self.mutation_strategy.mutate(child1, child2)

                child1 = self.chromosome_decoder.clamp_chromosome(child1)
                child2 = self.chromosome_decoder.clamp_chromosome(child2)

                # add the children to the new population
                new_population.append(child1)

                if len(new_population) < self.population_size:
                    new_population.append(child2)

            self.population = new_population

            # End of generation
            for cb in self.callbacks:
                cb.on_generation_end(
                    self.number_of_generation,
                    self.population,
                    self.optimal_fitness,
                    self.chromosome_decoder.decode(self.optimal_chromosome)
                )

        # End of evolution
        for cb in self.callbacks:
            cb.on_evolution_end(
                self.optimal_fitness,
                self.chromosome_decoder.decode(self.optimal_chromosome)
            )

    @property
    def result(self):
        if not self.optimal_chromosome:
            print("(Warning) Genetic Algorithm has not been run yet. Call run() method first")
        return self.optimal_fitness, self.chromosome_decoder.decode(self.optimal_chromosome)
