# Working on the pipeline diagrams

Read this before editing anything in `docs/diagrams/`. Most of what follows is
a constraint of the tool rather than a preference, and every one of them is
cheaper to read here than to rediscover by rendering something that compiled
and was unreadable once it landed in `docs/architecture/pipeline.md`.

> **Parity note:** `CLAUDE.md` and `AGENTS.md` in this directory are
> byte-identical on purpose, so an agent finds the same guidance under
> whichever name its harness looks for. `scripts/sync_docs.py` writes the
> `AGENTS.md` twin from this file, and `tests/test_docs.py` fails if they ever
> differ. Edit `CLAUDE.md` and run the generator; never edit the twin.

## What lives here

| File | Role |
| --- | --- |
| `theme-light.d2`, `theme-dark.d2` | Palette and class definitions. No nodes, no edges. |
| `pipeline-overview.d2` | The hero diagram: onboarding to outcomes, and the loop back. |
| `phase-{onboard,search,build,review}.d2` | One diagram per skill that has internal shape. |
| `render.sh` | Regenerates every SVG. The only supported way to produce them. |
| `*-light.svg`, `*-dark.svg` | **Generated.** Never hand-edit. |

Diagram bodies contain **no colors**. They reference class names only. All
color lives in the two theme files.

## What you need to render them

