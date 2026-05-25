# Pyxel Canvas

### 100 Stunning 2D & 3D Patterns in a Single Jupyter Notebook

> **This project is currently under active development.**
> The engine, UI, and architecture are complete. Pattern implementations are being added progressively.

---

## Overview

A fully interactive visual gallery engine that hosts **100 Python visual design patterns** — spanning geometric fractals, nature simulations, abstract art, 3D sculptures, and scientific visualizations — inside one organized, modular, and navigable Jupyter Notebook.

This is **not** a collection of 100 disconnected scripts. It is **Pyxel Canvas** — a visual engine with pattern plug-ins that dynamically loads and executes any of the 100 designs on demand.

---

## Current Status

| Milestone | Status |
|-----------|--------|
| Project structure & folder hierarchy | Complete |
| Core engine (`BasePattern`, color palettes, export utilities) | Complete |
| 100 pattern class stubs registered | Complete |
| Interactive UI (dropdowns, controls, render/export buttons) | Complete |
| Pattern implementations | **60 / 100** — in progress |

**Progress by group:**

| Group | Done | Total |
|-------|------|-------|
| Geometric & Mathematical (1–20) | 20 | 20 ✅ |
| Nature-Inspired (21–40) | 20 | 20 ✅ |
| Abstract & Artistic (41–60) | 20 | 20 ✅ |
| 2D Game-Style (61–70) | 0 | 10 |
| 3D Objects & Sculptures (71–90) | 0 | 20 |
| Scientific & Simulation (91–100) | 0 | 10 |

---

## Project Architecture

```
visual_engine/
│
├── notebook.ipynb               <- Single entry point — run this
│
├── engines/
│   ├── renderer.py              <- BasePattern ABC (render + get_controls)
│   ├── color_utils.py           <- 8 preset color palettes + utilities
│   ├── animation.py             <- Animation loop helpers
│   └── camera.py                <- 2D viewport (pan, zoom, meshgrid)
│
├── patterns/
│   ├── __init__.py              <- PATTERNS registry (100 entries) + CATEGORIES
│   ├── fractals.py              <- Geometric & Mathematical (1–20)
│   ├── nature.py                <- Nature-Inspired (21–40)
│   ├── abstract.py              <- Abstract & Artistic (41–60)
│   ├── game2d.py                <- 2D Game-Style (61–70)
│   ├── objects3d.py             <- 3D Objects & Sculptures (71–90)
│   └── scientific.py            <- Scientific & Simulation (91–100)
│
├── utils/
│   ├── export.py                <- PNG / GIF / MP4 export functions
│   └── physics.py               <- Shared physics helpers
│
├── assets/                      <- Textures, fonts, static resources
├── shaders/                     <- GLSL shader files
└── exports/                     <- Rendered outputs (auto-created)
```

