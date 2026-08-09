# Assessment History — {{Company}} {{Role}} {{req id}}

**Audit trail only. Not an input to any build.**

<!--
Created only when an assessment was revised: a contrarian net call other than
STAND, a user correction, or a materially changed score. A first-pass
assessment that stands needs no history file.

Why this is a separate file rather than a section of `role_analysis.md`:
`application-builder` and every review agent read the role analysis in full and
treat everything in it as a live finding. Give a downstream reader two numbers
for the same field and no instruction about which is current, and it will not
reliably pick the last one — it will average them, or pick the one that suits
the sentence it is writing. So the role analysis is kept at final state, and
everything that got cut lives here.

Nothing downstream reads this file. It exists so the revision history survives
without contaminating the document that does get read.

Append. Never overwrite.
-->

## Score trajectory

<!-- One row per revision. "What moved it" is the useful column — a trajectory
without causes is a list of numbers nobody can learn from. -->

| Date | Pool position | Tier | Channel | What moved it |
|---|---|---|---|---|
|  |  |  |  |  |

## Contrarian gate — findings integrated

<!-- The net call, then each finding and what it corrected. Prior values belong
here, not in `role_analysis.md`.

Record the findings that were struck as well as the ones adopted, and why. A
gate that only records what it changed cannot be audited for over-reach, and
the struck legs are the data that makes the gate better — invisible if you log
only outcomes. -->

**Net call:** {{STAND | DOWNGRADE_ONE_TIER | DOWNGRADE_TO_PASS | UPGRADE_ONE_TIER}}
**Run:** {{YYYY-MM-DD}}

| Finding | Adopted / struck | What it changed, or why it was struck |
|---|---|---|
|  |  |  |

## User corrections

<!-- Where the user overrode the pipeline, and what happened afterward. These
outrank the gate.

This is the highest-value section in the file. It is the only place the system
records being wrong in a way a human confirmed, which is what the calibration
priors are eventually built from. -->

## Instructions imposed and later lifted

<!-- Any prescription that was written into `role_analysis.md` and later
removed — a soft-kill-derived build block, a "do not pursue until X" note — and
why it was lifted.

This section exists because of a specific failure: a prohibition written at
scan time survives in the file long after the judgment behind it stopped
holding, and `application-builder` reads it as a standing order months later.
Recording the lift here is what stops a stale prohibition from silently
re-entering the analysis on the next edit. -->

## Cross-reference

- Search report: `searches/{{YYYY-MM-DD}}/{{company-slug}}_search.md`
- Structured record: `application.yaml`
- Current assessment: `role_analysis.md`
