#!/usr/bin/env python3
"""Builds /playbook (playbook.html): how I sound, how I look, and the rules I keep.

/brand covers the build marks. This page covers the words and the rules around them, and links to /brand
for anything about marks. Only rules that are already true on the site go here.

Usage:  python3 scripts/build-playbook.py
"""
import html
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from stamp_shared import SITE_URL, CASE_HEAD_ASSETS, CASE_TOP, CASE_FOOT, CASE_SCRIPTS, seal, build_mark  # noqa: E402

e = html.escape
TITLE = "Playbook"
HEADLINE = "How I sound, how I look, and what I never fake."
DESC = "My brand playbook: the voice, the colors and type, the rules of truth, and the checks before anything ships."
SHARE = f"{SITE_URL}/assets/img/og-paper.png"
UPDATED = "November 10, 2026"

TOC = [("core", "Core"), ("voice", "Voice"), ("layers", "Two layers"), ("color", "Color"), ("type", "Type"),
       ("name", "The name"), ("imagery", "Imagery and motion"), ("truth", "Rules of truth"),
       ("templates", "Where it shows up"), ("check", "Before it ships")]


def rules(items):
    return '<ul class="pb-rules">' + "".join(f"<li><b>{h}</b> {t}</li>" for h, t in items) + "</ul>"


def section_core():
    lines = [("Builds", "I like to build things, from startups to card games."),
             ("Work", "I run the operations behind the idea."),
             ("The ask", "Let's chat.")]
    rows = "".join(f'<div class="pb-line"><span>{k}</span><p>{v}</p></div>' for k, v in lines)
    return f'''
        <h2 id="core">The work is the proof. A conversation is the goal.</h2>
        <p>This site is for anyone who wants to know who I am. I don't pitch. I show what I built and invite a chat.</p>
        <div class="pb-lines">{rows}</div>
        <p>These three lines run on the site. Every other piece of copy should sound like it belongs next to them.</p>'''


def section_voice():
    pairs = [("Things I shipped", "Three to try first",
              "The real Builds header. It tells you what to do, not how much I did."),
             ("17 checks, 95 score, 0.1s fetch", "Can AI find, read and cite your page?",
              "The right line is the real AI Visibility Checker headline, with the numbers underneath. I wrote the left line for contrast."),
             ("Typography — a considered system", "Poppins for words, a plain monospace for facts",
              "The right line is a real design-notes header. I wrote the left one: vague, and it has an em dash.")]
    cards = "".join(f'''
          <div class="pb-pair"><div><span class="pb-no">Don't</span><s>{e(a)}</s></div><div><span class="pb-yes">Do</span><p>{e(b)}</p></div><p class="pb-why">{e(w)}</p></div>'''
                    for a, b, w in pairs)
    return f'''
        <h2 id="voice">Short, concrete, and in my own words.</h2>
        {rules([("Headlines are sentences, never statistics.", "Numbers go in the line underneath."),
                ("Short and punchy.", "One idea per sentence. Cut the warm-up."),
                ("No em dashes.", "Use a period or a comma."),
                ("Two words I don't use as headers:", "“sold” and “things I shipped.”")])}
        <div class="pb-pairs">{cards}
        </div>'''


def section_layers():
    return f'''
        <h2 id="layers">Quiet for me, loud for the builds, one line between them.</h2>
        <div class="pb-layers">
          <div class="pb-layer">{seal("pb-cal", label=False)}<p class="pb-tag">Stamp · me</p><p>Quiet colors and a brush name. The brush is for my name only. It never goes on a build.</p></div>
          <div class="pb-layer">{build_mark("tally", "pb-tile", 48, themed=True)}<p class="pb-tag">Electric · the builds</p><p>Lit tiles, one color per build. Each one speaks for what the build does.</p></div>
        </div>
        <p class="pb-endorse"><i aria-hidden="true"></i>A Chae Kim build</p>
        <p>The seal-red square and that line are the only bridge between the two. The mark rules live on <a href="/brand">/brand</a>, so this page links there instead of repeating them.</p>'''


