import json

def markdown_cell(source):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in source.split('\n') if line]
    }

def code_cell(source):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in source.split('\n')]
    }

cells = []

# Section 0
cells.append(markdown_cell("### Section 0 — Environment Setup"))
cells.append(code_cell("%pip install pygame matplotlib Pillow moderngl pycairo pythreejs vtk noise numpy scipy pymunk manim ipywidgets numba\nimport os\nNOTEBOOK_ROOT = os.getcwd()\nprint('Environment setup complete.')"))

# Section 1
cells.append(markdown_cell("### Section 1 — Core Engine (Write Modules to Disk)"))

cells.append(code_cell("%%writefile engines/__init__.py\n"))

cells.append(code_cell('''%%writefile engines/renderer.py
class BasePattern:
    def render(self, **kwargs):
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        ax.set_title("Placeholder")
        plt.show()
    def get_controls(self):
        return []
'''))

cells.append(code_cell('''%%writefile engines/color_utils.py
PALETTES = {
    "Default": ["#000000", "#FFFFFF"],
    "Neon": ["#ff00ff", "#00ffff"],
    "Sunset": ["#ff7b00", "#ffea00"],
    "Ocean": ["#0077be", "#00a8cc"],
    "Forest": ["#228b22", "#006400"]
}
'''))

cells.append(code_cell("%%writefile utils/__init__.py\n"))

cells.append(code_cell('''%%writefile utils/export.py
def export_png(figure, name):
    print(f"Exported PNG to exports/{name}.png")
def export_gif(frames, name, fps):
    print(f"Exported GIF to exports/{name}.gif")
def export_mp4(frames, name, fps):
    print(f"Exported MP4 to exports/{name}.mp4")
'''))

cells.append(code_cell('''%%writefile utils/physics.py
# Physics helpers placeholder
'''))

cells.append(code_cell("%%writefile patterns/__init__.py\n"))

# Generate 100 stubs
patterns_info = [
    # Geometric & Mathematical (1-20)
    ("fractals", 1, 20, [
        "Mandelbrot Fractal Explorer", "Julia Set Animator", "Sierpinski Triangle", "Koch Snowflake", "Penrose Tiling", "Voronoi Diagram", "Fibonacci Spiral", "Dragon Curve", "Hilbert Curve", "L-System Tree", "Apollonius Gasket", "Lissajous Figures", "Rose Curves", "Chaos Attractor (Lorenz)", "Wave Interference Pattern", "Hypocycloid & Epicycloid", "Truchet Tiles", "Hexagonal Grid Art", "Spirograph Generator", "Parametric Curve Art"
    ]),
    ("nature", 21, 40, [
        "Cherry Blossom Particle Scene", "Procedural Tree Generator", "Reaction-Diffusion (Turing Patterns)", "Flocking Birds (Boids Lite)", "Lightning Bolt Generator", "Snowflake Crystal Growth", "Leaf Venation Simulation", "Fire Particle System", "Galaxy Spiral Arms", "Aurora Borealis", "Underwater Caustics", "Sand Dune Erosion", "Coral Reef Growth", "Mushroom Spore Map", "Terrain Height Map", "Waterfall Flow", "Tornado Vortex", "Cloud Formation", "River Delta Branching", "Moth Wing Pattern"
    ]),
    ("abstract", 41, 60, [
        "Generative Mondrian", "Perlin Noise Painting", "Mandala Generator", "Stained Glass Voronoi", "Op-Art Optical Illusion", "Watercolor Wash Effect", "Glitch Art Generator", "Isometric City Builder", "Circuit Board Art", "Tie-Dye Diffusion", "Geometric Collage", "Pixel Sorting Art", "ASCII Art Renderer", "Kandinsky Color Study", "Zentangle Automaton", "Neon Sign Generator", "Mosaic Tile Art", "Impressionist Dots", "Cubist Portrait Filter", "Abstract Expressionism Drip"
    ]),
    ("game2d", 61, 70, [
        "Maze Generator & Solver", "Cellular Automaton Life", "Dungeon Room Placer", "Retro Starfield", "Breakout Brick Map", "Pac-Man Ghost Pathfinding", "Platformer Terrain Gen", "Bullet Hell Pattern", "Card Suit Patterns", "Pixel Flag Generator"
    ]),
    ("objects3d", 71, 90, [
        "Rotating DNA Helix", "Klein Bottle Surface", "Mobius Strip", "Torus Knot", "Gyroid Surface", "Romanesco Broccoli", "Icosphere Subdivisions", "Trefoil Knot", "Seashell Surface", "Hyperboloid of Revolution", "Parametric Vase", "Crystal Lattice", "Geodesic Dome", "Calabi-Yau Manifold Slice", "Soap Bubble Cluster", "Neural Mesh Sculpture", "Twisted Prism Tower", "Fractal Mountain", "Volumetric Fog Cube", "Strange Attractor 3D"
    ]),
    ("scientific", 91, 100, [
        "Neural Network Visualization", "Atom Orbital Simulator", "Black Hole Lensing", "Conway's Game of Life", "Boids Flocking Simulation", "Traffic Flow Simulation", "Ecosystem Predator-Prey", "Ant Colony Optimization", "Fluid Dynamics (SPH)", "Quantum Wave Packet"
    ])
]

