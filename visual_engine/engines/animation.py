"""
Animation helpers for Pyxel Canvas.
"""

import numpy as np


def capture_frame(fig):
    """
    Capture a matplotlib figure as a (H, W, 3) uint8 numpy array.
    Use this inside animate() methods to grab each frame.
    """
    fig.canvas.draw()
    buf = fig.canvas.buffer_rgba()
    arr = np.frombuffer(buf, dtype=np.uint8).reshape(
        fig.canvas.get_width_height()[::-1] + (4,))
    return arr[:, :, :3].copy()
