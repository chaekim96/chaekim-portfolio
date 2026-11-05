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
# Stamp: quiet, gallery-like, artifact-first. Plain string with %%TOKENS%%
# rather than an f-string, since the inline JS is brace-heavy.
# ----------------------------------------------------------------------------

from stamp_shared import STAMP_CSS_V as V, BOOT_SCRIPT, PALETTE_SCRIPT, nb_headlines, changelog_strip, INK_DEFS, seal, live_button, LIVE_DIALOG, LIVE_SCRIPT, CASE_HEAD_ASSETS, CASE_TOP, CASE_FOOT, CASE_SCRIPTS, THEME_COLOR, SIGNAL_CSS, GLASS_JS, build_mark, build_icons, mark_color, work_mark, LIVE_APPS
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

STAMP = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Chae Kim - Portfolio</title>
  <meta name="description" content="Chae Kim: MBA at Berkeley Haas, co-founded Lucent, previously at EY and Tritooling. I like to build things. Let's chat.">
  <meta property="og:title" content="Chae Kim - Portfolio">
  <meta property="og:description" content="MBA at Berkeley Haas. Co-founded Lucent. Previously at EY and Tritooling. I like to build things.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://chaekim-portfolio.vercel.app/">
  <meta property="og:image" content="https://chaekim-portfolio.vercel.app/assets/img/og-sky.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <link rel="canonical" href="https://chaekim-portfolio.vercel.app/">
%%THEME_COLOR%%
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap">
  <link rel="preload" as="image" href="/assets/img/thumbs/lucent-wide.jpg">
  <link rel="stylesheet" href="/assets/css/v-stamp.css?v=%%V%%">
%%SIGNAL_CSS%%
%%GLASS_JS%%
  %%BOOT%%
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Person",
    "name": "Chae Woon Kim",
    "alternateName": "Chae Kim",
    "url": "https://chaekim-portfolio.vercel.app/",
    "image": "https://chaekim-portfolio.vercel.app/assets/img/memoji.png",
    "jobTitle": "MBA Candidate, UC Berkeley Haas; Co-founder & CEO, Lucent",
    "worksFor": { "@type": "Organization", "name": "Lucent", "url": "https://trylucent.ai" },
    "alumniOf": [
      { "@type": "CollegeOrUniversity", "name": "UC Berkeley, Haas School of Business" },
      { "@type": "CollegeOrUniversity", "name": "Indiana University Bloomington" }
    ],
    "sameAs": ["https://www.linkedin.com/in/chaekim/", "https://github.com/chaekim96", "https://medium.com/@chaewoonkim"]
  }
  </script>
</head>
<body class="v v-stamp">
  <a class="skip" href="#main">Skip to content</a>
  %%INK%%
  <div class="aurora" aria-hidden="true"></div>

  <header class="top wrap">
    <a class="seal" href="#work">%%SEAL%%</a>
    <button class="theme-toggle" type="button" aria-label="Toggle dark mode">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>
    </button>
  </header>

  <main id="main" class="wrap">
    <section class="intro" aria-label="Introduction">
      <h1 class="name">chae kim</h1>
      <p class="thesis">I like to build things, from startups to card games.</p>
      <p class="cred">MBA at Berkeley Haas. Co-founded <a href="/projects/lucent">Lucent</a>. Previously at <a href="/projects/ey">EY</a> &amp; <a href="/projects/tritooling">Tritooling</a>.<br>
        <span class="status"><i aria-hidden="true"></i><span>Lately building <a href="#builds">TypeRace</a>, a typing race for my classmates.</span></span></p>
      <p class="hello">Let's chat: <a data-user="chaewoonkim" data-domain="berkeley.edu" data-show href="#">email me</a> <button class="hello__copy" type="button" data-copy-email>Copy</button></p>
    </section>

    <div class="tabs" role="tablist" aria-label="Sections">
      <button class="tab" role="tab" id="tab-builds" data-tab="builds" aria-controls="builds" aria-selected="true">Builds</button>
      <button class="tab" role="tab" id="tab-work" data-tab="work" aria-controls="work" aria-selected="false" tabindex="-1">Work</button>
      <button class="tab" role="tab" id="tab-writing" data-tab="writing" aria-controls="writing" aria-selected="false" tabindex="-1">Writing</button>
      <button class="tab" role="tab" id="tab-about" data-tab="about" aria-controls="about" aria-selected="false" tabindex="-1">About</button>
    </div>

    <!-- ============ BUILDS ============ -->
    <section class="panel" id="builds" role="tabpanel" aria-labelledby="tab-builds">
      <h2 class="sub-h">Three to try first</h2>
      <div class="feat" data-play>
