"""
Pyxel Canvas — Pattern Registry
All 100 pattern classes are imported here and registered in the PATTERNS dict.
Grouped by category for the UI.
"""

# ── Geometric & Mathematical (1–20) ──────────────────────────────
from .fractals import (
    MandelbrotRenderer, JuliaRenderer, SierpinskiRenderer,
    KochRenderer, PenroseRenderer, VoronoiRenderer,
    FibonacciRenderer, DragonCurveRenderer, HilbertCurveRenderer,
    LSystemTreeRenderer, ApolloniusRenderer, LissajousRenderer,
    RoseCurvesRenderer, LorenzAttractorRenderer, WaveInterferenceRenderer,
    HypocycloidRenderer, TruchetRenderer, HexGridRenderer,
    SpirographRenderer, ParametricCurveRenderer,
)

# ── Nature-Inspired (21–40) ──────────────────────────────────────
from .nature import (
    CherryBlossomRenderer, ProceduralTreeRenderer,
    ReactionDiffusionRenderer, FlockingBirdsRenderer,
    LightningBoltRenderer, SnowflakeCrystalRenderer,
    LeafVenationRenderer, FireParticleRenderer,
    GalaxySpiralRenderer, AuroraBorealisRenderer,
    UnderwaterCausticsRenderer, SandDuneRenderer,
    CoralReefRenderer, MushroomSporeRenderer,
    TerrainHeightRenderer, WaterfallFlowRenderer,
    TornadoVortexRenderer, CloudFormationRenderer,
    RiverDeltaRenderer, MothWingRenderer,
)

# ── Abstract & Artistic (41–60) ──────────────────────────────────
from .abstract import (
    MondrianRenderer, PerlinNoiseRenderer, MandalaRenderer,
    StainedGlassRenderer, OpArtRenderer, WatercolorRenderer,
    GlitchArtRenderer, IsometricCityRenderer, CircuitBoardRenderer,
    TieDyeRenderer, GeometricCollageRenderer, PixelSortingRenderer,
    AsciiArtRenderer, KandinskyRenderer, ZentangleRenderer,
    NeonSignRenderer, MosaicTileRenderer, ImpressionistDotsRenderer,
    CubistRenderer, AbstractDripRenderer,
)

# ── 2D Game-Style (61–70) ────────────────────────────────────────
from .game2d import (
    MazeRenderer, CellularAutomatonRenderer, DungeonRenderer,
    RetroStarfieldRenderer, BreakoutBrickRenderer,
    PacManGhostRenderer, PlatformerTerrainRenderer,
    BulletHellRenderer, CardSuitRenderer, PixelFlagRenderer,
)

# ── 3D Objects & Sculptures (71–90) ──────────────────────────────
from .objects3d import (
    DNAHelixRenderer, KleinBottleRenderer, MobiusStripRenderer,
    TorusKnotRenderer, GyroidRenderer, RomanescoRenderer,
    IcosphereRenderer, TrefoilKnotRenderer, SeashellRenderer,
    HyperboloidRenderer, ParametricVaseRenderer, CrystalLatticeRenderer,
    GeodesicDomeRenderer, CalabiYauRenderer, SoapBubbleRenderer,
    NeuralMeshRenderer, TwistedPrismRenderer, FractalMountainRenderer,
    VolumetricFogRenderer, StrangeAttractor3DRenderer,
)

# ── Scientific & Simulation (91–100) ─────────────────────────────
from .scientific import (
    NeuralNetworkVizRenderer, AtomOrbitalRenderer,
    BlackHoleLensingRenderer, GameOfLifeRenderer,
    BoidsFlockingRenderer, TrafficFlowRenderer,
    EcosystemRenderer, AntColonyRenderer,
    FluidDynamicsRenderer, QuantumWaveRenderer,
)


