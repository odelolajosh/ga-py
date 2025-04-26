from .base import Callback

def on_generation_end(fn):
    class FunctionalCallback(Callback):
        def on_generation_end(self, generation, population, best_individual):
            fn(generation, population, best_individual)
    return FunctionalCallback()
