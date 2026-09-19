#!/usr/bin/env python3
"""Builds the featured / more-work case studies from one template.

Usage:  python3 scripts/build-cases.py
Edits:  change the CASES list below, re-run, commit the generated HTML.
The rendered shell is also written to projects/_template.html for reference.
"""
import os, html

ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "projects")
V = "9"  # asset version (cache-bust)

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
  <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Lato:wght@400;700&display=swap" onload="this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Lato:wght@400;700&display=swap"></noscript>
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
        <a class="case-hero__back" href="/#work">← All work</a>
        <div class="case-hero__emoji" aria-hidden="true">{emoji}</div>
        <p class="eyebrow" style="margin-top:14px">{kicker}</p>
        <h1 class="display case-hero__title">{heading}{badge}</h1>
        <p class="tldr">{tldr}</p>
        <p class="meta-line"><b>Role</b> {role} · <b>Team</b> {team} · <b>Timeline</b> {timeline}</p>
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
    kicker="Featured · Co-founder & CEO · NSF I-Corps",
    heading="Lucent",
    desc="AI search visibility for small businesses. Lucent shows brands how they appear in ChatGPT, Perplexity, Gemini, and Claude answers, then helps them fix it.",
    tldr="AI search visibility for small businesses. See how your brand shows up in ChatGPT, Perplexity, Gemini, and Claude, then fix it.",
    role="Co-founder & CEO", team="Co-founder/CTO + a data science intern", timeline="October 2025 to present",
    cover='<a href="https://trylucent.ai" target="_blank" rel="noopener" aria-label="Open trylucent.ai"><img src="/assets/img/thumbs/lucent-wide.jpg" alt="Lucent homepage: The AI Search Console" width="1600" height="900"></a>', cover_class="",
    problem=p("Customers now ask AI instead of Google. Small businesses can't see whether AI recommends them, and GEO tools are priced for enterprises."),
    did=ul(
      "21 NSF I-Corps discovery interviews narrowed the ICP from \"everyone\" to digitally native SMBs and marketing agencies. 100+ interviews across U.S. and APAC SMBs tested willingness to pay.",
      "Positioned around the one-person marketing team: GEO plus SEO execution, not just citation tracking. 10 positioning tests across 65 prospects picked the message.",
      "Designed cheap tracking: statistical sampling, and re-running prompts only when models or rankings change.",
      "Led a paid pilot: multi-site SEO and AI visibility audits turned into an engineering action plan.",
      "Built the investor pitch: bottom-up SAM, phased GTM, 100+ question diligence bank.",
    ),
    results=results(("1", "first paying pilot"), ("5", "LOIs in 30 days"), ("+50%", "discovery response rate"), ("NSF", "I-Corps backing")) + "\n" + p("The pilot became an ongoing advisory relationship. " + C("any usage or revenue metric you're comfortable sharing")),
    differently=p("Lock the GTM motion earlier. Investors flagged it as the biggest gap. Positioning tests and pilots should have run in parallel, not in sequence."),
    artifacts=art(("", "artifact image: product screenshot (no client data)"), ("", "artifact image: pitch deck excerpt, e.g. SAM or GTM slide")),
  ),
  dict(slug="mobility", emoji="🦯", title="Mobility devices for older adults (stealth)",
    kicker="Featured · Co-founder · Stealth",
    heading="Mobility devices for older adults",
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
    results=p(C("what's shareable, e.g. advisors onboarded, prototype stage")),
    differently=p(C("what you'd do differently")),
    artifacts=art(("", "artifact image (nothing that shows the mechanism)")),
  ),
  dict(slug="ey", emoji="☁️", title="EY, AI & Data",
    kicker="Featured · Senior Consultant · New York · 2021 to 2024",
    heading="Cloud migration at Fortune 500 scale",
    desc="Program-wide risk, OKRs, and the first QBR for a $200M+ cloud migration at a Fortune 500 life sciences client, which contributed to a $14M contract extension.",
    tldr="Ran the operating system for a $200M+ cloud migration at a Fortune 500 life sciences client: risk, OKRs, and the first executive QBR. It helped secure a $14M extension.",
    role="Senior Consultant, AI & Data Strategy (Staff Consultant 2021 to 2023)", team="EY Technology Consulting, 25+ client teams", timeline="August 2021 to July 2024",
    cover='<img src="/assets/img/thumbs/ey-wide.jpg" alt="Earth at night from orbit, city lights glowing" width="1600" height="900">', cover_class="",
    problem=p("A Fortune 500 life sciences client was moving its application portfolio to the cloud across 25+ teams. Risks surfaced late, executives got escalations instead of decisions, and nobody had one view of what was on track."),
    did=ul(
      "Built the program-wide risk and OKR system: blocker and risk triage across 25+ teams. Earlier resource reallocation, 30% fewer executive escalations.",
      "Designed and launched the client's first QBR from 50+ executive interviews, then standardized QBR governance across 5+ programs.",
      "Drove adoption of a custom PM methodology with a 15-person team and hands-on tool training. 90% adoption across 4,000 users.",
      "Prioritized every application for migration, modernization, or retirement with a value-capture framework. SVP approval, $10M+ savings over 3+ years.",
    ),
    results=results(("$14M", "contract extension secured"), ("−30%", "executive escalations"), ("90%", "adoption across 4,000 users"), ("$10M+", "savings identified over 3+ years")) + "\n" + p("Also at EY: logistics lead for a Fortune 500 consumer foods client (on-time delivery +20%, accuracy +10% YoY), data architect on an internal initiative, and an internal AI adoption campaign that drove 200%+ usage across 5 user segments. Earlier: recovered $5M in pricing and mix leakage for a Fortune 500 software client, and re-architected Agile workflows for 25+ engineering teams (delivery +40% YoY)."),
    differently=p(C("what you'd do differently")),
    artifacts=art(("", "artifact image: sanitized QBR or OKR dashboard excerpt")),
  ),
  dict(slug="mirrorme", emoji="🃏", title="MirrorMe",
    kicker="More work · Co-founder, GTM · 2024",
    heading="MirrorMe",
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
    kicker="More work · Director of Operations · Philippines · 2024 to 2025",
    heading="Running operations at a precision manufacturer",
    desc="Director of Operations at a family-owned precision manufacturer serving semiconductor, medical device, and industrial clients across APAC.",
    tldr="A year running operations at a family-owned precision manufacturer serving semiconductor, medical device, and industrial clients. Fewer defects, faster delivery, a board-approved market entry.",
    role="Director of Operations", team="Operations, logistics, engineering", timeline="July 2024 to July 2025",
    cover='<img src="/assets/img/thumbs/tritooling-wide.jpg" alt="Engineer working at a precision machine" width="1600" height="900">', cover_class="",
    problem=p("Bottlenecks showed up as late deliveries and defects. Operations, logistics, and engineering had no shared performance framework."),
    did=ul(
      "Redesigned workflows across operations, logistics, and engineering around a performance-management framework.",
      "Built the ERP insourcing business case from vendor costs and internal requirements. Presented to leadership.",
      "Built a market entry case for 5 APAC countries from pricing benchmarks and scope expansion. " + C("doc says 'Japan market entry', resume says 5 APAC countries. Which wording?"),
    ),
    results=results(("+15%", "on-time delivery"), ("−30%", "defects"), ("$1.5M", "projected annual savings (ERP insourcing)"), ("$800K+", "revenue potential, board-approved launch")),
    differently=p(C("what you'd do differently")),
    artifacts=art(("", "artifact image: sanitized dashboard or shop-floor photo")),
  ),
  dict(slug="events-app", emoji="📱", title="Events app",
    kicker="More work · Engineering · Solo build",
    heading="Events app",
    desc="A full-stack events app built to learn how production systems fit together, end to end. React Native, NestJS, PostgreSQL, Stripe, Twilio, and more.",
    tldr=C("what the app does in one sentence") + " Built to learn how production systems fit together, end to end.",
    role="Solo developer", team="Just me", timeline=C("timeline"),
    cover='<img src="/assets/img/thumbs/events-app-wide.jpg" alt="Confetti falling over a crowd at a night event" width="1600" height="900">', cover_class="",
    problem=p("Tutorials teach one layer at a time. I wanted to see where a real product breaks: auth, payments, notifications, uploads, observability, wired together."),
    did=ul(
      "Mobile: React Native, Expo, TypeScript.",
      "API: NestJS with PostgreSQL and Prisma, Redis for caching and queues.",
      "Integrations: Stripe (payments), Twilio (SMS), SendGrid (email), AWS S3 (uploads).",
      "Observability: PostHog for product analytics, Sentry for errors.",
    ),
    results=p("Status: " + C("status, demo link or screenshots")),
    differently=p(C("what you'd do differently")),
    artifacts=art(("", "artifact image: app screenshots")),
  ),
  dict(slug="berkeley-builders", emoji="🛠️", title="Berkeley Builders Summer Program",
    kicker="More work · Organizer · Haas",
    heading="Berkeley Builders Summer Program",
    desc="Organized a structured summer accelerator for founders at Haas.",
    tldr="Organized a structured summer accelerator for founders at Haas.",
    role="Organizer", team=C("co-organizers"), timeline=C("dates, e.g. summer 2026"),
    cover='<img src="/assets/img/thumbs/berkeley-builders-wide.jpg" alt="A team planning at a whiteboard covered in sticky notes" width="1600" height="900">', cover_class="",
    problem=p("Haas founders lose the summer to unstructured time. The program gave them cadence, peers, and accountability."),
    did=ul(C("2 to 4 bullets: format, cadence, sessions, who you recruited")),
    results=p(C("number of teams/participants, outcomes")),
    differently=p(C("what you'd do differently")),
    artifacts=art(("", "artifact image: program schedule or cohort photo")),
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