---

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/Nipunchugh10/pyxel.git
   cd pyxel
   ```

2. **Open the notebook**
   ```bash
   jupyter lab visual_engine/notebook.ipynb
   ```

3. **Run all cells from top to bottom** — the environment setup cell (Section 0) will install all required libraries automatically.

4. **Use the UI** — select a category and pattern from the dropdowns, adjust controls, and click **RENDER**.

---

## How It Works

- Each pattern is a Python class inheriting from `BasePattern`
- Every class implements `render(**kwargs)` and `get_controls()`
- The notebook UI dynamically loads patterns via a lazy-loading cache
- Universal controls (palette, speed, resolution) + pattern-specific controls
- Export any render as PNG, GIF, or MP4 with one click

---

## Implemented Patterns

### Geometric & Mathematical (1–20) — 20/20 complete

| # | Pattern | Key Technique |
|---|---------|---------------|
| 1 | Mandelbrot Fractal Explorer | Vectorised escape-time iteration on complex grid |
| 2 | Julia Set Animator | Same escape-time with fixed `c`, variable `z0` plane |
| 3 | Sierpinski Triangle | Chaos game — random barycentric contraction |
| 4 | Koch Snowflake | Iterative segment subdivision + rotation |
| 5 | Penrose Tiling | Penrose P3 rhomb deflation with Robinson triangles |
| 6 | Voronoi Diagram | `scipy.cKDTree` rasterised nearest-neighbour field |
| 7 | Fibonacci Spiral | Golden-angle sunflower point placement |
| 8 | Dragon Curve | Iterative fold sequence + `LineCollection` |
| 9 | Hilbert Curve | `d2xy` space-filling index mapping |
| 10 | L-System Tree | Prusinkiewicz turtle-graphics branching grammar |
| 11 | Apollonius Gasket | BFS + Descartes' Circle Theorem curvature iteration |
| 12 | Lissajous Figures | Parametric `x=sin(at+δ)`, `y=sin(bt)` |
| 13 | Rose Curves | Polar `r=cos(p/q·θ)`, GCD-reduced period |
| 14 | Chaos Attractor (Lorenz) | RK4 integration of σ/ρ/β system, x–z projection |
| 15 | Wave Interference Pattern | Superposition of n coherent point sources via `imshow` |
| 16 | Hypocycloid & Epicycloid | Parametric rolling-circle equations, GCD period |
| 17 | Truchet Tiles | Random binary orientation matrix, `Arc` patches |
| 18 | Hexagonal Grid Art | Axial-coordinate pointy-top tessellation, 4 colour modes |
| 19 | Spirograph Generator | Layered hypotrochoids with linearly-spaced pen distances |
| 20 | Parametric Curve Art | Gallery of 8 named curves with singularity guard |

### Nature-Inspired (21–40) — 20/20 complete

| # | Pattern | Key Technique |
|---|---------|---------------|
| 21 | Cherry Blossom Particle Scene | Recursive tree `LineCollection` + wind-drift petal scatter |
| 22 | Procedural Tree Generator | Configurable recursive branching, palette gradient by depth |
| 23 | Reaction-Diffusion (Turing Patterns) | Gray-Scott model, 5-point Laplacian via `np.roll` |
| 24 | Flocking Birds (Boids Lite) | Fully vectorised sep/align/cohesion via (N,N,2) diff tensor |
| 25 | Lightning Bolt Generator | Recursive midpoint displacement + probabilistic branching |
| 26 | Snowflake Crystal Growth | 6-fold symmetric recursive arms, glow `LineCollection` |
| 27 | Leaf Venation Simulation | Space colonisation: elliptical attractor field, kill-radius |
| 28 | Fire Particle System | Beta-distributed age → height + temperature colour mapping |
| 29 | Galaxy Spiral Arms | Logarithmic spiral `r=r₀·exp(b·θ)`, warm→cool star gradient |
| 30 | Aurora Borealis | Raster curtain layers: sinusoidal edge + exponential fade |
| 31 | Underwater Caustics | Sum of N random-direction cosine waves, power-law sharpening |
| 32 | Sand Dune Erosion | Cellular automaton: saltation via `np.roll` + avalanche rule |
| 33 | Coral Reef Growth | Multi-colony recursive branching, 6 species palettes |
| 34 | Mushroom Spore Map | `cKDTree` 2-NN Voronoi + ring texture + noise blend |
| 35 | Terrain Height Map | Multi-octave fBm (layered sine octaves) + hypsometric colour |
| 36 | Waterfall Flow | Gravity-accelerated stream paths + sinusoidal sway + spray scatter |
| 37 | Tornado Vortex | Cylindrical particles + height-proportional twist + funnel taper |
| 38 | Cloud Formation | Persistence noise → threshold + γ lift → sky gradient composite |
| 39 | River Delta Branching | Recursive binary bifurcation, fan-spread, muddy→teal colour |
| 40 | Moth Wing Pattern | Elliptical wing masks + concentric bands + bilateral eyespots |

### Abstract & Artistic (41–60) — 20/20 complete

| # | Pattern | Key Technique |
|---|---------|---------------|
| 41 | Generative Mondrian | Recursive BSP partitioning + Mondrian palette (5:3 white-to-primary weighting) |
| 42 | Perlin Noise Painting | fBm via `scipy.ndimage.zoom` cubic upsampling of random value-noise grids |
| 43 | Mandala Generator | N-fold rotational symmetry, cosine-squared petal profile, concentric rings |
| 44 | Stained Glass Voronoi | `cKDTree` 2-NN rasterisation + distance shading + d2−d1 border threshold |
| 45 | Op-Art Optical Illusion | 3 styles: wavy concentric rings, Vasarely grid, hypnotic wavy squares |
| 46 | Watercolor Wash Effect | Random ellipse masks + Gaussian blur + power-law edge curve + alpha composite |
| 47 | Glitch Art Generator | Row-shift displacement + RGB chromatic aberration + corrupted data blocks |
| 48 | Isometric City Builder | Isometric projection + painter's algorithm on (c+r) sum + 3-face buildings |
| 49 | Circuit Board Art | Snap-grid L-shaped copper traces + annular-ring vias + IC chip bodies |
| 50 | Tie-Dye Diffusion | Cosine ripple superposition Σwᵢcos(2πf₀dᵢ+τθᵢ) with spiral twist parameter |
| 51 | Geometric Collage | 5 shape types, explicit rotation matrices, Porter-Duff alpha compositing |
| 52 | Pixel Sorting Art | Contiguous-span detection + `np.argsort` pixel reordering above threshold |
| 53 | ASCII Art Renderer | 10-level density ramp, two-octave value noise, monospace text grid |
| 54 | Kandinsky Color Study | 7 element types, 3 compositional styles (Composition VIII / YRB / Improvisation) |
| 55 | Zentangle Automaton | g×g grid, 6 tangle rules (lines / circles / dots / cross-hatch / diagonals / Archimedean spiral) |
| 56 | Neon Sign Generator | Multi-pass glow w_k=w_base·(1+3.5k/n_g) + alpha falloff + white core, 6 sign shapes |
| 57 | Mosaic Tile Art | Raster tessera renderer — ts-pixel tiles with grout, 3 colour modes, brightness jitter |
| 58 | Impressionist Dots | 4-octave fBm colour field, vectorised `cmap(vals)` scatter, Gaussian position jitter |
| 59 | Cubist Portrait Filter | Delaunay triangulation on n points + 36 border guards, centroid-sampled noise field |
| 60 | Abstract Expressionism Drip | Velocity-damped random walk v×=0.97 − gravity, terminal splatter Circle patches |

---

## Pattern Groups

| # | Group | Count |
|---|-------|-------|
| 1–20 | Geometric & Mathematical | 20 |
| 21–40 | Nature-Inspired | 20 |
| 41–60 | Abstract & Artistic | 20 |
| 61–70 | 2D Game-Style | 10 |
| 71–90 | 3D Objects & Sculptures | 20 |
| 91–100 | Scientific & Simulation | 10 |

<details>
<summary><b>Full list of all 100 patterns</b></summary>

### Geometric & Mathematical (1–20)
1. Mandelbrot Fractal Explorer
2. Julia Set Animator
3. Sierpinski Triangle
4. Koch Snowflake
5. Penrose Tiling
6. Voronoi Diagram
7. Fibonacci Spiral
8. Dragon Curve
9. Hilbert Curve
10. L-System Tree
11. Apollonius Gasket
12. Lissajous Figures
13. Rose Curves
14. Chaos Attractor (Lorenz)
15. Wave Interference Pattern
16. Hypocycloid & Epicycloid
17. Truchet Tiles
18. Hexagonal Grid Art
19. Spirograph Generator
20. Parametric Curve Art

### Nature-Inspired (21–40)
21. Cherry Blossom Particle Scene
22. Procedural Tree Generator
23. Reaction-Diffusion (Turing Patterns)
24. Flocking Birds (Boids Lite)
25. Lightning Bolt Generator
26. Snowflake Crystal Growth
27. Leaf Venation Simulation
28. Fire Particle System
29. Galaxy Spiral Arms
30. Aurora Borealis
31. Underwater Caustics
32. Sand Dune Erosion
33. Coral Reef Growth
34. Mushroom Spore Map
35. Terrain Height Map
36. Waterfall Flow
37. Tornado Vortex
38. Cloud Formation
39. River Delta Branching
40. Moth Wing Pattern

### Abstract & Artistic (41–60)
41. Generative Mondrian
42. Perlin Noise Painting
43. Mandala Generator
44. Stained Glass Voronoi
45. Op-Art Optical Illusion
46. Watercolor Wash Effect
47. Glitch Art Generator
48. Isometric City Builder
49. Circuit Board Art
50. Tie-Dye Diffusion
51. Geometric Collage
52. Pixel Sorting Art
53. ASCII Art Renderer
54. Kandinsky Color Study
55. Zentangle Automaton
56. Neon Sign Generator
57. Mosaic Tile Art
58. Impressionist Dots
59. Cubist Portrait Filter
60. Abstract Expressionism Drip

### 2D Game-Style (61–70)
61. Maze Generator & Solver
62. Cellular Automaton Life
63. Dungeon Room Placer
64. Retro Starfield
65. Breakout Brick Map
66. Pac-Man Ghost Pathfinding
67. Platformer Terrain Gen
68. Bullet Hell Pattern
69. Card Suit Patterns
70. Pixel Flag Generator

### 3D Objects & Sculptures (71–90)
71. Rotating DNA Helix
72. Klein Bottle Surface
73. Mobius Strip
74. Torus Knot
75. Gyroid Surface
76. Romanesco Broccoli
77. Icosphere Subdivisions
78. Trefoil Knot
79. Seashell Surface
80. Hyperboloid of Revolution
81. Parametric Vase
82. Crystal Lattice
83. Geodesic Dome
84. Calabi-Yau Manifold Slice
85. Soap Bubble Cluster
86. Neural Mesh Sculpture
87. Twisted Prism Tower
88. Fractal Mountain
89. Volumetric Fog Cube
90. Strange Attractor 3D

### Scientific & Simulation (91–100)
91. Neural Network Visualization
92. Atom Orbital Simulator
93. Black Hole Lensing
94. Conway's Game of Life
95. Boids Flocking Simulation
96. Traffic Flow Simulation
97. Ecosystem Predator-Prey
98. Ant Colony Optimization
99. Fluid Dynamics (SPH)
100. Quantum Wave Packet

</details>

---

## Tech Stack

| Category | Libraries |
|----------|-----------|
| 2D Graphics | `matplotlib`, `Pillow` |
| Generative Art | `noise`, `numpy` |
| Simulations | `scipy` |
| UI Controls | `ipywidgets` |
| Fast Math | `numpy`, `numba` |

---

## License

MIT License — feel free to fork, remix, and learn from this notebook.
