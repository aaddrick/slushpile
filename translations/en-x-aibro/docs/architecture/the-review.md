# The review

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../../docs/architecture/the-review.md">English</a> ·
  <a href="../../../zh-CN/docs/architecture/the-review.md">简体中文</a> ·
  <a href="../../../es/docs/architecture/the-review.md">Español</a> ·
  <a href="../../../pt-BR/docs/architecture/the-review.md">Português (BR)</a> ·
  <a href="../../../vi/docs/architecture/the-review.md">Tiếng Việt</a> ·
  <strong>AI Bro</strong>
</p>

<!-- END GENERATED language-nav -->

`/slushpile:adversarial-review` dispatches 7 reviewers against a resume and a
cover letter.

This page is why that topology, and not some other one. The picture is in
[pipeline.md](pipeline.md). The definitions are in `agents/`.

## Four failure modes. Four stages. One each.

This is not a committee. Every stage closes a specific way that a naive eval
pipeline produces confident nonsense.

**Single-perspective sycophancy.** Every reviewer in a naive pipeline works for
the candidate. None of them models the queue. The pool analyst forces comparative
reasoning: not "are these materials good" but "are they better than the other
seventy applications this requisition took in this week". Absolute scoring on a
relative problem. That is the category error the entire category is built on and
sells as a headline metric.

**Verdict collapse.** One INTERVIEW / MAYBE / PASS hides that the same materials
convert at wildly different rates cold versus referred. Different distributions,
different decisions about your afternoon. The hiring manager emits one verdict per
channel with a probability range instead of a word.

**Synthetic AI-detection concern.** An AI-detector persona flags patterns based on
hypothetical reader doubt and then overrides grounded judgment about what a real
reader notices. Replaced by the fatigued reader, which asks the answerable
question: would this annoy someone on their sixty-first application of the day?

**No falsification step.** Nothing in a normal review asks what would have to be
true for the whole exercise to be a waste of cycles. The contrarian asks it, last,
with authority to overturn everything upstream.

An eval that cannot return "none of this was worth running" is not an eval.

## The blind stage

The first 5 in parallel. One dispatch message. No reviewer sees another's output.

This is the load-bearing property of the entire review, and it is the one that
degrades silently.

Contamination does not raise an error. It produces agreement.

A specialist that already read the triage verdict drifts toward confirming it.
Five reports that agree then look like strong consensus, when they are one opinion
restated five times with different formatting. Consensus across the blind stage is
the highest-quality signal this pipeline emits, and it is worth exactly as much as
the isolation behind it. Break the isolation and you keep the confidence while
losing the information.

Each persona gets only what its role would genuinely hold:

| Persona | Given | Withheld, and why |
| --- | --- | --- |
| Triage screener | Resume text, title, company, level | The cover letter. It is simulating eleven seconds, and a screener who read the letter is not one. |
| Requirements analyst | Resume, cover letter, full posting, level | Nothing. Its job is checking every qualification against evidence. |
| ATS simulator | Resume text, full posting, and the `.tex` or `.docx` source if there is one | Nothing, but note it gets the *source* on purpose: tables, columns and header placement are invisible in extracted text and are exactly what it exists to catch. |
| Fatigued reader | Resume, cover letter | Any instruction to judge AI authorship. That is a different question and it is not this one's. |
| Pool analyst | Everything, plus prior application history and the observed conversion rates | Nothing. It needs the most context of the five. |

Withholding is a feature. Every one of those denials is doing work.

The resume every persona reads is `pdftotext` output, not the LaTeX or Markdown
source. Reviewing the source means reviewing a document nobody will ever see. If
the extracted text is empty or scrambled, that is the finding, not a tooling
failure. An ATS sees what `pdftotext` sees.

## Why the last two are serial

Hiring manager runs after all five return and sees all five. Contrarian runs after
the hiring manager and sees everything, including it.

Serializing costs wall clock and buys the one thing the blind stage structurally
cannot provide: someone who can weigh the five against each other, and then
someone who can attack that weighing. A contrarian running concurrently with the
hiring manager would be arguing with a synthesis it never read.

The contrarian is **automatic, not conditional**. A falsification step that fires
only when the orchestrator feels uncertain will skip itself in exactly the cases
where the certainty was misplaced. Opt-in rigor is not rigor.

## Priors go in verbatim, including empty

The pool analyst and the contrarian both receive the `calibration_priors` block
from `preferences.yaml` exactly as written.

Summarize it into "the candidate converts poorly" and you strip the sample size,
which is the only thing that says how much weight the number deserves.

Omit it when unset and the agent reads an ordinary run instead of an uncalibrated
one. An uncalibrated estimate that is not labelled is worse than no estimate,
because downstream it is indistinguishable from a calibrated one.

Where an observed rate has a sample size of five or more, the pool analyst uses it
in place of its own prior for that channel, and says that it did.

## The gatekeeper

The orchestrating skill is the gatekeeper. Not one of the personas. Deliberately.

The personas are tuned to be harsh, some of what they emit is wrong, and nothing
tuned to be harsh can also be the thing deciding what to discard.

It audits each persona against its own charter. Did the triage screener stay
inside eleven seconds or cite something off page three? Did the ATS simulator flag
formatting modern parsers handle fine? Did the fatigued reader flag a deliberate
voice marker, documented in the user's own voice agent, as a defect?

Two classes of contrarian argument get **struck** rather than weighed:

1. **Offer-stage contract terms.** Relocation funding, sign-on, equity, start
   date, buying out a clawback. Negotiated after an offer exists. Killing an
   application over money that is still negotiable, at the stage where the
   candidate has the least leverage, is a category error.
2. **An unassessed neighbouring requisition.** A better-looking seat elsewhere at
   the same company is not an input unless it has been fully assessed and the user
   asked for it to be weighed. Cross-requisition sequencing is the user's call.

Everything else the contrarian raises is in scope: conversion probability, channel
structure, pool position, qualification gaps, overclaims, swap-test failures,
materials density, level-fit signalling, adverse application history at the target
company.

Struck legs and surviving legs both get recorded in `role_analysis.md`. Record
only the outcome and the gate becomes impossible to improve, because the false
positives it caught go invisible the moment it catches them. Log the rejections or
you cannot tune the filter.

## The three-round cap

Rounds are compared, not just re-run.

Flagged twice, real. Flagged once, noise. That signal only exists if the review
runs more than once, which is why the builder runs it twice by default.

Every round uses **fresh agent instances**. A persona that already saw its own
verdict cannot re-derive it independently. Reuse a report across rounds and a
second opinion becomes an echo.

Three rounds is the ceiling. Past that the gaps are structural and the honest
output is to say so, not to burn a fourth round generating edits that feel like
progress.

## On a harness without subagent dispatch

Codex and Gemini CLI cannot dispatch subagents. The review still runs: personas
adopted in turn, one context, each report written before the next.

Two properties degrade. One is slower, which barely matters.

The other is that the blind stage is no longer blind. That is not a performance
note, that is the contamination described above, reintroduced by design
limitation. The skill instructs the model to write each report fully before
starting the next, which limits drift without eliminating it.

Know which guarantee you are running without.
