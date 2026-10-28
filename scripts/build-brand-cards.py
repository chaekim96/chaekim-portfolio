#!/usr/bin/env python3
"""Renders each build's link-preview card (1200x630) and touch icon (180x180).

Output: assets/img/brand/cards/<slug>-og.png and <slug>-touch.png, for every build that has a mark.
Rerun after changing a mark, a build's title or description:  python3 scripts/build-brand-cards.py
Needs Google Chrome (headless) and network access for the Poppins and JetBrains Mono web fonts.
Pass one or more slugs to render only those.
"""
import html
import importlib.util
import os
import re
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from stamp_shared import mark_file, CARD_DIR  # noqa: E402

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
BRAND = os.path.join(ROOT, "assets", "img", "brand")
OUT = os.path.join(ROOT, CARD_DIR)
SITE = "chaekim-portfolio.vercel.app"

# Same text the Arcade page carries (build-home.py); Arcade is not one of the case pages.
ARCADE = dict(slug="arcade", title="Arcade", label="Product",
              desc="Snake and Galaga, rebuilt from memory, plus a generative lo-fi radio.", url=f"{SITE}/arcade")
# Rule along the bottom: the mark's colors. Light tiles use their own color; dark tiles use their accents.
BAR = {
    "arcade": ["#30d158", "#e0bc09"],
    "web-anatomy": ["#7c5cff", "#ff6a00", "#30d158"],
    "palette-generator": ["#0a84ff", "#30d158", "#ffd60a", "#ff6a00", "#ff3b30"],
}
LABELS = {"PRODUCTS": "Product", "MODS": "Claude Code mod", "COURSEWORK": "AI/ML coursework"}


