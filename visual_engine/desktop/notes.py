"""'How This Works' concept notes, read from the notebook and turned into HTML.

The notebook stays the single source of truth. Math ($...$ and $$...$$) is
lifted out before Markdown conversion (Markdown would mangle the _ and *
inside formulas) and put back as elements that KaTeX renders in the UI.
"""
import html
import json
import re
import unicodedata
from functools import lru_cache

import markdown

from .paths import notebook_path

_HEADING = re.compile(r"^###\s+How This Works\s+—\s+(.+?)\s*$", re.M)
_DISPLAY_MATH = re.compile(r"\$\$(.+?)\$\$", re.S)
_INLINE_MATH = re.compile(r"(?<![\\$])\$(?!\$)(.+?)(?<![\\$])\$", re.S)


def normalise(name: str) -> str:
    """Accent-, case- and punctuation-insensitive key ('Möbius' == 'Mobius')."""
    plain = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", plain.lower()).strip()


def _split_notes(cells):
    """Yield (pattern title, markdown body) for every note; a cell may hold several."""
    for cell in cells:
        if cell.get("cell_type") != "markdown":
            continue
        text = "".join(cell["source"])
        heads = list(_HEADING.finditer(text))
        for k, m in enumerate(heads):
            end = heads[k + 1].start() if k + 1 < len(heads) else len(text)
            body = re.sub(r"\n\s*---\s*$", "", text[m.end():end].strip())
            yield m.group(1), body.strip()


def to_html(md_text: str) -> str:
    """Markdown with LaTeX -> HTML; math becomes <span|div class="math">."""
    maths = []

    def stash(kind):
        def repl(m):
            maths.append((kind, m.group(1).strip()))
            return f"PYXELMATH{len(maths) - 1}X"
        return repl

    text = _DISPLAY_MATH.sub(stash("display"), md_text)
    text = _INLINE_MATH.sub(stash("inline"), text)
    out = markdown.markdown(_structure(text), extensions=["tables", "sane_lists"])

    def restore(m):
        kind, tex = maths[int(m.group(1))]
        tag = "div" if kind == "display" else "span"
        return f'<{tag} class="math math-{kind}">{html.escape(tex)}</{tag}>'

    out = re.sub(r"<p>PYXELMATH(\d+)X</p>", restore, out)   # display math alone in a paragraph
    out = re.sub(r"PYXELMATH(\d+)X", restore, out)
    # "**Core Idea**" opening a paragraph is a section label: make it a heading
    out = re.sub(r"<p><strong>([^<]{1,60})</strong>\s*(?:<br\s*/?>)?\s*", r"<h4>\1</h4>\n<p>", out)
    return out.replace("<p></p>", "")


_LABEL = re.compile(r"^\*\*([^*]{1,60})\*\*\s*$")
_LIST_ITEM = re.compile(r"^\s*(?:\d+\.|[-*+])\s")


def _structure(text: str) -> str:
    """The notes put a bold label line ("**Core Idea**") directly above its
    paragraph or list. Turn labels into headings, and give lists the blank
    line Markdown requires, or "1. ... 2. ..." collapses into one paragraph."""
    lines, prev = [], ""
    for line in text.splitlines():
        label = _LABEL.match(line)
        if label:
            lines += ["", f"#### {label.group(1)}", ""]
            prev = ""
            continue
        if _LIST_ITEM.match(line) and prev.strip() and not _LIST_ITEM.match(prev):
            lines.append("")
        lines.append(line)
        prev = line
    return "\n".join(lines)


@lru_cache(maxsize=1)
def load_notes() -> dict:
    """{normalised pattern name: (title, html)} for every note in the notebook."""
    with open(notebook_path(), encoding="utf-8") as f:
        cells = json.load(f)["cells"]
    return {normalise(title): (title, to_html(body)) for title, body in _split_notes(cells)}


def note_for(pattern_name: str):
    """HTML of the pattern's note, or None if the notebook has none."""
    entry = load_notes().get(normalise(pattern_name))
    return entry[1] if entry else None
