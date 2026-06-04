"""
Scientific & Simulation Patterns (91–100)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from engines.renderer import BasePattern


# ─────────────────────────────────────────────────────────────────────────────────
# 91 — Neural Network Visualization
# ─────────────────────────────────────────────────────────────────────────────────
class NeuralNetworkVizRenderer(BasePattern):
    """91 — Neural Network Visualization"""
    name  = "Neural Network Visualization"
    group = "Scientific & Simulation"

    def render(self, resolution="Low", palette="Neon Cyberpunk", speed=1.0,
               layer_sizes="4,6,6,4,2", show_weights=True, activation_seed=42, **kwargs):
        PALETTES = {
            "Inferno":        ["#200060", "#8b0aff", "#ff6b35", "#ffe04b"],
            "Ocean Depths":   ["#0a1628", "#0066cc", "#00ccff", "#80ffee"],
            "Neon Cyberpunk":  ["#0d0221", "#ff006e", "#00f5d4", "#f9c80e"],
            "Forest":         ["#1a2e1a", "#2d6a2d", "#52b252", "#b8f0b8"],
            "Sunset Blaze":   ["#1a0505", "#cc2200", "#ff8800", "#ffee44"],
            "Arctic Aurora":  ["#050a14", "#0033aa", "#00ddaa", "#aaffee"],
            "Monochrome":     ["#111111", "#444444", "#aaaaaa", "#ffffff"],
            "Lava Flow":      ["#1a0000", "#aa1100", "#ff4400", "#ffcc00"],
        }
        cols = PALETTES.get(palette, PALETTES["Neon Cyberpunk"])
        try:
            layers = [max(1, int(x.strip())) for x in str(layer_sizes).split(",")]
        except Exception:
            layers = [4, 6, 6, 4, 2]
        layers = layers[:8]
        rng = np.random.default_rng(int(activation_seed))
        fig, ax = plt.subplots(figsize=(10, 7), facecolor="#07050f")
        ax.set_facecolor("#07050f")
        ax.set_aspect("equal")
        ax.axis("off")
        from matplotlib.colors import LinearSegmentedColormap
        from matplotlib.collections import LineCollection
        cmap_act = LinearSegmentedColormap.from_list(
            "act", [cols[0], cols[1], cols[2], cols[3]], N=256)
        n_layers    = len(layers)
        x_positions = np.linspace(0.1, 0.9, n_layers)
        max_nodes   = max(layers)
        node_pos, node_act = [], []
        for li, n in enumerate(layers):
            xs = np.full(n, x_positions[li])
            ys = np.linspace(0.5 - (n-1)*0.07, 0.5 + (n-1)*0.07, n)
            node_pos.append(np.column_stack([xs, ys]))
            node_act.append(rng.uniform(0.05, 0.95, n))
        if show_weights:
            for li in range(n_layers - 1):
                segs, colors_w = [], []
                for (px, py) in node_pos[li]:
                    for (qx, qy) in node_pos[li + 1]:
                        w = rng.uniform(-1.0, 1.0)
                        segs.append([(px, py), (qx, qy)])
                        if w >= 0:
                            c = cmap_act(0.3 + 0.5 * w)
                        else:
                            c = (*plt.cm.cool(0.3 - 0.3*w)[:3], 0.3)
                        colors_w.append((*c[:3], abs(w)*0.55 + 0.05))
                ax.add_collection(LineCollection(segs, colors=colors_w,
                                                 linewidths=0.7, zorder=1))
        node_r = max(0.012, min(0.018, 0.6 / (max_nodes * 8)))
        for li, (positions, activations) in enumerate(zip(node_pos, node_act)):
            for (px, py), act in zip(positions, activations):
                ax.add_patch(plt.Circle((px, py), node_r*2.2,
                                        color=cmap_act(act), alpha=0.12, zorder=2))
                ax.add_patch(plt.Circle((px, py), node_r,
                                        color=cmap_act(act), zorder=3))
                ax.text(px, py, f"{act:.2f}", ha="center", va="center",
                        fontsize=5.5, color="white", fontweight="bold", zorder=4)
        layer_labels = (["Input"]
                        + [f"Hidden {i}" for i in range(1, n_layers-1)]
                        + ["Output"])
        for li, (xp, lbl) in enumerate(zip(x_positions, layer_labels)):
            ax.text(xp, 0.04, lbl, ha="center", va="center",
                    fontsize=8, color=cols[2], fontweight="bold")
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        ax.set_title("Neural Network Visualization", color=cols[3],
                     fontsize=13, fontweight="bold", pad=10)
        plt.tight_layout()
        self._fig = fig
        plt.show()
        plt.close(fig)

    def get_controls(self):
        import ipywidgets as w
        return [
            w.Text(value="4,6,6,4,2",           description="layer_sizes"),
            w.Checkbox(value=True,                description="show_weights"),
            w.IntSlider(value=42, min=0, max=999,
                        step=1,                   description="activation_seed"),
        ]

# ─────────────────────────────────────────────────────────────────────────────────
# Remaining stubs
# ─────────────────────────────────────────────────────────────────────────────────
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

class TrafficFlowRenderer(_StubMixin, BasePattern):
    name = "Traffic Flow Simulation"
    group = "Scientific & Simulation"

class EcosystemRenderer(_StubMixin, BasePattern):
    name = "Ecosystem Predator-Prey"
    group = "Scientific & Simulation"

class AntColonyRenderer(_StubMixin, BasePattern):
    name = "Ant Colony Optimization"
    group = "Scientific & Simulation"

class FluidDynamicsRenderer(_StubMixin, BasePattern):
    name = "Fluid Dynamics (SPH)"
    group = "Scientific & Simulation"

class QuantumWaveRenderer(_StubMixin, BasePattern):
    name = "Quantum Wave Packet"
    group = "Scientific & Simulation"
