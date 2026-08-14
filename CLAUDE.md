# Working in this repository

This repository ships one job-application pipeline to several coding agents.
Nine skills and eight agent definitions are the product. Everything else is a
manifest, a template, or a check.

## Generated files

`AGENTS.md` is generated from `CLAUDE.md`. Never edit a generated file, and
never edit inside a `BEGIN GENERATED` / `END GENERATED` marker pair. The next
generator run deletes it.

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
| the `language-nav` region of every translated page and its English original | `TRANSLATED` and `LANGUAGES` |
| the `market-note` region of every translated `README.md` | `MARKET_NOTE` |
| the generated regions of every translated page | copied from the English page |

The dispatch table is in `skills/adversarial-review/SKILL.md`. It is the source
for the review's shape everywhere it appears.

Run this after editing `CLAUDE.md`, after adding, renaming, or removing a skill
or an agent, and after any change to the dispatch table:

```bash
python3 scripts/sync_docs.py
```

`scripts/sync_docs.py --check` is the CI gate.

## Declare it or the gate fails

Every derived fact is looked up by name, and a name matching nothing is an error
rather than a silent omission.

| When you | Also edit |
|---|---|
| add, rename, or remove a skill | `SKILLS` in `scripts/sync_docs.py` |
| reword a sentence stating a derived count | `COUNT_CLAIMS` |
| write a sentence counting a subset on purpose | `COUNT_EXEMPT`, with its reason |
| write a hand-written file that lists every skill as `/slushpile:<name>` | `COMMAND_ROSTERS` |
| add a field to `templates/preferences.yaml` | a skill or agent that reads it, or `PREFERENCES_UNREAD` with its reason |
| add a language to the mirror | `CARDS` in `scripts/make_card.py` |
| add a font weight to a template | `FACES` in `scripts/install_fonts.py`, and `NOTICE.md` |

`SKILLS` carries four names per skill because they are read at four lengths:
the Cursor skill router, the shorter always-on Cursor rule, the README's command
list, and the snippet `INSTALL.md` tells a user to paste. A row whose `rule` is
`None` is kept out of the always-on rule deliberately.

**Counts are swept, not just registered.** Every number-plus-counted-noun in
every `.md`, `.mdc`, `.json`, and `.d2` in the tree must be true right now,
registered or not. The sweep also catches the blind stage's size in shapes like
"N of whom run in parallel". Prose *about* a wrong count trips it the same way
the wrong count does, so describe a stale number rather than quoting it. This
paragraph is written that way for that reason.

Why any of this exists, and what each gate caught:
[docs/architecture/generated-surfaces.md](docs/architecture/generated-surfaces.md).

## Every preferences field must be read

A field in `templates/preferences.yaml` that onboarding asks for and nothing
reads is worse than a missing field. A missing field is noticed; a dead one is
trusted, and the user stops applying their own judgment to whatever they believe
it now handles. Work authorization and application posture both shipped dead.

`test_every_preference_field_is_read_by_something` in
`tests/test_structure.py` walks every leaf and requires a skill or an agent to
name it as a dotted path or as the bare name inside a code span. Prose does not
count: the only match for `posture` was "hiring posture" in a report heading.
A leaf name two blocks share, like `notes`, must be named with its parent, or
one block's reader vouches for the other's.

`PREFERENCES_UNREAD` holds the deliberate exemptions and is checked both ways.
An exemption for a field that no longer exists fails.

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

The hardest rule here, and the one most likely to be broken by accident.

This plugin was productized out of one person's working job-search repository.
Every personal fact became a field in `templates/preferences.yaml` or a section
in `templates/profile.md`. **Nothing in `skills/`, `agents/`, or `docs/` may
hardcode a fact about any user.** No compensation floors, no metro rent tables,
no citizenship, no clearance status, no named employers as the user's own, no
named stories, no "the candidate is open to relocation". A skill that needs one
of those reads it from `preferences.yaml` at run time.

Illustrative examples naming real companies are fine and useful. `"Most capacity
planning candidates come from one side"` as an example of a company-dependent
thesis is teaching. `"The candidate has ten years in secure document
manufacturing"` is a leak.

```bash
python3 scripts/check_no_pii.py
```

