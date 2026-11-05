from casekit import bullets, cover, links, paras, stat_grid

PROJECT = dict(slug="web-anatomy", title="Anatomy of a Website",
  kicker="product · illustrated encyclopedia · 2026",
  heading="Showing how a website works, from the DNS lookup to the AI answer.",
  desc="An illustrated, growing encyclopedia of how a website works, built on one idea: SEO and GEO start with the website.",
  tldr="An animated journey of one page load, a stack of the layers behind it, an example <head> linked line by line to a search result, a social card and an AI answer, and a searchable encyclopedia of 64 terms. A separate page explains the same ideas as a restaurant.",
  role="Builder", team="Solo, built with Claude Code", timeline="October 2026",
  cover=cover("/assets/img/builds/web-anatomy.jpg", "The Anatomy of a Website home page: the title, the line SEO and GEO start with the website, and the start of the journey of a request"),
  problem=paras("SEO and GEO advice usually starts with keywords or prompts. I think it starts earlier, with the website itself: if the foundation is weak, no keyword strategy or AI optimization can fix it. I wanted one place that shows the whole foundation, in plain English, with real code beside each idea."),
  did=bullets(
    "Drew the journey of a request as an animated SVG: browser, DNS, TLS, the CDN edge, the origin and the database, and back, plus the crawlers that make the same trip.",
    "Laid out the layers of a website (network, hosting, backend, HTML, CSS, JS, assets, SEO/GEO, quality, workflow), split into what visitors see and what only machines read.",
    "Built \"One head, three audiences\": an example <head> where each line links to the search result, the social card, or the AI answer it produces.",
    "Wrote a searchable, filterable encyclopedia of 64 terms. Each has a plain-English definition, how it works, a real snippet, and related terms, and every entry can be deep-linked, like #canonical.",
    "Added a simple version for newcomers: the website as a restaurant, what happens when you visit, how Google and AI find you, and a history of the web from 1969 to AI search, with 46 checked source links.",
    "Kept it static. All content lives in one data file, and a small script turns it into a page for every term, each labeled for search and AI answers, plus an A to Z index.",
  ),
  results=stat_grid(("64", "encyclopedia terms"), ("10", "layers of a website"), ("46", "checked source links in the history"), ("67", "pages in the sitemap")),
  artifacts=links(("Visit Anatomy of a Website", "https://webanatomy.vercel.app"), ("The simple version", "https://webanatomy.vercel.app/basics"), ("Source on GitHub", "https://github.com/chaekim96/web-anatomy")),
  live=("Anatomy of a Website", "https://webanatomy.vercel.app", ""),
  mark="web-anatomy-2",
  stage="arcade",
  tint="#7c5cff",
  card=r"""
          <div class="stage" style="--g: var(--g-arcade)"><div class="art"><div class="browser"><div class="browser__bar"><i></i><i></i><i></i><span>webanatomy</span></div><img src="/assets/img/builds/web-anatomy.jpg" alt="The Anatomy of a Website home page: the title, the line SEO and GEO start with the website, and the start of the journey of a request" width="960" height="600" loading="lazy"></div></div><span class="pill">Anatomy of a Website <em>2026</em></span></div>
          <h3 class="w-title">Showing how a website works, from the DNS lookup to the AI answer.</h3>
          <p class="meta">An illustrated encyclopedia on one idea: SEO and GEO start with the website.</p>
""",
)