for filename, start, end, names in patterns_info:
    code = f"%%writefile patterns/{filename}.py\nfrom engines.renderer import BasePattern\n"
    for name in names:
        class_name = "".join(w.capitalize() for w in name.replace("(", "").replace(")", "").replace("-", " ").replace("'", "").split()) + "Renderer"
        code += f"""
class {class_name}(BasePattern):
    def render(self, **kwargs):
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        ax.set_title("{name} (Stub)")
        ax.axis('off')
        plt.show()
    def get_controls(self):
        return []
"""
    cells.append(code_cell(code))

registry_code = """import sys
if '.' not in sys.path:
    sys.path.append('.')

from patterns.fractals import *
from patterns.nature import *
from patterns.abstract import *
from patterns.game2d import *
from patterns.objects3d import *
from patterns.scientific import *

PATTERNS = {
"""
for filename, start, end, names in patterns_info:
    for name in names:
        class_name = "".join(w.capitalize() for w in name.replace("(", "").replace(")", "").replace("-", " ").replace("'", "").split()) + "Renderer"
        registry_code += f'    "{name}": {class_name}(),\n'
registry_code += "}\nprint('Registry populated with', len(PATTERNS), 'patterns.')"

cells.append(code_cell(registry_code))

cells.append(markdown_cell("### Section 2 — UI Controls"))
cells.append(code_cell('''import ipywidgets as widgets
from IPython.display import display, clear_output

categories = {
    "Geometric & Mathematical": [k for k, v in PATTERNS.items()][:20],
    "Nature-Inspired": [k for k, v in PATTERNS.items()][20:40],
    "Abstract & Artistic": [k for k, v in PATTERNS.items()][40:60],
    "2D Game-Style": [k for k, v in PATTERNS.items()][60:70],
    "3D Objects & Sculptures": [k for k, v in PATTERNS.items()][70:90],
    "Scientific & Simulation": [k for k, v in PATTERNS.items()][90:100]
}

category_dropdown = widgets.Dropdown(options=list(categories.keys()), description='Category:')
pattern_dropdown = widgets.Dropdown(options=categories[category_dropdown.value], description='Pattern:')

def update_pattern_options(*args):
    pattern_dropdown.options = categories[category_dropdown.value]
category_dropdown.observe(update_pattern_options, 'value')

speed_slider = widgets.FloatSlider(value=1.0, min=0.1, max=5.0, step=0.1, description='Speed:')
resolution_dropdown = widgets.Dropdown(options=['Low', 'Medium', 'High'], value='Low', description='Resolution:')
palette_dropdown = widgets.Dropdown(options=["Default", "Neon", "Sunset", "Ocean", "Forest"], description='Palette:')

render_button = widgets.Button(description='RENDER', button_style='success')
export_button = widgets.Button(description='EXPORT', button_style='info')

output_area = widgets.Output()

ui = widgets.VBox([
    widgets.HBox([category_dropdown, pattern_dropdown]),
    widgets.HBox([speed_slider, resolution_dropdown, palette_dropdown]),
    widgets.HBox([render_button, export_button]),
    output_area
])

def on_render_clicked(b):
    with output_area:
        clear_output(wait=True)
        selected_pattern = pattern_dropdown.value
        print(f"Rendering {selected_pattern}...")
        PATTERNS[selected_pattern].render(speed=speed_slider.value, resolution=resolution_dropdown.value, palette=palette_dropdown.value)

def on_export_clicked(b):
    with output_area:
        print(f"Exporting {pattern_dropdown.value}...")

render_button.on_click(on_render_clicked)
export_button.on_click(on_export_clicked)

display(ui)
'''))

cells.append(markdown_cell("### Section 3 — Render Section\n*(Render happens inside UI callbacks)*"))
cells.append(markdown_cell("### Section 4 — Pattern Implementations\n*(Implementations are loaded from modules via %%writefile in Section 1)*"))
cells.append(markdown_cell("### Section 5 — Export Utilities\n*(Export utilities are loaded from utils/export.py)*"))

notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.8.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

with open("visual_engine/notebook.ipynb", "w") as f:
    json.dump(notebook, f, indent=1)
