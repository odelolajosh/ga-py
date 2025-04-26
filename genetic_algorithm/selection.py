from .type import Chromosome
import random

class Selection:
    def select(self, population: list[Chromosome], population_fitness: list[float]) -> list[Chromosome]:
        raise NotImplementedError()


class RouletteSelection:
    def select(self, population: list[Chromosome], population_fitness: list[float]) -> list[Chromosome]:
        roulette_wheel = []
        cumulative_fitness = 0

        for fitness in population_fitness:
            cumulative_fitness += fitness
            roulette_wheel.append(cumulative_fitness)

        total_fitness = cumulative_fitness

        if total_fitness == 0:
            return random.choices(population, k=len(population))

        selection = []
        while len(selection) < len(population):
            spin = random.uniform(0, total_fitness)
            for i in range(len(roulette_wheel)):
                if spin < roulette_wheel[i]:
                    selection.append(population[i])
                    break

        return selection
