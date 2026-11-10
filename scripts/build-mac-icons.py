#!/usr/bin/env python3
"""Builds a Mac app icon (.icns) from a shipped mark, with the depth treatment: a top highlight, a lower shade,
a light-to-dark edge stroke and a soft drop shadow. The glyph stays flat; all depth belongs to the tile.

Layout is the macOS app-icon grid: an 824px tile centered on a 1024px canvas. Sizes 16 to 1024 (with @2x) are written
to an .iconset and packed with iconutil. The 16px and 32px images use the hand-hinted favicon art (fav16_data.py)
instead of a downscale; larger sizes are the 1024px render scaled down.

Needs macOS (iconutil), Google Chrome and Pillow.
Usage:  python3 scripts/build-mac-icons.py <mark file name> <output .icns>
   e.g. python3 scripts/build-mac-icons.py token-fuel ~/token-fuel/brand/AppIcon.icns
"""
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fav16_render import pixels  # noqa: E402
from mark_art import Mark, h2r  # noqa: E402

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
DEPTH_DEFS = ('<linearGradient id="hi" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".34"/>'
              '<stop offset=".45" stop-color="#fff" stop-opacity="0"/></linearGradient>'
              '<linearGradient id="lo" x1="0" y1="0" x2="0" y2="1"><stop offset=".55" stop-color="#000" stop-opacity="0"/>'
              '<stop offset="1" stop-color="#000" stop-opacity=".22"/></linearGradient>'
              '<linearGradient id="ed" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".65"/>'
              '<stop offset=".4" stop-color="#fff" stop-opacity=".05"/><stop offset=".7" stop-color="#000" stop-opacity=".05"/>'
              '<stop offset="1" stop-color="#000" stop-opacity=".32"/></linearGradient>')
DEPTH_LAYERS = ('<rect width="64" height="64" rx="14" fill="url(#hi)"/><rect width="64" height="64" rx="14" fill="url(#lo)"/>'
                '<rect x=".75" y=".75" width="62.5" height="62.5" rx="13.25" fill="none" stroke="url(#ed)" stroke-width="1.5"/>')
SIZES = [(16, 1), (16, 2), (32, 1), (32, 2), (128, 1), (128, 2), (256, 1), (256, 2), (512, 1), (512, 2)]


def master_html(mark):
    inner = mark.src[mark.src.index("<defs>"):mark.src.index("</svg>")]
    inner = inner.replace("</defs>", DEPTH_DEFS + "</defs>", 1)
    tile_end = inner.index('rx="14" fill="url(#%s)"/>' % mark.grad_id) + len('rx="14" fill="url(#%s)"/>' % mark.grad_id)
    inner = inner[:tile_end] + DEPTH_LAYERS + inner[tile_end:]  # depth sits under the glyph
    return ('<!doctype html><html><head><style>html,body{margin:0;width:1024px;height:1024px;background:transparent;overflow:hidden}'
            '.t{position:absolute;left:100px;top:100px;width:824px;height:824px;'
            'filter:drop-shadow(0 14px 18px rgba(0,0,0,.28)) drop-shadow(0 2px 3px rgba(0,0,0,.25))}.t svg{display:block}</style></head>'
            '<body><div class="t"><svg width="824" height="824" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">%s</svg></div></body></html>' % inner)


def hinted(slug, stops, scale):
    from PIL import Image
    px = pixels(slug, stops)
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(px):
        for x, c in enumerate(row):
            if c:
                img.putpixel((x, y), tuple(h2r(c)) + (255,))
    return img.resize((16 * scale, 16 * scale), Image.NEAREST)  # exact pixel doubling, no smoothing


def main():
    from PIL import Image
    name, out = sys.argv[1], os.path.expanduser(sys.argv[2])
    mark = Mark(name)
    with tempfile.TemporaryDirectory() as tmp:
        page = os.path.join(tmp, "master.html")
        with open(page, "w", encoding="utf-8") as fh:
            fh.write(master_html(mark))
        shot = os.path.join(tmp, "master.png")
        subprocess.check_call([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                               "--default-background-color=00000000", "--window-size=1024,1024", "--screenshot=" + shot, "file://" + page],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        master = Image.open(shot).convert("RGBA")
        assert master.size == (1024, 1024), master.size
        iconset = os.path.join(tmp, "AppIcon.iconset")
        os.makedirs(iconset)
        for base, scale in SIZES:
            px = base * scale
            if px == 16:
                img = hinted(mark.slug, mark.stops, 1)
            elif px == 32:
                img = hinted(mark.slug, mark.stops, 2)
            else:
                img = master if px == 1024 else master.resize((px, px), Image.LANCZOS)
            img.save(os.path.join(iconset, "icon_%dx%d%s.png" % (base, base, "@2x" if scale == 2 else "")))
        os.makedirs(os.path.dirname(out), exist_ok=True)
        subprocess.check_call(["iconutil", "-c", "icns", iconset, "-o", out])
    print("wrote", out)


if __name__ == "__main__":
    main()
