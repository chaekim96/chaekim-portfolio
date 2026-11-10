"""Data for the command palette (assets/js/palette.js), written to assets/data/palette.json.

Built from the same lists the pages are built from, so a new build, case, essay or page appears
without touching the palette: case studies come from scripts/projects/, essays from
writing_data.py, and any other page in projects/ is found by its <title>. Nothing here is typed twice.
"""
import html
import json
import re
from pathlib import Path

from stamp_shared import mark_file, work_mark, WORK_GLYPH

ROOT = Path(__file__).resolve().parent.parent
TITLE_TAIL = " · Chae Kim - Portfolio"

# The home tabs and a few key pages that are not case studies. (title, url, group, hint, keywords)
TABS = [
    ("Builds", "/#builds", "Tabs", "Home", "projects products tools mods coursework"),
    ("Work", "/#work", "Tabs", "Home", "experience lucent ey tritooling mirrorme"),
    ("Writing", "/#writing", "Tabs", "Home", "essays reading list articles"),
    ("About", "/#about", "Tabs", "Home", "bio experience contact"),
]
KEY_PAGES = [
    ("Home", "/", "Pages", "", "chae kim portfolio"),
    ("How I decide", "/projects/decisions", "Pages", "Decision log", "decisions options choices log"),
    ("Writing and reading list", "/reading", "Pages", "", "essays articles reading"),
    ("Resume (PDF)", "/assets/pdf/chae-kim-resume.pdf", "Pages", "PDF", "resume cv"),
]


def _entry(title, url, group, hint="", keywords="", mark=""):
    e = {"t": title, "u": url, "g": group}
    if hint:
        e["h"] = hint
    if keywords:
        e["k"] = keywords.lower()
    if mark:
        e["m"] = mark
    return e


def page_title(path):
    text = path.read_text(encoding="utf-8")
    if re.search(r'<meta name="robots" content="[^"]*noindex', text):
        return None
    m = re.search(r"<title>(.*?)</title>", text, re.S)
    return html.unescape(m.group(1)).replace(TITLE_TAIL, "").strip() if m else None


def build(cases, build_slugs, essays):
    """cases: the CASES list (dicts with slug, title, kicker); build_slugs: slugs that are builds."""
    out = [_entry(*t) for t in TABS]
    seen = {"/", "/#builds", "/#work", "/#writing", "/#about"}
    kinds = {}
    for c in cases:
        slug, url = c["slug"], f"/projects/{c['slug']}"
        seen.add(url)
        is_build = slug in build_slugs
        mf = mark_file(slug) if is_build else None
        mark = f"/assets/img/brand/{mf}.svg" if mf else (f"/assets/img/brand/work-{WORK_GLYPH[slug]}.svg" if slug in WORK_GLYPH else "")
        hint = c["kicker"].split(" · ")[0] if is_build else "Work"
        out.append(_entry(c["title"], url, "Builds" if is_build else "Work", hint, c["kicker"] + " " + c["title"], mark))
    arcade = mark_file("arcade")
    out.append(_entry("Arcade", "/arcade", "Builds", "side quest", "snake galaga music games", f"/assets/img/brand/{arcade}.svg" if arcade else ""))
    seen.add("/arcade")
    for e in essays:
        seen.add(e["url"])
        out.append(_entry(e["title"], e["url"], "Writing", "Essay", "essay " + e.get("description", "")))
    for t in KEY_PAGES:
        out.append(_entry(*t))
        seen.add(t[1])
    # Any other public page in projects/ (hand-written case studies, the portfolio page, brand notes).
    for p in sorted((ROOT / "projects").glob("*.html")):
        url = f"/projects/{p.stem}"
        if url in seen:
            continue
        title = page_title(p)
        if title:
            out.append(_entry(title, url, "More", "", title))
    return out


def dump(entries):
    return json.dumps(entries, ensure_ascii=False, separators=(",", ":")) + "\n"
