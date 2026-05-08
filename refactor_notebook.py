import json

def markdown_cell(source):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in source.split('\n')]
    }

def code_cell(source):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in source.split('\n')]
    }

# Load the original notebook to keep metadata and other sections
with open("visual_engine/notebook.ipynb", "r") as f:
    nb = json.load(f)

# Clear Section 1 pattern writing cells (they are indices 9 to 14 in the original list)
# Let's find them by content
new_cells = []
for cell in nb['cells']:
    if 'patterns/fractals.py' in str(cell.get('source', [])):
        continue
    if 'patterns/nature.py' in str(cell.get('source', [])):
        continue
    if 'patterns/abstract.py' in str(cell.get('source', [])):
        continue
    if 'patterns/game2d.py' in str(cell.get('source', [])):
        continue
    if 'patterns/objects3d.py' in str(cell.get('source', [])):
        continue
    if 'patterns/scientific.py' in str(cell.get('source', [])):
        continue
    new_cells.append(cell)

# Re-insert initialization for pattern files in Section 1 (after patterns/__init__.py cell)
# Let's find where Section 1 ends.
idx = 0
for i, cell in enumerate(new_cells):
    if 'Section 2' in str(cell.get('source', [])):
        idx = i
        break

init_patterns_cell = code_cell("""import os
for f in ['fractals.py', 'nature.py', 'abstract.py', 'game2d.py', 'objects3d.py', 'scientific.py']:
    path = os.path.join('patterns', f)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as file:
        file.write('import numpy as np\\nimport matplotlib.pyplot as plt\\nfrom ipywidgets import FloatSlider, IntSlider\\nfrom engines.renderer import BasePattern\\nfrom scipy.spatial import Voronoi, voronoi_plot_2d\\n\\n')
""")
new_cells.insert(idx, init_patterns_cell)

# Now go to Section 4 and add patterns
# Find Section 4
s4_idx = 0
for i, cell in enumerate(new_cells):
    if 'Section 4' in str(cell.get('source', [])):
        s4_idx = i
        break

# Pattern 1
new_cells.insert(s4_idx + 1, markdown_cell("## 1. Mandelbrot Fractal Explorer"))
new_cells.insert(s4_idx + 2, code_cell("""%%writefile -a patterns/fractals.py

class MandelbrotFractalExplorerRenderer(BasePattern):
    def get_controls(self):
        return [
            FloatSlider(value=1.0, min=0.1, max=100.0, step=0.1, description='Zoom:'),
            FloatSlider(value=-0.5, min=-2.0, max=1.0, step=0.01, description='Center X:'),
            FloatSlider(value=0.0, min=-1.5, max=1.5, step=0.01, description='Center Y:'),
            IntSlider(value=100, min=10, max=1000, step=10, description='Max Iter:')
        ]

    def render(self, zoom=1.0, center_x=-0.5, center_y=0.0, max_iter=100, **kwargs):
        width, height = 800, 800
        x_min, x_max = center_x - 1.5/zoom, center_x + 1.5/zoom
        y_min, y_max = center_y - 1.5/zoom, center_y + 1.5/zoom
        x = np.linspace(x_min, x_max, width)
        y = np.linspace(y_min, y_max, height)
        X, Y = np.meshgrid(x, y)
        C = X + 1j * Y
        Z = np.zeros_like(C)
        M = np.full(C.shape, True, dtype=bool)
        N = np.zeros(C.shape, dtype=int)
        for i in range(max_iter):
            mask = M & (np.abs(Z) <= 2)
            if not np.any(mask): break
            Z[mask] = Z[mask] * Z[mask] + C[mask]
            N[mask] = i
            M[np.abs(Z) > 2] = False
        plt.figure(figsize=(10, 10))
        plt.imshow(N, extent=(x_min, x_max, y_min, y_max), cmap='magma')
        plt.colorbar(label='Iterations')
        plt.title(f"Mandelbrot Set (zoom={zoom}, iter={max_iter})")
        plt.axis('off')
        plt.show()
"""))
new_cells.insert(s4_idx + 3, markdown_cell("""### How This Works — Mandelbrot Fractal Explorer

**Core Idea**
The Mandelbrot set is the set of complex numbers $c$ for which the sequence produced by iterating $z_{n+1} = z_n^2 + c$ remains bounded. It is a famous example of fractal geometry, exhibiting infinite complexity and self-similarity at all scales.

**Mathematics**
The iteration follows:
$$z_{n+1} = z_n^2 + c, \quad z_0 = 0$$
where $z$ and $c$ are complex numbers. A point $c$ belongs to the set if $|z_n| \\le 2$ for all $n$. In practice, we check if the magnitude exceeds 2 within a fixed number of iterations (`max_iter`).

**Logic in the Code**
1. We create a 2D grid of complex numbers representing the complex plane within the viewport.
2. We iterate the formula $z^2 + c$ using NumPy's vectorized operations for efficiency.
3. We maintain a mask of points that haven't \"escaped\" (magnitude $\\le 2$).
4. The final image displays the number of iterations it took for each point to escape, mapped to a colormap.

**Interesting Properties**
The boundary of the Mandelbrot set is a fractal. Any zoom into the boundary reveals smaller, distorted copies of the entire set, along with unique structures like \"filaments\" and \"mini-Mandelbrots.\"
"""))

