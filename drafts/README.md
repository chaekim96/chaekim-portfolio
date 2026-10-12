# Drafts (not deployed: `drafts/` is in .vercelignore)

## personal-brand.html — "Choosing a brand by owning what I already am"

From the other session's `portfolio-v2` (commit 4df009b), held back when it was merged
into `main`, because it can't go live as written:

1. Two `[CONFIRM: ...]` tags need Chae's own words: the reason for a signature over a stamp,
   and what decided the finalist.
2. It is out of date. It says Ink or Craft becoming the main site is "undecided" and ends with
   "See it live → Ink and Craft variants", but Stamp became the only design (Oct 12, 2026) and
   the variants were retired (`/variants/*` redirects home).
3. "Army staff sergeant" conflicts with the resume, which says Sergeant.
4. It was built for the retired desktop design (loads the deleted `style.css`). To publish,
   move it into `scripts/build-cases.py` (CASES) so it gets the Stamp project-page look, add a
   card to the Stamp template in `scripts/build-home.py`, and add it to `sitemap.xml`.
