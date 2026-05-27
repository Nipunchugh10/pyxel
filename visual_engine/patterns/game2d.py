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

# ── 62. Cellular Automaton Life ───────────────────────────────────────────────

class CellularAutomatonRenderer(BasePattern):
    name = "Cellular Automaton Life"
    group = "2D Game-Style"

    def render(self, resolution="Low", palette="Inferno", speed=1.0,
               grid_size=80, generations=50, density=0.30, seed=0, **kwargs):
        from scipy.ndimage import convolve
        from engines.color_utils import ColorUtils
        rng = np.random.default_rng(int(seed))
        N = int(grid_size); gens = int(generations)
        grid = (rng.random((N, N)) < float(density)).astype(np.uint8)
        age  = grid.copy().astype(float)
        kernel = np.array([[1,1,1],[1,0,1],[1,1,1]], dtype=np.uint8)
        for _ in range(gens):
            nb = convolve(grid, kernel, mode="wrap")
            born  = (grid == 0) & (nb == 3)
            alive = (grid == 1) & ((nb == 2) | (nb == 3))
            grid  = (born | alive).astype(np.uint8)
            age   = np.where(grid == 1, age + 1, 0)
        age_norm = np.log1p(age) / (np.log1p(gens) + 1e-9)
        cmap = ColorUtils.make_colormap(palette)
        rgba = cmap(age_norm)
        dead = grid == 0
        rgba[dead, :3] = 0.04; rgba[dead, 3] = 1.0
        fig, ax = plt.subplots(figsize=(7, 7), facecolor="#060606")
        ax.set_facecolor("#060606"); ax.axis("off")
        ax.imshow(rgba, origin="upper", interpolation="nearest")
        pop = int(grid.sum())
        ax.set_title(f"Conway's Game of Life — {N}x{N}, {gens} generations",
                     color="#aaaaaa", fontsize=10, pad=6)
        ax.text(0.5, -0.02, f"Population: {pop}/{N*N}  ({100*pop/(N*N):.1f}%)",
                ha="center", va="top", transform=ax.transAxes,
                color="#888888", fontsize=9)
        self._fig = fig
        plt.tight_layout(); plt.show(); plt.close(fig)

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=80, min=20, max=200, description="grid_size"),
            widgets.IntSlider(value=50, min=5, max=200, description="generations"),
            widgets.FloatSlider(value=0.30, min=0.05, max=0.70, step=0.05,
                                description="density"),
            widgets.IntSlider(value=0, min=0, max=99, description="seed"),
        ]

# ── 63. Dungeon Room Placer ───────────────────────────────────────────────────

