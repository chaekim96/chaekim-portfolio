#!/usr/bin/env python3
"""Builds the on-site essay pages in projects/ from the plain-text sources in scripts/writing/.

Usage:  python3 scripts/build-writing.py            (add --check to fail if a page is out of date)
Source format: paragraphs separated by a blank line; "## " starts a heading; **bold** marks bold runs.
The first paragraph of the source is the essay title and is dropped from the body (it becomes the page title).
A paragraph that is wholly a quotation (starts with a straight or curly double quote) is set as a block quote.
Essay wording is Chae's own and is never edited here: only the markup around it.
"""
import html
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SITE_URL = "https://chaekim-portfolio.vercel.app"
sys.path.insert(0, str(HERE))
from stamp_shared import CASE_HEAD_ASSETS, CASE_TOP, CASE_FOOT, CASE_SCRIPTS  # noqa: E402

ESSAYS = [
    dict(
        slug="preinstalled-apps",
        title="What’s the Point of Preinstalled Apps?",
        desc="What if a new iPhone greeted you with Siri instead of pages of apps? On Siri becoming the operating system, and what that means for apps, Apple, and the App Store.",
        dek="Reimagining Siri as the operating system.",
        published="2026-10",
        date_label="October 2026",
        end='<a href="/projects/voiceprompter">The teleprompter in this essay</a> · <a href="/projects/siri-reimagined">The design concept: Siri, Reimagined</a>',
    ),
]

# Illustrations, placed after the paragraph whose text matches the key. Built from the essay's own examples.
FIGURES = {
    "preinstalled-apps": {
        "Instead of being greeted by pages of preinstalled apps, you're greeted by Siri.": """        <figure class="fig fig-phones" aria-label="Two phones: one opens to pages of preinstalled apps, the other opens to Siri building an expense tracker on request">
          <div class="fig-phones__row">
            <div class="phone"><div class="phone__screen phone__screen--apps">""" + "".join('<i></i>' for _ in range(20)) + """</div><span class="phone__label">Today: pages of preinstalled apps</span></div>
            <div class="phone"><div class="phone__screen phone__screen--siri">
              <span class="siri-orb" aria-hidden="true"></span>
              <p class="bubble">Make me a simple expense tracker for my trip to Japan.</p>
              <div class="mini-app"><b>Japan trip</b><span>Expenses</span><ul><li><em>Train pass</em><em>¥29,650</em></li><li><em>Ramen</em><em>¥1,200</em></li><li><em>Museum</em><em>¥2,000</em></li></ul><button type="button" tabindex="-1">+ Add</button></div>
            </div><span class="phone__label">Reimagined: greeted by Siri</span></div>
          </div>
          <figcaption>Instead of choosing from apps someone else built, you ask for the one you need. Amounts are illustrative.</figcaption>
        </figure>""",
        "The agent sits on top of them.": """        <figure class="fig fig-stack" aria-label="Three layers: primitives at the bottom, the agent in the middle, and the interface you asked for on top">
          <div class="stack__layer stack__layer--ui"><span class="stack__k">Interface</span><span>Built on request: a tracker, a timer, a teleprompter</span></div>
          <div class="stack__layer stack__layer--agent"><span class="stack__k">Agent</span><span>Siri, turning what you're trying to do into software</span></div>
          <div class="stack__layer stack__layer--prims"><span class="stack__k">Primitives</span><span class="chips"><i>camera</i><i>location</i><i>payments</i><i>storage</i><i>messaging</i><i>identity</i><i>sensors</i><i>compute</i></span></div>
          <figcaption>Siri becomes the operating system: the platform supplies primitives, the agent assembles them.</figcaption>
        </figure>""",
        "Tomorrow, it might be the **intent**.": """        <figure class="fig fig-shift" aria-label="The unit of computing shifts from the application to the intent">
          <div class="shift__col"><span class="stack__k">Today</span><b>Application</b><p class="bubble bubble--muted">What's the best app for X?</p></div>
          <span class="shift__arrow" aria-hidden="true">→</span>
          <div class="shift__col"><span class="stack__k">Tomorrow</span><b>Intent</b><p class="bubble">I need X.</p></div>
        </figure>""",
    },
}


