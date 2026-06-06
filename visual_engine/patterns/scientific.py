"""
Scientific & Simulation Patterns (91–100)
"""

import matplotlib.pyplot as plt
import numpy as np
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from engines.renderer import BasePattern


# ─────────────────────────────────────────────────────────────────────────────────
# 91 — Neural Network Visualization
# ─────────────────────────────────────────────────────────────────────────────────
class NeuralNetworkVizRenderer(BasePattern):
    """91 — Neural Network Visualization"""
    name  = "Neural Network Visualization"
    group = "Scientific & Simulation"

    def render(self, resolution="Low", palette="Neon Cyberpunk", speed=1.0,
               layer_sizes="4,6,6,4,2", show_weights=True, activation_seed=42, **kwargs):
        PALETTES = {
            "Inferno":        ["#200060", "#8b0aff", "#ff6b35", "#ffe04b"],
            "Ocean Depths":   ["#0a1628", "#0066cc", "#00ccff", "#80ffee"],
            "Neon Cyberpunk":  ["#0d0221", "#ff006e", "#00f5d4", "#f9c80e"],
            "Forest":         ["#1a2e1a", "#2d6a2d", "#52b252", "#b8f0b8"],
            "Sunset Blaze":   ["#1a0505", "#cc2200", "#ff8800", "#ffee44"],
            "Arctic Aurora":  ["#050a14", "#0033aa", "#00ddaa", "#aaffee"],
            "Monochrome":     ["#111111", "#444444", "#aaaaaa", "#ffffff"],
            "Lava Flow":      ["#1a0000", "#aa1100", "#ff4400", "#ffcc00"],
        }
        cols = PALETTES.get(palette, PALETTES["Neon Cyberpunk"])
        try:
            layers = [max(1, int(x.strip())) for x in str(layer_sizes).split(",")]
        except Exception:
            layers = [4, 6, 6, 4, 2]
        layers = layers[:8]
        rng = np.random.default_rng(int(activation_seed))
        fig, ax = plt.subplots(figsize=(10, 7), facecolor="#07050f")
        ax.set_facecolor("#07050f")
        ax.set_aspect("equal")
        ax.axis("off")
        from matplotlib.colors import LinearSegmentedColormap
        from matplotlib.collections import LineCollection
        cmap_act = LinearSegmentedColormap.from_list(
            "act", [cols[0], cols[1], cols[2], cols[3]], N=256)
        n_layers    = len(layers)
        x_positions = np.linspace(0.1, 0.9, n_layers)
        max_nodes   = max(layers)
        node_pos, node_act = [], []
        for li, n in enumerate(layers):
            xs = np.full(n, x_positions[li])
            ys = np.linspace(0.5 - (n-1)*0.07, 0.5 + (n-1)*0.07, n)
            node_pos.append(np.column_stack([xs, ys]))
            node_act.append(rng.uniform(0.05, 0.95, n))
        if show_weights:
            for li in range(n_layers - 1):
                segs, colors_w = [], []
                for (px, py) in node_pos[li]:
                    for (qx, qy) in node_pos[li + 1]:
                        w = rng.uniform(-1.0, 1.0)
                        segs.append([(px, py), (qx, qy)])
                        if w >= 0:
                            c = cmap_act(0.3 + 0.5 * w)
                        else:
                            c = (*plt.cm.cool(0.3 - 0.3*w)[:3], 0.3)
                        colors_w.append((*c[:3], abs(w)*0.55 + 0.05))
                ax.add_collection(LineCollection(segs, colors=colors_w,
                                                 linewidths=0.7, zorder=1))
        node_r = max(0.012, min(0.018, 0.6 / (max_nodes * 8)))
        for li, (positions, activations) in enumerate(zip(node_pos, node_act)):
            for (px, py), act in zip(positions, activations):
                ax.add_patch(plt.Circle((px, py), node_r*2.2,
                                        color=cmap_act(act), alpha=0.12, zorder=2))
                ax.add_patch(plt.Circle((px, py), node_r,
                                        color=cmap_act(act), zorder=3))
                ax.text(px, py, f"{act:.2f}", ha="center", va="center",
                        fontsize=5.5, color="white", fontweight="bold", zorder=4)
        layer_labels = (["Input"]
                        + [f"Hidden {i}" for i in range(1, n_layers-1)]
                        + ["Output"])
        for li, (xp, lbl) in enumerate(zip(x_positions, layer_labels)):
            ax.text(xp, 0.04, lbl, ha="center", va="center",
                    fontsize=8, color=cols[2], fontweight="bold")
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        ax.set_title("Neural Network Visualization", color=cols[3],
                     fontsize=13, fontweight="bold", pad=10)
        plt.tight_layout()
        self._fig = fig
        plt.show()
        plt.close(fig)

    def get_controls(self):
        import ipywidgets as w
        return [
            w.Text(value="4,6,6,4,2",           description="layer_sizes"),
            w.Checkbox(value=True,                description="show_weights"),
            w.IntSlider(value=42, min=0, max=999,
                        step=1,                   description="activation_seed"),
        ]

# ─────────────────────────────────────────────────────────────────────────────────
# 92 — Atom Orbital Simulator
# ─────────────────────────────────────────────────────────────────────────────────
class AtomOrbitalRenderer(BasePattern):
    """92 — Atom Orbital Simulator"""
    name  = "Atom Orbital Simulator"
    group = "Scientific & Simulation"

    def render(self, resolution="Low", palette="Ocean Depths", speed=1.0,
               n_qn=2, l_qn=1, m_qn=0, view_plane="xz", **kwargs):
        from scipy.special import sph_harm, assoc_laguerre
        from matplotlib.colors import LinearSegmentedColormap
        PALETTES = {
            "Inferno":        ["#200060", "#8b0aff", "#ff6b35", "#ffe04b"],
            "Ocean Depths":   ["#0a1628", "#0066cc", "#00ccff", "#80ffee"],
            "Neon Cyberpunk":  ["#0d0221", "#ff006e", "#00f5d4", "#f9c80e"],
            "Forest":         ["#1a2e1a", "#2d6a2d", "#52b252", "#b8f0b8"],
            "Sunset Blaze":   ["#1a0505", "#cc2200", "#ff8800", "#ffee44"],
            "Arctic Aurora":  ["#050a14", "#0033aa", "#00ddaa", "#aaffee"],
            "Monochrome":     ["#111111", "#444444", "#aaaaaa", "#ffffff"],
            "Lava Flow":      ["#1a0000", "#aa1100", "#ff4400", "#ffcc00"],
        }
        cols = PALETTES.get(palette, PALETTES["Ocean Depths"])
        cmap = LinearSegmentedColormap.from_list(
            "orb", [cols[0], cols[1], cols[2], cols[3]], N=512)
        n = max(1, min(4, int(n_qn)))
        l = max(0, min(n-1, int(l_qn)))
        m = max(-l, min(l, int(m_qn)))
        G = {"Low": 120, "Medium": 200, "High": 320}.get(resolution, 120)
        lim     = 20 * n
        ax_vals = np.linspace(-lim, lim, G)
        A, B    = np.meshgrid(ax_vals, ax_vals)
        vp = str(view_plane).lower()
        if vp == "xy":
            X, Y, Z = A, B, np.zeros_like(A)
        elif vp == "yz":
            X, Y, Z = np.zeros_like(A), A, B
        else:
            X, Y, Z = A, np.zeros_like(A), B
        r     = np.sqrt(X**2 + Y**2 + Z**2) + 1e-12
        theta = np.arccos(np.clip(Z / r, -1, 1))
        phi   = np.arctan2(Y, X)
        rho   = 2 * r / n
        deg   = n - l - 1
        if deg < 0:
            R = np.zeros_like(rho)
        else:
            L = assoc_laguerre(rho, deg, 2*l+1)
            R = np.exp(-rho/2) * (rho**l) * L
        Y_lm = (np.real(sph_harm(m, l, phi, theta)) if m >= 0
                else np.imag(sph_harm(abs(m), l, phi, theta)))
        psi2 = (R * Y_lm)**2
        pmax = psi2.max()
        if pmax > 0:
            psi2 /= pmax
        fig, ax = plt.subplots(figsize=(7, 7), facecolor="#050a14")
        ax.set_facecolor("#050a14")
        im   = ax.imshow(psi2, origin="lower", extent=[-lim, lim, -lim, lim],
                         cmap=cmap, interpolation="bilinear", vmin=0, vmax=1)
        cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label(r"$|\psi|^2$ (normalised)", color=cols[2], fontsize=9)
        cbar.ax.yaxis.set_tick_params(color=cols[2])
        plt.setp(cbar.ax.yaxis.get_ticklabels(), color=cols[2])
        cbar.outline.set_edgecolor(cols[1])
        xlabel, ylabel = {"xy": ("x","y"), "yz": ("y","z"),
                          "xz": ("x","z")}.get(vp, ("x","z"))
        ax.set_xlabel(f"{xlabel} (Bohr radii)", color=cols[2], fontsize=9)
        ax.set_ylabel(f"{ylabel} (Bohr radii)", color=cols[2], fontsize=9)
        ax.tick_params(colors=cols[2])
        for spine in ax.spines.values():
            spine.set_edgecolor(cols[1])
        ax.set_title(f"Hydrogen Orbital  |  n={n}, l={l}, m={m}  |  plane={vp.upper()}",
                     color=cols[3], fontsize=11, fontweight="bold", pad=8)
        plt.tight_layout()
        self._fig = fig
        plt.show()
        plt.close(fig)

    def get_controls(self):
        import ipywidgets as w
        return [
            w.IntSlider(value=2, min=1, max=4,  step=1, description="n_qn"),
            w.IntSlider(value=1, min=0, max=3,  step=1, description="l_qn"),
            w.IntSlider(value=0, min=-3, max=3, step=1, description="m_qn"),
            w.Dropdown(options=["xz","xy","yz"], value="xz", description="view_plane"),
        ]

