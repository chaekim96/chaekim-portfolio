from casekit import bullets, links, paras, stat_grid

PROJECT = dict(slug="smartmodel", title="SmartModel",
  kicker="claude code mod · solo build · 2026",
  heading="Matching each prompt to the right model, so easy work costs less.",
  desc="A Claude Code hook that scores how hard each prompt is and recommends the cheapest model that can handle it.",
  tldr="A model router built into Claude Code. Before Claude acts, a hook scores the prompt's effort from 0 to 100 and recommends Haiku, Sonnet, Opus, or Fable. Ask mode shows a picker, auto routes on its own, and block stops the prompt before any tokens are spent.",
  role="Designer and builder", team="Solo, built with Claude Code", timeline="October 2026",
  cover='<img src="/assets/img/smartmodel/smartmodel-wide.jpg" alt="SmartModel\'s picker in Claude Code: rates a prompt medium-effort and recommends Sonnet" width="1600" height="900">',
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
  card=r"""
          <div class="stage" style="--g: var(--g-arcade)"><div class="art"><div class="term" aria-hidden="true"><p>SmartModel rates this medium-effort.</p><p>Which model should run it?</p><ul><li class="on">Sonnet (recommended)</li><li>Haiku</li><li>Opus</li><li>Fable</li></ul></div></div><span class="pill">SmartModel <em>Claude Code</em></span></div>
          <h3 class="w-title">Matching each prompt to the right model, so easy work costs less.</h3>
          <p class="meta">A hook that scores how hard a prompt is and recommends Haiku, Sonnet, Opus, or Fable. Runs in ask, auto, or block mode.</p>
""",
)
