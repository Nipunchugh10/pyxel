# Pyxel Canvas

### 100 Stunning 2D & 3D Patterns in a Single Jupyter Notebook

> **All 100 patterns are now complete!**
> The engine, UI, architecture, and all pattern implementations are finished.

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
| Pattern implementations | **100 / 100** ✅ Complete |

**Progress by group:**

| Group | Done | Total |
|-------|------|-------|
| Geometric & Mathematical (1–20) | 20 | 20 ✅ |
| Nature-Inspired (21–40) | 20 | 20 ✅ |
| Abstract & Artistic (41–60) | 20 | 20 ✅ |
| 2D Game-Style (61–70) | 10 | 10 ✅ |
| 3D Objects & Sculptures (71–90) | 20 | 20 ✅ |
| Scientific & Simulation (91–100) | 10 | 10 ✅ |

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

| # | Pattern | What It Does |
|---|---------|--------------|
| 1 | Mandelbrot Fractal Explorer | Counts how long each point takes to escape to infinity when repeatedly squared — boundary points form the iconic fractal |
| 2 | Julia Set Animator | Same idea as Mandelbrot but with a fixed seed value, revealing a different fractal shape for every seed |
| 3 | Sierpinski Triangle | Picks a random corner and moves halfway toward it, over and over — a triangle pattern emerges by itself |
| 4 | Koch Snowflake | Repeatedly replaces the middle third of every line with a triangle bump, creating a snowflake with infinite detail |
| 5 | Penrose Tiling | Tiles a plane with two diamond shapes that never repeat their arrangement, no matter how far you extend them |
| 6 | Voronoi Diagram | Colours every pixel by whichever seed dot is closest to it — like territories on a map |
| 7 | Fibonacci Spiral | Places dots using nature's golden angle, producing the same spiral pattern as seeds in a sunflower |
| 8 | Dragon Curve | Simulates folding a strip of paper in half repeatedly, then unfolding it flat |
| 9 | Hilbert Curve | Draws a path that snakes through every cell in a grid without ever crossing itself |
| 10 | L-System Tree | Grows a tree by repeatedly replacing each branch with a smaller copy of the whole tree |
| 11 | Apollonius Gasket | Fills a circle with smaller and smaller tangent circles, packing them tighter and tighter forever |
| 12 | Lissajous Figures | Draws the path traced when two sine waves at different frequencies push a point in two directions at once |
| 13 | Rose Curves | Traces the petal shapes made by a point moving on a spinning wheel inside a circle |
| 14 | Chaos Attractor (Lorenz) | Simulates the butterfly-shaped path of a chaotic weather system that never quite repeats itself |
| 15 | Wave Interference Pattern | Shows how ripples from multiple sources add and cancel each other, creating bright and dark regions |
| 16 | Hypocycloid & Epicycloid | Traces the path of a point on a small circle rolling around the inside or outside of a larger one |
| 17 | Truchet Tiles | Fills a grid with randomly flipped curved tiles that join up into flowing river-like patterns |
| 18 | Hexagonal Grid Art | Colours a honeycomb grid using four different mathematical rules — distance, angle, checkerboard, random |
| 19 | Spirograph Generator | Mimics the classic toy — a pen tracing circles rolling inside other circles, layered on top of each other |
| 20 | Parametric Curve Art | Draws eight famous mathematical curves, each defined by a pair of simple equations |

### Nature-Inspired (21–40) — 20/20 complete

