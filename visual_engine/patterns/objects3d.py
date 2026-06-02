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
        x1 = r * np.cos(t)
        y1 = r * np.sin(t)
        z1 = t / (2 * np.pi)
        x2 = r * np.cos(t + np.pi)
        y2 = r * np.sin(t + np.pi)
        z2 = z1

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
        ct = np.cos(q * t)
        st = np.sin(q * t)
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
                xs.append(sx)
                ys.append(sy)
                zs.append(sz)
                cs.append(level / n_levels)

        xs = np.array(xs)
        ys = np.array(ys)
        zs = np.array(zs)
        cs = np.array(cs)

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
                ab = mid(a, b)
                bc = mid(b, c)
                ca = mid(c, a)
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

class SeashellRenderer(BasePattern):
    """79 — Seashell Surface"""
    name  = "Seashell Surface"
    group = "3D Objects & Sculptures"

    def render(self, resolution="Low", palette="Sunset Blaze", speed=1.0,
               n_turns=3, growth_rate=0.18, tube_scale=0.3, alpha=0.85,
               view_elev=25, view_azim=60, **kwargs):
        from mpl_toolkits.mplot3d import Axes3D          # noqa: F401
        from matplotlib.colors import LinearSegmentedColormap

        _RES = {"Low": (80, 30), "Medium": (140, 50), "High": (220, 80)}
        n_u, n_v = _RES.get(resolution, (80, 30))

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
        cmap = LinearSegmentedColormap.from_list("sh", cols, N=256)

        # Helicospiral seashell with exponential growth
        # v = coiling angle, u = cross-section angle
        v = np.linspace(0, 2 * np.pi * n_turns, n_u)
        u = np.linspace(0, 2 * np.pi, n_v)
        V, U = np.meshgrid(v, u)

        R = np.exp(growth_rate * V)          # exponentially growing coil radius
        r = tube_scale * R                   # tube cross-section proportional to R

        X = (R + r * np.cos(U)) * np.cos(V)
        Y = (R + r * np.cos(U)) * np.sin(V)
        Z = r * np.sin(U) + 0.4 * V         # gentle upward rise

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
            w.IntSlider(value=3, min=1, max=6, step=1,
                        description="n_turns"),
            w.FloatSlider(value=0.18, min=0.05, max=0.4, step=0.01,
                          description="growth_rate"),
            w.FloatSlider(value=0.3, min=0.1, max=0.6, step=0.05,
                          description="tube_scale"),
            w.IntSlider(value=60, min=0, max=360, step=5,
                        description="view_azim"),
        ]

class HyperboloidRenderer(BasePattern):
    """80 — Hyperboloid of Revolution"""
    name  = "Hyperboloid of Revolution"
    group = "3D Objects & Sculptures"

    def render(self, resolution="Low", palette="Neon Cyberpunk", speed=1.0,
               a=1.0, c_scale=1.0, t_range=2.0, show_lines=True, alpha=0.65,
               view_elev=20, view_azim=45, **kwargs):
        from mpl_toolkits.mplot3d import Axes3D          # noqa: F401
        from matplotlib.colors import LinearSegmentedColormap

        _RES = {"Low": (60, 40), "Medium": (100, 60), "High": (160, 80)}
        n_u, n_t = _RES.get(resolution, (60, 40))

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
        cmap = LinearSegmentedColormap.from_list("hyp", cols, N=256)

        # One-sheeted hyperboloid: x²/a² + y²/a² − z²/c² = 1
        # Parametric: x = a·cosh(t)·cos(u), y = a·cosh(t)·sin(u), z = c·sinh(t)
        u = np.linspace(0, 2 * np.pi, n_u)
        t = np.linspace(-t_range, t_range, n_t)
        U, T = np.meshgrid(u, t)

        X = a * np.cosh(T) * np.cos(U)
        Y = a * np.cosh(T) * np.sin(U)
        Z = c_scale * np.sinh(T)

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

        # Ruling lines (straight lines lying on the surface)
        if show_lines:
            n_rules = 16
            theta_k = np.linspace(0, 2 * np.pi, n_rules, endpoint=False)
            s = np.linspace(-t_range * 1.5, t_range * 1.5, 60)
            for theta in theta_k:
                # Family-1 rulings: x=a(cosθ−s sinθ), y=a(sinθ+s cosθ), z=c·s
                rx = a * (np.cos(theta) - s * np.sin(theta))
                ry = a * (np.sin(theta) + s * np.cos(theta))
                rz = c_scale * s
                ax.plot(rx, ry, rz, color="white", alpha=0.25, linewidth=0.8)

        ax.view_init(elev=view_elev, azim=view_azim)
        plt.tight_layout()
        self._fig = fig
        plt.show()
        plt.close(fig)

    def get_controls(self):
        import ipywidgets as w
        return [
            w.FloatSlider(value=1.0, min=0.5, max=2.0, step=0.1,
                          description="a"),
            w.FloatSlider(value=1.0, min=0.3, max=2.0, step=0.1,
                          description="c_scale"),
            w.Checkbox(value=True,
                       description="show_lines"),
            w.FloatSlider(value=0.65, min=0.2, max=1.0, step=0.05,
                          description="alpha"),
            w.IntSlider(value=45, min=0, max=360, step=5,
                        description="view_azim"),
        ]

