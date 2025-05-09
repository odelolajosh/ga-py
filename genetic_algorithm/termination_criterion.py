class BaseTerminationCriterion:
    def should_terminate(self, number_of_generation: int, optimal_fitness: float) -> bool:
        return False


class NumberOfGeneration(BaseTerminationCriterion):
    def __init__(self, max_number_of_generation) -> None:
        self.max_number_of_generation = max_number_of_generation
    
    def should_terminate(self, number_of_generation: int, optimal_fitness: float) -> bool:
        return number_of_generation >= self.max_number_of_generation


class ThresholdDifference(BaseTerminationCriterion):
    def __init__(self, threshold: float):
        self.threshold = threshold
        self.previous_optimal_fitness = None
    
    def should_terminate(self, number_of_generation: int, optimal_fitness: float) -> bool:
        if self.previous_optimal_fitness is None:
            self.previous_optimal_fitness = optimal_fitness
            return False

        is_within_threshold =  abs(optimal_fitness - self.previous_optimal_fitness) <= self.threshold
        self.previous_optimal_fitness = optimal_fitness
        return is_within_threshold

class OrTermination(BaseTerminationCriterion):
    def __init__(self, *args) -> None:
        super().__init__()

        self.terminators: list[BaseTerminationCriterion] = args;

    def should_terminate(self, number_of_generation: int, optimal_fitness: float) -> bool:
        for terminator in self.terminators:
            if terminator.should_terminate(number_of_generation, optimal_fitness):
                return True
        return False
