#!/usr/bin/env python3
"""Builds /brand (brand.html): the public, two-minute version of the brand book.

Everything on it is read from the shipped marks, so a recolored or added mark shows up here on the next build.
Also writes assets/brand-kit/marks.zip, the download of every mark file.

Usage:  python3 scripts/build-brand.py
Share card: python3 scripts/build-brand-og.py (needs Chrome; not part of build.py)
"""
import html
import os
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from mark_art import BRAND, Mark, ratio, stops, WHITE, INK, PAPER, LIT_TOP, LIT_BOTTOM  # noqa: E402
from projects import FOLDERS, PROJECTS  # noqa: E402
from stamp_shared import (SITE_URL, CASE_HEAD_ASSETS, CASE_TOP, CASE_FOOT, CASE_SCRIPTS, SPARK_SCRIPT,  # noqa: E402
                          build_mark, mark_file)

GITHUB = "https://github.com/chaekim96/chaekim-portfolio/blob/main/scripts/check-mark-colors.py"
e = html.escape

# Names as the case pages use them, except where a name carries someone else's brand: say the plain thing.
NAMES = {"spotify-review-triage": "Review Triage", "pacman-dqn": "Maze Agent", "parallel-prospect-brief": "Prospect Brief",
         "task-progress": "Task Progress", "web-anatomy": "Anatomy of a Website"}
TIERS = [("products", "Product"), ("mods", "Tool"), ("ai-ml", "Study")]
DARK_TILES = ["palette-generator", "web-anatomy", "arcade"]


def builds():
    """[(slug, name, tier, href)] for every build with a mark, in the site's order."""
    out = []
    for folder, tier in TIERS:
        for s in FOLDERS[folder]:
            if not mark_file(s):
                continue  # a build without a color-seal mark yet (Relay) stays off the brand page
            out.append((s, NAMES.get(s, PROJECTS[s]["title"]), tier, f"/projects/{s}"))
    out.append(("arcade", "Arcade", "Product", "/arcade"))
    return out


def mark_of(slug):
    return Mark(mark_file(slug))


def tile(slug, size, cls="brand__tile"):
    return build_mark(slug, cls, size, themed=True)


def section_intro():
    return f'''
        <h2 id="layers">Two layers, one bridge.</h2>
        <p>My brand has two layers. <b>Stamp</b> is me. <b>Electric</b> is the things I build.</p>
        <div class="layers">
          <div class="layer">
            <p class="layer__tag">Stamp · Chae</p>
            <p class="brush" lang="ko" aria-label="김채운, my name in Korean">김채운</p>
            <div class="bsw"><span><i style="background:#111110"></i>Ink<em>#111110</em></span><span><i style="background:#fbf8f1"></i>Paper<em>#fbf8f1</em></span><span><i style="background:#C63D2F"></i>Seal red<em>#C63D2F</em></span></div>
            <p class="layer__note">Quiet colors and a brush name. The brush is for my name only. It never goes on a build.</p>
          </div>
          <div class="layer">
            <p class="layer__tag">Electric · the builds</p>
            <div class="row">{"".join(tile(s, 48) for s in ("tally", "token-fuel", "typerace", "personal-wiki", "smartmodel", "voiceprompter"))}</div>
            <p class="layer__note">Loud, lit tiles, one color per build. Each one stands on its own and speaks for what the build does.</p>
          </div>
        </div>
        <p class="endorse"><i aria-hidden="true"></i>A Chae Kim build</p>
        <p>That small line, with a seal-red square, is the bridge. It is the only place Stamp shows up on an Electric build.</p>'''


