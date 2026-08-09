# Troubleshooting

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../docs/troubleshooting.md">English</a> ·
  <a href="../../zh-CN/docs/troubleshooting.md">简体中文</a> ·
  <a href="../../es/docs/troubleshooting.md">Español</a> ·
  <a href="../../pt-BR/docs/troubleshooting.md">Português (BR)</a> ·
  <a href="../../vi/docs/troubleshooting.md">Tiếng Việt</a> ·
  <strong>AI Bro</strong>
</p>

<!-- END GENERATED language-nav -->

Most of what looks like a bug here is the system working. Read the second half of
each answer.

**`plugin install` succeeded, no skills.** Run `claude plugin list`, check for
`enabled`. Skills load at session start. New session, or `/clear`.

**A skill cannot find `preferences.yaml`.** Wrong directory. Every skill resolves
the workspace from the current working directory. See
[The workspace](workspace.md).

**The review says the resume is nearly empty.** It is reading extracted text, not
your rendered PDF. Run `pdftotext yourresume.pdf -` and look.

If that output is empty or scrambled, this is not a tooling failure. It is the
finding. Multi-column grid, text box, contact details in a header: an ATS sees
exactly what `pdftotext` sees, and you have been shipping to the renderer while
the parser gets nothing. Your resume looks great to the one reader who does not
exist.

**The cover letter reads generic, or sounds like someone else.** Check
`voice.is_mine` in `preferences.yaml`.

False means you are running the shipped example voice, which belongs to the
plugin author. Generate your own with
[written-voice-replication](https://github.com/aaddrick/written-voice-replication)
and point `voice.agent` at it. Already true? The corpus was too thin. A few
thousand words is the floor, and below it the output regresses to the model
default no matter what the profile says. See [Your voice agent](voice.md).

**Every role dies on compensation.** Open `preferences.yaml`, check
`compensation`. With `net_qol`, the usual cause is a `current_baseline` entered as
gross instead of after-tax-after-housing. Wrong denominator, every offer in the
market looks like a downgrade.

**Every role comes back Tier 1.** Something is scoring against the posting instead
of against the pool. Check `role_analysis.md` for actual percentile archetypes,
not a keyword comparison.

A fit score with no pool estimate behind it is a match score wearing a
percentile's name. That is the exact failure this pipeline exists to not have, so
if you are seeing it, the pool estimation step did not really run. See
[Scoring](architecture/scoring.md).

**The review never says no.** Confirm the contrarian ran at all: its net call
belongs in the pipeline summary and in `application.yaml` under
`contrarian_net`.

It is automatic, never conditional. A review missing it has no falsification
step, and an eval that cannot fail is not an eval. It is a formatter with
opinions.

**Calibration says not enough data and there clearly is.** The floor is five
*resolved* applications. Resolved means `outcome.stage_reached` is set, or it was
submitted more than 30 days ago with no response. Records sitting in `application.yaml` with
an empty outcome count as in flight, not as rejections. `/slushpile:status` will tell you
which records are incomplete.

**Round two produced the same findings as round one.** That is the signal. Not a
bug.

An issue flagged in more than one round is real. An issue flagged once is noise.
That distinction is the entire reason the builder runs the review twice, and if
nothing has moved by round three the gaps are structural. The pipeline says so
and stops, because a fourth round is motion.

**It will not submit the application for you.** It never will. No skill touches a
portal, an email, or a form. It writes files. You read them. You send them.
