"""Regression tests for the simulation physics and algorithm fixes."""
import itertools
import time

import matplotlib.colors as mcolors
import numpy as np
import pytest

from patterns import get_pattern
from patterns.scientific import (_AntColony, _boids_init, _boids_step,
                                 _life_initial, _life_step, _orbital_density,
                                 _SPHFluid, _WavePacket)


# ── Atom orbitals (92) ───────────────────────────────────────────────────────

@pytest.mark.parametrize("m, on_z, on_x", [(0, 1.0, 0.0), (1, 0.0, 1.0)])
def test_p_orbital_lobes(m, on_z, on_x):
    psi2, _ = _orbital_density(2, 1, m, "xz", 101)   # 2p_z / 2p_x in the xz-plane
    assert psi2[:, 50].max() == pytest.approx(on_z, abs=1e-6)
    assert psi2[50, :].max() == pytest.approx(on_x, abs=1e-6)


def test_orbital_nodal_plane_is_empty():
    psi2, _ = _orbital_density(2, 1, -1, "xz", 101)  # 2p_y: the xz-plane is its node
    assert psi2.max() == 0.0


def test_s_orbital_is_spherically_symmetric():
    psi2, _ = _orbital_density(1, 0, 0, "xz", 101)
    assert np.allclose(psi2, psi2.T, atol=1e-9)


# ── Boids (95) ───────────────────────────────────────────────────────────────

def _flock(sep, ali=1.0, coh=1.0, steps=200):
    pos, vel = _boids_init(120, 42)
    for _ in range(steps):
        pos, vel = _boids_step(pos, vel, sep, ali, coh)
    offset = pos[:, None] - pos[None]
    offset -= np.round(offset)
    dist = np.linalg.norm(offset, axis=2)
    np.fill_diagonal(dist, np.inf)
    heading = vel / np.linalg.norm(vel, axis=1, keepdims=True)
    return dist.min(axis=1).mean(), np.linalg.norm(heading.mean(axis=0))


def test_separation_spreads_the_flock():
    nn = [_flock(sep)[0] for sep in (0.0, 1.6, 4.0)]
    assert nn[0] < nn[1] < nn[2]


def test_alignment_produces_ordered_flock():
    assert _flock(1.6)[1] > 0.6                       # polarised
    assert _flock(1.6, ali=0.0, coh=0.0)[1] < 0.3     # random headings


# ── SPH fluid (99) ───────────────────────────────────────────────────────────

def test_sph_starts_at_rest_density():
    fluid = _SPHFluid(300, 9.8, 0.02, 1000.0, 2000.0, seed=7)
    assert np.median(fluid.density) == pytest.approx(1000.0, rel=0.05)


def test_sph_dam_break_settles_into_a_layer():
    fluid = _SPHFluid(300, 9.8, 0.02, 1000.0, 2000.0, seed=7)
    fluid.advance(0.2)
    assert np.abs(fluid.vel).max() < 3.0              # ~free-fall speed, no explosion
    fluid.advance(1.8)
    assert np.isfinite(fluid.pos).all()
    assert np.median(fluid.density) == pytest.approx(1000.0, rel=0.05)
    assert fluid.pos[:, 1].max() < 0.25               # collapsed onto the floor
    assert np.ptp(fluid.pos[:, 0]) > 0.8              # spread across the box
    assert np.linalg.norm(fluid.vel, axis=1).max() < 0.5


@pytest.mark.parametrize("args", [(600, 20.0, 0.1, 3000.0, 5000.0),
                                  (600, 0.0, 0.0, 100.0, 500.0)])
def test_sph_extreme_settings_stay_finite(args):
    fluid = _SPHFluid(*args, seed=7)
    fluid.advance(0.5)
    assert np.isfinite(fluid.pos).all() and np.isfinite(fluid.vel).all()


# ── Ant colony (98) ──────────────────────────────────────────────────────────

@pytest.mark.parametrize("seed", range(3))
def test_aco_finds_optimal_small_tour(seed):
    colony = _AntColony(8, seed, 1.0, 3.0, 0.5)
    for _ in range(40):
        colony.iterate(20)
    d = np.where(np.isinf(colony.dist), 0.0, colony.dist)
    optimum = min(sum(d[p[i], p[(i + 1) % 8]] for i in range(8))
                  for p in ((0,) + q for q in itertools.permutations(range(1, 8))))
    assert colony.best_length == pytest.approx(optimum)


