# Python Visual Design Engine — Project Plan
### 100 Stunning 2D & 3D Patterns in a Single Jupyter Notebook

---

## Project Overview

This project is a **single Jupyter Notebook** that functions as a fully interactive visual engine and gallery system. It hosts all 100 Python visual design ideas — spanning geometric fractals, nature simulations, abstract art, 3D sculptures, and scientific visualizations — inside one organized, modular, and navigable notebook environment.

The notebook is **not** a collection of 100 disconnected scripts. It is architected as a **Visual Engine with Pattern Plug-ins**: a central renderer that dynamically loads and executes any of the 100 designs on demand, keeping the notebook fast, maintainable, and genuinely impressive.

---

## Core Constraint

> Everything must live and run inside a **single Jupyter Notebook** (`notebook.ipynb`).

This means:
- No separate Python files are executed directly by the user.
- All code cells, UI controls, and rendering logic are contained within the notebook.
- Supporting modules (pattern classes, utilities) are written to disk from within the notebook itself using `%%writefile` cells, then imported back — keeping the single-notebook contract intact.
- The user interacts entirely through the notebook interface: dropdowns, sliders, buttons, and inline visual output.

---

## Folder Structure (Generated From Within the Notebook)

The notebook will auto-create this structure on first run using `%%writefile` and `os.makedirs`:

```
visual_engine/
│
├── notebook.ipynb          ← The single entry point (everything lives here)
│
├── patterns/
│   ├── __init__.py
│   ├── fractals.py         ← Ideas 1–20 (Geometric & Mathematical)
│   ├── nature.py           ← Ideas 21–40 (Nature-Inspired)
│   ├── abstract.py         ← Ideas 41–60 (Abstract & Artistic)
│   ├── game2d.py           ← Ideas 61–70 (2D Game-Style)
│   ├── objects3d.py        ← Ideas 71–90 (3D Objects & Sculptures)
│   └── scientific.py       ← Ideas 91–100 (Scientific & Simulation)
│
├── engines/
│   ├── __init__.py
│   ├── renderer.py         ← Core rendering dispatcher
│   ├── animation.py        ← Animation loop utilities
│   ├── camera.py           ← Camera/viewport controls
│   └── color_utils.py      ← Palette and gradient helpers
│
├── utils/
│   ├── __init__.py
│   ├── export.py           ← Save PNG / GIF / MP4
│   └── physics.py          ← Shared physics helpers (pymunk, taichi)
│
├── assets/                 ← Textures, fonts, any static resources
├── shaders/                ← GLSL shader files for ModernGL patterns
└── exports/                ← All rendered outputs saved here
```

---

## Notebook Architecture

The notebook is divided into the following clearly labelled sections. Each section is a group of cells with a Markdown header.

---

### Section 0 — Environment Setup

**Purpose:** Install all required libraries and verify the environment.

**What to do:**
- Use `%pip install` inside a cell to install all dependencies.
- Print a confirmation message for each library: installed or already present.
- Define a global `NOTEBOOK_ROOT` path variable that all other sections reference.

**Libraries to install:**
| Category | Libraries |
|---|---|
| 2D Graphics | `pygame`, `matplotlib`, `Pillow` |
| Advanced Visuals | `moderngl`, `pycairo` |
| 3D Rendering | `pythreejs`, `vtk` |
| Generative Art | `noise`, `numpy` |
| Simulations | `scipy`, `pymunk` |
| Animation | `manim`, `matplotlib` (animation module) |
| UI Controls | `ipywidgets` |
| Fast Math | `numpy`, `numba` |

---

### Section 1 — Core Engine (Write Modules to Disk)

**Purpose:** Use `%%writefile` cells to write all supporting Python modules into the `patterns/`, `engines/`, and `utils/` directories.

**What to do:**
- Each `%%writefile` cell writes exactly one module file.
- Every pattern class inherits from a base `BasePattern` class defined in `engines/renderer.py`.
- The `BasePattern` interface must expose two methods: `render()` and `get_controls()`.
- After all files are written, run `import` cells to load them into the notebook namespace.
- Define the **Design Registry** — a dictionary mapping pattern names to class instances:

```python
PATTERNS = {
    # Geometric & Mathematical
    "Mandelbrot Fractal Explorer": MandelbrotRenderer(),
    "Julia Set Animator": JuliaRenderer(),
    "Sierpinski Triangle": SierpinskiRenderer(),
    # ... all 100 entries
}
```

