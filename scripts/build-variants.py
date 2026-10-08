#!/usr/bin/env python3
"""Builds the three alternate homepage metaphors under /variants.

Usage:  python3 scripts/build-variants.py
Output: variants/index.html (picker), variants/prd.html, variants/notebook.html, variants/schematic.html
Each page reuses assets/css/style.css for shared components and layers a variant stylesheet on top.
Content is identical to index.html; only the framing metaphor changes.
"""
import os

ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "variants")
V = "13"
TODAY = "2026-09-21"

# ----------------------------------------------------------------------------
# shared fragments
# ----------------------------------------------------------------------------

def head(slug, title, desc, fonts):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} · Chae Kim</title>
  <meta name="description" content="{desc}">
  <meta name="robots" content="noindex">
  <meta property="og:title" content="{title} · Chae Kim">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="website">
  <meta property="og:image" content="https://chaekim-portfolio.vercel.app/assets/img/og.png">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800{fonts}&display=swap">
  <link rel="preload" as="image" href="/assets/img/memoji.png">
  <link rel="stylesheet" href="/assets/css/style.css?v={V}">
  <link rel="stylesheet" href="/assets/css/v-{slug}.css?v={V}">
  <script>try {{ var t = localStorage.getItem('ck-theme'); if (t) document.documentElement.setAttribute('data-theme', t); }} catch (e) {{}}</script>
</head>
<body class="v v-{slug}">
  <a class="skip" href="#main">Skip to content</a>
"""

NAV = """  <header class="nav">
    <div class="container nav__inner">
      <a href="/" class="brand wordmark" aria-label="Chae Kim, home">chae<span class="wordmark__dot"></span></a>
      <button class="nav__burger" aria-label="Open menu" aria-expanded="false">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
      </button>
      <nav class="nav__links" aria-label="Primary">
        <a href="#work">Work</a>
        <a href="#experience">Experience</a>
        <a href="#about">About</a>
        <a href="/assets/pdf/chae-kim-resume.pdf">Resume</a>
        <a href="#contact">Contact</a>
        <button class="theme-toggle" type="button" aria-label="Toggle dark mode">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>
        </button>
        <a class="nav__cta" href="https://www.linkedin.com/in/chaekim/" target="_blank" rel="noopener">LinkedIn</a>
      </nav>
    </div>
  </header>
"""

def switcher(current):
    opts = [("desktop", "/"), ("prd", "/variants/prd"), ("notebook", "/variants/notebook"), ("schematic", "/variants/schematic"), ("stamp", "/variants/stamp")]
    links = "".join(f'<a href="{h}"{" class=is-active aria-current=page" if k == current else ""}>{k}</a>' for k, h in opts)
    return f'  <nav class="switch" aria-label="Design variants"><span>design</span>{links}</nav>\n'

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

EARLIER_LINKS = """            <a href="/projects/iu-study-assistant"><img class="e" src="/assets/img/thumbs/iusa.jpg" alt="" loading="lazy"><span>IU Study Assistant<span>Capstone · PM, UX, back end</span></span></a>
            <a href="/projects/alab"><img class="e" src="/assets/img/thumbs/alab.jpg" alt="" loading="lazy"><span>aLab<span>Adjustable dog bowl + app</span></span></a>
            <a href="/projects/luc"><img class="e" src="/assets/img/thumbs/luc.jpg" alt="" loading="lazy"><span>LUC<span>Self-weighing luggage</span></span></a>
            <a href="/projects/ptm"><img class="e" src="/assets/img/thumbs/ptm.jpg" alt="" loading="lazy"><span>PTM<span>Fever-sensing sleep mask</span></span></a>
            <a href="/projects/coursera"><img class="e" src="/assets/img/thumbs/coursera.jpg" alt="" loading="lazy"><span>Re-envisioning Coursera<span>PM dossier</span></span></a>
"""

TILES = """
            <a class="tile" href="https://tally-lake-seven.vercel.app" target="_blank" rel="noopener"><span class="tile__icon">🧾</span><span><span class="tile__title">Tally ↗</span><span class="tile__meta">To-do lists with a Claude time estimate on every line</span></span></a>
            <a class="tile" href="https://color-palette-generator-three-sand.vercel.app" target="_blank" rel="noopener"><span class="tile__icon">🎨</span><span><span class="tile__title">Palette Generator ↗</span><span class="tile__meta">Brand colors and fonts for founders who aren't designers</span></span></a>
            <a class="tile" href="https://typerace.typerace.workers.dev" target="_blank" rel="noopener"><span class="tile__icon">⌨️</span><span><span class="tile__title">TypeRace ↗</span><span class="tile__meta">Live typing races with classmates, no sign-up</span></span></a>
            <a class="tile" href="https://networking-tracker-five-sage.vercel.app" target="_blank" rel="noopener"><span class="tile__icon">🗂️</span><span><span class="tile__title">Networking Tracker ↗</span><span class="tile__meta">Coffee chats tracked privately, with row-level security</span></span></a>
            <a class="tile" href="https://github.com/chaekim96/VoicePrompter" target="_blank" rel="noopener"><span class="tile__icon">🎙️</span><span><span class="tile__title">VoicePrompter ↗</span><span class="tile__meta">A macOS teleprompter that hides from screen share</span></span></a>
            <div class="tile"><span class="tile__icon">🧭</span><span><span class="tile__title">SmartModel</span><span class="tile__meta">Claude Code mod: routes each prompt to the right model</span></span></div>
            <div class="tile"><span class="tile__icon">⛽</span><span><span class="tile__title">Token-Fuel</span><span class="tile__meta">Claude Code mod: a context gauge for Claude Code and Codex</span></span></div>
            <div class="tile"><span class="tile__icon">🔍</span><span><span class="tile__title">Code Improver</span><span class="tile__meta">Claude Code mod: a subagent that reviews every file I change</span></span></div>
            <a class="tile" href="https://github.com/chaekim96/personal-wiki" target="_blank" rel="noopener"><span class="tile__icon">📚</span><span><span class="tile__title">Personal Wiki ↗</span><span class="tile__meta">Ask my own notes questions, fully offline</span></span></a>
            <a class="tile" href="https://github.com/chaekim96/pacman-dqn" target="_blank" rel="noopener"><span class="tile__icon">👾</span><span><span class="tile__title">Pac-Man DQN ↗</span><span class="tile__meta">An agent that learned Ms. Pac-Man by trial and error</span></span></a>
            <a class="tile" href="https://github.com/chaekim96/custom-llm" target="_blank" rel="noopener"><span class="tile__icon">🧠</span><span><span class="tile__title">Custom LLM ↗</span><span class="tile__meta">A tiny language model trained on a laptop CPU</span></span></a>
            <a class="tile" href="/projects/home-gif"><span class="tile__icon">🏠</span><span><span class="tile__title">Home (during COVID)</span><span class="tile__meta">Pixel-art GIF · 2020</span></span></a>
            <a class="tile" href="/projects/yin-yang"><span class="tile__icon">☯️</span><span><span class="tile__title">Yin Yang in Motion</span><span class="tile__meta">Animated illustration · 2020</span></span></a>
            <a class="tile" href="/assets/pdf/WMCS-Weight-Machine-Cross-Sync.pdf" target="_blank" rel="noopener"><span class="tile__icon">🏋️</span><span><span class="tile__title">WMCS ↗</span><span class="tile__meta">Gym sets over NFC · PDF · 2019</span></span></a>
            <a class="tile" href="/assets/pdf/AAV-Auto-Adjusting-Volume.pdf" target="_blank" rel="noopener"><span class="tile__icon">🔊</span><span><span class="tile__title">AAV ↗</span><span class="tile__meta">Noise-aware volume · PDF · 2019</span></span></a>
            <a class="tile" href="/assets/pdf/I308-Lime-Scooter-Poster.pdf" target="_blank" rel="noopener"><span class="tile__icon">🛴</span><span><span class="tile__title">Fake News poster ↗</span><span class="tile__meta">Media literacy · 2020</span></span></a>
            <div class="tile"><span class="tile__icon">🖨️</span><span><span class="tile__title">3D prints</span><span class="tile__meta">Keychains, organizers, containers</span></span></div>
"""

POLAROIDS = """            <figure class="polaroid"><img src="/assets/img/profile.jpg" alt="Chae waving next to an elephant in Phuket" loading="lazy" width="1200" height="1600"><figcaption>phuket.jpg</figcaption></figure>
            <figure class="polaroid"><img src="/assets/img/travel-1.jpg" alt="A pink coconut by a pool in Bali" loading="lazy" width="900" height="1200"><figcaption>bali.jpg</figcaption></figure>
            <figure class="polaroid"><img src="/assets/img/travel-3.jpg" alt="Limestone cliffs over green water" loading="lazy" width="900" height="1200"><figcaption>ha-long-bay.jpg</figcaption></figure>
            <figure class="polaroid"><img src="/assets/img/travel-2.jpg" alt="Boat at sunset" loading="lazy" width="900" height="1200"><figcaption>golden-hour.jpg</figcaption></figure>
"""

CONTACT_LINKS = """            <a class="btn btn--primary" data-user="chaewoonkim" data-domain="berkeley.edu" data-show href="#">Email</a>
            <a class="btn btn--ghost" href="https://www.linkedin.com/in/chaekim/" target="_blank" rel="noopener">LinkedIn</a>
            <a class="btn btn--ghost" href="https://medium.com/@chaewoonkim" target="_blank" rel="noopener">Medium</a>
            <a class="btn btn--ghost" href="/assets/pdf/chae-kim-resume.pdf">Resume (PDF)</a>
"""

EMAIL = '<a class="em" data-user="chaewoonkim" data-domain="berkeley.edu" data-show href="#">chaewoonkim@berkeley.edu</a>'
MEDIUM = '<a class="em" href="https://medium.com/@chaewoonkim" target="_blank" rel="noopener">Medium ↗</a>'
CONFIRM_IU = '<span class="confirm">[CONFIRM: start year]</span>'

def tail(current):
    return f"""{switcher(current)}  <script src="/assets/js/main.js?v={V}"></script>
  <script defer src="/_vercel/insights/script.js"></script>
