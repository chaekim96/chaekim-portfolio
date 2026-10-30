#!/usr/bin/env python3
"""Builds the featured / more-work case studies from one template.

Usage:  python3 scripts/build-cases.py            (write every page)
        python3 scripts/build-cases.py --check    (write nothing; fail if a page is out of date)
Edits:  change the CASES list below, re-run, commit the generated HTML.
The page template is SHELL below. (No rendered copy is written: everything in the
repo is deployed, so a copy in projects/ would be a public page.)
"""
import html
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = ROOT / "projects"
SITE_URL = "https://chaekim-portfolio.vercel.app"

# The script name has a hyphen, so it can't be imported as a package; load the sibling module by path.
sys.path.insert(0, str(HERE))
from stamp_shared import CASE_HEAD_ASSETS, CASE_TOP, CASE_FOOT, CASE_SCRIPTS, LIVE_APPS, LIVE_DIALOG, LIVE_SCRIPT, live_button, build_mark, build_icons  # noqa: E402

def confirm_tag(msg):  # visible confirm tag
    return f'<span class="confirm">[CONFIRM: {html.escape(msg)}]</span>'

# Chrome (header, footer, stylesheet links, scripts) is shared with the Stamp homepage; see stamp_shared.py.

# stage gradient behind each cover, from the Stamp tokens
GRAD = {"lucent": "lucent", "ey": "ey", "tritooling": "tri", "mirrorme": "mirror", "mobility": "mobility", "pacman-dqn": "arcade"}

SITE_ICONS = ('  <link rel="icon" href="/favicon.svg" type="image/svg+xml">\n'
              '  <link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">\n'
              '  <link rel="apple-touch-icon" href="/apple-touch-icon.png">')

SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} · Chae Kim - Portfolio</title>
  <meta name="description" content="{desc}">
  <meta property="og:title" content="{title} · Chae Kim - Portfolio">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="article">
  <meta property="og:image" content="{og_image}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <link rel="canonical" href="{site_url}/projects/{slug}">
{icons}
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{head_assets}
{jsonld}
</head>
<body class="v v-stamp case {sec}">
  <a class="skip" href="#main">Skip to content</a>
{top}

  <main id="main">
    <section class="case-hero wrap">
      <a class="case-hero__back" href="{back_href}">← {back_label}</a>
      {mark}<p class="eyebrow">{kicker}</p>
      <h1 class="case-hero__title">{heading}{badge}</h1>
      <p class="tldr">{tldr}</p>
      <p class="meta-line"><b>Role</b> {role} · <b>Team</b> {team} · <b>Timeline</b> {timeline}</p>
    </section>

    <section class="wrap case-cover-wrap">
      <div class="stage case-cover {cover_class}" style="--g: var(--g-{grad})">{cover}{live}</div>
    </section>

    <section class="wrap case-body">
      <nav class="toc" aria-label="On this page">
{toc}
      </nav>
      <article class="prose">
{body}
      </article>
    </section>

    <section class="next wrap">
      <div class="next__grid">
        <a href="/projects/{prev_slug}"><small>← Previous</small><strong>{prev_title}</strong></a>
        <a class="next__forward" href="/projects/{next_slug}"><small>Next →</small><strong>{next_title}</strong></a>
      </div>
    </section>
  </main>

