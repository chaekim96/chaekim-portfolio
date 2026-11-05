from casekit import bullets, cover, links, paras, stat_grid

PROJECT = dict(slug="custom-llm", title="Custom LLM",
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
  mark="custom-llm-2",
  card=r"""
          <div class="stage"><div class="art fill fill--top"><img src="/assets/img/builds/custom-llm.jpg" alt="Terminal chat with the tiny model and its odd replies" width="768" height="474" loading="lazy"></div><span class="pill">Custom LLM <em>2026</em></span></div>
          <h3 class="w-title">Seeing how language models learn by training a tiny one.</h3>
          <p class="meta">A nanoGPT fork trained on a laptop CPU with my own teaching corpus, scored on 48 test prompts.</p>
""",
)
