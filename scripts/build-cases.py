#!/usr/bin/env python3
"""Builds the case studies from one template. The copy lives in scripts/projects/<slug>.py.

Usage:  python3 scripts/build-cases.py            (write every page)
        python3 scripts/build-cases.py --check    (write nothing; fail if a page is out of date)
Edits:  change the project's file, re-run, commit the generated HTML.
The page template is SHELL below. (No rendered copy is written: everything in the
repo is deployed, so a copy in projects/ would be a public page.)
"""
import html
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = ROOT / "projects"

# The script name has a hyphen, so it can't be imported as a package; load the sibling module by path.
sys.path.insert(0, str(HERE))
from stamp_shared import (SITE_URL, CASE_HEAD_ASSETS, CASE_TOP, CASE_FOOT, CASE_SCRIPTS, LIVE_APPS, LIVE_DIALOG, LIVE_SCRIPT,  # noqa: E402
                          live_button, build_mark, build_icons, work_mark, mark_color, finish, spark_ready, SPARK_SCRIPT)
import importlib.util  # noqa: E402
import palette_data  # noqa: E402

from projects import BUILDS, CASES, PROJECTS  # noqa: E402

# Chrome (header, footer, stylesheet links, scripts) is shared with the Stamp homepage; see stamp_shared.py.

SITE_ICONS = ('  <link rel="icon" href="/favicon.svg" type="image/svg+xml">\n'
              '  <link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">\n'
              '  <link rel="apple-touch-icon" href="/apple-touch-icon.png">')

SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} · Chae Kim - Portfolio</title>
  <meta name="description" content="{desc}">
  <meta property="og:title" content="{title} · Chae Kim - Portfolio">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="article">
  <meta property="og:image" content="{og_image}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <link rel="canonical" href="{site_url}/projects/{slug}">
{icons}
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{head_assets}
{jsonld}
</head>
<body class="v v-stamp case {sec}{tint_class}"{tint_style}>
  <a class="skip" href="#main">Skip to content</a>
{top}

  <main id="main">
{tint_wash}{switcher}
    <section class="case-hero wrap">
      <a class="case-hero__back" href="{back_href}">← {back_label}</a>
      {mark}<p class="eyebrow">{kicker}</p>
      <h1 class="case-hero__title">{heading}{badge}</h1>
      <p class="tldr">{tldr}</p>
      <p class="meta-line"><b>Role</b> {role} · <b>Team</b> {team} · <b>Timeline</b> {timeline}</p>
{docs}    </section>

    <section class="wrap case-cover-wrap">
      <div class="stage case-cover {cover_class}" style="--g: var(--g-{grad})">{cover}{live}</div>
    </section>

    <section class="wrap case-body">
      <nav class="toc" aria-label="On this page">
{toc}
      </nav>
      <article class="prose">
{body}
      </article>
    </section>

    <section class="next wrap" aria-label="{next_label}">
      <div class="next__grid">
        <a href="{prev_href}">{prev_mark}<span><small>← Previous {next_noun}</small><strong>{prev_title}</strong></span></a>
        <a class="next__forward" href="{next_href}">{next_mark}<span><small>Next {next_noun} →</small><strong>{next_title}</strong></span></a>
      </div>
    </section>
  </main>

