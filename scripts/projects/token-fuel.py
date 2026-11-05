from casekit import artifact_grid, bullets, links, paras, stat_grid

PROJECT = dict(slug="token-fuel", title="Token-Fuel",
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
  card=r"""
          <div class="stage" style="--g: var(--g-tri)"><div class="art fill"><img src="/assets/img/builds/token-fuel.jpg" alt="Token-Fuel in the menu bar at 67%, and its floating window: Good, 668.5k of 1M left, about 46 turns" width="800" height="600" loading="lazy"></div><span class="pill">Token-Fuel <em>macOS</em></span></div>
          <h3 class="w-title">Seeing how much context is left before a session runs out.</h3>
          <p class="meta">A floating gauge on the Claude window and a CLI status line for Claude Code and Codex.</p>
""",
)
