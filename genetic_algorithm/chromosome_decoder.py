from .type import Chromosome
import random

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
    
    def encode(self, value: list[float]) -> list[int]:
        """
        Encode a list of decision variable values into chromosome
        """
        raise NotImplementedError()
    
    def decode(self, chromosome: list) -> list[float]:
        """
        Decode chromosome to a list of decision variables
        """
        raise NotImplementedError()
    
    def random_chromosome(self) -> Chromosome:
        """
        Generates a random chromosome
        """
        raise NotImplementedError()


class BinaryChromosomeDecoder(ChromosomeDecoder):
    def encode(self, value: list[float]) -> list[int]:
        chromosome = []
        
        if len(value) != self.number_of_decision_variables:
            raise ValueError(f"encode: value must be an array of {self.number_of_decision_variables} length")
        
        for i, x_i in enumerate(value):
            if x_i < self.lower_bounds[i] or x_i > self.upper_bounds[i]:
                raise ValueError(f"encode: value[{i}] is not within the boundary [{self.lower_bounds[i]}, {self.upper_bounds[i]}]")

            fraction = (x_i - self.lower_bounds[i]) / (self.upper_bounds[i] - self.lower_bounds[i])
            denary = 0 + (2**self.number_of_bytes - 1) * fraction

            # convert denary to binary
            binary = []
            while denary > 0:
                denary, remainder = divmod(denary, 2)
                binary.append(int(remainder))
            
            # pad with zero to make binary exactly number_of_bytes long
            while len(binary) < self.number_of_bytes:
                binary.append(0)
            
            binary.reverse()
            chromosome.append(binary)

        return chromosome
    
    def decode(self, chromosome: Chromosome) -> list[float]:
        assert len(chromosome) == self.number_of_decision_variables, ""
        assert all([len(gene) == self.number_of_bytes for gene in chromosome]), ""

        x = []
        for i, gene in enumerate(chromosome):
            denary = sum([g * 2**j for j, g in enumerate(reversed(gene))])
            fraction = denary / (2**self.number_of_bytes - 1)
            x_i = self.lower_bounds[i] + (self.upper_bounds[i] - self.lower_bounds[i]) * fraction
            x.append(x_i)
        
        return x
    
    def random_chromosome(self) -> Chromosome:
        chromosome = []
        for _ in range(self.number_of_decision_variables):
            gene = [random.randint(0, 1) for _ in range(self.number_of_bytes)]
            chromosome.append(gene)
        return chromosome


class DenaryChromosomeDecoder(ChromosomeDecoder):
    def encode(self, value: list[float]) -> list[int]:
        raise NotImplementedError()
    
    def decode(self, chromosome: list) -> list[float]:
        raise NotImplementedError()
    
    def random_chromosome(self) -> Chromosome:
        raise NotImplementedError()
