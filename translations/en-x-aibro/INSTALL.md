# Deploy

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../INSTALL.md">English</a> ·
  <a href="../zh-CN/INSTALL.md">简体中文</a> ·
  <a href="../es/INSTALL.md">Español</a> ·
  <a href="../pt-BR/INSTALL.md">Português (BR)</a> ·
  <a href="../vi/INSTALL.md">Tiếng Việt</a> ·
  <strong>AI Bro</strong>
</p>

<!-- END GENERATED language-nav -->

10 skills and 8 agent definitions. All Markdown.

No runtime. No service. No container. No account. Nothing to spin up and nothing
to pay for. Every route below puts the same files somewhere your agent will read
them, and that is the entire install story.

Portability is not a feature we added. It is what the file format already was.

**Make one architectural decision before you install anything: where your
workspace lives.**

The plugin is code. Your workspace is your employment history, your comp, and
your constraints. Different assets. Different blast radius. They do not go in the
same directory. Install the plugin wherever your agent keeps plugins. Run
`/slushpile:onboard` somewhere private.

---

## Claude Code

Full topology, no degradation. Skills become slash commands, the 8 agents
dispatch as real subagents, and the 5 blind reviewers actually run concurrent.

```bash
claude plugin marketplace add VonTerraProject501c3/slushpile
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

Neither command touches your workspace. The state layer is yours and it outlives
the plugin.

---

## Codex

```bash
codex plugin marketplace add VonTerraProject501c3/slushpile --ref main
```

```bash
codex plugin add slushpile@slushpile
```

Inside Codex, `/plugins` opens the plugin browser.

Codex prefixes plugin skills with the plugin name:

```
$slushpile:onboard
```

**Read this before you run it here.** No subagent dispatch on this harness. The
review adopts each of the 7 reviewers out of the plugin's `agents/` directory in
turn, in one context, writing each report before the next.

Output shape is identical. Two properties degrade.

1. Wall clock. Seven sequential passes instead of 5 in parallel plus two.
2. Context isolation. Gone. The 5 blind stages are supposed to be blind. In one
   context they are not, and a reviewer that already read the triage verdict
   drifts toward agreeing with it.

The second one is the expensive one and it is invisible in the output. Five
reports that agree because they could not see each other is evidence. Five
reports that agree because they shared a context window is one opinion with a
bigger word count. Same artifact, less information.

The skill instructs the model to write each report out fully before starting the
next. That limits the drift. It does not eliminate it.

---

## Gemini CLI

```bash
gemini extensions install https://github.com/VonTerraProject501c3/slushpile
```

The extension names `GEMINI.md` as its context file, which imports every skill
and agent definition.

Then, in your workspace directory:

```
Set up a slushpile workspace here.
```

No subagent dispatch here either. Same caveat, same reason.

### Manual

Clone into the extensions directory:

```bash
git clone https://github.com/VonTerraProject501c3/slushpile ~/.gemini/extensions/slushpile
```

---

## Cursor

Cursor reads `.cursor/skills/` and `.cursor/rules/` out of the workspace it has
open. Three things go in: the skill router, the rules file, and the pipeline
itself. Point `WORKSPACE` at the directory Cursor has open and run the block as
one unit:

```bash
WORKSPACE="/path/to/your/workspace"
rm -rf /tmp/slushpile
git clone https://github.com/VonTerraProject501c3/slushpile /tmp/slushpile
mkdir -p "$WORKSPACE/.cursor/skills" "$WORKSPACE/.cursor/rules" "$WORKSPACE/.slushpile"
cp -r /tmp/slushpile/.cursor/skills/slushpile "$WORKSPACE/.cursor/skills/"
cp /tmp/slushpile/.cursor/rules/slushpile.mdc "$WORKSPACE/.cursor/rules/"
cp -r /tmp/slushpile/skills /tmp/slushpile/agents /tmp/slushpile/templates "$WORKSPACE/.slushpile/"
```

Confirm all three landed:

```bash
ls "$WORKSPACE/.cursor/skills/slushpile/SKILL.md" "$WORKSPACE/.cursor/rules/slushpile.mdc" "$WORKSPACE/.slushpile/skills"
```

The rules file is the one to verify. It carries the two standing rules — read
`preferences.yaml` before claiming anything about the user, and never submit
anything — and Cursor is the only harness where it arrives by hand-copy rather
than with the plugin. A workspace missing it looks exactly like a working one.

`rm -rf /tmp/slushpile` is there so you can re-run the block; `git clone`
refuses a destination that already exists.

The Cursor skill is a router. It points at the real skill files under
`.slushpile/`. One copy of the pipeline, four harnesses. Not four forks that
drift until nobody knows which one is current.

Then type `/slushpile` in Cursor and name what you want to do.

---

## Any other harness

Plain Markdown with YAML frontmatter. If your agent can read files, it can run
this. That is the whole integration surface.

Clone the repository somewhere your agent can reach:

```bash
git clone https://github.com/VonTerraProject501c3/slushpile ~/.slushpile
```

Then drop this into your `AGENTS.md`, your system prompt, or whatever your
harness uses for standing instructions:

<!-- BEGIN GENERATED harness-snippet: scripts/sync_docs.py -->

```markdown
## slushpile

A job application pipeline lives at `~/.slushpile`. When the user asks to set up
a job search, search a careers board, build an application, or review one, read
the matching skill and follow it:

- `~/.slushpile/skills/onboard/SKILL.md` — set up the workspace, once
- `~/.slushpile/skills/job-board-search/SKILL.md` — search and score roles
- `~/.slushpile/skills/outreach/SKILL.md` — find a referrer and draft the ask
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

That snippet is the entire adapter layer. No SDK, no client library, no version
pinning. Markdown in, pipeline out.

---

## The rest of the docs

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
