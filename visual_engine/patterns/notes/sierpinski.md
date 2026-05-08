# Sierpinski Triangle (Chaos Game)

## Core Idea
The Sierpinski triangle can be generated using a randomized "Chaos Game" algorithm.

## Mathematics
1. Start with three vertices of an equilateral triangle.
2. Start at a random point $P_0$.
3. For each step $n$, choose a random vertex $V$ and set:
   $$P_{n+1} = \frac{P_n + V}{2}$$

## Logic in Code
- Vertices are defined as $(0,0)$, $(1,0)$, and $(0.5, \sqrt{3}/2)$.
- A loop runs for `iterations` times, picking a random vertex and moving half-way towards it.
- The resulting points are plotted as a scatter plot.

## Interesting Properties
- **Determinism from Randomness:** Even though the process is random, it consistently produces a perfectly structured fractal.
- **Fractional Dimension:** The Sierpinski triangle has a Hausdorff dimension of $\log(3)/\log(2) \approx 1.585$.
