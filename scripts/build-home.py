#!/usr/bin/env python3
"""Builds the Stamp homepage (index.html) and the arcade page (arcade.html).

Usage:  python3 scripts/build-home.py
Stamp is the only design: assets/css/v-stamp.css (+ case-stamp.css on project pages, arcade.css on /arcade).
The calligraphy name mark, case-page chrome and live-preview dialog are shared via stamp_shared.py.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

# ----------------------------------------------------------------------------
# Arcade: Snake, Galaga and a generative lo-fi radio. main.js loads arcade.js
# and music.js once #break scrolls into view.
# ----------------------------------------------------------------------------

ARCADE = """          <div class="break">
            <div class="panel reveal" id="games-panel">
              <div class="panel__head">
                <div class="gametabs" role="tablist" aria-label="Choose a game">
                  <button class="gametab is-active" data-game="snake" role="tab" aria-selected="true">Snake</button>
                  <button class="gametab" data-game="galaga" role="tab" aria-selected="false">Galaga</button>
                </div>
                <div class="panel__score"><span>Score <b id="game-score">0</b></span><span>Best <b id="game-best">0</b></span></div>
              </div>
              <div class="game" id="snake-game" data-game="snake">
                <div class="snake">
                  <canvas id="snake" width="400" height="400" tabindex="0" aria-label="Snake game. Use arrow keys or WASD."></canvas>
                  <button class="snake__overlay btn btn--primary" id="snake-start" type="button">Play</button>
                </div>
                <p class="game__hint">Arrows · WASD · swipe</p>
                <div class="snake__dpad" aria-label="Touch controls">
                  <button data-dir="0,-1" aria-label="Up">▲</button>
                  <div><button data-dir="-1,0" aria-label="Left">◀</button><button data-dir="0,1" aria-label="Down">▼</button><button data-dir="1,0" aria-label="Right">▶</button></div>
                </div>
              </div>
              <div class="game is-hidden" id="galaga-game" data-game="galaga">
                <div class="snake galaga">
                  <canvas id="galaga" width="400" height="400" tabindex="0" aria-label="Galaga game. Left and right arrows move, space fires."></canvas>
                  <button class="snake__overlay btn btn--primary" id="galaga-start" type="button">Play</button>
                </div>
                <p class="game__hint">← → or drag to move · space / tap to fire</p>
              </div>
            </div>
            <div class="panel reveal" id="music-panel">
              <div class="panel__head">
                <div><p class="label" style="margin:0">Now playing</p><h3 class="panel__title" id="music-title">Cloud Nine</h3></div>
                <span class="panel__note">Generative lo-fi, synthesized live in your browser. Starts only when you press play.</span>
              </div>
              <canvas class="music__viz" id="music-viz" width="600" height="140" aria-hidden="true"></canvas>
              <div class="music__controls">
                <button class="music__btn" id="music-prev" type="button" aria-label="Previous track"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M6 6h2v12H6zM20 6v12L9 12z"/></svg></button>
                <button class="music__btn music__btn--main" id="music-play" type="button" aria-label="Play"><svg class="ico-play" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg><svg class="ico-pause" viewBox="0 0 24 24" fill="currentColor"><path d="M6 5h4v14H6zM14 5h4v14h-4z"/></svg></button>
                <button class="music__btn" id="music-next" type="button" aria-label="Next track"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M16 6h2v12h-2zM4 6v12l11-6z"/></svg></button>
                <label class="music__vol"><span class="visually-hidden">Volume</span><svg viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M3 9v6h4l5 5V4L7 9zM16 8a4.5 4.5 0 0 1 0 8v-2a2.5 2.5 0 0 0 0-4z"/></svg><input type="range" id="music-vol" min="0" max="1" step="0.01" value="0.6"></label>
              </div>
              <ul class="music__list" id="music-list"></ul>
            </div>
          </div>
