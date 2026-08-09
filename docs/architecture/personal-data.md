# Personal data

## The boundary

The plugin is public code. The workspace is one person's employment history,
compensation figures, and constraints. They are different things and they live
in different directories, and nearly every rule on this page follows from that
one sentence.

`/slushpile:onboard` is run in the user's own directory, not in the plugin
checkout. It writes `profile.md`, `preferences.yaml`, and `stories.md` there.
Onboarding says plainly that the directory should be a **private** repository or
no repository at all, and it will not initialize one or add a remote — that is a
decision to make deliberately, not a side effect of setting up a workspace.

## Nothing in `skills/` or `agents/` may hardcode a fact about any user

No compensation floors. No metro rent tables. No citizenship, no clearance
status, no named employer as the user's own, no named stories, no "the candidate
is open to relocation". A skill that needs one of those reads it from
`preferences.yaml` at run time.

The failure this prevents is specific and quiet. A hardcoded compensation floor
does not error; it kills roles, correctly-looking, for a reason the user never
chose and cannot see. A hardcoded "open to relocation" does not error either; it
produces twelve applications asserting something about someone that may not be
true.

Illustrative examples naming real companies are fine, and useful, because they
teach the pattern. *"Most capacity planning candidates come from one side"* as
an example of a company-dependent thesis is teaching. *"The candidate has ten
years in industrial control systems"* is a leak.

Note that the second example had to be paraphrased to appear on this page. The
real one names a domain that `check_no_pii.py` matches, and this file is one of
the files it scans — which is the gate working as intended, on the page that
documents it.

## The gate

```bash
python3 scripts/check_no_pii.py
```

It scans `skills/`, `agents/`, `templates/`, and `docs/` for the patterns that
leaked the last time, each with the reason it counts as a leak: author identity,
a prior employer stated as the user's own, a hardcoded home location, a
hardcoded compensation baseline, a citizenship or clearance status stated as
fact, a credential stated as fact, real contact details, and references to files
that exist only in the private repository this plugin was productized out of.

The patterns are deliberately narrow. A broad pattern that fires on legitimate
prose gets suppressed within a week, and a suppressed check is worse than no
check because it reads as covered.

A new leak pattern that gets through belongs in that script, not in a review
comment.

## The one exemption, and its limit

Voice agents are exempt from the **identity** patterns, and only those. A voice
agent *is* one person's identity by construction: it is generated from a corpus
of their writing, named after them, and its few-shot examples are their actual
sentences. Stripping the identity out would destroy the artifact.

Contact details are forbidden everywhere, voice agents included. A phone number
in a shipped agent is a leak under any theory.

The exemption list is per file and per pattern, in `check_no_pii.VOICE_AGENTS`.
There is a second list, `ALLOWED`, for anything else — and it is empty on
purpose. Every entry in it would be a hole, and a hole in this gate is invisible
until someone else's application says it is open to relocating to a city they
have never seen.

## The pipeline never submits anything

No skill touches an application portal, an email, or a form. Every stage writes
files. The user reads them and sends them.

This is a privacy property before it is a safety one: a pipeline that submits is
a pipeline that must hold credentials, and there is nowhere in this design to
put them that is not the user's own machine doing something they did not watch.
