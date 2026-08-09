#!/usr/bin/env python3
"""Cut the Chinese card's font down to the characters the Chinese card draws.

    python3 scripts/subset_cjk_font.py [path/to/NotoSansCJK-VF.ttc]

`.github/assets/hero-zh-CN.png` is the only thing in this repository set in Han
characters, and neither vendored family has one: Saira Condensed and IBM Plex
Mono cover Latin and stop. A full CJK face is twenty thousand glyphs and tens of
megabytes, which is not a reasonable thing to put in a repository so that one
picture can be drawn once. The card uses about a hundred and twenty characters,
and a subset of those is smaller than any of the fonts already here.

So this script instantiates Noto Sans CJK SC at the two weights the card sets,
subsets each to exactly the characters make_card.py's Chinese Card holds, and
writes them into assets/fonts/ beside the rest. The character list comes from
that Card rather than from a list kept here, because a list kept here would be a
second copy of the card's text that drifts the first time somebody rewrites a
line.

It also writes a coverage manifest next to the faces. make_card.py reads it and
refuses to draw a character the subset lacks, which is the part that matters: a
missing glyph is not an error at render time, it is a blank box in a picture
nobody looks at closely, and it ships.

The source font is not vendored. Pass a path, or let fontconfig find an
installed Noto Sans CJK. On a machine without one this script fails and
make_card.py keeps working from the committed faces -- the subset is a build
output that is committed, on the same terms as the diagrams' SVGs.

Needs fontTools. Like Pillow, it is a maintainer dependency and not a test one:
no gate runs this, and the committed faces are what anybody else reads.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTCollection, TTFont
from fontTools.varLib.instancer import instantiateVariableFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_card  # noqa: E402  -- the strings, read from where they are drawn
import sync_docs  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
FONTS = ROOT / "assets" / "fonts"

FAMILY = "Noto Sans CJK SC"
# The weight axis positions make_card's two CJK faces are cut from. Noto's
# Medium and Bold, named for the faces they stand in for.
WEIGHTS = {"Medium": 500, "Bold": 700}


def source_font(argument: str | None) -> Path:
    if argument:
        return Path(argument)
    found = subprocess.run(
        ["fc-match", "-f", "%{file}", FAMILY], capture_output=True, text=True
    )
    if found.returncode != 0 or not found.stdout:
        raise SystemExit(
            f"subset_cjk_font.py: no {FAMILY} on this machine and no path given. "
            f"Install it, or pass the path to a NotoSansCJK .ttc or .otf."
        )
    return Path(found.stdout.strip())


def face(path: Path) -> TTFont:
    """The SC face out of whatever was passed: a collection, or a single font."""
    if path.suffix.lower() in (".ttc", ".otc"):
        for font in TTCollection(path, lazy=False).fonts:
            if font["name"].getDebugName(1) == FAMILY:
                return font
        raise SystemExit(f"subset_cjk_font.py: {path} has no {FAMILY} face")
    return TTFont(path, lazy=False)


def rename(font: TTFont, weight: str) -> None:
    """Give the cut face its own family name.

    The subset is a hundred and nineteen characters wearing the name of a face
    that has twenty thousand. make_card.py loads it by path and would not care,
    but a file that lands in a font directory is matched by name, and this one
    would answer to `Noto Sans CJK SC` and then draw a box for every character
    the card does not use. Renaming it means the worst case is a font nothing
    finds. The copyright and licence records are left exactly as they came.
    """
    family = f"{FAMILY} Subset"
    for record in font["name"].names:
        if record.nameID == 1:
            record.string = family
        elif record.nameID == 2:
            record.string = weight
        elif record.nameID == 4:
            record.string = f"{family} {weight}"
        elif record.nameID == 6:
            record.string = f"{make_card.CJK_STEM}-{weight}"
    for extra in (16, 17):  # typographic family and subfamily, if the face has them
        font["name"].removeNames(nameID=extra)


def wanted() -> str:
    """Every character the Chinese card draws, from the card itself."""
    facts = sync_docs.Facts()
    card = make_card.CARDS["zh-CN"]
    numbers = {
        "n": len(facts.dispatch),
        "n_word": sync_docs.spell(len(facts.dispatch)),
        "N_WORD": sync_docs.spell(len(facts.dispatch)).upper(),
        "blind": len(facts.blind),
        "blind_word": sync_docs.spell(len(facts.blind)),
        "Blind_word": sync_docs.spell(len(facts.blind)).capitalize(),
    }
    strings = [
        card.eyebrow,
        card.keep_label,
        card.reviewers_label,
        *card.hook,
        *card.keep,
        *card.captions,
        *card.keep_note,
        *card.blind_note,
        *card.reviewers.values(),
    ]
    return "".join(sorted({c for s in strings for c in s.format(**numbers)}))


def main() -> None:
    source = source_font(sys.argv[1] if len(sys.argv) > 1 else None)
    characters = wanted()

    for name, weight in WEIGHTS.items():
        font = face(source)
        if "fvar" in font:
            font = instantiateVariableFont(font, {"wght": weight}, inplace=False)
        options = subset.Options(
            layout_features=[],       # no shaping features: the card sets no runs
            glyph_names=False,
            hinting=False,
            desubroutinize=True,
            drop_tables=["DSIG"],
            notdef_outline=True,      # so a character nobody caught draws a box
        )
        cut = subset.Subsetter(options=options)
        cut.populate(text=characters)
        cut.subset(font)
        rename(font, name)
        out = FONTS / f"{make_card.CJK_STEM}-{name}.ttf"
        font.flavor = None
        font.save(out)
        print(f"wrote {out.relative_to(ROOT)} "
              f"{out.stat().st_size // 1024}K, {len(characters)} characters")

    lines = "\n".join(f"U+{ord(c):04X} {c}" for c in characters)
    (FONTS / f"{make_card.CJK_STEM}.coverage.txt").write_text(
        f"# The characters {make_card.CJK_STEM}-*.ttf carry, one per line.\n"
        f"# Cut from {FAMILY} to the text of the zh-CN card in\n"
        f"# scripts/make_card.py. Regenerate both faces and this file with\n"
        f"# scripts/subset_cjk_font.py after changing a Chinese string there;\n"
        f"# make_card.py reads this and refuses to draw a character it lacks.\n"
        f"{lines}\n",
        encoding="utf-8",
    )
    print(f"wrote {(FONTS / f'{make_card.CJK_STEM}.coverage.txt').relative_to(ROOT)}")


if __name__ == "__main__":
    main()