class ParametricVaseRenderer(BasePattern):
    """81 — Parametric Vase"""
    name  = "Parametric Vase"
    group = "3D Objects & Sculptures"

    def render(self, resolution="Low", palette="Lava Flow", speed=1.0,
               style=0, alpha=0.9, view_elev=20, view_azim=30, **kwargs):
        from mpl_toolkits.mplot3d import Axes3D          # noqa: F401
        from matplotlib.colors import LinearSegmentedColormap

        _RES = {"Low": (60, 80), "Medium": (100, 140), "High": (160, 220)}
        n_u, n_z = _RES.get(resolution, (60, 80))

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
        cols = PALETTES.get(palette, PALETTES["Lava Flow"])
        cmap = LinearSegmentedColormap.from_list("vase", cols, N=256)

        z = np.linspace(0, 1, n_z)
        style_int = int(style) % 4

        if style_int == 0:     # Classic amphora
            r = 0.15 + 0.55 * np.sin(np.pi * z) + 0.12 * np.sin(2 * np.pi * z)
            taper = np.where(z < 0.08, z / 0.08, np.ones_like(z))
            r = r * taper
        elif style_int == 1:   # Chinese vase: high Gaussian shoulders
            r = 0.4 * np.exp(-8 * (z - 0.65) ** 2) + 0.1 + 0.25 * z * (1 - z)
        elif style_int == 2:   # Modernist with ripples
            r = 0.3 + 0.1 * np.sin(6 * np.pi * z) + 0.2 * np.sin(np.pi * z)
            r = np.clip(r, 0.05, 1.0)
        else:                  # Bulging round vase
            r = 0.15 + 0.55 * np.sin(np.pi * z ** 0.7)
            taper2 = np.where(z < 0.05, z / 0.05, np.ones_like(z))
            r = r * taper2

        u = np.linspace(0, 2 * np.pi, n_u)
        Z2d, U2d = np.meshgrid(z, u)
        R2d = np.interp(Z2d, z, r)

        X = R2d * np.cos(U2d)
        Y = R2d * np.sin(U2d)
        Zn = (Z2d - Z2d.min()) / (Z2d.max() - Z2d.min() + 1e-9)

        fig = plt.figure(figsize=(7, 7), facecolor="#030308")
        ax  = fig.add_subplot(111, projection="3d")
        ax.set_facecolor("#030308")
        for pane in (ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane):
            pane.fill = False
            pane.set_edgecolor("none")
        ax.grid(False)
        ax.set_axis_off()

        ax.plot_surface(X, Y, Z2d, facecolors=cmap(Zn), alpha=alpha,
                        linewidth=0, antialiased=True, shade=True)

        ax.view_init(elev=view_elev, azim=view_azim)
        plt.tight_layout()
        self._fig = fig
        plt.show()
        plt.close(fig)

    def get_controls(self):
        import ipywidgets as w
        return [
            w.IntSlider(value=0, min=0, max=3, step=1,
                        description="style"),
            w.FloatSlider(value=0.9, min=0.3, max=1.0, step=0.05,
                          description="alpha"),
            w.IntSlider(value=20, min=-90, max=90,  step=5,
                        description="view_elev"),
            w.IntSlider(value=30, min=0,   max=360, step=5,
                        description="view_azim"),
        ]

