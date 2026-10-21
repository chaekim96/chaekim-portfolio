#!/usr/bin/env python3
"""Builds /llms.txt: a short Markdown guide to this site for AI tools.

Usage:  python3 scripts/build-llms.py
Each entry's one-liner is the page's own meta description, so the guide stays in
step with the pages. Run it after build-cases.py / build-home.py.
"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://chaekim-portfolio.vercel.app"

# Same order as the homepage tabs.
SECTIONS = [
    ("Builds", "Products and tools, most with a live demo.", [
        "ai-visibility-checker", "tally", "palette-generator", "typerace", "networking-tracker",
        "web-anatomy", "voiceprompter", "smartmodel", "token-fuel", "code-improver",
        "spotify-review-triage", "personal-wiki", "pacman-dqn", "custom-llm", "home-gif", "yin-yang",
    ]),
    ("Work", "Startups, consulting and operations, then earlier projects at Indiana University.", [
        "lucent", "ey", "tritooling", "mirrorme", "mirrorme-tech-pack", "mobility",
        "alab", "coursera", "iu-study-assistant", "luc", "ptm",
    ]),
    ("How this site is made", "The decisions and options behind the portfolio itself.", [
        "decisions", "portfolio", "personal-brand",
    ]),
]


def page_info(slug):
    text = (ROOT / "projects" / f"{slug}.html").read_text(encoding="utf-8")
    title = re.search(r"<title>([^<]*)</title>", text).group(1)
    title = html.unescape(title.split(" · ")[0]).strip()
    desc = re.search(r'<meta name="description" content="([^"]*)"', text)
    return title, html.unescape(desc.group(1)).strip() if desc else ""


def main():
    listed = {s for _, _, slugs in SECTIONS for s in slugs}
    on_disk = {p.stem for p in (ROOT / "projects").glob("*.html") if not p.stem.startswith("_")}
    missing = sorted(on_disk - listed)
    if missing:
        raise SystemExit(f"Add these pages to a section in build-llms.py: {missing}")

    out = [
        "# Chae Kim",
        "",
        "> Chae Kim (Chaewoon Kim) builds products and tools. MBA candidate at UC Berkeley Haas, co-founder of Lucent (an AI search console), previously at EY (AI & Data) and Tritooling. This is their portfolio.",
        "",
        "Every project page follows the same shape: the problem, what Chae did, results, what they'd do differently, and artifacts. Numbers on the site match Chae's resume.",
        "",
    ]
    for name, blurb, slugs in SECTIONS:
        out += [f"## {name}", "", blurb, ""]
        for slug in slugs:
            title, desc = page_info(slug)
            out.append(f"- [{title}]({SITE}/projects/{slug})" + (f": {desc}" if desc else ""))
        out.append("")
    out += [
        "## More",
        "",
        f"- [Home]({SITE}/): the Builds, Work and About tabs",
        f"- [Reading list]({SITE}/reading)",
        f"- [Resume (PDF)]({SITE}/assets/pdf/chae-kim-resume.pdf)",
        f"- [Arcade]({SITE}/arcade): Snake, Galaga and a generative lo-fi radio",
        "",
    ]
    (ROOT / "llms.txt").write_text("\n".join(out), encoding="utf-8")
    print(f"wrote llms.txt ({sum(len(s) for _, _, s in SECTIONS)} pages)")


if __name__ == "__main__":
    main()
