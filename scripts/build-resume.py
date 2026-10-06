#!/usr/bin/env python3
"""Builds the public resume PDF from Chae's canonical cv.md.

Usage:  python3 scripts/build-resume.py [path/to/cv.md]      (default: ~/career-ops/cv.md)
Output: assets/pdf/chae-kim-resume.pdf

Mirrors the Word template (Letter, 0.5in x 0.625in margins, Calibri 10.5pt, right-tab dates).
For the public copy it always:
  - drops the phone number from the contact line
  - drops <!-- private notes --> from cv.md
and fails loudly if the result is not exactly one page.
"""
import html, os, re, subprocess, sys, tempfile

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/career-ops/cv.md")
OUT = os.path.join(ROOT, "assets", "pdf", "chae-kim-resume.pdf")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FONTS = "/Applications/Microsoft Word.app/Contents/Resources/DFonts"

# One-line versions for the ADDITIONAL block, in Chae's own wording from the tailored
# resumes (Amazon Prime Video PM, Oct 2026). cv.md's longer lines push the page to two.
PROJECTS_LINE = "Tally AI note-taker; Next.js/Postgres CRM; local-LLM RAG knowledge base"
SKILLS_LINE = "Claude Code, Codex, Cursor, SQL, Python, Atlassian (Jira, Confluence), Figma, Tableau, Power BI, Excel"
INTERESTS_LINE = "3D printing (Fusion 360); competitive tennis; latte art; board game design (sold 50+ decks of MirrorMe)"

md = open(SRC, encoding="utf-8").read()
md = re.sub(r"<!--.*?-->", "", md, flags=re.S)          # private notes never ship


def inline(s):
    s = html.escape(s.strip(), quote=False)
    s = re.sub(r"(\w)'(\w)", "\\1\u2019\\2", s)          # typographic apostrophes, as in the Word files
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<!\*)\*(?!\*)(.+?)\*", r"<i>\1</i>", s)
    return s


def link(item):
    item = item.strip()
    if "@" in item:
        return f'<a href="mailto:{item}">{item}</a>'
    if re.match(r"[\w.-]+\.\w+(/\S*)?$", item):
        return f'<a href="https://{item}">{item}</a>'
    return html.escape(item)


lines = [l.rstrip() for l in md.splitlines()]
name = next(l[2:] for l in lines if l.startswith("# "))
contact_src = next(l for l in lines if "@" in l and "·" in l)
contact = [c for c in contact_src.split("·") if not re.search(r"\+?\d[\d\s().-]{7,}", c)]   # no phone

# ---------- split into sections ----------
sections, cur = {}, None
for l in lines:
    if l.startswith("## "):
        cur = l[3:].strip(); sections[cur] = []
    elif cur:
        sections[cur].append(l)


def blocks(sec):
    """### Org — Location blocks, each with its raw lines."""
    out, b = [], None
    for l in sections.get(sec, []):
        if l.startswith("### "):
            b = {"head": l[4:], "lines": []}; out.append(b)
        elif b is not None and l.strip():
            b["lines"].append(l)
    return out


def org_line(head, right):
    org, _, loc = head.partition(" — ")
    loc = f", {html.escape(loc)}" if loc else ""
    return f'<div class="row"><span><b>{html.escape(org)}</b>{loc}</span><b>{right}</b></div>'


def bullets(items):
    return "<ul>" + "".join(f"<li>{inline(i)}</li>" for i in items) + "</ul>" if items else ""


# ---------- education ----------
edu = []
for b in blocks("Education"):
    deg_line = next(l for l in b["lines"] if l.startswith("**"))
    parts = [p.strip() for p in deg_line.split("·")]
    degree, date = parts[0].strip("*"), parts[1]
    gpa = parts[2] if len(parts) > 2 else ""
    items = [l[2:] for l in b["lines"] if l.startswith("- ")]
    edu.append(org_line(b["head"], html.escape(date))
               + f'<div class="row"><b><i>{html.escape(degree)}</i></b><b><i>{html.escape(gpa)}</i></b></div>'
               + bullets(items))

