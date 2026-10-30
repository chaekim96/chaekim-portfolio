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
V = "29"

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

STAMP_CHANGELOG = "10-04-26"

from stamp_shared import INK_DEFS, seal, live_button, LIVE_DIALOG, LIVE_SCRIPT, CASE_HEAD_ASSETS, CASE_TOP, CASE_FOOT, CASE_SCRIPTS, THEME_COLOR, build_mark, build_icons


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
  <script>try { var t = localStorage.getItem('ck-theme'); if (t) document.documentElement.setAttribute('data-theme', t); } catch (e) {}</script>
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
        <article class="feat__card reveal">
        <a class="w feat__w" href="/projects/ai-visibility-checker">
          <div class="stage" style="--g: var(--g-lucent)"><div class="art"><div class="browser play"><div class="browser__bar"><i></i><i></i><i></i><span>ai visibility checker</span></div><img src="/assets/img/builds/ai-visibility-checker-card-2.jpg" alt="The AI Visibility Checker report for chaekim.vercel.app, ready for AI answers" width="960" height="600" loading="lazy"><img class="play__f" src="/assets/img/cases/avc-crawlers-2.jpg" alt="Which crawlers robots.txt lets in, split into search and live fetching versus model training." loading="lazy"><img class="play__f" src="/assets/img/builds/ai-visibility-checker-2.jpg" alt="The checker report for chaekim.vercel.app, ready for AI answers, with the fixes worth the most listed first" loading="lazy"></div></div><span class="pill">AI Visibility Checker <em>2026</em></span></div>
          <h3 class="w-title">Knowing whether AI assistants can find, read and cite your site.</h3>
          <p class="meta">Paste a URL: crawler rules, llms.txt, structured data, and text that's there without JavaScript.</p>
        </a>
        <div class="feat__strip">%%LIVE_AVC%%<a class="feat__case" href="/projects/ai-visibility-checker">Read the case study →</a></div>
        </article>
        <article class="feat__card reveal">
        <a class="w feat__w" href="/projects/tally">
          <div class="stage" style="--g: var(--g-tri)"><div class="art"><div class="browser play"><div class="browser__bar"><i></i><i></i><i></i><span>tally</span></div><img src="/assets/img/builds/tally.jpg" alt="Tally estimating a week of to-dos: an hour for the case memo, 30 minutes for bug reports, 3h45 in all" width="960" height="600" loading="lazy"><img class="play__f" src="/assets/img/cases/tally-day.jpg" alt="The Day view: a capacity meter, the Unscheduled tray, and blocks on the calendar." loading="lazy"><img class="play__f" src="/assets/img/cases/tally-summary.jpg" alt="The Summary: what's left, the finish-by time, and where the time goes." loading="lazy"></div></div><span class="pill">Tally <em>2026</em></span></div>
          <h3 class="w-title">Knowing how long your to-do list will actually take.</h3>
          <p class="meta">A note-taker where every line gets a Claude time estimate, totaled in a ledger column.</p>
        </a>
        <div class="feat__strip">%%LIVE_TALLY%%<a class="feat__case" href="/projects/tally">Read the case study →</a></div>
        </article>
        <article class="feat__card reveal">
        <a class="w feat__w" href="/projects/typerace">
          <div class="stage" style="--g: var(--g-lucent)"><div class="art"><div class="browser play"><div class="browser__bar"><i></i><i></i><i></i><span>typerace</span></div><img src="/assets/img/builds/typerace-2.jpg" alt="A TypeRace race in progress at 70 WPM, ink on near-white, the progress bar halfway across" width="960" height="600" loading="lazy"><img class="play__f" src="/assets/img/cases/typerace-results-2.jpg" alt="Results from a test race on my own server: finishing order, WPM, accuracy, and a WPM chart." loading="lazy"></div></div><span class="pill">TypeRace <em>2026</em></span></div>
          <h3 class="w-title">Settling who types fastest, with one link and no sign-up.</h3>
          <p class="meta">Live races for classmates: share a code, type the same story, first to finish wins.</p>
        </a>
        <div class="feat__strip">%%LIVE_TYPERACE%%<a class="feat__case" href="/projects/typerace">Read the case study →</a></div>
        </article>
      </div>

      <h2 class="sub-h">More products</h2>
      <div class="grid grid--shelf">
        <div class="live-card reveal">
        <a class="w" href="/projects/palette-generator">
          <div class="stage" style="--g: var(--g-mirror)"><div class="art"><div class="browser"><div class="browser__bar"><i></i><i></i><i></i><span>palette</span></div><img src="/assets/img/builds/palette.jpg" alt="Palette Generator turning 'coffee subscription, warm and earthy' into five roles of color and a font pairing" width="960" height="600" loading="lazy"></div></div><span class="pill">Palette Generator <em>2026</em></span></div>
          <h3 class="w-title">Brand colors and fonts for founders who aren't designers.</h3>
          <p class="meta">Palettes that pass accessibility checks, font pairings, and what real startups use right now.</p>
        </a>
        %%LIVE_PALETTE_GENERATOR%%
        </div>
        <div class="live-card reveal">
        <a class="w" href="/projects/networking-tracker">
          <div class="stage" style="--g: var(--g-ey)"><div class="art"><div class="browser"><div class="browser__bar"><i></i><i></i><i></i><span>networking tracker</span></div><img src="/assets/img/builds/networking-tracker.jpg" alt="Networking Tracker filtered to high-priority contacts, with demo data" width="960" height="600" loading="lazy"></div></div><span class="pill">Networking Tracker <em>2026</em></span></div>
          <h3 class="w-title">Keeping track of every coffee chat, without sharing a thing.</h3>
          <p class="meta">A contact tracker where Postgres row-level security keeps each person's data their own.</p>
        </a>
        %%LIVE_NETWORKING_TRACKER%%
        </div>
        <div class="live-card reveal">
        <a class="w" href="/projects/web-anatomy">
          <div class="stage" style="--g: var(--g-arcade)"><div class="art"><div class="browser"><div class="browser__bar"><i></i><i></i><i></i><span>webanatomy</span></div><img src="/assets/img/builds/web-anatomy.jpg" alt="The Anatomy of a Website home page: the title, the line SEO and GEO start with the website, and the start of the journey of a request" width="960" height="600" loading="lazy"></div></div><span class="pill">Anatomy of a Website <em>2026</em></span></div>
          <h3 class="w-title">Showing how a website works, from the DNS lookup to the AI answer.</h3>
          <p class="meta">An illustrated encyclopedia on one idea: SEO and GEO start with the website.</p>
        </a>
        %%LIVE_WEB_ANATOMY%%
        </div>
        <a class="w reveal" href="/projects/voiceprompter">
          <div class="stage" style="--g: var(--g-mobility)"><div class="art fill"><img src="/assets/img/builds/voiceprompter.jpg" alt="VoicePrompter listening at word 108 of 139, with the prompter highlighting the spoken word" width="800" height="600" loading="lazy"></div><span class="pill">VoicePrompter <em>macOS</em></span></div>
          <h3 class="w-title">Reading your notes on a call without anyone seeing them.</h3>
          <p class="meta">A teleprompter that scrolls as you speak and stays out of Zoom, Meet, and screenshots.</p>
        </a>
        <a class="w reveal" href="/projects/parallel-prospect-brief">
          <div class="stage" style="--g: var(--g-tri)"><div class="art fill"><img src="/assets/img/builds/parallel-prospect-brief-card.jpg" alt="An illustrative prospect brief for an invented company: what they do, products, agent signal, and best-fit API, with sources" width="800" height="600" loading="lazy"></div><span class="pill">Parallel Prospect Brief <em>CLI</em></span></div>
          <h3 class="w-title">Walking into a first sales call with every claim sourced.</h3>
          <p class="meta">A CLI that turns a company name into a cited one-page sales brief, built on Parallel's Task API.</p>
        </a>
        <a class="w reveal" href="/projects/product-blueprint">
          <div class="stage" style="--g: var(--g-mirror)"><div class="art fill"><img src="/assets/img/builds/product-blueprint-card.jpg" alt="The build loop: six stages from Discover to Ship, each with the gate it has to pass" width="800" height="600" loading="lazy"></div><span class="pill">Product Blueprint <em>playbook</em></span></div>
          <h3 class="w-title">One way to build every product, with a test at each step.</h3>
          <p class="meta">A six-stage build loop, a design system, and 22 prompts that each come with their own evals.</p>
        </a>
      </div>

      <h2 class="sub-h">Claude Code mods</h2>
      <div class="grid grid--shelf">
        <a class="w reveal" href="/projects/smartmodel">
          <div class="stage" style="--g: var(--g-arcade)"><div class="art"><div class="term" aria-hidden="true"><p>SmartModel rates this medium-effort.</p><p>Which model should run it?</p><ul><li class="on">Sonnet (recommended)</li><li>Haiku</li><li>Opus</li><li>Fable</li></ul></div></div><span class="pill">SmartModel <em>Claude Code</em></span></div>
          <h3 class="w-title">Matching each prompt to the right model, so easy work costs less.</h3>
          <p class="meta">A hook that scores how hard a prompt is and recommends Haiku, Sonnet, Opus, or Fable. Runs in ask, auto, or block mode.</p>
        </a>
        <a class="w reveal" href="/projects/token-fuel">
          <div class="stage" style="--g: var(--g-tri)"><div class="art fill"><img src="/assets/img/builds/token-fuel.jpg" alt="Token-Fuel in the menu bar at 67%, and its floating window: Good, 668.5k of 1M left, about 46 turns" width="800" height="600" loading="lazy"></div><span class="pill">Token-Fuel <em>macOS</em></span></div>
          <h3 class="w-title">Seeing how much context is left before a session runs out.</h3>
          <p class="meta">A floating gauge on the Claude window and a CLI status line for Claude Code and Codex.</p>
        </a>
        <a class="w reveal" href="/projects/code-improver">
          <div class="stage" style="--g: var(--g-ey)"><div class="art fill"><img src="/assets/img/builds/code-improver.jpg" alt="Code Improver reviewing build-cases.py: 14 findings ordered by severity, starting with a template page that was publicly served" width="800" height="600" loading="lazy"></div><span class="pill">Code Improver <em>subagent</em></span></div>
          <h3 class="w-title">A second reviewer that reads every file I touch.</h3>
          <p class="meta">A custom Claude Code subagent that suggests readability, performance, and best-practice fixes.</p>
        </a>
        <a class="w reveal" href="/projects/task-progress">
          <div class="stage" style="--g: var(--g-arcade)"><div class="art fill"><img src="/assets/img/builds/task-progress.jpg" alt="The /task-progress pane at 3 of 6: three steps done, one in progress, two pending" width="800" height="600" loading="lazy"></div><span class="pill">task-progress <em>Claude Code</em></span></div>
          <h3 class="w-title">Seeing how far along a task is, right above the prompt.</h3>
          <p class="meta">A mod that turns Claude's own task checklist into a calm progress band above the prompt, plus a checklist pane.</p>
        </a>
      </div>

      <h2 class="sub-h">AI and ML coursework</h2>
      <div class="grid grid--shelf">
        <div class="live-card reveal">
        <a class="w" href="/projects/spotify-review-triage">
          <div class="stage" style="--g: var(--g-mobility)"><div class="art"><div class="browser"><div class="browser__bar"><i></i><i></i><i></i><span>spotify-review-triage</span></div><img src="/assets/img/builds/spotify-review-triage-card.jpg" alt="The Spotify Review Triage dashboard: 660,622 reviews, $4.36 spend, and the recommendation" width="960" height="600" loading="lazy"></div></div><span class="pill">Spotify Review Triage <em>2026</em></span></div>
          <h3 class="w-title">Turning a flood of app reviews into one clear product priority.</h3>
          <p class="meta">A multi-agent LLM pipeline over 660,622 reviews, with an independent checker and a live dashboard.</p>
        </a>
        %%LIVE_SPOTIFY%%
        </div>
        <a class="w reveal" href="/projects/personal-wiki">
          <div class="stage" style="--g: var(--g-arcade)"><div class="art fill"><img src="/assets/img/builds/personal-wiki.jpg" alt="Obsidian graph of the wiki's linked notes" width="900" height="646" loading="lazy"></div><span class="pill">Personal Wiki <em>2026</em></span></div>
          <h3 class="w-title">Asking my own notes questions, with no internet.</h3>
          <p class="meta">Local Gemma via Ollama, plus hybrid retrieval over a course wiki. Runs fully offline.</p>
        </a>
        <a class="w reveal" href="/projects/pacman-dqn">
          <div class="stage" style="--g: var(--g-arcade)"><div class="art fill fill--contain fill--pixel"><img src="/assets/img/builds/pacman-dqn.gif" alt="The trained agent playing Ms. Pac-Man" width="160" height="210" loading="lazy"></div><span class="pill">Pac-Man DQN <em>2026</em></span></div>
          <h3 class="w-title">Teaching an agent to play Ms. Pac-Man by trial and error.</h3>
          <p class="meta">A DQN agent that raised its mean evaluation score from 492 to 680.</p>
        </a>
        <a class="w reveal" href="/projects/custom-llm">
          <div class="stage"><div class="art fill fill--top"><img src="/assets/img/builds/custom-llm.jpg" alt="Terminal chat with the tiny model and its odd replies" width="768" height="474" loading="lazy"></div><span class="pill">Custom LLM <em>2026</em></span></div>
          <h3 class="w-title">Seeing how language models learn by training a tiny one.</h3>
          <p class="meta">A nanoGPT fork trained on a laptop CPU with my own teaching corpus, scored on 48 test prompts.</p>
        </a>
      </div>

      <h2 class="sub-h">Side quests</h2>
      <div class="grid grid--shelf">
        <a class="w reveal" href="/projects/siri-reimagined">
          <div class="stage" style="--g: var(--g-lucent)"><div class="art"><div class="browser"><div class="browser__bar"><i></i><i></i><i></i><span>siri, reimagined</span></div><img src="/assets/img/builds/siri-reimagined-card.jpg" alt="Siri, Reimagined: the headline The last app you'll install, above three iPhones with Liquid Glass screens" width="960" height="600" loading="lazy"></div></div><span class="pill">Siri, Reimagined <em>concept</em></span></div>
          <p class="meta">A design concept: an iPhone that ships with five apps, and a Siri that builds the rest.</p>
        </a>
        <a class="w reveal" href="/projects/portfolio">
          <div class="stage" style="--g: var(--g-lucent)"><div class="art"><div class="browser"><div class="browser__bar"><i></i><i></i><i></i><span>chaekim.vercel.app</span></div><img src="/assets/img/builds/portfolio-card.jpg" alt="This site's homepage" width="960" height="600" loading="lazy"></div></div><span class="pill">This portfolio <em>2026</em></span></div>
          <p class="meta">How this site got built: the decisions, the backlog, and what's next.</p>
        </a>
        <a class="w reveal" href="/projects/personal-brand">
          <div class="stage" style="--g: var(--g-plain)"><div class="art"><div class="brandart">%%BRANDSEAL%%<span class="brandart__sw"><i style="background:#C8372D"></i><i style="background:#FF5A1F"></i><i style="background:#B07A4F"></i><i style="background:#0066CC"></i><i style="background:#123B2E"></i></span></div></div><span class="pill">Personal brand <em>2026</em></span></div>
          <p class="meta">How I chose a brand: five directions, two built finalists, and why Stamp won.</p>
        </a>
        <a class="w reveal" href="/projects/build-marks">
          <div class="stage" style="--g: var(--g-plain)"><div class="art"><div style="display:grid;grid-template-columns:repeat(3,52px);gap:10px"><img src="/assets/img/brand/tally.svg" alt="" width="52" height="52" loading="lazy" style="display:block;width:52px;height:52px;border-radius:12px"><img src="/assets/img/brand/token-fuel.svg" alt="" width="52" height="52" loading="lazy" style="display:block;width:52px;height:52px;border-radius:12px"><img src="/assets/img/brand/typerace.svg" alt="" width="52" height="52" loading="lazy" style="display:block;width:52px;height:52px;border-radius:12px"><img src="/assets/img/brand/smartmodel.svg" alt="" width="52" height="52" loading="lazy" style="display:block;width:52px;height:52px;border-radius:12px"><img src="/assets/img/brand/spotify-review-triage.svg" alt="" width="52" height="52" loading="lazy" style="display:block;width:52px;height:52px;border-radius:12px"><img src="/assets/img/brand/ai-visibility-checker.svg" alt="" width="52" height="52" loading="lazy" style="display:block;width:52px;height:52px;border-radius:12px"></div></div><span class="pill">Build marks <em>2026</em></span></div>
          <p class="meta">Giving sixteen builds one family of logos.</p>
        </a>
        <a class="w reveal" href="/arcade">
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
      <p class="notes__lede">Quiet, one typeface, real work as the picture.</p>

      <div class="notes__grid">
        <details class="ncard ncard--color">
          <summary><p class="ncard__k"><i aria-hidden="true"></i>Color</p>
          <h3>Color follows the content, so the page stays neutral</h3><span class="ncard__more" aria-hidden="true">Read more</span></summary>
          <p class="notes__cap">Light, then dark. Tokens from <code>v-stamp.css</code>.</p>
          <ul class="swl">
            <li><span class="sw"><i style="background:#161618"></i><i style="background:#f5f5f7"></i></span><span class="swl__t"><b>ink</b> text</span><span class="swl__h"><code>#161618</code> / <code>#f5f5f7</code></span></li>
            <li><span class="sw"><i style="background:#6e6e73"></i><i style="background:#a1a1a6"></i></span><span class="swl__t"><b>ink-2</b> secondary text</span><span class="swl__h"><code>#6e6e73</code> / <code>#a1a1a6</code></span></li>
            <li><span class="sw"><i style="background:#ffffff"></i><i style="background:#0b0b0c"></i></span><span class="swl__t"><b>bg</b> page</span><span class="swl__h"><code>#ffffff</code> / <code>#0b0b0c</code></span></li>
            <li><span class="sw"><i style="background:rgba(0,0,0,.08)"></i><i style="background:rgba(255,255,255,.10)"></i></span><span class="swl__t"><b>line</b> hairlines</span><span class="swl__h"><code>rgba(0,0,0,.08)</code> / <code>rgba(255,255,255,.10)</code></span></li>
            <li><span class="sw"><i style="background:rgba(0,0,0,.05)"></i><i style="background:rgba(255,255,255,.08)"></i></span><span class="swl__t"><b>fill</b> active tab, hover</span><span class="swl__h"><code>rgba(0,0,0,.05)</code> / <code>rgba(255,255,255,.08)</code></span></li>
            <li><span class="sw"><i style="background:#0a66d6"></i><i style="background:#4ea1ff"></i></span><span class="swl__t"><b>link</b> active link</span><span class="swl__h"><code>#0a66d6</code> / <code>#4ea1ff</code></span></li>
            <li><span class="sw"><i style="background:#30b158"></i><i style="background:#30b158"></i></span><span class="swl__t"><b>ok</b> live status dot</span><span class="swl__h"><code>#30b158</code> / <code>#30b158</code></span></li>
          </ul>
          <div class="grads">
            <div><i style="background:linear-gradient(180deg,#bfdcf7 0%,#dcecfb 22%,#f2f8fe 48%,#ffffff 72%)"></i><span>Sky, light: <code>#bfdcf7</code> to <code>#dcecfb</code> to <code>#f2f8fe</code> to white, with soft white clouds</span></div>
            <div><i style="background:linear-gradient(180deg,#0f1a2e 0%,#0d1424 30%,#0b0e15 55%,#0b0b0c 75%)"></i><span>Night sky, dark: <code>#0f1a2e</code> to <code>#0b0b0c</code>, with faint clouds</span></div>
          </div>
          <p>Each project sits on its own soft gradient stage, so the work supplies the color. Everything else stays neutral. The page opens on a sky: soft blue overhead, a few clouds, fading to white behind the work. I like that blue. It stays calm, not loud, feels light and airy, and keeps the black and white from my brand exploration from feeling stark.</p>
        </details>

        <details class="ncard ncard--type">
          <summary><p class="ncard__k"><i aria-hidden="true"></i>Type</p>
          <h3>One typeface, Poppins, set mostly at regular weight</h3><span class="ncard__more" aria-hidden="true">Read more</span></summary>
          <p class="notes__cap">400, 500 and 600 are loaded. I kept Poppins instead of switching to the SF system font. Its round, geometric letters feel friendly, not corporate. One family everywhere keeps the focus on the work, and it has carried every version of this site.</p>
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
          </table>
          <p>The only other letters are the 김채운 strip at the top. It is brushed with East Sea Dokdo outlines drawn inline, so it costs no font download.</p>
        </details>

        <details class="ncard ncard--pages">
          <summary><p class="ncard__k"><i aria-hidden="true"></i>Structure</p>
          <h3>Pages you explore, with the work as the picture</h3><span class="ncard__more" aria-hidden="true">Read more</span></summary>
          <ul class="bul">
            <li>Pill tabs for Builds, Work and About, routed by the URL hash. Builds opens first.</li>
            <li>Every project is a framed artifact: a real screenshot, a card, a gauge.</li>
            <li>A live Berkeley clock and a day or night icon in the footer.</li>
            <li>Light and dark themes, saved in the browser.</li>
          </ul>
          <p class="notes__cap" style="margin-top:18px">Shapes and motion</p>
          <ul class="bul">
            <li>Cards 24px radius. Content width 1200px.</li>
            <li>Hover easing <code>cubic-bezier(.32, .72, 0, 1)</code>.</li>
            <li>Frosted blur on small tiles only. Everything else is a plain surface with a hairline.</li>
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
        <span><code>CHANGELOG: %%CHANGELOG%%</code></span>
      </div>
    </div>
  </footer>