---

### Section 2 — UI Controls

**Purpose:** Build the interactive gallery interface using `ipywidgets`.

**What to do:**
- Create a **Category Dropdown** with 6 options matching the 6 pattern files.
- Create a **Pattern Dropdown** that updates dynamically based on the selected category.
- Add universal controls available for all patterns:
  - Color palette picker (dropdown with preset palettes)
  - Animation speed slider (0.1x to 5x)
  - Resolution selector (Low / Medium / High)
  - Export button (saves current output to `exports/`)
- Add a **Pattern-Specific Controls** area: an `Output` widget that displays sliders and toggles unique to each design when it is selected. These are returned by each pattern's `get_controls()` method.
- Use `ipywidgets.interact` and `observe` callbacks to wire everything together.

**UI Layout:**
```
[ Category Dropdown ]   [ Pattern Dropdown ]
──────────────────────────────────────────────
[ Speed ]  [ Resolution ]  [ Palette ]
[ Pattern-Specific Controls (dynamic) ]
──────────────────────────────────────────────
[ RENDER ]                      [ EXPORT ]
──────────────────────────────────────────────
[ Output Display Area ]
```

---

### Section 3 — Render Section

**Purpose:** The single cell that triggers rendering.

**What to do:**
- On clicking the RENDER button, call:
  ```python
  PATTERNS[selected_pattern].render(**current_params)
  ```
- Use **lazy loading**: only instantiate a pattern's renderer the first time it is selected. Store already-loaded renderers in a cache dict.
- Display output inline using `IPython.display` for matplotlib figures, or embed a canvas for pygame/moderngl outputs.
- For animated patterns, render into a temporary GIF or MP4 in `exports/` and display it inline using `IPython.display.Video` or `display.Image`.

---

### Section 4 — Pattern Implementations (100 Designs)

This is the largest section. Each pattern is implemented as a class inside one of the six module files written in Section 1.

**Implementation rules for every pattern class:**
1. Inherits from `BasePattern`.
2. Has a `render(self, **kwargs)` method that produces its visual output.
3. Has a `get_controls(self)` method that returns a list of `ipywidgets` controls specific to this pattern.
4. Does not load any assets or run heavy computation at `__init__` time — only inside `render()`.
5. All random seeds are controllable via a parameter so results are reproducible.
6. **Every single pattern must be immediately followed by a dedicated Markdown cell containing a Concept Note.** This is a non-negotiable structural requirement. See the full specification in the "Pattern Concept Notes" section below.

**Pattern groups and their primary libraries:**

| Group | Ideas | Primary Libraries |
|---|---|---|
| Geometric & Mathematical | 1–20 | `numpy`, `matplotlib`, `moderngl` |
| Nature-Inspired | 21–40 | `noise`, `scipy`, `matplotlib.animation` |
| Abstract & Artistic | 41–60 | `pycairo`, `Pillow`, `matplotlib` |
| 2D Game-Style | 61–70 | `pygame`, `numpy` |
| 3D Objects & Sculptures | 71–90 | `pythreejs`, `vtk`, `moderngl` |
| Scientific & Simulation | 91–100 | `scipy`, `pymunk`, `numpy` |

---

### Section 5 — Export Utilities

**Purpose:** Let the user save any rendered output.

**What to do:**
- `export_png(figure, name)` — saves a matplotlib figure as PNG to `exports/`.
- `export_gif(frames, name, fps)` — saves a list of frames as an animated GIF.
- `export_mp4(frames, name, fps)` — saves frames as an MP4 using `matplotlib.animation.FFMpegWriter` if ffmpeg is available, otherwise falls back to GIF.
- All export functions print the absolute save path after writing.
- The EXPORT button in Section 2 calls the appropriate function based on the active pattern's output type.

---

## Pattern Concept Notes (Mandatory for All 100 Patterns)

This is a core structural requirement of the notebook. After every single pattern — meaning after its code cell and its rendered output — there must be a Markdown cell titled **"How This Works"** that explains the concept, mathematics, and logic behind that specific pattern.

This requirement applies to all 100 patterns without exception. A pattern is considered incomplete if its Concept Note cell is missing.

---

### What the Concept Note Must Contain

Each Concept Note Markdown cell must cover all four of the following parts:

