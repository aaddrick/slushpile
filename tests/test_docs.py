"""Gates for the `docs/` tree.

Documentation fails differently from code. It does not throw; it goes stale, or
it stops being reachable, and both are invisible in a diff because the diff only
shows the file somebody edited. Each test here corresponds to one of those:

- a relative link that resolves to nothing after a file moves
- a page nothing links to, which is a page nobody reads
- an `AGENTS.md` twin that drifted from the `CLAUDE.md` it mirrors
- prose that vanished during the extraction that created this tree
- a diagram source edited without re-rendering the SVG that is actually shipped
"""

from __future__ import annotations

import html
import json
import re
import subprocess
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIAGRAMS = ROOT / "docs" / "diagrams"


def tracked_markdown() -> list[str]:
    out = subprocess.run(
        ["git", "ls-files", "*.md"], cwd=ROOT, capture_output=True, text=True, check=True
    )
    return [line for line in out.stdout.splitlines() if line]


FENCE = re.compile(r"^\s*(`{3,}|~{3,})")


def strip_fences(text: str) -> str:
    """Blank out fenced code blocks, preserving line numbering.

    Without this, the illustrative `<picture>` snippet in the diagram guide —
    which uses the placeholder path `../diagrams/NAME-dark.svg` — reads as a
    real link this suite expects to resolve on disk.
    """
    out, fence = [], None
    for line in text.split("\n"):
        marker = FENCE.match(line)
        if marker:
            char = marker.group(1)[0]
            if fence is None:
                fence = char
            elif fence == char:
                fence = None
            out.append("")
            continue
        out.append("" if fence else line)
    return "\n".join(out)


