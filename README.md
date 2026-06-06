# Pyxel Canvas

### 100 Stunning 2D & 3D Patterns in a Single Jupyter Notebook

A fully interactive visual gallery engine that hosts **100 Python visual design patterns** — spanning geometric fractals, nature simulations, abstract art, 3D sculptures, and scientific visualizations — inside one organized, modular, and navigable Jupyter Notebook.

This is **not** a collection of 100 disconnected scripts. It is a **visual engine with pattern plug-ins** that dynamically loads and executes any of the 100 designs on demand through an interactive widget-based UI.

---

## Features

- **100 fully implemented patterns** across 6 categories
- **Interactive UI** — category/pattern dropdowns, universal controls (palette, speed, resolution), and pattern-specific sliders
- **Lazy loading** — only the selected pattern is instantiated, keeping memory low
- **8 colour palettes** — Inferno, Ocean Depths, Neon Cyberpunk, Forest, Sunset Blaze, Arctic Aurora, Monochrome, Lava Flow
- **Export** — save any render as PNG, GIF, or MP4 with one click
- **Concept Notes** — every pattern includes a "How This Works" explanation with LaTeX-rendered mathematics
- **Single-notebook architecture** — one `.ipynb` file is the entire user-facing application

---

## Quick Start

```bash
# Clone
git clone https://github.com/Nipunchugh10/pyxel.git
cd pyxel

# Launch
jupyter lab visual_engine/notebook.ipynb
```

Run all cells top-to-bottom. The environment setup cell installs all required libraries automatically. Then use the UI dropdowns to browse and render any pattern.

---

## Project Architecture

```
visual_engine/
├── notebook.ipynb               <- Single entry point — run this
│
├── engines/
│   ├── renderer.py              <- BasePattern ABC (render + get_controls)
│   ├── color_utils.py           <- 8 preset colour palettes + utilities
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
└── exports/                     <- Rendered outputs (auto-created, gitignored)
```

---

## All 100 Patterns

### Geometric & Mathematical (1–20)

| # | Pattern | Description |
|---|---------|-------------|
| 1 | Mandelbrot Fractal Explorer | Iterative escape-time fractal with zoomable complex-plane viewport |
| 2 | Julia Set Animator | Fixed-seed Julia sets revealing different fractal shapes per parameter |
| 3 | Sierpinski Triangle | Chaos-game construction converging to a self-similar gasket |
| 4 | Koch Snowflake | Recursive midpoint replacement producing an infinite-perimeter snowflake |
| 5 | Penrose Tiling | Aperiodic tiling with two rhombus shapes that never repeats |
| 6 | Voronoi Diagram | Nearest-seed territory partition via cKDTree rasterization |
| 7 | Fibonacci Spiral | Golden-angle phyllotaxis generating sunflower-like spirals |
| 8 | Dragon Curve | Iterative paper-folding fractal rendered as a LineCollection |
| 9 | Hilbert Curve | Space-filling curve visiting every grid cell without crossing |
| 10 | L-System Tree | Recursive string-rewriting system producing branching trees |
| 11 | Apollonius Gasket | Circle packing via Descartes' Circle Theorem |
| 12 | Lissajous Figures | Parametric curves from orthogonal sine-wave frequencies |
| 13 | Rose Curves | Polar curves $r = \cos(p/q \cdot \theta)$ with GCD-closed petals |
| 14 | Chaos Attractor (Lorenz) | RK4 integration of the Lorenz system's butterfly trajectory |
| 15 | Wave Interference Pattern | Superposition of coherent point-source ripples |
| 16 | Hypocycloid & Epicycloid | Rolling-circle parametric curves with exact period closure |
| 17 | Truchet Tiles | Randomly oriented arc tiles producing flowing patterns |
| 18 | Hexagonal Grid Art | Axial-coordinate tessellation with 4 colouring modes |
| 19 | Spirograph Generator | Layered hypotrochoids with variable pen distances |
| 20 | Parametric Curve Art | Gallery of 8 named mathematical curves |

### Nature-Inspired (21–40)

