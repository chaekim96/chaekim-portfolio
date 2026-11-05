#!/usr/bin/env python3
"""Refreshes <lastmod> in sitemap.xml from each page's last git change, and points
sitemap.xml and robots.txt at the site's address.

Run before committing page edits:  python3 scripts/build-sitemap.py
A page with uncommitted changes gets today's date.
"""
import datetime
import pathlib
import re
import subprocess

from stamp_shared import SITE_URL

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = SITE_URL
SITEMAP = ROOT / "sitemap.xml"


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True).stdout.strip()


def page_file(loc):
    path = re.sub(r"^https://[^/]+", "", loc).strip("/")
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
    loc = re.sub(r"^https://[^/]+", SITE, loc)
    return f"<url><loc>{loc}</loc><lastmod>{new}</lastmod>{rest}</url>"


xml = re.sub(r"<url>(.*?)</url>", refresh, xml)
SITEMAP.write_text(xml, encoding="utf-8")
(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
print(f"sitemap.xml: {changed} lastmod dates updated")
