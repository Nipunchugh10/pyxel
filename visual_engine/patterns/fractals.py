"""
Geometric & Mathematical Patterns (1–20)
Each class is a stub that will be replaced with full implementations during Phase 1.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from engines.renderer import BasePattern
from engines.color_utils import ColorUtils


class _StubMixin:
    """Shared stub render logic."""
    def render(self, resolution="Low", palette="Inferno", speed=1.0, **kwargs):
        fig, ax = plt.subplots(figsize=(6, 6), facecolor="#0f0f0f")
        ax.set_facecolor("#0f0f0f")
        rect = patches.FancyBboxPatch((0.1, 0.1), 0.8, 0.8,
                                       boxstyle="round,pad=0.05",
                                       linewidth=2, edgecolor="#555",
                                       facecolor="#1a1a2e")
        ax.add_patch(rect)
        ax.text(0.5, 0.55, self.name, ha="center", va="center",
                fontsize=14, color="#e0e0e0", fontweight="bold",
                transform=ax.transAxes)
        ax.text(0.5, 0.42, "⏳ Coming Soon", ha="center", va="center",
                fontsize=11, color="#888", style="italic",
                transform=ax.transAxes)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        plt.tight_layout()
        plt.show()
        plt.close(fig)

    def get_controls(self):
        return []


class MandelbrotRenderer(BasePattern):
    """Pattern 1 — Mandelbrot Fractal Explorer."""
    name = "Mandelbrot Fractal Explorer"
    group = "Geometric & Mathematical"

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=100, min=20, max=500, step=10,
                              description="Max Iter:"),
            widgets.FloatSlider(value=1.0, min=0.1, max=100.0, step=0.1,
                                description="Zoom:", readout_format=".1f"),
            widgets.FloatSlider(value=-0.5, min=-2.5, max=1.5, step=0.01,
                                description="Center X:", readout_format=".2f"),
            widgets.FloatSlider(value=0.0, min=-1.5, max=1.5, step=0.01,
                                description="Center Y:", readout_format=".2f"),
            widgets.IntSlider(value=42, min=0, max=999,
                              description="Seed:"),
        ]

    def render(self, resolution="Low", palette="Inferno", speed=1.0, **kwargs):
        res = self._resolve_resolution(resolution)
        max_iter = int(kwargs.get("max_iter", 100))
        zoom = float(kwargs.get("zoom", 1.0))
        cx = float(kwargs.get("center_x", -0.5))
        cy = float(kwargs.get("center_y", 0.0))

        # Build complex plane grid
        half = 2.0 / zoom
        x = np.linspace(cx - half, cx + half, res)
        y = np.linspace(cy - half, cy + half, res)
        X, Y = np.meshgrid(x, y)
        C = X + 1j * Y

        # Vectorized escape-time iteration
        Z = np.zeros_like(C)
        escape = np.full(C.shape, max_iter, dtype=np.float64)
        mask = np.ones(C.shape, dtype=bool)

        for i in range(max_iter):
            Z[mask] = Z[mask] ** 2 + C[mask]
            escaped = mask & (np.abs(Z) > 2.0)
            # Smooth coloring: fractional escape count
            escape[escaped] = i + 1 - np.log2(np.log2(np.abs(Z[escaped]) + 1e-10))
            mask[escaped] = False
            if not mask.any():
                break

        cmap = ColorUtils.make_colormap(palette)
        fig, ax = self._create_figure(figsize=(8, 8), dpi=100)
        ax.imshow(escape, extent=[cx - half, cx + half, cy - half, cy + half],
                  cmap=cmap, origin="lower", interpolation="bilinear")
        ax.set_title("Mandelbrot Fractal Explorer", color="#e0e0e0",
                     fontsize=14, fontweight="bold", pad=12)
        ax.axis("off")
        plt.tight_layout()
        plt.show()
        plt.close(fig)


class JuliaRenderer(BasePattern):
    """Pattern 2 — Julia Set Animator."""
    name = "Julia Set Animator"
    group = "Geometric & Mathematical"

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=100, min=20, max=500, step=10,
                              description="Max Iter:"),
            widgets.FloatSlider(value=-0.7, min=-2.0, max=2.0, step=0.005,
                                description="C Real:", readout_format=".3f"),
            widgets.FloatSlider(value=0.27015, min=-2.0, max=2.0, step=0.005,
                                description="C Imag:", readout_format=".3f"),
            widgets.FloatSlider(value=1.0, min=0.1, max=50.0, step=0.1,
                                description="Zoom:", readout_format=".1f"),
            widgets.IntSlider(value=42, min=0, max=999,
                              description="Seed:"),
        ]

    def render(self, resolution="Low", palette="Inferno", speed=1.0, **kwargs):
        res = self._resolve_resolution(resolution)
        max_iter = int(kwargs.get("max_iter", 100))
        c_real = float(kwargs.get("c_real", -0.7))
        c_imag = float(kwargs.get("c_imag", 0.27015))
        zoom = float(kwargs.get("zoom", 1.0))
        c = complex(c_real, c_imag)

        half = 1.5 / zoom
        x = np.linspace(-half, half, res)
        y = np.linspace(-half, half, res)
        X, Y = np.meshgrid(x, y)
        Z = X + 1j * Y

        escape = np.full(Z.shape, max_iter, dtype=np.float64)
        mask = np.ones(Z.shape, dtype=bool)

        for i in range(max_iter):
            Z[mask] = Z[mask] ** 2 + c
            escaped = mask & (np.abs(Z) > 2.0)
            escape[escaped] = i + 1 - np.log2(np.log2(np.abs(Z[escaped]) + 1e-10))
            mask[escaped] = False
            if not mask.any():
                break

        cmap = ColorUtils.make_colormap(palette)
        fig, ax = self._create_figure(figsize=(8, 8), dpi=100)
        ax.imshow(escape, extent=[-half, half, -half, half],
                  cmap=cmap, origin="lower", interpolation="bilinear")
        ax.set_title(f"Julia Set  c = {c_real:+.3f}{c_imag:+.3f}i",
                     color="#e0e0e0", fontsize=14, fontweight="bold", pad=12)
        ax.axis("off")
        plt.tight_layout()
        plt.show()
        plt.close(fig)


class SierpinskiRenderer(BasePattern):
    """Pattern 3 — Sierpinski Triangle via recursive subdivision."""
    name = "Sierpinski Triangle"
    group = "Geometric & Mathematical"

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=6, min=1, max=9, step=1,
                              description="Depth:"),
            widgets.FloatSlider(value=1.5, min=0.2, max=4.0, step=0.1,
                                description="Line Width:", readout_format=".1f"),
            widgets.IntSlider(value=42, min=0, max=999,
                              description="Seed:"),
        ]

    def _subdivide(self, v0, v1, v2, depth):
        """Recursively subdivide a triangle into 3 sub-triangles."""
        if depth == 0:
            return [[v0, v1, v2]]
        m01 = (v0 + v1) / 2
        m12 = (v1 + v2) / 2
        m02 = (v0 + v2) / 2
        tris = []
        tris.extend(self._subdivide(v0, m01, m02, depth - 1))
        tris.extend(self._subdivide(m01, v1, m12, depth - 1))
        tris.extend(self._subdivide(m02, m12, v2, depth - 1))
        return tris

    def render(self, resolution="Low", palette="Inferno", speed=1.0, **kwargs):
        depth = int(kwargs.get("depth", 6))
        lw = float(kwargs.get("line_width", 1.5))

        # Equilateral triangle vertices
        v0 = np.array([0.0, 0.0])
        v1 = np.array([1.0, 0.0])
        v2 = np.array([0.5, np.sqrt(3) / 2])

        triangles = self._subdivide(v0, v1, v2, depth)
        colors = ColorUtils.gradient_array(palette, len(triangles))

        fig, ax = self._create_figure(figsize=(8, 8), dpi=100)
        for idx, tri in enumerate(triangles):
            polygon = plt.Polygon(tri, closed=True, fill=True,
                                  facecolor=colors[idx],
                                  edgecolor=(1, 1, 1, 0.15), linewidth=lw * 0.3)
            ax.add_patch(polygon)

        ax.set_xlim(-0.05, 1.05)
        ax.set_ylim(-0.05, 0.95)
        ax.set_aspect("equal")
        ax.set_title("Sierpinski Triangle", color="#e0e0e0",
                     fontsize=14, fontweight="bold", pad=12)
        ax.axis("off")
        plt.tight_layout()
        plt.show()
        plt.close(fig)


class KochRenderer(BasePattern):
    """Pattern 4 — Koch Snowflake via L-system line subdivision."""
    name = "Koch Snowflake"
    group = "Geometric & Mathematical"

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=4, min=0, max=7, step=1,
                              description="Iterations:"),
            widgets.FloatSlider(value=2.0, min=0.3, max=5.0, step=0.1,
                                description="Line Width:", readout_format=".1f"),
            widgets.IntSlider(value=42, min=0, max=999,
                              description="Seed:"),
        ]

    def _koch_points(self, p1, p2, depth):
        """Recursively subdivide a line segment into Koch curve points."""
        if depth == 0:
            return [p1]
        # Divide segment into thirds
        a = p1 + (p2 - p1) / 3
        b = p1 + 2 * (p2 - p1) / 3
        # Peak point — rotate middle third by 60°
        dx = b[0] - a[0]
        dy = b[1] - a[1]
        peak = np.array([
            a[0] + dx * np.cos(np.pi / 3) - dy * np.sin(np.pi / 3),
            a[1] + dx * np.sin(np.pi / 3) + dy * np.cos(np.pi / 3),
        ])
        pts = []
        pts.extend(self._koch_points(p1, a, depth - 1))
        pts.extend(self._koch_points(a, peak, depth - 1))
        pts.extend(self._koch_points(peak, b, depth - 1))
        pts.extend(self._koch_points(b, p2, depth - 1))
        return pts

    def render(self, resolution="Low", palette="Inferno", speed=1.0, **kwargs):
        iterations = int(kwargs.get("iterations", 4))
        lw = float(kwargs.get("line_width", 2.0))

        # Equilateral triangle vertices (snowflake base)
        s = 1.0
        h = s * np.sqrt(3) / 2
        v0 = np.array([0.0, h * 2 / 3])
        v1 = np.array([s, h * 2 / 3])
        v2 = np.array([s / 2, h * 2 / 3 - h])

        # Generate Koch curve for each edge
        all_pts = []
        for p1, p2 in [(v0, v1), (v1, v2), (v2, v0)]:
            all_pts.extend(self._koch_points(p1, p2, iterations))
        all_pts.append(all_pts[0])  # close the snowflake
        pts = np.array(all_pts)

        # Color segments
        n_seg = len(pts) - 1
        colors = ColorUtils.gradient_array(palette, n_seg)

        fig, ax = self._create_figure(figsize=(8, 8), dpi=100)
        for i in range(n_seg):
            ax.plot([pts[i, 0], pts[i + 1, 0]],
                    [pts[i, 1], pts[i + 1, 1]],
                    color=colors[i], linewidth=lw, solid_capstyle="round")

        ax.set_aspect("equal")
        margin = 0.1
        ax.set_xlim(pts[:, 0].min() - margin, pts[:, 0].max() + margin)
        ax.set_ylim(pts[:, 1].min() - margin, pts[:, 1].max() + margin)
        ax.set_title(f"Koch Snowflake — depth {iterations}", color="#e0e0e0",
                     fontsize=14, fontweight="bold", pad=12)
        ax.axis("off")
        plt.tight_layout()
        plt.show()
        plt.close(fig)


class PenroseRenderer(BasePattern):
    """Pattern 5 — Penrose Tiling via Robinson triangle deflation."""
    name = "Penrose Tiling"
    group = "Geometric & Mathematical"

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=5, min=1, max=8, step=1,
                              description="Generations:"),
            widgets.FloatSlider(value=0.5, min=0.1, max=3.0, step=0.1,
                                description="Line Width:", readout_format=".1f"),
            widgets.IntSlider(value=42, min=0, max=999,
                              description="Seed:"),
        ]

    def _deflate(self, triangles, generation):
        """
        Deflate Robinson triangles to produce Penrose P3 tiling.
        Each triangle is (color, A, B, C) where color is 0 (thin) or 1 (thick).
        """
        phi = (1 + np.sqrt(5)) / 2  # golden ratio

        for _ in range(generation):
            new_tris = []
            for color, A, B, C in triangles:
                if color == 0:  # thin (acute) triangle
                    P = A + (B - A) / phi
                    new_tris.append((0, C, P, B))
                    new_tris.append((1, P, C, A))
                else:  # thick (obtuse) triangle
                    Q = B + (A - B) / phi
                    R = B + (C - B) / phi
                    new_tris.append((1, R, C, A))
                    new_tris.append((1, Q, R, B))
                    new_tris.append((0, R, Q, A))
            triangles = new_tris
        return triangles

    def render(self, resolution="Low", palette="Inferno", speed=1.0, **kwargs):
        gen = int(kwargs.get("generations", 5))
        lw = float(kwargs.get("line_width", 0.5))

        # Start with a sun configuration — 10 triangles arranged in a circle
        triangles = []
        for i in range(10):
            angle1 = (2 * i - 1) * np.pi / 10
            angle2 = (2 * i + 1) * np.pi / 10
            B = np.array([np.cos(angle1), np.sin(angle1)])
            C = np.array([np.cos(angle2), np.sin(angle2)])
            if i % 2 == 0:
                triangles.append((0, np.array([0.0, 0.0]), B, C))
            else:
                triangles.append((0, np.array([0.0, 0.0]), C, B))

        triangles = self._deflate(triangles, gen)

        # Get colors — two shades for thin/thick
        palette_colors = ColorUtils.get_palette(palette)
        color_thin = palette_colors[2]
        color_thick = palette_colors[6]

        fig, ax = self._create_figure(figsize=(8, 8), dpi=100)
        for color, A, B, C in triangles:
            fc = color_thick if color == 1 else color_thin
            tri = plt.Polygon([A, B, C], closed=True, fill=True,
                              facecolor=fc, edgecolor=(1, 1, 1, 0.12),
                              linewidth=lw)
            ax.add_patch(tri)

        ax.set_xlim(-1.3, 1.3)
        ax.set_ylim(-1.3, 1.3)
        ax.set_aspect("equal")
        ax.set_title(f"Penrose Tiling — generation {gen}", color="#e0e0e0",
                     fontsize=14, fontweight="bold", pad=12)
        ax.axis("off")
        plt.tight_layout()
        plt.show()
        plt.close(fig)

class VoronoiRenderer(BasePattern):
    """Pattern 6 — Voronoi Diagram via KD-tree nearest-neighbour rasterization."""
    name = "Voronoi Diagram"
    group = "Geometric & Mathematical"

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=60, min=5, max=200, step=5,
                              description="Points:"),
            widgets.Checkbox(value=True, description="Show Points"),
            widgets.IntSlider(value=42, min=0, max=999,
                              description="Seed:"),
        ]

    def render(self, resolution="Low", palette="Inferno", speed=1.0, **kwargs):
        from scipy.spatial import cKDTree
        n_pts = int(kwargs.get("points", 60))
        show_pts = bool(kwargs.get("show_points", True))
        seed = int(kwargs.get("seed", 42))
        res = self._resolve_resolution(resolution)
        rng = np.random.default_rng(seed)

        pts = rng.random((n_pts, 2))  # seeds in [0, 1]²

        # Build pixel grid and query nearest seed
        lin = np.linspace(0.0, 1.0, res)
        gx, gy = np.meshgrid(lin, lin)
        grid = np.column_stack([gx.ravel(), gy.ravel()])
        tree = cKDTree(pts)
        _, nearest = tree.query(grid, k=1)
        nearest_img = nearest.reshape(res, res)

        colors = ColorUtils.gradient_array(palette, n_pts)  # (n_pts, 3)
        img = colors[nearest_img]  # (res, res, 3)

        fig, ax = self._create_figure(figsize=(8, 8), dpi=100)
        ax.imshow(img, extent=[0, 1, 0, 1], origin="lower", aspect="equal",
                  interpolation="nearest")

        if show_pts:
            ax.scatter(pts[:, 0], pts[:, 1], s=22, c="white", zorder=5,
                       alpha=0.9, edgecolors="black", linewidths=0.5)

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_title(f"Voronoi Diagram — {n_pts} sites", color="#e0e0e0",
                     fontsize=14, fontweight="bold", pad=12)
        ax.axis("off")
        plt.tight_layout()
        plt.show()
        plt.close(fig)

class FibonacciRenderer(BasePattern):
    """Pattern 7 — Fibonacci Spiral via the golden-angle sunflower model."""
    name = "Fibonacci Spiral"
    group = "Geometric & Mathematical"

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=500, min=50, max=2000, step=50,
                              description="Points:"),
            widgets.FloatSlider(value=3.0, min=0.5, max=10.0, step=0.5,
                                description="Point Size:", readout_format=".1f"),
            widgets.Checkbox(value=False, description="Show Lines"),
            widgets.IntSlider(value=42, min=0, max=999,
                              description="Seed:"),
        ]

    def render(self, resolution="Low", palette="Inferno", speed=1.0, **kwargs):
        n = int(kwargs.get("points", 500))
        pt_size = float(kwargs.get("point_size", 3.0))
        show_lines = bool(kwargs.get("show_lines", False))

        golden_angle = np.pi * (3.0 - np.sqrt(5.0))  # ≈ 137.508°
        i = np.arange(n)
        r = np.sqrt(i / n)
        theta = i * golden_angle
        x = r * np.cos(theta)
        y = r * np.sin(theta)

        colors = ColorUtils.gradient_array(palette, n)

        fig, ax = self._create_figure(figsize=(8, 8), dpi=100)
        if show_lines:
            ax.plot(x, y, color="white", alpha=0.15, linewidth=0.5, zorder=1)
        ax.scatter(x, y, c=colors, s=pt_size ** 2, alpha=0.88, zorder=2,
                   linewidths=0)

        ax.set_aspect("equal")
        ax.set_xlim(-1.1, 1.1)
        ax.set_ylim(-1.1, 1.1)
        ax.set_title(f"Fibonacci Spiral — {n} seeds", color="#e0e0e0",
                     fontsize=14, fontweight="bold", pad=12)
        ax.axis("off")
        plt.tight_layout()
        plt.show()
        plt.close(fig)

class DragonCurveRenderer(BasePattern):
    """Pattern 8 — Dragon Curve via iterative paper-fold turn sequence."""
    name = "Dragon Curve"
    group = "Geometric & Mathematical"

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=12, min=1, max=16, step=1,
                              description="Iterations:"),
            widgets.FloatSlider(value=1.0, min=0.2, max=3.0, step=0.1,
                                description="Line Width:", readout_format=".1f"),
            widgets.IntSlider(value=42, min=0, max=999,
                              description="Seed:"),
        ]

    def render(self, resolution="Low", palette="Inferno", speed=1.0, **kwargs):
        from matplotlib.collections import LineCollection
        iterations = int(kwargs.get("iterations", 12))
        lw = float(kwargs.get("line_width", 1.0))

        # Build turn sequence: 1 = right (+90°), -1 = left (−90°)
        turns = [1]
        for _ in range(iterations - 1):
            turns = turns + [1] + [-t for t in reversed(turns)]

        # Walk the path
        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]
        x, y = [0], [0]
        direction = 0
        for t in turns:
            direction = (direction + t) % 4
            x.append(x[-1] + dx[direction])
            y.append(y[-1] + dy[direction])

        coords = np.column_stack([x, y])          # (n+1, 2)
        segments = np.stack([coords[:-1], coords[1:]], axis=1)  # (n, 2, 2)
        colors = ColorUtils.gradient_array(palette, len(segments))

        fig, ax = self._create_figure(figsize=(8, 8), dpi=100)
        lc = LineCollection(segments, colors=colors, linewidths=lw,
                            capstyle="round")
        ax.add_collection(lc)

        margin = max(coords[:, 0].max() - coords[:, 0].min(),
                     coords[:, 1].max() - coords[:, 1].min()) * 0.04 + 0.5
        ax.set_xlim(coords[:, 0].min() - margin, coords[:, 0].max() + margin)
        ax.set_ylim(coords[:, 1].min() - margin, coords[:, 1].max() + margin)
        ax.set_aspect("equal")
        ax.set_title(f"Dragon Curve — {iterations} iterations", color="#e0e0e0",
                     fontsize=14, fontweight="bold", pad=12)
        ax.axis("off")
        plt.tight_layout()
        plt.show()
        plt.close(fig)

class HilbertCurveRenderer(BasePattern):
    """Pattern 9 — Hilbert Curve space-filling curve via index-to-XY mapping."""
    name = "Hilbert Curve"
    group = "Geometric & Mathematical"

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=5, min=1, max=8, step=1,
                              description="Order:"),
            widgets.FloatSlider(value=1.0, min=0.2, max=3.0, step=0.1,
                                description="Line Width:", readout_format=".1f"),
            widgets.IntSlider(value=42, min=0, max=999,
                              description="Seed:"),
        ]

    def _hilbert_xy(self, order: int) -> np.ndarray:
        """Return (4^order, 2) array of integer grid coords along the Hilbert path."""
        n = 1 << order       # 2^order
        total = n * n
        coords = np.empty((total, 2), dtype=np.float64)
        for d in range(total):
            x = y = 0
            t = d
            s = 1
            while s < n:
                rx = 1 if (t & 2) else 0
                ry = 1 if ((t & 1) ^ rx) else 0
                if ry == 0:
                    if rx == 1:
                        x = s - 1 - x
                        y = s - 1 - y
                    x, y = y, x
                x += s * rx
                y += s * ry
                t >>= 2
                s <<= 1
            coords[d] = (x, y)
        return coords

    def render(self, resolution="Low", palette="Inferno", speed=1.0, **kwargs):
        from matplotlib.collections import LineCollection
        order = int(kwargs.get("order", 5))
        lw = float(kwargs.get("line_width", 1.0))

        coords = self._hilbert_xy(order)
        segments = np.stack([coords[:-1], coords[1:]], axis=1)
        colors = ColorUtils.gradient_array(palette, len(segments))

        fig, ax = self._create_figure(figsize=(8, 8), dpi=100)
        lc = LineCollection(segments, colors=colors, linewidths=lw,
                            capstyle="round")
        ax.add_collection(lc)

        n = 1 << order
        ax.set_xlim(-0.5, n - 0.5)
        ax.set_ylim(-0.5, n - 0.5)
        ax.set_aspect("equal")
        ax.set_title(f"Hilbert Curve — order {order}  ({n}×{n} grid)",
                     color="#e0e0e0", fontsize=14, fontweight="bold", pad=12)
        ax.axis("off")
        plt.tight_layout()
        plt.show()
        plt.close(fig)

class LSystemTreeRenderer(BasePattern):
    """Pattern 10 — L-System Tree via string rewriting + turtle interpretation."""
    name = "L-System Tree"
    group = "Geometric & Mathematical"

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=5, min=1, max=7, step=1,
                              description="Iterations:"),
            widgets.FloatSlider(value=25.0, min=10.0, max=45.0, step=1.0,
                                description="Angle:", readout_format=".0f"),
            widgets.FloatSlider(value=5.0, min=1.0, max=15.0, step=0.5,
                                description="Branch Len:", readout_format=".1f"),
            widgets.IntSlider(value=42, min=0, max=999,
                              description="Seed:"),
        ]

    def _expand(self, n: int) -> str:
        """Expand the axiom for n iterations using Prusinkiewicz's branching tree."""
        # Axiom: X   Rules: X → F+[[X]-X]-F[-FX]+X,  F → FF
        rules = {
            "X": "F+[[X]-X]-F[-FX]+X",
            "F": "FF",
        }
        s = "X"
        for _ in range(n):
            s = "".join(rules.get(c, c) for c in s)
        return s

    def render(self, resolution="Low", palette="Inferno", speed=1.0, **kwargs):
        from matplotlib.collections import LineCollection
        iterations = int(kwargs.get("iterations", 5))
        angle_deg = float(kwargs.get("angle", 25.0))
        branch_len = float(kwargs.get("branch_len", 5.0))

        sentence = self._expand(iterations)
        angle_rad = np.radians(angle_deg)

        # Turtle interpretation
        stack = []
        x, y = 0.0, 0.0
        heading = np.pi / 2.0   # start pointing up
        depth = 0
        segments = []
        seg_depths = []

        for ch in sentence:
            if ch == "F":
                nx = x + branch_len * np.cos(heading)
                ny = y + branch_len * np.sin(heading)
                segments.append([(x, y), (nx, ny)])
                seg_depths.append(depth)
                x, y = nx, ny
            elif ch == "+":
                heading += angle_rad
            elif ch == "-":
                heading -= angle_rad
            elif ch == "[":
                stack.append((x, y, heading, depth))
                depth += 1
            elif ch == "]":
                x, y, heading, depth = stack.pop()

        if not segments:
            return

        palette_colors = ColorUtils.gradient_array(palette, max(seg_depths) + 1
                                                   if seg_depths else 1)
        colors = [palette_colors[min(d, len(palette_colors) - 1)]
                  for d in seg_depths]

        all_pts = np.array([pt for seg in segments for pt in seg])
        mx = all_pts[:, 0]
        my = all_pts[:, 1]
        pad_x = max((mx.max() - mx.min()) * 0.05, 1.0)
        pad_y = max((my.max() - my.min()) * 0.05, 1.0)

        fig, ax = self._create_figure(figsize=(8, 10), dpi=100)
        lc = LineCollection(segments, colors=colors, linewidths=1.0, alpha=0.92)
        ax.add_collection(lc)

        ax.set_xlim(mx.min() - pad_x, mx.max() + pad_x)
        ax.set_ylim(my.min() - pad_y, my.max() + pad_y)
        ax.set_aspect("equal")
        ax.set_title(
            f"L-System Tree — {iterations} iter, {angle_deg:.0f}°",
            color="#e0e0e0", fontsize=14, fontweight="bold", pad=12,
        )
        ax.axis("off")
        plt.tight_layout()
        plt.show()
        plt.close(fig)

