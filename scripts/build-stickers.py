#!/usr/bin/env python3
"""Print-ready sticker sheet of every live mark: 1 inch tiles on US Letter, 0.08in white border, 0.125in bleed.

Writes assets/brand-kit/stickers.svg (artwork plus a named DIE-CUT layer), stickers-cut.svg (cut lines only) and
stickers.pdf (artwork only, vector, rendered by headless Chrome). Not linked from any page.
Units are points (72 to the inch), so the SVG opens at true size.

Usage:  python3 scripts/build-stickers.py
"""
import os
import re
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mark_art import ROOT, all_marks  # noqa: E402

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
IN = 72.0
PAGE_W, PAGE_H = 8.5 * IN, 11 * IN
TILE = 1.0 * IN          # the mark
BORDER = 0.08 * IN       # white border around it
BLEED = 0.125 * IN       # artwork runs this far past the cut line
CUT = TILE + 2 * BORDER  # width of the die-cut shape
PITCH = 1.8 * IN
COLS, ROWS = 4, 5
RADIUS = 14 / 64.0 * TILE + BORDER  # the tile's corner radius, grown by the border
OUT = os.path.join(ROOT, "assets", "brand-kit")


def f(v):
    return ("%.3f" % v).rstrip("0").rstrip(".")


def sheet(cut_only=False, with_cut=True):
    marks = all_marks()
    assert len(marks) <= COLS * ROWS
    x0 = (PAGE_W - ((COLS - 1) * PITCH + CUT)) / 2
    y0 = (PAGE_H - ((ROWS - 1) * PITCH + CUT)) / 2
    bleed, art, cut = [], [], []
    for i, m in enumerate(marks):
        x, y = x0 + (i % COLS) * PITCH, y0 + (i // COLS) * PITCH
        inner = m.src[m.src.index("<defs>"):m.src.rindex("</svg>")]
        bleed.append('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="#ffffff"/>'
                     % (f(x - BLEED), f(y - BLEED), f(CUT + 2 * BLEED), f(CUT + 2 * BLEED), f(RADIUS + BLEED)))
        art.append('<g id="sticker-%s"><rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="#ffffff"/>'
                   '<svg x="%s" y="%s" width="%s" height="%s" viewBox="0 0 64 64">%s</svg></g>'
                   % (m.slug, f(x), f(y), f(CUT), f(CUT), f(RADIUS), f(x + BORDER), f(y + BORDER), f(TILE), f(TILE), inner))
        cut.append('<rect x="%s" y="%s" width="%s" height="%s" rx="%s"/>' % (f(x), f(y), f(CUT), f(CUT), f(RADIUS)))
    head = ('<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" '
            'xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" width="8.5in" height="11in" viewBox="0 0 %s %s">\n'
            % (f(PAGE_W), f(PAGE_H)))
    cut_layer = ('<g id="die-cut" inkscape:groupmode="layer" inkscape:label="DIE-CUT (spot color CutContour, do not print)" '
                 'fill="none" stroke="#ff00ff" stroke-width="0.5">\n%s\n</g>\n' % "\n".join(cut))
    if cut_only:
        return head + "<title>Sticker sheet, die-cut lines only</title>\n" + cut_layer + "</svg>\n"
    body = ("<title>Sticker sheet, Letter, 1 inch marks</title>\n"
            '<g id="bleed" inkscape:groupmode="layer" inkscape:label="BLEED (0.125in past the cut)">\n%s\n</g>\n'
            '<g id="artwork" inkscape:groupmode="layer" inkscape:label="ARTWORK (0.08in white border)">\n%s\n</g>\n'
            % ("\n".join(bleed), "\n".join(art)))
    return head + body + (cut_layer if with_cut else "") + "</svg>\n"


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, text in (("stickers.svg", sheet()), ("stickers-cut.svg", sheet(cut_only=True))):
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
            fh.write(text)
    # PDF: the artwork alone, laid out on a Letter page with no margins; cut lines travel in stickers-cut.svg
    art = re.sub(r"^<\?xml[^>]*>\s*", "", sheet(with_cut=False))
    html = ('<!doctype html><meta charset="utf-8"><style>@page{size:8.5in 11in;margin:0}html,body{margin:0;background:#fff}'
            'svg{display:block;width:8.5in;height:11in}</style>' + art)
    with tempfile.TemporaryDirectory() as tmp:
        page = os.path.join(tmp, "sheet.html")
        with open(page, "w", encoding="utf-8") as fh:
            fh.write(html)
        subprocess.check_call([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                               "--print-to-pdf=" + os.path.join(OUT, "stickers.pdf"), "file://" + page],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("wrote stickers.svg, stickers-cut.svg, stickers.pdf in assets/brand-kit/")


if __name__ == "__main__":
    main()
