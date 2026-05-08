# Voronoi Diagram

## Core Idea
A Voronoi diagram partitions a plane into regions based on distance to a set of seed points. Each region contains all points closer to its seed than to any other.

## Mathematics
For a set of points $S = \{p_1, p_2, \dots, p_n\}$, the Voronoi cell $V_i$ is:
$$V_i = \{x \in \mathbb{R}^2 \mid d(x, p_i) \leq d(x, p_j) \text{ for all } j \neq i\}$$

## Logic in Code
- Uses `scipy.spatial.Voronoi` to compute the geometry.
- The `voronoi_plot_2d` utility handles the basic drawing.
- Custom logic fills each finite region with a random color for visual clarity.

## Interesting Properties
- **Natural Occurrence:** Found in cell structures, bubble formations, and territory maps.
- **Dual Graph:** The Delaunay triangulation is the dual of the Voronoi diagram.
