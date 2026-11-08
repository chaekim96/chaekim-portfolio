#!/usr/bin/env python3
"""Writes the hand-hinted 16px favicons: assets/img/brand/fav16/<slug>.png (16x16, no smoothing) and <slug>.svg (crispEdges).

The art is the grids in fav16_data.py; the colors come from each shipped mark, so a recolored mark recolors its favicon.
Usage:  python3 scripts/build-fav16.py           (write)
        python3 scripts/build-fav16.py --check   (write nothing; fail if a file is out of date)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fav16_render import pixels, png_bytes, svg_text  # noqa: E402
from mark_art import BRAND, all_marks  # noqa: E402


def build():
    out = {}
    for m in all_marks():
        px = pixels(m.slug, m.stops)
        out["fav16/%s.png" % m.slug] = png_bytes(px)
        out["fav16/%s.svg" % m.slug] = svg_text(px).encode("utf-8")
    return out


def main():
    check = "--check" in sys.argv[1:]
    stale = []
    for rel, data in sorted(build().items()):
        path = os.path.join(BRAND, rel)
        old = open(path, "rb").read() if os.path.exists(path) else None
        # PNG bytes depend on the zlib build, so only the SVGs are compared in --check
        if old != data and not (check and rel.endswith(".png") and old is not None):
            stale.append(rel)
            if not check:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "wb") as f:
                    f.write(data)
    if check:
        if stale:
            sys.exit("out of date: " + ", ".join(stale) + "\nRun python3 scripts/build-fav16.py")
        print("ok: 16px favicons up to date")
    else:
        print("wrote favicons (%d changed)" % len(stale))


if __name__ == "__main__":
    main()