class CrystalLatticeRenderer(BasePattern):
    """82 — Crystal Lattice"""
    name  = "Crystal Lattice"
    group = "3D Objects & Sculptures"

    def render(self, resolution="Low", palette="Arctic Aurora", speed=1.0,
               lattice_type=0, show_bonds=True,
               view_elev=25, view_azim=45, **kwargs):
        from mpl_toolkits.mplot3d import Axes3D          # noqa: F401
        from matplotlib.colors import LinearSegmentedColormap

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
        cmap = LinearSegmentedColormap.from_list("cl", cols, N=256)

        _RES = {"Low": 3, "Medium": 4, "High": 5}
        n = _RES.get(resolution, 3)

        lt = int(lattice_type) % 4
        r  = np.arange(n, dtype=float)

        # ── Lattice definitions (motif in fractional coords, Cartesian vectors) ──
        if lt == 0:    # Simple Cubic
            motif  = [(0., 0., 0.)]
            a1, a2, a3 = (1,0,0), (0,1,0), (0,0,1)
            bond_d, title = 1.05, "Simple Cubic"
        elif lt == 1:  # BCC
            motif  = [(0.,0.,0.), (0.5,0.5,0.5)]
            a1, a2, a3 = (1,0,0), (0,1,0), (0,0,1)
            bond_d, title = np.sqrt(3)/2 + 0.05, "Body-Centred Cubic"
        elif lt == 2:  # FCC
            motif  = [(0.,0.,0.), (0.5,0.5,0.), (0.5,0.,0.5), (0.,0.5,0.5)]
            a1, a2, a3 = (1,0,0), (0,1,0), (0,0,1)
            bond_d, title = np.sqrt(2)/2 + 0.05, "Face-Centred Cubic"
        else:          # Diamond cubic
            motif  = [(0.,0.,0.), (0.5,0.5,0.), (0.5,0.,0.5), (0.,0.5,0.5),
                      (0.25,0.25,0.25), (0.75,0.75,0.25),
                      (0.75,0.25,0.75), (0.25,0.75,0.75)]
            a1, a2, a3 = (1,0,0), (0,1,0), (0,0,1)
            bond_d, title = np.sqrt(3)/4 + 0.05, "Diamond Cubic"

        A = np.array([a1, a2, a3], dtype=float)   # rows are lattice vectors

        pts_list = []
        for i in r:
            for j in r:
                for k in r:
                    origin = i * A[0] + j * A[1] + k * A[2]
                    for fx, fy, fz in motif:
                        pos = origin + fx * A[0] + fy * A[1] + fz * A[2]
                        pts_list.append(pos)
        atoms = np.array(pts_list)
        atoms -= atoms.mean(axis=0)              # centre the lattice

        zmin = atoms[:, 2].min()
        zmax = atoms[:, 2].max()
        zn   = (atoms[:, 2] - zmin) / (zmax - zmin + 1e-9)
        colors = cmap(zn)

        fig = plt.figure(figsize=(7, 7), facecolor="#030308")
        ax  = fig.add_subplot(111, projection="3d")
        ax.set_facecolor("#030308")
        for pane in (ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane):
            pane.fill = False
            pane.set_edgecolor("none")
        ax.grid(False)
        ax.set_axis_off()

        # ── Bonds ─────────────────────────────────────────────────────
        if show_bonds:
            from scipy.spatial import cKDTree
            tree  = cKDTree(atoms)
            pairs = tree.query_pairs(bond_d)
            for i, j in pairs:
                p1, p2 = atoms[i], atoms[j]
                ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]],
                        color="white", alpha=0.25, linewidth=0.8)

        # ── Atoms ─────────────────────────────────────────────────────
        ax.scatter(atoms[:, 0], atoms[:, 1], atoms[:, 2],
                   c=colors, s=80, alpha=0.92, depthshade=True, zorder=3)

        ax.set_title(title, color="#cccccc", fontsize=10, pad=4)
        ax.view_init(elev=view_elev, azim=view_azim)
        plt.tight_layout()
        self._fig = fig
        plt.show()
        plt.close(fig)

    def get_controls(self):
        import ipywidgets as w
        return [
            w.IntSlider(value=0, min=0, max=3, step=1,
                        description="lattice_type"),
            w.Checkbox(value=True,
                       description="show_bonds"),
            w.IntSlider(value=25, min=-90, max=90,  step=5,
                        description="view_elev"),
            w.IntSlider(value=45, min=0,   max=360, step=5,
                        description="view_azim"),
        ]