# Pattern 2
new_cells.insert(s4_idx + 4, markdown_cell("## 2. Julia Set Animator"))
new_cells.insert(s4_idx + 5, code_cell("""%%writefile -a patterns/fractals.py

class JuliaSetAnimatorRenderer(BasePattern):
    def get_controls(self):
        return [
            FloatSlider(value=-0.7, min=-2.0, max=2.0, step=0.01, description='C Real:'),
            FloatSlider(value=0.27, min=-2.0, max=2.0, step=0.01, description='C Imag:'),
            IntSlider(value=100, min=10, max=1000, step=10, description='Max Iter:'),
            FloatSlider(value=1.0, min=0.1, max=10.0, step=0.1, description='Zoom:')
        ]

    def render(self, c_real=-0.7, c_imag=0.27, max_iter=100, zoom=1.0, **kwargs):
        width, height = 800, 800
        x_min, x_max = -1.5/zoom, 1.5/zoom
        y_min, y_max = -1.5/zoom, 1.5/zoom
        x = np.linspace(x_min, x_max, width)
        y = np.linspace(y_min, y_max, height)
        X, Y = np.meshgrid(x, y)
        Z = X + 1j * Y
        C = complex(c_real, c_imag)
        M = np.full(Z.shape, True, dtype=bool)
        N = np.zeros(Z.shape, dtype=int)
        for i in range(max_iter):
            mask = M & (np.abs(Z) <= 2)
            if not np.any(mask): break
            Z[mask] = Z[mask] * Z[mask] + C
            N[mask] = i
            M[np.abs(Z) > 2] = False
        plt.figure(figsize=(10, 10))
        plt.imshow(N, extent=(x_min, x_max, y_min, y_max), cmap='twilight')
        plt.colorbar(label='Iterations')
        plt.title(f"Julia Set (c={C}, zoom={zoom})")
        plt.axis('off')
        plt.show()
"""))
new_cells.insert(s4_idx + 6, markdown_cell("""### How This Works — Julia Set Animator

**Core Idea**
Julia sets are closely related to the Mandelbrot set. While the Mandelbrot set varies $c$ with $z_0=0$, a Julia set fixes $c$ and varies the starting value $z_0$. Each point $c$ in the complex plane corresponds to a unique Julia set.

**Mathematics**
The iteration is:
$$z_{n+1} = z_n^2 + c$$
The value of $c$ is constant for the entire image. If $c$ is chosen from within the Mandelbrot set, the resulting Julia set is \"connected.\" If $c$ is outside, the Julia set is a \"Cantor dust\" (totally disconnected).

**Logic in the Code**
1. Similar to the Mandelbrot implementation, but the grid of complex numbers represents the initial values $z_0$.
2. The constant $c$ is provided by the user via `c_real` and `c_imag` controls.
3. Vectorized iteration and escape-time coloring produce the visual.

**Interesting Properties**
Julia sets often exhibit beautiful rotational symmetry and elaborate spiral patterns. Small changes in the constant $c$ can lead to dramatic transformations in the shape of the set.
"""))

