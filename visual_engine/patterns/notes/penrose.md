# Penrose Tiling (P3 Tiling)

## Core Idea
Penrose tilings are non-periodic tilings of the plane. They lack translational symmetry but are self-similar.

## Mathematics
Based on the golden ratio $\phi = \frac{1+\sqrt{5}}{2}$.
The tiling uses two shapes: thin and thick rhombs (or subdivided "Robinson triangles").
- Thin triangle angles: $36^\circ, 72^\circ, 72^\circ$.
- Thick triangle angles: $108^\circ, 36^\circ, 36^\circ$.

## Logic in Code
- Uses the **deflation** method.
- Each generation, triangles are decomposed into smaller triangles of the same two types.
- The positions are calculated using complex numbers for easier rotations and scaling.

## Interesting Properties
- **Aperiodicity:** You can never shift the tiling and have it match itself.
- **Five-fold Symmetry:** Locally, it exhibits five-fold rotational symmetry, which is impossible for periodic tilings.
