#!/usr/bin/env python3
"""Builds the featured / more-work case studies from one template.

Usage:  python3 scripts/build-cases.py
Edits:  change the CASES list below, re-run, commit the generated HTML.
The rendered shell is also written to projects/_template.html for reference.
"""
import os, html

ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "projects")
V = "13"  # asset version (cache-bust)

def C(msg):  # visible confirm tag
    return f'<span class="confirm">[CONFIRM: {html.escape(msg)}]</span>'

NAV = """  <header class="nav">
    <div class="container nav__inner">
      <a href="/" class="brand wordmark" aria-label="Chae Kim, home">chae<span class="wordmark__dot"></span></a>
      <button class="nav__burger" aria-label="Open menu" aria-expanded="false">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
      </button>
      <nav class="nav__links" aria-label="Primary">
        <a href="/#work">Work</a>
        <a href="/#experience">Experience</a>
        <a href="/#about">About</a>
        <a href="/assets/pdf/chae-kim-resume.pdf">Resume</a>
        <a href="/#contact">Contact</a>
        <button class="theme-toggle" type="button" aria-label="Toggle dark mode">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>
        </button>
        <a class="nav__cta" href="https://www.linkedin.com/in/chaekim/" target="_blank" rel="noopener">LinkedIn</a>
      </nav>
    </div>
  </header>"""

FOOTER = """  <footer class="footer">
    <div class="container footer__inner">
      <span>© <span data-year>2026</span> Chae Woon Kim · 김채운</span>
      <span><a data-user="chaewoonkim" data-domain="berkeley.edu" href="#">Email</a> · <a href="https://github.com/chaekim96/chaekim-portfolio" target="_blank" rel="noopener">Source</a></span>
    </div>
  </footer>"""

SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} · Chae Kim</title>
  <meta name="description" content="{desc}">
  <meta property="og:title" content="{title} · Chae Kim">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="article">
  <meta property="og:image" content="https://chaekim-portfolio.vercel.app/assets/img/og.png">
  <link rel="canonical" href="https://chaekim-portfolio.vercel.app/projects/{slug}">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap" onload="this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap"></noscript>
  <link rel="stylesheet" href="/assets/css/style.css?v={v}">
  <script>try {{ var t = localStorage.getItem('ck-theme'); if (t) document.documentElement.setAttribute('data-theme', t); }} catch (e) {{}}</script>
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
  <canvas id="bg" aria-hidden="true"></canvas>
{nav}

  <main id="main">
    <section class="case-hero">
      <div class="container">
        <div class="win case-win">
          <div class="win__bar"><span class="win__dots"><i></i><i></i><i></i></span><span class="win__title">{slug}.md</span></div>
          <div class="win__body">
        <a class="case-hero__back" href="/#work">← All work</a>
        <div class="case-hero__emoji" aria-hidden="true">{emoji}</div>
        <p class="eyebrow" style="margin-top:14px">{kicker}</p>
        <h1 class="display case-hero__title">{heading}{badge}</h1>
        <p class="tldr">{tldr}</p>
        <p class="meta-line"><b>Role</b> {role} · <b>Team</b> {team} · <b>Timeline</b> {timeline}</p>
          </div>
        </div>
      </div>
    </section>

    <section class="container">
      <div class="case-cover {cover_class}">{cover}</div>
    </section>

    <section class="container case-body">
      <nav class="toc" aria-label="On this page">
        <a href="#problem">The problem</a>
        <a href="#did">What I did</a>
        <a href="#results">Results</a>
        <a href="#differently">What I'd do differently</a>
        <a href="#artifacts">Artifacts</a>
      </nav>
      <article class="prose">
        <h2 id="problem">The problem</h2>
{problem}
        <h2 id="did">What I did</h2>
{did}
        <h2 id="results">Results</h2>
{results}
        <h2 id="differently">What I'd do differently</h2>
{differently}
        <h2 id="artifacts">Artifacts</h2>
{artifacts}
      </article>
    </section>

    <section class="next">
      <div class="container next__grid">
        <a href="/projects/{prev_slug}"><small>← Previous</small><strong>{prev_title}</strong></a>
        <a href="/projects/{next_slug}" style="text-align:right"><small>Next →</small><strong>{next_title}</strong></a>
      </div>
    </section>
  </main>

{footer}
  <script src="/assets/js/main.js?v={v}"></script>
