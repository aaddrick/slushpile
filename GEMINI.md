# slushpile

An adversarial job search that gets better as it goes. Nine skills and eight
agents that take a role from a careers-board listing to a resume and cover
letter that have already survived an adversarial review, then write what that
review found back into the profile every later role is built from.

The design rests on one idea: an application is not graded against the job
description, it is graded against the other applications in the same queue.
Every scoring step here is anchored to that queue rather than to the posting.

## Setup, once per workspace

Run the onboarding skill in the directory where you keep your job search. It
reads whatever materials you already have, interviews you for the rest, and
writes four files:

- `profile.md` — every factual claim the pipeline may make on your behalf
- `preferences.yaml` — your constraints: compensation, relocation, targeting
- `stories.md` — the stories a cover letter gets built around
- a **voice agent** — how you write. Generated separately by
  https://github.com/aaddrick/written-voice-replication, then named in
  `preferences.yaml`. A working example ships as `aaddrick-voice`; it is the
  plugin author's voice, not yours.

Nothing in this pipeline hardcodes a fact about you. Those four files are where
every personal fact lives.

## The skills

<!-- BEGIN GENERATED skills: scripts/sync_docs.py -->

@./skills/onboard/SKILL.md
@./skills/job-board-search/SKILL.md
@./skills/explore-experience/SKILL.md
@./skills/application-builder/SKILL.md
@./skills/adversarial-review/SKILL.md
@./skills/removing-ai-tells/SKILL.md
@./skills/redesign-templates/SKILL.md
@./skills/status/SKILL.md
@./skills/help/SKILL.md

<!-- END GENERATED skills -->

## The agents

<!-- BEGIN GENERATED agents: scripts/sync_docs.py -->

The review pipeline dispatches seven personas. On a harness without subagent
dispatch, adopt each definition in turn and run them sequentially, writing each
report out before starting the next.

@./agents/slushpile-triage-screener.md
@./agents/slushpile-requirements-analyst.md
@./agents/slushpile-ats-simulator.md
@./agents/slushpile-fatigued-reader.md
@./agents/slushpile-pool-analyst.md
@./agents/slushpile-hiring-manager.md
@./agents/slushpile-contrarian.md
@./agents/aaddrick-voice.md

<!-- END GENERATED agents -->

## What this never does

It does not submit anything. No skill here touches an application portal, an
email, or a form. The output is files on your disk that you review and send
yourself.