class GeodesicDomeRenderer(BasePattern):
    """83 — Geodesic Dome"""
    name  = "Geodesic Dome"
    group = "3D Objects & Sculptures"

    def render(self, resolution="Low", palette="Ocean Depths", speed=1.0,
               frequency=2, show_base=True, alpha=0.55,
               view_elev=30, view_azim=45, **kwargs):
        from mpl_toolkits.mplot3d import Axes3D          # noqa: F401
        from mpl_toolkits.mplot3d.art3d import Poly3DCollection
        from matplotlib.colors import LinearSegmentedColormap

        _RES = {"Low": 2, "Medium": 3, "High": 4}
        frequency = _RES.get(resolution, frequency)

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
        cmap = LinearSegmentedColormap.from_list("gd", cols, N=256)

        # ── Build icosphere (same subdivision as pattern 77) ─────────
        phi = (1.0 + np.sqrt(5.0)) / 2.0
        raw = np.array([
            [-1,  phi, 0], [ 1,  phi, 0], [-1, -phi, 0], [ 1, -phi, 0],
            [ 0, -1,  phi], [ 0,  1,  phi], [ 0, -1, -phi], [ 0,  1, -phi],
            [ phi, 0, -1], [ phi, 0,  1], [-phi, 0, -1], [-phi, 0,  1],
        ], dtype=float)
        raw /= np.linalg.norm(raw[0])
        verts = [row.tolist() for row in raw]

        base_faces = [
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
                ab = mid(a, b)
                bc = mid(b, c)
                ca = mid(c, a)
                nf += [[a, ab, ca], [b, bc, ab], [c, ca, bc], [ab, bc, ca]]
            return nf

        faces = base_faces
        for _ in range(frequency):
            faces = subdivide(verts, faces)

        V  = np.array(verts)
        fa = np.array(faces)

        # ── Keep only upper dome (centroid z > -0.15) ────────────────
        centroid_z = V[fa, 2].mean(axis=1)
        dome_mask  = centroid_z > -0.15
        dome_fa    = fa[dome_mask]

        tri = V[dome_fa]                         # (F, 3, 3)
        zc  = tri[:, :, 2].mean(axis=1)
        zmin, zmax = zc.min(), zc.max()
        cn  = (zc - zmin) / (zmax - zmin + 1e-9)
        fc  = cmap(cn)

        fig = plt.figure(figsize=(7, 7), facecolor="#030308")
        ax  = fig.add_subplot(111, projection="3d")
        ax.set_facecolor("#030308")
        for pane in (ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane):
            pane.fill = False
            pane.set_edgecolor("none")
        ax.grid(False)
        ax.set_axis_off()

        poly = Poly3DCollection(tri, facecolors=fc,
                                edgecolors=(1, 1, 1, 0.30), linewidth=0.7,
                                alpha=alpha)
        ax.add_collection3d(poly)

        if show_base:
            base_z = -0.15
            base_r = np.sqrt(max(0.0, 1.0 - base_z ** 2))
            theta  = np.linspace(0, 2 * np.pi, 120)
            bx = base_r * np.cos(theta)
            by = base_r * np.sin(theta)
            bz = np.full_like(theta, base_z)
            ax.plot(bx, by, bz, color="white", alpha=0.55, linewidth=1.8, zorder=5)

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
            w.IntSlider(value=2, min=1, max=4, step=1,
                        description="frequency"),
            w.Checkbox(value=True,
                       description="show_base"),
            w.FloatSlider(value=0.55, min=0.2, max=1.0, step=0.05,
                          description="alpha"),
            w.IntSlider(value=30, min=0, max=90,  step=5,
                        description="view_elev"),
            w.IntSlider(value=45, min=0, max=360, step=5,
                        description="view_azim"),
        ]