# ─────────────────────────────────────────────────────────────────────────────────
# 93 — Black Hole Lensing
# ─────────────────────────────────────────────────────────────────────────────────
class BlackHoleLensingRenderer(BasePattern):
    """93 — Black Hole Lensing"""
    name  = "Black Hole Lensing"
    group = "Scientific & Simulation"

    def render(self, resolution="Low", palette="Inferno", speed=1.0,
               mass=1.0, n_rings=5, n_stars=400, star_seed=7,
               show_photon_sphere=True, **kwargs):
        from matplotlib.colors import LinearSegmentedColormap
        PALETTES = {
            "Inferno":        ["#200060", "#8b0aff", "#ff6b35", "#ffe04b"],
            "Ocean Depths":   ["#0a1628", "#0066cc", "#00ccff", "#80ffee"],
            "Neon Cyberpunk":  ["#0d0221", "#ff006e", "#00f5d4", "#f9c80e"],
            "Forest":         ["#1a2e1a", "#2d6a2d", "#52b252", "#b8f0b8"],
            "Sunset Blaze":   ["#1a0505", "#cc2200", "#ff8800", "#ffee44"],
            "Arctic Aurora":  ["#050a14", "#0033aa", "#00ddaa", "#aaffee"],
            "Monochrome":     ["#111111", "#444444", "#aaaaaa", "#ffffff"],
            "Lava Flow":      ["#1a0000", "#aa1100", "#ff4400", "#ffcc00"],
        }
        cols     = PALETTES.get(palette, PALETTES["Inferno"])
        cmap_acc = LinearSegmentedColormap.from_list(
            "acc", ["#000000","#200010","#aa2200","#ff8800","#ffffa0"], N=512)
        rng  = np.random.default_rng(int(star_seed))
        M    = max(0.1, float(mass))
        rs   = 2 * M
        N    = {"Low": 400, "Medium": 700, "High": 1000}.get(resolution, 400)
        fig, ax = plt.subplots(figsize=(8, 8), facecolor="#000000")
        ax.set_facecolor("#000000"); ax.set_aspect("equal"); ax.axis("off")
        view = 12 * M
        sx = rng.uniform(-view, view, n_stars)
        sy = rng.uniform(-view, view, n_stars)
        visible = np.sqrt(sx**2 + sy**2) > rs * 1.1
        sx, sy  = sx[visible], sy[visible]
        ax.scatter(sx, sy, s=rng.uniform(1, 8, len(sx)),
                   c=rng.uniform(0.3, 1.0, len(sx)),
                   cmap="gray", alpha=0.7, zorder=1, linewidths=0)
        theta_vals   = np.linspace(0, 2*np.pi, 400)
        source_radii = np.linspace(3.5*M, 10*M, n_rings)
        for ri, r_src in enumerate(source_radii):
            r_app = r_src / (1 + 4*M/r_src)
            hue   = ri / max(n_rings-1, 1)
            ax.plot(r_app*np.cos(theta_vals), r_app*np.sin(theta_vals),
                    color=plt.cm.hsv(hue), linewidth=max(0.5, 1.8-ri*0.2),
                    alpha=0.75, zorder=3)
        r_isco  = 3 * rs
        r_disk  = np.linspace(r_isco, 6*M, 120)
        phi_acc = np.linspace(0, 2*np.pi, N)
        R_acc, Phi_acc = np.meshgrid(r_disk, phi_acc)
        brightness = (r_isco/R_acc)**2.5 * rng.uniform(0.6, 1.0, R_acc.shape)
        brightness /= brightness.max()
        ax.scatter(R_acc.ravel()*np.cos(Phi_acc.ravel()),
                   R_acc.ravel()*np.sin(Phi_acc.ravel()),
                   c=brightness.ravel(), cmap=cmap_acc,
                   s=0.8, alpha=0.6, zorder=2, linewidths=0)
        ax.add_patch(plt.Circle((0, 0), rs, color="black", zorder=5))
        if show_photon_sphere:
            ax.add_patch(plt.Circle((0, 0), 1.5*rs, fill=False,
                                    edgecolor="#ff8800", linewidth=1.2,
                                    linestyle="--", alpha=0.6, zorder=6))
            ax.text(0, 1.5*rs+0.3*M, "photon sphere", ha="center",
                    color="#ff8800", fontsize=7, alpha=0.8, zorder=7)
        ax.set_xlim(-view, view); ax.set_ylim(-view, view)
        ax.set_title("Black Hole Lensing", color=cols[3],
                     fontsize=13, fontweight="bold", pad=8)
        plt.tight_layout()
        self._fig = fig
        plt.show()
        plt.close(fig)

    def get_controls(self):
        import ipywidgets as w
        return [
            w.FloatSlider(value=1.0, min=0.3, max=3.0, step=0.1, description="mass"),
            w.IntSlider(value=5,   min=2, max=12, step=1,         description="n_rings"),
            w.IntSlider(value=400, min=100, max=800, step=50,     description="n_stars"),
            w.Checkbox(value=True,                                 description="show_photon_sphere"),
        ]

