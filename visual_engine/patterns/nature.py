"""
Nature-Inspired Patterns (21-40)
Patterns 21-27 are fully implemented; 28-40 remain as stubs awaiting Phase 1 sessions.
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


# ── Stubs 28–40 ───────────────────────────────────────────────────────────────

class FireParticleRenderer(_StubMixin, BasePattern):
    name = "Fire Particle System"
    group = "Nature-Inspired"

class GalaxySpiralRenderer(_StubMixin, BasePattern):
    name = "Galaxy Spiral Arms"
    group = "Nature-Inspired"

class AuroraBorealisRenderer(_StubMixin, BasePattern):
    name = "Aurora Borealis"
    group = "Nature-Inspired"

class UnderwaterCausticsRenderer(_StubMixin, BasePattern):
    name = "Underwater Caustics"
    group = "Nature-Inspired"

class SandDuneRenderer(_StubMixin, BasePattern):
    name = "Sand Dune Erosion"
    group = "Nature-Inspired"

class CoralReefRenderer(_StubMixin, BasePattern):
    name = "Coral Reef Growth"
    group = "Nature-Inspired"

class MushroomSporeRenderer(_StubMixin, BasePattern):
    name = "Mushroom Spore Map"
    group = "Nature-Inspired"

class TerrainHeightRenderer(_StubMixin, BasePattern):
    name = "Terrain Height Map"
    group = "Nature-Inspired"

class WaterfallFlowRenderer(_StubMixin, BasePattern):
    name = "Waterfall Flow"
    group = "Nature-Inspired"

class TornadoVortexRenderer(_StubMixin, BasePattern):
    name = "Tornado Vortex"
    group = "Nature-Inspired"

class CloudFormationRenderer(_StubMixin, BasePattern):
    name = "Cloud Formation"
    group = "Nature-Inspired"

class RiverDeltaRenderer(_StubMixin, BasePattern):
    name = "River Delta Branching"
    group = "Nature-Inspired"

class MothWingRenderer(_StubMixin, BasePattern):
    name = "Moth Wing Pattern"
    group = "Nature-Inspired"