class ApolloniusRenderer(BasePattern):
    """Pattern 11 — Apollonius Gasket via Descartes' Circle Theorem."""
    name = "Apollonius Gasket"
    group = "Geometric & Mathematical"

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=4, min=1, max=6, step=1,
                              description="Depth:"),
            widgets.FloatSlider(value=0.005, min=0.001, max=0.02, step=0.001,
                                description="Min Radius:", readout_format=".3f"),
            widgets.Checkbox(value=True, description="Show Boundary"),
        ]

    def _apollonius_circles(self, depth, min_r):
        """Generate gasket circles via BFS + Descartes' theorem."""
        from collections import deque

        # Three equal mutually tangent inner circles inscribed in the unit disk.
        # Their curvature k_s satisfies  3k² − 6k − 1 = 0  →  k_s = 1 + 2/√3
        k_s = 1.0 + 2.0 / np.sqrt(3.0)
        r_s = 1.0 / k_s
        d_s = 1.0 - r_s          # distance from origin to each inner center

        c0 = (-1.0,  0.0 + 0.0j)                                       # outer bounding circle
        c1 = ( k_s,  d_s * np.exp(1j * np.pi / 2))
        c2 = ( k_s,  d_s * np.exp(1j * (np.pi / 2 + 2 * np.pi / 3)))
        c3 = ( k_s,  d_s * np.exp(1j * (np.pi / 2 + 4 * np.pi / 3)))

        def _key(k, z):
            return (round(float(k), 4),
                    round(float(z.real), 4),
                    round(float(z.imag), 4))

        circles = {
            _key(*c0): (*c0, -1),
            _key(*c1): (*c1,  0),
            _key(*c2): (*c2,  0),
            _key(*c3): (*c3,  0),
        }

        # Each queue entry: (k1, z1, k2, z2, k3, z3, exploration_depth)
        queue = deque([
            (*c0, *c1, *c2, 0),
            (*c0, *c1, *c3, 0),
            (*c0, *c2, *c3, 0),
            (*c1, *c2, *c3, 0),
        ])

        MAX = 20_000
        while queue and len(circles) < MAX:
            k1, z1, k2, z2, k3, z3, d = queue.popleft()
            if d >= depth:
                continue

            # ── Descartes' theorem: k4 = (k1+k2+k3) ± 2√(k1k2+k2k3+k1k3)
            s_k = k1 + k2 + k3
            p_k = k1 * k2 + k2 * k3 + k1 * k3
            if p_k < 0:
                continue
            sq_k = np.sqrt(p_k)

            # ── Extended Descartes: k4·z4 = (k1z1+k2z2+k3z3) ± 2√(k1k2z1z2+…)
            s_z  = k1 * z1 + k2 * z2 + k3 * z3
            p_z  = k1*k2*z1*z2 + k2*k3*z2*z3 + k1*k3*z1*z3
            sq_z = np.sqrt(p_z + 0j)

            for sign in (+1, -1):
                k4 = s_k + sign * 2.0 * sq_k
                if k4 <= 1e-9:
                    continue                      # skip zero / negative curvature
                r4 = 1.0 / k4
                if r4 < min_r:
                    continue                      # too small to draw
                z4 = (s_z + sign * 2.0 * sq_z) / k4
                if abs(z4) + r4 > 1.001:
                    continue                      # outside bounding circle
                ck = _key(k4, z4)
                if ck in circles:
                    continue                      # already discovered
                circles[ck] = (k4, z4, d + 1)
                queue.append((k1, z1, k2, z2, k4, z4, d + 1))
                queue.append((k1, z1, k3, z3, k4, z4, d + 1))
                queue.append((k2, z2, k3, z3, k4, z4, d + 1))

        return list(circles.values())

    def render(self, resolution="Low", palette="Inferno", speed=1.0, **kwargs):
        depth         = int(kwargs.get("depth",         4))
        min_r         = float(kwargs.get("min_radius",  0.005))
        show_boundary = bool(kwargs.get("show_boundary", True))

        cmap        = ColorUtils.make_colormap(palette)
        all_circles = self._apollonius_circles(depth, min_r)

        inner = [(k, z, d) for k, z, d in all_circles if k > 0]
        inner.sort(key=lambda c: c[0])              # largest radius first for correct layering
        max_d = max((d for _, _, d in inner), default=1)

        fig, ax = self._create_figure(figsize=(8, 8), dpi=100)

        if show_boundary:
            ax.add_patch(plt.Circle((0, 0), 1.0, fill=False,
                                    edgecolor="#888888", linewidth=1.5, zorder=1))

        for k, z, d in inner:
            r  = 1.0 / k
            t  = d / max(max_d, 1)
            c  = cmap(t)
            lw = max(0.05, 0.4 - d * 0.05)
            ax.add_patch(plt.Circle(
                (z.real, z.imag), r,
                facecolor=(*c[:3], 0.80),
                edgecolor=c[:3],
                linewidth=lw,
                zorder=2 + d,
            ))

        ax.set_xlim(-1.08, 1.08)
        ax.set_ylim(-1.08, 1.08)
        ax.set_aspect("equal")
        ax.set_title(
            f"Apollonius Gasket — depth {depth}  ({len(inner)} circles)",
            color="#e0e0e0", fontsize=14, fontweight="bold", pad=12,
        )
        ax.axis("off")
        plt.tight_layout()
        plt.show()
        plt.close(fig)


