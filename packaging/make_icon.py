"""Render the app icon: a Mandelbrot set in the Inferno palette, as a multi-size .ico."""
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "visual_engine"))
from engines.color_utils import ColorUtils  # noqa: E402


def mandelbrot(size=512, max_iter=120):
    x = np.linspace(-2.1, 0.7, size)
    y = np.linspace(-1.4, 1.4, size)
    c = x[None, :] + 1j * y[:, None]
    z = np.zeros_like(c)
    smooth = np.zeros(c.shape)
    alive = np.ones(c.shape, bool)
    for i in range(max_iter):
        z[alive] = z[alive] ** 2 + c[alive]
        escaped = alive & (np.abs(z) > 2)
        smooth[escaped] = i + 1 - np.log2(np.log2(np.abs(z[escaped])))
        alive &= ~escaped
    smooth[alive] = 0                       # the set itself is drawn dark
    return smooth / smooth.max()


def main(out=ROOT / "packaging" / "pyxel.ico"):
    t = mandelbrot() ** 0.5
    rgb = (ColorUtils.make_colormap("Inferno")(t)[:, :, :3] * 255).astype(np.uint8)
    img = Image.fromarray(rgb).convert("RGBA")
    # Rounded-square mask so the icon reads well on the taskbar
    size = img.size[0]
    yy, xx = np.mgrid[:size, :size]
    r, m = size * 0.18, size * 0.02
    dx = np.maximum(np.maximum(m + r - xx, xx - (size - 1 - m - r)), 0)
    dy = np.maximum(np.maximum(m + r - yy, yy - (size - 1 - m - r)), 0)
    alpha = np.clip(r + 0.5 - np.hypot(dx, dy), 0, 1)
    alpha[(xx < m) | (yy < m) | (xx > size - 1 - m) | (yy > size - 1 - m)] = 0
    img.putalpha(Image.fromarray((alpha * 255).astype(np.uint8)))
    img.save(out, sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    img.resize((256, 256), Image.LANCZOS).save(out.with_suffix(".png"))
    print("icon written:", out)


if __name__ == "__main__":
    main()