class CalabiYauRenderer(BasePattern):
    """84 — Calabi-Yau Manifold Slice"""
    name  = "Calabi-Yau Manifold Slice"
    group = "3D Objects & Sculptures"

    def render(self, resolution="Low", palette="Neon Cyberpunk", speed=1.0,
               n=5, point_size=0.4, **kwargs):
        from matplotlib.colors import LinearSegmentedColormap

        _RES = {"Low": 80, "Medium": 140, "High": 220}
        M = _RES.get(resolution, 80)

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
        cmap = LinearSegmentedColormap.from_list("cy", cols, N=256)

        n_val = max(2, int(n))

        # Parameterise z1^n + z2^n = 1 in C^2.
        # rho = |z1|, alpha = arg(z1^n)/n in [0, 2*pi/n].
        # Branch (k,j): z1 = rho*exp(i*(alpha + 2*pi*k/n)),
        #   z2 = |1-z1^n|^(1/n) * exp(i*(arg(1-z1^n)/n + 2*pi*j/n)).
        # Satisfies z1^n + z2^n = 1 for all k, j.
        rho   = np.linspace(0.01, 0.99, M)
        alpha = np.linspace(0.0, 2.0 * np.pi / n_val, M)
        RHO, ALPHA = np.meshgrid(rho, alpha)

        z1_n     = RHO ** n_val * np.exp(1j * n_val * ALPHA)
        z2_n     = 1.0 - z1_n
        z2_abs   = np.abs(z2_n) ** (1.0 / n_val)
        z2_arg_b = np.angle(z2_n) / n_val

        all_X, all_Y, all_C = [], [], []

        for k in range(n_val):
            theta1 = ALPHA + 2.0 * np.pi * k / n_val
            re_z1  = RHO * np.cos(theta1)
            im_z1  = RHO * np.sin(theta1)
            for j in range(n_val):
                theta2 = z2_arg_b + 2.0 * np.pi * j / n_val
                re_z2  = z2_abs * np.cos(theta2)
                im_z2  = z2_abs * np.sin(theta2)
                all_X.append(re_z1.ravel())
                all_Y.append(re_z2.ravel())
                all_C.append((im_z1 + im_z2).ravel())

        X  = np.concatenate(all_X)
        Y  = np.concatenate(all_Y)
        C  = np.concatenate(all_C)
        Cn = (C - C.min()) / (C.max() - C.min() + 1e-9)

        fig, ax = plt.subplots(figsize=(7, 7), facecolor="#030308")
        ax.set_facecolor("#030308")
        ax.scatter(X, Y, c=cmap(Cn), s=float(point_size),
                   alpha=0.65, linewidths=0, rasterized=True)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(f"Calabi-Yau Manifold Slice  (n = {n_val})",
                     color="#aaaaaa", fontsize=11, pad=10)
        plt.tight_layout()
        self._fig = fig
        plt.show()
        plt.close(fig)

    def get_controls(self):
        import ipywidgets as w
        return [
            w.IntSlider(value=5, min=2, max=8, step=1,
                        description="n"),
            w.FloatSlider(value=0.4, min=0.1, max=2.0, step=0.1,
                          description="point_size"),
        ]

