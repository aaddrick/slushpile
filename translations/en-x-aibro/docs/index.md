# Slushpile docs

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../docs/index.md">English</a> ·
  <a href="../../zh-CN/docs/index.md">简体中文</a> ·
  <a href="../../es/docs/index.md">Español</a> ·
  <a href="../../pt-BR/docs/index.md">Português (BR)</a> ·
  <a href="../../vi/docs/index.md">Tiếng Việt</a> ·
  <strong>AI Bro</strong>
</p>

<!-- END GENERATED language-nav -->

The [README](../README.md) is the thesis. This is the implementation.

Indexed by what you are trying to ship.

## Start here

- [Getting started](getting-started.md): what to gather before onboarding, and
  what the pipeline needs installed.
- [Skills](skills.md): every `/slushpile:*` command, what it does, and when to
  run it.
- [The workspace](workspace.md): the files onboarding writes into your directory,
  what each one is for, and who reads it. This is the memory layer. Read it
  second and read it properly.

## Reference

- [Your voice agent](voice.md): why cover letters need one, how to generate
  yours, and what happens until you do.
- [Troubleshooting](troubleshooting.md).

## Architecture

- [Architecture](architecture/index.md): the diagrams, the review topology, the
  scoring model, the calibration loop, and the personal-data boundary. This is
  where the decisions are, and every one of them has a failure mode attached.
- [Diagram guide](../../../docs/diagrams/AGENTS.md): how to edit and re-render
  the `.d2` diagrams the architecture pages embed.

## Contributing

Repository standards, the four gates, and the rules for editing a skill are in
[CLAUDE.md](../../../CLAUDE.md) and
[CONTRIBUTING.md](../../../CONTRIBUTING.md).

Read [Generated surfaces](../../../docs/architecture/generated-surfaces.md)
before you edit anything that lists the skills. Several of those lists are
generated. Editing the artifact instead of the source is the one change that
reliably disappears, and it disappears silently, which is worse.
