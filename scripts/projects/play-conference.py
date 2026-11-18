from casekit import artifact_grid, bullets, cover, paras

ASSETS = "/assets/img/play-conference"

PROJECT = dict(
    slug="play-conference",
    title="PLAY 2027",
    kicker="conference design · Berkeley Haas",
    heading="Building the visual identity for PLAY 2027.",
    desc="The poster, motion and brand system for Berkeley Haas DMEC’s PLAY Conference.",
    tldr="Poster, motion and a design system for Berkeley Haas’s conference on music, film and games.",
    role="Campaign and event design",
    team="Berkeley Haas Digital Media & Entertainment Club",
    timeline="February 27, 2027 · Clark Kerr Campus, UC Berkeley",
    cover=cover(
        f"{ASSETS}/poster-v1.jpg",
        "Black and violet PLAY 2027 poster with a glowing play triangle and the prompt To Create Is To.",
        1152, 1440,
    ),
    cover_class="case-cover--contain",
    problem=paras(
        "PLAY brings together people who make things across music, film and games. "
        "The identity had to work across a social feed, a printed flyer and a conference stage."
    ),
    did=bullets(
        "Built the Press Play campaign around a violet acrylic play triangle, with a flat version for simple print layouts.",
        "Turned the line <strong>To Create Is To _____</strong> into a prompt people can finish on a write-in card.",
        "Carried the identity across social and print formats and into reusable templates for slides, name tags and wayfinding.",
    ),
    milestones=paras(
        "PLAY 2027 is scheduled for February 27 in the Garden Room at Clark Kerr Campus. "
        "The campaign and event materials are in development."
    ),
    results="",
    artifacts=artifact_grid(
        (f"{ASSETS}/save-the-date-v1.jpg", "Save the date for the Garden Room"),
        (f"{ASSETS}/write-in-card-v1.jpg", "Write-in card with the campaign prompt"),
        (f"{ASSETS}/slide-system-v1.jpg", "Slide templates for talks, panels and transitions"),
    ) + "\n" + paras(f'<a href="{ASSETS}/motion-preview-v1.gif">Watch the animated poster (GIF)</a>'),
    glyph="product",
)
