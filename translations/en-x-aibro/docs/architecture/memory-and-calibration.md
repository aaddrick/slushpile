# Memory and calibration

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../../docs/architecture/memory-and-calibration.md">English</a> ·
  <a href="../../../zh-CN/docs/architecture/memory-and-calibration.md">简体中文</a> ·
  <a href="../../../es/docs/architecture/memory-and-calibration.md">Español</a> ·
  <a href="../../../pt-BR/docs/architecture/memory-and-calibration.md">Português (BR)</a> ·
  <a href="../../../vi/docs/architecture/memory-and-calibration.md">Tiếng Việt</a> ·
  <strong>AI Bro</strong>
</p>

<!-- END GENERATED language-nav -->

A job search is forty applications over three months.

A stateless tool charges full price for all forty. Paste, score, close the tab,
process terminates knowing exactly what it knew at init. Forty cold starts.

That is not a workflow. That is a subscription.

Slushpile's memory is a directory of files the user owns. No database, no account,
no state inside the plugin. The plugin is public code, the workspace is the user's
employment history, and those are different assets that live in different places.
See [personal-data.md](personal-data.md).

## What is durable

| File | Written by | Read by |
| --- | --- | --- |
| `profile.md` | `onboard`, extended by `explore-experience` and `application-builder` | every stage that writes prose |
| `preferences.yaml` | `onboard`, corrected by `status` | scoring, kill criteria, the review's dispatch |
| `stories.md` | `onboard` | the builder, when it picks the one story to tell |
| `job_search.md` | `job-board-search`, `application-builder`, `status` | the pool analyst, the contrarian, the queue |
| `companies.md` | `job-board-search` | later searches at the same company |
| `applications/<company>/<role>/` | `job-board-search`, then the builder | the review, and `status` |

`profile.md` is not a resume. It is the corpus a resume is sampled from, several
times longer than anything anyone would send, and the whole return on it is that
nothing ever asks the user those questions twice.

## Three write-back paths

Each one exists because something learned in one stage is dead weight if it stays
there.

**Review finding → profile.** A review flags a section thin. The interview that
follows finds the experience was real and never captured. `explore-experience`
surfaces it, it commits to `profile.md` permanently, every later application draws
on it.

That is the path that makes application twenty initialize from a better state than
application one. It is the whole compounding argument, and it is four files and a
convention, not a platform.

**Outcome → tracker.** The user records what happened: no response, screen,
interview, offer, rejection, and at which stage.

This is the one input the system cannot generate for itself, because the pipeline
never submits anything and never sees a reply. Which makes it the one step you
cannot skip. Skip it and everything below stops working, quietly.

**Tracker → priors.** `status` regresses the pipeline's predictions against those
outcomes and writes the correction into `preferences.yaml`.

## Why the correction goes into user data

The obvious place to record "this pipeline is 12 points optimistic about cold
submissions to frontier labs" is the agent that made the estimate.

Wrong layer, and wrong in the quiet way. Agent definitions ship with the plugin.
An edit there is reverted by the next update with no warning, leaving a pipeline
that *was* tuned and silently is not.

So the correction goes to `preferences.yaml`, which the user owns and no update
touches. `job-board-search` reads `calibration_priors` at scoring time.
`adversarial-review` passes the block to the pool analyst and the contrarian at
dispatch.

State with the user. Code with the plugin. Keep that boundary clean and updates
stop being destructive events.

## The rules that keep calibration honest

**Five resolved applications is the floor.** Below it, `status` prints counts and
says the sample is too small rather than emitting a table. A rate computed from
two outcomes is noise in the costume of calibration, and once it is in a table
nobody remembers the denominator.

**Silence is a rejection.** Submitted more than 30 days ago, no response,
`no_response`. Not pending. Excluding those is the single largest available source
of optimism in a table like this, and it is entirely self-inflicted. The count
inferred that way is reported.

**Grade against the channel actually used.** Never the best-case one. Grading a
cold submission against its warm-referral verdict is how a pipeline convinces
itself it was right all along.

**Both directions of error get reported.** An INTERVIEW that auto-rejected inside
72 hours means the review missed something a filter caught in seconds. A REJECT
that converted means the review was too harsh, and every role it talked you out of
since then is a cost that appears in no other metric.

One of those two is comfortable to report. That is exactly why the rule names
both.

**The finding names a segment, a direction, and a size.** "The pipeline is
miscalibrated" is unactionable and no agent can consume it. "INTERVIEW verdicts on
cold submissions to frontier labs converted 0 of 7, against an estimated 12%" can
be written into a prior and acted on.

**A null prior is a valid answer.** Only rates backed by five or more resolved
applications on that channel get written. Everything else stays null, agents run
shipped defaults, estimates are labelled uncalibrated. A prior fit to two outcomes
moves the scoring further from reality than no prior does, and it arrives wearing
the authority of an empirical number.

**The diff is shown before `preferences.yaml` is written.** It is the user's
constraints file and the change alters how every future assessment scores. A
scoring change nobody was told about is indistinguishable from the pipeline
drifting on its own.
