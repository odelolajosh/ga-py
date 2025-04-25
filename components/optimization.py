class Optimization:
    def is_optimal(self, new: float, old: float | None) -> bool:
        return False


class Minimization(Optimization):
    def is_optimal(self, new: float, old: float | None) -> bool:
        return old is None or new < old


class Maximization(Optimization):
    def is_optimal(self, new: float, old: float | None) -> bool:
        return old is None or new > old