# ---------- experience ----------
exp = []
for b in blocks("Experience"):
    roles, desc, cur_role = [], "", None
    for l in b["lines"]:
        if l.startswith("*") and not l.startswith("**"):
            desc = l.strip("*")
        elif l.startswith("**"):
            title, _, years = l.partition("·")
            cur_role = {"title": title.strip().strip("*"), "years": years.strip(), "items": []}
            roles.append(cur_role)
        elif l.startswith("- ") and cur_role:
            cur_role["items"].append(l[2:])
    yrs = [y for r in roles for y in re.findall(r"\d{4}", r["years"])]
    span = f"{min(yrs)} – {max(yrs)}" if yrs else ""
    h = org_line(b["head"], span)
    if desc:
        h += f'<div class="desc"><i>{inline(desc)}</i></div>'
    for r in roles:
        suffix = f" ({r['years'].replace(' – ', '–')})" if len(roles) > 1 else ""
        h += f'<div class="title"><b><i>{html.escape(r["title"])}{suffix}</i></b></div>' + bullets(r["items"])
    exp.append(h)

# ---------- additional (compact, like the Word template) ----------
extra = {}
for l in sections.get("Additional", []):
    m = re.match(r"- \*\*(.+?):\*\*\s*(.+)", l)
    if m:
        extra[m.group(1)] = m.group(2)
github = next((l.strip() for l in sections.get("Projects", []) if "github.com" in l), "")
additional = [f"<b>Skills:</b> {html.escape(SKILLS_LINE)}"]
if "Languages" in extra:
    additional.append(f"<b>Languages:</b> {html.escape(extra['Languages'])}")
additional.append(f"<b>Projects</b> ({link(github)}): {html.escape(PROJECTS_LINE)}")
if "Volunteering" in extra:
    additional.append(f"<b>Volunteering:</b> {html.escape(extra['Volunteering'])}")
additional.append(f"<b>Interests:</b> {html.escape(INTERESTS_LINE)}")

FACES = "".join(
    f'@font-face{{font-family:Cal;src:url("file://{FONTS}/{f}");font-weight:{w};font-style:{s}}}'
    for f, w, s in (("Calibri.ttf", 400, "normal"), ("Calibrib.ttf", 700, "normal"),
                    ("Calibrii.ttf", 400, "italic"), ("Calibriz.ttf", 700, "italic")))

page = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>{html.escape(name)} · Resume</title>
<style>
{FACES}
@page {{ size: Letter; margin: 0.5in 0.625in; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font: 10.5pt/1.22 Cal, Calibri, Carlito, sans-serif; color: #000; }}
a {{ color: inherit; text-decoration: none; }}
h1 {{ text-align: center; font-size: 18pt; line-height: 1.1; font-weight: 700; letter-spacing: .01em; }}
.contact {{ text-align: center; padding-bottom: 2pt; }}
h2 {{ text-align: center; font-size: 10.5pt; font-weight: 700; border-top: 1.5pt solid #000; border-bottom: .75pt solid #000; margin-top: 2pt; padding: .5pt 0; letter-spacing: .02em; }}
.entry {{ margin-top: 3.6pt; }}
.row {{ display: flex; justify-content: space-between; gap: 12pt; }}
.row span, .row b:first-child {{ min-width: 0; }}
.desc, .title {{ }}
ul {{ list-style: none; }}
li {{ position: relative; padding-left: .265in; margin-left: .095in; }}
li::before {{ content: "•"; position: absolute; left: .02in; }}
.additional {{ margin-top: 3pt; }}
</style></head><body>
<h1>{html.escape(name.upper())}</h1>
<div class="contact">{" &bull; ".join(link(c) for c in contact)}</div>
<h2>EDUCATION</h2>
{"".join(f'<div class="entry">{e}</div>' for e in edu)}
<h2 style="margin-top:4pt">EXPERIENCE</h2>
{"".join(f'<div class="entry">{e}</div>' for e in exp)}
<h2 style="margin-top:4pt">ADDITIONAL</h2>
<ul class="additional">{"".join(f"<li>{a}</li>" for a in additional)}</ul>
</body></html>"""

if re.search(r"\(\d{3}\)\s*\d{3}-\d{4}|\+1\s*\(", page):
    sys.exit("phone number leaked into the public resume")

tmp = tempfile.mkdtemp()
src_html = os.path.join(tmp, "resume.html")
open(src_html, "w", encoding="utf-8").write(page)
subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                f"--print-to-pdf={OUT}", f"file://{src_html}"],
               check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

pdf = open(OUT, "rb").read()
pages = len(re.findall(rb"/Type\s*/Page[^s]", pdf))
print(f"wrote {os.path.relpath(OUT, ROOT)} ({len(pdf)//1024} KB, {pages} page{'s' if pages != 1 else ''})")
print(f"preview html: {src_html}")
if pages != 1:
    sys.exit("resume must be exactly one page")