| # | Pattern | Description |
|---|---------|-------------|
| 21 | Cherry Blossom Particle Scene | Recursive tree with wind-drifted petal particles |
| 22 | Procedural Tree Generator | Configurable recursive branching with depth-coloured gradients |
| 23 | Reaction-Diffusion (Turing Patterns) | Gray-Scott model producing spots and stripes |
| 24 | Flocking Birds (Boids Lite) | Vectorized separation/alignment/cohesion flocking |
| 25 | Lightning Bolt Generator | Midpoint displacement with probabilistic branching |
| 26 | Snowflake Crystal Growth | 6-fold symmetric recursive arm structure |
| 27 | Leaf Venation Simulation | Space colonization algorithm with kill-radius pruning |
| 28 | Fire Particle System | Beta-distributed ages mapped to temperature colours |
| 29 | Galaxy Spiral Arms | Logarithmic spirals with Gaussian arm spread |
| 30 | Aurora Borealis | Sinusoidal curtains with exponential vertical fade |
| 31 | Underwater Caustics | Cosine wave sum with power-law peak sharpening |
| 32 | Sand Dune Erosion | Cellular automaton with saltation and avalanche rules |
| 33 | Coral Reef Growth | Multi-colony recursive branching in species palettes |
| 34 | Mushroom Spore Map | cKDTree 2-NN Voronoi with ring textures |
| 35 | Terrain Height Map | Multi-octave fBm with hypsometric colour bands |
| 36 | Waterfall Flow | Gravity-driven stream paths with spray scatter |
| 37 | Tornado Vortex | Cylindrical particle distribution with height-twist |
| 38 | Cloud Formation | Persistence noise threshold with sky gradient composite |
| 39 | River Delta Branching | Recursive binary bifurcation with fan-spread control |
| 40 | Moth Wing Pattern | Elliptical masks with concentric bands and eyespots |

### Abstract & Artistic (41–60)

| # | Pattern | Description |
|---|---------|-------------|
| 41 | Generative Mondrian | Recursive BSP splits with Mondrian primary palette |
| 42 | Perlin Noise Painting | 6-octave fBm via cubic-zoom upsampling |
| 43 | Mandala Generator | N-fold rotational symmetry with petal profiles |
| 44 | Stained Glass Voronoi | cKDTree cells with border detection and bold fills |
| 45 | Op-Art Optical Illusion | Bridget Riley / Vasarely / hypnotic ring styles |
| 46 | Watercolor Wash Effect | Gaussian-blurred ellipse masks with alpha compositing |
| 47 | Glitch Art Generator | Row-shift + chromatic aberration + data block corruption |
| 48 | Isometric City Builder | 2D isometric projection with painter's algorithm |
| 49 | Circuit Board Art | Snap-grid traces, annular vias, and FancyBboxPatch ICs |
| 50 | Tie-Dye Diffusion | Cosine ripple superposition with spiral twist |
| 51 | Geometric Collage | 5 shape types with Porter-Duff alpha compositing |
| 52 | Pixel Sorting Art | Brightness-span detection with per-span argsort |
| 53 | ASCII Art Renderer | 10-level density ramp mapped from noise field |
| 54 | Kandinsky Color Study | 7 element types in 3 composition modes |
| 55 | Zentangle Automaton | Grid of 6 tangle rules (spirals, crosshatch, dots, etc.) |
| 56 | Neon Sign Generator | Multi-pass glow halos with noble-gas colour palette |
| 57 | Mosaic Tile Art | Raster tessera renderer with grout lines |
| 58 | Impressionist Dots | 4-octave fBm scatter with size variation |
| 59 | Cubist Portrait Filter | Delaunay triangulation with centroid-sampled fills |
| 60 | Abstract Expressionism Drip | Velocity-damped random walks with terminal splatters |

### 2D Game-Style (61–70)

| # | Pattern | Description |
|---|---------|-------------|
| 61 | Maze Generator & Solver | DFS backtracker + BFS shortest-path solver |
| 62 | Cellular Automaton Life | Conway's GoL with age-coloured cells |
| 63 | Dungeon Room Placer | Random placement + L-shaped corridor carving |
| 64 | Retro Starfield | Perspective projection with depth-based sizing |
| 65 | Breakout Brick Map | 4 colouring styles with rounded bevel highlights |
| 66 | Pac-Man Ghost Pathfinding | Perfect maze + BFS ghost routes to Pac-Man |
| 67 | Platformer Terrain Gen | 1D fBm terrain with platforms, coins, and themes |
| 68 | Bullet Hell Pattern | 5 danmaku spray patterns (burst, spiral, fan, cross, scatter) |
| 69 | Card Suit Patterns | Parametric heart/diamond/club/spade with layout modes |
| 70 | Pixel Flag Generator | 6 grammar designs with 5x pixel-perfect upscale |

### 3D Objects & Sculptures (71–90)