%%CARDS_FEATURED%%
      </div>

      <h2 class="sub-h">Browse by folder</h2>
      <nav class="folders" aria-label="Project folders">
        <a class="fold reveal" href="#products" data-folder="products" aria-controls="products" aria-expanded="false">
          <span class="fold__art" style="--tint: var(--t-products)" aria-hidden="true"><span class="fold__back"></span><span class="fold__peek"><img src="/assets/img/brand/palette-generator-2.svg" alt="" width="64" height="64" loading="lazy"><img src="/assets/img/brand/networking-tracker.svg" alt="" width="64" height="64" loading="lazy"><img src="/assets/img/brand/web-anatomy-2.svg" alt="" width="64" height="64" loading="lazy"></span><span class="fold__front">%%COUNT_PRODUCTS%% items</span></span>
          <span class="fold__nm">Products<span>%%COUNT_PRODUCTS%%</span></span>
          <span class="fold__ds">Web apps you can try live</span>
        </a>
        <a class="fold reveal" href="#mods" data-folder="mods" aria-controls="mods" aria-expanded="false">
          <span class="fold__art" style="--tint: var(--t-mods)" aria-hidden="true"><span class="fold__back"></span><span class="fold__peek"><img src="/assets/img/brand/smartmodel.svg" alt="" width="64" height="64" loading="lazy"><img src="/assets/img/brand/token-fuel.svg" alt="" width="64" height="64" loading="lazy"><img src="/assets/img/brand/code-improver.svg" alt="" width="64" height="64" loading="lazy"></span><span class="fold__front">%%COUNT_MODS%% items</span></span>
          <span class="fold__nm">Claude Code mods<span>%%COUNT_MODS%%</span></span>
          <span class="fold__ds">Hooks, gauges, subagents</span>
        </a>
        <a class="fold reveal" href="#ai-ml" data-folder="ai-ml" aria-controls="ai-ml" aria-expanded="false">
          <span class="fold__art" style="--tint: var(--t-ai-ml)" aria-hidden="true"><span class="fold__back"></span><span class="fold__peek"><img src="/assets/img/brand/spotify-review-triage.svg" alt="" width="64" height="64" loading="lazy"><img src="/assets/img/brand/personal-wiki.svg" alt="" width="64" height="64" loading="lazy"><img src="/assets/img/brand/pacman-dqn-2.svg" alt="" width="64" height="64" loading="lazy"></span><span class="fold__front">%%COUNT_AI_ML%% items</span></span>
          <span class="fold__nm">AI and ML coursework<span>%%COUNT_AI_ML%%</span></span>
          <span class="fold__ds">LLMs, RL, retrieval</span>
        </a>
        <a class="fold reveal" href="#design" data-folder="design" aria-controls="design" aria-expanded="false">
          <span class="fold__art" style="--tint: var(--t-design)" aria-hidden="true"><span class="fold__back"></span><span class="fold__peek"><img src="/assets/img/folders/siri.jpg" alt="" width="64" height="64" loading="lazy"><img src="/favicon.svg" alt="" width="64" height="64" loading="lazy"><img src="/assets/img/brand/typerace.svg" alt="" width="64" height="64" loading="lazy"></span><span class="fold__front">%%COUNT_DESIGN%% items</span></span>
          <span class="fold__nm">Design &amp; brand<span>%%COUNT_DESIGN%%</span></span>
          <span class="fold__ds">Concepts, brand, this site</span>
        </a>
        <a class="fold reveal" href="#archive" data-folder="archive" aria-controls="archive" aria-expanded="false">
          <span class="fold__art" style="--tint: var(--t-archive)" aria-hidden="true"><span class="fold__back"></span><span class="fold__peek"><img src="/assets/img/brand/arcade-2.svg" alt="" width="64" height="64" loading="lazy"><img src="/assets/img/folders/home.jpg" alt="" width="64" height="64" loading="lazy"><img src="/assets/img/folders/yin-yang.jpg" alt="" width="64" height="64" loading="lazy"></span><span class="fold__front">%%COUNT_ARCHIVE%% items</span></span>
          <span class="fold__nm">Fun &amp; archive<span>%%COUNT_ARCHIVE%%</span></span>
          <span class="fold__ds">Games, art, 2019 to 2020 projects</span>
        </a>
      </nav>
      <script>document.documentElement.classList.add('js-folders')</script>
      <div class="trays">
      <section class="tray" id="products" aria-label="Products">
        <div class="tray__h"><h3>Products <span>· %%COUNT_PRODUCTS%%</span></h3><a class="tray__close" href="#builds" data-fold-close>Close ✕</a></div>
        <div class="grid grid--shelf">
%%CARDS_PRODUCTS%%
        </div>
      </section>
      <section class="tray" id="mods" aria-label="Claude Code mods">
        <div class="tray__h"><h3>Claude Code mods <span>· %%COUNT_MODS%%</span></h3><a class="tray__close" href="#builds" data-fold-close>Close ✕</a></div>
        <div class="grid grid--shelf">
%%CARDS_MODS%%
        </div>
      </section>
      <section class="tray" id="ai-ml" aria-label="AI and ML coursework">
        <div class="tray__h"><h3>AI and ML coursework <span>· %%COUNT_AI_ML%%</span></h3><a class="tray__close" href="#builds" data-fold-close>Close ✕</a></div>
        <div class="grid grid--shelf">
%%CARDS_AI_ML%%
        </div>
      </section>
      <section class="tray" id="design" aria-label="Design &amp; brand">
        <div class="tray__h"><h3>Design &amp; brand <span>· %%COUNT_DESIGN%%</span></h3><a class="tray__close" href="#builds" data-fold-close>Close ✕</a></div>
        <div class="grid grid--shelf">
%%CARDS_DESIGN%%
        </div>
      </section>
      <section class="tray" id="archive" aria-label="Fun &amp; archive">
        <div class="tray__h"><h3>Fun &amp; archive <span>· %%COUNT_ARCHIVE%%</span></h3><a class="tray__close" href="#builds" data-fold-close>Close ✕</a></div>
        <div class="grid grid--shelf">
%%CARDS_ARCHIVE%%
        </div>
      </section>
      </div>
    </section>

    <!-- ============ WRITING ============ -->
    <section class="panel" id="writing" role="tabpanel" aria-labelledby="tab-writing">
      <h2 class="sub-h">Essays</h2>
