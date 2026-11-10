"""Hand-drawn 16x16 favicon grids, one per mark. Data only; build-fav16.py renders them.

Each grid is drawn pixel by pixel, not shrunk from the 64-unit art, so the shapes stay sharp at 16px.
Only rows 2 to 13 carry the glyph (rows 0, 1, 14 and 15 are the tile's rounded caps, added by the renderer).
A row left out is plain tile. Every row is exactly 16 characters.

Legend (shared):
  .  clear            B  tile (the 3-stop gradient, sampled per row)
  k  ink              d  ink 45%      e  ink 22%      n  ink 60%
  w  white            h  white 55% (soft edge)         p  paper #f8f8f6
Per-mark colors for the multicolor dark tiles are in EXTRA.
"""

TOP = ["..BBBBBBBBBBBB..", ".BBBBBBBBBBBBBB."]
BOTTOM = [".BBBBBBBBBBBBBB.", "..BBBBBBBBBBBB.."]

# The three dark tiles carry their own glyph colors.
EXTRA = {
    "palette-generator": {"r": "#ff3b30", "o": "#ff6a00", "y": "#ffd60a", "g": "#30d158", "b": "#0a84ff"},
    "web-anatomy": {"v": "#7c5cff", "o": "#ff6a00", "g": "#30d158"},
    "arcade": {"g": "#30d158", "G": "#98e8ac", "y": "#ffd60a"},
}