class SoapBubbleRenderer(BasePattern):
    """85 — Soap Bubble Cluster"""
    name  = "Soap Bubble Cluster"
    group = "3D Objects & Sculptures"

    def render(self, resolution="Low", palette="Ocean Depths", speed=1.0,
               n_bubbles=12, seed=42, alpha=0.35,
               view_elev=20, view_azim=45, **kwargs):
        from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
        import colorsys

        _RES = {"Low": (18, 14), "Medium": (30, 24), "High": (50, 40)}
        n_u, n_v = _RES.get(resolution, (18, 14))

        rng = np.random.default_rng(int(seed))
        n_b = max(3, min(int(n_bubbles), 20))

        # Greedy sphere packing — accept new centre only if it doesn't overlap
        # existing bubbles by more than 8 % of the smaller radius.
        radii   = rng.uniform(0.18, 0.55, n_b)
        centers = np.zeros((n_b, 3))
        placed  = 0
        for _attempt in range(8000):
            if placed >= n_b:
                break
            cand  = rng.uniform(-1.6, 1.6, 3)
            r_new = radii[placed]
            ok = all(
                np.linalg.norm(cand - centers[q]) >= (r_new + radii[q]) * 0.92
                for q in range(placed)
            )
            if ok:
                centers[placed] = cand
                placed += 1
        for q in range(placed, n_b):          # fill any unplaced bubbles
            centers[q] = rng.uniform(-1.6, 1.6, 3)

        # Pre-compute unit sphere mesh once
        u = np.linspace(0, 2.0 * np.pi, n_u)
        v = np.linspace(0, np.pi, n_v)
        U, V   = np.meshgrid(u, v)
        SX = np.sin(V) * np.cos(U)
        SY = np.sin(V) * np.sin(U)
        SZ = np.cos(V)

        fig = plt.figure(figsize=(7, 7), facecolor="#030308")
        ax  = fig.add_subplot(111, projection="3d")
        ax.set_facecolor("#030308")
        for pane in (ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane):
            pane.fill = False
            pane.set_edgecolor("none")
        ax.grid(False)
        ax.set_axis_off()

        # Soap-film iridescent colours (thin-film hue cycling in HSV)
        hue_base = rng.uniform(0.0, 1.0)
        for i, (c, r) in enumerate(zip(centers, radii)):
            hue = (hue_base + i * 0.13) % 1.0
            sat = rng.uniform(0.25, 0.55)
            val = rng.uniform(0.88, 1.00)
            rgb = colorsys.hsv_to_rgb(hue, sat, val)

            X = c[0] + r * SX
            Y = c[1] + r * SY
            Z = c[2] + r * SZ

            ax.plot_surface(X, Y, Z, color=rgb, alpha=float(alpha),
                            linewidth=0, antialiased=True, shade=True)

            # Specular highlight: small white scatter inside the bubble surface
            hl_r = r * 0.55
            hlx  = c[0] + hl_r + rng.uniform(-0.05, 0.05) * r
            hly  = c[1] + hl_r + rng.uniform(-0.05, 0.05) * r
            hlz  = c[2] + hl_r
            ax.scatter([hlx], [hly], [hlz], c="white",
                       s=max(4.0, 55.0 * r ** 2),
                       alpha=0.75, zorder=5, depthshade=False)

        lim = 2.3
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
            w.IntSlider(value=12, min=3, max=20, step=1,
                        description="n_bubbles"),
            w.FloatSlider(value=0.35, min=0.10, max=0.70, step=0.05,
                          description="alpha"),
            w.IntSlider(value=42, min=0, max=100, step=1,
                        description="seed"),
            w.IntSlider(value=20, min=-90, max=90,  step=5,
                        description="view_elev"),
            w.IntSlider(value=45, min=0,   max=360, step=5,
                        description="view_azim"),
        ]