%%LIVE_DIALOG%%
  <script src="/assets/js/main.js?v=%%V%%"></script>
  <script src="/assets/js/play.js?v=%%V%%" defer></script>
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

    // deep links: #builds (default), #work, #about, or a section inside About such as #experience
    function fromHash() {
      var h = location.hash.slice(1);
      if (h === 'contact') h = 'elsewhere'; // old desktop-page links
      var el = h && document.getElementById(h);
      if (THESIS[h]) show(h);
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


STAMP = (STAMP.replace("%%WRITING_ESSAYS%%", _writing_essays())
              .replace("%%WRITING_READING%%", _writing_reading())
              .replace("%%V%%", V)
              .replace("%%INK%%", INK_DEFS)
              .replace("%%BRANDSEAL%%", seal("cal--card", label=False))
              .replace("%%SEAL%%", seal())
              .replace("%%SEAL_SMALL%%", seal(label=False))
              .replace("%%SNAKE%%", _snake())
              .replace("%%CHANGELOG%%", STAMP_CHANGELOG)
              .replace("%%THEME_COLOR%%", THEME_COLOR)
              .replace("%%LIVE_DIALOG%%", LIVE_DIALOG)
              .replace("%%LIVE_SCRIPT%%", LIVE_SCRIPT)
              .replace("%%LIVE_AVC%%", live_button("ai-visibility-checker"))
              .replace("%%LIVE_TALLY%%", live_button("tally"))
              .replace("%%LIVE_PALETTE_GENERATOR%%", live_button("palette-generator"))
              .replace("%%LIVE_TYPERACE%%", live_button("typerace"))
              .replace("%%LIVE_NETWORKING_TRACKER%%", live_button("networking-tracker"))
              .replace("%%LIVE_SPOTIFY%%", live_button("spotify-review-triage"))
              .replace("%%LIVE_WEB_ANATOMY%%", live_button("web-anatomy")))
assert "%%" not in STAMP, "unreplaced token"

# Each card's pill leads with the build's color-seal mark, found from the page the card links to.
# The name gets its own span so it can truncate on narrow cards instead of being clipped.
def _pill_mark(m):
    mark = build_mark(m.group(2), "pill__mark", 18)
    return m.group(1) + (f'{mark}<span class="pill__name">{m.group(3)}</span>' if mark else m.group(3))

STAMP = re.sub(r'(href="/(?:projects/)?([a-z0-9-]+)"[^>]*>\s*<div class="stage"(?:(?!</a>).)*?<span class="pill">)([^<]*?)(?=\s*<em>|</span>)',
               _pill_mark, STAMP, flags=re.S)

# ----------------------------------------------------------------------------
# Arcade page, in the same chrome as the project pages
# ----------------------------------------------------------------------------

ARCADE_ICONS = build_icons("arcade", "https://chaekim-portfolio.vercel.app")

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
    "A public changelog. This page is the first step.",
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
{CONSIDERING}
        </ul>
        <p class="updated">Last updated October 14, 2026.</p>
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
        f.write(page)
    print("wrote", name)
