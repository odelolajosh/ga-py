class Callback:
    """
    Base class for callbacks
    """
    def on_generation_start(self, generation, population):
        pass

    def on_generation_end(self, generation, population, best_fitness, best_individual):
        pass

    def on_evolution_end(self, best_fitness, best_individual):
        pass
