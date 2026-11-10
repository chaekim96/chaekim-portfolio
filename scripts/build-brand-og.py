#!/usr/bin/env python3
"""Renders the /brand link-preview card (1200x630) to assets/img/brand/cards/brand-og.png.
Same look as the build cards from build-brand-cards.py: paper, Poppins, the seal-red endorsement and a color bar.
Needs Google Chrome (headless) and network access for the Poppins web font.  Usage:  python3 scripts/build-brand-og.py
"""
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mark_art import BRAND, all_marks  # noqa: E402
from stamp_shared import SITE_URL  # noqa: E402

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT = os.path.join(os.path.dirname(HERE), "assets", "img", "brand", "cards", "brand-og.png")

PAGE = """<!DOCTYPE html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&family=JetBrains+Mono:wght@500&display=block">
<style>
  html, body { margin: 0; width: 1200px; height: 630px; overflow: hidden; }
  body { background: #f9f9f7; font-family: Poppins, system-ui, sans-serif; color: #111110; -webkit-font-smoothing: antialiased; position: relative; }
  .label { position: absolute; left: 80px; top: 66px; font-size: 20px; font-weight: 600; letter-spacing: .16em; text-transform: uppercase; color: #6b6b66; }
  h1 { position: absolute; left: 80px; top: 98px; margin: 0; font-size: 88px; line-height: 1.1; white-space: nowrap; font-weight: 600; letter-spacing: -.04em; }
  .desc { position: absolute; left: 80px; top: 226px; width: 1060px; font-size: 32px; line-height: 1.3; color: #3a3a38; }
  .grid { position: absolute; left: 80px; top: 330px; display: grid; grid-template-columns: repeat(10, 80px); gap: 24px 20px; }
  .grid svg { width: 80px; height: 80px; display: block; }
  .foot { position: absolute; left: 80px; right: 80px; bottom: 44px; display: flex; justify-content: space-between; align-items: center; }
  .by { font-size: 20px; font-weight: 500; letter-spacing: .14em; text-transform: uppercase; color: #6b6b66; display: flex; align-items: center; gap: 14px; }
  .by i { width: 14px; height: 14px; background: #c63d2f; display: block; }
  .url { font: 500 20px "JetBrains Mono", ui-monospace, monospace; color: #6b6b66; }
</style></head><body>
<div class="label">Brand</div><h1>Marks for every build</h1>
<div class="desc">One tile, one color recipe, three type tiers and one endorsement line.</div>
<div class="grid">@@marks@@</div>
<div class="foot"><span class="by"><i></i>A Chae Kim build</span><span class="url">@@url@@</span></div>
</body></html>"""


def main():
    import re
    marks = "".join(re.sub(r"^<\?xml[^>]*\?>\s*", "", m.src) for m in all_marks())
    page = PAGE.replace("@@marks@@", marks).replace("@@url@@", SITE_URL.split("://", 1)[1] + "/brand")
    with tempfile.TemporaryDirectory() as tmp:
        src = os.path.join(tmp, "card.html")
        with open(src, "w", encoding="utf-8") as f:
            f.write(page)
        subprocess.check_call([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                               "--window-size=1200,630", "--virtual-time-budget=8000", "--screenshot=" + OUT, "file://" + src],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