def section_color():
    sw = [("Ink", "#111110", "Headlines and body text."),
          ("Ink 2", "#5f5b53", "Captions and secondary text."),
          ("Accent", "#4a3fd1", "Active tab, links and focus. At night: #9b86ff."),
          ("Live", "#30d158", "Only for “this is live.” Never decoration."),
          ("Seal", "#c63d2f", "Only the endorsement square."),
          ("Paper", "#fbf8f1", "The page. At night: #121211.")]
    cells = "".join(f'<div class="pb-sw"><i style="background:{h}"></i><b>{n}</b><code>{h}</code><span>{u}</span></div>' for n, h, u in sw)
    return f'''
        <h2 id="color">Color follows the content, so the page stays neutral.</h2>
        <p>That line is the real design-notes header. The page stays paper and ink, so screenshots and build marks carry the color.</p>
        <div class="pb-grad" role="img" aria-label="Paper wash from warm cream to paper"></div>
        <p class="pb-cap">Stamp Ink: #f3ecdd, #f7f2e7, then paper #fbf8f1. At night (Night Press): #1d1b18 into #121211.</p>
        <div class="pb-swatches">{cells}</div>
        {rules([("Check dark mode every time.", "Every color has a night value, and the site has a theme toggle.")])}'''


def section_type():
    spec = [("Poppins 600 · headlines", '<span class="pb-t600">I like to build things.</span>'),
            ("Poppins 400 · body", '<span>The checker reads the page the way crawlers do, without running JavaScript.</span>'),
            ("Monospace · facts", '<span class="pb-mono">Role Product owner and builder · Timeline October 2026</span>')]
    rows = "".join(f'<div class="pb-spec"><span class="pb-k">{k}</span>{v}</div>' for k, v in spec)
    return f'''
        <h2 id="type">Poppins for words, a plain monospace for facts.</h2>
        <p>I kept Poppins instead of the SF system font. Its round, geometric letters feel friendly, not corporate, and one family for every word keeps the focus on the work.</p>
        <div class="pb-specs">{rows}</div>
        <p>Build names follow three tiers of their own: Products in Poppins 600, Tools in JetBrains Mono 500 and Studies in Fraunces italic. See <a href="/brand#type">/brand</a>.</p>'''


def section_name():
    return f'''
        <h2 id="name">A brush, because brush strokes show a person.</h2>
        <p>I swapped the official 도장 seal for brush calligraphy. A seal is an official object. Brush strokes carry motion and small imperfections. The whole story is in the <a href="/projects/personal-brand">personal brand case study</a>.</p>
        {rules([("My name only.", "Never on a product, a build mark, or someone else's work."),
                ("Next step:", "brush 김채운 by hand and trace it, so the mark is mine alone instead of a public font.")])}'''


def section_imagery():
    return f'''
        <h2 id="imagery">The work is the picture.</h2>
        {rules([("Real screenshots only.", "Captured from the real product in light mode. If a capture comes from a test run, the caption says so."),
                ("No stock photos and no other companies' logos.", "Work cases get plain ink tiles instead of company marks."),
                ("Motion happens once and means something.", "The seal stamps once per visit. Marks move only their white detail, and only on hover."),
                ("Less motion when asked.", "Everything sits still if your device asks for reduced motion.")])}'''


def section_truth():
    return f'''
        <h2 id="truth">If I can't show it, I don't say it.</h2>
        {rules([("Real artifacts only.", "No invented numbers, quotes or results."),
                ("Reasons are mine.", "A decision lists only the reasons I actually gave."),
                ("Credit partners plainly.", "Chris Jackson is credited as my Lucent co-founder and partner on the method."),
                ("Say where things stand.", "Lucent's advisory work is on pause, and the site says so.")])}'''


def section_templates():
    rows = [("This site", "Sky wash, Poppins, the brushed name and the case page kit.", "Done", "done"),
            ("Build marks and /brand", "A mark for every build, 16 pixel icons, line icons and the endorsement.", "Done", "done"),
            ("Email signature", "Name, one line, the site link and a small mark.", "Next", "next"),
            ("LinkedIn banner and GitHub header", "Sky wash, the brushed name and one line.", "Next", "next"),
            ("Slides", "Title, section, case and closing slides.", "Next", "next")]
    items = "".join(f'<li><div><b>{n}</b><span>{d}</span></div><em class="pb-st pb-st--{c}">{s}</em></li>' for n, d, s, c in rows)
    return f'''
        <h2 id="templates">Where the brand shows up, and what's next.</h2>
        <ul class="pb-tpl">{items}</ul>'''


