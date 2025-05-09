import random

class BaseMutation:
    def __init__(self, mutation_probability: float) -> None:
        if mutation_probability < 0 or mutation_probability > 1:
            raise ValueError("mutation_rate must be between 0 and 1")
        
        self.mutation_probability = mutation_probability
    
    def mutate(self, parent1: list[list[int]], parent2: list[list[int]]) -> tuple[list[list[int]], list[list[int]]]:
        raise NotImplementedError()


class BitFlipMutation(BaseMutation):
    def mutate(self, parent1: list[list[int]], parent2: list[list[int]]) -> tuple[list[list[int]], list[list[int]]]:
        assert len(parent1) == len(parent2), "Parents must have the same number of decision variables"

        child1, child2 = [], []
        for gene1, gene2 in zip(parent1, parent2):
            assert len(gene1) == len(gene2), "Genes must have the same size"
            if random.random() < self.mutation_probability:
                i = random.randint(0, len(parent1) - 1)
                child_gene1, child_gene2 = gene1.copy(), gene2.copy()
                child_gene1[i], child_gene2[i] = child_gene2[i], child_gene1[i]
                child1.append(child_gene1)
                child2.append(child_gene2)
            else:
                child1.append(gene1)
                child2.append(gene2)

        return child1, child2