# ─────────────────────────────────────────────────────────────────────────────────
# 94 — Conway's Game of Life
# ─────────────────────────────────────────────────────────────────────────────────
class GameOfLifeRenderer(BasePattern):
    """94 — Conway's Game of Life"""
    name  = "Conway's Game of Life"
    group = "Scientific & Simulation"

    def render(self, resolution="Low", palette="Neon Cyberpunk", speed=1.0,
               n_gens=60, start_pattern="random", density=0.30, seed=0, **kwargs):
        from scipy.ndimage import convolve
        from matplotlib.colors import LinearSegmentedColormap
        PALETTES = {
            "Inferno":        ["#200060", "#8b0aff", "#ff6b35", "#ffe04b"],
            "Ocean Depths":   ["#0a1628", "#0066cc", "#00ccff", "#80ffee"],
            "Neon Cyberpunk":  ["#0d0221", "#ff006e", "#00f5d4", "#f9c80e"],
            "Forest":         ["#1a2e1a", "#2d6a2d", "#52b252", "#b8f0b8"],
            "Sunset Blaze":   ["#1a0505", "#cc2200", "#ff8800", "#ffee44"],
            "Arctic Aurora":  ["#050a14", "#0033aa", "#00ddaa", "#aaffee"],
            "Monochrome":     ["#111111", "#444444", "#aaaaaa", "#ffffff"],
            "Lava Flow":      ["#1a0000", "#aa1100", "#ff4400", "#ffcc00"],
        }
        cols = PALETTES.get(palette, PALETTES["Neon Cyberpunk"])
        cmap = LinearSegmentedColormap.from_list(
            "gol", ["#000000", cols[1], cols[2], cols[3]], N=256)
        G   = {"Low": 80, "Medium": 120, "High": 160}.get(resolution, 80)
        rng = np.random.default_rng(int(seed))
        grid = np.zeros((G, G), dtype=np.int8)
        pat  = str(start_pattern).lower()
        if pat == "glider":
            for cy, cx in [(G//4, G//4), (G//2, G//2)]:
                for dy, dx in [(0,1),(1,2),(2,0),(2,1),(2,2)]:
                    grid[(cy+dy)%G, (cx+dx)%G] = 1
        elif pat == "r-pentomino":
            cy, cx = G//2, G//2
            for dy, dx in [(-1,0),(-1,1),(0,-1),(0,0),(1,0)]:
                grid[(cy+dy)%G, (cx+dx)%G] = 1
        elif pat == "gosper_gun":
            gun = [(5,1),(5,2),(6,1),(6,2),(5,11),(6,11),(7,11),(4,12),(8,12),
                   (3,13),(9,13),(3,14),(9,14),(6,15),(4,16),(8,16),(5,17),(6,17),
                   (7,17),(6,18),(3,21),(4,21),(5,21),(3,22),(4,22),(5,22),(2,23),
                   (6,23),(1,25),(2,25),(6,25),(7,25),(3,35),(4,35),(3,36),(4,36)]
            oy, ox = G//4, G//4
            for dy, dx in gun:
                if 0 <= oy+dy < G and 0 <= ox+dx < G:
                    grid[oy+dy, ox+dx] = 1
        else:
            grid = (rng.uniform(0, 1, (G, G)) < float(density)).astype(np.int8)
        kernel = np.ones((3, 3), dtype=np.int8); kernel[1,1] = 0
        age = grid.copy().astype(np.float32)
        for _ in range(int(n_gens)):
            nbrs = convolve(grid, kernel, mode="wrap")
            new_grid = ((grid==0)&(nbrs==3) | (grid==1)&((nbrs==2)|(nbrs==3))).astype(np.int8)
            age  = np.where(new_grid==1, age+1, 0.0)
            grid = new_grid
        disp = np.where(grid==1, np.log1p(age)/(np.log1p(age.max())+1e-9), 0.0)
        fig, ax = plt.subplots(figsize=(8, 8), facecolor="#000000")
        ax.set_facecolor("#000000")
        ax.imshow(disp, origin="lower", cmap=cmap, interpolation="nearest", vmin=0, vmax=1)
        ax.set_xticks([]); ax.set_yticks([])
        for spine in ax.spines.values(): spine.set_edgecolor(cols[1])
        ax.set_title(
            f"Conway's Game of Life  |  {G}x{G}  |  {int(n_gens)} gens  "
            f"|  {int(grid.sum())} alive  |  {start_pattern}",
            color=cols[3], fontsize=10, fontweight="bold", pad=8)
        plt.tight_layout()
        self._fig = fig
        plt.show()
        plt.close(fig)

    def get_controls(self):
        import ipywidgets as w
        return [
            w.Dropdown(options=["random","glider","r-pentomino","gosper_gun"],
                       value="random", description="start_pattern"),
            w.IntSlider(value=60,  min=10, max=200, step=10,         description="n_gens"),
            w.FloatSlider(value=0.30, min=0.05, max=0.60, step=0.05, description="density"),
            w.IntSlider(value=0, min=0, max=999, step=1,             description="seed"),
        ]

    def animate(self, n_frames=40, fps=10, resolution="Low", palette="Neon Cyberpunk",
                start_pattern="random", density=0.30, seed=0, **kwargs):
        from scipy.ndimage import convolve
        from matplotlib.colors import LinearSegmentedColormap
        from engines.animation import capture_frame
        PALETTES = {
            "Neon Cyberpunk": ["#0d0221", "#ff006e", "#00f5d4", "#f9c80e"],
            "Ocean Depths":   ["#0a1628", "#0066cc", "#00ccff", "#80ffee"],
            "Inferno":        ["#200060", "#8b0aff", "#ff6b35", "#ffe04b"],
        }
        cols = PALETTES.get(palette, PALETTES["Neon Cyberpunk"])
        cmap = LinearSegmentedColormap.from_list("gol", ["#000000", cols[1], cols[2], cols[3]], N=256)
        G = {"Low": 80, "Medium": 120, "High": 160}.get(resolution, 80)
        rng = np.random.default_rng(int(seed))
        grid = np.zeros((G, G), dtype=np.int8)
        pat = str(start_pattern).lower()
        if pat == "glider":
            for cy, cx in [(G//4, G//4), (G//2, G//2)]:
                for dy, dx in [(0,1),(1,2),(2,0),(2,1),(2,2)]:
                    grid[(cy+dy)%G, (cx+dx)%G] = 1
        elif pat == "r-pentomino":
            cy, cx = G//2, G//2
            for dy, dx in [(-1,0),(-1,1),(0,-1),(0,0),(1,0)]:
                grid[(cy+dy)%G, (cx+dx)%G] = 1
        else:
            grid = (rng.uniform(0, 1, (G, G)) < float(density)).astype(np.int8)
        kernel = np.ones((3, 3), dtype=np.int8); kernel[1,1] = 0
        age = grid.copy().astype(np.float32)
        total_gens = n_frames * 2
        frames = []
        for gen in range(total_gens):
            nbrs = convolve(grid, kernel, mode="wrap")
            new_grid = ((grid==0)&(nbrs==3) | (grid==1)&((nbrs==2)|(nbrs==3))).astype(np.int8)
            age = np.where(new_grid==1, age+1, 0.0)
            grid = new_grid
            if gen % 2 == 0:
                disp = np.where(grid==1, np.log1p(age)/(np.log1p(age.max())+1e-9), 0.0)
                fig, ax = plt.subplots(figsize=(6, 6), facecolor="#000000")
                ax.set_facecolor("#000000")
                ax.imshow(disp, origin="lower", cmap=cmap, interpolation="nearest", vmin=0, vmax=1)
                ax.set_xticks([]); ax.set_yticks([])
                ax.set_title(f"Game of Life | gen {gen+1}", color=cols[3], fontsize=9, pad=4)
                plt.tight_layout()
                frames.append(capture_frame(fig))
                plt.close(fig)
        return frames

# ─────────────────────────────────────────────────────────────────────────────────
# 95 — Boids Flocking Simulation
# ─────────────────────────────────────────────────────────────────────────────────
class BoidsFlockingRenderer(BasePattern):
    """95 — Boids Flocking Simulation"""
    name  = "Boids Flocking Simulation"
    group = "Scientific & Simulation"

    def render(self, resolution="Low", palette="Arctic Aurora", speed=1.0,
               n_boids=120, n_steps=80, sep_weight=1.6, align_weight=1.0,
               coh_weight=1.0, sep_radius=0.06, vis_radius=0.18, seed=42, **kwargs):
        from matplotlib.colors import LinearSegmentedColormap
        PALETTES = {
            "Inferno":        ["#200060", "#8b0aff", "#ff6b35", "#ffe04b"],
            "Ocean Depths":   ["#0a1628", "#0066cc", "#00ccff", "#80ffee"],
            "Neon Cyberpunk":  ["#0d0221", "#ff006e", "#00f5d4", "#f9c80e"],
            "Forest":         ["#1a2e1a", "#2d6a2d", "#52b252", "#b8f0b8"],
            "Sunset Blaze":   ["#1a0505", "#cc2200", "#ff8800", "#ffee44"],
            "Arctic Aurora":  ["#050a14", "#0033aa", "#00ddaa", "#aaffee"],
            "Monochrome":     ["#111111", "#444444", "#aaaaaa", "#ffffff"],
            "Lava Flow":      ["#1a0000", "#aa1100", "#ff4400", "#ffcc00"],
        }
        cols = PALETTES.get(palette, PALETTES["Arctic Aurora"])
        cmap = LinearSegmentedColormap.from_list(
            "boids", [cols[1], cols[2], cols[3]], N=256)
        rng = np.random.default_rng(int(seed))
        N   = max(10, int(n_boids))
        pos = rng.uniform(0.1, 0.9, (N, 2))
        vel = rng.uniform(-0.005, 0.005, (N, 2))
        max_speed, min_speed = 0.010, 0.003
        def _clip(v):
            spd = np.linalg.norm(v, axis=1, keepdims=True).clip(1e-12, None)
            v = np.where(spd > max_speed, v/spd*max_speed, v)
            v = np.where(spd < min_speed, v/spd*min_speed, v)
            return v
        R_sep, R_vis = float(sep_radius), float(vis_radius)
        for _ in range(int(n_steps)):
            diff = pos[:, None, :] - pos[None, :, :]
            dist = np.linalg.norm(diff, axis=2)
            eye    = np.eye(N, dtype=bool)
            in_vis = (dist < R_vis) & ~eye
            in_sep = (dist < R_sep) & ~eye
            accel  = np.zeros((N, 2))
            safe_d = np.where(dist < 1e-9, 1e-9, dist)
            accel += float(sep_weight) * np.where(
                in_sep[:,:,None], -diff/safe_d[:,:,None]**2, 0.0).sum(axis=1)
            cnt = in_vis.sum(axis=1, keepdims=True).clip(1, None)
            accel += float(align_weight) * (
                (vel[None,:,:]*in_vis[:,:,None]).sum(axis=1)/cnt - vel)
            accel += float(coh_weight) * (
                (pos[None,:,:]*in_vis[:,:,None]).sum(axis=1)/cnt - pos) * 0.05
            vel  = _clip(vel + accel*0.05)
            pos  = (pos + vel) % 1.0
        spd   = np.linalg.norm(vel, axis=1)
        spd_n = (spd - spd.min()) / (spd.max() - spd.min() + 1e-9)
        fig, ax = plt.subplots(figsize=(8, 8), facecolor=cols[0])
        ax.set_facecolor(cols[0]); ax.set_aspect("equal")
        ax.quiver(pos[:,0], pos[:,1], vel[:,0], vel[:,1],
                  color=cmap(spd_n), angles="xy", scale_units="xy",
                  scale=0.12, width=0.003, headwidth=4, headlength=5,
                  alpha=0.9, zorder=3)
        ax.scatter(pos[:,0], pos[:,1], c=spd_n, cmap=cmap, s=18,
                   zorder=4, linewidths=0)
        ax.set_xlim(0,1); ax.set_ylim(0,1)
        ax.set_xticks([]); ax.set_yticks([])
        for spine in ax.spines.values(): spine.set_edgecolor(cols[2])
        ax.set_title(
            f"Boids Flocking  |  N={N}  |  {int(n_steps)} steps  "
            f"|  sep={float(sep_weight):.1f}  align={float(align_weight):.1f}  "
            f"coh={float(coh_weight):.1f}",
            color=cols[3], fontsize=10, fontweight="bold", pad=8)
        plt.tight_layout()
        self._fig = fig
        plt.show()
        plt.close(fig)

    def get_controls(self):
        import ipywidgets as w
        return [
            w.IntSlider(value=120, min=20, max=300, step=10,        description="n_boids"),
            w.IntSlider(value=80,  min=10, max=200, step=10,        description="n_steps"),
            w.FloatSlider(value=1.6, min=0.0, max=4.0, step=0.2,   description="sep_weight"),
            w.FloatSlider(value=1.0, min=0.0, max=4.0, step=0.2,   description="align_weight"),
            w.FloatSlider(value=1.0, min=0.0, max=4.0, step=0.2,   description="coh_weight"),
        ]

    def animate(self, n_frames=40, fps=12, palette="Arctic Aurora", n_boids=80,
                sep_weight=1.6, align_weight=1.0, coh_weight=1.0, seed=42, **kwargs):
        from matplotlib.colors import LinearSegmentedColormap
        from engines.animation import capture_frame
        PALETTES = {
            "Arctic Aurora": ["#050a14", "#0033aa", "#00ddaa", "#aaffee"],
            "Neon Cyberpunk": ["#0d0221", "#ff006e", "#00f5d4", "#f9c80e"],
        }
        cols = PALETTES.get(palette, PALETTES["Arctic Aurora"])
        cmap = LinearSegmentedColormap.from_list("boids", [cols[1], cols[2], cols[3]], N=256)
        rng = np.random.default_rng(int(seed))
        N = max(10, int(n_boids))
        pos = rng.uniform(0.1, 0.9, (N, 2))
        vel = rng.uniform(-0.005, 0.005, (N, 2))
        max_speed, min_speed = 0.010, 0.003
        R_sep, R_vis = 0.06, 0.18
        frames = []
        for step in range(n_frames * 2):
            diff = pos[:, None, :] - pos[None, :, :]
            dist = np.linalg.norm(diff, axis=2)
            eye = np.eye(N, dtype=bool)
            in_vis = (dist < R_vis) & ~eye
            in_sep = (dist < R_sep) & ~eye
            accel = np.zeros((N, 2))
            safe_d = np.where(dist < 1e-9, 1e-9, dist)
            accel += float(sep_weight) * np.where(
                in_sep[:,:,None], -diff/safe_d[:,:,None]**2, 0.0).sum(axis=1)
            cnt = in_vis.sum(axis=1, keepdims=True).clip(1, None)
            accel += float(align_weight) * (
                (vel[None,:,:]*in_vis[:,:,None]).sum(axis=1)/cnt - vel)
            accel += float(coh_weight) * (
                (pos[None,:,:]*in_vis[:,:,None]).sum(axis=1)/cnt - pos) * 0.05
            vel = vel + accel * 0.05
            spd = np.linalg.norm(vel, axis=1, keepdims=True).clip(1e-12, None)
            vel = np.where(spd > max_speed, vel/spd*max_speed, vel)
            vel = np.where(spd < min_speed, vel/spd*min_speed, vel)
            pos = (pos + vel) % 1.0
            if step % 2 == 0:
                spd_n = (np.linalg.norm(vel, axis=1) - min_speed) / (max_speed - min_speed + 1e-9)
                fig, ax = plt.subplots(figsize=(6, 6), facecolor=cols[0])
                ax.set_facecolor(cols[0]); ax.set_aspect("equal")
                ax.quiver(pos[:,0], pos[:,1], vel[:,0], vel[:,1],
                          color=cmap(spd_n), angles="xy", scale_units="xy",
                          scale=0.12, width=0.003, headwidth=4, alpha=0.9)
                ax.set_xlim(0,1); ax.set_ylim(0,1)
                ax.set_xticks([]); ax.set_yticks([])
                ax.set_title(f"Boids | step {step+1}", color=cols[3], fontsize=9, pad=4)
                plt.tight_layout()
                frames.append(capture_frame(fig))
                plt.close(fig)
        return frames


class TrafficFlowRenderer(BasePattern):
    """96 — Traffic Flow Simulation (Nagel-Schreckenberg model)"""
    name  = "Traffic Flow Simulation"
    group = "Scientific & Simulation"

    def render(self, resolution="Low", palette="Sunset Blaze", speed=1.0,
               road_length=200, n_cars=50, v_max=5, p_slow=0.3,
               n_steps=150, seed=42, **kwargs):
        from matplotlib.colors import LinearSegmentedColormap
        PALETTES = {
            "Inferno":        ["#200060", "#8b0aff", "#ff6b35", "#ffe04b"],
            "Ocean Depths":   ["#0a1628", "#0066cc", "#00ccff", "#80ffee"],
            "Neon Cyberpunk": ["#0d0221", "#ff006e", "#00f5d4", "#f9c80e"],
            "Forest":         ["#1a2e1a", "#2d6a2d", "#52b252", "#b8f0b8"],
            "Sunset Blaze":   ["#1a0505", "#cc2200", "#ff8800", "#ffee44"],
            "Arctic Aurora":  ["#050a14", "#0033aa", "#00ddaa", "#aaffee"],
            "Monochrome":     ["#111111", "#444444", "#aaaaaa", "#ffffff"],
            "Lava Flow":      ["#1a0000", "#aa1100", "#ff4400", "#ffcc00"],
        }
        cols = PALETTES.get(palette, PALETTES["Sunset Blaze"])
        cmap = LinearSegmentedColormap.from_list(
            "traffic", ["#000000", cols[1], cols[2], cols[3]], N=256)
        rng = np.random.default_rng(int(seed))
        L       = max(50, int(road_length))
        N_cars  = min(int(n_cars), L - 1)
        Vmax    = max(1, int(v_max))
        p       = float(p_slow)
        steps   = max(20, int(n_steps))
        # Initialize: place cars randomly on circular road
        positions = np.sort(rng.choice(L, N_cars, replace=False))
        velocities = rng.integers(0, Vmax + 1, N_cars)
        # Space-time diagram: rows = time, cols = road cells
        # Value = velocity of car at that cell (0 = empty → -1)
        spacetime = np.full((steps, L), -1, dtype=np.int8)
        for t in range(steps):
            # Record current state
            spacetime[t, positions] = velocities
            # NaSch update rules (parallel update)
            # 1) Acceleration: v = min(v+1, Vmax)
            velocities = np.minimum(velocities + 1, Vmax)
            # 2) Braking: compute gap to next car (circular)
            sorted_idx = np.argsort(positions)
            pos_sorted = positions[sorted_idx]
            vel_sorted = velocities[sorted_idx]
            gaps = np.empty(N_cars, dtype=np.int64)
            gaps[:-1] = pos_sorted[1:] - pos_sorted[:-1] - 1
            gaps[-1]  = (pos_sorted[0] + L) - pos_sorted[-1] - 1
            vel_sorted = np.minimum(vel_sorted, gaps)
            # 3) Randomization: with probability p, v = max(v-1, 0)
            rand_mask = rng.uniform(0, 1, N_cars) < p
            vel_sorted = np.where(rand_mask, np.maximum(vel_sorted - 1, 0), vel_sorted)
            # 4) Movement
            pos_sorted = (pos_sorted + vel_sorted) % L
            # Unsort back
            inv_idx = np.empty_like(sorted_idx)
            inv_idx[sorted_idx] = np.arange(N_cars)
            positions  = pos_sorted[inv_idx]
            velocities = vel_sorted[inv_idx]
        # Visualization: space-time diagram
        display_data = np.where(spacetime >= 0, spacetime.astype(np.float32) / Vmax, np.nan)
        fig, ax = plt.subplots(figsize=(10, 6), facecolor=cols[0])
        ax.set_facecolor(cols[0])
        # Plot occupied cells as colored markers
        t_coords, x_coords = np.where(spacetime >= 0)
        v_vals = spacetime[spacetime >= 0].astype(np.float32) / Vmax
        ax.scatter(x_coords, t_coords, c=v_vals, cmap=cmap, s=1.2,
                   marker='s', linewidths=0, alpha=0.9, vmin=0, vmax=1)
        ax.set_xlim(0, L)
        ax.set_ylim(steps, 0)
        ax.set_xlabel("Road position (cells)", color=cols[2], fontsize=9)
        ax.set_ylabel("Time step", color=cols[2], fontsize=9)
        ax.tick_params(colors=cols[2])
        for spine in ax.spines.values():
            spine.set_edgecolor(cols[1])
        # Colorbar
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(0, Vmax))
        sm.set_array([])
        cbar = fig.colorbar(sm, ax=ax, fraction=0.03, pad=0.02)
        cbar.set_label("Velocity", color=cols[2], fontsize=9)
        cbar.ax.yaxis.set_tick_params(color=cols[2])
        plt.setp(cbar.ax.yaxis.get_ticklabels(), color=cols[2])
        cbar.outline.set_edgecolor(cols[1])
        density_val = N_cars / L
        avg_flow = np.mean(spacetime[spacetime >= 0])
        ax.set_title(
            f"Traffic Flow (Nagel-Schreckenberg)  |  L={L}  N={N_cars}  "
            f"ρ={density_val:.2f}  Vmax={Vmax}  p={p:.2f}",
            color=cols[3], fontsize=10, fontweight="bold", pad=8)
        plt.tight_layout()
        self._fig = fig
        plt.show()
        plt.close(fig)

    def get_controls(self):
        import ipywidgets as w
        return [
            w.IntSlider(value=200, min=50, max=500, step=10,       description="road_length"),
            w.IntSlider(value=50,  min=10, max=200, step=5,        description="n_cars"),
            w.IntSlider(value=5,   min=1,  max=10,  step=1,        description="v_max"),
            w.FloatSlider(value=0.3, min=0.0, max=0.8, step=0.05,  description="p_slow"),
            w.IntSlider(value=150, min=20, max=300, step=10,       description="n_steps"),
            w.IntSlider(value=42,  min=0,  max=999, step=1,        description="seed"),
        ]

    def animate(self, n_frames=50, fps=10, palette="Sunset Blaze",
                road_length=200, n_cars=50, v_max=5, p_slow=0.3, seed=42, **kwargs):
        from matplotlib.colors import LinearSegmentedColormap
        from engines.animation import capture_frame
        cols = ["#1a0505", "#cc2200", "#ff8800", "#ffee44"]
        cmap = LinearSegmentedColormap.from_list("traffic", ["#000000", cols[1], cols[2], cols[3]], N=256)
        rng = np.random.default_rng(int(seed))
        L = max(50, int(road_length))
        N_cars = min(int(n_cars), L - 1)
        Vmax = max(1, int(v_max))
        p = float(p_slow)
        positions = np.sort(rng.choice(L, N_cars, replace=False))
        velocities = rng.integers(0, Vmax + 1, N_cars)
        frames = []
        spacetime = np.full((n_frames * 3, L), -1, dtype=np.int8)
        for t in range(n_frames * 3):
            spacetime[t, positions] = velocities
            velocities = np.minimum(velocities + 1, Vmax)
            sorted_idx = np.argsort(positions)
            pos_sorted = positions[sorted_idx]
            vel_sorted = velocities[sorted_idx]
            gaps = np.empty(N_cars, dtype=np.int64)
            gaps[:-1] = pos_sorted[1:] - pos_sorted[:-1] - 1
            gaps[-1] = (pos_sorted[0] + L) - pos_sorted[-1] - 1
            vel_sorted = np.minimum(vel_sorted, gaps)
            rand_mask = rng.uniform(0, 1, N_cars) < p
            vel_sorted = np.where(rand_mask, np.maximum(vel_sorted - 1, 0), vel_sorted)
            pos_sorted = (pos_sorted + vel_sorted) % L
            inv_idx = np.empty_like(sorted_idx)
            inv_idx[sorted_idx] = np.arange(N_cars)
            positions = pos_sorted[inv_idx]
            velocities = vel_sorted[inv_idx]
            if t % 3 == 0:
                fig, ax = plt.subplots(figsize=(8, 4), facecolor=cols[0])
                ax.set_facecolor(cols[0])
                end = t + 1
                st = spacetime[:end]
                t_c, x_c = np.where(st >= 0)
                v_v = st[st >= 0].astype(np.float32) / Vmax
                ax.scatter(x_c, t_c, c=v_v, cmap=cmap, s=1.0, marker='s', linewidths=0, vmin=0, vmax=1)
                ax.set_xlim(0, L); ax.set_ylim(end, 0)
                ax.set_xticks([]); ax.set_yticks([])
                ax.set_title(f"Traffic Flow | t={t+1}", color=cols[3], fontsize=9, pad=4)
                plt.tight_layout()
                frames.append(capture_frame(fig))
                plt.close(fig)
        return frames


class EcosystemRenderer(BasePattern):
    """97 — Ecosystem Predator-Prey (Lotka-Volterra)"""
    name  = "Ecosystem Predator-Prey"
    group = "Scientific & Simulation"

    def render(self, resolution="Low", palette="Forest", speed=1.0,
               alpha=1.1, beta=0.4, delta=0.1, gamma=0.4,
               prey_0=10.0, pred_0=5.0, t_max=50.0, seed=0, **kwargs):
        from matplotlib.colors import LinearSegmentedColormap
        PALETTES = {
            "Inferno":        ["#200060", "#8b0aff", "#ff6b35", "#ffe04b"],
            "Ocean Depths":   ["#0a1628", "#0066cc", "#00ccff", "#80ffee"],
            "Neon Cyberpunk": ["#0d0221", "#ff006e", "#00f5d4", "#f9c80e"],
            "Forest":         ["#1a2e1a", "#2d6a2d", "#52b252", "#b8f0b8"],
            "Sunset Blaze":   ["#1a0505", "#cc2200", "#ff8800", "#ffee44"],
            "Arctic Aurora":  ["#050a14", "#0033aa", "#00ddaa", "#aaffee"],
            "Monochrome":     ["#111111", "#444444", "#aaaaaa", "#ffffff"],
            "Lava Flow":      ["#1a0000", "#aa1100", "#ff4400", "#ffcc00"],
        }
        cols = PALETTES.get(palette, PALETTES["Forest"])
        a, b, d, g = float(alpha), float(beta), float(delta), float(gamma)
        x0, y0 = float(prey_0), float(pred_0)
        T = float(t_max)
        # RK4 integration of Lotka-Volterra
        dt = 0.01
        N_pts = int(T / dt)
        t_arr = np.linspace(0, T, N_pts)
        x = np.empty(N_pts)
        y = np.empty(N_pts)
        x[0], y[0] = x0, y0
        def deriv(xi, yi):
            dx = a * xi - b * xi * yi
            dy = d * xi * yi - g * yi
            return dx, dy
        for i in range(N_pts - 1):
            k1x, k1y = deriv(x[i], y[i])
            k2x, k2y = deriv(x[i]+dt/2*k1x, y[i]+dt/2*k1y)
            k3x, k3y = deriv(x[i]+dt/2*k2x, y[i]+dt/2*k2y)
            k4x, k4y = deriv(x[i]+dt*k3x, y[i]+dt*k3y)
            x[i+1] = max(0, x[i] + dt/6*(k1x + 2*k2x + 2*k3x + k4x))
            y[i+1] = max(0, y[i] + dt/6*(k1y + 2*k2y + 2*k3y + k4y))
        # Dual plot: time series + phase portrait
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), facecolor=cols[0])
        for ax in (ax1, ax2):
            ax.set_facecolor(cols[0])
            ax.tick_params(colors=cols[2])
            for spine in ax.spines.values():
                spine.set_edgecolor(cols[1])
        # Time series
        ax1.plot(t_arr, x, color=cols[2], linewidth=1.5, label="Prey")
        ax1.plot(t_arr, y, color=cols[3], linewidth=1.5, label="Predator")
        ax1.fill_between(t_arr, 0, x, color=cols[2], alpha=0.1)
        ax1.fill_between(t_arr, 0, y, color=cols[3], alpha=0.1)
        ax1.set_xlabel("Time", color=cols[2], fontsize=9)
        ax1.set_ylabel("Population", color=cols[2], fontsize=9)
        ax1.legend(loc="upper right", fontsize=8, framealpha=0.5,
                   labelcolor=cols[3])
        ax1.set_title("Population Dynamics", color=cols[3], fontsize=10, fontweight="bold")
        # Phase portrait
        ax2.plot(x, y, color=cols[2], linewidth=0.8, alpha=0.8)
        ax2.scatter([x[0]], [y[0]], color=cols[3], s=60, zorder=5,
                    marker='o', label="Start")
        ax2.scatter([x[-1]], [y[-1]], color=cols[2], s=60, zorder=5,
                    marker='s', label="End")
        # Add nullclines
        x_range = np.linspace(0.01, x.max()*1.2, 100)
        ax2.axhline(a/b, color=cols[3], linestyle='--', alpha=0.4, linewidth=0.8)
        ax2.axvline(g/d, color=cols[2], linestyle='--', alpha=0.4, linewidth=0.8)
        ax2.set_xlabel("Prey population", color=cols[2], fontsize=9)
        ax2.set_ylabel("Predator population", color=cols[2], fontsize=9)
        ax2.legend(loc="upper right", fontsize=8, framealpha=0.5,
                   labelcolor=cols[3])
        ax2.set_title("Phase Portrait", color=cols[3], fontsize=10, fontweight="bold")
        fig.suptitle(
            f"Lotka-Volterra Predator-Prey  |  α={a:.1f}  β={b:.1f}  δ={d:.2f}  γ={g:.1f}",
            color=cols[3], fontsize=11, fontweight="bold", y=0.98)
        plt.tight_layout()
        self._fig = fig
        plt.show()
        plt.close(fig)

    def get_controls(self):
        import ipywidgets as w
        return [
            w.FloatSlider(value=1.1, min=0.1, max=3.0, step=0.1,  description="alpha"),
            w.FloatSlider(value=0.4, min=0.05, max=1.5, step=0.05, description="beta"),
            w.FloatSlider(value=0.1, min=0.01, max=0.5, step=0.01, description="delta"),
            w.FloatSlider(value=0.4, min=0.05, max=1.5, step=0.05, description="gamma"),
            w.FloatSlider(value=10.0, min=1.0, max=50.0, step=1.0, description="prey_0"),
            w.FloatSlider(value=5.0,  min=1.0, max=30.0, step=1.0, description="pred_0"),
            w.FloatSlider(value=50.0, min=10.0, max=200.0, step=10.0, description="t_max"),
        ]

    def animate(self, n_frames=40, fps=10, palette="Forest",
                alpha=1.1, beta=0.4, delta=0.1, gamma=0.4,
                prey_0=10.0, pred_0=5.0, t_max=50.0, **kwargs):
        from engines.animation import capture_frame
        cols = ["#1a2e1a", "#2d6a2d", "#52b252", "#b8f0b8"]
        a, b, d, g = float(alpha), float(beta), float(delta), float(gamma)
        x0, y0, T = float(prey_0), float(pred_0), float(t_max)
        dt = 0.01
        N_pts = int(T / dt)
        t_arr = np.linspace(0, T, N_pts)
        x, y = np.empty(N_pts), np.empty(N_pts)
        x[0], y[0] = x0, y0
        def deriv(xi, yi):
            return a*xi - b*xi*yi, d*xi*yi - g*yi
        for i in range(N_pts - 1):
            k1x, k1y = deriv(x[i], y[i])
            k2x, k2y = deriv(x[i]+dt/2*k1x, y[i]+dt/2*k1y)
            k3x, k3y = deriv(x[i]+dt/2*k2x, y[i]+dt/2*k2y)
            k4x, k4y = deriv(x[i]+dt*k3x, y[i]+dt*k3y)
            x[i+1] = max(0, x[i] + dt/6*(k1x + 2*k2x + 2*k3x + k4x))
            y[i+1] = max(0, y[i] + dt/6*(k1y + 2*k2y + 2*k3y + k4y))
        frames = []
        step = max(1, N_pts // n_frames)
        for f in range(n_frames):
            end = min((f+1) * step, N_pts)
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), facecolor=cols[0])
            for ax in (ax1, ax2):
                ax.set_facecolor(cols[0])
                ax.tick_params(colors=cols[2])
            ax1.plot(t_arr[:end], x[:end], color=cols[2], linewidth=1.2, label="Prey")
            ax1.plot(t_arr[:end], y[:end], color=cols[3], linewidth=1.2, label="Predator")
            ax1.set_xlim(0, T); ax1.set_ylim(0, max(x.max(), y.max())*1.1)
            ax1.set_title("Populations", color=cols[3], fontsize=9)
            ax1.legend(fontsize=7, framealpha=0.4, labelcolor=cols[3])
            ax2.plot(x[:end], y[:end], color=cols[2], linewidth=0.8)
            ax2.scatter([x[end-1]], [y[end-1]], color=cols[3], s=40, zorder=5)
            ax2.set_xlim(0, x.max()*1.1); ax2.set_ylim(0, y.max()*1.1)
            ax2.set_title("Phase Portrait", color=cols[3], fontsize=9)
            plt.tight_layout()
            frames.append(capture_frame(fig))
            plt.close(fig)
        return frames