def section_check():
    checks = ["Every headline is a sentence, with no statistic in it.",
              "No em dashes, and none of the words I don't use as headers.",
              "Every number, quote and screenshot is real, and I can point to where it came from.",
              "Colors come from the palette. Green only means live.",
              "The brushed name appears only as my name.",
              "Checked in dark mode and at phone width.",
              "A new build has its mark, its case page and the endorsement line."]
    items = "".join(f"<li>{c}</li>" for c in checks)
    return f'''
        <h2 id="check">Seven checks before anything goes out.</h2>
        <ol class="pb-check">{items}</ol>'''


CSS = """
    .pb-rules { list-style: none; padding: 0; margin: 14px 0; display: grid; gap: 10px; }
    .pb-rules li { padding-left: 20px; position: relative; }
    .pb-rules li::before { content: ""; position: absolute; left: 2px; top: .62em; width: 8px; height: 8px; border-radius: 2px; background: var(--accent); }
    .pb-rules b { font-weight: 600; }
    .pb-lines, .pb-pairs, .pb-specs { display: grid; gap: 10px; margin: 16px 0; }
    .pb-line, .pb-spec { display: grid; grid-template-columns: 120px 1fr; gap: 16px; align-items: baseline; border: 1px solid var(--line); border-radius: 14px; padding: 14px 16px; }
    .pb-line span, .pb-k { font: 500 12px/1.4 'JetBrains Mono', ui-monospace, monospace; color: var(--ink-2); }
    .pb-line p { margin: 0; font-size: 18px; font-weight: 500; line-height: 1.35; }
    .pb-pair { display: grid; grid-template-columns: 1fr 1fr; border: 1px solid var(--line); border-radius: 14px; overflow: hidden; }
    .pb-pair > div { padding: 14px 16px; display: grid; gap: 6px; align-content: start; min-width: 0; }
    .pb-pair > div + div { border-left: 1px solid var(--line); }
    .pb-pair p { margin: 0; }
    .pb-pair s { color: var(--ink-2); text-decoration-color: #c63d2f; text-decoration-thickness: 1.5px; }
    .pb-no, .pb-yes { font: 600 11px/1 'JetBrains Mono', ui-monospace, monospace; letter-spacing: .08em; text-transform: uppercase; color: #b4261b; }
    .pb-yes { color: #0f7a3b; }
    .pb-why { grid-column: 1 / -1; border-top: 1px solid var(--line); padding: 10px 16px !important; font-size: 14px; color: var(--ink-2); }
    .pb-layers { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 260px), 1fr)); gap: 14px; margin: 16px 0; }
    .pb-layer { border: 1px solid var(--line); border-radius: 16px; padding: 18px; display: grid; gap: 8px; align-content: start; }
    .pb-layer p { margin: 0; font-size: 15px; color: var(--ink-2); }
    .pb-layer .pb-tag { font: 500 12px/1 'JetBrains Mono', ui-monospace, monospace; letter-spacing: .1em; text-transform: uppercase; margin-top: 4px; }
    .pb-cal { width: 30px; height: auto; display: block; }
    .pb-tile { display: block; border-radius: 22%; }
    .pb-endorse { display: inline-flex; align-items: center; gap: 12px; font: 500 13px/1 Poppins, sans-serif; letter-spacing: .14em; text-transform: uppercase; color: var(--ink-2); }
    .pb-endorse i { width: 13px; height: 13px; background: #C63D2F; display: block; }
    .pb-grad { height: 44px; border-radius: 12px; box-shadow: inset 0 0 0 1px var(--line); background: linear-gradient(90deg, #f3ecdd, #f7f2e7 45%, #fbf8f1); margin-top: 14px; }
    .pb-cap { font: 400 12px/1.5 'JetBrains Mono', ui-monospace, monospace; color: var(--ink-2); margin-top: 6px; }
    .pb-swatches { display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 200px), 1fr)); gap: 14px; margin: 16px 0; }
    .pb-sw { display: grid; grid-template-columns: 44px 1fr; column-gap: 12px; row-gap: 1px; align-items: center; }
    .pb-sw i { grid-row: 1 / 4; width: 44px; height: 44px; border-radius: 12px; box-shadow: inset 0 0 0 1px var(--line); align-self: start; }
    .pb-sw b { font-size: 14px; font-weight: 500; }
    .pb-sw code { font: 500 12px 'JetBrains Mono', ui-monospace, monospace; background: none; padding: 0; color: var(--ink-2); }
    .pb-sw span { font-size: 12.5px; line-height: 1.4; color: var(--ink-2); }
    .pb-t600 { font: 600 22px/1.25 Poppins, sans-serif; }
    .pb-mono { font: 400 14px/1.5 'JetBrains Mono', ui-monospace, monospace; }
    .pb-spec > span:last-child { min-width: 0; overflow-wrap: anywhere; }
    .pb-tpl { list-style: none; padding: 0; margin: 16px 0; display: grid; gap: 8px; }
    .pb-tpl li { display: grid; grid-template-columns: 1fr auto; gap: 12px; align-items: center; border: 1px solid var(--line); border-radius: 14px; padding: 12px 16px; }
    .pb-tpl li::before { content: none; display: none; }
    .pb-tpl div { display: grid; gap: 2px; min-width: 0; }
    .pb-tpl span { font-size: 13.5px; color: var(--ink-2); }
    .pb-st { font: 500 11.5px/1 'JetBrains Mono', ui-monospace, monospace; font-style: normal; padding: 6px 9px; border-radius: 999px; white-space: nowrap; border: 1px solid var(--line); color: var(--ink-2); }
    .pb-st--done { border-color: transparent; background: rgba(48, 209, 88, .14); color: #0f7a3b; }
    .pb-check { margin: 14px 0; padding-left: 22px; display: grid; gap: 8px; }
    .pb-updated { font-size: 13px; color: var(--ink-2); margin-top: 28px; }
    [data-theme="dark"] .pb-no, [data-theme="dark"] .pb-pair s { color: #ff8a7d; }
    [data-theme="dark"] .pb-yes, [data-theme="dark"] .pb-st--done { color: #6fdc98; }
    @media (max-width: 600px) {
      .pb-line, .pb-spec { grid-template-columns: 1fr; gap: 6px; }
      .pb-pair { grid-template-columns: 1fr; }
      .pb-pair > div + div { border-left: 0; border-top: 1px solid var(--line); }
    }
"""


