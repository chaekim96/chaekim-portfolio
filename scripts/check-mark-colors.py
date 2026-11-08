#!/usr/bin/env python3
"""Checks every shipped mark SVG (lit tiles in assets/img/brand/, dark tiles in dark/, animated files in live/).

For each file:
  gradient  the three stops match the recipe within TOL per channel
            lit: top = base + 38% white, bottom = base + 10% black;  dark: top = base + 20% white, bottom = base + 6% black
  white     a white (#ffffff) detail has contrast >= 1.8 against the base
  ink       lit: the ink (#111110) glyph has contrast >= 3 against the base
            dark: the paper (#f8f8f6) glyph has contrast >= 3 against the base
Prints a table and exits non-zero when any check fails.

Usage:  python3 scripts/check-mark-colors.py
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mark_art import (BRAND, DARK_BOTTOM, DARK_TOP, EDGE, INK, LIT_BOTTOM, LIT_TOP, MIN_INK, MIN_WHITE,  # noqa: E402
                      PAPER, STOP_RE, TILE_RE, WHITE, h2r, luminance, ratio, stops)

TOL = 2  # per-channel rounding slack on the gradient stops

# The dark tiles are multicolor on a near-black base: their glyphs are red, orange, green and so on, with no ink or
# white detail to measure, and the base is already as dark as a tile gets. Exempt from the contrast checks by name.
# Their gradient still has to follow the recipe.
MULTICOLOR_DARK_TILES = {"arcade-2", "palette-generator-2", "web-anatomy-2"}

# Shipped marks whose gradient was drawn by eye before the recipe was fixed. They are reported, not recolored.
# The number is the largest per-channel gap today; a mark that drifts further than this fails.
KNOWN_GRADIENT_GAPS = {"timely": 14, "review-labeler": 8, "product-blueprint": 4}


def gap(a, b):
    return max(abs(x - y) for x, y in zip(h2r(a), h2r(b)))


def check(path, name, dark, exempt_contrast):
    svg = open(path, encoding="utf-8").read()
    tile = TILE_RE.search(svg)
    found = STOP_RE.findall(svg)
    if not tile or len(found) != 3:
        return None, ["no 3-stop tile"]
    base = found[1]
    glyph = svg[tile.end():svg.rindex("</svg>")].replace(EDGE, "")
    want = stops(base, DARK_TOP if dark else LIT_TOP, DARK_BOTTOM if dark else LIT_BOTTOM)
    dev = max(gap(w, f) for w, f in zip(want, found))
    problems, notes = [], []
    if dev > TOL:
        if dev <= KNOWN_GRADIENT_GAPS.get(name, -1):
            notes.append("known: gradient gap %d" % dev)
        else:
            problems.append("gradient off by %d" % dev)
    white = ratio(WHITE, base) if WHITE in glyph else None
    ink = ratio(PAPER if dark else INK, base) if (PAPER if dark else INK) in glyph else None
    if not exempt_contrast:
        if white is not None and white < MIN_WHITE:
            problems.append("white %.2f < %.1f" % (white, MIN_WHITE))
        if ink is not None and ink < MIN_INK:
            problems.append("%s %.2f < %.0f" % ("paper" if dark else "ink", ink, MIN_INK))
    if not dark and PAPER in glyph:
        # paper-built marks (a page, a tag) read as the light detail; the brief sets no number, so only note a thin one
        pr = ratio(PAPER, base)
        if pr < MIN_WHITE:
            notes.append("paper shape %.2f" % pr)
    return dict(base=base, dev=dev, white=white, ink=ink), problems + notes


def collect():
    files = []
    for kind, dark in (("", False), ("dark", True), ("live", None)):
        folder = os.path.join(BRAND, kind) if kind else BRAND
        for f in sorted(os.listdir(folder)):
            if not f.endswith(".svg") or (not kind and f.startswith("work-")):
                continue
            is_dark = dark if dark is not None else f.endswith("-dark.svg")
            files.append((kind or "lit", f[:-4], os.path.join(folder, f), is_dark))
    return files


def main():
    rows, failed = [], 0
    for kind, name, path, dark in collect():
        exempt = kind == "lit" and name in MULTICOLOR_DARK_TILES
        res, msgs = check(path, name, dark, exempt)
        if res is None:
            rows.append((kind, name, "-", "-", "-", "-", "FAIL " + "; ".join(msgs)))
            failed += 1
            continue
        bad = [m for m in msgs if not m.startswith(("known", "paper shape"))]
        notes = [m for m in msgs if m not in bad]
        status = ("FAIL " + "; ".join(bad)) if bad else "ok"
        if exempt and not bad:
            status = "ok (multicolor dark tile, contrast exempt)"
        if notes and not bad:
            status += "; note: " + "; ".join(notes)
        failed += bool(bad)
        fmt = lambda v: "-" if v is None else "%.2f" % v
        rows.append((kind, name, res["base"], "%d" % res["dev"], fmt(res["white"]), fmt(res["ink"]), status))

    head = ("set", "file", "base", "grad gap", "white", "ink/paper", "status")
    widths = [max(len(str(r[i])) for r in rows + [head]) for i in range(7)]
    for r in [head] + rows:
        print("  ".join(str(c).ljust(widths[i]) for i, c in enumerate(r)).rstrip())
    print("\n%d files checked, %d failed" % (len(rows), failed))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
