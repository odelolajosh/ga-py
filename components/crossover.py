from type import Chromosome

class Crossover:
    def __init__(self, crossover_probability: float) -> None:
        self.crossover_probability = crossover_probability
    
    def cross(parent1: Chromosome, parent2: Chromosome) -> tuple[Chromosome, Chromosome]:
        raise NotImplementedError()


class SinglePointCrossover(Crossover):
    def cross(parent1: Chromosome, parent2: Chromosome) -> tuple[Chromosome, Chromosome]:
        raise NotImplementedError()