| # | Pattern | What It Does |
|---|---------|--------------|
| 21 | Cherry Blossom Particle Scene | Draws a branching tree then scatters pink petals drifting sideways in the wind |
| 22 | Procedural Tree Generator | Builds a tree by recursively splitting every branch into smaller branches at random angles |
| 23 | Reaction-Diffusion (Turing Patterns) | Simulates two chemicals spreading and reacting to spontaneously form animal-skin-like spots and stripes |
| 24 | Flocking Birds (Boids Lite) | Simulates a flock where each bird follows three rules — avoid neighbours, match direction, stay close |
| 25 | Lightning Bolt Generator | Zigzags a bolt downward, randomly splitting into branches at each step |
| 26 | Snowflake Crystal Growth | Grows six identical arms outward from a centre, branching symmetrically to form a snowflake |
| 27 | Leaf Venation Simulation | Grows veins toward scattered nutrient points, removing each point once a vein reaches it |
| 28 | Fire Particle System | Launches particles upward from a glowing base, fading from deep red through orange to white as they age |
| 29 | Galaxy Spiral Arms | Spreads thousands of stars along logarithmic spiral arms with a bright compact glow at the centre |
| 30 | Aurora Borealis | Layers glowing curtains of colour that fade downward, with a starfield behind them |
| 31 | Underwater Caustics | Overlaps multiple sets of ripples to create the shifting bright patches seen on a sunlit pool floor |
| 32 | Sand Dune Erosion | Blows sand grains one cell downwind at a time, collapsing any slope that gets too steep |
| 33 | Coral Reef Growth | Sprouts branching coral colonies upward from a sandy seafloor in vivid species colours |
| 34 | Mushroom Spore Map | Colours a region map by which mushroom colony each point belongs to, with ringed territory textures |
| 35 | Terrain Height Map | Generates realistic landscape elevations by stacking noise waves at different scales |
| 36 | Waterfall Flow | Traces streams down a rocky cliff face, accelerating under gravity and scattering spray at the bottom |
| 37 | Tornado Vortex | Spins a cloud of particles in a funnel shape that widens at the top and narrows at the ground |
| 38 | Cloud Formation | Stacks multiple layers of smooth noise to build fluffy cloud shapes against a sky gradient |
| 39 | River Delta Branching | Splits a river into a spreading fan of smaller channels as it reaches the sea |
| 40 | Moth Wing Pattern | Draws paired wings with concentric colour bands and circular eyespots, like a real moth |

### Abstract & Artistic (41–60) — 20/20 complete

| # | Pattern | What It Does |
|---|---------|--------------|
| 41 | Generative Mondrian | Recursively splits a canvas into rectangles and fills them with white or bold primary colours |
| 42 | Perlin Noise Painting | Blends multiple layers of smooth random noise into a flowing abstract colour painting |
| 43 | Mandala Generator | Mirrors a repeated petal shape around a centre point to build up a symmetrical mandala |
| 44 | Stained Glass Voronoi | Divides the canvas into irregular cells, each filled with a bold colour and outlined with dark borders |
| 45 | Op-Art Optical Illusion | Draws precisely spaced geometric patterns that trick the eye into seeing movement or depth |
| 46 | Watercolor Wash Effect | Overlaps soft blurred colour shapes to imitate the look of watercolour brushwork on paper |
| 47 | Glitch Art Generator | Mimics digital corruption — shifted rows, colour channel fringing, and random noise blocks |
| 48 | Isometric City Builder | Draws a miniature city viewed at a 45° angle with three shaded faces giving each building depth |
| 49 | Circuit Board Art | Generates a printed circuit board layout with copper traces, solder pads, and chip bodies |
| 50 | Tie-Dye Diffusion | Overlaps ripple rings from random points to simulate the look of folded and dip-dyed fabric |
| 51 | Geometric Collage | Randomly places and overlaps circles, rectangles, triangles, hexagons, and stars |
| 52 | Pixel Sorting Art | Reorders pixels within rows or columns by brightness, creating a glitchy sweep effect |
| 53 | ASCII Art Renderer | Maps a noise field to text characters — bright areas get dense symbols, dark areas get spaces |
| 54 | Kandinsky Color Study | Recreates the bold abstract style of Kandinsky using circles, arcs, lines, and triangles |
| 55 | Zentangle Automaton | Fills every cell of a grid with a randomly chosen hand-drawn tile pattern |
| 56 | Neon Sign Generator | Draws shapes with layered glowing halos to simulate lit neon tubes in six different sign styles |
| 57 | Mosaic Tile Art | Covers the canvas in small coloured squares with thin grout lines between them |
| 58 | Impressionist Dots | Scatters thousands of coloured dots to mimic the Pointillist painting technique |
| 59 | Cubist Portrait Filter | Breaks the canvas into triangles via Delaunay triangulation and fills each with its centre colour |
| 60 | Abstract Expressionism Drip | Simulates paint dripping down a canvas, slowing from gravity and splattering at the end |

### 2D Game-Style (61–70) — 10/10 complete ✅

