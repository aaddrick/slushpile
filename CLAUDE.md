# Working in this repository

This repository ships one job-application pipeline to several coding agents.
Nine skills and eight agent definitions are the product. Everything else is a
manifest, a template, or a check.

Read this before you edit anything here.

## The one rule that breaks the build

`AGENTS.md` is generated from `CLAUDE.md`. Never edit `AGENTS.md` directly, and
never edit inside a `BEGIN GENERATED` / `END GENERATED` marker pair. An edit
inside a generated block survives until the next run of the generator, and then
disappears.

Several surfaces describe this pipeline, every one of them lists the skills,
and most of them state the review's shape. None of those facts belongs to the file
that prints it. They live in `skills/`, in `agents/`, and in the dispatch table
inside `skills/adversarial-review/SKILL.md`.

| Generated | Built from |
|---|---|
| all of `AGENTS.md` | `CLAUDE.md` |
| all of `.cursor/skills/slushpile/SKILL.md` | `skills/`, `agents/`, the dispatch table |
| all of `.cursor/rules/slushpile.mdc` | the same |
| the `skills` and `agents` regions of `GEMINI.md` | `skills/`, `agents/`, the dispatch table |
| the `pipeline` and `reviewers` regions of `README.md` | `skills/`, the dispatch table |
| the `harness-snippet` region of `INSTALL.md` | `skills/`, `agents/` |
| the `agent-table` region of `docs/architecture/agents-and-models.md` | `agents/`, the dispatch table |
| all of `docs/architecture/AGENTS.md` | `docs/architecture/CLAUDE.md` |
| all of `docs/diagrams/AGENTS.md` | `docs/diagrams/CLAUDE.md` |
| the `language-nav` region of every translated page and the English page it mirrors | `TRANSLATED` and `LANGUAGES` |
| the `market-note` region of every translated `README.md` | `MARKET_NOTE` |
| the generated regions of every translated page | copied from the English page |

After any edit to `CLAUDE.md`, after adding, renaming, or removing a skill or an
agent, and after any change to the review's dispatch table, run:

```bash
python3 scripts/sync_docs.py
```

`scripts/sync_docs.py --check` is the CI gate. It fails when a copy drifts.

The generator looks every derived fact up by name and fails when a name matches
nothing. Adding a skill without giving it a row in `SKILLS` in that script is an
error, not a silent omission — which is the point, because a skill missing from
the Cursor router is not a wrong file, it is a stage of the pipeline a Cursor
user cannot reach.

`SKILLS` carries one row per skill with the four names it goes by: the Cursor
skill router, the shorter always-on Cursor rule, the README's command list, and
the snippet `INSTALL.md` tells a user to paste. They are four fields rather than
one because they are read in different places at different lengths, and
collapsing them would make every surface read like the least specific one. A row
whose `rule` is `None` is kept out of the always-on rule deliberately, and that
decision is recorded there rather than being an omission nobody notices.

A few sentences state a derived number in prose — "nine skills and eight agent
definitions" — where wrapping one sentence in generator markers would cost more
than it buys. Those live in `COUNT_CLAIMS` and are checked rather than written:
the sentence must appear with the right number in it. Rewording one means
editing that table, which is the prompt to check whether the number is still
right.

A registered claim only covers a sentence somebody registered, so a count that
nobody thought about drifts in silence. That is not hypothetical: `INSTALL.md`,
the help skill, and the marketplace manifest each counted the skills one short
for as long as there have been nine, because none of the three had a row. So a
sweep runs next to the claims. It reads every `.md`, `.mdc`, and `.json` in the
tree for a counted noun — skills, agents, agent definitions, reviewers,
personas — and fails on any number that is not currently true, registered or
not.

The sweep also covers the size of the review's blind stage, which is stated in
prose across six hand-written files and in shapes a noun list alone does not
see: "N of whom run in parallel", "the first N are supposed to be blind", "N
parallel ones". Those go through a second pattern with the connectives
whitelisted, because a rule loose enough to catch them from the noun alone also
catches "three parallel phrases" in a voice agent's style notes. Before this,
the only thing pinning that number was a literal in `tests/test_structure.py`,
which fails naming the number and none of the files — so the cheapest way back
to green was to edit the literal and ship the prose it contradicted.