class NeuralMeshRenderer(BasePattern):
    """86 — Neural Mesh Sculpture"""
    name  = "Neural Mesh Sculpture"
    group = "3D Objects & Sculptures"

    def render(self, resolution="Low", palette="Neon Cyberpunk", speed=1.0,
               n_layers=5, conn_threshold=0.65, seed=42,
               view_elev=25, view_azim=45, **kwargs):
        from mpl_toolkits.mplot3d import Axes3D          # noqa: F401
        from mpl_toolkits.mplot3d.art3d import Line3DCollection
        from matplotlib.colors import LinearSegmentedColormap
        from scipy.spatial import cKDTree

        _RES = {"Low": 1.0, "Medium": 1.5, "High": 2.0}
        scale = _RES.get(resolution, 1.0)

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
        cmap = LinearSegmentedColormap.from_list("nm", cols, N=256)

        rng = np.random.default_rng(int(seed))
        n_l = max(3, min(int(n_layers), 8))

        # Build layered neuron positions in 3D.
        # Each layer occupies a fixed x-plane; neurons are spread randomly in y-z.
        pts_list, layer_ids = [], []
        pts_per_layer = [int(rng.integers(5, 14) * scale) for _ in range(n_l)]

        for li, n_pts in enumerate(pts_per_layer):
            x_pos = (li / (n_l - 1)) * 2.0 - 1.0
            for _ in range(n_pts):
                y = rng.uniform(-1.0, 1.0)
                z = rng.uniform(-1.0, 1.0)
                pts_list.append([x_pos, y, z])
                layer_ids.append(li)

        pts    = np.array(pts_list)
        layers = np.array(layer_ids)

        # Build inter-layer edges: connect each source neuron to target neurons
        # within conn_threshold Euclidean distance (adjacent layers only).
        segs, seg_frac = [], []
        thresh = float(conn_threshold)

        for li in range(n_l - 1):
            ma = layers == li
            mb = layers == (li + 1)
            pa, pb = pts[ma], pts[mb]
            if len(pa) == 0 or len(pb) == 0:
                continue
            tree = cKDTree(pb)
            for row_a in pa:
                k_near = min(4, len(pb))
                dists, idxs = tree.query(row_a, k=k_near)
                for d, idx in zip(np.atleast_1d(dists), np.atleast_1d(idxs)):
                    if d <= thresh:
                        segs.append([row_a, pb[idx]])
                        seg_frac.append(li / (n_l - 1))

        fig = plt.figure(figsize=(7, 7), facecolor="#030308")
        ax  = fig.add_subplot(111, projection="3d")
        ax.set_facecolor("#030308")
        for pane in (ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane):
            pane.fill = False
            pane.set_edgecolor("none")
        ax.grid(False)
        ax.set_axis_off()

        # Draw synaptic connections as a single Line3DCollection
        if segs:
            seg_arr  = np.array(segs)
            seg_cols = cmap(np.array(seg_frac))
            seg_cols[:, 3] = 0.30          # dim edges for depth effect
            lc = Line3DCollection(seg_arr, colors=seg_cols,
                                  linewidth=0.8, zorder=1)
            ax.add_collection(lc)

        # Draw neuron bodies — input/output layers rendered larger
        node_frac   = layers / (n_l - 1)
        node_cols   = cmap(node_frac)
        edge_layers = (layers == 0) | (layers == (n_l - 1))
        sizes       = np.where(edge_layers, 80, 35)
        ax.scatter(pts[:, 0], pts[:, 1], pts[:, 2],
                   c=node_cols, s=sizes, alpha=0.92,
                   depthshade=True, zorder=3,
                   edgecolors="white", linewidths=0.4)

        # Faint layer-ring dividers
        theta = np.linspace(0, 2.0 * np.pi, 40)
        for li in range(n_l):
            xp = (li / (n_l - 1)) * 2.0 - 1.0
            ax.plot(np.full(40, xp),
                    1.05 * np.cos(theta),
                    1.05 * np.sin(theta),
                    color="white", alpha=0.06, linewidth=0.6, zorder=0)

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
            w.IntSlider(value=5, min=3, max=8, step=1,
                        description="n_layers"),
            w.FloatSlider(value=0.65, min=0.30, max=1.20, step=0.05,
                          description="conn_threshold"),
            w.IntSlider(value=42, min=0, max=100, step=1,
                        description="seed"),
            w.IntSlider(value=25, min=-90, max=90,  step=5,
                        description="view_elev"),
            w.IntSlider(value=45, min=0,   max=360, step=5,
                        description="view_azim"),
        ]

