from casekit import artifact_grid, bullets, links, paras, stat_grid

PROJECT = dict(slug="mirrorme", title="MirrorMe",
  kicker="more work · co-founder, GTM · 2024 to 2025",
  heading="Icebreakers that go deeper without getting awkward.",
  desc="An icebreaker card game for people who host. 150+ pre-launch purchase commitments, sold through venue partnerships.",
  tldr="An icebreaker card game for hosts. 150+ pre-launch commitments at $30 to 40, sold through venue partnerships.",
  role="Co-founder, led GTM", team="2 co-founders", timeline="2024 to 2025",
  cover='<img src="/assets/img/mirrorme/mirrorme-wide.jpg" alt="MirrorMe question card" width="1600" height="900">',
  problem=paras("Hosts want guests to actually talk. Most icebreakers are too shallow to matter or too intense for near-strangers."),
  did=bullets(
    "200+ playtests, 100+ user surveys, and a 10-product competitive scan found two high-intent segments: regular hosts, and the venues that host them.",
    "Built the deck on the OCEAN personality model: category cards set a trait, question cards ask about someone at the table, players rate 1 to 5.",
    "Playtests showed players cared more about discovering each other than winning, so we repositioned the game around discovery.",
    "Sold in person at card game cafes and social events in New York. 50+ decks sold.",
  ),
  results=stat_grid(("150+", "pre-launch purchase commitments"), ("$30 to 40", "price point"), ("200+", "playtests"), ("50+", "decks sold")) + "\n" + paras("Insight: it sold itself in rooms where people already wanted to connect. Venue partnerships became the channel."),
  differently="",
  artifacts=paras("I later wrote up the deck as a tech pack: card spec, bill of materials, box dieline, costing, and a proofing checklist.") + "\n" + links(("Read the tech pack", "/projects/mirrorme-tech-pack")) + "\n" + artifact_grid(("/assets/img/mirrorme/mirrorme/card-category.png", "Category card"), ("/assets/img/mirrorme/mirrorme/card-question.png", "Question card"), ("/assets/img/mirrorme/mirrorme/card-rules.jpg", "Setup and rules card"), ("/assets/img/mirrorme/mirrorme/card-alt.png", "Alternative card design")),
  glyph="product",
  grad="mirror",
  docs=[("MirrorMe tech pack", "/projects/mirrorme-tech-pack",
         "A page with the card spec, bill of materials, box dieline, costing and a proofing checklist.")],
  card=r"""
          <div class="stage" style="--g: var(--g-mirror)">
            <div class="art"><div class="fan"><img src="/assets/img/mirrorme/mirrorme/card-category.png" alt="MirrorMe card: Openness to experience, pink" width="714" height="1000" loading="lazy"><img src="/assets/img/mirrorme/mirrorme/card-alt.png" alt="MirrorMe card: Openness to experience, orange" width="733" height="1000" loading="lazy"></div></div>
            <span class="pill">MirrorMe <em>2024–25</em></span>
          </div>
          <h3 class="w-title">Icebreakers that go deeper without getting awkward.</h3>
          <p class="meta">An icebreaker card game for hosts. <b>200+ playtests, 150+ pre-orders.</b></p>
""",
)
