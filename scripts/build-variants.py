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
V = "12"
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
    opts = [("desktop", "/"), ("prd", "/variants/prd"), ("notebook", "/variants/notebook"), ("schematic", "/variants/schematic")]
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

TILES = """            <div class="tile"><span class="tile__icon">🗂️</span><span><span class="tile__title">Personal CRM</span><span class="tile__meta">~310 contacts, AI-enriched, with outreach tracking</span></span></div>
            <a class="tile" href="https://www.figma.com/make/jM7KyUTe5uojF6qOMhuF6U/Color-Palette-Generator?node-id=0-4" target="_blank" rel="noopener"><span class="tile__icon">🎨</span><span><span class="tile__title">Color Palette Generator ↗</span><span class="tile__meta">Figma Make · 2025</span></span></a>
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
CONFIRM_ROK = '<span class="confirm">[CONFIRM: years]</span>'

def tail(current):
    return f"""{switcher(current)}  <script src="/assets/js/main.js?v={V}"></script>
  <script defer src="/_vercel/insights/script.js"></script>
</body>
</html>
"""

# ----------------------------------------------------------------------------
# 1) PRD — the portfolio as a product requirements document
# ----------------------------------------------------------------------------

PRD = head("prd", "PRD", "Chae Kim, specified as a product requirements document. MBA at Berkeley Haas, co-founder of Lucent, ex-EY AI & Data. Looking for PM and strategy roles.", "&family=JetBrains+Mono:wght@400;500;600") + NAV + f"""
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
            <div><dt>Status</dt><dd><span class="pill pill--live"><i></i>Open to PM and strategy roles</span></dd></div>
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
              <span class="req__ac"><b>$14M extension</b><span>−30% executive escalations</span></span>
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
              <tr><td class="mono">Oct 2025 to present</td><td><b>Lucent</b><br><span class="ms__role">Co-founder &amp; CEO</span></td><td>First paying pilot. 5 LOIs in 30 days. 100+ customer interviews. NSF I-Corps backed.</td></tr>
              <tr><td class="mono">Jul 2024 to Jul 2025</td><td><b>Tritooling Precision Corporation, Philippines</b><br><span class="ms__role">Director of Operations</span></td><td>On-time delivery +15%, defects −30%. $1.5M savings case (ERP). $800K+ board-approved APAC market entry.</td></tr>
              <tr><td class="mono">Aug 2021 to Jul 2024</td><td><b>EY, New York</b><br><span class="ms__role">Senior Consultant, AI &amp; Data Strategy (Staff Consultant, 2021 to 2023)</span></td><td>$14M extension after launching a Fortune 500 client's first QBR. −30% escalations on a $200M+ program. 90% tool adoption across 4,000 users.</td></tr>
              <tr><td class="mono">Class of 2021</td><td><b>Indiana University Bloomington</b><br><span class="ms__role">B.S. Informatics, minors in HCI &amp; Entrepreneurship</span></td><td>Board of Aeons (top 1%). GPA 3.74. {CONFIRM_IU}</td></tr>
              <tr><td class="mono">Gangwon, Korea</td><td><b>Republic of Korea Army</b><br><span class="ms__role">Staff Sergeant · Squad Leader</span></td><td>Led a squad. {CONFIRM_ROK}</td></tr>
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
          <p class="sec__sub">Hiring for a PM or strategy role? Or building in AI search? Let's talk.</p>
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
            <p><strong>Looking for PM and strategy roles.</strong> For roles or collabs, email {EMAIL}. Essays on {MEDIUM}.</p>
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
              <span class="hand result">→ $14M extension · −30% escalations</span>
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
          <div class="tl"><div class="tl__when">Oct 2025 to present</div><div><div class="tl__org">Lucent</div><div class="tl__role">Co-founder &amp; CEO</div><ul class="tl__body"><li>First paying pilot. 5 LOIs in 30 days.</li><li>100+ customer interviews. NSF I-Corps backed.</li></ul></div></div>
          <div class="tl"><div class="tl__when">Jul 2024 to Jul 2025</div><div><div class="tl__org">Tritooling Precision Corporation, Philippines</div><div class="tl__role">Director of Operations</div><ul class="tl__body"><li>On-time delivery +15%, defects −30%.</li><li>$1.5M savings case (ERP). $800K+ board-approved APAC market entry.</li></ul></div></div>
          <div class="tl"><div class="tl__when">Aug 2021 to Jul 2024</div><div><div class="tl__org">EY, New York</div><div class="tl__role">Senior Consultant, AI &amp; Data Strategy (Staff Consultant, 2021 to 2023)</div><ul class="tl__body"><li>$14M extension after launching a Fortune 500 client's first QBR.</li><li>−30% escalations on a $200M+ program. 90% tool adoption across 4,000 users.</li></ul></div></div>
          <div class="tl"><div class="tl__when">Class of 2021</div><div><div class="tl__org">Indiana University Bloomington</div><div class="tl__role">B.S. Informatics, minors in HCI &amp; Entrepreneurship</div><ul class="tl__body"><li>Board of Aeons (top 1%). GPA 3.74. {CONFIRM_IU}</li></ul></div></div>
          <div class="tl"><div class="tl__when">Gangwon, Korea</div><div><div class="tl__org">Republic of Korea Army</div><div class="tl__role">Staff Sergeant · Squad Leader</div><ul class="tl__body"><li>Led a squad. {CONFIRM_ROK}</li></ul></div></div>
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
f'''        <p class="lede">Hiring for a PM or strategy role? Or building in AI search? Let's talk.</p>
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
            <p class="mono spec">NOTES: UNLESS OTHERWISE SPECIFIED, ALL DIMENSIONS ARE IN OUTCOMES. STATUS: <b>OPEN TO PM AND STRATEGY ROLES.</b> CONTACT: {EMAIL}</p>
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
              <td><b>$14M extension</b><span>−30% executive escalations</span></td>
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
            <tr><td class="mono">E</td><td class="mono">Oct 2025 to present</td><td><b>Lucent</b><br><span class="role">Co-founder &amp; CEO</span></td><td>First paying pilot. 5 LOIs in 30 days. 100+ customer interviews. NSF I-Corps backed.</td></tr>
            <tr><td class="mono">D</td><td class="mono">Jul 2024 to Jul 2025</td><td><b>Tritooling Precision Corporation, Philippines</b><br><span class="role">Director of Operations</span></td><td>On-time delivery +15%, defects −30%. $1.5M savings case (ERP). $800K+ board-approved APAC market entry.</td></tr>
            <tr><td class="mono">C</td><td class="mono">Aug 2021 to Jul 2024</td><td><b>EY, New York</b><br><span class="role">Senior Consultant, AI &amp; Data Strategy (Staff Consultant, 2021 to 2023)</span></td><td>$14M extension after launching a Fortune 500 client's first QBR. −30% escalations on a $200M+ program. 90% tool adoption across 4,000 users.</td></tr>
            <tr><td class="mono">B</td><td class="mono">Class of 2021</td><td><b>Indiana University Bloomington</b><br><span class="role">B.S. Informatics, minors in HCI &amp; Entrepreneurship</span></td><td>Board of Aeons (top 1%). GPA 3.74. {CONFIRM_IU}</td></tr>
            <tr><td class="mono">A</td><td class="mono">Gangwon, Korea</td><td><b>Republic of Korea Army</b><br><span class="role">Staff Sergeant · Squad Leader</span></td><td>Led a squad. {CONFIRM_ROK}</td></tr>
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
f'''        <p class="zone__sub">Hiring for a PM or strategy role? Or building in AI search? Let's talk.</p>
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
    <h1>One portfolio, four metaphors.</h1>
    <p>Same content, different framing. Pick one to compare.</p>
    <div class="pick__grid">
      <a class="opt" href="/"><b>Desktop</b><span>macOS desktop, folders, and windows. The current v2.</span><small>current →</small></a>
      <a class="opt" href="/variants/prd"><b>PRD</b><span>A product requirements document with status, requirements, and sign-off.</span><small>open →</small></a>
      <a class="opt" href="/variants/notebook"><b>Field notebook</b><span>Dated entries on ruled paper, taped-in specimens, stamps.</span><small>open →</small></a>
      <a class="opt" href="/variants/schematic"><b>Schematic</b><span>An engineering drawing: parts list, revision history, title block.</span><small>open →</small></a>
    </div>
  </main>
</body>
</html>
"""

os.makedirs(OUT, exist_ok=True)
for name, html_ in (("index", INDEX), ("prd", PRD), ("notebook", NOTEBOOK), ("schematic", SCHEMATIC)):
    with open(os.path.join(OUT, f"{name}.html"), "w") as f:
        f.write(html_)
    print("wrote variants/%s.html" % name)
