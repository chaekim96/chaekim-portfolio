#!/usr/bin/env python3
"""Builds /reading (reading.html): Chae's own essays, plus a running list of helpful articles.

The articles and essays live in scripts/writing_data.py (shared with the homepage Writing tab).
After editing them run build-reading.py, build-home.py and build-sitemap.py.
Topic filter chips are generated from the topics used and only filter READING.
Run with --check to fail if reading.html is out of date.
"""
import html
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SITE_URL = "https://chaekim-portfolio.vercel.app"
sys.path.insert(0, str(HERE))
from writing_data import READING, ESSAYS, pub_label  # noqa: E402
from stamp_shared import CASE_HEAD_ASSETS, CASE_TOP, CASE_FOOT, CASE_SCRIPTS  # noqa: E402

CSS = """
  .reading__lede { max-width: 60ch; color: var(--ink-2); line-height: 1.6; margin-top: 12px; }
  .rl-section { margin-top: 56px; }
  .rl-section h2 { font-size: 22px; font-weight: 500; margin: 0 0 4px; }
  .rl-filters { display: flex; flex-wrap: wrap; gap: 6px; margin: 28px 0 8px; }
  .rl-chip { padding: 6px 14px 5px; border-radius: 999px; font-size: 14px; color: var(--ink-2); box-shadow: inset 0 0 0 1px var(--line); }
  .rl-chip:hover { color: var(--ink); background: var(--fill-2); }
  .rl-chip[aria-pressed="true"] { color: var(--ink); background: var(--fill); font-weight: 500; }
  .rl-list, .es-list { list-style: none; margin: 0; padding: 0; }
  .rl-item, .es-item { padding: 24px 0; border-top: 1px solid var(--line); }
  .rl-item[hidden] { display: none; }
  .rl-item h3, .es-item h3 { font-size: 19px; font-weight: 500; line-height: 1.35; margin: 0; }
  .rl-item h3 a, .es-item h3 a { color: var(--ink); }
  .rl-item h3 a:hover, .es-item h3 a:hover { text-decoration: underline; text-underline-offset: 3px; }
  .es-meta { margin: 6px 0 0; font-size: 14px; color: var(--ink-2); }
  .es-desc { margin: 12px 0 0; max-width: 64ch; line-height: 1.6; }
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
    summary = f'        <p class="rl-sum">{esc(a["summary"])}</p>\n' if a["summary"] else ""
    note = f'        <p class="rl-notes"><b>My notes:</b> {esc(a["note"])}</p>\n' if a["note"] else ""
    return (f'      <li class="rl-item" data-topics="{esc("|".join(a["topics"]))}">\n'
            f'        <h3><a href="{esc(a["url"])}" target="_blank" rel="noopener">{esc(a["title"])} ↗</a></h3>\n'
            f'        <p class="rl-by">{esc(a["author"])} · {esc(a["source"])} · added <time datetime="{a["added"]}">{a["added"]}</time></p>\n'
            f'{summary}{note}'
            f'        <div class="rl-tags">{tags}</div>\n'
            f'      </li>')


def essay(e):
    date = (f' · published <time datetime="{e["published"]}">{pub_label(e["published"])}</time>' if e["published"] else "")
    internal = e.get("internal")
    ext = "" if internal else ' target="_blank" rel="noopener"'
    arrow = "" if internal else " ↗"
    where = "On this site" if internal else "Medium"
    return (f'      <li class="es-item">\n'
            f'        <h3><a href="{esc(e["url"])}"{ext}>{esc(e["title"])}{arrow}</a></h3>\n'
            f'        <p class="es-meta">{where}{date}</p>\n'
            f'        <p class="es-desc">{esc(e["description"])}</p>\n'
            f'      </li>')


def build():
    topics = sorted({t for a in READING for t in a["topics"]})
    essay_items = "\n".join(essay(e) for e in ESSAYS)
    chips = '<button class="rl-chip" type="button" data-topic="all" aria-pressed="true">All</button>' + "".join(
        f'<button class="rl-chip" type="button" data-topic="{esc(t)}" aria-pressed="false">{esc(t)}</button>' for t in topics)
    items = "\n".join(item(a) for a in READING)
    desc = "Essays by Chae Kim, and a running list of articles found helpful, organized by topic."
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Writing &amp; reading · Chae Kim - Portfolio</title>
  <meta name="description" content="{desc}">
  <meta property="og:title" content="Writing &amp; reading · Chae Kim - Portfolio">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="website">
  <meta property="og:image" content="{SITE_URL}/assets/img/og-sky.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <link rel="canonical" href="{SITE_URL}/reading">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{CASE_HEAD_ASSETS}
  <style>{CSS}</style>
</head>
<body class="v v-stamp case sec-about">
  <a class="skip" href="#main">Skip to content</a>
{CASE_TOP}

  <main id="main">
    <section class="case-hero wrap">
      <a class="case-hero__back" href="/">← Home</a>
      <p class="eyebrow">Writing &amp; reading</p>
      <h1 class="case-hero__title">Writing and <em>reading</em>.</h1>
      <p class="reading__lede">My own essays, plus a running list of things I've read that were worth keeping, with a line on what each is about and room for my own notes. Newest first.</p>
    </section>

    <section class="wrap rl-section" aria-labelledby="essays-h">
      <h2 id="essays-h">Essays</h2>
      <ul class="es-list">
{essay_items}
      </ul>
    </section>

    <section class="wrap rl-section" aria-labelledby="reading-h">
      <h2 id="reading-h">Reading list</h2>
      <div class="rl-filters" role="group" aria-label="Filter reading list by topic">{chips}</div>
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