def page():
    toc = "\n".join(f'        <a href="#{i}">{t}</a>' for i, t in TOC)
    body = "\n".join(f() for f in (section_core, section_voice, section_layers, section_color, section_type, section_name,
                                   section_imagery, section_truth, section_templates, section_check))
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
  <link rel="canonical" href="{SITE_URL}/playbook">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{CASE_HEAD_ASSETS}
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap">
  <style>{CSS}  </style>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "CreativeWork",
    "name": "{TITLE}",
    "headline": "{e(HEADLINE)}",
    "description": "{e(DESC)}",
    "url": "{SITE_URL}/playbook",
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
      <a class="case-hero__back" href="/brand">← Brand</a>
      <p class="eyebrow">playbook · brand · 2026</p>
      <h1 class="case-hero__title">{e(HEADLINE)}</h1>
      <p class="tldr">The page I open before I write a cover letter, make a slide or ship a build. <a href="/brand">/brand</a> covers the marks. This covers the words and the rules around them.</p>
      <p class="meta-line"><b>Covers</b> Voice, color, type, imagery, rules of truth · <b>Read time</b> Three minutes</p>
    </section>

    <section class="wrap case-body">
      <nav class="toc" aria-label="On this page">
{toc}
      </nav>
      <article class="prose">{body}
        <p class="pb-updated">Last updated {UPDATED}.</p>
      </article>
    </section>
  </main>

{CASE_FOOT}
{CASE_SCRIPTS}
</body>
</html>
'''


if __name__ == "__main__":
    (ROOT / "playbook.html").write_text(page(), encoding="utf-8")
    print("wrote playbook.html")