def section_mark():
    m = mark_of("tally")
    s = m.stops
    w, k = ratio(WHITE, m.base), ratio(INK, m.base)
    return f'''
        <h2 id="mark">The mark: one tile, one recipe.</h2>
        <p>Every mark sits on the same tile. It is 64 units square with a corner radius of 14. One simple drawing goes on top. The drawing is ink (#111110) with one white detail.</p>
        <p>The color comes from a base. The top of the tile is the base mixed 38% with white. The middle is the base. The bottom is the base mixed 10% with black. That is the whole recipe.</p>
        <div class="worked">
          <div class="worked__tile">{build_mark("tally", "brand__tile brand__tile--xl", 168)}</div>
          <div>
            <p class="worked__title">Worked example: Tally</p>
            <div class="stops" role="img" aria-label="Three stops: {s[0]}, {s[1]}, {s[2]}"><i style="background:{s[0]}"></i><i style="background:{s[1]}"></i><i style="background:{s[2]}"></i></div>
            <div class="stopl"><span>top {s[0]}</span><span>base {s[1]}</span><span>bottom {s[2]}</span></div>
            <ul class="tight">
              <li>Base red <code>{s[1]}</code>.</li>
              <li>The white slash holds {w:.2f} to 1 against the base. The bar is 1.8 to 1.</li>
              <li>The ink bars hold {k:.2f} to 1. The bar is 3 to 1.</li>
            </ul>
          </div>
        </div>
        <p>A script checks every mark against these numbers each time the site is built.</p>'''


def section_all():
    cells = "".join(f'<a class="mk" href="{href}">{tile(s, 64)}<b>{e(name)}</b><span>{tier}</span></a>' for s, name, tier, href in builds())
    return f'''
        <h2 id="marks">All the marks.</h2>
        <p>Twenty builds, twenty marks. Each links to its case study. Switch the site to dark mode and the tiles deepen, so they sit calmly on a dark page.</p>
        <div class="mkgrid">{cells}</div>'''


def section_palette():
    rows = ""
    for s, name, tier, href in builds():
        m = mark_of(s)
        if s in DARK_TILES:
            continue
        rows += f'<div class="pal"><i style="background:{m.base}"></i><b>{e(name)}</b><code>{m.base}</code></div>'
    return f'''
        <h2 id="palette">Palette: one color per build.</h2>
        <p>Every build gets one base color, and no two builds share one. These are the bases.</p>
        <div class="palgrid">{rows}</div>
        <div class="callout"><span class="ico">📌</span><div><p><strong>The dark-tile rule:</strong> one color means a lit tile. Many colors means a dark tile. Palette Generator, Anatomy of a Website and Arcade use several colors, so they sit on a near-black tile and keep their own colors.</p></div></div>
        <div class="row row--tiles">{"".join(tile(s, 56) for s in DARK_TILES)}</div>'''


def section_type():
    return '''
        <h2 id="type">Type: three tiers.</h2>
        <p>The name beside a mark is set by what kind of build it is. A glance at the face tells you the tier.</p>
        <div class="tiers">
          <div class="tier"><p class="tier__tag">Products · Poppins 600</p><p class="t-product">Tally</p><p class="t-product">AI Visibility Checker</p></div>
          <div class="tier"><p class="tier__tag">Tools · JetBrains Mono 500</p><p class="t-tool">Token-Fuel</p><p class="t-tool">SmartModel</p></div>
          <div class="tier"><p class="tier__tag">Studies · Fraunces italic</p><p class="t-study">Personal Wiki</p><p class="t-study">Custom LLM</p></div>
        </div>'''


def section_small():
    cells = "".join(f'<figure class="fav"><div class="fav__row"><img class="px" src="/assets/img/brand/fav16/{mark_of(s).slug}.png" width="16" height="16" alt="">'
                    f'<img class="px" src="/assets/img/brand/fav16/{mark_of(s).slug}.png" width="64" height="64" alt="{e(name)} favicon, enlarged"></div><figcaption>{e(name)}</figcaption></figure>'
                    for s, name, tier, href in builds())
    return f'''
        <h2 id="small">Small sizes: drawn by hand at 16 pixels.</h2>
        <p>Most people meet a mark as a browser tab icon, 16 pixels wide. A shrunk copy goes soft there. So each mark is also drawn pixel by pixel. Each pair shows the real size, then the same file enlarged.</p>
        <div class="favgrid">{cells}</div>'''


def section_motion():
    items = [("tally", "Tally", "The slash draws across the bars."), ("typerace", "TypeRace", "The caret blinks."),
             ("token-fuel", "Token-Fuel", "The gauge arc fills and drains."), ("personal-wiki", "Personal Wiki", "The center node pulses.")]
    cells = "".join(f'<a class="mv" href="/projects/{s}">{build_mark(s, "brand__tile brand__spark", 88, themed=True)}<b>{name}</b><span>{what}</span></a>' for s, name, what in items)
    return f'''
        <h2 id="motion">Motion: only the white detail moves.</h2>
        <p>Four marks can move. Only the white detail animates, and only while you hover or focus the mark. They sit still otherwise, and always sit still if your device asks for less motion.</p>
        <div class="mvgrid">{cells}</div>'''


