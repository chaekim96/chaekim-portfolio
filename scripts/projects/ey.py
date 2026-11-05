from casekit import bullets, paras, stat_grid

PROJECT = dict(slug="ey", title="EY, AI & Data",
  kicker="featured · senior consultant · New York · 2021 to 2024",
  heading="Giving leaders one clear view of a sprawling cloud migration.",
  desc="Program-wide risk, OKRs, and the first QBR for a $200M+ cloud migration at a Fortune 500 life sciences client, with $10M+ in realized savings.",
  tldr="Ran the operating system for a $200M+ cloud migration at a Fortune 500 life sciences client: risk, OKRs, and the first executive QBR. It redirected $3M to priority initiatives and realized $10M+ in savings.",
  role="Senior Technology Consultant, AI & Data Strategy (Staff Technology Consultant 2021 to 2023)", team="EY Technology Consulting, 25+ client teams", timeline="August 2021 to July 2024",
  cover='<img src="/assets/img/thumbs/ey-wide.jpg" alt="Earth at night from orbit, city lights glowing" width="1600" height="900">',
  problem=paras("A Fortune 500 life sciences client was moving its application portfolio to the cloud across 25+ teams. Risks surfaced late, executives got escalations instead of decisions, and nobody had one view of what was on track."),
  did=bullets(
    "Built the program-wide risk and OKR system: blocker and risk triage across 25+ teams. Earlier resource reallocation, 30% fewer executive escalations.",
    "Designed and launched the client's first QBR, aligning the CTO and product teams on direction and redirecting $3M to priority initiatives. Then standardized QBR governance across 5+ programs.",
    "Drove adoption of a custom PM methodology with a 15-person team and hands-on tool training. 90% adoption across 4,000 users.",
    "Prioritized every application for migration, modernization, or retirement with a value-capture framework. SVP approval, $10M+ in realized savings over 2 years.",
  ),
  results=stat_grid(("$3M", "redirected to priority initiatives"), ("−30%", "executive escalations"), ("90%", "adoption across 4,000 users"), ("$10M+", "realized savings over 2 years")) + "\n" + paras("Also at EY: logistics lead for a Fortune 500 consumer foods client (forecast accuracy +10% YoY), data architect on an internal initiative, and an internal AI adoption campaign that drove 200%+ usage across 5 user segments. Earlier: recovered $5M in pricing and mix leakage for a Fortune 500 software client, and re-architected Agile workflows for 25+ engineering teams."),
  differently="",
  artifacts="",
  glyph="consulting",
  grad="ey",
  card=r"""
          <div class="stage" style="--g: var(--g-ey)">
            <div class="art"><div class="glass"><b>Cloud</b><span>migration program</span></div></div>
            <span class="pill">EY <em>2021–24</em></span>
          </div>
          <h3 class="w-title">Giving leaders one clear view of a sprawling cloud migration.</h3>
          <p class="meta">Risk, OKRs, and the first executive QBR for a $200M+ cloud migration. <b>−30% executive escalations.</b></p>
""",
)
