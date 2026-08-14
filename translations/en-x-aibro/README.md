<p align="center">
  <img src="../../.github/assets/hero-en-x-aibro.png" alt="Slushpile: the context-engineering substrate for candidate-market fit. 7 agents try to reject you before a recruiter gets the chance, and what they find, you keep. The memory layer: profile.md, single source of truth; preferences.yaml, your constraint vector; stories.md, four to eight, high-signal; job_search.md, the outcome ledger. Written once, read by every stage, updated by every review. The 7 reviewers: top-of-funnel filter, requirements parser, ATS parse simulation, attention-decay reader, comparative pool ranker, hiring-manager persona, kill-authority contrarian. 5 in parallel and blind to each other, then synthesis, then an agent whose only job is overturning the result." width="100%">
</p>

<p align="center">
  <strong>Slushpile</strong><br>
  <em>7 agents try to reject you before a recruiter gets the chance.</em><br>
  <em>What they find, you keep.</em>
</p>

<p align="center">
  <a href="../../LICENSE"><img src="https://img.shields.io/github/license/VonTerraProject501c3/slushpile?style=flat" alt="License"></a>
  <a href="../../.github/workflows/plugin-load-check.yml"><img src="https://img.shields.io/github/actions/workflow/status/VonTerraProject501c3/slushpile/plugin-load-check.yml?label=plugin%20loads&style=flat" alt="Plugin load check"></a>
</p>

<p align="center">
  <a href="https://www.linkedin.com/in/aaddrick/">Let's connect on LinkedIn.</a>
</p>

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../README.md">English</a> ·
  <a href="../zh-CN/README.md">简体中文</a> ·
  <a href="../es/README.md">Español</a> ·
  <a href="../pt-BR/README.md">Português (BR)</a> ·
  <a href="../vi/README.md">Tiếng Việt</a> ·
  <strong>AI Bro</strong>
</p>

<!-- END GENERATED language-nav -->

<!-- BEGIN GENERATED market-note: scripts/sync_docs.py -->

