from casekit import artifact_grid, bullets, links, paras, stat_grid

PROJECT = dict(slug="task-progress", title="task-progress",
  kicker="claude code mod · hooks module · 2026",
  heading="Seeing how far along a task is, right above the prompt.",
  desc="A Claude Code mod that turns Claude's own task checklist into a calm progress band above the prompt, plus a checklist pane.",
  tldr="Claude Code's spinner says something is happening, not how far along it is. task-progress reads the checklist Claude already keeps and draws it as a still band above the prompt: 3/5 · 60%, the step in progress, and a green ✓ all done at the end.",
  role="Product owner and builder", team="Solo, built with Claude Code", timeline="October 2026",
  cover='<img src="/assets/img/task-progress/task-progress-wide.jpg" alt="task-progress in Claude Code: a band above the prompt at 3 of 6 steps, and the /task-progress pane listing each step" width="1600" height="900">',
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
  artifacts=links(("Source on GitHub", "https://github.com/chaekim96/task-progress")) + "\n" + paras("Install from a Claude Code prompt: <code>/plugin install task-progress --marketplace chaekim96/task-progress</code>") + "\n" + artifact_grid(("/assets/img/task-progress/task-progress-card.png", "Its share card, with the build mark: a progress bar above a checklist.")),
  card=r"""
          <div class="stage" style="--g: var(--g-arcade)"><div class="art fill"><img src="/assets/img/task-progress/task-progress.jpg" alt="The /task-progress pane at 3 of 6: three steps done, one in progress, two pending" width="800" height="600" loading="lazy"></div><span class="pill">task-progress <em>Claude Code</em></span></div>
          <h3 class="w-title">Seeing how far along a task is, right above the prompt.</h3>
          <p class="meta">A mod that turns Claude's own task checklist into a calm progress band, with time left, a stuck warning and a context bar.</p>
""",
)
