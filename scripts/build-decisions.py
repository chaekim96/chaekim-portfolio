#!/usr/bin/env python3
"""Builds /projects/decisions: the options behind each call, and which one I picked.

Usage:  python3 scripts/build-decisions.py
Every entry is a real choice from my working sessions: the options I was shown, the one
I picked, and (only where I gave them) my reasons. Keep it that way: no invented options,
no reasons I didn't give. Private choices (job search, pay, visas) never go here.
"""
import html
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from stamp_shared import CASE_HEAD_ASSETS, CASE_TOP, CASE_FOOT, CASE_SCRIPTS  # noqa: E402

SITE_URL = "https://chaekim-portfolio.vercel.app"

AREAS = {
    "design": ("Design", "violet"),
    "content": ("Content", "peach"),
    "products": ("Products", "mint"),
    "coursework": ("Coursework", "sky"),
}

# opt(label, trade-off, chosen=False, rec=False)
def opt(label, note, chosen=False, rec=False):
    return dict(label=label, note=note, chosen=chosen, rec=rec)

def D(area, when, project, question, options, why=(), link=None):
    return dict(area=area, when=when, project=project, question=question, options=options, why=list(why), link=link)

DECISIONS = [
    # ---------------- this site: design ----------------
    D("design", "Sep 2026", "This site", "How far should Apple's typeface go?", [
        opt("Apple's system font everywhere", "Real Apple type scale and weights. The site would read as native on a Mac.", rec=True),
        opt("Poppins headings, system font for UI", "The brand stays mine; labels and buttons go native."),
        opt("Keep Poppins throughout", "No typeface change. Apple's influence comes through color, spacing and motion.", chosen=True),
    ], why=["Friendly geometry: round letters feel warm, not corporate", "One font, less noise", "Continuity with earlier versions of the site"]),
    D("design", "Oct 2026", "This site", "My name mark: a red seal or a brush?", [
        opt("A 도장 name seal", "Official and formal. The first version of Stamp used it."),
        opt("My name brushed in ink", "김채운 in black ink on paper.", chosen=True),
    ], why=["Shows a person: brush strokes carry motion and imperfection, so the mark reads as human"]),
    D("design", "Oct 2026", "This site", "Which design becomes the whole site?", [
        opt("Desktop", "Folders and windows, a macOS metaphor."),
        opt("Ink", "Monochrome, brush wordmark, serif headings."),
        opt("Desktop Craft", "Apple-style polish, blue accent, glass menu bar."),
        opt("Stamp", "Quiet and gallery-like. Real work as the picture.", chosen=True),
    ], why=["Quieter: the desktop was fun but busy; Stamp gets out of the way", "Faster to read: the work is one scroll away instead of behind windows"]),
    D("design", "Oct 2026", "This site", "What should \"live previews\" mean on the Builds cards?", [
        opt("Click to try it live", "Card keeps its screenshot; a button opens the running app. Nothing loads until asked.", chosen=True, rec=True),
        opt("Always-live embeds", "The real sites running in every card. Most alive, but slow, and phones struggle."),
        opt("Animated previews", "Short looping recordings. Alive and fast, but not interactive."),
        opt("Link previews", "A preview image per project for shared links."),
    ], link=("/#builds", "See it on the Builds tab")),
    D("design", "Oct 2026", "This site", "Which background?", [
        opt("Cool lavender-blue wash", "Lavender to near-white to sky. Light and calm, no warm tones.", chosen=True, rec=True),
        opt("Aurora", "Slow-drifting blobs of lavender, sky, mint and peach. More personality."),
        opt("Subtle neutral hue", "White fading to a cool gray-blue. Closest to before."),
    ], why=["The work is the color", "Calm, not loud", "Light and airy, like morning light", "Keeps black and white from feeling stark"]),
    D("design", "Oct 2026", "This site", "Which background, take two?", [
        opt("Lavender sky", "The wash I had. Fresh, but it shares hues with the Lucent card."),
        opt("Hanji paper", "Warm near-white from the paper behind my 김채운 seal.", chosen=True, rec=True),
        opt("Near white", "The off-white from my brand exploration. The quietest option."),
        opt("Cool fog", "A grey-blue mist, calm and techy."),
        opt("Warm dawn", "Peach into cream, friendly and personal."),
        opt("Sage morning", "A green whisper into soft blue."),
    ]),
    D("design", "Oct 2026", "This site", "Hanji felt too muted. Which background, take three?", [
        opt("Hanji, as is", "Pale cream paper with a warm glow."),
        opt("Hanji with fibers", "Faint grain and long paper fibers."),
        opt("Hanji with ink wash", "Sumi ink soaking in behind the seal."),
        opt("Hanji with vermilion", "The seal's red in the tab, the email underline, and a dot.", rec=True),
        opt("Deeper hanji", "A warmer, richer paper tone.", rec=True),
        opt("Sky and clouds", "Sky blue overhead, soft clouds, fading to white.", chosen=True),
    ], why=["I like that blue", "It reflects the sky and the clouds"]),
    D("design", "Oct 2026", "This site", "How should the homepage put builds first?", [
        opt("Swap tabs: Builds first", "Builds opens by default; Work moves to second. Smallest change, keeps the tabs.", chosen=True, rec=True),
        opt("Featured builds above the tabs", "Keep Work as the default, but show three flagship builds before the tabs."),
        opt("One scrolling page, no tabs", "Builds, then Work, then About on one page. Best for skimmers, a bigger change."),
        opt("Keep Work first", "Outcomes at known companies first; builds one click away."),
    ], why=["I want people to see what I've built first"], link=("/#builds", "See the Builds tab")),
    D("design", "Oct 2026", "This site", "Inside Builds, what should lead?", [
        opt("Live products first", "The four apps you can try live, then more products, mods, coursework, side quests.", chosen=True, rec=True),
        opt("Newest first", "One list by date. Shows momentum, but mixes big and small builds."),
        opt("Three flagships, then the rest", "Large cards for the strongest three, everything else compact."),
    ]),
    # ---------------- this site: content ----------------
    D("content", "Oct 2026", "This site", "The site's numbers predate my resume. Which should it use?", [
        opt("Match the resume", "Update every page to the resume's figures.", chosen=True, rec=True),
        opt("Keep the site's numbers", "Only if both sets were true and the resume just shortened them."),
        opt("Go line by line", "Decide each figure separately."),
    ]),
    D("content", "Oct 2026", "This site", "When should the new resume and headlines go live?", [
        opt("After the numbers are fixed", "Ship together, so the live resume never contradicts the homepage.", chosen=True, rec=True),
        opt("Push now", "Live right away, with the resume and homepage disagreeing for a while."),
        opt("Not yet", "Review on the test site first."),
    ]),
    D("content", "Oct 2026", "This site", "What should the homepage design notes cover?", [
        opt("Stamp, plus the journey", "The current tokens and type, with a short strip on how the site got here.", chosen=True, rec=True),
        opt("Stamp only", "Just the current design system."),
        opt("Bring back Desktop Craft", "Restore the desktop design first, then document it."),
    ], link=("/#design-notes", "Read the design notes")),
    D("content", "Oct 2026", "This site", "What happens to the draft case study on choosing a brand?", [
        opt("Rebuild for Stamp, publish later", "Restyle it, update the ending, and publish once it's in my own words.", chosen=True, rec=True),
        opt("Fold it into the design notes", "Drop the separate page."),
        opt("Leave it as is", "Don't touch the draft for now."),
    ]),
    D("content", "Oct 2026", "This site", "Is a hand-brushed 김채운, traced to vector, still a next step?", [
        opt("Yes, still planned", "Keep it on the backlog.", chosen=True),
        opt("Maybe later", "An idea, not a commitment."),
        opt("Drop it", "Remove it from the plan."),
    ], link=("/projects/portfolio#backlog", "See the backlog")),
    # ---------------- products ----------------
    D("products", "Oct 2026", "AI Visibility Checker", "Where should the checker live?", [
        opt("Its own app and repo", "A new Vercel app with a serverless function that fetches the URL, plus its own case page.", chosen=True, rec=True),
        opt("A page inside the portfolio", "Easiest to find, but mixes a product into the portfolio's code."),
        opt("A Cloudflare Worker", "Fast and free, but a different platform from my other web apps."),
    ], link=("/projects/ai-visibility-checker", "AI Visibility Checker")),
    D("products", "Oct 2026", "AI Visibility Checker", "How much should version 1 check?", [
        opt("One page, every signal", "Crawler rules, llms.txt, sitemap, structured data, previews, and text without JavaScript. Free and fast.", chosen=True, rec=True),
        opt("Crawl the whole site", "The same checks across many pages. Slower, and more requests to other people's sites."),
        opt("Also ask AI assistants", "Ask a model whether it cites the site. Closest to real GEO, but it costs money per check."),
    ]),
    D("products", "Oct 2026", "AI Visibility Checker", "Should the code be public?", [
        opt("Public", "The case page can link to the source.", chosen=True, rec=True),
        opt("Private", "Keep it private for now, possibly for Lucent."),
    ]),
    D("products", "Oct 2026", "AI Visibility Checker", "How should the Lucent audit playbook go into the checker?", [
        opt("Add its checks and credit it", "Turn the playbook's automatable checks into new ones and credit the playbook by name.", chosen=True, rec=True),
        opt("Credit only", "Mention the playbook and Chris without changing the checks."),
        opt("Link the Lucent repo too", "Only works once the repo is public."),
    ]),
    D("products", "Oct 2026", "AI Visibility Checker", "How should Chris Jackson, my Lucent co-founder, be credited?", [
        opt("Partner on the method", "The checks draw on the audit playbook we built at Lucent; the checker code is new.", chosen=True, rec=True),
        opt("Co-builder of the checker", "Name him as co-creator of the checker itself."),
        opt("Ask Chris first", "Hold anything that names him until he agrees."),
    ]),
    D("products", "Oct 2026", "Parallel Prospect Brief", "Which demo should I build on Parallel's API?", [
        opt("Prospect brief agent", "Type a company name, get a cited one-page sales brief: what they build, whether they run AI agents, which Parallel API fits, and discovery questions.", chosen=True, rec=True),
        opt("Search eval kit", "A 20-question gold set run across Parallel Search's modes, scored on accuracy, speed, and cost, with a one-page report."),
        opt("AI visibility checker", "Check how a brand shows up in answers to category questions, with cited sources. Closest to my Lucent work."),
    ], why=["It doubles as material a sales team can use"], link=("/projects/parallel-prospect-brief", "Parallel Prospect Brief")),
    D("products", "Oct 2026", "Parallel Prospect Brief", "What should finished include?", [
        opt("Polished CLI", "Verify the Parallel facts it uses, add tests and a clearly labeled sample brief, and tighten the README. Costs nothing until it runs.", chosen=True, rec=True),
        opt("CLI and a web page", "Plus a small page where a visitor types a company and gets a brief. Each brief spends credits, so it would need an access code."),
        opt("CLI and a prospect list step", "Plus a FindAll step: describe an ideal customer, get matching companies, and brief the top few. More API spend per run."),
    ]),
    D("products", "Oct 2026", "Parallel Prospect Brief", "Should the code be public?", [
        opt("Public", "The case page can link to the source. The key stays in a local file git ignores.", chosen=True, rec=True),
        opt("Private", "Keep it private for now."),
    ]),
    D("products", "Oct 2026", "Palette Generator", "Where should the weekly trend scan read brand colors from?", [
        opt("Startup lists", "New Product Hunt launches plus a curated list. Needs an API token.", rec=True),
        opt("A curated list only", "Hand-picked sites kept in the repo. No token; \"latest\" means the sites we add.", chosen=True),
        opt("Design galleries", "The most designed sites, but their terms prohibit scraping."),
    ], link=("/projects/palette-generator", "Palette Generator")),
    D("products", "Oct 2026", "Palette Generator", "How should Explore show each scanned site?", [
        opt("Name and palette", "Company name, its palette, and a link. No screenshots or logos.", chosen=True, rec=True),
        opt("Palette only", "Anonymous palettes by mood and industry. Safer, less interesting."),
    ]),
    D("products", "Oct 2026", "Palette Generator", "How often should the trends refresh?", [
        opt("Weekly", "Current enough; about 150 site visits a week.", chosen=True, rec=True),
        opt("Daily", "Fresher, but brand colors rarely change daily, and it means 7x the deploys."),
        opt("Manual", "Only when I ask."),
    ]),
    # ---------------- coursework ----------------
    D("coursework", "Oct 2026", "Spotify Review Triage", "The 10,000 development reviews were already labeled. Reuse those labels in the final run?", [
        opt("Reuse the development labels", "Keep the earlier labels for those 10,000 reviews."),
        opt("Classify them again in the final run", "Label them fresh with the final setup.", chosen=True),
    ], why=["Every graded label should come from one final configuration"], link=("/projects/spotify-review-triage", "Spotify Review Triage")),
    D("coursework", "Oct 2026", "Spotify Review Triage", "How close must the model's sentiment score be to my label to count as a match?", [
        opt("Exact", "Any difference counts as wrong."),
        opt("Average error only", "Report the mean error, with no pass or fail."),
        opt("Within ±0.5, with ±0.25 also reported", "The same or the next step on a five-step scale. The average error is reported too.", chosen=True),
    ], why=["Sentiment runs from -1 to 1, so an exact match would mark near-identical scores wrong"]),
    D("coursework", "Sep 2026", "Pac-Man DQN", "How much should the agent explore?", [
        opt("0.20", "Balanced: random one move in five after warm-up.", chosen=True, rec=True),
        opt("0.10", "Follows its own estimates more; settles into a habit faster."),
        opt("0.30", "More variety in memory, less practice of its own policy."),
    ], link=("/projects/pacman-dqn", "Pac-Man DQN")),
    D("coursework", "Sep 2026", "Pac-Man DQN", "How many training games?", [
        opt("100", "Best shot at real learning, with four checkpoints along the way.", chosen=True, rec=True),
        opt("50", "A middle ground, two checkpoints."),
        opt("25", "Meets the minimum; learning may be modest."),
        opt("5", "A setup check; may learn nothing."),
    ]),
    D("coursework", "Sep 2026", "Pac-Man DQN", "Which learning rate?", [
        opt("0.0001", "The standard value. Stable, best with longer runs.", rec=True),
        opt("0.00025", "Slightly faster learning, so change shows up in a short run.", chosen=True),
        opt("0.001", "Aggressive; values can blow up."),
    ], why=["2.5x the reference, so change would be visible in only 100 games, without going as far as 0.001"]),
    D("coursework", "Sep 2026", "Pac-Man DQN", "Where should training run?", [
        opt("Google Colab", "A cloud GPU, matching the assignment guide.", rec=True),
        opt("Locally on my Mac", "Apple GPU acceleration, no session expiring mid-run.", chosen=True),
    ]),
    D("coursework", "Sep 2026", "Personal Wiki", "Which sources should a fully offline study wiki use?", [
        opt("Three notes I write", "Fully shareable and easy to verify."),
        opt("My Custom LLM write-up", "My own project, my own words."),
        opt("Wikipedia articles", "Course topics, saved locally with attribution."),
        opt("A mix", "My Custom LLM write-up plus two Wikipedia articles: retrieval-augmented generation and transformers.", chosen=True),
    ], link=("/projects/personal-wiki", "Personal Wiki")),
    D("coursework", "Sep 2026", "Personal Wiki", "One source was too long for the local model. Cut it off, or fix it?", [
        opt("Fix it: split into a third subject", "Every part reaches the model, and each call stays short.", chosen=True, rec=True),
        opt("Fix it: send more per call", "Fewer notes, but longer prompts and slower calls."),
        opt("Keep the cut-off", "Document it as a known limitation."),
    ]),
    D("coursework", "Sep 2026", "Personal Wiki", "The offline recording missed some required chat checks. Re-record, or document the gap?", [
        opt("Re-record them offline", "About two minutes with Wi-Fi off.", rec=True),
        opt("Submit, and document the gap", "Say plainly in the README which checks ran online.", chosen=True),
    ]),
]


