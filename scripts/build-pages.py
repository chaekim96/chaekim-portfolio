#!/usr/bin/env python3
"""Builds the pages written by hand: their words are in scripts/pages/<name>.html, and the
shared head, header, footer and scripts are filled in here.

Usage:  python3 scripts/build-pages.py
"""
from pathlib import Path

from stamp_shared import SITE_URL, prefer_webp, CASE_FOOT, CASE_HEAD_ASSETS, CASE_SCRIPTS, CASE_TOP

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ROOT_PAGES = {"404"}  # everything else goes in projects/

TOKENS = {"%%HEAD_ASSETS%%": CASE_HEAD_ASSETS, "%%TOP%%": CASE_TOP, "%%FOOT%%": CASE_FOOT,
          "%%SCRIPTS%%": CASE_SCRIPTS, "%%SITE%%": SITE_URL}

for src in sorted((HERE / "pages").glob("*.html")):
    page = src.read_text(encoding="utf-8")
    for token, value in TOKENS.items():
        page = page.replace(token, value)
    page = prefer_webp(page)
    out = ROOT / (f"{src.name}" if src.stem in ROOT_PAGES else f"projects/{src.name}")
    out.write_text(page, encoding="utf-8")
    print("wrote", out.relative_to(ROOT))