class AntColonyRenderer(BasePattern):
    """98 — Ant Colony Optimization (TSP)"""
    name  = "Ant Colony Optimization"
    group = "Scientific & Simulation"

    def render(self, resolution="Low", palette="Lava Flow", speed=1.0,
               n_cities=25, n_ants=30, n_iterations=80, alpha_aco=1.0,
               beta_aco=3.0, evaporation=0.5, seed=42, **kwargs):
        from matplotlib.collections import LineCollection
        from matplotlib.colors import LinearSegmentedColormap
        PALETTES = {
            "Inferno":        ["#200060", "#8b0aff", "#ff6b35", "#ffe04b"],
            "Ocean Depths":   ["#0a1628", "#0066cc", "#00ccff", "#80ffee"],
            "Neon Cyberpunk": ["#0d0221", "#ff006e", "#00f5d4", "#f9c80e"],
            "Forest":         ["#1a2e1a", "#2d6a2d", "#52b252", "#b8f0b8"],
            "Sunset Blaze":   ["#1a0505", "#cc2200", "#ff8800", "#ffee44"],
            "Arctic Aurora":  ["#050a14", "#0033aa", "#00ddaa", "#aaffee"],
            "Monochrome":     ["#111111", "#444444", "#aaaaaa", "#ffffff"],
            "Lava Flow":      ["#1a0000", "#aa1100", "#ff4400", "#ffcc00"],
        }
        cols = PALETTES.get(palette, PALETTES["Lava Flow"])
        cmap_pher = LinearSegmentedColormap.from_list(
            "pher", ["#000000", cols[1], cols[2], cols[3]], N=256)
        rng = np.random.default_rng(int(seed))
        NC     = max(5, int(n_cities))
        N_ants = max(5, int(n_ants))
        iters  = max(5, int(n_iterations))
        a_exp  = float(alpha_aco)
        b_exp  = float(beta_aco)
        rho    = float(evaporation)
        # City positions
        cities = rng.uniform(0.05, 0.95, (NC, 2))
        # Distance matrix
        diff = cities[:, None, :] - cities[None, :, :]
        dist = np.sqrt((diff**2).sum(axis=2))
        np.fill_diagonal(dist, 1e-12)
        # Pheromone matrix
        pheromone = np.ones((NC, NC))
        eta = 1.0 / dist  # heuristic (inverse distance)
        best_tour = None
        best_length = np.inf
        for iteration in range(iters):
            tours = []
            lengths = []
            for _ in range(N_ants):
                visited = [rng.integers(0, NC)]
                for _ in range(NC - 1):
                    curr = visited[-1]
                    unvisited = [j for j in range(NC) if j not in visited]
                    probs = np.array([
                        (pheromone[curr, j] ** a_exp) * (eta[curr, j] ** b_exp)
                        for j in unvisited
                    ])
                    probs /= probs.sum()
                    next_city = unvisited[rng.choice(len(unvisited), p=probs)]
                    visited.append(next_city)
                tours.append(visited)
                length = sum(dist[visited[i], visited[(i+1) % NC]] for i in range(NC))
                lengths.append(length)
                if length < best_length:
                    best_length = length
                    best_tour = visited[:]
            # Evaporation
            pheromone *= (1 - rho)
            # Deposit
            for tour, length in zip(tours, lengths):
                deposit = 1.0 / length
                for i in range(NC):
                    a_c, b_c = tour[i], tour[(i+1) % NC]
                    pheromone[a_c, b_c] += deposit
                    pheromone[b_c, a_c] += deposit
        # Visualization
        fig, ax = plt.subplots(figsize=(8, 8), facecolor=cols[0])
        ax.set_facecolor(cols[0])
        ax.set_aspect("equal")
        # Draw pheromone trails (all edges with significant pheromone)
        segs, seg_colors = [], []
        pmax = pheromone.max()
        for i in range(NC):
            for j in range(i+1, NC):
                strength = pheromone[i, j] / pmax
                if strength > 0.05:
                    segs.append([cities[i], cities[j]])
                    seg_colors.append((*plt.cm.colors.to_rgba(
                        cmap_pher(strength))[:3], strength * 0.7))
        if segs:
            lc = LineCollection(segs, colors=seg_colors,
                                linewidths=[c[3]*3 for c in seg_colors], zorder=1)
            ax.add_collection(lc)
        # Draw best tour
        if best_tour is not None:
            tour_pts = cities[best_tour + [best_tour[0]]]
            ax.plot(tour_pts[:, 0], tour_pts[:, 1], color=cols[3],
                    linewidth=2.5, alpha=0.9, zorder=3)
        # Draw cities
        ax.scatter(cities[:, 0], cities[:, 1], s=80, color=cols[2],
                   edgecolors=cols[3], linewidths=1.5, zorder=4)
        for i, (cx, cy) in enumerate(cities):
            ax.text(cx, cy + 0.025, str(i), ha="center", va="bottom",
                    fontsize=7, color=cols[3], fontweight="bold", zorder=5)
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        ax.set_xticks([]); ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_edgecolor(cols[1])
        ax.set_title(
            f"Ant Colony Optimization (TSP)  |  {NC} cities  |  "
            f"best={best_length:.2f}  |  {iters} iters × {N_ants} ants",
            color=cols[3], fontsize=10, fontweight="bold", pad=8)
        plt.tight_layout()
        self._fig = fig
        plt.show()
        plt.close(fig)

    def get_controls(self):
        import ipywidgets as w
        return [
            w.IntSlider(value=25, min=5,  max=50,  step=1,         description="n_cities"),
            w.IntSlider(value=30, min=5,  max=100, step=5,         description="n_ants"),
            w.IntSlider(value=80, min=10, max=200, step=10,        description="n_iterations"),
            w.FloatSlider(value=1.0, min=0.5, max=3.0, step=0.1,  description="alpha_aco"),
            w.FloatSlider(value=3.0, min=1.0, max=6.0, step=0.5,  description="beta_aco"),
            w.FloatSlider(value=0.5, min=0.1, max=0.9, step=0.1,  description="evaporation"),
            w.IntSlider(value=42, min=0, max=999, step=1,          description="seed"),
        ]

    def animate(self, n_frames=30, fps=8, palette="Lava Flow",
                n_cities=20, n_ants=20, alpha_aco=1.0, beta_aco=3.0,
                evaporation=0.5, seed=42, **kwargs):
        from matplotlib.collections import LineCollection
        from engines.animation import capture_frame
        cols = ["#1a0000", "#aa1100", "#ff4400", "#ffcc00"]
        rng = np.random.default_rng(int(seed))
        NC = max(5, int(n_cities))
        N_ants = max(5, int(n_ants))
        a_exp, b_exp, rho = float(alpha_aco), float(beta_aco), float(evaporation)
        cities = rng.uniform(0.05, 0.95, (NC, 2))
        diff = cities[:, None, :] - cities[None, :, :]
        dist = np.sqrt((diff**2).sum(axis=2))
        np.fill_diagonal(dist, 1e-12)
        pheromone = np.ones((NC, NC))
        eta = 1.0 / dist
        best_tour, best_length = None, np.inf
        frames = []
        iters = n_frames
        for iteration in range(iters):
            tours, lengths = [], []
            for _ in range(N_ants):
                visited = [rng.integers(0, NC)]
                for _ in range(NC - 1):
                    curr = visited[-1]
                    unvisited = [j for j in range(NC) if j not in visited]
                    probs = np.array([(pheromone[curr,j]**a_exp)*(eta[curr,j]**b_exp) for j in unvisited])
                    probs /= probs.sum()
                    visited.append(unvisited[rng.choice(len(unvisited), p=probs)])
                tours.append(visited)
                length = sum(dist[visited[i], visited[(i+1)%NC]] for i in range(NC))
                lengths.append(length)
                if length < best_length:
                    best_length, best_tour = length, visited[:]
            pheromone *= (1 - rho)
            for tour, length in zip(tours, lengths):
                dep = 1.0 / length
                for i in range(NC):
                    a_c, b_c = tour[i], tour[(i+1)%NC]
                    pheromone[a_c, b_c] += dep
                    pheromone[b_c, a_c] += dep
            # Capture frame
            fig, ax = plt.subplots(figsize=(6, 6), facecolor=cols[0])
            ax.set_facecolor(cols[0]); ax.set_aspect("equal")
            pmax = pheromone.max()
            segs, seg_a = [], []
            for i in range(NC):
                for j in range(i+1, NC):
                    s = pheromone[i,j] / pmax
                    if s > 0.05:
                        segs.append([cities[i], cities[j]])
                        seg_a.append((*[int(c,16)/255 for c in [cols[2][1:3],cols[2][3:5],cols[2][5:7]]], s*0.7))
            if segs:
                ax.add_collection(LineCollection(segs, colors=seg_a, linewidths=[c[3]*3 for c in seg_a]))
            if best_tour:
                tp = cities[best_tour + [best_tour[0]]]
                ax.plot(tp[:,0], tp[:,1], color=cols[3], linewidth=2, alpha=0.9)
            ax.scatter(cities[:,0], cities[:,1], s=60, color=cols[2], edgecolors=cols[3], linewidths=1.2, zorder=4)
            ax.set_xlim(0,1); ax.set_ylim(0,1); ax.set_xticks([]); ax.set_yticks([])
            ax.set_title(f"ACO | iter {iteration+1} | best={best_length:.2f}", color=cols[3], fontsize=9, pad=4)
            plt.tight_layout()
            frames.append(capture_frame(fig))
            plt.close(fig)
        return frames


