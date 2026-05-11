"""
Export utilities — save rendered outputs as PNG, GIF, or MP4.
All files are saved to the visual_engine/exports/ directory.
"""

import os
from pathlib import Path
from datetime import datetime

import numpy as np
from PIL import Image

# Resolve exports directory relative to this file
_EXPORTS_DIR = Path(__file__).resolve().parent.parent / "exports"
_EXPORTS_DIR.mkdir(parents=True, exist_ok=True)


def _timestamped_name(name: str, ext: str) -> Path:
    """Generate a unique filename with timestamp."""
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = name.replace(" ", "_").lower()
    return _EXPORTS_DIR / f"{safe_name}_{stamp}.{ext}"


def export_png(figure, name: str = "pattern") -> str:
    """
    Save a matplotlib figure as a PNG file.

    Parameters
    ----------
    figure : matplotlib.figure.Figure
    name : str — base name for the file

    Returns
    -------
    str — absolute path to the saved file
    """
    path = _timestamped_name(name, "png")
    figure.savefig(str(path), dpi=150, bbox_inches="tight",
                   facecolor=figure.get_facecolor(), edgecolor="none")
    print(f"✅ PNG saved → {path}")
    return str(path)


def export_gif(frames, name: str = "pattern", fps: int = 15) -> str:
    """
    Save a list of numpy image arrays as an animated GIF.

    Parameters
    ----------
    frames : list of np.ndarray — each (H, W, 3) or (H, W, 4) uint8
    name : str — base name
    fps : int

    Returns
    -------
    str — absolute path
    """
    path = _timestamped_name(name, "gif")
    images = [Image.fromarray(f if f.shape[-1] == 3 else f[:, :, :3])
              for f in frames]
    duration = int(1000 / fps)
    images[0].save(str(path), save_all=True, append_images=images[1:],
                   duration=duration, loop=0)
    print(f"✅ GIF saved → {path}")
    return str(path)


def export_mp4(frames, name: str = "pattern", fps: int = 30) -> str:
    """
    Save frames as an MP4 video using matplotlib's FFMpegWriter.
    Falls back to GIF if ffmpeg is not available.

    Parameters
    ----------
    frames : list of np.ndarray — each (H, W, 3) or (H, W, 4) uint8
    name : str
    fps : int

    Returns
    -------
    str — absolute path
    """
    try:
        import matplotlib.pyplot as plt
        from matplotlib.animation import FFMpegWriter

        path = _timestamped_name(name, "mp4")
        h, w = frames[0].shape[:2]
        fig, ax = plt.subplots(figsize=(w / 100, h / 100), dpi=100)
        ax.axis("off")
        fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

        im = ax.imshow(frames[0][:, :, :3])
        writer = FFMpegWriter(fps=fps)

        with writer.saving(fig, str(path), dpi=100):
            for frame in frames:
                im.set_data(frame[:, :, :3])
                writer.grab_frame()

        plt.close(fig)
        print(f"✅ MP4 saved → {path}")
        return str(path)

    except Exception:
        print("⚠️  ffmpeg not available — falling back to GIF export.")
        return export_gif(frames, name, fps=min(fps, 20))