class LissajousRenderer(BasePattern):
    """Pattern 12 — Lissajous Figures via parametric sine curves."""
    name = "Lissajous Figures"
    group = "Geometric & Mathematical"

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=3, min=1, max=12, step=1,
                              description="Freq A:"),
            widgets.IntSlider(value=4, min=1, max=12, step=1,
                              description="Freq B:"),
            widgets.FloatSlider(value=90.0, min=0.0, max=360.0, step=5.0,
                                description="Phase Deg:", readout_format=".0f"),
            widgets.FloatSlider(value=1.5, min=0.2, max=3.0, step=0.1,
                                description="Line Width:", readout_format=".1f"),
            widgets.IntSlider(value=2000, min=500, max=5000, step=100,
                              description="Points:"),
        ]

    def render(self, resolution="Low", palette="Inferno", speed=1.0, **kwargs):
        from math import gcd
        from matplotlib.collections import LineCollection

        a     = int(kwargs.get("freq_a",    3))
        b     = int(kwargs.get("freq_b",    4))
        delta = np.radians(float(kwargs.get("phase_deg", 90.0)))
        lw    = float(kwargs.get("line_width", 1.5))
        n_pts = int(kwargs.get("points",    2000))

        # Full closed period: T = 2π / gcd(a, b)
        g = gcd(a, b)
        t = np.linspace(0, 2 * np.pi / g, n_pts, endpoint=False)
        x = np.sin(a * t + delta)
        y = np.sin(b * t)

        coords   = np.column_stack([x, y])
        segments = np.stack([coords[:-1], coords[1:]], axis=1)
        colors   = ColorUtils.gradient_array(palette, len(segments))

        fig, ax = self._create_figure(figsize=(8, 8), dpi=100)
        lc = LineCollection(segments, colors=colors, linewidths=lw,
                            capstyle="round", alpha=0.9)
        ax.add_collection(lc)

        ax.set_xlim(-1.15, 1.15)
        ax.set_ylim(-1.15, 1.15)
        ax.set_aspect("equal")
        ax.set_title(
            f"Lissajous Figure — a={a}, b={b}, δ={np.degrees(delta):.0f}°",
            color="#e0e0e0", fontsize=14, fontweight="bold", pad=12,
        )
        ax.axis("off")
        plt.tight_layout()
        plt.show()
        plt.close(fig)


