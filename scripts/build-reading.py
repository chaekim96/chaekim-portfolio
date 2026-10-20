#!/usr/bin/env python3
"""Builds /reading (reading.html), Chae's running list of helpful articles.

Add an article:  append one dict to the top of READING below, then run
    python3 scripts/build-reading.py && python3 scripts/build-sitemap.py
Fields: title, author, source, url, added (YYYY-MM-DD), topics (list), summary
(neutral, one sentence), note (Chae's own takeaway; leave "" until written).
Topic filter chips are generated from the topics used. Run with --check to
fail if reading.html is out of date.
"""
import html
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SITE_URL = "https://chaekim-portfolio.vercel.app"
sys.path.insert(0, str(HERE))
from stamp_shared import CASE_HEAD_ASSETS, CASE_TOP, CASE_FOOT, CASE_SCRIPTS  # noqa: E402

# Newest first. Keep summaries neutral and in your own words; never paste article text.
READING = [
    {
        "title": "Product Management is Still All About Telling Stories",
        "author": "Josh Elman",
        "source": "a16z newsletter",
        "url": "https://www.a16z.news/p/product-management-is-still-all-about",
        "added": "2026-10-14",
        "topics": ["Product management", "AI"],
        "summary": "Elman argues that as AI makes building software cheaper and faster, a product manager's core value shifts to judgment about what to build and to communicating a product's purpose, especially through onboarding.",
        "note": "",
    },
    {
        "title": "A Product Manager's Job",
        "author": "Josh Elman",
        "source": "Medium",
        "url": "https://joshelman.medium.com/a-product-managers-job-63c09a43d0ec",
        "added": "2026-10-14",
        "topics": ["Product management"],
        "summary": "A short essay on what a product manager is responsible for, framing the job as helping a team ship the right product for users and breaking it into five smaller parts.",
        "note": "",
    },
    {
        "title": "My Blueprint",
        "author": "Josh Elman",
        "source": "Medium",
        "url": "https://joshelman.medium.com/my-blueprint-9693a6059a1a",
        "added": "2026-10-14",
        "topics": ["Working style", "Career"],
        "summary": "Elman shares his own personal blueprint, a written outline of how he works and his quirks, inspired by a friend's essay on the practice.",
        "note": "",
    },
    {
        "title": "51",
        "author": "Josh Elman",
        "source": "Medium",
        "url": "https://joshelman.medium.com/51-7fbfb877e869",
        "added": "2026-10-14",
        "topics": ["Career"],
        "summary": "",  # TODO: Medium blocked fetching; title taken from the URL slug. Confirm title and write a one-sentence summary.
        "note": "",
    },
]

CSS = """
  .reading__lede { max-width: 60ch; color: var(--ink-2); line-height: 1.6; margin-top: 12px; }
  .rl-filters { display: flex; flex-wrap: wrap; gap: 6px; margin: 28px 0 8px; }
  .rl-chip { padding: 6px 14px 5px; border-radius: 999px; font-size: 14px; color: var(--ink-2); box-shadow: inset 0 0 0 1px var(--line); }
  .rl-chip:hover { color: var(--ink); background: var(--fill-2); }
  .rl-chip[aria-pressed="true"] { color: var(--ink); background: var(--fill); font-weight: 500; }
  .rl-list { list-style: none; margin: 0; padding: 0; }
  .rl-item { padding: 24px 0; border-top: 1px solid var(--line); }
  .rl-item[hidden] { display: none; }
  .rl-item h2 { font-size: 19px; font-weight: 500; line-height: 1.35; margin: 0; }
  .rl-item h2 a { color: var(--ink); }
  .rl-item h2 a:hover { text-decoration: underline; text-underline-offset: 3px; }
  .rl-by { margin: 6px 0 0; font-size: 14px; color: var(--ink-2); }
  .rl-sum { margin: 12px 0 0; max-width: 64ch; line-height: 1.6; }
  .rl-notes { margin: 10px 0 0; max-width: 64ch; font-size: 14px; color: var(--ink-2); }
  .rl-notes b { color: var(--ink); font-weight: 500; }
  .rl-tags { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 12px; }
  .rl-tags span { font-size: 12px; padding: 2px 10px; border-radius: 999px; background: var(--fill); color: var(--ink-2); }
  .rl-count { font-size: 13px; color: var(--ink-2); margin: 0 0 4px; }
"""

