"""Every pattern: registry, control wiring, rendering at slider extremes, animation."""
import time

import numpy as np
import pytest

from conftest import control_values
from patterns import CATEGORIES, PATTERNS, get_pattern

NAMES = list(PATTERNS)
ANIMATABLE = [n for n in NAMES if get_pattern(n).is_animatable]

# Wall-clock budgets (seconds), generous enough for slow CI machines
BUDGET = {"default": 10, "min": 10, "max": 30}


def test_registry_is_complete():
    assert len(PATTERNS) == 100
    listed = [n for names in CATEGORIES.values() for n in names]
    assert sorted(listed) == sorted(NAMES)
    assert len(ANIMATABLE) == 10


def test_registry_is_lazy():
    assert all(isinstance(cls, type) for cls in PATTERNS.values())
    assert get_pattern(NAMES[0]) is get_pattern(NAMES[0])


@pytest.mark.parametrize("name", NAMES)
def test_every_control_is_read_by_render(name):
    assert get_pattern(name).unused_control_keys() == []


@pytest.mark.parametrize("mode", ["default", "min", "max"])
@pytest.mark.parametrize("name", NAMES)
def test_render(name, mode, capture):
    pattern = get_pattern(name)
    resolution = {"default": "Low", "min": "Low", "max": "High"}[mode]
    start = time.perf_counter()
    pattern.render(resolution=resolution, palette="Ocean Depths",
                   **control_values(pattern, mode))
    elapsed = time.perf_counter() - start
    assert len(capture) == 1, "render() must display exactly one figure"
    assert pattern._fig is capture[0], "render() must set self._fig for PNG export"
    assert elapsed < BUDGET[mode], f"{name} [{mode}] took {elapsed:.1f}s"


@pytest.mark.parametrize("name", ANIMATABLE)
def test_animate(name):
    pattern = get_pattern(name)
    kwargs = control_values(pattern, "default")
    frames = pattern.animate(n_frames=6, fps=12, resolution="Low",
                             palette="Forest", **kwargs)
    assert len(frames) == 6
    assert len({f.shape for f in frames}) == 1, "all frames must share one size"
    assert all(f.dtype == np.uint8 and f.shape[2] == 3 for f in frames)
    assert not np.array_equal(frames[0], frames[-1]), "animation must change"
