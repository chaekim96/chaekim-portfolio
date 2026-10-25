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
        desc="If AI can build the app you need in minutes, what is the point of preinstalled apps, and of apps at all?",
        published="2026-10",
        date_label="October 2026",
        end='<a href="/projects/voiceprompter">The teleprompter in this essay</a> · <a href="/projects/siri-reimagined">The design concept: Siri, Reimagined</a>',
    ),
]


def inline(text):
    out = html.escape(text, quote=False)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", out)


def body_html(source):
    paras = [p.strip() for p in source.strip().split("\n\n") if p.strip()][1:]  # drop the title paragraph
    out = []
    for p in paras:
        if p.startswith("## "):
            out.append(f"        <h2>{inline(p[3:])}</h2>")
        elif re.match(r'^(\*\*)?["“]', p) and re.search(r'["”](\*\*)?$', p):
            out.append(f"        <blockquote>{inline(p)}</blockquote>")
        else:
            out.append(f"        <p>{inline(p)}</p>")
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
      <p class="eyebrow">essay · {e['date_label'].lower()}</p>
      <h1 class="case-hero__title">{title}</h1>
      <p class="meta-line"><b>By</b> Chae Kim · <time datetime="{e['published']}">{e['date_label']}</time> · {mins} min read</p>
    </section>

    <section class="wrap essay-wrap">
      <article class="prose essay">
{body_html(source)}
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
