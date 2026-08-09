# The pipeline, stage by stage

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../../docs/architecture/pipeline.md">English</a> ·
  <a href="../../../zh-CN/docs/architecture/pipeline.md">简体中文</a> ·
  <a href="../../../es/docs/architecture/pipeline.md">Español</a> ·
  <a href="../../../pt-BR/docs/architecture/pipeline.md">Português (BR)</a> ·
  <a href="../../../vi/docs/architecture/pipeline.md">Tiếng Việt</a> ·
  <strong>AI Bro</strong>
</p>

<!-- END GENERATED language-nav -->

## The whole loop

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../../../docs/diagrams/pipeline-overview-dark.svg">
  <img alt="Slushpile end to end. Row one, left to right: onboard, which interviews and ingests a resume to write profile, preferences and stories; job board search, which extracts postings verbatim and scores pool-anchored fit and channel expected value; application builder, which produces the angle, resume, letter, voice pass and humanize step; and adversarial review, 7 reviewers of which 5 in parallel are blind to each other, returning a verdict per channel. Builder and review are joined by a bidirectional arrow labelled up to three rounds. The flow drops from review to a blue box, you send it, noting that no skill touches a portal, an email or a form. Row two reads back right to left: outcome recorded, then status, which regresses the pipeline's predictions against outcomes, then a dashed arrow labelled priors into the workspace box holding profile.md, preferences.yaml, stories.md and job_search.md. A dashed arrow joins the workspace back to onboard, labelled written by onboarding, read by every stage." src="../../../../docs/diagrams/pipeline-overview-light.svg">
</picture>

Three commands are the spine. `onboard` once per workspace, then
`job-board-search` and `application-builder` per company and per role. The
builder dispatches `explore-experience`, `adversarial-review`, and
`removing-ai-tells` itself.

Now look at row two, because row two is the entire differentiator.

Outcomes get recorded. `status` regresses what the pipeline predicted against
what happened. Corrected priors write back into `preferences.yaml`, where the
next search reads them.

That arrow is a closed loop. Nothing else in this category has one. Everything
else is row one, executed forty times, learning nothing. See
[memory-and-calibration.md](memory-and-calibration.md).

## Legend

Every diagram here draws from one class vocabulary, defined in
`docs/diagrams/theme-light.d2` and `theme-dark.d2`. The theme files and this
table are checked against each other by `tests/test_docs.py`.

| Class | Means |
| --- | --- |
| `stage` | An ordinary step the orchestrating skill performs itself |
| `agent` | A dispatched persona: a subagent with its own definition in `agents/` |
| `gate` | A gate or a capped loop: somewhere the run can iterate, stall, or stop |
| `memory` | A durable workspace file, written once and read by every later stage |
| `human` | The one place the user is required |
| `terminal` | A terminal state for that diagram |
| `phase` | A container grouping cells that run together |
| `flow` | A normal forward edge |
| `loop` | A backward edge: rework, re-review, another round |
| `writeback` | An edge that writes into the workspace memory |

`stage` versus `agent` is the distinction that matters.

An `agent` box is a subagent with its own definition and its own context window.
On a harness that cannot dispatch subagents, every one of those collapses into
one shared context. That collapse is the whole difference between the real
topology and a degraded one, and it does not show up in the output.

## `/slushpile:onboard`

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../../../docs/diagrams/phase-onboard-dark.svg">
  <img alt="The onboarding phases. Row one: ingest a resume in any format or a LinkedIn export; interview for the gaps a document cannot fill, with numbers given baselines; profile.md, described as the pool a resume is cut from rather than a resume; preferences.yaml, holding the compensation method and constraints, with calibration_priors left empty. Row two reads back right to left: stories.md, four to eight tellable stories with the numbers attached; a voice agent gate that points the user at their own and leaves is_mine false until they have one; scaffold, writing job_search.md and companies.md and running the toolchain check; and verify and hand off, where every check is reported including the passes." src="../../../../docs/diagrams/phase-onboard-light.svg">
</picture>

An interview, not a form. Runs once. Everything downstream reads what it wrote.

Two of those steps are gates rather than work, and both are refusals.