# Pattern 3
new_cells.insert(s4_idx + 7, markdown_cell("## 3. Sierpinski Triangle"))
new_cells.insert(s4_idx + 8, code_cell("""%%writefile -a patterns/fractals.py

class SierpinskiTriangleRenderer(BasePattern):
    def get_controls(self):
        return [IntSlider(value=5000, min=100, max=20000, step=500, description='Iterations:')]

    def render(self, iterations=5000, **kwargs):
        vertices = np.array([[0, 0], [1, 0], [0.5, np.sqrt(3)/2]])
        points = [np.array([0.5, 0.5])]
        for _ in range(iterations):
            target = vertices[np.random.randint(3)]
            points.append((points[-1] + target) / 2)
        points = np.array(points)
        plt.figure(figsize=(10, 10))
        plt.scatter(points[:, 0], points[:, 1], s=1, c='blue', alpha=0.5)
        plt.title(f"Sierpinski Triangle (Chaos Game, {iterations} points)")
        plt.axis('equal')
        plt.axis('off')
        plt.show()
"""))
new_cells.insert(s4_idx + 9, markdown_cell("""### How This Works — Sierpinski Triangle

**Core Idea**
The Sierpinski Triangle is a fractal with a shape of an equilateral triangle, subdivided recursively into smaller equilateral triangles. This implementation uses the \"Chaos Game,\" a randomized algorithm that remarkably converges to the fractal shape.

**Mathematics**
1. Take three vertices of an equilateral triangle.
2. Start at a random point $P_0$.
3. In each step, randomly choose one of the three vertices and move halfway from the current point to that vertex:
$$P_{n+1} = \\frac{P_n + V_{random}}{2}$$

**Logic in the Code**
1. Define the three vertices of the triangle.
2. Start with an initial point and iterate the Chaos Game rule for a specified number of `iterations`.
3. Plot each resulting point. As the number of points increases, the empty spaces forming the nested triangles become clearly visible.

**Interesting Properties**
Despite being generated by random choices, the resulting pattern is perfectly deterministic in its overall structure. This is an example of an Iterated Function System (IFS).
"""))

