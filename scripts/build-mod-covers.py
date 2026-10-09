#!/usr/bin/env python3
"""Renders the cover images for the Claude Code mod case studies.

Usage:  python3 scripts/build-mod-covers.py
Output: assets/img/thumbs/{smartmodel,token-fuel,code-improver}-wide.jpg (1600x900)

Each cover shows the mod's real output, not an illustration:
  SmartModel     the picker its hook actually raises in ask mode
  Token-Fuel     the gauge line and menu-bar item from its README
  Code Improver  its subagent definition file, verbatim
"""
import os, subprocess, tempfile

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "assets", "img", "thumbs")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

BASE = """<!DOCTYPE html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600&display=block">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { width: 1600px; height: 900px; overflow: hidden; }
body { font-family: Poppins, sans-serif; display: grid; place-items: center; background: %(bg)s; }
.win { width: %(w)spx; border-radius: 22px; overflow: hidden; box-shadow: 0 2px 6px rgba(0,0,0,.08), 0 50px 100px -40px rgba(10,20,50,.55); }
.bar { height: 52px; display: flex; align-items: center; gap: 10px; padding: 0 20px; }
.bar i { width: 14px; height: 14px; border-radius: 50%%; display: block; }
.bar i:nth-child(1) { background: #ff5f57; } .bar i:nth-child(2) { background: #febc2e; } .bar i:nth-child(3) { background: #28c840; }
.bar span { flex: 1; text-align: center; font-size: 17px; margin-right: 72px; }
.mono { font-family: "JetBrains Mono", ui-monospace, monospace; }
%(css)s
</style></head><body>%(body)s</body></html>"""

