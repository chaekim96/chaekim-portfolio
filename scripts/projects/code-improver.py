from casekit import artifact_grid, bullets, paras

PROJECT = dict(slug="code-improver", title="Code Improver",
  kicker="claude code mod · subagent · 2026",
  heading="A second reviewer that reads every file I touch.",
  desc="A custom Claude Code subagent that reviews changed files for readability, performance, and best practices.",
  tldr="A read-only reviewer I can call after any change. It explains each issue, shows the current code, and proposes an improved version, without touching a file itself.",
  role="Builder", team="Solo", timeline="October 2026",
  cover='<img src="/assets/img/code-improver/code-improver-wide.jpg" alt="The code-improver subagent definition file" width="1600" height="900">',
  problem=paras("Code written fast with an AI pair often gets reviewed by nobody. I wanted a second pass that is consistent, quick, and safe to run anywhere."),
  did=bullets(
    "Defined a subagent with one job: scan files for readability, performance, and best-practice issues.",
    "Limited it to read-only tools (Read, Grep, Glob), so it can suggest changes but never make them.",
    "Required the same shape for every finding: the problem, the current code, and an improved version.",
    "Wrote its description so Claude Code knows to reach for it right after code is written or changed.",
  ),
  results=paras("Small by design. Eight lines of configuration change how every review goes, and because it can't edit, I can run it on anything."),
  differently=paras("Give it a severity ranking and permission to say \"no issues.\" Without one, a reviewer always finds something, and small nits crowd out real bugs."),
  artifacts=paras("The file above is the whole thing, verbatim. Below, it reviewing the script that builds this page: 14 findings, ordered by severity, and no files touched.") + "\n" + artifact_grid(("/assets/img/code-improver/code-improver-review.jpg", "An excerpt of its review of build-cases.py. Its top finding checked out on the live site.")),
  card=r"""
          <div class="stage" style="--g: var(--g-ey)"><div class="art fill"><img src="/assets/img/code-improver/code-improver.jpg" alt="Code Improver reviewing build-cases.py: 14 findings ordered by severity, starting with a template page that was publicly served" width="800" height="600" loading="lazy"></div><span class="pill">Code Improver <em>subagent</em></span></div>
          <h3 class="w-title">A second reviewer that reads every file I touch.</h3>
          <p class="meta">A custom Claude Code subagent that suggests readability, performance, and best-practice fixes.</p>
""",
)
