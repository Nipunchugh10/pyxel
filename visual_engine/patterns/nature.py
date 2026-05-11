"""
Nature-Inspired Patterns (21–40)
Each class is a stub that will be replaced with full implementations during Phase 1.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import sys, os
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
        ax.text(0.5, 0.42, "⏳ Coming Soon", ha="center", va="center",
                fontsize=11, color="#888", style="italic",
                transform=ax.transAxes)
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        ax.axis("off")
        plt.tight_layout()
        plt.show()
        plt.close(fig)

    def get_controls(self):
        return []


class CherryBlossomRenderer(_StubMixin, BasePattern):
    name = "Cherry Blossom Particle Scene"
    group = "Nature-Inspired"

class ProceduralTreeRenderer(_StubMixin, BasePattern):
    name = "Procedural Tree Generator"
    group = "Nature-Inspired"

class ReactionDiffusionRenderer(_StubMixin, BasePattern):
    name = "Reaction-Diffusion (Turing Patterns)"
    group = "Nature-Inspired"

class FlockingBirdsRenderer(_StubMixin, BasePattern):
    name = "Flocking Birds (Boids Lite)"
    group = "Nature-Inspired"

class LightningBoltRenderer(_StubMixin, BasePattern):
    name = "Lightning Bolt Generator"
    group = "Nature-Inspired"

class SnowflakeCrystalRenderer(_StubMixin, BasePattern):
    name = "Snowflake Crystal Growth"
    group = "Nature-Inspired"

class LeafVenationRenderer(_StubMixin, BasePattern):
    name = "Leaf Venation Simulation"
    group = "Nature-Inspired"

class FireParticleRenderer(_StubMixin, BasePattern):
    name = "Fire Particle System"
    group = "Nature-Inspired"

class GalaxySpiralRenderer(_StubMixin, BasePattern):
    name = "Galaxy Spiral Arms"
    group = "Nature-Inspired"

class AuroraBorealisRenderer(_StubMixin, BasePattern):
    name = "Aurora Borealis"
    group = "Nature-Inspired"

class UnderwaterCausticsRenderer(_StubMixin, BasePattern):
    name = "Underwater Caustics"
    group = "Nature-Inspired"

class SandDuneRenderer(_StubMixin, BasePattern):
    name = "Sand Dune Erosion"
    group = "Nature-Inspired"

class CoralReefRenderer(_StubMixin, BasePattern):
    name = "Coral Reef Growth"
    group = "Nature-Inspired"

class MushroomSporeRenderer(_StubMixin, BasePattern):
    name = "Mushroom Spore Map"
    group = "Nature-Inspired"

class TerrainHeightRenderer(_StubMixin, BasePattern):
    name = "Terrain Height Map"
    group = "Nature-Inspired"

class WaterfallFlowRenderer(_StubMixin, BasePattern):
    name = "Waterfall Flow"
    group = "Nature-Inspired"

class TornadoVortexRenderer(_StubMixin, BasePattern):
    name = "Tornado Vortex"
    group = "Nature-Inspired"

class CloudFormationRenderer(_StubMixin, BasePattern):
    name = "Cloud Formation"
    group = "Nature-Inspired"

class RiverDeltaRenderer(_StubMixin, BasePattern):
    name = "River Delta Branching"
    group = "Nature-Inspired"

class MothWingRenderer(_StubMixin, BasePattern):
    name = "Moth Wing Pattern"
    group = "Nature-Inspired"
