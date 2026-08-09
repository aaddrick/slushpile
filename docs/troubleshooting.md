# Troubleshooting

**`plugin install` succeeds but the skills do not appear.** Run `claude plugin
list` and check for `enabled`. Skills load at session start, so start a new
session or run `/clear`.

**A skill says it cannot find `preferences.yaml`.** You are in a different
directory than the one you onboarded. Every skill reads the workspace from the
current working directory. See [The workspace](workspace.md).

**The review agents report a nearly empty resume.** They are reading extracted
text, not your PDF as rendered. Run `pdftotext yourresume.pdf -` and look at the
output. If it is empty or scrambled, the resume has a layout problem — a
multi-column grid, a text box, contact details in a header — and that is a real
finding, not a tooling failure. An ATS sees what `pdftotext` sees.

**The cover letter reads generic, or sounds like someone else.** Check
`voice.is_mine` in `preferences.yaml`. If it is false you are using the shipped
example voice, which belongs to the plugin author. Generate your own with
[written-voice-replication](https://github.com/aaddrick/written-voice-replication)
and point `voice.agent` at it. If it is already true, the corpus was probably
too thin — a few thousand words is the floor. See
[Your voice agent](voice.md).

**Every role comes back killed on compensation.** Open `preferences.yaml` and
check `compensation`. With `net_qol`, the most common cause is a
`current_baseline` entered as gross rather than after-tax-after-housing, which
makes every offer look worse than it is.

**Every role comes back Tier 1.** Something is scoring against the posting
rather than against the pool. Check that `role_analysis.md` actually contains
percentile archetypes for the role, not just a keyword comparison — a fit score
with no pool estimate behind it is a match score wearing a percentile's name.
See [Scoring](architecture/scoring.md).

**The review never says no.** Check that the contrarian ran at all: its net call
should appear in the pipeline summary and in `application.yaml` under
`contrarian_net`. It is meant to be automatic rather than conditional, and a
review missing it is a review with no falsification step.

**Calibration says there is not enough data, and there clearly is.** The floor is
five *resolved* applications, and an application counts as resolved only when
`outcome.stage_reached` is set, or when it was submitted more than 30 days ago
with no response. Applications sitting in `application.yaml` with an empty
outcome are counted as in flight, not as rejections. `/slushpile:status` reports
which records are incomplete.

**A review round produces the same findings as the last one.** That is the
signal, not a bug. An issue flagged in more than one round is real; an issue
flagged once is noise. If nothing has moved by round three the gaps are
structural, and the pipeline is meant to say so rather than run a fourth round.

**The pipeline will not submit the application for you.** It never will. No
skill touches a portal, an email, or a form. It writes files; you read them and
you send them.
