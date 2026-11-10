from casekit import artifact_grid, bullets, cover, links, paras, stat_grid

PROJECT = dict(slug="ai-visibility-checker", title="AI Visibility Checker",
  kicker="product · solo build · 2026",
  heading="Knowing whether AI assistants can find, read and cite your site.",
  desc="A free checker that reads a page the way a crawler does and reports whether search engines and AI assistants can find, read and cite it.",
  tldr="Paste a URL. A server fetches the page the way a crawler that doesn't run JavaScript would, then runs seventeen scored checks in three groups: can AI find it, read it, and understand and cite it. It gives a score, the three fixes worth the most, and which of eleven crawlers robots.txt lets in.",
  role="Product owner and builder", team="With Chris Jackson, my Lucent co-founder; built with Claude Code", timeline="October 2026",
  cover=cover("/assets/img/ai-visibility-checker/ai-visibility-checker-2.jpg", "The checker report for chaekim.vercel.app, ready for AI answers, with the fixes worth the most listed first", 1600, 1000),
  problem=paras("An AI assistant can only cite a page it can fetch and read. Those basics are invisible from the outside: you can't tell by looking whether robots.txt blocks ChatGPT's crawler, or whether a page's words only appear after JavaScript runs. I'm researching the GEO space, and this is where it starts."),
  did=bullets(
    "Read each page from its raw HTML, the way a crawler that doesn't run JavaScript sees it.",
    "Checked robots.txt for eleven crawlers, separating search and live fetching, where blocking hurts visibility, from model training, where blocking is a choice. Matching follows the robots.txt standard.",
    "Turned six checks from the SEO audit playbook Chris Jackson and I built at Lucent into automatic ones: HTTPS and redirects, redirect chains, the mobile viewport, image alt text, heading order, and mixed content.",
    "Turned seventeen checks into a score in three groups, with a \"fix first\" list ranked by the points each fix is worth.",
    "Reported a partial check when a site refuses unknown bots, instead of scoring it zero.",
    "Made it safe to run in public: only public addresses on every redirect, a 2 MB cap, and an 8-second timeout.",
    "Shipped it with no dependencies and eleven tests, and made it pass its own check.",
  ),
  results=stat_grid(("17", "scored checks in three groups"), ("11", "crawlers read from robots.txt"), ("0", "dependencies"), ("100", "its own score")) + "\n" + paras("Its first run on my own portfolio found two real gaps: no llms.txt, and a short address that names the longer one as its main URL."),
  differently=paras("Test on sites I don't control, early. My first version scored sites that refuse unknown bots as zero, which made a major news site look invisible when it had only refused my checker. Running it on real sites before launch caught that."),
  artifacts=links(("Try the checker", "https://chaekim-ai-visibility.vercel.app"), ("Source on GitHub", "https://github.com/chaekim96/ai-visibility-checker")) + "\n" + artifact_grid(("/assets/img/ai-visibility-checker/avc-crawlers-2.jpg", "Which crawlers robots.txt lets in, split into search and live fetching versus model training.")),
  live=("AI Visibility Checker", "https://chaekim-ai-visibility.vercel.app", ""),
  card=r"""
          <div class="stage" style="--g: var(--g-lucent)"><div class="art"><div class="browser play"><div class="browser__bar"><i></i><i></i><i></i><span>ai visibility checker</span></div><img src="/assets/img/ai-visibility-checker/ai-visibility-checker-card-2.jpg" alt="The AI Visibility Checker report for chaekim.vercel.app, ready for AI answers" width="960" height="600" loading="lazy"><img class="play__f" src="/assets/img/ai-visibility-checker/avc-crawlers-2.jpg" alt="Which crawlers robots.txt lets in, split into search and live fetching versus model training." loading="lazy"><img class="play__f" src="/assets/img/ai-visibility-checker/ai-visibility-checker-2.jpg" alt="The checker report for chaekim.vercel.app, ready for AI answers, with the fixes worth the most listed first" loading="lazy"></div></div><span class="pill">AI Visibility Checker <em>2026</em></span></div>
          <h3 class="w-title">Knowing whether AI assistants can find, read and cite your site.</h3>
          <p class="meta">Paste a URL: crawler rules, llms.txt, structured data, and text that's there without JavaScript.</p>
""",
)