def inline(text):
    out = html.escape(text, quote=False)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", out)


def body_html(source, figures=None):
    figures = dict(figures or {})
    paras = [p.strip() for p in source.strip().split("\n\n") if p.strip()][1:]  # drop the title paragraph
    out = []
    for p in paras:
        fig = figures.pop(p, None)
        if p.startswith("## "):
            out.append(f"        <h2>{inline(p[3:])}</h2>")
        elif re.match(r'^(\*\*)?["“]', p) and re.search(r'["”](\*\*)?$', p):
            out.append(f"        <blockquote>{inline(p)}</blockquote>")
        else:
            out.append(f"        <p>{inline(p)}</p>")
        if fig:
            out.append(fig)
    if figures:
        raise SystemExit(f"figure anchors not found in the essay: {list(figures)}")
    return "\n".join(out)


def words(source):
    return len(re.sub(r"\*\*|## ", "", source).split())


def render(e):
    source = (HERE / "writing" / f"{e['slug']}.txt").read_text(encoding="utf-8")
    mins = max(1, round(words(source) / 220))
    title, desc = html.escape(e["title"]), html.escape(e["desc"])
    url = f"{SITE_URL}/projects/{e['slug']}"
    ld = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": e["title"],
        "description": e["desc"],
        "url": url,
        "mainEntityOfPage": url,
        "datePublished": e["published"],
        "image": f"{SITE_URL}/assets/img/og-sky.png",
        "author": {"@type": "Person", "name": "Chae Kim", "alternateName": "Chae Woon Kim", "url": f"{SITE_URL}/"},
    }
    ldj = json.dumps(ld, ensure_ascii=False, indent=2).replace("</", "<\\/")
    ldj = '  <script type="application/ld+json">\n' + "\n".join("  " + l for l in ldj.splitlines()) + "\n  </script>"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} · Chae Kim - Portfolio</title>
  <meta name="description" content="{desc}">
  <meta name="author" content="Chae Kim">
  <meta property="og:title" content="{title} · Chae Kim - Portfolio">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="article">
  <meta property="og:image" content="{SITE_URL}/assets/img/og-sky.png">
  <link rel="canonical" href="{url}">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{CASE_HEAD_ASSETS}
{ldj}
</head>
<body class="v v-stamp case sec-writing">
  <a class="skip" href="#main">Skip to content</a>
{CASE_TOP}

  <main id="main">
    <section class="case-hero wrap">
      <a class="case-hero__back" href="/#writing">← Writing</a>
      <p class="eyebrow">essay · siri, reimagined</p>
      <h1 class="case-hero__title">{title}</h1>
      <p class="essay-dek">{html.escape(e['dek'])}</p>
      <p class="meta-line"><b>By</b> Chae Kim · <time datetime="{e['published']}">{e['date_label']}</time> · {mins} min read</p>
    </section>

    <section class="wrap essay-wrap">
      <article class="prose essay">
{body_html(source, FIGURES.get(e['slug']))}
        <p class="essay__end">{e['end']}</p>
      </article>
    </section>
  </main>

{CASE_FOOT}
{CASE_SCRIPTS}
</body>
</html>
"""


def main():
    check = "--check" in sys.argv[1:]
    stale = []
    for e in ESSAYS:
        out, path = render(e), ROOT / "projects" / f"{e['slug']}.html"
        if check:
            if not path.exists() or path.read_text(encoding="utf-8") != out:
                stale.append(e["slug"])
        else:
            path.write_text(out, encoding="utf-8")
            print("wrote", path.relative_to(ROOT))
    if stale:
        sys.exit(f"out of date, run python3 scripts/build-writing.py: {stale}")


if __name__ == "__main__":
    main()