def test_aco_extreme_settings_no_nan():
    colony = _AntColony(50, 42, 3.0, 6.0, 0.9)
    for _ in range(200):
        colony.iterate(100)
    assert sorted(colony.best_tour) == list(range(50))
    assert np.isfinite(colony.pheromone).all()


# ── Quantum wave packet (100) ────────────────────────────────────────────────

def test_split_step_conserves_probability():
    wp = _WavePacket(512, -3.0, 5.0, 0.5, "barrier", 8.0)
    dx = wp.x[1] - wp.x[0]
    norm0 = wp.prob.sum() * dx
    for _ in range(300):
        wp.step()
    assert wp.prob.sum() * dx == pytest.approx(norm0, rel=1e-9)


def test_higher_barrier_transmits_less():
    def transmitted(height):
        wp = _WavePacket(512, -3.0, 5.0, 0.5, "barrier", height)
        for _ in range(200):
            wp.step()
        return wp.prob[wp.x > 0.5].sum() / wp.prob.sum()
    assert transmitted(2.0) > transmitted(12.0) > transmitted(30.0)


def test_well_potential_is_displayed():
    wp = _WavePacket(512, -3.0, 5.0, 0.5, "well", 8.0)
    assert wp.potential_display(1.0).max() == pytest.approx(1.0)


# ── Game of Life (94) ────────────────────────────────────────────────────────

def test_gosper_gun_emits_gliders():
    grid = _life_initial("gosper_gun", 80, 0.3, 0)
    age = grid.astype(float)
    assert grid.sum() == 36
    for _ in range(120):                       # four 30-generation periods
        grid, age = _life_step(grid, age)
    assert grid.sum() == 36 + 4 * 5            # gun + four 5-cell gliders


# ── Black hole (93) ──────────────────────────────────────────────────────────

def test_accretion_disk_has_radial_extent(capture):
    get_pattern("Black Hole Lensing").render()
    disk = max(capture[0].axes[0].collections, key=lambda c: len(c.get_offsets()))
    radii = np.linalg.norm(disk.get_offsets(), axis=1)
    assert radii.max() - radii.min() > 4.0     # was zero width (6M..6M)


# ── Hexagonal grid (18) ──────────────────────────────────────────────────────

def _face_colours(fig):
    ax = fig.axes[0]
    faces = [p.get_facecolor() for p in ax.patches]
    for coll in ax.collections:
        faces.extend(map(tuple, coll.get_facecolors()))
    return {mcolors.to_hex(c) for c in faces}


def test_hex_checkerboard_uses_three_colours(capture):
    get_pattern("Hexagonal Grid Art").render(coloring="Checkerboard", rings=4)
    assert len(_face_colours(capture[0])) == 3


# ── Procedural tree (22) ─────────────────────────────────────────────────────

def test_tree_segment_budget(capture):
    start = time.perf_counter()
    get_pattern("Procedural Tree Generator").render(depth=13, branches=4)
    assert time.perf_counter() - start < 10
    segments = sum(len(c.get_segments()) for c in capture[0].axes[0].collections)
    assert segments <= 60_000


# ── Pac-Man maze (66) ────────────────────────────────────────────────────────

def test_pacman_maze_is_a_perfect_maze(capture):
    import sys
    limit = sys.getrecursionlimit()
    get_pattern("Pac-Man Ghost Pathfinding").render(maze_size=41)
    assert sys.getrecursionlimit() == limit, "must not change the global recursion limit"
    img = capture[0].axes[0].images[0].get_array()
    open_ = img[:, :, 0] < 0.03                 # corridors are near-black
    cells = list(zip(*np.nonzero(open_)))
    edges = sum(open_[r + 1, c] for r, c in cells if r + 1 < open_.shape[0]) + \
            sum(open_[r, c + 1] for r, c in cells if c + 1 < open_.shape[1])
    # A perfect maze is a spanning tree: connected with exactly V - 1 edges
    assert edges == len(cells) - 1