# ── Category → Pattern Names mapping (for UI dropdowns) ─────────
CATEGORIES = {
    "Geometric & Mathematical": [
        "Mandelbrot Fractal Explorer", "Julia Set Animator",
        "Sierpinski Triangle", "Koch Snowflake", "Penrose Tiling",
        "Voronoi Diagram", "Fibonacci Spiral", "Dragon Curve",
        "Hilbert Curve", "L-System Tree", "Apollonius Gasket",
        "Lissajous Figures", "Rose Curves", "Chaos Attractor (Lorenz)",
        "Wave Interference Pattern", "Hypocycloid & Epicycloid",
        "Truchet Tiles", "Hexagonal Grid Art", "Spirograph Generator",
        "Parametric Curve Art",
    ],
    "Nature-Inspired": [
        "Cherry Blossom Particle Scene", "Procedural Tree Generator",
        "Reaction-Diffusion (Turing Patterns)", "Flocking Birds (Boids Lite)",
        "Lightning Bolt Generator", "Snowflake Crystal Growth",
        "Leaf Venation Simulation", "Fire Particle System",
        "Galaxy Spiral Arms", "Aurora Borealis",
        "Underwater Caustics", "Sand Dune Erosion",
        "Coral Reef Growth", "Mushroom Spore Map",
        "Terrain Height Map", "Waterfall Flow",
        "Tornado Vortex", "Cloud Formation",
        "River Delta Branching", "Moth Wing Pattern",
    ],
    "Abstract & Artistic": [
        "Generative Mondrian", "Perlin Noise Painting",
        "Mandala Generator", "Stained Glass Voronoi",
        "Op-Art Optical Illusion", "Watercolor Wash Effect",
        "Glitch Art Generator", "Isometric City Builder",
        "Circuit Board Art", "Tie-Dye Diffusion",
        "Geometric Collage", "Pixel Sorting Art",
        "ASCII Art Renderer", "Kandinsky Color Study",
        "Zentangle Automaton", "Neon Sign Generator",
        "Mosaic Tile Art", "Impressionist Dots",
        "Cubist Portrait Filter", "Abstract Expressionism Drip",
    ],
    "2D Game-Style": [
        "Maze Generator & Solver", "Cellular Automaton Life",
        "Dungeon Room Placer", "Retro Starfield",
        "Breakout Brick Map", "Pac-Man Ghost Pathfinding",
        "Platformer Terrain Gen", "Bullet Hell Pattern",
        "Card Suit Patterns", "Pixel Flag Generator",
    ],
    "3D Objects & Sculptures": [
        "Rotating DNA Helix", "Klein Bottle Surface",
        "Mobius Strip", "Torus Knot", "Gyroid Surface",
        "Romanesco Broccoli", "Icosphere Subdivisions",
        "Trefoil Knot", "Seashell Surface",
        "Hyperboloid of Revolution", "Parametric Vase",
        "Crystal Lattice", "Geodesic Dome",
        "Calabi-Yau Manifold Slice", "Soap Bubble Cluster",
        "Neural Mesh Sculpture", "Twisted Prism Tower",
        "Fractal Mountain", "Volumetric Fog Cube",
        "Strange Attractor 3D",
    ],
    "Scientific & Simulation": [
        "Neural Network Visualization", "Atom Orbital Simulator",
        "Black Hole Lensing", "Conway's Game of Life",
        "Boids Flocking Simulation", "Traffic Flow Simulation",
        "Ecosystem Predator-Prey", "Ant Colony Optimization",
        "Fluid Dynamics (SPH)", "Quantum Wave Packet",
    ],
}

