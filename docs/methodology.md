# Methodology

Here, we discuss how the code is structured.

## Anatomy of a Chromosome

A chromosome in a binary representation has this structure
$$
Chromosome = [
  [1, 0, 1, 1, 0],
  [0, 1, 0, 1, 0],
  [1, 1, 0, 1, 0]
]
$$

From this chromosome, we see three decision variables say $x_1 = [1, 0, 1, 1, 0]$, $x_2 = [0, 1, 0, 1, 0]$ and $x_3 = [1, 1, 0, 1, 0]$.