"""The personal-data gate is only worth having if it catches things.

A scanner nobody has ever seen fail is indistinguishable from a scanner whose
patterns no longer match anything, and the second one passes CI forever.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import check_no_pii  # noqa: E402


class PatternsCatchRealLeaks(unittest.TestCase):
    """Each pattern is fed a line taken from the source repository it guards against."""

    LEAKS = (
        ("author identity", "Written by aaddrick, who maintains the pipeline."),
        ("author identity", "See nonconvexlabs.com for the consulting work."),
        ("prior employer as the user's own", "Reorder the CBN bullets to lead with NPI."),
        (
            "prior employer as the user's own",
            "10+ years secure document manufacturing under government contract",
        ),
        ("hardcoded home location", "Currently in Ottawa, ON. US Citizen."),
        (
            "hardcoded compensation baseline",
            "A US offer must beat the Ottawa baseline by enough to justify the move.",
        ),
        (
            "hardcoded citizenship or clearance status",
            "The user is open to US relocation, East Coast preferred.",
        ),
        ("hardcoded credential", "No bachelor's degree. Degree requirements are not blockers."),
        ("personal contact details", "Contact: someone@gmail.com"),
        ("reference to the private workspace", "Read MEMORY.md before doing any work."),
        (
            "reference to the private workspace",
            "See feedback_no_hard_blockers_clearance_degree.md",
        ),
    )

    def test_every_sample_leak_is_caught(self) -> None:
        for expected_name, line in self.LEAKS:
            with self.subTest(line=line):
                hits = [
                    name
                    for name, pattern, _ in check_no_pii.PATTERNS
                    if pattern.search(line)
                ]
                self.assertIn(
                    expected_name,
                    hits,
                    f"pattern {expected_name!r} no longer matches: {line!r}",
                )

    def test_every_pattern_has_at_least_one_sample(self) -> None:
        """A pattern with no test is a pattern that can silently stop matching."""
        covered = {name for name, _ in self.LEAKS}
        declared = {name for name, _, _ in check_no_pii.PATTERNS}
        self.assertEqual(
            declared - covered,
            set(),
            "these patterns have no sample leak in LEAKS",
        )


class PatternsDoNotFireOnLegitimateProse(unittest.TestCase):
    """A pattern that fires on ordinary skill text gets suppressed, and a
    suppressed check reads as covered while checking nothing."""

    CLEAN = (
        "Estimate the median, 75th, and 90th percentile applicants for this role.",
        "Read preferences.yaml for the compensation method and any stated constraints.",
        "The candidate's claimed differentiators come from preferences.yaml.",
        "A clearance requirement is a risk factor, not a blocker, unless preferences say so.",
        "Most capacity planning candidates come from one side of the business.",
        "Owned a $30M capital portfolio — meaningful in the candidate's own domain.",
        "Manufacturing quality inspection maps to model evaluation pipelines.",
        "Do not treat degree requirements as hard blockers.",
        "Relocation funding and sign-on are negotiated after an offer exists.",
        # The two narrowings on the author-identity pattern. A skill has to be
        # able to name the agent it dispatches and the tool it points users at.
        'slushpile ships `aaddrick-voice` as a working example.',
        'agent: "aaddrick-voice"',
        "Generate your own: https://github.com/aaddrick/written-voice-replication",
        "| `aaddrick-voice` | The example voice agent. Replace it. |",
    )

    def test_clean_lines_produce_no_hits(self) -> None:
        for line in self.CLEAN:
            with self.subTest(line=line):
                hits = [
                    name
                    for name, pattern, _ in check_no_pii.PATTERNS
                    if pattern.search(line)
                ]
                self.assertEqual(hits, [], f"false positive on: {line!r}")


class RepositoryIsClean(unittest.TestCase):
    def test_shipped_pipeline_has_no_personal_data(self) -> None:
        self.assertEqual(check_no_pii.scan(), [])

    def test_general_allowlist_is_empty(self) -> None:
        """The voice-agent exemption is principled and lives in its own table.
        This one is for everything else, and everything else is a hole."""
        self.assertEqual(
            check_no_pii.ALLOWED,
            {},
            "a general allowlist entry was added — confirm it is genuinely necessary",
        )


class VoiceAgentExemption(unittest.TestCase):
    """A voice agent IS one person's identity, so the identity patterns cannot
    apply to it. The exemption has to stay narrow, or it becomes the hole every
    future leak walks through."""

    def test_exempted_files_exist(self) -> None:
        for relative in check_no_pii.VOICE_AGENTS:
            with self.subTest(path=relative):
                self.assertTrue(
                    (ROOT / relative).exists(),
                    f"{relative} is exempted but does not exist — stale entry",
                )

    def test_exemption_never_covers_contact_details(self) -> None:
        """A phone number or personal email in a shipped file is a leak under
        any theory, including 'it is a voice agent'."""
        for relative, exempt in check_no_pii.VOICE_AGENTS.items():
            with self.subTest(path=relative):
                self.assertNotIn("personal contact details", exempt)

    def test_exempted_files_still_carry_no_contact_details(self) -> None:
        contact = next(
            pattern
            for name, pattern, _ in check_no_pii.PATTERNS
            if name == "personal contact details"
        )
        for relative in check_no_pii.VOICE_AGENTS:
            with self.subTest(path=relative):
                text = (ROOT / relative).read_text(encoding="utf-8")
                self.assertIsNone(contact.search(text))

    def test_exemption_does_not_leak_to_other_files(self) -> None:
        """The exemption is keyed by exact path. A skill that starts naming the
        author must still fail."""
        self.assertEqual(check_no_pii.exemptions_for("skills/onboard/SKILL.md"), set())

    def test_only_the_agents_directory_is_exempted(self) -> None:
        """No skill or template may ever be exempted. Those are the files that
        must work for a stranger."""
        for relative in check_no_pii.VOICE_AGENTS:
            with self.subTest(path=relative):
                self.assertTrue(relative.startswith("agents/"))


if __name__ == "__main__":
    unittest.main()