def section_line():
    from line_icons import NAMES
    picks = ["tally", "typerace", "token-fuel", "personal-wiki", "smartmodel", "code-improver", "spotify-review-triage", "voiceprompter", "ai-visibility-checker", "product-blueprint"]
    def strip(suffix):
        return "".join(f'<span title="{e(NAMES[p])}"><svg class="li" viewBox="0 0 24 24" aria-hidden="true"><use href="/assets/img/brand/line/sprite.svg#line-{p}{suffix}"/></svg></span>' for p in picks)
    return f'''
        <h2 id="line">Line icons for small spaces.</h2>
        <p>A full color tile is too loud for a menu or a tab bar. So every glyph also has a line version on a 24 pixel grid, in two weights.</p>
        <div class="linerow"><div><p>Regular, 2 pixel line</p>{strip("")}</div><div><p>Bold, 3 pixel line</p>{strip("-bold")}</div></div>'''


def section_endorse():
    return '''
        <h2 id="endorse">The endorsement.</h2>
        <p>Every build ends with the same line.</p>
        <div class="callout"><span class="ico">💡</span><div><p><strong>The footer rule:</strong> a small seal-red square and the words "A Chae Kim build." It goes at the foot of a build's page and on its share card. The brush name never does.</p></div></div>
        <div class="foot-sample"><span class="endorse"><i aria-hidden="true"></i>A Chae Kim build</span><span class="foot-sample__url">example.com</span></div>'''


def section_downloads():
    return f'''
        <h2 id="downloads">Downloads.</h2>
        <ul class="dl">
          <li><a href="/assets/brand-kit/stickers.pdf">Sticker sheet (PDF)</a><span>Every mark on one US Letter page, one inch each.</span></li>
          <li><a href="/assets/brand-kit/marks.zip">All the marks (ZIP)</a><span>Light and dark tiles, 16 pixel icons and line icons.</span></li>
          <li><a href="{GITHUB}" target="_blank" rel="noopener">The color-check script ↗</a><span>The script that checks every mark on each build.</span></li>
        </ul>
        <p>For the whole story of how these marks were chosen, read the <a href="/projects/build-marks">decision log</a>. For the voice, colors and rules around them, read the <a href="/playbook">playbook</a>.</p>'''


