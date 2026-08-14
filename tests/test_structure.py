"""Structural invariants that a reviewer cannot see in a diff.

Each test here corresponds to a way this plugin breaks silently: a skill that
loads under a slash command nobody documented, an agent a skill dispatches that
does not exist, a template that stopped parsing, or a documented command that
was renamed.
"""

from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import check_configs  # noqa: E402
import sync_docs  # noqa: E402

try:
    import yaml
except ImportError:  # pragma: no cover - exercised only without PyYAML
    raise SystemExit("these tests need PyYAML. Run: pip install pyyaml")


EXPECTED_SKILLS = {
    "onboard",
    "job-board-search",
    "explore-experience",
    "application-builder",
    "adversarial-review",
    "removing-ai-tells",
    "redesign-templates",
    "status",
    "help",
}

EXPECTED_AGENTS = {
    "slushpile-triage-screener",
    "slushpile-requirements-analyst",
    "slushpile-ats-simulator",
    "slushpile-fatigued-reader",
    "slushpile-pool-analyst",
    "slushpile-hiring-manager",
    "slushpile-contrarian",
    "aaddrick-voice",
}

# The voice agent is generated per person and named after its author, so it is
# the one agent exempt from the slushpile-* namespace rule.
VOICE_AGENTS = {"aaddrick-voice"}

# Fields in preferences.yaml that no skill reads, on purpose, with the reason.
# Every other field must be named by a skill or an agent — see
# Templates.test_every_preference_field_is_read_by_something for why.
PREFERENCES_UNREAD = {
    "schema_version": "Identifies the file's shape for a future migration. "
    "Nothing in the pipeline branches on it and nothing should.",
    # The four channels below are read as the observed_conversion block, which
    # both status and adversarial-review pass whole. Naming each one in a skill
    # would put application.yaml's channel list in a second place to maintain.
    "cold_submission": "Read as part of the observed_conversion block.",
    "warm_referral": "Read as part of the observed_conversion block.",
    "cold_outreach": "Read as part of the observed_conversion block.",
    "public_visibility_inbound": "Read as part of the observed_conversion block.",
}


def preference_fields(node: dict | None = None, path: tuple = ()) -> list[tuple]:
    """Every leaf field in preferences.yaml, as a dotted path. A leaf is a key
    whose value is not a mapping — a list is a leaf, because a skill reads it
    as one value."""
    if node is None:
        node = yaml.safe_load((ROOT / "templates/preferences.yaml").read_text())
    out = []
    for key, value in node.items():
        if isinstance(value, dict):
            out += preference_fields(value, path + (key,))
        else:
            out.append(path + (key,))
    return out


def frontmatter(path: Path) -> dict:
    data = check_configs.parse_frontmatter(path, yaml.safe_load)
    if isinstance(data, str):
        raise AssertionError(f"{path}: {data}")
    return data


