"""
Scientific & Simulation Patterns (91–100)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
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

# ─────────────────────────────────────────────────────────────────────────────────
# Remaining stubs
# ─────────────────────────────────────────────────────────────────────────────────
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
        ax.text(0.5, 0.42, "Coming Soon", ha="center", va="center",
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

class TrafficFlowRenderer(_StubMixin, BasePattern):
    name = "Traffic Flow Simulation"
    group = "Scientific & Simulation"

class EcosystemRenderer(_StubMixin, BasePattern):
    name = "Ecosystem Predator-Prey"
    group = "Scientific & Simulation"

class AntColonyRenderer(_StubMixin, BasePattern):
    name = "Ant Colony Optimization"
    group = "Scientific & Simulation"

class FluidDynamicsRenderer(_StubMixin, BasePattern):
    name = "Fluid Dynamics (SPH)"
    group = "Scientific & Simulation"

class QuantumWaveRenderer(_StubMixin, BasePattern):
    name = "Quantum Wave Packet"
    group = "Scientific & Simulation"
