from genetic_algorithm.termination_criterion import NumberOfGeneration, ThresholdDifference

def test_number_of_generation_stopping_criterion():
    number_of_generations = 0
    criterion = NumberOfGeneration(5)

    while not criterion.should_terminate(number_of_generations, 0):
        number_of_generations += 1
    
    assert number_of_generations == 5


def test_threshold_difference():
    fitness_values = [2, 3.2, 3.1, 3.1, 3.1, 3.1, 3.4]
    optimal_fitness = None
    number_of_generations = 0
    criterion = ThresholdDifference(0.05)

    for fitness in fitness_values:
        number_of_generations += 1
        optimal_fitness = fitness
        if criterion.should_terminate(number_of_generations, optimal_fitness):
            break
    
    # assert number_of_generations == 5
    assert optimal_fitness == 3.1
