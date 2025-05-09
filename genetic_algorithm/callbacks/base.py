class Callback:
    """
    Base class for callbacks
    """
    def on_generation_start(self, generation: int, best_fitness: float, best_individual: list[float], population: list[list[int]]):
        pass

    def on_generation_end(self, generation: int, best_fitness: float, best_individual: list[float], population: list[list[int]]):
        pass

    def on_evolution_end(self, generation: int, best_fitness: float, best_individual: list[float], population: list[list[int]]):
        pass