</body>
</html>
"""

def p(*paras):
    return "\n".join(f"        <p>{x}</p>" for x in paras)

def ul(*items):
    return "        <ul>\n" + "\n".join(f"          <li>{x}</li>" for x in items) + "\n        </ul>"

def results(*pairs):
    cells = "".join(f'<div><b>{b}</b><span>{s}</span></div>' for b, s in pairs)
    return f'        <div class="results">{cells}</div>'

def art(*items):
    """items: (src, caption) for real images, or ('', caption) for a placeholder."""
    out = []
    for src, cap in items:
        if src:
            out.append(f'<figure><img src="{src}" alt="{html.escape(cap)}" loading="lazy"><figcaption>{cap}</figcaption></figure>')
        else:
            out.append(f'<div class="ph">{C(cap)}</div>')
    return '        <div class="artifacts">' + "".join(out) + "</div>"

def typecover(big, small):
    return f'<div class="feat__media feat__media--type" style="aspect-ratio:auto;min-height:220px"><div class="big">{big}<small>{small}</small></div></div>'

CASES = [
  dict(slug="lucent", emoji="🔦", title="Lucent",
    kicker="featured · co-founder & CEO · NSF I-Corps",
    heading="Making small businesses visible in AI search.",
    desc="Lucent is an AI search observability platform and consultancy. It shows brands how they rank in ChatGPT, Perplexity, and Gemini, then helps them fix it.",
    tldr="An AI search observability platform and a consultancy. Lucent shows brands how they rank in ChatGPT, Perplexity, and Gemini, then helps them fix it, through the product and hands-on GEO and SEO work.",
    role="Co-founder & CEO", team="Co-founder/CTO + a data science intern", timeline="2025 to 2026",
    cover='<a href="https://trylucent.ai" target="_blank" rel="noopener" aria-label="Open trylucent.ai"><img src="/assets/img/thumbs/lucent-wide.jpg" alt="Lucent homepage: The AI Search Console" width="1600" height="900"></a>', cover_class="",
    problem=p("Customers now ask AI instead of Google. Small businesses can't see whether AI recommends them, and GEO tools are priced for enterprises."),
    did=ul(
      "21 NSF I-Corps discovery interviews narrowed the ICP from \"everyone\" to digitally native SMBs and marketing agencies. 100+ interviews across U.S. and APAC SMBs tested willingness to pay.",
      "Positioned around the one-person marketing team: GEO plus SEO execution, not just citation tracking. 5 positioning hypotheses tested across 65 outbound prospects picked the message.",
      "Designed cheap tracking: statistical sampling, and re-running prompts only when models or rankings change.",
      "Led a paid pilot: multi-site SEO and AI visibility audits turned into an engineering action plan.",
      "Built the investor pitch: bottom-up SAM, phased GTM, 100+ question diligence bank.",
    ),
    results=results(("1", "first paying pilot"), ("5", "LOIs in 30 days"), ("+50%", "discovery response rate"), ("NSF", "I-Corps backing")) + "\n" + p("The pilot became an ongoing advisory relationship. " + C("any usage or revenue metric you're comfortable sharing")),
    differently=p("Lock the GTM motion earlier. Investors flagged it as the biggest gap. Positioning tests and pilots should have run in parallel, not in sequence."),
    artifacts=art(("", "artifact image: product screenshot (no client data)"), ("", "artifact image: pitch deck excerpt, e.g. SAM or GTM slide")),
  ),
  dict(slug="mobility", emoji="🦯", title="Mobility devices for older adults (stealth)",
    kicker="in progress · co-founder · stealth",
    heading="Mobility aids people aren't embarrassed to use.",
    badge='<span class="stealth">Stealth</span>',
    desc="Premium, design-forward mobility products that help older adults stay independent longer.",
    tldr="Premium, design-forward mobility products that help older adults stay independent longer.",
    role="Co-founder: GTM, brand, outreach, strategy (my co-founder owns product)", team="2 co-founders", timeline=C("timeline"),
    cover='<img src="/assets/img/thumbs/mobility-wide.jpg" alt="An older couple walking along a garden path" width="1600" height="900">', cover_class="",
    problem=p("Mobility aids look like medical equipment. Users feel stigmatized, and common designs have real safety gaps."),
    did=ul(
      "Visited senior centers and assisted living facilities around Berkeley. 14+ conversations with operators, caregivers, and advisors.",
      "Studied why companies here stall: payer, user, and decider are three different people; hardware margins erode; incumbents own distribution.",
      "Built the brand-as-moat thesis and a decision framework for the first product.",
      "Set an operating cadence for a team 16 time zones apart.",
    ),
    results=p("Early stage and in progress. Results will be added as they're shareable. " + C("anything shareable now, e.g. advisors onboarded, prototype stage")),
    differently=p("Too early to say. This section fills in once there's a first product decision to look back on."),
    artifacts=p("None yet that don't show the mechanism."),
  ),
  dict(slug="ey", emoji="☁️", title="EY, AI & Data",
    kicker="featured · senior consultant · New York · 2021 to 2024",
    heading="Giving leaders one clear view of a sprawling cloud migration.",
    desc="Program-wide risk, OKRs, and the first QBR for a $200M+ cloud migration at a Fortune 500 life sciences client, with $10M+ in realized savings.",
    tldr="Ran the operating system for a $200M+ cloud migration at a Fortune 500 life sciences client: risk, OKRs, and the first executive QBR. It redirected $3M to priority initiatives and realized $10M+ in savings.",
    role="Senior Technology Consultant, AI & Data Strategy (Staff Technology Consultant 2021 to 2023)", team="EY Technology Consulting, 25+ client teams", timeline="August 2021 to July 2024",
    cover='<img src="/assets/img/thumbs/ey-wide.jpg" alt="Earth at night from orbit, city lights glowing" width="1600" height="900">', cover_class="",
    problem=p("A Fortune 500 life sciences client was moving its application portfolio to the cloud across 25+ teams. Risks surfaced late, executives got escalations instead of decisions, and nobody had one view of what was on track."),
    did=ul(
      "Built the program-wide risk and OKR system: blocker and risk triage across 25+ teams. Earlier resource reallocation, 30% fewer executive escalations.",
      "Designed and launched the client's first QBR, aligning the CTO and product teams on direction and redirecting $3M to priority initiatives. Then standardized QBR governance across 5+ programs.",
      "Drove adoption of a custom PM methodology with a 15-person team and hands-on tool training. 90% adoption across 4,000 users.",
      "Prioritized every application for migration, modernization, or retirement with a value-capture framework. SVP approval, $10M+ in realized savings over 2 years.",
    ),
    results=results(("$3M", "redirected to priority initiatives"), ("−30%", "executive escalations"), ("90%", "adoption across 4,000 users"), ("$10M+", "realized savings over 2 years")) + "\n" + p("Also at EY: logistics lead for a Fortune 500 consumer foods client (forecast accuracy +10% YoY), data architect on an internal initiative, and an internal AI adoption campaign that drove 200%+ usage across 5 user segments. Earlier: recovered $5M in pricing and mix leakage for a Fortune 500 software client, and re-architected Agile workflows for 25+ engineering teams."),
    differently=p(C("what you'd do differently")),
    artifacts=art(("", "artifact image: sanitized QBR or OKR dashboard excerpt")),
  ),
  dict(slug="mirrorme", emoji="🃏", title="MirrorMe",
    kicker="more work · co-founder, GTM · 2024",
    heading="Icebreakers that go deeper without getting awkward.",
    desc="An icebreaker card game for people who host. 150+ pre-launch purchase commitments with zero paid budget.",
    tldr="An icebreaker card game for hosts. 150+ pre-launch commitments at $30 to 40, with zero paid budget.",
    role="Co-founder, led GTM", team="2 co-founders", timeline="2024 " + C("exact months"),
    cover='<img src="/assets/img/thumbs/mirrorme-wide.jpg" alt="MirrorMe question card" width="1600" height="900">', cover_class="",
    problem=p("Hosts want guests to actually talk. Most icebreakers are too shallow to matter or too intense for near-strangers."),
    did=ul(
      "100+ user surveys and a 10-product competitive scan found two high-intent segments: regular hosts, and the venues that host them.",
      "Built the deck on the OCEAN personality model: category cards set a trait, question cards ask about someone at the table, players rate 1 to 5.",
      "Skipped paid channels. Sold in person at card game cafes and social events in New York. 50+ decks sold.",
    ),
    results=results(("150+", "pre-launch purchase commitments"), ("$30 to 40", "price point"), ("$0", "paid budget"), ("50+", "decks sold")) + "\n" + p("Insight: it sold itself in rooms where people already wanted to connect. Venue partnerships became the channel."),
    differently=p(C("what you'd do differently")),
    artifacts=art(("/assets/img/projects/mirrorme/card-category.png", "Category card"), ("/assets/img/projects/mirrorme/card-question.png", "Question card"), ("/assets/img/projects/mirrorme/card-rules.png", "Setup and rules card"), ("/assets/img/projects/mirrorme/card-alt.png", "Alternative card design")),
  ),
  dict(slug="tritooling", emoji="🏭", title="Tritooling",
    kicker="featured · director of operations · Philippines · 2024 to 2025",
    heading="Fixing late deliveries and defects at a precision manufacturer.",
    desc="Director of Operations at a family-owned precision manufacturer serving semiconductor, medical device, and industrial clients across APAC.",
    tldr="A year running operations at a family-owned precision manufacturer serving semiconductor, medical device, and industrial clients. Fewer defects, faster delivery, a board-approved Japan launch.",
    role="Director of Operations", team="Operations, logistics, engineering", timeline="July 2024 to July 2025",
    cover='<img src="/assets/img/thumbs/tritooling-wide.jpg" alt="Engineer working at a precision machine" width="1600" height="900">', cover_class="",
    problem=p("Bottlenecks showed up as late deliveries and defects. Operations, logistics, and engineering had no shared performance framework."),
    did=ul(
      "Redesigned workflows across operations, logistics, and engineering around a performance-management framework, managing 7 direct reports.",
      "Built the ERP make-vs-buy business case from vendor costs and internal requirements. Secured executive approval, $100K in annual savings.",
      "Benchmarked pricing and expansion potential across 5 APAC countries. Secured board approval to launch in Japan, a $300K+ revenue opportunity.",
    ),
    results=results(("+15%", "on-time delivery"), ("−30%", "defects"), ("$100K", "annual savings (ERP make-vs-buy)"), ("$300K+", "revenue opportunity, board-approved Japan launch")),
    differently=p(C("what you'd do differently")),
    artifacts=art(("", "artifact image: sanitized dashboard or shop-floor photo")),
  ),
  dict(slug="smartmodel", emoji="🧭", title="SmartModel",
    kicker="claude code mod · solo build · 2026",
    heading="Matching each prompt to the right model, so easy work costs less.",
    desc="A Claude Code hook that scores how hard each prompt is and recommends the cheapest model that can handle it.",
    tldr="A model router built into Claude Code. Before Claude acts, a hook scores the prompt's effort from 0 to 100 and recommends Haiku, Sonnet, Opus, or Fable. Ask mode shows a picker, auto routes on its own, and block stops the prompt before any tokens are spent.",
    role="Designer and builder", team="Solo, built with Claude Code", timeline="October 2026",
    cover='<img src="/assets/img/thumbs/smartmodel-wide.jpg" alt="SmartModel\'s picker in Claude Code: rates a prompt medium-effort and recommends Sonnet" width="1600" height="900">', cover_class="",
    problem=p("Every prompt ran on the most expensive model, renames and git chores included. Switching by hand meant remembering to, and a fresh session meant losing the conversation."),
    did=ul(
      "Wrote a hook that runs before Claude reads each prompt and scores its effort from 0 to 100 on keywords and structure. Under 20 is Haiku, up to 44 is Sonnet, up to 84 is Opus, and above that is Fable.",
      "Built three modes. Ask shows a picker with the recommendation first. Auto routes silently. Block rejects the prompt before the current model spends a token on it.",
      "Picking a different model hands the whole task to a subagent on that model, with a self-contained brief.",
      "Added inline tags (sm:skip, sm:haiku, sm:opus) and skips for approvals, slash commands, and short acknowledgments like \"thanks\".",
      "Taught it to ignore text the harness injects, like subagent reports and shell output, which kept opening the picker for messages nobody typed.",
      "Logged every decision to a file, so the routing can be audited and tuned.",
    ),
    results=results(("66", "prompts scored across 18 sessions"), ("15", "flagged as Haiku-sized"), ("44", "flagged as Sonnet-sized"), ("35", "non-prompts correctly skipped")) + "\n" + p("59 of those 66 prompts arrived in a session running Opus. Each Haiku or Sonnet recommendation was a chance to do the same work for less."),
    differently=p("Score the work, not the wording. A keyword heuristic reads a short request that mentions git as a chore, even when it means building three pages. Next: let Haiku classify (the hook already supports it when an API key is set) and log which model I actually pick, so the thresholds learn from my overrides."),
    artifacts=p("Not published yet. It lives in my own Claude Code setup as a hook, a small config file, a README, and the decision log. The picker above is a capture of what it shows."),
  ),
  dict(slug="token-fuel", emoji="⛽", title="Token-Fuel",
    kicker="claude code mod · macOS app · 2026",
    heading="Seeing how much context is left before a session runs out.",
    desc="A menu-bar fuel gauge for Claude Code and Codex sessions, built from the exact token counts each tool already writes to disk.",
    tldr="Running out of context is invisible until answers get worse or the session compacts. Token-Fuel makes it visible: a fuel bar in the menu bar and a floating window, with percent left, turns left, and a 12-turn chart, for Claude Code and Codex.",
    role="Product owner and builder", team="Solo, built with Claude Code", timeline="October 2026",
    cover='<img src="/assets/img/thumbs/token-fuel-wide.jpg" alt="Token-Fuel\'s menu-bar gauge and floating window showing context left for Claude Code and Codex" width="1600" height="900">', cover_class="",
    problem=p("Context runs out silently. The Claude desktop Code tab ignores the status-line setting, so there was nowhere to put a gauge, and chat apps keep no token counts at all."),
    did=ul(
      "v0.1: a status-line gauge with a 10-cell fuel bar, turns left, a 12-turn chart, and a \"Refueled\" notice after /compact.",
      "v0.2: a floating pill on the Claude window, because the desktop Code tab ignores status lines.",
      "Fixed the window size. Opus 5 sessions have a 1M window, so assuming 200k made the gauge wrong by 5x.",
      "Tore it all down and ran a feasibility review with one rule: exact sources only. Claude Code and Codex log real token counts, chat apps don't, so chat apps are out.",
      "v1.1: rebuilt as a native Swift menu-bar app with a floating window. Live every 2 seconds, across Claude Code and Codex, launched at login, restarted after a crash.",
    ),
    results=results(("2", "tools gauged from exact logs"), ("2 sec", "refresh, near 0% CPU"), ("~40MB", "memory"), ("12", "turns charted per session")) + "\n" + p("Checked against the logs themselves: the numbers match what each tool records."),
    differently=p("Write the acceptance checks before the build. One rebuild looked done but wasn't. The menu-bar icon hid behind the MacBook notch, the window never updated, and it counted output tokens as context. A checklist drawn from the milestones would have caught all of it on day one."),
    artifacts=p("Not published yet. A native Swift app with a README that records every milestone: what changed, why, and the tradeoff."),
  ),
  dict(slug="code-improver", emoji="🔍", title="Code Improver",
    kicker="claude code mod · subagent · 2026",
    heading="A second reviewer that reads every file I touch.",
    desc="A custom Claude Code subagent that reviews changed files for readability, performance, and best practices.",
    tldr="A read-only reviewer I can call after any change. It explains each issue, shows the current code, and proposes an improved version, without touching a file itself.",
    role="Builder", team="Solo", timeline="October 2026",
    cover='<img src="/assets/img/thumbs/code-improver-wide.jpg" alt="The code-improver subagent definition file" width="1600" height="900">', cover_class="",
    problem=p("Code written fast with an AI pair often gets reviewed by nobody. I wanted a second pass that is consistent, quick, and safe to run anywhere."),
    did=ul(
      "Defined a subagent with one job: scan files for readability, performance, and best-practice issues.",
      "Limited it to read-only tools (Read, Grep, Glob), so it can suggest changes but never make them.",
      "Required the same shape for every finding: the problem, the current code, and an improved version.",
      "Wrote its description so Claude Code knows to reach for it right after code is written or changed.",
    ),
    results=p("Small by design. Eight lines of configuration change how every review goes, and because it can't edit, I can run it on anything."),
    differently=p("Give it a severity ranking and permission to say \"no issues.\" Without one, a reviewer always finds something, and small nits crowd out real bugs."),
    artifacts=p("The file above is the whole thing, verbatim."),
  ),
]

os.makedirs(OUT, exist_ok=True)
n = len(CASES)
for i, c in enumerate(CASES):
    prev, nxt = CASES[(i - 1) % n], CASES[(i + 1) % n]
    html_out = SHELL.format(v=V, nav=NAV, footer=FOOTER, badge=c.get("badge", ""),
        desc=html.escape(c["desc"], quote=True), prev_slug=prev["slug"], prev_title=prev["title"], next_slug=nxt["slug"], next_title=nxt["title"], **{k: v for k, v in c.items() if k not in ("desc", "badge")})
    with open(os.path.join(OUT, c["slug"] + ".html"), "w") as f:
        f.write(html_out)
    print("wrote", c["slug"])

# reference copy of the empty template
with open(os.path.join(OUT, "_template.html"), "w") as f:
    f.write(SHELL.replace("{", "{{").replace("}", "}}").replace("{{v}}", V).replace("{{nav}}", NAV).replace("{{footer}}", FOOTER))
print("wrote _template.html")
