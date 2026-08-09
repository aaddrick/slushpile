# Agents and models

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <strong>English</strong> ·
  <a href="../../translations/zh-CN/docs/architecture/agents-and-models.md">简体中文</a> ·
  <a href="../../translations/es/docs/architecture/agents-and-models.md">Español</a> ·
  <a href="../../translations/pt-BR/docs/architecture/agents-and-models.md">Português (BR)</a> ·
  <a href="../../translations/vi/docs/architecture/agents-and-models.md">Tiếng Việt</a>
</p>

<!-- END GENERATED language-nav -->

## A skill orchestrates. An agent has one job.

The two are different kinds of file and the boundary between them is load
bearing.

A skill knows about the pipeline: what stage it is in, what ran before it, what
it hands off to. An agent knows only its own job. **An agent that knows what
stage it is in will optimize for the stage instead of doing its job** — a triage
screener told it is the first of five will start hedging, because it can tell
someone else is going to check its work.

The corollary is the rule that keeps the review's output comparable:

**Binding constraints live in the agent definition, not in the dispatching
prompt.** An orchestrator that improvises extra constraints per run produces
findings that cannot be compared across applications, which destroys the
calibration data the whole system depends on. The contrarian's scope limits are
in `agents/slushpile-contrarian.md` for this reason, and the review skill is
explicitly told not to restate or extend them.

Data is the exception, and the distinction is worth stating precisely.
`calibration_priors` goes in the dispatch prompt because it changes *what the
agent knows*. Scope limits stay in the definition because they change *what the
agent is allowed to say*. The first varies per run by design; the second must
not.

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

The model is in each agent's frontmatter, and the dispatch table in
`skills/adversarial-review/SKILL.md` names one per agent as well. The two are
checked against each other by `tests/test_structure.py`: the frontmatter is what
a harness actually dispatches on, and the table column is documentation of it.

An agent with no declared model takes whatever the session is running. That
silently flattens a review that mixes tiers on purpose, which is why the field
is required rather than optional.

The split is not arbitrary. The cheaper personas each simulate a **bounded,
mechanical** reading: eleven seconds of skimming, a qualification checklist, a
parser, a tired reader's irritation. Those are well-specified tasks where a
larger model mostly adds cost.

The expensive ones each require **estimating something that is not in the
document**. The pool analyst has to characterize applicants who are not in front
of it. The hiring manager has to weigh five reports against each other and
produce probabilities. The contrarian has to construct the strongest argument
that all of the above is wrong. Those degrade visibly on a smaller model, and
they are the three whose output the user actually acts on.

## Namespacing

Every pipeline agent is prefixed `slushpile-` so it cannot collide with an agent
the user already has. A user with their own `contrarian` keeps it; this
pipeline's is `slushpile-contrarian` and the two never meet.

## Voice agents are the deliberate exception

The voice agent is the one agent in this repository not named `slushpile-*`, and
the one whose name is a person's.

That is because it is generated per person by
[written-voice-replication](https://github.com/aaddrick/written-voice-replication)
and named after its author. A user swapping in their own must be able to keep
that name, so the name is read from `preferences.yaml` at run time rather than
hardcoded anywhere:

```yaml
voice:
  agent: "your-name-voice"
  is_mine: true
```

`agents/aaddrick-voice.md` ships as that pipeline's public worked example, so
slushpile runs out of the box before a user has generated one. It is the plugin
author's voice, not the user's, and while `is_mine` is false every skill that
drafts prose warns before it runs. That warning is the only thing standing
between a user and twelve applications sent in a stranger's voice.

It is exempted from the identity patterns in `scripts/check_no_pii.py` — but
never from the contact-details pattern. See
[personal-data.md](personal-data.md).

**Do not add a second voice agent to this repository.** One example is a demo;
two is a library of other people's voices that nobody asked for.