def load_cases():
    spec = importlib.util.spec_from_file_location("build_cases", os.path.join(HERE, "build-cases.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    items = [ARCADE]
    for group, label in LABELS.items():
        for c in getattr(mod, group):
            items.append(dict(slug=c["slug"], title=c["title"], label=label, desc=c["desc"],
                              url=f"{SITE}/projects/{c['slug']}"))
    return items


def svg_of(slug):
    return open(os.path.join(BRAND, mark_file(slug) + ".svg"), encoding="utf-8").read()


def mid_stop(svg):
    return re.findall(r'stop-color="(#[0-9a-f]{6})"', svg)[1]


def strip_xml(svg):
    return re.sub(r"^<\?xml[^>]*\?>\s*", "", svg)


CARD = """<!DOCTYPE html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=block">
<style>
  html, body { margin: 0; width: 1200px; height: 630px; overflow: hidden; }
  body { background: #f9f9f7; font-family: Poppins, system-ui, sans-serif; color: #111110; -webkit-font-smoothing: antialiased; position: relative; }
  .mark { position: absolute; left: 80px; top: 72px; width: 150px; height: 150px; }
  .mark svg { width: 100%; height: 100%; display: block; }
  .head { position: absolute; left: 266px; top: 72px; width: 854px; height: 150px; display: flex; flex-direction: column; justify-content: center; }
  .label { font-size: 20px; font-weight: 600; letter-spacing: .16em; text-transform: uppercase; color: #6b6b66; margin-bottom: 2px; }
  h1 { margin: 0; font-size: 88px; line-height: 1.12; font-weight: 600; letter-spacing: -.035em; white-space: nowrap; align-self: flex-start; }
  .desc { position: absolute; left: 80px; top: 300px; width: 1040px; height: 180px; font-size: 40px; line-height: 1.3; color: #3a3a38; }
  .foot { position: absolute; left: 80px; right: 80px; bottom: 62px; display: flex; justify-content: space-between; align-items: center; }
  .by { font-size: 20px; font-weight: 500; letter-spacing: .14em; text-transform: uppercase; color: #6b6b66; display: flex; align-items: center; gap: 14px; }
  .by i { width: 14px; height: 14px; background: #c63d2f; display: block; }
  .url { font: 500 20px "JetBrains Mono", ui-monospace, monospace; color: #6b6b66; }
  .bar { position: absolute; left: 0; right: 0; bottom: 0; height: 12px; display: flex; }
  .bar i { flex: 1; display: block; }
</style></head><body>
<div class="mark">@@svg@@</div>
<div class="head"><div class="label">@@label@@</div><h1 id="t">@@title@@</h1></div>
<div class="desc" id="d">@@desc@@</div>
<div class="foot"><span class="by"><i></i>A Chae Kim build</span><span class="url">@@url@@</span></div>
<div class="bar">@@bar@@</div>
<script>
  // long names and descriptions shrink to fit instead of wrapping into each other
  function fit() {
    var t = document.getElementById('t'), s = 88;
    while (t.scrollWidth > 850 && s > 40) { s -= 2; t.style.fontSize = s + 'px'; }
    var d = document.getElementById('d'), z = 40;
    while (d.scrollHeight > 180 && z > 26) { z -= 1; d.style.fontSize = z + 'px'; }
  }
  document.fonts.ready.then(fit);
</script></body></html>"""

# Touch icon: the mark full-bleed (iOS rounds the corners itself), so square the tile and drop the edge stroke.
TOUCH = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>
  html, body { margin: 0; width: 180px; height: 180px; overflow: hidden; background: transparent; }
  svg { width: 180px; height: 180px; display: block; }
</style></head><body>@@svg@@</body></html>"""


def fill(template, fields):
    for k, v in fields.items():
        template = template.replace(f"@@{k}@@", v)
    return template


def shoot(page_html, w, h, out, tmp):
    src = os.path.join(tmp, "page.html")
    with open(src, "w", encoding="utf-8") as f:
        f.write(page_html)
    raw = os.path.join(tmp, "raw.png")
    if os.path.exists(raw):
        os.remove(raw)
    # headless Chrome can linger after it has written the file, so wait for the file and then stop it
    proc = subprocess.Popen([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                             f"--window-size={w},{h}", f"--screenshot={raw}", "--virtual-time-budget=8000",
                             f"--user-data-dir={tempfile.mkdtemp(dir=tmp)}", "file://" + src],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(120):
        if os.path.exists(raw) and os.path.getsize(raw) > 0:
            break
        time.sleep(0.5)
    time.sleep(0.5)
    proc.kill()
    if os.path.exists(out):
        os.remove(out)
    assert os.path.exists(raw), "Chrome did not write a screenshot"
    subprocess.run(["sips", "-z", str(h), str(w), "-s", "format", "png", raw, "--out", out], check=True, stdout=subprocess.DEVNULL)


def main(argv):
    only = set(argv)
    os.makedirs(OUT, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        for c in load_cases():
            if only and c["slug"] not in only:
                continue
            if not mark_file(c["slug"]):
                continue
            svg = svg_of(c["slug"])
            bar = BAR.get(c["slug"]) or [mid_stop(svg)]
            fields = dict(svg=strip_xml(svg), label=html.escape(c["label"]), title=html.escape(c["title"]),
                          desc=html.escape(c["desc"]), url=html.escape(c["url"]),
                          bar="".join(f'<i style="background:{x}"></i>' for x in bar))
            shoot(fill(CARD, fields), 1200, 630, os.path.join(OUT, f"{c['slug']}-og.png"), tmp)
            flat = re.sub(r'(<rect width="64" height="64") rx="14"', r'\1 rx="0"', strip_xml(svg))
            flat = re.sub(r'<rect x="\.5" y="\.5"[^>]*stroke-opacity[^>]*/>', "", flat)  # edge stroke, not needed full-bleed
            shoot(fill(TOUCH, dict(svg=flat)), 180, 180, os.path.join(OUT, f"{c['slug']}-touch.png"), tmp)
            print("wrote", c["slug"])


if __name__ == "__main__":
    main(sys.argv[1:])
