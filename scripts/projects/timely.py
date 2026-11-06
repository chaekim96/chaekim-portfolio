from casekit import artifact_grid, bullets, cover, paras, stat_grid

PROJECT = dict(slug="timely", title="Timely",
  kicker="product · solo build · 2026",
  heading="Turning a messy note into a realistic plan for the day.",
  desc="A note-taker I built in Google AI Studio, where Gemini estimates and categorizes every line so a to-do list adds up to a real amount of time.",
  tldr="Timely was my first take on time-aware notes. You write a to-do list, and Gemini gives each line a duration and a category, so the note shows how much time it really asks for. Months later I used it as the worked example for my Product Blueprint. That audit found three things that would have hurt a public launch, and I fixed all three.",
  role="Product owner and builder", team="Solo, built with Google AI Studio and Claude Code", timeline="February 2026, revisited October to November 2026",
  cover=cover("/assets/img/timely/timely.jpg", "Timely with sample notes: a list on the left, and six lines on the right, each with a category tag and an estimate, totaling 4h 5m", 1600, 1000),
  problem=paras("A to-do list says what to do, not how long it takes, so a day can be overbooked before it starts. I wanted a note that does the math as I write: every line sized, and the whole list totaled."),
  did=bullets(
    "Built it in Google AI Studio with React. Each line goes to Gemini, which returns a short estimate, the minutes, and one of six categories in a fixed JSON format.",
    "Added a total for every note, sorting by longest or shortest, and search across notes. Notes save in the browser, with a migration so older notes keep working.",
    "Designed it like paper: a warm off-white page, ink-dark selection, and small pills for the numbers. It later became the Paper theme in my design system.",
    "In October, filled in my Product Blueprint template for it and wrote 25 test cases for the estimator, including empty, long, non-English and prompt-injection inputs.",
    "That audit found three launch blockers: the Gemini key was readable in the browser, a note's text went straight into the prompt, and the page title said \"SmartNotes Estimator\".",
    "Fixed all three: moved the Gemini call into a server function, put the prompt's rules in a system instruction with the note's text marked as data, and renamed the page to Timely.",
  ),
  results=stat_grid(("6", "categories per line"), ("25", "test cases for the estimator"), ("3 of 3", "launch blockers fixed"), ("7", "offline tests")) + "\n" + paras("A test build with a key set used to put that key in the browser code. After the fix it holds neither the key nor any Gemini code, and typing a note sends one request to the app's own server. Durations over 24 hours are rejected, so an injected \"99999 minutes\" can't be stored. The 25 test cases still need a run against the live model."),
  milestones=bullets(
    "<b>Completed:</b> the app, the product brief, the 25 test cases, and the three launch fixes, with tests.",
    "<b>Next:</b> deploy it with the Gemini key stored on the server, and run the 25 test cases against the live model.",
    "<b>Known issue:</b> in development only, React runs the app's start-up twice, which saves an empty list over saved notes before reading them. A production build isn't affected.",
  ),
  differently=paras("Put the AI call on a server from day one. Calling Gemini straight from the browser made Timely quick to build, and it was the first thing that had to be undone before launch. I later rebuilt the idea as <a href=\"/projects/tally\">Tally</a>, with Claude and a server from the start."),
  artifacts=paras("The repo is private. Screenshots use sample notes, so the estimates shown are illustrative, not live model output.") + "\n" + artifact_grid(("/assets/img/timely/timely-phone.jpg", "On a phone: the notes list, each with its total, using sample notes.")),
  card=r"""
          <div class="stage" style="--g: var(--g-mirror)"><div class="art"><div class="browser"><div class="browser__bar"><i></i><i></i><i></i><span>timely</span></div><img src="/assets/img/timely/timely-card.jpg" alt="Timely with sample notes: six lines, each with a category tag and an estimate, totaling 4h 5m" width="960" height="600" loading="lazy"></div></div><span class="pill">Timely <em>2026</em></span></div>
          <h3 class="w-title">Turning a messy note into a realistic plan for the day.</h3>
          <p class="meta">A note-taker built in Google AI Studio, where Gemini sizes and sorts every line.</p>
""",
)
