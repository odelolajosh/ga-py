from type import Chromosome

class Mutation:
    def __init__(self, mutation_probability: float) -> None:
        self.mutation_probability = mutation_probability
    
    def mutate(parent1: Chromosome, parent2: Chromosome) -> tuple[Chromosome, Chromosome]:
        raise NotImplementedError()
