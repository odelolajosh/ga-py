from type import Chromosome

class Crossing:
    def __init__(self, crossing_probability: float) -> None:
        self.crossing_probability = crossing_probability
    
    def cross(parent1: Chromosome, parent2: Chromosome) -> tuple[Chromosome, Chromosome]:
        raise NotImplementedError()


class SinglePointCrossing(Crossing):
    def cross(parent1: Chromosome, parent2: Chromosome) -> tuple[Chromosome, Chromosome]:
        raise NotImplementedError()