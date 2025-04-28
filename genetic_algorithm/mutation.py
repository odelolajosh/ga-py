from .type import Chromosome
import random

class BaseMutation:
    def __init__(self, mutation_probability: float) -> None:
        if mutation_probability < 0 or mutation_probability > 1:
            raise ValueError("mutation_rate must be between 0 and 1")
        
        self.mutation_probability = mutation_probability
    
    def mutate(self, parent1: Chromosome, parent2: Chromosome) -> tuple[Chromosome, Chromosome]:
        raise NotImplementedError()

    def _can_mutate(self):
        return random.random() < self.mutation_probability


class BitFlipMutation(BaseMutation):
    def mutate(self, parent1: Chromosome, parent2: Chromosome) -> tuple[Chromosome, Chromosome]:
        assert len(parent1) == len(parent2), "Parents must have the same number of decision variables"
        assert all([len(g1) == len(g2) for g1, g2 in zip(parent1, parent2)]), "Parents must have same number of bytes"

        i = random.randint(0, len(parent1) - 1)
        child1, child2 = parent1.copy(), parent2.copy()
        child1[i], child2[i] = child2[i], child1[i]
        return child1, child2