{foot}
{live_dialog}{scripts}{live_script}
</body>
</html>
"""

BUILD_SLUGS = set(BUILDS)

# Sections in page order; a section whose content is empty is left out of the TOC and the body.
SECTIONS = (("problem", "The problem"), ("requirements", "Product requirements"),
            ("did", "What I did"), ("results", "Results"),
            ("milestones", "Milestones and next steps"), ("iterations", "Iterations and decisions"),
            ("forks", "Calls I made, and what I passed on"),
            ("differently", "What I'd do differently"), ("artifacts", "Artifacts"))
REQUIRED = ("slug", "title", "kicker", "heading", "desc", "tldr", "role", "team", "timeline",
            "cover", "problem", "did", "results")
DEFAULTS = dict(badge="", cover_class="", differently="", artifacts="",
                requirements="", milestones="", iterations="", forks="")
PLAIN_TEXT = ("title", "kicker", "role", "team", "timeline")  # text only, never HTML: escape on output


# ---------------------------------------------------------------------------
# Case page kit: switcher, per-product tint, decision forks, documents row
# ---------------------------------------------------------------------------

def _load_sibling(filename, name):
    """Load a sibling script whose file name has a hyphen (so it can't be imported normally)."""
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

# Builds that have a color-seal mark but no case study of their own sit after the case studies in the switcher.
EXTRA_BUILDS = (("arcade", "Arcade", "/arcade"),)

def _group(slug):
    """(label, noun, [(slug, title, href)]) for the group a page belongs to: builds, or work."""
    builds = [(c["slug"], c["title"], f"/projects/{c['slug']}") for c in CASES if c["slug"] in BUILD_SLUGS] + list(EXTRA_BUILDS)
    if slug in {b[0] for b in builds}:
        return "Builds", "build", builds
    return "Work", "work", [(c["slug"], c["title"], f"/projects/{c['slug']}") for c in CASES if c["slug"] not in BUILD_SLUGS]

def _tile(slug, cls, size):
    return build_mark(slug, cls, size) or work_mark(slug, cls, size)

def render_switcher(slug):
    """A sticky row of marks to hop between builds. Work cases have no marks, so they get their ink tiles."""
    label, _noun, items = _group(slug)
    cur = next(t for s_, t, _h in items if s_ == slug)
    lis = []
    for s_, title, href in items:
        here = ' aria-current="page"' if s_ == slug else ""
        lis.append(f'<li><a href="{href}"{here} data-name="{html.escape(title)}" aria-label="{html.escape(title)}">{_tile(s_, "switcher__mark", 32)}</a></li>')
    return (f'    <nav class="switcher wrap" aria-label="{"Jump to another build" if label == "Builds" else "Jump to other work"}">\n'
            f'      <div class="switcher__bar">\n'
            f'        <a class="switcher__k" href="/#{label.lower()}">{label}</a>\n'
            f'        <ul class="switcher__row">{"".join(lis)}</ul>\n'
            f'        <span class="switcher__name" aria-hidden="true">{html.escape(cur)}</span>\n'
            f'      </div>\n'
            f'    </nav>\n')

def neighbours(slug):
    """(previous, next) inside the page's own group, wrapping round."""
    _label, _noun, items = _group(slug)
    i = [s_ for s_, _t, _h in items].index(slug)
    return items[i - 1], items[(i + 1) % len(items)]

def product_tint(slug):
    """The product's own color, from its Electric mark. The three dark-tile marks use the accent drawn on the tile."""
    color = PROJECTS[slug].get("tint") or mark_color(slug)
    if not color:
        return None
    r, g, b = (int(color[i:i + 2], 16) for i in (1, 3, 5))
    return color if (r * 299 + g * 587 + b * 114) / 255000 > 0.2 else None  # navy and other near-black marks give no tint

_DECISIONS = None
def decisions_for(title):
    global _DECISIONS
    if _DECISIONS is None:
        _DECISIONS = _load_sibling("build-decisions.py", "build_decisions").DECISIONS
    return [d for d in _DECISIONS if d["project"] == title]

def render_forks(title):
    """The project's real decisions from build-decisions.py: options passed on struck through, the pick in bold,
    reasons only where Chae gave them. Nothing is written here that the data doesn't say."""
    out = []
    for d in decisions_for(title):
        if not any(o["chosen"] for o in d["options"]):
            continue
        lis = []
        for o in d["options"]:
            label = html.escape(o["label"])
            if o["chosen"]:
                lis.append(f'<li class="is-chosen"><b>{label}</b><span class="visually-hidden"> (my pick)</span></li>')
            else:
                lis.append(f'<li class="is-passed"><s>{label}</s><span class="visually-hidden"> (passed on)</span></li>')
        why = ""
        if d["why"]:
            why = ('\n          <div class="fork__why"><p>Why</p><ul>' + "".join(f"<li>{html.escape(w)}</li>" for w in d["why"]) + "</ul></div>")
        out.append(f'        <article class="fork">\n          <h3>{html.escape(d["question"])}</h3>\n'
                   f'          <ul class="fork__opts">{"".join(lis)}</ul>{why}\n        </article>')
    if not out:
        return ""
    return ('        <div class="forks">\n' + "\n".join(out) + "\n        </div>\n"
            '        <p><a href="/projects/decisions">See every option I weighed, across all my projects</a></p>')

# Documents behind a build or case: only files that already live in this repo. Each is (name, href, what it is).
# A build with none gets no row. Builds whose notes live in their own GitHub repos are not listed: those are not here.
def render_docs(slug):
    docs = PROJECTS[slug].get("docs")
    if not docs:
        return ""
    chips = "".join(
        f'<a class="doc" href="{h}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        f'<path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5M10 13h6M10 17h6"/></svg><span><b>{html.escape(n)}</b><small>{html.escape(d)}</small></span></a>'
        for n, h, d in docs)
    return f'      <div class="docs" role="group" aria-label="Documents behind it"><p class="docs__k">Documents behind it</p><div class="docs__row">{chips}</div></div>\n'


def validate(cases):
    slugs = [c["slug"] for c in cases]
    dupes = {s for s in slugs if slugs.count(s) > 1}
    assert not dupes, f"duplicate slugs: {dupes}"
    for c in cases:
        missing = [k for k in REQUIRED if k not in c]
        assert not missing, f"{c.get('slug', '?')}: missing {missing}"
    # a decision whose project name matches no case would silently never show up: name the ones that are allowed to
    titles = {c["title"] for c in cases} | {"This site", "Build marks"}
    stray = {d["project"] for d in _load_sibling("build-decisions.py", "build_decisions").DECISIONS} - titles
    assert not stray, f"decisions for projects with no case page: {stray}"


def render_sections(c):
    present = [(k, label) for k, label in SECTIONS if c[k].strip()]
    toc = "\n".join(f'        <a href="#{k}">{label}</a>' for k, label in present)
    body = "\n".join(f'        <h2 id="{k}">{label}</h2>\n{c[k]}' for k, label in present)
    return toc, body


def jsonld(c, og_image):
    """Labels the page as a project by Chae Kim, so search engines and AI assistants can cite it."""
    data = {
        "@context": "https://schema.org",
        "@type": "CreativeWork",
        "name": c["title"],
        "headline": html.unescape(re.sub(r"<[^>]+>", "", c["heading"])),
        "description": c["desc"],
        "url": f"{SITE_URL}/projects/{c['slug']}",
        "image": og_image,
        "creator": {"@type": "Person", "name": "Chae Kim", "alternateName": "Chae Woon Kim", "url": f"{SITE_URL}/"},
    }
    body = json.dumps(data, ensure_ascii=False, indent=2).replace("</", "<\\/")
    return '  <script type="application/ld+json">\n' + "\n".join("  " + line for line in body.splitlines()) + "\n  </script>"


def render(c):
    c = {**DEFAULTS, **c}
    c["forks"] = c["forks"] or render_forks(c["title"])
    toc, body = render_sections(c)
    tint = product_tint(c["slug"]) if c["slug"] in BUILD_SLUGS else None
    is_build = c["slug"] in BUILD_SLUGS
    mark = build_mark(c["slug"], "case-hero__mark", 56, themed=True) if is_build else ""
    # builds use their own favicon, touch icon and share card; everything else keeps the site's 김 set
    own = build_icons(c["slug"], SITE_URL) if is_build else None
    icons, og_image = own or (SITE_ICONS, f"{SITE_URL}/assets/img/og-sky.png")
    prev, nxt = neighbours(c["slug"])
    _label, noun, _items = _group(c["slug"])
    fields = {
        **{k: c[k] for k in ("slug", "heading", "tldr", "cover", "cover_class", "badge")},
        **{k: html.escape(c[k]) for k in PLAIN_TEXT},
        "desc": html.escape(c["desc"]),
        "toc": toc,
        "body": body,
        "grad": c.get("grad", "plain"),
        "sec": "sec-builds" if is_build else "sec-work",
        "jsonld": jsonld(c, og_image),
        "back_href": "/#builds" if is_build else "/#work",
        "back_label": "All builds" if is_build else "All work",
        "prev_href": prev[2], "prev_title": html.escape(prev[1]), "prev_mark": _tile(prev[0], "next__mark", 36),
        "next_href": nxt[2], "next_title": html.escape(nxt[1]), "next_mark": _tile(nxt[0], "next__mark", 36),
        "next_noun": noun, "next_label": f"Previous and next {noun}",
        "switcher": render_switcher(c["slug"]), "docs": render_docs(c["slug"]),
        "tint_class": " has-tint" if tint else "", "tint_style": f' style="--pt: {tint}"' if tint else "",
        "tint_wash": '    <div class="tint-wash" aria-hidden="true"></div>\n' if tint else "",
        "site_url": SITE_URL, "icons": icons, "og_image": og_image,
        # builds show their color-seal mark above the eyebrow
        "mark": mark + "\n      " if mark else "",
        # web apps get a "Try it live" button on the cover and the dialog it opens
        "live": live_button(c["slug"]) if c["slug"] in LIVE_APPS else "",
        "live_dialog": LIVE_DIALOG + "\n" if c["slug"] in LIVE_APPS else "",
        "live_script": ("\n" + LIVE_SCRIPT if c["slug"] in LIVE_APPS else "") + ("\n" + SPARK_SCRIPT if is_build and spark_ready(c["slug"]) else ""),
        "head_assets": CASE_HEAD_ASSETS, "top": CASE_TOP, "foot": CASE_FOOT, "scripts": CASE_SCRIPTS,
    }
    return finish(SHELL.format_map(fields))


def main(argv=None):
    """Write projects/<slug>.html for every case. With --check, write nothing and fail if any page is out of date."""
    check = "--check" in (sys.argv[1:] if argv is None else argv)
    validate(CASES)
    OUT.mkdir(exist_ok=True)
    stale = []
    for i, c in enumerate(CASES):
        out = render(c)
        if "[CONFIRM:" in out:
            sys.exit(f"{c['slug']}: unresolved CONFIRM placeholder")
        path = OUT / f"{c['slug']}.html"
        if check:
            if not path.exists() or path.read_text(encoding="utf-8") != out:
                stale.append(c["slug"])
        else:
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(out)
            print("wrote", c["slug"])
    # the command palette's data comes from the same lists, so a new case study appears there on its own
    from writing_data import ESSAYS
    palette = palette_data.dump(palette_data.build(CASES, BUILD_SLUGS, ESSAYS))
    ppath = ROOT / "assets" / "data" / "palette.json"
    if check:
        if not ppath.exists() or ppath.read_text(encoding="utf-8") != palette:
            stale.append("assets/data/palette.json")
    else:
        ppath.parent.mkdir(exist_ok=True)
        with open(ppath, "w", encoding="utf-8", newline="\n") as f:
            f.write(palette)
        print("wrote assets/data/palette.json")
    if stale:
        sys.exit(f"out of date, run python3 scripts/build-cases.py: {stale}")
    if check:
        print(f"ok: {len(CASES)} pages up to date")


if __name__ == "__main__":
    main()
