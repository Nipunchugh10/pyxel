"""Desktop app backend: notes, control specs, rendering and export."""
import base64
import json
import re

import pytest

from desktop import backend as backend_mod
from desktop.backend import Backend
from desktop.notes import load_notes, normalise, note_for, to_html
from patterns import PATTERNS, get_pattern


@pytest.fixture(scope="module")
def api(tmp_path_factory):
    return Backend(exports_dir=tmp_path_factory.mktemp("exports"))


def _defaults(api, name):
    return {s["key"]: s["value"] for s in api.get_controls(name)["controls"]}


# ── notes ────────────────────────────────────────────────────────────────────

def test_every_pattern_has_exactly_one_note():
    notes = load_notes()
    assert len(notes) == 100
    assert all(note_for(n) for n in PATTERNS)
    assert set(notes) == {normalise(n) for n in PATTERNS}


def test_notes_structure():
    for title, html in load_notes().values():
        assert "<h4>" in html, title                          # section labels became headings
        assert not re.search(r"<p>[^<]*\b1\. [^<]*\b2\. ", html), f"{title}: list collapsed"
        stray = re.sub(r'<(span|div) class="math.*?</\1>', "", html, flags=re.S)
        assert "$" not in stray, f"{title}: unconverted math"


def test_math_is_protected_from_markdown_and_escaped():
    html = to_html("**Core Idea**\nIf $a_1 < b_2$ then\n$$x^*_i = 1$$\n\n1. one\n2. two")
    assert '<span class="math math-inline">a_1 &lt; b_2</span>' in html
    assert '<div class="math math-display">x^*_i = 1</div>' in html
    assert "<h4>Core Idea</h4>" in html and "<ol>" in html


def test_accents_match():
    assert normalise("Möbius Strip") == normalise("Mobius Strip")


# ── catalogue & controls ─────────────────────────────────────────────────────

def test_catalog(api):
    cat = api.get_catalog()
    assert cat["ok"]
    json.dumps(cat)
    names = [p["name"] for c in cat["categories"] for p in c["patterns"]]
    assert sorted(names) == sorted(PATTERNS) and len(set(names)) == 100
    assert [p["number"] for c in cat["categories"] for p in c["patterns"]] == list(range(1, 101))
    assert sum(p["animatable"] for c in cat["categories"] for p in c["patterns"]) == 10


@pytest.mark.parametrize("name", list(PATTERNS))
def test_control_specs_round_trip(api, name):
    """UI defaults decode to exactly what the notebook would pass to render()."""
    res = api.get_controls(name)
    assert res["ok"]
    json.dumps(res)
    pattern = get_pattern(name)
    expected = pattern.control_kwargs(pattern.get_controls())
    assert api._kwargs(name, _defaults(api, name)) == expected


def test_dropdown_values_decode_by_index(api):
    vals = _defaults(api, "Breakout Brick Map")
    vals["style"] = 2                                         # third option: "Radial" -> 2
    assert api._kwargs("Breakout Brick Map", vals)["style"] == 2
    vals = _defaults(api, "Atom Orbital Simulator")
    vals["view_plane"] = 1                                    # ["xz","xy","yz"] -> "xy"
    assert api._kwargs("Atom Orbital Simulator", vals)["view_plane"] == "xy"


# ── rendering & export ───────────────────────────────────────────────────────

@pytest.mark.parametrize("name", ["Koch Snowflake", "Fire Particle System", "Mosaic Tile Art",
                                  "Retro Starfield", "Torus Knot", "Quantum Wave Packet"])
def test_render_returns_png(api, name):
    res = api.render(name, "Forest", "Low", _defaults(api, name))
    assert res["ok"], res.get("error")
    png = base64.b64decode(res["image"].split(",", 1)[1])
    assert png[:8] == b"\x89PNG\r\n\x1a\n" and len(png) > 5000


def test_export_png_and_gif(api):
    from utils.export import get_exports_dir
    name = "Conway's Game of Life"
    assert api.render(name, "Inferno", "Low", _defaults(api, name))["ok"]
    png = api.export_png(name)
    gif = api.export_gif(name, "Inferno", "Low", _defaults(api, name), 10)
    assert png["ok"] and gif["ok"]
    for res in (png, gif):
        path = res["path"]
        assert path.startswith(str(get_exports_dir()))
        assert "'" not in path.rsplit("\\", 1)[-1]            # filesystem-safe name


def test_misuse_is_reported_not_raised(api):
    assert not api.export_png("Penrose Tiling")["ok"]       # nothing rendered yet
    assert not api.export_gif("Penrose Tiling", "Inferno", "Low", {}, 12)["ok"]
    bad = api.render("No Such Pattern", "Inferno", "Low", {})
    assert not bad["ok"] and "No Such Pattern" in bad["error"]


def test_export_names_never_collide(tmp_path):
    from utils import export
    old = export.get_exports_dir()
    try:
        export.set_exports_dir(tmp_path)
        a = export._timestamped_name("Maze Generator & Solver", "png")
        a.write_bytes(b"x")
        b = export._timestamped_name("Maze Generator & Solver", "png")
        assert a != b and a.name.startswith("maze_generator_solver_")
    finally:
        export.set_exports_dir(old)


def test_backend_never_uses_an_interactive_backend():
    import matplotlib
    assert backend_mod.matplotlib is matplotlib
    assert matplotlib.get_backend().lower() == "agg"


def test_widget_shim_matches_ipywidgets(monkeypatch):
    """The desktop app's ipywidgets stand-in must describe every control exactly
    as the real ipywidgets does (types included), for all 100 patterns."""
    import sys
    from desktop import widget_shim
    from desktop.backend import control_spec
    from engines.renderer import BasePattern

    def describe(cls):
        p = cls()
        ws = p.get_controls()
        return json.dumps([[control_spec(w, BasePattern.control_key(w)) for w in ws],
                           p.control_kwargs(ws), [type(v).__name__ for v in p.control_kwargs(ws).values()]])

    real = {n: describe(c) for n, c in PATTERNS.items()}
    monkeypatch.setitem(sys.modules, "ipywidgets", widget_shim)
    assert {n: describe(c) for n, c in PATTERNS.items()} == real
