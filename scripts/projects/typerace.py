from casekit import artifact_grid, bullets, cover, links, paras, stat_grid

PROJECT = dict(slug="typerace", title="TypeRace",
  kicker="product · solo build · 2026",
  heading="Settling who types fastest, with one link and no sign-up.",
  desc="A live browser typing race for classmates: share a four-letter code, type the same short story, first to finish wins.",
  tldr="Start a room and share the link. Everyone types the same short story at once, with live progress bars, WPM, and accuracy, then a results chart and a weekly class leaderboard. No accounts, no ads.",
  role="Product owner and builder", team="Solo, built with Claude Code", timeline="October 2026",
  cover=cover("/assets/img/typerace/typerace-2.jpg", "A TypeRace race in progress at 70 WPM, ink on near-white, the progress bar halfway across"),
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
  artifacts=links(("Play TypeRace", "https://typerace.typerace.workers.dev")) + "\n" + artifact_grid(("/assets/img/typerace/typerace-results-2.jpg", "Results from a test race on my own server: finishing order, WPM, accuracy, and a WPM chart.")),
  live=("TypeRace", "https://typerace.typerace.workers.dev", "Races here are real: a finished race posts to the weekly class leaderboard."),
  card=r"""
          <div class="stage" style="--g: var(--g-lucent)"><div class="art"><div class="browser play"><div class="browser__bar"><i></i><i></i><i></i><span>typerace</span></div><img src="/assets/img/typerace/typerace-2.jpg" alt="A TypeRace race in progress at 70 WPM, ink on near-white, the progress bar halfway across" width="960" height="600" loading="lazy"><img class="play__f" src="/assets/img/typerace/typerace-results-2.jpg" alt="Results from a test race on my own server: finishing order, WPM, accuracy, and a WPM chart." loading="lazy"></div></div><span class="pill">TypeRace <em>2026</em></span></div>
          <h3 class="w-title">Settling who types fastest, with one link and no sign-up.</h3>
          <p class="meta">Live races for classmates: share a code, type the same story, first to finish wins.</p>
""",
)
