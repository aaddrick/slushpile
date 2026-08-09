# Install

slushpile is nine skills and eight agent definitions, all Markdown. Every route
below puts the same files somewhere your agent will read them.

**One thing to decide before you install anything:** where your workspace goes.

The plugin is code. Your workspace is your employment history, your salary, and
your constraints. They are different things and they belong in different
directories. Install the plugin wherever your agent keeps plugins; run
`/slushpile:onboard` in a separate directory that you keep private.

---

## Claude Code

The full pipeline. Skills become slash commands, the eight agents are dispatched
as subagents, and the five parallel review stages actually run in parallel.

```bash
claude plugin marketplace add aaddrick/slushpile
```

```bash
claude plugin install slushpile@slushpile
```

Verify:

```bash
claude plugin list
```

You should see `slushpile@slushpile` and `enabled`.

Then start:

```
/slushpile:onboard
```

Run it in the directory where you want your job search to live.

### Updating

```bash
claude plugin marketplace update slushpile
```

```bash
claude plugin install slushpile@slushpile
```

### Uninstalling

```bash
claude plugin uninstall slushpile
```

```bash
claude plugin marketplace remove slushpile
```

Neither command touches your workspace files.

---

## Codex

```bash
codex plugin marketplace add aaddrick/slushpile --ref main
```

```bash
codex plugin add slushpile@slushpile
```

Inside Codex, `/plugins` opens the plugin browser.

Codex prefixes plugin skills with the plugin name:

```
$slushpile:onboard
```

**What differs.** Codex has no subagent dispatch. The review pipeline runs its
seven personas sequentially in one context: read each agent definition from the
plugin's `agents/` directory, adopt it, write the report, then move to the next.

The output is the same shape. Two things degrade, and it is worth knowing which:

1. It is slower. Seven sequential passes instead of five parallel ones plus two.
2. The five specialist stages are supposed to be blind to each other. In one
   context they are not, and a specialist that has already seen the triage
   verdict will drift toward agreeing with it. Write each report out fully
   before starting the next, which is what the skill instructs.

---

## Gemini CLI

```bash
gemini extensions install https://github.com/aaddrick/slushpile
```

The extension names `GEMINI.md` as its context file, which imports every skill
and agent definition.

Then, in your workspace directory:

```
Set up a slushpile workspace here.
```

Gemini has no subagent dispatch either, so the same sequential caveat applies.

### Manual

Clone into the extensions directory:

```bash
git clone https://github.com/aaddrick/slushpile ~/.gemini/extensions/slushpile
```

---

## Cursor

Cursor reads `.cursor/skills/` and `.cursor/rules/` from the workspace it has
open. Clone the repository and copy them into your workspace:

```bash
git clone https://github.com/aaddrick/slushpile /tmp/slushpile
```

```bash
cp -r /tmp/slushpile/.cursor/skills/slushpile <your-workspace>/.cursor/skills/
```

```bash
cp -r /tmp/slushpile/skills /tmp/slushpile/agents /tmp/slushpile/templates <your-workspace>/.slushpile/
```

The Cursor skill is a router: it points at the real skill files under
`.slushpile/`. That keeps one copy of the pipeline rather than four.

Then type `/slushpile` in Cursor and name what you want to do.

---

## Any other harness

The pipeline is plain Markdown with YAML frontmatter. Any agent that can read
files can run it.

Clone the repository somewhere your agent can reach:

```bash
git clone https://github.com/aaddrick/slushpile ~/.slushpile
```

Then put this in your `AGENTS.md`, your system prompt, or whatever your harness
uses for standing instructions:

<!-- BEGIN GENERATED harness-snippet: scripts/sync_docs.py -->

