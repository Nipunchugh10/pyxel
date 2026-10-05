"""
Scientific & Simulation Patterns (91–100)
"""

import matplotlib.pyplot as plt
import numpy as np
from engines.renderer import BasePattern
from engines.color_utils import ColorUtils


# ─────────────────────────────────────────────────────────────────────────────────
# 91 — Neural Network Visualization
# ─────────────────────────────────────────────────────────────────────────────────
def _nn_layout(layer_sizes):
    """Parse "4,6,2"-style sizes; return (layers, x_positions, node_pos, node_r)."""
    try:
        layers = [max(1, int(x.strip())) for x in str(layer_sizes).split(",")]
    except ValueError:
        layers = [4, 6, 6, 4, 2]
    layers = layers[:8]
    x_positions = np.linspace(0.1, 0.9, len(layers))
    max_nodes = max(layers)
    gap = min(0.07, 0.8 / max(max_nodes - 1, 1))   # keep tall layers on canvas
    node_pos = [np.column_stack([np.full(n, xp),
                                 np.linspace(0.5 - (n-1)*gap, 0.5 + (n-1)*gap, n)])
                for xp, n in zip(x_positions, layers)]
    node_r = max(0.012, min(0.018, 0.6 / (max_nodes * 8)))
    return layers, x_positions, node_pos, node_r


def _weight_color(cmap_act, w, alpha):
    c = cmap_act(0.3 + 0.5 * w) if w >= 0 else plt.cm.cool(0.3 - 0.3 * w)
    return (*c[:3], alpha)


class NeuralNetworkVizRenderer(BasePattern):
    """91 — Neural Network Visualization"""
    name  = "Neural Network Visualization"
    group = "Scientific & Simulation"

    def render(self, resolution="Low", palette="Neon Cyberpunk", speed=1.0,
               layer_sizes="4,6,6,4,2", show_weights=True, activation_seed=42, **kwargs):
        from matplotlib.colors import LinearSegmentedColormap
        from matplotlib.collections import LineCollection
        cols = ColorUtils.accent_colors(palette, "Neon Cyberpunk")
        cmap_act = LinearSegmentedColormap.from_list("act", cols, N=256)
        layers, x_positions, node_pos, node_r = _nn_layout(layer_sizes)
        n_layers = len(layers)
        rng = np.random.default_rng(int(activation_seed))
        node_act = [rng.uniform(0.05, 0.95, n) for n in layers]
        fig, ax = plt.subplots(figsize=(10, 7), facecolor="#07050f")
        ax.set_facecolor("#07050f")
        ax.set_aspect("equal")
        ax.axis("off")
        if show_weights:
            for li in range(n_layers - 1):
                segs, colors_w = [], []
                for (px, py) in node_pos[li]:
                    for (qx, qy) in node_pos[li + 1]:
                        w = rng.uniform(-1.0, 1.0)
                        segs.append([(px, py), (qx, qy)])
                        colors_w.append(_weight_color(cmap_act, w, abs(w)*0.55 + 0.05))
                ax.add_collection(LineCollection(segs, colors=colors_w,
                                                 linewidths=0.7, zorder=1))
        for positions, activations in zip(node_pos, node_act):
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
        for xp, lbl in zip(x_positions, layer_labels):
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

    def animate(self, n_frames=30, fps=6, palette="Neon Cyberpunk",
                layer_sizes="4,6,6,4,2", activation_seed=42, **kwargs):
        """Animate activation signal propagating through layers."""
        from matplotlib.colors import LinearSegmentedColormap
        from matplotlib.collections import LineCollection
        from engines.animation import capture_frame
        cols = ColorUtils.accent_colors(palette, "Neon Cyberpunk")
        cmap_act = LinearSegmentedColormap.from_list("act", cols, N=256)
        layers, _, node_pos, node_r = _nn_layout(layer_sizes)
        n_layers = len(layers)
        rng = np.random.default_rng(int(activation_seed))
        all_acts = [[rng.uniform(0.05, 0.95, n) for n in layers] for _ in range(n_frames)]
        weights = [rng.uniform(-1.0, 1.0, (layers[li], layers[li+1]))
                   for li in range(n_layers - 1)]
        fig, ax = plt.subplots(figsize=(8, 6), facecolor="#07050f")
        ax.set_facecolor("#07050f"); ax.set_aspect("equal"); ax.axis("off")
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        edge_sets = []
        for li in range(n_layers - 1):
            segs = [[tuple(p), tuple(q)] for p in node_pos[li] for q in node_pos[li+1]]
            lc = LineCollection(segs, linewidths=0.7, zorder=1)
            ax.add_collection(lc)
            edge_sets.append(lc)
        halos, cores = [], []
        for positions in node_pos:
            halos.append([ax.add_patch(plt.Circle(tuple(p), node_r*2.2, zorder=2)) for p in positions])
            cores.append([ax.add_patch(plt.Circle(tuple(p), node_r, zorder=3)) for p in positions])
        title = ax.set_title("", color=cols[3], fontsize=9, pad=4)
        fig.tight_layout()
        frames = []
        for f_idx in range(n_frames):
            active_layer = f_idx % n_layers           # layer the signal has reached
            for li, lc in enumerate(edge_sets):
                bright = 1.0 if li == active_layer else 0.3
                lc.set_color([_weight_color(cmap_act, w, abs(w) * 0.55 * bright + 0.05)
                              for w in weights[li].ravel()])
            for li, activations in enumerate(all_acts[f_idx]):
                glow = 1.0 if li <= active_layer else 0.15
                for halo, core, act in zip(halos[li], cores[li], activations):
                    halo.set_color(cmap_act(act * glow)); halo.set_alpha(0.12 * glow)
                    core.set_color(cmap_act(act * glow)); core.set_alpha(glow)
            title.set_text(f"Neural Network | signal at layer {active_layer+1}/{n_layers}")
            frames.append(capture_frame(fig))
        plt.close(fig)
        return frames


# ─────────────────────────────────────────────────────────────────────────────────
# 92 — Atom Orbital Simulator
# ─────────────────────────────────────────────────────────────────────────────────
def _real_spherical_harmonic(l, m, theta, phi):
    """Real spherical harmonic Y_lm at polar angle `theta` and azimuth `phi`.

    SciPy >= 1.15 provides sph_harm_y(l, m, theta, phi); older releases only
    have sph_harm(m, l, phi, theta) (removed in 1.17).
    """
    try:
        from scipy.special import sph_harm_y
        Y = sph_harm_y(l, abs(m), theta, phi)
    except ImportError:
        from scipy.special import sph_harm
        Y = sph_harm(abs(m), l, phi, theta)
    return np.real(Y) if m >= 0 else np.imag(Y)


