# The review

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <strong>English</strong> ·
  <a href="../../translations/zh-CN/docs/architecture/the-review.md">简体中文</a> ·
  <a href="../../translations/es/docs/architecture/the-review.md">Español</a> ·
  <a href="../../translations/pt-BR/docs/architecture/the-review.md">Português (BR)</a> ·
  <a href="../../translations/vi/docs/architecture/the-review.md">Tiếng Việt</a>
</p>

<!-- END GENERATED language-nav -->

`/slushpile:adversarial-review` dispatches seven personas against a resume and a
cover letter. This page is why it is shaped that way. The picture is in
[pipeline.md](pipeline.md); the per-agent definitions are in `agents/`.

## Four failure modes, four stages

The shape is not an arbitrary committee. Each stage answers a specific way that
a naive review pipeline produces confident nonsense.

**Single-perspective sycophancy.** Every reviewer in a naive pipeline works for
the candidate. None of them models the queue. The pool analyst exists to force
comparative reasoning: not "are these materials good" but "are they better than
the other seventy applications this requisition got this week".

**Verdict collapse.** One INTERVIEW / MAYBE / PASS answer hides that the same
materials convert at very different rates cold and through a referral. Those are
different decisions about the user's afternoon. The hiring manager produces one
verdict per channel, with a probability range rather than a word.

**Synthetic AI-detection concern.** An AI-detector persona flags patterns based
on hypothetical reader doubt, and it will override grounded judgment about what
a real reader notices. It is replaced by the fatigued reader, which asks the
answerable question: would this annoy someone on their sixty-first application
of the day?

**No falsification step.** Nothing in a normal review asks what would have to be
true for the whole exercise to be a waste of cycles. The contrarian asks it,
last, with permission to overturn everything upstream.

## The blind stage

The first five run in parallel, dispatched in a single message. None is given
another's output.

This is the load-bearing property of the whole review, and it is the one that
degrades quietly. Contamination does not produce an error; it produces
agreement. A specialist that has already read the triage verdict drifts toward
confirming it, and five reports that agree look like strong consensus rather
than like one opinion restated five times. Consensus across the blind stage is
the most reliable signal the pipeline produces, and it is only worth anything
because the five could not talk.

Each persona is given only what its role would genuinely have:

| Persona | Given | Withheld, and why |
| --- | --- | --- |
| Triage screener | Resume text, title, company, level | The cover letter. It is simulating eleven seconds, and a screener who read the letter is not one. |
| Requirements analyst | Resume, cover letter, full posting, level | Nothing. Its job is checking every qualification against evidence. |
| ATS simulator | Resume text, full posting, and the `.tex` or `.docx` source if there is one | Nothing, but note it gets the *source* on purpose: tables, columns and header placement are invisible in extracted text and are exactly what it exists to catch. |
| Fatigued reader | Resume, cover letter | Any instruction to judge AI authorship. That is a different question and it is not this one's. |
| Pool analyst | Everything, plus prior application history and the observed conversion rates | Nothing. It needs the most context of the five. |

The resume every persona reads is `pdftotext` output, not the LaTeX or Markdown
source. Reviewing the source is reviewing a document nobody will ever see. If
the extracted text comes out empty or scrambled, that is a finding rather than a
tooling failure: an ATS sees what `pdftotext` sees.

## Why the last two are sequential

The hiring manager runs after all five return, and sees all five. The contrarian
runs after the hiring manager, and sees everything including it.

Ordering them this way costs wall-clock time and buys the one thing the blind
stage cannot provide: someone who can weigh the five against each other, and
then someone who can attack that weighing. A contrarian that ran in parallel
with the hiring manager would be arguing with a synthesis it never read.

The contrarian is **automatic, not conditional**. A falsification step that runs
only when the orchestrator feels uncertain will skip itself in exactly the cases
where certainty was misplaced.

## Priors are passed verbatim, including when they are empty

Both the pool analyst and the contrarian receive the `calibration_priors` block
from `preferences.yaml` as written.

Summarizing it into "the candidate converts poorly" strips the sample size,
which is the only thing that says how much weight the number deserves. And
omitting the block when it is unset reads to the agent as an ordinary run rather
than an uncalibrated one — an uncalibrated estimate that is not labelled as one
is worse than no estimate, because downstream it is indistinguishable from a
calibrated one.

Where an observed rate has a sample size of five or more, the pool analyst is
instructed to use it in place of its own prior for that channel, and to say that
it did.

## The gatekeeper

The orchestrating skill is the gatekeeper. It is not one of the personas, and
that is deliberate: the personas are tuned to be harsh, some of what they
produce is wrong, and nothing tuned to be harsh can also be the thing that
decides what to discard.

It checks each persona against its own charter — did the triage screener stay
inside eleven seconds, or did it cite something from the third page? Did the ATS
simulator flag formatting that modern parsers handle fine? Did the fatigued
reader flag a deliberate voice marker, documented in the user's own voice agent,
as a defect?

Two classes of contrarian argument get **struck** rather than weighed:

1. **Offer-stage contract terms.** Relocation funding, sign-on, equity, start
   date, buying out a clawback. These are negotiated after an offer exists.
   Killing an application over money that is still negotiable, at the stage
   where the candidate has the least leverage, is a category error.
2. **An unassessed neighbouring requisition.** A better-looking seat elsewhere
   at the same company is not an input unless it has been fully assessed and the
   user has asked for it to be weighed. Cross-requisition sequencing is the
   user's call.

Everything else the contrarian raises is in scope: conversion probability,
channel structure, pool position, qualification gaps, overclaims, swap-test
failures, materials density, level-fit signalling, and adverse application
history at the target company.

Both the struck legs and the surviving ones are recorded in `role_analysis.md`.
Recording only the outcome makes the gate impossible to improve, because the
false positives it caught become invisible the moment it catches them.

## The three-round cap

Rounds are compared, not just re-run. An issue flagged in more than one round is
real; an issue flagged once is noise. That signal only exists if the review runs
more than once, which is why the builder runs it twice by default.

Every round uses **fresh agent instances**. A persona that has already seen its
own verdict cannot re-derive it independently, so reusing a report across rounds
converts a second opinion into an echo.

Three rounds is the ceiling. Past that the remaining gaps are structural, and
the honest output is to say so rather than to run a fourth round and produce
more edits.

## On a harness without subagent dispatch

Codex and Gemini CLI have no subagent dispatch. The review still runs: the
personas are adopted in turn, in one context, each report written out before the
next begins.

Two things degrade, and it is worth knowing which. It is slower, which does not
matter much. And the blind stage is no longer blind, which does — the
contamination described above is exactly what one shared context reintroduces.
The skill instructs the model to write each report out fully before starting the
next, which limits the drift without eliminating it.