%%WRITING_ESSAYS%%

      <h2 class="sub-h">Case-study write-ups</h2>
      <div class="grid grid--3">
        <a class="w reveal" href="/projects/decisions">
          <div class="stage" style="--g: var(--g-mobility)"><div class="art"><div class="glass"><b>Options</b><span>and the pick</span></div></div><span class="pill">How I decide <em>2026</em></span></div>
          <p class="meta">The options I laid out for each call on this site and my projects, which one I picked, and why.</p>
        </a>
        <a class="w reveal" href="/projects/portfolio">
          <div class="stage" style="--g: var(--g-lucent)"><div class="art"><div class="browser"><div class="browser__bar"><i></i><i></i><i></i><span>chaekim.vercel.app</span></div><img src="/assets/img/builds/portfolio-card.jpg" alt="This site's homepage" width="960" height="600" loading="lazy"></div></div><span class="pill">This portfolio <em>2026</em></span></div>
          <p class="meta">How this site got built: the decisions, the backlog, and what's next.</p>
        </a>
        <a class="w reveal" href="/projects/personal-brand">
          <div class="stage" style="--g: var(--g-plain)"><div class="art"><div class="brandart">%%BRANDSEAL%%<span class="brandart__sw"><i style="background:#C8372D"></i><i style="background:#FF5A1F"></i><i style="background:#B07A4F"></i><i style="background:#0066CC"></i><i style="background:#123B2E"></i></span></div></div><span class="pill">Personal brand <em>2026</em></span></div>
          <p class="meta">How I chose a brand: five directions, two built finalists, and why Stamp won.</p>
        </a>
      </div>

      <h2 class="sub-h">Reading list</h2>
%%WRITING_READING%%
      <p class="wl-more">The same list, with topic filters, is on its own page: <a href="/reading">Writing &amp; reading</a>.</p>
    </section>

    <!-- ============ WORK ============ -->
    <section class="panel" id="work" role="tabpanel" aria-labelledby="tab-work">
      <h2 class="visually-hidden">Work</h2>
      <div class="grid">
%%CARDS_WORK%%
      </div>

      <h2 class="sub-h">Earlier, at Indiana University (2019 to 2021)</h2>
      <div class="grid grid--5">