{foot}
{live_dialog}{scripts}{live_script}
</body>
</html>
"""

def paras(*texts):
    return "\n".join(f"        <p>{x}</p>" for x in texts)

def bullets(*items):
    return "        <ul>\n" + "\n".join(f"          <li>{x}</li>" for x in items) + "\n        </ul>"

def stat_grid(*pairs):
    cells = "".join(f'<div><b>{b}</b><span>{s}</span></div>' for b, s in pairs)
    return f'        <div class="results">{cells}</div>'

def artifact_grid(*items):
    """items: (src, caption) for real images, or ('', caption) for a placeholder."""
    out = []
    for src, cap in items:
        if src:
            out.append(f'<figure><img src="{src}" alt="{html.escape(cap)}" loading="lazy"><figcaption>{cap}</figcaption></figure>')
        else:
            out.append(f'<div class="ph">{C(cap)}</div>')
    return '        <div class="artifacts">' + "".join(out) + "</div>"



def links(*pairs):
    return "        <p>" + " · ".join(f'<a href="{u}" target="_blank" rel="noopener">{t} ↗</a>' for t, u in pairs) + "</p>"

def cover(src, alt, w=960, h=600):
    return f'<img src="{src}" alt="{html.escape(alt)}" width="{w}" height="{h}">'

PRODUCTS = [
  dict(slug="relay", title="Relay: YouTube to action",
    kicker="product concept · interactive prototype · 2026",
    heading="Turning a saved playlist into something you can do.",
    desc="Relay is an interactive product concept that bridges video learning and project work: import a playlist, follow a plan, practice alongside the source, and submit a project for actionable feedback.",
    tldr="YouTube makes it easy to collect explanations. The hard part is turning them into a skill. Relay explores the missing step: a playlist becomes a goal, a realistic practice plan, five small tasks, and a finished project. This is an independent, browser-local concept, not a launched YouTube integration.",
    role="Product concept and interaction design", team="Independent concept, prototyped with Codex", timeline="October 2026",
    cover=cover("/assets/img/builds/relay-cover.svg", "Relay concept: a learning plan connects source videos to practice tasks and a final project", 1200, 750),
    problem=paras("A saved playlist captures intent, but it does not tell a learner what to practice, how much time to reserve, or whether they can apply the idea. The opportunity is to bridge the video and the learner’s notebook with a concrete output.", "The working hypothesis: self-directed beginners are more likely to put a lesson into practice when each video has one small task and every task contributes to a project. This is a hypothesis to test, not a finding from user research."),
    requirements=bullets("Start with a playlist and an outcome, then make the time commitment visible.", "Keep source material within reach while capturing notes and practicing.", "Measure watching and doing separately. A watched video is not evidence of competence.", "End with a project and a useful next iteration, with honest limits on automated feedback."),
    did=bullets("Designed five connected views: overview, learning plan, video workspace, task checklist, and project submission with feedback.", "Built a responsive, keyboard-accessible prototype in plain HTML, CSS, and JavaScript. Notes, task progress, and draft submissions persist in local browser storage.", "Used a realistic landing-page learning path with creator source links, four authored lessons, five exercises, and a project rubric.", "Made import validation and sample loading explicit. Custom URLs do not trigger API calls, and feedback is a labeled, deterministic checklist rather than a claim that AI reviewed the work.", "Added an exportable project summary so a learner leaves with an artifact, not only a progress percentage."),
    results=paras("The deliverable is a complete interactive concept covering the journey from intent to iteration. Visitors can validate a playlist URL, choose a goal and weekly time budget, open source videos, take notes, complete tasks, submit a draft, and download a project summary. The default sample starts at two completed tasks so the value is visible immediately.", "No adoption, retention, completion lift, or learning outcomes have been measured. All learner data is fictional. The prototype demonstrates interaction design and product judgment, not a production AI system."),
    iterations=paras("Chose a project-first plan over a summary-first interface. The primary action after a lesson is practice; watching has its own status. This keeps the concept focused on transfer of learning rather than content consumption.", "Chose external creator links over a fake video player or an unverified transcript. Original learning prompts are clearly separated from the source. Chose a transparent feedback checklist over an invented grade."),
    milestones=bullets("Discovery: interview self-directed learners about the last tutorial they abandoned and observe where they switch between YouTube, notes, and project tools.", "Usability: test whether five participants can import the sample, find the next task, and submit a draft without help. Track successful attempts and time to first practice action.", "Learning experiment: compare a source-only playlist with the same playlist plus Relay tasks. Use a blind project rubric and a delayed transfer task. Track completion, return to practice, and demonstrated skill rather than minutes watched.", "Production: add authorized YouTube metadata retrieval, transcript availability handling, source-linked plan generation, editable task sequencing, and consent-based project evaluation. Assess privacy, creator attribution, and evaluation confidence before launch."),
    differently=paras("Validate the exercise sequence with a learning designer and real beginners before adding more subjects. A polished plan can still be the wrong plan. I would also let learners adjust tasks after their first practice attempt so the path responds to what they can actually do."),
    artifacts=paras('<a class="button" href="/demos/relay/index.html">Explore the interactive prototype ↗</a>') + links(("Source and setup instructions", "https://github.com/chaekim96/chaekim-portfolio")) + paras("Demo boundaries: no accounts, no uploads, no API keys, no YouTube import, and no AI assessment. Notes and draft URLs remain in the visitor’s browser. Reset restores the fictional sample. Independent of YouTube, NotebookLM, and Google."),
  ),
  dict(slug="ai-visibility-checker", title="AI Visibility Checker",
    kicker="product · solo build · 2026",
    heading="Knowing whether AI assistants can find, read and cite your site.",
    desc="A free checker that reads a page the way a crawler does and reports whether search engines and AI assistants can find, read and cite it.",
    tldr="Paste a URL. A server fetches the page the way a crawler that doesn't run JavaScript would, then runs seventeen scored checks in three groups: can AI find it, read it, and understand and cite it. It gives a score, the three fixes worth the most, and which of eleven crawlers robots.txt lets in.",
    role="Product owner and builder", team="With Chris Jackson, my Lucent co-founder; built with Claude Code", timeline="October 2026",
    cover=cover("/assets/img/builds/ai-visibility-checker-2.jpg", "The checker report for chaekim.vercel.app, ready for AI answers, with the fixes worth the most listed first", 1600, 1000),
    problem=paras("An AI assistant can only cite a page it can fetch and read. Those basics are invisible from the outside: you can't tell by looking whether robots.txt blocks ChatGPT's crawler, or whether a page's words only appear after JavaScript runs. I'm researching the GEO space, and this is where it starts."),
    did=bullets(
      "Read each page from its raw HTML, the way a crawler that doesn't run JavaScript sees it.",
      "Checked robots.txt for eleven crawlers, separating search and live fetching, where blocking hurts visibility, from model training, where blocking is a choice. Matching follows the robots.txt standard.",
      "Turned six checks from the SEO audit playbook Chris Jackson and I built at Lucent into automatic ones: HTTPS and redirects, redirect chains, the mobile viewport, image alt text, heading order, and mixed content.",
      "Turned seventeen checks into a score in three groups, with a \"fix first\" list ranked by the points each fix is worth.",
      "Reported a partial check when a site refuses unknown bots, instead of scoring it zero.",
      "Made it safe to run in public: only public addresses on every redirect, a 2 MB cap, and an 8-second timeout.",
      "Shipped it with no dependencies and eleven tests, and made it pass its own check.",
    ),
    results=stat_grid(("17", "scored checks in three groups"), ("11", "crawlers read from robots.txt"), ("0", "dependencies"), ("100", "its own score")) + "\n" + paras("Its first run on my own portfolio found two real gaps: no llms.txt, and a short address that names the longer one as its main URL."),
    differently=paras("Test on sites I don't control, early. My first version scored sites that refuse unknown bots as zero, which made a major news site look invisible when it had only refused my checker. Running it on real sites before launch caught that."),
    artifacts=links(("Try the checker", "https://chaekim-ai-visibility.vercel.app"), ("Source on GitHub", "https://github.com/chaekim96/ai-visibility-checker")) + "\n" + artifact_grid(("/assets/img/cases/avc-crawlers-2.jpg", "Which crawlers robots.txt lets in, split into search and live fetching versus model training.")),
  ),
  dict(slug="tally", title="Tally",
    kicker="product · solo build · 2026",
    heading="Knowing how long your to-do list will actually take.",
    desc="A note-taker where every line gets a Claude time estimate, totaled in a ledger so a to-do list becomes an honest picture of the day.",
    tldr="Tally turns a to-do list into a plan. You write lines like a normal note. Claude reads the whole note and gives each line a most-likely time, a range, and a category. The ledger adds it up, and the Day view lets you drag items onto a calendar.",
    role="Product owner and builder", team="Solo, built with Claude Code", timeline="September to October 2026",
    cover=cover("/assets/img/builds/tally.jpg", "Tally estimating a week of to-dos: an hour for the case memo, 30 minutes for bug reports, 3h45 in all"),
    problem=paras("A to-do list says what to do, not how long it will take, so a day can be overbooked before it starts. I liked Timely, a note-taker that sizes each line, and wanted my own version: a different design, with the estimates in a column on the right."),
    did=bullets(
      "Rebuilt the idea from scratch in React, with an estimate column beside every line.",
      "Sent each line to Claude with the whole note as context. It returns the most likely minutes, an 80% range, a confidence level, and one of seven categories.",
      "Built the Ledger: remaining vs. done, a finish-by time, a capacity meter, where the time goes, quick wins under 15 minutes, and deep-work blocks over 90.",
      "Added a Day view. Drag items from an Unscheduled tray onto the calendar, resize a block to change how long it takes, or do all of it from the keyboard.",
      "Kept the user in charge. Click any estimate to override it, write \"(1h)\" in a line and it's honored exactly, and ⌘B splits a big line into 3 to 7 estimated sub-tasks.",
      "Made it work with no key at all. Estimates fall back to a keyword heuristic, marked with ~. A visitor's own key always pays for their use, and the server key needs an access code.",
    ),
    results=stat_grid(("7", "categories per estimate"), ("80%", "range around every estimate"), ("3–7", "sub-tasks per breakdown"), ("0", "accounts needed")) + "\n" + paras("Notes live in the browser. Requests are capped at 50 lines and 64 KB per call, so a runaway loop can't run up a bill."),
    differently=paras("Test against the deployed runtime, not just the dev server. Vite and the type checker accepted imports that Node rejected once deployed, so I added a check that loads every function the way Vercel does. Next on the roadmap: an agent that does the task, not just sizes it."),
    artifacts=links(("Try Tally", "https://tally-lake-seven.vercel.app"), ("Source on GitHub", "https://github.com/chaekim96/tally")) + "\n" + artifact_grid(("/assets/img/cases/tally-day.jpg", "The Day view: a capacity meter, the Unscheduled tray, and blocks on the calendar."), ("/assets/img/cases/tally-summary.jpg", "The Summary: what's left, the finish-by time, and where the time goes.")),
  ),
  dict(slug="palette-generator", title="Palette Generator",
    kicker="product · solo build · 2026",
    heading="Brand colors and fonts for founders who aren't designers.",
    desc="A palette and font-pairing generator that takes a non-designer from a one-line description to a brand look they can ship.",
    tldr="Describe what you're building and pick a mood. You get five colors with a job for each, a font pairing, and a sample website painted in them. Contrast is checked against WCAG, and the whole result lives in a share link.",
    role="Product owner and builder", team="Solo, built with Claude Code", timeline="September to October 2026",
    cover=cover("/assets/img/builds/palette.jpg", "Palette Generator turning 'coffee subscription, warm and earthy' into five roles of color and a font pairing"),
    problem=paras("Founders need a brand look long before they can hire a designer. Most palette tools hand you five pretty colors and stop there. Which one is the button? Which is the text? Can anyone read it?"),
    did=bullets(
      "Started from a Figma Make export and set one rule for every feature: does it get a non-designer to a shippable palette faster? If not, it waits.",
      "Generated palettes in OKLCH across seven moods, and tuned the Earthy and Romantic moods against a benchmark of 97 real palettes.",
      "Gave every color a job (text, primary, supporting, accent, background) and matched it with one of 25 curated Google Fonts pairings.",
      "Painted a sample startup homepage in the palette, and checked every color pairing for WCAG contrast, with the smallest fix suggested when one fails.",
      "Built Explore: a weekly scan of 115 startup homepages showing which moods and brand colors are common right now. Curated public sites only, robots.txt respected.",
      "Kept it serverless. The palette, fonts, and mood live in the URL, so sharing is copying a link. Export goes to CSS variables, Tailwind, or a PNG.",
    ),
    results=stat_grid(("7", "moods"), ("25", "curated font pairings"), ("115", "startup homepages scanned weekly"), ("0", "sign-ups")) + "\n" + paras("The coffee subscription palette above passes WCAG AA on all seven of its color pairings."),
    differently=paras("Build the benchmark before the generator. I tuned the moods against real palettes only after the first version worked. Starting with the benchmark would have set the target on day one."),
    artifacts=links(("Try Palette Generator", "https://color-palette-generator-three-sand.vercel.app"), ("Source on GitHub", "https://github.com/chaekim96/ColorPaletteGenerator")) + "\n" + artifact_grid(("/assets/img/cases/palette-preview.jpg", "Website preview: the palette painted onto a sample startup homepage, with the contrast check above it."), ("/assets/img/cases/palette-explore.jpg", "Explore: moods and brand colors across 115 startup homepages, refreshed weekly.")),
  ),
  dict(slug="typerace", title="TypeRace",
    kicker="product · solo build · 2026",
    heading="Settling who types fastest, with one link and no sign-up.",
    desc="A live browser typing race for classmates: share a four-letter code, type the same short story, first to finish wins.",
    tldr="Start a room and share the link. Everyone types the same short story at once, with live progress bars, WPM, and accuracy, then a results chart and a weekly class leaderboard. No accounts, no ads.",
    role="Product owner and builder", team="Solo, built with Claude Code", timeline="October 2026",
    cover=cover("/assets/img/builds/typerace-2.jpg", "A TypeRace race in progress at 70 WPM, ink on near-white, the progress bar halfway across"),
    problem=paras("Typing races are a fun way to compete with friends. I wanted one a class could join from one link in a few seconds, on a laptop or a phone, with no accounts and no ads."),
    did=bullets(
      "Wrote a PRD first, then built to it: rooms by four-letter code, a synced countdown, live progress, results, and rejoining after a refresh.",
      "Ran each room as one Cloudflare Durable Object, so a race needs no database. Progress updates are under 30 bytes, about ten a second.",
      "Checked typing in the browser with zero network delay. One input path handles desktop keyboards, phone keyboards, autocorrect, and smart quotes.",
      "Made the start fair. Each browser syncs its clock with the server and counts down to the same instant, on timers rather than animation frames, so background tabs still hear GO.",
      "Added anti-cheat (big jumps or a finish above 250 WPM count as did-not-finish) and a weekly top-10 leaderboard that resets Monday at midnight Pacific.",
      "Wrote a 3-bot simulation that runs a full race end to end, in unranked rooms so test bots stay off the real board.",
    ),
    results=stat_grid(("10", "players per room"), ("20", "original stories"), ("<30 B", "per progress update"), ("11.5 KB", "client code, gzipped")),
    differently=paras("Keep test traffic out of production by design. Right after one deploy, my simulation put two bots on the live leaderboard because the old server was still answering. I removed them and made the simulation wait for the new version, but that guard should have come first."),
    artifacts=links(("Play TypeRace", "https://typerace.typerace.workers.dev")) + "\n" + artifact_grid(("/assets/img/cases/typerace-results-2.jpg", "Results from a test race on my own server: finishing order, WPM, accuracy, and a WPM chart.")),
  ),
  dict(slug="networking-tracker", title="Networking Tracker",
    kicker="product · solo build · 2026",
    heading="Keeping track of every coffee chat, without sharing a thing.",
    desc="A private contact tracker where Postgres row-level security keeps each person's data their own.",
    tldr="Sign in and keep a list of the people you meet: company, role, where you met, notes, and priority. Sort, filter, and search it. Every row is private to the person who wrote it, and the database enforces that, not just the app.",
    role="Builder", team="Solo", timeline="September 2026",
    cover=cover("/assets/img/builds/networking-tracker.jpg", "Networking Tracker filtered to high-priority contacts, with demo data"),
    problem=paras("At Berkeley you meet a lot of people quickly, and notes on them end up scattered. A tool for that has to answer one question before any other: can anyone else see my contacts?"),
    did=bullets(
      "Built sign-up, sign-in, and a contact list with create, edit, delete, sort, filter, and search, in Next.js on Vercel.",
      "Stored contacts in Neon Postgres and isolated them with row-level security in the database, so even a direct call to the public Data API can't read someone else's rows.",
      "Proved it. Queried as the role the API uses while two rows existed, and got zero back.",
      "Validated input three times: in the form, on the server, and with a database constraint. The friendly message is a courtesy, not the defense.",
      "Designed all four list states: loading skeletons, two distinct empty states, a plain-language error with one-click retry, and success.",
      "Captured every screenshot in the write-up from the deployed app, not localhost.",
    ),
    results=stat_grid(("0", "rows visible to the wrong user"), ("3", "layers of input validation"), ("4", "list states designed"), ("15", "screenshots from the live app")),
    differently=paras("Check the security boundary on every push. The isolation test needs two real accounts and a live database, so today it runs on demand. Next: run it in CI against a throwaway database branch that seeds its own accounts."),
    artifacts=links(("Try it", "https://networking-tracker-five-sage.vercel.app"), ("Source on GitHub", "https://github.com/chaekim96/networking-tracker")) + "\n" + artifact_grid(("/assets/img/cases/nt-invalid.jpg", "An empty name, rejected with the reason in plain language. Demo data."), ("/assets/img/cases/nt-mobile.jpg", "The contact list on a phone. Demo data.")),
  ),
  dict(slug="web-anatomy", title="Anatomy of a Website",
    kicker="product · illustrated encyclopedia · 2026",
    heading="Showing how a website works, from the DNS lookup to the AI answer.",
    desc="An illustrated, growing encyclopedia of how a website works, built on one idea: SEO and GEO start with the website.",
    tldr="An animated journey of one page load, a stack of the layers behind it, an example <head> linked line by line to a search result, a social card and an AI answer, and a searchable encyclopedia of 64 terms. A separate page explains the same ideas as a restaurant.",
    role="Builder", team="Solo, built with Claude Code", timeline="October 2026",
    cover=cover("/assets/img/builds/web-anatomy.jpg", "The Anatomy of a Website home page: the title, the line SEO and GEO start with the website, and the start of the journey of a request"),
    problem=paras("SEO and GEO advice usually starts with keywords or prompts. I think it starts earlier, with the website itself: if the foundation is weak, no keyword strategy or AI optimization can fix it. I wanted one place that shows the whole foundation, in plain English, with real code beside each idea."),
    did=bullets(
      "Drew the journey of a request as an animated SVG: browser, DNS, TLS, the CDN edge, the origin and the database, and back, plus the crawlers that make the same trip.",
      "Laid out the layers of a website (network, hosting, backend, HTML, CSS, JS, assets, SEO/GEO, quality, workflow), split into what visitors see and what only machines read.",
      "Built \"One head, three audiences\": an example <head> where each line links to the search result, the social card, or the AI answer it produces.",
      "Wrote a searchable, filterable encyclopedia of 64 terms. Each has a plain-English definition, how it works, a real snippet, and related terms, and every entry can be deep-linked, like #canonical.",
      "Added a simple version for newcomers: the website as a restaurant, what happens when you visit, how Google and AI find you, and a history of the web from 1969 to AI search, with 46 checked source links.",
      "Kept it static. All content lives in one data file, and a small script turns it into a page for every term, each labeled for search and AI answers, plus an A to Z index.",
    ),
    results=stat_grid(("64", "encyclopedia terms"), ("10", "layers of a website"), ("46", "checked source links in the history"), ("67", "pages in the sitemap")),
    artifacts=links(("Visit Anatomy of a Website", "https://webanatomy.vercel.app"), ("The simple version", "https://webanatomy.vercel.app/basics"), ("Source on GitHub", "https://github.com/chaekim96/web-anatomy")),
  ),
  dict(slug="voiceprompter", title="VoicePrompter",
    kicker="product · macOS app · 2026",
    heading="Reading your notes on a call without anyone seeing them.",
    desc="A macOS teleprompter that follows your voice as you read, with capture protection tested against specific macOS recording APIs.",
    tldr="Your script floats above other apps. As you speak, it highlights the word you're on and scrolls to keep your line near the top. The capture test hides its content from ScreenCaptureKit on the tested Mac; older recording paths can still show it, and individual sharing apps need a manual check.",
    role="Builder", team="Solo, built with Claude Code", timeline="September to October 2026",
    cover=cover("/assets/img/builds/voiceprompter.jpg", "VoicePrompter listening at word 108 of 139, with the prompter highlighting the spoken word", 800, 600),
    problem=paras("I was practicing presenting and interviewing and wanted my notes on screen, without cluttering the screen I was sharing. The teleprompters I found either fell short or wanted me to pay."),
    requirements=bullets(
      "Keep the script readable above other apps, with controls to pause, hide, reposition, and resize it.",
      "Follow spoken words despite small skips, ad-libs, and recognition errors, without jumping on weak matches.",
      "Support on-device speech recognition, explain microphone and speech permissions, and make capture-protection limits visible.",
      "Keep the first version to one script at a time. Configurable hotkeys and additional speech engines remain outside the current build.",
    ),
    did=bullets(
      "Built a native Swift app: an overlay that floats on every Space, and a main window with every setting in a sidebar.",
      "Transcribed speech on the device with Apple's recognizer, restarting the session about every 50 seconds so results stay short and fast.",
      "Wrote the alignment. Each update matches the last 8 spoken words against the script, with fuzzy matching for misheard words and guards so it never jumps on weak evidence.",
      "Tested capture protection on macOS 15.7.4. ScreenCaptureKit and tested still-image APIs hide the content; legacy video paths can show it. The window name can still appear in a sharing picker.",
      "Added global hotkeys that need no Accessibility permission, double-click to jump to a word, and click-through so clicks reach the app underneath.",
    ),
    results=stat_grid(("~0.3 ms", "alignment update on an 8,800-word script"), ("8", "spoken words matched each update"), ("2", "permissions: mic and speech"), ("3", "capture-harness runs reproduced")),
    milestones=bullets(
      "<b>Built:</b> a floating script, voice tracking, a settings sidebar, and global controls.",
      "<b>Tested:</b> capture APIs on macOS 15.7.4, including a control panel to confirm that each recording actually captured the display.",
      "<b>Still to verify:</b> interactive sharing in Zoom, Meet, QuickTime, and OBS, plus a full uninterrupted latency run. These are checks to complete, not shipped guarantees.",
    ),
    iterations=bullets(
      "<b>Keeping up with speech:</b> restart recognition about every 50 seconds and carry alignment context across sessions.",
      "<b>Avoiding false jumps:</b> use fuzzy matching, a local search window, and stronger confirmation for larger moves.",
      "<b>Learning the protection boundary:</b> the API tests showed why a hide hotkey is still necessary, even when the normal capture path hides the overlay.",
    ) + "\n" + links(("Requirements and limitations", "https://github.com/chaekim96/VoicePrompter/blob/main/README.md"), ("Capture-test evidence", "https://github.com/chaekim96/VoicePrompter/blob/main/ProtectionTest/RESULTS.md")),
    differently=paras("Measure latency from the start. The speech recognizer dominates the delay, and I built the latency test only after the app worked. A full, uninterrupted latency run is still on my list."),
    artifacts=links(("Source on GitHub", "https://github.com/chaekim96/VoicePrompter"), ("Essay: What\u2019s the Point of Preinstalled Apps?", "/projects/preinstalled-apps")) + "\n" + artifact_grid(("/assets/img/cases/vp-main.jpg", "The main window while listening: status, position in the script, and prompter settings."), ("/assets/img/cases/vp-prompter.jpg", "The prompter further in. Read text dims and the current word turns gold. Captured with protection off.")),
  ),
  dict(slug="parallel-prospect-brief", title="Parallel Prospect Brief",
    kicker="product · solo build · 2026",
    heading="Walking into a first sales call with every claim sourced.",
    desc="A command-line tool that turns a company name into a cited one-page sales brief, built on Parallel's Task API.",
    tldr="Type a company name. The CLI sends one Task API request with a 13-field schema and waits for a structured answer: what the company builds, how far it has gone with AI agents, which Parallel API fits, a first-call pitch, why now, who to talk to, discovery questions, and likely objections. It saves a markdown brief with numbered sources and a confidence level on each field.",
    role="Product owner and builder", team="Solo, built with Claude Code", timeline="October 2026",
    cover=cover("/assets/img/builds/parallel-prospect-brief.jpg", "An illustrative brief for an invented company, Example Co: what they do, products, agent signal, and best-fit API, with sources and confidence", 1600, 1000),
    problem=paras("Before a first sales call, a rep needs to know what the prospect does, whether they need the product, and what to say. That research is spread across many tabs, and the notes rarely say where each claim came from. Parallel sells web research APIs for AI agents, so I built the prep tool on its own Task API."),
    did=bullets(
      "Wrote the brief as a Task API output schema: 13 fields, with fixed choices for the agent signal and the best-fit API so briefs compare cleanly.",
      "Passed in what Parallel sells, its six APIs with prices, checked against parallel.ai on October 22, so the research agent can match a prospect's need to a specific API.",
      "Showed each field with numbered sources and the API's confidence rating, sharing one source list across the brief.",
      "Explained failures in plain language: a rejected key, an account out of credits, or a request Parallel didn't accept.",
      "Added a dry run that prints the exact request without calling the API, so it can be checked for free.",
      "Wrote six offline tests against an invented company, so they cost nothing and need no key.",
    ),
    results=stat_grid(("13", "fields per brief, each cited"), ("6", "Parallel APIs it can recommend"), ("~$0.025", "per brief on the core processor"), ("6", "offline tests")) + "\n" + paras("It hasn't run against the live API yet; that needs a Parallel account and key. The sample below is invented to show the format, and says so."),
    differently=paras("Get an API key on day one. I built and tested everything offline, so the first live run is still ahead, and that run is the real test of the schema."),
    artifacts=links(("Source on GitHub", "https://github.com/chaekim96/parallel-prospect-brief"), ("Sample brief", "https://github.com/chaekim96/parallel-prospect-brief/blob/main/examples/sample-brief.md")) + "\n" + artifact_grid(("/assets/img/cases/ppb-sample.jpg", "The full illustrative sample. Every fact is invented to show the format.")),
  ),
  dict(slug="product-blueprint", title="Product Blueprint",
    kicker="method · solo build · 2026",
    heading="One way to build every product, with a test at each step.",
    desc="My personal prompt library and playbook for building products with AI tools: a six-stage loop with a pass/fail gate at each stage, a design system, a product template, and a database of 22 versioned prompts with evals.",
    tldr="I build fast with Lovable, Google AI Studio and Claude, and my prompts and design choices lived in chat history. The blueprint writes the method down: six stages from Discover to Ship, each ending with a pass/fail gate, a design system pulled from my own products, a template to fill in per product, and 22 prompts that each carry their own evals. Two scripts check the prompt database and score AI features against a locked test set.",
    role="Product owner and builder", team="Solo, built with Claude Code", timeline="October 2026",
    cover=cover("/assets/img/builds/product-blueprint.jpg", "The build loop: six stages from Discover to Ship, each with the gate it has to pass", 1600, 1000),
    problem=paras("AI builders make the first draft easy. Keeping products consistent is harder. My prompts lived in old chats, each product picked its own colors, and I judged AI output by feel. When a prompt worked, I couldn't find it again or tell whether a change made it better."),
    did=bullets(
      "Wrote a six-stage build loop, Discover to Ship. Each stage ends with a short pass/fail gate, so problems get fixed where they start.",
      "Pulled a design system from two of my products: a dark technical theme from FaFo and a warm paper theme from Timely, with shared rules for layout, type, motion and copy voice, and an 8-point design rubric.",
      "Built a product template that walks one product through every stage and records each gate result.",
      "Wrote 22 prompts across the six stages, from problem framing to launch posts. Each has a version, its inputs, pass/fail evals and a changelog.",
      "Set pass targets by risk (85%, 90% or 98%) and a test-set format that always includes empty input, long input, other languages and prompt-injection attempts.",
      "Wrote a checker that fails if a prompt is missing evals, a version or an input. On its first run it caught a gap in one of my own prompts.",
      "Filled in the template for Timely as a worked example, with a 25-case test set for its time estimator.",
    ),
    results=stat_grid(("6", "stages, each with a gate"), ("22", "versioned prompts with evals"), ("25", "test cases for Timely's estimator"), ("3", "launch blockers found in Timely")) + "\n" + paras("Filling in the template for Timely found three things to fix before launch: the Gemini key is readable in the browser, user text goes into the prompt unprotected, and the page title doesn't match the product name. Every prompt is still marked draft. One moves to tested only after it passes its evals on three real uses."),
    differently=paras("Start from one real product, not the whole method. Filling in the template for Timely taught me more than writing it did, and it found the launch blockers. I'd fill it in for the next product first and write each stage as I reach it."),
    artifacts=paras("The repo is private. Below, one prompt from the database, as it appears in the repo.") + "\n" + artifact_grid(("/assets/img/cases/pb-prompt.jpg", "The copy review prompt: when to use it, the prompt, and the evals its output has to pass.")),
  ),
]

COURSEWORK = [
  dict(slug="spotify-review-triage", title="Spotify Review Triage",
    kicker="ai/ml coursework · final project · 2026",
    heading="Turning a flood of app reviews into one clear product priority.",
    desc="A multi-agent LLM pipeline that labels Spotify app reviews, checks its own work, and recommends where next quarter's product effort should go.",
    tldr="660,622 Spotify reviews in, one recommendation out. A small model labels a declared 100,000-review sample under a $10 cap, a different model checks a blind sample, and a public dashboard traces the ranking down to single reviews. The answer: usability.",
    role="Builder", team="Solo, built with Claude Code", timeline="October 2026",
    cover=cover("/assets/img/builds/spotify-review-triage.jpg", "The live dashboard: 660,622 reviews in file, 100,000 in scope, $4.36 measured spend, and the recommendation: usability", 1600, 1000),
    problem=paras("Nobody can read 660,000 reviews. A model can label them, but its answer is only useful if it is affordable, checked, and every number traces back to a real review."),
    requirements=bullets(
      "Answer one product question: should next quarter's effort go to access, usability, playback, or billing and support?",
      "Account for every input review, declare the classification scope, and keep the run within a $10 API budget.",
      "Trace recommendations to claims and individual reviews, validate model outputs, and resume interrupted work without re-labeling completed records.",
      "Show sample coverage, human-label agreement, and unresolved failures alongside the dashboard's recommendation.",
    ),
    did=bullets(
      "Accounted for all 660,622 reviews in code before any model saw them, matching the course's own checksum.",
      "Labeled a declared 100,000-review sample with a small, cheap model, 50 reviews per request, with a cache so each distinct text is labeled once.",
      "Had a different model check a blind 1% sample, and tested that checker with 20 planted wrong labels and 5 prompt-injection reviews.",
      "Hand-labeled 50 reviews myself and compared them to the model, field by field.",
      "Grouped complaints into issues, ranked four business areas by severity, and wrote a memo where every number cites a claim and a review.",
      "Shipped a public dashboard backed by a database and an API, so anyone can follow the ranking down to a single review.",
    ),
    results=stat_grid(("$4.36", "API spend within the declared 100,000-review scope"), ("20 / 20", "planted wrong labels caught"), ("5 / 5", "prompt injections resisted"), ("35.5%", "of sample complaint severity is usability")) + "\n" + paras("All 660,622 input reviews were accounted for. Within the declared 100,000-review scope, 99,936 were validly classified and 64 were quarantined. The recommendation applies to that sample: prioritize usability, ahead of billing and support at 19.1%."),
    milestones=bullets(
      "<b>Completed:</b> full input accounting, a declared sample, a cold/warm cost pilot, and an interrupt-and-resume demonstration.",
      "<b>Completed:</b> a blind model verification sample, 50 human labels, reproducible ranking, and a dashboard backed by an API and database.",
      "<b>Next, not completed:</b> more human labels and a run over every nonempty review. The $25 to $48 full-run cost is an estimate, not measured spend.",
    ),
    iterations=bullets(
      "<b>Grouping:</b> long literal phrases left about 56% of complaints in catch-all issues. Short stems, spelling variants, and word-start matching reduced that share to 45.1%.",
      "<b>Recovery:</b> re-queue transport failures separately from invalid labels, then resume with a shared rate limiter. The resumed run recorded no transport failures.",
      "<b>Caching:</b> make the memo's evidence pack deterministic so the warm 100-review pilot reuses all results, makes zero model calls, and costs $0.00.",
    ) + "\n" + links(("Decision log", "https://github.com/chaekim96/spotify-review-triage/blob/main/DECISIONS.md"), ("Human evaluation", "https://github.com/chaekim96/spotify-review-triage/blob/main/evals/golden/golden_eval.md"), ("Resume demonstration", "https://github.com/chaekim96/spotify-review-triage/releases/tag/resume-demo-2026-10-20")),
    differently=paras("Get more human labels in early. Only 50 labels are mine, and the model matched me on topic 42% of the time, so the answer leans on the model and its checker. A larger run would increase coverage; it would not by itself resolve the labeling uncertainty."),
    artifacts=links(("Open the dashboard", "https://spotify-review-triage.vercel.app"), ("Source and evidence on GitHub", "https://github.com/chaekim96/spotify-review-triage")) + "\n" + artifact_grid(("/assets/img/cases/spotify-alternatives.jpg", "The memo weighs every alternative: billing and support, playback, and access, each with its evidence and review links.")),
  ),
  dict(slug="personal-wiki", title="Personal Wiki",
    kicker="ai/ml coursework · mba 290t · 2026",
    heading="Asking my own notes questions, with no internet.",
    desc="A command-line study wiki that runs fully offline: a local Gemma model turns sources into linked Obsidian notes and answers questions with citations.",
    tldr="A study wiki for my AI course that never touches the cloud. Local Gemma, through Ollama, turns sources into linked Obsidian notes. An ask command answers from those notes with citations, or says the evidence isn't there.",
    role="Builder", team="Solo", timeline="September 2026",
    cover=cover("/assets/img/builds/personal-wiki.jpg", "Obsidian graph of the wiki's linked notes", 900, 646),
    problem=paras("Cloud assistants answer confidently from anywhere. For studying I wanted the opposite: answers only from my own sources, a citation for every claim, on a laptop with Wi-Fi off."),
    requirements=bullets(
      "Ingest my course sources into linked Obsidian notes and answer study questions from those sources with citations.",
      "Run entirely on the laptop after setup, with no cloud calls or hosted embeddings, within the machine's available memory.",
      "Keep ask, chat, and search behavior separate; unsupported questions should return insufficient evidence.",
      "Preserve hand-edited notes and source links when ingesting the same material again.",
    ),
    did=bullets(
      "Picked the model to fit the machine. Gemma 4 E2B at 4-bit, because the larger versions didn't fit in the 5 to 6 GB free on an 18 GB Mac.",
      "Wrote the CLI and harness with only Python's standard library: ingest, search, ask, and chat modes.",
      "Built hybrid retrieval: my own BM25 plus local embeddings, merged with reciprocal rank fusion.",
      "Wrote the expected answers for four tests before running them, including one the wiki should refuse.",
      "Checked ask-mode citations against the retrieved passages in code and flagged invalid answers. Chat has a separate citation check with one retry.",
      "Recorded an offline demo with Wi-Fi off. All four tests matched the online results.",
    ),
    results=stat_grid(("3 of 4", "tests passed, written in advance"), ("4.4 s", "per answer, warm"), ("~1.7 GB", "working memory"), ("0", "cloud calls")) + "\n" + paras("The failure is documented. A question in my own shorthand (\"A3\") missed the right passage, and the model answered a nearby question with a real citation."),
    milestones=bullets(
      "<b>Built:</b> local ingestion, linked notes, hybrid search, cited answers, and a separate study-partner chat mode.",
      "<b>Evaluated:</b> four prewritten ask tests, mode-separation checks, memory and response-time measurements, and an offline demonstration. Three of four ask tests passed.",
      "<b>Proposed, not implemented:</b> expand aliases such as A3, reserve retrieval space across sources, and add an answer-relevance check. Re-run the original tests and retain the baseline for comparison.",
    ),
    iterations=bullets(
      "<b>Keyword search to hybrid retrieval:</b> adding local embeddings moved the paraphrase test's relevant passages from ranks 5 and 4 to ranks 2 and 3.",
      "<b>Reliable ingestion:</b> save a plan for each source and detect hand edits, so repeated ingestion reuses note names and keeps edited notes.",
      "<b>Citations to relevance:</b> the A3 test exposed a real citation attached to the wrong answer. The next experiment must check whether the evidence answers the actual question, as well as whether the citation exists.",
    ) + "\n" + links(("Retrieval changes", "https://github.com/chaekim96/personal-wiki/blob/main/evidence/retrieval_changes.md"), ("Test results", "https://github.com/chaekim96/personal-wiki/blob/main/evidence/ask_tests/results.md"), ("Limitations and proposed improvements", "https://github.com/chaekim96/personal-wiki/blob/main/README.md#10-limitation-and-improvement")),
    differently=paras("Write more questions in my own shorthand before tuning retrieval. A citation check proves a citation exists, not that it answers the question; the failed A3 test made that distinction concrete."),
    artifacts=links(("Source and evidence on GitHub", "https://github.com/chaekim96/personal-wiki")) + "\n" + artifact_grid(("/assets/img/cases/wiki-note.jpg", "A generated note in Obsidian, with its sources linked back to the raw files."), ("/assets/img/cases/wiki-index.jpg", "The wiki's index: concepts and projects, each with a one-line summary.")),
  ),
  dict(slug="pacman-dqn", title="Pac-Man DQN",
    kicker="ai/ml coursework · 2026",
    heading="Teaching an agent to play Ms. Pac-Man by trial and error.",
    desc="A Deep Q-Network trained on Atari Ms. Pac-Man, with every number reported straight from the run's own output files.",
    tldr="An agent that sees only pixels and points learned Ms. Pac-Man over 100 games. Its mean score across five fixed test games rose from 492 to 680. I chose three settings, ran it once end to end, and reported what happened, including where it got worse.",
    role="Builder", team="Solo", timeline="September 2026",
    cover='<img src="/assets/img/builds/pacman-dqn.gif" alt="The trained agent playing Ms. Pac-Man" width="160" height="210">', cover_class="case-cover--pixel",
    problem=paras("Reinforcement learning is easy to describe and hard to trust. The question wasn't only whether the score goes up, but whether the gain is real or noise."),
    did=bullets(
      "Chose three settings and justified each: 100 episodes, exploration held at 0.20 as a control, and a learning rate 2.5x the reference so change would show up in a short run.",
      "Wrote down my expectation before running: a modest gain of about 100 to 200 points.",
      "Trained on a laptop GPU: 57,801 decisions and 14,201 updates in about 3.3 minutes.",
      "Evaluated before and after on the same five seeds, and kept every GIF, plot, and checkpoint.",
      "Explained the surprise. Loss went up while scores improved, which is expected in DQN as the value targets grow.",
    ),
    results=stat_grid(("492 → 680", "mean evaluation score"), ("+188", "inside my predicted range"), ("4 of 5", "test games improved"), ("3.3 min", "to train")),
    differently=paras("Five test games is too few to trust the mean. One game fell from 800 to 300, and the curve was flat for 80 episodes before a late jump. Next experiment: change only the episodes, from 100 to 500, to see whether the gain holds or was a lucky streak."),
    artifacts=links(("Notebook and evidence on GitHub", "https://github.com/chaekim96/pacman-dqn")) + "\n" + artifact_grid(("/assets/img/cases/pacman-untrained.gif", "Before training: the agent mostly circles one corner of the maze."), ("/assets/img/cases/pacman-trained.gif", "After training: the best game from the final evaluation."), ("/assets/img/cases/pacman-training.jpg", "The training dashboard: scores, update loss, and exploration per episode.")),
  ),
  dict(slug="custom-llm", title="Custom LLM",
    kicker="ai/ml coursework · mba 290t · 2026",
    heading="Seeing how language models learn by training a tiny one.",
    desc="A tiny nanoGPT model trained from scratch on a laptop CPU, with my own teaching corpus and 48 fixed language tests.",
    tldr="A word-level language model with 2 blocks and 4 heads, trained in about 14 seconds on a laptop. I ran it twice, on the starter corpus and then with my own files on grammar, opposites, and spatial relations, and scored both on the same 48 tests.",
    role="Builder", team="Solo", timeline="September 2026",
    cover=cover("/assets/img/builds/custom-llm.jpg", "Terminal chat with the tiny model and its odd replies", 768, 474),
    problem=paras("It's hard to build intuition for language models when the ones you use have billions of parameters. A model small enough to train in seconds makes every step visible: tokens, vectors, probabilities, and updates."),
    did=bullets(
      "Predicted each result in writing before every run, then compared.",
      "Wrote 355 new teaching passages on tense and agreement, opposites, and spatial relations, without reading the test items.",
      "Trained two experiments with identical settings: 3,000 steps at a learning rate of 0.001, on a laptop CPU.",
      "Traced one token all the way through: word to ID to vector to probability to gradient to update.",
      "Built a small chat interface and was clear about what it is: a sentence continuer, not a chatbot.",
    ),
    results=stat_grid(("9 → 20", "of 48 tests, starter corpus"), ("7 → 25", "of 48 tests, with my corpus"), ("16/16", "familiar patterns"), ("14 s", "to train")),
    differently=paras("The model learned templates, not language. And because the public tests guided my choices, a good score doesn't prove it generalizes. Next: write my own held-out test set and never look at it while building the corpus."),
    artifacts=links(("Write-up and evidence on GitHub", "https://github.com/chaekim96/custom-llm")),
  ),
]

MODS = [
  dict(slug="smartmodel", title="SmartModel",
    kicker="claude code mod · solo build · 2026",
    heading="Matching each prompt to the right model, so easy work costs less.",
    desc="A Claude Code hook that scores how hard each prompt is and recommends the cheapest model that can handle it.",
    tldr="A model router built into Claude Code. Before Claude acts, a hook scores the prompt's effort from 0 to 100 and recommends Haiku, Sonnet, Opus, or Fable. Ask mode shows a picker, auto routes on its own, and block stops the prompt before any tokens are spent.",
    role="Designer and builder", team="Solo, built with Claude Code", timeline="October 2026",
    cover='<img src="/assets/img/thumbs/smartmodel-wide.jpg" alt="SmartModel\'s picker in Claude Code: rates a prompt medium-effort and recommends Sonnet" width="1600" height="900">',
    problem=paras("Every prompt ran on the most expensive model, renames and git chores included. Switching by hand meant remembering to, and a fresh session meant losing the conversation."),
    did=bullets(
      "Wrote a hook that runs before Claude reads each prompt and scores its effort from 0 to 100 on keywords and structure. Under 20 is Haiku, up to 44 is Sonnet, up to 84 is Opus, and above that is Fable.",
      "Built three modes. Ask shows a picker with the recommendation first. Auto routes silently. Block rejects the prompt before the current model spends a token on it.",
      "Picking a different model hands the whole task to a subagent on that model, with a self-contained brief.",
      "Added inline tags (sm:skip, sm:haiku, sm:opus) and skips for approvals, slash commands, and short acknowledgments like \"thanks\".",
      "Taught it to ignore text the harness injects, like subagent reports and shell output, which kept opening the picker for messages nobody typed.",
      "Logged every decision to a file, so the routing can be audited and tuned.",
    ),
    results=stat_grid(("66", "prompts scored across 18 sessions"), ("15", "flagged as Haiku-sized"), ("44", "flagged as Sonnet-sized"), ("35", "non-prompts correctly skipped")) + "\n" + paras("59 of those 66 prompts arrived in a session running Opus. Each Haiku or Sonnet recommendation was a chance to do the same work for less."),
    differently=paras("Score the work, not the wording. A keyword heuristic reads a short request that mentions git as a chore, even when it means building three pages. Next: let Haiku classify (the hook already supports it when an API key is set) and log which model I actually pick, so the thresholds learn from my overrides."),
    artifacts=links(("Source on GitHub", "https://github.com/chaekim96/smartmodel")) + "\n" + paras("A hook, a small config file, a README, and the decision log. The picker above is a capture of what it shows."),
  ),
  dict(slug="token-fuel", title="Token-Fuel",
    kicker="claude code mod · macOS app · 2026",
    heading="Seeing how much context is left before a session runs out.",
    desc="A menu-bar fuel gauge for Claude Code and Codex sessions, built from the exact token counts each tool already writes to disk.",
    tldr="Running out of context is invisible until answers get worse or the session compacts. Token-Fuel makes it visible: a fuel bar in the menu bar and a floating window, with percent left, turns left, and a 12-turn chart, for Claude Code and Codex.",
    role="Product owner and builder", team="Solo, built with Claude Code", timeline="October 2026",
    cover='<img src="/assets/img/thumbs/token-fuel-wide.jpg" alt="Token-Fuel\'s menu-bar gauge and floating window showing context left for Claude Code and Codex" width="1600" height="900">',
    problem=paras("Context runs out silently. The Claude desktop Code tab ignores the status-line setting, so there was nowhere to put a gauge, and chat apps keep no token counts at all."),
    did=bullets(
      "v0.1: a status-line gauge with a 10-cell fuel bar, turns left, a 12-turn chart, and a \"Refueled\" notice after /compact.",
      "v0.2: a floating pill on the Claude window, because the desktop Code tab ignores status lines.",
      "Fixed the window size. Opus 5 sessions have a 1M window, so assuming 200k made the gauge wrong by 5x.",
      "Tore it all down and ran a feasibility review with one rule: exact sources only. Claude Code and Codex log real token counts, chat apps don't, so chat apps are out.",
      "v1.1: rebuilt as a native Swift menu-bar app with a floating window. Live every 2 seconds, across Claude Code and Codex, launched at login, restarted after a crash.",
    ),
    results=stat_grid(("2", "tools gauged from exact logs"), ("2 sec", "refresh, near 0% CPU"), ("~40MB", "memory"), ("12", "turns charted per session")) + "\n" + paras("Checked against the logs themselves: the numbers match what each tool records."),
    differently=paras("Write the acceptance checks before the build. One rebuild looked done but wasn't. The menu-bar icon hid behind the MacBook notch, the window never updated, and it counted output tokens as context. A checklist drawn from the milestones would have caught all of it on day one."),
    artifacts=links(("Source on GitHub", "https://github.com/chaekim96/token-fuel")) + "\n" + paras("A native Swift app with a README that records every milestone: what changed, why, and the tradeoff.") + "\n" + artifact_grid(("/assets/img/builds/token-fuel.jpg", "Running on my Mac: the menu-bar gauge at 67%, and the floating window for this session.")),
  ),
  dict(slug="code-improver", title="Code Improver",
    kicker="claude code mod · subagent · 2026",
    heading="A second reviewer that reads every file I touch.",
    desc="A custom Claude Code subagent that reviews changed files for readability, performance, and best practices.",
    tldr="A read-only reviewer I can call after any change. It explains each issue, shows the current code, and proposes an improved version, without touching a file itself.",
    role="Builder", team="Solo", timeline="October 2026",
    cover='<img src="/assets/img/thumbs/code-improver-wide.jpg" alt="The code-improver subagent definition file" width="1600" height="900">',
    problem=paras("Code written fast with an AI pair often gets reviewed by nobody. I wanted a second pass that is consistent, quick, and safe to run anywhere."),
    did=bullets(
      "Defined a subagent with one job: scan files for readability, performance, and best-practice issues.",
      "Limited it to read-only tools (Read, Grep, Glob), so it can suggest changes but never make them.",
      "Required the same shape for every finding: the problem, the current code, and an improved version.",
      "Wrote its description so Claude Code knows to reach for it right after code is written or changed.",
    ),
    results=paras("Small by design. Eight lines of configuration change how every review goes, and because it can't edit, I can run it on anything."),
    differently=paras("Give it a severity ranking and permission to say \"no issues.\" Without one, a reviewer always finds something, and small nits crowd out real bugs."),
    artifacts=paras("The file above is the whole thing, verbatim. Below, it reviewing the script that builds this page: 14 findings, ordered by severity, and no files touched.") + "\n" + artifact_grid(("/assets/img/cases/code-improver-review.jpg", "An excerpt of its review of build-cases.py. Its top finding checked out on the live site.")),
  ),
  dict(slug="task-progress", title="task-progress",
    kicker="claude code mod · hooks module · 2026",
    heading="Seeing how far along a task is, right above the prompt.",
    desc="A Claude Code mod that turns Claude's own task checklist into a calm progress band above the prompt, plus a checklist pane.",
    tldr="Claude Code's spinner says something is happening, not how far along it is. task-progress reads the checklist Claude already keeps and draws it as a still band above the prompt: 3/5 · 60%, the step in progress, and a green ✓ all done at the end.",
    role="Product owner and builder", team="Solo, built with Claude Code", timeline="October 2026",
    cover='<img src="/assets/img/thumbs/task-progress-wide.jpg" alt="task-progress in Claude Code: a band above the prompt at 3 of 6 steps, and the /task-progress pane listing each step" width="1600" height="900">',
    problem=paras("On a long task, the flickering spinner looks the same at step 1 as at step 5. To know whether Claude was nearly done or barely started, I had to scroll back through the transcript. I wanted to glance at the screen and know \"3 of 5 done, now running tests.\""),
    did=bullets(
      "Wrote the job first: one glance, no reading, and no extra list for me to keep up to date.",
      "First version: a terminal status line. It worked, but I spend my day in the desktop app's Code tab, which doesn't show status lines. I reverted it instead of shipping something I'd never see.",
      "Rebuilt it as a mod (a hooks module) that follows the app's own task checklist: update_plan and wrap_up in the Code tab, and TodoWrite, TaskCreate and TaskUpdate in the terminal. Claude already keeps that list, so the bar can't drift from it.",
      "Kept it calm on purpose. No animation: it redraws only when the list changes. Cyan while working, green with ✓ all done at the end, and hidden when there's no list.",
      "Added a /task-progress pane that lists every step as done (✓), in progress (▸) or pending (·).",
      "Ignored subagents' task lists, so a helper's checklist never takes over the main bar.",
      "Published it as a public plugin with a one-line install, with tests for the desktop list, the terminal list, and the hidden state.",
    ),
    results=stat_grid(("4/4", "steps filled in a live demo"), ("5", "task-list tools it follows"), ("0", "animation frames"), ("1", "line to install")) + "\n" + paras("I ran a 4-step demo task in the Code tab and watched the band fill one segment per step to 4/4, then turn green with ✓ all done."),
    iterations=paras("<b>v0.2.</b> v0.1 answered \"how far along?\" With that answered, the next questions were \"how long is left, is it stuck, and is the context running out?\" v0.2 answers those, with one rule carried over: no fake numbers and no animation.") + "\n" + bullets(
      "<b>Time left:</b> <code>~40s left</code>, the average of the finished steps times the steps still to go. It appears only after the first step finishes.",
      "<b>Progress inside a step:</b> the step's elapsed time and its tool calls (<code>· 7 actions</code>). A sub-bar appears only where a real count exists, like a step named \"Migrate 3/10 files\" or a test summary like <code>tests 11/12</code>. No guessed percentages.",
      "<b>A clear finish:</b> a pop-up (\"All 5 steps done in 2m 10s\") and a soft 0.4 second two-note chime, once per list. The chime has an off switch.",
      "<b>Stuck warning:</b> the step turns amber when it runs longer than twice the median step time, and never sooner than 3 minutes. The band redraws every 20 seconds only while a step is active, and still never animates.",
      "<b>History in the pane:</b> each step's time and action count, the total, and the last five runs under \"Previous runs\".",
      "<b>Context bar:</b> <code>ctx ███░░ 48%</code> from Claude Code's own context measurement, green, then amber above 60% and red above 80%. On narrow screens the extras drop off first, so the bar, the count and the current step always stay.",
      "<b>Checked before shipping:</b> 17 tests, and a live 4-step demo in the Code tab before it was pushed.",
    ) + "\n" + paras("A working band now reads <code>███████░░░░░░░░ 1/3 · 33% · ~25s left ▸ Run tests · 15s · 7 actions ctx ███░░ 48%</code>, and a finished one <code>███████████████ 3/3 · 100% ✓ all done in 2m 10s</code>."),
    differently=paras("Check where the user actually looks before choosing the surface. I knew I lived in the desktop app and still built for the terminal first. The place I'd most like it is the session sidebar, so progress shows across sessions at once. Mods can't draw there, so that would take a change in the app itself."),
    artifacts=links(("Source on GitHub", "https://github.com/chaekim96/task-progress")) + "\n" + paras("Install from a Claude Code prompt: <code>/plugin install task-progress --marketplace chaekim96/task-progress</code>") + "\n" + artifact_grid(("/assets/img/cases/task-progress-card.png", "Its share card, with the build mark: a progress bar above a checklist.")),
  ),
]

CASES = [
  dict(slug="lucent", title="Lucent",
    kicker="featured · co-founder & CEO · NSF I-Corps",
    heading="Making small businesses visible in AI search.",
    desc="Lucent is an AI search observability platform and consultancy. It shows brands how they rank in ChatGPT, Perplexity, and Gemini, then helps them fix it.",
    tldr="An AI search observability platform and a consultancy. Lucent shows brands how they rank in ChatGPT, Perplexity, and Gemini, then helps them fix it, through the product and hands-on GEO and SEO work.",
    role="Co-founder & CEO", team="Co-founder/CTO + a data science intern", timeline="2025 to 2026",
    cover='<a href="https://trylucent.ai" target="_blank" rel="noopener" aria-label="Open trylucent.ai"><img src="/assets/img/thumbs/lucent-wide.jpg" alt="Lucent homepage: The AI Search Console" width="1600" height="900"></a>',
    problem=paras("Customers now ask AI instead of Google. Small businesses can't see whether AI recommends them, and GEO tools are priced for enterprises."),
    did=bullets(
      "21 NSF I-Corps discovery interviews narrowed the ICP from \"everyone\" to digitally native SMBs and marketing agencies. 100+ interviews across U.S. and APAC SMBs tested willingness to pay.",
      "Positioned around the one-person marketing team: GEO plus SEO execution, not just citation tracking. 5 positioning hypotheses tested across 65 outbound prospects picked the message.",
      "Designed cheap tracking: statistical sampling, and re-running prompts only when models or rankings change.",
      "Led a paid pilot: multi-site SEO and AI visibility audits turned into an engineering action plan.",
      "Built the business case: bottom-up SAM, phased GTM, and a 100+ question diligence bank.",
    ),
    results=stat_grid(("1", "first paying pilot"), ("5", "LOIs in 30 days"), ("+50%", "discovery response rate"), ("NSF", "I-Corps backing")) + "\n" + paras("The advisory work that grew out of the pilot is on pause while we research more in the GEO space."),
    differently=paras("Lock the GTM motion earlier. It was the biggest gap. Positioning tests and pilots should have run in parallel, not in sequence."),
    artifacts="",
  ),
  dict(slug="mobility", title="Mobility devices for older adults (stealth)",
    kicker="in progress · co-founder · stealth",
    heading="Mobility aids people aren't embarrassed to use.",
    badge='<span class="stealth">Stealth</span>',
    desc="Premium, design-forward mobility products that help older adults stay independent longer.",
    tldr="Premium, design-forward mobility products that help older adults stay independent longer.",
    role="Co-founder: GTM, brand, outreach, strategy (my co-founder owns product)", team="2 co-founders", timeline="In progress",
    cover='<img src="/assets/img/thumbs/mobility-wide.jpg" alt="An older couple walking along a garden path" width="1600" height="900">',
    problem=paras("Mobility aids look like medical equipment. Users feel stigmatized, and common designs have real safety gaps."),
    did=bullets(
      "Visited senior centers and assisted living facilities around Berkeley. 14+ conversations with operators, caregivers, and advisors.",
      "Studied why companies here stall: payer, user, and decider are three different people; hardware margins erode; incumbents own distribution.",
      "Built the brand-as-moat thesis and a decision framework for the first product.",
      "Set an operating cadence for a team 16 time zones apart.",
    ),
    results=paras("Early stage and in progress. Results will be added as they're shareable."),
    differently=paras("Too early to say. This section fills in once there's a first product decision to look back on."),
    artifacts=paras("None yet that don't show the mechanism."),
  ),
  dict(slug="ey", title="EY, AI & Data",
    kicker="featured · senior consultant · New York · 2021 to 2024",
    heading="Giving leaders one clear view of a sprawling cloud migration.",
    desc="Program-wide risk, OKRs, and the first QBR for a $200M+ cloud migration at a Fortune 500 life sciences client, with $10M+ in realized savings.",
    tldr="Ran the operating system for a $200M+ cloud migration at a Fortune 500 life sciences client: risk, OKRs, and the first executive QBR. It redirected $3M to priority initiatives and realized $10M+ in savings.",
    role="Senior Technology Consultant, AI & Data Strategy (Staff Technology Consultant 2021 to 2023)", team="EY Technology Consulting, 25+ client teams", timeline="August 2021 to July 2024",
    cover='<img src="/assets/img/thumbs/ey-wide.jpg" alt="Earth at night from orbit, city lights glowing" width="1600" height="900">',
    problem=paras("A Fortune 500 life sciences client was moving its application portfolio to the cloud across 25+ teams. Risks surfaced late, executives got escalations instead of decisions, and nobody had one view of what was on track."),
    did=bullets(
      "Built the program-wide risk and OKR system: blocker and risk triage across 25+ teams. Earlier resource reallocation, 30% fewer executive escalations.",
      "Designed and launched the client's first QBR, aligning the CTO and product teams on direction and redirecting $3M to priority initiatives. Then standardized QBR governance across 5+ programs.",
      "Drove adoption of a custom PM methodology with a 15-person team and hands-on tool training. 90% adoption across 4,000 users.",
      "Prioritized every application for migration, modernization, or retirement with a value-capture framework. SVP approval, $10M+ in realized savings over 2 years.",
    ),
    results=stat_grid(("$3M", "redirected to priority initiatives"), ("−30%", "executive escalations"), ("90%", "adoption across 4,000 users"), ("$10M+", "realized savings over 2 years")) + "\n" + paras("Also at EY: logistics lead for a Fortune 500 consumer foods client (forecast accuracy +10% YoY), data architect on an internal initiative, and an internal AI adoption campaign that drove 200%+ usage across 5 user segments. Earlier: recovered $5M in pricing and mix leakage for a Fortune 500 software client, and re-architected Agile workflows for 25+ engineering teams."),
    differently="",
    artifacts="",
  ),
  dict(slug="mirrorme", title="MirrorMe",
    kicker="more work · co-founder, GTM · 2024",
    heading="Icebreakers that go deeper without getting awkward.",
    desc="An icebreaker card game for people who host. 150+ pre-launch purchase commitments with zero paid budget.",
    tldr="An icebreaker card game for hosts. 150+ pre-launch commitments at $30 to 40, with zero paid budget.",
    role="Co-founder, led GTM", team="2 co-founders", timeline="2024",
    cover='<img src="/assets/img/thumbs/mirrorme-wide.jpg" alt="MirrorMe question card" width="1600" height="900">',
    problem=paras("Hosts want guests to actually talk. Most icebreakers are too shallow to matter or too intense for near-strangers."),
    did=bullets(
      "100+ user surveys and a 10-product competitive scan found two high-intent segments: regular hosts, and the venues that host them.",
      "Built the deck on the OCEAN personality model: category cards set a trait, question cards ask about someone at the table, players rate 1 to 5.",
      "Skipped paid channels. Sold in person at card game cafes and social events in New York. 50+ decks sold.",
    ),
    results=stat_grid(("150+", "pre-launch purchase commitments"), ("$30 to 40", "price point"), ("$0", "paid budget"), ("50+", "decks sold")) + "\n" + paras("Insight: it sold itself in rooms where people already wanted to connect. Venue partnerships became the channel."),
    differently="",
    artifacts=paras("I later wrote up the deck as a tech pack: card spec, bill of materials, box dieline, costing, and a proofing checklist.") + "\n" + links(("Read the tech pack", "/projects/mirrorme-tech-pack")) + "\n" + artifact_grid(("/assets/img/projects/mirrorme/card-category.png", "Category card"), ("/assets/img/projects/mirrorme/card-question.png", "Question card"), ("/assets/img/projects/mirrorme/card-rules.jpg", "Setup and rules card"), ("/assets/img/projects/mirrorme/card-alt.png", "Alternative card design")),
  ),
  dict(slug="tritooling", title="Tritooling",
    kicker="featured · director of operations · Philippines · 2024 to 2025",
    heading="Fixing late deliveries and defects at a precision manufacturer.",
    desc="Director of Operations at a family-owned precision manufacturer serving semiconductor, medical device, and industrial clients across APAC.",
    tldr="A year running operations at a family-owned precision manufacturer serving semiconductor, medical device, and industrial clients. Fewer defects, faster delivery, a board-approved Japan launch.",
    role="Director of Operations", team="Operations, logistics, engineering", timeline="July 2024 to July 2025",
    cover='<img src="/assets/img/thumbs/tritooling-wide.jpg" alt="Engineer working at a precision machine" width="1600" height="900">',
    problem=paras("Bottlenecks showed up as late deliveries and defects. Operations, logistics, and engineering had no shared performance framework."),
    did=bullets(
      "Redesigned workflows across operations, logistics, and engineering around a performance-management framework, managing 7 direct reports.",
      "Built the ERP make-vs-buy business case from vendor costs and internal requirements. Secured executive approval, $100K in annual savings.",
      "Benchmarked pricing and expansion potential across 5 APAC countries. Secured board approval to launch in Japan, a $300K+ revenue opportunity.",
    ),
    results=stat_grid(("+15%", "on-time delivery"), ("−30%", "defects"), ("$100K", "annual savings (ERP make-vs-buy)"), ("$300K+", "revenue opportunity, board-approved Japan launch")),
    differently="",
    artifacts="",
  ),
  *PRODUCTS,
  *MODS,
  *COURSEWORK,
]

BUILD_SLUGS = {c["slug"] for c in (*PRODUCTS, *MODS, *COURSEWORK)}

# Sections in page order; a section whose content is empty is left out of the TOC and the body.
SECTIONS = (("problem", "The problem"), ("requirements", "Product requirements"),
            ("did", "What I did"), ("results", "Results"),
            ("milestones", "Milestones and next steps"), ("iterations", "Iterations and decisions"),
            ("differently", "What I'd do differently"), ("artifacts", "Artifacts"))
REQUIRED = ("slug", "title", "kicker", "heading", "desc", "tldr", "role", "team", "timeline",
            "cover", "problem", "did", "results")
DEFAULTS = dict(badge="", cover_class="", differently="", artifacts="",
                requirements="", milestones="", iterations="")
PLAIN_TEXT = ("title", "kicker", "role", "team", "timeline")  # text only, never HTML: escape on output


def validate(cases):
    slugs = [c["slug"] for c in cases]
    dupes = {s for s in slugs if slugs.count(s) > 1}
    assert not dupes, f"duplicate slugs: {dupes}"
    for c in cases:
        missing = [k for k in REQUIRED if k not in c]
        assert not missing, f"{c.get('slug', '?')}: missing {missing}"
    unknown = set(GRAD) - set(slugs)
    assert not unknown, f"GRAD keys with no case: {unknown}"


def render_sections(c):
    present = [(k, label) for k, label in SECTIONS if c[k].strip()]
    toc = "\n".join(f'        <a href="#{k}">{label}</a>' for k, label in present)
    body = "\n".join(f'        <h2 id="{k}">{label}</h2>\n{c[k]}' for k, label in present)
    return toc, body


def jsonld(c, og_image):
    """Labels the page as a project by Chae Kim, so search engines and AI assistants can cite it."""
    data = {
        "@context": "https://schema.org",
        "@type": "CreativeWork",
        "name": c["title"],
        "headline": html.unescape(re.sub(r"<[^>]+>", "", c["heading"])),
        "description": c["desc"],
        "url": f"{SITE_URL}/projects/{c['slug']}",
        "image": og_image,
        "creator": {"@type": "Person", "name": "Chae Kim", "alternateName": "Chae Woon Kim", "url": f"{SITE_URL}/"},
    }
    body = json.dumps(data, ensure_ascii=False, indent=2).replace("</", "<\\/")
    return '  <script type="application/ld+json">\n' + "\n".join("  " + line for line in body.splitlines()) + "\n  </script>"


def render(c, prev, nxt):
    c = {**DEFAULTS, **c}
    toc, body = render_sections(c)
    is_build = c["slug"] in BUILD_SLUGS
    mark = build_mark(c["slug"], "case-hero__mark", 56) if is_build else ""
    # builds use their own favicon, touch icon and share card; everything else keeps the site's 김 set
    own = build_icons(c["slug"], SITE_URL) if is_build else None
    icons, og_image = own or (SITE_ICONS, f"{SITE_URL}/assets/img/og-sky.png")
    fields = {
        **{k: c[k] for k in ("slug", "heading", "tldr", "cover", "cover_class", "badge")},
        **{k: html.escape(c[k]) for k in PLAIN_TEXT},
        "desc": html.escape(c["desc"]),
        "toc": toc,
        "body": body,
        "grad": GRAD.get(c["slug"], "plain"),
        "sec": "sec-builds" if is_build else "sec-work",
        "jsonld": jsonld(c, og_image),
        "back_href": "/#builds" if is_build else "/#work",
        "back_label": "All builds" if is_build else "All work",
        "prev_slug": prev["slug"], "prev_title": html.escape(prev["title"]),
        "next_slug": nxt["slug"], "next_title": html.escape(nxt["title"]),
        "site_url": SITE_URL, "icons": icons, "og_image": og_image,
        # builds show their color-seal mark above the eyebrow
        "mark": mark + "\n      " if mark else "",
        # web apps get a "Try it live" button on the cover and the dialog it opens
        "live": live_button(c["slug"]) if c["slug"] in LIVE_APPS else "",
        "live_dialog": LIVE_DIALOG + "\n" if c["slug"] in LIVE_APPS else "",
        "live_script": "\n" + LIVE_SCRIPT if c["slug"] in LIVE_APPS else "",
        "head_assets": CASE_HEAD_ASSETS, "top": CASE_TOP, "foot": CASE_FOOT, "scripts": CASE_SCRIPTS,
    }
    return SHELL.format_map(fields)


def main(argv=None):
    """Write projects/<slug>.html for every case. With --check, write nothing and fail if any page is out of date."""
    check = "--check" in (sys.argv[1:] if argv is None else argv)
    validate(CASES)
    OUT.mkdir(exist_ok=True)
    stale = []
    for i, c in enumerate(CASES):
        out = render(c, CASES[i - 1], CASES[(i + 1) % len(CASES)])
        if "[CONFIRM:" in out:
            sys.exit(f"{c['slug']}: unresolved CONFIRM placeholder")
        path = OUT / f"{c['slug']}.html"
        if check:
            if not path.exists() or path.read_text(encoding="utf-8") != out:
                stale.append(c["slug"])
        else:
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(out)
            print("wrote", c["slug"])
    if stale:
        sys.exit(f"out of date, run python3 scripts/build-cases.py: {stale}")
    if check:
        print(f"ok: {len(CASES)} pages up to date")


if __name__ == "__main__":
    main()
