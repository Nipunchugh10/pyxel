"""
2D Game-Style Patterns (61–70)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from engines.renderer import BasePattern


class _StubMixin:
    """Shared stub render logic."""
    def render(self, resolution="Low", palette="Inferno", speed=1.0, **kwargs):
        fig, ax = plt.subplots(figsize=(6, 6), facecolor="#0f0f0f")
        ax.set_facecolor("#0f0f0f")
        rect = patches.FancyBboxPatch((0.1, 0.1), 0.8, 0.8,
                                       boxstyle="round,pad=0.05",
                                       linewidth=2, edgecolor="#555",
                                       facecolor="#1a1a2e")
        ax.add_patch(rect)
        ax.text(0.5, 0.55, self.name, ha="center", va="center",
                fontsize=14, color="#e0e0e0", fontweight="bold",
                transform=ax.transAxes)
        ax.text(0.5, 0.42, "Coming Soon", ha="center", va="center",
                fontsize=11, color="#888", style="italic",
                transform=ax.transAxes)
        ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
        plt.tight_layout(); plt.show(); plt.close(fig)

    def get_controls(self):
        return []

# ── 61. Maze Generator & Solver ───────────────────────────────────────────────

class MazeRenderer(BasePattern):
    name = "Maze Generator & Solver"
    group = "2D Game-Style"

    def render(self, resolution="Low", palette="Inferno", speed=1.0,
               rows=20, cols=20, seed=42, show_solution=True, **kwargs):
        rng = np.random.default_rng(int(seed))
        R, C = int(rows), int(cols)

        wall_h = np.ones((R + 1, C), dtype=bool)
        wall_v = np.ones((R, C + 1), dtype=bool)
        visited = np.zeros((R, C), dtype=bool)
        stack = [(0, 0)]
        visited[0, 0] = True
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while stack:
            r, c = stack[-1]
            neighbours = [(r+dr, c+dc, dr, dc) for dr, dc in dirs
                          if 0 <= r+dr < R and 0 <= c+dc < C and not visited[r+dr, c+dc]]
            if neighbours:
                nr, nc, dr, dc = neighbours[rng.integers(len(neighbours))]
                if dr == -1:   wall_h[r][c]     = False
                elif dr == 1:  wall_h[r + 1][c] = False
                elif dc == -1: wall_v[r][c]     = False
                elif dc == 1:  wall_v[r][c + 1] = False
                visited[nr, nc] = True
                stack.append((nr, nc))
            else:
                stack.pop()

        path_cells = set()
        if show_solution:
            prev = {(0, 0): None}
            queue = [(0, 0)]; qi = 0
            while qi < len(queue):
                r, c = queue[qi]; qi += 1
                if (r, c) == (R - 1, C - 1): break
                for dr, dc in dirs:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < R and 0 <= nc < C and (nr, nc) not in prev:
                        p = False
                        if dr==-1 and not wall_h[r][c]:    p=True
                        elif dr==1 and not wall_h[r+1][c]: p=True
                        elif dc==-1 and not wall_v[r][c]:  p=True
                        elif dc==1 and not wall_v[r][c+1]: p=True
                        if p:
                            prev[(nr, nc)] = (r, c)
                            queue.append((nr, nc))
            cur = (R - 1, C - 1)
            while cur is not None:
                path_cells.add(cur); cur = prev.get(cur)

        fig, ax = plt.subplots(figsize=(7, 7), facecolor="#0d0d0d")
        ax.set_facecolor("#0d0d0d")
        ax.set_xlim(-0.5, C + 0.5); ax.set_ylim(-0.5, R + 0.5)
        ax.set_aspect("equal"); ax.axis("off")
        lw = max(0.5, 4.0 / max(R, C) * 8)

        for (pr, pc) in path_cells:
            ax.add_patch(patches.Rectangle((pc, R-1-pr), 1, 1,
                         facecolor="#2a1a4a", edgecolor="none", zorder=1))
        ax.add_patch(patches.Rectangle((0, R-1), 1, 1, facecolor="#1a7a3a",
                     edgecolor="none", zorder=2))
        ax.add_patch(patches.Rectangle((C-1, 0), 1, 1, facecolor="#7a1a1a",
                     edgecolor="none", zorder=2))

        for r in range(R + 1):
            for c in range(C):
                if wall_h[r][c]:
                    ax.plot([c, c+1], [R-r, R-r], color="#c8c8d0", lw=lw, zorder=3)
        for r in range(R):
            for c in range(C + 1):
                if wall_v[r][c]:
                    ax.plot([c, c], [R-r-1, R-r], color="#c8c8d0", lw=lw, zorder=3)

        ax.text(0.5, R-0.5, "S", ha="center", va="center",
                color="white", fontsize=8, fontweight="bold", zorder=4)
        ax.text(C-0.5, 0.5, "E", ha="center", va="center",
                color="white", fontsize=8, fontweight="bold", zorder=4)
        ax.set_title(f"Maze {R}x{C} — Recursive Backtracker + BFS Solver",
                     color="#aaaaaa", fontsize=10, pad=6)
        self._fig = fig
        plt.tight_layout(); plt.show(); plt.close(fig)

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=20, min=5, max=50, description="rows"),
            widgets.IntSlider(value=20, min=5, max=50, description="cols"),
            widgets.IntSlider(value=42, min=0, max=999, description="seed"),
            widgets.Checkbox(value=True, description="show_solution"),
        ]

class CellularAutomatonRenderer(_StubMixin, BasePattern):
    name = "Cellular Automaton Life"
    group = "2D Game-Style"

class DungeonRenderer(_StubMixin, BasePattern):
    name = "Dungeon Room Placer"
    group = "2D Game-Style"

class RetroStarfieldRenderer(_StubMixin, BasePattern):
    name = "Retro Starfield"
    group = "2D Game-Style"

class BreakoutBrickRenderer(_StubMixin, BasePattern):
    name = "Breakout Brick Map"
    group = "2D Game-Style"

class PacManGhostRenderer(_StubMixin, BasePattern):
    name = "Pac-Man Ghost Pathfinding"
    group = "2D Game-Style"

class PlatformerTerrainRenderer(_StubMixin, BasePattern):
    name = "Platformer Terrain Gen"
    group = "2D Game-Style"

class BulletHellRenderer(_StubMixin, BasePattern):
    name = "Bullet Hell Pattern"
    group = "2D Game-Style"

class CardSuitRenderer(_StubMixin, BasePattern):
    name = "Card Suit Patterns"
    group = "2D Game-Style"

class PixelFlagRenderer(_StubMixin, BasePattern):
    name = "Pixel Flag Generator"
    group = "2D Game-Style"

