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

## The rest of the manual

Everything past installing lives in [docs/](docs/index.md):

- [Getting started](docs/getting-started.md): what to gather before onboarding,
  and what the pipeline needs installed — `pdftotext`, and optionally a LaTeX
  toolchain and the vendored document fonts.
- [Skills](docs/skills.md): every `/slushpile:*` command and when to run it.
- [The workspace](docs/workspace.md): the files onboarding writes into your
  directory, and what reads each one.
- [Your voice agent](docs/voice.md): why cover letters need one and how to
  generate yours.
- [Troubleshooting](docs/troubleshooting.md).
- [Architecture](docs/architecture/index.md): why the pipeline is shaped the way
  it is.