It greps `skills/`, `agents/`, `templates/`, and `docs/`. A new leak pattern
that gets through belongs in that script, not in a code review comment.
Full boundary: [docs/architecture/personal-data.md](docs/architecture/personal-data.md).

## Prose standards

The skills are prose another model reads and acts on.

**Say why, not only what.** A rule with its failure mode attached survives
paraphrase, summarization, and a model under load. A bare imperative does not.

**Never leave a rule where its violation is invisible.** "Run the kill-criteria
check" is weaker than "state the checks that passed, not only the ones that
failed — a check that only reports failures is indistinguishable from one that
did not run." Write the observable.

**No em dashes are fine; hedges are not.** Cut hedging that carries no
information. Keep every number, condition, and scope qualifier: a rule that
loses its condition becomes wrong.

## Skills and agents

A skill lives at `skills/<name>/SKILL.md` with frontmatter carrying `name`,
`description`, and optionally `argument-hint` and `license`. The directory name
and the frontmatter `name` must match. Claude Code exposes it as
`/slushpile:<name>`.

An agent lives at `agents/slushpile-<name>.md` with frontmatter carrying `name`,
`description`, and `model`. `model` is required: an agent without one takes
whatever the session is running, which silently flattens a review that mixes
tiers on purpose. The dispatch table names a model per agent too, and the two
are checked against each other. The `slushpile-` prefix keeps these from
colliding with an agent the user already has.