**Part 1 — The Core Idea**
One to three sentences explaining the concept in plain language. What is this pattern? Where does it come from — mathematics, physics, nature, computer graphics? What makes it visually interesting?

**Part 2 — The Mathematics**
A precise explanation of the underlying mathematical or algorithmic foundation. This must include:
- The key formula, recurrence relation, rule set, or equation that drives the pattern, written using LaTeX inline math (`$...$`) or block math (`$$...$$`) so it renders properly in JupyterLab.
- The meaning of each variable or parameter in that formula.
- How changing those parameters (the ones exposed in the UI controls) affects the output mathematically.

**Part 3 — The Logic Implemented in the Code**
A step-by-step walkthrough of how the `render()` method translates the mathematics into pixels or geometry. This is not a line-by-line code commentary — it is a higher-level explanation of the algorithmic steps:
- What data structures are set up and why.
- What the main loop or vectorized operation is doing at each iteration.
- How the numerical output is mapped to visual properties (color, position, brightness, scale).
- Any optimizations used (numpy vectorization, early escape conditions, spatial indexing, etc.) and why they are necessary for this particular pattern.

**Part 4 — Interesting Properties or Variations**
One short paragraph noting one or two mathematically or visually notable properties of the pattern. For example: what happens at the boundary between stable and chaotic regions, why self-similarity appears, how the pattern relates to other patterns in the notebook, or what a well-known variation of this algorithm looks like.

---

### Formatting Rules for Concept Notes

- The Markdown cell must begin with the heading: `### How This Works — [Pattern Name]`
- Use LaTeX for all formulas. Do not write formulas as plain text.
- Keep each Concept Note focused and precise. The target length is 150 to 300 words. Do not pad with filler sentences.
- Do not repeat code from the implementation cell. Refer to variable names by name when needed, but do not paste blocks of code into the Concept Note.
- Write for an audience that understands Python and basic calculus but may not be familiar with this specific algorithm or mathematical domain.

---

### Example Structure (Mandelbrot Fractal Explorer)

The cell immediately after the Mandelbrot render cell must look like this:

```markdown
### How This Works — Mandelbrot Fractal Explorer

**Core Idea**
The Mandelbrot set is the set of complex numbers $c$ for which the sequence produced
by iterating $z_{n+1} = z_n^2 + c$ (starting from $z_0 = 0$) remains bounded — that
is, never escapes to infinity. Points inside the set are colored black; points outside
are colored by how quickly they escape, producing the iconic fractal boundary.

**Mathematics**
The iteration is:
$$z_{n+1} = z_n^2 + c, \quad z_0 = 0, \quad c \in \mathbb{C}$$
Each pixel on screen maps to a value of $c = x + iy$, where $x$ and $y$ are the real
and imaginary axes of the complex plane. The escape condition is $|z_n| > 2$. The
`max_iter` control sets the iteration ceiling: higher values reveal finer boundary
detail at the cost of computation time.

**Logic in the Code**
1. A 2D numpy array of complex numbers is constructed by meshgridding the x and y
   ranges of the viewport.
2. The iteration $z = z^2 + c$ is applied element-wise across the entire array each
   step, using numpy broadcasting — no Python loop over pixels.
3. An escape mask tracks which pixels have crossed $|z| > 2$. Those pixels are frozen
   (their iteration count recorded) and excluded from subsequent steps.
4. The iteration count array is passed through a colormap to produce the final image.

**Interesting Properties**
The Mandelbrot set is infinitely self-similar: zooming into any part of the boundary
reveals structures that resemble — but are not identical to — the whole set. The
`zoom` and `center` controls allow exploration of this property directly.
```

---

### Placement Rule

The exact cell order for every pattern must be:

```
[Markdown cell]   ← Pattern heading and one-line description
[Code cell]       ← The render() class implementation
[Output cell]     ← The rendered visual (produced by running the code cell)
[Markdown cell]   ← "How This Works" Concept Note  ← MANDATORY
```

This order must be maintained consistently across all 100 patterns. The Concept Note always comes after the output, never before.

---

## Build Order for the AI Coding Assistant

This project is built over **1 to 2 months**. The AI coding assistant must never attempt to implement all 100 patterns in a single session. Work is driven entirely by the owner's daily command. The assistant waits, does nothing, and touches no pattern code until it receives an explicit instruction for that day.

