#!/usr/bin/env python3
"""Draw the two cards under .github/assets/.

`hero.png` is the image at the top of README.md: the loop in three columns. The
wordmark and the hook on the left, the files the workspace keeps in the middle,
the seven reviewers on the right. Read left to right it says: here is the claim,
here is what the system holds onto, here is what attacks it. The middle column
is the argument -- every other tool in this category would have an empty one.

`social.png` is the file uploaded at Settings -> General -> Social preview, and
it is what LinkedIn, Signal, Teams, and Slack actually render when someone pastes
the repository link. It carries the wordmark and the hook and nothing else.

The two exist separately because they are read at different sizes and the same
image cannot serve both. An unfurl renders around 400px wide. At that size the
hero's columns collapse into grey texture, and every earlier attempt to fix that
meant deleting detail the README wants. Splitting them ends the argument: the
hero is free to be dense because nobody sees it at 400px, and the social card is
free to be nearly empty because nobody sees it at 1280.

The right column's agents and the bar that groups the blind ones are read from
the review's dispatch table through sync_docs, not typed here. That column is a
diagram of the pipeline's shape, and a diagram of a shape the pipeline no longer
has is worse than no diagram. The middle column's file list is still typed here,
because it names what onboarding writes rather than anything the tree declares --
so each name is checked against the onboard skill before the card is drawn.

Run after any change to the header text, the file list, or the agent list:

    python3 scripts/make_card.py

Both cards are 1280x640, which is GitHub's social preview size and a clean 2:1.
Anything taller loses its top and bottom edge in a preview.

Needs Pillow. It is not a test dependency, so CI does not run this and no gate
checks the committed PNGs against a fresh render. Pillow encodes the same pixels
differently across versions, so a checksum gate would fail on an unrelated
upgrade. Regenerate by hand and commit the result.

Fonts live in assets/fonts/. Both families are OFL; the licenses sit beside
them.
"""

import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sync_docs  # noqa: E402  -- the dispatch order, read from where it is true

ROOT = Path(__file__).resolve().parents[1]
FONTS = ROOT / "assets" / "fonts"
DEFAULT_DIR = ROOT / ".github" / "assets"

S = 2                      # supersample factor, resized down at the end
W, H = 1280 * S, 640 * S   # GitHub's social preview size, and a clean 2:1 unfurl

# --- palette ---------------------------------------------------------------
# GitHub's dark canvas, so the card sits flush with the README behind it.
CANVAS   = (0x0D, 0x11, 0x17)
RULE     = (0x21, 0x26, 0x2D)
INK      = (0xE6, 0xED, 0xF3)
INK_MUTE = (0x7D, 0x85, 0x90)
INK_BODY = (0xA8, 0xB2, 0xBF)
BLUE     = (0x53, 0x9B, 0xF5)   # the accent: what the card exists to add
BLUE_DIM = (0x31, 0x5C, 0x94)
AMBER    = (0xC6, 0x90, 0x26)


def disp(size, weight="Bold"):
    return ImageFont.truetype(str(FONTS / f"SairaCondensed-{weight}.ttf"), int(size * S))


def mono(size, weight="Regular"):
    return ImageFont.truetype(str(FONTS / f"IBMPlexMono-{weight}.ttf"), int(size * S))


def new_card():
    """A dark canvas with the faint dot grid both cards share."""
    img = Image.new("RGB", (W, H), CANVAS)
    d = ImageDraw.Draw(img)
    for gy in range(0, H, 24 * S):
        for gx in range(0, W, 24 * S):
            d.point((gx, gy), fill=(0x16, 0x1B, 0x22))
    return img, d