CSS = """
    .brush { font-family: 'Nanum Brush Script', 'Apple SD Gothic Neo', cursive; font-size: clamp(56px, 12vw, 88px); line-height: 1.05; color: var(--ink) !important; margin: 4px 0 8px; }
    .layers { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr)); gap: 14px; margin: 18px 0; }
    .layer { border: 1px solid var(--line); border-radius: 16px; padding: 18px; }
    .layer__tag, .tier__tag { font: 500 12px/1 'JetBrains Mono', ui-monospace, monospace; letter-spacing: .1em; text-transform: uppercase; color: var(--ink-2); margin: 0 0 12px; }
    .layer__note { font-size: 14px; color: var(--ink-2); margin: 12px 0 0; }
    .bsw { display: flex; flex-wrap: wrap; gap: 12px; }
    .bsw span { display: grid; gap: 2px; font-size: 13px; }
    .bsw i, .pal i { display: block; width: 44px; height: 44px; border-radius: 12px; box-shadow: inset 0 0 0 1px var(--line); }
    .bsw em, .pal code { font: 500 12px 'JetBrains Mono', ui-monospace, monospace; font-style: normal; color: var(--ink-2); }
    .row { display: flex; flex-wrap: wrap; gap: 10px; }
    .row--tiles { margin-top: 14px; }
    .brand__tile { display: block; border-radius: 22%; }
    .endorse { display: inline-flex; align-items: center; gap: 12px; font: 500 13px/1 Poppins, sans-serif; letter-spacing: .14em; text-transform: uppercase; color: var(--ink-2); margin: 6px 0; }
    .endorse i { width: 13px; height: 13px; background: #C63D2F; display: block; }
    .worked { display: grid; grid-template-columns: auto 1fr; gap: 24px; align-items: center; margin: 18px 0; }
    .worked__title { font-weight: 500; margin: 0 0 8px; }
    .stops { display: flex; height: 28px; border-radius: 8px; overflow: hidden; box-shadow: inset 0 0 0 1px var(--line); }
    .stops i { flex: 1; display: block; }
    .stopl { display: flex; justify-content: space-between; gap: 8px; flex-wrap: wrap; font: 400 12px 'JetBrains Mono', ui-monospace, monospace; color: var(--ink-2); margin-top: 4px; }
    .tight { margin: 12px 0 0; padding-left: 18px; }
    @media (max-width: 560px) { .worked { grid-template-columns: 1fr; justify-items: start; } }
    .mkgrid { display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 132px), 1fr)); gap: 12px; margin: 16px 0; }
    .mk { display: grid; justify-items: center; gap: 4px; text-align: center; border: 1px solid var(--line); border-radius: 16px; padding: 14px 8px; color: var(--ink); text-decoration: none; }
    .mk:hover, .mk:focus-visible { border-color: var(--accent); }
    .mk b { font-size: 13px; font-weight: 500; margin-top: 6px; overflow-wrap: anywhere; }
    .mk span, .mv span { font: 500 11px/1.3 'JetBrains Mono', ui-monospace, monospace; letter-spacing: .08em; text-transform: uppercase; color: var(--ink-2); }
    .palgrid { display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 200px), 1fr)); gap: 10px 14px; margin: 16px 0; }
    .pal { display: grid; grid-template-columns: 44px 1fr; grid-template-rows: auto auto; column-gap: 12px; align-items: center; }
    .pal i { grid-row: 1 / 3; }
    .pal b { font-size: 14px; font-weight: 500; align-self: end; }
    .pal code { background: none; padding: 0; align-self: start; }
    .tiers { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 190px), 1fr)); gap: 14px; margin: 16px 0; }
    .tier { border: 1px solid var(--line); border-radius: 16px; padding: 18px; }
    .tier p { margin: 0; }
    .t-product { font: 600 26px/1.3 Poppins, sans-serif; letter-spacing: -.02em; }
    .t-tool { font: 500 21px/1.5 'JetBrains Mono', ui-monospace, monospace; }
    .t-study { font: italic 400 28px/1.3 Fraunces, Georgia, serif; }
    .favgrid { display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 150px), 1fr)); gap: 10px; margin: 16px 0; }
    .fav { margin: 0; border: 1px solid var(--line); border-radius: 14px; padding: 12px; }
    .fav__row { display: flex; align-items: center; gap: 12px; }
    .fav figcaption { font-size: 12px; color: var(--ink-2); margin-top: 8px; }
    .px { image-rendering: pixelated; display: block; }
    .mvgrid { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 150px), 1fr)); gap: 12px; margin: 16px 0; }
    .mv { display: grid; justify-items: center; gap: 4px; text-align: center; border: 1px solid var(--line); border-radius: 16px; padding: 16px 10px; color: var(--ink); text-decoration: none; }
    .mv b { font-size: 14px; font-weight: 500; margin-top: 6px; }
    .mv span { text-transform: none; letter-spacing: 0; font-family: Poppins, sans-serif; font-size: 12px; font-weight: 400; }
    .linerow { display: grid; gap: 12px; margin: 16px 0; color: var(--ink); }
    .linerow > div { display: flex; flex-wrap: wrap; align-items: center; gap: 14px; }
    .linerow > div > p { flex-basis: 100%; }
    .li { width: 28px; height: 28px; fill: none; stroke: currentColor; stroke-linecap: round; stroke-linejoin: round; display: block; }
    .foot-sample { display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap; border-top: 1px solid var(--line); padding-top: 14px; margin: 14px 0; }
    .foot-sample__url { font: 400 13px 'JetBrains Mono', ui-monospace, monospace; color: var(--ink-2); }
    .dl { list-style: none; padding: 0; margin: 14px 0; display: grid; gap: 10px; }
    .dl li { display: grid; gap: 2px; border: 1px solid var(--line); border-radius: 14px; padding: 12px 16px; }
    .dl span { font-size: 13px; color: var(--ink-2); }
    .dl li::before { content: none; display: none; }
    .dl li { padding-left: 16px; }
    .dl a { justify-self: start; }
    .prose a.mk, .prose a.mv { background: none; }
    .linerow p { font: 500 11px/1 'JetBrains Mono', ui-monospace, monospace; letter-spacing: .1em; text-transform: uppercase; color: var(--ink-2); margin: 0 0 8px; }
"""