class DungeonRenderer(BasePattern):
    name = "Dungeon Room Placer"
    group = "2D Game-Style"

    def render(self, resolution="Low", palette="Inferno", speed=1.0,
               grid_size=60, n_rooms=12, seed=7, **kwargs):
        rng = np.random.default_rng(int(seed))
        G = int(grid_size); n_rooms = int(n_rooms)
        dungeon = np.zeros((G, G), dtype=np.uint8)
        rooms = []
        min_sz, max_sz = 4, max(5, G // 6)

        for _ in range(n_rooms * 10):
            if len(rooms) >= n_rooms: break
            w = rng.integers(min_sz, max_sz + 1)
            h = rng.integers(min_sz, max_sz + 1)
            x = rng.integers(1, G - w - 1)
            y = rng.integers(1, G - h - 1)
            overlap = any(x < rx+rw+1 and x+w+1 > rx and
                          y < ry+rh+1 and y+h+1 > ry
                          for (rx,ry,rw,rh) in rooms)
            if not overlap:
                dungeon[y:y+h, x:x+w] = 1
                rooms.append((x, y, w, h))

        def center(r): return r[0]+r[2]//2, r[1]+r[3]//2
        def corridor(x1,y1,x2,y2):
            for cx in range(min(x1,x2), max(x1,x2)+1):
                dungeon[y1,cx] = 2 if dungeon[y1,cx]==0 else dungeon[y1,cx]
            for cy in range(min(y1,y2), max(y1,y2)+1):
                dungeon[cy,x2] = 2 if dungeon[cy,x2]==0 else dungeon[cy,x2]

        order = list(range(len(rooms))); rng.shuffle(order)
        ro = [rooms[i] for i in order]
        for i in range(len(ro)-1):
            corridor(*center(ro[i]), *center(ro[i+1]))

        img = np.zeros((G, G, 3), dtype=float)
        img[dungeon==0] = [0.07, 0.06, 0.08]
        img[dungeon==1] = [0.72, 0.63, 0.48]
        img[dungeon==2] = [0.42, 0.36, 0.28]
        for (rx,ry,rw,rh) in rooms:
            img[ry+rh//2, rx+rw//2] = [1.0, 0.85, 0.3]

        fig, ax = plt.subplots(figsize=(7, 7), facecolor="#080808")
        ax.set_facecolor("#080808"); ax.axis("off")
        ax.imshow(img, origin="upper", interpolation="nearest")
        ax.set_title(f"Dungeon — {len(rooms)} rooms on {G}x{G} grid",
                     color="#aaaaaa", fontsize=10, pad=6)
        self._fig = fig
        plt.tight_layout(); plt.show(); plt.close(fig)

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=60, min=30, max=120, description="grid_size"),
            widgets.IntSlider(value=12, min=3, max=30, description="n_rooms"),
            widgets.IntSlider(value=7, min=0, max=999, description="seed"),
        ]

# ── 64. Retro Starfield ───────────────────────────────────────────────────────

class RetroStarfieldRenderer(BasePattern):
    name = "Retro Starfield"
    group = "2D Game-Style"

    def render(self, resolution="Low", palette="Inferno", speed=1.0,
               n_stars=800, warp=0.4, seed=0, **kwargs):
        rng = np.random.default_rng(int(seed))
        n = int(n_stars); warp = float(warp)
        x3 = rng.uniform(-1.0, 1.0, n)
        y3 = rng.uniform(-1.0, 1.0, n)
        z  = rng.power(1.0 + warp * 4, n)
        px = x3 / (z + 0.01); py = y3 / (z + 0.01)
        mask = (np.abs(px) < 2.0) & (np.abs(py) < 2.0)
        px, py, z = px[mask], py[mask], z[mask]
        brightness = 1.0 - z
        sizes = (1.0 - z) ** 2 * 60 + 0.5
        r_ch = 0.6 + 0.4 * brightness
        g_ch = 0.6 + 0.4 * brightness
        b_ch = np.ones_like(brightness)
        colors = np.clip(np.stack([r_ch, g_ch, b_ch, brightness], axis=1), 0, 1)
        streak_mask = z < 0.25
        sx, sy, sz = px[streak_mask], py[streak_mask], z[streak_mask]
        streak_len = (0.25 - sz) * 0.3

        fig, ax = plt.subplots(figsize=(7, 7), facecolor="#000005")
        ax.set_facecolor("#000005")
        ax.set_xlim(-2, 2); ax.set_ylim(-2, 2)
        ax.set_aspect("equal"); ax.axis("off")
        for xi, yi, dl in zip(sx, sy, streak_len):
            ax.plot([xi, xi*(1+dl)], [yi, yi*(1+dl)],
                    color="white", lw=0.4, alpha=0.35, zorder=1)
        ax.scatter(px, py, s=sizes, c=colors, zorder=2, linewidths=0)
        from matplotlib.patches import Circle
        for rg, ag in [(0.6,0.06),(0.25,0.10),(0.08,0.18)]:
            ax.add_patch(Circle((0,0), rg, color="white", alpha=ag, zorder=0))
        ax.set_title(f"Retro Starfield — {len(px)} stars, warp={warp:.1f}",
                     color="#6688aa", fontsize=10, pad=6)
        self._fig = fig
        plt.tight_layout(); plt.show(); plt.close(fig)

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=800, min=100, max=3000, step=100,
                              description="n_stars"),
            widgets.FloatSlider(value=0.4, min=0.0, max=1.0, step=0.05,
                                description="warp"),
            widgets.IntSlider(value=0, min=0, max=99, description="seed"),
        ]