| # | Pattern | What It Does |
|---|---------|--------------|
| 61 | Maze Generator & Solver | Carves a perfect maze by randomly knocking down walls, then finds the shortest path through it |
| 62 | Cellular Automaton Life | Runs Conway's Game of Life — cells live, die, or are born based on how many neighbours they have |
| 63 | Dungeon Room Placer | Drops rooms at random positions, rejects any that overlap, then connects them with corridors |
| 64 | Retro Starfield | Simulates flying through space by moving stars toward you and making nearer ones bigger and brighter |
| 65 | Breakout Brick Map | Generates a coloured brick layout styled after the classic Breakout arcade game |
| 66 | Pac-Man Ghost Pathfinding | Builds a maze and shows the shortest route each ghost would take to reach Pac-Man |
| 67 | Platformer Terrain Gen | Generates a side-scrolling level with varied terrain, floating platforms, coins, and a player character |
| 68 | Bullet Hell Pattern | Renders five different projectile spray patterns from a shoot-em-up bullet-hell game |
| 69 | Card Suit Patterns | Draws the four playing card suits — heart, diamond, club, spade — using precise mathematical curves |
| 70 | Pixel Flag Generator | Creates pixel-art flags using six different stripe and symbol layout rules |

### 3D Objects & Sculptures (71–90) — 20/20 complete ✅

| # | Pattern | What It Does |
|---|---------|--------------|
| 71 | Rotating DNA Helix | Draws two intertwined helical strands with coloured rungs connecting them, like a real DNA molecule |
| 72 | Klein Bottle Surface | Renders a surface with no inside or outside — it passes through itself because it can't exist in 3D without self-intersection |
| 73 | Mobius Strip | Renders a twisted loop that has only one side and one edge |
| 74 | Torus Knot | Draws a knotted curve that winds around the surface of a donut shape |
| 75 | Gyroid Surface | Renders a sponge-like curved surface found in nature inside butterfly wings and sea coral skeletons |
| 76 | Romanesco Broccoli | Places spiralling bud clusters using the same golden angle as a real Romanesco — a fractal vegetable |
| 77 | Icosphere Subdivisions | Starts from a 20-sided solid and repeatedly splits its triangular faces to approximate a smooth sphere |
| 78 | Trefoil Knot | Renders the simplest possible knot in 3D — it looks like a three-leaf clover looped through itself |
| 79 | Seashell Surface | Wraps a tube around an exponentially growing spiral, reproducing the shape of a real mollusc shell |
| 80 | Hyperboloid of Revolution | Renders the hourglass / cooling-tower shape made by rotating a hyperbola around its axis |
| 81 | Parametric Vase | Spins a profile curve around a vertical axis to create four different vase shapes |
| 82 | Crystal Lattice | Shows four atom arrangements found in real crystals — Simple Cubic, BCC, FCC, and Diamond — with bond lines |
| 83 | Geodesic Dome | Takes the top half of a subdivided sphere to build a dome made entirely of triangular panels |
| 84 | Calabi-Yau Manifold Slice | Projects the algebraic surface z₁ⁿ + z₂ⁿ = 1 from complex space onto a 2D plane, revealing the n²-patch lattice symmetry studied in string theory |
| 85 | Soap Bubble Cluster | Packs spheres of varying radii using greedy collision detection, then renders each with iridescent thin-film colouring and a specular highlight |
| 86 | Neural Mesh Sculpture | Places neuron nodes in layered 3D planes and connects adjacent layers with proximity-based synaptic edges, forming a glowing network sculpture |
| 87 | Twisted Prism Tower | Stacks regular polygon floors that rotate by a cumulative angle as they rise, creating the helical facade seen in landmark skyscrapers |
| 88 | Fractal Mountain | Uses the Diamond-Square algorithm to generate a heightmap with fractal self-similarity, producing realistic terrain at any resolution |
| 89 | Volumetric Fog Cube | Builds a 3D density field from stacked noise octaves and renders high-density voxels as semi-transparent points, simulating fog or a nebula |
| 90 | Strange Attractor 3D | Integrates four 3D chaotic ODE systems (Lorenz, Rössler, Thomas', Halvorsen) and draws the fractal phase-space trajectory as a gradient line |

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
