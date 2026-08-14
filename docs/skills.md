# Skills

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <strong>English</strong> ·
  <a href="../translations/zh-CN/docs/skills.md">简体中文</a> ·
  <a href="../translations/es/docs/skills.md">Español</a> ·
  <a href="../translations/pt-BR/docs/skills.md">Português (BR)</a> ·
  <a href="../translations/vi/docs/skills.md">Tiếng Việt</a> ·
  <a href="../translations/en-x-aibro/docs/skills.md">AI Bro</a>
</p>

<!-- END GENERATED language-nav -->

Slushpile installs as ten skills. Claude Code exposes each as
`/slushpile:<name>`; Codex uses `$slushpile:<name>`; Gemini CLI and other
harnesses read the same files and you ask for the stage in words.

Three of them are the spine. Three more are dispatched for you in the course of
building an application, and you only run them by hand on materials this
pipeline did not build. The last four you run when they apply, in any order.

## The spine

### `/slushpile:onboard`

Sets up the workspace. Ingests an existing resume or LinkedIn export, interviews
you for the gaps, and writes `profile.md`, `preferences.yaml`, and `stories.md`.
Checks the document toolchain, scaffolds the tracker, and hands off.

Run once per workspace, before anything else. See
[Getting started](getting-started.md) for what to have ready and
[The workspace](workspace.md) for what it writes.

### `/slushpile:job-board-search`

Searches a careers board, extracts each posting verbatim, estimates the
realistic applicant pool, scores pool-anchored and channel-conditional fit, runs
the kill criteria, puts a contrarian in front of the tier list, and creates a
role folder per surviving role.

**Argument:** a company name, or a query describing the work and where you want
it. Given a query, Phase 0 resolves it into a company list — reading your
constraints from `preferences.yaml` and your history from `companies.md` — shows
you that list, and searches it once you confirm. Everything after Phase 0 is the
same either way, so an assessment from a query run is comparable against one
from a named-company run and the calibration table can pool them.

This is the highest-return stage in the pipeline and the one most tools do not
have. Everything after it costs an afternoon per application; this costs minutes
and can end with "none of these". See [Scoring](architecture/scoring.md).

### `/slushpile:application-builder`

Builds the targeted resume and cover letter for a role folder that already has a
job description and a role analysis, then iterates them against the review until
they stabilize or hit the three-round cap.

**Argument:** a role folder path.

It dispatches `explore-experience`, `adversarial-review`, and
`removing-ai-tells` itself. It never submits anything; it hands you finished
files.

## The three dispatched for you

Run one of these directly only to work on materials this pipeline did not build
— a resume written elsewhere, a letter drafted by hand.

### `/slushpile:adversarial-review`

Runs seven personas against a resume and cover letter. Returns a verdict and a
probability range per submission channel, materials quality scored separately
from expected value, and a contrarian pass that can overturn the rest.

**Argument:** a role folder path containing at minimum a resume and
`job_description.md`.

See [The review](architecture/the-review.md) for what each persona is shown and
what it is deliberately withheld.

### `/slushpile:explore-experience`

Interviews you to surface experience that is real but undocumented, mapped
against a specific role's requirements, then writes it into `profile.md`
permanently.

Use when a fit assessment or a review flags a section as thin. Most of the time
the experience turns out to be real and simply never written down, which is why
this is an interview rather than a rewrite.

### `/slushpile:removing-ai-tells`

Strips phrasing, structure, and word choices that signal AI authorship, running
iterative passes through fresh voice-agent instances with the orchestrator
gating every individual change.

Use on a cover letter before submission, or on any prose that has to read as
human-written.

## Any time

### `/slushpile:outreach`

Opens the warm channel for one role. Reads the Referrals table and your profile
for people you already know at the company, asks you the question no file can
answer, researches named targets from public professional presence only when you
know nobody, grades each path by what that person could actually say about your
work, and drafts the referral ask or the cold note through your voice agent.

**Argument:** a role folder path.

Run it where the assessment says the referral converts several times better than
cold submission and you have no referrer. Without it the pipeline computes that
your best channel is a referral, tells you so, and then builds cold-portal
materials anyway. It writes the contacts into `job_search.md`, which is where
the review reads them from — until a row exists there, every review of every
role at that company prices the warm channel as unavailable, correctly.

It never sends anything. The messages are yours to send, from your own account.

### `/slushpile:redesign-templates`

Restyles `resume.tex` and `cover_letter.tex` into your own house style —
typography, palette, layout — while holding the ATS constraints fixed, then
proves the result still compiles and still extracts.

Run this rather than editing the plugin checkout, which the next update
replaces.

### `/slushpile:status`

Reads every `application.yaml` in the workspace and reports the state of the
search: the ranked queue, what is waiting on you, what has gone quiet, and the
regression of the pipeline's own predictions against what actually happened.
Writes the calibration findings back into `job_search.md` and
`preferences.yaml`.

Run it after outcomes land. See
[Memory and calibration](architecture/memory-and-calibration.md).

### `/slushpile:help`

Explains what slushpile is, what each skill does, what order to run them in,
where the workspace files live, and how to set up a voice agent.

Run it when you are not sure what to run.
