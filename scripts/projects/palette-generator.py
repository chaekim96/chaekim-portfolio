from casekit import artifact_grid, bullets, cover, links, paras, stat_grid

PROJECT = dict(slug="palette-generator", title="Palette Generator",
  kicker="product · solo build · 2026",
  heading="Brand colors and fonts for founders who aren't designers.",
  desc="A palette and font-pairing generator that takes a non-designer from a one-line description to a brand look they can ship.",
  tldr="Describe what you're building and pick a mood. You get five colors with a job for each, a font pairing, and a sample website painted in them. Contrast is checked against WCAG, and the whole result lives in a share link.",
  role="Product owner and builder", team="Solo, built with Claude Code", timeline="September to October 2026",
  cover=cover("/assets/img/builds/palette.jpg", "Palette Generator turning 'coffee subscription, warm and earthy' into five roles of color and a font pairing"),
  problem=paras("Founders need a brand look long before they can hire a designer. Most palette tools hand you five pretty colors and stop there. Which one is the button? Which is the text? Can anyone read it?"),
  did=bullets(
    "Started from a Figma Make export and set one rule for every feature: does it get a non-designer to a shippable palette faster? If not, it waits.",
    "Generated palettes in OKLCH across seven moods, and tuned the Earthy and Romantic moods against a benchmark of 97 real palettes.",
    "Gave every color a job (text, primary, supporting, accent, background) and matched it with one of 25 curated Google Fonts pairings.",
    "Painted a sample startup homepage in the palette, and checked every color pairing for WCAG contrast, with the smallest fix suggested when one fails.",
    "Built Explore: a weekly scan of 115 startup homepages showing which moods and brand colors are common right now. Curated public sites only, robots.txt respected.",
    "Kept it serverless. The palette, fonts, and mood live in the URL, so sharing is copying a link. Export goes to CSS variables, Tailwind, or a PNG.",
  ),
  results=stat_grid(("7", "moods"), ("25", "curated font pairings"), ("115", "startup homepages scanned weekly"), ("0", "sign-ups")) + "\n" + paras("The coffee subscription palette above passes WCAG AA on all seven of its color pairings."),
  differently=paras("Build the benchmark before the generator. I tuned the moods against real palettes only after the first version worked. Starting with the benchmark would have set the target on day one."),
  artifacts=links(("Try Palette Generator", "https://color-palette-generator-three-sand.vercel.app"), ("Source on GitHub", "https://github.com/chaekim96/ColorPaletteGenerator")) + "\n" + artifact_grid(("/assets/img/cases/palette-preview.jpg", "Website preview: the palette painted onto a sample startup homepage, with the contrast check above it."), ("/assets/img/cases/palette-explore.jpg", "Explore: moods and brand colors across 115 startup homepages, refreshed weekly.")),
  live=("Palette Generator", "https://color-palette-generator-three-sand.vercel.app", ""),
  mark="palette-generator-2",
  stage="plain",
  tint="#0a84ff",
  card=r"""
          <div class="stage" style="--g: var(--g-mirror)"><div class="art"><div class="browser"><div class="browser__bar"><i></i><i></i><i></i><span>palette</span></div><img src="/assets/img/builds/palette.jpg" alt="Palette Generator turning 'coffee subscription, warm and earthy' into five roles of color and a font pairing" width="960" height="600" loading="lazy"></div></div><span class="pill">Palette Generator <em>2026</em></span></div>
          <h3 class="w-title">Brand colors and fonts for founders who aren't designers.</h3>
          <p class="meta">Palettes that pass accessibility checks, font pairings, and what real startups use right now.</p>
""",
)
