import random
import matplotlib.pyplot as plt
from prettytable import PrettyTable

type Individual = list[float]
type Chromosome = list[list[int]]

def roulette_select(population: list[Chromosome], population_fitness: list[float]) -> list[Chromosome]:
    roulette_wheel = []
    cumulative_fitness = 0

    for fitness in population_fitness:
        cumulative_fitness += fitness
        roulette_wheel.append(cumulative_fitness)

    total_fitness = cumulative_fitness

    if total_fitness == 0:
        return random.choices(population, k=len(population))

    selection = []
    while len(selection) < len(population):
        spin = random.uniform(0, total_fitness)
        for i in range(len(roulette_wheel)):
            if spin < roulette_wheel[i]:
                selection.append(population[i])
                break

    return selection


def cross(crossover_probability: float, parent1: Chromosome, parent2: Chromosome) -> tuple[Chromosome, Chromosome]:
    assert len(parent1) == len(parent2), "Parents must have the same number of decision variables"

    child1, child2 = [], []
    for gene1, gene2 in zip(parent1, parent2):
        assert len(gene1) == len(gene2), "Genes must have the same size"
        if random.random() < crossover_probability:
            crossover_point = random.randrange(1, len(gene1))
            child_gene1 = gene1[:crossover_point] + gene2[crossover_point:]
            child_gene2 = gene2[:crossover_point] + gene1[crossover_point:]
            child1.append(child_gene1)
            child2.append(child_gene2)
        else:
            child1.append(gene1)
            child2.append(gene2)

    return child1, child2


def mutate(mutation_probability: float, parent1: Chromosome, parent2: Chromosome) -> tuple[Chromosome, Chromosome]:
    assert len(parent1) == len(parent2), "Parents must have the same number of decision variables"

    child1, child2 = [], []
    for gene1, gene2 in zip(parent1, parent2):
        assert len(gene1) == len(gene2), "Genes must have the same size"
        if random.random() < mutation_probability:
            i = random.randint(0, len(parent1) - 1)
            child_gene1, child_gene2 = gene1.copy(), gene2.copy()
            child_gene1[i], child_gene2[i] = child_gene2[i], child_gene1[i]
            child1.append(child_gene1)
            child2.append(child_gene2)
        else:
            child1.append(gene1)
            child2.append(gene2)

    return child1, child2


def encode(
        value: Individual,
        number_of_decision_variables,
        lower_bounds,
        upper_bounds,
        number_of_bytes
    ) -> Chromosome:
    assert len(value) == number_of_decision_variables, f"encode: value must be an array of {number_of_decision_variables} length"
    assert len(lower_bounds) == number_of_decision_variables, f"encode: lower bounds must have {number_of_decision_variables} values"
    assert len(upper_bounds) == number_of_decision_variables, f"encode: upper bounds must have {number_of_decision_variables} values"

    chromosome = []
    
    for i, x_i in enumerate(value):
        if x_i < lower_bounds[i] or x_i > upper_bounds[i]:
            raise ValueError(f"encode: value[{i}] is not within the boundary [{lower_bounds[i]}, {upper_bounds[i]}]")

        fraction = (x_i - lower_bounds[i]) / (upper_bounds[i] - lower_bounds[i])
        denary = 0 + (2**number_of_bytes - 1) * fraction

        # convert denary to binary
        binary = []
        while denary > 0:
            denary, remainder = divmod(denary, 2)
            binary.append(int(remainder))
        
        # pad with zero to make binary exactly number_of_bytes long
        while len(binary) < number_of_bytes:
            binary.append(0)
        
        binary.reverse()
        chromosome.append(binary)

    return chromosome


def decode(
        chromosome: Chromosome,
        number_of_decision_variables,
        lower_bounds,
        upper_bounds,
        number_of_bytes
    ) -> Individual:
    assert len(chromosome) == number_of_decision_variables, ""

    x = []
    for i, gene in enumerate(chromosome):
        denary = sum([g * 2**j for j, g in enumerate(reversed(gene))])
        fraction = denary / (2**number_of_bytes - 1)
        x_i = lower_bounds[i] + (upper_bounds[i] - lower_bounds[i]) * fraction
        x.append(x_i)
    
    return x


