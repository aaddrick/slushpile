# Slushpile architecture

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <strong>English</strong> ·
  <a href="../../translations/zh-CN/docs/architecture/index.md">简体中文</a> ·
  <a href="../../translations/es/docs/architecture/index.md">Español</a> ·
  <a href="../../translations/pt-BR/docs/architecture/index.md">Português (BR)</a> ·
  <a href="../../translations/vi/docs/architecture/index.md">Tiếng Việt</a> ·
  <a href="../../translations/en-x-aibro/docs/architecture/index.md">AI Bro</a>
</p>

<!-- END GENERATED language-nav -->

Slushpile is not a program. It is a set of Markdown files that a coding agent
reads and acts on: ten skills that orchestrate, eight agent definitions that
each do one job, and a handful of templates. There is no engine, no runtime, and
no state outside the user's own workspace directory.

That shapes every decision documented here. A rule this pipeline wants enforced
has to survive being paraphrased by a model under load, because there is no
interpreter to enforce it. A fact the pipeline needs has to live in a file the
model will actually read, because there is no database to query.

| File | Contents |
| --- | --- |
| [pipeline.md](pipeline.md) | The five diagrams, the legend, and what each stage does. |
| [the-review.md](the-review.md) | Why the review is shaped the way it is: the blind stage, the dispatch order, the gatekeeper, and the three-round cap. |
| [scoring.md](scoring.md) | Pool anchoring, channel-conditional verdicts, tiers, and kill criteria. |
| [memory-and-calibration.md](memory-and-calibration.md) | The workspace as durable memory, the write-back paths, and how predictions get corrected by outcomes. |
| [agents-and-models.md](agents-and-models.md) | The skill/agent boundary, the model tier per persona, and voice agents. |
| [personal-data.md](personal-data.md) | Why no personal fact may live in the plugin, and the gate that enforces it. |
| [generated-surfaces.md](generated-surfaces.md) | Why six surfaces describe this pipeline and none of them owns a fact. |
| [AGENTS.md](AGENTS.md) | Byte-identical twin of this directory's `CLAUDE.md`, constraining edits to these conventions. |
