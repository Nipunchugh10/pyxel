"""
Abstract & Artistic Patterns (41–60)
Patterns 41–54 are fully implemented; 55–60 remain as stubs.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from engines.renderer import BasePattern


# ── Stub mixin for patterns 48–60 ─────────────────────────────────────────────

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



# ── 41. Generative Mondrian ────────────────────────────────────────────────────

class MondrianRenderer(BasePattern):
    name = "Generative Mondrian"
    group = "Abstract & Artistic"

    def render(self, resolution="Low", palette="Inferno", speed=1.0,
               seed=42, splits=6, line_width=4, **kwargs):
        rng = np.random.default_rng(int(seed))

        # Mondrian palette: weighted toward white, then primary red/blue/yellow
        mondrian_colors = [
            "#F5F5F5", "#F5F5F5", "#F5F5F5", "#F5F5F5", "#F5F5F5",
            "#CC1010",  # red
            "#1060CC",  # blue
            "#F0C030",  # yellow
        ]

        # Binary-space partition: list of (x, y, w, h)
        rects = [(0.0, 0.0, 1.0, 1.0)]
        for _ in range(int(splits)):
            next_rects = []
            for (x, y, w, h) in rects:
                if rng.random() < 0.75:
                    if w >= h:
                        cut = x + rng.uniform(0.25, 0.75) * w
                        next_rects.append((x, y, cut - x, h))
                        next_rects.append((cut, y, x + w - cut, h))
                    else:
                        cut = y + rng.uniform(0.25, 0.75) * h
                        next_rects.append((x, y, w, cut - y))
                        next_rects.append((x, cut, w, y + h - cut))
                else:
                    next_rects.append((x, y, w, h))
            rects = next_rects

        fig, ax = plt.subplots(figsize=(7, 7), facecolor="white")
        ax.set_facecolor("white")
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect("equal")
        ax.axis("off")

        for (x, y, w, h) in rects:
            color = rng.choice(mondrian_colors)
            rect_patch = patches.Rectangle(
                (x, y), w, h,
                facecolor=color,
                edgecolor="black",
                linewidth=float(line_width),
                zorder=1,
            )
            ax.add_patch(rect_patch)

        self._fig = fig
        plt.tight_layout()
        plt.show()
        plt.close(fig)

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=42, min=0, max=200, description="seed"),
            widgets.IntSlider(value=6, min=2, max=12, description="splits"),
            widgets.FloatSlider(value=4.0, min=1.0, max=10.0, step=0.5,
                                description="line_width"),
        ]



# ── 42. Perlin Noise Painting ──────────────────────────────────────────────────

class PerlinNoiseRenderer(BasePattern):
    name = "Perlin Noise Painting"
    group = "Abstract & Artistic"

    def render(self, resolution="Low", palette="Inferno", speed=1.0,
               octaves=6, scale=4, seed=0, **kwargs):
        from scipy.ndimage import zoom as nd_zoom
        from engines.color_utils import ColorUtils

        res = self._resolve_resolution(resolution)
        rng = np.random.default_rng(int(seed))

        # Fractal Brownian Motion via value noise + cubic zoom upsampling
        img = np.zeros((res, res), dtype=float)
        amplitude = 1.0
        total_amp = 0.0
        for k in range(int(octaves)):
            freq = 2 ** k
            grid_n = max(4, int(scale) * freq + 2)
            noise_grid = rng.random((grid_n, grid_n)).astype(float)
            zf = res / grid_n
            layer = nd_zoom(noise_grid, zf, order=3, mode="wrap")
            ly, lx = layer.shape
            if ly >= res and lx >= res:
                layer = layer[:res, :res]
            else:
                pad = np.zeros((res, res))
                pad[:min(ly, res), :min(lx, res)] = layer[:min(ly, res), :min(lx, res)]
                layer = pad
            img += amplitude * layer
            total_amp += amplitude
            amplitude *= 0.5

        img /= total_amp
        img = (img - img.min()) / (img.max() - img.min() + 1e-9)

        cmap = ColorUtils.make_colormap(palette)

        fig, ax = plt.subplots(figsize=(7, 7), facecolor="#0a0a0a")
        ax.set_facecolor("#0a0a0a")
        ax.axis("off")
        ax.imshow(img, cmap=cmap, origin="upper", interpolation="bilinear",
                  vmin=0, vmax=1)

        self._fig = fig
        plt.tight_layout()
        plt.show()
        plt.close(fig)

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=6, min=1, max=10, description="octaves"),
            widgets.IntSlider(value=4, min=1, max=12, description="scale"),
            widgets.IntSlider(value=0, min=0, max=99, description="seed"),
        ]



# ── 43. Mandala Generator ─────────────────────────────────────────────────────

class MandalaRenderer(BasePattern):
    name = "Mandala Generator"
    group = "Abstract & Artistic"

    def render(self, resolution="Low", palette="Arctic Aurora", speed=1.0,
               symmetry=8, rings=5, seed=42, **kwargs):
        from engines.color_utils import ColorUtils

        rng = np.random.default_rng(int(seed))
        n = int(symmetry)
        n_rings = int(rings)

        fig, ax = plt.subplots(figsize=(7, 7), facecolor="#05050f")
        ax.set_facecolor("#05050f")
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_xlim(-1.15, 1.15)
        ax.set_ylim(-1.15, 1.15)

        cmap = ColorUtils.make_colormap(palette)

        for ring_idx in range(n_rings):
            t = ring_idx / max(n_rings - 1, 1)
            r_base = 0.10 + ring_idx * 0.19
            # Alternate petal phase by ring
            phase_offset = (np.pi / n) if ring_idx % 2 else 0.0

            for k in range(n):
                a_center = 2 * np.pi * k / n + phase_offset
                half = np.pi / n * 0.88

                # Smooth lens-shaped petal in polar coords
                theta = np.linspace(a_center - half, a_center + half, 80)
                r_profile = (r_base
                             + 0.13 * np.cos((theta - a_center) / half
                                             * np.pi / 2) ** 2)
                px = r_profile * np.cos(theta)
                py = r_profile * np.sin(theta)

                fill_c = cmap(t + 0.04 * rng.random())
                edge_c = cmap((t + 0.38) % 1.0)

                ax.fill(px, py, color=fill_c, alpha=0.55, zorder=ring_idx)
                ax.plot(px, py, color=edge_c, alpha=0.85,
                        linewidth=0.9, zorder=ring_idx + 0.5)

            # Accent dots at petal tips
            for k in range(n):
                for r_dot, alpha in [(r_base + 0.14, 0.9), (r_base - 0.01, 0.5)]:
                    a = 2 * np.pi * k / n + phase_offset
                    ax.plot(r_dot * np.cos(a), r_dot * np.sin(a), "o",
                            color=cmap((t + 0.5) % 1.0),
                            markersize=2.0 + ring_idx * 0.4,
                            alpha=alpha, zorder=n_rings + 1)

        # Central circle
        c_t = np.linspace(0, 2 * np.pi, 100)
        ax.fill(0.06 * np.cos(c_t), 0.06 * np.sin(c_t),
                color=cmap(0.95), alpha=1.0, zorder=n_rings + 2)

        self._fig = fig
        plt.tight_layout()
        plt.show()
        plt.close(fig)

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=8, min=4, max=24, step=2, description="symmetry"),
            widgets.IntSlider(value=5, min=2, max=8, description="rings"),
            widgets.IntSlider(value=42, min=0, max=200, description="seed"),
        ]



# ── 44. Stained Glass Voronoi ─────────────────────────────────────────────────

class StainedGlassRenderer(BasePattern):
    name = "Stained Glass Voronoi"
    group = "Abstract & Artistic"

    def render(self, resolution="Low", palette="Neon Cyberpunk", speed=1.0,
               n_cells=40, seed=7, border_width=3, **kwargs):
        from scipy.spatial import cKDTree
        from engines.color_utils import ColorUtils
        import matplotlib.colors as mcolors

        res = self._resolve_resolution(resolution)
        rng = np.random.default_rng(int(seed))
        n = int(n_cells)
        bw = float(border_width)
        cmap = ColorUtils.make_colormap(palette)

        pts = rng.uniform(0.02, 0.98, (n, 2))
        tree = cKDTree(pts)

        lin = np.linspace(0, 1, res)
        gx, gy = np.meshgrid(lin, lin)
        grid = np.column_stack([gx.ravel(), gy.ravel()])

        dists, idxs = tree.query(grid, k=2)
        d1 = dists[:, 0].reshape(res, res)
        d2 = dists[:, 1].reshape(res, res)
        cell_idx = idxs[:, 0].reshape(res, res)

        # Assign a colour to each cell
        cell_colors = np.array([
            mcolors.to_rgb(cmap(rng.random())) for _ in range(n)
        ])
        img = cell_colors[cell_idx]   # (res, res, 3)

        # Voronoi edge border
        border_thresh = bw / res
        border_mask = (d2 - d1) < border_thresh

        # Subtle distance-based shading within each cell
        dist_norm = d1 / (d1.max() + 1e-9)
        shading = 1.0 - 0.28 * dist_norm
        img = np.clip(img * shading[:, :, None], 0.0, 1.0)
        img[border_mask] = 0.0   # black leading lines

        fig, ax = plt.subplots(figsize=(7, 7), facecolor="black")
        ax.set_facecolor("black")
        ax.axis("off")
        ax.imshow(img, origin="upper", interpolation="nearest")

        self._fig = fig
        plt.tight_layout()
        plt.show()
        plt.close(fig)

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=40, min=8, max=120, description="n_cells"),
            widgets.IntSlider(value=7, min=0, max=99, description="seed"),
            widgets.FloatSlider(value=3.0, min=1.0, max=8.0, step=0.5,
                                description="border_width"),
        ]



# ── 45. Op-Art Optical Illusion ───────────────────────────────────────────────

class OpArtRenderer(BasePattern):
    name = "Op-Art Optical Illusion"
    group = "Abstract & Artistic"

    def render(self, resolution="Low", palette="Monochrome", speed=1.0,
               rings=28, wave_amp=0.04, wave_freq=8, style=0, **kwargs):
        n = int(rings)
        amp = float(wave_amp)
        freq = int(wave_freq)
        style_val = int(style) % 3

        fig, ax = plt.subplots(figsize=(7, 7), facecolor="white")
        ax.set_facecolor("white")
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_xlim(-1.1, 1.1)
        ax.set_ylim(-1.1, 1.1)

        theta = np.linspace(0, 2 * np.pi, 900)

        if style_val == 0:
            # Concentric wavy rings — Bridget Riley style
            for i in range(n, 0, -1):
                t = i / n
                r = 0.05 + t * 1.0
                r_wavy = r + amp * np.sin(freq * theta)
                color = "black" if i % 2 == 0 else "white"
                ax.fill(r_wavy * np.cos(theta), r_wavy * np.sin(theta),
                        color=color, zorder=n - i + 1)

        elif style_val == 1:
            # Vasarely-style grid of concentric distorted circles
            ax.set_facecolor("black")
            fig.set_facecolor("black")
            grid = 9
            xs = np.linspace(-0.95, 0.95, grid)
            ys = np.linspace(-0.95, 0.95, grid)
            t2 = np.linspace(0, 2 * np.pi, 60)
            for i, gx_val in enumerate(xs):
                for j, gy_val in enumerate(ys):
                    dist = np.sqrt(gx_val ** 2 + gy_val ** 2)
                    r = 0.10 * (1.0 - 0.55 * dist / 1.4)
                    r_i = r * 0.50
                    r_w = r + amp * 0.6 * np.sin(freq * t2 + dist * 4)
                    r_wi = r_i + amp * 0.3 * np.sin(freq * t2 + dist * 4 + np.pi)
                    color = "white" if (i + j) % 2 == 0 else "#888888"
                    ax.fill(gx_val + r_w * np.cos(t2),
                            gy_val + r_w * np.sin(t2),
                            color=color, zorder=1)
                    ax.fill(gx_val + r_wi * np.cos(t2),
                            gy_val + r_wi * np.sin(t2),
                            color="black", zorder=2)

        else:
            # Hypnotic concentric squares with wavy sides
            for i in range(n, 0, -1):
                t = i / n
                s = 0.04 + t * 0.98
                n_pts = 60
                top_x = np.linspace(-s, s, n_pts)
                top_y = s + amp * np.sin(freq * np.pi * top_x / s)
                bot_x = np.linspace(s, -s, n_pts)
                bot_y = -s - amp * np.sin(freq * np.pi * bot_x / s)
                rgt_y = np.linspace(s, -s, n_pts)
                rgt_x = s + amp * np.sin(freq * np.pi * rgt_y / s)
                lft_y = np.linspace(-s, s, n_pts)
                lft_x = -s - amp * np.sin(freq * np.pi * lft_y / s)
                sq_x = np.concatenate([top_x, rgt_x, bot_x, lft_x])
                sq_y = np.concatenate([top_y, rgt_y, bot_y, lft_y])
                color = "black" if i % 2 == 0 else "white"
                ax.fill(sq_x, sq_y, color=color, zorder=n - i + 1)

        self._fig = fig
        plt.tight_layout()
        plt.show()
        plt.close(fig)

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=28, min=8, max=60, description="rings"),
            widgets.FloatSlider(value=0.04, min=0.0, max=0.15, step=0.01,
                                description="wave_amp"),
            widgets.IntSlider(value=8, min=2, max=20, description="wave_freq"),
            widgets.IntSlider(value=0, min=0, max=2, description="style"),
        ]



# ── 46. Watercolor Wash Effect ────────────────────────────────────────────────

class WatercolorRenderer(BasePattern):
    name = "Watercolor Wash Effect"
    group = "Abstract & Artistic"

    def render(self, resolution="Low", palette="Sunset Blaze", speed=1.0,
               n_layers=8, n_blobs=12, blur_sigma=30, seed=17, **kwargs):
        from scipy.ndimage import gaussian_filter
        from engines.color_utils import ColorUtils
        import matplotlib.colors as mcolors

        rng = np.random.default_rng(int(seed))
        res = self._resolve_resolution(resolution)
        cmap = ColorUtils.make_colormap(palette)
        # Cap sigma so the Gaussian kernel stays bounded at all resolutions
        sigma = min(float(blur_sigma) * res / 256.0, res * 0.10)

        # Coordinate grid allocated once; reused for every ellipse
        yy, xx = np.mgrid[0:res, 0:res]

        # RGBA canvas — white paper
        canvas = np.ones((res, res, 4), dtype=float)

        for layer_idx in range(int(n_layers)):
            t = layer_idx / max(int(n_layers) - 1, 1)
            base_rgba = np.array(
                mcolors.to_rgba(cmap(t + rng.uniform(-0.05, 0.05)))
            )

            # Random rotated ellipses build the blob mask
            mask = np.zeros((res, res), dtype=float)
            for _ in range(int(n_blobs)):
                cx = rng.integers(0, res)
                cy = rng.integers(0, res)
                r = rng.integers(res // 12, res // 4)
                rx = rng.uniform(0.5, 1.8) * r
                ry = rng.uniform(0.5, 1.8) * r
                angle = rng.uniform(0, np.pi)
                ca, sa = np.cos(angle), np.sin(angle)
                xr = ca * (xx - cx) + sa * (yy - cy)
                yr = -sa * (xx - cx) + ca * (yy - cy)
                mask[(xr / rx) ** 2 + (yr / ry) ** 2 < 1.0] += 1.0

            mask = gaussian_filter(mask, sigma=sigma, truncate=2.5)
            peak = mask.max()
            if peak > 0:
                mask /= peak
            mask = mask ** 0.65   # soft watercolour edge curve

            alpha = base_rgba[3] * mask * 0.55
            for ch in range(3):
                canvas[:, :, ch] = (canvas[:, :, ch] * (1.0 - alpha)
                                    + base_rgba[ch] * alpha)
            canvas[:, :, 3] = 1.0

        # Subtle paper texture
        paper = rng.uniform(0.94, 1.0, (res, res))
        canvas[:, :, :3] *= paper[:, :, None]
        canvas = np.clip(canvas, 0.0, 1.0)

        fig, ax = plt.subplots(figsize=(7, 7), facecolor="white")
        ax.set_facecolor("white")
        ax.axis("off")
        ax.imshow(canvas, origin="upper", interpolation="bilinear")

        self._fig = fig
        plt.tight_layout()
        plt.show()
        plt.close(fig)

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=8, min=3, max=20, description="n_layers"),
            widgets.IntSlider(value=12, min=4, max=30, description="n_blobs"),
            widgets.IntSlider(value=30, min=5, max=80, description="blur_sigma"),
            widgets.IntSlider(value=17, min=0, max=99, description="seed"),
        ]



# ── 47. Glitch Art Generator ──────────────────────────────────────────────────

class GlitchArtRenderer(BasePattern):
    name = "Glitch Art Generator"
    group = "Abstract & Artistic"

    def render(self, resolution="Low", palette="Neon Cyberpunk", speed=1.0,
               n_slices=40, shift_max=80, channel_shift=15, seed=5, **kwargs):
        from engines.color_utils import ColorUtils
        import matplotlib.colors as mcolors

        rng = np.random.default_rng(int(seed))
        res = self._resolve_resolution(resolution)
        cmap = ColorUtils.make_colormap(palette)

        # Base image: horizontal palette gradient + vertical interference
        base = np.zeros((res, res, 3), dtype=float)
        for i in range(res):
            base[i, :] = mcolors.to_rgb(cmap(i / res))
        for j in range(res):
            overlay = np.array(
                mcolors.to_rgb(cmap(0.5 + 0.5 * np.sin(j / res * 5 * np.pi)))
            )
            base[:, j] = np.clip(base[:, j] * 0.75 + overlay * 0.25, 0, 1)

        # Horizontal row-shift glitch
        glitched = base.copy()
        n_s = int(n_slices)
        shift_m = max(1, int(shift_max))
        starts = rng.integers(0, res, n_s)
        heights = rng.integers(1, max(2, res // 16), n_s)
        shifts = rng.integers(-shift_m, shift_m + 1, n_s)

        for start, height, shift in zip(starts, heights, shifts):
            end = min(res, start + height)
            if shift > 0:
                glitched[start:end, shift:] = base[start:end, :-shift]
                glitched[start:end, :shift] = base[start:end, -shift:]
            elif shift < 0:
                s = -shift
                glitched[start:end, :res - s] = base[start:end, s:]
                glitched[start:end, res - s:] = base[start:end, :s]

        # RGB chromatic aberration (channel shift)
        cs = int(channel_shift)
        result = np.zeros_like(glitched)
        result[:, :, 0] = np.roll(glitched[:, :, 0], cs, axis=1)
        result[:, :, 1] = glitched[:, :, 1]
        result[:, :, 2] = np.roll(glitched[:, :, 2], -cs, axis=1)

        # Corrupted data blocks
        for _ in range(rng.integers(8, 25)):
            bx = rng.integers(0, max(1, res - res // 8))
            by = rng.integers(0, res)
            bw = rng.integers(res // 20, max(res // 20 + 1, res // 7))
            bh = rng.integers(1, max(2, res // 25))
            result[by:by + bh, bx:bx + bw] = mcolors.to_rgb(cmap(rng.random()))

        # Scanline darkening
        scanlines = np.ones((res, 1), dtype=float)
        scanlines[::2] = 0.88
        result = np.clip(result * scanlines[:, :, None], 0, 1)

        fig, ax = plt.subplots(figsize=(7, 7), facecolor="black")
        ax.set_facecolor("black")
        ax.axis("off")
        ax.imshow(result, origin="upper", interpolation="nearest")

        self._fig = fig
        plt.tight_layout()
        plt.show()
        plt.close(fig)

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=40, min=5, max=100, description="n_slices"),
            widgets.IntSlider(value=80, min=5, max=200, description="shift_max"),
            widgets.IntSlider(value=15, min=0, max=60, description="channel_shift"),
            widgets.IntSlider(value=5, min=0, max=99, description="seed"),
        ]


# ── 48. Isometric City Builder ────────────────────────────────────────────────

class IsometricCityRenderer(BasePattern):
    name = "Isometric City Builder"
    group = "Abstract & Artistic"

    def render(self, resolution="Low", palette="Neon Cyberpunk", speed=1.0,
               grid_size=10, max_height=8, seed=7, **kwargs):
        from engines.color_utils import ColorUtils
        import matplotlib.colors as mcolors

        rng = np.random.default_rng(int(seed))
        cmap = ColorUtils.make_colormap(palette)
        g = int(grid_size)
        H = int(max_height)

        # Isometric projection constants
        iso_w, iso_h, z_s = 1.0, 0.5, 0.7

        def to_iso(cx, cy, cz):
            return np.array([(cx - cy) * iso_w,
                              (cx + cy) * iso_h + cz * z_s])

        fig, ax = plt.subplots(figsize=(8, 8), facecolor="#0d1117")
        ax.set_facecolor("#0d1117")
        ax.set_aspect("equal")
        ax.axis("off")

        # Assign each tile a random height and palette colour
        grid_data = {}
        for col in range(g):
            for row in range(g):
                grid_data[(col, row)] = (
                    int(rng.integers(1, H + 1)),
                    float(rng.uniform(0.0, 1.0)),
                )

        # Painter's algorithm: tiles with large col+row are furthest back
        draw_order = sorted(grid_data.keys(), key=lambda cr: -(cr[0] + cr[1]))

        for (col, row) in draw_order:
            h, t = grid_data[(col, row)]
            c, r = col, row

            base = np.array(mcolors.to_rgb(cmap(t)))
            top_c   = np.clip(base * 1.35, 0, 1)
            right_c = np.clip(base * 0.72, 0, 1)
            left_c  = np.clip(base * 0.46, 0, 1)

            # Three visible faces of each building block
            t_face = [to_iso(c,   r,   h), to_iso(c+1, r,   h),
                      to_iso(c+1, r+1, h), to_iso(c,   r+1, h)]
            r_face = [to_iso(c+1, r,   0), to_iso(c+1, r+1, 0),
                      to_iso(c+1, r+1, h), to_iso(c+1, r,   h)]
            l_face = [to_iso(c,   r+1, 0), to_iso(c+1, r+1, 0),
                      to_iso(c+1, r+1, h), to_iso(c,   r+1, h)]

            ec, lw = "#0d1117", 0.4
            ax.add_patch(patches.Polygon(r_face, closed=True,
                                         facecolor=right_c, edgecolor=ec,
                                         linewidth=lw))
            ax.add_patch(patches.Polygon(l_face, closed=True,
                                         facecolor=left_c, edgecolor=ec,
                                         linewidth=lw))
            ax.add_patch(patches.Polygon(t_face, closed=True,
                                         facecolor=top_c, edgecolor=ec,
                                         linewidth=lw))

            # Window lights on the right face (every other floor)
            if h >= 3:
                for wz in range(1, h, 2):
                    mid = (to_iso(c+1, r, wz) + to_iso(c+1, r+1, wz)) * 0.5
                    ax.plot(*mid, "o", color="#fffde7",
                            markersize=1.4, alpha=0.85, zorder=10)

        pad = 0.5
        ax.set_xlim(-g * iso_w - pad, g * iso_w + pad)
        ax.set_ylim(-pad, 2 * g * iso_h + H * z_s + pad)

        self._fig = fig
        plt.tight_layout()
        plt.show()
        plt.close(fig)

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=10, min=4,  max=20, description="grid_size"),
            widgets.IntSlider(value=8,  min=1,  max=16, description="max_height"),
            widgets.IntSlider(value=7,  min=0,  max=99, description="seed"),
        ]



# ── 49. Circuit Board Art ─────────────────────────────────────────────────────

class CircuitBoardRenderer(BasePattern):
    name = "Circuit Board Art"
    group = "Abstract & Artistic"

    def render(self, resolution="Low", palette="Neon Cyberpunk", speed=1.0,
               n_traces=80, n_vias=60, trace_width=2.0, seed=12, **kwargs):
        rng = np.random.default_rng(int(seed))

        fig, ax = plt.subplots(figsize=(8, 8), facecolor="#0a2e0a")
        ax.set_facecolor("#0a2e0a")
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)

        trace_col  = "#c8a000"   # copper gold
        pad_col    = "#e8c400"   # solder pad
        silk_col   = "#f0f0f0"   # silkscreen white
        lw_base    = float(trace_width)

        # Snap coordinates to a grid for that PCB look
        snap = 0.04
        def snap_v(v):
            return round(float(v) / snap) * snap

        # Traces: straight lines and L-shaped polylines
        for _ in range(int(n_traces)):
            x0 = snap_v(rng.uniform(0.05, 0.95))
            y0 = snap_v(rng.uniform(0.05, 0.95))
            if rng.random() < 0.45:
                # Straight segment (horizontal or vertical)
                if rng.random() < 0.5:
                    x1 = snap_v(rng.uniform(0.05, 0.95))
                    ax.plot([x0, x1], [y0, y0], color=trace_col,
                            linewidth=lw_base, solid_capstyle="round", alpha=0.85)
                else:
                    y1 = snap_v(rng.uniform(0.05, 0.95))
                    ax.plot([x0, x0], [y0, y1], color=trace_col,
                            linewidth=lw_base, solid_capstyle="round", alpha=0.85)
            else:
                # L-shaped: horizontal leg then vertical leg
                x1 = snap_v(rng.uniform(0.05, 0.95))
                y1 = snap_v(rng.uniform(0.05, 0.95))
                ax.plot([x0, x1, x1], [y0, y0, y1], color=trace_col,
                        linewidth=lw_base, solid_capstyle="round",
                        solid_joinstyle="miter", alpha=0.85)
                # Elbow reinforcement dot
                ax.plot(x1, y0, "o", color=trace_col,
                        markersize=lw_base * 1.5, alpha=0.85)

        # Vias / through-holes (annular rings)
        for _ in range(int(n_vias)):
            x = snap_v(rng.uniform(0.05, 0.95))
            y = snap_v(rng.uniform(0.05, 0.95))
            r_outer = rng.uniform(0.007, 0.013)
            ax.add_patch(patches.Circle((x, y), r_outer,
                                        facecolor=pad_col, linewidth=0, zorder=3))
            ax.add_patch(patches.Circle((x, y), r_outer * 0.42,
                                        facecolor="#001a00", linewidth=0, zorder=4))

        # IC chip bodies with silkscreen and pin stubs
        n_chips = int(rng.integers(2, 6))
        for _ in range(n_chips):
            cx = rng.uniform(0.08, 0.78)
            cy = rng.uniform(0.08, 0.78)
            cw = rng.uniform(0.06, 0.13)
            ch = rng.uniform(0.05, 0.10)
            ax.add_patch(patches.FancyBboxPatch(
                (cx, cy), cw, ch, boxstyle="round,pad=0.003",
                facecolor="#111111", edgecolor=silk_col,
                linewidth=0.8, zorder=5))
            # Pin-1 dot marker
            ax.plot(cx + 0.006, cy + ch - 0.006, "o",
                    color=silk_col, markersize=2.2, zorder=6)
            # Pins along left and right edges
            n_pins = int(rng.integers(4, 9))
            pin_step = ch / (n_pins + 1)
            for p in range(n_pins):
                py = cy + (p + 1) * pin_step
                ax.plot([cx - 0.013, cx], [py, py], color=trace_col,
                        linewidth=lw_base * 0.7, solid_capstyle="butt", zorder=2)
                ax.plot([cx + cw, cx + cw + 0.013], [py, py], color=trace_col,
                        linewidth=lw_base * 0.7, solid_capstyle="butt", zorder=2)

        # Corner mounting holes
        for mx, my in [(0.05, 0.05), (0.95, 0.05), (0.05, 0.95), (0.95, 0.95)]:
            ax.add_patch(patches.Circle((mx, my), 0.019,
                                        facecolor="#c0c0c0", linewidth=0, zorder=3))
            ax.add_patch(patches.Circle((mx, my), 0.010,
                                        facecolor="#001a00", linewidth=0, zorder=4))

        # Board outline
        ax.add_patch(patches.FancyBboxPatch(
            (0.01, 0.01), 0.98, 0.98, boxstyle="round,pad=0.005",
            facecolor="none", edgecolor="#ffcc00",
            linewidth=1.5, zorder=7))

        self._fig = fig
        plt.tight_layout()
        plt.show()
        plt.close(fig)

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=80,  min=20, max=160, description="n_traces"),
            widgets.IntSlider(value=60,  min=10, max=120, description="n_vias"),
            widgets.FloatSlider(value=2.0, min=0.5, max=5.0, step=0.5,
                                description="trace_width"),
            widgets.IntSlider(value=12, min=0, max=99, description="seed"),
        ]



# ── 50. Tie-Dye Diffusion ─────────────────────────────────────────────────────

class TieDyeRenderer(BasePattern):
    name = "Tie-Dye Diffusion"
    group = "Abstract & Artistic"

    def render(self, resolution="Low", palette="Arctic Aurora", speed=1.0,
               n_centers=6, freq=8.0, twist=1.5, seed=42, **kwargs):
        from engines.color_utils import ColorUtils

        rng = np.random.default_rng(int(seed))
        res = self._resolve_resolution(resolution)
        cmap = ColorUtils.make_colormap(palette)

        lin = np.linspace(0.0, 1.0, res)
        xx, yy = np.meshgrid(lin, lin)

        nc = int(n_centers)
        cx = rng.uniform(0.05, 0.95, nc)
        cy = rng.uniform(0.05, 0.95, nc)
        weights = rng.uniform(0.6, 1.4, nc)

        # Superposition of cosine ripples: each centre emits concentric waves.
        # A twist term adds spiral chirality by mixing in the polar angle.
        field = np.zeros((res, res), dtype=float)
        fv = float(freq)
        tv = float(twist)

        for i in range(nc):
            dx = xx - cx[i]
            dy = yy - cy[i]
            dist = np.sqrt(dx ** 2 + dy ** 2)
            angle = np.arctan2(dy, dx)
            phase = dist * fv * 2.0 * np.pi + tv * angle
            field += weights[i] * np.cos(phase)

        field = (field - field.min()) / (field.max() - field.min() + 1e-9)

        fig, ax = plt.subplots(figsize=(7, 7), facecolor="white")
        ax.set_facecolor("white")
        ax.axis("off")
        ax.imshow(field, cmap=cmap, origin="upper",
                  interpolation="bilinear", vmin=0, vmax=1)

        self._fig = fig
        plt.tight_layout()
        plt.show()
        plt.close(fig)

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=6,   min=1,   max=15,  description="n_centers"),
            widgets.FloatSlider(value=8.0, min=2.0, max=30.0, step=1.0,
                                description="freq"),
            widgets.FloatSlider(value=1.5, min=0.0, max=6.0, step=0.25,
                                description="twist"),
            widgets.IntSlider(value=42, min=0, max=99, description="seed"),
        ]



# ── 51. Geometric Collage ─────────────────────────────────────────────────────

class GeometricCollageRenderer(BasePattern):
    name = "Geometric Collage"
    group = "Abstract & Artistic"

    def render(self, resolution="Low", palette="Neon Cyberpunk", speed=1.0,
               n_shapes=70, alpha=0.72, seed=3, **kwargs):
        from engines.color_utils import ColorUtils
        import matplotlib.colors as mcolors

        rng = np.random.default_rng(int(seed))
        cmap = ColorUtils.make_colormap(palette)

        fig, ax = plt.subplots(figsize=(7, 7), facecolor="#111111")
        ax.set_facecolor("#111111")
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)

        al = float(alpha)

        for _ in range(int(n_shapes)):
            t = float(rng.uniform())
            color = mcolors.to_rgba(cmap(t), alpha=al)
            cx = float(rng.uniform(0.0, 1.0))
            cy = float(rng.uniform(0.0, 1.0))
            size = float(rng.uniform(0.04, 0.24))
            shape = int(rng.integers(0, 5))

            if shape == 0:
                # Circle
                ax.add_patch(patches.Circle((cx, cy), size * 0.5,
                                             facecolor=color, linewidth=0))

            elif shape == 1:
                # Rotated rectangle (manual rotation for centre-pivoted transform)
                w = size * float(rng.uniform(0.6, 2.0))
                h = size * float(rng.uniform(0.5, 1.6))
                angle = float(rng.uniform(0, np.pi))
                ca, sa = np.cos(angle), np.sin(angle)
                corners = np.array([[-w/2, -h/2], [w/2, -h/2],
                                     [w/2,  h/2], [-w/2,  h/2]])
                rot = corners @ np.array([[ca, sa], [-sa, ca]]) + [cx, cy]
                ax.add_patch(patches.Polygon(rot, facecolor=color, linewidth=0))

            elif shape == 2:
                # Equilateral triangle
                rot = float(rng.uniform(0, 2 * np.pi))
                angs = np.linspace(rot, rot + 2 * np.pi, 4)[:-1]
                verts = np.column_stack([cx + size * 0.55 * np.cos(angs),
                                         cy + size * 0.55 * np.sin(angs)])
                ax.add_patch(patches.Polygon(verts, facecolor=color, linewidth=0))

            elif shape == 3:
                # Regular hexagon
                rot = float(rng.uniform(0, np.pi / 6))
                angs = np.linspace(rot, rot + 2 * np.pi, 7)[:-1]
                verts = np.column_stack([cx + size * 0.5 * np.cos(angs),
                                         cy + size * 0.5 * np.sin(angs)])
                ax.add_patch(patches.Polygon(verts, facecolor=color, linewidth=0))

            else:
                # 5-pointed star
                outer = size * 0.5
                inner = outer * 0.40
                rot = float(rng.uniform(0, 2 * np.pi / 5))
                star_angs = np.linspace(-np.pi/2, -np.pi/2 + 2*np.pi, 11)[:-1]
                rs = np.where(np.arange(10) % 2 == 0, outer, inner)
                verts = np.column_stack([cx + rs * np.cos(star_angs + rot),
                                         cy + rs * np.sin(star_angs + rot)])
                ax.add_patch(patches.Polygon(verts, facecolor=color, linewidth=0))

        self._fig = fig
        plt.tight_layout()
        plt.show()
        plt.close(fig)

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=70,  min=10, max=150, description="n_shapes"),
            widgets.FloatSlider(value=0.72, min=0.1, max=1.0, step=0.05,
                                description="alpha"),
            widgets.IntSlider(value=3, min=0, max=99, description="seed"),
        ]



# ── 52. Pixel Sorting Art ─────────────────────────────────────────────────────

class PixelSortingRenderer(BasePattern):
    name = "Pixel Sorting Art"
    group = "Abstract & Artistic"

    def render(self, resolution="Low", palette="Inferno", speed=1.0,
               threshold=0.30, sort_mode=0, vertical=0, seed=9, **kwargs):
        from scipy.ndimage import zoom as nd_zoom
        from engines.color_utils import ColorUtils

        rng = np.random.default_rng(int(seed))
        res = self._resolve_resolution(resolution)
        cmap = ColorUtils.make_colormap(palette)
        thresh = float(threshold)

        # Multi-octave value noise → luminance field
        field = np.zeros((res, res), dtype=float)
        amp = 1.0
        total = 0.0
        for k in range(5):
            n_g = max(4, (2 ** k) * 6 + 2)
            noise = rng.random((n_g, n_g)).astype(float)
            zf = res / n_g
            layer = nd_zoom(noise, zf, order=3, mode="wrap")
            ly, lx = layer.shape
            if ly >= res and lx >= res:
                layer = layer[:res, :res]
            else:
                tmp = np.zeros((res, res))
                tmp[:min(ly, res), :min(lx, res)] = layer[:min(ly, res), :min(lx, res)]
                layer = tmp
            field += amp * layer
            total += amp
            amp *= 0.5
        field /= total
        field = (field - field.min()) / (field.max() - field.min() + 1e-9)

        # Vectorised colormap application → RGB image
        rgb = cmap(field)[:, :, :3].copy()   # (res, res, 3)

        do_vert = int(vertical) % 2 == 1
        if do_vert:
            rgb = np.rot90(rgb)

        # Pixel sorting: for each row find contiguous spans above threshold,
        # then sort those spans by the chosen key (luminance / red / saturation).
        mode = int(sort_mode) % 3
        sorted_rgb = rgb.copy()

        for row_i in range(res):
            row = rgb[row_i]            # (res, 3)
            if mode == 0:
                keys = 0.299 * row[:, 0] + 0.587 * row[:, 1] + 0.114 * row[:, 2]
            elif mode == 1:
                keys = row[:, 0]        # red channel
            else:
                keys = np.max(row, axis=1) - np.min(row, axis=1)  # sat proxy

            above = keys > thresh
            if not np.any(above):
                continue

            # Walk the boolean mask to find contiguous segments
            in_seg = False
            seg_start = 0
            for col_i in range(res):
                if above[col_i] and not in_seg:
                    seg_start = col_i
                    in_seg = True
                elif not above[col_i] and in_seg:
                    order = np.argsort(keys[seg_start:col_i])
                    sorted_rgb[row_i, seg_start:col_i] = row[seg_start:col_i][order]
                    in_seg = False
            if in_seg:
                order = np.argsort(keys[seg_start:])
                sorted_rgb[row_i, seg_start:] = row[seg_start:][order]

        if do_vert:
            sorted_rgb = np.rot90(sorted_rgb, k=-1)

        sorted_rgb = np.clip(sorted_rgb, 0, 1)

        fig, ax = plt.subplots(figsize=(7, 7), facecolor="black")
        ax.set_facecolor("black")
        ax.axis("off")
        ax.imshow(sorted_rgb, origin="upper", interpolation="nearest")

        self._fig = fig
        plt.tight_layout()
        plt.show()
        plt.close(fig)

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.FloatSlider(value=0.30, min=0.0, max=0.90, step=0.05,
                                description="threshold"),
            widgets.IntSlider(value=0, min=0, max=2, description="sort_mode"),
            widgets.IntSlider(value=0, min=0, max=1, description="vertical"),
            widgets.IntSlider(value=9, min=0, max=99, description="seed"),
        ]



# ── 53. ASCII Art Renderer ────────────────────────────────────────────────────

class AsciiArtRenderer(BasePattern):
    name = "ASCII Art Renderer"
    group = "Abstract & Artistic"

    # Luminance ramp: dense (dark) → sparse (bright)
    _RAMP = "@%#*+=- :. "

    def render(self, resolution="Low", palette="Monochrome", speed=1.0,
               cols=60, seed=22, invert=0, **kwargs):
        from scipy.ndimage import zoom as nd_zoom
        from engines.color_utils import ColorUtils

        rng = np.random.default_rng(int(seed))
        ncols = int(cols)
        nrows = max(1, ncols // 2)   # chars are ~2× taller than wide

        # Build a two-octave noise field at char resolution
        def make_layer(grid_div, nrows, ncols):
            g = rng.random((max(4, nrows // grid_div),
                            max(4, ncols // grid_div))).astype(float)
            z = nd_zoom(g,
                        (nrows / g.shape[0], ncols / g.shape[1]),
                        order=3, mode="wrap")
            return z[:nrows, :ncols]

        field = make_layer(4, nrows, ncols) * 0.65 + make_layer(2, nrows, ncols) * 0.35
        field = (field - field.min()) / (field.max() - field.min() + 1e-9)
        if int(invert) % 2 == 1:
            field = 1.0 - field

        cmap = ColorUtils.make_colormap(palette)
        # Vectorised colormap lookup
        rgba = cmap(field)    # (nrows, ncols, 4)
        ramp = self._RAMP
        rlen = len(ramp)

        fw = max(6.0, ncols * 0.13)
        fh = max(4.0, nrows * 0.24)
        fig, ax = plt.subplots(figsize=(fw, fh), facecolor="#080808")
        ax.set_facecolor("#080808")
        ax.axis("off")
        ax.set_xlim(0, ncols)
        ax.set_ylim(0, nrows)

        for ri in range(nrows):
            for ci in range(ncols):
                v = field[ri, ci]
                char = ramp[min(int(v * rlen), rlen - 1)]
                ax.text(ci + 0.5, nrows - ri - 0.5, char,
                        ha="center", va="center",
                        fontsize=6.5, color=rgba[ri, ci, :3],
                        fontfamily="monospace")

        self._fig = fig
        plt.tight_layout()
        plt.show()
        plt.close(fig)

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=60, min=20, max=90, description="cols"),
            widgets.IntSlider(value=22, min=0, max=99, description="seed"),
            widgets.IntSlider(value=0,  min=0, max=1,  description="invert"),
        ]



# ── 54. Kandinsky Color Study ─────────────────────────────────────────────────

class KandinskyRenderer(BasePattern):
    name = "Kandinsky Color Study"
    group = "Abstract & Artistic"

    def render(self, resolution="Low", palette="Inferno", speed=1.0,
               n_elements=65, style=0, seed=0, **kwargs):
        from engines.color_utils import ColorUtils
        import matplotlib.colors as mcolors

        rng = np.random.default_rng(int(seed))
        cmap = ColorUtils.make_colormap(palette)
        n = int(n_elements)
        sv = int(style) % 3

        # Three compositional styles inspired by Kandinsky periods
        if sv == 0:
            bg = "#0a0a12"    # Composition VIII: dark ground, hard geometry
            palette_hex = ["#e63946", "#457b9d", "#f4d03f",
                           "#2ecc71", "#e67e22", "#9b59b6", "#ecf0f1"]
        elif sv == 1:
            bg = "#f5e6c8"    # Yellow-Red-Blue: warm ground, primary palette
            palette_hex = ["#c0392b", "#2980b9", "#f1c40f",
                           "#27ae60", "#8e44ad", "#e74c3c", "#3498db"]
        else:
            bg = "#0d0d1a"    # Improvisation: dark, cmap-driven colours
            palette_hex = [mcolors.to_hex(cmap(i / 6.0)) for i in range(7)]

        fig, ax = plt.subplots(figsize=(8, 8), facecolor=bg)
        ax.set_facecolor(bg)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)

        def pick(alpha=1.0):
            return mcolors.to_rgba(rng.choice(palette_hex), alpha=alpha)

        for _ in range(n):
            etype = int(rng.integers(0, 7))
            cx = float(rng.uniform(-0.88, 0.88))
            cy = float(rng.uniform(-0.88, 0.88))

            if etype == 0:
                # Solid filled circle
                r = float(rng.uniform(0.04, 0.26))
                ax.add_patch(patches.Circle((cx, cy), r,
                                             facecolor=pick(float(rng.uniform(0.6, 1.0))),
                                             linewidth=0))

            elif etype == 1:
                # Concentric circle halo
                r = float(rng.uniform(0.06, 0.20))
                ax.add_patch(patches.Circle((cx, cy), r,
                                             facecolor="none",
                                             edgecolor=pick(),
                                             linewidth=float(rng.uniform(1.0, 5.0))))
                ax.add_patch(patches.Circle((cx, cy), r * 0.55,
                                             facecolor=pick(0.55), linewidth=0))

            elif etype == 2:
                # Equilateral triangle (random rotation)
                size = float(rng.uniform(0.05, 0.24))
                rot = float(rng.uniform(0, 2 * np.pi))
                angs = rot + np.linspace(0, 2 * np.pi, 4)[:-1]
                verts = np.column_stack([cx + size * np.cos(angs),
                                         cy + size * np.sin(angs)])
                ax.add_patch(patches.Polygon(verts,
                                              facecolor=pick(float(rng.uniform(0.65, 1.0))),
                                              linewidth=0))

            elif etype == 3:
                # Bold line stroke
                x2 = float(rng.uniform(-0.88, 0.88))
                y2 = float(rng.uniform(-0.88, 0.88))
                ax.plot([cx, x2], [cy, y2],
                        color=pick(),
                        linewidth=float(rng.uniform(1.0, 9.0)),
                        solid_capstyle="round", alpha=0.88)

            elif etype == 4:
                # Rotated rectangle
                w = float(rng.uniform(0.05, 0.22))
                h = float(rng.uniform(0.04, 0.18))
                angle = float(rng.uniform(0, np.pi))
                ca, sa = np.cos(angle), np.sin(angle)
                corners = np.array([[-w/2, -h/2], [w/2, -h/2],
                                     [w/2,  h/2], [-w/2,  h/2]])
                rot = corners @ np.array([[ca, sa], [-sa, ca]]) + [cx, cy]
                ax.add_patch(patches.Polygon(rot,
                                              facecolor=pick(float(rng.uniform(0.7, 1.0))),
                                              linewidth=0))

            elif etype == 5:
                # Arc / partial ring
                r = float(rng.uniform(0.06, 0.22))
                theta1 = float(rng.uniform(0, 360))
                theta2 = theta1 + float(rng.uniform(60, 280))
                ax.add_patch(patches.Arc((cx, cy), 2*r, 2*r,
                                          theta1=theta1, theta2=theta2,
                                          color=pick(),
                                          linewidth=float(rng.uniform(1.0, 6.0))))

            else:
                # Fan of radiating spokes
                n_sp = int(rng.integers(5, 14))
                length = float(rng.uniform(0.06, 0.22))
                base_a = float(rng.uniform(0, 2 * np.pi))
                for k in range(n_sp):
                    a = base_a + k * np.pi / n_sp
                    ax.plot([cx, cx + length * np.cos(a)],
                            [cy, cy + length * np.sin(a)],
                            color=pick(0.85),
                            linewidth=float(rng.uniform(0.6, 3.0)))

        self._fig = fig
        plt.tight_layout()
        plt.show()
        plt.close(fig)

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=65, min=10, max=120, description="n_elements"),
            widgets.IntSlider(value=0,  min=0,  max=2,  description="style"),
            widgets.IntSlider(value=0,  min=0,  max=99, description="seed"),
        ]



# ── Stubs: 55–60 ──────────────────────────────────────────────────────────────

class ZentangleRenderer(_StubMixin, BasePattern):
    name = "Zentangle Automaton"
    group = "Abstract & Artistic"

class NeonSignRenderer(_StubMixin, BasePattern):
    name = "Neon Sign Generator"
    group = "Abstract & Artistic"

class MosaicTileRenderer(_StubMixin, BasePattern):
    name = "Mosaic Tile Art"
    group = "Abstract & Artistic"

class ImpressionistDotsRenderer(_StubMixin, BasePattern):
    name = "Impressionist Dots"
    group = "Abstract & Artistic"

class CubistRenderer(_StubMixin, BasePattern):
    name = "Cubist Portrait Filter"
    group = "Abstract & Artistic"

class AbstractDripRenderer(_StubMixin, BasePattern):
    name = "Abstract Expressionism Drip"
    group = "Abstract & Artistic"
