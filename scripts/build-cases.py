#!/usr/bin/env python3
"""Builds the featured / more-work case studies from one template.

Usage:  python3 scripts/build-cases.py
Edits:  change the CASES list below, re-run, commit the generated HTML.
The rendered shell is also written to projects/_template.html for reference.
"""
import os, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stamp_shared import CASE_HEAD_ASSETS, CASE_TOP, CASE_FOOT, CASE_SCRIPTS

ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "projects")
V = "13"  # asset version (cache-bust)

def C(msg):  # visible confirm tag
    return f'<span class="confirm">[CONFIRM: {html.escape(msg)}]</span>'

# Chrome (header, footer, stylesheet links, scripts) is shared with the Stamp homepage; see stamp_shared.py.
NAV = CASE_TOP
FOOTER = CASE_FOOT

# stage gradient behind each cover, from the Stamp tokens
GRAD = {"lucent": "lucent", "ey": "ey", "tritooling": "tri", "mirrorme": "mirror", "mobility": "mobility", "pacman-dqn": "arcade"}

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
{head_assets}
</head>
<body class="v v-stamp case">
  <a class="skip" href="#main">Skip to content</a>
{nav}

  <main id="main">
    <section class="case-hero wrap">
      <a class="case-hero__back" href="{back_href}">← {back_label}</a>
      <p class="eyebrow">{kicker}</p>
      <h1 class="case-hero__title">{heading}{badge}</h1>
      <p class="tldr">{tldr}</p>
      <p class="meta-line"><b>Role</b> {role} · <b>Team</b> {team} · <b>Timeline</b> {timeline}</p>
    </section>

    <section class="wrap case-cover-wrap">
      <div class="stage case-cover {cover_class}" style="--g: var(--g-{grad})">{cover}</div>
    </section>

    <section class="wrap case-body">
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

    <section class="next wrap">
      <div class="next__grid">
        <a href="/projects/{prev_slug}"><small>← Previous</small><strong>{prev_title}</strong></a>
        <a href="/projects/{next_slug}" style="text-align:right"><small>Next →</small><strong>{next_title}</strong></a>
      </div>
    </section>
  </main>

{footer}
{scripts}
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


def links(*pairs):
    return "        <p>" + " · ".join(f'<a href="{u}" target="_blank" rel="noopener">{t} ↗</a>' for t, u in pairs) + "</p>"

def cover(src, alt, w=960, h=600):
    return f'<img src="{src}" alt="{alt}" width="{w}" height="{h}">'

