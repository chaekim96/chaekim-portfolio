from casekit import artifact_grid, bullets, cover, links, paras, stat_grid

PROJECT = dict(slug="personal-wiki", title="Personal Wiki",
  kicker="ai/ml coursework · mba 290t · 2026",
  heading="Asking my own notes questions, with no internet.",
  desc="A command-line study wiki that runs fully offline: a local Gemma model turns sources into linked Obsidian notes and answers questions with citations.",
  tldr="A study wiki for my AI course that never touches the cloud. Local Gemma, through Ollama, turns sources into linked Obsidian notes. An ask command answers from those notes with citations, or says the evidence isn't there.",
  role="Builder", team="Solo", timeline="September 2026",
  cover=cover("/assets/img/builds/personal-wiki.jpg", "Obsidian graph of the wiki's linked notes", 900, 646),
  problem=paras("Cloud assistants answer confidently from anywhere. For studying I wanted the opposite: answers only from my own sources, a citation for every claim, on a laptop with Wi-Fi off."),
  requirements=bullets(
    "Ingest my course sources into linked Obsidian notes and answer study questions from those sources with citations.",
    "Run entirely on the laptop after setup, with no cloud calls or hosted embeddings, within the machine's available memory.",
    "Keep ask, chat, and search behavior separate; unsupported questions should return insufficient evidence.",
    "Preserve hand-edited notes and source links when ingesting the same material again.",
  ),
  did=bullets(
    "Picked the model to fit the machine. Gemma 4 E2B at 4-bit, because the larger versions didn't fit in the 5 to 6 GB free on an 18 GB Mac.",
    "Wrote the CLI and harness with only Python's standard library: ingest, search, ask, and chat modes.",
    "Built hybrid retrieval: my own BM25 plus local embeddings, merged with reciprocal rank fusion.",
    "Wrote the expected answers for four tests before running them, including one the wiki should refuse.",
    "Checked ask-mode citations against the retrieved passages in code and flagged invalid answers. Chat has a separate citation check with one retry.",
    "Recorded an offline demo with Wi-Fi off. All four tests matched the online results.",
  ),
  results=stat_grid(("3 of 4", "tests passed, written in advance"), ("4.4 s", "per answer, warm"), ("~1.7 GB", "working memory"), ("0", "cloud calls")) + "\n" + paras("The failure is documented. A question in my own shorthand (\"A3\") missed the right passage, and the model answered a nearby question with a real citation."),
  milestones=bullets(
    "<b>Built:</b> local ingestion, linked notes, hybrid search, cited answers, and a separate study-partner chat mode.",
    "<b>Evaluated:</b> four prewritten ask tests, mode-separation checks, memory and response-time measurements, and an offline demonstration. Three of four ask tests passed.",
    "<b>Proposed, not implemented:</b> expand aliases such as A3, reserve retrieval space across sources, and add an answer-relevance check. Re-run the original tests and retain the baseline for comparison.",
  ),
  iterations=bullets(
    "<b>Keyword search to hybrid retrieval:</b> adding local embeddings moved the paraphrase test's relevant passages from ranks 5 and 4 to ranks 2 and 3.",
    "<b>Reliable ingestion:</b> save a plan for each source and detect hand edits, so repeated ingestion reuses note names and keeps edited notes.",
    "<b>Citations to relevance:</b> the A3 test exposed a real citation attached to the wrong answer. The next experiment must check whether the evidence answers the actual question, as well as whether the citation exists.",
  ) + "\n" + links(("Retrieval changes", "https://github.com/chaekim96/personal-wiki/blob/main/evidence/retrieval_changes.md"), ("Test results", "https://github.com/chaekim96/personal-wiki/blob/main/evidence/ask_tests/results.md"), ("Limitations and proposed improvements", "https://github.com/chaekim96/personal-wiki/blob/main/README.md#10-limitation-and-improvement")),
  differently=paras("Write more questions in my own shorthand before tuning retrieval. A citation check proves a citation exists, not that it answers the question; the failed A3 test made that distinction concrete."),
  artifacts=links(("Source and evidence on GitHub", "https://github.com/chaekim96/personal-wiki")) + "\n" + artifact_grid(("/assets/img/cases/wiki-note.jpg", "A generated note in Obsidian, with its sources linked back to the raw files."), ("/assets/img/cases/wiki-index.jpg", "The wiki's index: concepts and projects, each with a one-line summary.")),
  card=r"""
          <div class="stage" style="--g: var(--g-arcade)"><div class="art fill"><img src="/assets/img/builds/personal-wiki.jpg" alt="Obsidian graph of the wiki's linked notes" width="900" height="646" loading="lazy"></div><span class="pill">Personal Wiki <em>2026</em></span></div>
          <h3 class="w-title">Asking my own notes questions, with no internet.</h3>
          <p class="meta">Local Gemma via Ollama, plus hybrid retrieval over a course wiki. Runs fully offline.</p>
""",
)
