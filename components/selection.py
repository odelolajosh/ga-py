from type import Chromosome

class Selection:
    def select(population: list[Chromosome], population_fitness: list[float]) -> list[Chromosome]:
        raise NotImplementedError()


class RouletteSelection:
    def select(population: list[Chromosome], population_fitness: list[float]) -> list[Chromosome]:
        raise NotImplementedError()