def ga(
        objective_function,
        number_of_decision_variables,
        lower_bounds,
        upper_bounds,
        population_size = 50,
        number_of_bytes = 5,
        crossover_probability = 0.80,
        mutation_probability = 0.20,
        max_number_of_generation = 10,
        threshold=0.05,
        on_generation_start = None,
        on_generation_end = None,
    ):
    assert len(lower_bounds) == number_of_decision_variables, f"ga: lower bounds must have {number_of_decision_variables} values"
    assert len(upper_bounds) == number_of_decision_variables, f"ga: upper bounds must have {number_of_decision_variables} values"
    
    number_of_generation = 0
    population: list[Individual] = []
    previous_optimal_fitness = None
    optimal_fitness: float = None
    optimal_individual: Individual = None

    # initialize population
    population = []
    for _ in range(population_size):
        individual = [random.uniform(lower_bounds[i], upper_bounds[i]) for i in range(number_of_decision_variables)]
        population.append(individual)

    while True:
        has_reached_max_generation = number_of_generation >= max_number_of_generation
        has_reached_optimal_threshold = (
            previous_optimal_fitness is not None
            and abs(optimal_fitness - previous_optimal_fitness) <= threshold
        )

        if has_reached_max_generation or has_reached_optimal_threshold:
            break

        previous_optimal_fitness = optimal_fitness;

        # Start of generation
        if on_generation_start:
            on_generation_start(
                number_of_generation,
                optimal_fitness,
                optimal_individual,
                population
            )

        # Evaluate population
        population_fitness = []
        best_individual = None
        best_fitness = None
        
        for individual in population:
            fitness = objective_function(individual)
            population_fitness.append(fitness)

            # Update the optimal fitness individual with max fitness
            if best_fitness is None or fitness > best_fitness:
                best_fitness = fitness
                best_individual = individual
        
        optimal_fitness = best_fitness
        optimal_individual = best_individual

        # Do selection
        population = roulette_select(population, population_fitness)

        number_of_generation += 1

        new_population = []
        while len(new_population) < population_size:
            # select two different parents, randomly
            parent1 = random.choice(population)
            parent2 = random.choice(population)

            parent1 = encode(parent1, number_of_decision_variables, lower_bounds, upper_bounds, number_of_bytes)
            parent2 = encode(parent2, number_of_decision_variables, lower_bounds, upper_bounds, number_of_bytes)

            # crossover
            child1, child2 = cross(crossover_probability, parent1, parent2)

            # mutation
            child1, child2 = mutate(mutation_probability, child1, child2)

            child1 = decode(child1, number_of_decision_variables, lower_bounds, upper_bounds, number_of_bytes)
            child2 = decode(child2, number_of_decision_variables, lower_bounds, upper_bounds, number_of_bytes)

            # add the children to the new population
            new_population.append(child1)

            if len(new_population) < population_size:
                new_population.append(child2)

        population = new_population

        # End of generation
        if on_generation_end:
            on_generation_end(
                number_of_generation,
                optimal_fitness,
                optimal_individual,
                population
            )
    
    return optimal_fitness, optimal_individual


def f(x):
    return 2*x[0]*x[1]*x[2] - 4*x[0]*x[2] - 2*x[1]*x[2] + x[0]**2 + x[1]**2 + x[2]**2 - 2*x[0] - 4*x[1] + 4*x[2]


logs = {
    "generations": [],
    "best_fitnesses_per_generation": [],
    "best_individuals_per_generation": [],
}

table = PrettyTable()
table.field_names = ["Generation", "Best Individual", "Best fitness"]

def on_generation_end(generation, best_fitness: float, best_individual: Individual, population: list[Individual]):
    logs["generations"].append(generation)
    logs["best_individuals_per_generation"].append(best_individual.copy())
    logs["best_fitnesses_per_generation"].append(best_fitness)

    # Add to table
    table.add_row([generation, best_individual, best_fitness])

result1 = ga(
    population_size=100,
    objective_function=f,
    number_of_bytes=10,
    number_of_decision_variables=3,
    lower_bounds=[10, 0, -20],
    upper_bounds=[90, 90, 60],
    max_number_of_generation=50,
    on_generation_end=on_generation_end
)

print(result1)

print(table)

plt.figure(figsize=(10, 6))
plt.plot(logs["generations"], logs["best_fitnesses_per_generation"], marker='o', label='Best Fitness')
plt.title('Genetic Algorithm: Fitness vs Generation')
plt.xlabel('Generation')
plt.ylabel('Fitness')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()