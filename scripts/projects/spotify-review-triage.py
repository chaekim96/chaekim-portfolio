from casekit import artifact_grid, bullets, cover, links, paras, stat_grid

PROJECT = dict(slug="spotify-review-triage", title="Spotify Review Triage",
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
  live=("Spotify Review Triage", "https://spotify-review-triage.vercel.app", ""),
  card=r"""
          <div class="stage" style="--g: var(--g-mobility)"><div class="art"><div class="browser"><div class="browser__bar"><i></i><i></i><i></i><span>spotify-review-triage</span></div><img src="/assets/img/builds/spotify-review-triage-card.jpg" alt="The Spotify Review Triage dashboard: 660,622 reviews, $4.36 spend, and the recommendation" width="960" height="600" loading="lazy"></div></div><span class="pill">Spotify Review Triage <em>2026</em></span></div>
          <h3 class="w-title">Turning a flood of app reviews into one clear product priority.</h3>
          <p class="meta">A multi-agent LLM pipeline over 660,622 reviews, with an independent checker and a live dashboard.</p>
""",
)