PRODUCTS = [
  dict(slug="tally", emoji="🧮", title="Tally",
    kicker="product · solo build · 2026",
    heading="Knowing how long your to-do list will actually take.",
    desc="A note-taker where every line gets a Claude time estimate, totaled in a ledger so a to-do list becomes an honest picture of the day.",
    tldr="Tally turns a to-do list into a plan. You write lines like a normal note. Claude reads the whole note and gives each line a most-likely time, a range, and a category. The ledger adds it up, and the Day view lets you drag items onto a calendar.",
    role="Product owner and builder", team="Solo, built with Claude Code", timeline="September to October 2026",
    cover=cover("/assets/img/builds/tally.jpg", "Tally estimating a week of to-dos: an hour for the case memo, 30 minutes for bug reports, 3h45 in all"), cover_class="",
    problem=p("A to-do list says what to do, not how long it will take, so a day can be overbooked before it starts. I liked Timely, a note-taker that sizes each line, and wanted my own version: a different design, with the estimates in a column on the right."),
    did=ul(
      "Rebuilt the idea from scratch in React, with an estimate column beside every line.",
      "Sent each line to Claude with the whole note as context. It returns the most likely minutes, an 80% range, a confidence level, and one of seven categories.",
      "Built the Ledger: remaining vs. done, a finish-by time, a capacity meter, where the time goes, quick wins under 15 minutes, and deep-work blocks over 90.",
      "Added a Day view. Drag items from an Unscheduled tray onto the calendar, resize a block to change how long it takes, or do all of it from the keyboard.",
      "Kept the user in charge. Click any estimate to override it, write \"(1h)\" in a line and it's honored exactly, and ⌘B splits a big line into 3 to 7 estimated sub-tasks.",
      "Made it work with no key at all. Estimates fall back to a keyword heuristic, marked with ~. A visitor's own key always pays for their use, and the server key needs an access code.",
    ),
    results=results(("7", "categories per estimate"), ("80%", "range around every estimate"), ("3–7", "sub-tasks per breakdown"), ("0", "accounts needed")) + "\n" + p("Notes live in the browser. Requests are capped at 50 lines and 64 KB per call, so a runaway loop can't run up a bill."),
    differently=p("Test against the deployed runtime, not just the dev server. Vite and the type checker accepted imports that Node rejected once deployed, so I added a check that loads every function the way Vercel does. Next on the roadmap: an agent that does the task, not just sizes it."),
    artifacts=links(("Try Tally", "https://tally-lake-seven.vercel.app"), ("Source on GitHub", "https://github.com/chaekim96/tally")) + "\n" + art(("/assets/img/cases/tally-day.jpg", "The Day view: a capacity meter, the Unscheduled tray, and blocks on the calendar."), ("/assets/img/cases/tally-summary.jpg", "The Summary: what's left, the finish-by time, and where the time goes.")),
  ),
  dict(slug="palette-generator", emoji="🎨", title="Palette Generator",
    kicker="product · solo build · 2026",
    heading="Brand colors and fonts for founders who aren't designers.",
    desc="A palette and font-pairing generator that takes a non-designer from a one-line description to a brand look they can ship.",
    tldr="Describe what you're building and pick a mood. You get five colors with a job for each, a font pairing, and a sample website painted in them. Contrast is checked against WCAG, and the whole result lives in a share link.",
    role="Product owner and builder", team="Solo, built with Claude Code", timeline="September to October 2026",
    cover=cover("/assets/img/builds/palette.jpg", "Palette Generator turning 'coffee subscription, warm and earthy' into five roles of color and a font pairing"), cover_class="",
    problem=p("Founders need a brand look long before they can hire a designer. Most palette tools hand you five pretty colors and stop there. Which one is the button? Which is the text? Can anyone read it?"),
    did=ul(
      "Started from a Figma Make export and set one rule for every feature: does it get a non-designer to a shippable palette faster? If not, it waits.",
      "Generated palettes in OKLCH across seven moods, and tuned the Earthy and Romantic moods against a benchmark of 97 real palettes.",
      "Gave every color a job (text, primary, supporting, accent, background) and matched it with one of 25 curated Google Fonts pairings.",
      "Painted a sample startup homepage in the palette, and checked every color pairing for WCAG contrast, with the smallest fix suggested when one fails.",
      "Built Explore: a weekly scan of 115 startup homepages showing which moods and brand colors are common right now. Curated public sites only, robots.txt respected.",
      "Kept it serverless. The palette, fonts, and mood live in the URL, so sharing is copying a link. Export goes to CSS variables, Tailwind, or a PNG.",
    ),
    results=results(("7", "moods"), ("25", "curated font pairings"), ("115", "startup homepages scanned weekly"), ("0", "sign-ups")) + "\n" + p("The coffee subscription palette above passes WCAG AA on all seven of its color pairings."),
    differently=p("Build the benchmark before the generator. I tuned the moods against real palettes only after the first version worked. Starting with the benchmark would have set the target on day one."),
    artifacts=links(("Try Palette Generator", "https://color-palette-generator-three-sand.vercel.app"), ("Source on GitHub", "https://github.com/chaekim96/ColorPaletteGenerator")) + "\n" + art(("/assets/img/cases/palette-preview.jpg", "Website preview: the palette painted onto a sample startup homepage, with the contrast check above it."), ("/assets/img/cases/palette-explore.jpg", "Explore: moods and brand colors across 115 startup homepages, refreshed weekly.")),
  ),
  dict(slug="typerace", emoji="⌨️", title="TypeRace",
    kicker="product · solo build · 2026",
    heading="Settling who types fastest, with one link and no sign-up.",
    desc="A live browser typing race for classmates: share a four-letter code, type the same short story, first to finish wins.",
    tldr="Start a room and share the link. Everyone types the same short story at once, with live progress bars, WPM, and accuracy, then a results chart and a weekly class leaderboard. No accounts, no ads.",
    role="Product owner and builder", team="Solo, built with Claude Code", timeline="October 2026",
    cover=cover("/assets/img/builds/typerace.jpg", "A TypeRace race in progress at 72 WPM, the progress bar halfway across"), cover_class="",
    problem=p("Typing races are a fun way to compete with friends. I wanted one a class could join from one link in a few seconds, on a laptop or a phone, with no accounts and no ads."),
    did=ul(
      "Wrote a PRD first, then built to it: rooms by four-letter code, a synced countdown, live progress, results, and rejoining after a refresh.",
      "Ran each room as one Cloudflare Durable Object, so a race needs no database. Progress updates are under 30 bytes, about ten a second.",
      "Checked typing in the browser with zero network delay. One input path handles desktop keyboards, phone keyboards, autocorrect, and smart quotes.",
      "Made the start fair. Each browser syncs its clock with the server and counts down to the same instant, on timers rather than animation frames, so background tabs still hear GO.",
      "Added anti-cheat (big jumps or a finish above 250 WPM count as did-not-finish) and a weekly top-10 leaderboard that resets Monday at midnight Pacific.",
      "Wrote a 3-bot simulation that runs a full race end to end, in unranked rooms so test bots stay off the real board.",
    ),
    results=results(("10", "players per room"), ("20", "original stories"), ("<30 B", "per progress update"), ("11.5 KB", "client code, gzipped")),
    differently=p("Keep test traffic out of production by design. Right after one deploy, my simulation put two bots on the live leaderboard because the old server was still answering. I removed them and made the simulation wait for the new version, but that guard should have come first."),
    artifacts=links(("Play TypeRace", "https://typerace.typerace.workers.dev")) + "\n" + art(("/assets/img/cases/typerace-results.jpg", "Results: finishing order, WPM, accuracy, and a WPM chart for the race.")),
  ),
  dict(slug="networking-tracker", emoji="🗂️", title="Networking Tracker",
    kicker="product · solo build · 2026",
    heading="Keeping track of every coffee chat, without sharing a thing.",
    desc="A private contact tracker where Postgres row-level security keeps each person's data their own.",
    tldr="Sign in and keep a list of the people you meet: company, role, where you met, notes, and priority. Sort, filter, and search it. Every row is private to the person who wrote it, and the database enforces that, not just the app.",
    role="Builder", team="Solo", timeline="September 2026",
    cover=cover("/assets/img/builds/networking-tracker.jpg", "Networking Tracker filtered to high-priority contacts, with demo data"), cover_class="",
    problem=p("At Berkeley you meet a lot of people quickly, and notes on them end up scattered. A tool for that has to answer one question before any other: can anyone else see my contacts?"),
    did=ul(
      "Built sign-up, sign-in, and a contact list with create, edit, delete, sort, filter, and search, in Next.js on Vercel.",
      "Stored contacts in Neon Postgres and isolated them with row-level security in the database, so even a direct call to the public Data API can't read someone else's rows.",
      "Proved it. Queried as the role the API uses while two rows existed, and got zero back.",
      "Validated input three times: in the form, on the server, and with a database constraint. The friendly message is a courtesy, not the defense.",
      "Designed all four list states: loading skeletons, two distinct empty states, a plain-language error with one-click retry, and success.",
      "Captured every screenshot in the write-up from the deployed app, not localhost.",
    ),
    results=results(("0", "rows visible to the wrong user"), ("3", "layers of input validation"), ("4", "list states designed"), ("15", "screenshots from the live app")),
    differently=p("Check the security boundary on every push. The isolation test needs two real accounts and a live database, so today it runs on demand. Next: run it in CI against a throwaway database branch that seeds its own accounts."),
    artifacts=links(("Try it", "https://networking-tracker-five-sage.vercel.app"), ("Source on GitHub", "https://github.com/chaekim96/networking-tracker")) + "\n" + art(("/assets/img/cases/nt-invalid.jpg", "An empty name, rejected with the reason in plain language. Demo data."), ("/assets/img/cases/nt-mobile.jpg", "The contact list on a phone. Demo data.")),
  ),
  dict(slug="voiceprompter", emoji="🎙️", title="VoicePrompter",
    kicker="product · macOS app · 2026",
    heading="Reading your notes on a call without anyone seeing them.",
    desc="A macOS teleprompter that follows your voice as you read and stays hidden from Zoom, Meet, and screenshots.",
    tldr="Your script floats above every app, even full-screen ones. As you speak, it highlights the word you're on and scrolls to keep your line near the top. Screen sharing and recordings that use ScreenCaptureKit, including Zoom, Google Meet, OBS, and QuickTime, don't see it.",
    role="Builder", team="Solo, built with Claude Code", timeline="September to October 2026",
    cover=cover("/assets/img/builds/voiceprompter.jpg", "VoicePrompter listening at word 108 of 139, with the prompter highlighting the spoken word", 800, 600), cover_class="",
    problem=p("I was practicing presenting and interviewing and wanted my notes on screen, without cluttering the screen I was sharing. The teleprompters I found either fell short or wanted me to pay."),
    did=ul(
      "Built a native Swift app: an overlay that floats on every Space, and a main window with every setting in a sidebar.",
      "Transcribed speech on the device with Apple's recognizer, restarting the session about every 50 seconds so results stay short and fast.",
      "Wrote the alignment. Each update matches the last 8 spoken words against the script, with fuzzy matching for misheard words and guards so it never jumps on weak evidence.",
      "Hid the overlay from capture, then tested it. It's hidden from ScreenCaptureKit, screenshots, and window lists, and still visible to older recorders, which the README says plainly.",
      "Added global hotkeys that need no Accessibility permission, double-click to jump to a word, and click-through so clicks reach the app underneath.",
    ),
    results=results(("~0.3 ms", "per update on an 8,800-word script"), ("8", "spoken words matched each update"), ("2", "permissions: mic and speech"), ("4", "capture tools it hides from")),
    differently=p("Measure latency from the start. The speech recognizer dominates the delay, and I built the latency test only after the app worked. A full, uninterrupted latency run is still on my list."),
    artifacts=links(("Source on GitHub", "https://github.com/chaekim96/VoicePrompter")) + "\n" + art(("/assets/img/cases/vp-main.jpg", "The main window while listening: status, position in the script, and prompter settings."), ("/assets/img/cases/vp-prompter.jpg", "The prompter further in. Read text dims and the current word turns gold. Captured with protection off.")),
  ),
]

