"""
Camera / viewport controls for Pyxel Canvas.
Manages pan, zoom, and coordinate transformations for 2D patterns.
"""

import numpy as np


class Camera2D:
    """Simple 2D viewport with pan and zoom."""

    def __init__(self, center=(0.0, 0.0), zoom=1.0):
        self.center = np.array(center, dtype=np.float64)
        self.zoom = zoom

    def get_extent(self, aspect=1.0):
        """Return (xmin, xmax, ymin, ymax) for the current viewport."""
        half_w = 2.0 / self.zoom
        half_h = half_w / aspect
        cx, cy = self.center
        return (cx - half_w, cx + half_w, cy - half_h, cy + half_h)

    def pan(self, dx, dy):
        """Shift the viewport center."""
        self.center += np.array([dx, dy]) / self.zoom

    def zoom_in(self, factor=1.5):
        self.zoom *= factor

    def zoom_out(self, factor=1.5):
        self.zoom /= factor

    def linspace_grid(self, resolution):
        """
        Return (X, Y) meshgrid arrays for the current viewport
        at the given resolution (pixels per axis).
        """
        xmin, xmax, ymin, ymax = self.get_extent()
        x = np.linspace(xmin, xmax, resolution)
        y = np.linspace(ymin, ymax, resolution)
        return np.meshgrid(x, y)

    def reset(self):
        self.center = np.array([0.0, 0.0])
        self.zoom = 1.0