**Voice agents are the one exception.** A voice agent is generated per person by
[written-voice-replication](https://github.com/aaddrick/written-voice-replication)
and named after its author, so a user swapping in their own must keep that name.
`agents/aaddrick-voice.md` is the shipped worked example, named in
`check_configs.VOICE_AGENTS` and exempted from the identity patterns — never
from the contact-details pattern — in `check_no_pii.VOICE_AGENTS`. Do not add a
second one. One example is a demo; two is a library of other people's voices
that nobody asked for.

Two rules about the boundary:

1. **A skill orchestrates. An agent has one job and no awareness of the
   pipeline.** An agent that knows what stage it is in optimizes for the stage
   instead of doing its job.
2. **Binding constraints live in the agent definition, not in the dispatching
   prompt.** An orchestrator that improvises constraints per run produces
   findings that are not comparable across applications, which destroys the
   calibration data the system depends on.

## Docs

`README.md` argues, `INSTALL.md` gets the plugin onto a machine, `docs/` is
everything else. `tests/test_docs.py` gates all of it: relative links resolve,
every `docs/` page is within two hops of `docs/index.md`, every `AGENTS.md`
matches its sibling `CLAUDE.md` byte for byte, and a heading census pins what
`README.md` and `INSTALL.md` held before the docs were extracted.

The census cuts both ways. A new `docs/` heading colliding with a tracked one
raises that heading's count and fails, because the gate then cannot tell the
original going missing from the duplicate covering for it. Rename instead.

### Diagrams

`docs/diagrams/` holds D2 sources and a committed light/dark SVG pair per
diagram. Rendering is manual: `docs/diagrams/render.sh`, needing d2 v0.7.x on
`PATH`. Re-render and commit both SVGs in the same commit as a `.d2` edit, or
the staleness gate fails: every `\n`-separated label segment in a `.d2` body
must appear in both of its SVGs.

Read [docs/diagrams/CLAUDE.md](docs/diagrams/CLAUDE.md) before editing a `.d2`.
It is long because d2 grid connections are center-to-center with no
path-finding, so an edge between non-neighbouring cells cuts through whatever
sits between them. The remaining gates (no `foreignObject`, matching theme class
names, the legend in `docs/architecture/pipeline.md`, `<picture>` with both
sources, alt text, natural width under 1280px) are listed there and in
[generated-surfaces.md](docs/architecture/generated-surfaces.md).

## Translations

`README.md`, `INSTALL.md`, and the reader-facing half of `docs/` ship in English
and five mirrors under `translations/<tag>/`, at the same paths the English tree
uses. `TRANSLATED` and `LANGUAGES` in `scripts/sync_docs.py` declare them;
`tests/test_translations.py` gates them.

**An edit to a fence in `README.md` is an edit to six files.** A translation
drifts in silence: it is the one class of file where nobody who reads the diff
also reads the language.

Checked per page pair, because these reach a reader as a wrong command rather
than as awkward prose:

1. Every command fence, character for character. Commands are copied, never
   translated.
2. Every inline code span, as a multiset. Word order belongs to the translator;
   a dropped or renamed identifier does not. This is also what keeps
   `docs/skills.md` naming every skill in every language.
3. The diagrams a page embeds, and `alt` text at least a quarter the length of
   the English. Translated pages embed the English renders; only the alt text
   moves. The fraction is there because a fixed character floor tuned for Latin
   script fails a correct Chinese translation for being dense. The hero card is
   the one exception: each language gets its own.
4. Reachability from that language's own `docs/index.md`. The language nav only
   ever points at the same page in another language.

Three mechanisms to know before writing in one of these files:

- **The language nav is generated.** Keep the marker pair, leave it empty, run
  the generator.
- **Counts are digits plus a registered noun.** The sweep matches English number
  words, so a spelled-out number in another language is checked by nothing.
  `TRANSLATED_COUNTED_NOUNS` carries the nouns per language, translated prose
  writes `9 habilidades` rather than `nueve habilidades`, and every translated
  page must carry at least as many counted phrases as its English original.
  That last rule is what fails a translation that dropped the sentence.
- **Generated regions are copied in English.** Skill names and slash commands
  are literals a user types. `MARKET_NOTE` is the one piece of translated prose
  living in the generator, so a vocabulary pass over the mirror leaves it
  behind. Check it by hand when terminology moves.

Four of the five are real languages, chosen for market fit. This pipeline models
anglophone hiring: `templates/resume.tex` prints a work authorization block,
`application-builder` enforces one page, `slushpile-ats-simulator` treats a
photo as a parse failure. Every translated `README.md` carries a generated
`market-note` region saying so. Markets whose hiring uses a standardized form
this pipeline would score as broken were left out rather than shipped with a
disclaimer; widening the set is gated on issue #2, not on finding a translator.

The fifth, `en-x-aibro`, is the same manual in the register this category is
sold in, and it is a joke that has to be true. It goes through every gate the
real languages go through, which is why it lives here rather than in a gist: a
parody manual that drifted into being wrong is just a wrong manual, and somebody
will read it for the instructions. Register is the only thing that varies. If a
fact changes, it changes there too, in the same commit.

## Cards

`scripts/make_card.py` draws the images in `.github/assets/`. They are not
interchangeable.

| File | Where it is seen | What it holds |
|---|---|---|
| `hero.png` | the top of `README.md` | the loop in three columns: hook, kept files, seven reviewers |
| `hero-<tag>.png` | the top of `translations/<tag>/README.md` | the same card, in that language |
| `social.png` | uploaded at Settings → General → Social preview | the wordmark and the hook, nothing else |

Redraw and commit after any change to the header text, the workspace file list,
or the agent list:

```bash
python3 scripts/make_card.py
```

It needs Pillow and the vendored fonts in `assets/fonts/`. No gate runs it and
no gate compares the committed PNG against a fresh render, because Pillow
encodes the same pixels differently across versions.

What the script enforces, and what it cannot:

- The middle column must match the workspace files `onboard` writes in Phase 6.
  The script refuses to draw a name that never appears in
  `skills/onboard/SKILL.md`, and refuses when onboarding's scaffold writes a
  file the column neither shows nor records in `OMITTED` with a reason. It
  cannot catch a stale caption. Read those when the workspace changes.
- The right column and the bar grouping the blind agents come from the dispatch
  table through `sync_docs.Facts`, keyed by each agent's English dispatch name,
  so a renamed agent fails per language instead of shifting labels by one.
- `CARDS` holds one `Card` per language and the script refuses to draw when the
  mirror carries a language it has no `Card` for.
  `tests/test_translations.py` holds the other half: every translated
  `README.md` must name its own `hero-<tag>.png`.
- Every line is hand-written rather than wrapped, then measured. The script
  refuses a card whose text crosses into the next column. A Spanish sentence is
  reliably a third longer than the English one, and an overflow reads as the
  three-column structure failing rather than as an error.

Three things no test holds:

- Both canvases are 1280x640 because that is what the unfurl surfaces crop to.
  Check every change to `social.png` at 400px, the only size anyone sees it at.
  The hero and the social card are separate because of that 400px: the hero's
  columns collapse into grey texture there, so the social card is drawn nearly
  empty at two to three times the type size, and the hero stays dense.
- GitHub does not take the social preview from the README. `social.png` is
  uploaded by hand in the repository settings; until someone does, every unfurl
  shows the owner's avatar. Check with:

  ```bash
  gh api graphql -f query='{ repository(owner:"VonTerraProject501c3", name:"slushpile") { usesCustomOpenGraphImage } }'
  ```

- Each `README.md` image `alt` text must say what that card says, in that
  language. It is the only description a screen reader gets and it drifts
  silently. The eyebrow and the hook come from the English `Card`, which both
  the hero and the social preview draw, so the unfurl cannot drift from the
  README subtitle without the hero drifting too. Keep it that way. There is no
  translated social card: GitHub picks one without knowing who is looking.

Changing a Chinese string means re-running `scripts/subset_cjk_font.py` from a
machine with Noto Sans CJK installed. It cuts that face down to the characters
the card draws and writes a coverage manifest; `make_card.py` reads the manifest
and refuses a character the subset lacks, because a missing glyph renders as a
blank box and would ship looking like a rendering bug.

## Document fonts

`assets/fonts/` serves two consumers. The cards use Saira Condensed, Plex Mono
Medium, and the CJK subset. `templates/resume.tex` and
`templates/cover_letter.tex` use Public Sans and Plex Mono Regular and SemiBold.
Only Plex Mono is shared, which is why `install_fonts.py` carries an explicit
`FACES` list rather than installing the directory: nobody should acquire a card
font because they built a resume, least of all the CJK subset, which draws a box
for everything outside its hundred characters. That subset answers to
`Noto Sans CJK SC Subset` so it cannot shadow the real face.

Three decisions that are easy to undo by accident:

- **The templates name families, never paths.** `application-builder` copies
  them into a per-role folder in the user's workspace, at a depth this
  repository does not control. A relative `Path=` resolves to nothing; an
  absolute one names a checkout the next update replaces. Name lookup through
  fontconfig is why `install_fonts.py` exists.
- **Every font is wrapped in `\IfFontExistsTF` with a fallback that ships with a
  normal system.** A missing font is a hard XeLaTeX error, not a warning. The
  document does not look wrong, it does not build.
- **Public Sans comes from the upstream `uswds/public-sans` release, not Google
  Fonts.** Google Fonts ships a variable font, and XeLaTeX cannot select a named
  instance out of one, so `BoldFont={* Bold}` fails against it.

`tests/test_structure.py` requires `FACES` to hold exactly the faces the two
templates name, in both directions. The `NOTICE.md` half is still a discipline:
no gate can tell whether an attribution is correct. Nothing runs
`install_fonts.py` automatically, because it writes into the user's home
directory.

## Testing

```bash
python3 scripts/check_configs.py       # every shipped manifest parses
python3 scripts/check_no_pii.py        # no personal data leaked into the plugin
python3 scripts/sync_docs.py --check   # generated copies match their source
python3 -m unittest discover -s tests -v
```

Run them against committed work. Every one reads the working tree, so a probe
that mutates a file and restores it with `git checkout` or `git clean` destroys
anything uncommitted, including a translation mirror not yet in a commit.

CI runs all four on every pull request and every push to `main`, plus a
plugin-load check that installs this checkout into a scratch config and fails if
it does not reach "enabled". No job filters by path.

## Git

Push to `main`. Pull request creation is set to collaborators only, so a
branch-and-merge cycle with one participant costs a round trip without adding a
reader. Branch when you want the work to sit somewhere before it lands, and
rebase rather than merge.

Run the four checks before you push. CI tells you what you shipped; the local
run tells you what you are about to.

Do not force-push `main`. It breaks every clone and fork and orphans any open
pull request.

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

## Voice

This is the register every hand-written file here is in: this file, `README.md`,
`INSTALL.md`, `docs/`, the skills, the agents, and commit bodies. It is
`agents/aaddrick-voice.md` with the person taken out. That agent replicates one
author for the cover letter; the rules below are the parts of it that describe
writing rather than describing him.

### Shape

**Position first.** State the answer or the recommendation in the first sentence
or two, then the evidence and the reasoning. A reader who stops after one line
should still have the answer.

**Alternate short and long sentences.** Average 8 to 12 words, ranging from 3 to
25. Never write a run of sentences that are all one length. This is the single
most visible difference between prose a person wrote and prose a model wrote.

**Plain words for hard ideas.** Aim at a grade 6 to 8 reading level. Technical
vocabulary is fine when the reader is technical, and does not need defining.

**Contractions, at about one word in fifty.** Not fully expanded formal English,
not every possible contraction either.

**State facts flat. Hedge only what is uncertain.** "I think", "probably", and
"might" belong on opinions and predictions. A measured number, a file path, or a
gate's behavior gets stated directly.

**Concede, then reinforce.** "but", "though", "granted", "to be fair". An
argument that never acknowledges the other side reads as marketing.

**Structure once there are three or more discrete items.** Numbered lists, a
table, or bold labels. Prefer that to a prose wall.

**Report. Do not editorialize.** Say what a thing does and what it costs. Do not
tell the reader how to feel about it. Needing to write "that's significant" means
the paragraph before it failed.

**Stop when the content stops.** No closing sentence that summarizes what the
section already said.

Starting a sentence with "And" or "But" is natural. Rhetorical questions are
rare, and diagnostic when they appear.

### Cut these

Every item is a pattern that appears far more often in generated text than in
written text. A reader who has seen a few of them stops trusting the page.

- **"It's not X, it's Y."** All variants: "Not X. Y." as a two-sentence punch,
  "X, not Y" as a comma correction, "X isn't just Y" as a setup. State the
  positive claim. If the reader needs to know what it isn't, say that second.
- **"Not X" alone as emphasis.** Same move, compressed further.
- **Participial endings.** "The update shipped, revealing a deeper issue." End
  the sentence and start a new one.
- **Significance labels.** "That's the gap between policy and practice." "That
  changes the framing." Naming the meaning of a fact you just stated is
  redundant. If it needs the label, restate the fact better.
- **Vague gestures at meaning.** "says a lot about", "is the most telling thing
  about". Either say what it tells you or let the fact stand.
- **Announced frames.** "Here's what this looks like in practice:", "Let me walk
  through". The content announces itself.
- **Throat-clearing hedges.** The whole "it's worth [verb]-ing" family, plus
  "it's important to note", "generally speaking", "to some extent", "from a
  broader perspective".
- **Dramatic openers and recaps.** "The takeaway:", "The bottom line:",
  "Overall,", "In summary,", "In conclusion,".
- **Transition filler.** "Moreover,", "Furthermore,", "Additionally,".
- **Authority claims.** "Let's be clear,", "To be sure,", "The reality is,",
  "Make no mistake".
- **"From X to Y" as a scene-setter.** Get to the point.
- **Rhythm devices.** Staccato fragment pairs used as punch. The
  X-then-"it's also"-Y two-beat. Repeated triplets of parallel clauses. Two
  consecutive sentences with mirrored structure. One of any of these is fine;
  the pattern repeating across sections is the tell.
- **Mechanical lists.** If every item follows the same syntactic template
  exactly, vary them.
- **Bookend summaries.** If the intro said it, the conclusion should not echo it.
- **Em-dash overuse.** A period or a colon does the same work.
- **Emoji.**
- **These words.** delve, underscore, harness, illuminate, facilitate, bolster,
  tapestry, realm, beacon, cacophony, landscape, paradigm, ecosystem, leverage,
  robust, comprehensive, crucial, utilize, streamline. Plain words instead.

### Check before you commit

1. Sentence lengths visibly vary, and no paragraph is all one length.
2. Facts are unhedged. Opinions are hedged.
3. No reframe, no significance label, no editorial closer.
4. Ordering claims match the source. Saying A happens before B when A is what
   fires B is the error that survives review, because it reads fine.
5. Pronouns still have referents. A cut or a move orphans them silently.