def card(d):
    label, hue = AREAS[d["area"]]
    opts = []
    for o in d["options"]:
        cls = "opt opt--chosen" if o["chosen"] else "opt"
        mark = '<span class="opt__mark" aria-hidden="true">✓</span>' if o["chosen"] else '<span class="opt__mark" aria-hidden="true"></span>'
        tags = []
        if o["chosen"]:
            tags.append('<span class="tagc tagc--pick">My pick</span>')
        if o["rec"]:
            tags.append('<span class="tagc">Recommended</span>')
        sr = " (my pick)" if o["chosen"] else ""
        opts.append(
            f'          <li class="{cls}">{mark}<div><p class="opt__l"><b>{html.escape(o["label"])}</b>{"".join(tags)}<span class="visually-hidden">{sr}</span></p>'
            f'<p class="opt__n">{html.escape(o["note"])}</p></div></li>')
    went_against = any(o["rec"] and not o["chosen"] for o in d["options"])
    flag = '<span class="flag">Went against the recommendation</span>' if went_against else ""
    why = ""
    if d["why"]:
        why = ('        <div class="why"><p class="why__k">Why</p><ul>'
               + "".join(f"<li>{html.escape(w)}</li>" for w in d["why"]) + "</ul></div>\n")
    link = f'        <p class="dlink"><a href="{d["link"][0]}">{html.escape(d["link"][1])} →</a></p>\n' if d["link"] else ""
    return (f'      <article class="dcard dcard--{hue}" data-area="{d["area"]}">\n'
            f'        <p class="dcard__k"><i aria-hidden="true"></i>{label} · {html.escape(d["project"])} · {d["when"]}</p>\n'
            f'        <h3>{html.escape(d["question"])}</h3>{flag}\n'
            f'        <ol class="opts">\n' + "\n".join(opts) + "\n        </ol>\n"
            + why + link + "      </article>")