| # | Pattern | Description |
|---|---------|-------------|
| 71 | Rotating DNA Helix | Dual helical strands with nucleotide-coloured rungs |
| 72 | Klein Bottle Surface | Figure-8 immersion showing self-intersection |
| 73 | Mobius Strip | Parametric half-twist surface with N-turn control |
| 74 | Torus Knot | T(p,q) knot wound around a torus surface |
| 75 | Gyroid Surface | Implicit triply-periodic minimal surface via threshold scatter |
| 76 | Romanesco Broccoli | Golden-angle phyllotaxis with recursive sub-bud clusters |
| 77 | Icosphere Subdivisions | Iterative midpoint subdivision of icosahedron |
| 78 | Trefoil Knot | Simplest non-trivial knot in 3D |
| 79 | Seashell Surface | Exponential helicospiral with proportional tube radius |
| 80 | Hyperboloid of Revolution | Doubly-ruled surface with ruling line overlays |
| 81 | Parametric Vase | 4 profile styles as surfaces of revolution |
| 82 | Crystal Lattice | SC / BCC / FCC / Diamond Cubic with cKDTree bonds |
| 83 | Geodesic Dome | Upper-hemisphere icosphere with strut edges |
| 84 | Calabi-Yau Manifold Slice | 2D projection of $z_1^n + z_2^n = 1$ from $\mathbb{C}^2$ |
| 85 | Soap Bubble Cluster | Greedy sphere packing with iridescent thin-film colour |
| 86 | Neural Mesh Sculpture | Layered neurons with k-NN inter-layer synaptic edges |
| 87 | Twisted Prism Tower | Polygon stack with cumulative twist and linear taper |
| 88 | Fractal Mountain | Diamond-Square heightmap with Hurst-exponent scaling |
| 89 | Volumetric Fog Cube | 3D fBm density field rendered as depth-sorted scatter |
| 90 | Strange Attractor 3D | Lorenz / Rossler / Thomas' / Halvorsen via RK4 |

### Scientific & Simulation (91–100)

| # | Pattern | Description |
|---|---------|-------------|
| 91 | Neural Network Visualization | Layer-width network with weighted edges and activation values |
| 92 | Atom Orbital Simulator | Hydrogen $\psi_{nlm}$ cross-section heatmaps |
| 93 | Black Hole Lensing | Schwarzschild weak-field deflection + accretion disk |
| 94 | Conway's Game of Life | Moore-kernel convolution with 4 starter patterns |
| 95 | Boids Flocking Simulation | Craig Reynolds 3-rule model with pairwise tensor |
| 96 | Traffic Flow Simulation | Nagel-Schreckenberg cellular automaton with space-time diagram |
| 97 | Ecosystem Predator-Prey | Lotka-Volterra RK4 integration + phase portrait |
| 98 | Ant Colony Optimization | ACO metaheuristic for TSP with pheromone visualization |
| 99 | Fluid Dynamics (SPH) | Smoothed Particle Hydrodynamics with pressure/viscosity kernels |
| 100 | Quantum Wave Packet | Split-step Fourier propagation through potential barriers |

---

## Tech Stack

| Category | Libraries |
|----------|-----------|
| 2D Graphics | `matplotlib`, `Pillow` |
| 3D Rendering | `mpl_toolkits.mplot3d` |
| Generative Math | `numpy`, `scipy` |
| UI Controls | `ipywidgets` |
| Performance | `numpy` vectorization, lazy loading |

---

## How It Works

```
┌─────────────────────────────────────────────────────┐
│  Notebook UI (ipywidgets)                           │
│  ┌───────────┐ ┌───────────┐ ┌──────────────────┐  │
│  │ Category  │ │  Pattern  │ │ Controls (sliders)│  │
│  └─────┬─────┘ └─────┬─────┘ └────────┬─────────┘  │
│        │              │                │             │
│        v              v                v             │
│  ┌─────────────────────────────────────────────┐    │
│  │         Pattern Registry (100 entries)       │    │
│  │         Lazy-loaded on first selection        │    │
│  └──────────────────────┬──────────────────────┘    │
│                         │                            │
│                         v                            │
│  ┌─────────────────────────────────────────────┐    │
│  │   BasePattern.render(**kwargs) → matplotlib  │    │
│  └──────────────────────┬──────────────────────┘    │
│                         │                            │
│                         v                            │
│  ┌─────────────────────────────────────────────┐    │
│  │     Inline display  /  Export to PNG/GIF/MP4 │    │
│  └─────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────┘
```

Each pattern class:
- Inherits from `BasePattern`
- Implements `render(**kwargs)` — produces the visual output
- Implements `get_controls()` — returns pattern-specific ipywidgets
- Supports 8 colour palettes and 3 resolution levels (Low/Medium/High)

---

## License

MIT License — feel free to fork, remix, and learn from this notebook.
