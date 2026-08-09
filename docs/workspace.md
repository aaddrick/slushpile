# The workspace

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <strong>English</strong> ·
  <a href="../translations/zh-CN/docs/workspace.md">简体中文</a> ·
  <a href="../translations/es/docs/workspace.md">Español</a> ·
  <a href="../translations/pt-BR/docs/workspace.md">Português (BR)</a> ·
  <a href="../translations/vi/docs/workspace.md">Tiếng Việt</a> ·
  <a href="../translations/en-x-aibro/docs/workspace.md">AI Bro</a>
</p>

<!-- END GENERATED language-nav -->

`/slushpile:onboard` runs in **your** directory, not in the plugin checkout, and
everything the pipeline knows about you lives there.

That directory will contain your full employment history, your compensation
figures, and your constraints. Keep it in a **private** repository, or in no
repository at all. Onboarding will say this to you and it will not initialize
one for you, or add a remote — that is a decision to make deliberately rather
than to inherit from a setup step.

## What onboarding writes

```
profile.md          every factual claim about you
preferences.yaml    compensation, location, constraints, calibration priors
stories.md          four to eight tellable stories, with the numbers attached
job_search.md       the tracker: applications, outcomes, calibration
companies.md        one line per company ever looked at
applications/       one folder per role, created by job-board-search
```

### `profile.md`

**Not a resume.** It is the pool a resume gets cut from — several times longer
than anything you would ever send, because a resume is a selection and this is
the thing selected from.

Every number in it carries a baseline or is explicitly marked as not needing
one. "Cut latency 40%" is unusable until the reader knows 40% of what, and an
unattributed number is the one you will be asked about in an interview and
cannot answer. Numbers whose source is unverified are marked `UNVERIFIED` rather
than dropped.

It grows. When a review says a section is thin,
`/slushpile:explore-experience` interviews you and writes what it finds back
here, so the next application starts from it.

### `preferences.yaml`

The machine-readable half. Compensation method and baseline, location and
relocation constraints, clearance and degree status, your claimed
differentiators, your voice agent, and `calibration_priors`.

Two fields do more work than the rest:

```yaml
voice:
  agent: "your-name-voice"
  is_mine: true
```

While `is_mine` is false, every skill that drafts prose warns you before it
runs. See [Your voice agent](voice.md).

`calibration_priors` starts empty and stays empty until you have five or more
resolved applications on a channel. An empty prior means the agents use their
shipped defaults and label their estimates uncalibrated, which is the correct
behaviour — a prior computed from two outcomes moves the scoring further from
reality than no prior does, and it arrives looking empirical.

### `stories.md`

Four to eight stories you can actually tell, with the numbers attached. The
builder picks one per application; the interview you eventually get runs on
these.

### `job_search.md`

The tracker, and the pipeline's long-term memory. Applications, their outcomes,
prior applications per company, and a `Calibration` section that
`/slushpile:status` rewrites from your own results.

Prior application history at a company is read by the pool analyst and the
contrarian during a review. A prior rejection at a **higher** level matters
materially: the recruiter sees the whole applicant-tracking history, and a later
application at a lower level reads as a multi-level drop.

### `companies.md`

One line per company you have ever looked at, so a second search at the same
company starts from what the first one found.

## Role folders

`/slushpile:job-board-search` creates one folder per role that survives the
tiering:

```
applications/<Company>/<Function>/<Role>/
  job_description.md    the posting, captured verbatim
  role_analysis.md      pool position, channel EV, kill criteria, contrarian notes
  application.yaml      the record: verdicts, scores, channel used, outcome
  resume.tex            copied per role by the builder
  cover_letter.tex      copied per role by the builder
```

The posting is stored **verbatim**, not summarized. Three agents parse that text
directly during a review, and a paraphrase silently removes the exact
qualification wording they exist to check.

`application.yaml` is the file `/slushpile:status` reads to build the queue and
to regress predictions against outcomes. It is also the file to update when
something happens: a rejection, a screen, an interview, an offer. Nothing else
in the pipeline can learn that, because the pipeline never submits anything and
never sees a reply.

The templates are copied **into each role folder** rather than kept at the
workspace root. A pristine copy at the root becomes a stale copy the moment the
first application diverges from it.

## What the plugin never holds

Nothing in `skills/` or `agents/` hardcodes a fact about you. No compensation
floor, no location, no clearance status, no employer. A skill that needs one of
those reads it from `preferences.yaml` at run time, and a CI gate fails the
build if a personal fact leaks into the plugin.

That is what makes the workspace portable and the plugin updatable: you can
reinstall, fork, or update slushpile without touching anything about yourself.
See [Personal data](architecture/personal-data.md).
