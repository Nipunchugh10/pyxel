"""Engine helpers: palettes, control wiring, exporters."""
import numpy as np
import pytest

from engines.color_utils import ACCENT_PALETTES, PALETTES, ColorUtils
from engines.renderer import BasePattern


def test_accent_palettes_cover_every_palette():
    assert set(ACCENT_PALETTES) == set(PALETTES)
    assert ColorUtils.accent_colors("Forest") == ACCENT_PALETTES["Forest"]
    assert ColorUtils.accent_colors("nope", "Lava Flow") == ACCENT_PALETTES["Lava Flow"]


def test_accent_colors_returns_a_copy():
    ColorUtils.accent_colors("Forest").append("#000000")
    assert len(ACCENT_PALETTES["Forest"]) == 4


def test_control_key_and_kwargs():
    import ipywidgets as w
    controls = [w.IntSlider(value=3, description="Max Iter:"),
                w.Checkbox(value=True, description="show_bonds"),
                w.HTML(value="label")]
    assert BasePattern.control_kwargs(controls) == {"max_iter": 3, "show_bonds": True}


def test_unused_control_key_is_detected():
    import ipywidgets as w

    class Demo(BasePattern):
        def render(self, resolution="Low", used=1, unused=2, **kwargs):
            return used + kwargs.get("also_used", 0)

        def get_controls(self):
            return [w.IntSlider(description="used"), w.IntSlider(description="unused"),
                    w.IntSlider(description="Also Used:"), w.IntSlider(description="missing")]

    assert Demo().unused_control_keys() == ["unused", "missing"]


@pytest.fixture
def exports(tmp_path, monkeypatch):
    import utils.export as export
    monkeypatch.setattr(export, "_EXPORTS_DIR", tmp_path)
    return export


def test_export_png(exports, tmp_path):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1])
    path = exports.export_png(fig, "My Pattern")
    plt.close(fig)
    assert path.startswith(str(tmp_path)) and path.endswith(".png")
    assert "my_pattern_" in path


def test_export_gif(exports):
    from PIL import Image
    frames = [np.full((8, 8, 3), v, np.uint8) for v in (0, 120, 240)]
    path = exports.export_gif(frames, "anim", fps=10)
    with Image.open(path) as gif:
        assert gif.n_frames == 3


def test_notebook_has_no_control_characters():
    r"""A LaTeX command like \beta written into JSON unescaped becomes a
    control character (\b = backspace) and breaks KaTeX rendering."""
    import re
    from pathlib import Path
    import nbformat
    nb = nbformat.read(Path(__file__).resolve().parents[1] / "notebook.ipynb", as_version=4)
    bad = {i: re.findall(r"[\x00-\x08\x0b\x0c\x0e-\x1f\t][A-Za-z]{0,10}", c.source)
           for i, c in enumerate(nb.cells)}
    assert not {i: m for i, m in bad.items() if m}
