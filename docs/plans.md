# Genetic Algorithm Framework – Next Steps

This document outlines the upcoming enhancements to the framework, focusing on:

1. Flexible Termination Logic  
2. Callback Hook System (Functional & Class-based)  
3. Design Rationale for Maintainability and Extensibility

---

## 1. Termination Logic

Currently, the GA only stops after a fixed number of generations. The goal is to allow **pluggable, composable termination criteria** such as:

- Number of Generations
- Target Fitness Achieved
- Early Stopping (no improvement)
- Max Runtime
- Logical Combinations (e.g., AND/OR of multiple criteria)

### Example

```python
termination = OrTermination(
    NumberOfGeneration(50),
    TargetFitnessReached(95.0)
)
```

### Design

```python
class TerminationCondition:
    def should_terminate(self, generation, best_individual, population) -> bool:
        raise NotImplementedError()
```

Built-ins:
- `NumberOfGeneration(max_generations)`
- `TargetFitnessReached(threshold)`
- `EarlyStopping(patience)`
- `MaxRuntime(seconds)`
- `AndTermination(...)`, `OrTermination(...)`

These conditions will be checked at the end of each generation.

---

## 2. Callback Hook System

To support monitoring, logging, and extension without altering the GA core logic, we introduce a **callback system**.

### 🔧 Lifecycle Methods

```python
class Callback:
    def on_generation_start(self, generation, population): pass
    def on_generation_end(self, generation, population, best_individual): pass
    def on_evolution_end(self, best_individual): pass
```

---

### Class-based Callback

```python
class PrintBestFitness(Callback):
    def on_generation_end(self, generation, population, best_individual):
        print(f"Gen {generation}: Best Fitness = {best_individual.fitness}")
```

---

### Functional Callback (via Decorator)

```python
@callback
def log_best(generation, population, best_individual):
    print(f"[LOG] Gen {generation}: {best_individual.fitness}")
```

The decorator `@callback` automatically wraps a simple function into a `Callback` object.

---

### Usage

```python
ga = GeneticAlgorithm(
    population_size=100,
    ...,
    termination=NumberOfGeneration(50),
    callbacks=[
        PrintBestFitness(),
        log_best
    ]
)
```

---

## 3. Design Philosophy

The core design principles of this framework:

| Principle         | Description |
|------------------|-------------|
| **Composable**   | Components like termination, mutation, and callbacks can be swapped in and out. |
| **Extensible**   | Easy to add new encodings, selection methods, or observers. |
| **Functional First** | Users can write lambdas or functions, not just classes. |
| **Decoupled**    | GA engine is separate from problem-specific logic like encoding or logging. |
| **Readable API** | Emphasizes human-friendly syntax and self-documenting code. |

---

## Planned Extras

- `LivePlotCallback()` for real-time plotting
- `SaveProgressCallback()` to store run history
- `GIFRecorderCallback()` for visual simulations
- TensorBoard / WandB integrations

---

## Contributing

Have an idea for a custom callback, mutation operator, or visualization tool? Feel free to submit a PR or open an issue!