LINK = re.compile(r"\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
ATTR = re.compile(r"\b(?:src|srcset)=\"([^\"]+)\"")
SCHEME = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")


def link_targets(relative: str) -> list[tuple[str, Path]]:
    """Every relative link in one file, as (raw target, resolved absolute path)."""
    path = ROOT / relative
    text = strip_fences(path.read_text(encoding="utf-8"))

    raw = [match.group(1) for match in LINK.finditer(text)]
    for match in ATTR.finditer(text):
        # srcset is a comma-separated list of "url descriptor" pairs. None of
        # this repo's carry a descriptor; handle it anyway.
        raw += [part.strip().split()[0] for part in match.group(1).split(",") if part.strip()]

    found = []
    for target in raw:
        if target.startswith("#") or SCHEME.match(target):
            continue
        clean = target.split("#")[0].split("?")[0]
        if clean:
            found.append((target, (path.parent / clean).resolve()))
    return found


class RelativeLinks(unittest.TestCase):
    def test_every_relative_link_resolves(self) -> None:
        """A moved file breaks links in files nobody edited, so nobody looks."""
        files = tracked_markdown()
        self.assertTrue(files, "git ls-files found no tracked markdown")

        broken = [
            f"{relative} -> {target}"
            for relative in files
            for target, resolved in link_targets(relative)
            if not resolved.exists()
        ]
        self.assertEqual(broken, [], "unresolved relative link(s)")


# The only files under docs/ allowed to sit outside two hops of docs/index.md.
# Each carries its own reason, and the set is asserted exactly, so growing the
# carve-out is a deliberate edit rather than a quiet one.
REACHABILITY_EXEMPT = {
    "docs/index.md": (
        "The traversal root itself. It is what hops are counted from, never a "
        "target that has to be reached."
    ),
    "docs/architecture/CLAUDE.md": (
        "Byte-identical twin of docs/architecture/AGENTS.md, kept so both agent "
        "filename conventions resolve to the same guidance. The architecture "
        "index links the AGENTS.md half; linking one twin is enough."
    ),
    "docs/diagrams/CLAUDE.md": (
        "Byte-identical twin of docs/diagrams/AGENTS.md, same reason. docs/index.md "
        "links the AGENTS.md half."
    ),
}


class Reachability(unittest.TestCase):
    def docs_graph(self) -> tuple[list[str], dict[str, list[str]]]:
        docs = [f for f in tracked_markdown() if f.startswith("docs/")]
        known = set(docs)
        graph = {f: [] for f in docs}
        for relative in docs:
            for _, resolved in link_targets(relative):
                if resolved.suffix != ".md":
                    continue
                target = resolved.relative_to(ROOT).as_posix()
                if target in known:
                    graph[relative].append(target)
        return docs, graph

    def test_every_docs_page_is_within_two_hops_of_the_index(self) -> None:
        """A page nothing links to is a page nobody reads, and the diff that
        added it looks exactly like the diff that added a linked one."""
        docs, graph = self.docs_graph()
        self.assertIn("docs/index.md", docs)

        reached = {"docs/index.md"}
        first = graph["docs/index.md"]
        reached.update(first)
        for near in first:
            reached.update(graph[near])

        unreached = sorted(set(docs) - reached - set(REACHABILITY_EXEMPT))
        self.assertEqual(unreached, [], "docs page(s) more than two hops from docs/index.md")

    def test_the_exemption_list_is_exactly_what_it_claims(self) -> None:
        self.assertEqual(
            set(REACHABILITY_EXEMPT),
            {"docs/index.md", "docs/architecture/CLAUDE.md", "docs/diagrams/CLAUDE.md"},
        )
        for path, reason in REACHABILITY_EXEMPT.items():
            with self.subTest(path=path):
                self.assertGreater(len(reason), 40, f"{path} needs a real reason")
                self.assertTrue((ROOT / path).exists(), f"{path} is exempt but does not exist")

    def test_both_agents_twins_are_reachable_rather_than_exempt(self) -> None:
        """The exemption covers the CLAUDE half of each pair only. If the
        AGENTS half were exempt too, the pair would be unreachable in a way the
        first test could not see."""
        _, graph = self.docs_graph()
        reached = {"docs/index.md"}
        first = graph["docs/index.md"]
        reached.update(first)
        for near in first:
            reached.update(graph[near])
        for twin in ("docs/architecture/AGENTS.md", "docs/diagrams/AGENTS.md"):
            with self.subTest(twin=twin):
                self.assertIn(twin, reached)
                self.assertNotIn(twin, REACHABILITY_EXEMPT)


class FreezePairs(unittest.TestCase):
    """A directory's AGENTS.md and CLAUDE.md must be byte-identical.

    Found by scanning rather than from a hardcoded list, so a future pair
    anywhere in the tree is covered without editing this file.
    """

    # The repository root is the one pair that is not byte-identical: AGENTS.md
    # there is generated from CLAUDE.md with a provenance header, and
    # `sync_docs.py --check` already covers it.
    EXEMPT_DIRS = {"."}

    def pairs(self) -> list[tuple[str, str]]:
        by_dir: dict[str, dict[str, str]] = {}
        for relative in tracked_markdown():
            path = Path(relative)
            if path.name not in ("AGENTS.md", "CLAUDE.md"):
                continue
            by_dir.setdefault(path.parent.as_posix(), {})[path.name] = relative
        return [
            (entry["AGENTS.md"], entry["CLAUDE.md"])
            for directory, entry in sorted(by_dir.items())
            if directory not in self.EXEMPT_DIRS and len(entry) == 2
        ]

    def test_the_scan_finds_the_pairs_that_exist(self) -> None:
        """A scan that matches nothing passes forever."""
        directories = {Path(agents).parent.as_posix() for agents, _ in self.pairs()}
        self.assertEqual(directories, {"docs/architecture", "docs/diagrams"})

    def test_each_pair_is_byte_identical(self) -> None:
        for agents, claude in self.pairs():
            with self.subTest(pair=agents):
                self.assertEqual(
                    (ROOT / agents).read_bytes(),
                    (ROOT / claude).read_bytes(),
                    f"{agents} has drifted from {claude}. Edit {claude} and run "
                    f"python3 scripts/sync_docs.py",
                )


HEADING = re.compile(r"^(#{1,2})\s+(.*?)\s*$")
CENSUS_FIXTURE = ROOT / "tests" / "fixtures" / "base-headings.json"


class HeadingCensus(unittest.TestCase):
    """Prose extracted into docs/ must have moved, not evaporated.

    The fixture records every level-1 and level-2 heading README.md and
    INSTALL.md carried before the extraction, with its count. Every one of them
    must still appear exactly that often across README.md, INSTALL.md, and
    docs/. A section quietly dropped mid-move fails here; a section that moved
    keeps its heading and passes.

    The baseline is a committed fixture rather than a `git show` at test time.
    A shallow CI checkout does not have that commit's blob, and any later
    history rewrite changes the sha.
    """

    def counts(self) -> Counter:
        files = ["README.md", "INSTALL.md"] + [
            f for f in tracked_markdown() if f.startswith("docs/")
        ]
        found: Counter = Counter()
        for relative in files:
            for line in (ROOT / relative).read_text(encoding="utf-8").split("\n"):
                match = HEADING.match(line)
                if match:
                    found[match.group(2)] += 1
        return found

    def test_the_fixture_describes_the_files_it_claims_to(self) -> None:
        fixture = json.loads(CENSUS_FIXTURE.read_text(encoding="utf-8"))
        self.assertEqual(fixture["files"], ["README.md", "INSTALL.md"])
        self.assertTrue(fixture["headings"], "the fixture records no headings")

    def test_every_base_heading_survived_the_extraction(self) -> None:
        fixture = json.loads(CENSUS_FIXTURE.read_text(encoding="utf-8"))
        found = self.counts()
        wrong = {
            heading: (expected, found[heading])
            for heading, expected in fixture["headings"].items()
            if found[heading] != expected
        }
        self.assertEqual(
            wrong,
            {},
            "heading: (expected, found) across README.md, INSTALL.md and docs/. "
            "A count of 0 means a section was dropped rather than moved; a count "
            "above the baseline means a new page reused a heading the census "
            "tracks, which makes the gate blind to that section going missing.",
        )

    def test_the_moved_sections_landed_where_they_were_meant_to(self) -> None:
        """The census proves a heading still exists somewhere. These three were
        moved on purpose, and where they landed is the reason the move happened."""
        for heading, target in (
            ("Requirements", "docs/getting-started.md"),
            ("What onboarding will ask you for", "docs/getting-started.md"),
            ("Troubleshooting", "docs/troubleshooting.md"),
        ):
            with self.subTest(heading=heading):
                text = (ROOT / target).read_text(encoding="utf-8")
                self.assertRegex(text, rf"(?m)^#{{1,2}} {re.escape(heading)}$")
                self.assertNotIn(
                    f"\n## {heading}\n", (ROOT / "INSTALL.md").read_text(encoding="utf-8")
                )


CLASSES_BLOCK = re.compile(r"^classes:\s*\{(.*)^\}", re.DOTALL | re.MULTILINE)
CLASS_NAME = re.compile(r"^  ([a-z][a-z0-9-]*):\s*\{", re.MULTILINE)
LEGEND_ROW = re.compile(r"^\|\s*`([a-z][a-z0-9-]*)`\s*\|", re.MULTILINE)
QUOTED = re.compile(r'"((?:[^"\\]|\\.)*)"')
VIEWBOX = re.compile(r'viewBox="0 0 (\d+) (\d+)"')

# GitHub's markdown column is about 1012px and the SVGs carry no width, so they
# scale to fit it. Past roughly 1300 natural width the 14px label text renders
# under 11px. The ceiling is set above the current maximum, not at it, so an
# ordinary edit does not have to be pixel-golfed.
MAX_NATURAL_WIDTH = 1280


def theme_classes(name: str) -> set[str]:
    block = CLASSES_BLOCK.search((DIAGRAMS / name).read_text(encoding="utf-8"))
    assert block, f"{name}: no classes block"
    return set(CLASS_NAME.findall(block.group(1)))


def diagram_bodies() -> list[Path]:
    return sorted(p for p in DIAGRAMS.glob("*.d2") if not p.name.startswith("theme-"))


def svg_text(path: Path) -> str:
    """Every rendered label in one SVG, unescaped and joined.

    d2 emits labels as native <text> elements with XML entities for quotes and
    apostrophes, so the raw file does not contain the source string.
    """
    raw = path.read_text(encoding="utf-8")
    return html.unescape(" ".join(re.findall(r"<text[^>]*>(.*?)</text>", raw, re.DOTALL)))


def label_lines(body: Path) -> list[str]:
    """Each `\\n`-separated segment of every quoted label in a `.d2` body."""
    source = "\n".join(
        line for line in body.read_text(encoding="utf-8").split("\n")
        if not line.lstrip().startswith("#")
    )
    lines = []
    for quoted in QUOTED.findall(source):
        lines += [segment.strip() for segment in quoted.split("\\n") if segment.strip()]
    return lines


class Diagrams(unittest.TestCase):
    def test_there_are_diagrams_to_check(self) -> None:
        self.assertTrue(diagram_bodies(), "docs/diagrams/ has no .d2 bodies")

    def test_every_body_has_both_renders_committed(self) -> None:
        """The SVGs are committed so a reader never needs d2 installed. A body
        with only one render breaks exactly one colour scheme."""
        for body in diagram_bodies():
            for mode in ("light", "dark"):
                with self.subTest(diagram=body.stem, mode=mode):
                    self.assertTrue((DIAGRAMS / f"{body.stem}-{mode}.svg").exists())

    def test_no_svg_uses_foreignobject(self) -> None:
        """A |md| label renders into <foreignObject>, which is HTML inside SVG.
        Support for it collapses when the SVG is loaded through an <img>, which
        is exactly how GitHub embeds these."""
        for svg in sorted(DIAGRAMS.glob("*.svg")):
            with self.subTest(svg=svg.name):
                self.assertNotIn("foreignObject", svg.read_text(encoding="utf-8"))

    def test_both_themes_define_the_same_classes(self) -> None:
        """A body referencing a class only one theme defines still compiles.
        That mode silently falls back to d2 defaults, and the only way to notice
        is to look at the render."""
        light, dark = theme_classes("theme-light.d2"), theme_classes("theme-dark.d2")
        self.assertTrue(light)
        self.assertEqual(light, dark)

    def test_the_legend_names_exactly_the_theme_classes(self) -> None:
        """The legend in pipeline.md and the theme files are a contract, and
        they drift silently: a new class renders fine with nothing explaining
        what its colour means."""
        legend = set(
            LEGEND_ROW.findall(
                (ROOT / "docs" / "architecture" / "pipeline.md").read_text(encoding="utf-8")
            )
        )
        self.assertEqual(legend, theme_classes("theme-light.d2"))

    def test_every_body_references_only_defined_classes(self) -> None:
        used = re.compile(r"class:\s*([a-z][a-z0-9-]*)")
        defined = theme_classes("theme-light.d2")
        for body in diagram_bodies():
            with self.subTest(diagram=body.stem):
                self.assertLessEqual(set(used.findall(body.read_text(encoding="utf-8"))), defined)

    def test_the_committed_svgs_match_their_sources(self) -> None:
        """The staleness gate. A `.d2` edited without re-running render.sh
        ships a picture of a pipeline that no longer exists, and the diff shows
        the edit rather than the stale render."""
        for body in diagram_bodies():
            lines = label_lines(body)
            self.assertTrue(lines, f"{body.name}: no labels found to check")
            for mode in ("light", "dark"):
                rendered = svg_text(DIAGRAMS / f"{body.stem}-{mode}.svg")
                missing = [line for line in lines if line not in rendered]
                with self.subTest(diagram=body.stem, mode=mode):
                    self.assertEqual(
                        missing,
                        [],
                        f"label text in {body.name} is absent from the committed "
                        f"{body.stem}-{mode}.svg. Run docs/diagrams/render.sh and "
                        f"commit both renders.",
                    )

    def test_every_diagram_stays_inside_the_width_budget(self) -> None:
        for svg in sorted(DIAGRAMS.glob("*.svg")):
            box = VIEWBOX.search(svg.read_text(encoding="utf-8"))
            with self.subTest(svg=svg.name):
                self.assertIsNotNone(box, "no viewBox, so the SVG will not scale")
                self.assertLessEqual(int(box.group(1)), MAX_NATURAL_WIDTH)

    def test_every_diagram_is_embedded_and_paired(self) -> None:
        """A rendered diagram nothing embeds is a file that is maintained and
        never seen. A <picture> missing its dark source shows the light diagram
        on a dark page."""
        page = (ROOT / "docs" / "architecture" / "pipeline.md").read_text(encoding="utf-8")
        for body in diagram_bodies():
            with self.subTest(diagram=body.stem):
                self.assertIn(f"../diagrams/{body.stem}-light.svg", page)
                self.assertIn(f"../diagrams/{body.stem}-dark.svg", page)

    def test_every_embedded_diagram_has_alt_text(self) -> None:
        """The alt text is the only description a screen reader gets, and it is
        the part of a <picture> block that drifts without breaking anything."""
        for relative in [f for f in tracked_markdown() if f.startswith("docs/")]:
            text = strip_fences((ROOT / relative).read_text(encoding="utf-8"))
            for img in re.findall(r"<img\s[^>]*>", text):
                with self.subTest(file=relative):
                    alt = re.search(r'alt="([^"]*)"', img)
                    self.assertIsNotNone(alt, f"{relative}: <img> with no alt attribute")
                    self.assertGreater(
                        len(alt.group(1)), 60, f"{relative}: alt text too short to describe a diagram"
                    )


if __name__ == "__main__":
    unittest.main()
