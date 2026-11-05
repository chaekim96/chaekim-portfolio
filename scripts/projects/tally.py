from casekit import artifact_grid, bullets, cover, links, paras, stat_grid

PROJECT = dict(slug="tally", title="Tally",
  kicker="product · solo build · 2026",
  heading="Knowing how long your to-do list will actually take.",
  desc="A note-taker where every line gets a Claude time estimate, totaled in a ledger so a to-do list becomes an honest picture of the day.",
  tldr="Tally turns a to-do list into a plan. You write lines like a normal note. Claude reads the whole note and gives each line a most-likely time, a range, and a category. The ledger adds it up, and the Day view lets you drag items onto a calendar.",
  role="Product owner and builder", team="Solo, built with Claude Code", timeline="September to October 2026",
  cover=cover("/assets/img/tally/tally.jpg", "Tally estimating a week of to-dos: an hour for the case memo, 30 minutes for bug reports, 3h45 in all"),
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
  artifacts=links(("Try Tally", "https://tally-lake-seven.vercel.app"), ("Source on GitHub", "https://github.com/chaekim96/tally")) + "\n" + artifact_grid(("/assets/img/tally/tally-day.jpg", "The Day view: a capacity meter, the Unscheduled tray, and blocks on the calendar."), ("/assets/img/tally/tally-summary.jpg", "The Summary: what's left, the finish-by time, and where the time goes.")),
  live=("Tally", "https://tally-lake-seven.vercel.app", ""),
  card=r"""
          <div class="stage" style="--g: var(--g-tri)"><div class="art"><div class="browser play"><div class="browser__bar"><i></i><i></i><i></i><span>tally</span></div><img src="/assets/img/tally/tally.jpg" alt="Tally estimating a week of to-dos: an hour for the case memo, 30 minutes for bug reports, 3h45 in all" width="960" height="600" loading="lazy"><img class="play__f" src="/assets/img/tally/tally-day.jpg" alt="The Day view: a capacity meter, the Unscheduled tray, and blocks on the calendar." loading="lazy"><img class="play__f" src="/assets/img/tally/tally-summary.jpg" alt="The Summary: what's left, the finish-by time, and where the time goes." loading="lazy"></div></div><span class="pill">Tally <em>2026</em></span></div>
          <h3 class="w-title">Knowing how long your to-do list will actually take.</h3>
          <p class="meta">A note-taker where every line gets a Claude time estimate, totaled in a ledger column.</p>
""",
)
