"""Gates for the translated mirror under `translations/`.

A translation drifts in silence. It is the one class of file where nobody who
can read the diff also reads the language, so the ordinary review that catches a
stale command everywhere else does not happen here. Both drifts this suite
covers have already happened in the sibling repository this pattern comes from:
a translated README carried a renamed skill and an out-of-date rule count while
CI stayed green.

What these assertions cover is the part that reaches a reader as a wrong
command, a broken path, or a missing section:

- a language that is missing a page, or carries one the English tree dropped
- a command block that drifted from the English original
- an identifier, path, or slash command that was translated when it should not
  have been, or dropped entirely
- a page nothing in its own language links to
- a diagram that lost its embed or its alt text on the way across

They do not check the prose. A translator still owns that, and no gate here
pretends otherwise.
"""

from __future__ import annotations

import collections
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import sync_docs  # noqa: E402

MIRROR = ROOT / sync_docs.MIRROR


def tracked_markdown() -> list[str]:
    out = subprocess.run(
        ["git", "ls-files", "*.md"], cwd=ROOT, capture_output=True, text=True, check=True
    )
    return [line for line in out.stdout.splitlines() if line]


INLINE_CODE = re.compile(r"`([^`]+)`")
IMG = re.compile(r"<img\s[^>]*>")
ALT = re.compile(r'alt="([^"]*)"')
SRC = re.compile(r'\b(?:src|srcset)="([^"]+)"')
DIAGRAM = re.compile(r"([a-z0-9-]+)-(?:light|dark)\.svg")

# A fence in one of these languages holds commands, paths, or settings that a
# user types or copies. Every language must carry it character for character,
# whatever the surrounding prose does.
VERBATIM_FENCES = frozenset({"bash", "json", "toml", "yaml", "text", ""})