---

### The Cardinal Rule

> **Do not build anything that has not been explicitly asked for today.**

If the owner has not given a command, the assistant's only permitted actions are: answering questions about the plan, reviewing already-committed code, or preparing setup infrastructure (Steps 1–4 below). Pattern implementation — writing render code, writing Concept Notes, pushing commits — only happens when the owner says so.

---

### Phase 0 — One-Time Foundation Setup (Do This First, Once)

This phase is done in a single session before any pattern work begins. It does not count toward the 100 patterns.

**Step 1 — Repository Initialization**
- Create the GitHub repository with a `README.md` that describes the project.
- Set up the folder structure (`patterns/`, `engines/`, `utils/`, `assets/`, `shaders/`, `exports/`).
- Add a `.gitignore` that excludes: `exports/`, `__pycache__/`, `.ipynb_checkpoints/`, `*.pyc`.
- Commit with message: `chore: initialize project structure`

**Step 2 — Environment Setup (Section 0 of the notebook)**
- Write the environment setup cells: `%pip install` for all libraries, confirmation prints, `NOTEBOOK_ROOT` variable.
- Commit with message: `chore: add environment setup cells`

**Step 3 — Core Engine (Section 1 of the notebook)**
- Write `engines/renderer.py` with the `BasePattern` base class.
- Write `engines/color_utils.py` with at least 5 preset palettes.
- Write `utils/export.py` with the three export functions (`export_png`, `export_gif`, `export_mp4`).
- Write `utils/physics.py` as an empty module with a placeholder comment.
- Commit with message: `feat: add core engine — BasePattern, color utils, export utils`

**Step 4 — Stub All 100 Pattern Classes**
- For each of the 6 pattern module files, write a stub class for every pattern in that group.
- Each stub `render()` simply plots a titled placeholder rectangle. Each stub `get_controls()` returns an empty list.
- Populate the full `PATTERNS` registry dict with all 100 stubs.
- Commit with message: `feat: stub all 100 pattern classes and populate registry`

**Step 5 — Build the UI (Section 2 of the notebook)**
- Build the full `ipywidgets` UI: category dropdown, pattern dropdown, universal controls, pattern-specific controls area, RENDER button, EXPORT button, output area.
- Verify the UI renders and clicking RENDER invokes the stub for the selected pattern.
- Commit with message: `feat: add interactive UI — dropdowns, controls, render and export buttons`

After Step 5 is committed and verified, Phase 0 is complete. The notebook is now a fully working shell. **Stop here and wait for the first daily pattern command.**

---

### Phase 1 — Daily Pattern Implementation (The Main Phase)

This phase lasts the full duration of the project. Every working session begins with the owner issuing a command in this format:

> **"Today we are making: [Pattern Name 1], [Pattern Name 2], [Pattern Name 3]"**

The assistant must not start, assume, or pre-emptively build any pattern that is not listed in that day's command.

---

#### What the Assistant Does Each Day

Upon receiving the daily command, the assistant executes the following steps for each named pattern, one at a time, before moving to the next:

1. **Identify the pattern** in the `PATTERNS` registry and locate its stub class in the correct module file.
2. **Replace the stub** `render()` method with the full working implementation.
3. **Implement `get_controls()`** with the pattern-specific `ipywidgets` controls.
4. **Run the pattern** and confirm it renders without errors at Low resolution.
5. **Write the Concept Note** Markdown cell immediately after the output cell — covering all four parts: Core Idea, Mathematics (with LaTeX), Logic in the Code, Interesting Properties.
6. **Verify** the Concept Note LaTeX renders correctly in JupyterLab.
7. **Commit to GitHub** — see commit rules below.

Only after all of these steps are verified for one pattern does the assistant move on to the next pattern in that day's list.

---

#### Daily GitHub Commit Rules

Each pattern completed in a session gets its own individual commit. Do not batch multiple patterns into one commit.

**Commit message format:**
```
feat(pattern): add [Pattern Name] — [Group Name]
```

**Examples:**
```
feat(pattern): add Mandelbrot Fractal Explorer — Geometric & Mathematical
feat(pattern): add Cherry Blossom Particle Scene — Nature-Inspired
feat(pattern): add Rotating DNA Helix — 3D Objects & Sculptures
```

After all patterns for the day are committed individually, push all commits to the `main` branch in one push:
```
git push origin main
```