TOC = [("layers", "Two layers"), ("mark", "The mark"), ("marks", "All marks"), ("palette", "Palette"), ("type", "Type"),
       ("small", "Small sizes"), ("motion", "Motion"), ("line", "Line icons"), ("endorse", "Endorsement"), ("downloads", "Downloads")]
DESC = "The brand system behind my builds: one tile, one color recipe, three type tiers and one endorsement line."
TITLE = "Brand"
SHARE = f"{SITE_URL}/assets/img/brand/cards/brand-og.png"


def page():
    toc = "\n".join(f'        <a href="#{i}">{t}</a>' for i, t in TOC)
    body = "\n".join(f() for f in (section_intro, section_mark, section_all, section_palette, section_type, section_small,
                                   section_motion, section_line, section_endorse, section_downloads))
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{TITLE} · Chae Kim - Portfolio</title>
  <meta name="description" content="{e(DESC)}">
  <meta property="og:title" content="{TITLE} · Chae Kim - Portfolio">
  <meta property="og:description" content="{e(DESC)}">
  <meta property="og:type" content="article">
  <meta property="og:image" content="{SHARE}">
  <link rel="canonical" href="{SITE_URL}/brand">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{CASE_HEAD_ASSETS}
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@1,400&family=JetBrains+Mono:wght@400;500&display=swap">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Nanum+Brush+Script&text=%EA%B9%80%EC%B1%84%EC%9A%B4&display=swap">
  <style>{CSS}  </style>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "CreativeWork",
    "name": "Brand",
    "headline": "One family of marks for every build.",
    "description": "{e(DESC)}",
    "url": "{SITE_URL}/brand",
    "image": "{SHARE}",
    "creator": {{
      "@type": "Person",
      "name": "Chae Kim",
      "alternateName": "Chae Woon Kim",
      "url": "{SITE_URL}/"
    }}
  }}
  </script>
</head>
<body class="v v-stamp case sec-builds">
  <a class="skip" href="#main">Skip to content</a>
{CASE_TOP}

  <main id="main">
    <section class="case-hero wrap">
      <a class="case-hero__back" href="/#builds">← All builds</a>
      <p class="eyebrow">brand · builds · 2026</p>
      <h1 class="case-hero__title">One family of marks for every build.</h1>
      <p class="tldr">The short version of my brand book. One tile, one color recipe, three type tiers and one line that ties it back to me.</p>
      <p class="meta-line"><b>Role</b> Designer and decision maker · <b>Scope</b> Marks, color, type, small sizes, motion · <b>Read time</b> Two minutes</p>
    </section>

    <section class="wrap case-body">
      <nav class="toc" aria-label="On this page">
{toc}
      </nav>
      <article class="prose">{body}
      </article>
    </section>
  </main>

{CASE_FOOT}
{CASE_SCRIPTS}
{SPARK_SCRIPT}
</body>
</html>
'''


def kit():
    """assets/brand-kit/marks.zip: every mark file, with fixed timestamps so the bytes don't change between builds."""
    out = ROOT / "assets" / "brand-kit"
    out.mkdir(parents=True, exist_ok=True)
    files = []
    for f in sorted(os.listdir(BRAND)):
        if f.endswith(".svg") and not f.startswith("work-"):
            files.append((f"marks/{f[:-4].rsplit('-2', 1)[0] if f.endswith('-2.svg') else f[:-4]}.svg", os.path.join(BRAND, f)))
    for sub, exts in (("dark", (".svg",)), ("fav16", (".png",)), ("line", (".svg",))):
        for f in sorted(os.listdir(os.path.join(BRAND, sub))):
            if f.endswith(exts):
                files.append((f"marks/{sub}/{f}", os.path.join(BRAND, sub, f)))
    with zipfile.ZipFile(out / "marks.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for name, path in files:
            info = zipfile.ZipInfo(name, (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, open(path, "rb").read())
    return len(files)


if __name__ == "__main__":
    (ROOT / "brand.html").write_text(page(), encoding="utf-8")
    print(f"wrote brand.html and marks.zip ({kit()} files)")