class RoseCurvesRenderer(BasePattern):
    """Pattern 13 — Rose Curves: r = cos(p/q · θ) in polar coordinates."""
    name = "Rose Curves"
    group = "Geometric & Mathematical"

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=5, min=1, max=12, step=1,
                              description="Numerator:"),
            widgets.IntSlider(value=3, min=1, max=8, step=1,
                              description="Denominator:"),
            widgets.FloatSlider(value=1.5, min=0.2, max=3.0, step=0.1,
                                description="Line Width:", readout_format=".1f"),
            widgets.IntSlider(value=3000, min=500, max=8000, step=100,
                              description="Points:"),
        ]

    def render(self, resolution="Low", palette="Inferno", speed=1.0, **kwargs):
        from math import gcd
        from matplotlib.collections import LineCollection

        p     = int(kwargs.get("numerator",   5))
        q     = int(kwargs.get("denominator", 3))
        lw    = float(kwargs.get("line_width", 1.5))
        n_pts = int(kwargs.get("points",    3000))

        # Reduce to lowest terms
        g = gcd(p, q)
        p, q = p // g, q // g

        # θ ∈ [0, 2π·q] guarantees closure for any rational k = p/q
        theta = np.linspace(0, 2 * np.pi * q, n_pts, endpoint=True)
        r     = np.cos((p / q) * theta)
        x     = r * np.cos(theta)
        y     = r * np.sin(theta)

        coords   = np.column_stack([x, y])
        segments = np.stack([coords[:-1], coords[1:]], axis=1)
        colors   = ColorUtils.gradient_array(palette, len(segments))

        fig, ax = self._create_figure(figsize=(8, 8), dpi=100)
        lc = LineCollection(segments, colors=colors, linewidths=lw,
                            capstyle="round", alpha=0.9)
        ax.add_collection(lc)

        ax.set_xlim(-1.1, 1.1)
        ax.set_ylim(-1.1, 1.1)
        ax.set_aspect("equal")
        ax.set_title(
            f"Rose Curve — r = cos({p}/{q} · θ)",
            color="#e0e0e0", fontsize=14, fontweight="bold", pad=12,
        )
        ax.axis("off")
        plt.tight_layout()
        plt.show()
        plt.close(fig)