%%CARDS_COLLEGE%%
      </div>
    </section>

    <!-- ============ ABOUT ============ -->
    <section class="panel" id="about" role="tabpanel" aria-labelledby="tab-about">
      <div class="about">
        <nav class="toc" aria-label="About sections">
          <a href="#hi">Hi!</a><a href="#experience">Experience</a><a href="#off-the-clock">Off the clock</a><a href="#elsewhere">Elsewhere</a>
        </nav>
        <div class="about__body">
          <section id="hi">
            <h2>Hi, I'm Chae.</h2>
            <div class="facts">
              <span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/></svg>Berkeley, CA</span>
              <span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c3 2 9 2 12 0v-5"/></svg>MBA, Berkeley Haas '27</span>
              <span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c3 2 9 2 12 0v-5"/></svg>B.S. Informatics, Indiana University</span>
            </div>
            <p>Thirteen years growing up overseas made me curious by default. I'm happiest making things: a wireframe, a 3D print, a card game.</p>
            <p>I've founded an NSF I-Corps AI startup, led Fortune 500 cloud programs, and run a precision manufacturer's operations. These days I build tools I'd actually use. If you're making something too, I'd love to hear about it.</p>
            <p>I'm also writing a memoir, <em>The Treaded Path</em>, and essays on <a href="https://medium.com/@chaewoonkim" target="_blank" rel="noopener">Medium ↗</a>. My essays and the articles that helped are on the <a href="#writing">Writing tab</a>.</p>
          </section>

          <section id="experience">
            <h3>Experience</h3>
            <ul class="xp">
              <li><b>UC Berkeley Haas</b><small>2025–27</small><span><em>MBA Candidate.</em> Merit Scholarship. Co-President, Asian Business Club (300+ members).</span></li>
              <li><b>Lucent</b><small>2025–26</small><span><em>Co-founder &amp; CEO.</em> First paying pilot. 5 LOIs in 30 days. 100+ customer interviews. NSF I-Corps backed.</span></li>
              <li><b>Tritooling Precision Corporation</b><small>Jul 2024–Jul 2025</small><span><em>Director of Operations, Philippines.</em> On-time delivery +15%, defects −30%. ERP make-vs-buy case approved, $100K in annual savings. Board approval to launch in Japan, a $300K+ revenue opportunity.</span></li>
              <li><b>EY</b><small>Aug 2021–Jul 2024</small><span><em>Senior Technology Consultant, AI &amp; Data Strategy, New York.</em> Redirected $3M to priority initiatives after launching a Fortune 500 client's first QBR. $10M+ in realized savings over 2 years. −30% escalations on a $200M+ program. 90% tool adoption across 4,000 users.</span></li>
              <li><b>Indiana University Bloomington</b><small>Class of 2021</small><span><em>B.S. Informatics, minors in HCI &amp; Entrepreneurship.</em> Dean's List. GPA 3.74.</span></li>
              <li><b>Republic of Korea Army, Gangwon</b><small>2017–19</small><span><em>Sergeant, 2nd Artillery Brigade.</em> Ran 15 high-stakes artillery operations, leading 10 soldiers and interpreting for ROK and U.S. commanders.</span></li>
            </ul>
          </section>

          <section id="off-the-clock">
            <h3>Off the clock</h3>
            <ul class="likes">
              <li><b>3D printing</b>, design and prototyping</li>
              <li><b>Competitive tennis</b> and latte art</li>
              <li><b>Big Brothers Big Sisters</b> mentor, 4+ year match</li>
            </ul>
            <div class="photos">
              <figure><img src="/assets/img/profile.jpg" alt="Chae waving next to an elephant in Phuket" width="1200" height="1600" loading="lazy"></figure>
              <figure><img src="/assets/img/travel-1.jpg" alt="A pink coconut by a pool in Bali" width="900" height="1200" loading="lazy"></figure>
              <figure><img src="/assets/img/travel-3.jpg" alt="Limestone cliffs over green water in Ha Long Bay" width="900" height="1200" loading="lazy"></figure>
              <figure><img src="/assets/img/travel-2.jpg" alt="A boat at sunset" width="900" height="1200" loading="lazy"></figure>
            </div>
          </section>

          <section id="elsewhere">
            <h3>Elsewhere</h3>
            <div class="links">
              <a data-user="chaewoonkim" data-domain="berkeley.edu" href="#">Email</a>
              <a href="https://www.linkedin.com/in/chaekim/" target="_blank" rel="noopener">LinkedIn ↗</a>
              <a href="https://medium.com/@chaewoonkim" target="_blank" rel="noopener">Medium ↗</a>
              <a href="https://github.com/chaekim96" target="_blank" rel="noopener">GitHub ↗</a>
              <a href="/assets/pdf/chae-kim-resume.pdf">Resume (PDF)</a>
            </div>
          </section>
        </div>
      </div>
    </section>

    <!-- ============ DESIGN NOTES ============ -->
    <section class="notes" id="design-notes" aria-labelledby="notes-h">
      <h2 id="notes-h">How this page is put together</h2>
      <p class="notes__lede">Quiet, Poppins for words, real work as the picture.</p>

      <div class="notes__grid">
        <details class="ncard ncard--color">
          <summary><p class="ncard__k"><i aria-hidden="true"></i>Color</p>
          <h3>Color follows the content, so the page stays neutral</h3><span class="ncard__more" aria-hidden="true">Read more</span></summary>
          <p class="notes__cap">Light, then dark. Tokens from <code>v-stamp.css</code> and <code>signal-green.css</code>.</p>
          <ul class="swl">
            <li><span class="sw"><i style="background:#0d1b2e"></i><i style="background:#f5f5f7"></i></span><span class="swl__t"><b>ink</b> text</span><span class="swl__h"><code>#0d1b2e</code> / <code>#f5f5f7</code></span></li>
            <li><span class="sw"><i style="background:#44566e"></i><i style="background:#a1a1a6"></i></span><span class="swl__t"><b>ink-2</b> secondary text</span><span class="swl__h"><code>#44566e</code> / <code>#a1a1a6</code></span></li>
            <li><span class="sw"><i style="background:#eef7fe"></i><i style="background:#0b0b0c"></i></span><span class="swl__t"><b>bg</b> page, under the sky</span><span class="swl__h"><code>#eef7fe</code> / <code>#0b0b0c</code></span></li>
            <li><span class="sw"><i style="background:rgba(20,70,130,.12)"></i><i style="background:rgba(255,255,255,.10)"></i></span><span class="swl__t"><b>line</b> hairlines</span><span class="swl__h"><code>rgba(20,70,130,.12)</code> / <code>rgba(255,255,255,.10)</code></span></li>
            <li><span class="sw"><i style="background:#064e8c"></i><i style="background:#6bbcff"></i></span><span class="swl__t"><b>sky accent</b> links, back arrows</span><span class="swl__h"><code>#064e8c</code> / <code>#6bbcff</code></span></li>
            <li><span class="sw"><i style="background:#0b63b8"></i><i style="background:#6bbcff"></i></span><span class="swl__t"><b>sky fill</b> active tab, focus ring</span><span class="swl__h"><code>#0b63b8</code> / <code>#6bbcff</code></span></li>
            <li><span class="sw"><i style="background:#30d158"></i><i style="background:#30d158"></i></span><span class="swl__t"><b>live</b> status dot, nothing else</span><span class="swl__h"><code>#30d158</code> / <code>#30d158</code></span></li>
          </ul>
          <div class="grads">
            <div><i style="background:linear-gradient(180deg,#74bff0 0%,#a8d7f7 24%,#d6ecfc 58%,#eef7fe 100%)"></i><span>Sky, light: <code>#74bff0</code> to <code>#a8d7f7</code> to <code>#d6ecfc</code> to <code>#eef7fe</code>, with soft white clouds</span></div>
            <div><i style="background:linear-gradient(180deg,#0f1a2e 0%,#0d1424 30%,#0b0e15 55%,#0b0b0c 75%)"></i><span>Night sky, dark: <code>#0f1a2e</code> to <code>#0b0b0c</code>, with faint clouds</span></div>
          </div>
          <p>Each project sits on its own soft gradient stage, tinted from its build mark, so the work supplies the color. Everything else stays neutral: these four notes share one sky tint on purpose. The page opens on a sky: soft blue overhead, a few clouds, fading to white behind the work. I like that blue. It stays calm, not loud, feels light and airy, and keeps the black and white from my brand exploration from feeling stark.</p>
          <p>One accent does the rest of the work. A deep sky blue marks links, back arrows, the active tab and focus rings. Green appears in one place only: the dot that means something is live. Link and button text clears 4.5:1 against the sky and white.</p>
        </details>

        <details class="ncard ncard--type">
          <summary><p class="ncard__k"><i aria-hidden="true"></i>Type</p>
          <h3>Poppins for words, a plain monospace for facts</h3><span class="ncard__more" aria-hidden="true">Read more</span></summary>
          <p class="notes__cap">400, 500 and 600 are loaded. I kept Poppins instead of switching to the SF system font. Its round, geometric letters feel friendly, not corporate. One family for every word keeps the focus on the work, and it has carried every version of this site.</p>
          <div class="spec">
            <p class="spec__a">chae kim</p>
            <p class="spec__b">Making small businesses visible in AI search.</p>
            <p class="spec__c">Product, strategy, operations, and the occasional 3D print.</p>
            <p class="spec__d">Aa Bb Cc 0123456789</p>
          </div>
          <table class="scale">
            <tr><td>Name</td><td>500 · 28 to 34px · -0.025em</td></tr>
            <tr><td>Section title</td><td>500 · 22px · -0.02em</td></tr>
            <tr><td>Project headline</td><td>500 · 17px</td></tr>
            <tr><td>Body</td><td>400 · 16px / 1.55</td></tr>
            <tr><td>Notes</td><td>400 · 14px</td></tr>
            <tr><td>Case page facts</td><td>400 · 13.5px · system monospace</td></tr>
          </table>
          <p>The one exception to Poppins is the role, team and dates line on a case page. It is set in the system monospace, so facts read differently from the story around them. It costs no font download. The only other letters are the 김채운 strip at the top, brushed with East Sea Dokdo outlines drawn inline.</p>
        </details>

        <details class="ncard ncard--pages">
          <summary><p class="ncard__k"><i aria-hidden="true"></i>Structure</p>
          <h3>Pages you explore, with the work as the picture</h3><span class="ncard__more" aria-hidden="true">Read more</span></summary>
          <ul class="bul">
            <li>Pill tabs for Builds, Work, Writing and About, routed by the URL hash. Builds opens first.</li>
            <li>Builds shows three projects to try, then five folders. Each opens in a tray, so the page stays short.</li>
            <li>Every project is a framed artifact: a real screenshot, a card, a gauge.</li>
            <li>A live Berkeley clock and a day or night icon in the footer.</li>
            <li>Light and dark themes, saved in the browser.</li>
            <li>Press ⌘K (Ctrl K on Windows) to jump to any build, tab or page.</li>
            <li>Every build page has a row of build marks to hop between builds, and a contents list that follows your scroll.</li>
          </ul>
          <p class="notes__cap" style="margin-top:18px">Shapes and motion</p>
          <ul class="bul">
            <li>Cards 24px radius. Content width 1200px.</li>
            <li>Hover easing <code>cubic-bezier(.32, .72, 0, 1)</code>.</li>
            <li>Frosted blur on small tiles only. Everything else is a plain surface with a hairline.</li>
            <li>Motion is slow and soft, plays once, and switches off when your device asks for less motion.</li>
          </ul>
        </details>

        <details class="ncard ncard--path">
          <summary><p class="ncard__k"><i aria-hidden="true"></i>History</p>
          <h3>How I got here</h3><span class="ncard__more" aria-hidden="true">Read more</span></summary>
          <ol class="path">
            <li><b>2021</b><span>An IU portfolio built for class.</span></li>
            <li><b>Sept 2026</b><span>Rebuilt as a macOS desktop, inspired by renee.wiki. Then an Apple HIG layer, with Poppins kept over SF.</span></li>
            <li><b>Oct 4</b><span>A quiet, artifact-first page inspired by liumichelle.com. That became Stamp.</span></li>
            <li><b>Oct 8 to 9</b><span>A brand exploration: five directions, narrowed to two built finalists. Ink was monochrome with brush calligraphy. Desktop Craft was Apple polish. <a href="/projects/personal-brand">Read the brand decision log</a>.</span></li>
            <li><b>Oct 12</b><span>Stamp became the whole site. The other designs were retired. Stamp is quieter, and you can find the work in one scroll instead of opening windows.</span></li>
          </ol>
          <p class="notes__cap" style="margin-top:14px"><a href="/projects/portfolio">Read the full decision log: how this site was built</a><br><a href="/projects/decisions">See the options behind each call</a></p>
        </details>
      </div>
    </section>
  </main>

  <footer class="foot wrap">
    <div>
      <a class="foot__id" href="#builds">%%SEAL_SMALL%%chae kim</a>
      <p class="clock">
        <svg id="clock-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <g class="sun"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></g>
          <g class="moon"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></g>
        </svg>
        <time id="clock"></time><span>Berkeley, CA</span>
      </p>
    </div>
    <nav aria-label="Footer">
      <a href="#builds">Builds</a><a href="#work">Work</a><a href="#writing">Writing</a><a href="#about">About</a><a href="/assets/pdf/chae-kim-resume.pdf">Resume</a>
    </nav>
    <div class="foot__cta">
      <b>Let's chat.</b>
      <a data-user="chaewoonkim" data-domain="berkeley.edu" data-show href="#">chaewoonkim@berkeley.edu</a>
      <div class="foot__small">
        <span><a href="/projects/portfolio">Built by hand in plain HTML</a>, between latte art attempts.</span>
        <div class="changelog" aria-labelledby="changelog-h">
          <p class="changelog__k" id="changelog-h">Latest changes to this site</p>
          <ul>%%CHANGELOG%%</ul>
          <a href="https://github.com/chaekim96/chaekim-portfolio/commits/main" target="_blank" rel="noopener">All changes ↗</a>
        </div>
      </div>
    </div>
  </footer>

