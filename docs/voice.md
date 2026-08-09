# Your voice agent

An eighth agent writes the cover letter, and it writes in one specific person's
style, built from a corpus of that person's own writing.

That is the only part of this pipeline you have to bring yourself.

## Why a separate agent

A cover letter is the one document in an application that is supposed to sound
like a person. A model writing "in your voice" from a resume produces the
model's default register with your facts in it — competent, uniform, and
recognizable as such by the sixty-first reader of the day.

So the voice is not a prompt instruction. It is an agent definition generated
from several thousand words of your actual prose, measured across a set of
stylistic dimensions, with numeric targets a later pass can check against.

## Generating yours

[written-voice-replication](https://github.com/aaddrick/written-voice-replication)
is a separate pipeline you run once. It analyzes a corpus of your writing across
25 dimensions and outputs a voice agent, a voice skill, and a numeric profile
with measurable targets.

Gathering the corpus is the slow part, so start before you need it.

**Good sources:** forum and Reddit posts, blog posts, long Slack messages,
emails to colleagues, pull request descriptions, documentation you wrote alone.
A Reddit or Twitter data export works directly.

**Bad sources:** anything co-written, anything edited by someone else, anything
already run through an LLM, anything in an institutional voice. Marketing copy
and performance reviews are the two worst — both are written in a register
nobody uses voluntarily.

A few thousand words is the floor. Below that the output reads generic, which is
the failure mode that is hardest to notice because it looks finished.

## Pointing slushpile at it

```yaml
voice:
  agent: "your-name-voice"
  is_mine: true
```

`voice.agent` names the agent by name and nothing hardcodes it, which is what
lets you swap in your own without editing the plugin.

## Until then

`aaddrick-voice` ships as a working example so the pipeline runs out of the box.
It is the plugin author's voice, not yours. Letters written with it will sound
like a specific stranger — fine for seeing the pipeline work, wrong for anything
you actually send.

While `is_mine` is false, every skill that drafts prose warns you before it
runs. That warning is the only thing standing between you and twelve
applications sent in a stranger's voice, so do not silence it by setting the
flag true before the agent is actually yours.

## How the voice is used, and defended

`/slushpile:removing-ai-tells` runs the letter through fresh voice-agent
instances, with the orchestrating skill acting as gatekeeper on every individual
change. A pass that accepted every suggestion would sand the letter back toward
the average, which is the thing the voice agent exists to prevent.

The review's fatigued reader is checked against your voice agent for the same
reason. A distinctive habit documented there is not a defect because a persona
flagged it, and removing it is exactly how a letter drifts back to generic.

Note that a voice agent is one person's identity by construction — generated
from their writing, named after them, and its examples are their real sentences.
That is why it is the one agent in this repository exempt from the personal-data
rules that bind everything else, and why the exemption stops at contact details.
See [Agents and models](architecture/agents-and-models.md).
