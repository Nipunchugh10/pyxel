# Julia Set Animator

## Core Idea
Julia sets are related to the Mandelbrot set. For a fixed complex number $c$, the Julia set $J_c$ is the set of points $z$ that do not diverge under the iteration $f_c(z) = z^2 + c$.

## Mathematics
Similar to the Mandelbrot set, but $c$ is constant and $z_0$ varies:
$$z_{n+1} = z_n^2 + c$$
The Mandelbrot set is the map of all $c$ for which the Julia set $J_c$ is connected.

## Logic in Code
1. Fix a constant $c$ (e.g., $-0.7 + 0.27i$).
2. Define a grid of initial complex numbers $z_0$.
3. Iterate each $z_0$ and color based on the escape time.

## Interesting Properties
- **Variety:** Changing $c$ slightly can dramatically change the appearance of the Julia set.
- **Symmetry:** Julia sets are centrally symmetric around the origin.