</body>
</html>
"""

# ----------------------------------------------------------------------------
# 1) PRD — the portfolio as a product requirements document
# ----------------------------------------------------------------------------

PRD = head("prd", "PRD", "Chae Kim, specified as a product requirements document. MBA at Berkeley Haas, co-founded Lucent, ex-EY AI & Data. I like to build things.", "&family=JetBrains+Mono:wght@400;500;600") + NAV + f"""
  <main id="main" class="doc">
    <div class="container doc__grid">
      <aside class="doc__toc" aria-label="Contents">
        <p class="toc__label">Contents</p>
        <ol>
          <li><a href="#tldr">TL;DR</a></li>
          <li><a href="#problem">Problem statement</a></li>
          <li><a href="#goals">Goals and non-goals</a></li>
          <li><a href="#work">Requirements</a></li>
          <li><a href="#more">Additional scope</a></li>
          <li><a href="#experience">Milestones</a></li>
          <li><a href="#playground">Appendix A: side quests</a></li>
          <li><a href="#break">Appendix B: arcade</a></li>
          <li><a href="#about">Open questions</a></li>
          <li><a href="#contact">Sign-off</a></li>
        </ol>
      </aside>

      <article class="doc__body">
        <header class="doc__head">
          <p class="doc__kicker"><span class="mono">PRD-0001</span> · Product requirements document</p>
          <h1 class="doc__title" data-stagger>Chae Kim</h1>
          <p class="doc__sub">A product manager, written up like a product.</p>
          <dl class="meta">
            <div><dt>Status</dt><dd><span class="pill pill--live"><i></i>Building, and up for a chat</span></dd></div>
            <div><dt>Owner</dt><dd><img class="avatar" src="/assets/img/memoji.png" alt="">Chae Kim</dd></div>
            <div><dt>Version</dt><dd class="mono">2.0</dd></div>
            <div><dt>Last updated</dt><dd class="mono">{TODAY}</dd></div>
            <div><dt>Reviewer</dt><dd>You, hopefully</dd></div>
            <div><dt>Location</dt><dd>Berkeley, CA</dd></div>
          </dl>
        </header>

        <section class="sec" id="tldr">
          <h2><span class="num">0</span>TL;DR</h2>
          <div class="callout callout--accent tldr-box reveal">
            <p class="tldr">Hi, I'm Chae. I turn messy problems into <span class="mark">products and plans that ship</span>.</p>
            <p>MBA at Berkeley Haas ('27). Co-founder of Lucent. Ex-EY AI &amp; Data.</p>
            <ul class="checks">
              <li>Founded an NSF I-Corps AI startup</li>
              <li>Led Fortune 500 cloud programs</li>
              <li>Ran a precision manufacturer's operations</li>
            </ul>
            <div class="actions">
              <a class="btn btn--primary" href="#work">Read the requirements</a>
              <a class="btn btn--ghost" href="/assets/pdf/chae-kim-resume.pdf" download="Chae-Kim-Resume.pdf">Download resume</a>
            </div>
          </div>
        </section>

        <section class="sec" id="problem">
          <h2><span class="num">1</span>Problem statement</h2>
          <p class="reveal">Cross-functional work stalls when nobody owns the plan. Teams have more ideas than shipped outcomes, and the gap is usually a person who can write the doc, get alignment, and follow through.</p>
          <p class="reveal"><strong>Proposed solution:</strong> me. I've done this in a seed-stage startup, a Fortune 500 program, and on a factory floor. For roles or collabs, email {EMAIL}. I also write on {MEDIUM}.</p>
        </section>

        <section class="sec" id="goals">
          <h2><span class="num">2</span>Goals and non-goals</h2>
          <div class="two reveal">
            <div class="box">
              <h3 class="box__t">Goals</h3>
              <ul class="checks">
                <li>Ship products people pay for</li>
                <li>Turn strategy into a plan with owners and dates</li>
                <li>Bring AI into real workflows, not demos</li>
              </ul>
            </div>
            <div class="box box--no">
              <h3 class="box__t">Non-goals</h3>
              <ul class="checks checks--no">
                <li>Decks nobody reads</li>
                <li>Roadmaps without customers</li>
                <li>Meetings that could have been a doc</li>
              </ul>
            </div>
          </div>
        </section>

        <section class="sec" id="work">
          <h2><span class="num">3</span>Requirements</h2>
          <p class="sec__sub">Featured work. Each row is a requirement I've already met, with the acceptance criteria that proved it.</p>
          <div class="reqs">
            <div class="req__head" aria-hidden="true"><span>ID</span><span>Priority</span><span>Requirement</span><span>Acceptance criteria</span></div>
            <a class="req reveal" href="/projects/lucent">
              <span class="req__id mono">REQ-01</span>
              <span class="req__pri"><span class="pill pill--p0">P0</span><span class="pill pill--done">Shipped</span></span>
              <span class="req__body">
                <img class="req__thumb" src="/assets/img/thumbs/lucent.jpg" alt="" loading="lazy" width="1200" height="900">
                <span><b>Lucent</b><span class="req__desc">AI search observability platform and consultancy. See how your brand ranks in ChatGPT, Perplexity, and Gemini, then fix it.</span></span>
              </span>
              <span class="req__ac"><b>First paying pilot</b><span>5 LOIs in 30 days</span></span>
            </a>
            <a class="req reveal" href="/projects/ey">
              <span class="req__id mono">REQ-02</span>
              <span class="req__pri"><span class="pill pill--p0">P0</span><span class="pill pill--done">Shipped</span></span>
              <span class="req__body">
                <img class="req__thumb" src="/assets/img/thumbs/ey.jpg" alt="" loading="lazy" width="1200" height="900">
                <span><b>EY, AI &amp; Data</b><span class="req__desc">Risk, OKRs, and the first executive QBR for a $200M+ cloud migration across 25+ teams.</span></span>
              </span>
              <span class="req__ac"><b>$10M+ savings realized</b><span>−30% executive escalations</span></span>
            </a>
            <a class="req reveal" href="/projects/tritooling">
              <span class="req__id mono">REQ-03</span>
              <span class="req__pri"><span class="pill pill--p0">P0</span><span class="pill pill--done">Shipped</span></span>
              <span class="req__body">
                <img class="req__thumb" src="/assets/img/thumbs/tritooling.jpg" alt="" loading="lazy" width="1200" height="900">
                <span><b>Tritooling</b><span class="req__desc">A year running operations at a precision manufacturer serving semiconductor and medical device clients.</span></span>
              </span>
              <span class="req__ac"><b>+15% on-time delivery</b><span>−30% defects</span></span>
            </a>
          </div>
        </section>

        <section class="sec" id="more">
          <h2><span class="num">4</span>Additional scope</h2>
          <div class="reqs">
            <a class="req reveal" href="/projects/mirrorme">
              <span class="req__id mono">REQ-04</span>
              <span class="req__pri"><span class="pill pill--p1">P1</span><span class="pill pill--done">Shipped</span></span>
              <span class="req__body">
                <img class="req__thumb req__thumb--contain" src="/assets/img/projects/mirrorme/card-question.png" alt="" loading="lazy">
                <span><b>MirrorMe</b><span class="req__desc">An icebreaker card game for hosts. 150+ pre-orders with $0 ad spend.</span></span>
              </span>
              <span class="req__ac"><b>150+ pre-orders</b><span>$0 ad spend · 2024</span></span>
            </a>
            <a class="req reveal" href="/projects/mobility">
              <span class="req__id mono">REQ-05</span>
              <span class="req__pri"><span class="pill pill--p1">P1</span><span class="pill pill--wip">In progress</span></span>
              <span class="req__body">
                <img class="req__thumb" src="/assets/img/thumbs/mobility.jpg" alt="" loading="lazy" width="1200" height="900">
                <span><b>Mobility devices for older adults <span class="stealth">Stealth</span></b><span class="req__desc">Working on it now: design-forward mobility products that keep older adults independent longer.</span></span>
              </span>
              <span class="req__ac"><b>GTM and brand</b><span>Co-founder</span></span>
            </a>
          </div>
          <details class="earlier reveal">
            <summary>Deprecated: v1 requirements (Indiana University, 2019 to 2021)</summary>
            <div class="earlier__list">
{EARLIER_LINKS}            </div>
          </details>
        </section>

        <section class="sec" id="experience">
          <h2><span class="num">5</span>Milestones</h2>
          <p class="sec__sub">Results, not duties.</p>
          <table class="ms reveal">
            <thead><tr><th>Date</th><th>Milestone</th><th>Outcome</th></tr></thead>
            <tbody>
              <tr><td class="mono">2025 to 2027</td><td><b>UC Berkeley Haas</b> <span class="pill pill--live"><i></i>Now</span><br><span class="ms__role">MBA Candidate</span></td><td>Merit Scholarship. Co-President, Asian Business Club (300+ members).</td></tr>
              <tr><td class="mono">2025 to 2026</td><td><b>Lucent</b><br><span class="ms__role">Co-founder &amp; CEO</span></td><td>First paying pilot. 5 LOIs in 30 days. 100+ customer interviews. NSF I-Corps backed.</td></tr>
              <tr><td class="mono">Jul 2024 to Jul 2025</td><td><b>Tritooling Precision Corporation, Philippines</b><br><span class="ms__role">Director of Operations</span></td><td>On-time delivery +15%, defects −30%. ERP make-vs-buy case approved, $100K in annual savings. Board approval to launch in Japan, a $300K+ revenue opportunity.</td></tr>
              <tr><td class="mono">Aug 2021 to Jul 2024</td><td><b>EY, New York</b><br><span class="ms__role">Senior Technology Consultant, AI &amp; Data Strategy (Staff Technology Consultant, 2021 to 2023)</span></td><td>Redirected $3M to priority initiatives after launching a Fortune 500 client's first QBR. $10M+ in realized savings over 2 years. −30% escalations on a $200M+ program. 90% tool adoption across 4,000 users.</td></tr>
              <tr><td class="mono">Class of 2021</td><td><b>Indiana University Bloomington</b><br><span class="ms__role">B.S. Informatics, minors in HCI &amp; Entrepreneurship</span></td><td>Dean's List. GPA 3.74. {CONFIRM_IU}</td></tr>
              <tr><td class="mono">2017 to 2019</td><td><b>Republic of Korea Army, Gangwon</b><br><span class="ms__role">Sergeant, 2nd Artillery Brigade</span></td><td>Ran 15 high-stakes artillery operations, leading 10 soldiers and interpreting for ROK and U.S. commanders.</td></tr>
            </tbody>
          </table>
        </section>

        <section class="sec" id="playground">
          <h2><span class="num">A</span>Appendix A: side quests</h2>
          <p class="sec__sub">Weekend builds and early concepts.</p>
          <div class="tiles reveal">
{TILES}          </div>
        </section>

        <section class="sec" id="break">
          <h2><span class="num">B</span>Appendix B: arcade</h2>
          <p class="sec__sub">Games I grew up playing, rebuilt from memory, with a soundtrack. Nothing autoplays. <a href="#about" class="em">Skip →</a></p>
{ARCADE}        </section>

        <section class="sec" id="about">
          <h2><span class="num">6</span>Open questions</h2>
          <div class="two reveal">
            <div class="about__text">
              <p>Thirteen years growing up overseas made me curious by default. I'm happiest making things: a wireframe, a 3D print, a card game.</p>
              <p>I'm also writing a memoir, <em>The Treaded Path</em>, and essays on {MEDIUM}.</p>
              <ul class="qs">
                <li><b>Q:</b> Will the 3D printer ever stop? <span>Status: unresolved. Keychains, organizers, containers.</span></li>
                <li><b>Q:</b> Tennis or latte art? <span>Status: both. Competitively, in one case.</span></li>
                <li><b>Q:</b> Longest-running commitment? <span>Big Brothers Big Sisters mentor, 4+ year match.</span></li>
              </ul>
            </div>
            <div class="polaroids figs" aria-label="Travel photos">
{POLAROIDS}            </div>
          </div>
        </section>

        <section class="sec" id="contact">
          <h2><span class="num">7</span>Sign-off</h2>
          <p class="sec__sub">Building something, or just curious? Let's chat.</p>
          <table class="ms sign reveal">
            <thead><tr><th>Role</th><th>Name</th><th>Status</th></tr></thead>
            <tbody>
              <tr><td>Author</td><td>Chae Kim</td><td><span class="pill pill--done">Signed</span></td></tr>
              <tr><td>Reviewer</td><td>You</td><td><span class="pill pill--wip">Pending</span></td></tr>
            </tbody>
          </table>
          <div class="contact__links reveal">
{CONTACT_LINKS}          </div>
        </section>

        <footer class="doc__foot">
          <p class="mono">Changelog · 2.0 desktop metaphor, case-study template, resume PDF · 1.0 first launch</p>
          <p>© <span data-year>2026</span> Chae Woon Kim · 김채운 · Photos via Unsplash · <a href="https://github.com/chaekim96/chaekim-portfolio" target="_blank" rel="noopener">Source</a></p>
        </footer>
      </article>
    </div>
  </main>
""" + tail("prd")

# ----------------------------------------------------------------------------
# 2) Field notebook — dated entries on ruled paper, taped-in specimens
# ----------------------------------------------------------------------------

def entry(n, date, title, body, id_=None):
    idattr = f' id="{id_}"' if id_ else ""
    return f"""      <section class="entry"{idattr}>
        <header class="entry__head">
          <span class="entry__n hand">Entry {n:02d}</span>
          <h2 class="entry__t">{title}</h2>
          <span class="entry__d hand">{date}</span>
        </header>
{body}      </section>
"""

NOTEBOOK = head("notebook", "Field notebook", "Chae Kim's field notebook: dated entries on products, plans, and things that ship. MBA at Berkeley Haas, co-founder of Lucent, ex-EY AI & Data.", "&family=Caveat:wght@500;600;700") + NAV + f"""
  <main id="main" class="nb">
    <div class="container nb__page">
      <div class="nb__binding" aria-hidden="true"></div>

      <header class="nb__cover">
        <p class="stamp stamp--red">Field notebook</p>
        <h1 class="nb__title" data-stagger>Property of <span class="mark">Chae Kim</span></h1>
        <dl class="nb__meta">
          <div><dt>Subject</dt><dd>products, plans, and things that ship</dd></div>
          <div><dt>Book №</dt><dd class="hand">2</dd></div>
          <div><dt>Started</dt><dd class="hand">{TODAY}</dd></div>
          <div><dt>If found</dt><dd>email {EMAIL}</dd></div>
        </dl>
      </header>

{entry(1, "Sep 21, 2026", "Who is writing this",
f'''        <div class="two">
          <div>
            <p class="lead">Hi, I'm Chae. I turn messy problems into <span class="mark">products and plans that ship</span>.</p>
            <p>MBA at Berkeley Haas ('27). Co-founder of Lucent. Ex-EY AI &amp; Data.</p>
            <p class="hand note">observations so far:</p>
            <ul class="ticks">
              <li>Founded an NSF I-Corps AI startup</li>
              <li>Led Fortune 500 cloud programs</li>
              <li>Ran a precision manufacturer's operations</li>
            </ul>
            <p><strong>I like to build things.</strong> Want to swap ideas? Email {EMAIL}. Essays on {MEDIUM}.</p>
            <div class="actions">
              <a class="btn btn--primary" href="#work">See the experiments</a>
              <a class="btn btn--ghost" href="/assets/pdf/chae-kim-resume.pdf" download="Chae-Kim-Resume.pdf">Download resume</a>
            </div>
          </div>
          <figure class="taped taped--memoji reveal">
            <img src="/assets/img/memoji.png" alt="Chae's memoji, mind blown" width="512" height="512">
            <figcaption class="hand">fig. 1 — the author, mind blown</figcaption>
          </figure>
        </div>
''', "hello")}
{entry(2, "ongoing", "Experiments that worked",
f'''        <p class="hand note">a startup, a Fortune 500 program, a factory floor. all three held up.</p>
        <div class="specimens">
          <a class="specimen reveal" href="/projects/lucent">
            <span class="stamp stamp--green">Shipped</span>
            <span class="specimen__label hand">specimen A</span>
            <img src="/assets/img/thumbs/lucent.jpg" alt="Lucent homepage" loading="lazy" width="1200" height="900">
            <span class="specimen__body">
              <b>Lucent</b>
              <span>AI search observability platform and consultancy. See how your brand ranks in ChatGPT, Perplexity, and Gemini, then fix it.</span>
              <span class="hand result">→ first paying pilot · 5 LOIs in 30 days</span>
            </span>
          </a>
          <a class="specimen reveal" href="/projects/ey">
            <span class="stamp stamp--green">Shipped</span>
            <span class="specimen__label hand">specimen B</span>
            <img src="/assets/img/thumbs/ey.jpg" alt="Earth at night from orbit" loading="lazy" width="1200" height="900">
            <span class="specimen__body">
              <b>EY, AI &amp; Data</b>
              <span>Risk, OKRs, and the first executive QBR for a $200M+ cloud migration across 25+ teams.</span>
              <span class="hand result">→ $10M+ savings realized · −30% escalations</span>
            </span>
          </a>
          <a class="specimen reveal" href="/projects/tritooling">
            <span class="stamp stamp--green">Shipped</span>
            <span class="specimen__label hand">specimen C</span>
            <img src="/assets/img/thumbs/tritooling.jpg" alt="Engineer at a precision machine" loading="lazy" width="1200" height="900">
            <span class="specimen__body">
              <b>Tritooling</b>
              <span>A year running operations at a precision manufacturer serving semiconductor and medical device clients.</span>
              <span class="hand result">→ +15% on-time delivery · −30% defects</span>
            </span>
          </a>
        </div>
''', "work")}
{entry(3, "in the field", "Ongoing experiments",
f'''        <div class="specimens specimens--2">
          <a class="specimen reveal" href="/projects/mirrorme">
            <span class="stamp stamp--green">Shipped</span>
            <span class="specimen__label hand">specimen D · 2024</span>
            <img class="contain" src="/assets/img/projects/mirrorme/card-question.png" alt="MirrorMe question card" loading="lazy">
            <span class="specimen__body">
              <b>MirrorMe</b>
              <span>An icebreaker card game for hosts. 150+ pre-orders with $0 ad spend.</span>
              <span class="hand result">→ co-founder, GTM</span>
            </span>
          </a>
          <a class="specimen reveal" href="/projects/mobility">
            <span class="stamp stamp--amber">In progress</span>
            <span class="specimen__label hand">specimen E · stealth</span>
            <img src="/assets/img/thumbs/mobility.jpg" alt="An older couple walking along a garden path" loading="lazy" width="1200" height="900">
            <span class="specimen__body">
              <b>Mobility devices for older adults</b>
              <span>Working on it now: design-forward mobility products that keep older adults independent longer.</span>
              <span class="hand result">→ co-founder, GTM and brand</span>
            </span>
          </a>
        </div>
        <details class="earlier reveal">
          <summary>Earlier notebooks (Indiana University, 2019 to 2021)</summary>
          <div class="earlier__list">
{EARLIER_LINKS}          </div>
        </details>
''', "more")}
{entry(4, "weekends", "Scraps and side quests",
f'''        <p class="hand note">weekend builds and early concepts. some glued in, some just pinned.</p>
        <div class="tiles reveal">
{TILES}        </div>
''', "playground")}
{entry(5, "recess", "Games I grew up playing",
f'''        <p class="hand note">rebuilt from memory, with a soundtrack. nothing autoplays. <a href="#experience" class="em">skip →</a></p>
{ARCADE}''', "break")}
{entry(6, "log", "Where I've been",
f'''        <p class="hand note">results, not duties.</p>
        <div class="timeline reveal">
          <div class="tl"><div class="tl__when">2025 to 2027</div><div><div class="tl__org">UC Berkeley Haas <span class="tl__now">Now</span></div><div class="tl__role">MBA Candidate</div><ul class="tl__body"><li>Merit Scholarship. Co-President, Asian Business Club (300+ members).</li></ul></div></div>
          <div class="tl"><div class="tl__when">2025 to 2026</div><div><div class="tl__org">Lucent</div><div class="tl__role">Co-founder &amp; CEO</div><ul class="tl__body"><li>First paying pilot. 5 LOIs in 30 days.</li><li>100+ customer interviews. NSF I-Corps backed.</li></ul></div></div>
          <div class="tl"><div class="tl__when">Jul 2024 to Jul 2025</div><div><div class="tl__org">Tritooling Precision Corporation, Philippines</div><div class="tl__role">Director of Operations</div><ul class="tl__body"><li>On-time delivery +15%, defects −30%.</li><li>ERP make-vs-buy case approved, $100K in annual savings. Board approval to launch in Japan, a $300K+ revenue opportunity.</li></ul></div></div>
          <div class="tl"><div class="tl__when">Aug 2021 to Jul 2024</div><div><div class="tl__org">EY, New York</div><div class="tl__role">Senior Technology Consultant, AI &amp; Data Strategy (Staff Technology Consultant, 2021 to 2023)</div><ul class="tl__body"><li>Redirected $3M to priority initiatives after launching a Fortune 500 client's first QBR. $10M+ in realized savings over 2 years.</li><li>−30% escalations on a $200M+ program. 90% tool adoption across 4,000 users.</li></ul></div></div>
          <div class="tl"><div class="tl__when">Class of 2021</div><div><div class="tl__org">Indiana University Bloomington</div><div class="tl__role">B.S. Informatics, minors in HCI &amp; Entrepreneurship</div><ul class="tl__body"><li>Dean's List. GPA 3.74. {CONFIRM_IU}</li></ul></div></div>
          <div class="tl"><div class="tl__when">2017 to 2019</div><div><div class="tl__org">Republic of Korea Army, Gangwon</div><div class="tl__role">Sergeant, 2nd Artillery Brigade</div><ul class="tl__body"><li>Ran 15 high-stakes artillery operations, leading 10 soldiers and interpreting for ROK and U.S. commanders.</li></ul></div></div>
        </div>
''', "experience")}
{entry(7, "off the clock", "Off the clock",
f'''        <div class="two">
          <div class="about__text reveal">
            <p>Thirteen years growing up overseas made me curious by default. I'm happiest making things: a wireframe, a 3D print, a card game.</p>
            <p>I'm also writing a memoir, <em>The Treaded Path</em>, and essays on {MEDIUM}.</p>
            <ul class="ticks">
              <li><b>3D printing</b>, design and prototyping</li>
              <li><b>Competitive tennis</b> and latte art</li>
              <li><b>Big Brothers Big Sisters</b> mentor, 4+ year match</li>
            </ul>
          </div>
          <div class="polaroids reveal" aria-label="Travel photos">
{POLAROIDS}          </div>
        </div>
''', "about")}
{entry(8, "to do", "Write to me",
f'''        <p class="lede">Building something, or just curious? Let's chat.</p>
        <div class="contact__links reveal">
{CONTACT_LINKS}        </div>
''', "contact")}
      <footer class="nb__foot">
        <span>© <span data-year>2026</span> Chae Woon Kim · 김채운</span>
        <span class="hand">p. 8</span>
        <span>Photos via Unsplash · <a href="https://github.com/chaekim96/chaekim-portfolio" target="_blank" rel="noopener">Source</a></span>
      </footer>
    </div>
  </main>
""" + tail("notebook")

# ----------------------------------------------------------------------------
# 3) Schematic — an engineering drawing with parts list, revisions, title block
# ----------------------------------------------------------------------------

def zone(id_, label, title, body):
    return f"""      <section class="zone" id="{id_}">
        <header class="zone__head"><span class="mono zone__label">{label}</span><h2 class="zone__t">{title}</h2></header>
{body}      </section>
"""

SCHEMATIC = head("schematic", "Schematic", "Chae Kim, drawn as an engineering schematic: parts list, revision history, title block. MBA at Berkeley Haas, co-founder of Lucent, ex-EY AI & Data.", "&family=JetBrains+Mono:wght@400;500;600") + NAV + f"""
  <main id="main" class="sheet">
    <div class="container sheet__frame">
      <div class="ruler ruler--x" aria-hidden="true"><span>A</span><span>B</span><span>C</span><span>D</span><span>E</span><span>F</span></div>
      <div class="ruler ruler--y" aria-hidden="true"><span>1</span><span>2</span><span>3</span><span>4</span><span>5</span><span>6</span></div>

      <section class="zone zone--hero" id="hello">
        <header class="zone__head"><span class="mono zone__label">DWG CK-2026-002 · SHEET 1 OF 1</span><h2 class="zone__t">General arrangement</h2></header>
        <div class="ga">
          <figure class="ga__fig reveal">
            <span class="dim dim--w mono"><i></i><em>curiosity, 13 yrs overseas</em><i></i></span>
            <span class="dim dim--h mono"><i></i><em>mind, blown</em><i></i></span>
            <img src="/assets/img/memoji.png" alt="Chae's memoji" width="512" height="512">
            <span class="bal bal--l" style="--x:6%;--y:28%"><b>1</b></span>
            <span class="bal" style="--x:94%;--y:42%"><b>2</b></span>
            <span class="bal bal--l" style="--x:8%;--y:78%"><b>3</b></span>
            <figcaption class="mono">FIG. 1 — CHAE KIM, ISOMETRIC. NOT TO SCALE.</figcaption>
          </figure>
          <div class="ga__notes">
            <h1 class="ga__title" data-stagger>Hi, I'm Chae. I turn messy problems into <span class="mark">products and plans that ship</span>.</h1>
            <ol class="notes">
              <li><span class="bal bal--inline"><b>1</b></span>MBA at Berkeley Haas ('27)</li>
              <li><span class="bal bal--inline"><b>2</b></span>Co-founder of Lucent</li>
              <li><span class="bal bal--inline"><b>3</b></span>Ex-EY AI &amp; Data</li>
            </ol>
            <p class="mono spec">NOTES: UNLESS OTHERWISE SPECIFIED, ALL DIMENSIONS ARE IN OUTCOMES. STATUS: <b>BUILDING. ALWAYS UP FOR A CHAT.</b> CONTACT: {EMAIL}</p>
            <div class="actions">
              <a class="btn btn--primary" href="#work">Parts list</a>
              <a class="btn btn--ghost" href="/assets/pdf/chae-kim-resume.pdf" download="Chae-Kim-Resume.pdf">Download resume</a>
              <a class="btn btn--ghost" href="https://medium.com/@chaewoonkim" target="_blank" rel="noopener">Medium ↗</a>
            </div>
          </div>
        </div>
      </section>

{zone("work", "PARTS LIST · BOM", "Work I'm proudest of",
f'''        <table class="bom reveal">
          <thead><tr><th class="mono">ITEM</th><th class="mono">PART NO.</th><th class="mono">DESCRIPTION</th><th class="mono">RESULT</th><th class="mono">DWG</th></tr></thead>
          <tbody>
            <tr class="bom__row" onclick="location.href='/projects/lucent'">
              <td class="mono">1</td>
              <td><img class="bom__thumb" src="/assets/img/thumbs/lucent.jpg" alt="" loading="lazy" width="1200" height="900"><span class="mono">LCT-01</span></td>
              <td><b>Lucent</b><span>AI search observability platform and consultancy. See how your brand ranks in ChatGPT, Perplexity, and Gemini, then fix it.</span></td>
              <td><b>First paying pilot</b><span>5 LOIs in 30 days</span></td>
              <td><a class="mono dwg" href="/projects/lucent" aria-label="Read the Lucent case study">→</a></td>
            </tr>
            <tr class="bom__row" onclick="location.href='/projects/ey'">
              <td class="mono">2</td>
              <td><img class="bom__thumb" src="/assets/img/thumbs/ey.jpg" alt="" loading="lazy" width="1200" height="900"><span class="mono">EY-02</span></td>
              <td><b>EY, AI &amp; Data</b><span>Risk, OKRs, and the first executive QBR for a $200M+ cloud migration across 25+ teams.</span></td>
              <td><b>$10M+ savings realized</b><span>−30% executive escalations</span></td>
              <td><a class="mono dwg" href="/projects/ey" aria-label="Read the EY case study">→</a></td>
            </tr>
            <tr class="bom__row" onclick="location.href='/projects/tritooling'">
              <td class="mono">3</td>
              <td><img class="bom__thumb" src="/assets/img/thumbs/tritooling.jpg" alt="" loading="lazy" width="1200" height="900"><span class="mono">TRI-03</span></td>
              <td><b>Tritooling</b><span>A year running operations at a precision manufacturer serving semiconductor and medical device clients.</span></td>
              <td><b>+15% on-time delivery</b><span>−30% defects</span></td>
              <td><a class="mono dwg" href="/projects/tritooling" aria-label="Read the Tritooling case study">→</a></td>
            </tr>
          </tbody>
        </table>
''')}
{zone("more", "DETAIL VIEWS", "Also on my desk",
f'''        <div class="details">
          <a class="detail reveal" href="/projects/mirrorme">
            <span class="detail__cap mono">DETAIL B · SCALE 2:1</span>
            <span class="detail__media detail__media--contain"><img src="/assets/img/projects/mirrorme/card-question.png" alt="MirrorMe question card" loading="lazy"></span>
            <span class="detail__body"><b>MirrorMe</b><span>An icebreaker card game for hosts. 150+ pre-orders with $0 ad spend.</span><span class="mono detail__meta">CO-FOUNDER · GTM · 2024</span></span>
          </a>
          <a class="detail reveal" href="/projects/mobility">
            <span class="detail__cap mono">DETAIL C · IN PROGRESS · DO NOT SCALE</span>
            <span class="detail__media"><img src="/assets/img/thumbs/mobility.jpg" alt="An older couple walking along a garden path" loading="lazy" width="1200" height="900"></span>
            <span class="detail__body"><b>Mobility devices for older adults <span class="stealth">Stealth</span></b><span>Working on it now: design-forward mobility products that keep older adults independent longer.</span><span class="mono detail__meta">CO-FOUNDER · GTM &amp; BRAND</span></span>
          </a>
        </div>
        <details class="earlier reveal">
          <summary>Superseded drawings (Indiana University, 2019 to 2021)</summary>
          <div class="earlier__list">
{EARLIER_LINKS}          </div>
        </details>
''')}
{zone("experience", "REVISION HISTORY", "Where I've been",
f'''        <table class="rev reveal">
          <thead><tr><th class="mono">REV</th><th class="mono">DATE</th><th class="mono">DESCRIPTION</th><th class="mono">RESULT</th></tr></thead>
          <tbody>
            <tr><td class="mono">F</td><td class="mono">2025 to 2027</td><td><b>UC Berkeley Haas</b> <span class="tl__now">Now</span><br><span class="role">MBA Candidate</span></td><td>Merit Scholarship. Co-President, Asian Business Club (300+ members).</td></tr>
            <tr><td class="mono">E</td><td class="mono">2025 to 2026</td><td><b>Lucent</b><br><span class="role">Co-founder &amp; CEO</span></td><td>First paying pilot. 5 LOIs in 30 days. 100+ customer interviews. NSF I-Corps backed.</td></tr>
            <tr><td class="mono">D</td><td class="mono">Jul 2024 to Jul 2025</td><td><b>Tritooling Precision Corporation, Philippines</b><br><span class="role">Director of Operations</span></td><td>On-time delivery +15%, defects −30%. ERP make-vs-buy case approved, $100K in annual savings. Board approval to launch in Japan, a $300K+ revenue opportunity.</td></tr>
            <tr><td class="mono">C</td><td class="mono">Aug 2021 to Jul 2024</td><td><b>EY, New York</b><br><span class="role">Senior Technology Consultant, AI &amp; Data Strategy (Staff Technology Consultant, 2021 to 2023)</span></td><td>Redirected $3M to priority initiatives after launching a Fortune 500 client's first QBR. $10M+ in realized savings over 2 years. −30% escalations on a $200M+ program. 90% tool adoption across 4,000 users.</td></tr>
            <tr><td class="mono">B</td><td class="mono">Class of 2021</td><td><b>Indiana University Bloomington</b><br><span class="role">B.S. Informatics, minors in HCI &amp; Entrepreneurship</span></td><td>Dean's List. GPA 3.74. {CONFIRM_IU}</td></tr>
            <tr><td class="mono">A</td><td class="mono">2017 to 2019</td><td><b>Republic of Korea Army, Gangwon</b><br><span class="role">Sergeant, 2nd Artillery Brigade</span></td><td>Ran 15 high-stakes artillery operations, leading 10 soldiers and interpreting for ROK and U.S. commanders.</td></tr>
          </tbody>
        </table>
''')}
{zone("playground", "SPARE PARTS", "Side quests",
f'''        <p class="zone__sub">Weekend builds and early concepts.</p>
        <div class="tiles reveal">
{TILES}        </div>
''')}
{zone("break", "TEST FIXTURE · NOTHING AUTOPLAYS", "Games I grew up playing",
f'''        <p class="zone__sub">Rebuilt from memory, with a soundtrack. <a href="#about" class="em">Skip →</a></p>
{ARCADE}''')}
{zone("about", "SECTION A-A", "Off the clock",
f'''        <div class="two">
          <div class="about__text reveal">
            <p>Thirteen years growing up overseas made me curious by default. I'm happiest making things: a wireframe, a 3D print, a card game.</p>
            <p>I'm also writing a memoir, <em>The Treaded Path</em>, and essays on {MEDIUM}.</p>
            <ul class="notes notes--plain">
              <li><b>3D printing</b>, design and prototyping</li>
              <li><b>Competitive tennis</b> and latte art</li>
              <li><b>Big Brothers Big Sisters</b> mentor, 4+ year match</li>
            </ul>
          </div>
          <div class="polaroids reveal" aria-label="Travel photos">
{POLAROIDS}          </div>
        </div>
''')}
{zone("contact", "APPROVALS", "Say hello",
f'''        <p class="zone__sub">Building something, or just curious? Let's chat.</p>
        <div class="contact__links reveal">
{CONTACT_LINKS}        </div>
''')}
      <footer class="tb" aria-label="Title block">
        <div class="tb__cell tb__cell--wide"><span class="mono">TITLE</span><b>CHAE KIM · PRODUCT AND STRATEGY</b></div>
        <div class="tb__cell"><span class="mono">DRAWN BY</span><b>C. KIM</b></div>
        <div class="tb__cell"><span class="mono">CHECKED BY</span><b class="blank">&nbsp;</b></div>
        <div class="tb__cell"><span class="mono">DATE</span><b class="mono">{TODAY}</b></div>
        <div class="tb__cell"><span class="mono">SCALE</span><b class="mono">NTS</b></div>
        <div class="tb__cell"><span class="mono">REV</span><b class="mono">B</b></div>
        <div class="tb__cell"><span class="mono">DWG NO.</span><b class="mono">CK-2026-002</b></div>
        <div class="tb__cell"><span class="mono">SHEET</span><b class="mono">1 OF 1</b></div>
        <div class="tb__cell tb__cell--wide"><span class="mono">© <span data-year>2026</span> CHAE WOON KIM · 김채운</span><b>Photos via Unsplash · <a href="https://github.com/chaekim96/chaekim-portfolio" target="_blank" rel="noopener">Source</a></b></div>
      </footer>
    </div>
  </main>
""" + tail("schematic")

# ----------------------------------------------------------------------------
# 4) Stamp — quiet, gallery-like, artifact-first. One saturated element: a 도장.
#    Standalone stylesheet (v-stamp.css); does not load style.css.
#    Plain string with %%TOKENS%% rather than an f-string, since the inline JS is brace-heavy.
# ----------------------------------------------------------------------------

STAMP_CHANGELOG = "10-04-26"

# 김채운 brushed in black ink on a strip of hanji (Korean mulberry paper).
# Glyphs are East Sea Dokdo (SIL OFL) outlines, defined once in INK_DEFS and reused,
# so the calligraphy costs no font download. The paper gets a deckled edge and faint fibres.
def seal(cls="", label=True):
    aria = 'role="img" aria-label="김채운, Chae Kim\'s name in Korean calligraphy"' if label else 'aria-hidden="true"'
    return (f'<svg class="cal {cls}" viewBox="0 0 44 104" {aria}>'
            '<rect class="paper" x="1.5" y="1.5" width="41" height="101" rx="1" fill="#fbf8f1" filter="url(#paper)"/>'
            '<use class="ink" href="#cal-glyphs" fill="#161514" filter="url(#ink)"/>'
            '</svg>')

INK_DEFS = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>'
            '<filter id="paper" x="-5%" y="-3%" width="110%" height="106%">'
            '<feTurbulence type="fractalNoise" baseFrequency="0.33" numOctaves="2" seed="3" result="edge"/>'
            '<feDisplacementMap in="SourceGraphic" in2="edge" scale="1.5" xChannelSelector="R" yChannelSelector="G" result="deckle"/>'
            '<feTurbulence type="fractalNoise" baseFrequency="1.4 0.3" numOctaves="2" seed="9" result="fib"/>'
            '<feColorMatrix in="fib" type="matrix" values="0 0 0 0 .55  0 0 0 0 .5  0 0 0 0 .42  .32 0 0 0 -.1" result="fibres"/>'
            '<feComposite in="fibres" in2="deckle" operator="in" result="fibresIn"/>'
            '<feMerge><feMergeNode in="deckle"/><feMergeNode in="fibresIn"/></feMerge>'
            '</filter>'
            '<filter id="ink" x="-6%" y="-6%" width="112%" height="112%">'
            '<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="5" result="n"/>'
            '<feDisplacementMap in="SourceGraphic" in2="n" scale="0.6" xChannelSelector="R" yChannelSelector="G" result="d"/>'
            '<feGaussianBlur in="d" stdDeviation="0.1"/>'
            '</filter>'
            '<g id="cal-glyphs"><path transform="translate(22.8 21.0) rotate(-2.0) scale(0.0310 -0.0310) translate(-274.0 -180.5)" d="M263 -191H261Q258 -191 254 -194Q251 -198 248 -198Q243 -198 235 -194Q227 -189 226 -183Q223 -186 220 -186H218Q218 -185 214 -184Q210 -182 206 -180Q201 -179 198 -178Q194 -176 194 -175Q196 -171 202 -165L200 -160L202 -154V-153Q202 -150 199 -146Q196 -141 193 -136Q190 -131 187 -126Q184 -122 184 -119Q184 -113 188 -113Q189 -113 189 -114L194 -117Q192 -115 193 -112Q194 -110 189 -104H192Q201 -104 202 -92Q202 -81 202 -67Q202 -60 208 -40Q215 -21 215 -6V0H210V1Q210 2 209 2Q208 3 207 5Q207 7 210 13Q213 19 213 21Q212 25 212 30Q212 35 214 38Q215 41 219 48Q223 55 230 68Q236 81 245 106H242Q241 107 241 107Q241 109 243 113Q245 117 250 127Q251 129 252 136Q254 142 256 149Q259 156 262 162Q265 168 269 170L274 167Q273 167 278 168Q282 168 287 170Q298 160 306 155Q314 150 320 146Q325 143 330 138Q334 134 338 125Q336 123 334 116Q333 110 331 103L327 85H329Q332 85 337 86Q342 87 345 87Q364 94 377 98Q390 101 400 104Q409 106 417 110Q425 114 433 122Q436 121 440 121Q445 121 446 123Q448 125 451 128Q454 131 460 133Q467 135 482 135Q484 135 490 134Q496 133 503 130Q510 126 517 120Q524 115 529 106Q526 105 524 98Q521 90 518 81Q516 72 514 63Q513 54 513 50Q514 46 514 39Q514 26 510 13Q505 0 500 -14Q495 -27 490 -40Q486 -52 486 -64Q486 -80 494 -85L491 -88Q485 -90 478 -98Q472 -106 469 -106H468Q466 -106 458 -106Q449 -107 438 -109Q428 -111 417 -114Q406 -117 399 -122Q376 -122 364 -128Q351 -133 343 -133Q342 -132 340 -132Q333 -132 322 -142Q310 -152 303 -152Q303 -152 298 -156Q292 -160 286 -166Q280 -173 274 -184Q269 -194 269 -207H266Q263 -204 263 -200Q263 -196 263 -191ZM131 235V241Q133 245 136 254Q138 262 140 270Q142 279 143 286Q144 293 144 295Q144 297 148 306Q152 315 156 326Q161 336 165 345Q169 354 169 356Q169 361 172 367L175 374V398Q169 398 154 396Q139 393 123 390Q107 387 94 384Q81 382 78 382Q77 381 74 381Q66 381 58 389Q51 397 43 402L31 408L25 414Q25 416 24 419Q23 422 22 425L19 432Q19 435 25 440L31 444Q35 444 45 445Q55 446 66 448Q76 449 85 450Q94 452 96 452Q100 452 116 455Q132 458 150 461Q168 464 184 467Q200 470 205 470Q210 470 216 472Q221 473 225 473Q230 473 248 468Q266 464 283 464L290 444Q288 439 286 430Q283 421 280 412Q278 402 276 393Q273 384 271 380L265 368V362Q260 355 252 336Q244 317 236 296Q228 274 220 255Q213 236 209 229L206 222Q203 216 202 210Q202 205 200 197L197 187V163L179 145H173L167 157L155 145L149 149L143 145L131 157L125 169V223ZM384 172Q384 174 386 178Q387 181 387 183Q385 186 384 191Q384 196 384 200Q383 205 381 208Q379 212 373 212Q377 217 378 222Q379 228 381 233Q384 234 386 246Q388 257 390 272Q392 288 396 304Q399 321 405 332Q405 343 403 345Q401 347 401 349Q401 350 402 351H405Q406 361 408 367Q409 373 410 378Q411 384 412 390Q413 396 413 406Q413 415 416 425Q418 435 422 446Q425 456 428 466Q430 475 430 481Q430 483 430 484Q429 484 429 486Q429 486 432 492Q434 499 437 508Q440 516 442 524Q445 532 445 534Q445 546 446 556Q447 566 458 568Q459 567 465 566Q471 566 471 563H519Q528 558 528 552Q528 547 527 538Q526 530 524 520Q523 510 520 501Q517 492 514 486H516Q509 465 505 454Q501 443 500 438Q498 434 497 433Q496 432 495 430V409Q490 409 490 406Q489 403 487 401L490 398Q486 392 484 388Q482 384 479 382Q485 381 487 377Q486 371 484 369Q481 367 481 364Q481 362 482 361H487Q483 359 482 356Q482 353 482 351L478 297Q478 296 476 288Q475 281 473 270Q471 260 470 248Q468 237 468 230Q468 223 469 222H472Q472 209 464 204L449 158Q441 160 438 161Q435 162 433 162Q431 162 429 161V169Q424 167 424 162Q423 158 421 153Q419 156 417 156Q416 156 416 156Q416 155 415 155Q413 155 406 164Q398 172 384 172ZM303 -61Q299 -66 293 -73Q287 -80 287 -90H293Q313 -90 328 -81Q344 -72 364 -72Q367 -71 376 -70Q385 -68 394 -66Q404 -65 413 -64Q422 -62 425 -61L428 -59Q429 -59 429 -58Q426 -58 424 -54Q422 -51 421 -46Q420 -40 420 -29L422 -27Q422 -25 426 -19Q430 -13 430 -11H429V-10Q429 -8 432 0Q435 8 439 18Q443 28 446 39Q449 50 449 58Q449 64 446 66Q432 60 415 52Q398 45 382 36Q365 27 352 18Q340 9 335 0V-13Q333 -13 327 -12Q321 -11 319 -11Q316 -13 316 -18Q315 -22 314 -27Q314 -32 314 -36Q313 -40 311 -40L300 -37Q294 -42 294 -50Q294 -52 295 -53L300 -48V-50Q300 -55 302 -57Q303 -59 303 -61ZM161 145Q166 145 166 139Q166 133 161 133Q156 133 156 139Q156 145 161 145ZM516 499Q514 499 514 496Q514 494 516 494Q518 494 518 496Q518 499 516 499ZM442 166 443 165Q445 165 447 169H442ZM473 297Q473 298 472 298Q469 298 469 294H470Q473 294 473 297ZM410 393Q410 390 408 390Q407 390 407 391Q408 391 408 392Q408 394 409 394ZM402 337H400L402 340Z"/><path transform="translate(21.2 52.0) rotate(1.2) scale(0.0387 -0.0387) translate(-327.5 -202.0)" d="M509 -89 503 -86Q501 -85 498 -84Q496 -83 494 -83L484 -78L479 -68V-58L473 -53L487 -6V8Q487 9 488 18Q490 26 492 36Q494 46 496 54Q497 63 497 65L501 54V80L492 74L497 90V100L507 115V125L497 119Q497 121 498 129Q499 137 500 146Q502 154 503 162Q504 169 504 171L508 212L493 210Q488 209 484 208Q481 208 479 208H443V202Q443 196 441 184Q439 171 437 158Q435 145 433 136Q431 126 431 125V115L427 110L431 100V34L427 30L422 19V9L416 4Q412 4 406 9Q400 14 396 14L391 19H381L371 30H356L345 39V95L351 115V156Q351 170 354 198Q357 226 371 281Q371 297 375 312Q379 328 384 344Q388 361 392 379Q396 397 396 418V428Q396 452 400 465Q405 478 411 484Q417 491 424 492Q431 493 436 493H441Q453 485 460 484Q466 483 471 478L476 473L478 462Q479 457 480 453Q481 449 481 447V437L478 423Q476 417 475 412Q474 406 472 402L467 387L460 341Q460 338 459 332Q458 325 457 318Q456 310 455 304Q454 298 454 296Q458 296 467 295Q476 294 486 294Q495 293 504 292Q514 291 520 291L525 296L530 326Q530 328 532 338Q535 348 538 359Q541 370 544 380Q546 390 546 392L552 407Q552 408 555 419Q558 430 562 443Q566 456 569 467Q572 478 572 480Q572 481 574 489L582 500L590 502Q593 503 596 504Q600 505 602 505H607L617 500L628 489Q640 486 640 474Q640 472 638 464L632 418Q632 407 630 394Q627 380 624 366Q622 353 620 340Q617 326 617 316Q617 302 610 284Q602 266 602 246V201Q602 199 601 194Q600 188 600 181Q599 174 598 168Q597 162 597 160V150L592 119Q592 116 590 102Q587 89 587 85L582 -6Q582 -10 580 -22Q578 -35 576 -49Q574 -63 572 -75Q570 -87 570 -89L558 -103Q553 -108 549 -108H539L524 -97L519 -83ZM61 8Q61 11 63 16Q65 22 65 27L78 55Q81 75 85 86Q89 97 94 103Q98 109 101 112Q104 115 104 120Q104 125 112 133Q120 141 120 145Q120 149 127 160Q134 171 134 175H114Q97 175 83 168Q69 160 55 160L49 163Q42 168 41 170L15 195V199L21 209L31 215H41Q42 215 52 217L60 219L76 233Q83 238 90 244Q96 250 100 254L110 264Q110 267 114 272Q117 276 120 278V288Q123 315 127 338Q131 361 134 387L140 413Q140 437 147 460Q154 483 154 502L169 512L193 506Q198 506 209 500Q220 495 223 492L229 486Q231 484 233 481Q235 478 237 475L243 467L241 461Q239 453 239 452L233 442Q231 440 230 436Q228 433 226 428L223 417V407Q223 405 222 399Q222 393 221 386Q220 378 220 372Q219 365 219 363V353Q219 351 218 344Q216 338 214 330Q212 323 210 316Q209 310 209 308V274Q209 270 206 264Q203 258 203 254L219 249Q220 249 226 248Q232 246 238 244Q245 242 250 240Q256 239 258 239L263 234V229L250 196L237 186L228 175Q228 172 220 168Q213 164 213 160Q220 155 225 150Q230 144 236 138Q241 132 248 126Q255 121 266 116L298 99Q300 97 302 94Q305 90 309 87L318 79V69L312 64L302 44H278Q274 44 264 50Q253 55 245 58L209 86L179 106H169L159 96V86L151 73Q148 68 145 63Q142 58 140 56L112 10L107 -4L102 -10H92L87 -4H77ZM126 269H135L142 288ZM494 9V-2L500 -9L499 4ZM339 74Q344 74 344 72Q344 70 339 70Q335 70 335 72Q335 74 339 74Z"/><path transform="translate(22.4 83.0) rotate(-0.6) scale(0.0323 -0.0323) translate(-268.5 -209.0)" d="M292 -62Q286 -62 281 -64Q276 -66 269 -67L259 -48L250 -53L245 -48Q241 -48 229 -43Q217 -38 217 -34L214 -21Q213 -16 212 -10Q212 -5 212 -1V27Q212 31 214 39Q217 47 217 51V64L222 74V83L212 79Q216 82 221 88Q226 94 226 97L228 112Q229 118 230 128Q232 137 235 139L231 144V149L236 163V172L240 181V200L226 195H212L198 186H184L174 181Q171 181 160 178Q150 176 146 176L118 172Q116 172 111 173Q106 174 104 176L99 181L89 186L85 190L75 195L61 214L42 223L39 231Q37 241 37 242V247L42 252L50 254Q60 256 61 256H66Q70 256 76 254Q81 252 85 252L99 247H127L137 249Q141 250 145 251Q149 252 151 252L170 256Q177 256 186 258Q195 260 203 262Q211 264 217 266Q223 268 223 268L231 270L250 280Q259 280 272 285Q284 290 298 296Q311 302 326 307Q340 312 354 313L378 314L392 327Q395 327 406 332Q416 336 420 336L439 332H453L462 327L467 322H472L481 318Q483 316 486 314Q488 313 490 311L495 308V294L500 289V285L495 280L481 275Q477 275 465 268Q453 261 448 261H443L434 256Q421 248 406 238Q390 229 378 222Q366 215 359 211Q352 207 355 209L340 195V176Q340 173 338 160Q335 148 335 144Q335 140 338 137Q340 134 340 130Q340 127 338 119Q335 111 335 107V83L332 73Q331 68 330 65Q330 62 330 60L325 56L330 37H325V9L321 -1V-20L316 -34Q316 -35 318 -43L321 -48V-53L297 -62ZM121 438Q121 441 122 448Q123 454 124 462Q126 470 127 476Q128 483 128 486Q128 488 130 496Q132 504 134 513Q137 522 139 530Q141 537 141 540Q141 554 149 568Q157 581 168 581Q173 581 185 578Q197 574 202 574L216 567L243 533L251 529Q257 526 263 526H270Q279 526 292 522Q305 519 310 516L318 513Q319 513 328 508Q337 504 346 498Q356 491 364 484Q372 477 372 472L375 461Q379 452 379 445V438Q373 432 362 418Q351 403 345 397L338 384Q338 381 335 378Q332 374 328 371L318 363Q313 358 301 350Q289 343 284 343L270 339Q264 337 258 336Q252 336 250 336H223Q210 336 195 340Q180 345 173 350L162 357L128 390L121 404ZM105 -59Q105 -37 114 -20Q124 -2 124 11Q124 17 133 26L142 30H166Q172 23 181 12Q190 0 190 -7V-26Q190 -27 188 -34Q186 -41 183 -50Q180 -60 178 -70Q176 -79 176 -83Q176 -85 175 -90Q174 -94 173 -99L171 -111H248L306 -101L355 -111Q359 -111 366 -116Q374 -121 374 -125V-144L364 -147Q347 -157 322 -160Q298 -163 275 -163H194Q168 -163 156 -156Q143 -149 138 -149Q132 -149 124 -144L114 -139L105 -130L100 -116V-78ZM216 479Q209 472 210 467Q211 462 205 452L202 445V397H216Q220 397 226 400Q233 404 239 408Q245 412 249 415Q253 418 253 418Q257 421 260 424Q263 428 263 431V438L247 458Q245 462 242 465Q239 468 236 472ZM240 83Q236 83 236 78Q236 76 238 72Q236 70 236 69Q236 64 240 64Q244 64 244 70Q244 72 242 74Q244 74 244 77Q244 83 240 83ZM236 -10V26Q235 21 233 16Q231 11 231 9V-1ZM236 60H235Q232 60 232 50Q232 40 235 40Q237 40 238 44Q239 48 239 51Q239 57 236 60ZM239 102V90L245 96V110ZM250 135Q246 135 246 130Q246 126 250 126Q254 126 254 130Q254 135 250 135ZM255 158Q251 158 251 153Q251 149 255 149Q258 149 258 153Q258 158 255 158ZM245 60Q241 60 241 58Q241 56 245 56Q249 56 249 58Q249 60 245 60Z"/></g>'
            '</defs></svg>')

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
  <title>Stamp · Chae Kim</title>
  <meta name="description" content="Chae Kim: MBA at Berkeley Haas, co-founded Lucent, previously at EY and Tritooling. I like to build things. Let's chat.">
  <meta name="robots" content="noindex">
  <meta property="og:title" content="Chae Kim · Product and strategy">
  <meta property="og:image" content="https://chaekim-portfolio.vercel.app/assets/img/og.png">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap">
  <link rel="preload" as="image" href="/assets/img/thumbs/lucent-wide.jpg">
  <link rel="stylesheet" href="/assets/css/v-stamp.css?v=%%V%%">
  <script>try { var t = localStorage.getItem('ck-theme'); if (t) document.documentElement.setAttribute('data-theme', t); } catch (e) {}</script>
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
        <span class="status"><i aria-hidden="true"></i><span>Lately building <a href="#builds">TypeRace</a>, a typing race for my classmates.</span></span> <a data-user="chaewoonkim" data-domain="berkeley.edu" href="#">Let's chat</a>.</p>
    </section>

    <div class="tabs" role="tablist" aria-label="Sections">
      <button class="tab" role="tab" id="tab-work" data-tab="work" aria-controls="work" aria-selected="true">Work</button>
      <button class="tab" role="tab" id="tab-builds" data-tab="builds" aria-controls="builds" aria-selected="false" tabindex="-1">Builds</button>
      <button class="tab" role="tab" id="tab-about" data-tab="about" aria-controls="about" aria-selected="false" tabindex="-1">About</button>
    </div>

    <!-- ============ WORK ============ -->
    <section class="panel" id="work" role="tabpanel" aria-labelledby="tab-work">
      <div class="grid">
        <a class="w w--wide reveal" href="/projects/lucent">
          <div class="stage" style="--g: var(--g-lucent)">
            <div class="art"><div class="browser"><div class="browser__bar"><i></i><i></i><i></i><span>trylucent.ai</span></div><img src="/assets/img/thumbs/lucent-wide.jpg" alt="Lucent's homepage: The AI Search Console" width="1440" height="810"></div></div>
            <span class="pill">Lucent <em>2025–26</em></span>
          </div>
          <h3 class="w-title">Making small businesses visible in AI search.</h3>
          <p class="meta">AI search observability platform and consultancy. <b>First paying pilot, 5 LOIs in 30 days.</b></p>
        </a>

        <a class="w reveal" href="/projects/ey">
          <div class="stage" style="--g: var(--g-ey)">
            <div class="art"><div class="glass"><b>Cloud</b><span>migration program</span></div></div>
            <span class="pill">EY <em>2021–24</em></span>
          </div>
          <h3 class="w-title">Giving leaders one clear view of a sprawling cloud migration.</h3>
          <p class="meta">Risk, OKRs, and the first executive QBR for a $200M+ cloud migration. <b>−30% executive escalations.</b></p>
        </a>

        <a class="w reveal" href="/projects/tritooling">
          <div class="stage" style="--g: var(--g-tri)">
            <div class="art"><div class="glass"><b>Factory</b><span>operations</span></div></div>
            <span class="pill">Tritooling <em>2024–25</em></span>
          </div>
          <h3 class="w-title">Fixing late deliveries and defects at a precision manufacturer.</h3>
          <p class="meta">A year running operations at a precision manufacturer. <b>−30% defects.</b></p>
        </a>

        <a class="w reveal" href="/projects/mirrorme">
          <div class="stage" style="--g: var(--g-mirror)">
            <div class="art"><div class="fan"><img src="/assets/img/projects/mirrorme/card-category.png" alt="MirrorMe card: Openness to experience, pink" width="714" height="1000" loading="lazy"><img src="/assets/img/projects/mirrorme/card-alt.png" alt="MirrorMe card: Openness to experience, orange" width="733" height="1000" loading="lazy"></div></div>
            <span class="pill">MirrorMe <em>2024</em></span>
          </div>
          <h3 class="w-title">Icebreakers that go deeper without getting awkward.</h3>
          <p class="meta">An icebreaker card game for hosts. <b>150+ pre-orders, $0 ad spend.</b></p>
        </a>

        <a class="w reveal" href="/projects/mobility">
          <div class="stage" style="--g: var(--g-mobility)">
            <div class="art"><div class="glass glass--status"><b>Stealth</b><span><i aria-hidden="true"></i>in progress</span></div></div>
            <span class="pill">Mobility <em>now</em></span>
          </div>
          <h3 class="w-title">Mobility aids people aren't embarrassed to use.</h3>
          <p class="meta">Design-forward mobility products that keep older adults independent longer.</p>
        </a>
      </div>

      <h2 class="sub-h">Earlier, at Indiana University (2019 to 2021)</h2>
      <div class="grid grid--5">
        <a class="w reveal" href="/projects/iu-study-assistant">
          <div class="stage"><div class="art fill"><img src="/assets/img/projects/iusa/home.jpg" alt="IU Study Assistant home screen" width="1400" height="720" loading="lazy"></div><span class="pill">Study Assistant</span></div>
          <p class="meta">One place to study, not nine tabs.</p>
        </a>
        <a class="w reveal" href="/projects/alab">
          <div class="stage" style="--g: linear-gradient(160deg,#eaf6fb,#d9eef7)"><div class="art fill fill--contain"><img src="/assets/img/projects/alab/cover-intro.png" alt="aLab app login screen" width="418" height="823" loading="lazy"></div><span class="pill">aLab</span></div>
          <p class="meta">A dog bowl that rises to meet a recovering pup.</p>
        </a>
        <a class="w reveal" href="/projects/luc">
          <div class="stage"><div class="art fill"><img src="/assets/img/projects/luc/mockup.jpg" alt="Pencil schematic of LUC's luggage wheels" width="1400" height="1208" loading="lazy"></div><span class="pill">LUC</span></div>
          <p class="meta">Luggage that weighs itself before the check-in counter does.</p>
        </a>
        <a class="w reveal" href="/projects/ptm">
          <div class="stage"><div class="art fill"><img src="/assets/img/projects/ptm/mockup.jpg" alt="Pencil schematic of the PTM sleep mask" width="1400" height="614" loading="lazy"></div><span class="pill">PTM</span></div>
          <p class="meta">A sleep mask that notices your fever before you do.</p>
        </a>
        <a class="w reveal" href="/projects/coursera">
          <div class="stage"><div class="art fill fill--contain"><img src="/assets/img/projects/coursera-cover.jpg" alt="Cover of the Coursera PM dossier" width="464" height="600" loading="lazy"></div><span class="pill">Coursera</span></div>
          <p class="meta">Making online learning transferable to real careers.</p>
        </a>
      </div>
    </section>

    <!-- ============ BUILDS ============ -->
    <section class="panel" id="builds" role="tabpanel" aria-labelledby="tab-builds">
      <h2 class="sub-h">Products</h2>
      <div class="grid grid--3">
        <a class="w reveal" href="https://tally-lake-seven.vercel.app" target="_blank" rel="noopener">
          <div class="stage" style="--g: var(--g-tri)"><div class="art"><div class="browser"><div class="browser__bar"><i></i><i></i><i></i><span>tally</span></div><img src="/assets/img/builds/tally.jpg" alt="Tally's notes screen: Notes That Add Up" width="960" height="600" loading="lazy"></div></div><span class="pill">Tally ↗ <em>2026</em></span></div>
          <h3 class="w-title">Knowing how long your to-do list will actually take.</h3>
          <p class="meta">A note-taker where every line gets a Claude time estimate, totaled in a ledger column.</p>
        </a>
        <a class="w reveal" href="https://color-palette-generator-three-sand.vercel.app" target="_blank" rel="noopener">
          <div class="stage" style="--g: var(--g-mirror)"><div class="art"><div class="browser"><div class="browser__bar"><i></i><i></i><i></i><span>palette</span></div><img src="/assets/img/builds/palette.jpg" alt="Color Palette Generator home: colors and fonts for your startup, in minutes" width="960" height="600" loading="lazy"></div></div><span class="pill">Palette Generator ↗ <em>2026</em></span></div>
          <h3 class="w-title">Brand colors and fonts for founders who aren't designers.</h3>
          <p class="meta">Palettes that pass accessibility checks, font pairings, and what real startups use right now.</p>
        </a>
        <a class="w reveal" href="https://typerace.typerace.workers.dev" target="_blank" rel="noopener">
          <div class="stage" style="--g: var(--g-lucent)"><div class="art"><div class="browser"><div class="browser__bar"><i></i><i></i><i></i><span>typerace</span></div><img src="/assets/img/builds/typerace.jpg" alt="TypeRace home: Race your friends" width="960" height="600" loading="lazy"></div></div><span class="pill">TypeRace ↗ <em>2026</em></span></div>
          <h3 class="w-title">Settling who types fastest, with one link and no sign-up.</h3>
          <p class="meta">Live races for classmates: share a code, type the same story, first to finish wins.</p>
        </a>
        <a class="w reveal" href="https://networking-tracker-five-sage.vercel.app" target="_blank" rel="noopener">
          <div class="stage" style="--g: var(--g-ey)"><div class="art"><div class="glass"><b>Contacts</b><span>yours alone</span></div></div><span class="pill">Networking Tracker ↗ <em>2026</em></span></div>
          <h3 class="w-title">Keeping track of every coffee chat, without sharing a thing.</h3>
          <p class="meta">A contact tracker where Postgres row-level security keeps each person's data their own.</p>
        </a>
        <a class="w reveal" href="https://github.com/chaekim96/VoicePrompter" target="_blank" rel="noopener">
          <div class="stage" style="--g: var(--g-mobility)"><div class="art"><div class="glass"><b>Prompter</b><span>follows your voice</span></div></div><span class="pill">VoicePrompter ↗ <em>macOS</em></span></div>
          <h3 class="w-title">Reading your notes on a call without anyone seeing them.</h3>
          <p class="meta">A teleprompter that scrolls as you speak and stays out of Zoom, Meet, and screenshots.</p>
        </a>
      </div>

      <h2 class="sub-h">Claude Code mods</h2>
      <div class="grid grid--3">
        <div class="w reveal">
          <div class="stage" style="--g: var(--g-arcade)"><div class="art"><div class="term" aria-hidden="true"><p>SmartModel rates this medium-effort.</p><p>Which model should run it?</p><ul><li class="on">Sonnet (recommended)</li><li>Haiku</li><li>Opus</li><li>Fable</li></ul></div></div><span class="pill">SmartModel <em>Claude Code</em></span></div>
          <h3 class="w-title">Matching each prompt to the right model, so easy work costs less.</h3>
          <p class="meta">A hook that scores how hard a prompt is and recommends Haiku, Sonnet, Opus, or Fable. Runs in ask, auto, or block mode.</p>
        </div>
        <div class="w reveal">
          <div class="stage" style="--g: var(--g-tri)"><div class="art"><div class="gauge" aria-hidden="true"><span>context</span><i><b></b></i></div></div><span class="pill">Token-Fuel <em>macOS</em></span></div>
          <h3 class="w-title">Seeing how much context is left before a session runs out.</h3>
          <p class="meta">A floating gauge on the Claude window and a CLI status line for Claude Code and Codex.</p>
        </div>
        <div class="w reveal">
          <div class="stage" style="--g: var(--g-ey)"><div class="art"><div class="glass"><b>Review</b><span>readability, performance</span></div></div><span class="pill">Code Improver <em>subagent</em></span></div>
          <h3 class="w-title">A second reviewer that reads every file I touch.</h3>
          <p class="meta">A custom Claude Code subagent that suggests readability, performance, and best-practice fixes.</p>
        </div>
      </div>

      <h2 class="sub-h">AI and ML coursework</h2>
      <div class="grid grid--3">
        <a class="w reveal" href="https://github.com/chaekim96/personal-wiki" target="_blank" rel="noopener">
          <div class="stage" style="--g: var(--g-arcade)"><div class="art fill"><img src="/assets/img/builds/personal-wiki.jpg" alt="Obsidian graph of the wiki's linked notes" width="900" height="646" loading="lazy"></div><span class="pill">Personal Wiki ↗ <em>2026</em></span></div>
          <h3 class="w-title">Asking my own notes questions, with no internet.</h3>
          <p class="meta">Local Gemma via Ollama, plus hybrid retrieval over a course wiki. Runs fully offline.</p>
        </a>
        <a class="w reveal" href="https://github.com/chaekim96/pacman-dqn" target="_blank" rel="noopener">
          <div class="stage" style="--g: var(--g-arcade)"><div class="art fill fill--contain fill--pixel"><img src="/assets/img/builds/pacman-dqn.gif" alt="The trained agent playing Ms. Pac-Man" width="160" height="210" loading="lazy"></div><span class="pill">Pac-Man DQN ↗ <em>2026</em></span></div>
          <h3 class="w-title">Teaching an agent to play Ms. Pac-Man by trial and error.</h3>
          <p class="meta">A DQN agent that raised its mean evaluation score from 492 to 680.</p>
        </a>
        <a class="w reveal" href="https://github.com/chaekim96/custom-llm" target="_blank" rel="noopener">
          <div class="stage"><div class="art fill fill--top"><img src="/assets/img/builds/custom-llm.jpg" alt="Terminal chat with the tiny model and its odd replies" width="768" height="474" loading="lazy"></div><span class="pill">Custom LLM ↗ <em>2026</em></span></div>
          <h3 class="w-title">Seeing how language models learn by training a tiny one.</h3>
          <p class="meta">A nanoGPT fork trained on a laptop CPU with my own teaching corpus, scored on 48 test prompts.</p>
        </a>
      </div>

      <h2 class="sub-h">Side quests</h2>
      <div class="grid grid--3">
        <a class="w reveal" href="/#break">
          <div class="stage" style="--g: var(--g-arcade)"><div class="art">%%SNAKE%%</div><span class="pill">Arcade <em>play</em></span></div>
          <p class="meta">Snake and Galaga, rebuilt from memory, plus a generative lo-fi radio.</p>
        </a>
        <a class="w reveal" href="/projects/home-gif">
          <div class="stage"><div class="art fill fill--pixel"><img src="/assets/img/projects/home.gif" alt="Pixel-art house at dusk" width="1067" height="600" loading="lazy"></div><span class="pill">Home <em>2020</em></span></div>
          <p class="meta">A pixel-art GIF, made during COVID.</p>
        </a>
        <a class="w reveal" href="/projects/yin-yang">
          <div class="stage"><div class="art fill"><img src="/assets/img/projects/yin-yang.gif" alt="Animated yin yang over a framed painting" width="1067" height="600" loading="lazy"></div><span class="pill">Yin Yang <em>2020</em></span></div>
          <p class="meta">An animated illustration.</p>
        </a>
        <div class="w reveal">
          <div class="stage" style="--g: var(--g-mobility)"><div class="art"><div class="glass"><b>3D</b><span>printing</span></div></div><span class="pill">3D prints</span></div>
          <p class="meta">Keychains, organizers, and containers.</p>
        </div>
        <a class="w reveal" href="/assets/pdf/I308-Lime-Scooter-Poster.pdf" target="_blank" rel="noopener">
          <div class="stage"><div class="art fill"><img src="/assets/img/projects/fake-news.jpg" alt="A phone showing a news app, held over a scooter" width="489" height="601" loading="lazy"></div><span class="pill">Poster ↗ <em>2020</em></span></div>
          <p class="meta">A media literacy poster.</p>
        </a>
        <a class="w reveal" href="/assets/pdf/WMCS-Weight-Machine-Cross-Sync.pdf" target="_blank" rel="noopener">
          <div class="stage" style="--g: var(--g-ey)"><div class="art"><div class="glass"><b>NFC</b><span>gym sets, synced</span></div></div><span class="pill">WMCS ↗ <em>2019</em></span></div>
          <p class="meta">Weight Machine Cross Sync: log gym sets over NFC.</p>
        </a>
        <a class="w reveal" href="/assets/pdf/AAV-Auto-Adjusting-Volume.pdf" target="_blank" rel="noopener">
          <div class="stage" style="--g: var(--g-tri)"><div class="art"><div class="glass"><b>dB</b><span>auto volume</span></div></div><span class="pill">AAV ↗ <em>2019</em></span></div>
          <p class="meta">Auto-Adjusting Volume: noise-aware volume.</p>
        </a>
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
            <p>I'm also writing a memoir, <em>The Treaded Path</em>, and essays on <a href="https://medium.com/@chaewoonkim" target="_blank" rel="noopener">Medium ↗</a>.</p>
          </section>

          <section id="experience">
            <h3>Experience</h3>
            <ul class="xp">
              <li><b>UC Berkeley Haas</b><small>2025–27</small><span><em>MBA Candidate.</em> Merit Scholarship. Co-President, Asian Business Club (300+ members).</span></li>
              <li><b>Lucent</b><small>2025–26</small><span><em>Co-founder &amp; CEO.</em> First paying pilot. 5 LOIs in 30 days. 100+ customer interviews. NSF I-Corps backed.</span></li>
              <li><b>Tritooling Precision Corporation</b><small>Jul 2024–Jul 2025</small><span><em>Director of Operations, Philippines.</em> On-time delivery +15%, defects −30%. ERP make-vs-buy case approved, $100K in annual savings. Board approval to launch in Japan, a $300K+ revenue opportunity.</span></li>
              <li><b>EY</b><small>Aug 2021–Jul 2024</small><span><em>Senior Technology Consultant, AI &amp; Data Strategy, New York.</em> Redirected $3M to priority initiatives after launching a Fortune 500 client's first QBR. $10M+ in realized savings over 2 years. −30% escalations on a $200M+ program. 90% tool adoption across 4,000 users.</span></li>
              <li><b>Indiana University Bloomington</b><small>Class of 2021</small><span><em>B.S. Informatics, minors in HCI &amp; Entrepreneurship.</em> Dean's List. GPA 3.74. <span class="confirm">[CONFIRM: start year]</span></span></li>
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
  </main>

  <footer class="foot wrap">
    <div>
      <a class="foot__id" href="#work">%%SEAL_SMALL%%chae kim</a>
      <p class="clock">
        <svg id="clock-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <g class="sun"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></g>
          <g class="moon"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></g>
        </svg>
        <time id="clock"></time><span>Berkeley, CA</span>
      </p>
    </div>
    <nav aria-label="Footer">
      <a href="#work">Work</a><a href="#builds">Builds</a><a href="#about">About</a><a href="/assets/pdf/chae-kim-resume.pdf">Resume</a>
    </nav>
    <div class="foot__cta">
      <b>Let's chat.</b>
      <a data-user="chaewoonkim" data-domain="berkeley.edu" data-show href="#">chaewoonkim@berkeley.edu</a>
      <div class="foot__small">
        <span>Built by hand in plain HTML, between latte art attempts.</span>
        <span><code>CHANGELOG: %%CHANGELOG%%</code></span>
      </div>
    </div>
  </footer>

%%SWITCHER%%  <script src="/assets/js/main.js?v=%%V%%"></script>
  <script>
  (function () {
    var THESIS = {
      'work': 'I like to build things, from startups to card games.',
      'builds': 'Tools I build for myself, then share.',
      'about': 'Product, strategy, operations, and the occasional 3D print.'
    };
    var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
    var tabs = [].slice.call(document.querySelectorAll('.tab'));
    var panels = [].slice.call(document.querySelectorAll('.panel'));
    var thesis = document.querySelector('.thesis');
    var current = null;

    function show(id, opts) {
      opts = opts || {};
      if (!THESIS[id]) id = 'work';
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

    // deep links: #work, #about, or a section inside About such as #experience
    function fromHash() {
      var h = location.hash.slice(1), el = h && document.getElementById(h);
      if (THESIS[h]) show(h);
      else if (el && el.closest('#about')) { show('about'); requestAnimationFrame(function () { el.scrollIntoView(); }); }
      else show('work');
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
  <script defer src="/_vercel/insights/script.js"></script>
</body>
</html>
"""

STAMP = (STAMP.replace("%%V%%", V)
              .replace("%%INK%%", INK_DEFS)
              .replace("%%SEAL%%", seal())
              .replace("%%SEAL_SMALL%%", seal(label=False))
              .replace("%%SNAKE%%", _snake())
              .replace("%%CHANGELOG%%", STAMP_CHANGELOG)
              .replace("%%SWITCHER%%", switcher("stamp")))

# ----------------------------------------------------------------------------
# picker
# ----------------------------------------------------------------------------

INDEX = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Design variants · Chae Kim</title>
  <meta name="robots" content="noindex">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap">
  <link rel="stylesheet" href="/assets/css/style.css?v={V}">
  <style>
    .pick {{ max-width: 860px; margin: 0 auto; padding: clamp(40px, 8vw, 96px) var(--gutter); }}
    .pick h1 {{ font-size: clamp(28px, 4vw, 40px); margin-bottom: 8px; }}
    .pick p {{ color: var(--ink-2); margin-bottom: 28px; }}
    .pick__grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 14px; }}
    .pick a.opt {{ display: block; padding: 20px; border: 1px solid var(--line); border-radius: var(--radius); background: var(--bg-elev); transition: .25s; }}
    .pick a.opt:hover {{ transform: translateY(-4px); border-color: var(--accent); box-shadow: var(--shadow-lg); }}
    .pick a.opt b {{ display: block; font-size: 18px; margin-bottom: 4px; }}
    .pick a.opt span {{ font-size: 14px; color: var(--ink-3); }}
    .pick a.opt small {{ display: block; margin-top: 10px; font-size: 12px; color: var(--accent); font-weight: 600; }}
  </style>