class LorenzAttractorRenderer(BasePattern):
    """Pattern 14 — Lorenz Attractor via RK4 numerical integration."""
    name = "Chaos Attractor (Lorenz)"
    group = "Geometric & Mathematical"

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.FloatSlider(value=10.0, min=5.0, max=20.0, step=0.5,
                                description="Sigma:", readout_format=".1f"),
            widgets.FloatSlider(value=28.0, min=10.0, max=50.0, step=0.5,
                                description="Rho:", readout_format=".1f"),
            widgets.FloatSlider(value=2.667, min=1.0, max=5.0, step=0.05,
                                description="Beta:", readout_format=".3f"),
            widgets.IntSlider(value=20000, min=5000, max=50000, step=1000,
                              description="Steps:"),
        ]

    def render(self, resolution="Low", palette="Inferno", speed=1.0, **kwargs):
        from matplotlib.collections import LineCollection

        sigma = float(kwargs.get("sigma",  10.0))
        rho   = float(kwargs.get("rho",    28.0))
        beta  = float(kwargs.get("beta",   2.667))
        steps = int(kwargs.get("steps",    20000))
        dt    = 0.01

        # RK4 integration — use Python floats in the hot loop for speed
        traj_x = np.empty(steps)
        traj_y = np.empty(steps)
        traj_z = np.empty(steps)
        x, y, z = 0.1, 0.0, 0.0
        traj_x[0] = x
        traj_y[0] = y
        traj_z[0] = z

        for i in range(1, steps):
            # k1
            dx1 = sigma * (y - x)
            dy1 = x * (rho - z) - y
            dz1 = x * y - beta * z
            # k2
            x2 = x + 0.5 * dt * dx1
            y2 = y + 0.5 * dt * dy1
            z2 = z + 0.5 * dt * dz1
            dx2 = sigma * (y2 - x2)
            dy2 = x2 * (rho - z2) - y2
            dz2 = x2 * y2 - beta * z2
            # k3
            x3 = x + 0.5 * dt * dx2
            y3 = y + 0.5 * dt * dy2
            z3 = z + 0.5 * dt * dz2
            dx3 = sigma * (y3 - x3)
            dy3 = x3 * (rho - z3) - y3
            dz3 = x3 * y3 - beta * z3
            # k4
            x4 = x + dt * dx3
            y4 = y + dt * dy3
            z4 = z + dt * dz3
            dx4 = sigma * (y4 - x4)
            dy4 = x4 * (rho - z4) - y4
            dz4 = x4 * y4 - beta * z4
            # combine
            x += dt / 6 * (dx1 + 2 * dx2 + 2 * dx3 + dx4)
            y += dt / 6 * (dy1 + 2 * dy2 + 2 * dy3 + dy4)
            z += dt / 6 * (dz1 + 2 * dz2 + 2 * dz3 + dz4)
            traj_x[i] = x
            traj_y[i] = y
            traj_z[i] = z

        # Drop transient; plot on the classic x–z butterfly plane
        skip = min(500, steps // 10)
        xs, zs  = traj_x[skip:], traj_z[skip:]
        coords  = np.column_stack([xs, zs])
        segments = np.stack([coords[:-1], coords[1:]], axis=1)
        colors   = ColorUtils.gradient_array(palette, len(segments))

        fig, ax = self._create_figure(figsize=(8, 8), dpi=100)
        lc = LineCollection(segments, colors=colors, linewidths=0.5, alpha=0.85)
        ax.add_collection(lc)

        pad_x = (xs.max() - xs.min()) * 0.05
        pad_z = (zs.max() - zs.min()) * 0.05
        ax.set_xlim(xs.min() - pad_x, xs.max() + pad_x)
        ax.set_ylim(zs.min() - pad_z, zs.max() + pad_z)
        ax.set_title(
            f"Lorenz Attractor — σ={sigma:.1f}  ρ={rho:.1f}  β={beta:.3f}",
            color="#e0e0e0", fontsize=14, fontweight="bold", pad=12,
        )
        ax.axis("off")
        plt.tight_layout()
        plt.show()
        plt.close(fig)


class WaveInterferenceRenderer(BasePattern):
    """Pattern 15 — Wave Interference from multiple coherent point sources."""
    name = "Wave Interference Pattern"
    group = "Geometric & Mathematical"

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=3, min=2, max=8, step=1,
                              description="N Sources:"),
            widgets.FloatSlider(value=15.0, min=5.0, max=40.0, step=1.0,
                                description="Wavelength:", readout_format=".0f"),
            widgets.IntSlider(value=42, min=0, max=999,
                              description="Seed:"),
        ]

    def render(self, resolution="Low", palette="Inferno", speed=1.0, **kwargs):
        res        = self._resolve_resolution(resolution)
        n_src      = int(kwargs.get("n_sources",   3))
        wavelength = float(kwargs.get("wavelength", 15.0))
        seed       = int(kwargs.get("seed",         42))

        rng = np.random.default_rng(seed)

        # Source positions in a coordinate system spanning ±100 units
        angles = rng.uniform(0, 2 * np.pi, n_src)
        radii  = np.sqrt(rng.uniform(0.04, 0.49, n_src)) * 100
        src_x  = radii * np.cos(angles)
        src_y  = radii * np.sin(angles)

        # Rasterise: grid from −100 to +100 matches source units
        lin    = np.linspace(-100.0, 100.0, res)
        X, Y   = np.meshgrid(lin, lin)
        k_wave = 2.0 * np.pi / wavelength

        A = np.zeros((res, res))
        for i in range(n_src):
            d  = np.hypot(X - src_x[i], Y - src_y[i])
            d  = np.maximum(d, 0.5)          # avoid singularity at source location
            A += np.cos(k_wave * d)

        # Normalise to [−1, 1]
        a_max = np.abs(A).max()
        if a_max > 0:
            A /= a_max

        cmap = ColorUtils.make_colormap(palette)
        fig, ax = self._create_figure(figsize=(8, 8), dpi=100)
        ax.imshow(A, cmap=cmap, origin="lower", extent=[-100, 100, -100, 100],
                  vmin=-1.0, vmax=1.0, interpolation="bilinear")

        # Mark source locations
        for i in range(n_src):
            ax.plot(src_x[i], src_y[i], "+", color="white",
                    markersize=10, markeredgewidth=2, zorder=5, alpha=0.9)

        ax.set_xlim(-100, 100)
        ax.set_ylim(-100, 100)
        ax.set_aspect("equal")
        ax.set_title(
            f"Wave Interference — {n_src} sources, λ = {wavelength:.0f}",
            color="#e0e0e0", fontsize=14, fontweight="bold", pad=12,
        )
        ax.axis("off")
        plt.tight_layout()
        plt.show()
        plt.close(fig)

class HypocycloidRenderer(_StubMixin, BasePattern):
    name = "Hypocycloid & Epicycloid"
    group = "Geometric & Mathematical"

class TruchetRenderer(_StubMixin, BasePattern):
    name = "Truchet Tiles"
    group = "Geometric & Mathematical"

class HexGridRenderer(_StubMixin, BasePattern):
    name = "Hexagonal Grid Art"
    group = "Geometric & Mathematical"

class SpirographRenderer(_StubMixin, BasePattern):
    name = "Spirograph Generator"
    group = "Geometric & Mathematical"

class ParametricCurveRenderer(_StubMixin, BasePattern):
    name = "Parametric Curve Art"
    group = "Geometric & Mathematical"
