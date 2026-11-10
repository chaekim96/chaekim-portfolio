"""Shared mark art: reads the shipped color-seal marks in assets/img/brand/ and derives the other forms from them.

The shipped SVGs are the source of truth. Everything here (dark tiles, animated variants, the 16px favicons,
the sticker sheet, the color check) is computed from them, so a recolored mark flows through on the next build.

Recipe for a lit tile (64 units, rx 14): the top stop is the base mixed 38% with white, the middle is the base,
the bottom is the base mixed 10% with black. Glyph ink is #111110; the white detail is #ffffff.
Dark tile: base 12% deeper, top 20% white, bottom 6% black, ink becomes paper (#f8f8f6), plus a 1px white 16% edge.
"""
import os
import re

INK = "#111110"
PAPER = "#f8f8f6"
WHITE = "#ffffff"

LIT_TOP, LIT_BOTTOM = 0.38, 0.10
DARK_DEEPEN, DARK_TOP, DARK_BOTTOM = 0.12, 0.20, 0.06
MIN_WHITE, MIN_INK = 1.8, 3.0

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRAND = os.path.join(ROOT, "assets", "img", "brand")

TILE_RE = re.compile(r'<rect width="64" height="64" rx="14" fill="url\(#([^)]+)\)"/>')
STOP_RE = re.compile(r'stop-color="(#[0-9a-fA-F]{6})"')
EDGE = '<rect x=".5" y=".5" width="63" height="63" rx="13.5" fill="none" stroke="#ffffff" stroke-opacity=".16"/>'


# --- color math -------------------------------------------------------------
def h2r(h):
    h = h.lstrip("#")
    return [int(h[i:i + 2], 16) for i in (0, 2, 4)]


def r2h(rgb):
    return "#" + "".join("%02x" % max(0, min(255, int(round(v)))) for v in rgb)


def mix(a, b, p):
    """a mixed p of the way toward b."""
    x, y = h2r(a), h2r(b)
    return r2h([x[i] * (1 - p) + y[i] * p for i in range(3)])


def stops(base, top, bottom):
    return [mix(base, WHITE, top), base, mix(base, "#000000", bottom)]


def luminance(h):
    def lin(v):
        v /= 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = [lin(v) for v in h2r(h)]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a, b):
    x, y = luminance(a), luminance(b)
    return (max(x, y) + 0.05) / (min(x, y) + 0.05)


# --- reading the shipped marks ---------------------------------------------
def base_slug(name):
    """File stem without a version suffix: 'custom-llm-2' -> 'custom-llm'."""
    return re.sub(r"-\d+$", "", name)


def shipped_names():
    """Stems of the live mark files: one per build, the newest version where a '-2' file replaces the original."""
    stems = sorted(f[:-4] for f in os.listdir(BRAND) if f.endswith(".svg") and not f.startswith("work-"))
    newest = {}
    for s in stems:
        b = base_slug(s)
        if b not in newest or s > newest[b]:
            newest[b] = s
    return [newest[b] for b in sorted(newest)]


class Mark(object):
    def __init__(self, name):
        self.name = name
        self.slug = base_slug(name)
        with open(os.path.join(BRAND, name + ".svg"), encoding="utf-8") as f:
            self.src = f.read()
        m = TILE_RE.search(self.src)
        self.grad_id = m.group(1)
        self.stops = STOP_RE.findall(self.src)
        self.base = self.stops[1]
        self.body = self.src[m.end():self.src.rindex("</svg>")]  # everything drawn on top of the tile
        # Tiles that already carry the 1px white edge are the dark tiles: multicolor glyphs, no lit/dark pair.
        self.is_dark_tile = EDGE in self.body
        self.glyph = self.body.replace(EDGE, "")

    @property
    def paper_body(self):
        """True when the glyph is built on a paper-colored shape (ink then sits on top of it)."""
        return PAPER in self.glyph


def all_marks():
    return [Mark(n) for n in shipped_names()]


# --- dark tile --------------------------------------------------------------
def dark_base(mark, extra=0.0):
    """The deepened base, optionally pushed further toward black to pass the contrast checks."""
    return mix(mark.base, "#000000", DARK_DEEPEN + extra)


def dark_extra(mark):
    """Smallest extra darkening (in 1% steps) that keeps white >= 1.8 and the paper glyph >= 3 against the base."""
    extra = 0.0
    while extra < 0.6:
        b = dark_base(mark, extra)
        if (WHITE not in mark.glyph or ratio(WHITE, b) >= MIN_WHITE) and ratio(PAPER, b) >= MIN_INK:
            return round(extra, 2)
        extra += 0.01
    raise ValueError("no deepened base passes for " + mark.name)


def dark_glyph(mark, base, glyph=None):
    g = mark.glyph if glyph is None else glyph
    if mark.paper_body:
        # The paper shape is the glyph and its ink details stay ink. Details drawn in the old base color follow the new base.
        return g.replace(mark.base, base)
    return g.replace(INK, PAPER)


def tile_svg(grad_id, s, glyph, edge=False, style=""):
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><defs>'
            '<linearGradient id="%s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="%s"/>'
            '<stop offset=".5" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>%s</defs>'
            '<rect width="64" height="64" rx="14" fill="url(#%s)"/>%s%s</svg>\n'
            % (grad_id, s[0], s[1], s[2], style, grad_id, EDGE if edge else "", glyph))


def dark_svg(mark, glyph=None, style=""):
    """(svg text, extra) for a mark's dark tile. extra is the darkening applied beyond the standard 12%."""
    extra = dark_extra(mark)
    base = dark_base(mark, extra)
    s = stops(base, DARK_TOP, DARK_BOTTOM)
    return tile_svg(mark.grad_id + "-dark", s, dark_glyph(mark, base, glyph), edge=True, style=style), extra
