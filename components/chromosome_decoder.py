from components.type import Chromosome

class ChromosomeDecoder():
    def __init__(
        self,
        number_of_bytes: int,
        number_of_decision_variables: int,
        lower_bounds: list[float],
        upper_bounds: list[float],
    ) -> None:
        self.number_of_bytes = number_of_bytes
        self.number_of_decision_variables = number_of_decision_variables
        self.lower_bounds = lower_bounds
        self.upper_bounds = upper_bounds
    
    def decode(self, chromosome: Chromosome) -> list[float]:
        return [0] * self.number_of_decision_variables
    
    def random_chromosome() -> Chromosome:
        """
        Generates a random chromosome
        """
        raise NotImplementedError()


class BinaryChromosomeDecoder(ChromosomeDecoder):
    def decode(self, chromosome: Chromosome) -> list[float]:
        return [0] * self.number_of_decision_variables
    
    def random_chromosome() -> Chromosome:
        raise NotImplementedError()


class DenaryChromosomeDecoder(ChromosomeDecoder):
    def decode(self, chromosome: Chromosome) -> list[float]:
        return [0] * self.number_of_decision_variables
    
    def random_chromosome() -> Chromosome:
        raise NotImplementedError()