LINK = re.compile(r"\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
FENCE = re.compile(r"^\s*(`{3,}|~{3,})")


def strip_fences(text: str) -> str:
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


def fenced_lines(text: str) -> list[str]:
    lines: list[str] = []
    inside = False
    language = ""
    for line in text.split("\n"):
        if line.startswith("```"):
            inside = not inside
            language = line[3:].strip() if inside else ""
            continue
        if inside and language in VERBATIM_FENCES and line.strip():
            lines.append(line.strip())
    return lines


def inline_code(text: str) -> collections.Counter:
    """Every inline code span, whitespace-normalized, fences excluded.

    Two decisions here, both learned from a page that shipped.

    The pattern allows a newline inside a span, because these files are
    hard-wrapped and `` `claude plugin\\nlist` `` is ordinary Markdown that
    renders as one identifier. A pattern that stopped at the line break did not
    merely miss that span: it paired the span's *closing* backtick with the
    *opening* backtick of the next one and captured the English prose between
    them. The census then held a phantom span that no translation could
    reproduce without leaving half a sentence untranslated, and lacked the two
    real identifiers it was supposed to be pinning. That is exactly how
    `docs/troubleshooting.md` behaved.

    Fences are stripped first because a newline-tolerant pattern would otherwise
    pair the backticks of a fence delimiter and swallow the block. Fence content
    is compared verbatim by its own test, so nothing is lost.
    """
    return collections.Counter(
        " ".join(span.split()) for span in INLINE_CODE.findall(strip_fences(text))
    )


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def pairs() -> list[tuple[str, str, str]]:
    """(language tag, English path, translated path) for every page."""
    return [
        (language.tag, relative, sync_docs.page_path(relative, language.tag))
        for relative in sync_docs.TRANSLATED
        for language in sync_docs.LANGUAGES
    ]


class Scope(unittest.TestCase):
    """Which files are translated is a decision, and it has to stay one."""

    def test_the_declared_languages_have_directories(self) -> None:
        self.assertTrue(sync_docs.LANGUAGES, "no languages declared")
        for language in sync_docs.LANGUAGES:
            with self.subTest(language=language.tag):
                self.assertTrue((MIRROR / language.tag).is_dir())
                self.assertTrue(language.label.strip(), "the nav needs a label")

    def test_every_tracked_page_is_translated_or_has_a_reason(self) -> None:
        """The gate that catches a new English page nobody translated.

        Counting the mirror cannot see this: four complete languages of the old
        page set look exactly like four complete languages.
        """
        unaccounted = []
        for relative in tracked_markdown():
            if relative.startswith(f"{sync_docs.MIRROR}/"):
                continue
            if relative in sync_docs.TRANSLATED:
                continue
            if any(relative.startswith(rule) for rule, _ in sync_docs.NOT_TRANSLATED):
                continue
            unaccounted.append(relative)
        self.assertEqual(
            unaccounted,
            [],
            "tracked page(s) neither in TRANSLATED nor matched by a rule in "
            "NOT_TRANSLATED. Add the page to one or the other in "
            "scripts/sync_docs.py; a page that is silently out of scope is a "
            "reader dropped into English with no warning.",
        )

    def test_every_exclusion_rule_still_matches_something(self) -> None:
        """A rule that stops matching is a rule nobody will notice is dead, and
        it makes the coverage test above look stricter than it is."""
        tracked = [f for f in tracked_markdown() if not f.startswith(f"{sync_docs.MIRROR}/")]
        for rule, reason in sync_docs.NOT_TRANSLATED:
            with self.subTest(rule=rule):
                self.assertTrue(
                    any(f.startswith(rule) for f in tracked),
                    f"{rule} matches no tracked file",
                )
                self.assertGreater(len(reason), 40, f"{rule} needs a real reason")

    def test_each_language_mirrors_the_page_set_exactly(self) -> None:
        """Both directions. A missing page strands a reader; an extra one is a
        page with no English original, which nothing else in this suite reads."""
        expected = set(sync_docs.TRANSLATED)
        for language in sync_docs.LANGUAGES:
            base = MIRROR / language.tag
            found = {
                path.relative_to(base).as_posix()
                for path in base.rglob("*.md")
            }
            with self.subTest(language=language.tag):
                self.assertEqual(
                    found,
                    expected,
                    f"missing: {sorted(expected - found)} / "
                    f"extra: {sorted(found - expected)}",
                )


class Parity(unittest.TestCase):
    def test_every_translation_carries_the_same_commands(self) -> None:
        for tag, english, translated in pairs():
            expected = fenced_lines(read(english))
            if not expected:
                continue
            with self.subTest(page=translated):
                self.assertEqual(
                    expected,
                    fenced_lines(read(translated)),
                    f"a command block drifted from {english}. Commands are "
                    f"copied, never translated.",
                )

    def test_the_fence_check_is_not_vacuous(self) -> None:
        """Most pages carry a fence. If none did, the test above would pass on
        an empty tree forever."""
        covered = [rel for rel in sync_docs.TRANSLATED if fenced_lines(read(rel))]
        self.assertGreaterEqual(len(covered), 5)

    def test_every_translation_names_the_same_code(self) -> None:
        """Slash commands, file names, and YAML keys are literals a user types.

        Compared as a multiset because word order inside a sentence belongs to
        the translator and a Chinese or Vietnamese sentence will not carry them
        in the English order. A dropped or renamed one is not the translator's.
        """
        for tag, english, translated in pairs():
            expected = inline_code(read(english))
            if not expected:
                continue
            with self.subTest(page=translated):
                found = inline_code(read(translated))
                self.assertEqual(
                    expected,
                    found,
                    f"against {english} — missing: {expected - found} / "
                    f"extra: {found - expected}",
                )


class Diagrams(unittest.TestCase):
    """Translated pages embed the English renders. Only the alt text moves."""

    def stems(self, text: str) -> collections.Counter:
        return collections.Counter(DIAGRAM.findall(text))

    def test_every_translation_embeds_the_same_diagrams(self) -> None:
        for tag, english, translated in pairs():
            expected = self.stems(read(english))
            if not expected:
                continue
            with self.subTest(page=translated):
                self.assertEqual(
                    expected,
                    self.stems(read(translated)),
                    f"the diagrams on {translated} do not match {english}. A "
                    f"<picture> that lost its dark source shows a light diagram "
                    f"on a dark page; a dropped one is invisible.",
                )

    def test_every_translated_diagram_keeps_real_alt_text(self) -> None:
        """The alt text is the only description a screen reader gets, and it is
        the one part of a <picture> block that can be left in English, or
        emptied, without anything looking wrong.

        The floor is a fraction of the English alt rather than a character count.
        A Chinese translation of a 600-character description runs to about half
        that, and a fixed floor tuned for Latin script would fail it for being
        correct.
        """
        for tag, english, translated in pairs():
            source = read(english)
            if not IMG.search(source):
                continue
            wanted = [ALT.search(img) for img in IMG.findall(source)]
            got = [ALT.search(img) for img in IMG.findall(read(translated))]
            with self.subTest(page=translated):
                self.assertEqual(
                    len(wanted), len(got), f"{translated} has a different number of images"
                )
                for index, (before, after) in enumerate(zip(wanted, got)):
                    self.assertIsNotNone(after, f"image {index}: no alt attribute")
                    self.assertGreaterEqual(
                        len(after.group(1)),
                        len(before.group(1)) * 0.25,
                        f"image {index}: alt text too short to be a translation "
                        f"of the English description",
                    )


class Reachability(unittest.TestCase):
    """Every translated docs page is within two hops of its own index.

    tests/test_docs.py asserts this for the English tree and cannot see the
    mirror, because it selects files by the `docs/` prefix. The same failure is
    worse here: a reader who reaches a language's index and finds no path to a
    page has no way to know the page exists, and the language nav will not help
    because it only ever points at the same page in another language.
    """

    def graph(self, tag: str) -> tuple[list[str], dict[str, list[str]]]:
        base = MIRROR / tag
        docs = sorted(
            path.relative_to(ROOT).as_posix()
            for path in (base / "docs").rglob("*.md")
        )
        known = set(docs)
        graph = {f: [] for f in docs}
        for relative in docs:
            text = strip_fences(read(relative))
            here = (ROOT / relative).parent
            for target in LINK.findall(text):
                clean = target.split("#")[0].split("?")[0]
                if not clean or clean.startswith("#") or "://" in clean:
                    continue
                resolved = (here / clean).resolve()
                if not resolved.is_relative_to(ROOT):
                    continue
                name = resolved.relative_to(ROOT).as_posix()
                if name in known:
                    graph[relative].append(name)
        return docs, graph

    def test_every_page_is_within_two_hops_of_its_language_index(self) -> None:
        for language in sync_docs.LANGUAGES:
            docs, graph = self.graph(language.tag)
            root = f"{sync_docs.MIRROR}/{language.tag}/docs/index.md"
            with self.subTest(language=language.tag):
                self.assertIn(root, docs)
                reached = {root, *graph[root]}
                for near in graph[root]:
                    reached.update(graph[near])
                self.assertEqual(
                    sorted(set(docs) - reached),
                    [],
                    f"page(s) more than two hops from {root}",
                )


class MarketNote(unittest.TestCase):
    """Every translated README states what market the pipeline models.

    It is generated rather than checked for presence, so this suite only has to
    hold the boundary: it belongs in the translated READMEs and nowhere else. It
    exists for the reader the English tree does not have — someone who found
    this in their own language and has no reason to assume it models a hiring
    market other than their own. See issue #2.
    """

    def test_every_language_has_a_note(self) -> None:
        self.assertEqual(
            set(sync_docs.MARKET_NOTE),
            {language.tag for language in sync_docs.LANGUAGES},
        )
        for tag, note in sync_docs.MARKET_NOTE.items():
            with self.subTest(language=tag):
                self.assertTrue(note.startswith(">"), "the note renders as a blockquote")
                self.assertIn("issues/2", note, "the note points at the tracking issue")

    def test_the_note_reaches_every_translated_readme(self) -> None:
        for language in sync_docs.LANGUAGES:
            target = sync_docs.page_path("README.md", language.tag)
            with self.subTest(language=language.tag):
                self.assertIn(sync_docs.MARKET_NOTE[language.tag], read(target))

    def test_no_english_page_carries_a_note(self) -> None:
        for relative in sync_docs.TRANSLATED:
            text = read(relative)
            for note in sync_docs.MARKET_NOTE.values():
                with self.subTest(page=relative):
                    self.assertNotIn(note, text)


class CountedNouns(unittest.TestCase):
    """The per-language noun tables the count sweep reads.

    scripts/sync_docs.py checks the numbers. This checks the table itself, which
    that pass cannot: a language whose nouns nobody registered produces no
    matches and therefore no errors, which reads exactly like a clean sweep.
    """

    def test_every_language_registers_nouns(self) -> None:
        self.assertEqual(
            set(sync_docs.TRANSLATED_COUNTED_NOUNS),
            {language.tag for language in sync_docs.LANGUAGES},
        )

    def test_every_noun_maps_to_a_real_total(self) -> None:
        known = {"skills", "dispatch", "shipped", "blind"}
        for tag, nouns in sync_docs.TRANSLATED_COUNTED_NOUNS.items():
            self.assertTrue(nouns, f"{tag} registers no counted nouns")
            for noun, totals in nouns.items():
                with self.subTest(language=tag, noun=noun):
                    self.assertTrue(totals)
                    self.assertLessEqual(set(totals), known)

    def test_every_language_covers_every_total(self) -> None:
        """A total no noun claims is a number that cannot be stated in that
        language without falling outside the sweep."""
        for tag, nouns in sync_docs.TRANSLATED_COUNTED_NOUNS.items():
            covered = {total for totals in nouns.values() for total in totals}
            with self.subTest(language=tag):
                self.assertEqual(covered, {"skills", "dispatch", "shipped", "blind"})


if __name__ == "__main__":
    unittest.main()
