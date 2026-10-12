#!/usr/bin/env python3
"""Refreshes <lastmod> in sitemap.xml from each page's last git change.

Run before committing page edits:  python3 scripts/build-sitemap.py
A page with uncommitted changes gets today's date.
"""
import datetime
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://chaekim-portfolio.vercel.app"
SITEMAP = ROOT / "sitemap.xml"


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True).stdout.strip()


def page_file(loc):
    path = loc[len(SITE):].strip("/") if loc.startswith(SITE) else loc
    return "index.html" if not path else f"{path}.html"


def lastmod(rel):
    if git("status", "--porcelain", "--", rel):
        return datetime.date.today().isoformat()
    return git("log", "-1", "--format=%cs", "--", rel) or datetime.date.today().isoformat()


xml = SITEMAP.read_text(encoding="utf-8")
changed = 0


def refresh(m):
    global changed
    entry = m.group(1)
    loc = re.search(r"<loc>([^<]+)</loc>", entry).group(1)
    old = re.search(r"<lastmod>([^<]+)</lastmod>", entry)
    rel = page_file(loc)
    if not (ROOT / rel).exists():
        raise SystemExit(f"sitemap lists {loc} but {rel} does not exist")
    new = lastmod(rel)
    changed += not old or new != old.group(1)
    rest = re.sub(r"<loc>[^<]+</loc>|<lastmod>[^<]+</lastmod>", "", entry)
    return f"<url><loc>{loc}</loc><lastmod>{new}</lastmod>{rest}</url>"


xml = re.sub(r"<url>(.*?)</url>", refresh, xml)
SITEMAP.write_text(xml, encoding="utf-8")
print(f"sitemap.xml: {changed} lastmod dates updated")
