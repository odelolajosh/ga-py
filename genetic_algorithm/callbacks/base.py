from ..type import Individual

class Callback:
    """
    Base class for callbacks
    """
    def on_generation_start(self, generation, best_fitness: float, best_individual: Individual, population: list[Individual]):
        pass

    def on_generation_end(self, generation, best_fitness: float, best_individual: Individual, population: list[Individual]):
        pass

    def on_evolution_end(self, generation, best_fitness: float, best_individual: Individual, population: list[Individual]):
        pass
