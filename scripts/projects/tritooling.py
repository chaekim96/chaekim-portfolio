from casekit import bullets, paras, stat_grid

PROJECT = dict(slug="tritooling", title="Tritooling",
  kicker="featured · director of operations · Philippines · 2024 to 2025",
  heading="Fixing late deliveries and defects at a precision manufacturer.",
  desc="Director of Operations at a family-owned precision manufacturer serving semiconductor, medical device, and industrial clients across APAC.",
  tldr="A year running operations at a family-owned precision manufacturer serving semiconductor, medical device, and industrial clients. Fewer defects, faster delivery, a board-approved Japan launch.",
  role="Director of Operations", team="Operations, logistics, engineering", timeline="July 2024 to July 2025",
  cover='<img src="/assets/img/tritooling/tritooling-wide.jpg" alt="Engineer working at a precision machine" width="1600" height="900">',
  problem=paras("Bottlenecks showed up as late deliveries and defects. Operations, logistics, and engineering had no shared performance framework."),
  did=bullets(
    "Redesigned workflows across operations, logistics, and engineering around a performance-management framework, managing 7 direct reports.",
    "Built the ERP make-vs-buy business case from vendor costs and internal requirements. Secured executive approval, $100K in annual savings.",
    "Benchmarked pricing and expansion potential across 5 APAC countries. Secured board approval to launch in Japan, a $300K+ revenue opportunity.",
  ),
  results=stat_grid(("+15%", "on-time delivery"), ("−30%", "defects"), ("$100K", "annual savings (ERP make-vs-buy)"), ("$300K+", "revenue opportunity, board-approved Japan launch")),
  differently="",
  artifacts="",
  glyph="ops",
  grad="tri",
  card=r"""
          <div class="stage" style="--g: var(--g-tri)">
            <div class="art"><div class="glass"><b>Factory</b><span>operations</span></div></div>
            <span class="pill">Tritooling <em>2024–25</em></span>
          </div>
          <h3 class="w-title">Fixing late deliveries and defects at a precision manufacturer.</h3>
          <p class="meta">A year running operations at a precision manufacturer. <b>−30% defects.</b></p>
""",
)
