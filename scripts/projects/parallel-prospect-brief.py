from casekit import artifact_grid, bullets, cover, links, paras, stat_grid

PROJECT = dict(slug="parallel-prospect-brief", title="Parallel Prospect Brief",
  kicker="product · solo build · 2026",
  heading="Walking into a first sales call with every claim sourced.",
  desc="A command-line tool that turns a company name into a cited one-page sales brief, built on Parallel's Task API.",
  tldr="Type a company name. The CLI sends one Task API request with a 13-field schema and waits for a structured answer: what the company builds, how far it has gone with AI agents, which Parallel API fits, a first-call pitch, why now, who to talk to, discovery questions, and likely objections. It saves a markdown brief with numbered sources and a confidence level on each field.",
  role="Product owner and builder", team="Solo, built with Claude Code", timeline="October 2026",
  cover=cover("/assets/img/builds/parallel-prospect-brief.jpg", "An illustrative brief for an invented company, Example Co: what they do, products, agent signal, and best-fit API, with sources and confidence", 1600, 1000),
  problem=paras("Before a first sales call, a rep needs to know what the prospect does, whether they need the product, and what to say. That research is spread across many tabs, and the notes rarely say where each claim came from. Parallel sells web research APIs for AI agents, so I built the prep tool on its own Task API."),
  did=bullets(
    "Wrote the brief as a Task API output schema: 13 fields, with fixed choices for the agent signal and the best-fit API so briefs compare cleanly.",
    "Passed in what Parallel sells, its six APIs with prices, checked against parallel.ai on October 22, so the research agent can match a prospect's need to a specific API.",
    "Showed each field with numbered sources and the API's confidence rating, sharing one source list across the brief.",
    "Explained failures in plain language: a rejected key, an account out of credits, or a request Parallel didn't accept.",
    "Added a dry run that prints the exact request without calling the API, so it can be checked for free.",
    "Wrote six offline tests against an invented company, so they cost nothing and need no key.",
  ),
  results=stat_grid(("13", "fields per brief, each cited"), ("6", "Parallel APIs it can recommend"), ("~$0.025", "per brief on the core processor"), ("6", "offline tests")) + "\n" + paras("It hasn't run against the live API yet; that needs a Parallel account and key. The sample below is invented to show the format, and says so."),
  differently=paras("Get an API key on day one. I built and tested everything offline, so the first live run is still ahead, and that run is the real test of the schema."),
  artifacts=links(("Source on GitHub", "https://github.com/chaekim96/parallel-prospect-brief"), ("Sample brief", "https://github.com/chaekim96/parallel-prospect-brief/blob/main/examples/sample-brief.md")) + "\n" + artifact_grid(("/assets/img/cases/ppb-sample.jpg", "The full illustrative sample. Every fact is invented to show the format.")),
  card=r"""
          <div class="stage" style="--g: var(--g-tri)"><div class="art fill"><img src="/assets/img/builds/parallel-prospect-brief-card.jpg" alt="An illustrative prospect brief for an invented company: what they do, products, agent signal, and best-fit API, with sources" width="800" height="600" loading="lazy"></div><span class="pill">Parallel Prospect Brief <em>CLI</em></span></div>
          <h3 class="w-title">Walking into a first sales call with every claim sourced.</h3>
          <p class="meta">A CLI that turns a company name into a cited one-page sales brief, built on Parallel's Task API.</p>
""",
)