GRIDS = {
    # four ink bars, one white slash cut through them in even two-pixel steps
    "tally": {
        3: "BBBBkBkBkBkBBBBB", 4: "BBBBkBkBkBkBBBBB", 5: "BBBBkBkBkBkBwwBB",
        6: "BBBBkBkBkBwwBBBB", 7: "BBBBkBkBwwkBBBBB", 8: "BBBBkBwwkBkBBBBB",
        9: "BBBBwwkBkBkBBBBB", 10: "BBwwkBkBkBkBBBBB", 11: "BBBBkBkBkBkBBBBB", 12: "BBBBkBkBkBkBBBBB",
    },
    # two faint lines, one ink line, a white caret
    "typerace": {
        5: "BBBBBBBBBBwwBBBB", 6: "BBBdddddBBwwBBBB", 7: "BBBBBBBBBBwwBBBB",
        8: "BBBBkkkkkBwwBBBB", 9: "BBBBBBBBBBwwBBBB", 10: "BBBddddBBBwwBBBB",
    },
    # half-ring gauge: white arc filled, faint track, needle and hub
    "token-fuel": {
        5: "BBBBBBwwwwBBBBBB", 6: "BBBBBwwwwweBBBBB", 7: "BBBBwwBBBBeeBBBB", 8: "BBBwwBBBBkBeeBBB",
        9: "BBBwBBBBkBBBeBBB", 10: "BBBwBBBkkBBBeBBB", 11: "BBBBBBBkkBBBBBBB",
    },
    # a round white hub, four ink nodes, one spoke each
    "personal-wiki": {
        3: "BBBkkBBBBBBkkBBB", 4: "BBBkkBBBBBBkkBBB", 5: "BBBBBdBBBBdBBBBB",
        6: "BBBBBBhwwhBBBBBB", 7: "BBBBBBwwwwBBBBBB", 8: "BBBBBBwwwwBBBBBB", 9: "BBBBBBhwwhdBBBBB",
        10: "BBBBBdBBBBBkkBBB", 11: "BBBkkBBBBBBkkBBB", 12: "BBBkkBBBBBBBBBBB",
    },
    # a magnifier: 2px ring, 2px lens dot, diagonal handle
    "ai-visibility-checker": {
        3: "BBBBBwwwwBBBBBBB", 4: "BBBBwwwwwwBBBBBB", 5: "BBBwwBBBBwwBBBBB", 6: "BBBwwBwwBwwBBBBB",
        7: "BBBwwBwwBwwBBBBB", 8: "BBBwwBBBBwwBBBBB", 9: "BBBBwwwwwwBBBBBB",
        10: "BBBBBwwwwBwwBBBB", 11: "BBBBBBBBBBBwwBBB", 12: "BBBBBBBBBBBBwwBB",
    },
    # two ring nodes joined by a bridge, a white padlock under them
    "networking-tracker": {
        4: "BBBBkkBBBBkkBBBB", 5: "BBBkBBkddkBBkBBB", 6: "BBBkBBkBBkBBkBBB", 7: "BBBBkkBBBBkkBBBB",
        8: "BBBBBBBwwBBBBBBB", 9: "BBBBBBwBBwBBBBBB", 10: "BBBBBBwwwwBBBBBB", 11: "BBBBBBwwwwBBBBBB", 12: "BBBBBBwwwwBBBBBB",
    },
    # sound bars on the left, three prompt lines on the right with the live one white
    "voiceprompter": {
        5: "BBBBBwBBBBBBBBBB", 6: "BBBBBwBwBddddBBB", 7: "BBBwBwBwBBBBBBBB", 8: "BBBwBwBwBwwwBBBB",
        9: "BBBBBwBwBBBBBBBB", 10: "BBBBBwBBBddddBBB",
    },
    # paper page: three ink lines, amber dots and an amber bar in the tile color
    "parallel-prospect-brief": {
        3: "BBBBBppppppBBBBB", 4: "BBBBppppppppBBBB", 5: "BBBBpkkkkpBpBBBB", 6: "BBBBppppppppBBBB",
        7: "BBBBpkkkpBppBBBB", 8: "BBBBppppppppBBBB", 9: "BBBBpkkkkpBpBBBB", 10: "BBBBppppppppBBBB",
        11: "BBBBpBBBBBBpBBBB", 12: "BBBBBppppppBBBBB",
    },
    # two rows of faint dots falling into an ink funnel, one white dot out
    "spotify-review-triage": {
        3: "BBBBdBdBdBdBdBBB", 5: "BBBBBdBdBdBdBBBB",
        6: "BBBkkkkkkkkkkBBB", 7: "BBBBkeeeeeekBBBB", 8: "BBBBBkeeeekBBBBB", 9: "BBBBBBkeekBBBBBB",
        10: "BBBBBBBkkBBBBBBB", 12: "BBBBBBBwwBBBBBBB", 13: "BBBBBBBwwBBBBBBB",
    },
    # one white route climbing to a white node; three faint routes to dark nodes
    "smartmodel": {
        3: "BBBnnBwwBnnBnnBB", 4: "BBBnnBwwBnnBnnBB", 5: "BBBBdBBwBdBBdBBB", 6: "BBBBdBBwBdBBdBBB",
        7: "BBBBdBBwBdBBdBBB", 8: "BBBBBdBwBdBdBBBB", 9: "BBBBBBddwddBBBBB",
        10: "BBBBBBBBwBBBBBBB", 11: "BBBBBBBBwBBBBBBB", 12: "BBBBBBBBwBBBBBBB", 13: "BBBBBBBBwBBBBBBB",
    },
    # ink angle brackets with a white check between them
    "code-improver": {
        5: "BBBBBkBBBBkBBBBB", 6: "BBBBkBBBBBBkBBBB", 7: "BBBkBBBBBwBBkBBB", 8: "BBBkBBwBwBBBkBBB",
        9: "BBBBkBBwBBBkBBBB", 10: "BBBBBkBBBBkBBBBB",
    },
    # a faint progress bar (white part done), a checked line, a play line, a faded line
    "task-progress": {
        3: "BBBwwwwwwweeeBBB", 4: "BBBwwwwwwweeeBBB",
        7: "BBBBBBkBBBBBBBBB", 8: "BBBkBkBBkkkkkBBB", 9: "BBBBkBBBBBBBBBBB",
        11: "BBBBkBBBkkkkBBBB", 13: "BBBBdBBBddddBBBB",
    },
    # a stepped paper block with an ink check on its top step
    "product-blueprint": {
        4: "BBBBBBBBpppppBBB", 5: "BBBBBBBBppppkBBB", 6: "BBBBBBBBpkpkpBBB",
        7: "BBBBBBppppkppBBB", 8: "BBBBBBpdpppppBBB", 9: "BBBBBBpppppppBBB",
        10: "BBBppppppppppBBB", 11: "BBBpdppppppppBBB", 12: "BBBppppppppppBBB",
    },
    # axes, a white loss curve falling to a flat line, an end dot
    "custom-llm": {
        3: "BBBdBBBBBBBBBBBB", 4: "BBBdBwBBBBBBBBBB", 5: "BBBdBwBBBBBBBBBB", 6: "BBBdBwBBBBBBBBBB",
        7: "BBBdBBwBBBBBBBBB", 8: "BBBdBBwBBBBBBBBB", 9: "BBBdBBBwBBBBBBBB",
        10: "BBBdBBBBwwwwwBBB", 11: "BBBdBBBBBBBwwBBB", 12: "BBBddddddddddBBB",
    },
    # a faint maze, a white agent, three ink pellets
    "pacman-dqn": {
        2: "BBeeeeeeeeeeeeBB", 3: "BBeBBBBBBBBBBeBB", 4: "BBeBBBBBBBBBBeBB", 5: "BBeBBeeeeeeBBeBB",
        6: "BBeBBBBBBBBBBeBB", 7: "BBeBwwwBBBBBBeBB", 8: "BBeBwwwBkBkBkeBB", 9: "BBeBwwwBBBBBBeBB",
        10: "BBeBBeeeeeeBBeBB", 11: "BBeBBBBBBBBBBeBB", 12: "BBeBBBBBBBBBBeBB", 13: "BBeeeeeeeeeeeeBB",
    },
    # a faint video frame, an ink arrow, a white check box: watching handed off to doing
    "relay": {
        5: "BBBBBBBBBwwwwwwB", 6: "BdddBBkBBwwwwwwB", 7: "BdddkkkkBwwwwkwB",
        8: "BdddkkkkBwkwkwwB", 9: "BdddBBkBBwwkwwwB", 10: "BBBBBBBBBwwwwwwB",
    },
    # a paper price tag with an ink check and a hole in the tile color
    "review-labeler": {
        5: "BBBpppppppBBBBBB", 6: "BBBppppppppBBBBB", 7: "BBBpppppkpppBBBB", 8: "BBBppkpkppBppBBB",
        9: "BBBpppkpppppBBBB", 10: "BBBppppppppBBBBB", 11: "BBBpppppppBBBBBB",
    },
    # a paper page, three ink lines, and a clock with its hands
    "timely": {
        3: "BBBppppppppBBBBB", 4: "BBBppppppppBBBBB", 5: "BBBppkkkkppBBBBB", 6: "BBBppppppppBBBBB",
        7: "BBBppkkkpppBBBBB", 8: "BBBppppppkkkkBBB", 9: "BBBpppppkpkppkBB", 10: "BBBpppppkpkkpkBB",
        11: "BBBpppppkppppkBB", 12: "BBBpppppkppppkBB", 13: "BBBBBBBBBkkkkBBB",
    },
    # five rods fanned from one pivot: red, orange, yellow, green, blue
    "palette-generator": {
        4: "BBBBBBByyBBBBBBB", 5: "BBBrrooyyggbbBBB", 6: "BBBrrooyyggbbBBB", 7: "BBBBrrooygbbBBBB",
        8: "BBBBBrroygbBBBBB", 9: "BBBBBrroygbBBBBB", 10: "BBBBBBroygBBBBBB", 11: "BBBBBBBppBBBBBBB",
    },
    # three stacked bars: violet, orange, green
    "web-anatomy": {
        4: "BBBvvvvvvvvvvBBB", 5: "BBBvvvvvvvvvvBBB", 7: "BBBooooooooooBBB", 8: "BBBooooooooooBBB",
        10: "BBBggggggggggBBB", 11: "BBBggggggggggBBB",
    },
    # a snake in an L: body, light head, a yellow bite ahead
    "arcade": {
        5: "BBBBBBggggGGByBB", 6: "BBBBBBggggGGByBB", 7: "BBBBBBggBBBBBBBB", 8: "BBBBBBggBBBBBBBB",
        9: "BBggggggBBBBBBBB", 10: "BBggggggBBBBBBBB",
    },
}