%%LIVE_DIALOG%%
  <script src="/assets/js/main.js?v=%%V%%"></script>
  <script src="/assets/js/play.js?v=%%V%%" defer></script>
%%PALETTE_SCRIPT%%
%%LIVE_SCRIPT%%
  <script>
  (function () {
    var THESIS = {
      'builds': 'I like to build things, from startups to card games.',
      'work': 'I run the operations behind the idea.',
      'writing': 'Essays, how I decide, and what I read.',
      'about': 'Product, strategy, operations, and the occasional 3D print.'
    };
    var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
    var tabs = [].slice.call(document.querySelectorAll('.tab'));
    var panels = [].slice.call(document.querySelectorAll('.panel'));
    var thesis = document.querySelector('.thesis');
    var current = null;

    function show(id, opts) {
      opts = opts || {};
      if (!THESIS[id]) id = 'builds';
      tabs.forEach(function (t) {
        var on = t.dataset.tab === id;
        t.setAttribute('aria-selected', on);
        t.tabIndex = on ? 0 : -1;
        if (on && opts.focus) t.focus();
      });
      panels.forEach(function (p) { p.hidden = p.id !== id; });
      if (current && current !== id && !reduce) {
        thesis.classList.add('is-swapping');
        setTimeout(function () { thesis.textContent = THESIS[id]; thesis.classList.remove('is-swapping'); }, 180);
      } else {
        thesis.textContent = THESIS[id];
      }
      current = id;
      if (opts.scroll) document.querySelector('.tabs').scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
    }
    function go(id, opts) { show(id, opts); history.replaceState(null, '', '#' + id); }

    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { go(t.dataset.tab); });
      t.addEventListener('keydown', function (e) {
        var j = { ArrowRight: (i + 1) % tabs.length, ArrowLeft: (i - 1 + tabs.length) % tabs.length, Home: 0, End: tabs.length - 1 }[e.key];
        if (j === undefined) return;
        e.preventDefault(); go(tabs[j].dataset.tab, { focus: true });
      });
    });

    // in-page links to a tab (footer, seal) switch tabs instead of jumping
    document.addEventListener('click', function (e) {
      var a = e.target.closest('a[href^="#"]');
      if (!a) return;
      var id = a.getAttribute('href').slice(1);
      if (THESIS[id]) { e.preventDefault(); go(id, { scroll: true }); }
    });

    // Builds folders: one open at a time. The open tray moves into the folder grid right after
    // the row holding its folder, so on a phone it opens under the folder you tapped.
    // Without JS every tray stays visible below the folders and the folder links jump to it.
    var folds = [].slice.call(document.querySelectorAll('.fold'));
    var trays = [].slice.call(document.querySelectorAll('.tray'));
    var shelf = document.querySelector('.folders');
    function placeTray(tray) {
      var cols = getComputedStyle(shelf).gridTemplateColumns.split(' ').length || 1;
      var i = folds.findIndex(function (f) { return f.dataset.folder === tray.id; });
      var last = folds[Math.min(Math.ceil((i + 1) / cols) * cols, folds.length) - 1];
      if (last.nextElementSibling !== tray) last.after(tray);
    }
    function openFolder(id, opts) {
      opts = opts || {};
      var tray = null, fold = null;
      trays.forEach(function (t) { t.classList.remove('is-open'); if (t.id === id) tray = t; });
      folds.forEach(function (f) { var on = f.dataset.folder === id; f.setAttribute('aria-expanded', String(on)); if (on) fold = f; });
      if (!tray) return;
      placeTray(tray);
      tray.classList.add('is-open');
      // Bring the folder to the top of the screen when its tray would start low or off screen.
      if (opts.scroll) requestAnimationFrame(function () {
        var r = fold.getBoundingClientRect(), t = tray.getBoundingClientRect();
        if (r.top < 0 || t.top > innerHeight * 0.6) scrollTo({ top: scrollY + r.top - 80, behavior: reduce ? 'auto' : 'smooth' });
      });
    }
    // Column count changes with the screen width, so re-place the open tray on resize.
    var resizing = 0;
    addEventListener('resize', function () {
      cancelAnimationFrame(resizing);
      resizing = requestAnimationFrame(function () { var t = document.querySelector('.tray.is-open'); if (t) placeTray(t); });
    });
    folds.forEach(function (f) {
      f.addEventListener('click', function (e) {
        e.preventDefault();
        var id = f.getAttribute('aria-expanded') === 'true' ? null : f.dataset.folder;
        openFolder(id, { scroll: true });
        history.replaceState(null, '', '#' + (id || 'builds'));
      });
    });
    document.querySelectorAll('[data-fold-close]').forEach(function (a) {
      a.addEventListener('click', function (e) {
        e.preventDefault(); e.stopPropagation();
        var id = a.closest('.tray').id;
        openFolder(null);
        history.replaceState(null, '', '#builds');
        var f = document.querySelector('.fold[data-folder="' + id + '"]');
        if (f) f.focus({ preventScroll: true });
      });
    });

    // deep links: #builds (default), #work, #about, a Builds folder such as #mods, or a section inside About such as #experience
    function fromHash() {
      var h = location.hash.slice(1);
      if (h === 'contact') h = 'elsewhere'; // old desktop-page links
      var el = h && document.getElementById(h);
      if (THESIS[h]) show(h);
      else if (el && el.classList.contains('tray')) { show('builds'); openFolder(h, { scroll: true }); }
      else if (el && el.closest('#about')) { show('about'); requestAnimationFrame(function () { el.scrollIntoView(); }); }
      else show('builds');
    }
    addEventListener('hashchange', fromHash);
    fromHash();

    // local time in Berkeley, with a sun or a moon
    var clock = document.getElementById('clock'), icon = document.getElementById('clock-icon');
    var fmt = new Intl.DateTimeFormat('en-US', { hour: 'numeric', minute: '2-digit', timeZone: 'America/Los_Angeles' });
    var hr = new Intl.DateTimeFormat('en-US', { hour: 'numeric', hourCycle: 'h23', timeZone: 'America/Los_Angeles' });
    function tick() {
      var d = new Date(), h = parseInt(hr.format(d), 10);
      clock.textContent = fmt.format(d);
      clock.dateTime = d.toISOString();
      icon.dataset.night = String(h < 6 || h >= 19);
    }
    tick(); setInterval(tick, 30000);

    // About: highlight the section in view
    var links = [].slice.call(document.querySelectorAll('.toc a'));
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (en) {
          if (!en.isIntersecting) return;
          links.forEach(function (a) { a.classList.toggle('is-active', a.getAttribute('href') === '#' + en.target.id); });
        });
      }, { rootMargin: '-15% 0px -70% 0px' });
      links.forEach(function (a) { var s = document.querySelector(a.getAttribute('href')); if (s) io.observe(s); });
    }
  })();
  </script>
  <script>
    // "Let's chat" copy button: copies the address main.js assembled
    document.querySelectorAll('[data-copy-email]').forEach(function (b) {
      b.addEventListener('click', function () {
        var a = b.parentElement.querySelector('[data-user][data-domain]'), addr = a.dataset.user + '@' + a.dataset.domain;
        if (!navigator.clipboard) return;
        navigator.clipboard.writeText(addr).then(function () { b.textContent = 'Copied'; setTimeout(function () { b.textContent = 'Copy'; }, 1600); });
      });
    });
  </script>
  <script defer src="/_vercel/insights/script.js"></script>
