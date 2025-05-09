# Methodology

Here, we discuss how the code is structured.

## The Algorithm

A problem is solved by initially getting random, but bounded solutions of size `population_size`. This makes up the `population`. Each solution is regarded as an individual.

## Anatomy of an Individual

An individual is an 1D array of size `number_of_decision_variables`. That is in the form
$$
Individual = [x_1, x_2, x_3, ..., x_n]\\
\text{where n is number of decision variables}
$$