class FluidDynamicsRenderer(BasePattern):
    """99 — Fluid Dynamics (Smoothed Particle Hydrodynamics)"""
    name  = "Fluid Dynamics (SPH)"
    group = "Scientific & Simulation"

    def render(self, resolution="Low", palette="Ocean Depths", speed=1.0,
               n_particles=300, n_steps=60, gravity=9.8, viscosity=0.02,
               rest_density=1000.0, gas_const=2000.0, seed=7, **kwargs):
        from matplotlib.colors import LinearSegmentedColormap
        PALETTES = {
            "Inferno":        ["#200060", "#8b0aff", "#ff6b35", "#ffe04b"],
            "Ocean Depths":   ["#0a1628", "#0066cc", "#00ccff", "#80ffee"],
            "Neon Cyberpunk": ["#0d0221", "#ff006e", "#00f5d4", "#f9c80e"],
            "Forest":         ["#1a2e1a", "#2d6a2d", "#52b252", "#b8f0b8"],
            "Sunset Blaze":   ["#1a0505", "#cc2200", "#ff8800", "#ffee44"],
            "Arctic Aurora":  ["#050a14", "#0033aa", "#00ddaa", "#aaffee"],
            "Monochrome":     ["#111111", "#444444", "#aaaaaa", "#ffffff"],
            "Lava Flow":      ["#1a0000", "#aa1100", "#ff4400", "#ffcc00"],
        }
        cols = PALETTES.get(palette, PALETTES["Ocean Depths"])
        cmap = LinearSegmentedColormap.from_list(
            "sph", [cols[0], cols[1], cols[2], cols[3]], N=256)
        rng = np.random.default_rng(int(seed))
        N = max(50, int(n_particles))
        steps = max(10, int(n_steps))
        g_val = float(gravity)
        mu = float(viscosity)
        rho0 = float(rest_density)
        k = float(gas_const)
        # SPH parameters
        h = 0.04  # smoothing radius
        mass = 1.0
        dt = 0.0008
        # Initialize: block of fluid in upper-left quadrant
        side = int(np.ceil(np.sqrt(N)))
        spacing = 0.015
        pos = []
        for i in range(side):
            for j in range(side):
                if len(pos) >= N:
                    break
                pos.append([0.15 + i * spacing + rng.uniform(-0.001, 0.001),
                            0.5 + j * spacing + rng.uniform(-0.001, 0.001)])
        pos = np.array(pos[:N])
        vel = np.zeros((N, 2))
        # SPH kernels (poly6 for density, spiky for pressure, viscosity)
        h2 = h * h
        poly6_coeff = 315.0 / (64.0 * np.pi * h**9)
        spiky_coeff = -45.0 / (np.pi * h**6)
        visc_coeff  = 45.0 / (np.pi * h**6)
        for step in range(steps):
            # Compute densities
            diff = pos[:, None, :] - pos[None, :, :]  # (N, N, 2)
            r2 = (diff**2).sum(axis=2)  # (N, N)
            mask = r2 < h2
            density = mass * poly6_coeff * np.where(mask, (h2 - r2)**3, 0.0).sum(axis=1)
            density = np.maximum(density, rho0 * 0.1)
            # Pressure
            pressure = k * (density - rho0)
            # Forces
            r_dist = np.sqrt(r2 + 1e-12)
            # Per-particle force computation
            force = np.zeros((N, 2))
            for i in range(N):
                neighbours = np.where(mask[i] & (r_dist[i] > 1e-6))[0]
                if len(neighbours) == 0:
                    continue
                rij = diff[i, neighbours]  # (K, 2)
                dij = r_dist[i, neighbours]  # (K,)
                # Pressure force (spiky gradient)
                p_avg = (pressure[i] + pressure[neighbours]) / (2.0 * density[neighbours])
                w_spiky = spiky_coeff * (h - dij)**2
                f_p = (p_avg * w_spiky)[:, None] * (rij / dij[:, None])
                force[i] += mass * f_p.sum(axis=0)
                # Viscosity force
                v_diff = vel[neighbours] - vel[i]
                w_visc = visc_coeff * (h - dij)
                f_v = mu * mass * (v_diff * w_visc[:, None]) / density[neighbours, None]
                force[i] += f_v.sum(axis=0)
            # Gravity
            force[:, 1] -= g_val * density
            # Integration (symplectic Euler)
            vel += dt * force / density[:, None]
            pos += dt * vel
            # Boundary conditions (box: [0,1] x [0,1])
            for dim in range(2):
                below = pos[:, dim] < 0.02
                above = pos[:, dim] > 0.98
                pos[below, dim] = 0.02
                pos[above, dim] = 0.98
                vel[below, dim] *= -0.3
                vel[above, dim] *= -0.3
        # Visualization
        fig, ax = plt.subplots(figsize=(8, 8), facecolor=cols[0])
        ax.set_facecolor(cols[0])
        ax.set_aspect("equal")
        # Color by density
        rho_norm = (density - density.min()) / (density.max() - density.min() + 1e-9)
        speed_val = np.linalg.norm(vel, axis=1)
        color_val = 0.6 * rho_norm + 0.4 * speed_val / (speed_val.max() + 1e-9)
        ax.scatter(pos[:, 0], pos[:, 1], c=color_val, cmap=cmap,
                   s=35, alpha=0.85, linewidths=0, vmin=0, vmax=1, zorder=3)
        # Draw container
        rect = plt.Rectangle((0.02, 0.02), 0.96, 0.96, fill=False,
                              edgecolor=cols[2], linewidth=1.5, zorder=5)
        ax.add_patch(rect)
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        ax.set_xticks([]); ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_edgecolor(cols[1])
        ax.set_title(
            f"Fluid Dynamics (SPH)  |  N={N}  |  {steps} steps  |  "
            f"g={g_val:.1f}  μ={mu:.3f}  k={k:.0f}",
            color=cols[3], fontsize=10, fontweight="bold", pad=8)
        plt.tight_layout()
        self._fig = fig
        plt.show()
        plt.close(fig)

    def get_controls(self):
        import ipywidgets as w
        return [
            w.IntSlider(value=300, min=50, max=600, step=50,          description="n_particles"),
            w.IntSlider(value=60,  min=10, max=150, step=10,          description="n_steps"),
            w.FloatSlider(value=9.8, min=0.0, max=20.0, step=0.5,    description="gravity"),
            w.FloatSlider(value=0.02, min=0.0, max=0.1, step=0.005,  description="viscosity"),
            w.FloatSlider(value=1000.0, min=100, max=3000, step=100,  description="rest_density"),
            w.FloatSlider(value=2000.0, min=500, max=5000, step=250,  description="gas_const"),
            w.IntSlider(value=7, min=0, max=999, step=1,              description="seed"),
        ]

    def animate(self, n_frames=40, fps=10, palette="Ocean Depths",
                n_particles=200, gravity=9.8, viscosity=0.02,
                rest_density=1000.0, gas_const=2000.0, seed=7, **kwargs):
        from matplotlib.colors import LinearSegmentedColormap
        from engines.animation import capture_frame
        cols = ["#0a1628", "#0066cc", "#00ccff", "#80ffee"]
        cmap = LinearSegmentedColormap.from_list("sph", cols, N=256)
        rng = np.random.default_rng(int(seed))
        N = max(50, int(n_particles))
        g_val, mu, rho0, k = float(gravity), float(viscosity), float(rest_density), float(gas_const)
        h, mass, dt = 0.04, 1.0, 0.0008
        h2 = h * h
        poly6_c = 315.0 / (64.0 * np.pi * h**9)
        spiky_c = -45.0 / (np.pi * h**6)
        visc_c  = 45.0 / (np.pi * h**6)
        side = int(np.ceil(np.sqrt(N)))
        spacing = 0.015
        pos = []
        for i in range(side):
            for j in range(side):
                if len(pos) >= N: break
                pos.append([0.15+i*spacing+rng.uniform(-0.001,0.001), 0.5+j*spacing+rng.uniform(-0.001,0.001)])
        pos = np.array(pos[:N])
        vel = np.zeros((N, 2))
        frames = []
        total_steps = n_frames * 3
        for step in range(total_steps):
            diff = pos[:, None, :] - pos[None, :, :]
            r2 = (diff**2).sum(axis=2)
            mask = r2 < h2
            density = mass * poly6_c * np.where(mask, (h2 - r2)**3, 0.0).sum(axis=1)
            density = np.maximum(density, rho0 * 0.1)
            pressure = k * (density - rho0)
            r_dist = np.sqrt(r2 + 1e-12)
            force = np.zeros((N, 2))
            for i in range(N):
                nb = np.where(mask[i] & (r_dist[i] > 1e-6))[0]
                if len(nb) == 0: continue
                rij, dij = diff[i, nb], r_dist[i, nb]
                p_avg = (pressure[i] + pressure[nb]) / (2.0 * density[nb])
                force[i] += mass * (p_avg * spiky_c * (h - dij)**2)[:, None] * (rij / dij[:, None])
                force[i] += (mu * mass * ((vel[nb] - vel[i]) * visc_c * (h - dij)[:, None]) / density[nb, None]).sum(axis=0)
            force[:, 1] -= g_val * density
            vel += dt * force / density[:, None]
            pos += dt * vel
            for dim in range(2):
                below, above = pos[:, dim] < 0.02, pos[:, dim] > 0.98
                pos[below, dim] = 0.02; pos[above, dim] = 0.98
                vel[below, dim] *= -0.3; vel[above, dim] *= -0.3
            if step % 3 == 0:
                rho_n = (density - density.min()) / (density.max() - density.min() + 1e-9)
                spd = np.linalg.norm(vel, axis=1)
                cv = 0.6 * rho_n + 0.4 * spd / (spd.max() + 1e-9)
                fig, ax = plt.subplots(figsize=(6, 6), facecolor=cols[0])
                ax.set_facecolor(cols[0]); ax.set_aspect("equal")
                ax.scatter(pos[:,0], pos[:,1], c=cv, cmap=cmap, s=25, alpha=0.85, linewidths=0, vmin=0, vmax=1)
                ax.add_patch(plt.Rectangle((0.02,0.02), 0.96, 0.96, fill=False, edgecolor=cols[2], linewidth=1.2))
                ax.set_xlim(0,1); ax.set_ylim(0,1); ax.set_xticks([]); ax.set_yticks([])
                ax.set_title(f"SPH Fluid | step {step+1}", color=cols[3], fontsize=9, pad=4)
                plt.tight_layout()
                frames.append(capture_frame(fig))
                plt.close(fig)
        return frames


