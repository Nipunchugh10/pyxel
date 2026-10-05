# Changelog

## [1.0.1] — 2026-10-06

### Fixed
- The app could not start when downloaded with a browser: Windows marks
  downloaded files ("Mark of the Web") and .NET then refused to load the app's
  own components, showing "Pyxel Canvas could not start". The app now ships a
  .NET configuration that allows this, and the release check simulates a real
  browser download.
- The start-up error message wrongly blamed WebView2; it now reports the real
  cause and explains how to unblock a download.

## [1.0.0] — 2026-10-06

First release of the **Pyxel Canvas desktop app** for Windows: download one zip,
unzip, run `Pyxel.exe`. No Python or Jupyter required.

### Added
- Desktop app (Edge WebView2 window): welcome page, category/pattern browser,
  live controls, and a side-by-side view of each render and its
  "How This Works" notes, with formulas typeset offline by KaTeX.
- PNG export for every pattern and animated GIF export for the 10 simulations,
  saved to `Pictures\Pyxel`.
- Automated test suite (pytest): every pattern at default, minimum and maximum
  settings, control wiring, animation export, and physics regression tests.

### Fixed
- Atom Orbital Simulator crashed with current SciPy (`sph_harm` was removed).
- Boids separation pulled boids together instead of apart.
- Fluid Dynamics (SPH) was numerically unstable; rewritten as a stable 2D
  weakly-compressible solver (dam break settles at rest density).
- Black Hole accretion disk had zero width.
- Hexagonal Grid "Checkerboard" colouring produced a single colour.
- Procedural Tree hung, and Ant Colony crashed, at maximum slider settings.
- Quantum "well" potential was never drawn; orbital nodal planes showed noise.
- Concept notes: broken LaTeX (`\beta`, `\text`, `\approx`, `\varepsilon`).
- The global Speed slider and 10 Seed sliders did nothing; removed or repurposed.

### Improved
- Up to 36× faster rendering for heavy patterns at maximum settings
  (e.g. Watercolor 51.6 s → 2.2 s, Koch Snowflake 13.9 s → 0.6 s) and 2–8×
  faster GIF export.
