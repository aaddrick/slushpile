# Personal data

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../../docs/architecture/personal-data.md">English</a> ·
  <a href="../../../zh-CN/docs/architecture/personal-data.md">简体中文</a> ·
  <a href="../../../es/docs/architecture/personal-data.md">Español</a> ·
  <a href="../../../pt-BR/docs/architecture/personal-data.md">Português (BR)</a> ·
  <a href="../../../vi/docs/architecture/personal-data.md">Tiếng Việt</a> ·
  <strong>AI Bro</strong>
</p>

<!-- END GENERATED language-nav -->

## The boundary

The plugin is public code. The workspace is one person's employment history, comp
figures, and constraints.

Different assets. Different directories. Nearly every rule on this page falls out
of that one sentence.

`/slushpile:onboard` runs in the user's own directory, not the plugin checkout,
and writes `profile.md`, `preferences.yaml`, and `stories.md` there. Onboarding
says plainly that the directory should be a **private** repository or no
repository at all, and it will not initialize one or add a remote. A git remote
you inherited from a setup step is a decision nobody made.

## Nothing in `skills/` or `agents/` hardcodes a fact about any user

No compensation floors. No metro rent tables. No citizenship. No clearance status.
No named employer as the user's own. No named stories. No "the candidate is open
to relocation".

A skill that needs one of those reads it from `preferences.yaml` at run time.

The failure this prevents is specific, and it is quiet.

A hardcoded compensation floor does not error. It kills roles, looking entirely
correct while it does it, for a reason the user never chose and cannot see. A
hardcoded "open to relocation" does not error either. It ships twelve applications
asserting something about somebody that may not be true.

Neither of those shows up as a bug. They show up as a search that went badly.

Illustrative examples naming real companies are fine and useful, because they
teach the pattern. *"Most capacity planning candidates come from one side"* as an
example of a company-dependent thesis is teaching. *"The candidate has ten years
in industrial control systems"* is a leak.

Note that the second example had to be paraphrased to appear on this page. The
real one names a domain `check_no_pii.py` matches, and this file is one of the
files it scans. That is the gate working as intended, on the page documenting the
gate.

## The gate

```bash
python3 scripts/check_no_pii.py
```

Not a policy document. A test that goes red.

It scans `skills/`, `agents/`, `templates/`, and `docs/` for the patterns that
leaked last time, each with the reason it counts: author identity, a prior
employer stated as the user's own, a hardcoded home location, a hardcoded
compensation baseline, a citizenship or clearance status stated as fact, a
credential stated as fact, real contact details, and references to files that
exist only in the private repository this plugin was productized out of.

The patterns are deliberately narrow.

A broad pattern that fires on legitimate prose gets suppressed within a week, and
a suppressed check is worse than no check, because it reads as covered. Precision
over recall, every time, when the alternative is a gate nobody trusts.

A new leak pattern that gets through belongs in that script. Not in a review
comment.

## The one exemption, and its limit

Voice agents are exempt from the **identity** patterns. Only those.

A voice agent *is* one person's identity by construction: generated from a corpus
of their writing, named after them, few-shot examples are their actual sentences.
Strip the identity and you have destroyed the artifact.

Contact details are forbidden everywhere, voice agents included. A phone number in
a shipped agent is a leak under any theory anybody has ever proposed.

The exemption list is per file and per pattern, in `check_no_pii.VOICE_AGENTS`.
There is a second list, `ALLOWED`, for anything else, and it is empty on purpose.

Every entry in it would be a hole. A hole in this gate stays invisible until
somebody else's application says they are open to relocating to a city they have
never seen.

## The pipeline never submits anything

No skill touches an application portal, an email, or a form. Every stage writes
files. The user reads them and sends them.

That is a privacy property before it is a safety one. A pipeline that submits is a
pipeline that has to hold credentials, and there is nowhere in this design to put
credentials except the user's own machine, doing something they did not watch.

No telemetry. No account. No server. Nothing to opt out of, because there is
nothing collecting.
