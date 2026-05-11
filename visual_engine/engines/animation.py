"""
Animation loop utilities for Pyxel Canvas.
Helpers for creating matplotlib animations and frame sequences.
"""

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML, display
import numpy as np


def animate_figure(fig, update_func, frames=60, interval=50, blit=True):
    """
    Create and display a matplotlib FuncAnimation inline.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
    update_func : callable(frame_number) -> list of artists
    frames : int
    interval : int — milliseconds between frames
    blit : bool
    """
    anim = FuncAnimation(fig, update_func, frames=frames,
                         interval=interval, blit=blit)
    display(HTML(anim.to_jshtml()))
    plt.close(fig)
    return anim


def frame_sequence(render_func, n_frames=30, figsize=(6, 6), dpi=72):
    """
    Call render_func(frame_index) n_frames times, capturing each as an image array.
    Returns a list of numpy arrays (H, W, 4) suitable for export_gif / export_mp4.
    """
    frames = []
    for i in range(n_frames):
        fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
        render_func(i, ax)
        fig.canvas.draw()
        data = np.frombuffer(fig.canvas.buffer_rgba(), dtype=np.uint8)
        data = data.reshape(fig.canvas.get_width_height()[::-1] + (4,))
        frames.append(data.copy())
        plt.close(fig)
    return frames