"""


# ----------------------------------------------------------------------------
# Stamp: quiet, gallery-like, artifact-first. The page is scripts/home.html, with %%TOKENS%% filled in below.
# ----------------------------------------------------------------------------

from stamp_shared import SITE_URL, asset, BOOT_SCRIPT, PALETTE_SCRIPT, nb_headlines, changelog_strip, INK_DEFS, seal, live_button, LIVE_DIALOG, LIVE_SCRIPT, CASE_HEAD_ASSETS, CASE_TOP, CASE_FOOT, CASE_SCRIPTS, THEME_COLOR, GLASS_JS, build_mark, build_icons, mark_color, work_mark, LIVE_APPS
from projects import COLLEGE, FEATURED, FOLDERS, PROJECTS, WORK, field


def _snake():
    body = [(2,6),(3,6),(4,6),(5,6),(5,5),(5,4),(6,4),(7,4),(8,4),(9,4),(9,5),(10,5)]
    cell = lambda c, r, fill: f'<rect x="{c*10+1}" y="{r*10+1}" width="8" height="8" rx="1.6" fill="{fill}"/>'
    return ('<svg class="snake-art" viewBox="0 0 160 100" aria-hidden="true">'
            '<defs><pattern id="px" width="10" height="10" patternUnits="userSpaceOnUse">'
            '<path d="M10 0H0V10" fill="none" stroke="rgba(255,255,255,.07)"/></pattern></defs>'
            '<rect width="160" height="100" fill="url(#px)"/>'
            + "".join(cell(c, r, "#58cf86") for c, r in body)
            + cell(11, 5, "#a6f0bf") + cell(13, 5, "#ffd60a") + '</svg>')

STAMP = open(os.path.join(HERE, "home.html"), encoding="utf-8").read()

# ----------------------------------------------------------------------------
# Writing tab: essays and the reading list come from writing_data.py (shared with /reading)
# ----------------------------------------------------------------------------
import html as _html
from writing_data import ESSAYS, READING, pub_label


def _writing_essays():
    rows = []
    for e in ESSAYS:
        internal = e.get("internal")
        ext = "" if internal else ' target="_blank" rel="noopener"'
        arrow = "" if internal else " ↗"
        date = f' · {pub_label(e["published"])}' if e["published"] else ""
        rows.append(f'        <li class="reveal"><h3><a href="{_html.escape(e["url"], quote=True)}"{ext}>{_html.escape(e["title"])}{arrow}</a></h3>'
                    f'<p class="wl-by">{"On this site" if internal else "Medium"}{date}</p>'
                    f'<p class="wl-sum">{_html.escape(e["description"])}</p></li>')
    return '      <ul class="wlist">\n' + "\n".join(rows) + "\n      </ul>"


def _writing_reading():
    rows = []
    for a in READING:
        summary = f'<p class="wl-sum">{_html.escape(a["summary"])}</p>' if a["summary"] else ""
        note = f'<p class="wl-sum"><b>My notes:</b> {_html.escape(a["note"])}</p>' if a["note"] else ""
        tags = "".join(f"<span>{_html.escape(t)}</span>" for t in a["topics"])
        rows.append(f'        <li class="reveal"><h3><a href="{_html.escape(a["url"], quote=True)}" target="_blank" rel="noopener">{_html.escape(a["title"])} ↗</a></h3>'
                    f'<p class="wl-by">{_html.escape(a["author"])} · {_html.escape(a["source"])} · added {a["added"]}</p>'
                    f'{summary}{note}<div class="wl-tags">{tags}</div></li>')
    return '      <ul class="wlist">\n' + "\n".join(rows) + "\n      </ul>"


# Builds folders: count each tray's cards so the numbers on the folders never go stale.
def _card_open(p, cls):
    href = p.get("card_href", f"/projects/{p['slug']}")
    return f'<a class="{cls}" href="{href}"{p.get("card_attrs", "")}>'

def _card(slug):
    """A home card. Live apps wrap the link so the "Try it live" button can sit beside it."""
    p = PROJECTS[slug]
    body = p["card"].strip("\n")
    if slug in FEATURED:
        return (f'        <article class="feat__card reveal">\n        {_card_open(p, "w feat__w")}\n{body}\n        </a>\n'
                f'        <div class="feat__strip">{live_button(slug)}<a class="feat__case" href="/projects/{slug}">Read the case study →</a></div>\n'
                '        </article>')
    if slug in LIVE_APPS:
        return (f'        <div class="live-card reveal">\n        {_card_open(p, "w")}\n{body}\n        </a>\n'
                f'        {live_button(slug)}\n        </div>')
    if p.get("card_href", "") is None:
        return f'        <div class="w reveal">\n{body}\n        </div>'
    wide = " w--wide" if p.get("card_wide") else ""
    return f'        {_card_open(p, f"w{wide} reveal")}\n{body}\n        </a>'

def _cards(page):
    page = page.replace("%%CARDS_FEATURED%%", "\n".join(_card(s) for s in FEATURED))
    for fid, slugs in FOLDERS.items():
        shelf = [s for s in slugs if s not in FEATURED]
        key = fid.upper().replace("-", "_")
        page = (page.replace(f"%%CARDS_{key}%%", "\n".join(_card(s) for s in shelf))
                    .replace(f"%%COUNT_{key}%%", str(len(shelf))))
    return (page.replace("%%CARDS_WORK%%", "\n\n".join(_card(s) for s in WORK))
                .replace("%%CARDS_COLLEGE%%", "\n".join(_card(s) for s in COLLEGE)))


STAMP = _cards(STAMP)
STAMP = re.sub(r"%%ASSET:([^%]+)%%", lambda m: asset(m.group(1)), STAMP)
STAMP = (STAMP.replace("%%WRITING_ESSAYS%%", _writing_essays())
              .replace("%%WRITING_READING%%", _writing_reading())
              .replace("%%GLASS_JS%%", GLASS_JS)
              .replace("%%SITE%%", SITE_URL)
              .replace("%%INK%%", INK_DEFS)
              .replace("%%BRANDSEAL%%", seal("cal--card", label=False))
              .replace("%%SEAL%%", seal())
              .replace("%%SEAL_SMALL%%", seal(label=False))
              .replace("%%SNAKE%%", _snake())
              .replace("%%CHANGELOG%%", changelog_strip("index.html"))
              .replace("%%BOOT%%", BOOT_SCRIPT).replace("%%PALETTE_SCRIPT%%", PALETTE_SCRIPT)
              .replace("%%THEME_COLOR%%", THEME_COLOR)
              .replace("%%LIVE_DIALOG%%", LIVE_DIALOG)
              .replace("%%LIVE_SCRIPT%%", LIVE_SCRIPT))
assert "%%" not in STAMP, "unreplaced token"

# Each card's pill leads with the build's color-seal mark, found from the page the card links to.
# The name gets its own span so it can truncate on narrow cards instead of being clipped.
def _pill_mark(m):
    mark = build_mark(m.group(2), "pill__mark", 18, themed=True) or work_mark(m.group(2), "pill__mark", 18)
    return m.group(1) + (f'{mark}<span class="pill__name">{m.group(3)}</span>' if mark else m.group(3))

STAMP = re.sub(r'(href="/(?:projects/)?([a-z0-9-]+)"[^>]*>\s*<div class="stage"(?:(?!</a>).)*?<span class="pill">)([^<]*?)(?=\s*<em>|</span>)',
               _pill_mark, STAMP, flags=re.S)

# Each build's card washes with its mark's base color (the .tint rule in v-stamp.css mixes it into paper or night).
# Dark-tile builds keep a dark or neutral stage instead, matching their dark tiles.
STAGE_KEEPS = field("stage")

def _wash_stage(m):
    slug = m.group(2)
    if slug in STAGE_KEEPS:
        return m.group(1) + f'<div class="stage" style="--g: var(--g-{STAGE_KEEPS[slug]})">'
    color = mark_color(slug)
    return m.group(1) + (f'<div class="stage tint" style="--bc: {color}">' if color else m.group(3))

STAMP = re.sub(r'(href="/(?:projects/)?([a-z0-9-]+)"[^>]*>\s*)(<div class="stage"(?: style="--g: var\(--g-[a-z]+\)")?>)',
               _wash_stage, STAMP)

# ----------------------------------------------------------------------------
# Arcade page, in the same chrome as the project pages
# ----------------------------------------------------------------------------

ARCADE_ICONS = build_icons("arcade", SITE_URL)

# The row of build marks comes from build-cases.py, so Arcade is in step with the case studies.
import importlib.util
_spec = importlib.util.spec_from_file_location("build_cases", os.path.join(HERE, "build-cases.py"))
_cases = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_cases)
ARCADE_SWITCHER = _cases.render_switcher("arcade")

ARCADE_PAGE = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Arcade · Chae Kim - Portfolio</title>
  <meta name="description" content="Snake and Galaga, rebuilt from memory, plus a generative lo-fi radio.">
  <meta property="og:title" content="Arcade · Chae Kim - Portfolio">
  <meta property="og:description" content="Snake and Galaga, rebuilt from memory, plus a generative lo-fi radio.">
  <meta property="og:type" content="website">
  <meta property="og:image" content="{ARCADE_ICONS[1]}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <link rel="canonical" href="{SITE_URL}/arcade">
{ARCADE_ICONS[0]}
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{CASE_HEAD_ASSETS}
  <link rel="stylesheet" href="{asset("css/arcade.css")}">
</head>
<body class="v v-stamp case sec-builds">
  <a class="skip" href="#main">Skip to content</a>
{CASE_TOP}

  <main id="main">
{ARCADE_SWITCHER}
    <section class="case-hero wrap">
      <a class="case-hero__back" href="/#builds">← All builds</a>
      {build_mark("arcade", "case-hero__mark", 56, themed=True)}
      <p class="eyebrow">side quest · arcade</p>
      <h1 class="case-hero__title">Arcade</h1>
      <p class="tldr">Snake and Galaga, rebuilt from memory, plus a generative lo-fi radio.</p>
    </section>

    <section class="wrap arcade" id="break">
{ARCADE}    </section>
  </main>

{CASE_FOOT}
{CASE_SCRIPTS}
</body>
</html>
"""
for name, page in (("index.html", STAMP), ("arcade.html", ARCADE_PAGE)):
    with open(os.path.join(ROOT, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(nb_headlines(page))
    print("wrote", name)
