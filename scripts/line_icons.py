"""Monoline icon paths for every mark's glyph, on a 24px grid. Data only; build-mark-variants.py renders them.

Drawn with stroke="currentColor", round caps and joins, no fills. A tiny dot is written as ("dot", cx, cy, r)
in DOTS and is the only filled shape. Two weights are rendered from the same paths: 2 (regular) and 3 (bold).
Keys are the mark slugs (see mark_art.base_slug).
"""

NAMES = {
    "ai-visibility-checker": "Check", "arcade": "Play", "code-improver": "Review", "custom-llm": "Train",
    "networking-tracker": "Connect", "pacman-dqn": "Maze", "palette-generator": "Palette",
    "parallel-prospect-brief": "Brief", "personal-wiki": "Notes", "product-blueprint": "Plan",
    "relay": "Hand off", "review-labeler": "Label", "smartmodel": "Route", "spotify-review-triage": "Sort", "tally": "Count",
    "task-progress": "Progress", "timely": "Time", "token-fuel": "Fuel", "typerace": "Type",
    "voiceprompter": "Speak", "web-anatomy": "Layers",
}

PATHS = {
    "ai-visibility-checker": '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5 21 21"/>',
    "arcade": '<path d="M3.5 18H10v-6h6.5"/><path d="M16.5 12V6.5"/>',
    "code-improver": '<path d="M8 7 3 12l5 5M16 7l5 5-5 5M10 12.6l1.9 1.9 3.2-3.8"/>',
    "custom-llm": '<path d="M4 4v16h16"/><path d="M7.5 8c1.2 5.2 3 8 5.6 8.8 2.2.7 3.5.5 5.4.5"/>',
    "networking-tracker": '<circle cx="6" cy="6.5" r="2.6"/><circle cx="18" cy="6.5" r="2.6"/><path d="M9.2 6.5h5.6"/>'
                          '<rect x="7.5" y="13.5" width="9" height="7" rx="1.8"/><path d="M9.8 13.5V12a2.2 2.2 0 0 1 4.4 0v1.5"/>',
    "pacman-dqn": '<rect x="3.5" y="3.5" width="17" height="17" rx="2"/><rect x="6.5" y="10.5" width="3" height="3" rx=".6"/>',
    "palette-generator": '<path d="M12 3.5a8.5 8.5 0 0 0 0 17c1.3 0 1.9-.8 1.9-1.7 0-.5-.2-.9-.5-1.3-.3-.4-.5-.8-.5-1.3 0-.9.8-1.7 1.7-1.7h2.1a3.8 3.8 0 0 0 3.8-3.8c0-4-3.8-7.2-8.5-7.2z"/>',
    "parallel-prospect-brief": '<path d="M7 3.5h7.5L19 8v11a1.5 1.5 0 0 1-1.5 1.5h-10A1.5 1.5 0 0 1 6 19V5A1.5 1.5 0 0 1 7 3.5z"/>'
                               '<path d="M14.5 3.5V8H19M9 12.5h6M9 16.5h4"/>',
    "personal-wiki": '<circle cx="12" cy="12" r="2.2"/><path d="M10.4 10.4 7 7.4M13.8 10.4l3.6-3.8M13.8 13.6l3.6 2.8M10.4 13.6 8 16.8"/>'
                     '<circle cx="5.6" cy="6" r="1.6"/><circle cx="18.6" cy="5.4" r="1.6"/><circle cx="19" cy="17.6" r="1.6"/><circle cx="6.6" cy="18.4" r="1.6"/>',
    "product-blueprint": '<path d="M4 20v-4.5h4.5V11H13V4.5h7V20z"/><path d="M14.8 9.2l1.5 1.5 2.6-3"/>',
    "relay": '<rect x="2" y="8.5" width="6.5" height="7" rx="1.6"/><path d="M10.5 12h4M13 10l2 2-2 2"/><rect x="16" y="8" width="6" height="8" rx="1.8"/><path d="M17.8 12.2l1.2 1.2 2-2.4"/>',
    "review-labeler": '<path d="M3.5 7.5A2.5 2.5 0 0 1 6 5h7.5l7 7-7 7H6a2.5 2.5 0 0 1-2.5-2.5z"/><path d="M7.5 12l2 2 3.5-4"/>',
    "smartmodel": '<path d="M12 21v-7c0-3.5-5-4-5-8M12 14c0-3.5 5-4 5-8M12 14V6"/><circle cx="7" cy="4.6" r="1.4"/><circle cx="12" cy="4.6" r="1.4"/><circle cx="17" cy="4.6" r="1.4"/>',
    "spotify-review-triage": '<path d="M4 5h16l-6 7.5V18l-4 2v-7.5z"/>',
    "tally": '<path d="M6 5v14M10 5v14M14 5v14M18 5v14M3 16.5 21 7.5"/>',
    "task-progress": '<rect x="3" y="3" width="18" height="6" rx="3"/><path d="M4 15l1.6 1.6L8.6 13.2M12 15h8M12 20h6"/>',
    "timely": '<path d="M7 3.5h6.5L18 8v4"/><path d="M7 3.5A1.5 1.5 0 0 0 5.5 5v12A1.5 1.5 0 0 0 7 18.5h4"/>'
              '<circle cx="16.5" cy="17" r="4.5"/><path d="M16.5 14.6v2.6l1.7 1"/>',
    "token-fuel": '<path d="M4 17a8 8 0 0 1 16 0M12 17l3.4-5"/>',
    "typerace": '<path d="M4 8h7M4 12h9M4 16h6M18 5.5v13"/>',
    "voiceprompter": '<path d="M5 10v4M9 6.5v11M13 9v6M17 8v8M21 11v2"/>',
    "web-anatomy": '<path d="M5 6h14M5 12h14M5 18h14"/>',
}

# The only filled shapes: (cx, cy, r). Everything else is stroke.
DOTS = {
    "arcade": [(19, 6, 1.3)],
    "pacman-dqn": [(13.5, 12, 1), (17, 12, 1)],
    "token-fuel": [(12, 17, 1.4)],
    "custom-llm": [(19, 16.3, 1.3)],
    "palette-generator": [(7.8, 11.6, 1.3), (9.8, 7.6, 1.3), (14.2, 7.4, 1.3), (17, 11, 1.3)],
    "spotify-review-triage": [],
}
