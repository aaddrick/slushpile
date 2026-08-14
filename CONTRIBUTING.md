# Contributing

This repository takes no pull requests from outside contributors. GitHub blocks
them: pull request creation is set to **collaborators only**. A fork you push to
cannot open one here.

Two things still work, and both are better fits for this project.

## Found a problem? Open an issue

[Open an issue](https://github.com/VonTerraProject501c3/slushpile/issues/new). Include:

1. The harness and version: `claude --version`, `codex --version`.
2. The exact command you ran.
3. What happened.
4. What you expected instead.

A wrong path or a wrong command in [INSTALL.md](./INSTALL.md) is the most
useful report there is. Those claims are checked by hand against each harness,
and a harness changes them without warning.

**Never paste your own materials into an issue.** A bug report about the review
pipeline does not need your resume. Describe the shape of the problem — "the
pool analyst estimated a p90 archetype that does not exist for this kind of
role" — and redact anything specific. Issues are public and permanent.

## The bar for a change to a skill or an agent

These files are prose that a model reads and acts on, which makes them harder to
review than code. Two things do not show up in a diff:

**A rule needs its reason.** A bare imperative gets dropped when the model is
under load or paraphrasing. A rule with its failure mode attached survives.
If you add a rule, say what goes wrong without it.

**A rule needs an observable violation.** "Run the kill-criteria check" cannot
be verified from the output. "State the checks that passed, not only the ones
that failed" can. Write the version you could catch someone skipping.

## Never put a person in this repository

The hardest rule here, and the one most likely to be broken by accident.

This plugin was productized out of one person's working job-search repository.
Every personal fact became a field in `templates/preferences.yaml` or a section
in `templates/profile.md`. **Nothing in `skills/` or `agents/` may hardcode a
fact about any user.**

No compensation floors. No rent tables. No citizenship, clearance, or degree
status. No named employers presented as the user's own. No named stories.

A skill that needs one of those reads it from `preferences.yaml` at run time.

Illustrative examples naming real companies are fine and useful. The difference:

- Teaching — *"Most capacity planning candidates come from one side of the business"*, as an example of a thesis that breaks under a company swap.
- A leak — *"The candidate has ten years in secure document manufacturing."*

`python3 scripts/check_no_pii.py` greps for the patterns that leaked before.
A new leak pattern that slips past it belongs in that script, not in a review
comment.

## Before you push

```bash
python3 scripts/check_configs.py
```

```bash
python3 scripts/check_no_pii.py
```

```bash
python3 scripts/sync_docs.py --check
```

```bash
python3 -m unittest discover -s tests -v
```

CI runs all four on every pull request and on every push to `main`, plus a fifth
job that installs this checkout into a scratch config and fails if the plugin
does not reach "enabled". Nothing here is filtered by path, so every commit gets
every gate on whichever route it arrives by.

Run the four locally first. CI on the pull request catches the same failures a
push later, and the local run is the faster of the two.

`AGENTS.md` is generated from `CLAUDE.md`. A patch against `AGENTS.md` cannot
be merged — edit `CLAUDE.md` and run `python3 scripts/sync_docs.py`.

The same generator writes both `.cursor/` files outright, and the regions marked
`BEGIN GENERATED` / `END GENERATED` in `README.md`, `INSTALL.md`, and
`GEMINI.md`. It builds them from the skill and agent directories and from the
dispatch table in `skills/adversarial-review/SKILL.md`. Adding a skill means
adding a row to `SKILLS` in that script; it fails rather than shipping a skill
the README documents and the Cursor router never mentions.

## Want different rules? Fork

MIT. The nine skills and eight agents are Markdown with no build step. Fork,
edit, and install your copy — the four commands are in the README's
[Tune it](./README.md#tune-it) section.

This is the right route for a change that reflects how *your* field hires. The
pool priors, the tier thresholds, and the kill criteria are calibrated against
one person's search in one set of industries. A defense hiring pool and a
seed-stage startup pool do not behave the same way, and a fork gives you the
change without a negotiation about whose priors are correct.

If your fork's priors are better for a whole industry, open an issue describing
the calibration data behind them. That is a change worth merging.

## Why outside pull requests are off

Maintainers work through pull requests; the block is on patches from outside.
Three reasons for it.

**Six surfaces are generated.** `scripts/sync_docs.py` writes `AGENTS.md`, both
`.cursor/` files, and the marked regions of `README.md`, `INSTALL.md`, and
`GEMINI.md` from `skills/`, `agents/`, and the dispatch table. A patch against
any of them cannot be merged: it fails CI, and the fix is always to edit the
source and rerun the generator. Most first patches to a repository shaped like
this one land on a generated file, because a generated file is what a reader
finds first.

**A patch is the likeliest way a person leaks in.** The rule above — nothing in
`skills/` or `agents/` hardcodes a fact about a user — is easy to break while
making a change that is otherwise correct, and a contributor writing from their
own search has their own facts closest to hand. `check_no_pii.py` catches the
patterns that leaked before, not the ones that have not happened yet.

**The priors are one person's calibration, not a standard.** The pool
archetypes, the tier thresholds, and the kill criteria come from one search in
one set of industries. A rule that is right for how your field hires may be
wrong here, and the fork route gives you the change without a negotiation about
whose priors are correct.

## Maintainers

Every change goes issue, branch, pull request, merge. Nothing lands by a direct
push to `main`. Pull request creation stays collaborators only, so this is the
route for people with commit access; everyone else arrives through an issue.

Open the issue first, including for your own work. Keep it short: what is wrong,
and what should be true instead. A few sentences is a whole issue, and one
front-loaded with the investigation gets skimmed past the sentence that says
what broke.

The pull request is short for the same reason. What changed, and why this way,
in enough detail for a reviewer to decide where to look. The evidence goes in
the commit bodies, where someone deep-diving is already reading, and the diff is
the authority over both.

Reference the issue with `Closes #12`, so it closes on merge and the search that
finds one finds the other. CI runs all five jobs on the pull request, which is
the point of the route: a gate fails before the commit is public rather than
after. Run the four locally first anyway.

Merge by rebase or squash, never a merge commit. Squash a branch that is one
change told in several commits; rebase one whose commits each stand alone.

Do not force-push `main`. Rewriting published history breaks every clone and
fork, and orphans any pull request a collaborator has open.

A commit subject states what changed. The body states why, with the evidence:
the failing command, the harness's documentation, or the calibration run.