[D2](https://d2lang.com) v0.7.x. Nothing in this repository vendors it and no
gate installs it, so you supply the binary:

```bash
# Either put d2 on PATH, or point render.sh at it:
D2=/path/to/d2 ./render.sh
```

To fetch it without piping a remote script into a shell:

```bash
curl -fsSL -o d2.tar.gz \
  https://github.com/terrastruct/d2/releases/download/v0.7.1/d2-v0.7.1-linux-amd64.tar.gz
tar -xzf d2.tar.gz          # binary lands at d2-v0.7.1/bin/d2
```

## How to make a change

1. Edit the `.d2` body, or a theme file.
2. Run `./render.sh`. It writes **both** the light and dark SVG for every
   diagram. Always commit the pair.
3. Eyeball the result at the width it will actually be viewed at. See
   "Verifying" below. Do not skip this: nearly every rule on this page exists
   because something passed a compile and failed a look.
4. If you added or removed a diagram, update the `<picture>` blocks in
   `docs/architecture/pipeline.md` to match.
5. If you changed what a class *means*, update the legend table in
   `docs/architecture/pipeline.md`. `tests/test_docs.py` checks that the legend
   and the theme files name the same classes, so a new class with no legend row
   fails the suite — but no gate can tell whether the row's prose is still true.

`render.sh` builds each diagram by **concatenating** a theme file and a body
file into a temp file. That is why bodies must not declare their own `vars` or
`classes` blocks. They would collide with the theme's.

## Theme contract

`theme-light.d2` and `theme-dark.d2` must define **exactly the same class
names**. A body that references a class only one theme defines still compiles;
that mode's render silently falls back to d2 defaults, and you find out by
looking. `tests/test_docs.py` checks the two class lists against each other for
that reason.

Current vocabulary. Keep it in sync with the legend in
`docs/architecture/pipeline.md`:

| Class | Means |
| --- | --- |
| `stage` | An ordinary step the orchestrating skill performs itself |
| `agent` | A dispatched persona: a subagent with its own definition in `agents/` |
| `gate` | A gate or a capped loop: somewhere the run can iterate, stall, or stop |
| `memory` | A durable workspace file, written once and read by every later stage |
| `human` | The one place the user is required |
| `terminal` | A terminal state for that diagram |
| `phase` | A container grouping cells that run together |
| `flow` | A normal forward edge |
| `loop` | A backward edge: rework, re-review, another round (dashed amber) |
| `writeback` | An edge that writes into the workspace memory (dashed cyan) |

`agent` and `stage` are separate classes because the distinction is the one
this repository cares most about. A reader who cannot tell which boxes are
dispatched personas cannot tell what the review would lose on a harness with no
subagent dispatch.

## Hard-won rules

### d2 comments are `#`, not `//`

`//` is not a comment. d2 parses those lines as shape declarations, and you get
a bogus node plus a parse error somewhere else in the file, often pointing at a
line that is fine.

### Never use `|md|` blocks

Markdown blocks render into `<svg:foreignObject>`. That is HTML inside an SVG,
and support for it collapses the moment the SVG is loaded through an `<img>`
tag, which is exactly how GitHub embeds these.

Use plain quoted labels with `\n` instead. They render as native `<text>`
elements, d2 sizes the box correctly around them, and they work everywhere.
`tests/test_docs.py` asserts zero `foreignObject` elements across every
committed SVG, so this one is a gate rather than a discipline.

### Two themes exist because d2 inlines custom fills

d2 does emit a `prefers-color-scheme` block, but only for its *built-in* theme
colors. Any `style.fill` you write yourself is inlined as a literal hex value
and will not adapt. One SVG therefore cannot carry both palettes.

So: two renders per diagram, paired in `docs/architecture/pipeline.md` through
a `<picture>` element, which GitHub officially supports:

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../diagrams/NAME-dark.svg">
  <img alt="..." src="../diagrams/NAME-light.svg">
</picture>
```

### The canvas must stay transparent

Both themes set a root-level `style.fill: transparent`. Without it d2 paints an
opaque white background rect, which renders as a white slab behind the dark
diagram on GitHub's dark theme. Do not remove it.

### Four of the five are grid snakes; review is the exception

Every diagram sets `grid-rows` / `grid-columns`, which bypasses the layout
engine entirely, so the `layout-engine: dagre` in the theme files currently
governs nothing. Keep it: a body that drops its grid falls back to dagre rather
than to no engine at all.

Reading order is **boustrophedon**: row 1 left-to-right, the flow drops straight
down the last column, row 2 reads back right-to-left. That is what keeps the
wrap edge orthogonal. A naive left-to-right wrap sends a diagonal all the way
back across the image.

Cells fill **row-major over declaration order**, and declaration order is the
only thing that controls placement. Declare `grid-rows` *before* `grid-columns`;
reversed, d2 packs the cells column-major instead.

`phase-review.d2` is a grid too, but it is the one diagram with a fan-out, and
it only fits in a grid because the fan is wrapped in a container. See below.

### THE DIAGONAL RULE

Grid connections are center-to-center straight segments with **no path-finding**
([d2 docs](https://d2lang.com/tour/grid-diagrams/)). An edge is orthogonal only
when its two cells are *neighbours* sharing a row or a column:

- same row, adjacent columns → horizontal
- same column, adjacent rows → vertical
- anything else → a diagonal
- an edge spanning two cells in a row draws straight **through** the cell
  between them

So place nodes to suit the edges, not the reading order, and check every new
edge against this rule. There is no engine to rescue a bad placement.

Two consequences to know before you fight them:

- **A fan-out cannot be drawn as sibling cells.** Only one target can share a
  column with its source, so every other branch edge is a diagonal. Wrap the
  fan in a container and the fan becomes one edge, which is what
  `phase-review.d2` does with the blind stage.
- **Neither engine can wrap a chain for you.** d2 does not expose ELK's
  [`wrapping.strategy`](https://eclipse.dev/elk/reference/options/org-eclipse-elk-layered-wrapping-strategy.html),
  and a `direction` set on a container is ignored by both dagre and ELK. Grid is
  the only wrap mechanism. Do not spend time re-testing these.

### Column width and row height are shared

A grid column takes the width of its widest cell and a grid row the height of
its tallest, so one large cell distorts everything beside and beneath it.

`phase-review.d2` shows both directions at once. Its blind-stage container is a
nested 2×3 grid, which makes it the widest cell in its column and the tallest in
its row. The gatekeeper below it is stretched to the container's width, and the
two cells beside it are stretched to the container's height. None of that can be
styled away, because the container *is* one cell.

The fix is not to shrink the container. It is to **give the stretched cells
enough label to fill the space they are given** — the gatekeeper carries three
lines for exactly this reason. An empty stretched box reads as a rendering
fault; a full one reads as a deliberate emphasis.

### Two-cycles get one bidirectional connector

Grid draws both directions of a 2-cycle on the same center-to-center line, so
writing `a -> b` and `b -> a` stacks two labels on top of each other. Use a
single `a <-> b` with a combined label instead.

Keep those labels short and multi-line. The label is centered on the connector,
so a label wider than the gap hides the very edge it describes. Widen
`horizontal-gap` or shorten the text.

### An edge the grid cannot draw goes in a label, not in a diagonal

Two real edges in this set are stated in prose inside a node's own label:

- `phase-search.d2`'s contrarian gate can demote a tier, which re-derives the
  fit score four cells back.
- `phase-review.d2`'s gatekeeper sends the run back through the whole pipeline
  with fresh agent instances when the materials change.

Both would be long diagonals cutting through intervening boxes. A sentence in
the node that owns the behaviour is more accurate than a line that crosses
three cells it has nothing to do with.

### An edge must not overstate which thing gated it

The hiring manager runs after **all five** blind specialists return. The edge
into it therefore leaves the container, not any one specialist box. An edge
sourced from a single cell of a joint condition reads as that cell alone being
the gate, which is a different pipeline.

### Size budget: the SVG is responsive, so natural width is display width

d2's root `<svg>` carries a `viewBox` and **no** width or height, so it scales
to whatever container holds it. GitHub's markdown column is roughly **1012px**.
That cuts both ways: too wide and it scales down, shrinking the text with it;
too narrow and it scales **up** into a wall of enormous boxes.

Aim for a natural width near 1012px. Current widths run 1188 to 1232 and heights
338 to 578, which renders between 0.82 and 0.85 scale — 14px label text lands
around 12px, which is legible. Past roughly 1300 it is not. Check after every
edit:

```bash
for f in *-light.svg; do
  printf "%-30s " "$f"; grep -o 'viewBox="[^"]*"' "$f" | head -1
done
```

Width is driven by the longest label line in the widest column, so keep body
lines to about 30 characters and break them yourself. Raising the font size does
not buy legibility: box widths grow with the text, so the ratio barely moves.

## Verifying

Compiling is not verifying. Render at real width and look at it:

```bash
cat > /tmp/preview.html <<HTML
<html><body style="margin:0;background:#fff">
<div style="max-width:1012px;margin:0 auto">
  <img src="file://$PWD/phase-review-light.svg" style="max-width:100%">
</div></body></html>
HTML
google-chrome --headless --disable-gpu --screenshot=/tmp/preview.png \
  --window-size=1030,900 --hide-scrollbars file:///tmp/preview.html
```

Swap the background to `#0d1117` and the `-light` suffix to `-dark` to check
dark mode. Check both. They are separate files, and a theme edit can break one
while leaving the other correct.

`inkscape` and `rsvg-convert` will *not* show you what GitHub shows; they warn
`unknown type: svg:foreignObject` and skip content. Use a browser.

## Repo conventions that apply here

- The generated SVGs are intentionally committed. Contributors and CI do not
  need d2 installed to read the docs, only to change them.
- A change to a skill's stage order must update both the affected `.d2` **and**
  the committed SVGs in the same commit. `tests/test_docs.py` checks that every
  label line in a `.d2` body appears in both of its SVGs, so an edited source
  with a stale render fails the suite rather than shipping a picture of a
  pipeline that no longer exists.
- `.d2` bodies are read by the count sweep in `scripts/sync_docs.py`, the same
  as any Markdown surface. A label that says "five blind" has to still be true.
