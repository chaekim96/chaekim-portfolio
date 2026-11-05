from casekit import artifact_grid, bullets, cover, links, paras, stat_grid

PROJECT = dict(slug="networking-tracker", title="Networking Tracker",
  kicker="product · solo build · 2026",
  heading="Keeping track of every coffee chat, without sharing a thing.",
  desc="A private contact tracker where Postgres row-level security keeps each person's data their own.",
  tldr="Sign in and keep a list of the people you meet: company, role, where you met, notes, and priority. Sort, filter, and search it. Every row is private to the person who wrote it, and the database enforces that, not just the app.",
  role="Builder", team="Solo", timeline="September 2026",
  cover=cover("/assets/img/networking-tracker/networking-tracker.jpg", "Networking Tracker filtered to high-priority contacts, with demo data"),
  problem=paras("At Berkeley you meet a lot of people quickly, and notes on them end up scattered. A tool for that has to answer one question before any other: can anyone else see my contacts?"),
  did=bullets(
    "Built sign-up, sign-in, and a contact list with create, edit, delete, sort, filter, and search, in Next.js on Vercel.",
    "Stored contacts in Neon Postgres and isolated them with row-level security in the database, so even a direct call to the public Data API can't read someone else's rows.",
    "Proved it. Queried as the role the API uses while two rows existed, and got zero back.",
    "Validated input three times: in the form, on the server, and with a database constraint. The friendly message is a courtesy, not the defense.",
    "Designed all four list states: loading skeletons, two distinct empty states, a plain-language error with one-click retry, and success.",
    "Captured every screenshot in the write-up from the deployed app, not localhost.",
  ),
  results=stat_grid(("0", "rows visible to the wrong user"), ("3", "layers of input validation"), ("4", "list states designed"), ("15", "screenshots from the live app")),
  differently=paras("Check the security boundary on every push. The isolation test needs two real accounts and a live database, so today it runs on demand. Next: run it in CI against a throwaway database branch that seeds its own accounts."),
  artifacts=links(("Try it", "https://networking-tracker-five-sage.vercel.app"), ("Source on GitHub", "https://github.com/chaekim96/networking-tracker")) + "\n" + artifact_grid(("/assets/img/networking-tracker/nt-invalid.jpg", "An empty name, rejected with the reason in plain language. Demo data."), ("/assets/img/networking-tracker/nt-mobile.jpg", "The contact list on a phone. Demo data.")),
  live=('Networking Tracker', 'https://networking-tracker-five-sage.vercel.app', "Some browsers block signing in inside a frame. If it won't let you in, open it in a new tab."),
  card=r"""
          <div class="stage" style="--g: var(--g-ey)"><div class="art"><div class="browser"><div class="browser__bar"><i></i><i></i><i></i><span>networking tracker</span></div><img src="/assets/img/networking-tracker/networking-tracker.jpg" alt="Networking Tracker filtered to high-priority contacts, with demo data" width="960" height="600" loading="lazy"></div></div><span class="pill">Networking Tracker <em>2026</em></span></div>
          <h3 class="w-title">Keeping track of every coffee chat, without sharing a thing.</h3>
          <p class="meta">A contact tracker where Postgres row-level security keeps each person's data their own.</p>
""",
)