# ── 65. Breakout Brick Map ────────────────────────────────────────────────────

class BreakoutBrickRenderer(BasePattern):
    name = "Breakout Brick Map"
    group = "2D Game-Style"

    def render(self, resolution="Low", palette="Inferno", speed=1.0,
               brick_rows=10, brick_cols=16, style=0, seed=3, **kwargs):
        from engines.color_utils import ColorUtils
        rng = np.random.default_rng(int(seed))
        R, C = int(brick_rows), int(brick_cols)
        style = int(style) % 4
        cmap  = ColorUtils.make_colormap(palette)
        vals  = np.zeros((R, C), dtype=float)

        if style == 0:
            for r in range(R): vals[r, :] = r / max(R-1, 1)
        elif style == 1:
            for r in range(R):
                for c in range(C): vals[r, c] = (r + c) % 2
        elif style == 2:
            cx, cy = C/2.0, R/2.0
            for r in range(R):
                for c in range(C):
                    vals[r, c] = np.hypot(c-cx, r-cy) / np.hypot(cx, cy)
        elif style == 3:
            vals = rng.random((R, C))

        vals = (vals - vals.min()) / (vals.max() - vals.min() + 1e-9)
        present = np.ones((R, C), dtype=bool)
        if style == 3:
            present = rng.random((R, C)) > 0.15

        pad = 0.04; bw = (1.0 - 2*pad) / C
        bh  = (0.55 - pad) / R; gap = 0.004; top_y = 0.95

        fig, ax = plt.subplots(figsize=(8, 6), facecolor="#0a0a10")
        ax.set_facecolor("#0a0a10")
        ax.set_xlim(0,1); ax.set_ylim(0,1)
        ax.set_aspect("auto"); ax.axis("off")

        for r in range(R):
            for c in range(C):
                if not present[r, c]: continue
                x = pad + c*bw + gap
                y = top_y - (r+1)*bh + gap
                w = bw - 2*gap; h = bh - 2*gap
                color = cmap(vals[r, c])
                ax.add_patch(patches.FancyBboxPatch(
                    (x,y), w, h, boxstyle="round,pad=0.002",
                    facecolor=color, edgecolor="none", zorder=2))
                ax.add_patch(patches.FancyBboxPatch(
                    (x+0.002, y+h*0.72), w-0.004, h*0.22,
                    boxstyle="round,pad=0.001",
                    facecolor="white", alpha=0.28, edgecolor="none", zorder=3))

        pw = 0.18; px = 0.5 - pw/2
        ax.add_patch(patches.FancyBboxPatch(
            (px, 0.05), pw, 0.025, boxstyle="round,pad=0.003",
            facecolor="#b0c8ff", edgecolor="#5080cc", linewidth=1.5, zorder=4))
        ax.add_patch(patches.Circle(
            (0.5, 0.13), 0.016, facecolor="white", edgecolor="#cccccc",
            linewidth=1, zorder=5))

        names = ["Row Gradient","Checkerboard","Radial","Noise Art"]
        ax.set_title(f"Breakout Brick Map — {R}x{C}, Style: {names[style]}",
                     color="#aaaaaa", fontsize=10, pad=6)
        self._fig = fig
        plt.tight_layout(); plt.show(); plt.close(fig)

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=10, min=3, max=18, description="brick_rows"),
            widgets.IntSlider(value=16, min=4, max=24, description="brick_cols"),
            widgets.Dropdown(options=[("Row Gradient",0),("Checkerboard",1),
                                      ("Radial",2),("Noise Art",3)],
                             value=0, description="style"),
            widgets.IntSlider(value=3, min=0, max=99, description="seed"),
        ]

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

