# The pipeline, stage by stage

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <strong>English</strong> ·
  <a href="../../translations/zh-CN/docs/architecture/pipeline.md">简体中文</a> ·
  <a href="../../translations/es/docs/architecture/pipeline.md">Español</a> ·
  <a href="../../translations/pt-BR/docs/architecture/pipeline.md">Português (BR)</a> ·
  <a href="../../translations/vi/docs/architecture/pipeline.md">Tiếng Việt</a>
</p>

<!-- END GENERATED language-nav -->

## The whole loop

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../diagrams/pipeline-overview-dark.svg">
  <img alt="Slushpile end to end. Row one, left to right: onboard, which interviews and ingests a resume to write profile, preferences and stories; job board search, which extracts postings verbatim and scores pool-anchored fit and channel expected value; application builder, which produces the angle, resume, letter, voice pass and humanize step; and adversarial review, seven personas of which five are blind, returning a verdict per channel. Builder and review are joined by a bidirectional arrow labelled up to three rounds. The flow drops from review to a blue box, you send it, noting that no skill touches a portal, an email or a form. Row two reads back right to left: outcome recorded, then status, which compares the pipeline's predictions against outcomes, then a dashed arrow labelled priors into the workspace box holding profile.md, preferences.yaml, stories.md and job_search.md. A dashed arrow joins the workspace back to onboard, labelled written by onboarding, read by every stage." src="../diagrams/pipeline-overview-light.svg">
</picture>

Three commands make up the spine: `onboard` once per workspace, then
`job-board-search` and `application-builder` per company and per role. The
builder dispatches `explore-experience`, `adversarial-review`, and
`removing-ai-tells` itself.

The loop at the bottom is the part that has no equivalent in a resume
optimizer. Outcomes get recorded, `status` regresses what the pipeline
predicted against what happened, and the corrected priors go back into
`preferences.yaml`, where the next search reads them. See
[memory-and-calibration.md](memory-and-calibration.md).

## Legend

Every diagram on this page draws from one class vocabulary, defined in
`docs/diagrams/theme-light.d2` and `theme-dark.d2`. The two theme files and this
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

The distinction between `stage` and `agent` is the one worth reading carefully.
An `agent` box is a subagent with its own definition and its own context. On a
harness that cannot dispatch subagents, those are what collapse into one
context, and that collapse is the whole difference between a full run and a
degraded one.

## `/slushpile:onboard`

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../diagrams/phase-onboard-dark.svg">
  <img alt="The onboarding phases. Row one: ingest a resume in any format or a LinkedIn export; interview for the gaps a document cannot fill, with numbers given baselines; profile.md, described as the pool a resume is cut from rather than a resume; preferences.yaml, holding the compensation method and constraints, with calibration_priors left empty. Row two reads back right to left: stories.md, four to eight tellable stories with the numbers attached; a voice agent gate that points the user at their own and leaves is_mine false until they have one; scaffold, writing job_search.md and companies.md and running the toolchain check; and verify and hand off, where every check is reported including the passes." src="../diagrams/phase-onboard-light.svg">
</picture>

Onboarding is an interview, not a form. It runs once and everything after it
reads what it wrote.