# Pattern 4
new_cells.insert(s4_idx + 10, markdown_cell("## 4. Koch Snowflake"))
new_cells.insert(s4_idx + 11, code_cell("""%%writefile -a patterns/fractals.py

class KochSnowflakeRenderer(BasePattern):
    def get_controls(self):
        return [IntSlider(value=3, min=0, max=6, description='Depth:')]

    def render(self, depth=3, **kwargs):
        def get_koch_points(p1, p2, depth):
            if depth == 0: return [p1, p2]
            p1, p2 = np.array(p1), np.array(p2)
            v = p2 - p1
            s1, s3 = p1 + v/3, p1 + 2*v/3
            angle = np.pi/3
            rot = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
            s2 = s1 + rot @ (v/3)
            pts = []
            pts.extend(get_koch_points(p1, s1, depth-1)[:-1])
            pts.extend(get_koch_points(s1, s2, depth-1)[:-1])
            pts.extend(get_koch_points(s2, s3, depth-1)[:-1])
            pts.extend(get_koch_points(s3, p2, depth-1))
            return pts
        v1, v2, v3 = np.array([0, 0]), np.array([1, 0]), np.array([0.5, -np.sqrt(3)/2])
        pts = []
        pts.extend(get_koch_points(v1, v2, depth)[:-1])
        pts.extend(get_koch_points(v2, v3, depth)[:-1])
        pts.extend(get_koch_points(v3, v1, depth))
        pts = np.array(pts)
        plt.figure(figsize=(10, 10))
        plt.plot(pts[:, 0], pts[:, 1], 'b-')
        plt.title(f"Koch Snowflake (depth={depth})")
        plt.axis('equal')
        plt.axis('off')
        plt.show()
"""))
new_cells.insert(s4_idx + 12, markdown_cell("""### How This Works — Koch Snowflake

**Core Idea**
The Koch Snowflake is one of the earliest fractal curves to be described. It is constructed by starting with an equilateral triangle and recursively replacing the middle third of each line segment with two sides of a smaller equilateral triangle pointing outwards.

**Mathematics**
For each line segment of length $L$:
1. Divide it into three segments of length $L/3$.
2. Replace the middle segment with two segments of length $L/3$ that form an equilateral triangle \"spike.\"
3. The total length increases by a factor of 4/3 at each iteration, meaning the perimeter of the snowflake is infinite in the limit, while its area remains finite.

**Logic in the Code**
1. The `render` method uses a recursive function `get_koch_points` that splits segments according to the Koch rule.
2. It uses rotation matrices to calculate the position of the new \"spike\" vertex.
3. The recursion continues until the specified `depth` is reached.

**Interesting Properties**
The Koch Snowflake is a continuous curve that is nowhere differentiable. It is a classic example of a \"monster curve\" that challenged traditional 19th-century notions of geometry.
"""))

# Pattern 5
new_cells.insert(s4_idx + 13, markdown_cell("## 5. Penrose Tiling"))
new_cells.insert(s4_idx + 14, code_cell("""%%writefile -a patterns/fractals.py

class PenroseTilingRenderer(BasePattern):
    def get_controls(self):
        return [IntSlider(value=4, min=0, max=7, description='Generations:')]

    def render(self, generations=4, **kwargs):
        phi = (1 + np.sqrt(5)) / 2
        def subdivide(triangles):
            result = []
            for type, A, B, C in triangles:
                if type == 0:
                    P = A + (B - A) / phi
                    result += [(0, C, P, B), (1, P, C, A)]
                else:
                    Q, R = B + (A - B) / phi, B + (C - B) / phi
                    result += [(1, R, Q, B), (0, Q, R, A), (1, C, A, Q)]
            return result
        triangles = []
        for i in range(10):
            B = np.exp(1j * (2*i - 1) * np.pi / 10)
            C = np.exp(1j * (2*i + 1) * np.pi / 10)
            triangles.append((0, 0j, B, C) if i % 2 == 0 else (0, 0j, C, B))
        for _ in range(generations): triangles = subdivide(triangles)
        plt.figure(figsize=(10, 10))
        for type, A, B, C in triangles:
            pts = np.array([[A.real, A.imag], [B.real, B.imag], [C.real, C.imag]])
            poly = plt.Polygon(pts, facecolor='orange' if type == 0 else 'blue', edgecolor='white', linewidth=0.1)
            plt.gca().add_patch(poly)
        plt.axis('equal')
        plt.axis('off')
        plt.title(f"Penrose Tiling (Gens={generations})")
        plt.show()
"""))
new_cells.insert(s4_idx + 15, markdown_cell("""### How This Works — Penrose Tiling

**Core Idea**
Penrose tiling is a non-periodic tiling generated by an aperiodic set of prototiles. It was discovered by Roger Penrose. Unlike traditional tilings (like squares or hexagons), Penrose tilings lack translational symmetry but possess long-range order and five-fold rotational symmetry.

**Mathematics**
This implementation uses the \"P3\" tiling, consisting of two types of rhombuses: \"thin\" and \"thick.\" The tiling is generated via \"deflation\" (or subdivision), where each tile is broken down into smaller tiles of the same two types according to specific geometric rules.

**Logic in the Code**
1. Start with an initial set of triangles (representing halves of the rhombuses) arranged in a sun-like pattern.
2. The `subdivide` function applies the deflation rules to each triangle, creating a new generation of smaller triangles.
3. After several `generations`, the triangles are rendered as polygons with colors distinguishing the \"thin\" and \"thick\" types.

**Interesting Properties**
Penrose tilings are related to quasicrystals, which are materials with atomic structures that are ordered but not periodic. They are a physical manifestation of these mathematical patterns.
"""))

