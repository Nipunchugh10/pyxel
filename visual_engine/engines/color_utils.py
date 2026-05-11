"""
Color palette and gradient helpers for Pyxel Canvas patterns.
"""

import numpy as np
import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap


# ── Preset Palettes ───────────────────────────────────────────────

PALETTES = {
    "Inferno": [
        "#000004", "#1b0c41", "#4a0c6b", "#781c6d", "#a52c60",
        "#cf4446", "#ed6925", "#fb9b06", "#f7d13d", "#fcffa4",
    ],
    "Ocean Depths": [
        "#0b0c10", "#0d1b2a", "#1b263b", "#264653", "#2a9d8f",
        "#43b0a2", "#76c8b8", "#a8dadc", "#d4f0f0", "#e0fbfc",
    ],
    "Neon Cyberpunk": [
        "#0d0221", "#150734", "#261447", "#460b6a", "#7b2d8e",
        "#c850c0", "#ff6ec7", "#ff85d0", "#ffb3e6", "#ffdcf5",
    ],
    "Forest": [
        "#1a1c16", "#2d321d", "#4a5828", "#6b8e23", "#7cb518",
        "#a4c639", "#c5e17a", "#dde8a3", "#f0f4cc", "#fafdf0",
    ],
    "Sunset Blaze": [
        "#1a0005", "#3d0014", "#6b001a", "#a3001e", "#d4230f",
        "#f25c54", "#f4845f", "#f7b267", "#f7d08a", "#fce4a8",
    ],
    "Arctic Aurora": [
        "#020024", "#03002e", "#090979", "#0042a8", "#00a0d4",
        "#00d4aa", "#72efdd", "#a0f5ca", "#c4ffd9", "#eafff7",
    ],
    "Monochrome": [
        "#000000", "#1a1a1a", "#333333", "#4d4d4d", "#666666",
        "#808080", "#999999", "#b3b3b3", "#cccccc", "#ffffff",
    ],
    "Lava Flow": [
        "#0a0000", "#1c0800", "#3d1000", "#5e1a00", "#802400",
        "#b33000", "#e64500", "#ff6600", "#ff9933", "#ffcc66",
    ],
}


class ColorUtils:
    """Utility class for color palette operations."""

    @staticmethod
    def get_palette(name: str) -> list:
        """Return a palette by name, defaulting to Inferno."""
        return PALETTES.get(name, PALETTES["Inferno"])

    @staticmethod
    def palette_names() -> list:
        """Return all available palette names."""
        return list(PALETTES.keys())

    @staticmethod
    def make_colormap(name: str) -> LinearSegmentedColormap:
        """Build a matplotlib LinearSegmentedColormap from a named palette."""
        colors = ColorUtils.get_palette(name)
        return LinearSegmentedColormap.from_list(name, colors, N=256)

    @staticmethod
    def interpolate_color(color_a: str, color_b: str, t: float) -> str:
        """Linearly interpolate between two hex colors (t in [0, 1])."""
        a = np.array(mcolors.to_rgb(color_a))
        b = np.array(mcolors.to_rgb(color_b))
        mixed = (1 - t) * a + t * b
        return mcolors.to_hex(mixed)

    @staticmethod
    def gradient_array(palette_name: str, n: int) -> np.ndarray:
        """Return an (n, 3) array of RGB floats sampled from a palette."""
        cmap = ColorUtils.make_colormap(palette_name)
        return cmap(np.linspace(0, 1, n))[:, :3]
