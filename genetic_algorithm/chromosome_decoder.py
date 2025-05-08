from .type import Chromosome
import random

class BaseChromosomeDecoder():
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
    
    def clamp_chromosome(self, chromosome: Chromosome) -> Chromosome:
        """
        Returns a valid chromosome that is in bound
        """
        return chromosome



class BinaryChromosomeDecoder(BaseChromosomeDecoder):
    def encode(self, value: list[float]) -> Chromosome:
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


class DenaryChromosomeDecoder(BaseChromosomeDecoder):
    def __init__(
        self,
        number_of_bytes: int,
        number_of_decision_variables: int,
        dp: int,
        lower_bounds: list[float],
        upper_bounds: list[float],
    ) -> None:
        super().__init__(
            number_of_bytes=number_of_bytes,
            number_of_decision_variables=number_of_decision_variables,
            lower_bounds=lower_bounds,
            upper_bounds=upper_bounds
        )
        assert dp > 0 and number_of_bytes > 1 and dp < number_of_bytes, "Invalid dp or number_of_bytes"
        self.dp = dp
        self.digit_bytes = number_of_bytes
        self.number_of_bytes = number_of_bytes + 1  # Including sign

    def encode(self, value: list[float]) -> Chromosome:
        chromosome: Chromosome = []

        if len(value) != self.number_of_decision_variables:
            raise ValueError(f"encode: Expected {self.number_of_decision_variables} values, got {len(value)}")

        for i, x_i in enumerate(value):
            if not (self.lower_bounds[i] <= x_i <= self.upper_bounds[i]):
                raise ValueError(f"encode: value[{i}] = {x_i} is out of bounds [{self.lower_bounds[i]}, {self.upper_bounds[i]}]")

            gene = self.__float_to_gene(x_i)
            chromosome.append(gene)

        return chromosome
    
    def decode(self, chromosome: Chromosome) -> list[float]:
        x = []
        for i, gene in enumerate(chromosome):
            sign = -1 if gene[0] == 1 else 1
            magnitude = sum([g * 10**j for j, g in enumerate(reversed(gene[1:]))])
            x_i = sign * magnitude / 10**self.dp
            x_i = min(max(x_i, self.lower_bounds[i]), self.upper_bounds[i])
            x.append(x_i)
        return x
    
    def random_chromosome(self) -> Chromosome:
        chromosome: Chromosome = []
        for i in range(self.number_of_decision_variables):
            lower = self.lower_bounds[i] * 10**self.dp
            upper = self.upper_bounds[i] * 10**self.dp
            value = (lower + random.random() * (upper - lower)) / (10**self.dp)
            gene = self.__float_to_gene(value)
            chromosome.append(gene)
        return chromosome

    def __float_to_gene(self, value: float) -> list[int]:
        sign = 0 if value >= 0 else 1
        value = abs(value)
        scaled = int(round(value * 10**self.dp))

        max_digits = 10**self.digit_bytes
        assert scaled < max_digits, f"{value} exceeds digit capacity for {self.digit_bytes} bytes"

        gene = [sign]
        divisor = 10**(self.digit_bytes - 1)
        for _ in range(self.digit_bytes):
            gene.append(scaled // divisor)
            scaled %= divisor
            divisor //= 10

        return gene
    
    def clamp_chromosome(self, chromosome: Chromosome) -> Chromosome:
        new_chromosome = []
        for i, gene in enumerate(chromosome):
            sign = -1 if gene[0] == 1 else 1
            magnitude = sum([g * 10**j for j, g in enumerate(reversed(gene[1:]))])
            x_i = sign * magnitude / 10**self.dp
            x_i = min(max(x_i, self.lower_bounds[i]), self.upper_bounds[i])
            new_gene = self.__float_to_gene(x_i)
            new_chromosome.append(new_gene)
        return new_chromosome
