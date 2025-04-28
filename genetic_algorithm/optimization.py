class BaseOptimization:
    def is_optimal(self, new: float, old: float | None) -> bool:
        return False


class Minimization(BaseOptimization):
    def is_optimal(self, new: float, old: float | None) -> bool:
        return old is None or new < old


class Maximization(BaseOptimization):
    def is_optimal(self, new: float, old: float | None) -> bool:
        return old is None or new > old
