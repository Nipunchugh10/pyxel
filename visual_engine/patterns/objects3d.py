"""
3D Objects & Sculptures (71–90)
Each class is a stub that will be replaced with full implementations during Phase 1.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from engines.renderer import BasePattern


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

class DNAHelixRenderer(BasePattern):
    """71 — Rotating DNA Helix"""
    name  = "Rotating DNA Helix"
    group = "3D Objects & Sculptures"

    def render(self, resolution="Low", palette="Inferno", speed=1.0,
               n_turns=4, n_points=600, view_elev=20, view_azim=30,
               show_rungs=True, **kwargs):
        from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
        import matplotlib.colors as mcolors

        _RES_SCALE = {"Low": 0.6, "Medium": 1.0, "High": 1.4}
        scale = _RES_SCALE.get(resolution, 1.0)

        PALETTES = {
            "Inferno":       ["#200060", "#8b0aff", "#ff6b35", "#ffe04b"],
            "Ocean Depths":  ["#0a1628", "#0066cc", "#00ccff", "#80ffee"],
            "Neon Cyberpunk":["#0d0221", "#ff006e", "#00f5d4", "#f9c80e"],
            "Forest":        ["#1a2e1a", "#2d6a2d", "#52b252", "#b8f0b8"],
            "Sunset Blaze":  ["#1a0505", "#cc2200", "#ff8800", "#ffee44"],
            "Arctic Aurora": ["#050a14", "#0033aa", "#00ddaa", "#aaffee"],
            "Monochrome":    ["#111111", "#444444", "#aaaaaa", "#ffffff"],
            "Lava Flow":     ["#1a0000", "#aa1100", "#ff4400", "#ffcc00"],
        }
        cols = PALETTES.get(palette, PALETTES["Inferno"])

        N = int(n_points * scale)
        t = np.linspace(0, n_turns * 2 * np.pi, N)

        # Two backbone strands
        r = 1.0
        x1 =  r * np.cos(t);  y1 =  r * np.sin(t);  z1 = t / (2 * np.pi)
        x2 =  r * np.cos(t + np.pi); y2 = r * np.sin(t + np.pi); z2 = z1

        fig = plt.figure(figsize=(7, 7), facecolor="#030308")
        ax  = fig.add_subplot(111, projection="3d")
        ax.set_facecolor("#030308")
        for pane in (ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane):
            pane.fill = False
            pane.set_edgecolor("none")
        ax.grid(False)
        ax.set_axis_off()

        heights = (z1 - z1.min()) / (z1.max() - z1.min() + 1e-9)

        # Gradient colouring via segments
        from matplotlib.colors import LinearSegmentedColormap
        cmap = LinearSegmentedColormap.from_list("dna", [cols[0], cols[2], cols[3]], N=256)

        ax.scatter(x1, y1, z1, c=cmap(heights), s=8 * scale, depthshade=True, zorder=2)
        ax.scatter(x2, y2, z2, c=cmap(1 - heights), s=8 * scale, depthshade=True, zorder=2)

        # Base-pair rungs
        if show_rungs:
            n_rungs = int(n_turns * 10)
            rung_idx = np.linspace(0, N - 1, n_rungs, dtype=int)
            rung_cols = ["#ff4466", "#44aaff", "#44ff88", "#ffcc00"]
            for k, ri in enumerate(rung_idx):
                rc = rung_cols[k % 4]
                ax.plot([x1[ri], x2[ri]], [y1[ri], y2[ri]], [z1[ri], z2[ri]],
                        color=rc, linewidth=1.2 * scale, alpha=0.7, zorder=1)

        ax.view_init(elev=view_elev, azim=view_azim)
        plt.tight_layout()
        self._fig = fig
        plt.show()
        plt.close(fig)

    def get_controls(self):
        import ipywidgets as w
        return [
            w.IntSlider(value=4, min=2, max=8, step=1,   description="n_turns"),
            w.IntSlider(value=30, min=0, max=180, step=5, description="view_azim"),
            w.Checkbox(value=True,                         description="show_rungs"),
        ]

class KleinBottleRenderer(BasePattern):
    """72 — Klein Bottle Surface"""
    name  = "Klein Bottle Surface"
    group = "3D Objects & Sculptures"

    def render(self, resolution="Low", palette="Neon Cyberpunk", speed=1.0,
               n_u=80, n_v=80, alpha=0.75, view_elev=25, view_azim=45, **kwargs):
        from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
        from matplotlib.colors import LinearSegmentedColormap

        _RES = {"Low": 60, "Medium": 90, "High": 130}
        n_u = _RES.get(resolution, n_u)
        n_v = n_u

        PALETTES = {
            "Inferno":       ["#200060", "#8b0aff", "#ff6b35", "#ffe04b"],
            "Ocean Depths":  ["#0a1628", "#0066cc", "#00ccff", "#80ffee"],
            "Neon Cyberpunk":["#0d0221", "#ff006e", "#00f5d4", "#f9c80e"],
            "Forest":        ["#1a2e1a", "#2d6a2d", "#52b252", "#b8f0b8"],
            "Sunset Blaze":  ["#1a0505", "#cc2200", "#ff8800", "#ffee44"],
            "Arctic Aurora": ["#050a14", "#0033aa", "#00ddaa", "#aaffee"],
            "Monochrome":    ["#111111", "#444444", "#aaaaaa", "#ffffff"],
            "Lava Flow":     ["#1a0000", "#aa1100", "#ff4400", "#ffcc00"],
        }
        cols = PALETTES.get(palette, PALETTES["Neon Cyberpunk"])
        cmap = LinearSegmentedColormap.from_list("kb", cols, N=256)

        u = np.linspace(0, 2 * np.pi, n_u)
        v = np.linspace(0, 2 * np.pi, n_v)
        U, V = np.meshgrid(u, v)

        # Standard immersion of the Klein bottle in R^3
        # (figure-8 immersion — self-intersects along a circle)
        half = U / 2
        X = (2 + np.cos(half) * np.sin(V) - np.sin(half) * np.sin(2 * V)) * np.cos(U)
        Y = (2 + np.cos(half) * np.sin(V) - np.sin(half) * np.sin(2 * V)) * np.sin(U)
        Z =  np.sin(half) * np.sin(V) + np.cos(half) * np.sin(2 * V)

        # Colour by Z height
        Zn = (Z - Z.min()) / (Z.max() - Z.min() + 1e-9)

        fig = plt.figure(figsize=(7, 7), facecolor="#030308")
        ax  = fig.add_subplot(111, projection="3d")
        ax.set_facecolor("#030308")
        for pane in (ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane):
            pane.fill = False
            pane.set_edgecolor("none")
        ax.grid(False)
        ax.set_axis_off()

        ax.plot_surface(X, Y, Z, facecolors=cmap(Zn), alpha=alpha,
                        linewidth=0, antialiased=True, shade=True)

        ax.view_init(elev=view_elev, azim=view_azim)
        plt.tight_layout()
        self._fig = fig
        plt.show()
        plt.close(fig)

    def get_controls(self):
        import ipywidgets as w
        return [
            w.FloatSlider(value=0.75, min=0.2, max=1.0, step=0.05, description="alpha"),
            w.IntSlider(value=25, min=-90, max=90,  step=5, description="view_elev"),
            w.IntSlider(value=45, min=0,   max=360, step=5, description="view_azim"),
        ]

class MobiusStripRenderer(BasePattern):
    """73 — Möbius Strip"""
    name  = "Mobius Strip"
    group = "3D Objects & Sculptures"

    def render(self, resolution="Low", palette="Sunset Blaze", speed=1.0,
               width=0.6, twist=1, alpha=0.9, view_elev=30, view_azim=60, **kwargs):
        from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
        from matplotlib.colors import LinearSegmentedColormap

        _RES = {"Low": 80, "Medium": 160, "High": 320}
        n_u = _RES.get(resolution, 80)
        n_v = 20

        PALETTES = {
            "Inferno":       ["#200060", "#8b0aff", "#ff6b35", "#ffe04b"],
            "Ocean Depths":  ["#0a1628", "#0066cc", "#00ccff", "#80ffee"],
            "Neon Cyberpunk":["#0d0221", "#ff006e", "#00f5d4", "#f9c80e"],
            "Forest":        ["#1a2e1a", "#2d6a2d", "#52b252", "#b8f0b8"],
            "Sunset Blaze":  ["#1a0505", "#cc2200", "#ff8800", "#ffee44"],
            "Arctic Aurora": ["#050a14", "#0033aa", "#00ddaa", "#aaffee"],
            "Monochrome":    ["#111111", "#444444", "#aaaaaa", "#ffffff"],
            "Lava Flow":     ["#1a0000", "#aa1100", "#ff4400", "#ffcc00"],
        }
        cols = PALETTES.get(palette, PALETTES["Sunset Blaze"])
        cmap = LinearSegmentedColormap.from_list("mob", cols, N=256)

        u = np.linspace(0, 2 * np.pi, n_u)
        v = np.linspace(-width, width, n_v)
        U, V = np.meshgrid(u, v)

        # Möbius strip parametric equations (twist half-turns)
        phi = twist * U / 2
        X = (1 + V * np.cos(phi)) * np.cos(U)
        Y = (1 + V * np.cos(phi)) * np.sin(U)
        Z = V * np.sin(phi)

        # Colour by azimuthal angle u
        Un = U / (2 * np.pi)

        fig = plt.figure(figsize=(7, 7), facecolor="#030308")
        ax  = fig.add_subplot(111, projection="3d")
        ax.set_facecolor("#030308")
        for pane in (ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane):
            pane.fill = False
            pane.set_edgecolor("none")
        ax.grid(False)
        ax.set_axis_off()

        ax.plot_surface(X, Y, Z, facecolors=cmap(Un), alpha=alpha,
                        linewidth=0, antialiased=True, shade=True)

        ax.view_init(elev=view_elev, azim=view_azim)
        plt.tight_layout()
        self._fig = fig
        plt.show()
        plt.close(fig)

    def get_controls(self):
        import ipywidgets as w
        return [
            w.IntSlider(value=1, min=1, max=5, step=1,        description="twist"),
            w.FloatSlider(value=0.6, min=0.1, max=1.0, step=0.1, description="width"),
            w.FloatSlider(value=0.9, min=0.2, max=1.0, step=0.05, description="alpha"),
            w.IntSlider(value=60, min=0, max=360, step=5,      description="view_azim"),
        ]

class TorusKnotRenderer(BasePattern):
    """74 — Torus Knot"""
    name  = "Torus Knot"
    group = "3D Objects & Sculptures"

    def render(self, resolution="Low", palette="Arctic Aurora", speed=1.0,
               p=3, q=2, R=2.0, r=0.5, tube_pts=12, view_elev=30, view_azim=45, **kwargs):
        from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
        from matplotlib.colors import LinearSegmentedColormap
        from mpl_toolkits.mplot3d.art3d import Line3DCollection

        _RES = {"Low": 600, "Medium": 1200, "High": 2400}
        N = _RES.get(resolution, 600)

        PALETTES = {
            "Inferno":       ["#200060", "#8b0aff", "#ff6b35", "#ffe04b"],
            "Ocean Depths":  ["#0a1628", "#0066cc", "#00ccff", "#80ffee"],
            "Neon Cyberpunk":["#0d0221", "#ff006e", "#00f5d4", "#f9c80e"],
            "Forest":        ["#1a2e1a", "#2d6a2d", "#52b252", "#b8f0b8"],
            "Sunset Blaze":  ["#1a0505", "#cc2200", "#ff8800", "#ffee44"],
            "Arctic Aurora": ["#050a14", "#0033aa", "#00ddaa", "#aaffee"],
            "Monochrome":    ["#111111", "#444444", "#aaaaaa", "#ffffff"],
            "Lava Flow":     ["#1a0000", "#aa1100", "#ff4400", "#ffcc00"],
        }
        cols = PALETTES.get(palette, PALETTES["Arctic Aurora"])
        cmap = LinearSegmentedColormap.from_list("tk", cols, N=256)

        t = np.linspace(0, 2 * np.pi, N)
        # Torus knot T(p,q)
        ct = np.cos(q * t);  st = np.sin(q * t)
        X = (R + r * ct) * np.cos(p * t)
        Y = (R + r * ct) * np.sin(p * t)
        Z = r * st

        fig = plt.figure(figsize=(7, 7), facecolor="#030308")
        ax  = fig.add_subplot(111, projection="3d")
        ax.set_facecolor("#030308")
        for pane in (ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane):
            pane.fill = False
            pane.set_edgecolor("none")
        ax.grid(False)
        ax.set_axis_off()

        # Draw as colour-gradient line using Line3DCollection segments
        pts   = np.array([X, Y, Z]).T
        segs  = np.stack([pts[:-1], pts[1:]], axis=1)
        colors = cmap(np.linspace(0, 1, len(segs)))
        lc = Line3DCollection(segs, colors=colors, linewidth=1.8, alpha=0.9)
        ax.add_collection(lc)
        ax.auto_scale_xyz(X, Y, Z)

        ax.view_init(elev=view_elev, azim=view_azim)
        plt.tight_layout()
        self._fig = fig
        plt.show()
        plt.close(fig)

    def get_controls(self):
        import ipywidgets as w
        return [
            w.IntSlider(value=3, min=2, max=7, step=1, description="p"),
            w.IntSlider(value=2, min=1, max=6, step=1, description="q"),
            w.IntSlider(value=30, min=0, max=90,  step=5, description="view_elev"),
            w.IntSlider(value=45, min=0, max=360, step=5, description="view_azim"),
        ]

class GyroidRenderer(BasePattern):
    """75 — Gyroid Surface"""
    name  = "Gyroid Surface"
    group = "3D Objects & Sculptures"

    def render(self, resolution="Low", palette="Ocean Depths", speed=1.0,
               threshold=0.10, n_grid=40, point_size=4, view_elev=25, view_azim=40, **kwargs):
        from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
        from matplotlib.colors import LinearSegmentedColormap

        _RES = {"Low": 30, "Medium": 45, "High": 60}
        n_grid = _RES.get(resolution, n_grid)

        PALETTES = {
            "Inferno":       ["#200060", "#8b0aff", "#ff6b35", "#ffe04b"],
            "Ocean Depths":  ["#0a1628", "#0066cc", "#00ccff", "#80ffee"],
            "Neon Cyberpunk":["#0d0221", "#ff006e", "#00f5d4", "#f9c80e"],
            "Forest":        ["#1a2e1a", "#2d6a2d", "#52b252", "#b8f0b8"],
            "Sunset Blaze":  ["#1a0505", "#cc2200", "#ff8800", "#ffee44"],
            "Arctic Aurora": ["#050a14", "#0033aa", "#00ddaa", "#aaffee"],
            "Monochrome":    ["#111111", "#444444", "#aaaaaa", "#ffffff"],
            "Lava Flow":     ["#1a0000", "#aa1100", "#ff4400", "#ffcc00"],
        }
        cols = PALETTES.get(palette, PALETTES["Ocean Depths"])
        cmap = LinearSegmentedColormap.from_list("gy", cols, N=256)

        lin = np.linspace(-2 * np.pi, 2 * np.pi, n_grid)
        gx, gy, gz = np.meshgrid(lin, lin, lin)

        # Gyroid implicit surface: cos(x)sin(y) + cos(y)sin(z) + cos(z)sin(x) = 0
        F = (np.cos(gx) * np.sin(gy) +
             np.cos(gy) * np.sin(gz) +
             np.cos(gz) * np.sin(gx))

        mask = np.abs(F) < threshold
        xs, ys, zs = gx[mask], gy[mask], gz[mask]

        heights = (zs - zs.min()) / (zs.max() - zs.min() + 1e-9)

        fig = plt.figure(figsize=(7, 7), facecolor="#030308")
        ax  = fig.add_subplot(111, projection="3d")
        ax.set_facecolor("#030308")
        for pane in (ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane):
            pane.fill = False
            pane.set_edgecolor("none")
        ax.grid(False)
        ax.set_axis_off()

        ax.scatter(xs, ys, zs, c=cmap(heights), s=point_size,
                   alpha=0.6, depthshade=True)

        ax.view_init(elev=view_elev, azim=view_azim)
        plt.tight_layout()
        self._fig = fig
        plt.show()
        plt.close(fig)

    def get_controls(self):
        import ipywidgets as w
        return [
            w.FloatSlider(value=0.10, min=0.02, max=0.3, step=0.01, description="threshold"),
            w.IntSlider(value=4, min=1, max=12, step=1,              description="point_size"),
            w.IntSlider(value=25,  min=-90, max=90,  step=5, description="view_elev"),
            w.IntSlider(value=40,  min=0,   max=360, step=5, description="view_azim"),
        ]

class RomanescoRenderer(BasePattern):
    """76 — Romanesco Broccoli"""
    name  = "Romanesco Broccoli"
    group = "3D Objects & Sculptures"

    def render(self, resolution="Low", palette="Forest", speed=1.0,
               n_buds=500, n_levels=6, view_elev=55, view_azim=30, **kwargs):
        from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
        from matplotlib.colors import LinearSegmentedColormap

        _RES = {"Low": 400, "Medium": 800, "High": 1600}
        n_buds = _RES.get(resolution, n_buds)

        PALETTES = {
            "Inferno":       ["#200060", "#8b0aff", "#ff6b35", "#ffe04b"],
            "Ocean Depths":  ["#0a1628", "#0066cc", "#00ccff", "#80ffee"],
            "Neon Cyberpunk":["#0d0221", "#ff006e", "#00f5d4", "#f9c80e"],
            "Forest":        ["#1a2e1a", "#2d6a2d", "#52b252", "#b8f0b8"],
            "Sunset Blaze":  ["#1a0505", "#cc2200", "#ff8800", "#ffee44"],
            "Arctic Aurora": ["#050a14", "#0033aa", "#00ddaa", "#aaffee"],
            "Monochrome":    ["#111111", "#444444", "#aaaaaa", "#ffffff"],
            "Lava Flow":     ["#1a0000", "#aa1100", "#ff4400", "#ffcc00"],
        }
        cols = PALETTES.get(palette, PALETTES["Forest"])
        cmap = LinearSegmentedColormap.from_list("rom", cols, N=256)

        PHI_G = 2.39996323  # golden angle in radians
        xs, ys, zs, cs = [], [], [], []

        for i in range(n_buds):
            frac  = i / n_buds
            angle = i * PHI_G
            level = int(frac * n_levels)
            rho   = 0.8 * np.sqrt(frac)            # radial distance expands outward
            height = frac * 1.5                     # buds spiral upward
            scale  = (1 - frac) * 0.25 + 0.02      # buds shrink toward top

            # Conical spiral
            cx = rho * np.cos(angle)
            cy = rho * np.sin(angle)
            cz = height

            # Add a small cluster of sub-buds around each main bud
            n_sub = max(1, int(8 * scale / 0.25))
            for j in range(n_sub):
                sub_a = j * PHI_G
                sub_r = scale * np.sqrt(j / max(n_sub, 1))
                sx = cx + sub_r * np.cos(sub_a)
                sy = cy + sub_r * np.sin(sub_a)
                sz = cz + sub_r * 0.5
                xs.append(sx); ys.append(sy); zs.append(sz)
                cs.append(level / n_levels)

        xs = np.array(xs); ys = np.array(ys)
        zs = np.array(zs); cs = np.array(cs)

        fig = plt.figure(figsize=(7, 7), facecolor="#030308")
        ax  = fig.add_subplot(111, projection="3d")
        ax.set_facecolor("#030308")
        for pane in (ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane):
            pane.fill = False
            pane.set_edgecolor("none")
        ax.grid(False)
        ax.set_axis_off()

        sizes = 20 * (1 - cs) + 2
        ax.scatter(xs, ys, zs, c=cmap(cs), s=sizes, alpha=0.85, depthshade=True)

        ax.view_init(elev=view_elev, azim=view_azim)
        plt.tight_layout()
        self._fig = fig
        plt.show()
        plt.close(fig)

    def get_controls(self):
        import ipywidgets as w
        return [
            w.IntSlider(value=6, min=3, max=10, step=1,        description="n_levels"),
            w.IntSlider(value=55, min=10, max=90, step=5,       description="view_elev"),
            w.IntSlider(value=30, min=0, max=360, step=5,       description="view_azim"),
        ]

class IcosphereRenderer(BasePattern):
    """77 — Icosphere Subdivisions"""
    name  = "Icosphere Subdivisions"
    group = "3D Objects & Sculptures"

    def render(self, resolution="Low", palette="Ocean Depths", speed=1.0,
               subdivisions=2, alpha=0.75, view_elev=20, view_azim=30, **kwargs):
        from mpl_toolkits.mplot3d import Axes3D          # noqa: F401
        from mpl_toolkits.mplot3d.art3d import Poly3DCollection
        from matplotlib.colors import LinearSegmentedColormap

        _RES = {"Low": 2, "Medium": 3, "High": 4}
        subdivisions = _RES.get(resolution, subdivisions)

        PALETTES = {
            "Inferno":       ["#200060", "#8b0aff", "#ff6b35", "#ffe04b"],
            "Ocean Depths":  ["#0a1628", "#0066cc", "#00ccff", "#80ffee"],
            "Neon Cyberpunk":["#0d0221", "#ff006e", "#00f5d4", "#f9c80e"],
            "Forest":        ["#1a2e1a", "#2d6a2d", "#52b252", "#b8f0b8"],
            "Sunset Blaze":  ["#1a0505", "#cc2200", "#ff8800", "#ffee44"],
            "Arctic Aurora": ["#050a14", "#0033aa", "#00ddaa", "#aaffee"],
            "Monochrome":    ["#111111", "#444444", "#aaaaaa", "#ffffff"],
            "Lava Flow":     ["#1a0000", "#aa1100", "#ff4400", "#ffcc00"],
        }
        cols = PALETTES.get(palette, PALETTES["Ocean Depths"])
        cmap = LinearSegmentedColormap.from_list("ico", cols, N=256)

        # ── Base icosahedron ──────────────────────────────────────────
        phi = (1.0 + np.sqrt(5.0)) / 2.0
        raw = np.array([
            [-1,  phi, 0], [ 1,  phi, 0], [-1, -phi, 0], [ 1, -phi, 0],
            [ 0, -1,  phi], [ 0,  1,  phi], [ 0, -1, -phi], [ 0,  1, -phi],
            [ phi, 0, -1], [ phi, 0,  1], [-phi, 0, -1], [-phi, 0,  1],
        ], dtype=float)
        raw /= np.linalg.norm(raw[0])
        verts = [row.tolist() for row in raw]

        faces = [
            [0,11,5],[0,5,1],[0,1,7],[0,7,10],[0,10,11],
            [1,5,9],[5,11,4],[11,10,2],[10,7,6],[7,1,8],
            [3,9,4],[3,4,2],[3,2,6],[3,6,8],[3,8,9],
            [4,9,5],[2,4,11],[6,2,10],[8,6,7],[9,8,1],
        ]

        def subdivide(vl, fl):
            cache = {}
            nf = []
            def mid(i, j):
                key = (min(i, j), max(i, j))
                if key not in cache:
                    m = (np.array(vl[i]) + np.array(vl[j])) * 0.5
                    m /= np.linalg.norm(m)
                    cache[key] = len(vl)
                    vl.append(m.tolist())
                return cache[key]
            for a, b, c in fl:
                ab = mid(a, b); bc = mid(b, c); ca = mid(c, a)
                nf += [[a, ab, ca], [b, bc, ab], [c, ca, bc], [ab, bc, ca]]
            return nf

        for _ in range(subdivisions):
            faces = subdivide(verts, faces)

        V  = np.array(verts)
        fa = np.array(faces)
        tri = V[fa]                                        # (F, 3, 3)
        zc  = tri[:, :, 2].mean(axis=1)                   # centroid Z
        zmin, zmax = zc.min(), zc.max()
        cn  = (zc - zmin) / (zmax - zmin + 1e-9)
        fc  = cmap(cn)                                     # (F, 4) RGBA

        fig = plt.figure(figsize=(7, 7), facecolor="#030308")
        ax  = fig.add_subplot(111, projection="3d")
        ax.set_facecolor("#030308")
        for pane in (ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane):
            pane.fill = False
            pane.set_edgecolor("none")
        ax.grid(False)
        ax.set_axis_off()

        poly = Poly3DCollection(tri, facecolors=fc,
                                edgecolors=(1, 1, 1, 0.08), linewidth=0.3,
                                alpha=alpha)
        ax.add_collection3d(poly)
        lim = 1.3
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_zlim(-lim, lim)
        ax.view_init(elev=view_elev, azim=view_azim)
        plt.tight_layout()
        self._fig = fig
        plt.show()
        plt.close(fig)

    def get_controls(self):
        import ipywidgets as w
        return [
            w.IntSlider(value=2, min=0, max=4, step=1,
                        description="subdivisions"),
            w.FloatSlider(value=0.75, min=0.2, max=1.0, step=0.05,
                          description="alpha"),
            w.IntSlider(value=20, min=-90, max=90,  step=5,
                        description="view_elev"),
            w.IntSlider(value=30, min=0,   max=360, step=5,
                        description="view_azim"),
        ]

class TrefoilKnotRenderer(BasePattern):
    """78 — Trefoil Knot"""
    name  = "Trefoil Knot"
    group = "3D Objects & Sculptures"

    def render(self, resolution="Low", palette="Neon Cyberpunk", speed=1.0,
               linewidth=2.5, view_elev=30, view_azim=45, **kwargs):
        from mpl_toolkits.mplot3d import Axes3D          # noqa: F401
        from mpl_toolkits.mplot3d.art3d import Line3DCollection
        from matplotlib.colors import LinearSegmentedColormap

        _RES = {"Low": 600, "Medium": 1200, "High": 2400}
        N = _RES.get(resolution, 600)

        PALETTES = {
            "Inferno":       ["#200060", "#8b0aff", "#ff6b35", "#ffe04b"],
            "Ocean Depths":  ["#0a1628", "#0066cc", "#00ccff", "#80ffee"],
            "Neon Cyberpunk":["#0d0221", "#ff006e", "#00f5d4", "#f9c80e"],
            "Forest":        ["#1a2e1a", "#2d6a2d", "#52b252", "#b8f0b8"],
            "Sunset Blaze":  ["#1a0505", "#cc2200", "#ff8800", "#ffee44"],
            "Arctic Aurora": ["#050a14", "#0033aa", "#00ddaa", "#aaffee"],
            "Monochrome":    ["#111111", "#444444", "#aaaaaa", "#ffffff"],
            "Lava Flow":     ["#1a0000", "#aa1100", "#ff4400", "#ffcc00"],
        }
        cols = PALETTES.get(palette, PALETTES["Neon Cyberpunk"])
        cmap = LinearSegmentedColormap.from_list("tf", cols, N=256)

        t = np.linspace(0, 2 * np.pi, N)
        # Standard trefoil knot parametrization
        X = np.sin(t) + 2 * np.sin(2 * t)
        Y = np.cos(t) - 2 * np.cos(2 * t)
        Z = -np.sin(3 * t)

        fig = plt.figure(figsize=(7, 7), facecolor="#030308")
        ax  = fig.add_subplot(111, projection="3d")
        ax.set_facecolor("#030308")
        for pane in (ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane):
            pane.fill = False
            pane.set_edgecolor("none")
        ax.grid(False)
        ax.set_axis_off()

        pts    = np.column_stack([X, Y, Z])
        segs   = np.stack([pts[:-1], pts[1:]], axis=1)
        colors = cmap(np.linspace(0, 1, len(segs)))
        lc = Line3DCollection(segs, colors=colors, linewidth=linewidth, alpha=0.95)
        ax.add_collection(lc)
        ax.auto_scale_xyz(X, Y, Z)

        ax.view_init(elev=view_elev, azim=view_azim)
        plt.tight_layout()
        self._fig = fig
        plt.show()
        plt.close(fig)

    def get_controls(self):
        import ipywidgets as w
        return [
            w.FloatSlider(value=2.5, min=0.5, max=6.0, step=0.5,
                          description="linewidth"),
            w.IntSlider(value=30, min=-90, max=90,  step=5,
                        description="view_elev"),
            w.IntSlider(value=45, min=0,   max=360, step=5,
                        description="view_azim"),
        ]

class SeashellRenderer(_StubMixin, BasePattern):
    name = "Seashell Surface"
    group = "3D Objects & Sculptures"

class HyperboloidRenderer(_StubMixin, BasePattern):
    name = "Hyperboloid of Revolution"
    group = "3D Objects & Sculptures"

class ParametricVaseRenderer(_StubMixin, BasePattern):
    name = "Parametric Vase"
    group = "3D Objects & Sculptures"

class CrystalLatticeRenderer(_StubMixin, BasePattern):
    name = "Crystal Lattice"
    group = "3D Objects & Sculptures"

class GeodesicDomeRenderer(_StubMixin, BasePattern):
    name = "Geodesic Dome"
    group = "3D Objects & Sculptures"

class CalabiYauRenderer(_StubMixin, BasePattern):
    name = "Calabi-Yau Manifold Slice"
    group = "3D Objects & Sculptures"

class SoapBubbleRenderer(_StubMixin, BasePattern):
    name = "Soap Bubble Cluster"
    group = "3D Objects & Sculptures"

class NeuralMeshRenderer(_StubMixin, BasePattern):
    name = "Neural Mesh Sculpture"
    group = "3D Objects & Sculptures"

class TwistedPrismRenderer(_StubMixin, BasePattern):
    name = "Twisted Prism Tower"
    group = "3D Objects & Sculptures"

class FractalMountainRenderer(_StubMixin, BasePattern):
    name = "Fractal Mountain"
    group = "3D Objects & Sculptures"

class VolumetricFogRenderer(_StubMixin, BasePattern):
    name = "Volumetric Fog Cube"
    group = "3D Objects & Sculptures"

class StrangeAttractor3DRenderer(_StubMixin, BasePattern):
    name = "Strange Attractor 3D"
    group = "3D Objects & Sculptures"
