# Slushpile architecture

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../../docs/architecture/index.md">English</a> ·
  <a href="../../../zh-CN/docs/architecture/index.md">简体中文</a> ·
  <a href="../../../es/docs/architecture/index.md">Español</a> ·
  <a href="../../../pt-BR/docs/architecture/index.md">Português (BR)</a> ·
  <a href="../../../vi/docs/architecture/index.md">Tiếng Việt</a> ·
  <strong>AI Bro</strong>
</p>

<!-- END GENERATED language-nav -->

Slushpile is not a program.

10 skills that orchestrate. 8 agent definitions that each do exactly one job. A
handful of templates. All Markdown, read and acted on by a coding agent.

No engine. No runtime. No server. No state outside the user's own directory. The
harness is the runtime, the prompt is the program, and the filesystem is the
state.

That is not minimalism as a lifestyle choice. It is a constraint with teeth, and
it shapes every decision on these pages:

A rule this pipeline wants enforced has to survive being paraphrased by a model
under load, because there is no interpreter to enforce it. Which is why every
rule in this repository ships with its failure mode attached. A bare imperative
gets dropped the first time context gets tight. A rule that says what breaks does
not.

A fact this pipeline needs has to live in a file the model will actually read,
because there is no database to query.

Build on those two and you get something portable across every major harness.
Ignore them and you get a wrapper that works on one vendor until they ship a
breaking change.

| File | Contents |
| --- | --- |
| [pipeline.md](pipeline.md) | The five diagrams, the legend, and what each stage does. |
| [the-review.md](the-review.md) | Why the review is shaped the way it is: the blind stage, the dispatch order, the gatekeeper, and the three-round cap. |
| [scoring.md](scoring.md) | Pool anchoring, channel-conditional verdicts, tiers, and kill criteria. |
| [memory-and-calibration.md](memory-and-calibration.md) | The workspace as durable memory, the write-back paths, and how predictions get corrected by outcomes. |
| [agents-and-models.md](agents-and-models.md) | The skill/agent boundary, the model tier per persona, and voice agents. |
| [personal-data.md](personal-data.md) | Why no personal fact may live in the plugin, and the gate that enforces it. |
| [generated-surfaces.md](../../../../docs/architecture/generated-surfaces.md) | Why six surfaces describe this pipeline and none of them owns a fact. |
| [AGENTS.md](../../../../docs/architecture/AGENTS.md) | Byte-identical twin of this directory's `CLAUDE.md`, constraining edits to these conventions. |
