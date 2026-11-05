from casekit import artifact_grid, bullets, cover, links, paras, stat_grid

PROJECT = dict(slug="voiceprompter", title="VoicePrompter",
  kicker="product · macOS app · 2026",
  heading="Reading your notes on a call without anyone seeing them.",
  desc="A macOS teleprompter that follows your voice as you read, with capture protection tested against specific macOS recording APIs.",
  tldr="Your script floats above other apps. As you speak, it highlights the word you're on and scrolls to keep your line near the top. The capture test hides its content from ScreenCaptureKit on the tested Mac; older recording paths can still show it, and individual sharing apps need a manual check.",
  role="Builder", team="Solo, built with Claude Code", timeline="September to October 2026",
  cover=cover("/assets/img/builds/voiceprompter.jpg", "VoicePrompter listening at word 108 of 139, with the prompter highlighting the spoken word", 800, 600),
  problem=paras("I was practicing presenting and interviewing and wanted my notes on screen, without cluttering the screen I was sharing. The teleprompters I found either fell short or wanted me to pay."),
  requirements=bullets(
    "Keep the script readable above other apps, with controls to pause, hide, reposition, and resize it.",
    "Follow spoken words despite small skips, ad-libs, and recognition errors, without jumping on weak matches.",
    "Support on-device speech recognition, explain microphone and speech permissions, and make capture-protection limits visible.",
    "Keep the first version to one script at a time. Configurable hotkeys and additional speech engines remain outside the current build.",
  ),
  did=bullets(
    "Built a native Swift app: an overlay that floats on every Space, and a main window with every setting in a sidebar.",
    "Transcribed speech on the device with Apple's recognizer, restarting the session about every 50 seconds so results stay short and fast.",
    "Wrote the alignment. Each update matches the last 8 spoken words against the script, with fuzzy matching for misheard words and guards so it never jumps on weak evidence.",
    "Tested capture protection on macOS 15.7.4. ScreenCaptureKit and tested still-image APIs hide the content; legacy video paths can show it. The window name can still appear in a sharing picker.",
    "Added global hotkeys that need no Accessibility permission, double-click to jump to a word, and click-through so clicks reach the app underneath.",
  ),
  results=stat_grid(("~0.3 ms", "alignment update on an 8,800-word script"), ("8", "spoken words matched each update"), ("2", "permissions: mic and speech"), ("3", "capture-harness runs reproduced")),
  milestones=bullets(
    "<b>Built:</b> a floating script, voice tracking, a settings sidebar, and global controls.",
    "<b>Tested:</b> capture APIs on macOS 15.7.4, including a control panel to confirm that each recording actually captured the display.",
    "<b>Still to verify:</b> interactive sharing in Zoom, Meet, QuickTime, and OBS, plus a full uninterrupted latency run. These are checks to complete, not shipped guarantees.",
  ),
  iterations=bullets(
    "<b>Keeping up with speech:</b> restart recognition about every 50 seconds and carry alignment context across sessions.",
    "<b>Avoiding false jumps:</b> use fuzzy matching, a local search window, and stronger confirmation for larger moves.",
    "<b>Learning the protection boundary:</b> the API tests showed why a hide hotkey is still necessary, even when the normal capture path hides the overlay.",
  ) + "\n" + links(("Requirements and limitations", "https://github.com/chaekim96/VoicePrompter/blob/main/README.md"), ("Capture-test evidence", "https://github.com/chaekim96/VoicePrompter/blob/main/ProtectionTest/RESULTS.md")),
  differently=paras("Measure latency from the start. The speech recognizer dominates the delay, and I built the latency test only after the app worked. A full, uninterrupted latency run is still on my list."),
  artifacts=links(("Source on GitHub", "https://github.com/chaekim96/VoicePrompter"), ("Essay: What\u2019s the Point of Preinstalled Apps?", "/projects/preinstalled-apps")) + "\n" + artifact_grid(("/assets/img/cases/vp-main.jpg", "The main window while listening: status, position in the script, and prompter settings."), ("/assets/img/cases/vp-prompter.jpg", "The prompter further in. Read text dims and the current word turns gold. Captured with protection off.")),
  card=r"""
          <div class="stage" style="--g: var(--g-mobility)"><div class="art fill"><img src="/assets/img/builds/voiceprompter.jpg" alt="VoicePrompter listening at word 108 of 139, with the prompter highlighting the spoken word" width="800" height="600" loading="lazy"></div><span class="pill">VoicePrompter <em>macOS</em></span></div>
          <h3 class="w-title">Reading your notes on a call without anyone seeing them.</h3>
          <p class="meta">A teleprompter that scrolls as you speak and stays out of Zoom, Meet, and screenshots.</p>
""",
)
