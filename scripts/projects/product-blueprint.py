from casekit import artifact_grid, bullets, cover, paras, stat_grid

PROJECT = dict(slug="product-blueprint", title="Product Blueprint",
  kicker="method · solo build · 2026",
  heading="One way to build every product, with a test at each step.",
  desc="My personal prompt library and playbook for building products with AI tools: a six-stage loop with a pass/fail gate at each stage, a design system, a product template, and a database of 22 versioned prompts with evals.",
  tldr="I build fast with Lovable, Google AI Studio and Claude, and my prompts and design choices lived in chat history. The blueprint writes the method down: six stages from Discover to Ship, each ending with a pass/fail gate, a design system pulled from my own products, a template to fill in per product, and 22 prompts that each carry their own evals. Two scripts check the prompt database and score AI features against a locked test set.",
  role="Product owner and builder", team="Solo, built with Claude Code", timeline="October to November 2026",
  cover=cover("/assets/img/product-blueprint/product-blueprint.jpg", "The build loop: six stages from Discover to Ship, each with the gate it has to pass", 1600, 1000),
  problem=paras("AI builders make the first draft easy. Keeping products consistent is harder. My prompts lived in old chats, each product picked its own colors, and I judged AI output by feel. When a prompt worked, I couldn't find it again or tell whether a change made it better."),
  did=bullets(
    "Wrote a six-stage build loop, Discover to Ship. Each stage ends with a short pass/fail gate, so problems get fixed where they start.",
    "Pulled a design system from two of my products: a dark technical theme from FaFo and a warm paper theme from Timely, with shared rules for layout, type, motion and copy voice, and an 8-point design rubric.",
    "Built a product template that walks one product through every stage and records each gate result.",
    "Wrote 22 prompts across the six stages, from problem framing to launch posts. Each has a version, its inputs, pass/fail evals and a changelog.",
    "Set pass targets by risk (85%, 90% or 98%) and a test-set format that always includes empty input, long input, other languages and prompt-injection attempts.",
    "Wrote a checker that fails if a prompt is missing evals, a version or an input. On its first run it caught a gap in one of my own prompts.",
    "Filled in the template for Timely as a worked example, with a 25-case test set for its time estimator.",
    "Fixed the three launch blockers it found: moved the Gemini call to a server function, put the prompt's rules in a system instruction with the user's text marked as data, and renamed the page to Timely.",
  ),
  results=stat_grid(("6", "stages, each with a gate"), ("22", "versioned prompts with evals"), ("25", "test cases for Timely's estimator"), ("3 of 3", "Timely launch blockers fixed")) + "\n" + paras("Filling in the template for Timely found three things to fix before launch: the Gemini key was readable in the browser, user text went into the prompt unprotected, and the page title didn't match the product name. All three are fixed. A test build with a key set used to put that key in the browser code, and now holds neither the key nor any Gemini code. Durations over 24 hours are now rejected, so an injected \"99999 minutes\" can't be stored. The 25 test cases haven't been run against the live model yet, and every prompt is still marked draft. One moves to tested only after it passes its evals on three real uses."),
  differently=paras("Start from one real product, not the whole method. Filling in the template for Timely taught me more than writing it did: it found the launch blockers, and the gates told me when they were fixed. I'd fill it in for the next product first and write each stage as I reach it."),
  artifacts=paras("The repo is private. Below, one prompt from the database, as it appears in the repo.") + "\n" + artifact_grid(("/assets/img/product-blueprint/pb-prompt.jpg", "The copy review prompt: when to use it, the prompt, and the evals its output has to pass.")),
  card=r"""
          <div class="stage" style="--g: var(--g-mirror)"><div class="art fill"><img src="/assets/img/product-blueprint/product-blueprint-card.jpg" alt="The build loop: six stages from Discover to Ship, each with the gate it has to pass" width="800" height="600" loading="lazy"></div><span class="pill">Product Blueprint <em>playbook</em></span></div>
          <h3 class="w-title">One way to build every product, with a test at each step.</h3>
          <p class="meta">A six-stage build loop, a design system, and 22 prompts that each come with their own evals.</p>
""",
)