class Skills(unittest.TestCase):
    def test_expected_skills_are_present(self) -> None:
        found = {p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md")}
        self.assertEqual(found, EXPECTED_SKILLS)

    def test_frontmatter_name_matches_directory(self) -> None:
        for path in (ROOT / "skills").glob("*/SKILL.md"):
            with self.subTest(skill=path.parent.name):
                self.assertEqual(frontmatter(path)["name"], path.parent.name)

    def test_every_skill_has_a_description(self) -> None:
        for path in (ROOT / "skills").glob("*/SKILL.md"):
            with self.subTest(skill=path.parent.name):
                self.assertTrue(frontmatter(path).get("description"))


class Agents(unittest.TestCase):
    def test_expected_agents_are_present(self) -> None:
        found = {p.stem for p in (ROOT / "agents").glob("*.md")}
        self.assertEqual(found, EXPECTED_AGENTS)

    def test_frontmatter_name_matches_filename(self) -> None:
        for path in (ROOT / "agents").glob("*.md"):
            with self.subTest(agent=path.stem):
                self.assertEqual(frontmatter(path)["name"], path.stem)

    def test_pipeline_agents_are_namespaced(self) -> None:
        """An unprefixed agent name can collide with one the user already has.
        Voice agents are exempt: they are named after the person whose writing
        produced them, and a user swapping in their own must keep that name."""
        for path in (ROOT / "agents").glob("*.md"):
            if path.stem in VOICE_AGENTS:
                continue
            with self.subTest(agent=path.stem):
                self.assertTrue(path.stem.startswith("slushpile-"))

    def test_check_configs_agrees_on_the_voice_agent_set(self) -> None:
        """Two tables naming the same exception drift apart silently."""
        import check_configs as cc

        self.assertEqual(cc.VOICE_AGENTS, VOICE_AGENTS)

    def test_default_voice_agent_in_preferences_is_shipped(self) -> None:
        """preferences.yaml names a default voice agent. If that agent is not
        in this repo, a fresh workspace dispatches an agent that does not
        exist and the cover letter step fails at run time."""
        prefs = yaml.safe_load((ROOT / "templates/preferences.yaml").read_text())
        default = prefs["voice"]["agent"]
        self.assertTrue(
            (ROOT / "agents" / f"{default}.md").exists(),
            f"preferences.yaml defaults voice.agent to {default!r}, which is not shipped",
        )

    def test_shipped_voice_agent_is_flagged_as_not_the_users(self) -> None:
        """is_mine must ship false. If it shipped true, nothing would warn a
        user that their letters are being written in a stranger's voice."""
        prefs = yaml.safe_load((ROOT / "templates/preferences.yaml").read_text())
        self.assertIs(prefs["voice"]["is_mine"], False)

    def test_every_agent_declares_a_model(self) -> None:
        """The dispatch table documents a model per agent, and the frontmatter
        is what a harness actually dispatches on. An agent with no model takes
        whatever the session runs, which silently flattens a pipeline that mixes
        tiers deliberately."""
        for path in (ROOT / "agents").glob("*.md"):
            with self.subTest(agent=path.stem):
                self.assertTrue(frontmatter(path).get("model"))

    def test_dispatch_table_models_match_the_definitions(self) -> None:
        """Two files name a model per agent. Facts() raises when they disagree;
        this names the check so a future edit that drops it is visible."""
        facts = sync_docs.Facts()
        table = dict(
            sync_docs.DISPATCH_ROW.match(line.strip()).group(2, 3)
            for line in (ROOT / sync_docs.DISPATCH_SOURCE).read_text().splitlines()
            if sync_docs.DISPATCH_ROW.match(line.strip())
        )
        self.assertEqual(set(table), set(facts.dispatch))
        for name, model in table.items():
            with self.subTest(agent=name):
                self.assertEqual(sync_docs.agent_model(name), model.strip())

    def test_every_dispatched_agent_exists(self) -> None:
        """A skill naming a missing agent fails inside a subagent, where the
        user sees a confusing partial result instead of an error."""
        self.assertEqual(check_configs.check_dispatched_agents_exist(), [])


class Manifests(unittest.TestCase):
    def test_plugin_and_marketplace_agree_on_the_name(self) -> None:
        plugin = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
        market = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
        self.assertEqual(plugin["name"], "slushpile")
        self.assertEqual([p["name"] for p in market["plugins"]], ["slushpile"])

    def test_versions_match_across_harnesses(self) -> None:
        """A version that drifts between manifests makes an install report a
        version the user does not have.

        The marketplace entry is included because that is the one an install
        resolves against and `claude plugin list` prints back. A plugin.json
        that says 1.0.0 behind a marketplace entry that says 0.9.0 installs the
        old number and reports it as current."""
        versions = {
            path: json.loads((ROOT / path).read_text())["version"]
            for path in (
                ".claude-plugin/plugin.json",
                ".codex-plugin/plugin.json",
                "gemini-extension.json",
            )
        }
        market = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
        versions[".claude-plugin/marketplace.json"] = market["plugins"][0]["version"]
        self.assertEqual(len(set(versions.values())), 1, versions)

    def test_gemini_context_file_exists(self) -> None:
        name = json.loads((ROOT / "gemini-extension.json").read_text())["contextFileName"]
        self.assertTrue((ROOT / name).exists(), f"{name} is named but missing")

    def test_marketplace_lists_as_many_skills_as_it_counts(self) -> None:
        """The description states a number and then enumerates the skills. The
        sweep checks the number. Nothing checked the list, and it shipped naming
        eight of the nine plus one item that is a behavior rather than a skill.

        Keep the blurbs comma-free — the count is items between commas."""
        market = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
        description = market["plugins"][0]["description"]
        self.assertIn("The skills:", description)
        roster = description.split("The skills:", 1)[1].strip().rstrip(".")
        items = [part.strip() for part in roster.split(",") if part.strip()]
        self.assertEqual(len(items), len(EXPECTED_SKILLS), items)

    def test_codex_skills_path_exists(self) -> None:
        path = json.loads((ROOT / ".codex-plugin/plugin.json").read_text())["skills"]
        self.assertTrue((ROOT / path.lstrip("./")).is_dir())


class Templates(unittest.TestCase):
    def test_yaml_templates_parse(self) -> None:
        for name in ("preferences.yaml", "application.yaml"):
            with self.subTest(template=name):
                yaml.safe_load((ROOT / "templates" / name).read_text())

    def test_every_preference_field_is_read_by_something(self) -> None:
        """A field in preferences.yaml that nothing reads is worse than a
        missing one. Onboarding presents it as a working dial, so a user sets
        it and stops applying their own judgment to whatever they believe it
        now handles. Six shipped that way, and each one's comment documented
        behavior that did not exist anywhere in the pipeline.

        A field is read when a skill or an agent names it in a form that is
        unambiguously the field: a dotted path ending in it, or the name as a
        token inside a code span. Prose alone does not count. `posture` went
        unnoticed for exactly that reason — the only match for it was "hiring
        posture" in a report heading, so any check loose enough to accept prose
        would have passed the field that motivated this test."""
        code = {
            p.relative_to(ROOT).as_posix(): [
                span
                for span in re.findall(r"`([^`\n]+)`", p.read_text())
                if "://" not in span
            ]
            + re.findall(r"(?:[a-z_]+\.)+[a-z_]+", p.read_text())
            for p in list((ROOT / "skills").rglob("*.md"))
            + list((ROOT / "agents").rglob("*.md"))
        }
        fields = preference_fields()
        ambiguous = {
            leaf
            for leaf in (p[-1] for p in fields)
            if sum(p[-1] == leaf for p in fields) > 1
        }
        for path in fields:
            leaf = path[-1]
            with self.subTest(field=".".join(path)):
                if leaf in PREFERENCES_UNREAD:
                    continue
                # Two blocks both have a `notes`. A bare match on the name would
                # let either one's reader vouch for both, which is the exact
                # false pass this test exists to prevent — so an ambiguous leaf
                # has to be named with its parent.
                wanted = ".".join(path[-2:]) if leaf in ambiguous else leaf
                token = re.compile(rf"(?:^|[^\w.]|\.){re.escape(wanted)}(?:\W|$)")
                self.assertTrue(
                    any(token.search(s) for spans in code.values() for s in spans),
                    f"preferences.yaml collects {'.'.join(path)} and no skill or "
                    f"agent reads it. Wire it in, or give it a row in "
                    f"PREFERENCES_UNREAD saying why it is not read.",
                )

    def test_no_unread_exemption_outlives_its_field(self) -> None:
        """The other direction. An exemption for a field that no longer exists
        is a note about nothing, and it makes the next reader trust the table
        less than the file it describes."""
        leaves = {path[-1] for path in preference_fields()}
        self.assertEqual(set(PREFERENCES_UNREAD) - leaves, set())

    def test_every_template_referenced_by_a_skill_exists(self) -> None:
        referenced = set()
        for path in (ROOT / "skills").glob("*/SKILL.md"):
            referenced |= set(
                re.findall(r"templates/([\w.-]+\.(?:md|yaml|tex))", path.read_text())
            )
        missing = {n for n in referenced if not (ROOT / "templates" / n).exists()}
        self.assertEqual(missing, set())


class GeneratedDocs(unittest.TestCase):
    def test_derived_files_are_in_sync(self) -> None:
        self.assertEqual(sync_docs.check(), 0)

    def test_agents_md_carries_the_generated_marker(self) -> None:
        self.assertIn(sync_docs.MARKER, (ROOT / "AGENTS.md").read_text())

    def test_the_cursor_router_is_generated_not_just_marked(self) -> None:
        """Both Cursor files carry a 'do not edit' marker. That marker is a lie
        unless the generator actually produces them, and a lie there means the
        next person hand-edits a file that the following run overwrites."""
        for target in (".cursor/skills/slushpile/SKILL.md", ".cursor/rules/slushpile.mdc"):
            with self.subTest(target=target):
                self.assertIn(target, sync_docs.BUILDERS)
                self.assertIn(sync_docs.MARKER, (ROOT / target).read_text())

    def test_every_skill_is_routed_on_every_surface(self) -> None:
        """A skill with no row in the router is a stage a Cursor user cannot
        reach, and one missing from the README is a command nobody runs. One
        table feeds all four surfaces, so covering it covers them."""
        self.assertEqual({skill.name for skill in sync_docs.SKILLS}, EXPECTED_SKILLS)
        for skill in sync_docs.SKILLS:
            with self.subTest(skill=skill.name):
                self.assertTrue(skill.cursor and skill.install and skill.readme)

    def test_generator_rejects_a_skill_it_was_never_told_about(self) -> None:
        """The failure this whole generator exists to produce."""
        declared = [skill.name for skill in sync_docs.SKILLS]
        with self.assertRaises(ValueError):
            sync_docs.require_exact(declared, EXPECTED_SKILLS | {"unlisted"}, "SKILLS")

    def test_counted_claims_hold(self) -> None:
        """Sentences that state a number in prose are checked, not generated.
        This pins the wording of the ones that were registered."""
        self.assertEqual(sync_docs.check_count_claims(sync_docs.Facts()), [])

    def test_no_surface_states_a_stale_count(self) -> None:
        """The half COUNT_CLAIMS cannot cover. Three files read 'eight skills'
        for as long as there were nine, because no row named them."""
        self.assertEqual(sync_docs.check_stray_counts(sync_docs.Facts()), [])

    def test_the_sweep_reads_the_surfaces_it_claims_to(self) -> None:
        """A sweep that matches nothing passes every time. These are the files
        the stale counts were actually found in."""
        swept = {path.relative_to(ROOT).as_posix() for path in sync_docs.swept_files()}
        for target in (
            "INSTALL.md",
            "README.md",
            "CONTRIBUTING.md",
            "skills/help/SKILL.md",
            ".claude-plugin/marketplace.json",
        ):
            with self.subTest(target=target):
                self.assertIn(target, swept)

    def test_the_sweep_fails_on_a_count_nobody_registered(self) -> None:
        """The failure the sweep exists to produce, on a file with no row in
        COUNT_CLAIMS and no entry in COUNT_EXEMPT."""
        planted = ROOT / "stale-count-fixture.md"
        planted.write_text("slushpile is two skills.\n", encoding="utf-8")
        try:
            problems = sync_docs.check_stray_counts(sync_docs.Facts())
        finally:
            planted.unlink()
        self.assertTrue(
            any("stale-count-fixture.md" in problem for problem in problems),
            f"the sweep did not flag 'two skills': {problems}",
        )

    def test_every_hand_written_roster_names_every_skill(self) -> None:
        """The generated lists cover the router, the README, and the INSTALL
        snippet. This covers the ones typed by hand, which is where the
        omissions happened."""
        self.assertEqual(sync_docs.check_command_rosters(sync_docs.Facts()), [])

    def test_the_roster_gate_fails_on_a_skill_it_cannot_find(self) -> None:
        """The failure that gate exists to produce."""
        planted = ROOT / "roster-fixture.md"
        planted.write_text("Run /slushpile:onboard, then stop.\n", encoding="utf-8")
        original = sync_docs.COMMAND_ROSTERS
        sync_docs.COMMAND_ROSTERS = ("roster-fixture.md",)
        try:
            problems = sync_docs.check_command_rosters(sync_docs.Facts())
        finally:
            sync_docs.COMMAND_ROSTERS = original
            planted.unlink()
        self.assertTrue(problems, "the roster gate passed a file naming one skill")
        self.assertIn("redesign-templates", problems[0])

    def test_the_sweep_covers_the_blind_stage_count(self) -> None:
        """How many reviewers run blind is spelled out across six hand-written
        files in shapes the noun sweep alone does not see — "five of whom run in
        parallel", "the first five are supposed to be blind". Until those were
        swept, the only thing pinning the number was the literal in
        test_dispatch_order_matches_the_review_pipeline, which fails with the
        number and none of the files, so the cheapest way back to green is to
        edit the literal and ship the stale prose."""
        planted = ROOT / "blind-count-fixture.md"
        planted.write_text("Four of whom run in parallel.\n", encoding="utf-8")
        try:
            problems = sync_docs.check_stray_counts(sync_docs.Facts())
        finally:
            planted.unlink()
        self.assertTrue(
            any("blind-count-fixture.md" in problem for problem in problems),
            f"the sweep did not flag 'Four of whom run in parallel': {problems}",
        )

    def test_every_exemption_still_matches_something(self) -> None:
        """An exemption whose sentence was reworded silently stops covering
        anything, and reads as a live exception that nothing needs."""
        for target, phrase in sync_docs.COUNT_EXEMPT:
            with self.subTest(target=target, phrase=phrase):
                self.assertIn(phrase, (ROOT / target).read_text(encoding="utf-8"))

    def test_every_reviewer_has_a_readme_row(self) -> None:
        self.assertEqual(set(sync_docs.REVIEWERS), set(sync_docs.Facts().dispatch))

    def test_dispatch_order_matches_the_review_pipeline(self) -> None:
        """The Cursor router states the persona order and how many run blind.
        Both are read from the dispatch table, so a reordered pipeline moves
        them. If it stops being read, this catches it."""
        facts = sync_docs.Facts()
        self.assertEqual(facts.dispatch[0], "slushpile-triage-screener")
        self.assertEqual(facts.sequential, ["slushpile-hiring-manager", "slushpile-contrarian"])
        # Changing this literal is not the fix for a red run. The blind count is
        # spelled out in six hand-written files; check_stray_counts names them.
        self.assertEqual(len(facts.blind), 5)
        self.assertEqual(set(facts.dispatch) | set(facts.voice), EXPECTED_AGENTS)

    def test_every_declared_region_is_marked_in_its_file(self) -> None:
        """A region whose markers were deleted stops being generated, and the
        file keeps whatever it last held. The generator raises on a missing
        marker; this names which file lost it."""
        for target, regions in sync_docs.REGIONS.items():
            text = (ROOT / target).read_text()
            for region in regions:
                with self.subTest(target=target, region=region):
                    self.assertEqual(text.count(sync_docs.begin(region)), 1)
                    self.assertEqual(text.count(sync_docs.end(region)), 1)


class Documentation(unittest.TestCase):
    def test_readme_names_only_real_skills(self) -> None:
        """A renamed skill leaves a documented command that does not exist."""
        for doc in ("README.md", "INSTALL.md"):
            text = (ROOT / doc).read_text()
            for name in set(re.findall(r"/slushpile:([a-z-]+)", text)):
                with self.subTest(doc=doc, command=name):
                    self.assertIn(name, EXPECTED_SKILLS)

    def test_gemini_context_imports_every_skill_and_agent(self) -> None:
        text = (ROOT / "GEMINI.md").read_text()
        for name in EXPECTED_SKILLS:
            with self.subTest(skill=name):
                self.assertIn(f"skills/{name}/SKILL.md", text)
        for name in EXPECTED_AGENTS:
            with self.subTest(agent=name):
                self.assertIn(f"agents/{name}.md", text)


# A face named "Bold Italic" in a template's options is PublicSans-BoldItalic.ttf
# on disk. Only the two vendored families appear here; the fallback families are
# whatever the user's system already has, which is the point of the fallback.
FONT_FAMILY_PREFIX = {"Public Sans": "PublicSans", "IBM Plex Mono": "IBMPlexMono"}
FALLBACK_FAMILIES = {"DejaVu Sans", "DejaVu Sans Mono"}

FONT_DECL = re.compile(
    r"\\(?:setmainfont|setmonofont|newfontfamily\\[A-Za-z]+)"
    r"\{([^{}]+)\}(?:\[([^\]]*)\])?",
    re.DOTALL,
)
FACE_OPTION = re.compile(r"[A-Za-z]+Font=\{\*\s*([^}]+)\}")


class Fonts(unittest.TestCase):
    def test_install_fonts_carries_every_face_the_templates_name(self) -> None:
        """A weight added to a template but not to FACES makes the installer
        silently short. The user runs it, every step reports success, and that
        one face takes the fallback branch on a machine where they did
        everything right — which reads as the script being broken."""
        import install_fonts

        checked = 0
        for name in ("resume.tex", "cover_letter.tex"):
            text = (ROOT / "templates" / name).read_text()
            for family, options in FONT_DECL.findall(text):
                if family in FALLBACK_FAMILIES:
                    continue
                if family not in FONT_FAMILY_PREFIX:
                    self.fail(
                        f"templates/{name} names the family {family!r}, which is "
                        f"neither vendored in assets/fonts/ nor a documented "
                        f"fallback. Vendor it and add it here, or fall back to "
                        f"something a normal system has."
                    )
                for weight in FACE_OPTION.findall(options):
                    face = f"{FONT_FAMILY_PREFIX[family]}-{weight.replace(' ', '')}.ttf"
                    checked += 1
                    with self.subTest(template=name, face=face):
                        self.assertIn(face, install_fonts.FACES)
                        self.assertTrue((ROOT / "assets" / "fonts" / face).is_file())

        # A regex that stops matching passes this test in silence otherwise.
        self.assertGreaterEqual(checked, 10, "the template font parse found nothing")

    def test_faces_carries_nothing_the_templates_do_not_name(self) -> None:
        """The other direction. A face installed into someone's home directory
        because a template used to want it is a font they did not ask for."""
        import install_fonts

        named = set()
        for name in ("resume.tex", "cover_letter.tex"):
            text = (ROOT / "templates" / name).read_text()
            for family, options in FONT_DECL.findall(text):
                if family not in FONT_FAMILY_PREFIX:
                    continue
                for weight in FACE_OPTION.findall(options):
                    named.add(f"{FONT_FAMILY_PREFIX[family]}-{weight.replace(' ', '')}.ttf")
        self.assertEqual(set(install_fonts.FACES), named)


class GitIgnore(unittest.TestCase):
    def test_workspace_files_are_ignored(self) -> None:
        """A user who runs onboarding inside a checkout must not be able to
        commit their employment history to this repository by accident."""
        ignored = (ROOT / ".gitignore").read_text()
        for name in (
            "profile.md",
            "preferences.yaml",
            "stories.md",
            "voice-samples/",
            "applications/",
        ):
            with self.subTest(path=name):
                self.assertIn(name, ignored)


if __name__ == "__main__":
    unittest.main()