</head>
<body>
  <main class="pick">
    <p class="label">variants</p>
    <h1>One portfolio, five metaphors.</h1>
    <p>Same content, different framing. Pick one to compare.</p>
    <div class="pick__grid">
      <a class="opt" href="/"><b>Desktop</b><span>macOS desktop, folders, and windows. The current v2.</span><small>current →</small></a>
      <a class="opt" href="/variants/prd"><b>PRD</b><span>A product requirements document with status, requirements, and sign-off.</span><small>open →</small></a>
      <a class="opt" href="/variants/notebook"><b>Field notebook</b><span>Dated entries on ruled paper, taped-in specimens, stamps.</span><small>open →</small></a>
      <a class="opt" href="/variants/schematic"><b>Schematic</b><span>An engineering drawing: parts list, revision history, title block.</span><small>open →</small></a>
      <a class="opt" href="/variants/stamp"><b>Stamp</b><span>Quiet and gallery-like. Real artifacts, pill tabs, my name in Korean calligraphy.</span><small>open →</small></a>
    </div>
  </main>
</body>
</html>
"""

os.makedirs(OUT, exist_ok=True)
for name, html_ in (("index", INDEX), ("prd", PRD), ("notebook", NOTEBOOK), ("schematic", SCHEMATIC), ("stamp", STAMP)):
    with open(os.path.join(OUT, f"{name}.html"), "w") as f:
        f.write(html_)
    print("wrote variants/%s.html" % name)
