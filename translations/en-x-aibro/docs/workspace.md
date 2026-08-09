# The workspace

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../docs/workspace.md">English</a> ·
  <a href="../../zh-CN/docs/workspace.md">简体中文</a> ·
  <a href="../../es/docs/workspace.md">Español</a> ·
  <a href="../../pt-BR/docs/workspace.md">Português (BR)</a> ·
  <a href="../../vi/docs/workspace.md">Tiếng Việt</a> ·
  <strong>AI Bro</strong>
</p>

<!-- END GENERATED language-nav -->

Filesystem-as-memory.

No database. No account. No sync layer. No export button, because there is
nothing to export from. `/slushpile:onboard` runs in **your** directory and
everything this system knows about you is a file you can open in a text editor
and delete.

That is not a limitation we are spinning as a feature. It is the reason the
plugin can be updated, forked, or thrown away without touching a single thing
about you.

That directory holds your full employment history, your comp figures, and your
constraints. Private repository, or no repository. Onboarding will tell you that
and it will not initialize one for you, or add a remote. Inheriting a git remote
from a setup step is a decision nobody made.

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

**Not a resume.**

It is the corpus a resume gets sampled from. Several times longer than anything
you would ever send, because a resume is a selection and this is the thing being
selected from. Every stage that writes prose reads it.

Every number in it carries a baseline or is explicitly marked as not needing one.
"Cut latency 40%" is unusable until somebody knows 40% of what, and an
unattributed number is precisely the one you get asked about in an interview and
cannot answer. Unverified sources are marked `UNVERIFIED` rather than dropped,
because a number you have not confirmed is still worth having, and a number you
have silently confirmed to yourself is a liability.

It grows. Review flags a section thin, `/slushpile:explore-experience` interviews
you, what it finds commits here. Permanently. The next application initializes
from it.

That is the compounding part. Everything else in this repository is downstream of
this file.

### `preferences.yaml`

The machine-readable half. Compensation method and baseline, location and
relocation constraints, clearance and degree status, claimed differentiators,
voice agent, `calibration_priors`.

Two fields carry more weight than the rest:

```yaml
voice:
  agent: "your-name-voice"
  is_mine: true
```

While `is_mine` is false, every skill that drafts prose warns you before it runs.
See [Your voice agent](voice.md).

`calibration_priors` starts empty and stays empty until you have five or more
resolved applications on a channel.

Empty means the agents run shipped defaults and label their estimates
uncalibrated. That is correct behavior, not a gap. A prior fit to two outcomes
moves the scoring further from reality than no prior does, and it arrives looking
empirical. Fake precision that nobody labelled is the worst state this system can
be in.

### `stories.md`

Four to eight stories you can actually tell, numbers attached. The builder selects
one per application. The interview you eventually get runs on these.

### `job_search.md`

The tracker, and the long-term memory. Applications, outcomes, prior applications
per company, and a `Calibration` section that `/slushpile:status` rewrites from
your own results.

Prior application history at a company is read by the pool analyst and the
contrarian during a review. A prior rejection at a **higher** level is material:
the recruiter sees the whole applicant-tracking history, and a later application
at a lower level reads as a multi-level drop.

Nobody else models that, because nobody else remembers your last application.

### `companies.md`

One line per company you have ever looked at. A second search at the same company
initializes from what the first one found instead of paying for it twice.

## Role folders

`/slushpile:job-board-search` creates one folder per role that survives tiering:

```
applications/<Company>/<Function>/<Role>/
  job_description.md    the posting, captured verbatim
  role_analysis.md      pool position, channel EV, kill criteria, contrarian notes
  application.yaml      the record: verdicts, scores, channel used, outcome
  resume.tex            copied per role by the builder
  cover_letter.tex      copied per role by the builder
```

The posting is stored **verbatim**. Not summarized.

3 agents parse that text directly during a review. A paraphrase silently deletes
the exact qualification wording those three exist to check. Lossy compression at
the input layer is not a saving. It is a corrupted eval that still returns a
confident number.

`application.yaml` is what `/slushpile:status` reads to build the queue and
regress predictions against outcomes. It is also the file you update when
something happens: rejection, screen, interview, offer.

You have to do that part. The pipeline never submits anything and never sees a
reply, so this is the one input it cannot generate for itself. Skip it and the
calibration loop never closes, which means the system stops compounding and
becomes a very well-architected stateless tool.

Templates are copied **into each role folder** rather than kept at the workspace
root. A pristine root copy becomes a stale copy the moment the first application
diverges from it.

## What the plugin never holds

Nothing in `skills/` or `agents/` hardcodes a fact about you. No compensation
floor. No location. No clearance status. No employer.

A skill that needs one reads it from `preferences.yaml` at run time, and a CI gate
fails the build if a personal fact leaks into the plugin. Not a guideline. A test
that goes red.

That separation is what makes the workspace portable and the plugin updatable.
Reinstall, fork, or update slushpile without touching anything about yourself.
See [Personal data](architecture/personal-data.md).
