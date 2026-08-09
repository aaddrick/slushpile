# Memory and calibration

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <strong>English</strong> ·
  <a href="../../translations/zh-CN/docs/architecture/memory-and-calibration.md">简体中文</a> ·
  <a href="../../translations/es/docs/architecture/memory-and-calibration.md">Español</a> ·
  <a href="../../translations/pt-BR/docs/architecture/memory-and-calibration.md">Português (BR)</a> ·
  <a href="../../translations/vi/docs/architecture/memory-and-calibration.md">Tiếng Việt</a>
</p>

<!-- END GENERATED language-nav -->

A job search is forty applications over three months. A tool with no memory
charges full price for every one of them: you paste a resume in, get a number
back, close the tab, and the tool ends the session knowing exactly what it knew
at the start.

Slushpile's memory is a directory of files the user owns. There is no database,
no account, and no state inside the plugin — the plugin is public code and the
workspace is the user's employment history, so they are different things kept in
different places. See [personal-data.md](personal-data.md).

## What is durable

| File | Written by | Read by |
| --- | --- | --- |
| `profile.md` | `onboard`, extended by `explore-experience` and `application-builder` | every stage that writes prose |
| `preferences.yaml` | `onboard`, corrected by `status` | scoring, kill criteria, the review's dispatch |
| `stories.md` | `onboard` | the builder, when it picks the one story to tell |
| `job_search.md` | `job-board-search`, `application-builder`, `status` | the pool analyst, the contrarian, the queue |
| `companies.md` | `job-board-search` | later searches at the same company |
| `applications/<company>/<role>/` | `job-board-search`, then the builder | the review, and `status` |

`profile.md` is not a resume. It is the pool a resume is cut from, several times
longer than anything anyone would send, and its value is that nothing ever asks
the user those questions twice.

## The write-back paths

Three of them, and each exists because something learned in one stage is useless
if it stays there.

**Review finding → profile.** When a review says a section is thin, the
interview that follows usually finds the experience was real and the user had
never written it down. `explore-experience` surfaces it and it goes into
`profile.md` permanently, where every later application can draw on it. This is
the path that makes the twentieth application start from a better place than the
first.

**Outcome → tracker.** The user records what happened: no response, screen,
interview, offer, rejection, and at which stage. Nothing else in the pipeline
can produce this, because the pipeline never submits anything and never sees a
reply.

**Tracker → priors.** `status` regresses the pipeline's own predictions against
those outcomes and writes the correction into `preferences.yaml`.

## Why the correction goes into user data

The obvious place to record "this pipeline is 12 points optimistic about cold
submissions to frontier labs" is in the agent that made the estimate. That is
the wrong place, and quietly so: agent definitions ship with the plugin, so an
edit there is reverted by the next update without warning, leaving a pipeline
that *was* tuned and no longer is.

So the correction goes to `preferences.yaml`, which the user owns and no update
touches. `job-board-search` reads `calibration_priors` at scoring time, and
`adversarial-review` passes the block to the pool analyst and the contrarian at
dispatch.

## The rules that keep calibration honest

**Five resolved applications is the floor.** Below that, `status` prints the
counts and says the sample is too small to regress rather than producing a
table. A rate computed from two outcomes is noise wearing the costume of
calibration, and once it is in a table nobody remembers the denominator.

**Silence counts as a rejection.** An application submitted more than 30 days
ago with no response is recorded as `no_response`, not left pending. Excluding
those is the single largest source of optimism available to a table like this.
The count inferred that way is reported.

**Grade against the channel actually used.** Verdicts are grouped by the verdict
for the channel the application actually went through, never the best-case one.
Grading a cold submission against its warm-referral verdict is how a pipeline
convinces itself it was right.

**Both directions of error are reported.** An INTERVIEW verdict that
auto-rejected inside 72 hours means the review missed something a filter caught
in seconds. A REJECT that converted means the review was too harsh — and every
role it talked the user out of since then is a cost that appears nowhere else.
Only one of those two is comfortable to report, which is why the rule names
both.

**The finding names a segment, a direction, and a size.** "The pipeline is
miscalibrated" is unactionable and no agent can consume it. "INTERVIEW verdicts
on cold submissions to frontier labs converted 0 of 7, against an estimated 12%"
can be written into a prior and acted on.

**A null prior is a valid answer.** Only rates backed by five or more resolved
applications on that channel are written. Everything else stays null, the agents
use their shipped defaults, and they label the estimate uncalibrated. A prior
computed from two outcomes moves the scoring further from reality than no prior
does, and it arrives wearing the authority of an empirical number.

**The diff is shown before `preferences.yaml` is written.** It is the user's
constraints file and the change alters how every future assessment scores. A
scoring change nobody was told about is indistinguishable from the pipeline
drifting on its own.