```markdown
## slushpile

A job application pipeline lives at `~/.slushpile`. When the user asks to set up
a job search, search a careers board, build an application, or review one, read
the matching skill and follow it:

- `~/.slushpile/skills/onboard/SKILL.md` — set up the workspace, once
- `~/.slushpile/skills/job-board-search/SKILL.md` — search and score roles
- `~/.slushpile/skills/explore-experience/SKILL.md` — interview for undocumented experience
- `~/.slushpile/skills/application-builder/SKILL.md` — build the resume and cover letter
- `~/.slushpile/skills/adversarial-review/SKILL.md` — run the seven-agent review
- `~/.slushpile/skills/removing-ai-tells/SKILL.md` — strip AI-authorship signals from prose
- `~/.slushpile/skills/redesign-templates/SKILL.md` — restyle the document templates
- `~/.slushpile/skills/status/SKILL.md` — report the queue and check pipeline calibration
- `~/.slushpile/skills/help/SKILL.md` — what to run next, and how to read the output

The review dispatches personas defined in `~/.slushpile/agents/`. If you cannot
dispatch subagents, adopt each definition in turn and run them sequentially,
writing each report out before starting the next.

Cover letters are written by the voice agent named in `preferences.yaml` under
`voice.agent`. A working example ships as `aaddrick-voice`; it is the plugin
author's voice, and users generate their own with
https://github.com/aaddrick/written-voice-replication

Workspace templates are in `~/.slushpile/templates/`.
```

<!-- END GENERATED harness-snippet -->

---

## What onboarding will ask you for

Worth gathering before you start, because two of these take you longer to find
than the interview takes to run.

**A resume**, in any format. PDF, `.tex`, `.docx`, Markdown. Replaces about ten
minutes of interview with thirty seconds of reading. A LinkedIn data export
works too — `Positions.csv` and `Education.csv` carry most of it.

**A writing corpus**, for your voice agent. Several thousand words of your own
unedited prose. Onboarding does not analyze this itself — it points you at
[written-voice-replication](https://github.com/aaddrick/written-voice-replication),
which is a separate pipeline you run once. Gathering the corpus is the slow
part, so start early.

Good sources: forum and Reddit posts, blog posts, long Slack messages, emails
to colleagues, pull request descriptions, documentation you wrote alone. A
Reddit or Twitter data export works directly.

Bad sources: anything co-written, anything edited by someone else, anything
already run through an LLM, anything in an institutional voice. Marketing copy
and performance reviews are the two worst.

**Your numbers.** Budgets, headcounts, percentages, and the *before* state for
each. "Cut latency 40%" is unusable until you know 40% of what, and onboarding
will ask.

**Your compensation situation**, if you want the compensation gate to work. For
the recommended method it needs your current gross, your tax, and your housing
cost. It does the arithmetic; you do not have to arrive with a number.

---

## Requirements

**Required:** an agent that can read local files and browse the web.

**Recommended:** `pdftotext` (from `poppler-utils`), so the review agents see
what an ATS sees rather than what your PDF viewer shows.

```bash
sudo dnf install poppler-utils     # Fedora
sudo apt install poppler-utils     # Debian, Ubuntu
brew install poppler               # macOS
```

**Optional:** a LaTeX toolchain, if you use `templates/resume.tex` and
`templates/cover_letter.tex`. Every skill works on extracted text and none of
them require LaTeX — only those two templates do.

```bash
sudo dnf install -y texlive-xetex texlive-fontspec texlive-microtype latexmk dejavu-fonts-all
sudo apt install texlive-xetex texlive-fonts-extra fonts-dejavu latexmk
brew install --cask mactex-no-gui
```

Build with `latexmk -xelatex resume.tex && latexmk -c`. Two commands: the first
builds, the second cleans. Neither does both.

The templates are set in Public Sans and IBM Plex Mono. Neither ships with TeX
Live, so both are vendored in this repository and one command installs them:

```bash
python3 scripts/install_fonts.py            # install
python3 scripts/install_fonts.py --check    # report, change nothing
python3 scripts/install_fonts.py --uninstall
```

It copies seven font files into your user font directory and refreshes the
cache. Nothing else runs it, and skipping it is fine: both templates fall back
to DejaVu when a family is absent, so a missing font changes how the documents
look and never whether they build.

To restyle them into something of your own, run
`/slushpile:redesign-templates` rather than editing the plugin checkout, which
the next update replaces.

---

## Troubleshooting

**`plugin install` succeeds but the skills do not appear.** Run `claude plugin
list` and check for `enabled`. Skills load at session start, so start a new
session or run `/clear`.

**A skill says it cannot find `preferences.yaml`.** You are in a different
directory than the one you onboarded. Every skill reads the workspace from the
current working directory.

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
too thin — a few thousand words is the floor.

**Every role comes back killed on compensation.** Open `preferences.yaml` and
check `compensation`. With `net_qol`, the most common cause is a
`current_baseline` entered as gross rather than after-tax-after-housing, which
makes every offer look worse than it is.
