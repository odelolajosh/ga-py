import random

class BaseCrossover:
    def __init__(self, crossover_probability: float) -> None:
        self.crossover_probability = crossover_probability
    
    def cross(self, parent1: list[list[int]], parent2: list[list[int]]) -> tuple[list[list[int]], list[list[int]]]:
        raise NotImplementedError()


class SinglePointCrossover(BaseCrossover):
    def cross(self, parent1: list[list[int]], parent2: list[list[int]]) -> tuple[list[list[int]], list[list[int]]]:
        assert len(parent1) == len(parent2), "Parents must have the same number of decision variables"

        child1, child2 = [], []
        for gene1, gene2 in zip(parent1, parent2):
            assert len(gene1) == len(gene2), "Genes must have the same size"
            if random.random() < self.crossover_probability:
                crossover_point = random.randrange(1, len(gene1))
                child_gene1 = gene1[:crossover_point] + gene2[crossover_point:]
                child_gene2 = gene2[:crossover_point] + gene1[crossover_point:]
                child1.append(child_gene1)
                child2.append(child_gene2)
            else:
                child1.append(gene1)
                child2.append(gene2)

        return child1, child2
