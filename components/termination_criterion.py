class TerminationCriterion:
    def should_terminate(self, number_of_generation: int, optimal_fitness: float) -> bool:
        return False


class NumberOfGeneration(TerminationCriterion):
    def __init__(self, max_number_of_generation) -> None:
        self.max_number_of_generation = max_number_of_generation
    
    def should_terminate(self, number_of_generation: int, optimal_fitness: float) -> bool:
        return number_of_generation >= self.max_number_of_generation


class ThresholdDifference(TerminationCriterion):
    def __init__(self, threshold: float):
        self.threshold = threshold
    
    def should_terminate(self, number_of_generation: int, optimal_fitness: float) -> bool:
        return False
