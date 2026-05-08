# Mandelbrot Fractal Explorer

## Core Idea
The Mandelbrot set is the set of complex numbers $c$ for which the function $f_c(z) = z^2 + c$ does not diverge when iterated from $z=0$.

## Mathematics
The iteration follows the recurrence:
$$z_{n+1} = z_n^2 + c$$
where $z_0 = 0$.
A point $c$ is in the set if $|z_n| \leq 2$ for all $n$.

## Logic in Code
1. Define a grid of complex numbers $c$ in the complex plane.
2. For each point $c$, iterate $z_{n+1} = z_n^2 + c$ up to `max_iter`.
3. If $|z_n|$ exceeds 2, the point is outside the set.
4. Color the point based on the number of iterations it took to escape.

## Interesting Properties
- **Self-Similarity:** The set contains infinitely many smaller versions of itself.
- **Boundary:** The boundary of the Mandelbrot set is a fractal with infinite complexity.