class QuantumWaveRenderer(BasePattern):
    """100 — Quantum Wave Packet (Split-Step Fourier Method)"""
    name  = "Quantum Wave Packet"
    group = "Scientific & Simulation"

    def render(self, resolution="Low", palette="Neon Cyberpunk", speed=1.0,
               x0=-3.0, k0=5.0, sigma=0.5, n_steps=200,
               potential="barrier", barrier_height=8.0, seed=0, **kwargs):
        from matplotlib.colors import LinearSegmentedColormap
        PALETTES = {
            "Inferno":        ["#200060", "#8b0aff", "#ff6b35", "#ffe04b"],
            "Ocean Depths":   ["#0a1628", "#0066cc", "#00ccff", "#80ffee"],
            "Neon Cyberpunk": ["#0d0221", "#ff006e", "#00f5d4", "#f9c80e"],
            "Forest":         ["#1a2e1a", "#2d6a2d", "#52b252", "#b8f0b8"],
            "Sunset Blaze":   ["#1a0505", "#cc2200", "#ff8800", "#ffee44"],
            "Arctic Aurora":  ["#050a14", "#0033aa", "#00ddaa", "#aaffee"],
            "Monochrome":     ["#111111", "#444444", "#aaaaaa", "#ffffff"],
            "Lava Flow":      ["#1a0000", "#aa1100", "#ff4400", "#ffcc00"],
        }
        cols = PALETTES.get(palette, PALETTES["Neon Cyberpunk"])
        cmap = LinearSegmentedColormap.from_list(
            "qm", [cols[0], cols[1], cols[2], cols[3]], N=256)
        # Grid setup
        Nx = {"Low": 512, "Medium": 1024, "High": 2048}.get(resolution, 512)
        L = 12.0  # domain half-width
        x = np.linspace(-L, L, Nx)
        dx = x[1] - x[0]
        dk = 2 * np.pi / (Nx * dx)
        k_arr = np.fft.fftfreq(Nx, d=dx) * 2 * np.pi
        # Time step
        dt = 0.005
        steps = max(10, int(n_steps))
        # Initial Gaussian wave packet
        x_0 = float(x0)
        k_0 = float(k0)
        sig = float(sigma)
        psi = (2 * np.pi * sig**2)**(-0.25) * np.exp(
            -(x - x_0)**2 / (4 * sig**2) + 1j * k_0 * x)
        # Potential
        pot_type = str(potential).lower()
        V_height = float(barrier_height)
        if pot_type == "barrier":
            V = np.where((x > 0) & (x < 0.5), V_height, 0.0)
        elif pot_type == "well":
            V = np.where((x > -1) & (x < 1), -V_height, 0.0)
        elif pot_type == "harmonic":
            V = 0.5 * V_height * x**2 / L**2
        else:
            V = np.where((x > 0) & (x < 0.5), V_height, 0.0)
        # Split-step operators
        exp_V_half = np.exp(-0.5j * V * dt)
        exp_T = np.exp(-0.5j * k_arr**2 * dt)  # ħ=1, m=1
        # Store snapshots for space-time plot
        n_snapshots = min(steps, 100)
        snap_interval = max(1, steps // n_snapshots)
        snapshots = []
        psi_init = np.abs(psi)**2
        for step in range(steps):
            # Split-step Fourier
            psi = exp_V_half * psi
            psi = np.fft.ifft(exp_T * np.fft.fft(psi))
            psi = exp_V_half * psi
            if step % snap_interval == 0:
                snapshots.append(np.abs(psi)**2)
        snapshots.append(np.abs(psi)**2)
        # Build space-time image
        st_image = np.array(snapshots)  # (T, Nx)
        # Visualization
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), facecolor=cols[0],
                                        gridspec_kw={'height_ratios': [1, 1.5]})
        for ax in (ax1, ax2):
            ax.set_facecolor(cols[0])
            ax.tick_params(colors=cols[2])
            for spine in ax.spines.values():
                spine.set_edgecolor(cols[1])
        # Top: final |ψ|² with potential overlay
        prob = np.abs(psi)**2
        ax1.fill_between(x, 0, prob, color=cols[2], alpha=0.6)
        ax1.plot(x, prob, color=cols[3], linewidth=1.5, label=r"$|\psi|^2$ (final)")
        ax1.plot(x, psi_init, color=cols[1], linewidth=1.0, alpha=0.5,
                 linestyle='--', label=r"$|\psi|^2$ (initial)")
        # Scale potential for display
        v_scale = prob.max() / (V.max() + 1e-9) * 0.4 if V.max() > 0 else 0
        ax1.fill_between(x, 0, V * v_scale, color=cols[1], alpha=0.3, label="V(x)")
        ax1.set_xlim(-L, L)
        ax1.set_ylim(0, prob.max() * 1.3)
        ax1.set_xlabel("x", color=cols[2], fontsize=9)
        ax1.set_ylabel(r"$|\psi(x)|^2$", color=cols[2], fontsize=9)
        ax1.legend(loc="upper right", fontsize=8, framealpha=0.5, labelcolor=cols[3])
        ax1.set_title("Quantum Wave Packet — Probability Density",
                      color=cols[3], fontsize=10, fontweight="bold")
        # Bottom: space-time diagram
        extent = [-L, L, steps * dt, 0]
        ax2.imshow(st_image, aspect='auto', extent=extent, cmap=cmap,
                   interpolation='bilinear', vmin=0, vmax=st_image.max())
        ax2.set_xlabel("x", color=cols[2], fontsize=9)
        ax2.set_ylabel("Time", color=cols[2], fontsize=9)
        ax2.set_title("Space-Time Evolution", color=cols[3], fontsize=10, fontweight="bold")
        fig.suptitle(
            f"Quantum Wave Packet  |  k₀={k_0:.1f}  σ={sig:.2f}  "
            f"V={pot_type}  h={V_height:.1f}  |  {steps} steps",
            color=cols[3], fontsize=11, fontweight="bold", y=0.99)
        plt.tight_layout()
        self._fig = fig
        plt.show()
        plt.close(fig)

    def get_controls(self):
        import ipywidgets as w
        return [
            w.FloatSlider(value=-3.0, min=-8.0, max=0.0, step=0.5,   description="x0"),
            w.FloatSlider(value=5.0,  min=1.0,  max=15.0, step=0.5,  description="k0"),
            w.FloatSlider(value=0.5,  min=0.2,  max=2.0, step=0.1,   description="sigma"),
            w.IntSlider(value=200, min=50, max=500, step=25,          description="n_steps"),
            w.Dropdown(options=["barrier","well","harmonic"],
                       value="barrier", description="potential"),
            w.FloatSlider(value=8.0, min=1.0, max=20.0, step=1.0,    description="barrier_height"),
        ]

    def animate(self, n_frames=50, fps=15, palette="Neon Cyberpunk",
                x0=-3.0, k0=5.0, sigma=0.5, potential="barrier",
                barrier_height=8.0, **kwargs):
        from matplotlib.colors import LinearSegmentedColormap
        from engines.animation import capture_frame
        cols = ["#0d0221", "#ff006e", "#00f5d4", "#f9c80e"]
        Nx = 512
        L = 12.0
        x = np.linspace(-L, L, Nx)
        dx = x[1] - x[0]
        k_arr = np.fft.fftfreq(Nx, d=dx) * 2 * np.pi
        dt = 0.005
        steps = n_frames * 4
        x_0, k_0, sig = float(x0), float(k0), float(sigma)
        V_height = float(barrier_height)
        psi = (2*np.pi*sig**2)**(-0.25) * np.exp(-(x-x_0)**2/(4*sig**2) + 1j*k_0*x)
        pot_type = str(potential).lower()
        if pot_type == "barrier":
            V = np.where((x > 0) & (x < 0.5), V_height, 0.0)
        elif pot_type == "well":
            V = np.where((x > -1) & (x < 1), -V_height, 0.0)
        elif pot_type == "harmonic":
            V = 0.5 * V_height * x**2 / L**2
        else:
            V = np.where((x > 0) & (x < 0.5), V_height, 0.0)
        exp_V_half = np.exp(-0.5j * V * dt)
        exp_T = np.exp(-0.5j * k_arr**2 * dt)
        psi_init = np.abs(psi)**2
        v_max_display = psi_init.max() * 1.5
        v_scale = v_max_display / (V.max() + 1e-9) * 0.3 if V.max() > 0 else 0
        frames = []
        for step in range(steps):
            psi = exp_V_half * psi
            psi = np.fft.ifft(exp_T * np.fft.fft(psi))
            psi = exp_V_half * psi
            if step % 4 == 0:
                prob = np.abs(psi)**2
                fig, ax = plt.subplots(figsize=(8, 4), facecolor=cols[0])
                ax.set_facecolor(cols[0])
                ax.fill_between(x, 0, V * v_scale, color=cols[1], alpha=0.25)
                ax.fill_between(x, 0, prob, color=cols[2], alpha=0.5)
                ax.plot(x, prob, color=cols[3], linewidth=1.5)
                ax.set_xlim(-L, L); ax.set_ylim(0, v_max_display)
                ax.set_xticks([]); ax.set_yticks([])
                ax.set_title(f"Quantum Wave Packet | t={step*dt:.3f}", color=cols[3], fontsize=9, pad=4)
                plt.tight_layout()
                frames.append(capture_frame(fig))
                plt.close(fig)
        return frames
