from casekit import bullets, paras, stat_grid

PROJECT = dict(slug="lucent", title="Lucent",
  kicker="featured · co-founder & CEO · NSF I-Corps",
  heading="Making small businesses visible in AI search.",
  desc="Lucent is an AI search visibility platform with hands-on GEO and SEO advisory. It shows brands how they rank in ChatGPT, Perplexity, and Gemini, then helps them fix it.",
  tldr="An AI search visibility platform with hands-on GEO and SEO advisory. Lucent shows brands how they rank in ChatGPT, Perplexity, and Gemini, then helps them fix it.",
  role="Co-founder & CEO", team="Co-founder/CTO + a data science intern", timeline="2025 to 2026",
  cover='<a href="https://trylucent.ai" target="_blank" rel="noopener" aria-label="Open trylucent.ai"><img src="/assets/img/thumbs/lucent-wide.jpg" alt="Lucent homepage: The AI Search Console" width="1600" height="900"></a>',
  problem=paras("Customers now ask AI instead of Google. Small businesses can't see whether AI recommends them, and GEO tools are priced for enterprises."),
  did=bullets(
    "21 NSF I-Corps discovery interviews narrowed the ICP from \"everyone\" to digitally native SMBs and marketing agencies. 100+ interviews across U.S. and APAC SMBs tested willingness to pay.",
    "Positioned around the one-person marketing team: GEO plus SEO execution, not just citation tracking. 5 positioning hypotheses tested across 65 outbound prospects picked the message.",
    "Designed cheap tracking: statistical sampling, and re-running prompts only when models or rankings change.",
    "Closed and led our first paid pilot: multi-site SEO and AI visibility audits turned into an engineering action plan.",
    "Built the business case: bottom-up SAM, phased GTM, and a 100+ question diligence bank.",
  ),
  results=stat_grid(("1", "first paying pilot"), ("5", "LOIs in 30 days"), ("+50%", "discovery response rate"), ("NSF", "I-Corps backing")) + "\n" + paras("The advisory work that grew out of the pilot is on pause while we research more in the GEO space."),
  differently=paras("Lock the GTM motion earlier. It was the biggest gap. Positioning tests and pilots should have run in parallel, not in sequence."),
  artifacts="",
  glyph="startup",
  grad="lucent",
  card_wide=True,
  card=r"""
          <div class="stage" style="--g: var(--g-lucent)">
            <div class="art"><div class="browser"><div class="browser__bar"><i></i><i></i><i></i><span>trylucent.ai</span></div><img src="/assets/img/thumbs/lucent-wide.jpg" alt="Lucent's homepage: The AI Search Console" width="1440" height="810"></div></div>
            <span class="pill">Lucent <em>2025–26</em></span>
          </div>
          <h3 class="w-title">Making small businesses visible in AI search.</h3>
          <p class="meta">AI search visibility platform with GEO and SEO advisory. <b>First paying pilot, 5 LOIs in 30 days.</b></p>
""",
)
