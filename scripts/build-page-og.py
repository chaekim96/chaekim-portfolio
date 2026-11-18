#!/usr/bin/env python3
"""Renders a link-preview card (1200x630) for every page that isn't a build, so shared links
stop all showing the same paper card. Builds get theirs from build-brand-cards.py.

Output: assets/img/og/<name>.png. Text comes from the built page (title, eyebrow, description),
so run the build first, then this, then the build again so pages point at their card:
  python3 scripts/build.py && python3 scripts/build-page-og.py && python3 scripts/build.py
Needs Google Chrome (headless) and network access for the web fonts. Pass names to render only those.
"""
import html
import importlib.util
import os
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from stamp_shared import SITE_URL, OG_DIR, WORK_GLYPH  # noqa: E402

_spec = importlib.util.spec_from_file_location("cards", os.path.join(HERE, "build-brand-cards.py"))
cards = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cards)

SITE = SITE_URL.split("://", 1)[1]
SKIP = {"index", "404", "mirrorme-tech-pack"}  # home keeps the site card; the others aren't meant to be shared
PAPER = "/assets/img/og-sky.png"
# A work page's eyebrow says where it sits on the home page; on a card it just reads as work.
LABEL = {"featured": "work", "more work": "work", "in progress": "work", "reading": "writing & reading"}

# The build card, minus the color bar, with an ink work tile (or no tile) and a plain byline.
CARD = cards.CARD.replace('<div class="bar">@@bar@@</div>\n', "").replace("A Chae Kim build", "Chae Kim")
NO_MARK = "<style>.mark{display:none}.head{left:80px;width:1040px}</style>"


def meta(page, attr, key):
    m = re.search(r'<meta %s="%s" content="([^"]*)"' % (attr, re.escape(key)), page)
    return html.unescape(m.group(1)) if m else ""


def pages():
    for path in [*sorted(f for f in os.listdir(ROOT) if f.endswith(".html")),
                 *sorted("projects/" + f for f in os.listdir(os.path.join(ROOT, "projects")) if f.endswith(".html"))]:
        name = os.path.basename(path)[:-5]
        page = open(os.path.join(ROOT, path), encoding="utf-8").read()
        image = meta(page, "property", "og:image")
        if name in SKIP or 'name="robots" content="noindex' in page:
            continue
        if not (image.endswith(PAPER) or image.endswith(f"/{OG_DIR}/{name}.png")):
            continue  # has a card of its own already
        eyebrow = re.search(r'class="eyebrow[^"]*">([^<]*)<', page)
        yield dict(name=name,
                   title=re.sub(r"\s*·\s*Chae Kim.*$", "", meta(page, "property", "og:title")),
                   label=LABEL.get(*[html.unescape(eyebrow.group(1)).split(" · ")[0] if eyebrow else ""] * 2),
                   desc=meta(page, "name", "description"),
                   url=SITE + (f"/projects/{name}" if path.startswith("projects/") else f"/{name}"))


def main(argv):
    only = set(argv)
    out_dir = os.path.join(ROOT, OG_DIR)
    os.makedirs(out_dir, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        for p in pages():
            if only and p["name"] not in only:
                continue
            glyph = WORK_GLYPH.get(p["name"])
            svg = open(os.path.join(ROOT, "assets/img/brand", f"work-{glyph}.svg"), encoding="utf-8").read() if glyph else ""
            page = cards.fill(CARD, dict(svg=cards.strip_xml(svg), label=html.escape(p["label"]),
                                         title=html.escape(p["title"]), desc=html.escape(p["desc"]),
                                         url=html.escape(p["url"])))
            if not glyph:
                page = page.replace("</head>", NO_MARK + "</head>", 1).replace("scrollWidth > 850", "scrollWidth > 1040")
            out = os.path.join(out_dir, f"{p['name']}.png")
            cards.shoot(page, 1200, 630, out, tmp)
            print("wrote", os.path.relpath(out, ROOT))


if __name__ == "__main__":
    main(sys.argv[1:])