COURSEWORK = [
  dict(slug="personal-wiki", emoji="📚", title="Personal Wiki",
    kicker="ai/ml coursework · mba 290t · 2026",
    heading="Asking my own notes questions, with no internet.",
    desc="A command-line study wiki that runs fully offline: a local Gemma model turns sources into linked Obsidian notes and answers questions with citations.",
    tldr="A study wiki for my AI course that never touches the cloud. Local Gemma, through Ollama, turns sources into linked Obsidian notes. An ask command answers from those notes with citations, or says the evidence isn't there.",
    role="Builder", team="Solo", timeline="September 2026",
    cover=cover("/assets/img/builds/personal-wiki.jpg", "Obsidian graph of the wiki's linked notes", 900, 646), cover_class="",
    problem=p("Cloud assistants answer confidently from anywhere. For studying I wanted the opposite: answers only from my own sources, a citation for every claim, on a laptop with Wi-Fi off."),
    did=ul(
      "Picked the model to fit the machine. Gemma 4 E2B at 4-bit, because the larger versions didn't fit in the 5 to 6 GB free on an 18 GB Mac.",
      "Wrote the CLI and harness with only Python's standard library: ingest, search, ask, and chat modes.",
      "Built hybrid retrieval: my own BM25 plus local embeddings, merged with reciprocal rank fusion.",
      "Wrote the expected answers for four tests before running them, including one the wiki should refuse.",
      "Checked every citation in code, with one automatic retry when a citation doesn't point to a retrieved passage.",
      "Recorded an offline demo with Wi-Fi off. All four tests matched the online results.",
    ),
    results=results(("3 of 4", "tests passed, written in advance"), ("4.4 s", "per answer, warm"), ("~1.7 GB", "working memory"), ("0", "cloud calls")) + "\n" + p("The failure is documented. A question in my own shorthand (\"A3\") missed the right passage, and the model answered a nearby question with a real citation."),
    differently=p("A citation check proves a citation exists, not that it answers the question. Next: an alias file so my shorthand expands (A3 means Assignment 3), a guaranteed slot for each source's best passage, and a second check that asks whether the answer fits the question."),
    artifacts=links(("Source and evidence on GitHub", "https://github.com/chaekim96/personal-wiki")) + "\n" + art(("/assets/img/cases/wiki-note.jpg", "A generated note in Obsidian, with its sources linked back to the raw files."), ("/assets/img/cases/wiki-index.jpg", "The wiki's index: concepts and projects, each with a one-line summary.")),
  ),
  dict(slug="pacman-dqn", emoji="👾", title="Pac-Man DQN",
    kicker="ai/ml coursework · 2026",
    heading="Teaching an agent to play Ms. Pac-Man by trial and error.",
    desc="A Deep Q-Network trained on Atari Ms. Pac-Man, with every number reported straight from the run's own output files.",
    tldr="An agent that sees only pixels and points learned Ms. Pac-Man over 100 games. Its mean score across five fixed test games rose from 492 to 680. I chose three settings, ran it once end to end, and reported what happened, including where it got worse.",
    role="Builder", team="Solo", timeline="September 2026",
    cover='<img src="/assets/img/builds/pacman-dqn.gif" alt="The trained agent playing Ms. Pac-Man" width="160" height="210" style="image-rendering:pixelated;height:clamp(260px,40vw,460px);width:auto;margin:0 auto;padding:24px 0;display:block;box-sizing:content-box">', cover_class="",
    problem=p("Reinforcement learning is easy to describe and hard to trust. The question wasn't only whether the score goes up, but whether the gain is real or noise."),
    did=ul(
      "Chose three settings and justified each: 100 episodes, exploration held at 0.20 as a control, and a learning rate 2.5x the reference so change would show up in a short run.",
      "Wrote down my expectation before running: a modest gain of about 100 to 200 points.",
      "Trained on a laptop GPU: 57,801 decisions and 14,201 updates in about 3.3 minutes.",
      "Evaluated before and after on the same five seeds, and kept every GIF, plot, and checkpoint.",
      "Explained the surprise. Loss went up while scores improved, which is expected in DQN as the value targets grow.",
    ),
    results=results(("492 → 680", "mean evaluation score"), ("+188", "inside my predicted range"), ("4 of 5", "test games improved"), ("3.3 min", "to train")),
    differently=p("Five test games is too few to trust the mean. One game fell from 800 to 300, and the curve was flat for 80 episodes before a late jump. Next experiment: change only the episodes, from 100 to 500, to see whether the gain holds or was a lucky streak."),
    artifacts=links(("Notebook and evidence on GitHub", "https://github.com/chaekim96/pacman-dqn")) + "\n" + art(("/assets/img/cases/pacman-untrained.gif", "Before training: the agent mostly circles one corner of the maze."), ("/assets/img/cases/pacman-trained.gif", "After training: the best game from the final evaluation."), ("/assets/img/cases/pacman-training.jpg", "The training dashboard: scores, update loss, and exploration per episode.")),
  ),
  dict(slug="custom-llm", emoji="🧠", title="Custom LLM",
    kicker="ai/ml coursework · mba 290t · 2026",
    heading="Seeing how language models learn by training a tiny one.",
    desc="A tiny nanoGPT model trained from scratch on a laptop CPU, with my own teaching corpus and 48 fixed language tests.",
    tldr="A word-level language model with 2 blocks and 4 heads, trained in about 14 seconds on a laptop. I ran it twice, on the starter corpus and then with my own files on grammar, opposites, and spatial relations, and scored both on the same 48 tests.",
    role="Builder", team="Solo", timeline="September 2026",
    cover=cover("/assets/img/builds/custom-llm.jpg", "Terminal chat with the tiny model and its odd replies", 768, 474), cover_class="",
    problem=p("It's hard to build intuition for language models when the ones you use have billions of parameters. A model small enough to train in seconds makes every step visible: tokens, vectors, probabilities, and updates."),
    did=ul(
      "Predicted each result in writing before every run, then compared.",
      "Wrote 355 new teaching passages on tense and agreement, opposites, and spatial relations, without reading the test items.",
      "Trained two experiments with identical settings: 3,000 steps at a learning rate of 0.001, on a laptop CPU.",
      "Traced one token all the way through: word to ID to vector to probability to gradient to update.",
      "Built a small chat interface and was clear about what it is: a sentence continuer, not a chatbot.",
    ),
    results=results(("9 → 20", "of 48 tests, starter corpus"), ("7 → 25", "of 48 tests, with my corpus"), ("16/16", "familiar patterns"), ("14 s", "to train")),
    differently=p("The model learned templates, not language. And because the public tests guided my choices, a good score doesn't prove it generalizes. Next: write my own held-out test set and never look at it while building the corpus."),
    artifacts=links(("Write-up and evidence on GitHub", "https://github.com/chaekim96/custom-llm")),
  ),
]

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
    results=results(("1", "first paying pilot"), ("5", "LOIs in 30 days"), ("+50%", "discovery response rate"), ("NSF", "I-Corps backing")) + "\n" + p("The pilot became an ongoing advisory relationship."),
    differently=p("Lock the GTM motion earlier. Investors flagged it as the biggest gap. Positioning tests and pilots should have run in parallel, not in sequence."),
    artifacts="",
  ),
  dict(slug="mobility", emoji="🦯", title="Mobility devices for older adults (stealth)",
    kicker="in progress · co-founder · stealth",
    heading="Mobility aids people aren't embarrassed to use.",
    badge='<span class="stealth">Stealth</span>',
    desc="Premium, design-forward mobility products that help older adults stay independent longer.",
    tldr="Premium, design-forward mobility products that help older adults stay independent longer.",
    role="Co-founder: GTM, brand, outreach, strategy (my co-founder owns product)", team="2 co-founders", timeline="In progress",
    cover='<img src="/assets/img/thumbs/mobility-wide.jpg" alt="An older couple walking along a garden path" width="1600" height="900">', cover_class="",
    problem=p("Mobility aids look like medical equipment. Users feel stigmatized, and common designs have real safety gaps."),
    did=ul(
      "Visited senior centers and assisted living facilities around Berkeley. 14+ conversations with operators, caregivers, and advisors.",
      "Studied why companies here stall: payer, user, and decider are three different people; hardware margins erode; incumbents own distribution.",
      "Built the brand-as-moat thesis and a decision framework for the first product.",
      "Set an operating cadence for a team 16 time zones apart.",
    ),
    results=p("Early stage and in progress. Results will be added as they're shareable."),
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
    differently="",
    artifacts="",
  ),
  dict(slug="mirrorme", emoji="🃏", title="MirrorMe",
    kicker="more work · co-founder, GTM · 2024",
    heading="Icebreakers that go deeper without getting awkward.",
    desc="An icebreaker card game for people who host. 150+ pre-launch purchase commitments with zero paid budget.",
    tldr="An icebreaker card game for hosts. 150+ pre-launch commitments at $30 to 40, with zero paid budget.",
    role="Co-founder, led GTM", team="2 co-founders", timeline="2024",
    cover='<img src="/assets/img/thumbs/mirrorme-wide.jpg" alt="MirrorMe question card" width="1600" height="900">', cover_class="",
    problem=p("Hosts want guests to actually talk. Most icebreakers are too shallow to matter or too intense for near-strangers."),
    did=ul(
      "100+ user surveys and a 10-product competitive scan found two high-intent segments: regular hosts, and the venues that host them.",
      "Built the deck on the OCEAN personality model: category cards set a trait, question cards ask about someone at the table, players rate 1 to 5.",
      "Skipped paid channels. Sold in person at card game cafes and social events in New York. 50+ decks sold.",
    ),
    results=results(("150+", "pre-launch purchase commitments"), ("$30 to 40", "price point"), ("$0", "paid budget"), ("50+", "decks sold")) + "\n" + p("Insight: it sold itself in rooms where people already wanted to connect. Venue partnerships became the channel."),
    differently="",
    artifacts=art(("/assets/img/projects/mirrorme/card-category.png", "Category card"), ("/assets/img/projects/mirrorme/card-question.png", "Question card"), ("/assets/img/projects/mirrorme/card-rules.jpg", "Setup and rules card"), ("/assets/img/projects/mirrorme/card-alt.png", "Alternative card design")),
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
    differently="",
    artifacts="",
  ),
  *PRODUCTS,
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
    artifacts=links(("Source on GitHub", "https://github.com/chaekim96/smartmodel")) + "\n" + p("A hook, a small config file, a README, and the decision log. The picker above is a capture of what it shows."),
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
    artifacts=links(("Source on GitHub", "https://github.com/chaekim96/token-fuel")) + "\n" + p("A native Swift app with a README that records every milestone: what changed, why, and the tradeoff.") + "\n" + art(("/assets/img/builds/token-fuel.jpg", "Running on my Mac: the menu-bar gauge at 67%, and the floating window for this session.")),
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
    artifacts=p("The file above is the whole thing, verbatim. Below, it reviewing the script that builds this page: 14 findings, ordered by severity, and no files touched.") + "\n" + art(("/assets/img/cases/code-improver-review.jpg", "An excerpt of its review of build-cases.py. Its top finding checked out on the live site.")),
  ),
  *COURSEWORK,
]

