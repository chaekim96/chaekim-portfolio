#!/usr/bin/env python3
"""Builds every generated page, in the right order.

Usage:  python3 scripts/build.py           (write everything; commit the result)
        python3 scripts/build.py --check   (write nothing; fail if a page is out of date or unfinished)

Not part of this: build-brand-cards.py, build-mod-covers.py and make-og.sh, which render images in
headless Chrome, and build-resume.py. Run those by hand when a mark, cover or the resume changes.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# build-cases.py lists every page in the command palette and build-llms.py reads every page's description,
# so they run after the scripts that write pages. build-sitemap.py dates what the others changed, so it runs last.
STEPS = ["decisions", "writing", "reading", "home", "cases", "llms", "sitemap"]

# Built from git history, so they move on their own: a stale copy is not a stale page.
VOLATILE = [re.compile(r'(<div class="changelog".*?<ul>).*?(</ul>)', re.S), re.compile(r"(<lastmod>)[^<]*(</lastmod>)")]


def run_all():
    for step in STEPS:
        result = subprocess.run([sys.executable, str(ROOT / "scripts" / f"build-{step}.py")], stdout=subprocess.DEVNULL)
        if result.returncode:
            sys.exit(f"build-{step}.py failed")


def generated():
    """Every file the build can write, read straight from the working tree."""
    files = [*ROOT.glob("*.html"), *(ROOT / "projects").glob("*.html"), ROOT / "llms.txt", ROOT / "sitemap.xml",
             ROOT / "assets" / "data" / "palette.json"]
    return {p: p.read_text(encoding="utf-8") for p in files}


def steady(text):
    for pattern in VOLATILE:
        text = pattern.sub(r"\1\2", text)
    return text


def problems(pages):
    """Things a build can't fix: placeholders left in, and public pages search engines aren't told about."""
    found = [f"{p.relative_to(ROOT)}: unresolved [CONFIRM:" for p, text in pages.items() if "[CONFIRM:" in text]
    locs = set(re.findall(r"<loc>https://[^/]+/?([^<]*)</loc>", pages[ROOT / "sitemap.xml"]))
    hidden = set(re.findall(r"^Disallow: /(\S+)$", (ROOT / "robots.txt").read_text(encoding="utf-8"), re.M))
    for p, text in pages.items():
        if p.suffix == ".html" and p.stem != "404" and 'content="noindex' not in text[:3000]:
            rel = str(p.relative_to(ROOT).with_suffix(""))
            if (rel if rel != "index" else "") not in locs and rel not in hidden:
                found.append(f"{rel}: public page missing from sitemap.xml")
    return found


def check():
    before = generated()
    try:
        run_all()
        after = generated()
    finally:
        for p, text in before.items():
            p.write_text(text, encoding="utf-8")
        for p in set(generated()) - set(before):
            p.unlink()
    found = problems(before)
    found += [f"{p.relative_to(ROOT)}: out of date" for p in after
              if p not in before or steady(before[p]) != steady(after[p])]
    if found:
        sys.exit("\n".join(found + ["Run python3 scripts/build.py and commit the result."]))
    print(f"ok: {len(before)} files up to date")


if __name__ == "__main__":
    if "--check" in sys.argv[1:]:
        check()
    else:
        run_all()
        print("built")
