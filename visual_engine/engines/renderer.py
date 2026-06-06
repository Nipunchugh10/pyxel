"""
Core rendering dispatcher — BasePattern base class.

Every pattern in Pyxel Canvas inherits from BasePattern and implements:
    - render(**kwargs)     → produces the visual output
    - get_controls()       → returns a list of ipywidgets controls
"""

from abc import ABC, abstractmethod
import matplotlib
try:
    # Use inline backend when running inside Jupyter
    get_ipython()  # noqa: F821 — only exists in IPython
    matplotlib.use("module://matplotlib_inline.backend_inline")
except NameError:
    # Non-interactive: use Agg (no GUI window)
    matplotlib.use("agg")
import matplotlib.pyplot as plt


class BasePattern(ABC):
    """Abstract base class for all 100 Pyxel Canvas patterns."""

    # Subclasses should override these
    name: str = "Unnamed Pattern"
    group: str = "Uncategorized"
    description: str = ""

    def __init__(self):
        self._fig = None

    # ── Public Interface ──────────────────────────────────────────

    @abstractmethod
    def render(self, **kwargs):
        """
        Produce the visual output for this pattern.

        Parameters are passed from the UI controls. Every implementation
        must accept **kwargs so unknown parameters are silently ignored.

        Must call plt.show() or return an IPython-displayable object.
        """
        ...

    @abstractmethod
    def get_controls(self):
        """
        Return a list of ipywidgets controls specific to this pattern.

        Each element should be an ipywidgets widget (Slider, Dropdown, etc.).
        The UI layer reads `.description` and `.value` from each widget.
        Return an empty list if the pattern has no extra controls.
        """
        ...

    # ── Animation Support ─────────────────────────────────────────

    def animate(self, n_frames=30, fps=15, **kwargs):
        """
        Override in animatable patterns to produce a frame sequence.

        Returns a list of (H, W, 3) uint8 numpy arrays suitable for
        export_gif() / export_mp4(), or None if not animatable.
        """
        return None

    @property
    def is_animatable(self):
        """True if this pattern overrides animate() and supports frame export."""
        return type(self).animate is not BasePattern.animate

    # ── Helpers ───────────────────────────────────────────────────

    def _create_figure(self, figsize=(8, 8), dpi=100, bg_color="#0a0a0a"):
        """Create a matplotlib figure with dark background."""
        fig, ax = plt.subplots(figsize=figsize, dpi=dpi,
                               facecolor=bg_color)
        ax.set_facecolor(bg_color)
        self._fig = fig
        return fig, ax

    def _close_figure(self):
        """Explicitly close the stored figure to free memory."""
        if self._fig is not None:
            plt.close(self._fig)
            self._fig = None

    def _resolve_resolution(self, resolution: str) -> int:
        """Map resolution labels to pixel counts."""
        return {"Low": 256, "Medium": 512, "High": 1024}.get(resolution, 512)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name}>"
