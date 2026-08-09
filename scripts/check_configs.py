#!/usr/bin/env python3
"""Parse every config file this repository ships, and validate the skills and agents.

A manifest that does not parse breaks the install route it belongs to, and no
reviewer catches a missing comma by reading JSON. The frontmatter checks catch
the other silent failure: a skill whose directory name and declared name
disagree loads under a slash command nobody documented, and an agent whose name
does not match its filename cannot be dispatched by the skill that names it.

    python3 scripts/check_configs.py    # exit 1 and name every file that fails
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]

JSON_FILES = (
    ".claude-plugin/marketplace.json",
    ".claude-plugin/plugin.json",
    ".codex-plugin/plugin.json",
    "gemini-extension.json",
    ".gemini/settings.json",
)

YAML_FILES = ("templates/preferences.yaml", "templates/application.yaml")

# Pipeline agents are namespaced `slushpile-*` so they cannot collide with an
# agent the user already has. Voice agents are the deliberate exception: they
# are generated per person by written-voice-replication and named after their
# author, and a user swapping in their own must be able to keep that name. The
# one shipped here is that pipeline's public worked example, included so
# slushpile runs out of the box.
VOICE_AGENTS = {"aaddrick-voice"}

FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def load_yaml() -> Callable[[Any], Any]:
    try:
        import yaml
    except ImportError:
        print("ERROR: this check needs PyYAML. Run: pip install pyyaml", file=sys.stderr)
        raise SystemExit(2)
    return yaml.safe_load


def parse_frontmatter(path: Path, safe_load: Callable[[Any], Any]) -> dict | str:
    """Return the parsed frontmatter mapping, or an error string."""
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER.match(text)
    if not match:
        return "no YAML frontmatter block at the top of the file"
    try:
        data = safe_load(match.group(1))
    except Exception as error:
        return f"frontmatter does not parse: {str(error).splitlines()[0]}"
    if not isinstance(data, dict):
        return "frontmatter is not a mapping"
    return data


def check_parses(relative: str, load: Callable[[Any], Any]) -> str | None:
    path = ROOT / relative
    if not path.exists():
        return "file not found"
    try:
        with path.open("r", encoding="utf-8") as handle:
            load(handle)
    except Exception as error:  # every parser raises its own type
        return str(error).replace("\n", " ")
    return None


def check_skills(safe_load: Callable[[Any], Any]) -> list[str]:
    problems = []
    skills_dir = ROOT / "skills"
    found = sorted(skills_dir.glob("*/SKILL.md"))

    if not found:
        return ["skills/: no SKILL.md files found"]

    for path in found:
        relative = path.relative_to(ROOT).as_posix()
        data = parse_frontmatter(path, safe_load)
        if isinstance(data, str):
            problems.append(f"{relative}: {data}")
            continue

        for field in ("name", "description"):
            if not data.get(field):
                problems.append(f"{relative}: frontmatter is missing '{field}'")

        directory = path.parent.name
        if data.get("name") and data["name"] != directory:
            problems.append(
                f"{relative}: frontmatter name '{data['name']}' "
                f"does not match directory '{directory}'"
            )

    return problems


def check_agents(safe_load: Callable[[Any], Any]) -> list[str]:
    problems = []
    agents_dir = ROOT / "agents"
    found = sorted(agents_dir.glob("*.md"))

    if not found:
        return ["agents/: no agent definitions found"]

    for path in found:
        relative = path.relative_to(ROOT).as_posix()
        data = parse_frontmatter(path, safe_load)
        if isinstance(data, str):
            problems.append(f"{relative}: {data}")
            continue

        # `model` is required on an agent and not on a skill: it is what the
        # harness dispatches on, and the review's dispatch table documents it
        # per agent. An agent without one takes whatever the session is running,
        # which makes a pipeline that mixes tiers on purpose stop doing so.
        for field in ("name", "description", "model"):
            if not data.get(field):
                problems.append(f"{relative}: frontmatter is missing '{field}'")

        name = data.get("name")
        if name and name != path.stem:
            problems.append(
                f"{relative}: frontmatter name '{name}' does not match filename"
            )
        if name and not name.startswith("slushpile-") and name not in VOICE_AGENTS:
            problems.append(
                f"{relative}: agent name '{name}' must start with 'slushpile-' "
                f"so it cannot collide with a user's own agent, or be listed in "
                f"VOICE_AGENTS"
            )

    return problems


def check_dispatched_agents_exist() -> list[str]:
    """Every slushpile-* agent named in a skill must have a definition."""
    defined = {path.stem for path in (ROOT / "agents").glob("*.md")}
    referenced: dict[str, set[str]] = {}

    for path in sorted((ROOT / "skills").glob("*/SKILL.md")):
        text = path.read_text(encoding="utf-8")
        for name in re.findall(r"slushpile-[a-z0-9-]+", text):
            referenced.setdefault(name, set()).add(path.relative_to(ROOT).as_posix())

    problems = []
    for name in sorted(referenced):
        if name not in defined:
            where = ", ".join(sorted(referenced[name]))
            problems.append(f"{where}: dispatches '{name}', which has no definition")
    return problems


def main() -> int:
    safe_load = load_yaml()
    failures = 0

    for relative in JSON_FILES:
        problem = check_parses(relative, json.load)
        if problem:
            failures += 1
            print(f"::error file={relative}::{problem}")

    for relative in YAML_FILES:
        problem = check_parses(relative, safe_load)
        if problem:
            failures += 1
            print(f"::error file={relative}::{problem}")

    for problem in check_skills(safe_load) + check_agents(safe_load) + check_dispatched_agents_exist():
        failures += 1
        print(f"::error::{problem}")

    if failures:
        print(f"\n{failures} problem(s) found.", file=sys.stderr)
        return 1

    checked = len(JSON_FILES) + len(YAML_FILES)
    skills = len(list((ROOT / "skills").glob("*/SKILL.md")))
    agents = len(list((ROOT / "agents").glob("*.md")))
    print(f"{checked} config files parse. {skills} skills and {agents} agents are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
