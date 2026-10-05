"""Python side of the desktop app: the API the web UI calls through pywebview.

Every public method is callable from JavaScript as window.pywebview.api.<name>
and returns JSON-serialisable data. pywebview runs each call on its own
thread, and matplotlib is not thread-safe, so rendering is serialised by a lock.
"""
import base64
import io
import os
import threading
import traceback
import warnings
import webbrowser

import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt  # noqa: E402

from . import notes, paths  # noqa: E402

# Patterns call plt.show(); with the Agg backend that only warns, harmlessly
warnings.filterwarnings("ignore", message=".*non-interactive.*")

RESOLUTIONS = ["Low", "Medium", "High"]
GIF_FRAMES = 40


def _result(fn):
    """Return {"ok": True, ...} or {"ok": False, "error": ...} instead of raising
    into the JS bridge, where an exception would only appear as a vague error."""
    def wrapper(*args, **kwargs):
        try:
            out = fn(*args, **kwargs)
            return {"ok": True, **(out or {})}
        except Exception as exc:
            traceback.print_exc()
            return {"ok": False, "error": f"{type(exc).__name__}: {exc}"}
    wrapper.__name__ = fn.__name__
    wrapper.__doc__ = fn.__doc__
    return wrapper


def control_spec(widget, key):
    """JSON description of one ipywidgets control (or None if it is display-only)."""
    kind = type(widget).__name__
    label = widget.description.strip(": ").replace("_", " ")
    if kind in ("IntSlider", "FloatSlider"):
        return {"type": "slider", "key": key, "label": label,
                "integer": kind == "IntSlider", "min": widget.min, "max": widget.max,
                "step": widget.step, "value": widget.value}
    if kind == "Dropdown":
        labels, values = [], []
        for opt in widget.options:
            label_i, value_i = opt if isinstance(opt, tuple) else (str(opt), opt)
            labels.append(str(label_i))
            values.append(value_i)
        return {"type": "dropdown", "key": key, "label": label, "options": labels,
                "value": values.index(widget.value)}
    if kind == "Checkbox":
        return {"type": "checkbox", "key": key, "label": label, "value": bool(widget.value)}
    if hasattr(widget, "value"):
        return {"type": "text", "key": key, "label": label, "value": str(widget.value)}
    return None


class Backend:
    def __init__(self, exports_dir=None):
        from utils import export
        self._export = export
        export.set_exports_dir(exports_dir or paths.exports_dir())
        self._lock = threading.Lock()
        self._controls = {}          # pattern name -> widget list (values decoded against these)
        self._last = None            # (pattern name, figure) of the latest render
        self._window = None          # set by app.py; used by the self-test

    # ── catalogue ────────────────────────────────────────────────

    @_result
    def get_catalog(self):
        from engines.color_utils import PALETTES
        from engines.renderer import BasePattern
        from patterns import CATEGORIES, PATTERNS
        number, categories = 0, []
        for cat, names in CATEGORIES.items():
            items = []
            for name in names:
                number += 1
                cls = PATTERNS[name]
                items.append({"name": name, "number": number,
                              "animatable": cls.animate is not BasePattern.animate})
            categories.append({"name": cat, "patterns": items})
        return {"categories": categories, "palettes": list(PALETTES),
                "resolutions": RESOLUTIONS, "gif_frames": GIF_FRAMES,
                "app": {"name": paths.APP_NAME, "version": paths.APP_VERSION,
                        "source": paths.SOURCE_URL,
                        "exports": str(self._export.get_exports_dir())}}

    def _widgets(self, name):
        if name not in self._controls:
            from patterns import get_pattern
            self._controls[name] = get_pattern(name).get_controls()
        return self._controls[name]

    @_result
    def get_controls(self, name):
        from engines.renderer import BasePattern
        specs = []
        for w in self._widgets(name):
            key = BasePattern.control_key(w) if getattr(w, "description", "") else ""
            spec = control_spec(w, key) if key else None
            if spec:
                specs.append(spec)
        return {"controls": specs}

    @_result
    def get_note(self, name):
        html = notes.note_for(name)
        return {"html": html or "<p><em>No notes are available for this pattern.</em></p>"}

    # ── rendering & export ───────────────────────────────────────

    def _kwargs(self, name, values):
        """Decode UI values against the pattern's own widgets."""
        from engines.renderer import BasePattern
        kwargs = {}
        for w in self._widgets(name):
            if not getattr(w, "description", "").strip(": ") or not hasattr(w, "value"):
                continue
            key = BasePattern.control_key(w)
            if key not in values:
                continue
            v, kind = values[key], type(w).__name__
            if kind == "IntSlider":
                v = int(round(float(v)))
            elif kind == "FloatSlider":
                v = float(v)
            elif kind == "Dropdown":
                opts = [o[1] if isinstance(o, tuple) else o for o in w.options]
                v = opts[int(v)]
            elif kind == "Checkbox":
                v = bool(v)
            else:
                v = str(v)
            kwargs[key] = v
        return kwargs

    @_result
    def render(self, name, palette, resolution, values):
        from patterns import get_pattern
        with self._lock:
            pattern = get_pattern(name)
            pattern._fig = None
            pattern.render(resolution=resolution, palette=palette,
                           **self._kwargs(name, values or {}))
            fig = pattern._fig
            if fig is None:
                raise RuntimeError("the pattern produced no figure")
            buf = io.BytesIO()
            fig.savefig(buf, format="png", dpi=100, bbox_inches="tight",
                        facecolor=fig.get_facecolor(), edgecolor="none")
            plt.close("all")
            self._last = (name, fig)
        return {"image": "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()}

    @_result
    def export_png(self, name):
        with self._lock:
            if not self._last or self._last[0] != name:
                raise RuntimeError("Render this pattern before exporting it.")
            path = self._export.export_png(self._last[1], name)
        return {"path": path}

    @_result
    def export_gif(self, name, palette, resolution, values, fps):
        from patterns import get_pattern
        with self._lock:
            pattern = get_pattern(name)
            if not pattern.is_animatable:
                raise RuntimeError("This pattern does not support GIF export.")
            fps = max(1, min(int(fps), 30))
            frames = pattern.animate(n_frames=GIF_FRAMES, fps=fps, resolution=resolution,
                                     palette=palette, **self._kwargs(name, values or {}))
            plt.close("all")
            if not frames:
                raise RuntimeError("The animation produced no frames.")
            path = self._export.export_gif(frames, name, fps=fps)
        return {"path": path}

    # ── desktop integration ──────────────────────────────────────

    @_result
    def open_exports_folder(self):
        folder = self._export.get_exports_dir()
        folder.mkdir(parents=True, exist_ok=True)
        os.startfile(folder)

    @_result
    def open_source(self):
        webbrowser.open(paths.SOURCE_URL)

    # ── self-test (packaging verification) ───────────────────────

    def selftest_report(self, report):
        """Called by the UI self-test with its results; app.py writes and exits."""
        self._selftest_result = report
        if self._window is not None:
            threading.Timer(0.3, self._window.destroy).start()
        return True
