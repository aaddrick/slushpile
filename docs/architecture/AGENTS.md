# Working on the architecture docs

Read this before editing anything in `docs/architecture/`.

> **Parity note:** `CLAUDE.md` and `AGENTS.md` in this directory are
> byte-identical on purpose, so an agent finds the same guidance under
> whichever name its harness looks for. `scripts/sync_docs.py` writes the
> `AGENTS.md` twin from this file, and `tests/test_docs.py` fails if they ever
> differ. Edit `CLAUDE.md` and run the generator; never edit the twin.

## What these pages are for

`README.md` argues. `docs/` explains. These pages are the third thing: they
record **why the pipeline is shaped the way it is**, for a reader who has
already accepted that it works and wants to change it without breaking a
property they did not know was there.

The test for whether something belongs here: could a contributor delete the
behaviour, watch every gate pass, and only find out it mattered from a user? If
so, the reason belongs on one of these pages.

## Rules

**Every page states a failure mode, not just a rule.** This whole repository is
prose that a model reads and acts on, and a bare imperative is dropped the first
time the model is under load. A rule with the failure attached survives
paraphrase. That applies to the docs describing the rules as much as to the
skills carrying them.

**No page owns a fact that lives in the tree.** The skill list, the agent list,
the model per agent, the dispatch order, and the size of the blind stage all
live in `skills/` and `agents/`. A page that needs one either derives it through
a generated region, or states it in a sentence that
`scripts/sync_docs.py`'s count sweep can check. Do not hand-write a table of
agents here; there is one, and it is generated.

**Link to the file, not to the fact.** `agents-and-models.md` says where the
model is declared rather than restating each declaration in prose. The moment a
page restates a fact it does not own, that page becomes the seventh place a
rename has to reach.

**Cite the skill by path when a rule comes from one.** `skills/status/SKILL.md`,
not "the status skill". A path is greppable and survives a rename badly enough
to be noticed; a description does not and does not.

**Prefer the concrete number and its condition.** "Three rounds is the ceiling"
is checkable. "A few rounds" is not, and it is the form a summarizer produces
when the condition was not load bearing in the original.

## Mechanics

**Diagrams.** Every diagram embedded here comes from `docs/diagrams/`, is
paired light and dark through a `<picture>` element, and needs `alt` text on the
`<img>`. The alt text is the only description a screen reader gets, and it
drifts silently — update it in the same commit as the `.d2`. See
[../diagrams/AGENTS.md](../diagrams/AGENTS.md) before touching a diagram.

**The legend.** `pipeline.md` carries the class legend for every diagram on it.
`tests/test_docs.py` requires the legend and the two theme files to name exactly
the same classes, so a new class needs a row. No gate can tell whether the row's
prose is still true.

**Reachability.** Every file here must be reachable within two hops of
`docs/index.md`. In practice that means [index.md](index.md)'s file table gets a
row for every new page. A page nobody links to is a page nobody reads, and the
gate exists because that failure is invisible in a diff.

**Adding a page.** Add the file, add its row to [index.md](index.md), and add a
line to the `docs/index.md` architecture section if it is something a reader
would look for from the front door. Then run the four gates in `CLAUDE.md` at
the repository root.
