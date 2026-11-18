#!/usr/bin/env python3
"""Builds the homepage (index.html) and the arcade page (arcade.html).

Usage:  python3 scripts/build-home.py
The home page is scripts/home.html with its own stylesheet and script (home-sky.css, home-sky.js).
Arcade uses the project-page chrome from stamp_shared.py, with arcade.css on top.
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
                <div><p class="label" style="margin:0">Now playing</p><p class="panel__title" id="music-title">Cloud Nine</p></div>
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
# Home: the sky page. scripts/home.html is the whole page, written by hand, with its own stylesheet
# (assets/css/home-sky.css) and script (assets/js/home-sky.js). Only %%TOKENS%% are filled in here.
# ----------------------------------------------------------------------------

from stamp_shared import SITE_URL, asset, BOOT_SCRIPT, finish, CASE_HEAD_ASSETS, CASE_TOP, CASE_FOOT, CASE_SCRIPTS, build_mark, build_icons
from projects import COLLEGE, FOLDERS, PROJECTS, WORK
from writing_data import ESSAYS

HOME = open(os.path.join(HERE, "home.html"), encoding="utf-8").read()
HOME = re.sub(r"%%ASSET:([^%]+)%%", lambda m: asset(m.group(1)), HOME)
HOME = HOME.replace("%%SITE%%", SITE_URL).replace("%%BOOT%%", BOOT_SCRIPT)
assert "%%" not in HOME, "unreplaced token"

# The cards are typed into home.html, so a project or essay added elsewhere has to be added there too.
def _on_home(slug):
    p = PROJECTS[slug]
    if "card_href" in p and p["card_href"] is None:
        return True  # a card with no page of its own has nothing to link to
    return f'href="{p.get("card_href", f"/projects/{slug}")}"' in HOME

_missing = [s for s in (*(s for slugs in FOLDERS.values() for s in slugs), *WORK, *COLLEGE) if not _on_home(s)]
_missing += [e["title"] for e in ESSAYS if f'href="{e["url"]}"' not in HOME]
assert not _missing, f"add these to scripts/home.html: {_missing}"

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
for name, page in (("index.html", HOME), ("arcade.html", ARCADE_PAGE)):
    with open(os.path.join(ROOT, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(finish(page))
    print("wrote", name)
