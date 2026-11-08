#!/usr/bin/env python3
"""Derives the other forms of each color-seal mark from the shipped SVGs in assets/img/brand/.

Writes (all generated; edit the recipe in mark_art.py or the data in line_icons.py, then rerun):
  assets/img/brand/dark/<slug>.svg         dark-theme tile for every lit mark (the three dark tiles are already dark)
  assets/img/brand/live/<slug>.svg         animated white detail for the marks that move; <slug>-dark.svg for dark theme
  assets/img/brand/line/<slug>.svg         monoline glyph, 24px grid, stroke 2;  <slug>-bold.svg, stroke 3
  assets/img/brand/line/sprite.svg         every line icon as a <symbol> (ids line-<slug> and line-<slug>-bold)

Usage:  python3 scripts/build-mark-variants.py           (write)
        python3 scripts/build-mark-variants.py --check   (write nothing; fail if a file is out of date)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mark_art import BRAND, all_marks, dark_svg, tile_svg  # noqa: E402
from line_icons import DOTS, PATHS  # noqa: E402

# Only the white detail moves; the tile and the ink glyph stay still. Each entry is (edits, css):
# edits tag the detail with class "sp" in the shipped markup, css is embedded in the SVG.
# prefers-reduced-motion turns every animation off, which leaves the same still frame the static mark shows.
REDUCE = "@media (prefers-reduced-motion: reduce){.sp,.halo{animation:none}}"
ANIMATED = {
    # the slash draws itself across the bars
    "tally": ([('<path d="M13 43 51 21" stroke="#ffffff"', '<path class="sp" pathLength="1" d="M13 43 51 21" stroke="#ffffff"')],
              ".sp{stroke-dasharray:1 1;animation:mk-draw 2.8s ease-in-out infinite}"
              "@keyframes mk-draw{0%{stroke-dashoffset:1;opacity:0}10%{opacity:1}55%,85%{stroke-dashoffset:0;opacity:1}100%{stroke-dashoffset:0;opacity:0}}"),
    # the caret blinks like a cursor
    "typerace": ([('<rect x="41" y="19" width="6" height="26" rx="1.5" fill="#ffffff"/>', '<rect class="sp" x="41" y="19" width="6" height="26" rx="1.5" fill="#ffffff"/>')],
                 ".sp{animation:mk-blink 1.1s step-end infinite}@keyframes mk-blink{0%{opacity:1}50%{opacity:0}}"),
    # the gauge arc fills and drains
    "token-fuel": ([('<path d="M14 42a18 18 0 0 1 27.2-15.5" fill="none" stroke="#ffffff"', '<path class="sp" pathLength="1" d="M14 42a18 18 0 0 1 27.2-15.5" fill="none" stroke="#ffffff"')],
                   ".sp{stroke-dasharray:1 1;animation:mk-fill 3s ease-in-out infinite}"
                   "@keyframes mk-fill{0%,10%{stroke-dashoffset:.7}55%,70%{stroke-dashoffset:0}100%{stroke-dashoffset:.7}}"),
    # the center node pulses and sends out a ring
    "personal-wiki": ([('<circle cx="32" cy="32" r="6" fill="#ffffff"/>',
                        '<circle class="halo" cx="32" cy="32" r="6" fill="none" stroke="#ffffff" stroke-width="2" opacity="0"/>'
                        '<circle class="sp" cx="32" cy="32" r="6" fill="#ffffff"/>')],
                      ".sp,.halo{transform-box:fill-box;transform-origin:center}"
                      ".sp{animation:mk-node 2.4s ease-in-out infinite}.halo{animation:mk-halo 2.4s ease-out infinite}"
                      "@keyframes mk-node{0%,100%{transform:scale(1)}50%{transform:scale(1.3)}}"
                      "@keyframes mk-halo{0%{opacity:.8;transform:scale(1)}100%{opacity:0;transform:scale(2.6)}}"),
}


def animated_glyph(mark):
    edits, css = ANIMATED[mark.slug]
    g = mark.glyph
    for old, new in edits:
        assert g.count(old) == 1, "%s: %r not found once" % (mark.name, old)
        g = g.replace(old, new)
    return g, "<style>%s%s</style>" % (css, REDUCE)


def build():
    """{relative path: text} for every file this script owns."""
    out = {}
    for m in all_marks():
        if not m.is_dark_tile:
            out["dark/%s.svg" % m.slug] = dark_svg(m)[0]
        if m.slug in ANIMATED:
            g, style = animated_glyph(m)
            out["live/%s.svg" % m.slug] = tile_svg(m.grad_id, m.stops, g, style=style)
            out["live/%s-dark.svg" % m.slug] = dark_svg(m, glyph=g, style=style)[0]
    out.update(line_icons())
    return out


def line_icons():
    def body(slug):
        dots = "".join('<circle cx="%s" cy="%s" r="%s" fill="currentColor" stroke="none"/>' % d for d in DOTS.get(slug, []))
        return PATHS[slug] + dots

    def svg(slug, w):
        return ('<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" '
                'fill="none" stroke="currentColor" stroke-width="%d" stroke-linecap="round" stroke-linejoin="round">%s</svg>\n' % (w, body(slug)))

    out, symbols = {}, []
    for slug in sorted(PATHS):
        out["line/%s.svg" % slug] = svg(slug, 2)
        out["line/%s-bold.svg" % slug] = svg(slug, 3)
        for suffix, w in (("", 2), ("-bold", 3)):
            symbols.append('<symbol id="line-%s%s" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="%d" '
                           'stroke-linecap="round" stroke-linejoin="round">%s</g></symbol>' % (slug, suffix, w, body(slug)))
    out["line/sprite.svg"] = ('<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="0" height="0" '
                              'style="position:absolute" aria-hidden="true">\n%s\n</svg>\n' % "\n".join(symbols))
    return out


def main():
    files = build()
    stale = []
    for rel, text in sorted(files.items()):
        path = os.path.join(BRAND, rel)
        old = open(path, encoding="utf-8").read() if os.path.exists(path) else None
        if old != text:
            stale.append(rel)
            if "--check" not in sys.argv[1:]:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(text)
    if "--check" in sys.argv[1:]:
        if stale:
            sys.exit("out of date: " + ", ".join(stale) + "\nRun python3 scripts/build-mark-variants.py")
        print("ok: %d mark variant files up to date" % len(files))
    else:
        print("wrote %d files (%d changed)" % (len(files), len(stale)))


if __name__ == "__main__":
    main()
