# Generated surfaces

This is the contributor-facing half of the architecture. If you are only trying
to run the pipeline, nothing here affects you.

## Why any of this is generated

Several files describe this pipeline: `CLAUDE.md` and its `AGENTS.md` mirror,
the two Cursor router files, `GEMINI.md`, `README.md`, the paste-in snippet in
`INSTALL.md`, and now these docs. Every one of them lists the skills, and most
of them state the review's shape.

None of those facts belongs to the file that prints it. They live in `skills/`,
in `agents/`, and in the dispatch table inside
`skills/adversarial-review/SKILL.md`.

A list that drifts is not a cosmetic problem here. A skill missing from the
Cursor router is a stage a Cursor user cannot reach, and a reviewer reading a
diff has no way to see it.

## Three mechanisms

`scripts/sync_docs.py` writes the derived copies; `--check` is the CI gate.

**Whole files.** `AGENTS.md` mirrors `CLAUDE.md`. The two Cursor files are built
from the tree. The `AGENTS.md` twins in `docs/architecture/` and
`docs/diagrams/` are byte-identical copies of their `CLAUDE.md` siblings, so an
agent finds the same guidance under whichever name its harness looks for.

**Marked regions.** `README.md`, `INSTALL.md`, `GEMINI.md`, and
[agents-and-models.md](agents-and-models.md) are hand-written except between
`BEGIN GENERATED` and `END GENERATED` markers. Anything inside a marked region
is overwritten on the next run.

**Count claims.** A few sentences state a derived number in prose, where a
marked region would be heavier than the sentence it wraps. Those are checked
rather than written: the sentence must appear verbatim, with the right number in
it, or the generator fails and names the file.

Everything derived is looked up by name, and a name that matches nothing is an
error rather than a silent omission. Adding a skill without giving it a row in
`SKILLS` fails the build. That is the point: a skill missing from the router is
not a wrong file, it is a stage of the pipeline a user cannot reach.

## Two gates that exist because of specific failures

**The count sweep.** A registered claim only covers a sentence somebody
registered, so a count nobody thought about drifts in silence. That is not
hypothetical: three shipped files counted the skills one short for as long as
there have been nine, because none of the three had a row. So a sweep reads
every `.md`, `.mdc`, `.json`, and `.d2` file in the tree for a counted noun —
skills, agents, reviewers, personas, specialists — and fails on any number that
is not currently true, registered or not.

It also covers the size of the review's blind stage, which appears in shapes a
noun list alone cannot see: "five of whom run in parallel", "the first five are
supposed to be blind". Those go through a second pattern with the connectives
whitelisted, because a rule loose enough to catch them from the noun alone also
catches "three parallel phrases" in a voice agent's style notes.

A sentence that counts a subset on purpose goes in `COUNT_EXEMPT` with its
reason. No total will ever match it, and the number is what the sentence is for.

**The command rosters.** `COMMAND_ROSTERS` lists the hand-written files that
must name every skill as `/slushpile:<name>`. Generation already covers the
Cursor router, the README's command list, and the `INSTALL.md` snippet; the
omissions happened on the surfaces a person types out. The help skill named one
short for as long as there have been nine, and it is the file whose whole job is
answering "what do I run next".

## The docs gates

`tests/test_docs.py` covers this directory tree specifically:

- Every relative link, `src`, and `srcset` in every tracked Markdown file
  resolves to a real file on disk. Fenced code blocks are stripped first, so the
  illustrative `<picture>` snippet in the diagram guide is not mistaken for a
  real link.
- Every tracked file under `docs/` is within two hops of
  [docs/index.md](../index.md), except a short list of named exemptions each
  carrying its own reason.
- Every `AGENTS.md` with a sibling `CLAUDE.md` is byte-identical to it. The scan
  is general rather than a hardcoded pair list, so a future pair anywhere in the
  tree is covered without editing the test. The repository root is the one
  exemption: its `AGENTS.md` is generated with a provenance marker and is
  already covered by `sync_docs.py --check`.
- The census: every heading that `README.md` and `INSTALL.md` had before the
  docs were extracted still exists, exactly as often as it did, across those two
  files plus `docs/`. That is what proves an extraction moved prose rather than
  losing it.
- The diagram gates: no `foreignObject` in any committed SVG, both themes
  defining the same class names, the legend table naming exactly those classes,
  and every label line in a `.d2` body appearing in both of its rendered SVGs —
  which is what catches a source edited without a re-render.

## Writing about a wrong count

Prose *about* a stale number trips the sweep the same way the stale number does,
because the sweep reads text and cannot see intent. Describe the wrong number
rather than quoting it. The paragraphs above are written that way for that
reason.
