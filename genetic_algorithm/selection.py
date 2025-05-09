import numpy as np
from numpy.typing import NDArray

class BaseSelection:
    def select(self, population: NDArray[np.float64], population_fitness: NDArray[np.float64]) -> NDArray[np.float64]:
        raise NotImplementedError()


class RouletteSelection(BaseSelection):
    def select(self, population: NDArray[np.float64], population_fitness: NDArray[np.float64]) -> NDArray[np.float64]:
        offset = min(np.min(population_fitness), 0) * -1
        fitness = population_fitness + offset
        total_fitness = np.sum(fitness)

        if total_fitness == 0:
            indices = np.random.choice(len(population), size=len(population), replace=True)
            return population[indices]

        probabilities = fitness / total_fitness

        selected_indices = np.random.choice(
            len(population), size=len(population), p=probabilities, replace=True
        )

        return population[selected_indices]