</body>
</html>
"""

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
STAMP = (STAMP.replace("%%WRITING_ESSAYS%%", _writing_essays())
              .replace("%%WRITING_READING%%", _writing_reading())
              .replace("%%SIGNAL_CSS%%", SIGNAL_CSS).replace("%%GLASS_JS%%", GLASS_JS)
              .replace("%%V%%", V)
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
    mark = build_mark(m.group(2), "pill__mark", 18) or work_mark(m.group(2), "pill__mark", 18)
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

ARCADE_ICONS = build_icons("arcade", "https://chaekim-portfolio.vercel.app")

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
  <link rel="canonical" href="https://chaekim-portfolio.vercel.app/arcade">
{ARCADE_ICONS[0]}
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{CASE_HEAD_ASSETS}
  <link rel="stylesheet" href="/assets/css/arcade.css?v=1">
</head>
<body class="v v-stamp case sec-builds">
  <a class="skip" href="#main">Skip to content</a>
{CASE_TOP}

  <main id="main">
{ARCADE_SWITCHER}
    <section class="case-hero wrap">
      <a class="case-hero__back" href="/#builds">← All builds</a>
      {build_mark("arcade", "case-hero__mark", 56)}
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

# ----------------------------------------------------------------------------
# /projects/portfolio: how this site was made. Decisions come from the git
# history; backlog status from the Oct 8 backlog. Keep it true: no invented
# reasons, and done items stay listed.
# ----------------------------------------------------------------------------

def _decision(when, title, why=""):
    return (when, title, why)

def _month_cards(items):
    """Decisions grouped by month, one tint per month, titles first; tap a title for the why."""
    months = [("Sep", "September 2026", "sky"), ("Oct", "October 2026", "violet")]
    out = []
    for prefix, label, hue in months:
        group = [d for d in items if d[0].startswith(prefix)]
        rows = "\n".join(
            f'            <li><details><summary><time>{when}</time><b>{title}</b></summary><p>{why}</p></details></li>'
            for when, title, why in group)
        out.append(
            f'        <div class="mgroup mgroup--{hue}">\n'
            f'          <p class="mgroup__k"><i aria-hidden="true"></i>{label} · {len(group)} decisions</p>\n'
            f'          <ol class="mlog">\n{rows}\n          </ol>\n'
            f'        </div>')
    return '      <div class="mgroups">\n' + "\n".join(out) + "\n      </div>"

DECISIONS = _month_cards([
    _decision("Sep 15", "Start from plain HTML.",
              "Hosted on Vercel, with no framework to maintain. Version one was a homepage and seven case studies."),
    _decision("Sep 16", "A wordmark instead of a symbol.",
              "I drew eight logo directions as SVGs on one page and picked a plain wordmark."),
    _decision("Sep 16", "Put games on the site, but make them free until played.",
              "Snake, Galaga and a generative lo-fi radio, loaded only when someone scrolls to them or presses play."),
    _decision("Sep 16", "Every case study from one template.",
              "A small script writes each project page from structured content, so every page has the same shape: the problem, what I did, results, what I'd do differently, artifacts. Anything I hadn't confirmed was tagged in the copy instead of guessed."),
    _decision("Sep 20", "One system, a macOS desktop.",
              "Folders and windows across the whole site, inspired by renee.wiki. I also cut the thin pages."),
    _decision("Sep 21", "Try other framings as real pages.",
              "A product requirements doc, a field notebook and an engineering schematic, each a working homepage rather than a mockup."),
    _decision("Sep 27", "An Apple design pass, but keep my font.",
              "Semantic colors, an 8-point grid and calmer glass. I kept Poppins instead of switching to the system font."),
    _decision("Oct 1", "Launch the desktop.",
              "Unconfirmed details were hidden from visitors rather than shown with placeholder text."),
    _decision("Oct 4", "A quieter direction: Stamp.",
              "Gallery-like and artifact-first, inspired by liumichelle.com. Real screenshots instead of descriptions."),
    _decision("Oct 6", "Headlines say the problem, not a number.",
              "Each project's title says what it solves. The figures moved into the supporting line, and every number now matches my resume. The resume itself is now generated from one source file."),
    _decision("Oct 8", "Write the brief, then cut everything that didn't fit it.",
              "The site is for anyone curious, not a job application. I removed the role-seeking lines, replaced my red name seal with my name brushed in black ink, and added a Builds tab for the tools I make."),
    _decision("Oct 9", "Two more brand finalists.",
              "Ink, monochrome with a brush wordmark, and Desktop Craft, Apple-style polish. Both were built as live pages."),
    _decision("Oct 11", "Every build gets its own story and a screenshot of it in use.",
              "If the work is the evidence, a thumbnail isn't enough. Each tool got a case page and a capture of it actually running."),
    _decision("Oct 11", "Stamp becomes the homepage.",
              "The project pages were restyled to match, so clicking a card no longer drops you into another design."),
    _decision("Oct 11", "Let an AI reviewer read the code that builds this site.",
              "My Code Improver subagent reviewed the page generator. Its top finding was real: a template page was publicly reachable. I fixed that and the other thirteen findings."),
    _decision("Oct 12", "One design, and the tools run live.",
              "I retired every other design. Web apps on the Builds tab now open live in the page, the background got a soft gradient, and the games moved to their own arcade page."),
    _decision("Oct 20", "Builds first, then Work.",
              "I want people to see what I've built first. Builds now opens by default, led by the four apps you can try live."),
])

def _item(text, status=""):
    chip = {"done": '<span class="chip chip--done">Done</span>', "open": '<span class="chip">Open</span>', "idea": '<span class="chip chip--idea">Idea</span>'}.get(status, "")
    return f"          <li>{chip}<span>{text}</span></li>"

BACKLOG_DONE = "\n".join(_item(t, "done") for t in [
    "Pick one direction and retire the rest. <em>Oct 12</em>",
    "A case page for every build, not just a thumbnail. <em>Oct 11</em>",
    "Real screenshots of every tool in use. <em>Oct 11</em>",
    "Answer or cut every unconfirmed detail on the live pages. <em>Oct 11</em>",
    "Consolidate five layers of stylesheet into one design. <em>Oct 12</em>",
    "Publish the case study on choosing this brand. <em>Oct 14</em>",
])
BACKLOG_OPEN = "\n".join(_item(t, "open") for t in [
    "Analytics on every page, counting \"Let's chat\" clicks. That's the one number this site should move.",
    "Real artifacts for the EY and Tritooling case studies.",
    "Brush 김채운 by hand and scan it in, instead of using a font.",
    "A link preview that shows the work, not statistics.",
    "A custom domain.",
    "Self-host Poppins, the last request that blocks the first paint.",
])
CONSIDERING = "\n".join(_item(t, "idea") for t in [
    "A bookshelf: what I'm reading and what stuck.",
    "\"How I work\" principles in About.",
    "An excerpt from my memoir, <i>The Treaded Path</i>, and a list of my Medium essays.",
    "One testimonial from someone I've built with.",
    "Playable cards: a mini TypeRace or Snake right in the grid.",
])
CONSIDERING_DONE = "\n".join(_item(t, "done") for t in [
    "A public changelog. It's in the homepage footer now, built from the site's commits. <em>Nov 4</em>",
])

PORTFOLIO_PAGE = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>This portfolio · Chae Kim - Portfolio</title>
  <meta name="description" content="How I built this portfolio like a product: where it started, the decisions that shaped it, what's on the backlog, and what I'm considering next.">
  <meta property="og:title" content="This portfolio · Chae Kim - Portfolio">
  <meta property="og:description" content="How I built this portfolio like a product: where it started, the decisions that shaped it, what's on the backlog, and what I'm considering next.">
  <meta property="og:type" content="article">
  <meta property="og:image" content="https://chaekim-portfolio.vercel.app/assets/img/og-sky.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <link rel="canonical" href="https://chaekim-portfolio.vercel.app/projects/portfolio">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{CASE_HEAD_ASSETS}
</head>
<body class="v v-stamp case sec-builds">
  <a class="skip" href="#main">Skip to content</a>
{CASE_TOP}

  <main id="main">
    <section class="case-hero wrap">
      <a class="case-hero__back" href="/#builds">← All builds</a>
      <p class="eyebrow">this site · solo build · 2026</p>
      <h1 class="case-hero__title">Building my portfolio like a product.</h1>
      <p class="tldr">Where this site started, the decisions that shaped it, what's still on the backlog, and what I'm considering next. Every decision below is in the site's history.</p>
      <p class="meta-line"><b>Role</b> Designer and builder · <b>Team</b> Solo, built with Claude Code · <b>Timeline</b> September 2026 to now</p>
    </section>

    <section class="wrap case-cover-wrap">
      <div class="stage case-cover" style="--g: var(--g-lucent)"><img src="/assets/img/builds/portfolio.jpg" alt="This site's homepage: my name brushed in ink, a one-line intro, and Work, Builds and About tabs" width="1600" height="1000"></div>
    </section>

    <section class="wrap case-body">
      <nav class="toc" aria-label="On this page">
        <a href="#brief">The brief</a>
        <a href="#start">Where it started</a>
        <a href="#decisions">Decisions</a>
        <a href="#backlog">Backlog</a>
        <a href="#considering">Considering</a>
      </nav>
      <article class="prose">
        <h2 id="brief">The brief</h2>
        <p>I treat this site as a product with one user and one job.</p>
        <ul>
          <li><b>User:</b> anyone curious about who I am, not only recruiters.</li>
          <li><b>Job:</b> answer "who is this person, and what do they make?"</li>
          <li><b>Proof:</b> craft. The work is the evidence: live tools, real screenshots, case studies.</li>
          <li><b>Conversion:</b> a conversation. Every page ends with "Let's chat."</li>
        </ul>
        <p>That brief came on October 8. Most of what happened before it was finding it.</p>

        <h2 id="start">Where it started</h2>
        <p>On September 15, 2026, I rebuilt my 2021 Indiana University portfolio and a Notion page into one static site. It has no framework and no build step: hand-written HTML and CSS, with small scripts that generate the repetitive pages.</p>

        <h2 id="decisions">Decisions</h2>
        <p>Grouped by month. Tap a decision to see why, or <a href="/projects/decisions">see every option I weighed</a>.</p>
{DECISIONS}

        <h2 id="backlog">Backlog</h2>
        <p>From the backlog I wrote on October 8. Done items stay on the list, so it stays honest.</p>
        <ul class="backlog">
{BACKLOG_DONE}
{BACKLOG_OPEN}
        </ul>

        <h2 id="considering">Considering</h2>
        <p>Ideas I haven't committed to yet.</p>
        <ul class="backlog">
{CONSIDERING_DONE}
{CONSIDERING}
        </ul>
        <p class="updated">Last updated November 4, 2026.</p>
      </article>
    </section>
  </main>

{CASE_FOOT}
{CASE_SCRIPTS}
</body>
</html>
"""

for name, page in (("index.html", STAMP), ("arcade.html", ARCADE_PAGE), ("projects/portfolio.html", PORTFOLIO_PAGE)):
    with open(os.path.join(ROOT, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(nb_headlines(page))
    print("wrote", name)
