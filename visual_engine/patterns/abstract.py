"""
Abstract & Artistic Patterns (41–60)
Patterns 41–47 are fully implemented; 48–60 remain as stubs.
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
        sigma = float(blur_sigma) * res / 256.0

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
                yy, xx = np.mgrid[0:res, 0:res]
                xr = ca * (xx - cx) + sa * (yy - cy)
                yr = -sa * (xx - cx) + ca * (yy - cy)
                mask[(xr / rx) ** 2 + (yr / ry) ** 2 < 1.0] += 1.0

            mask = gaussian_filter(mask, sigma=sigma)
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


# ── Stubs: 48–60 ──────────────────────────────────────────────────────────────

class IsometricCityRenderer(_StubMixin, BasePattern):
    name = "Isometric City Builder"
    group = "Abstract & Artistic"

class CircuitBoardRenderer(_StubMixin, BasePattern):
    name = "Circuit Board Art"
    group = "Abstract & Artistic"

class TieDyeRenderer(_StubMixin, BasePattern):
    name = "Tie-Dye Diffusion"
    group = "Abstract & Artistic"

class GeometricCollageRenderer(_StubMixin, BasePattern):
    name = "Geometric Collage"
    group = "Abstract & Artistic"

class PixelSortingRenderer(_StubMixin, BasePattern):
    name = "Pixel Sorting Art"
    group = "Abstract & Artistic"

class AsciiArtRenderer(_StubMixin, BasePattern):
    name = "ASCII Art Renderer"
    group = "Abstract & Artistic"

class KandinskyRenderer(_StubMixin, BasePattern):
    name = "Kandinsky Color Study"
    group = "Abstract & Artistic"

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

# ── Stub mixin for patterns 48–60 ─────────────────────────────────────────────
