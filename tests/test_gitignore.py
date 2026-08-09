"""The workspace ignore rules must not swallow the shipped templates.

Both halves of this matter and they pull in opposite directions.

A user who runs `/slushpile:onboard` inside a checkout of this repository must
not be able to commit their employment history and salary to it by accident.
That wants broad patterns.

But `templates/profile.md` and four of its neighbours are the product. An
unanchored `profile.md` rule matches them too, and drops them from the first
commit with no error — the exact bug this file exists to prevent from
returning.
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Written into a user's workspace by /slushpile:onboard. Never committed here.
WORKSPACE_PATHS = (
    "profile.md",
    "preferences.yaml",
    "stories.md",
    "voice-profile.md",
    "voice-samples/reddit-post.md",
    "applications/Acme/Engineering/Staff-SRE/application.yaml",
    "searches/2026-08-07/acme_search.md",
    "job_search.md",
    "companies.md",
)

# Shipped by this repository. Must survive the ignore rules.
TEMPLATE_PATHS = tuple(
    f"templates/{name}"
    for name in (
        "profile.md",
        "preferences.yaml",
        "stories.md",
        "job_search.md",
        "companies.md",
        "application.yaml",
        "job_description.md",
        "role_analysis.md",
        "resume.tex",
        "cover_letter.tex",
    )
)


def git(*args: str, cwd: Path) -> str:
    return subprocess.run(
        ["git", *args], cwd=cwd, capture_output=True, text=True, check=True
    ).stdout


class GitignoreBehavior(unittest.TestCase):
    """Exercised against a real git in a scratch repo, because the semantics
    being tested are git's pattern matching, not a string in a file."""

    @classmethod
    def setUpClass(cls) -> None:
        if shutil.which("git") is None:
            raise unittest.SkipTest("git is not installed")

        cls._tmp = tempfile.TemporaryDirectory()
        cls.repo = Path(cls._tmp.name)
        git("init", "-q", cwd=cls.repo)
        shutil.copyfile(ROOT / ".gitignore", cls.repo / ".gitignore")

        for relative in WORKSPACE_PATHS + TEMPLATE_PATHS:
            path = cls.repo / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("x", encoding="utf-8")

    @classmethod
    def tearDownClass(cls) -> None:
        cls._tmp.cleanup()

    def is_ignored(self, relative: str) -> bool:
        result = subprocess.run(
            ["git", "check-ignore", "-q", relative],
            cwd=self.repo,
            capture_output=True,
        )
        return result.returncode == 0

    def test_workspace_files_are_ignored(self) -> None:
        for relative in WORKSPACE_PATHS:
            with self.subTest(path=relative):
                self.assertTrue(
                    self.is_ignored(relative),
                    f"{relative} is not ignored — a user could commit personal data here",
                )

    def test_shipped_templates_are_not_ignored(self) -> None:
        for relative in TEMPLATE_PATHS:
            with self.subTest(path=relative):
                self.assertFalse(
                    self.is_ignored(relative),
                    f"{relative} is ignored — an unanchored rule is swallowing a template",
                )


class TemplatesAreTracked(unittest.TestCase):
    def test_every_template_on_disk_is_tracked_by_git(self) -> None:
        """Catches the same bug from the other side: a template that exists in
        a working tree but was never committed."""
        if not (ROOT / ".git").exists():
            self.skipTest("not a git repository")

        tracked = set(git("ls-files", "templates", cwd=ROOT).split())
        on_disk = {
            p.relative_to(ROOT).as_posix() for p in (ROOT / "templates").iterdir() if p.is_file()
        }
        self.assertEqual(on_disk - tracked, set(), "templates present but untracked")


if __name__ == "__main__":
    unittest.main()