def tracked(draw, xy, text, font, fill, track=0):
    """Draw text with letter spacing. Returns the end x."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + track * S
    return x


def tracked_len(draw, text, font, track=0):
    return sum(draw.textlength(c, font=font) + track * S for c in text)


PAD = 72 * S
# The hook, in one place. Both cards draw these exact strings, so the social
# preview cannot drift from the README subtitle without the hero drifting too.
EYEBROW = "AN ADVERSARIAL JOB SEARCH WITH A MEMORY"
HOOK = ("Seven agents try to reject you", "before a recruiter gets the chance.")
KEEP = "What they find, you keep."

URL = "github.com/aaddrick/slushpile"

# Drawn as separate runs so the second half carries the accent. Kept here rather
# than inline in each card, because a wordmark that differs between the README
# image and the link preview looks like two different projects.
WORDMARK = (("slush", INK), ("pile", BLUE))

# Workspace files onboarding writes that the middle column leaves out, with the
# reason. Four rows is what fits above the caption at this type size, so the
# omission is a layout decision — recorded here so it reads as one, rather than
# as a file nobody noticed. The guard in draw_hero refuses to draw when a fifth
# file appears in the workspace and lands in neither list.
OMITTED = {
    "companies.md": "one line per company ever looked at — the least "
                    "load-bearing of the five, and the column holds four",
}

# Onboarding's Phase 6 scaffold block, and the workspace files inside it.
SCAFFOLD_BLOCK = re.compile(r"Create the directory structure:\s*```(.*?)```", re.DOTALL)
WORKSPACE_FILE = re.compile(r"^([\w.-]+\.(?:md|yaml))", re.MULTILINE)


def draw_wordmark(d, x, y, font):
    for part, colour in WORDMARK:
        d.text((x, y), part, font=font, fill=colour)
        x += d.textlength(part, font=font)


def centred(draw, y, text, font, fill):
    draw.text(((W - draw.textlength(text, font=font)) / 2, y), text, font=font, fill=fill)


def draw_hero(d):
    """README.md's header image: the loop in three columns."""
    COL_M, COL_R = 580 * S, 902 * S     # middle and right column left edges
    LABEL_Y, LIST_Y, NOTE_Y = 52 * S, 104 * S, 448 * S

    label_font = disp(20, "SemiBold")
    note_font = disp(20, "Medium")

    # Two hairlines carry the three-column structure. Without them the middle and
    # right lists read as one ragged block of grey text.
    for x in (540 * S, 862 * S):
        d.rectangle([x, 44 * S, x + 1, 524 * S], fill=RULE)

    # --- left: the wordmark and the hook, verbatim from README.md --------------
    tracked(d, (PAD, LABEL_Y), EYEBROW, label_font, INK_MUTE, track=2.5)

    # Sized to clear the x=540 hairline: nine mono characters at 80px is 432px
    # from a 72px margin, which leaves the column its gutter.
    draw_wordmark(d, PAD, 104 * S, mono(80, "Medium"))

    # The third line is the one the card exists to add, so it carries the accent.
    # In body colour it reads as a trailing clause and gets skipped at small sizes.
    tag = disp(36, "Medium")
    d.text((PAD, 272 * S), HOOK[0], font=tag, fill=INK_BODY)
    d.text((PAD, 312 * S), HOOK[1], font=tag, fill=INK_BODY)
    d.text((PAD, 352 * S), KEEP, font=tag, fill=BLUE)

    # ===========================================================================
    # Middle: the durable workspace. These are the files onboard writes and every
    # later skill reads. Adding a file to the workspace without adding it here
    # leaves the card quietly wrong.
    # ===========================================================================
    tracked(d, (COL_M, LABEL_Y), "WHAT YOU KEEP", label_font, INK_MUTE, track=2.5)

    FILES = [
        ("profile.md",       "every factual claim"),
        ("preferences.yaml", "comp, location, constraints"),
        ("stories.md",       "four to eight, tellable"),
        ("job_search.md",    "outcomes, for calibration"),
    ]

    # A file the card claims the workspace keeps, that onboarding never writes,
    # is the card being wrong about the one thing it exists to claim.
    onboard = (ROOT / "skills" / "onboard" / "SKILL.md").read_text(encoding="utf-8")
    unwritten = [name for name, _ in FILES if name not in onboard]
    if unwritten:
        raise SystemExit(
            f"make_card.py: the workspace column names {', '.join(unwritten)}, "
            f"which skills/onboard/SKILL.md never writes"
        )

    # And the other direction, which is the one that was open. The check above
    # catches a deleted file; it cannot catch a file added to the workspace and
    # never added here, which leaves the column quietly short on the one claim
    # the card exists to make.
    block = SCAFFOLD_BLOCK.search(onboard)
    if not block:
        raise SystemExit(
            "make_card.py: skills/onboard/SKILL.md no longer has the scaffold "
            "block this column is checked against. Restore it, or point "
            "SCAFFOLD_BLOCK at wherever the workspace file list moved."
        )
    unaccounted = sorted(
        set(WORKSPACE_FILE.findall(block.group(1)))
        - {name for name, _ in FILES}
        - set(OMITTED)
    )
    if unaccounted:
        raise SystemExit(
            f"make_card.py: onboarding writes {', '.join(unaccounted)}, which the "
            f"workspace column neither shows nor records as a deliberate "
            f"omission. Add it to FILES, or to OMITTED with the reason."
        )

    file_font, caption_font = mono(22, "Medium"), disp(21, "Medium")
    for i, (name, caption) in enumerate(FILES):
        y = LIST_Y + i * 72 * S
        d.rectangle([COL_M, y + 4 * S, COL_M + 3 * S, y + 24 * S], fill=BLUE_DIM)
        d.text((COL_M + 16 * S, y), name, font=file_font, fill=INK)
        d.text((COL_M + 16 * S, y + 32 * S), caption, font=caption_font, fill=INK_MUTE)

    d.text((COL_M, NOTE_Y), "Written once. Read by every", font=note_font, fill=INK_MUTE)
    d.text((COL_M, NOTE_Y + 26 * S), "stage. Updated by every review.", font=note_font, fill=INK_MUTE)

    # ===========================================================================
    # Right: the seven, in dispatch order. The bracket is the architecture -- the
    # first five run concurrently and cannot see each other's findings, which is
    # the whole reason their agreement counts as evidence.
    # ===========================================================================
    facts = sync_docs.Facts()
    AGENTS = [sync_docs.plain(name) for name in facts.dispatch]
    blind = len(facts.blind)  # 1..blind run concurrently; then synthesis, then falsification

    heading = f"THE {sync_docs.spell(len(AGENTS)).upper()} REVIEWERS"
    tracked(d, (COL_R, LABEL_Y), heading, label_font, INK_MUTE, track=2.5)

    agent_font = mono(20, "Medium")
    rows = [LIST_Y + i * 48 * S for i in range(len(AGENTS))]
    for y, name in zip(rows, AGENTS):
        d.text((COL_R + 16 * S, y), name, font=agent_font, fill=INK_BODY)

    # One bar spanning the parallel stages, then a bar each for the two that run
    # alone. The grouping is the claim; the colour change marks the new job.
    d.rectangle([COL_R, rows[0] + 4 * S, COL_R + 3 * S, rows[blind - 1] + 24 * S], fill=BLUE_DIM)
    d.rectangle([COL_R, rows[blind] + 4 * S, COL_R + 3 * S, rows[blind] + 24 * S], fill=AMBER)
    d.rectangle(
        [COL_R, rows[blind + 1] + 4 * S, COL_R + 3 * S, rows[blind + 1] + 24 * S], fill=BLUE
    )

    note = f"{sync_docs.spell(blind).capitalize()} in parallel, blind to each"
    d.text((COL_R, NOTE_Y), note, font=note_font, fill=INK_MUTE)
    d.text((COL_R, NOTE_Y + 26 * S), "other. Then synthesis. Then an", font=note_font, fill=INK_MUTE)
    d.text((COL_R, NOTE_Y + 52 * S), "agent whose job is overturning it.", font=note_font, fill=INK_MUTE)

    # --- footer ----------------------------------------------------------------
    # The hairline is load-bearing. Without it the URL reads as a fifth line of the
    # left column rather than as the card's footer.
    d.rectangle([PAD, 562 * S, W - PAD, 562 * S + 1], fill=RULE)

    # Both lines sit on one baseline. The two faces have different ascents, so a
    # shared top edge would leave them visibly off by a few pixels.
    BASE = H - 44 * S
    url_font = mono(23, "Medium")
    d.text((PAD, BASE - url_font.getmetrics()[0]), URL, font=url_font, fill=INK_MUTE)
    harnesses = "CLAUDE CODE  ·  CODEX  ·  CURSOR  ·  GEMINI CLI"
    hf = disp(21, "SemiBold")
    tracked(d, (W - PAD - tracked_len(d, harnesses, hf, track=2.5), BASE - hf.getmetrics()[0]),
            harnesses, hf, (0x6E, 0x73, 0x7B), track=2.5)

