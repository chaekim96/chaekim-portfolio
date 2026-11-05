from casekit import artifact_grid, bullets, links, paras, stat_grid

PROJECT = dict(slug="pacman-dqn", title="Pac-Man DQN",
  kicker="ai/ml coursework · 2026",
  heading="Teaching an agent to play Ms. Pac-Man by trial and error.",
  desc="A Deep Q-Network trained on Atari Ms. Pac-Man, with every number reported straight from the run's own output files.",
  tldr="An agent that sees only pixels and points learned Ms. Pac-Man over 100 games. Its mean score across five fixed test games rose from 492 to 680. I chose three settings, ran it once end to end, and reported what happened, including where it got worse.",
  role="Builder", team="Solo", timeline="September 2026",
  cover='<img src="/assets/img/pacman-dqn/pacman-dqn.gif" alt="The trained agent playing Ms. Pac-Man" width="160" height="210">', cover_class="case-cover--pixel",
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
  artifacts=links(("Notebook and evidence on GitHub", "https://github.com/chaekim96/pacman-dqn")) + "\n" + artifact_grid(("/assets/img/pacman-dqn/pacman-untrained.gif", "Before training: the agent mostly circles one corner of the maze."), ("/assets/img/pacman-dqn/pacman-trained.gif", "After training: the best game from the final evaluation."), ("/assets/img/pacman-dqn/pacman-training.jpg", "The training dashboard: scores, update loss, and exploration per episode.")),
  mark="pacman-dqn-2",
  grad="arcade",
  card=r"""
          <div class="stage" style="--g: var(--g-arcade)"><div class="art fill fill--contain fill--pixel"><img src="/assets/img/pacman-dqn/pacman-dqn.gif" alt="The trained agent playing Ms. Pac-Man" width="160" height="210" loading="lazy"></div><span class="pill">Pac-Man DQN <em>2026</em></span></div>
          <h3 class="w-title">Teaching an agent to play Ms. Pac-Man by trial and error.</h3>
          <p class="meta">A DQN agent that raised its mean evaluation score from 492 to 680.</p>
""",
)