def _orbital_density(n, l, m, view_plane, grid):
    """Normalised hydrogen |psi_nlm|^2 on a plane slice; returns (psi2, half-width)."""
    from scipy.special import assoc_laguerre
    lim = 20 * n
    ax_vals = np.linspace(-lim, lim, grid)
    A, B = np.meshgrid(ax_vals, ax_vals)
    zero = np.zeros_like(A)
    X, Y, Z = {"xy": (A, B, zero), "yz": (zero, A, B)}.get(view_plane, (A, zero, B))
    r = np.sqrt(X**2 + Y**2 + Z**2) + 1e-12
    theta = np.arccos(np.clip(Z / r, -1, 1))
    phi = np.arctan2(Y, X)
    rho = 2 * r / n
    R = np.exp(-rho / 2) * rho**l * assoc_laguerre(rho, n - l - 1, 2 * l + 1)
    psi2 = (R * _real_spherical_harmonic(l, m, theta, phi))**2
    pmax = psi2.max()
    # A plane lying in a nodal plane leaves only float noise (~1e-33): show it as empty
    return (psi2 / pmax if pmax > 1e-20 else np.zeros_like(psi2)), lim


class AtomOrbitalRenderer(BasePattern):
    """92 — Atom Orbital Simulator"""
    name  = "Atom Orbital Simulator"
    group = "Scientific & Simulation"

    def render(self, resolution="Low", palette="Ocean Depths", speed=1.0,
               n_qn=2, l_qn=1, m_qn=0, view_plane="xz", **kwargs):
        from matplotlib.colors import LinearSegmentedColormap
        cols = ColorUtils.accent_colors(palette, "Ocean Depths")
        cmap = LinearSegmentedColormap.from_list("orb", cols, N=512)
        n = max(1, min(4, int(n_qn)))
        l = max(0, min(n-1, int(l_qn)))
        m = max(-l, min(l, int(m_qn)))
        G = {"Low": 120, "Medium": 200, "High": 320}.get(resolution, 120)
        vp = str(view_plane).lower()
        psi2, lim = _orbital_density(n, l, m, vp, G)
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

    def animate(self, n_frames=30, fps=4, palette="Ocean Depths",
                view_plane="xz", **kwargs):
        """Animate by cycling through all valid (n, l, m) quantum states."""
        from matplotlib.colors import LinearSegmentedColormap
        from engines.animation import capture_frame
        cols = ColorUtils.accent_colors(palette, "Ocean Depths")
        cmap = LinearSegmentedColormap.from_list("orb", cols, N=512)
        states = [(n, l, m) for n in range(1, 5) for l in range(n) for m in range(-l, l+1)]
        states = (states * (n_frames // len(states) + 1))[:n_frames]
        vp = str(view_plane).lower()
        fig, ax = plt.subplots(figsize=(6, 6), facecolor="#050a14")
        ax.set_facecolor("#050a14")
        ax.set_xticks([]); ax.set_yticks([])
        im = ax.imshow(np.zeros((2, 2)), origin="lower", cmap=cmap,
                       interpolation="bilinear", vmin=0, vmax=1)
        title = ax.set_title("", color=cols[3], fontsize=10, fontweight="bold", pad=4)
        fig.tight_layout()
        frames = []
        for n, l, m in states:
            psi2, lim = _orbital_density(n, l, m, vp, 100)
            im.set_data(psi2)
            im.set_extent([-lim, lim, -lim, lim])
            title.set_text(f"n={n}  l={l}  m={m}  |  {vp.upper()} plane")
            frames.append(capture_frame(fig))
        plt.close(fig)
        return frames

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
        cols     = ColorUtils.accent_colors(palette, "Inferno")
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
        r_disk  = np.linspace(r_isco, 11*M, 120)   # ISCO (6M) out to the view edge
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

    def animate(self, n_frames=36, fps=12, palette="Inferno",
                mass=1.0, n_rings=5, n_stars=300, star_seed=7, **kwargs):
        """Animate the accretion disk rotating around the black hole."""
        from matplotlib.colors import LinearSegmentedColormap
        from engines.animation import capture_frame
        cmap_acc = LinearSegmentedColormap.from_list(
            "acc", ["#000000", "#200010", "#aa2200", "#ff8800", "#ffffa0"], N=512)
        cols = ColorUtils.accent_colors(palette, "Inferno")
        rng = np.random.default_rng(int(star_seed))
        M = max(0.1, float(mass))
        rs = 2 * M
        view = 12 * M
        # Pre-generate stars
        sx = rng.uniform(-view, view, n_stars)
        sy = rng.uniform(-view, view, n_stars)
        visible = np.sqrt(sx**2 + sy**2) > rs * 1.1
        sx, sy = sx[visible], sy[visible]
        s_sizes = rng.uniform(1, 8, len(sx))
        s_bright = rng.uniform(0.3, 1.0, len(sx))
        # Pre-generate accretion disk (polar coords)
        r_isco = 3 * rs
        r_disk = np.linspace(r_isco, 11*M, 80)
        phi_acc = np.linspace(0, 2*np.pi, 300)
        R_acc, Phi_acc = np.meshgrid(r_disk, phi_acc)
        base_brightness = (r_isco / R_acc)**2.5
        base_brightness /= base_brightness.max()
        # Source rings
        theta_vals = np.linspace(0, 2*np.pi, 400)
        source_radii = np.linspace(3.5*M, 10*M, n_rings)
        fig, ax = plt.subplots(figsize=(6, 6), facecolor="#000000")
        ax.set_facecolor("#000000"); ax.set_aspect("equal"); ax.axis("off")
        ax.scatter(sx, sy, s=s_sizes, c=s_bright, cmap="gray",
                   alpha=0.7, zorder=1, linewidths=0)
        for ri, r_src in enumerate(source_radii):
            r_app = r_src / (1 + 4*M/r_src)
            hue = ri / max(n_rings-1, 1)
            ax.plot(r_app*np.cos(theta_vals), r_app*np.sin(theta_vals),
                    color=plt.cm.hsv(hue), linewidth=max(0.5, 1.5-ri*0.15),
                    alpha=0.7, zorder=3)
        disk = ax.scatter(np.zeros(R_acc.size), np.zeros(R_acc.size),
                          c=np.zeros(R_acc.size), cmap=cmap_acc,
                          s=0.6, alpha=0.6, zorder=2, linewidths=0, vmin=0, vmax=1)
        ax.add_patch(plt.Circle((0, 0), rs, color="black", zorder=5))
        ax.add_patch(plt.Circle((0, 0), 1.5*rs, fill=False,
                                edgecolor="#ff8800", linewidth=0.8,
                                linestyle="--", alpha=0.4, zorder=6))
        ax.set_xlim(-view, view); ax.set_ylim(-view, view)
        title = ax.set_title("", color=cols[3], fontsize=9, pad=4)
        fig.tight_layout()
        frames = []
        for f in range(n_frames):
            rotation = 2 * np.pi * f / n_frames
            Phi_rot = Phi_acc + rotation
            # Angular brightness variation makes the rotation visible
            bright = base_brightness * (0.7 + 0.3 * np.cos(Phi_rot * 3 + rotation * 2))
            disk.set_offsets(np.column_stack([(R_acc * np.cos(Phi_rot)).ravel(),
                                              (R_acc * np.sin(Phi_rot)).ravel()]))
            disk.set_array(bright.ravel())
            title.set_text(f"Black Hole Lensing | frame {f+1}/{n_frames}")
            frames.append(capture_frame(fig))
        plt.close(fig)
        return frames

# ─────────────────────────────────────────────────────────────────────────────────
# 94 — Conway's Game of Life
# ─────────────────────────────────────────────────────────────────────────────────
_GOSPER_GUN = [(5,1),(5,2),(6,1),(6,2),(5,11),(6,11),(7,11),(4,12),(8,12),
               (3,13),(9,13),(3,14),(9,14),(6,15),(4,16),(8,16),(5,17),(6,17),
               (7,17),(6,18),(3,21),(4,21),(5,21),(3,22),(4,22),(5,22),(2,23),
               (6,23),(1,25),(2,25),(6,25),(7,25),(3,35),(4,35),(3,36),(4,36)]


def _life_initial(start_pattern, G, density, seed):
    """Initial G x G Game of Life grid for a named start pattern."""
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
    elif pat == "gosper_gun":
        oy, ox = G//4, G//4
        for dy, dx in _GOSPER_GUN:
            if 0 <= oy+dy < G and 0 <= ox+dx < G:
                grid[oy+dy, ox+dx] = 1
    else:
        rng = np.random.default_rng(int(seed))
        grid = (rng.uniform(0, 1, (G, G)) < float(density)).astype(np.int8)
    return grid


def _life_step(grid, age):
    """One B3/S23 generation on a torus; returns (grid, age)."""
    from scipy.ndimage import convolve
    kernel = np.ones((3, 3), dtype=np.int8); kernel[1, 1] = 0
    nbrs = convolve(grid, kernel, mode="wrap")
    new_grid = ((grid==0)&(nbrs==3) | (grid==1)&((nbrs==2)|(nbrs==3))).astype(np.int8)
    return new_grid, np.where(new_grid==1, age+1, 0.0)


def _life_display(grid, age):
    return np.where(grid==1, np.log1p(age)/(np.log1p(age.max())+1e-9), 0.0)


class GameOfLifeRenderer(BasePattern):
    """94 — Conway's Game of Life"""
    name  = "Conway's Game of Life"
    group = "Scientific & Simulation"

    def render(self, resolution="Low", palette="Neon Cyberpunk", speed=1.0,
               n_gens=60, start_pattern="random", density=0.30, seed=0, **kwargs):
        from matplotlib.colors import LinearSegmentedColormap
        cols = ColorUtils.accent_colors(palette, "Neon Cyberpunk")
        cmap = LinearSegmentedColormap.from_list(
            "gol", ["#000000", cols[1], cols[2], cols[3]], N=256)
        G   = {"Low": 80, "Medium": 120, "High": 160}.get(resolution, 80)
        grid = _life_initial(start_pattern, G, density, seed)
        age = grid.astype(np.float32)
        for _ in range(int(n_gens)):
            grid, age = _life_step(grid, age)
        fig, ax = plt.subplots(figsize=(8, 8), facecolor="#000000")
        ax.set_facecolor("#000000")
        ax.imshow(_life_display(grid, age), origin="lower", cmap=cmap,
                  interpolation="nearest", vmin=0, vmax=1)
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
        from matplotlib.colors import LinearSegmentedColormap
        from engines.animation import capture_frame
        cols = ColorUtils.accent_colors(palette, "Neon Cyberpunk")
        cmap = LinearSegmentedColormap.from_list("gol", ["#000000", cols[1], cols[2], cols[3]], N=256)
        G = {"Low": 80, "Medium": 120, "High": 160}.get(resolution, 80)
        grid = _life_initial(start_pattern, G, density, seed)
        age = grid.astype(np.float32)
        fig, ax = plt.subplots(figsize=(6, 6), facecolor="#000000")
        ax.set_facecolor("#000000")
        ax.set_xticks([]); ax.set_yticks([])
        im = ax.imshow(np.zeros((G, G)), origin="lower", cmap=cmap,
                       interpolation="nearest", vmin=0, vmax=1)
        title = ax.set_title("", color=cols[3], fontsize=9, pad=4)
        fig.tight_layout()
        frames = []
        for gen in range(n_frames * 2):
            grid, age = _life_step(grid, age)
            if gen % 2 == 0:
                im.set_data(_life_display(grid, age))
                title.set_text(f"Game of Life | gen {gen+1}")
                frames.append(capture_frame(fig))
        plt.close(fig)
        return frames


# ─────────────────────────────────────────────────────────────────────────────────
# 95 — Boids Flocking Simulation
# ─────────────────────────────────────────────────────────────────────────────────
def _boids_init(n, seed):
    rng = np.random.default_rng(int(seed))
    return rng.uniform(0.1, 0.9, (n, 2)), rng.uniform(-0.005, 0.005, (n, 2))


def _boids_step(pos, vel, sep_w, ali_w, coh_w, r_sep=0.06, r_vis=0.18,
                max_speed=0.010, min_speed=0.003):
    """One Reynolds boids update on the unit torus; returns (pos, vel)."""
    # offset[i, j] points from boid j to boid i, wrapped to the nearest image
    offset = pos[:, None, :] - pos[None, :, :]
    offset -= np.round(offset)
    dist = np.linalg.norm(offset, axis=2)
    np.fill_diagonal(dist, np.inf)
    in_vis = dist < r_vis
    in_sep = dist < r_sep
    cnt = in_vis.sum(axis=1, keepdims=True).clip(1, None)
    # Separation: push away from close neighbours, stronger when closer
    sep = (np.where(in_sep[:, :, None], offset, 0.0)
           / np.maximum(dist, 1e-9)[:, :, None]**2).sum(axis=1)
    # Alignment: steer toward the neighbours' mean velocity
    ali = (vel[None, :, :] * in_vis[:, :, None]).sum(axis=1) / cnt - vel
    # Cohesion: steer toward the neighbours' centre (mean of wrapped offsets)
    coh = (-offset * in_vis[:, :, None]).sum(axis=1) / cnt
    accel = sep_w * sep * 1e-4 + ali_w * ali + coh_w * coh * 0.05
    vel = vel + accel * 0.05
    spd = np.linalg.norm(vel, axis=1, keepdims=True).clip(1e-12, None)
    vel = vel / spd * np.clip(spd, min_speed, max_speed)
    return (pos + vel) % 1.0, vel


class BoidsFlockingRenderer(BasePattern):
    """95 — Boids Flocking Simulation"""
    name  = "Boids Flocking Simulation"
    group = "Scientific & Simulation"

    def render(self, resolution="Low", palette="Arctic Aurora", speed=1.0,
               n_boids=120, n_steps=80, sep_weight=1.6, align_weight=1.0,
               coh_weight=1.0, seed=42, **kwargs):
        from matplotlib.colors import LinearSegmentedColormap
        cols = ColorUtils.accent_colors(palette, "Arctic Aurora")
        cmap = LinearSegmentedColormap.from_list(
            "boids", [cols[1], cols[2], cols[3]], N=256)
        N   = max(10, int(n_boids))
        pos, vel = _boids_init(N, seed)
        for _ in range(int(n_steps)):
            pos, vel = _boids_step(pos, vel, float(sep_weight),
                                   float(align_weight), float(coh_weight))
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
        cols = ColorUtils.accent_colors(palette, "Arctic Aurora")
        cmap = LinearSegmentedColormap.from_list("boids", [cols[1], cols[2], cols[3]], N=256)
        N = max(10, int(n_boids))
        pos, vel = _boids_init(N, seed)
        fig, ax = plt.subplots(figsize=(6, 6), facecolor=cols[0])
        ax.set_facecolor(cols[0]); ax.set_aspect("equal")
        ax.set_xlim(0,1); ax.set_ylim(0,1)
        ax.set_xticks([]); ax.set_yticks([])
        quiv = ax.quiver(pos[:,0], pos[:,1], vel[:,0], vel[:,1], np.zeros(N),
                         cmap=cmap, clim=(0, 1), angles="xy", scale_units="xy",
                         scale=0.12, width=0.003, headwidth=4, alpha=0.9)
        title = ax.set_title("", color=cols[3], fontsize=9, pad=4)
        fig.tight_layout()
        frames = []
        for step in range(n_frames * 2):
            pos, vel = _boids_step(pos, vel, float(sep_weight),
                                   float(align_weight), float(coh_weight))
            if step % 2 == 0:
                spd_n = (np.linalg.norm(vel, axis=1) - 0.003) / 0.007
                quiv.set_offsets(pos)
                quiv.set_UVC(vel[:,0], vel[:,1], spd_n)
                title.set_text(f"Boids | step {step+1}")
                frames.append(capture_frame(fig))
        plt.close(fig)
        return frames


class _NagelSchreckenberg:
    """Nagel-Schreckenberg cellular automaton on a circular road."""

    def __init__(self, road_length, n_cars, v_max, p_slow, seed):
        self.rng = np.random.default_rng(int(seed))
        self.L = max(50, int(road_length))
        self.n = min(int(n_cars), self.L - 1)
        self.vmax = max(1, int(v_max))
        self.p = float(p_slow)
        self.positions = np.sort(self.rng.choice(self.L, self.n, replace=False))
        self.velocities = self.rng.integers(0, self.vmax + 1, self.n)

    def step(self):
        """Parallel update: accelerate, brake to gap, random slowdown, move."""
        velocities = np.minimum(self.velocities + 1, self.vmax)
        sorted_idx = np.argsort(self.positions)
        pos_sorted = self.positions[sorted_idx]
        vel_sorted = velocities[sorted_idx]
        gaps = np.empty(self.n, dtype=np.int64)
        gaps[:-1] = pos_sorted[1:] - pos_sorted[:-1] - 1
        gaps[-1]  = (pos_sorted[0] + self.L) - pos_sorted[-1] - 1
        vel_sorted = np.minimum(vel_sorted, gaps)
        rand_mask = self.rng.uniform(0, 1, self.n) < self.p
        vel_sorted = np.where(rand_mask, np.maximum(vel_sorted - 1, 0), vel_sorted)
        pos_sorted = (pos_sorted + vel_sorted) % self.L
        inv_idx = np.empty_like(sorted_idx)
        inv_idx[sorted_idx] = np.arange(self.n)
        self.positions  = pos_sorted[inv_idx]
        self.velocities = vel_sorted[inv_idx]

    def spacetime(self, steps):
        """Run `steps` updates; rows = time, value = car velocity (-1 = empty)."""
        st = np.full((steps, self.L), -1, dtype=np.int8)
        for t in range(steps):
            st[t, self.positions] = self.velocities
            self.step()
        return st


class TrafficFlowRenderer(BasePattern):
    """96 — Traffic Flow Simulation (Nagel-Schreckenberg model)"""
    name  = "Traffic Flow Simulation"
    group = "Scientific & Simulation"

    def render(self, resolution="Low", palette="Sunset Blaze", speed=1.0,
               road_length=200, n_cars=50, v_max=5, p_slow=0.3,
               n_steps=150, seed=42, **kwargs):
        from matplotlib.colors import LinearSegmentedColormap
        cols = ColorUtils.accent_colors(palette, "Sunset Blaze")
        cmap = LinearSegmentedColormap.from_list(
            "traffic", ["#000000", cols[1], cols[2], cols[3]], N=256)
        road = _NagelSchreckenberg(road_length, n_cars, v_max, p_slow, seed)
        L, N_cars, Vmax, p = road.L, road.n, road.vmax, road.p
        steps = max(20, int(n_steps))
        spacetime = road.spacetime(steps)
        fig, ax = plt.subplots(figsize=(10, 6), facecolor=cols[0])
        ax.set_facecolor(cols[0])
        # Space-time diagram: occupied cells as coloured squares
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
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(0, Vmax))
        sm.set_array([])
        cbar = fig.colorbar(sm, ax=ax, fraction=0.03, pad=0.02)
        cbar.set_label("Velocity", color=cols[2], fontsize=9)
        cbar.ax.yaxis.set_tick_params(color=cols[2])
        plt.setp(cbar.ax.yaxis.get_ticklabels(), color=cols[2])
        cbar.outline.set_edgecolor(cols[1])
        ax.set_title(
            f"Traffic Flow (Nagel-Schreckenberg)  |  L={L}  N={N_cars}  "
            f"ρ={N_cars / L:.2f}  Vmax={Vmax}  p={p:.2f}",
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
        cols = ColorUtils.accent_colors(palette, "Sunset Blaze")
        cmap = LinearSegmentedColormap.from_list("traffic", ["#000000", cols[1], cols[2], cols[3]], N=256)
        road = _NagelSchreckenberg(road_length, n_cars, v_max, p_slow, seed)
        total = n_frames * 3
        spacetime = road.spacetime(total)
        # The diagram grows downward: draw the full history once as an image
        # and reveal one more slice of rows per frame.
        img = np.where(spacetime >= 0, spacetime / road.vmax, np.nan)
        fig, ax = plt.subplots(figsize=(8, 4), facecolor=cols[0])
        ax.set_facecolor(cols[0])
        ax.set_xticks([]); ax.set_yticks([])
        im = ax.imshow(img[:1], cmap=cmap, vmin=0, vmax=1, aspect="auto",
                       interpolation="nearest", extent=[0, road.L, 1, 0])
        title = ax.set_title("", color=cols[3], fontsize=9, pad=4)
        fig.tight_layout()
        frames = []
        for t in range(0, total, 3):
            end = t + 1
            im.set_data(img[:end])
            im.set_extent([0, road.L, end, 0])
            title.set_text(f"Traffic Flow | t={end}")
            frames.append(capture_frame(fig))
        plt.close(fig)
        return frames


def _lotka_volterra(a, b, d, g, x0, y0, T, dt=0.01):
    """RK4 integration of dx/dt = ax - bxy, dy/dt = dxy - gy; returns (t, x, y)."""
    n = int(T / dt)
    x, y = np.empty(n), np.empty(n)
    x[0], y[0] = x0, y0
    def deriv(xi, yi):
        return a*xi - b*xi*yi, d*xi*yi - g*yi
    for i in range(n - 1):
        k1x, k1y = deriv(x[i], y[i])
        k2x, k2y = deriv(x[i]+dt/2*k1x, y[i]+dt/2*k1y)
        k3x, k3y = deriv(x[i]+dt/2*k2x, y[i]+dt/2*k2y)
        k4x, k4y = deriv(x[i]+dt*k3x, y[i]+dt*k3y)
        x[i+1] = max(0, x[i] + dt/6*(k1x + 2*k2x + 2*k3x + k4x))
        y[i+1] = max(0, y[i] + dt/6*(k1y + 2*k2y + 2*k3y + k4y))
    return np.arange(n) * dt, x, y


class EcosystemRenderer(BasePattern):
    """97 — Ecosystem Predator-Prey (Lotka-Volterra)"""
    name  = "Ecosystem Predator-Prey"
    group = "Scientific & Simulation"

    def render(self, resolution="Low", palette="Forest", speed=1.0,
               alpha=1.1, beta=0.4, delta=0.1, gamma=0.4,
               prey_0=10.0, pred_0=5.0, t_max=50.0, **kwargs):
        cols = ColorUtils.accent_colors(palette, "Forest")
        a, b, d, g = float(alpha), float(beta), float(delta), float(gamma)
        t_arr, x, y = _lotka_volterra(a, b, d, g, float(prey_0), float(pred_0), float(t_max))
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
        # Nullclines: prey stationary at y = a/b, predators at x = g/d
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
        cols = ColorUtils.accent_colors(palette, "Forest")
        T = float(t_max)
        t_arr, x, y = _lotka_volterra(float(alpha), float(beta), float(delta),
                                      float(gamma), float(prey_0), float(pred_0), T)
        n = len(t_arr)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), facecolor=cols[0])
        for ax in (ax1, ax2):
            ax.set_facecolor(cols[0])
            ax.tick_params(colors=cols[2])
        prey_line, = ax1.plot([], [], color=cols[2], linewidth=1.2, label="Prey")
        pred_line, = ax1.plot([], [], color=cols[3], linewidth=1.2, label="Predator")
        ax1.set_xlim(0, T); ax1.set_ylim(0, max(x.max(), y.max())*1.1)
        ax1.set_title("Populations", color=cols[3], fontsize=9)
        ax1.legend(fontsize=7, framealpha=0.4, labelcolor=cols[3])
        phase_line, = ax2.plot([], [], color=cols[2], linewidth=0.8)
        head = ax2.scatter([x[0]], [y[0]], color=cols[3], s=40, zorder=5)
        ax2.set_xlim(0, x.max()*1.1); ax2.set_ylim(0, y.max()*1.1)
        ax2.set_title("Phase Portrait", color=cols[3], fontsize=9)
        fig.tight_layout()
        frames = []
        step = max(1, n // n_frames)
        for f in range(n_frames):
            end = min((f+1) * step, n)
            prey_line.set_data(t_arr[:end], x[:end])
            pred_line.set_data(t_arr[:end], y[:end])
            phase_line.set_data(x[:end], y[:end])
            head.set_offsets([[x[end-1], y[end-1]]])
            frames.append(capture_frame(fig))
        plt.close(fig)
        return frames


class _AntColony:
    """Ant Colony Optimisation for the TSP, with all ants built in parallel.

    Transition weights are evaluated in log space and normalised per ant, so
    they cannot underflow to an all-zero (NaN) distribution; pheromone is kept
    above a floor (Max-Min Ant System) so no edge is ever ruled out entirely.
    """

    def __init__(self, n_cities, seed, alpha, beta, rho):
        self.rng = np.random.default_rng(int(seed))
        self.cities = self.rng.uniform(0.05, 0.95, (n_cities, 2))
        diff = self.cities[:, None, :] - self.cities[None, :, :]
        self.dist = np.sqrt((diff**2).sum(axis=2))
        np.fill_diagonal(self.dist, np.inf)
        self.log_eta = -np.log(self.dist)            # heuristic: 1 / distance
        self.pheromone = np.ones((n_cities, n_cities))
        self.alpha, self.beta, self.rho = alpha, beta, rho
        self.best_tour, self.best_length = None, np.inf

    def iterate(self, n_ants):
        nc = len(self.cities)
        ants = np.arange(n_ants)
        tours = np.empty((n_ants, nc), dtype=np.intp)
        tours[:, 0] = self.rng.integers(0, nc, n_ants)
        visited = np.zeros((n_ants, nc), dtype=bool)
        visited[ants, tours[:, 0]] = True
        log_tau = np.log(self.pheromone)
        for step in range(1, nc):
            cur = tours[:, step - 1]
            logw = self.alpha * log_tau[cur] + self.beta * self.log_eta[cur]
            logw[visited] = -np.inf
            w = np.exp(logw - logw.max(axis=1, keepdims=True))
            cum = np.cumsum(w, axis=1)
            r = (1.0 - self.rng.random(n_ants)) * cum[:, -1]   # in (0, total]
            nxt = np.minimum((cum < r[:, None]).sum(axis=1), nc - 1)
            tours[:, step] = nxt
            visited[ants, nxt] = True
        nxt_city = np.roll(tours, -1, axis=1)
        lengths = self.dist[tours, nxt_city].sum(axis=1)
        best = int(np.argmin(lengths))
        if lengths[best] < self.best_length:
            self.best_length = float(lengths[best])
            self.best_tour = tours[best].tolist()
        # Evaporate, deposit 1/L on every edge each ant used (both directions)
        self.pheromone *= (1 - self.rho)
        dep = np.repeat(1.0 / lengths, nc)
        np.add.at(self.pheromone, (tours.ravel(), nxt_city.ravel()), dep)
        np.add.at(self.pheromone, (nxt_city.ravel(), tours.ravel()), dep)
        np.maximum(self.pheromone, 1e-6 * self.pheromone.max(), out=self.pheromone)

    def strong_edges(self, threshold=0.05):
        """Edges whose pheromone is above `threshold` of the maximum."""
        p = self.pheromone / self.pheromone.max()
        i, j = np.triu_indices(len(self.cities), k=1)
        keep = p[i, j] > threshold
        return np.stack([self.cities[i[keep]], self.cities[j[keep]]], axis=1), p[i[keep], j[keep]]


class AntColonyRenderer(BasePattern):
    """98 — Ant Colony Optimization (TSP)"""
    name  = "Ant Colony Optimization"
    group = "Scientific & Simulation"

    def render(self, resolution="Low", palette="Lava Flow", speed=1.0,
               n_cities=25, n_ants=30, n_iterations=80, alpha_aco=1.0,
               beta_aco=3.0, evaporation=0.5, seed=42, **kwargs):
        from matplotlib.collections import LineCollection
        from matplotlib.colors import LinearSegmentedColormap
        cols = ColorUtils.accent_colors(palette, "Lava Flow")
        cmap_pher = LinearSegmentedColormap.from_list(
            "pher", ["#000000", cols[1], cols[2], cols[3]], N=256)
        NC     = max(5, int(n_cities))
        N_ants = max(5, int(n_ants))
        iters  = max(5, int(n_iterations))
        colony = _AntColony(NC, seed, float(alpha_aco), float(beta_aco), float(evaporation))
        for _ in range(iters):
            colony.iterate(N_ants)
        cities = colony.cities
        fig, ax = plt.subplots(figsize=(8, 8), facecolor=cols[0])
        ax.set_facecolor(cols[0])
        ax.set_aspect("equal")
        # Pheromone trails (edges above 5% of the strongest)
        segs, strength = colony.strong_edges()
        if len(segs):
            seg_colors = cmap_pher(strength)
            seg_colors[:, 3] = strength * 0.7
            ax.add_collection(LineCollection(segs, colors=seg_colors,
                                             linewidths=strength * 2.1, zorder=1))
        # Best tour
        tour_pts = cities[colony.best_tour + [colony.best_tour[0]]]
        ax.plot(tour_pts[:, 0], tour_pts[:, 1], color=cols[3],
                linewidth=2.5, alpha=0.9, zorder=3)
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
            f"best={colony.best_length:.2f}  |  {iters} iters × {N_ants} ants",
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
        from matplotlib.colors import to_rgb
        from engines.animation import capture_frame
        cols = ColorUtils.accent_colors(palette, "Lava Flow")
        NC = max(5, int(n_cities))
        N_ants = max(5, int(n_ants))
        colony = _AntColony(NC, seed, float(alpha_aco), float(beta_aco), float(evaporation))
        cities = colony.cities
        fig, ax = plt.subplots(figsize=(6, 6), facecolor=cols[0])
        ax.set_facecolor(cols[0]); ax.set_aspect("equal")
        ax.set_xlim(0,1); ax.set_ylim(0,1); ax.set_xticks([]); ax.set_yticks([])
        trails = LineCollection([], zorder=1)
        ax.add_collection(trails)
        tour_line, = ax.plot([], [], color=cols[3], linewidth=2, alpha=0.9, zorder=3)
        ax.scatter(cities[:,0], cities[:,1], s=60, color=cols[2], edgecolors=cols[3],
                   linewidths=1.2, zorder=4)
        title = ax.set_title("", color=cols[3], fontsize=9, pad=4)
        fig.tight_layout()
        trail_rgb = to_rgb(cols[2])
        frames = []
        for iteration in range(n_frames):
            colony.iterate(N_ants)
            segs, strength = colony.strong_edges()
            trails.set_segments(segs)
            trails.set_color([(*trail_rgb, s * 0.7) for s in strength])
            trails.set_linewidth(strength * 2.1)
            tp = cities[colony.best_tour + [colony.best_tour[0]]]
            tour_line.set_data(tp[:, 0], tp[:, 1])
            title.set_text(f"ACO | iter {iteration+1} | best={colony.best_length:.2f}")
            frames.append(capture_frame(fig))
        plt.close(fig)
        return frames


class _SPHFluid:
    """Weakly-compressible 2D SPH (Müller et al. 2003 kernels, 2D normalisation).

    A dam-break block in the unit box. Particle mass is calibrated so the
    initial interior density equals `rho0`; the time step obeys the CFL
    condition for sound speed c = sqrt(k), so any slider setting is stable.
    """
    H = 0.04                    # smoothing radius
    ALPHA_AV = 0.3              # artificial-viscosity strength
    WALL_LO, WALL_HI = 0.02, 0.98

    def __init__(self, n, g, mu, rho0, k, seed):
        h = self.H
        self.g, self.mu, self.rho0, self.k = g, mu, rho0, k
        self.c = np.sqrt(k)                  # speed of sound: dp/drho = k
        self.poly6 = 4.0 / (np.pi * h**8)
        self.spiky_grad = 30.0 / (np.pi * h**5)
        self.visc_lap = 40.0 / (np.pi * h**5)
        rng = np.random.default_rng(int(seed))
        spacing = 0.4 * h                    # ~19 neighbours per particle
        side = int(np.ceil(np.sqrt(n)))
        idx = np.arange(n)
        self.pos = np.column_stack([0.06 + (idx % side) * spacing,
                                    0.40 + (idx // side) * spacing])
        self.pos += rng.uniform(-1e-3, 1e-3, self.pos.shape)
        self.vel = np.zeros((n, 2))
        self.wall_k = 0.5 * k / h                  # stiff relative to pressure forces
        self.wall_damp = 2.0 * np.sqrt(self.wall_k)  # critical damping
        self.mass = 1.0
        self.mass = rho0 / np.percentile(self._density(self._pairs()), 90)
        self.density = self._density(self._pairs())

    SKIN = 0.2                  # Verlet-list margin, as a fraction of H

    def _pairs(self):
        """Pairs closer than H, from a Verlet candidate list searched at
        H * (1 + SKIN) and rebuilt only once some particle has moved more
        than half the skin since the last build."""
        from scipy.spatial import cKDTree
        moved = getattr(self, "_list_pos", None)
        if (moved is None or len(moved) != len(self.pos) or
                np.abs(self.pos - moved).max() > 0.5 * self.SKIN * self.H):
            cand = cKDTree(self.pos).query_pairs(self.H * (1 + self.SKIN),
                                                 output_type="ndarray")
            self._cand_i, self._cand_j = cand[:, 0], cand[:, 1]
            self._list_pos = self.pos.copy()
        i, j = self._cand_i, self._cand_j
        rij = self.pos[i] - self.pos[j]
        r = np.sqrt((rij**2).sum(axis=1))
        near = r < self.H
        return i[near], j[near], rij[near], r[near].clip(1e-9, None)

    def _scatter(self, i, j, w_ij, w_ji):
        """Sum pairwise contributions onto both particles of each pair."""
        n = len(self.pos)
        return np.bincount(i, w_ij, n) + np.bincount(j, w_ji, n)

    def _density(self, pairs):
        i, j, _, r = pairs
        w = self.poly6 * (self.H**2 - r**2)**3
        self_term = self.poly6 * self.H**6
        return self.mass * (self_term + self._scatter(i, j, w, w))

    def step(self, dt):
        pairs = self._pairs()
        i, j, rij, r = pairs
        rho = self._density(pairs)
        p = self.k * np.maximum(rho - self.rho0, 0.0)
        grad = self.spiky_grad * (self.H - r)**2 / r      # |grad W| / r
        dv = self.vel[j] - self.vel[i]
        # Every pair term is antisymmetric: particle i gains a_ij, j loses it.
        #  pressure  -m (p_i+p_j)/(2 rho_i rho_j) grad W   (repulsive)
        #  viscosity  mu m (v_j - v_i)/(rho_i rho_j) lap W
        pres = self.mass * (p[i] + p[j]) / 2 * grad
        lap = self.mu * self.mass * self.visc_lap * (self.H - r)
        a_ij = (pres[:, None] * rij + lap[:, None] * dv) / (rho[i] * rho[j])[:, None]
        # Monaghan artificial viscosity on approaching pairs: dissipates
        # impact energy so particles cannot interpenetrate in collisions
        approach = np.minimum((-dv * rij).sum(axis=1), 0.0)
        pi_ij = (-self.ALPHA_AV * self.c * self.H * approach
                 / (0.5 * (rho[i] + rho[j]) * (r**2 + 0.01 * self.H**2)))
        a_ij += (self.mass * pi_ij * grad)[:, None] * rij
        # One bincount over (particle, axis) slots for both ends of every pair
        n = len(self.pos)
        slots = (np.concatenate([i, j])[:, None] * 2 + np.arange(2)).ravel()
        acc = np.bincount(slots, np.concatenate([a_ij, -a_ij]).ravel(),
                          2 * n).reshape(n, 2)
        acc[:, 1] -= self.g
        # Walls: critically damped penalty springs within H/2 of each wall.
        # (Hard clamping stacks particles on top of each other, r -> 0, and
        # the pressure term explodes.)
        margin = 0.5 * self.H
        for d in range(2):
            pen_lo = np.maximum(self.WALL_LO + margin - self.pos[:, d], 0.0)
            pen_hi = np.maximum(self.pos[:, d] - (self.WALL_HI - margin), 0.0)
            touching = (pen_lo > 0) | (pen_hi > 0)
            acc[:, d] += self.wall_k * (pen_lo - pen_hi)
            acc[touching, d] -= self.wall_damp * self.vel[touching, d]
        # Symplectic Euler; hard clamp only as a safety net
        self.vel += dt * acc
        self.pos += dt * self.vel
        np.clip(self.pos, 0.005, 0.995, out=self.pos)
        self.density = rho

    def advance(self, duration):
        """Advance by `duration` seconds in CFL-limited sub-steps."""
        c = self.c
        t = 0.0
        while t < duration:
            vmax = np.sqrt((self.vel**2).sum(axis=1).max())
            dt = min(0.4 * self.H / (c + vmax), 0.5 / self.wall_damp, duration - t)
            self.step(dt)
            t += dt

    def colour_values(self):
        rho_n = (self.density - self.density.min()) / (np.ptp(self.density) + 1e-9)
        spd = np.linalg.norm(self.vel, axis=1)
        return 0.6 * rho_n + 0.4 * spd / (spd.max() + 1e-9)


class FluidDynamicsRenderer(BasePattern):
    """99 — Fluid Dynamics (Smoothed Particle Hydrodynamics)"""
    name  = "Fluid Dynamics (SPH)"
    group = "Scientific & Simulation"
    STEP_SECONDS = 0.01         # simulated time per "n_steps" unit

    def render(self, resolution="Low", palette="Ocean Depths", speed=1.0,
               n_particles=300, n_steps=60, gravity=9.8, viscosity=0.02,
               rest_density=1000.0, gas_const=2000.0, seed=7, **kwargs):
        from matplotlib.colors import LinearSegmentedColormap
        cols = ColorUtils.accent_colors(palette, "Ocean Depths")
        cmap = LinearSegmentedColormap.from_list("sph", cols, N=256)
        N = max(50, int(n_particles))
        steps = max(10, int(n_steps))
        g_val, mu, k = float(gravity), float(viscosity), float(gas_const)
        fluid = _SPHFluid(N, g_val, mu, float(rest_density), k, seed)
        fluid.advance(steps * self.STEP_SECONDS)
        fig, ax = plt.subplots(figsize=(8, 8), facecolor=cols[0])
        ax.set_facecolor(cols[0])
        ax.set_aspect("equal")
        ax.scatter(fluid.pos[:, 0], fluid.pos[:, 1], c=fluid.colour_values(), cmap=cmap,
                   s=35, alpha=0.85, linewidths=0, vmin=0, vmax=1, zorder=3)
        ax.add_patch(plt.Rectangle((0.02, 0.02), 0.96, 0.96, fill=False,
                                   edgecolor=cols[2], linewidth=1.5, zorder=5))
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        ax.set_xticks([]); ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_edgecolor(cols[1])
        ax.set_title(
            f"Fluid Dynamics (SPH)  |  N={N}  |  t={steps * self.STEP_SECONDS:.2f}s  |  "
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
        cols = ColorUtils.accent_colors(palette, "Ocean Depths")
        cmap = LinearSegmentedColormap.from_list("sph", cols, N=256)
        fluid = _SPHFluid(max(50, int(n_particles)), float(gravity), float(viscosity),
                          float(rest_density), float(gas_const), seed)
        fig, ax = plt.subplots(figsize=(6, 6), facecolor=cols[0])
        ax.set_facecolor(cols[0]); ax.set_aspect("equal")
        ax.set_xlim(0,1); ax.set_ylim(0,1); ax.set_xticks([]); ax.set_yticks([])
        ax.add_patch(plt.Rectangle((0.02,0.02), 0.96, 0.96, fill=False,
                                   edgecolor=cols[2], linewidth=1.2))
        sc = ax.scatter(fluid.pos[:,0], fluid.pos[:,1], c=fluid.colour_values(), cmap=cmap,
                        s=25, alpha=0.85, linewidths=0, vmin=0, vmax=1)
        title = ax.set_title("", color=cols[3], fontsize=9, pad=4)
        fig.tight_layout()
        frame_time = 3 * self.STEP_SECONDS
        frames = []
        for f in range(n_frames):
            sc.set_offsets(fluid.pos)
            sc.set_array(fluid.colour_values())
            title.set_text(f"SPH Fluid | t={f * frame_time:.2f}s")
            frames.append(capture_frame(fig))
            fluid.advance(frame_time)
        plt.close(fig)
        return frames


class _WavePacket:
    """1D Gaussian wave packet evolved by the split-step Fourier method (hbar = m = 1)."""
    L = 12.0                    # domain half-width (periodic)
    DT = 0.005

    def __init__(self, nx, x0, k0, sigma, potential, height):
        self.x = np.linspace(-self.L, self.L, nx)
        dx = self.x[1] - self.x[0]
        k = np.fft.fftfreq(nx, d=dx) * 2 * np.pi
        self.psi = (2 * np.pi * sigma**2)**(-0.25) * np.exp(
            -(self.x - x0)**2 / (4 * sigma**2) + 1j * k0 * self.x)
        self.potential = str(potential).lower()
        x = self.x
        if self.potential == "well":
            self.V = np.where((x > -1) & (x < 1), -height, 0.0)
        elif self.potential == "harmonic":
            self.V = 0.5 * height * x**2 / self.L**2
        else:                   # "barrier"
            self.V = np.where((x > 0) & (x < 0.5), height, 0.0)
        # Strang splitting: half potential kick, full kinetic drift, half kick
        self._kick = np.exp(-0.5j * self.V * self.DT)
        self._drift = np.exp(-0.5j * k**2 * self.DT)

    def step(self):
        self.psi = self._kick * np.fft.ifft(self._drift * np.fft.fft(self._kick * self.psi))

    @property
    def prob(self):
        return np.abs(self.psi)**2

    def potential_display(self, top):
        """Potential shape shifted to start at 0 and scaled to peak at `top`
        (a well is negative, so it would otherwise never appear)."""
        shape = self.V - self.V.min()
        return shape * (top / shape.max()) if shape.max() > 0 else shape


class QuantumWaveRenderer(BasePattern):
    """100 — Quantum Wave Packet (Split-Step Fourier Method)"""
    name  = "Quantum Wave Packet"
    group = "Scientific & Simulation"

    def render(self, resolution="Low", palette="Neon Cyberpunk", speed=1.0,
               x0=-3.0, k0=5.0, sigma=0.5, n_steps=200,
               potential="barrier", barrier_height=8.0, **kwargs):
        from matplotlib.colors import LinearSegmentedColormap
        cols = ColorUtils.accent_colors(palette, "Neon Cyberpunk")
        cmap = LinearSegmentedColormap.from_list("qm", cols, N=256)
        Nx = {"Low": 512, "Medium": 1024, "High": 2048}.get(resolution, 512)
        wp = _WavePacket(Nx, float(x0), float(k0), float(sigma), potential,
                         float(barrier_height))
        x, L, dt = wp.x, wp.L, wp.DT
        steps = max(10, int(n_steps))
        snap_interval = max(1, steps // min(steps, 100))
        psi_init = wp.prob
        snapshots = []
        for step in range(steps):
            wp.step()
            if step % snap_interval == 0:
                snapshots.append(wp.prob)
        snapshots.append(wp.prob)
        st_image = np.array(snapshots)  # (T, Nx)
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), facecolor=cols[0],
                                        gridspec_kw={'height_ratios': [1, 1.5]})
        for ax in (ax1, ax2):
            ax.set_facecolor(cols[0])
            ax.tick_params(colors=cols[2])
            for spine in ax.spines.values():
                spine.set_edgecolor(cols[1])
        # Top: final |ψ|² with potential overlay
        prob = wp.prob
        ax1.fill_between(x, 0, prob, color=cols[2], alpha=0.6)
        ax1.plot(x, prob, color=cols[3], linewidth=1.5, label=r"$|\psi|^2$ (final)")
        ax1.plot(x, psi_init, color=cols[1], linewidth=1.0, alpha=0.5,
                 linestyle='--', label=r"$|\psi|^2$ (initial)")
        ax1.fill_between(x, 0, wp.potential_display(prob.max() * 0.4),
                         color=cols[1], alpha=0.3, label="V(x)")
        ax1.set_xlim(-L, L)
        ax1.set_ylim(0, prob.max() * 1.3)
        ax1.set_xlabel("x", color=cols[2], fontsize=9)
        ax1.set_ylabel(r"$|\psi(x)|^2$", color=cols[2], fontsize=9)
        ax1.legend(loc="upper right", fontsize=8, framealpha=0.5, labelcolor=cols[3])
        ax1.set_title("Quantum Wave Packet — Probability Density",
                      color=cols[3], fontsize=10, fontweight="bold")
        # Bottom: space-time diagram
        ax2.imshow(st_image, aspect='auto', extent=[-L, L, steps * dt, 0], cmap=cmap,
                   interpolation='bilinear', vmin=0, vmax=st_image.max())
        ax2.set_xlabel("x", color=cols[2], fontsize=9)
        ax2.set_ylabel("Time", color=cols[2], fontsize=9)
        ax2.set_title("Space-Time Evolution", color=cols[3], fontsize=10, fontweight="bold")
        fig.suptitle(
            f"Quantum Wave Packet  |  k₀={float(k0):.1f}  σ={float(sigma):.2f}  "
            f"V={wp.potential}  h={float(barrier_height):.1f}  |  {steps} steps",
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
        from engines.animation import capture_frame
        cols = ColorUtils.accent_colors(palette, "Neon Cyberpunk")
        wp = _WavePacket(512, float(x0), float(k0), float(sigma), potential,
                         float(barrier_height))
        x, L = wp.x, wp.L
        top = wp.prob.max() * 1.5
        fig, ax = plt.subplots(figsize=(8, 4), facecolor=cols[0])
        ax.set_facecolor(cols[0])
        ax.fill_between(x, 0, wp.potential_display(top * 0.3), color=cols[1], alpha=0.25)
        fill = ax.fill_between(x, 0, wp.prob, color=cols[2], alpha=0.5)
        line, = ax.plot(x, wp.prob, color=cols[3], linewidth=1.5)
        ax.set_xlim(-L, L); ax.set_ylim(0, top)
        ax.set_xticks([]); ax.set_yticks([])
        title = ax.set_title("", color=cols[3], fontsize=9, pad=4)
        fig.tight_layout()
        frames = []
        for step in range(n_frames * 4):
            wp.step()
            if step % 4 == 0:
                prob = wp.prob
                fill.remove()
                fill = ax.fill_between(x, 0, prob, color=cols[2], alpha=0.5)
                line.set_ydata(prob)
                title.set_text(f"Quantum Wave Packet | t={step * wp.DT:.3f}")
                frames.append(capture_frame(fig))
        plt.close(fig)
        return frames


