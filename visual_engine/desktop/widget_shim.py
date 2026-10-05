"""A minimal stand-in for ipywidgets, used by the desktop app.

Patterns describe their controls with ipywidgets (IntSlider, FloatSlider,
Dropdown, Checkbox, Text). The desktop app only reads those descriptions, so
it substitutes these plain classes instead of importing ipywidgets, which
would drag IPython, jedi and zmq (~35 MB) into the packaged app.
Defaults and value clamping follow ipywidgets.
"""


class _Widget:
    def __init__(self, value=None, description="", **kwargs):
        self.description = description
        self.value = value
        for key, val in kwargs.items():
            setattr(self, key, val)

    def __repr__(self):
        return f"{type(self).__name__}(description={self.description!r}, value={self.value!r})"


class _Slider(_Widget):
    _defaults = {}

    def __init__(self, value=None, min=None, max=None, step=None, description="", **kwargs):
        d = self._defaults
        self.min = self._cast(d["min"] if min is None else min)
        self.max = self._cast(d["max"] if max is None else max)
        self.step = self._cast(d["step"] if step is None else step)
        value = self.min if value is None else value
        super().__init__(value=self._cast(sorted((self.min, value, self.max))[1]),
                         description=description, **kwargs)

    @staticmethod
    def _cast(v):
        return v


class IntSlider(_Slider):
    _defaults = {"min": 0, "max": 100, "step": 1}
    _cast = staticmethod(int)


class FloatSlider(_Slider):
    _defaults = {"min": 0.0, "max": 10.0, "step": 0.1}
    _cast = staticmethod(float)


class Dropdown(_Widget):
    def __init__(self, options=(), value=None, description="", **kwargs):
        self.options = tuple(options)
        values = [o[1] if isinstance(o, tuple) else o for o in self.options]
        if value is None and values:
            value = values[0]
        super().__init__(value=value, description=description, **kwargs)


class Checkbox(_Widget):
    def __init__(self, value=False, description="", **kwargs):
        super().__init__(value=bool(value), description=description, **kwargs)


class Text(_Widget):
    def __init__(self, value="", description="", **kwargs):
        super().__init__(value=str(value), description=description, **kwargs)


def install():
    """Make `import ipywidgets` resolve to this module (desktop app only)."""
    import sys
    sys.modules["ipywidgets"] = sys.modules[__name__]