A second gate covers rosters rather than counts. `COMMAND_ROSTERS` in the
generator lists the hand-written files that must name every skill as
`/slushpile:<name>`, and the help skill and `docs/skills.md` are both in it. Generation already covers the
Cursor router, the README's command list, and the `INSTALL.md` snippet; the
omissions happened on the surfaces a person types out. The help skill named one
short for as long as there have been nine, and it is the file whose whole job is
answering "what do I run next", so the skill it dropped was unreachable from the
only place a confused user looks.

A roster written as prose rather than as commands cannot be checked that way.
The marketplace manifest's description states a number and then enumerates the
skills, and it shipped listing an item that is a behavior rather than a skill
while dropping a real one. `tests/test_structure.py` counts the items after `The
skills:` against the number of skills, which is why those blurbs have to stay
comma-free.

Two consequences worth knowing before you write about this pipeline.

A sentence that counts a subset on purpose — the agents that parse a posting
verbatim, say — goes in `COUNT_EXEMPT` with its reason. No total will ever match
it, and the number is what the sentence is for.

Prose *about* a wrong count trips the sweep the same way the wrong count does,
because the sweep reads text and cannot see intent. Describe the stale number
rather than quoting it. This paragraph is written that way for that reason.

## Which file your tool reads

| Tool | Reads | For |
|---|---|---|
| Claude Code | `CLAUDE.md` | these standards |
| Cursor | `AGENTS.md` and `CLAUDE.md`, both automatic | these standards |
| Gemini CLI | `AGENTS.md`, then `GEMINI.md` | these standards, then the pipeline |
| Codex, and any other `AGENTS.md` harness | `AGENTS.md` | these standards |

`GEMINI.md` is not a repository guide. `gemini-extension.json` names it as the
extension's context file, so it is what a Gemini CLI user gets on install.
Leave it describing the pipeline.

## Never put a person in this repository

The single hardest rule here, and the one most likely to be broken by accident.

This plugin was productized out of one person's working job-search repository.
Every personal fact in that repository became a field in `templates/preferences.yaml`
or a section in `templates/profile.md`. **Nothing in `skills/` or `agents/` may
hardcode a fact about any user.**

That means no compensation floors, no metro rent tables, no citizenship, no
clearance status, no named employers as the user's own, no named stories, no
"the candidate is open to relocation". A skill that needs one of those reads it
from `preferences.yaml` at run time.

Illustrative examples naming real companies are fine, and useful — they teach
the pattern. `"Most capacity planning candidates come from one side"` as an
example of a company-dependent thesis is teaching. `"The candidate has ten
years in secure document manufacturing"` is a leak.

Before committing, run:

```bash
python3 scripts/check_no_pii.py
```

It greps `skills/`, `agents/`, and `templates/` for the patterns that leaked
last time. A new leak pattern that gets through belongs in that script, not in
a code review comment.

## Prose standards

The skills are prose that another model reads and acts on. Three consequences.

**Say why, not only what.** A rule with its reasoning attached survives
paraphrase, summarization, and a model under load. A bare imperative does not.
Every non-obvious rule in these skills carries its failure mode, because the
model is going to hit that failure mode and the reason is what stops it.

**Never leave a rule where its violation is invisible.** "Run the kill-criteria
check" is weaker than "state the checks that passed, not only the ones that
failed — a check that only reports failures is indistinguishable from one that
did not run." Write the observable.

**No em dashes are fine; hedges are not.** Cut hedging that carries no
information. Keep a hedge that carries real uncertainty, and keep every number,
condition, and scope qualifier. A rule that loses its condition becomes wrong.

## Skills and agents

A skill lives at `skills/<name>/SKILL.md` with YAML frontmatter carrying
`name`, `description`, and optionally `argument-hint` and `license`. The
directory name and the frontmatter `name` must match. Claude Code exposes it as
`/slushpile:<name>`.

