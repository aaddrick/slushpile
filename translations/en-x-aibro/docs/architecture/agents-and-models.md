# Agents and models

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../../docs/architecture/agents-and-models.md">English</a> ·
  <a href="../../../zh-CN/docs/architecture/agents-and-models.md">简体中文</a> ·
  <a href="../../../es/docs/architecture/agents-and-models.md">Español</a> ·
  <a href="../../../pt-BR/docs/architecture/agents-and-models.md">Português (BR)</a> ·
  <a href="../../../vi/docs/architecture/agents-and-models.md">Tiếng Việt</a> ·
  <strong>AI Bro</strong>
</p>

<!-- END GENERATED language-nav -->

## A skill orchestrates. An agent has one job.

Two kinds of file. The boundary between them is load bearing.

A skill knows about the pipeline: what stage it is in, what ran before, what it
hands off to. An agent knows its own job and nothing else.

**An agent that knows what stage it is in will optimize for the stage instead of
doing its job.**

Tell a triage screener it is the first of five and it starts hedging, because it
can infer somebody downstream will check its work. Context is not free and it is
not neutral. Every token of pipeline awareness you hand an agent is a token
arguing against the thing you asked it for.

The corollary keeps the output comparable across runs:

**Binding constraints live in the agent definition, not in the dispatching
prompt.** An orchestrator improvising constraints per run produces findings that
cannot be compared across applications, which destroys the calibration data the
whole system runs on. The contrarian's scope limits live in
`agents/slushpile-contrarian.md`, and the review skill is explicitly told not to
restate or extend them.

Data is the exception, and the line is precise. `calibration_priors` goes in the
dispatch prompt because it changes *what the agent knows*. Scope limits stay in
the definition because they change *what the agent is allowed to say*. The first
varies per run by design. The second must not.

## Every agent declares a model

<!-- BEGIN GENERATED agent-table: scripts/sync_docs.py -->

| # | Agent | Model | Simulates |
|---|---|---|---|
| 1 | `slushpile-triage-screener` | sonnet | 11 seconds, F-pattern, 347 resumes already read today |
| 2 | `slushpile-requirements-analyst` | sonnet | 30 seconds, methodical, checks every qualification against evidence |
| 3 | `slushpile-ats-simulator` | sonnet | A parser. Not a reader. Structure, keywords, and years-of-experience math |
| 4 | `slushpile-fatigued-reader` | sonnet | Application #61 of 80. What annoys, what gets skimmed, what closes the tab |
| 5 | `slushpile-pool-analyst` | opus | A recruiter who knows what the queue actually looks like |
| 6 | `slushpile-hiring-manager` | opus | The person who has to justify the interview slot to their skip-level |
| 7 | `slushpile-contrarian` | opus | Whoever should have asked whether any of this was worth doing |

Plus the voice agent, `aaddrick-voice`, which the review never dispatches and
which is named in `preferences.yaml` rather than here. The first five run in
parallel and are blind to each other; the last two run in order.

<!-- END GENERATED agent-table -->

Heterogeneous model routing. Four cheap, three expensive, and the split is a cost
decision somebody actually made.

The model is declared in each agent's frontmatter, and the dispatch table in
`skills/adversarial-review/SKILL.md` names one per agent too. `tests/test_structure.py`
checks them against each other: frontmatter is what a harness dispatches on, the
table column is documentation of it.

An agent with no declared model inherits whatever the session is running.

That silently flattens a review that mixes tiers on purpose. Which is why the
field is required, not optional. Silent flattening is the worst failure mode
available to a system like this, because the output still looks like a full run
and there is nothing in it that says otherwise.

The split is not vibes.

The cheap personas each simulate a **bounded, mechanical** read. Eleven seconds of
skimming. A qualification checklist. A parser. A tired reader's irritation.
Well-specified tasks where a larger model mostly adds cost.

The expensive ones each have to **estimate something that is not in the
document**. The pool analyst characterizes applicants who are not in front of it.
The hiring manager weighs five reports and emits probabilities. The contrarian
constructs the strongest argument that all of the above is wrong. Those degrade
visibly on a smaller model, and they are the three whose output the user actually
acts on.

Spend where the reasoning is unbounded. Save where it is not. That is the entire
routing policy and it fits in two sentences.

## Namespacing

Every pipeline agent is prefixed `slushpile-` so it cannot collide with an agent
the user already has. A user with their own `contrarian` keeps it. This pipeline's
is `slushpile-contrarian` and the two never meet.

## Voice agents are the deliberate exception

One agent here is not named `slushpile-*`, and its name is a person's.

It is generated per person by
[written-voice-replication](https://github.com/aaddrick/written-voice-replication)
and named after its author, so a user swapping in their own has to be able to keep
that name. The name is read from `preferences.yaml` at run time, hardcoded
nowhere:

```yaml
voice:
  agent: "your-name-voice"
  is_mine: true
```

`agents/aaddrick-voice.md` ships as that pipeline's public worked example, so
slushpile runs on install before a user has generated one. It is the plugin
author's voice, not the user's, and while `is_mine` is false every skill that
drafts prose warns before it runs. That warning is the only thing between a user
and twelve applications shipped in a stranger's voice.

It is exempted from the identity patterns in `scripts/check_no_pii.py`, and never
from the contact-details pattern. See [personal-data.md](personal-data.md).

**Do not add a second voice agent to this repository.**

One example is a demo. Two is a library of other people's voices that nobody asked
for.
