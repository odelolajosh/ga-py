class Optimization:
    def is_optimal(new: float, old: float) -> bool:
        return False


class Minimization(Optimization):
    def is_optimal(new: float, old: float) -> bool:
        return new < old


class Maximization(Optimization):
    def is_optimal(new: float, old: float) -> bool:
        return new > old
