from .base import Callback

class PrintBestFitness(Callback):
    def on_generation_end(self, generation, population, best_fitness, best_individual):
        print(f"Generation {generation}: Best Fitness = {best_fitness}")

    def on_evolution_end(self, best_fitness, best_individual):
        print(f"Best Fitness = {best_fitness}")
