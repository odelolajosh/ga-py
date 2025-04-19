import random

from components.type import Chromosome
from components.selection import Selection, RouletteSelection
from components.crossing import Crossing, SinglePointCrossing
from components.mutation import Mutation
from components.chromosome_decoder import ChromosomeDecoder, BinaryChromosomeDecoder
from components.optimization import Optimization, Maximization
from components.termination_criterion import TerminationCriterion, NumberOfGeneration


class GeneticAlgorithm:
    def __init__(
        self,
        population_size: int,
        objective_function,
        chromosome_decoder: ChromosomeDecoder,
        terminator: TerminationCriterion,
        optimization: Optimization = Maximization(),
        selector: Selection = RouletteSelection(),
        crossing_strategy: Crossing = SinglePointCrossing(0.85),
        mutation_strategy: Mutation = Mutation(),
    ) -> None:
        self.population_size = population_size
        self.optimization = optimization
        self.chromosome_decoder = chromosome_decoder
        self.selector = selector
        self.crossing_strategy = crossing_strategy
        self.mutation_strategy = mutation_strategy
        self.terminator = terminator
        self.objective_function = objective_function

        self.number_of_generation = 0
        self.population: list[Chromosome] = None
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
            # Evaluate population
            population_fitness = []
            for chromosome in self.population:
                # Decode each chromosome
                values = self.chromosome_decoder.decode(chromosome)
                # Get fitness for each chromosome
                fitness = self.objective_function(values)
                population_fitness.append(fitness)

                # Update the optimal fitness chromosome
                if self.optimization.is_optimal(fitness, self.optimal_fitness):
                    self.optimal_fitness = fitness
                    self.optimal_chromosome = chromosome
            
            # Do selection
            self.population = self.selector.select(self.population, population_fitness)

            self.number_of_generation += 1

            new_population = []
            while len(new_population) < self.parameter.population_size:
                # select two different parents, randomly
                parent1 = random.choice(self.population)
                parent2 = random.choice(self.population)

                # crossover
                child1, child2 = self.crossing_strategy.cross(parent1, parent2)

                # mutation
                child1, child2 = self.mutation_strategy.mutate(child1, child1)

                # add the children to the new population
                new_population.append(child1)

                if len(new_population) < self.parameter.population_size:
                    new_population.append(child2)

            self.population = new_population

    @property
    def result(self):
        if not self.optimal_chromosome:
            print("(Warning) Genetic Algorithm has not been run yet. Call run() method first")
        return self.optimal_fitness, self.chromosome_decoder.decode(self.optimal_chromosome)


if __name__ == "__main__":
    print(f"Solving a basic f(x1, x2) = x1^2 x2 + 2x1 - x2")
    ga = GeneticAlgorithm(
        population_size=100,
        objective_function=lambda x: (x[0]**2)*x[1] + 2*x[0] - x[1],
        chromosome_decoder=BinaryChromosomeDecoder(
            number_of_bytes=6,
            number_of_decision_variables=2,
            lower_bounds=[2, -1],
            upper_bounds=[6, 4]
        ),
        terminator=NumberOfGeneration(10),
        optimization=Maximization(),
        selector=RouletteSelection(),
        crossing_strategy=SinglePointCrossing(0.85),
        mutation_strategy=Mutation(0.2),
    )
    ga.run()
    print(ga.result)