class TwistedPrismRenderer(BasePattern):
    """87 — Twisted Prism Tower"""
    name  = "Twisted Prism Tower"
    group = "3D Objects & Sculptures"

    def render(self, resolution="Low", palette="Sunset Blaze", speed=1.0,
               n_sides=6, twist_deg=90, taper=0.30, show_floors=True,
               alpha=0.70, view_elev=20, view_azim=30, **kwargs):
        from mpl_toolkits.mplot3d import Axes3D          # noqa: F401
        from mpl_toolkits.mplot3d.art3d import Poly3DCollection
        from matplotlib.colors import LinearSegmentedColormap

        _RES = {"Low": 20, "Medium": 40, "High": 70}
        n_floors = _RES.get(resolution, 20)

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
        cmap = LinearSegmentedColormap.from_list("tp", cols, N=256)

        n_s = max(3, int(n_sides))
        n_f = int(n_floors)
        twist_total = np.radians(float(twist_deg))
        tap = np.clip(float(taper), 0.0, 0.95)

        def floor_verts(i):
            t = i / n_f
            r = 1.0 - tap * t
            angle_off = t * twist_total
            angles = np.linspace(0, 2.0 * np.pi, n_s, endpoint=False) + angle_off
            return np.column_stack([r * np.cos(angles),
                                    r * np.sin(angles),
                                    np.full(n_s, t)])

        floors = [floor_verts(i) for i in range(n_f + 1)]

        # Side quads — one per (floor, edge) pair
        side_faces, side_zc = [], []
        for i in range(n_f):
            f0, f1 = floors[i], floors[i + 1]
            zc = (i + 0.5) / n_f
            for k in range(n_s):
                k1 = (k + 1) % n_s
                side_faces.append([f0[k].tolist(), f0[k1].tolist(),
                                    f1[k1].tolist(), f1[k].tolist()])
                side_zc.append(zc)

        fig = plt.figure(figsize=(7, 7), facecolor="#030308")
        ax  = fig.add_subplot(111, projection="3d")
        ax.set_facecolor("#030308")
        for pane in (ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane):
            pane.fill = False
            pane.set_edgecolor("none")
        ax.grid(False)
        ax.set_axis_off()

        # Coloured side faces
        zn = np.array(side_zc)
        fcs = cmap(zn)
        fcs[:, 3] = float(alpha)
        poly = Poly3DCollection(side_faces, facecolors=fcs,
                                edgecolors=(1, 1, 1, 0.12), linewidth=0.3)
        ax.add_collection3d(poly)

        # Sparse floor plates
        if show_floors:
            step_fp = max(1, n_f // 8)
            fp_faces = [floors[i].tolist() for i in range(0, n_f + 1, step_fp)]
            fp_zc    = np.array([i / n_f for i in range(0, n_f + 1, step_fp)])
            fpcs     = cmap(fp_zc)
            fpcs[:, 3] = 0.55
            ax.add_collection3d(
                Poly3DCollection(fp_faces, facecolors=fpcs,
                                 edgecolors=(1, 1, 1, 0.25), linewidth=0.5))

        lim = 1.15
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_zlim(-0.05, 1.10)
        ax.view_init(elev=view_elev, azim=view_azim)
        plt.tight_layout()
        self._fig = fig
        plt.show()
        plt.close(fig)

    def get_controls(self):
        import ipywidgets as w
        return [
            w.IntSlider(value=6,  min=3,   max=12,  step=1,
                        description="n_sides"),
            w.IntSlider(value=90, min=0,   max=360, step=15,
                        description="twist_deg"),
            w.FloatSlider(value=0.30, min=0.0, max=0.80, step=0.05,
                          description="taper"),
            w.Checkbox(value=True, description="show_floors"),
            w.FloatSlider(value=0.70, min=0.20, max=1.00, step=0.05,
                          description="alpha"),
            w.IntSlider(value=20, min=0,   max=90,  step=5,
                        description="view_elev"),
            w.IntSlider(value=30, min=0,   max=360, step=5,
                        description="view_azim"),
        ]

class FractalMountainRenderer(_StubMixin, BasePattern):
    name = "Fractal Mountain"
    group = "3D Objects & Sculptures"

class VolumetricFogRenderer(_StubMixin, BasePattern):
    name = "Volumetric Fog Cube"
    group = "3D Objects & Sculptures"

class StrangeAttractor3DRenderer(_StubMixin, BasePattern):
    name = "Strange Attractor 3D"
    group = "3D Objects & Sculptures"