# ── Full PATTERNS registry (name → instance) ────────────────────
PATTERNS = {
    # Geometric & Mathematical (1–20)
    "Mandelbrot Fractal Explorer": MandelbrotRenderer(),
    "Julia Set Animator": JuliaRenderer(),
    "Sierpinski Triangle": SierpinskiRenderer(),
    "Koch Snowflake": KochRenderer(),
    "Penrose Tiling": PenroseRenderer(),
    "Voronoi Diagram": VoronoiRenderer(),
    "Fibonacci Spiral": FibonacciRenderer(),
    "Dragon Curve": DragonCurveRenderer(),
    "Hilbert Curve": HilbertCurveRenderer(),
    "L-System Tree": LSystemTreeRenderer(),
    "Apollonius Gasket": ApolloniusRenderer(),
    "Lissajous Figures": LissajousRenderer(),
    "Rose Curves": RoseCurvesRenderer(),
    "Chaos Attractor (Lorenz)": LorenzAttractorRenderer(),
    "Wave Interference Pattern": WaveInterferenceRenderer(),
    "Hypocycloid & Epicycloid": HypocycloidRenderer(),
    "Truchet Tiles": TruchetRenderer(),
    "Hexagonal Grid Art": HexGridRenderer(),
    "Spirograph Generator": SpirographRenderer(),
    "Parametric Curve Art": ParametricCurveRenderer(),
    # Nature-Inspired (21–40)
    "Cherry Blossom Particle Scene": CherryBlossomRenderer(),
    "Procedural Tree Generator": ProceduralTreeRenderer(),
    "Reaction-Diffusion (Turing Patterns)": ReactionDiffusionRenderer(),
    "Flocking Birds (Boids Lite)": FlockingBirdsRenderer(),
    "Lightning Bolt Generator": LightningBoltRenderer(),
    "Snowflake Crystal Growth": SnowflakeCrystalRenderer(),
    "Leaf Venation Simulation": LeafVenationRenderer(),
    "Fire Particle System": FireParticleRenderer(),
    "Galaxy Spiral Arms": GalaxySpiralRenderer(),
    "Aurora Borealis": AuroraBorealisRenderer(),
    "Underwater Caustics": UnderwaterCausticsRenderer(),
    "Sand Dune Erosion": SandDuneRenderer(),
    "Coral Reef Growth": CoralReefRenderer(),
    "Mushroom Spore Map": MushroomSporeRenderer(),
    "Terrain Height Map": TerrainHeightRenderer(),
    "Waterfall Flow": WaterfallFlowRenderer(),
    "Tornado Vortex": TornadoVortexRenderer(),
    "Cloud Formation": CloudFormationRenderer(),
    "River Delta Branching": RiverDeltaRenderer(),
    "Moth Wing Pattern": MothWingRenderer(),
    # Abstract & Artistic (41–60)
    "Generative Mondrian": MondrianRenderer(),
    "Perlin Noise Painting": PerlinNoiseRenderer(),
    "Mandala Generator": MandalaRenderer(),
    "Stained Glass Voronoi": StainedGlassRenderer(),
    "Op-Art Optical Illusion": OpArtRenderer(),
    "Watercolor Wash Effect": WatercolorRenderer(),
    "Glitch Art Generator": GlitchArtRenderer(),
    "Isometric City Builder": IsometricCityRenderer(),
    "Circuit Board Art": CircuitBoardRenderer(),
    "Tie-Dye Diffusion": TieDyeRenderer(),
    "Geometric Collage": GeometricCollageRenderer(),
    "Pixel Sorting Art": PixelSortingRenderer(),
    "ASCII Art Renderer": AsciiArtRenderer(),
    "Kandinsky Color Study": KandinskyRenderer(),
    "Zentangle Automaton": ZentangleRenderer(),
    "Neon Sign Generator": NeonSignRenderer(),
    "Mosaic Tile Art": MosaicTileRenderer(),
    "Impressionist Dots": ImpressionistDotsRenderer(),
    "Cubist Portrait Filter": CubistRenderer(),
    "Abstract Expressionism Drip": AbstractDripRenderer(),
    # 2D Game-Style (61–70)
    "Maze Generator & Solver": MazeRenderer(),
    "Cellular Automaton Life": CellularAutomatonRenderer(),
    "Dungeon Room Placer": DungeonRenderer(),
    "Retro Starfield": RetroStarfieldRenderer(),
    "Breakout Brick Map": BreakoutBrickRenderer(),
    "Pac-Man Ghost Pathfinding": PacManGhostRenderer(),
    "Platformer Terrain Gen": PlatformerTerrainRenderer(),
    "Bullet Hell Pattern": BulletHellRenderer(),
    "Card Suit Patterns": CardSuitRenderer(),
    "Pixel Flag Generator": PixelFlagRenderer(),
    # 3D Objects & Sculptures (71–90)
    "Rotating DNA Helix": DNAHelixRenderer(),
    "Klein Bottle Surface": KleinBottleRenderer(),
    "Mobius Strip": MobiusStripRenderer(),
    "Torus Knot": TorusKnotRenderer(),
    "Gyroid Surface": GyroidRenderer(),
    "Romanesco Broccoli": RomanescoRenderer(),
    "Icosphere Subdivisions": IcosphereRenderer(),
    "Trefoil Knot": TrefoilKnotRenderer(),
    "Seashell Surface": SeashellRenderer(),
    "Hyperboloid of Revolution": HyperboloidRenderer(),
    "Parametric Vase": ParametricVaseRenderer(),
    "Crystal Lattice": CrystalLatticeRenderer(),
    "Geodesic Dome": GeodesicDomeRenderer(),
    "Calabi-Yau Manifold Slice": CalabiYauRenderer(),
    "Soap Bubble Cluster": SoapBubbleRenderer(),
    "Neural Mesh Sculpture": NeuralMeshRenderer(),
    "Twisted Prism Tower": TwistedPrismRenderer(),
    "Fractal Mountain": FractalMountainRenderer(),
    "Volumetric Fog Cube": VolumetricFogRenderer(),
    "Strange Attractor 3D": StrangeAttractor3DRenderer(),
    # Scientific & Simulation (91–100)
    "Neural Network Visualization": NeuralNetworkVizRenderer(),
    "Atom Orbital Simulator": AtomOrbitalRenderer(),
    "Black Hole Lensing": BlackHoleLensingRenderer(),
    "Conway's Game of Life": GameOfLifeRenderer(),
    "Boids Flocking Simulation": BoidsFlockingRenderer(),
    "Traffic Flow Simulation": TrafficFlowRenderer(),
    "Ecosystem Predator-Prey": EcosystemRenderer(),
    "Ant Colony Optimization": AntColonyRenderer(),
    "Fluid Dynamics (SPH)": FluidDynamicsRenderer(),
    "Quantum Wave Packet": QuantumWaveRenderer(),
}