The voice-agent step refuses to build a voice profile itself. An ad-hoc profile
assembled from a few writing samples reads as the model's default wearing the
user's name, and the user will trust it precisely because it looks finished. So
it sets `voice.is_mine: false` and routes to
[written-voice-replication](https://github.com/aaddrick/written-voice-replication).
Shipping a plausible fake is worse than shipping nothing.

The verification step states which checks *passed*, not only which failed. A
check that reports only failures is indistinguishable from a check that never
ran, and there is no interpreter here to prove it ran.

`calibration_priors` is left empty deliberately. An invented prior is a
constraint the user never chose, silently killing roles for a reason they cannot
inspect. Empty, or real. Never plausible.

## `/slushpile:job-board-search`

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../../../docs/diagrams/phase-search-dark.svg">
  <img alt="The job board search phases. Row one: discovery, finding the careers URL and running several queries before triaging on titles; capture verbatim, taking the posting as written rather than summarized; pool estimation, characterizing who else applies as p50, p75 and p90 archetypes; and the fit score, where the pool percentile rather than the keyword match is the number. Row two reads back right to left: the channel expected-value matrix across cold, referral, outreach and inbound, where the tier is the best channel actually available; kill criteria on compensation, location and clearance, checked and stated either way; a contrarian gate that runs before tiers are final and can demote a tier or kill a role; and role folders, one per role with a job description and analysis, plus the tracker and companies file updated." src="../../../../docs/diagrams/phase-search-light.svg">
</picture>

Highest return in the system. Everything downstream costs the user an afternoon
per application. This costs minutes and is allowed to terminate with "do not
apply to any of these".

The posting is captured **verbatim**. 3 agents parse that text directly later on:
the requirements analyst, the ATS simulator, the pool analyst. Summarize it and
you silently delete the exact qualification wording those three exist to check.
The eval still runs. It just runs on a document that no longer contains the thing
being evaluated.

The contrarian gate runs *before* tiers are finalized, not after. A tier list the
user has already read is a tier list they have already committed to. Anchoring is
real, it is well documented, and ordering is the only mitigation that works. See
[scoring.md](scoring.md).

## `/slushpile:application-builder`

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../../../docs/diagrams/phase-build-dark.svg">
  <img alt="The application builder phases. Row one: angle, choosing the base resume, thesis, hook and the one story worth telling; resume, adapted then compiled, reading the extracted text rather than the source; cover letter, written by the voice agent named in preferences.yaml; and humanize, running removing-ai-tells with the orchestrator gating each change. Row two reads back right to left: adversarial review round one, producing an ATS score, swap tests and expected value per channel; fix, mechanical corrections first and then depth drawn from profile.md; adversarial review round two, whose decision gate reads the highest-expected-value channel verdict, joined to fix by a dashed loop labelled three rounds maximum; and finish, the final build with application.yaml, the profile and the tracker updated." src="../../../../docs/diagrams/phase-build-light.svg">
</picture>

Write, then attack what you wrote.

A model asked whether its own draft is good returns yes, at length, with
structure. So the builder never asks. It hands the materials to an evaluator with
no stake in them. Self-assessment is not a weak eval, it is not an eval.

Fix ordering is deliberate. Mechanical first: missing keywords, year-only dates, a
bullet lifted near-verbatim from the posting. Cheap, unambiguous, no judgment
required. Only then the expensive class, where a thin section has to be filled
from `profile.md`.

And if the material genuinely is not in the profile, it runs
`/slushpile:explore-experience` instead of inventing it. That is the one failure
this pipeline cannot ship. Hallucinated experience in a document you will be
interviewed on is not a bug in the output, it is a bug in your next conversation
with a human being.

**Three rounds is the ceiling.**

Verdict has not moved by round three? The gap is structural and more editing is
motion. The cap exists because the alternative is a loop that always finds
something, and a review that always finds something is indistinguishable from one
that finds nothing.

## `/slushpile:adversarial-review`

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../../../docs/diagrams/phase-review-dark.svg">
  <img alt="The adversarial review. Gather materials first: pdftotext the compiled PDF, plus the job description, role analysis, preferences.yaml and job_search.md. These feed a container holding 5 blind specialists dispatched in one message, none seeing another's report: the triage screener at eleven seconds with the resume only, the requirements analyst at thirty seconds checking every qualification, the ATS simulator as a parser rather than a reader, the fatigued reader on application sixty-one of eighty, and the pool analyst asking who else is in the queue. An edge labelled all five return leads to the hiring manager, which sees all five reports and produces one verdict per channel with quality scored apart from expected value. Then the contrarian, which sees everything including the hiring manager and may overturn it, and is never optional. Then the gatekeeper, the orchestrator rather than an agent, which strikes false positives and out-of-scope kills and re-derives the net call, and re-runs the whole pipeline with fresh instances when the materials change. Last, present and record, prioritized by impact on the highest-expected-value channel rather than by which agent shouted loudest." src="../../../../docs/diagrams/phase-review-light.svg">
</picture>

One message, 5 in parallel, zero shared context.

Each gets only what its role would genuinely hold. The triage screener never sees
the cover letter, because a screener who read the letter is not a screener.

Then the gatekeeper, which is the orchestrating skill and not an agent. The
personas are tuned to be harsh and some of what they emit is wrong, so something
has to apply judgment to their output, and that something cannot be one of them.

[the-review.md](the-review.md) has the dispatch order, what each of the 7
reviewers is denied, and which findings the gatekeeper is allowed to strike.
