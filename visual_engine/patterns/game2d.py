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
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        plt.tight_layout()
        plt.show()
        plt.close(fig)

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
                if dr == -1:
                    wall_h[r][c] = False
                elif dr == 1:
                    wall_h[r + 1][c] = False
                elif dc == -1:
                    wall_v[r][c] = False
                elif dc == 1:
                    wall_v[r][c + 1] = False
                visited[nr, nc] = True
                stack.append((nr, nc))
            else:
                stack.pop()

        path_cells = set()
        if show_solution:
            prev = {(0, 0): None}
            queue = [(0, 0)]
            qi = 0
            while qi < len(queue):
                r, c = queue[qi]
                qi += 1
                if (r, c) == (R - 1, C - 1):
                    break
                for dr, dc in dirs:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < R and 0 <= nc < C and (nr, nc) not in prev:
                        p = False
                        if dr == -1 and not wall_h[r][c]:
                            p = True
                        elif dr == 1 and not wall_h[r+1][c]:
                            p = True
                        elif dc == -1 and not wall_v[r][c]:
                            p = True
                        elif dc == 1 and not wall_v[r][c+1]:
                            p = True
                        if p:
                            prev[(nr, nc)] = (r, c)
                            queue.append((nr, nc))
            cur = (R - 1, C - 1)
            while cur is not None:
                path_cells.add(cur)
                cur = prev.get(cur)

        fig, ax = plt.subplots(figsize=(7, 7), facecolor="#0d0d0d")
        ax.set_facecolor("#0d0d0d")
        ax.set_xlim(-0.5, C + 0.5)
        ax.set_ylim(-0.5, R + 0.5)
        ax.set_aspect("equal")
        ax.axis("off")
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
        plt.tight_layout()
        plt.show()
        plt.close(fig)

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
        N = int(grid_size)
        gens = int(generations)
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
        rgba[dead, :3] = 0.04
        rgba[dead, 3] = 1.0
        fig, ax = plt.subplots(figsize=(7, 7), facecolor="#060606")
        ax.set_facecolor("#060606")
        ax.axis("off")
        ax.imshow(rgba, origin="upper", interpolation="nearest")
        pop = int(grid.sum())
        ax.set_title(f"Conway's Game of Life — {N}x{N}, {gens} generations",
                     color="#aaaaaa", fontsize=10, pad=6)
        ax.text(0.5, -0.02, f"Population: {pop}/{N*N}  ({100*pop/(N*N):.1f}%)",
                ha="center", va="top", transform=ax.transAxes,
                color="#888888", fontsize=9)
        self._fig = fig
        plt.tight_layout()
        plt.show()
        plt.close(fig)

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
        G = int(grid_size)
        n_rooms = int(n_rooms)
        dungeon = np.zeros((G, G), dtype=np.uint8)
        rooms = []
        min_sz, max_sz = 4, max(5, G // 6)

        for _ in range(n_rooms * 10):
            if len(rooms) >= n_rooms:
                break
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

        order = list(range(len(rooms)))
        rng.shuffle(order)
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
        ax.set_facecolor("#080808")
        ax.axis("off")
        ax.imshow(img, origin="upper", interpolation="nearest")
        ax.set_title(f"Dungeon — {len(rooms)} rooms on {G}x{G} grid",
                     color="#aaaaaa", fontsize=10, pad=6)
        self._fig = fig
        plt.tight_layout()
        plt.show()
        plt.close(fig)

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
        n = int(n_stars)
        warp = float(warp)
        x3 = rng.uniform(-1.0, 1.0, n)
        y3 = rng.uniform(-1.0, 1.0, n)
        z  = rng.power(1.0 + warp * 4, n)
        px = x3 / (z + 0.01)
        py = y3 / (z + 0.01)
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
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        ax.set_aspect("equal")
        ax.axis("off")
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
        plt.tight_layout()
        plt.show()
        plt.close(fig)

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
            for r in range(R):
                vals[r, :] = r / max(R-1, 1)
        elif style == 1:
            for r in range(R):
                for c in range(C):
                    vals[r, c] = (r + c) % 2
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

        pad = 0.04
        bw = (1.0 - 2*pad) / C
        bh = (0.55 - pad) / R
        gap = 0.004
        top_y = 0.95

        fig, ax = plt.subplots(figsize=(8, 6), facecolor="#0a0a10")
        ax.set_facecolor("#0a0a10")
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect("auto")
        ax.axis("off")

        for r in range(R):
            for c in range(C):
                if not present[r, c]:
                    continue
                x = pad + c*bw + gap
                y = top_y - (r+1)*bh + gap
                w = bw - 2*gap
                h = bh - 2*gap
                color = cmap(vals[r, c])
                ax.add_patch(patches.FancyBboxPatch(
                    (x,y), w, h, boxstyle="round,pad=0.002",
                    facecolor=color, edgecolor="none", zorder=2))
                ax.add_patch(patches.FancyBboxPatch(
                    (x+0.002, y+h*0.72), w-0.004, h*0.22,
                    boxstyle="round,pad=0.001",
                    facecolor="white", alpha=0.28, edgecolor="none", zorder=3))

        pw = 0.18
        px = 0.5 - pw/2
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
        plt.tight_layout()
        plt.show()
        plt.close(fig)

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

# ── 66. Pac-Man Ghost Pathfinding ─────────────────────────────────────────────

class PacManGhostRenderer(BasePattern):
    name = "Pac-Man Ghost Pathfinding"
    group = "2D Game-Style"

    def render(self, resolution="Low", palette="Inferno", speed=1.0,
               maze_size=21, n_ghosts=4, seed=5, **kwargs):
        rng = np.random.default_rng(int(seed))
        N = int(maze_size) | 1
        maze = np.ones((N, N), dtype=np.uint8)

        def carve(r, c):
            maze[r, c] = 0
            ds = [(0,2),(0,-2),(2,0),(-2,0)]
            rng.shuffle(ds)
            for dr, dc in ds:
                nr, nc = r+dr, c+dc
                if 0 <= nr < N and 0 <= nc < N and maze[nr, nc] == 1:
                    maze[r+dr//2, c+dc//2] = 0
                    carve(nr, nc)

        import sys as _sys
        _sys.setrecursionlimit(max(5000, N*N*2))
        carve(1, 1)

        open_cells = list(zip(*np.where(maze == 0)))
        pacman_pos = min(open_cells,
                         key=lambda p: abs(p[0]-N//2)+abs(p[1]-N//2))
        cands = [p for p in open_cells
                 if abs(p[0]-pacman_pos[0])+abs(p[1]-pacman_pos[1]) > N//3]
        if len(cands) < n_ghosts:
            cands = open_cells
        ghost_positions = []
        used = {pacman_pos}
        for _ in range(int(n_ghosts)):
            for _ in range(200):
                pos = cands[rng.integers(len(cands))]
                if pos not in used:
                    ghost_positions.append(pos)
                    used.add(pos)
                    break

        g_cols  = ["#FF0000","#FFB8FF","#00FFFF","#FFB852"]
        g_names = ["Blinky","Pinky","Inky","Clyde"]

        def bfs(start, goal):
            if start == goal:
                return [start]
            prev = {start: None}
            q = [start]
            qi = 0
            while qi < len(q):
                r, c = q[qi]
                qi += 1
                if (r, c) == goal:
                    break
                for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                    nr, nc = r+dr, c+dc
                    if 0<=nr<N and 0<=nc<N and maze[nr,nc]==0 and (nr,nc) not in prev:
                        prev[(nr, nc)] = (r, c)
                        q.append((nr, nc))
            path = []
            cur = goal
            while cur is not None:
                path.append(cur)
                cur = prev.get(cur)
            path.reverse()
            return path if path and path[0] == start else []

        ghost_paths = [bfs(gp, pacman_pos) for gp in ghost_positions]

        fig, ax = plt.subplots(figsize=(7, 7), facecolor="#000033")
        ax.set_facecolor("#000033")
        ax.set_xlim(-0.5, N-0.5)
        ax.set_ylim(-0.5, N-0.5)
        ax.set_aspect("equal")
        ax.axis("off")

        img = np.zeros((N, N, 3), dtype=float)
        img[maze==1] = [0.05, 0.05, 0.55]
        img[maze==0] = [0.02, 0.02, 0.05]
        ax.imshow(img, origin="upper", interpolation="nearest", zorder=1,
                  extent=[-0.5, N-0.5, -0.5, N-0.5])

        for path, gcol in zip(ghost_paths, g_cols):
            if len(path) < 2:
                continue
            ys = [N-1-p[0] for p in path]
            xs = [p[1] for p in path]
            ax.plot(xs, ys, color=gcol, lw=2.5, alpha=0.55, zorder=2,
                    solid_capstyle="round")
            ax.scatter(xs[1:-1], ys[1:-1], s=8, color=gcol,
                       alpha=0.35, zorder=3, linewidths=0)

        def draw_ghost(r, c, color, label):
            x = c
            y = N-1-r
            ax.add_patch(patches.FancyBboxPatch(
                (x-0.38, y-0.42), 0.76, 0.80, boxstyle="round,pad=0.05",
                facecolor=color, edgecolor="none", zorder=5))
            for bi in range(3):
                ax.add_patch(patches.Circle(
                    (x-0.32+bi*0.26, y-0.42), 0.13,
                    facecolor=color, edgecolor="none", zorder=5))
            for ex in [x-0.14, x+0.14]:
                ax.add_patch(patches.Circle((ex, y+0.12), 0.10,
                             facecolor="white", zorder=6))
                ax.add_patch(patches.Circle((ex+0.04, y+0.08), 0.05,
                             facecolor="#000080", zorder=7))
            ax.text(x, y-0.65, label, ha="center", va="top",
                    color=color, fontsize=5, fontweight="bold", zorder=8)

        for gi, (gp, gcol) in enumerate(zip(ghost_positions, g_cols[:len(ghost_positions)])):
            draw_ghost(gp[0], gp[1], gcol,
                       g_names[gi] if gi < len(g_names) else f"G{gi+1}")

        pr, pc = pacman_pos
        px_x, px_y = pc, N-1-pr
        ax.add_patch(patches.Wedge(
            (px_x, px_y), 0.42, 30, 330,
            facecolor="#FFE000", edgecolor="none", zorder=5))
        ax.add_patch(patches.Circle(
            (px_x+0.10, px_y+0.18), 0.06, facecolor="black", zorder=6))

        for (pr2,pc2) in open_cells:
            if (pr2, pc2) == pacman_pos or any((pr2, pc2) == gp for gp in ghost_positions):
                continue
            ax.add_patch(patches.Circle(
                (pc2, N-1-pr2), 0.06, facecolor="#ffee88",
                alpha=0.3, edgecolor="none", zorder=2))

        ax.set_title(f"Pac-Man Ghost Pathfinding — BFS on {N}x{N} maze",
                     color="#aaaaaa", fontsize=10, pad=6)
        self._fig = fig
        plt.tight_layout()
        plt.show()
        plt.close(fig)

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=21, min=11, max=41, step=2,
                              description="maze_size"),
            widgets.IntSlider(value=4, min=1, max=4, description="n_ghosts"),
            widgets.IntSlider(value=5, min=0, max=99, description="seed"),
        ]


# ── 67. Platformer Terrain Gen ────────────────────────────────────────────────

class PlatformerTerrainRenderer(BasePattern):
    name = "Platformer Terrain Gen"
    group = "2D Game-Style"

    def render(self, resolution="Low", palette="Inferno", speed=1.0,
               seed=42, n_platforms=8, style=0, **kwargs):
        from scipy.interpolate import interp1d
        rng  = np.random.default_rng(int(seed))
        style = int(style) % 3      # 0=grassy  1=cave  2=snow
        W = 200                      # terrain sample points

        # ── 1D fBm terrain height ──────────────────────────────────────────
        def fbm1d(n, octaves=4, scale=20):
            h = np.zeros(n)
            amp, total = 1.0, 0.0
            for k in range(octaves):
                freq = 2 ** k
                pts  = max(4, n // scale * freq + 2)
                ctrl = rng.uniform(0, 1, pts)
                f    = interp1d(np.linspace(0, 1, pts), ctrl, kind='cubic')
                h   += amp * f(np.linspace(0, 1, n))
                total += amp
                amp  *= 0.5
            return h / total

        ground = fbm1d(W)
        ground = 0.08 + 0.38 * (ground - ground.min()) / (
                 ground.max() - ground.min() + 1e-9)

        # ── Style palette ──────────────────────────────────────────────────
        if style == 0:     # grassy
            bg_col, dirt_col, grass_col = "#87CEEB", "#7a4a1e", "#3d7a2e"
            plat_col, plat_top_col = "#5c4a3a", "#7a6040"
            title_col = "#224422"
        elif style == 1:   # cave
            bg_col, dirt_col, grass_col = "#111120", "#3a3a4e", "#5a5a6e"
            plat_col, plat_top_col = "#404055", "#6070a0"
            title_col = "#aaaacc"
        else:              # snow
            bg_col, dirt_col, grass_col = "#b0cce8", "#708090", "#f0f4f8"
            plat_col, plat_top_col = "#808898", "#c0ccd8"
            title_col = "#334455"

        # ── Floating platforms ─────────────────────────────────────────────
        platforms = []
        for _ in range(int(n_platforms)):
            px = rng.uniform(0.04, 0.82)
            py = rng.uniform(0.32, 0.68)
            pw = rng.uniform(0.06, 0.16)
            # Reject platforms that sit below the terrain height at that x
            gidx = int(np.clip(px * W, 0, W - 1))
            if py > ground[gidx] + 0.08:
                platforms.append((px, py, pw))

        # ── Coins ──────────────────────────────────────────────────────────
        coins = []
        for _ in range(14):
            if rng.random() < 0.55 and platforms:
                pp = platforms[rng.integers(len(platforms))]
                cx = pp[0] + rng.uniform(0.01, max(0.01, pp[2] - 0.02))
                cy = pp[1] + 0.032
            else:
                cx  = rng.uniform(0.03, 0.97)
                gidx = int(np.clip(cx * W, 0, W - 1))
                cy  = ground[gidx] + 0.04
            coins.append((cx, cy))

        # ── Draw ──────────────────────────────────────────────────────────
        fig, ax = plt.subplots(figsize=(10, 5), facecolor=bg_col)
        ax.set_facecolor(bg_col)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect("auto")
        ax.axis("off")

        # Sky gradient (20 bands)
        sky_top = np.array(patches.mcolors.to_rgb(bg_col)) * 0.85 + 0.15
        sky_bot = np.array(patches.mcolors.to_rgb(bg_col))
        for i in range(20):
            t   = i / 19
            col = (1 - t) * sky_top + t * sky_bot
            y0  = 0.5 + t * 0.5 / 20
            ax.axhspan(y0, y0 + 0.5 / 20 + 0.002,
                       facecolor=col, edgecolor="none", zorder=0)

        # Ground fill
        xs = np.linspace(0, 1, W)
        ax.fill(np.concatenate([[0], xs, [1]]),
                np.concatenate([[0], ground, [0]]),
                color=dirt_col, zorder=2)

        # Grass top strip
        for i in range(W - 1):
            ax.fill([i/W, (i+1)/W, (i+1)/W, i/W],
                    [ground[i], ground[i+1],
                     ground[i+1] + 0.013, ground[i] + 0.013],
                    color=grass_col, zorder=3, linewidth=0)

        # Platforms
        for (px2, py2, pw) in platforms:
            ax.add_patch(patches.FancyBboxPatch(
                (px2, py2 - 0.018), pw, 0.026,
                boxstyle="round,pad=0.002",
                facecolor=plat_col, edgecolor="none", zorder=4))
            ax.add_patch(patches.Rectangle(
                (px2, py2 + 0.005), pw, 0.009,
                facecolor=plat_top_col, edgecolor="none", zorder=5))

        # Coins
        coin_col = "#FFD700"
        for (cx2, cy2) in coins:
            ax.add_patch(patches.Circle((cx2, cy2), 0.009,
                         facecolor=coin_col, edgecolor="#b8940a",
                         linewidth=0.7, zorder=6))
            ax.add_patch(patches.Circle((cx2 - 0.002, cy2 + 0.002),
                         0.004, facecolor="#ffe566",
                         edgecolor="none", zorder=7))

        # Player (small platformer hero)
        p_xi = W // 5
        px3  = p_xi / W
        py3  = ground[p_xi] + 0.013
        body_col = "#2244cc"
        ax.add_patch(patches.FancyBboxPatch(
            (px3 - 0.011, py3), 0.022, 0.032,
            boxstyle="round,pad=0.002",
            facecolor=body_col, edgecolor="none", zorder=8))
        ax.add_patch(patches.Circle(
            (px3, py3 + 0.043), 0.014,
            facecolor="#f4c68c", edgecolor="none", zorder=8))
        # Hat
        ax.add_patch(patches.Rectangle(
            (px3 - 0.014, py3 + 0.048), 0.028, 0.010,
            facecolor="#cc2222", edgecolor="none", zorder=9))
        ax.add_patch(patches.Rectangle(
            (px3 - 0.010, py3 + 0.058), 0.020, 0.013,
            facecolor="#cc2222", edgecolor="none", zorder=9))

        style_names = ["Grassy", "Cave", "Snow"]
        ax.set_title(
            f"Platformer Terrain — {style_names[style]} | "
            f"{len(platforms)} platforms, {len(coins)} coins",
            color=title_col, fontsize=10, pad=6)

        self._fig = fig
        plt.tight_layout()
        plt.show()
        plt.close(fig)

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.IntSlider(value=42, min=0, max=999, description="seed"),
            widgets.IntSlider(value=8, min=2, max=16, description="n_platforms"),
            widgets.Dropdown(
                options=[("Grassy", 0), ("Cave", 1), ("Snow", 2)],
                value=0, description="style"),
        ]


# ── 68. Bullet Hell Pattern ───────────────────────────────────────────────────

class BulletHellRenderer(BasePattern):
    name = "Bullet Hell Pattern"
    group = "2D Game-Style"

    def render(self, resolution="Low", palette="Inferno", speed=1.0,
               pattern=0, n_bullets=16, n_rings=5, seed=0, **kwargs):
        from engines.color_utils import ColorUtils
        rng     = np.random.default_rng(int(seed))
        pattern = int(pattern) % 5
        n_b     = int(n_bullets)
        n_r     = int(n_rings)
        cmap    = ColorUtils.make_colormap(palette)

        # ── Compute bullet positions (x, y, age_t ∈ [0,1]) ──────────────
        bullets = []   # (x, y, t)

        if pattern == 0:          # Circular burst — concentric rings
            for ring in range(n_r):
                radius = 0.15 + ring * 0.18
                offset = ring * (np.pi / n_b)   # stagger each ring
                for b in range(n_b):
                    angle  = 2 * np.pi * b / n_b + offset
                    bullets.append((radius * np.cos(angle),
                                    radius * np.sin(angle),
                                    ring / max(n_r - 1, 1)))

        elif pattern == 1:        # Double spiral
            steps = n_r * 4
            for step in range(steps):
                for arm in range(2):
                    radius = 0.08 + step * 0.08
                    if radius > 1.05:
                        continue
                    for b in range(n_b // 2):
                        angle = (2 * np.pi * b / max(n_b // 2, 1)
                                 + step * 0.30
                                 + arm * np.pi)
                        bullets.append((radius * np.cos(angle),
                                        radius * np.sin(angle),
                                        step / max(steps - 1, 1)))

        elif pattern == 2:        # Aimed fan — spreading upward
            spread = np.pi * 0.5
            for ring in range(n_r):
                radius = 0.15 + ring * 0.18
                for b in range(n_b):
                    angle = (np.pi / 2
                             - spread / 2
                             + spread * b / max(n_b - 1, 1))
                    bullets.append((radius * np.cos(angle),
                                    radius * np.sin(angle),
                                    ring / max(n_r - 1, 1)))

        elif pattern == 3:        # 8-arm star cross
            n_arms = 8
            for ring in range(n_r):
                radius = 0.15 + ring * 0.18
                for arm in range(n_arms):
                    base = 2 * np.pi * arm / n_arms
                    for sub in range(-1, 2):
                        angle = base + sub * 0.10
                        bullets.append((radius * np.cos(angle),
                                        radius * np.sin(angle),
                                        ring / max(n_r - 1, 1)))

        elif pattern == 4:        # Randomised scatter
            for ring in range(n_r):
                radius  = 0.15 + ring * 0.18
                angles  = rng.uniform(0, 2 * np.pi, n_b)
                for angle in angles:
                    bullets.append((radius * np.cos(angle),
                                    radius * np.sin(angle),
                                    ring / max(n_r - 1, 1)))

        # ── Draw ──────────────────────────────────────────────────────────
        fig, ax = plt.subplots(figsize=(7, 7), facecolor="#040408")
        ax.set_facecolor("#040408")
        ax.set_xlim(-1.25, 1.25)
        ax.set_ylim(-1.25, 1.25)
        ax.set_aspect("equal")
        ax.axis("off")

        # Faint trajectory guide rings
        for ring in range(n_r):
            r = 0.15 + ring * 0.18
            circle = plt.Circle((0, 0), r, fill=False,
                                 color="white", lw=0.25, alpha=0.07, zorder=1)
            ax.add_patch(circle)

        # Bullets (outer glow + core dot)
        for bx, by, t in bullets:
            if np.hypot(bx, by) > 1.15:
                continue
            col  = cmap(t)
            size = max(2, 55 * (1 - t * 0.4))
            ax.scatter([bx], [by], s=size * 2.5, color=[col],
                       alpha=0.18, zorder=4, linewidths=0)
            ax.scatter([bx], [by], s=size, color=[col],
                       alpha=0.90, zorder=5, linewidths=0)

        # Boss sprite
        for r2, col2, a2 in [(0.10, "#aa1111", 1.0),
                              (0.07, "#dd2222", 1.0),
                              (0.04, "#ff8888", 1.0)]:
            ax.add_patch(plt.Circle((0, 0), r2,
                                    facecolor=col2, edgecolor="none",
                                    alpha=a2, zorder=10))

        # Player triangle at top
        ax.add_patch(patches.RegularPolygon(
            (0, 1.10), 3, radius=0.065,
            facecolor="#4499ff", edgecolor="#88ccff",
            linewidth=1.0, orientation=np.pi, zorder=10))

        pattern_names = ["Circular Burst", "Double Spiral", "Aimed Fan",
                         "Cross Star", "Random Scatter"]
        ax.set_title(
            f"Bullet Hell — {pattern_names[pattern]} | "
            f"{n_b} bullets x {n_r} rings",
            color="#aaaaaa", fontsize=10, pad=6)

        self._fig = fig
        plt.tight_layout()
        plt.show()
        plt.close(fig)

    def get_controls(self):
        import ipywidgets as widgets
        return [
            widgets.Dropdown(
                options=[("Circular Burst", 0), ("Double Spiral", 1),
                         ("Aimed Fan", 2), ("Cross Star", 3),
                         ("Random Scatter", 4)],
                value=0, description="pattern"),
            widgets.IntSlider(value=16, min=4, max=32, step=2,
                              description="n_bullets"),
            widgets.IntSlider(value=5, min=2, max=10, description="n_rings"),
            widgets.IntSlider(value=0, min=0, max=99, description="seed"),
        ]

class CardSuitRenderer(_StubMixin, BasePattern):
    name = "Card Suit Patterns"
    group = "2D Game-Style"

class PixelFlagRenderer(_StubMixin, BasePattern):
    name = "Pixel Flag Generator"
    group = "2D Game-Style"

