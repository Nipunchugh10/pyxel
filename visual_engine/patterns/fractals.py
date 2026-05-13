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

class DragonCurveRenderer(_StubMixin, BasePattern):
    name = "Dragon Curve"
    group = "Geometric & Mathematical"

class HilbertCurveRenderer(_StubMixin, BasePattern):
    name = "Hilbert Curve"
    group = "Geometric & Mathematical"

class LSystemTreeRenderer(_StubMixin, BasePattern):
    name = "L-System Tree"
    group = "Geometric & Mathematical"

class ApolloniusRenderer(_StubMixin, BasePattern):
    name = "Apollonius Gasket"
    group = "Geometric & Mathematical"

class LissajousRenderer(_StubMixin, BasePattern):
    name = "Lissajous Figures"
    group = "Geometric & Mathematical"

class RoseCurvesRenderer(_StubMixin, BasePattern):
    name = "Rose Curves"
    group = "Geometric & Mathematical"

class LorenzAttractorRenderer(_StubMixin, BasePattern):
    name = "Chaos Attractor (Lorenz)"
    group = "Geometric & Mathematical"

class WaveInterferenceRenderer(_StubMixin, BasePattern):
    name = "Wave Interference Pattern"
    group = "Geometric & Mathematical"

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