def counts():
    total = len(DECISIONS)
    against = sum(1 for d in DECISIONS if any(o["rec"] and not o["chosen"] for o in d["options"]))
    options = sum(len(d["options"]) for d in DECISIONS)
    return total, options, against


def page():
    total, options, against = counts()
    filters = "".join(
        f'<button type="button" class="fchip fchip--{hue}" data-filter="{k}" aria-pressed="false">{label}</button>'
        for k, (label, hue) in AREAS.items())
    cards = "\n".join(card(d) for d in DECISIONS)
    desc = "How I make decisions: the options I laid out for each call on this site and my projects, which one I picked, and why."
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>How I decide · Chae Kim - Portfolio</title>
  <meta name="description" content="{desc}">
  <meta property="og:title" content="How I decide · Chae Kim - Portfolio">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="article">
  <meta property="og:image" content="{SITE_URL}/assets/img/og-sky.png">
  <link rel="canonical" href="{SITE_URL}/projects/decisions">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/favicon-32.png" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{CASE_HEAD_ASSETS}
</head>
<body class="v v-stamp case sec-builds">
  <a class="skip" href="#main">Skip to content</a>
{CASE_TOP}

  <main id="main">
    <section class="case-hero wrap">
      <a class="case-hero__back" href="/projects/portfolio">← This portfolio</a>
      <p class="eyebrow">this site · how I decide · 2026</p>
      <h1 class="case-hero__title">How I decide: the options behind each call.</h1>
      <p class="tldr">I work by laying out two to four options, each with what it costs, then picking one and writing down why. These are real choices from building this site and my projects, including the options I passed on.</p>
      <p class="meta-line"><b>Decisions</b> {total} · <b>Options weighed</b> {options} · <b>Went against the recommendation</b> {against} times</p>
    </section>

    <section class="wrap how">
      <ol class="how__steps">
        <li><b>1</b><span><strong>Lay out the options.</strong> Two to four, each with its trade-off in one line.</span></li>
        <li><b>2</b><span><strong>Pick one, and say why.</strong> The recommended option is a starting point, not the answer.</span></li>
        <li><b>3</b><span><strong>See it before committing.</strong> When it's visual, mock it up first, like the eight ideas I tried on a test page.</span></li>
        <li><b>4</b><span><strong>Write it down.</strong> So the next decision starts from this one.</span></li>
      </ol>
      <div class="legend" aria-hidden="true">
        <span class="lg lg--pick"><i>✓</i>My pick</span><span class="lg"><i></i>Passed on</span><span class="tagc">Recommended</span>
      </div>
    </section>

    <section class="wrap decisions" aria-label="Decisions">
      <div class="filters" role="group" aria-label="Filter by area"><button type="button" class="fchip is-on" data-filter="all" aria-pressed="true">All</button>{filters}</div>
      <div class="dgrid">
{cards}
      </div>
    </section>
  </main>

{CASE_FOOT}
{CASE_SCRIPTS}
  <script>
    (function () {{
      var chips = document.querySelectorAll('.fchip'), cards = document.querySelectorAll('.dcard');
      chips.forEach(function (c) {{
        c.addEventListener('click', function () {{
          var f = c.dataset.filter;
          chips.forEach(function (x) {{ var on = x === c; x.classList.toggle('is-on', on); x.setAttribute('aria-pressed', on); }});
          cards.forEach(function (d) {{ d.hidden = !(f === 'all' || d.dataset.area === f); }});
        }});
      }});
    }})();
  </script>
</body>
</html>
"""


if __name__ == "__main__":
    out = ROOT / "projects" / "decisions.html"
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(page())
    t, o, a = counts()
    print(f"wrote projects/decisions.html ({t} decisions, {o} options, {a} against the recommendation)")
