# Your voice agent

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../docs/voice.md">English</a> ·
  <a href="../../zh-CN/docs/voice.md">简体中文</a> ·
  <a href="../../es/docs/voice.md">Español</a> ·
  <a href="../../pt-BR/docs/voice.md">Português (BR)</a> ·
  <a href="../../vi/docs/voice.md">Tiếng Việt</a> ·
  <strong>AI Bro</strong>
</p>

<!-- END GENERATED language-nav -->

An eighth agent writes the cover letter, in one specific person's style, built
from a corpus of that person's own writing.

It is the only input in this system you cannot buy, borrow, or prompt your way
into.

Bring it yourself.

## Why a separate agent

Everybody has a frontier model now.

Which means everybody ships competent prose now. Which means competent prose is
table stakes, and table stakes are worth nothing. The entire applicant
distribution collapsed onto one register in about eighteen months, and the person
reading application sixty-one can spot that register in four seconds without
being able to name what they spotted.

A model writing "in your voice" off a resume does not solve this. It emits the
model's default with your facts injected. Same register, different nouns.

So the voice is not a prompt instruction.

It is an agent definition generated from several thousand words of your actual
prose, measured across a set of stylistic dimensions, with numeric targets a
later pass can evaluate against. "Write like me" is a wish. This is a spec with
an eval attached.

## Generating yours

[written-voice-replication](https://github.com/aaddrick/written-voice-replication)
is a separate pipeline. Run it once. It analyzes a corpus across 25 dimensions
and emits a voice agent, a voice skill, and a numeric profile with measurable
targets.

The corpus is the long pole. Start before you need it.

**High-signal:** forum and Reddit posts, blog posts, long Slack messages, emails
to colleagues, pull request descriptions, docs you wrote alone. A Reddit or
Twitter export drops straight in.

**Contaminated:** anything co-written, anything edited by someone else, anything
already through an LLM, anything institutional. Marketing copy and performance
reviews are the two worst inputs available. Both are written in a register nobody
uses voluntarily, and training on them produces a voice agent that sounds like
compliance.

A few thousand words is the floor. Below that the output reads generic, which is
the failure mode hardest to catch, because generic looks finished.

## Pointing slushpile at it

```yaml
voice:
  agent: "your-name-voice"
  is_mine: true
```

`voice.agent` is read at run time and hardcoded nowhere. Swap yours in without
forking anything. Configuration, not code.

## Until then

`aaddrick-voice` ships as a working example so the pipeline runs on install.

It is the plugin author's voice. Not yours. Letters written with it sound like a
specific stranger, which is fine for validating the loop and wrong for anything
you send to a human being.

While `is_mine` is false, every skill that drafts prose warns you before it runs.

That warning is the only thing between you and twelve applications shipped in a
stranger's voice. Do not flip the flag to make the warning stop. Flip it when the
agent is actually yours.

## How the voice is used, and defended

`/slushpile:removing-ai-tells` runs the letter through fresh voice-agent
instances, orchestrator gatekeeping every individual change.

The gatekeeping is the whole design. A pass that accepted every suggestion would
regress the letter straight back to the mean, which is exactly what the voice
agent exists to prevent. An unbounded cleanup loop is a mean-reversion machine.

The review's fatigued reader is checked against your voice agent for the same
reason. A distinctive habit documented there is not a defect because a persona
flagged it. Strip those and the letter drifts back to generic, one defensible
edit at a time.

One more thing worth knowing. A voice agent is one person's identity by
construction: generated from their writing, named after them, examples are their
real sentences. That is why it is the single agent in this repository exempt from
the personal-data rules that bind everything else, and why the exemption stops
hard at contact details. See [Agents and models](architecture/agents-and-models.md).
