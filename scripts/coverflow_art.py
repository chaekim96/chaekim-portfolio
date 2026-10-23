"""Cover art for the Builds Cover Flow: one ink sketch per build, all in the same hand.

Every cover is a 240x240 line drawing: round caps, one stroke weight, ink only, roughened
by the shared #sketch filter so it reads as drawn rather than plotted. Keep new covers in
the same style: one idea per project, centered, no text beyond a few glyphs.
"""

COVERS = {
    # magnifier over a page, with a check inside the lens
    "ai-visibility-checker": """
      <rect x="52" y="38" width="104" height="138" rx="10"/>
      <path d="M72 70h64M72 92h50M72 114h58M72 136h36"/>
      <circle cx="150" cy="146" r="36" class="fill"/>
      <path d="M176 172l30 30"/>
      <path d="M134 147l11 11 21-24"/>""",
    # a note with a ledger column and a clock
    "tally": """
      <rect x="46" y="40" width="148" height="160" rx="10"/>
      <path d="M150 40v160"/>
      <path d="M64 78h68M64 108h56M64 138h62M64 168h44"/>
      <path d="M162 78h16M162 108h12M162 138h16M162 168h10"/>
      <circle cx="186" cy="56" r="22" class="fill"/>
      <path d="M186 44v13l9 6"/>""",
    # a painter's palette with swatches and a type pairing
    "palette-generator": """
      <path d="M120 44c-46 0-80 32-80 72 0 38 30 70 66 70 14 0 18-8 18-16 0-12-10-14-10-26 0-10 8-16 20-16h22c26 0 44-16 44-38 0-26-34-46-80-46z"/>
      <circle cx="84" cy="104" r="10"/><circle cx="108" cy="76" r="10"/>
      <circle cx="144" cy="74" r="10"/><circle cx="172" cy="94" r="10"/>
      <text x="150" y="190" class="glyph">Aa</text>""",
    # keyboard keys with a checkered flag
    "typerace": """
      <rect x="36" y="112" width="168" height="82" rx="12"/>
      <path d="M56 136h14M82 136h14M108 136h14M134 136h14M160 136h24"/>
      <path d="M56 158h24M92 158h14M118 158h14M144 158h14M170 158h14"/>
      <path d="M78 178h84"/>
      <path d="M150 104V36"/>
      <path d="M150 38h46v34h-46"/>
      <path d="M150 50h12v11h12V50h11v11h11M162 61v11M185 61v11" class="thin"/>""",
    # a coffee cup beside a contact card
    "networking-tracker": """
      <path d="M44 104h70v52c0 18-14 30-35 30s-35-12-35-30z"/>
      <path d="M114 118h8c10 0 16 6 16 15s-6 15-16 15h-9"/>
      <path d="M64 92c0-8 8-8 8-16M86 92c0-8 8-8 8-16" class="thin"/>
      <rect x="132" y="52" width="76" height="56" rx="8" class="fill"/>
      <circle cx="152" cy="74" r="9"/>
      <path d="M144 96c2-8 14-8 16 0M170 70h26M170 84h18"/>""",
    # a browser window opened up into stacked layers
    "web-anatomy": """
      <rect x="40" y="44" width="160" height="152" rx="12"/>
      <path d="M40 72h160"/>
      <path d="M56 58h.1M70 58h.1M84 58h.1" class="dot"/>
      <path d="M72 96h96l-14 18H58z"/>
      <path d="M72 126h96l-14 18H58z"/>
      <path d="M72 156h96l-14 18H58z"/>""",
    # a microphone with sound waves and script lines
    "voiceprompter": """
      <rect x="96" y="40" width="48" height="90" rx="24"/>
      <path d="M78 110c0 26 18 42 42 42s42-16 42-42"/>
      <path d="M120 152v34M96 190h48"/>
      <path d="M178 82c8 10 8 26 0 36M194 70c14 18 14 42 0 60" class="thin"/>
      <path d="M34 74h40M34 94h32M34 114h38" class="thin"/>""",
    # a brief where every line carries a citation
    "parallel-prospect-brief": """
      <path d="M58 36h88l36 36v132H58z"/>
      <path d="M146 36v36h36"/>
      <path d="M76 96h64M76 124h56M76 152h62M76 180h40"/>
      <text x="146" y="101" class="glyph sm">[1]</text>
      <text x="138" y="129" class="glyph sm">[2]</text>
      <text x="144" y="157" class="glyph sm">[3]</text>""",
    # one prompt routed to small, medium and large models
    "smartmodel": """
      <circle cx="56" cy="120" r="20" class="fill"/>
      <path d="M76 120h34"/>
      <path d="M110 120c20 0 22-58 54-58M110 120h52M110 120c20 0 22 58 54 58"/>
      <circle cx="176" cy="62" r="9"/>
      <circle cx="180" cy="120" r="15"/>
      <circle cx="184" cy="178" r="22"/>""",
    # a fuel gauge reading how much context is left
    "token-fuel": """
      <path d="M40 160a80 80 0 0 1 160 0"/>
      <path d="M58 116l12 8M90 88l7 12M120 78v14M150 88l-7 12M182 116l-12 8" class="thin"/>
      <path d="M120 160l40-52"/>
      <circle cx="120" cy="160" r="9" class="fill"/>
      <text x="44" y="196" class="glyph">E</text>
      <text x="182" y="196" class="glyph">F</text>""",
    # code brackets under a reviewer's lens
    "code-improver": """
      <path d="M78 76l-38 40 38 40M162 76l38 40-38 40"/>
      <path d="M134 62l-28 108" class="thin"/>
      <circle cx="160" cy="166" r="26" class="fill"/>
      <path d="M179 185l22 22"/>
      <path d="M149 166l8 8 14-16"/>""",
    # many reviews narrowed down to one priority flag
    "spotify-review-triage": """
      <path d="M38 50h64v30H58l-10 10V80H38z"/>
      <path d="M38 104h64v30H58l-10 10v-10H38z"/>
      <path d="M38 158h64v30H58l-10 10v-10H38z"/>
      <path d="M50 65h40M50 119h40M50 173h40" class="thin"/>
      <path d="M108 66l46 46M108 120h46M108 174l46-46"/>
      <path d="M172 150V74"/>
      <path d="M172 76h32l-8 14 8 14h-32"/>""",
    # an open book answering a question, offline
    "personal-wiki": """
      <path d="M120 98c-20-12-48-14-74-8v100c26-6 54-4 74 8 20-12 48-14 74-8V90c-26-6-54-4-74 8z"/>
      <path d="M120 98v100"/>
      <path d="M64 120h38M64 140h38M138 120h38M138 140h38" class="thin"/>
      <path d="M150 34h52v34h-30l-12 12V68h-10z" class="fill"/>
      <text x="168" y="61" class="glyph sm">?</text>""",
    # a little chomper learning its way through a maze
    "pacman-dqn": """
      <path d="M36 44h168v152H36z" class="thin"/>
      <path d="M36 92h56M148 92h56M92 140h56M120 44v26M120 170v26" class="thin"/>
      <path d="M96 118l-26-17a32 32 0 1 0 0 34z" class="fill"/>
      <path d="M118 118h.1M142 118h.1M166 118h.1M190 118h.1" class="dot"/>""",
    # a tiny network that learns to write
    "custom-llm": """
      <circle cx="56" cy="64" r="11"/><circle cx="56" cy="112" r="11"/><circle cx="56" cy="160" r="11"/>
      <circle cx="120" cy="88" r="11"/><circle cx="120" cy="136" r="11"/>
      <circle cx="184" cy="112" r="13" class="fill"/>
      <path d="M67 64l42 22M67 112l42-22M67 112l42 22M67 160l42-22M67 64l42 70M67 160l42-70M131 88l40 20M131 136l40-20" class="thin"/>
      <text x="92" y="204" class="glyph">abc</text>""",
}

# products, mods and coursework each get one tint, so the shelf reads as a series
TINT = {"PRODUCTS": "sky", "MODS": "violet", "COURSEWORK": "mint"}

SKETCH_DEFS = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>'
               '<filter id="sketch" x="-5%" y="-5%" width="110%" height="110%">'
               '<feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="7" result="n"/>'
               '<feDisplacementMap in="SourceGraphic" in2="n" scale="3.2" xChannelSelector="R" yChannelSelector="G"/>'
               '</filter></defs></svg>')
