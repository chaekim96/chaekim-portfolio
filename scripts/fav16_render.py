"""Turns the hand-drawn grids in fav16_data.py into pixels, a 16x16 PNG and a crisp SVG. No dependencies."""
import struct
import zlib

from fav16_data import BOTTOM, EXTRA, GRIDS, TOP
from mark_art import INK, PAPER, WHITE, h2r, mix, r2h

MIX = {"d": 0.45, "e": 0.22, "n": 0.60}


def grid_rows(slug):
    g = GRIDS[slug]
    rows = TOP + [g.get(y, "BBBBBBBBBBBBBBBB") for y in range(2, 14)] + BOTTOM
    assert len(rows) == 16 and all(len(r) == 16 for r in rows), slug
    return rows


def row_color(stops, y):
    t = (y + 0.5) / 16.0
    return mix(stops[0], stops[1], t / 0.5) if t < 0.5 else mix(stops[1], stops[2], (t - 0.5) / 0.5)


def pixels(slug, stops):
    """16x16 list of rows; each pixel is a hex color or None for clear."""
    extra = EXTRA.get(slug, {})
    out = []
    for y, row in enumerate(grid_rows(slug)):
        bg = row_color(stops, y)
        line = []
        for ch in row:
            if ch == ".":
                line.append(None)
            elif ch == "B":
                line.append(bg)
            elif ch == "k":
                line.append(INK)
            elif ch in MIX:
                line.append(mix(bg, INK, MIX[ch]))
            elif ch == "w":
                line.append(WHITE)
            elif ch == "h":
                line.append(mix(bg, WHITE, 0.55))
            elif ch == "p":
                line.append(PAPER)
            else:
                line.append(extra[ch])
        out.append(line)
    return out


def png_bytes(px, scale=1):
    """RGBA PNG of the pixel rows, each pixel drawn as a scale x scale block (no smoothing)."""
    raw = bytearray()
    for line in px:
        r = bytearray([0])
        for c in line:
            r += bytes(h2r(c) + [255]) * scale if c else bytes([0, 0, 0, 0]) * scale
        raw += bytes(r) * scale
    n = len(px) * scale

    def chunk(tag, data):
        body = tag + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xffffffff)

    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", n, n, 8, 6, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9)) + chunk(b"IEND", b""))


def svg_text(px):
    """Same-color horizontal runs become one rect each, drawn with crispEdges."""
    rects = []
    for y, line in enumerate(px):
        x = 0
        while x < 16:
            c = line[x]
            if c is None:
                x += 1
                continue
            x2 = x
            while x2 + 1 < 16 and line[x2 + 1] == c:
                x2 += 1
            rects.append('<rect x="%d" y="%d" width="%d" height="1" fill="%s"/>' % (x, y, x2 - x + 1, c))
            x = x2 + 1
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="16" height="16" '
            'shape-rendering="crispEdges">%s</svg>\n' % "".join(rects))
