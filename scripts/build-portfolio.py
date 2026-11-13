#!/usr/bin/env python3
"""Builds /projects/portfolio: how this site got built, its decisions and its backlog.

Usage:  python3 scripts/build-portfolio.py
"""
import os

from stamp_shared import SITE_URL, finish, CASE_HEAD_ASSETS, CASE_TOP, CASE_FOOT, CASE_SCRIPTS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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
  <meta property="og:image" content="{SITE_URL}/assets/img/og-paper.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <link rel="canonical" href="{SITE_URL}/projects/portfolio">
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

with open(os.path.join(ROOT, "projects", "portfolio.html"), "w", encoding="utf-8", newline="\n") as f:
    f.write(finish(PORTFOLIO_PAGE))
print("wrote projects/portfolio.html")
