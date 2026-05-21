"""
Nature-Inspired Patterns (21-40)
Patterns 21-34 are fully implemented; 35-40 remain as stubs awaiting Phase 1 sessions.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.collections as mc
import numpy as np
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from engines.renderer import BasePattern
from engines.color_utils import ColorUtils


class _StubMixin:
    """Shared stub render logic for not-yet-implemented patterns."""
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
        ax.text(0.5, 0.42, "\u23f3 Coming Soon", ha="center", va="center",
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


# ── Pattern 21 ────────────────────────────────────────────────────────────────

class CherryBlossomRenderer(BasePattern):
    """Pattern 21 — Cherry Blossom Particle Scene."""
    name = "Cherry Blossom Particle Scene"
    group = "Nature-Inspired"

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=600, min=100, max=1500, step=50,
                              description="Petals:"),
            widgets.FloatSlider(value=0.4, min=0.0, max=1.0, step=0.05,
                                description="Wind:", readout_format=".2f"),
            widgets.IntSlider(value=7, min=3, max=11, step=1,
                              description="Tree Depth:"),
            widgets.IntSlider(value=42, min=0, max=999,
                              description="Seed:"),
        ]

    def render(self, resolution="Low", palette="Inferno", speed=1.0, **kwargs):
        n_petals   = int(kwargs.get("petals", 600))
        wind       = float(kwargs.get("wind", 0.4))
        tree_depth = int(kwargs.get("tree_depth", 7))
        seed       = int(kwargs.get("seed", 42))
        rng        = np.random.default_rng(seed)

        fig, ax = self._create_figure(figsize=(8, 8), bg_color="#100a18")

        # ── Recursive tree: collect segments then draw with LineCollection ──
        branch_segs, branch_cols, branch_lws = [], [], []

        def _branch(x, y, angle, length, d):
            if d == 0 or length < 0.008:
                return
            x2 = x + length * np.cos(angle)
            y2 = y + length * np.sin(angle)
            branch_segs.append([[x, y], [x2, y2]])
            branch_cols.append("#3b1a08" if d > 3 else "#5c2e12")
            branch_lws.append(max(0.4, d * 0.55))
            spread = np.radians(rng.uniform(18, 30))
            _branch(x2, y2, angle + spread, length * 0.67, d - 1)
            _branch(x2, y2, angle - spread, length * 0.67, d - 1)
            if d > 3 and rng.random() < 0.35:
                _branch(x2, y2, angle + rng.uniform(-0.1, 0.1),
                        length * 0.50, d - 2)

        _branch(0.5, 0.0, np.pi / 2, 0.24, tree_depth)

        lc = mc.LineCollection(branch_segs, colors=branch_cols,
                               linewidths=branch_lws, alpha=0.95,
                               capstyle="round", zorder=1)
        ax.add_collection(lc)

        # ── Falling petals ──────────────────────────────────────────────────
        px = rng.uniform(0.02, 0.98, n_petals)
        py = rng.uniform(0.0, 1.0, n_petals)
        # Wind-driven drift: stronger at top (longer flight path)
        px = np.clip(px + wind * (1.0 - py) * rng.uniform(-0.3, 0.3, n_petals),
                     0.0, 1.0)
        sizes = rng.uniform(8, 60, n_petals)
        hue = rng.uniform(0.0, 1.0, n_petals)
        # Deep rose (1, 0.35, 0.50) → pale blush (1, 0.85, 0.90)
        colors = np.column_stack([
            np.ones(n_petals),
            0.35 + 0.50 * hue,
            0.50 + 0.40 * hue,
            rng.uniform(0.4, 0.95, n_petals),
        ])
        ax.scatter(px, py, s=sizes, c=colors, zorder=3, linewidths=0)

        # ── Ground layer of settled petals ──────────────────────────────────
        ng = n_petals // 4
        gx = rng.uniform(0.0, 1.0, ng)
        gy = rng.uniform(0.0, 0.055, ng)
        ax.scatter(gx, gy, s=rng.uniform(3, 18, ng),
                   color="#e8a0c0", alpha=0.55, zorder=2, linewidths=0)

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        ax.set_title("Cherry Blossom Particle Scene", color="#f5c2d4",
                     fontsize=13, pad=8)
        plt.tight_layout()
        plt.show()
        plt.close(fig)


# ── Pattern 22 ────────────────────────────────────────────────────────────────

class ProceduralTreeRenderer(BasePattern):
    """Pattern 22 — Procedural Tree Generator."""
    name = "Procedural Tree Generator"
    group = "Nature-Inspired"

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=10, min=3, max=13, step=1,
                              description="Depth:"),
            widgets.IntSlider(value=2, min=2, max=4, step=1,
                              description="Branches:"),
            widgets.FloatSlider(value=28.0, min=10.0, max=55.0, step=1.0,
                                description="Branch Angle:", readout_format=".1f"),
            widgets.FloatSlider(value=0.67, min=0.50, max=0.85, step=0.01,
                                description="Length Decay:", readout_format=".2f"),
            widgets.IntSlider(value=42, min=0, max=999,
                              description="Seed:"),
        ]

    def render(self, resolution="Low", palette="Inferno", speed=1.0, **kwargs):
        depth      = int(kwargs.get("depth", 10))
        n_branches = int(kwargs.get("branches", 2))
        ang_deg    = float(kwargs.get("branch_angle", 28.0))
        decay      = float(kwargs.get("length_decay", 0.67))
        seed       = int(kwargs.get("seed", 42))
        rng        = np.random.default_rng(seed)

        cmap = ColorUtils.make_colormap(palette)
        fig, ax = self._create_figure(figsize=(8, 9), bg_color="#060d06")

        ang = np.radians(ang_deg)
        seg_list, t_list, lw_list = [], [], []

        def _draw(x, y, angle, length, d):
            if d == 0 or length < 0.005:
                return
            x2 = x + length * np.cos(angle)
            y2 = y + length * np.sin(angle)
            seg_list.append([[x, y], [x2, y2]])
            t_list.append(1.0 - d / depth)          # trunk=0 (dark), tip=1 (bright)
            lw_list.append(max(0.3, d * 0.55))
            # Compute branch angles
            half = ang * (n_branches - 1) / 2.0
            branch_angs = [angle - half + ang * i for i in range(n_branches)]
            for ba in branch_angs:
                jitter = rng.uniform(-0.06, 0.06)
                _draw(x2, y2, ba + jitter,
                      length * (decay + rng.uniform(-0.03, 0.03)), d - 1)

        _draw(0.5, 0.0, np.pi / 2, 0.26, depth)

        if seg_list:
            colors = cmap(np.array(t_list))
            lc = mc.LineCollection(seg_list, colors=colors,
                                   linewidths=lw_list, alpha=0.90,
                                   capstyle="round")
            ax.add_collection(lc)

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1.05)
        ax.axis("off")
        ax.set_title("Procedural Tree Generator", color="#a8e0a8",
                     fontsize=13, pad=8)
        plt.tight_layout()
        plt.show()
        plt.close(fig)


# ── Pattern 23 ────────────────────────────────────────────────────────────────

class ReactionDiffusionRenderer(BasePattern):
    """Pattern 23 — Reaction-Diffusion (Gray-Scott Turing Patterns)."""
    name = "Reaction-Diffusion (Turing Patterns)"
    group = "Nature-Inspired"

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.FloatSlider(value=0.055, min=0.010, max=0.100, step=0.001,
                                description="Feed Rate:", readout_format=".3f"),
            widgets.FloatSlider(value=0.062, min=0.040, max=0.080, step=0.001,
                                description="Kill Rate:", readout_format=".3f"),
            widgets.IntSlider(value=2000, min=200, max=5000, step=100,
                              description="Iterations:"),
            widgets.IntSlider(value=42, min=0, max=999,
                              description="Seed:"),
        ]

    def render(self, resolution="Low", palette="Inferno", speed=1.0, **kwargs):
        f      = float(kwargs.get("feed_rate", 0.055))
        k      = float(kwargs.get("kill_rate", 0.062))
        n_iter = int(kwargs.get("iterations", 2000))
        seed   = int(kwargs.get("seed", 42))
        rng    = np.random.default_rng(seed)

        N = {"Low": 100, "Medium": 150, "High": 200}.get(resolution, 100)
        Da, Db, dt = 1.0, 0.5, 1.0

        # Initialize: A=1 everywhere, B=0; seed random small patches
        A = np.ones((N, N))
        B = np.zeros((N, N))
        n_seeds = int(rng.integers(5, 14))
        for _ in range(n_seeds):
            r0 = int(rng.integers(5, N - 5))
            c0 = int(rng.integers(5, N - 5))
            hw = int(rng.integers(2, 6))
            A[r0 - hw:r0 + hw, c0 - hw:c0 + hw] = 0.50 + rng.uniform(-0.05, 0.05)
            B[r0 - hw:r0 + hw, c0 - hw:c0 + hw] = 0.25 + rng.uniform(-0.05, 0.05)

        # Gray-Scott iteration — 5-point Laplacian via np.roll (periodic BC)
        for _ in range(n_iter):
            lapA = (np.roll(A, 1, 0) + np.roll(A, -1, 0) +
                    np.roll(A, 1, 1) + np.roll(A, -1, 1) - 4.0 * A)
            lapB = (np.roll(B, 1, 0) + np.roll(B, -1, 0) +
                    np.roll(B, 1, 1) + np.roll(B, -1, 1) - 4.0 * B)
            ABB = A * B * B
            A += dt * (Da * lapA - ABB + f * (1.0 - A))
            B += dt * (Db * lapB + ABB - (f + k) * B)
            np.clip(A, 0.0, 1.0, out=A)
            np.clip(B, 0.0, 1.0, out=B)

        cmap = ColorUtils.make_colormap(palette)
        fig, ax = self._create_figure(figsize=(8, 8))
        bmax = B.max() if B.max() > 0 else 1.0
        ax.imshow(B, cmap=cmap, origin="lower", interpolation="bilinear",
                  vmin=0, vmax=bmax)
        ax.set_title(f"Reaction-Diffusion  f={f:.3f}  k={k:.3f}",
                     color="#e0e0e0", fontsize=13, pad=8)
        ax.axis("off")
        plt.tight_layout()
        plt.show()
        plt.close(fig)


# ── Pattern 24 ────────────────────────────────────────────────────────────────

class FlockingBirdsRenderer(BasePattern):
    """Pattern 24 — Flocking Birds (Boids Lite), fully vectorized."""
    name = "Flocking Birds (Boids Lite)"
    group = "Nature-Inspired"

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=120, min=20, max=300, step=10,
                              description="N Boids:"),
            widgets.FloatSlider(value=1.5, min=0.0, max=5.0, step=0.1,
                                description="Sep Weight:", readout_format=".1f"),
            widgets.FloatSlider(value=1.0, min=0.0, max=5.0, step=0.1,
                                description="Ali Weight:", readout_format=".1f"),
            widgets.FloatSlider(value=1.0, min=0.0, max=5.0, step=0.1,
                                description="Coh Weight:", readout_format=".1f"),
            widgets.IntSlider(value=42, min=0, max=999,
                              description="Seed:"),
        ]

    def render(self, resolution="Low", palette="Inferno", speed=1.0, **kwargs):
        N       = int(kwargs.get("n_boids", 120))
        w_sep   = float(kwargs.get("sep_weight", 1.5))
        w_ali   = float(kwargs.get("ali_weight", 1.0))
        w_coh   = float(kwargs.get("coh_weight", 1.0))
        seed    = int(kwargs.get("seed", 42))
        rng     = np.random.default_rng(seed)

        n_steps   = 200
        max_speed = 0.008
        sep_r, ali_r, coh_r = 0.05, 0.10, 0.15

        pos    = rng.uniform(0, 1, (N, 2))
        angles = rng.uniform(0, 2 * np.pi, N)
        vel    = np.column_stack([np.cos(angles), np.sin(angles)]) * max_speed * 0.5

        for _ in range(n_steps):
            # Pairwise difference + minimum-image periodic wrapping
            diff = pos[:, None] - pos[None]        # (N, N, 2)
            diff -= np.round(diff)
            dist = np.sqrt((diff ** 2).sum(axis=-1))   # (N, N)
            np.fill_diagonal(dist, np.inf)

            # Separation: steer away from close neighbors
            sep_mask = (dist < sep_r)[:, :, None]     # (N, N, 1)
            sep_force = (diff * sep_mask).sum(axis=1)  # (N, 2)
            sep_n = np.linalg.norm(sep_force, axis=-1, keepdims=True)
            sep_force = np.where(sep_n > 0,
                                 sep_force / np.maximum(sep_n, 1e-8), 0.0)

            # Alignment: match velocity of neighbors in range
            ali_mask = (dist < ali_r)[:, :, None]
            ali_count = ali_mask.sum(axis=1)           # (N, 1)
            ali_sum = (vel[None] * ali_mask).sum(axis=1)   # (N, 2)
            ali_vel = np.where(ali_count > 0,
                               ali_sum / np.maximum(ali_count, 1), 0.0)
            ali_n = np.linalg.norm(ali_vel, axis=-1, keepdims=True)
            ali_force = np.where(ali_n > 0,
                                 ali_vel / np.maximum(ali_n, 1e-8), 0.0)

            # Cohesion: steer toward center of mass of neighbors
            coh_mask = (dist < coh_r)[:, :, None]
            coh_count = coh_mask.sum(axis=1)
            coh_sum = (pos[None] * coh_mask).sum(axis=1)
            coh_com = np.where(coh_count > 0,
                               coh_sum / np.maximum(coh_count, 1), pos)
            to_com = coh_com - pos
            coh_n = np.linalg.norm(to_com, axis=-1, keepdims=True)
            coh_force = np.where(coh_n > 1e-8,
                                 to_com / np.maximum(coh_n, 1e-8), 0.0)

            vel += (w_sep * sep_force + w_ali * ali_force + w_coh * coh_force) * max_speed
            speeds = np.linalg.norm(vel, axis=-1, keepdims=True)
            vel    = vel / np.maximum(speeds, 1e-8) * np.minimum(speeds, max_speed)
            pos    = (pos + vel) % 1.0

        # ── Visualize final frame ────────────────────────────────────────────
        cmap = ColorUtils.make_colormap(palette)
        fig, ax = self._create_figure(figsize=(8, 8), bg_color="#030810")

        speeds_f = np.linalg.norm(vel, axis=-1)
        sp_min, sp_rng = speeds_f.min(), speeds_f.max() - speeds_f.min()
        t_vals = (speeds_f - sp_min) / (sp_rng + 1e-8)
        colors = cmap(t_vals)

        u = vel[:, 0].copy()
        v_q = vel[:, 1].copy()
        norms = np.sqrt(u ** 2 + v_q ** 2)
        norms = np.maximum(norms, 1e-8)
        u /= norms
        v_q /= norms

        ax.quiver(pos[:, 0], pos[:, 1], u, v_q,
                  color=colors, scale=35, width=0.003,
                  headwidth=4, headlength=5, alpha=0.9)

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        ax.set_title(f"Flocking Birds (Boids)  N={N}", color="#b0d0f0",
                     fontsize=13, pad=8)
        plt.tight_layout()
        plt.show()
        plt.close(fig)


# ── Pattern 25 ────────────────────────────────────────────────────────────────

class LightningBoltRenderer(BasePattern):
    """Pattern 25 — Lightning Bolt Generator (recursive midpoint displacement)."""
    name = "Lightning Bolt Generator"
    group = "Nature-Inspired"

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.FloatSlider(value=0.35, min=0.05, max=0.80, step=0.02,
                                description="Roughness:", readout_format=".2f"),
            widgets.IntSlider(value=8, min=4, max=12, step=1,
                              description="Depth:"),
            widgets.FloatSlider(value=0.25, min=0.0, max=0.6, step=0.02,
                                description="Branch Prob:", readout_format=".2f"),
            widgets.IntSlider(value=42, min=0, max=999,
                              description="Seed:"),
        ]

    def render(self, resolution="Low", palette="Inferno", speed=1.0, **kwargs):
        roughness   = float(kwargs.get("roughness", 0.35))
        depth       = int(kwargs.get("depth", 8))
        branch_prob = float(kwargs.get("branch_prob", 0.25))
        seed        = int(kwargs.get("seed", 42))
        rng         = np.random.default_rng(seed)

        fig, ax = self._create_figure(figsize=(6, 9), bg_color="#020510")

        start = np.array([rng.uniform(0.3, 0.7), 0.95])
        end   = np.array([rng.uniform(0.3, 0.7), 0.05])

        all_segs = []   # (p1, p2, intensity)

        def _bolt(p1, p2, d, intensity):
            if d == 0:
                all_segs.append((p1.copy(), p2.copy(), intensity))
                return
            mid = (p1 + p2) / 2.0
            perp = np.array([-(p2[1] - p1[1]), p2[0] - p1[0]])
            plen = np.linalg.norm(perp)
            if plen > 0:
                perp /= plen
            disp = roughness * np.linalg.norm(p2 - p1) * rng.uniform(-1, 1)
            mid  = mid + perp * disp
            _bolt(p1, mid, d - 1, intensity)
            _bolt(mid, p2, d - 1, intensity)
            if rng.random() < branch_prob and d < depth - 1:
                bdir = (p2 - mid) * rng.uniform(0.5, 1.5) + \
                       perp * rng.uniform(-0.8, 0.8) * 0.25
                branch_end = np.clip(mid + bdir, 0.02, 0.98)
                _bolt(mid.copy(), branch_end, max(0, d - 2), intensity * 0.45)

        _bolt(start, end, depth, 1.0)

        for p1, p2, intensity in all_segs:
            lw    = max(0.3, intensity * 2.5)
            alpha = min(1.0, intensity * 0.9 + 0.1)
            col   = (0.70 + 0.30 * intensity, 0.80 + 0.20 * intensity, 1.0)
            # Core bolt
            ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=col, lw=lw,
                    alpha=alpha, solid_capstyle="round", zorder=2)
            # Soft glow halo
            ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=(0.4, 0.5, 1.0),
                    lw=lw * 5, alpha=alpha * 0.12, solid_capstyle="round", zorder=1)

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        ax.set_title("Lightning Bolt Generator", color="#c8d8ff", fontsize=13, pad=8)
        plt.tight_layout()
        plt.show()
        plt.close(fig)


# ── Pattern 26 ────────────────────────────────────────────────────────────────

class SnowflakeCrystalRenderer(BasePattern):
    """Pattern 26 — Snowflake Crystal Growth (6-fold recursive arms)."""
    name = "Snowflake Crystal Growth"
    group = "Nature-Inspired"

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=6, min=2, max=10, step=1,
                              description="Depth:"),
            widgets.FloatSlider(value=0.45, min=0.25, max=0.70, step=0.02,
                                description="Branch Scale:", readout_format=".2f"),
            widgets.FloatSlider(value=0.55, min=0.30, max=0.80, step=0.02,
                                description="Arm Scale:", readout_format=".2f"),
            widgets.IntSlider(value=42, min=0, max=999,
                              description="Seed:"),
        ]

    def render(self, resolution="Low", palette="Inferno", speed=1.0, **kwargs):
        depth        = int(kwargs.get("depth", 6))
        branch_scale = float(kwargs.get("branch_scale", 0.45))
        arm_scale    = float(kwargs.get("arm_scale", 0.55))
        seed         = int(kwargs.get("seed", 42))
        rng          = np.random.default_rng(seed)

        cmap = ColorUtils.make_colormap(palette)
        fig, ax = self._create_figure(figsize=(8, 8), bg_color="#04080f")

        cx, cy     = 0.5, 0.5
        arm_length = 0.38
        # Per-depth jitter for organic variation (seeded so reproducible)
        branch_off = rng.uniform(0.88, 1.12, depth + 2) * (np.pi / 3)

        seg_list, t_list, lw_list = [], [], []

        def _arm(x, y, angle, length, d):
            if d == 0 or length < 0.004:
                return
            x2 = x + length * np.cos(angle)
            y2 = y + length * np.sin(angle)
            t  = 1.0 - d / (depth + 1)
            seg_list.append([[x, y], [x2, y2]])
            t_list.append(t)
            lw_list.append(max(0.3, (1.0 - t) * 3.8 + 0.3))

            # Side branches at ±(π/3 + jitter) from midpoint of this segment
            if d >= 1:
                boff = branch_off[d]
                bx   = x + length * 0.5 * np.cos(angle)
                by   = y + length * 0.5 * np.sin(angle)
                for sign in (+1, -1):
                    _arm(bx, by, angle + sign * boff,
                         length * branch_scale, d - 1)

            # Continue main arm
            _arm(x2, y2, angle, length * arm_scale, d - 1)

        for k in range(6):
            _arm(cx, cy, k * np.pi / 3, arm_length, depth)

        if seg_list:
            colors = cmap(np.array(t_list))
            lc = mc.LineCollection(seg_list, colors=colors,
                                   linewidths=lw_list, alpha=0.95,
                                   capstyle="round")
            ax.add_collection(lc)

        # Faint glow overlay (wider, lower alpha)
        if seg_list:
            lc_glow = mc.LineCollection(seg_list,
                                        colors=[(0.7, 0.9, 1.0, 0.06)] * len(seg_list),
                                        linewidths=[lw * 5 for lw in lw_list],
                                        capstyle="round")
            ax.add_collection(lc_glow)

        # Central dot
        ax.plot(cx, cy, "o", color="#ffffff", ms=3, zorder=5)

        ax.set_xlim(0.05, 0.95)
        ax.set_ylim(0.05, 0.95)
        ax.axis("off")
        ax.set_title("Snowflake Crystal Growth", color="#c0e8ff", fontsize=13, pad=8)
        plt.tight_layout()
        plt.show()
        plt.close(fig)


# ── Pattern 27 ────────────────────────────────────────────────────────────────

class LeafVenationRenderer(BasePattern):
    """Pattern 27 — Leaf Venation Simulation (space colonisation algorithm)."""
    name = "Leaf Venation Simulation"
    group = "Nature-Inspired"

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=250, min=50, max=600, step=25,
                              description="N Attractors:"),
            widgets.IntSlider(value=60, min=20, max=150, step=10,
                              description="Iterations:"),
            widgets.FloatSlider(value=0.040, min=0.010, max=0.120, step=0.005,
                                description="Kill Dist:", readout_format=".3f"),
            widgets.FloatSlider(value=0.015, min=0.005, max=0.040, step=0.002,
                                description="Step Size:", readout_format=".3f"),
            widgets.IntSlider(value=42, min=0, max=999,
                              description="Seed:"),
        ]

    def render(self, resolution="Low", palette="Inferno", speed=1.0, **kwargs):
        n_attr = int(kwargs.get("n_attractors", 250))
        n_iter = int(kwargs.get("iterations", 60))
        kill_d = float(kwargs.get("kill_dist", 0.040))
        step   = float(kwargs.get("step_size", 0.015))
        seed   = int(kwargs.get("seed", 42))
        rng    = np.random.default_rng(seed)

        # ── Leaf shape: vertical ellipse ──────────────────────────────────────
        a_ax, b_ax = 0.30, 0.44   # semi-axes (x, y)
        cx_l, cy_l = 0.50, 0.52

        # Sample attractor points uniformly inside the ellipse
        attr_list, tries = [], 0
        while len(attr_list) < n_attr and tries < n_attr * 20:
            px = rng.uniform(cx_l - a_ax, cx_l + a_ax)
            py = rng.uniform(cy_l - b_ax, cy_l + b_ax)
            if ((px - cx_l) / a_ax) ** 2 + ((py - cy_l) / b_ax) ** 2 < 1.0:
                attr_list.append([px, py])
            tries += 1
        attractors = np.array(attr_list, dtype=float) if attr_list else np.empty((0, 2))

        # Root node at stem base (bottom of ellipse)
        nodes   = [np.array([0.50, cy_l - b_ax])]
        parents = [-1]

        for _ in range(n_iter):
            if len(attractors) == 0:
                break
            nodes_arr = np.array(nodes)

            # Distance from each attractor to every node: (A, N) matrix
            diff_an = attractors[:, None] - nodes_arr[None]   # (A, N, 2)
            D       = np.sqrt((diff_an ** 2).sum(axis=-1))    # (A, N)
            closest = np.argmin(D, axis=1)                    # (A,)
            min_D   = D[np.arange(len(attractors)), closest]

            # Remove attractors within kill distance
            alive      = min_D > kill_d
            attractors = attractors[alive]
            closest    = closest[alive]
            if len(attractors) == 0:
                break

            # Accumulate normalised growth directions per node
            n_nodes  = len(nodes)
            growth   = np.zeros((n_nodes, 2))
            count    = np.zeros(n_nodes)
            for ai, ni in zip(range(len(attractors)), closest):
                d_vec = attractors[ai] - nodes[ni]
                norm  = np.linalg.norm(d_vec)
                if norm > 1e-8:
                    growth[ni] += d_vec / norm
                    count[ni]  += 1

            # Grow one new node per active node in this iteration
            new_positions, new_parents = [], []
            for ni in np.where(count > 0)[0]:
                dir_vec = growth[ni] / count[ni]
                norm    = np.linalg.norm(dir_vec)
                if norm < 1e-8:
                    continue
                dir_vec /= norm
                new_pos = nodes[ni] + dir_vec * step
                if (((new_pos[0] - cx_l) / a_ax) ** 2
                        + ((new_pos[1] - cy_l) / b_ax) ** 2) < 1.0:
                    new_positions.append(new_pos.copy())
                    new_parents.append(int(ni))

            nodes.extend(new_positions)
            parents.extend(new_parents)

        # ── Render venation network ──────────────────────────────────────────
        cmap = ColorUtils.make_colormap(palette)
        fig, ax = self._create_figure(figsize=(7, 9), bg_color="#060c04")

        # Leaf outline
        theta = np.linspace(0, 2 * np.pi, 300)
        ox = cx_l + a_ax * np.cos(theta)
        oy = cy_l + b_ax * np.sin(theta)
        ax.fill(ox, oy, color="#0a1a08", alpha=0.55, zorder=0)
        ax.plot(ox, oy, color="#1c3818", lw=1.2, alpha=0.65, zorder=1)

        if len(nodes) > 1:
            # Depth-first depth calculation
            depth_map = [0] * len(nodes)
            for i in range(1, len(nodes)):
                depth_map[i] = depth_map[parents[i]] + 1
            max_d = max(depth_map) if max(depth_map) > 0 else 1

            seg_list, t_list, lw_list = [], [], []
            for i in range(1, len(nodes)):
                p = nodes[parents[i]]
                c = nodes[i]
                t = depth_map[i] / max_d
                seg_list.append([[p[0], p[1]], [c[0], c[1]]])
                t_list.append(t)
                lw_list.append(max(0.3, 2.2 * (1.0 - t * 0.8)))

            colors = cmap(0.15 + 0.85 * np.array(t_list))
            lc = mc.LineCollection(seg_list, colors=colors,
                                   linewidths=lw_list, alpha=0.85, zorder=2)
            ax.add_collection(lc)

        # Stem line below leaf
        ax.plot([0.50, 0.50], [0.0, cy_l - b_ax + 0.01],
                color="#2a4a20", lw=2.0, alpha=0.7, zorder=1)

        ax.set_xlim(0.12, 0.88)
        ax.set_ylim(0.0, 0.98)
        ax.axis("off")
        ax.set_title("Leaf Venation Simulation", color="#90c878", fontsize=13, pad=8)
        plt.tight_layout()
        plt.show()
        plt.close(fig)


# ── Pattern 28 ────────────────────────────────────────────────────────────────

class FireParticleRenderer(BasePattern):
    """Pattern 28 — Fire Particle System."""
    name = "Fire Particle System"
    group = "Nature-Inspired"

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=3000, min=500, max=8000, step=200,
                              description="Particles:"),
            widgets.FloatSlider(value=0.70, min=0.20, max=1.50, step=0.05,
                                description="Heat:", readout_format=".2f"),
            widgets.FloatSlider(value=0.35, min=0.00, max=1.00, step=0.05,
                                description="Turbulence:", readout_format=".2f"),
            widgets.IntSlider(value=42, min=0, max=999, description="Seed:"),
        ]

    def render(self, resolution="Low", palette="Inferno", speed=1.0, **kwargs):
        n    = int(kwargs.get("particles", 3000))
        heat = float(kwargs.get("heat", 0.70))
        turb = float(kwargs.get("turbulence", 0.35))
        seed = int(kwargs.get("seed", 42))
        rng  = np.random.default_rng(seed)

        # age ∈ [0,1]: 0 = just born (hot, at base), 1 = dying (cool, at top).
        # Beta(1, 2.5) skews toward young particles — base of fire is densest.
        age = rng.beta(1.0, 2.5, n)

        # Horizontal: spreads with age and turbulence
        px = rng.normal(0.5, 0.05 + turb * 0.12 * age, n)
        px = np.clip(px, 0.04, 0.96)

        # Vertical: rises with age; heat scales max height
        py = age * (0.70 + heat * 0.22) + rng.normal(0, 0.014, n)
        py = np.clip(py, 0.0, 0.97)

        # Temperature colour: 0 = dark red, 0.5 = orange, 0.8 = yellow, 1 = white
        temp = np.clip(1.0 - age, 0.0, 1.0)
        r_ch = np.ones(n)
        g_ch = np.clip(temp * 1.9, 0.0, 1.0)
        b_ch = np.clip((temp - 0.65) * 3.0, 0.0, 1.0)
        a_ch = np.clip((1.0 - age * 0.75) * rng.uniform(0.5, 1.0, n), 0.05, 1.0)
        sizes = np.clip((1.0 - age) * heat * 90 + rng.uniform(1, 12, n), 1, 250)
        colors = np.column_stack([r_ch, g_ch, b_ch, a_ch])

        fig, ax = self._create_figure(figsize=(6, 9), bg_color="#030202")

        # Ember cluster at base — very hot, tight spread
        n_emb = n // 6
        ex = np.clip(rng.normal(0.5, 0.04, n_emb), 0.12, 0.88)
        ey = rng.uniform(0.0, 0.04, n_emb)
        er = np.ones(n_emb)
        eg = rng.uniform(0.75, 1.0, n_emb)
        eb = rng.uniform(0.0, 0.35, n_emb)
        ea = np.full(n_emb, 0.90)
        ember_c = np.column_stack([er, eg, eb, ea])
        ax.scatter(ex, ey, s=rng.uniform(10, 55, n_emb), c=ember_c,
                   linewidths=0, zorder=3)

        # Main fire body
        ax.scatter(px, py, s=sizes, c=colors, linewidths=0, zorder=2)

        ax.set_xlim(0.05, 0.95)
        ax.set_ylim(0.0, 1.0)
        ax.axis("off")
        ax.set_title("Fire Particle System", color="#ff7030", fontsize=13, pad=8)
        plt.tight_layout()
        plt.show()
        plt.close(fig)


# ── Pattern 29 ────────────────────────────────────────────────────────────────

class GalaxySpiralRenderer(BasePattern):
    """Pattern 29 — Galaxy Spiral Arms (logarithmic spiral)."""
    name = "Galaxy Spiral Arms"
    group = "Nature-Inspired"

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=3, min=1, max=6, step=1,
                              description="Arms:"),
            widgets.FloatSlider(value=1.2, min=0.5, max=3.0, step=0.1,
                                description="Winding:", readout_format=".1f"),
            widgets.IntSlider(value=5000, min=1000, max=12000, step=500,
                              description="N Stars:"),
            widgets.IntSlider(value=42, min=0, max=999, description="Seed:"),
        ]

    def render(self, resolution="Low", palette="Inferno", speed=1.0, **kwargs):
        n_arms  = int(kwargs.get("arms", 3))
        winding = float(kwargs.get("winding", 1.2))
        n_stars = int(kwargs.get("n_stars", 5000))
        seed    = int(kwargs.get("seed", 42))
        rng     = np.random.default_rng(seed)

        # Logarithmic spiral: r = r0 * exp(b * theta)
        # theta_max = winding * 3π  →  winding=1 gives 1.5 turns, 2 gives 3 turns.
        # b is chosen so r grows from r0=0.01 to r_max=0.46 over [0, theta_max].
        r0, r_max = 0.010, 0.460
        theta_max = winding * 3.0 * np.pi
        b_param = np.log(r_max / r0) / theta_max

        fig, ax = self._create_figure(figsize=(8, 8), bg_color="#01020a")

        all_x, all_y, all_t = [], [], []
        n_per_arm = n_stars // n_arms

        for arm in range(n_arms):
            arm_offset = arm * 2.0 * np.pi / n_arms
            t = rng.uniform(0.0, 1.0, n_per_arm)   # position along arm (0=inner)
            theta = t * theta_max
            r = np.clip(r0 * np.exp(b_param * theta), 0.0, r_max)

            x = r * np.cos(theta + arm_offset) + 0.5
            y = r * np.sin(theta + arm_offset) + 0.5

            # Gaussian spread perpendicular to arm tangent (wider toward outer edge)
            spread = rng.normal(0, 0.004 + t * 0.020, n_per_arm)
            perp_x = -np.sin(theta + arm_offset) * spread
            perp_y =  np.cos(theta + arm_offset) * spread
            all_x.append(x + perp_x)
            all_y.append(y + perp_y)
            all_t.append(t)

        # Central bulge: compact spherical distribution
        n_bulge = n_stars // 2
        br = np.abs(rng.normal(0, 0.042, n_bulge))
        ba = rng.uniform(0, 2 * np.pi, n_bulge)
        all_x.append(br * np.cos(ba) + 0.5)
        all_y.append(br * np.sin(ba) + 0.5)
        all_t.append(np.zeros(n_bulge))   # bulge stars → inner colour (t=0)

        sx = np.concatenate(all_x)
        sy = np.concatenate(all_y)
        sc = np.concatenate(all_t)

        mask = (sx > 0.01) & (sx < 0.99) & (sy > 0.01) & (sy < 0.99)
        sx, sy, sc = sx[mask], sy[mask], sc[mask]

        # Colour gradient: inner warm yellow-white → outer cool blue-white
        r_col = np.clip(1.00 - sc * 0.30, 0.5, 1.0)
        g_col = np.clip(0.90 - sc * 0.35, 0.4, 1.0)
        b_col = np.clip(0.60 + sc * 0.40, 0.5, 1.0)
        a_col = np.clip(rng.uniform(0.3, 1.0, len(sx)), 0.1, 1.0)
        star_colors = np.column_stack([r_col, g_col, b_col, a_col])
        sizes = rng.uniform(0.5, 9, len(sx)) * (1.0 - sc * 0.55)

        ax.scatter(sx, sy, s=sizes, c=star_colors, linewidths=0)

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title("Galaxy Spiral Arms", color="#b0baff", fontsize=13, pad=8)
        plt.tight_layout()
        plt.show()
        plt.close(fig)


# ── Pattern 30 ────────────────────────────────────────────────────────────────

class AuroraBorealisRenderer(BasePattern):
    """Pattern 30 — Aurora Borealis (sinusoidal curtain layers on raster image)."""
    name = "Aurora Borealis"
    group = "Nature-Inspired"

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=5, min=2, max=10, step=1,
                              description="Curtains:"),
            widgets.FloatSlider(value=3.0, min=1.0, max=8.0, step=0.5,
                                description="Wave Freq:", readout_format=".1f"),
            widgets.FloatSlider(value=0.70, min=0.10, max=1.50, step=0.10,
                                description="Intensity:", readout_format=".1f"),
            widgets.IntSlider(value=42, min=0, max=999, description="Seed:"),
        ]

    def render(self, resolution="Low", palette="Inferno", speed=1.0, **kwargs):
        n_curtains = int(kwargs.get("curtains", 5))
        freq   = float(kwargs.get("wave_freq", 3.0))
        intens = float(kwargs.get("intensity", 0.70))
        seed   = int(kwargs.get("seed", 42))
        rng    = np.random.default_rng(seed)

        H = W = {"Low": 256, "Medium": 400, "High": 512}.get(resolution, 256)

        # Aurora colour palette: classic polar spectrum
        aurora_palette = np.array([
            [0.00, 1.00, 0.40],   # bright green
            [0.00, 0.80, 0.90],   # teal
            [0.10, 0.30, 1.00],   # blue
            [0.70, 0.00, 1.00],   # purple
            [1.00, 0.00, 0.60],   # magenta
            [0.00, 0.90, 0.60],   # cyan-green
        ])

        img = np.zeros((H, W, 3), dtype=float)
        x_idx = np.arange(W, dtype=float)
        y_idx = np.arange(H, dtype=float)

        for _ in range(n_curtains):
            color = aurora_palette[rng.integers(0, len(aurora_palette))]

            # Curtain top edge: primary + secondary sinusoidal wave
            center_y = rng.uniform(0.20, 0.60) * H
            amp      = rng.uniform(0.04, 0.10) * H
            phase    = rng.uniform(0, 2 * np.pi)
            f2       = freq * rng.uniform(0.7, 1.4)

            wave = (center_y
                    + amp * np.sin(2 * np.pi * f2 * x_idx / W + phase)
                    + amp * 0.4 * np.sin(2 * np.pi * f2 * 2.3 * x_idx / W + phase * 1.7))

            # Curtain length (downward fade distance in pixels)
            c_len = rng.uniform(0.12, 0.32) * H

            # dy[row, col] = pixel_row - wave_top[col]  (H×W)
            dy = y_idx[:, None] - wave[None, :]
            curtain = np.where(dy >= 0, np.exp(-dy / (c_len + 1e-6)), 0.0)
            curtain *= intens * rng.uniform(0.5, 1.0)

            # Shimmer: slight horizontal brightness modulation
            shimmer = 0.5 + 0.5 * np.sin(2 * np.pi * f2 * 1.8 * x_idx / W + phase * 0.7)
            curtain *= shimmer[None, :]

            img += curtain[:, :, None] * color[None, None, :]

        # Tone-map: normalise then gamma-brighten
        img = np.clip(img, 0, None)
        mx = img.max()
        if mx > 0:
            img /= mx
        img = np.power(img, 0.55)
        img = np.clip(img, 0, 1)

        # Sparse starfield
        n_stars = 300
        sy = rng.integers(0, H, n_stars)
        sx = rng.integers(0, W, n_stars)
        sb = rng.uniform(0.5, 1.0, n_stars)
        for i in range(n_stars):
            img[sy[i], sx[i]] = np.maximum(img[sy[i], sx[i]], sb[i])

        fig, ax = self._create_figure(figsize=(10, 6), bg_color="#010208")
        ax.imshow(img, origin="upper", aspect="auto")
        ax.axis("off")
        ax.set_title("Aurora Borealis", color="#80ffb0", fontsize=13, pad=8)
        plt.tight_layout()
        plt.show()
        plt.close(fig)


# ── Pattern 31 ────────────────────────────────────────────────────────────────

class UnderwaterCausticsRenderer(BasePattern):
    """Pattern 31 — Underwater Caustics (random-direction wave interference)."""
    name = "Underwater Caustics"
    group = "Nature-Inspired"

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=12, min=4, max=30, step=2,
                              description="N Sources:"),
            widgets.FloatSlider(value=18.0, min=5.0, max=40.0, step=1.0,
                                description="Frequency:", readout_format=".1f"),
            widgets.FloatSlider(value=2.5, min=1.0, max=5.0, step=0.1,
                                description="Sharpness:", readout_format=".1f"),
            widgets.IntSlider(value=42, min=0, max=999, description="Seed:"),
        ]

    def render(self, resolution="Low", palette="Inferno", speed=1.0, **kwargs):
        n_src = int(kwargs.get("n_sources", 12))
        freq  = float(kwargs.get("frequency", 18.0))
        sharp = float(kwargs.get("sharpness", 2.5))
        seed  = int(kwargs.get("seed", 42))
        rng   = np.random.default_rng(seed)

        N = {"Low": 300, "Medium": 450, "High": 600}.get(resolution, 300)
        x = np.linspace(0, 1, N)
        y = np.linspace(0, 1, N)
        X, Y = np.meshgrid(x, y)

        # Sum cosine waves from random directions — interference mimics refraction
        field = np.zeros((N, N))
        for _ in range(n_src):
            angle = rng.uniform(0, 2 * np.pi)
            kx    = np.cos(angle) * freq * 2 * np.pi
            ky    = np.sin(angle) * freq * 2 * np.pi
            phase = rng.uniform(0, 2 * np.pi)
            field += np.cos(kx * X + ky * Y + phase)

        # Normalise to [0, 1] then power-map to sharpen caustic bright spots
        field = (field - field.min()) / (field.max() - field.min() + 1e-8)
        field = np.power(field, sharp)

        # Deep-water blue-teal RGB mapping
        r_ch = np.clip(field * 0.75 + 0.05, 0, 1)
        g_ch = np.clip(field * 0.70 + 0.25, 0, 1)
        b_ch = np.clip(field * 0.45 + 0.45, 0, 1)
        img  = np.stack([r_ch, g_ch, b_ch], axis=-1)

        fig, ax = self._create_figure(figsize=(8, 8), bg_color="#000a14")
        ax.imshow(img, origin="lower", interpolation="bilinear", aspect="equal")
        ax.axis("off")
        ax.set_title(f"Underwater Caustics  sources={n_src}",
                     color="#80d0e8", fontsize=13, pad=8)
        plt.tight_layout()
        plt.show()
        plt.close(fig)


# ── Pattern 32 ────────────────────────────────────────────────────────────────

class SandDuneRenderer(BasePattern):
    """Pattern 32 — Sand Dune Erosion (cellular automaton saltation model)."""
    name = "Sand Dune Erosion"
    group = "Nature-Inspired"

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=150, min=30, max=400, step=10,
                              description="Iterations:"),
            widgets.FloatSlider(value=0.15, min=0.01, max=0.50, step=0.01,
                                description="Wind Speed:", readout_format=".2f"),
            widgets.FloatSlider(value=0.30, min=0.05, max=0.60, step=0.02,
                                description="Avalanche:", readout_format=".2f"),
            widgets.IntSlider(value=42, min=0, max=999, description="Seed:"),
        ]

    def render(self, resolution="Low", palette="Inferno", speed=1.0, **kwargs):
        n_iter   = int(kwargs.get("iterations", 150))
        wind     = float(kwargs.get("wind_speed", 0.15))
        av_thresh = float(kwargs.get("avalanche", 0.30))
        seed     = int(kwargs.get("seed", 42))
        rng      = np.random.default_rng(seed)

        N = {"Low": 100, "Medium": 150, "High": 200}.get(resolution, 100)

        # Initial heightfield: random noise + a few pre-formed ridges
        h = rng.uniform(0.0, 0.4, (N, N))
        for _ in range(rng.integers(3, 8)):
            cx = rng.integers(N // 4, 3 * N // 4)
            h[:, max(0, cx - 4):cx + 4] += rng.uniform(0.2, 0.6)
        h = np.clip(h, 0, 1)

        for _ in range(n_iter):
            # ── Saltation: carry a fraction of each cell's height rightward ──
            q = h * wind * 0.12
            h = h - q + np.roll(q, 1, axis=1)   # cell j receives from j-1

            # ── Avalanche: redistribute excess slope (angle-of-repose rule) ──
            # Right-facing slope
            slope_r  = h - np.roll(h, -1, axis=1)   # h[j] - h[j+1]
            excess_r = np.clip(slope_r - av_thresh, 0, None)
            tr       = excess_r * 0.5
            h        = h - tr + np.roll(tr, 1, axis=1)   # j+1 receives from j

            # Down-facing slope
            slope_d  = h - np.roll(h, -1, axis=0)
            excess_d = np.clip(slope_d - av_thresh, 0, None)
            td       = excess_d * 0.5
            h        = h - td + np.roll(td, 1, axis=0)

            h = np.clip(h, 0, None)

        # Normalise and map to a sandy palette
        h = (h - h.min()) / (h.max() - h.min() + 1e-8)
        r_ch = 0.40 + h * 0.55
        g_ch = 0.28 + h * 0.52
        b_ch = 0.08 + h * 0.38
        img  = np.clip(np.stack([r_ch, g_ch, b_ch], axis=-1), 0, 1)

        fig, ax = self._create_figure(figsize=(9, 7), bg_color="#1a1000")
        ax.imshow(img, origin="lower", interpolation="bilinear", aspect="auto")
        ax.axis("off")
        ax.set_title(f"Sand Dune Erosion  iters={n_iter}",
                     color="#e8c870", fontsize=13, pad=8)
        plt.tight_layout()
        plt.show()
        plt.close(fig)


# ── Pattern 33 ────────────────────────────────────────────────────────────────

class CoralReefRenderer(BasePattern):
    """Pattern 33 — Coral Reef Growth (multi-colony recursive branching)."""
    name = "Coral Reef Growth"
    group = "Nature-Inspired"

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=8, min=3, max=12, step=1,
                              description="Depth:"),
            widgets.IntSlider(value=5, min=2, max=8, step=1,
                              description="N Colonies:"),
            widgets.FloatSlider(value=0.55, min=0.25, max=0.85, step=0.02,
                                description="Fan Spread:", readout_format=".2f"),
            widgets.IntSlider(value=42, min=0, max=999, description="Seed:"),
        ]

    def render(self, resolution="Low", palette="Inferno", speed=1.0, **kwargs):
        depth      = int(kwargs.get("depth", 8))
        n_colonies = int(kwargs.get("n_colonies", 5))
        fan_spread = float(kwargs.get("fan_spread", 0.55))
        seed       = int(kwargs.get("seed", 42))
        rng        = np.random.default_rng(seed)

        # Species colour palettes: [trunk, mid, tip]
        coral_palettes = [
            ["#cc3300", "#ff6633", "#ffaa80"],   # orange fire coral
            ["#cc2266", "#ff44aa", "#ffaadd"],   # pink coral
            ["#0077aa", "#22aadd", "#88ddff"],   # blue coral
            ["#886633", "#ccaa55", "#eedd99"],   # tan brain coral
            ["#226633", "#44aa66", "#88dd99"],   # green staghorn
            ["#880088", "#cc44cc", "#ffaaff"],   # purple sea fan
        ]

        fig, ax = self._create_figure(figsize=(9, 8), bg_color="#010d1a")
        seg_list, col_list, lw_list = [], [], []

        for col_i in range(n_colonies):
            pal        = coral_palettes[col_i % len(coral_palettes)]
            root_x     = rng.uniform(0.07, 0.93)
            root_y     = rng.uniform(0.00, 0.12)
            base_angle = np.pi / 2 + rng.uniform(-0.35, 0.35)
            init_len   = rng.uniform(0.06, 0.13)

            def _coral(x, y, angle, length, d, _pal=pal):
                if d == 0 or length < 0.004:
                    return
                x2 = x + length * np.cos(angle)
                y2 = y + length * np.sin(angle)
                t  = 1.0 - d / depth
                c_idx = min(int(t * len(_pal)), len(_pal) - 1)
                seg_list.append([[x, y], [x2, y2]])
                col_list.append(_pal[c_idx])
                lw_list.append(max(0.3, d * 0.50))

                n_sub = 2 if rng.random() < 0.55 else 3
                half  = fan_spread * np.pi / 2
                for ba in np.linspace(angle - half, angle + half, n_sub):
                    _coral(x2, y2,
                           ba + rng.uniform(-0.08, 0.08),
                           length * rng.uniform(0.57, 0.73),
                           d - 1, _pal)

            _coral(root_x, root_y, base_angle, init_len, depth)

        if seg_list:
            lc = mc.LineCollection(seg_list, colors=col_list,
                                   linewidths=lw_list, alpha=0.90,
                                   capstyle="round")
            ax.add_collection(lc)

        # Sandy seafloor strip
        sx = np.linspace(0, 1, 300)
        sy = rng.uniform(-0.005, 0.005, 300)
        ax.fill_between(sx, -0.01, sy + 0.025, color="#7a6240", alpha=0.70, zorder=0)

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        ax.set_title("Coral Reef Growth", color="#ff9f60", fontsize=13, pad=8)
        plt.tight_layout()
        plt.show()
        plt.close(fig)


# ── Pattern 34 ────────────────────────────────────────────────────────────────

class MushroomSporeRenderer(BasePattern):
    """Pattern 34 — Mushroom Spore Map (Voronoi distance-field + ring texture)."""
    name = "Mushroom Spore Map"
    group = "Nature-Inspired"

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=40, min=8, max=120, step=4,
                              description="N Spores:"),
            widgets.FloatSlider(value=0.50, min=0.10, max=1.50, step=0.05,
                                description="Ring Freq:", readout_format=".2f"),
            widgets.FloatSlider(value=0.40, min=0.00, max=1.00, step=0.05,
                                description="Noise Blend:", readout_format=".2f"),
            widgets.IntSlider(value=42, min=0, max=999, description="Seed:"),
        ]

    def render(self, resolution="Low", palette="Inferno", speed=1.0, **kwargs):
        n_spores   = int(kwargs.get("n_spores", 40))
        ring_freq  = float(kwargs.get("ring_freq", 0.50))
        noise_blend = float(kwargs.get("noise_blend", 0.40))
        seed       = int(kwargs.get("seed", 42))
        rng        = np.random.default_rng(seed)

        from scipy.spatial import cKDTree

        N = {"Low": 256, "Medium": 384, "High": 512}.get(resolution, 256)

        pts  = rng.uniform(0.02, 0.98, (n_spores, 2))
        tree = cKDTree(pts)

        gx = np.linspace(0, 1, N)
        gy = np.linspace(0, 1, N)
        GX, GY = np.meshgrid(gx, gy)
        qpts = np.column_stack([GX.ravel(), GY.ravel()])

        k      = min(2, n_spores)
        dists, idxs = tree.query(qpts, k=k)
        d1     = dists[:, 0].reshape(N, N)
        d2     = (dists[:, 1].reshape(N, N) if k >= 2 else d1 * 1.5)
        idx1   = idxs[:, 0].reshape(N, N)

        # Concentric rings centred on each spore
        rings  = np.sin(d1 * ring_freq * 60 * np.pi) * 0.5 + 0.5

        # Layered sine noise (approximates Perlin without extra dependencies)
        ox = rng.uniform(0, 100)
        oy = rng.uniform(0, 100)
        noise = (np.sin((GX + ox) * 12) * np.cos((GY + oy) * 12)
                 + 0.5  * np.sin((GX + ox) * 25 + 0.7) * np.cos((GY + oy) * 22 + 1.3)
                 + 0.25 * np.sin((GX + ox) * 51 + 2.1) * np.cos((GY + oy) * 47 + 0.9))
        noise = (noise - noise.min()) / (noise.max() - noise.min() + 1e-8)

        # Cell boundary darkening: (d2-d1) is small at Voronoi edges
        edge_mask = np.clip((d2 - d1) / (d1 + 0.02), 0, 1) ** 0.35

        # Per-cell colour shift using spore index
        cell_var = (idx1 % 9) / 9.0 * 0.18

        # Combine rings, noise, edges
        field = (rings * (1.0 - noise_blend) + noise * noise_blend) * edge_mask
        field = np.clip(field + cell_var, 0, 1)

        # Earthy mushroom palette: cream/tan/ochre/brown
        r_ch = np.clip(0.55 + field * 0.42, 0, 1)
        g_ch = np.clip(0.38 + field * 0.36, 0, 1)
        b_ch = np.clip(0.18 + field * 0.20, 0, 1)
        img  = np.stack([r_ch, g_ch, b_ch], axis=-1)

        fig, ax = self._create_figure(figsize=(8, 8), bg_color="#1a0f08")
        ax.imshow(img, origin="lower", interpolation="bilinear", aspect="equal")
        ax.axis("off")
        ax.set_title(f"Mushroom Spore Map  n={n_spores}",
                     color="#d4a46a", fontsize=13, pad=8)
        plt.tight_layout()
        plt.show()
        plt.close(fig)


# ── Pattern 35 ────────────────────────────────────────────────────────────────

class TerrainHeightRenderer(BasePattern):
    """Pattern 35 — Terrain Height Map (fractal Brownian motion + hypsometric colour)."""
    name = "Terrain Height Map"
    group = "Nature-Inspired"

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=7, min=2, max=10, step=1,
                              description="Octaves:"),
            widgets.FloatSlider(value=0.55, min=0.20, max=0.90, step=0.05,
                                description="Roughness:", readout_format=".2f"),
            widgets.FloatSlider(value=0.35, min=0.00, max=0.65, step=0.05,
                                description="Water Level:", readout_format=".2f"),
            widgets.IntSlider(value=42, min=0, max=999, description="Seed:"),
        ]

    def render(self, resolution="Low", palette="Inferno", speed=1.0, **kwargs):
        octaves   = int(kwargs.get("octaves", 7))
        roughness = float(kwargs.get("roughness", 0.55))
        water_lvl = float(kwargs.get("water_level", 0.35))
        seed      = int(kwargs.get("seed", 42))
        rng       = np.random.default_rng(seed)

        N = {"Low": 256, "Medium": 384, "High": 512}.get(resolution, 256)
        x = np.linspace(0, 1, N)
        y = np.linspace(0, 1, N)
        X, Y = np.meshgrid(x, y)

        # Fractal Brownian motion: sum octaves of layered sine noise
        h = np.zeros((N, N))
        amp = 1.0
        freq = 3.0
        total_amp = 0.0
        for _ in range(octaves):
            ox = rng.uniform(0, 100)
            oy = rng.uniform(0, 100)
            ph = rng.uniform(0, 2 * np.pi)
            h += amp * (np.sin((X + ox) * freq * 2 * np.pi + ph)
                        * np.cos((Y + oy) * freq * 2 * np.pi + ph * 1.37))
            total_amp += amp
            amp  *= roughness
            freq *= 2.0

        h = (h / total_amp) * 0.5 + 0.5
        h = np.clip(h, 0, 1)

        # Hypsometric colouring: water → sand/green → brown → grey → snow
        w_mask  = h <= water_lvl
        lo_mask = (h > water_lvl)        & (h <= water_lvl + 0.18)
        mi_mask = (h > water_lvl + 0.18) & (h <= water_lvl + 0.42)
        hi_mask = h > water_lvl + 0.42

        r_ch = np.zeros((N, N))
        g_ch = np.zeros((N, N))
        b_ch = np.zeros((N, N))

        t_w = h / (water_lvl + 1e-8)
        r_ch = np.where(w_mask, 0.04 + t_w * 0.08, r_ch)
        g_ch = np.where(w_mask, 0.12 + t_w * 0.22, g_ch)
        b_ch = np.where(w_mask, 0.50 + t_w * 0.42, b_ch)

        t_l = (h - water_lvl) / 0.18
        r_ch = np.where(lo_mask, 0.70 - t_l * 0.35, r_ch)
        g_ch = np.where(lo_mask, 0.60 - t_l * 0.05, g_ch)
        b_ch = np.where(lo_mask, 0.22 - t_l * 0.17, b_ch)

        t_m = (h - (water_lvl + 0.18)) / 0.24
        r_ch = np.where(mi_mask, 0.35 + t_m * 0.28, r_ch)
        g_ch = np.where(mi_mask, 0.55 - t_m * 0.30, g_ch)
        b_ch = np.where(mi_mask, 0.05 + t_m * 0.05, b_ch)

        t_h = np.clip((h - (water_lvl + 0.42)) / max(1.0 - water_lvl - 0.42, 0.01), 0, 1)
        r_ch = np.where(hi_mask, 0.63 + t_h * 0.37, r_ch)
        g_ch = np.where(hi_mask, 0.25 + t_h * 0.75, g_ch)
        b_ch = np.where(hi_mask, 0.10 + t_h * 0.90, b_ch)

        img = np.clip(np.stack([r_ch, g_ch, b_ch], axis=-1), 0, 1)

        fig, ax = self._create_figure(figsize=(9, 8), bg_color="#03080f")
        ax.imshow(img, origin="lower", interpolation="bilinear", aspect="auto")
        # Shoreline contour + subtle elevation bands
        ax.contour(h, levels=[water_lvl], colors="#a0c8ff",
                   linewidths=0.9, alpha=0.60)
        if water_lvl < 0.85:
            elev_levels = np.linspace(water_lvl + 0.06, 0.92, 5)
            ax.contour(h, levels=elev_levels, colors="k",
                       linewidths=0.28, alpha=0.28)
        ax.axis("off")
        ax.set_title(f"Terrain Height Map  octaves={octaves}",
                     color="#c8dce8", fontsize=13, pad=8)
        plt.tight_layout()
        plt.show()
        plt.close(fig)


# ── Pattern 36 ────────────────────────────────────────────────────────────────

class WaterfallFlowRenderer(BasePattern):
    """Pattern 36 — Waterfall Flow (gravity-driven stream paths + spray)."""
    name = "Waterfall Flow"
    group = "Nature-Inspired"

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=70, min=20, max=160, step=10,
                              description="N Streams:"),
            widgets.IntSlider(value=110, min=30, max=250, step=10,
                              description="Steps:"),
            widgets.FloatSlider(value=0.014, min=0.004, max=0.035, step=0.001,
                                description="Step Size:", readout_format=".3f"),
            widgets.IntSlider(value=42, min=0, max=999, description="Seed:"),
        ]

    def render(self, resolution="Low", palette="Inferno", speed=1.0, **kwargs):
        n_streams = int(kwargs.get("n_streams", 70))
        n_steps   = int(kwargs.get("steps", 110))
        step_size = float(kwargs.get("step_size", 0.014))
        seed      = int(kwargs.get("seed", 42))
        rng       = np.random.default_rng(seed)

        N = {"Low": 256, "Medium": 384, "High": 512}.get(resolution, 256)
        xg = np.linspace(0, 1, N)
        yg = np.linspace(0, 1, N)
        X, Y = np.meshgrid(xg, yg)

        # ── Rocky cliff background (raster) ──────────────────────────────────
        tex = np.zeros((N, N))
        for k in range(5):
            f  = 4 * 2 ** k
            ox = rng.uniform(0, 50)
            oy = rng.uniform(0, 50)
            tex += (0.55 ** k) * (
                np.sin((X + ox) * f * np.pi)
                * np.cos((Y + oy) * f * np.pi) * 0.5 + 0.5
            )
        tex = (tex - tex.min()) / (tex.max() - tex.min() + 1e-8)

        rock_r = 0.22 + tex * 0.28
        rock_g = 0.20 + tex * 0.24
        rock_b = 0.16 + tex * 0.20
        pool = Y < 0.18
        rock_r = np.where(pool, 0.06 + tex * 0.08, rock_r)
        rock_g = np.where(pool, 0.14 + tex * 0.12, rock_g)
        rock_b = np.where(pool, 0.32 + tex * 0.28, rock_b)
        bg_img = np.clip(np.stack([rock_r, rock_g, rock_b], axis=-1), 0, 1)

        fig, ax = self._create_figure(figsize=(7, 9), bg_color="#080e14")
        ax.imshow(bg_img, origin="lower", extent=[0, 1, 0, 1], aspect="auto",
                  interpolation="bilinear", zorder=0)

        # ── Stream paths (LineCollection) ────────────────────────────────────
        ctr_x = 0.50 + rng.uniform(-0.05, 0.05)
        ctr_w = 0.28 + rng.uniform(-0.04, 0.04)
        all_segs, all_cols, all_lws = [], [], []

        for _ in range(n_streams):
            px    = ctr_x + rng.uniform(-ctr_w / 2, ctr_w / 2)
            py    = rng.uniform(0.88, 0.98)
            phase = rng.uniform(0, 2 * np.pi)
            sway  = rng.uniform(0.002, 0.009)
            prev  = [px, py]

            for si in range(n_steps):
                # Gravity-driven descent with sinusoidal lateral sway
                dy = -step_size * (1.0 + (1.0 - py) * 0.60)
                dx =  sway * np.sin(phase + si * 0.28)
                px = np.clip(px + dx, 0.02, 0.98)
                py = py + dy
                if py < 0.02:
                    break
                curr = [px, py]
                t = 1.0 - py    # 0 = at top, 1 = at pool
                all_segs.append([prev, curr])
                all_cols.append((0.72 + t * 0.28, 0.87 + t * 0.13, 1.0,
                                 min(1.0, 0.28 + t * 0.60)))
                all_lws.append(max(0.25, 1.1 - t * 0.75))
                prev = curr

        if all_segs:
            lc = mc.LineCollection(all_segs, colors=all_cols,
                                   linewidths=all_lws, capstyle="round", zorder=2)
            ax.add_collection(lc)

        # ── Spray / mist cloud at pool base ──────────────────────────────────
        n_sp = 1400
        sx = np.clip(rng.normal(ctr_x, ctr_w * 0.5, n_sp), 0.04, 0.96)
        sy = rng.beta(1.5, 3.5, n_sp) * 0.24
        sa = rng.uniform(0.04, 0.28, n_sp)
        spray_c = np.column_stack([
            np.full(n_sp, 0.84), np.full(n_sp, 0.92),
            np.ones(n_sp), sa,
        ])
        ax.scatter(sx, sy, s=rng.uniform(6, 50, n_sp),
                   c=spray_c, linewidths=0, zorder=3)

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        ax.set_title("Waterfall Flow", color="#a0c8e8", fontsize=13, pad=8)
        plt.tight_layout()
        plt.show()
        plt.close(fig)


# ── Pattern 37 ────────────────────────────────────────────────────────────────

class TornadoVortexRenderer(BasePattern):
    """Pattern 37 — Tornado Vortex (cylindrical particle vortex with funnel taper)."""
    name = "Tornado Vortex"
    group = "Nature-Inspired"

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=5000, min=500, max=12000, step=500,
                              description="Particles:"),
            widgets.FloatSlider(value=2.0, min=0.5, max=5.0, step=0.2,
                                description="Vortex Str:", readout_format=".1f"),
            widgets.FloatSlider(value=0.08, min=0.02, max=0.35, step=0.02,
                                description="Funnel Top:", readout_format=".2f"),
            widgets.IntSlider(value=42, min=0, max=999, description="Seed:"),
        ]

    def render(self, resolution="Low", palette="Inferno", speed=1.0, **kwargs):
        n_part   = int(kwargs.get("particles", 5000))
        vstr     = float(kwargs.get("vortex_str", 2.0))
        funnel_t = float(kwargs.get("funnel_top", 0.08))
        seed     = int(kwargs.get("seed", 42))
        rng      = np.random.default_rng(seed)

        # Height ∈ [0,1]; funnel radius linearly widens toward base
        py      = rng.uniform(0.0, 1.0, n_part)
        funnel_r = funnel_t + (1.0 - py) * (0.42 - funnel_t)

        # Radial distance: concentrated near funnel wall with Gaussian spread
        r_frac = np.abs(rng.normal(1.0, 0.25, n_part))
        r      = np.clip(r_frac * funnel_r, 0.0, 0.55)
        theta  = rng.uniform(0, 2 * np.pi, n_part)
        # Vortex twist proportional to height and vstr
        twist  = vstr * py * 2 * np.pi
        px     = 0.5 + r * np.cos(theta + twist)

        mask = (px > 0.01) & (px < 0.99)
        px_v, py_v, r_v = px[mask], py[mask], r[mask]

        # Colour: bright white core → dark grey debris wall; fade near ground
        t_r   = np.clip(r_v / 0.45, 0, 1)
        col_r = np.clip(1.00 - t_r * 0.80, 0, 1) * (0.45 + 0.55 * py_v)
        col_g = np.clip(0.96 - t_r * 0.72, 0, 1) * (0.45 + 0.55 * py_v)
        col_b = np.clip(0.92 - t_r * 0.60, 0, 1) * (0.45 + 0.55 * py_v)
        alpha  = np.clip(rng.uniform(0.20, 0.85, len(px_v)), 0.1, 1.0)
        colors = np.column_stack([col_r, col_g, col_b, alpha])
        sizes  = np.clip((1.0 - t_r) * 15 + rng.uniform(0.5, 4, len(px_v)), 0.5, 28)

        # Stormy sky gradient background
        H2  = {"Low": 256, "Medium": 384, "High": 512}.get(resolution, 256)
        bg_y = np.linspace(0, 1, H2)[:, None] * np.ones((H2, H2))
        bg_img = np.clip(np.stack([
            0.05 + (1.0 - bg_y) * 0.06,
            0.05 + (1.0 - bg_y) * 0.06,
            0.10 + (1.0 - bg_y) * 0.08,
        ], axis=-1), 0, 1)

        fig, ax = self._create_figure(figsize=(6, 9), bg_color="#050608")
        ax.imshow(bg_img, origin="lower", extent=[0, 1, 0, 1], aspect="auto",
                  interpolation="bilinear", zorder=0)
        ax.scatter(px_v, py_v, s=sizes, c=colors, linewidths=0, zorder=2)

        # Funnel outline
        y_line = np.linspace(0, 1, 300)
        r_line = funnel_t + (1.0 - y_line) * (0.42 - funnel_t)
        ax.plot(0.5 + r_line, y_line, color="#8090a8", lw=0.7, alpha=0.25, zorder=3)
        ax.plot(0.5 - r_line, y_line, color="#8090a8", lw=0.7, alpha=0.25, zorder=3)

        # Ground debris scatter
        n_deb = 600
        dx = rng.uniform(0, 1, n_deb)
        dy = rng.uniform(0, 0.06, n_deb)
        dc = rng.uniform(0.30, 0.60, n_deb)
        da = rng.uniform(0.10, 0.50, n_deb)
        ax.scatter(dx, dy, s=rng.uniform(1, 12, n_deb),
                   c=np.column_stack([dc, dc * 0.85, dc * 0.70, da]),
                   linewidths=0, zorder=2)

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        ax.set_title("Tornado Vortex", color="#c0c8d8", fontsize=13, pad=8)
        plt.tight_layout()
        plt.show()
        plt.close(fig)


# ── Pattern 38 ────────────────────────────────────────────────────────────────

class CloudFormationRenderer(BasePattern):
    """Pattern 38 — Cloud Formation (fractal noise thresholding + sky composite)."""
    name = "Cloud Formation"
    group = "Nature-Inspired"

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=6, min=2, max=10, step=1,
                              description="Octaves:"),
            widgets.FloatSlider(value=0.60, min=0.20, max=1.40, step=0.05,
                                description="Density:", readout_format=".2f"),
            widgets.FloatSlider(value=0.60, min=0.30, max=0.85, step=0.05,
                                description="Persistence:", readout_format=".2f"),
            widgets.IntSlider(value=42, min=0, max=999, description="Seed:"),
        ]

    def render(self, resolution="Low", palette="Inferno", speed=1.0, **kwargs):
        octaves     = int(kwargs.get("octaves", 6))
        density     = float(kwargs.get("density", 0.60))
        persistence = float(kwargs.get("persistence", 0.60))
        seed        = int(kwargs.get("seed", 42))
        rng         = np.random.default_rng(seed)

        W = {"Low": 400, "Medium": 600, "High": 800}.get(resolution, 400)
        H = W * 5 // 8

        xg = np.linspace(0, 1, W)
        yg = np.linspace(0, 1, H)
        X, Y = np.meshgrid(xg, yg)

        # Multi-octave persistence noise
        noise = np.zeros((H, W))
        amp   = 1.0
        freq  = 2.5
        total = 0.0
        for _ in range(octaves):
            ox = rng.uniform(0, 100)
            oy = rng.uniform(0, 100)
            ph = rng.uniform(0, 2 * np.pi)
            layer = (np.sin((X + ox) * freq * 2 * np.pi + ph)
                     * np.cos((Y + oy) * freq * 2 * np.pi + ph * 1.71)) * 0.5 + 0.5
            noise += amp * layer
            total += amp
            amp  *= persistence
            freq *= 2.1
        noise = np.clip(noise / total, 0, 1)

        # Threshold → cloud alpha with power-law lift
        threshold   = np.clip(1.0 - density, 0.05, 0.95)
        cloud_alpha = np.clip((noise - threshold) / max(1.0 - threshold, 0.05), 0, 1)
        cloud_alpha = np.power(cloud_alpha, 0.50)

        # Sky gradient: warm hazy horizon → deep blue zenith
        sky_r = np.clip(0.48 - Y * 0.22, 0, 1)
        sky_g = np.clip(0.67 - Y * 0.24, 0, 1)
        sky_b = np.clip(0.95 - Y * 0.28, 0, 1)

        # Cloud shadow: offset a copy down-right, darken sky below
        shad   = np.roll(np.roll(cloud_alpha, 10, axis=0), 7, axis=1) * 0.50
        shadow = 1.0 - shad * 0.22

        # Cloud luminance (near-white with slight texture variation)
        cloud_r = 0.96 + noise * 0.04
        cloud_g = 0.96 + noise * 0.04
        cloud_b = 0.97 + noise * 0.03

        img_r = sky_r * shadow * (1 - cloud_alpha) + cloud_r * cloud_alpha
        img_g = sky_g * shadow * (1 - cloud_alpha) + cloud_g * cloud_alpha
        img_b = sky_b * shadow * (1 - cloud_alpha) + cloud_b * cloud_alpha
        img = np.clip(np.stack([img_r, img_g, img_b], axis=-1), 0, 1)

        fig, ax = self._create_figure(figsize=(10, 6), bg_color="#1a3a6a")
        ax.imshow(img, origin="upper", aspect="auto", interpolation="bilinear")
        ax.axis("off")
        ax.set_title(f"Cloud Formation  octaves={octaves}",
                     color="#e0e8ff", fontsize=13, pad=8)
        plt.tight_layout()
        plt.show()
        plt.close(fig)


# ── Pattern 39 ────────────────────────────────────────────────────────────────

class RiverDeltaRenderer(BasePattern):
    """Pattern 39 — River Delta Branching (recursive bifurcating channel network)."""
    name = "River Delta Branching"
    group = "Nature-Inspired"

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=9, min=3, max=13, step=1,
                              description="Depth:"),
            widgets.FloatSlider(value=0.32, min=0.08, max=0.70, step=0.02,
                                description="Fan Spread:", readout_format=".2f"),
            widgets.FloatSlider(value=0.72, min=0.45, max=0.90, step=0.02,
                                description="Length Decay:", readout_format=".2f"),
            widgets.IntSlider(value=42, min=0, max=999, description="Seed:"),
        ]

    def render(self, resolution="Low", palette="Inferno", speed=1.0, **kwargs):
        depth  = int(kwargs.get("depth", 9))
        spread = float(kwargs.get("fan_spread", 0.32))
        decay  = float(kwargs.get("length_decay", 0.72))
        seed   = int(kwargs.get("seed", 42))
        rng    = np.random.default_rng(seed)

        fig, ax = self._create_figure(figsize=(8, 10), bg_color="#04101c")

        # Sea/estuary and land background fills
        ax.fill_between([0, 1], 0, 0.30, color="#061c30", alpha=0.95, zorder=0)
        ax.fill_between([0, 1], 0.30, 1.0, color="#0a1808", alpha=0.80, zorder=0)

        seg_list, t_list, lw_list = [], [], []

        def _channel(x, y, ang, length, d):
            if d == 0 or length < 0.004:
                return
            # ang = deviation from vertical (0 = straight down)
            x2 = x + length * np.sin(ang)
            y2 = max(0.01, y - length * np.cos(ang))
            t  = 1.0 - d / depth
            seg_list.append([[x, y], [x2, y2]])
            t_list.append(t)
            lw_list.append(max(0.3, d * 0.65))
            if y2 < 0.04:
                return
            half = spread * np.pi / 2
            jit  = rng.uniform(-0.06, 0.06)
            _channel(x2, y2, ang - half + jit,
                     length * (decay + rng.uniform(-0.03, 0.03)), d - 1)
            _channel(x2, y2, ang + half + jit,
                     length * (decay + rng.uniform(-0.03, 0.03)), d - 1)
            # Occasional mid-splay tertiary channel
            if d > 3 and rng.random() < 0.28:
                _channel(x2, y2, ang + rng.uniform(-half * 0.4, half * 0.4),
                         length * (decay - 0.08), d - 2)

        _channel(0.50, 0.98, 0.0, 0.16, depth)

        if seg_list:
            t_arr = np.array(t_list)
            # Water colour: muddy-brown upstream → teal-blue at sea
            col_r = np.clip(0.28 - t_arr * 0.12, 0, 1)
            col_g = np.clip(0.48 + t_arr * 0.18, 0, 1)
            col_b = np.clip(0.52 + t_arr * 0.38, 0, 1)
            colors = np.column_stack([col_r, col_g, col_b,
                                      np.full(len(t_arr), 0.88)])
            lc = mc.LineCollection(seg_list, colors=colors,
                                   linewidths=lw_list, capstyle="round", zorder=2)
            ax.add_collection(lc)

        # Sediment fan scatter
        n_sed = 700
        sed_x = np.clip(rng.normal(0.5, 0.24, n_sed), 0.03, 0.97)
        sed_y = np.clip(rng.beta(1.2, 2.8, n_sed) * 0.35, 0, 0.35)
        ax.scatter(sed_x, sed_y, s=rng.uniform(1, 10, n_sed),
                   color="#9a8460", alpha=0.16, linewidths=0, zorder=1)

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        ax.set_title("River Delta Branching", color="#88c8b0", fontsize=13, pad=8)
        plt.tight_layout()
        plt.show()
        plt.close(fig)


# ── Pattern 40 ────────────────────────────────────────────────────────────────

class MothWingRenderer(BasePattern):
    """Pattern 40 — Moth Wing Pattern (elliptical wings + eyespots + concentric bands)."""
    name = "Moth Wing Pattern"
    group = "Nature-Inspired"

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=2, min=1, max=4, step=1,
                              description="N Eyespots:"),
            widgets.IntSlider(value=8, min=3, max=14, step=1,
                              description="Band Count:"),
            widgets.FloatSlider(value=0.55, min=0.20, max=1.00, step=0.05,
                                description="Pat Scale:", readout_format=".2f"),
            widgets.IntSlider(value=42, min=0, max=999, description="Seed:"),
        ]

    def render(self, resolution="Low", palette="Inferno", speed=1.0, **kwargs):
        n_eyes  = int(kwargs.get("n_eyespots", 2))
        n_bands = int(kwargs.get("band_count", 8))
        pat_sc  = float(kwargs.get("pat_scale", 0.55))
        seed    = int(kwargs.get("seed", 42))
        rng     = np.random.default_rng(seed)

        N = {"Low": 400, "Medium": 600, "High": 800}.get(resolution, 400)
        x = np.linspace(-1, 1, N)
        y = np.linspace(-0.7, 0.7, N)
        X, Y = np.meshgrid(x, y)

        # Wing shape: fore (upper) + hind (lower) ellipses
        fore_dist = np.sqrt((X / 0.88) ** 2 + ((Y - 0.12) / 0.52) ** 2)
        hind_dist = np.sqrt((X / 0.70) ** 2 + ((Y + 0.38) / 0.36) ** 2)
        wing_mask = (fore_dist < 1.0) | (hind_dist < 1.0)
        edge_fade = np.clip(
            np.minimum(
                1.0 - np.clip(fore_dist - 0.85, 0, 0.15) / 0.15,
                1.0 - np.clip(hind_dist - 0.85, 0, 0.15) / 0.15,
            ), 0, 1
        )

        # Concentric elliptical band field
        dist_field = np.minimum(fore_dist, hind_dist * 1.05)
        bands = np.sin(dist_field * n_bands * np.pi * pat_sc) * 0.5 + 0.5

        # Layered texture noise
        ox, oy = rng.uniform(0, 10, 2)
        ph = rng.uniform(0, 2 * np.pi)
        noise  = (np.sin((X + ox) * 9  * np.pi + ph)
                  * np.cos((Y + oy) * 9  * np.pi + ph * 1.60) * 0.5 + 0.5)
        noise2 = (np.sin((X + oy) * 20 * np.pi)
                  * np.cos((Y + ox) * 20 * np.pi) * 0.5 + 0.5)
        field = bands * 0.65 + (noise * 0.70 + noise2 * 0.30) * 0.35

        # Earthy moth palette: tan → ochre → deep brown
        r_ch = np.clip(0.38 + field * 0.58, 0, 1)
        g_ch = np.clip(0.24 + field * 0.44, 0, 1)
        b_ch = np.clip(0.08 + field * 0.24, 0, 1)

        # Radial wing veins (faint dark lines from body centre)
        n_veins = 10
        for k in range(n_veins):
            ang      = k * np.pi / n_veins - np.pi / 2 + 0.05
            vx_d, vy_d = np.cos(ang), np.sin(ang)
            perp_dist = np.abs(-vy_d * X + vx_d * Y)
            forward   = np.clip(vx_d * X + vy_d * Y, 0, 2)
            vein_w    = np.exp(-perp_dist ** 2 * 1800) * forward * 0.50
            vein_w    = np.where(wing_mask, vein_w, 0.0)
            r_ch -= vein_w * 0.18
            g_ch -= vein_w * 0.14
            b_ch -= vein_w * 0.07

        # Bilateral eyespots: symmetrically placed in fore wing
        eye_ys = np.linspace(-0.05, 0.35, n_eyes)
        for ey in eye_ys:
            for ex_sign in (+1, -1):
                ex = ex_sign * 0.45
                er = np.sqrt((X - ex) ** 2 + (Y - ey) ** 2)
                r1 = np.exp(-(er - 0.110) ** 2 / 0.0008)   # outer light ring
                r2 = np.exp(-(er - 0.065) ** 2 / 0.0005)   # dark ring
                r3 = np.exp(-(er - 0.028) ** 2 / 0.0002)   # inner iris
                pu = np.exp(-er ** 2 / 0.0010)              # pupil
                in_wing = wing_mask & (er < 0.155)
                r_ch = np.where(in_wing,
                                r_ch + r1*0.35 - r2*0.25 + r3*0.30 - pu*0.45, r_ch)
                g_ch = np.where(in_wing,
                                g_ch + r1*0.28 - r2*0.22 + r3*0.28 - pu*0.45, g_ch)
                b_ch = np.where(in_wing,
                                b_ch + r1*0.08 + r2*0.08 + r3*0.15 - pu*0.35, b_ch)

        r_ch = np.clip(r_ch, 0, 1)
        g_ch = np.clip(g_ch, 0, 1)
        b_ch = np.clip(b_ch, 0, 1)

        # Composite over dark background
        alpha = np.where(wing_mask, edge_fade, 0.0)
        bg = 0.07
        img_r = r_ch * alpha + bg * (1 - alpha)
        img_g = g_ch * alpha + bg * (1 - alpha)
        img_b = (b_ch + 0.01) * alpha + bg * (1 - alpha)
        img = np.clip(np.stack([img_r, img_g, img_b], axis=-1), 0, 1)

        fig, ax = self._create_figure(figsize=(9, 8), bg_color="#090808")
        ax.imshow(img, origin="lower", aspect="auto", interpolation="bilinear")
        ax.axis("off")
        ax.set_title(f"Moth Wing Pattern  eyespots={n_eyes * 2}",
                     color="#d4b068", fontsize=13, pad=8)
        plt.tight_layout()
        plt.show()
        plt.close(fig)
