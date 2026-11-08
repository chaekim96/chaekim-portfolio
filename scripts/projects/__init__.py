"""Every project on the site: one file per project in this folder, listed once below.

To add a project, write scripts/projects/<slug>.py and add the slug to the list where it belongs.
Each file sets PROJECT, a dict with slug and any of:

  card, card_href, card_attrs, card_wide   the home card. card is the markup inside the link;
                                           card_href defaults to /projects/<slug>, None for no link
  live=(title, url, note)                  gets a "Try it live" button and dialog
  mark, glyph, grad, stage, tint, docs     color-seal file name, Work tile glyph, cover gradient,
                                           home stage to keep, case-page tint, document links
  kicker, heading, desc, tldr, ...         case-study copy. A project with a kicker gets a generated
                                           page from build-cases.py; see REQUIRED and SECTIONS there

The build scripts read everything from here, so nothing about a project is typed twice.
"""
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent

# The home page's "Three to try first". They stay in their folder's order everywhere else.
FEATURED = ["ai-visibility-checker", "tally", "typerace"]

# Folders on the Builds tab, in order. The first three are the builds with case studies,
# and this order also runs the project switcher, the command palette and llms.txt.
FOLDERS = {
    "products": ["ai-visibility-checker", "tally", "timely", "palette-generator", "typerace", "networking-tracker",
                 "web-anatomy", "voiceprompter", "parallel-prospect-brief", "product-blueprint"],
    "mods": ["smartmodel", "token-fuel", "code-improver", "task-progress"],
    "ai-ml": ["spotify-review-triage", "review-labeler", "personal-wiki", "pacman-dqn", "custom-llm"],
    "design": ["siri-reimagined", "portfolio", "personal-brand", "build-marks", "brand"],
    "archive": ["arcade", "home-gif", "yin-yang", "3d-prints", "lime-poster", "wmcs", "aav"],
}
BUILDS = FOLDERS["products"] + FOLDERS["mods"] + FOLDERS["ai-ml"]

# The Work tab, in order, and the order the Work case pages step through.
WORK = ["lucent", "ey", "tritooling", "mirrorme", "mobility"]
WORK_CASES = ["lucent", "mobility", "ey", "mirrorme", "tritooling"]
COLLEGE = ["iu-study-assistant", "alab", "luc", "ptm", "coursera"]

# Pages with no card of their own. DOCUMENTS follow the page they belong to in llms.txt.
DOCUMENTS = {"mirrorme": ["mirrorme-tech-pack"]}
SITE_PAGES = ["decisions", "portfolio", "personal-brand", "build-marks"]  # "How this site is made" in llms.txt


def _load(slug):
    spec = importlib.util.spec_from_file_location(f"projects_{slug.replace('-', '_')}", HERE / f"{slug}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert mod.PROJECT["slug"] == slug, f"{slug}.py: slug is {mod.PROJECT['slug']}"
    return mod.PROJECT


_listed = {s for slugs in (*FOLDERS.values(), WORK, COLLEGE, *DOCUMENTS.values(), SITE_PAGES) for s in slugs}
_on_disk = {p.stem for p in HERE.glob("*.py") if p.stem != "__init__"}
assert _listed == _on_disk, f"list these in projects/__init__.py: {sorted(_on_disk - _listed)}; no file for: {sorted(_listed - _on_disk)}"
assert sorted(WORK) == sorted(WORK_CASES) and set(FEATURED) <= set(FOLDERS["products"])

PROJECTS = {s: _load(s) for s in sorted(_listed)}
CASES = [PROJECTS[s] for s in (*WORK_CASES, *BUILDS)]


def field(name):
    """{slug: value} for the projects that set this field."""
    return {s: p[name] for s, p in PROJECTS.items() if name in p}