COVERS = {
  "smartmodel": dict(
    bg="radial-gradient(70% 80% at 30% 20%, #26305a 0%, #0d1124 60%, #080b18 100%)", w=1180,
    css="""
.win { background: #0f1325; border: 1px solid rgba(255,255,255,.08); }
.bar { background: #161b31; border-bottom: 1px solid rgba(255,255,255,.06); } .bar span { color: #8a93b8; }
.body { padding: 38px 48px 44px; color: #c9d1e8; font-size: 25px; line-height: 1.55; }
.q { color: #fff; font-weight: 500; }
.hdr { display: inline-block; margin: 26px 0 16px; padding: 4px 12px; border-radius: 8px; background: #23305e; color: #9fb6ff; font-size: 19px; }
.opt { display: grid; grid-template-columns: 34px 1fr; padding: 10px 14px; border-radius: 10px; }
.opt b { font-weight: 600; color: #fff; } .opt small { display: block; font-size: 19px; color: #8a93b8; }
.opt.on { background: rgba(143, 212, 168, .12); box-shadow: inset 0 0 0 1px rgba(143, 212, 168, .35); } .opt.on b { color: #8fd4a8; }
.tag { position: absolute; left: 64px; bottom: 50px; font-size: 20px; color: #8a93b8; }
""",
    body="""<div class="win"><div class="bar"><i></i><i></i><i></i><span class="mono">claude code</span></div>
<div class="body mono">
<p class="q">SmartModel rates this medium-effort (score 34/100).<br>Which model should run it?</p>
<span class="hdr">Model</span>
<div class="opt on"><span>1.</span><span><b>Sonnet 5.5 (Recommended)</b><small>$$ · everyday features, bug fixes, tests, single-module refactors</small></span></div>
<div class="opt"><span>2.</span><span><b>Haiku 4.5</b><small>$ · lookups, renames, small edits, git/shell chores, quick explanations</small></span></div>
<div class="opt"><span>3.</span><span><b>Opus 5.5 · current</b><small>$$$ · multi-file changes, tricky debugging, design decisions</small></span></div>
<div class="opt"><span>4.</span><span><b>Fable 5.1</b><small>$$$$ · architecture, from-scratch systems, deep research, hard reasoning</small></span></div>
</div></div>"""),

  "token-fuel": dict(
    bg="linear-gradient(160deg, #fff4ea 0%, #ffe6d4 55%, #ffd9c2 100%)", w=1300,
    css="""
.menubar { position: absolute; top: 0; left: 0; right: 0; height: 40px; background: rgba(255,255,255,.72); backdrop-filter: blur(20px);
  display: flex; align-items: center; justify-content: flex-end; gap: 26px; padding: 0 30px; font-size: 18px; color: #1c1c1e; border-bottom: 1px solid rgba(0,0,0,.06); }
.menubar .fuel { padding: 3px 10px; border-radius: 6px; background: rgba(0,0,0,.07); font-weight: 600; }
.win { background: rgba(28,28,30,.92); border: 1px solid rgba(255,255,255,.1); margin-top: 40px; }
.bar { background: rgba(255,255,255,.04); } .bar span { color: #a1a1a6; }
.rows { padding: 30px 40px 38px; display: grid; gap: 22px; }
.row small { display: block; font-size: 17px; color: #a1a1a6; margin-bottom: 6px; font-family: Poppins, sans-serif; }
.row p { font-size: 23px; color: #f5f5f7; white-space: nowrap; }
.g { color: #30d158; } .y { color: #ffd60a; } .c { color: #64d2ff; } .dim { color: #6e6e73; }
""",
    body="""<div class="menubar"><span>Wi-Fi</span><span class="fuel mono">⛽ ████░ 80%</span><span>Thu 9:41 AM</span></div>
<div class="win"><div class="bar"><i></i><i></i><i></i><span>Token Fuel</span></div>
<div class="rows mono">
<div class="row"><small>Claude Code · the README example</small><p><span class="y">▕███░░░░░░░▏</span> Low · 33% · 65.6k of 200k left · ~3 turns left · <span class="dim">▂▁▃▂▅▂▁▃▄▂▇▅</span></p></div>
<div class="row"><small>Codex · the v1.1 verification reading</small><p><span class="c">▕███████░░░▏</span> Good · 74% · 261.8k of 354.4k left</p></div>
</div></div>"""),

  "code-improver": dict(
    bg="linear-gradient(150deg, #f1f3f7 0%, #dfe6f0 100%)", w=1240,
    css="""
.win { background: #ffffff; border: 1px solid rgba(0,0,0,.08); }
.bar { background: #f2f2f5; border-bottom: 1px solid rgba(0,0,0,.06); } .bar span { color: #6e6e73; }
.code { padding: 34px 44px 40px; font-size: 25px; line-height: 1.7; color: #1c1c1e; counter-reset: ln; }
.code p { white-space: pre-wrap; padding-left: 60px; position: relative; }
.code p::before { counter-increment: ln; content: counter(ln); position: absolute; left: 0; width: 34px; text-align: right; color: #b0b0b8; }
.k { color: #0063d8; } .s { color: #a3520f; } .m { color: #8e8e93; }
""",
    body="""<div class="win"><div class="bar"><i></i><i></i><i></i><span class="mono">~/.claude/agents/code-improver.md</span></div>
<div class="code mono">
<p class="m">---</p>
<p><span class="k">name:</span> code-improver</p>
<p><span class="k">description:</span> <span class="s">Scans files and suggests improvements for readability,</span></p>
<p><span class="s">  performance, and best practices. Use after writing or modifying code.</span></p>
<p><span class="k">tools:</span> Read, Grep, Glob</p>
<p class="m">---</p>
<p>You are a code improvement specialist. For each issue you find,</p>
<p>explain the problem, show the current code, and provide an improved version.</p>
</div></div>"""),
}

tmp = tempfile.mkdtemp()
for slug, c in COVERS.items():
    src = os.path.join(tmp, f"{slug}.html")
    open(src, "w", encoding="utf-8").write(BASE % c)
    png = os.path.join(tmp, f"{slug}.png")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--window-size=1600,900", "--virtual-time-budget=6000", f"--screenshot={png}", f"file://{src}"],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60)
    out = os.path.join(OUT, f"{slug}-wide.jpg")
    subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "84", png, "--out", out],
                   check=True, stdout=subprocess.DEVNULL)
    print("wrote", os.path.relpath(out, ROOT))