Then confirm to the owner how many patterns are now complete out of 100, e.g.: `"3 of 100 patterns complete. Pushed to main."`

---

#### End-of-Session Checklist

Before finishing a session, the assistant must verify:
- [ ] Every pattern built today renders without errors at Low resolution.
- [ ] Every pattern built today has a complete Concept Note with working LaTeX.
- [ ] Every pattern built today has its own individual commit with the correct message format.
- [ ] All commits have been pushed to `main`.
- [ ] The `PATTERNS` registry still loads cleanly (no import errors from today's changes).
- [ ] No stub patterns were accidentally broken by today's edits.

---

### Recommended Implementation Order (Across the Full Project)

This is the suggested order for which patterns to tackle across the weeks. The owner is free to deviate from this order in their daily commands — this is guidance, not a constraint.

| Week | Suggested Patterns | Group | Actual Completion |
|---|---|---|---|
| Week 1 | Patterns 1–6 (Mandelbrot, Julia Set, Sierpinski, Koch Snowflake, Penrose Tiling, Voronoi) | Geometric & Mathematical | ✅ 2026-05-13 |
| Week 2 | Patterns 7–14 (Fibonacci Spiral through Chaos Attractor) | Geometric & Mathematical | ✅ 2026-05-13–14 |
| Week 3 | Patterns 15–20 (Wave Interference through Parametric Curve Art) | Geometric & Mathematical | ✅ 2026-05-16 |
| Week 4 | Patterns 91–96 (Neural Network Viz, Atom Simulator, Black Hole, Game of Life, Boids, Traffic) | Scientific & Simulation | ⬜ Pending |
| Week 5 | Patterns 97–100 + 21–24 (Ecosystem, Ant Colony, Fluid Dynamics, Quantum + first Nature patterns) | Mixed | ✅ 21–27 done 2026-05-18 |
| Week 6–7 | Patterns 25–40 | Nature-Inspired | ✅ 2026-05-18–21 |
| Week 7–8 | Patterns 41–60 | Abstract & Artistic | ✅ 2026-05-25 — all 20 done (41–47: 2026-05-23 · 48–54: 2026-05-24 · 55–60: 2026-05-25) |
| Week 9 | Patterns 61–70 | 2D Game-Style | ⬜ Pending |
| Week 10–12 | Patterns 71–90 | 3D Objects & Sculptures | ⬜ Pending |

The 3D group (71–90) is deliberately placed last — it has the heaviest dependencies and most complex rendering code.

---

### Phase 2 — Final Polish (Last Session)

This phase is a single session done after all 100 patterns are complete and committed.

- Add a Table of Contents Markdown cell at the very top of the notebook with anchor links to all 100 pattern sections.
- Verify all 100 patterns render at Low resolution in a clean kernel restart (no import errors, no stale state).
- Update the `README.md` on GitHub with: project description, screenshot of at least 3 patterns, setup instructions, and the full list of all 100 pattern names.
- Commit with message: `docs: final polish — TOC, README update, full notebook verification`
- Push and tag the release: `git tag v1.0.0 && git push origin v1.0.0`

---

## Performance Rules

- **Never load all 100 patterns at startup.** Use the lazy loading cache described in Section 3.
- Heavy patterns (fluid simulations, volumetric rendering, neural visualizations, terrain generation) must default to Low resolution on first render.
- Any pattern that takes longer than 10 seconds at Medium resolution must display a progress bar using `tqdm` or `ipywidgets.IntProgress`.
- Matplotlib figures must be explicitly closed with `plt.close()` after display to prevent memory accumulation across many renders.

---

## Definition of Done

The project is complete when:
- All 100 patterns render without unhandled exceptions.
- Every pattern has at least one working control beyond the universal ones.
- Every pattern is followed by a "How This Works" Concept Note Markdown cell covering all four required parts: Core Idea, Mathematics (with LaTeX), Logic in the Code, and Interesting Properties.
- All LaTeX formulas in Concept Notes render correctly in JupyterLab (no broken `$` syntax).
- The EXPORT function works for at least PNG output on all 100 patterns.
- A new user can open the notebook, run all cells top-to-bottom, and immediately use the UI to browse and render any pattern without reading any code.
- A reader with no prior knowledge of a pattern can read its Concept Note and understand what mathematical idea produces the visual they are looking at.
