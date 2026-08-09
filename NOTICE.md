# Notice

## Origin

slushpile is a productized version of a private job-search repository maintained
by [aaddrick](https://github.com/aaddrick) through 2026. The pipeline design —
pool-anchored scoring, channel-conditional verdicts, the seven-agent review, and
the contrarian gate — was developed there against real applications, and the
calibration rules exist because specific things went wrong.

Three of them are worth naming, since the rules they produced look arbitrary
without them.

**Absolute grading inflates every score.** The original rubric graded each role
on keyword match against the posting. It produced Tier 1 and Tier 2 scores that
did not survive contact with the actual applicant pool. The fix was to make pool
position the canonical fit number and demote keyword match to a secondary field.

**A single verdict hides the decision.** Collapsing the channels into one
INTERVIEW / MAYBE / PASS obscured that the same materials converted at wildly
different rates cold versus referred. The hiring manager now returns a
probability per channel, and a verdict word is never accepted in place of a
number.

**A gate that appends is not a gate.** The contrarian originally ran after tier
tables were published, so its findings read as commentary and the upstream
over-grading survived intact. It now runs before the tables are written and its
net calls change them.

The scope limits in `agents/slushpile-contrarian.md` come from the same place. A
contrarian pass once built a DO_NOT_SUBMIT on the argument that the posted band
could not fund a make-whole for money the candidate would have left behind — a
negotiation that happens after an offer exists, at a stage where the candidate
has leverage. The application was sent anyway. Offer-stage contract terms are
now out of scope by construction, and so is letting an unassessed neighbouring
requisition veto an assessed one.

No personal data from that repository is present here. Every personal fact it
contained became a field in `templates/preferences.yaml` or a section in
`templates/profile.md`, and `scripts/check_no_pii.py` gates against regression.

## Voice agents

Cover letters are written by a voice agent, which slushpile does not generate.
That is
[aaddrick/written-voice-replication](https://github.com/aaddrick/written-voice-replication),
a separate pipeline by the same author. It analyzes a corpus of someone's
writing across 25 dimensions and outputs a voice agent, a voice skill, and a
numeric profile.

`agents/aaddrick-voice.md` is that project's own public worked example,
generated from a Reddit data export, and it ships here unmodified so slushpile
runs before a user has built their own. It is the plugin author's voice. Anyone
using slushpile for real applications should generate their own and point
`voice.agent` in `preferences.yaml` at it.

This is the one place a person appears in the shipped pipeline, and it is
deliberate: a voice agent *is* one person's identity by construction, and
stripping that out would leave nothing. The exemption in
`scripts/check_no_pii.py` is scoped to that single file and does not cover
contact details.

## Repository structure

The repository layout, the multi-harness manifest set, the generated-docs
pattern, and the CI gates follow
[aaddrick/attention-control](https://github.com/aaddrick/attention-control),
by the same author. MIT.

## What this is not

**Not a submission bot.** Nothing here touches an application portal, an email,
or a form. Every skill writes files. A human reads them and sends them.

**Not an ATS.** `agents/slushpile-ats-simulator.md` simulates how applicant
tracking systems parse and score a document, from public documentation and
observed behavior. It is not any vendor's product, it is not affiliated with
one, and its match score is an estimate. No ATS vendor endorses this project.

**Not a prediction.** The conversion probabilities the pipeline produces are
informed estimates. They are labelled as estimates throughout, and the
`Calibration` table in `templates/job_search.md` exists so a user can correct
them against their own outcomes rather than trusting the priors indefinitely.

**Not advice about anyone's specific situation.** The compensation gate does
arithmetic on numbers you supply. It is not tax, immigration, legal, or
financial advice.

## Company names

Company names appear in the skills as illustrative examples — of a careers-board
platform, of an applicant pool archetype, or of a cover-letter thesis that
breaks under a company swap. They are used descriptively. No company named here
is affiliated with, sponsors, or endorses this project.

## Your data

`/slushpile:onboard` writes to your working directory and nowhere else. The
plugin has no telemetry, no network calls of its own, and no storage outside the
directory you run it in.

What your agent does with the files it reads is governed by whatever harness you
are running, not by this plugin. If that matters to you, check your harness's
data policy — the pipeline will be handing it your full employment history.

## Typefaces

`assets/fonts/` holds eleven font files serving two unrelated purposes.
`scripts/make_card.py` draws `.github/assets/hero.png` with some of them, and
`templates/resume.tex` and `templates/cover_letter.tex` are set in the others.
All three families are licensed under the SIL Open Font License 1.1, and all
three license texts sit beside the fonts.

**[Saira Condensed](https://github.com/google/fonts/tree/main/ofl/sairacondensed)**,
version 0.072, copyright 2016 The Saira Project Authors. Three weights: Bold,
SemiBold, Medium. Card only. License in
[`assets/fonts/OFL-SairaCondensed.txt`](./assets/fonts/OFL-SairaCondensed.txt).

**[IBM Plex Mono](https://github.com/google/fonts/tree/main/ofl/ibmplexmono)**,
version 2.3, copyright 2017 IBM Corp. Three weights: Regular, Medium, SemiBold.
Regular and SemiBold set the eyebrows and datelines in both document templates;
Medium is card only. License in
[`assets/fonts/OFL-IBMPlexMono.txt`](./assets/fonts/OFL-IBMPlexMono.txt).

**[Public Sans](https://github.com/uswds/public-sans)**, version 2.001,
copyright 2015 The Public Sans Project Authors. Five faces: Regular, Bold,
Italic, Bold Italic, ExtraBold. Document templates only. Taken from the upstream
release rather than from Google Fonts, which ships Public Sans as a variable
font, and XeLaTeX cannot select a named instance out of one. License in
[`assets/fonts/OFL-PublicSans.txt`](./assets/fonts/OFL-PublicSans.txt).

The fonts are vendored, not downloaded at build time. A build that fetches from
a branch is not reproducible, because the branch moves.

`scripts/install_fonts.py` copies the document faces, and the two license files
that must travel with them, into the user's own font directory. It installs only
the faces the templates name: Saira Condensed and Plex Mono Medium exist for the
card and have no business on someone's system as a side effect of building a
resume. Nothing runs it automatically, and skipping it is supported rather than
broken, because both templates fall back to DejaVu when a family is absent.

Neither foundry, nor IBM, nor the U.S. Web Design System endorses this project.
