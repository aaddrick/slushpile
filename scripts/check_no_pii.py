#!/usr/bin/env python3
"""Fail if a personal fact has leaked into the shipped pipeline.

This plugin was productized out of one person's working job-search repository.
Every personal fact there became a field in templates/preferences.yaml or a
section in templates/profile.md. Nothing in skills/ or agents/ may hardcode a
fact about any user.

The failure mode this guards against is quiet. A skill that says "the candidate
is open to US relocation" works perfectly for one person and silently produces
wrong assessments for everyone else, with no error and no way for them to know.

    python3 scripts/check_no_pii.py

A new leak that gets past this belongs here as a new pattern, not in a review
comment. Review comments do not run in CI.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# `docs` is scanned for the same reason the skills are: it is shipped prose
# about a job search, written by someone who has one, and the examples that
# teach a rule are exactly where a real employer or a real number gets used
# because it was the one at hand.
SCANNED = ("skills", "agents", "templates", "docs")

# The translated mirror, scanned at exactly the scope its English original is.
#
# `docs/` is scanned and the repository root is not, so the mirror's `docs/` is
# scanned and its `README.md` and `INSTALL.md` are not. Scanning the whole
# mirror instead looks stricter and is not: it pulls in translated READMEs,
# which carry the author-credit line the English README also carries, and the
# gate then reports four leaks that are the same deliberate credit the English
# page is trusted with. A gate that fires on a fact the original states is one
# somebody switches off.
#
# What the mirror is genuinely covered against is the contact patterns, which
# survive a language change: an address, a phone number, a profile URL look the
# same in every script. The identity patterns are English-shaped and will not
# fire on translated prose, so a paraphrased biography would get through. That
# is a real gap, and it is written down rather than implied by a directory
# appearing in a list.
MIRROR_SCANNED = "translations/*/docs"


def scan_roots() -> list[str]:
    """Every directory the patterns are run over, as repo-relative paths."""
    return list(SCANNED) + sorted(
        path.relative_to(ROOT).as_posix()
        for path in ROOT.glob(MIRROR_SCANNED)
        if path.is_dir()
    )

# (name, pattern, why it is a leak)
#
# Patterns are deliberately narrow. A broad pattern that fires on legitimate
# prose gets suppressed with a noqa comment within a week, and a suppressed
# check is worse than no check because it reads as covered.
PATTERNS: tuple[tuple[str, re.Pattern[str], str], ...] = (
    (
        "author identity",
        # Two exclusions, both narrow and both load-bearing.
        #
        # `aaddrick-voice` is the identifier of the shipped example voice agent.
        # Skills must be able to name the agent they dispatch, the same way they
        # name `slushpile-pool-analyst`.
        #
        # `github.com/aaddrick/...` is a URL to a tool the pipeline points users
        # at, and `aaddrick/slushpile` is the marketplace slug an install
        # command has to name. A repository address is not a claim about the
        # user, and neither is the plugin's own coordinates.
        #
        # Bare `aaddrick` anywhere else is still a leak, which is the case that
        # actually matters: a skill asserting something about the author as if
        # it were true of whoever installed this.
        re.compile(
            r"(?<!github\.com/)\baaddrick\b(?!-voice)(?!/slushpile\b)"
            r"|Non-?Convex Labs"
            r"|nonconvexlabs",
            re.I,
        ),
        "names the original author. Personal identity belongs in the user's profile.md.",
    ),
    (
        "prior employer as the user's own",
        re.compile(r"\bCBN\b|Canadian Bank Note|secure document manufactur", re.I),
        "names the original author's employer or domain as if it were the user's.",
    ),
    (
        "hardcoded home location",
        re.compile(r"\bOttawa\b|\bDanville\b", re.I),
        "hardcodes a location. Location belongs in preferences.yaml.",
    ),
    (
        "hardcoded compensation baseline",
        re.compile(r"\$?\d{2,3}k\s+(?:CAD|Ottawa)|Ottawa baseline|\$54k baseline", re.I),
        "hardcodes a compensation baseline. It belongs in preferences.yaml.",
    ),
    (
        "hardcoded citizenship or clearance status",
        re.compile(
            r"the candidate is a US Citizen|user is a US Citizen"
            r"|candidate holds (?:a )?(?:US |Canadian )?Secret"
            r"|user is open to (?:US )?relocation",
            re.I,
        ),
        "states a status as fact. It belongs in preferences.yaml.",
    ),
    (
        "hardcoded credential",
        re.compile(r"the candidate(?:'s)? PMP|user(?:'s)? PMP\b|no bachelor'?s degree", re.I),
        "states a credential as fact. It belongs in preferences.yaml or profile.md.",
    ),
    (
        "personal contact details",
        re.compile(r"\b[\w.+-]+@(?:gmail|outlook|yahoo|proton)\.\w+\b|\(\d{3}\)\s?\d{3}-\d{4}"),
        "contains real contact details.",
    ),
    (
        "reference to the private workspace",
        re.compile(r"MEMORY\.md|COMPANIES\.md\b|feedback_[a-z_]+\.md|user_[a-z_]+\.md"),
        "references a file from the private source repository that does not ship here.",
    ),
)

# Voice agents are the one principled exception, and it is worth being precise
# about why rather than treating it as a hole.
#
# A voice agent IS one person's identity, by construction. It is generated from
# a corpus of their writing by written-voice-replication, it is named after
# them, and its few-shot examples are their actual sentences. Stripping the
# identity out of one would destroy the artifact.
#
# slushpile ships exactly one, as a working example, so the pipeline runs before
# a user has generated their own. Users swap it out via `voice.agent` in
# preferences.yaml.
#
# The exemption is narrow on purpose. These files are exempt from the identity
# patterns only. Contact details are still forbidden everywhere, because a
# phone number in a shipped agent is a leak under any theory.
VOICE_AGENTS: dict[str, set[str]] = {
    "agents/aaddrick-voice.md": {
        "author identity",
        "prior employer as the user's own",
        "hardcoded home location",
    },
}

# Files allowed to contain something that would otherwise trip a pattern, for
# any reason other than being a voice agent. Keep this empty. Every entry here
# is a hole, and a hole in this gate is invisible until someone else's
# application says it is open to relocating to a city they have never seen.
ALLOWED: dict[str, set[str]] = {}


# A problem string is either "path:line: what" from a matched pattern or
# "dir/: directory not found" from a missing scan root. Only the first carries a
# line number, and splitting on ":" without checking put the words "directory
# not found" in the annotation's line= field — on the one branch that fires when
# this check is most broken.
LOCATED = re.compile(r"^(?P<file>[^:]+):(?P<line>\d+): ")


def exemptions_for(relative: str) -> set[str]:
    return VOICE_AGENTS.get(relative, set()) | ALLOWED.get(relative, set())


def scan() -> list[str]:
    problems = []

    for directory in scan_roots():
        base = ROOT / directory
        if not base.exists():
            problems.append(f"{directory}/: directory not found")
            continue

        for path in sorted(base.rglob("*")):
            if not path.is_file() or path.suffix not in {".md", ".yaml", ".yml", ".tex", ".txt"}:
                continue

            relative = path.relative_to(ROOT).as_posix()
            allowed = exemptions_for(relative)
            text = path.read_text(encoding="utf-8", errors="replace")

            for name, pattern, why in PATTERNS:
                if name in allowed:
                    continue
                for match in pattern.finditer(text):
                    line = text.count("\n", 0, match.start()) + 1
                    problems.append(
                        f"{relative}:{line}: {name} — {why}\n"
                        f"    matched: {match.group(0)!r}"
                    )

    return problems


def main() -> int:
    problems = scan()

    if problems:
        for problem in problems:
            head = problem.split("\n", 1)[0]
            if found := LOCATED.match(head):
                print(f"::error file={found['file']},line={found['line']}::{head}")
            else:
                print(f"::error::{head}")
        print("\nPersonal data found in the shipped pipeline:\n", file=sys.stderr)
        for problem in problems:
            print(f"  {problem}", file=sys.stderr)
        print(
            f"\n{len(problems)} leak(s). Move the fact into templates/preferences.yaml "
            f"or templates/profile.md and have the skill read it at run time.",
            file=sys.stderr,
        )
        return 1

    scanned = sum(
        1
        for directory in scan_roots()
        for path in (ROOT / directory).rglob("*")
        if path.is_file() and path.suffix in {".md", ".yaml", ".yml", ".tex", ".txt"}
    )
    print(f"No personal data found. {scanned} files scanned against {len(PATTERNS)} patterns.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
