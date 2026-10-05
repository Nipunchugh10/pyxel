"""Shared fixtures: headless matplotlib and access to rendered figures."""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt  # noqa: E402
import pytest  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


@pytest.fixture
def capture(monkeypatch):
    """Patch plt.show so each render draws (catching draw-time errors) and
    records its figure; returns the list of captured figures."""
    figures = []

    def show(*args, **kwargs):
        fig = plt.gcf()
        fig.canvas.draw()
        figures.append(fig)

    monkeypatch.setattr(plt, "show", show)
    yield figures
    plt.close("all")


def control_values(pattern, mode):
    """render() kwargs with every slider at its default, min or max."""
    kwargs = {}
    for c in pattern.get_controls():
        if not (hasattr(c, "description") and hasattr(c, "value")):
            continue
        value = c.value
        if mode in ("min", "max") and hasattr(c, mode):
            value = getattr(c, mode)
        kwargs[pattern.control_key(c)] = value
    return kwargs
