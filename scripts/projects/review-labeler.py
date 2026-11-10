from casekit import artifact_grid, bullets, cover, paras, stat_grid

PROJECT = dict(slug="review-labeler", title="Review Labeler",
  kicker="ai/ml · solo build · in progress",
  heading="Finding out when a small fine-tuned model is good enough.",
  desc="An experiment, in progress, testing whether a small fine-tuned model can label app reviews as well as a big prompted one for a fraction of the cost.",
  tldr="Spotify Review Triage labeled 100,000 reviews with a small, cheap model. This asks the next question: would a small model fine-tuned for the job match a big model? Before training anything, I reread the old results and found that most of the gap I blamed on the model came from my own hand labels. So I rewrote the label guide, built a labeling sheet, and wrote the scripts that lock the test set and score the models. No model has been trained yet.",
  role="Product owner and builder", team="Solo, built with Claude Code", timeline="October 2026, in progress",
  cover=cover("/assets/img/review-labeler/review-labeler.jpg", "The labeling sheet: one review, Duo Premium no ads at all, labeled billing, praise, severity 1, with the guide's rules beside it", 1600, 1000),
  problem=paras("Teams that label feedback every week pay big-model prices for a narrow, repetitive task. A small model trained for that one job might do as well for much less, but nobody on those teams knows until they measure it. In Spotify Review Triage, the cheap model agreed with my hand labels on topic only 42% of the time, which looked like a reason to try fine-tuning."),
  requirements=bullets(
    "Compare three models on one locked set of human labels: the cheap model as it ran, a strong prompted model, and a small open model fine-tuned on the strong model's labels.",
    "Judge topic by macro F1 so small topics like billing and access count, with intent, severity, valid output and cost as guardrails.",
    "Lock the test set before any training, and keep copies of test reviews out of training.",
    "Get two people to agree on topic at least 80% of the time before trusting any model score.",
    "Stay under $30, and write the hypothesis down before seeing results.",
  ),
  did=bullets(
    "Wrote the brief first: hypothesis, one primary metric, a not-doing list, and a pass/fail gate at each stage, using my Product Blueprint.",
    "Reread all 29 topic disagreements from the Spotify golden set. By my reading, the model had followed the old guide on about 25 of them, and my hand labels hadn't. Thirteen were generic reviews like \"Super\" that the guide sends to other.",
    "Rewrote the label guide: six steps, ten rules that each settle one of those disagreements, and worked examples in English, Hindi and Indonesian.",
    "Built a labeling sheet that runs in the browser, keeps the reviews on my computer, and never shows the old labels, so they can't sway the new ones.",
    "Wrote scripts to lock the test set, score models per topic, check agreement between two labelers, and rescore the old model.",
    "Checked the scorer by having it reproduce the Spotify project's published golden-set results exactly before trusting it on new labels.",
  ),
  results=stat_grid(("29", "old disagreements reread"), ("10", "rules in the new guide"), ("0.2711", "published topic F1, matched exactly"), ("18", "offline tests")) + "\n" + paras("The main finding so far is about the measurement, not the models: the 42% understated the cheap model. Whether fine-tuning is worth it is still open. No model has been trained or scored on the new labels yet."),
  milestones=bullets(
    "<b>Completed:</b> the brief, the label guide, the labeling sheet, and scripts to split, score, rescore and check agreement.",
    "<b>Next:</b> relabel the 50 golden reviews with the new guide and rescore the old model on them.",
    "<b>Then:</b> lock 250 human-labeled test reviews, label 3,000 training reviews with the strong model, fine-tune the small one, and score all three.",
  ),
  differently=paras("Check the labels before blaming the model. My first draft of the brief blamed a vague guide for the 42%. The guide was clear; my hand labels broke it."),
  artifacts=paras("The repo is private until I've checked the review dataset's terms.") + "\n" + artifact_grid(("/assets/img/review-labeler/rl-examples.jpg", "Worked examples from the new guide: reviews the old labels and the model disagreed on, with the answer each rule gives.")),
  card=r"""
          <div class="stage" style="--g: var(--g-mirror)"><div class="art fill"><img src="/assets/img/review-labeler/review-labeler-card.jpg" alt="The labeling sheet: one review labeled billing, praise, severity 1, with the guide's rules beside it" width="800" height="600" loading="lazy"></div><span class="pill">Review Labeler <em>in progress</em></span></div>
          <h3 class="w-title">Finding out when a small fine-tuned model is good enough.</h3>
          <p class="meta">Testing fine-tuned vs. prompted models on app reviews. So far: a rewritten label guide and a labeling sheet.</p>
""",
)