Two of its steps are gates rather than work. The voice-agent step refuses to
build a voice profile itself — an ad-hoc profile assembled from a few writing
samples reads as the model's default wearing the user's name, and the user will
trust it because it looks finished. It sets `voice.is_mine: false` and points at
[written-voice-replication](https://github.com/aaddrick/written-voice-replication)
instead. The verification step states which checks *passed*, not only which
failed, because a check that reports only failures is indistinguishable from one
that never ran.

`calibration_priors` is left empty deliberately. An invented prior is a
constraint the user never chose, silently killing roles for a reason they cannot
see. It fills in from real outcomes later, or it stays empty and every estimate
downstream is labelled uncalibrated.

## `/slushpile:job-board-search`

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../diagrams/phase-search-dark.svg">
  <img alt="The job board search phases. Row one: discovery, finding the careers URL and running several queries before triaging on titles; capture verbatim, taking the posting as written rather than summarized; pool estimation, characterizing who else applies as p50, p75 and p90 archetypes; and the fit score, where the pool percentile rather than the keyword match is the number. Row two reads back right to left: the channel expected-value matrix across cold, referral, outreach and inbound, where the tier is the best channel actually available; kill criteria on compensation, location and clearance, checked and stated either way; a contrarian gate that runs before tiers are final and can demote a tier or kill a role; and role folders, one per role with a job description and analysis, plus the tracker and companies file updated." src="../diagrams/phase-search-light.svg">
</picture>

This is the stage with the highest return, and it is the one most tools do not
have. Everything downstream costs the user an afternoon per application. This
stage costs minutes and can end with "do not apply to any of these".

The posting is captured **verbatim**. Three agents later parse that text
directly — the requirements analyst, the ATS simulator, and the pool analyst —
and a summarized posting silently removes the exact qualification wording those
three exist to check.

The contrarian gate runs *before* tiers are finalized rather than after, because
a tier list the user has already read is a tier list they have already committed
to. See [scoring.md](scoring.md) for what the tiers mean and what the kill
criteria check.

## `/slushpile:application-builder`

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../diagrams/phase-build-dark.svg">
  <img alt="The application builder phases. Row one: angle, choosing the base resume, thesis, hook and the one story worth telling; resume, adapted then compiled, reading the extracted text rather than the source; cover letter, written by the voice agent named in preferences.yaml; and humanize, running removing-ai-tells with the orchestrator gating each change. Row two reads back right to left: adversarial review round one, producing an ATS score, swap tests and expected value per channel; fix, mechanical corrections first and then depth drawn from profile.md; adversarial review round two, whose decision gate reads the highest-expected-value channel verdict, joined to fix by a dashed loop labelled three rounds maximum; and finish, the final build with application.yaml, the profile and the tracker updated." src="../diagrams/phase-build-light.svg">
</picture>

The builder writes, then attacks what it wrote. A model asked whether its own
draft is good will say yes at length, so the builder never asks — it hands the
materials to a review that has no stake in them.

The order of the fixes matters. Mechanical fixes come first because they are
cheap and unambiguous: missing keywords, year-only dates, a bullet lifted
near-verbatim from the posting. Only then does it attempt the expensive kind,
where a thin section has to be filled from `profile.md` — and where, if the
material genuinely is not in the profile, it runs `/slushpile:explore-experience`
rather than inventing it.

**Three rounds is the ceiling.** If the verdict has not moved by round three the
gap is structural, and further editing is motion rather than progress. The cap
exists because the alternative is a loop that always finds something, and a
review that always finds something is indistinguishable from one that finds
nothing.

## `/slushpile:adversarial-review`

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../diagrams/phase-review-dark.svg">
  <img alt="The adversarial review. Gather materials first: pdftotext the compiled PDF, plus the job description, role analysis, preferences.yaml and job_search.md. These feed a container holding five blind specialists dispatched in one message, none seeing another's report: the triage screener at eleven seconds with the resume only, the requirements analyst at thirty seconds checking every qualification, the ATS simulator as a parser rather than a reader, the fatigued reader on application sixty-one of eighty, and the pool analyst asking who else is in the queue. An edge labelled all five return leads to the hiring manager, which sees all five reports and produces one verdict per channel with quality scored apart from expected value. Then the contrarian, which sees everything including the hiring manager and may overturn it, and is never optional. Then the gatekeeper, the orchestrator rather than an agent, which strikes false positives and out-of-scope kills and re-derives the net call, and re-runs the whole pipeline with fresh instances when the materials change. Last, present and record, prioritized by impact on the highest-expected-value channel rather than by which agent shouted loudest." src="../diagrams/phase-review-light.svg">
</picture>

The five specialists in the container are dispatched in a single message and
cannot see each other's findings. Each is given only what its role would
genuinely have: the triage screener is never shown the cover letter, because a
screener who read the letter is not a screener.

The gatekeeper is the orchestrating skill, not an agent. The personas are
deliberately harsh and some of what they produce is wrong, so something has to
apply judgment to their output — and that something cannot be one of them.

[the-review.md](the-review.md) covers the dispatch order, what each persona is
withheld, and which findings the gatekeeper is allowed to strike.