os.makedirs(OUT, exist_ok=True)
n = len(CASES)
for i, c in enumerate(CASES):
    prev, nxt = CASES[(i - 1) % n], CASES[(i + 1) % n]
    is_build = c in PRODUCTS or c in COURSEWORK or c["slug"] in ("smartmodel", "token-fuel", "code-improver")
    html_out = SHELL.format(head_assets=CASE_HEAD_ASSETS, scripts=CASE_SCRIPTS, grad=GRAD.get(c["slug"], "plain"), nav=NAV, footer=FOOTER, badge=c.get("badge", ""), back_href="/#builds" if is_build else "/#work", back_label="All builds" if is_build else "All work",
        desc=html.escape(c["desc"], quote=True), prev_slug=prev["slug"], prev_title=prev["title"], next_slug=nxt["slug"], next_title=nxt["title"], **{k: v for k, v in c.items() if k not in ("desc", "badge")})
    for key, anchor, label in (("differently", "differently", "What I'd do differently"), ("artifacts", "artifacts", "Artifacts")):
        if not c.get(key, "").strip():
            html_out = html_out.replace(f'        <a href="#{anchor}">{label}</a>\n', "").replace(f'        <h2 id="{anchor}">{label}</h2>\n\n', "")
    with open(os.path.join(OUT, c["slug"] + ".html"), "w") as f:
        f.write(html_out)
    print("wrote", c["slug"])

# reference copy of the empty template
with open(os.path.join(OUT, "_template.html"), "w") as f:
    f.write(SHELL.replace("{", "{{").replace("}", "}}").replace("{{head_assets}}", CASE_HEAD_ASSETS).replace("{{scripts}}", CASE_SCRIPTS).replace("{{nav}}", NAV).replace("{{footer}}", FOOTER))
print("wrote _template.html")