SCRIPT = """  <script>
    (function () {
      var chips = [].slice.call(document.querySelectorAll('.rl-chip'));
      var items = [].slice.call(document.querySelectorAll('.rl-item'));
      var count = document.getElementById('rl-count');
      function apply(topic) {
        var n = 0;
        chips.forEach(function (c) { c.setAttribute('aria-pressed', String(c.dataset.topic === topic)); });
        items.forEach(function (li) {
          var show = topic === 'all' || li.dataset.topics.split('|').indexOf(topic) > -1;
          li.hidden = !show; if (show) n++;
        });
        count.textContent = n + (n === 1 ? ' article' : ' articles');
      }
      chips.forEach(function (c) { c.addEventListener('click', function () { apply(c.dataset.topic); }); });
      apply('all');
    })();
  </script>"""


def esc(s):
    return html.escape(s, quote=True)


def item(a):
    tags = "".join(f"<span>{esc(t)}</span>" for t in a["topics"])
    summary = esc(a["summary"]) if a["summary"] else '<span class="confirm">[CONFIRM: summary pending]</span>'
    note = esc(a["note"]) if a["note"] else "<i>(add your own takeaway)</i>"
    return (f'      <li class="rl-item" data-topics="{esc("|".join(a["topics"]))}">\n'
            f'        <h2><a href="{esc(a["url"])}" target="_blank" rel="noopener">{esc(a["title"])} ↗</a></h2>\n'
            f'        <p class="rl-by">{esc(a["author"])} · {esc(a["source"])} · added <time datetime="{a["added"]}">{a["added"]}</time></p>\n'
            f'        <p class="rl-sum">{summary}</p>\n'
            f'        <p class="rl-notes"><b>My notes:</b> {note}</p>\n'
            f'        <div class="rl-tags">{tags}</div>\n'
            f'      </li>')


def build():
    topics = sorted({t for a in READING for t in a["topics"]})
    chips = '<button class="rl-chip" type="button" data-topic="all" aria-pressed="true">All</button>' + "".join(
        f'<button class="rl-chip" type="button" data-topic="{esc(t)}" aria-pressed="false">{esc(t)}</button>' for t in topics)
    items = "\n".join(item(a) for a in READING)
    desc = "A running list of articles Chae Kim has found helpful, organized by topic."
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Reading list · Chae Kim - Portfolio</title>
  <meta name="description" content="{desc}">
  <meta property="og:title" content="Reading list · Chae Kim - Portfolio">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="website">
  <meta property="og:image" content="{SITE_URL}/assets/img/og-card.png">
  <link rel="canonical" href="{SITE_URL}/reading">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{CASE_HEAD_ASSETS}
  <style>{CSS}</style>
</head>
<body class="v v-stamp case">
  <a class="skip" href="#main">Skip to content</a>
{CASE_TOP}

  <main id="main">
    <section class="case-hero wrap">
      <a class="case-hero__back" href="/">← Home</a>
      <p class="eyebrow">Reading list</p>
      <h1 class="case-hero__title">Articles that <em>helped</em>.</h1>
      <p class="reading__lede">A running list of things I've read that were worth keeping, with a line on what each is about and room for my own notes. Newest first.</p>
    </section>

    <section class="wrap">
      <div class="rl-filters" role="group" aria-label="Filter by topic">{chips}</div>
      <p class="rl-count" id="rl-count" aria-live="polite"></p>
      <ul class="rl-list">
{items}
      </ul>
    </section>
  </main>

{CASE_FOOT}
{CASE_SCRIPTS}
{SCRIPT}
</body>
</html>
"""


if __name__ == "__main__":
    out = ROOT / "reading.html"
    new = build()
    if "--check" in sys.argv:
        sys.exit(0 if out.exists() and out.read_text(encoding="utf-8") == new else "reading.html is out of date")
    out.write_text(new, encoding="utf-8")
    print("wrote reading.html")
