# Skills

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../docs/skills.md">English</a> ·
  <a href="../../zh-CN/docs/skills.md">简体中文</a> ·
  <a href="../../es/docs/skills.md">Español</a> ·
  <a href="../../pt-BR/docs/skills.md">Português (BR)</a> ·
  <a href="../../vi/docs/skills.md">Tiếng Việt</a> ·
  <strong>AI Bro</strong>
</p>

<!-- END GENERATED language-nav -->

10 skills. One surface, four runtimes.

Claude Code exposes each as `/slushpile:<name>`. Codex uses `$slushpile:<name>`.
Gemini CLI and everything else read the same files and you ask for the stage in
words. Same Markdown, every harness. No adapter layer, because there is nothing
to adapt.

Three are the spine. Three are dispatched for you mid-build and you only invoke
them by hand on materials this pipeline did not produce. Four run whenever they
apply, in any order.

## The spine

### `/slushpile:onboard`

Stands up the workspace. Ingests a resume or a LinkedIn export, interviews you
for the gaps, writes `profile.md`, `preferences.yaml`, and `stories.md`. Checks
the toolchain, scaffolds the tracker, hands off.

Once per workspace, before anything else. See
[Getting started](getting-started.md) for what to bring and
[The workspace](workspace.md) for what it writes.

This is the only stage that builds the substrate. Everything after it is
downstream of how well this went.

### `/slushpile:job-board-search`

Searches a company's careers board. Extracts each posting verbatim. Estimates the
realistic applicant pool. Scores pool-anchored and channel-conditional fit. Runs
the kill criteria. Puts a contrarian in front of the tier list. Creates a role
folder per surviving role.

**Argument:** a company name, or a query describing the work and where you want
it.

Given a query, Phase 0 resolves it into a company list before anything gets
searched. It reads your constraints out of `preferences.yaml` and your history
out of `companies.md`, shows you the list, and searches it only once you confirm.
One human checkpoint, at the cheapest possible moment.

Everything after Phase 0 is identical in both modes, which is the part that
matters. An assessment from a query run is comparable against one from a
named-company run, so the calibration table pools them instead of accumulating
two incompatible histories of the same search.

Highest return in the system. Nothing else in this category has this stage at
all, and that is not an oversight on their part, it is the business model:
everything downstream of "yes, apply" is billable and this stage says no.

Everything after it costs you an afternoon per application. This costs minutes
and is allowed to terminate with "none of these". See
[Scoring](architecture/scoring.md).

### `/slushpile:application-builder`

Builds the targeted resume and cover letter for a role folder that already has a
job description and a role analysis, then iterates them against the review until
they stabilize or hit the three-round cap.

**Argument:** a role folder path.

It dispatches `explore-experience`, `adversarial-review`, and
`removing-ai-tells` itself. Write, attack, patch, converge.

It never submits anything. It hands you artifacts.

## The three dispatched for you

Invoke these directly only for materials this pipeline did not build. A resume
written elsewhere. A letter drafted by hand.

### `/slushpile:adversarial-review`

7 reviewers against a resume and cover letter. Verdict and probability range per
submission channel. Materials quality scored independently of expected value. A
contrarian pass with authority to overturn the rest.

**Argument:** a role folder path containing at minimum a resume and
`job_description.md`.

Context isolation is the design, not an implementation detail. See
[The review](architecture/the-review.md) for what each persona is shown and,
more importantly, what it is denied.

### `/slushpile:explore-experience`

Interviews you to surface experience that is real and undocumented, mapped
against a specific role's requirements, then commits it to `profile.md`
permanently.

Run it when a fit assessment or a review flags a section as thin.

Nine times out of ten the experience is real and was never captured. That is why
this is an interview and not a rewrite. A rewrite of a thin section is a
hallucination with better formatting.

### `/slushpile:removing-ai-tells`

Strips phrasing, structure, and word choices that signal AI authorship. Iterative
passes through fresh voice-agent instances, orchestrator gating every individual
change.

Run it on a cover letter before submission, or on any prose that has to read as
human-written.

## Any time

### `/slushpile:outreach`

Opens the warm channel for one role. Reads the referrals table and your profile
for people you already know at the company. Asks you the one question no file
can answer. Researches named targets from public professional presence only when
you know nobody. Grades each path on what that person could actually say about
your work, then drafts the referral ask or the cold note through your voice
agent.

**Argument:** a role folder path.

Run it where the assessment prices a referral several times above cold
submission and you have no referrer. Without it the pipeline computes that your
highest-EV channel is a referral, surfaces that finding, and then ships
cold-portal materials anyway. Optimizing for the channel you can execute is not
the same as optimizing for the channel that converts.

Contacts land in `job_search.md`, which is the read path the review uses. Until
a row exists there, every review of every role at that company prices the warm
channel as unavailable. Correctly.

It never sends. The messages are yours, from your own account.

### `/slushpile:redesign-templates`

Restyles `resume.tex` and `cover_letter.tex` into your own house style.
Typography, palette, layout. ATS constraints held fixed, then proves the result
still compiles and still extracts.

Run this instead of editing the plugin checkout, which the next update
overwrites.

### `/slushpile:status`

Reads every `application.yaml` in the workspace. Reports the ranked queue, what
is blocked on you, what has gone quiet, and the regression of the pipeline's own
predictions against what actually happened. Writes the calibration findings back
into `job_search.md` and `preferences.yaml`.

Run it after outcomes land. This is the loop closing, and a loop that never
closes is just a pipeline with extra steps. See
[Memory and calibration](architecture/memory-and-calibration.md).

### `/slushpile:help`

What slushpile is, what each skill does, what order to run them in, where the
workspace files live, how to set up a voice agent.

Run it when you are not sure what to run.