> **Market fit**: this pipeline is built against anglophone hiring conventions, primarily US: one page, no photo, no date of birth, reverse chronological, one work-authorization line. If your target market runs a standardized CV form, the formatting layer is misaligned for your use case and the review will score local convention as a defect. Expansion is a roadmap conversation, not a translation conversation, and it is tracked in [issue #2](https://github.com/VonTerraProject501c3/slushpile/issues/2).

<!-- END GENERATED market-note -->

We didn't build a resume tool.

We built the context-engineering substrate for candidate-market fit.

Multi-agent adversarial evaluation. Blind ensemble dispatch. Heterogeneous model
routing. Filesystem-as-memory. A contrarian agent with kill authority over the
entire upstream pipeline. Portable across every major agent harness.

This is what agent-native software looks like.

Everything else is a wrapper.

## Deploy

<details open>
<summary><strong>Claude Code</strong></summary>

```bash
claude plugin marketplace add VonTerraProject501c3/slushpile
```

```bash
claude plugin install slushpile@slushpile
```

Then, in the directory where you keep your job search:

```
/slushpile:onboard
```

</details>

<details>
<summary><strong>Codex</strong></summary>

```bash
codex plugin marketplace add VonTerraProject501c3/slushpile --ref main
```

```bash
codex plugin add slushpile@slushpile
```

Codex prefixes plugin skills with the plugin name:

```
$slushpile:onboard
```

No subagent dispatch on this harness. The topology degrades: 7 reviewers
sequential in one context instead of 5 in parallel. Same artifact. Longer wall
clock. And you lose isolation, which is the expensive one, because a reviewer
that already read the triage verdict will agree with it.

Ship on Claude Code if you have the choice.

</details>

<details>
<summary><strong>Cursor, Gemini CLI, and manual install</strong></summary>

See [INSTALL.md](./INSTALL.md).

</details>

## Everyone in this category is solving the wrong problem

You are not being graded against the job description.

You are being graded against the other seventy people who applied to the same
requisition this week.

Read that again, because every product in this space is built on the opposite
assumption. Feed a resume and a posting into an optimizer, get keyword match:
68% to 91%. Real number. Wrong variable. If the 75th-percentile applicant in that
queue matches at 94%, your 91% is a rejection, and the tool has no
representation of that fact anywhere in its state. It cannot tell you. It was
never modeling the thing that decides.

Failure mode two: single-verdict output.

Same resume, same letter. 2% through a cold portal. 30% through a referral.
Those are different distributions. Collapsing them into one "strong match" is
not abstraction. It is information destruction with a confident UI bolted on
top.

Failure mode three is the one nobody in this space will say out loud.

These tools are stateless.

You paste. You get a score. You close the tab. The process terminates knowing
exactly what it knew at init. A search is forty applications over three months.
Forty cold starts. Forty times paying full price for context that should have
been compounding since application one.

That is not a product. That is a metered API with a landing page.

## The substrate

**One model of you. Persisted.** `/slushpile:onboard` runs the interview and
writes three artifacts: a profile, a preferences file, a story set. The profile
is not a resume. It is the corpus a resume gets sampled from, several times
longer than anything you would ship. Every downstream stage reads it. Nothing
re-asks. Ever.

**Kill the application before you spend a cycle on it.** Pool-anchored scoring.
Kill criteria. An expected-value matrix per channel. A contrarian in front of the
tier list. Every other tool activates *after* you decided to apply. The expensive
decision is upstream of that. This is the only stage positioned to catch it while
it is still free.

**Adversarial evals on your own output.** A model asked to grade its own draft
returns yes, at length, with structure. So the builder never asks. It dispatches
to 7 reviewers, 5 in parallel, blind, each context-isolated to exactly what its
role would really hold. The 11-second screener never sees the cover letter,
because a screener who read the letter is not a screener, it is a fan. Patch,
re-run, converge. Cap at three rounds, because past that the gaps are structural
and more editing is motion, not progress.

**Every eval writes back into the substrate.** Review flags a section thin. The
interview that follows finds the experience was real and never captured. That
commits to the profile permanently. Conversion estimates get corrected against
your recorded outcomes. Application twenty initializes from a strictly better
state than application one.

That is the compounding asset. Nobody else in this category has one, because
nobody else in this category has memory.

Output is a verdict per channel. Cold, referral, outreach, inbound. Probability
range instead of a verdict word. Materials quality scored independently of
expected value.

"1-3% interview" is signal.

"MAYBE" is a vibe.

## Before and after

Same resume, same posting, same afternoon.

### What a resume optimizer returns

> **Match score: 91%** ✅
>
> Great news — your resume is a strong match for this role!
>
> ✅ 14 of 16 required keywords found
> ✅ ATS-friendly formatting detected
> ⚠️ Consider adding: "stakeholder alignment", "OKRs"
>
> You're ready to apply!

### What Slushpile returns

> **Pool position: p55.** Median applicant here has shipped at comparable scale
> at a company the hiring manager recognizes. Your open-source work is real and
> it is not rare in this pool — roughly a third of the p75 cohort has something
> equivalent.
>
> **Cold submission: REJECT, 1-3%.** The years-of-experience dropdown on the
> form gates at 8. You have 6 in the titled function.
>
> **Warm referral: MAYBE, 20-30%.** This is the only channel with a real path.
>
> **Materials quality: 8/10.** The materials are not the problem.
>
> **Contrarian:** SUBMIT_AS_PORTFOLIO_ONLY. Sending this cold spends an hour for
> a 2% shot. Two hours finding a referral is worth more than ten more cold
> applications.

One of those is a metric about a document.

The other is a decision about your afternoon.

Only one of them is worth the compute.

## The orchestration layer

<!-- BEGIN GENERATED pipeline: scripts/sync_docs.py -->

### The main pipeline

Three commands, in order. A search runs on these alone.

```
/slushpile:onboard              once per workspace — builds your profile,
                                preferences, and stories

/slushpile:job-board-search     search a careers board, extract postings,
                                score pool-anchored fit, contrarian gate,
                                create role folders

/slushpile:application-builder  build the resume and cover letter, then
                                iterate them against the review until they
                                stabilize
```

### The three it runs for you

`/slushpile:application-builder` dispatches all three of these itself, in the
course of building an application. Run one directly only to work on materials
this pipeline did not build — a resume written elsewhere, a letter drafted by
hand.

```
/slushpile:explore-experience   interview to surface experience you have
                                but never wrote down

/slushpile:adversarial-review   seven agents, five in parallel, verdict
                                per channel

/slushpile:removing-ai-tells    strip AI-authorship signals from prose,
                                with a gatekeeper on every change
```

### Any time

```
/slushpile:redesign-templates   restyle the resume and letter templates,
                                holding the ATS constraints fixed

/slushpile:status               the queue, what is waiting on you, and whether
                                the pipeline's predictions are holding up

/slushpile:help                 what to run next, and how to read the output
```

<!-- END GENERATED pipeline -->

<!-- BEGIN GENERATED reviewers: scripts/sync_docs.py -->

### The seven reviewers

| Agent | Simulates |
|---|---|
| **Triage screener** | 11 seconds, F-pattern, 347 resumes already read today |
| **Requirements analyst** | 30 seconds, methodical, checks every qualification against evidence |
| **ATS simulator** | A parser. Not a reader. Structure, keywords, and years-of-experience math |
| **Fatigued reader** | Application #61 of 80. What annoys, what gets skimmed, what closes the tab |
| **Pool analyst** | A recruiter who knows what the queue actually looks like |
| **Hiring manager** | The person who has to justify the interview slot to their skip-level |
| **Contrarian** | Whoever should have asked whether any of this was worth doing |

The first five run in parallel and cannot see each other's work. The hiring
manager sees all five. The contrarian sees everything, including the hiring
manager, and can overrule it.

<!-- END GENERATED reviewers -->

That table is the architecture. Not a feature list.

Stage one dispatches 5 in parallel with zero shared context. No cross-talk. No
anchoring. Their agreement is evidence instead of an echo, and that property is
worth more than any individual reviewer in the set.

Stage two synthesizes.

Stage three is an agent with kill authority over everything upstream of it,
including the synthesis, including the decision to apply at all. It runs every
time. It is never conditional, because a falsification step that fires only when
the orchestrator feels uncertain will skip itself in exactly the cases where the
confidence was wrong.

An eval that cannot return "none of this was worth running" is not an eval.

## The docs

Full documentation in [docs/](docs/index.md):

- [Getting started](docs/getting-started.md): what to gather before onboarding,
  and what to install.
- [Skills](docs/skills.md): every command, and when to run it.
- [The workspace](docs/workspace.md): the files this writes into your directory.
- [Your voice agent](docs/voice.md), [Troubleshooting](docs/troubleshooting.md).
- [Architecture](docs/architecture/index.md): the diagrams, the review topology,
  and how scoring and calibration work.

## Voice is the moat

An eighth agent writes the cover letter. It writes in one specific person's
style, built from a corpus of their own writing.

Here is the part people miss. Every candidate now has a frontier model. Every
candidate now ships competent prose. Competent prose is table stakes and table
stakes are worthless. The distribution collapsed onto one register and the
sixty-first reader of the day can spot it in four seconds.

Your voice is the only input in this system nobody else can obtain.

slushpile ships **`aaddrick-voice`** as a working example so the pipeline runs on
install. It is the plugin author's voice, not yours. Letters written with it will
sound like a specific stranger. Fine for validating the loop. Wrong for anything
you send.

Generate your own with
**[written-voice-replication](https://github.com/aaddrick/written-voice-replication)**.
It analyzes a corpus of your writing across 25 dimensions and emits a voice
agent, a voice skill, and a numeric profile with measurable targets.
`aaddrick-voice` is that pipeline's own worked example.

Then point `preferences.yaml` at it:

```yaml
voice:
  agent: "your-name-voice"
  is_mine: true
```

While `is_mine` is false, every skill that drafts prose warns you before it runs.

That warning is the only thing between you and twelve applications shipped in a
stranger's voice. Do not turn it off to make the output quieter.

## Your data never leaves your machine

`/slushpile:onboard` writes three files into *your* directory: `profile.md`,
`preferences.yaml`, and `stories.md`. Every personal fact the pipeline consumes
lives there.

Nothing is hardcoded into the plugin. There is a CI gate that fails the build if
a personal fact leaks into a skill. Not a policy. A test.

That workspace holds your full employment history, your comp figures, and your
constraints. Private repository, or no repository. The onboarding skill will tell
you that and it will not initialize one for you, because a git remote you
inherited from a setup step is a decision nobody made.

**The pipeline never submits anything.** No skill touches a portal, an email, or
a form. It writes files. You read them. You send them.

No telemetry. No account. No server. There is nothing to opt out of.

## Negative signal is the product

This tool will tell you a differentiator you are proud of is median.

It will tell you a role you want converts at 2%.

It will tell you not to apply.

That is the feature, and it is the only reason any of the rest is worth running.
A pipeline that grades most applications INTERVIEW and converts 5% of them is not
producing signal. It is producing optimism, and it will keep producing it forever
because nothing in the loop ever pushes back. Optimism is what the incumbents
sell. It retains beautifully. It just does not get anybody hired.

The contrarian pass, the pool anchoring, and the per-channel probabilities exist
for one purpose: to make the output load-bearing specifically when it says no.

There is a `Calibration` table in the workspace tracker for exactly this. You
record what the pipeline predicted and what actually happened. The priors get
corrected against your history instead of anyone's confidence.

Ship the tool that can tell you no. Everything else is a hype machine with a
progress bar.

## Fork the substrate

The 9 skills and 8 agents are Markdown. No build step. No runtime. Fork, edit,
install your copy:

```bash
claude plugin uninstall slushpile
```

```bash
claude plugin marketplace remove slushpile
```

```bash
claude plugin marketplace add <your-username>/slushpile
```

```bash
claude plugin install slushpile@slushpile
```

If you change a skill, run the gates before you push. See [CONTRIBUTING.md](../../CONTRIBUTING.md).

## License

MIT. See [LICENSE](../../LICENSE).
