from components.type import Chromosome
import random

class Crossover:
    def __init__(self, crossover_probability: float) -> None:
        self.crossover_probability = crossover_probability
    
    def cross(self, parent1: Chromosome, parent2: Chromosome) -> tuple[Chromosome, Chromosome]:
        raise NotImplementedError()
    
    def _can_cross(self):
        return random.random() < self.crossover_probability


class SinglePointCrossover(Crossover):
    def cross(self, parent1: Chromosome, parent2: Chromosome) -> tuple[Chromosome, Chromosome]:
        if self._can_cross():
            crossover_point = random.randint(0, len(parent1) - 1)
            child1 = parent1[:crossover_point] + parent2[crossover_point:]
            child2 = parent2[:crossover_point] + parent1[crossover_point:]
            return child1, child2
        else:
            return parent1, parent2