def draw_social(d):
    """The unfurl card. Read at ~400px wide, so it holds the hook and nothing else.

    Everything here is set two to three times larger than the same text on the
    hero. A 42px line survives the scale down to roughly 13px; the hero's 20px
    list items would land at 6px, which is why none of them are here.
    """
    eyebrow = disp(26, "SemiBold")
    tracked(d, ((W - tracked_len(d, EYEBROW, eyebrow, track=4)) / 2, 138 * S),
            EYEBROW, eyebrow, INK_MUTE, track=4)

    # Centred, so the whole wordmark is measured before it is placed.
    wordmark = mono(124, "Medium")
    total = sum(d.textlength(p, font=wordmark) for p, _ in WORDMARK)
    draw_wordmark(d, (W - total) / 2, 190 * S, wordmark)

    tag = disp(42, "Medium")
    centred(d, 396 * S, HOOK[0], tag, INK_BODY)
    centred(d, 444 * S, HOOK[1], tag, INK_BODY)
    centred(d, 492 * S, KEEP, tag, BLUE)

    centred(d, 570 * S, URL, mono(21, "Medium"), (0x5C, 0x63, 0x6D))


CARDS = {"hero.png": draw_hero, "social.png": draw_social}


def main():
    out_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_DIR
    for name, draw in CARDS.items():
        img, d = new_card()
        draw(d)
        out = img.resize((W // S, H // S), Image.LANCZOS)
        out.save(out_dir / name, optimize=True)
        print(f"wrote {out_dir / name} {out.size[0]}x{out.size[1]}")


if __name__ == "__main__":
    main()