An agent lives at `agents/slushpile-<name>.md` with frontmatter carrying `name`,
`description`, and `model`. All three are required, `model` included: an agent
without one takes whatever the session is running, which silently flattens a
review that mixes tiers on purpose. Every pipeline agent is prefixed
`slushpile-` so it cannot collide with an agent the user already has.

The review's dispatch table names a model per agent too, and the two are checked
against each other. The frontmatter is what a harness dispatches on; the column
is documentation of it. The generator captured that column and threw it away for
as long as it existed, which made it the one fact in that table nothing read.

**Voice agents are the one exception**, and it is deliberate. A voice agent is
generated per person by
[written-voice-replication](https://github.com/aaddrick/written-voice-replication)
and named after its author, so a user swapping in their own must be able to
keep that name. `agents/aaddrick-voice.md` is that pipeline's public worked
example, shipped so slushpile runs before a user has generated one. It is named
in `check_configs.VOICE_AGENTS` and exempted from the identity patterns — but
never from the contact-details pattern — in `check_no_pii.VOICE_AGENTS`.

Do not add a second voice agent here. One example is a demo; two is a library
of other people's voices that nobody asked for.

Two rules about the boundary between them:

1. **A skill orchestrates. An agent has one job and no awareness of the
   pipeline.** An agent that knows what stage it is in will optimize for the
   stage instead of doing its job.
2. **Binding constraints live in the agent definition, not in the dispatching
   prompt.** An orchestrator that improvises extra constraints per run produces
   findings that are not comparable across applications, which destroys the
   calibration data the whole system depends on.

## The docs tree

`README.md` argues, `INSTALL.md` gets the plugin onto a machine, and `docs/` is
everything else. It was extracted out of those two files rather than written
beside them, which is why `tests/test_docs.py` carries a census: every level-1
and level-2 heading those files had before the extraction, recorded in
`tests/fixtures/base-headings.json`, must still appear exactly as often across
`README.md`, `INSTALL.md`, and `docs/`. A section dropped mid-move fails there.

The census cuts the other way too, and that is the half worth knowing before
you add a page. A new `docs/` heading that collides with one the fixture tracks
raises that heading's count and fails, because from then on the gate could not
tell the original going missing from the duplicate covering for it. Two
headings had to be renamed while this tree was written for exactly that reason.

Three more gates live in the same file:

- **Relative links.** Every markdown link, `src`, and `srcset` in every tracked
  `.md` resolves on disk. Fenced code blocks are stripped first, so the
  illustrative `<picture>` snippet in the diagram guide is not read as a real
  link.
- **Reachability.** Every file under `docs/` is within two hops of
  `docs/index.md`. A page nothing links to is a page nobody reads, and it looks
  exactly like a linked one in a diff. Three files are exempt by name, each
  with its reason in the test.
- **Freeze pairs.** Any `<dir>/AGENTS.md` with a sibling `CLAUDE.md` must be
  byte-identical to it. The scan is general rather than a list of paths, so a
  future pair anywhere is covered without editing the test. The repository root
  is the one exemption, because its `AGENTS.md` carries a provenance header and
  `sync_docs.py --check` already covers it.

`docs/` is scanned by `check_no_pii.py` alongside `skills/`, `agents/`, and
`templates/`. Documentation is where a real employer or a real salary gets used
as an example because it was the one at hand. This is not hypothetical either:
the leak example on `docs/architecture/personal-data.md` had to be paraphrased
to survive the gate that page documents.

### The diagrams

`docs/diagrams/` holds D2 sources and the light and dark SVG pair rendered from
each. The rendering is manual — `docs/diagrams/render.sh`, needing d2 v0.7.x on
`PATH` — and the SVGs are committed so nobody needs d2 installed to read the
docs, only to change them.

`docs/diagrams/CLAUDE.md` is the authoring guide, and it is long because d2
grids have sharp edges: connections are center-to-center with no path-finding,
so an edge between non-neighbouring cells cuts through whatever sits between
them. Read it before editing a `.d2`.

The gate that matters most here is the staleness one. Every `\n`-separated
label segment in a `.d2` body must appear in both of its committed SVGs, so a
source edited without a re-render fails the suite instead of shipping a picture
of a pipeline that no longer exists. `.d2` files are also read by the count
sweep, which is what keeps a label reading "five blind" honest.

The rest are cheaper and still worth having: no `foreignObject` in any SVG (a
`|md|` label produces one, and it disappears when GitHub loads the SVG through
an `<img>`), both themes defining the same class names, the legend in
`docs/architecture/pipeline.md` naming exactly those classes, every diagram
embedded in a `<picture>` with both sources, alt text on every embedded diagram,
and a natural width under 1280px so the text is still legible after GitHub
scales it into a 1012px column.

## The translations

`README.md`, `INSTALL.md`, and the reader-facing half of `docs/` ship in English
and in five more, mirrored under `translations/<tag>/` at the same
paths the English tree uses. `TRANSLATED` and `LANGUAGES` in `scripts/sync_docs.py`
are the declarations; `tests/test_translations.py` is the gate.

**An edit to a fence in `README.md` is an edit to five files.** That is the rule
worth internalising before you touch a translated page or the English page it
mirrors. A translation drifts in silence, because it is the one class of file
where nobody who can read the diff also reads the language, and the ordinary
review that catches a stale command everywhere else does not happen here.

The mirror keeps the English path shape on purpose. A link between two
translated pages is then byte-identical to the English link, so a translator
never recomputes a path, and the relative-link gate in `tests/test_docs.py`
covers the mirror without knowing it exists. Links *leaving* the translated set
point back at the English original.

Four things are checked per page pair, and the reasoning for each is the same:
these are the parts of a page that reach a reader as a wrong command rather than
as awkward prose.

1. Every command fence, character for character. Commands are copied, never
   translated.
2. Every inline code span, as a multiset. Word order belongs to the translator;
   a dropped or renamed identifier does not. This is also what keeps
   `docs/skills.md` naming every skill in every language, so that roster needs
   no separate check.
3. The diagrams a page embeds, and `alt` text at least a quarter the length of
   the English. Translated pages embed the English renders; only the alt text
   moves. The fraction is there because a fixed character floor tuned for Latin
   script fails a correct Chinese translation for being dense. The hero card at
   the top of each `README.md` is the exception, and the only one: it is a
   picture made of sentences rather than of boxes and arrows, so each language
   gets its own, drawn by `scripts/make_card.py` and checked by the same file.
4. Reachability from that language's own `docs/index.md`, because a reader who
   cannot reach a page from their index has no way to know it exists — the
   language nav only ever points at the same page in another language.

Two mechanisms are worth knowing before you write in one of these files.

**The language nav is generated.** There are ninety of them, each with five
links whose relative depth differs by directory. Keep the marker pair,
leave it empty, run the generator.

**Counts are digits plus a registered noun.** The count sweep matches English
number words, so a spelled-out number in another language is a count nothing
checks — and a sweep that matches nothing reports success, which is the failure
this repository already shipped three times in English where a check existed. So
`TRANSLATED_COUNTED_NOUNS` carries the nouns per language, translated prose
writes `9 habilidades` rather than `nueve habilidades`, and every translated page
must carry at least as many counted phrases as the English page it mirrors. That
last rule is the one that matters: it is what fails a translation that dropped
the sentence instead of getting the number wrong.

Generated regions are copied into the mirror in English. Skill names and slash
commands are literals a user types, so there is nothing in those tables to
translate, and a per-language rendering would make every new skill block on four
translations before the generator could run.

`MARKET_NOTE` is the one piece of translated prose that lives in the generator
rather than in the mirror. A pass that normalizes a language's vocabulary sweeps
every page and silently leaves that paragraph behind, so check it by hand when
the terminology moves.

Four of the five are real languages, chosen for market fit rather than speaker
count. This pipeline models anglophone hiring — `templates/resume.tex` prints a
work authorization block, `application-builder` enforces one page,
`slushpile-ats-simulator` treats a photo as a parse failure. A manual in
someone's language is an implicit promise the tool fits their market. Every
translated `README.md` therefore carries a generated `market-note` region saying
what market that is, and languages whose domestic hiring uses a standardized
form this pipeline would score as broken were left out rather than shipped with
a disclaimer. Widening the set is gated on issue #2, not on finding a
translator.

The fifth, `en-x-aibro`, is the same manual in the register this category is
sold in, and it is a joke that has to be true. It goes through every gate the
real languages go through: its commands are byte-identical, its counts are
checked, its inline identifiers are compared as a multiset against the English
page. That is the whole reason it lives here rather than in a gist — a parody
manual that drifted into being wrong is just a wrong manual, and somebody will
read it for the instructions. The tag is BCP-47's private-use form because it is
English, and pretending otherwise would break the one thing a tag is for.

Two consequences for editing. A doc change is now a six-file change rather than
a five-file one. And the register is the only thing that varies: if a fact
changes, it changes there too, in the same commit.

## Testing

```bash
python3 scripts/check_configs.py       # every shipped manifest parses
python3 scripts/check_no_pii.py        # no personal data leaked into the plugin
python3 scripts/sync_docs.py --check   # generated copies match their source
python3 -m unittest discover -s tests -v
```

`tests/test_docs.py` is discovered by that last command; it is where the
link, reachability, freeze-pair, census, and diagram gates live, and
`tests/test_translations.py` beside it holds the mirror's. Nothing runs
`docs/diagrams/render.sh` for you, so re-render and commit both SVGs in the same
commit as a `.d2` edit.

Run the gates against committed work. Every one of these reads the working tree,
so a probe that mutates a file and then restores it with `git checkout` or
`git clean` destroys anything uncommitted — including a translation mirror that
is not yet in a commit.

CI runs all four on every pull request and on every push to `main`, plus a
plugin-load check that installs this checkout into a scratch config and fails if
it does not reach "enabled". No job filters by path, so a change that looks like
documentation still has to prove the plugin loads.

## The cards

`scripts/make_card.py` draws the images in `.github/assets/`, and they are not
interchangeable.

| File | Where it is seen | What it holds |
|---|---|---|
| `hero.png` | the top of `README.md` | the loop in three columns: hook, kept files, seven reviewers |
| `hero-<tag>.png` | the top of `translations/<tag>/README.md` | the same card, in that language |
| `social.png` | uploaded at Settings → General → Social preview | the wordmark and the hook, nothing else |

The hero and the social card are separate because they are read at different
sizes. An unfurl in
LinkedIn, Signal, Teams, or Slack renders around 400px wide, where the hero's
columns collapse into grey texture. Rather than thin the hero until it survives
a thumbnail, the social card is drawn nearly empty at two to three times the
type size. The hero is then free to be dense, because nothing reads it at 400px.

GitHub does not take the social preview from the README. `social.png` has to be
uploaded by hand in the repository settings, and until someone does, every
unfurl shows the owner's avatar. Check with:

```bash
gh api graphql -f query='{ repository(owner:"VonTerraProject501c3", name:"slushpile") { usesCustomOpenGraphImage } }'
```

Redraw all of them after any change to the header text, the file list, or the
agent list:

```bash
python3 scripts/make_card.py
```

It needs Pillow and reads the vendored fonts in `assets/fonts/`. Pillow is not a
test dependency, so no gate runs this script and no gate compares the committed
PNG against a fresh render. Pillow encodes the same pixels differently across
versions, so a checksum gate would fail on an unrelated upgrade. Commit the
redrawn files yourself.

The hero is the one image here that is mostly words, which is why it is the one
image translated rather than captioned. It is also the first thing on the page,
so a reader who arrived in their own language otherwise reads the pitch in
somebody else's before reaching a word of the translation. `CARDS` in the script
holds one `Card` per language and the script refuses to draw when the mirror
carries a language it has no `Card` for, on the same rule as a skill missing
from `SKILLS`. `tests/test_translations.py` holds the other half, because the
script cannot see whether the page it drew for actually embeds the result:
every translated `README.md` must name its own `hero-<tag>.png`.

Three things about writing those cards. Every line is written by hand rather
than wrapped, because the columns are narrow and a break is a choice about what
the card emphasises. Every line is then measured, and the script refuses to draw
a card whose text crosses into the next column — a Spanish sentence is reliably
a third longer than the English one it translates, and an overflow does not look
like an overflow, it looks like the three-column structure failing. And the
strings should say what that page's `alt` text says: the alt is the description
of that card, in that language, and the two drifting apart is a screen reader
describing a picture nobody else is looking at.

Two of the three facts the card depends on are now held by the script itself:

1. The middle column lists the durable workspace files, and it must match what
   `onboard` actually writes in Phase 6. Add a file to the workspace without
   adding it here and the card is quietly wrong about the thing it exists to
   claim. `make_card.py` refuses to draw when a name in that column never
   appears in `skills/onboard/SKILL.md`, and refuses again when onboarding's
   scaffold block writes a file the column neither shows nor records in
   `OMITTED` with its reason. The first direction catches a deletion; the second
   is the one that was open, and it is the one that matters, because a workspace
   file nobody thought to add leaves the card short on its own central claim.
   Neither catches a stale caption, so read those when the workspace changes.
2. The right column lists the agents in dispatch order, and the bar grouping the
   blind ones is the claim that they run concurrently. Both are read from the
   dispatch table through `sync_docs.Facts`, so changing the pipeline's shape in
   `adversarial-review` moves the column with it rather than leaving a diagram
   of a system that no longer exists. Redraw and commit after any such change.
   Every number any card prints comes from the same place, in every language,
   and a card keys its reviewer labels by the agent's English dispatch name — so
   a renamed agent fails loudly per language instead of shifting one column's
   labels down by one.

The third no test can hold:

3. Both canvases are 1280x640 because that is what the unfurl surfaces crop to.
   A taller card loses its top and bottom edge in a preview. Check every change
   to `social.png` at 400px, since that is the only size anyone sees it at, and
   it is the one card with no room to hide an illegible element.

The eyebrow and the hook come from the English `Card`, which both the hero and
the social preview draw, so the unfurl cannot drift from the README subtitle
without the hero drifting too. Keep it that way — the alternative is discovering
that the image people actually see says something the repository stopped
claiming. There is no translated social card: a repository has one social
preview and GitHub picks it without knowing who is looking.

Update each `README.md` image `alt` text alongside its card. It is the only
description a screen reader gets, and it drifts silently.

The Chinese card needs a font this repository would otherwise have no reason to
carry: neither Saira Condensed nor Plex Mono has a Han glyph, and a full CJK
face is twenty thousand of them. `scripts/subset_cjk_font.py` cuts Noto Sans CJK
SC down to the characters that one card draws, which is about a hundred, and
writes the two faces plus a coverage manifest into `assets/fonts/`. Change a
Chinese string and you must run it, from a machine with Noto Sans CJK installed
or with the path to a copy — `make_card.py` reads that manifest and refuses to
draw a character the subset lacks, because a missing glyph renders as a blank
box rather than as an error and would ship looking like a rendering bug.

## The document fonts

`assets/fonts/` now serves two unrelated consumers. `make_card.py` draws the
cards with Saira Condensed, Plex Mono Medium, and the subset of Noto Sans CJK SC
the Chinese card needs. `templates/resume.tex` and `templates/cover_letter.tex`
are set in Public Sans and Plex Mono Regular and SemiBold. Only Plex Mono is
shared, which is why there is one directory instead of two, and why
`install_fonts.py` carries an explicit `FACES` list rather than installing the
directory: nobody's system should acquire a card font because they built a
resume, least of all the CJK subset, which holds about a hundred characters and
draws a box for everything else. That subset carries its own family name,
`Noto Sans CJK SC Subset`, for the same reason: a hundred-character file
answering to `Noto Sans CJK SC` would shadow the real face wherever it landed.

Three decisions here are easy to undo by accident.

**The templates name families, never paths.** `application-builder` copies them
into a per-role folder inside the user's workspace, at a depth this repository
does not control, so a relative `Path=` resolves to nothing and an absolute one
names a checkout the next plugin update replaces. Name-based lookup goes through
fontconfig and works from anywhere, which is the whole reason `install_fonts.py`
exists rather than the templates pointing at `assets/fonts/` directly.

**Every font is wrapped in `\IfFontExistsTF` with a fallback that ships with a
normal system.** A missing font is a hard XeLaTeX error, not a warning: the
document does not look wrong, it does not build. A template that names a family
without a fallback works on the author's machine and nowhere else.

**Public Sans comes from the upstream `uswds/public-sans` release, not Google
Fonts.** Google Fonts ships it as a variable font, and XeLaTeX cannot select a
named instance out of one, so `BoldFont={* Bold}` fails against that file. If
you ever refresh these, take the static TTFs.

Adding a weight to a template means adding it to `FACES` in `install_fonts.py`
and to the typeface section of `NOTICE.md`. Miss the first and the template
silently takes the fallback branch on a machine where the user did everything
right, which reads as the installer being broken. Miss the second and the OFL
attribution stops matching what ships.

The first half is now a test rather than a discipline: `tests/test_structure.py`
parses both templates' font declarations and requires `FACES` to hold exactly
the faces they name, in both directions. A face in `FACES` that no template asks
for is a font installed into someone's home directory for no reason, which is
the same class of error pointing the other way. The `NOTICE.md` half is still a
discipline, because no gate can tell whether an attribution is correct.

Nothing runs `install_fonts.py` automatically and no gate calls it. It writes
into the user's home directory, which is not something a documentation check or
an onboarding interview should do on its own initiative.

## Git

Push to `main`. Pull request creation on this repository is set to
collaborators only, so there is no outside patch waiting for review, and a
branch-and-merge cycle with one participant costs a round trip without adding a
reader. Branch when you want the work to sit somewhere before it lands, and
rebase rather than merge, because the history is linear and worth keeping that
way.

Run the four checks before you push, not after. Both workflows also run on every
push to `main`, but by then the commit is public: CI tells you what you shipped,
the local run tells you what you are about to.

Do not force-push `main`. Rewriting published history breaks every clone and
fork, and orphans any pull request a collaborator has open. It is a deliberate
decision made out loud, not a way to tidy a commit you dislike.

A commit subject states what changed. The body states why, with the evidence.

## Layout

| Path | What it holds |
|---|---|
| `skills/` | the nine skills. The product. |
| `agents/` | the eight agent definitions. The product. |
| `templates/` | what a user's workspace gets scaffolded from |
| `docs/` | the manual, its architecture pages, and the D2 diagram sources |
| `translations/` | the manual again, in five more languages, mirroring the English paths |
| `scripts/check_configs.py` | parses every shipped manifest |
| `scripts/check_no_pii.py` | the personal-data gate |
| `scripts/sync_docs.py` | the generator and its `--check` gate |
| `scripts/make_card.py` | draws the hero card in every language, and `social.png` |
| `scripts/subset_cjk_font.py` | cuts the Chinese card's font down to the characters it draws |
| `docs/diagrams/render.sh` | renders every diagram's light and dark SVG from its `.d2` |
| `scripts/install_fonts.py` | installs the document fonts into the user's font directory |
| `assets/fonts/` | the vendored fonts the card and the templates are drawn with, and all three OFL licenses |
| `.claude-plugin/`, `.codex-plugin/`, `gemini-extension.json` | plugin manifests |
| `GEMINI.md` | the pipeline, as the Gemini extension's context file |
| `.gemini/settings.json` | the context file list for an agent working here |
| `.cursor/` | the Cursor rule and skill routing |