# Pattern 6
new_cells.insert(s4_idx + 16, markdown_cell("## 6. Voronoi Diagram"))
new_cells.insert(s4_idx + 17, code_cell("""%%writefile -a patterns/fractals.py

class VoronoiDiagramRenderer(BasePattern):
    def get_controls(self):
        return [IntSlider(value=20, min=5, max=100, step=5, description='Points:')]

    def render(self, num_points=20, **kwargs):
        from scipy.spatial import Voronoi, voronoi_plot_2d
        points = np.random.rand(num_points, 2)
        vor = Voronoi(points)
        fig, ax = plt.subplots(figsize=(10, 10))
        voronoi_plot_2d(vor, ax=ax, show_vertices=False, line_colors='black', line_width=1, line_alpha=0.6, point_size=2)
        for region_index in vor.point_region:
            region = vor.regions[region_index]
            if not -1 in region and len(region) > 0:
                polygon = [vor.vertices[i] for i in region]
                plt.fill(*zip(*polygon), alpha=0.4)
        plt.title(f"Voronoi Diagram ({num_points} points)")
        plt.xlim(0, 1); plt.ylim(0, 1); plt.axis('off')
        plt.show()
"""))
new_cells.insert(s4_idx + 18, markdown_cell("""### How This Works — Voronoi Diagram

**Core Idea**
A Voronoi diagram is a partition of a plane into regions close to each of a given set of objects. In the simplest case, these objects are just points (called seeds), and for each seed, there is a corresponding region consisting of all points of the plane closer to that seed than to any other.

**Mathematics**
Given a set of points $S = \{p_1, p_2, ..., p_n\}$, the Voronoi cell $R_i$ for $p_i$ is:
$$R_i = \{x \\in \\mathbb{R}^2 \\mid d(x, p_i) \\le d(x, p_j) \\text{ for all } j \\ne i\}$$
where $d$ is the Euclidean distance. The boundaries of the cells are segments of perpendicular bisectors of the lines connecting neighboring seeds.

**Logic in the Code**
1. Generate a set of random seed points in a unit square.
2. Use `scipy.spatial.Voronoi` to efficiently compute the vertices and regions of the diagram.
3. Render the regions as colored polygons and the seed points themselves.

**Interesting Properties**
Voronoi diagrams appear everywhere in nature: from the patterns on a giraffe's coat and the structure of dragonfly wings to the way bubbles pack together and how cities are partitioned into service areas.
"""))

# Stub for the rest of fractals.py to keep the file valid if we run it
new_cells.insert(s4_idx + 19, code_cell("""%%writefile -a patterns/fractals.py

class FibonacciSpiralRenderer(BasePattern): pass
class DragonCurveRenderer(BasePattern): pass
class HilbertCurveRenderer(BasePattern): pass
class LSystemTreeRenderer(BasePattern): pass
class ApolloniusGasketRenderer(BasePattern): pass
class LissajousFiguresRenderer(BasePattern): pass
class RoseCurvesRenderer(BasePattern): pass
class ChaosAttractorLorenzRenderer(BasePattern): pass
class WaveInterferencePatternRenderer(BasePattern): pass
class HypocycloidAndEpicycloidRenderer(BasePattern): pass
class TruchetTilesRenderer(BasePattern): pass
class HexagonalGridArtRenderer(BasePattern): pass
class SpirographGeneratorRenderer(BasePattern): pass
class ParametricCurveArtRenderer(BasePattern): pass
"""))

# Update notebook cells
nb['cells'] = new_cells
with open("visual_engine/notebook.ipynb", "w", encoding='utf-8') as f:
    json.dump(nb, f, indent=1)
