<p align="center">
  <img src=".github/assets/hero.png" alt="Slushpile: an adversarial job search with a memory. Seven agents try to reject you before a recruiter gets the chance, and what they find, you keep. What you keep: profile.md, every factual claim; preferences.yaml, comp, location and constraints; stories.md, four to eight tellable; job_search.md, outcomes for calibration. Written once, read by every stage, updated by every review. The seven reviewers: triage screener, requirements analyst, ATS simulator, fatigued reader, pool analyst, hiring manager, contrarian. Five in parallel, blind to each other, then synthesis, then an agent whose job is overturning it." width="100%">
</p>

<p align="center">
  <strong>Slushpile</strong><br>
  <em>Seven agents try to reject you before a recruiter gets the chance.</em><br>
  <em>What they find, you keep.</em>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/github/license/aaddrick/slushpile?style=flat" alt="License"></a>
  <a href=".github/workflows/plugin-load-check.yml"><img src="https://img.shields.io/github/actions/workflow/status/aaddrick/slushpile/plugin-load-check.yml?label=plugin%20loads&style=flat" alt="Plugin load check"></a>
</p>

<p align="center">
  <a href="https://www.linkedin.com/in/aaddrick/">Connect on LinkedIn!</a>
</p>

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <strong>English</strong> ·
  <a href="translations/zh-CN/README.md">简体中文</a> ·
  <a href="translations/es/README.md">Español</a> ·
  <a href="translations/pt-BR/README.md">Português (BR)</a> ·
  <a href="translations/vi/README.md">Tiếng Việt</a>
</p>

<!-- END GENERATED language-nav -->

## Install

<details open>
<summary><strong>Claude Code</strong></summary>

```bash
claude plugin marketplace add aaddrick/slushpile
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
codex plugin marketplace add aaddrick/slushpile --ref main
```

```bash
codex plugin add slushpile@slushpile
```

Codex prefixes plugin skills with the plugin name:

```
$slushpile:onboard
```

Codex has no subagent dispatch, so the review pipeline runs its seven personas
sequentially in one context instead of five of them in parallel. Same output,
slower, and slightly more prone to one persona's reasoning bleeding into the
next.

</details>

<details>
<summary><strong>Cursor, Gemini CLI, and manual install</strong></summary>

See [INSTALL.md](./INSTALL.md).

</details>

## The problem

You are not being graded against the job description. You are being graded
against the other seventy people who applied to the same requisition this week.

Almost every tool in this space gets that backwards. Feed a resume and a posting
into a resume optimizer and it will tell you your keyword match went from 68% to
91%, which is a real number about the wrong question. If the 75th-percentile
applicant in that queue matches at 94%, your 91% is a rejection, and nothing in
the tool will ever tell you so.

The second thing they get wrong: they return one verdict. But the same resume
and the same letter convert at maybe 2% through a cold portal submission and 30%
through a referral. Those are not the same decision, and collapsing them into a
single "strong match" is not a simplification. It is an error with a confident
interface on top of it.

The third is the one nobody names. These tools have no memory. You paste a
resume in, you get a number back, you close the tab, and the tool ends the
session knowing exactly what it knew at the start. A search is forty
applications over three months. Every one of them costs full price.

## What this does instead

**It builds a model of you, once.** `/slushpile:onboard` interviews you and writes
three files: a profile, a preferences file, and a set of stories. The profile is
not a resume — it is the pool a resume gets cut from, several times longer than
anything you would ever send. Every later stage reads it, and nothing asks you
those questions twice.

**It tries to talk you out of the role before you write anything.** The search
stage scores each posting against the estimated applicant pool, runs kill
criteria, builds an expected-value matrix per application channel, and puts a
contrarian in front of the tier list. Every other tool starts working after you
have already decided to apply. The expensive mistake happens before that, and
this is the only stage that can still catch it for free.

**It attacks what it just wrote.** A model asked whether its own draft is any
good will tell you yes, at length. So the builder does not ask. It hands the
resume and the letter to seven reviewers, five of whom run in parallel and
cannot see each other's findings, each given only what its role would really
have — the eleven-second screener is never shown the cover letter, because a
screener who read the letter is not one. The builder fixes what comes back and
sends it through again. Round two has to hold before it will let you submit, and
it stops at three rounds, because past that the gaps are structural and more
editing is motion.

**It writes what it learns back into you.** When a review says a section is thin,
the interview that follows usually finds the experience was real and you never
wrote it down. That goes into the profile permanently. The conversion estimates
get corrected against the outcomes you record. Your twentieth application starts
from a better place than your first, which in every other tool is simply not
true.

What comes out is a verdict per channel — cold submission, warm referral, cold
outreach, inbound from your public work — each with a probability range rather
than a verdict word, and with materials quality scored separately from expected
value. "1-3% interview" is information. "MAYBE" is not. Excellent materials sent
to a wrong-fit role still have low expected value, and those two numbers
routinely disagree.

## What changes

Same resume, same posting, same afternoon.

### What a resume optimizer tells you

> **Match score: 91%** ✅
>
> Great news — your resume is a strong match for this role!
>
> ✅ 14 of 16 required keywords found
> ✅ ATS-friendly formatting detected
> ⚠️ Consider adding: "stakeholder alignment", "OKRs"
>
> You're ready to apply!

### What Slushpile tells you

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

One of these is a number about your document. The other is a decision about your
afternoon.

## The pipeline

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

## The manual

The rest of it lives in [docs/](docs/index.md):

- [Getting started](docs/getting-started.md): what to gather before onboarding,
  and what to install.
- [Skills](docs/skills.md): every command, and when to run it.
- [The workspace](docs/workspace.md): the files this writes into your directory.
- [Your voice agent](docs/voice.md), [Troubleshooting](docs/troubleshooting.md).
- [Architecture](docs/architecture/index.md): the diagrams, why the review is
  shaped this way, and how scoring and calibration work.

## Your cover letters need your voice

An eighth agent writes the cover letter. It writes in one specific person's
style, built from a corpus of their own writing.

slushpile ships **`aaddrick-voice`** as a working example so the pipeline runs
out of the box. It is the plugin author's voice, not yours. Letters written with
it will sound like a specific stranger — fine for seeing the pipeline work,
wrong for anything you actually send.

Generate your own with
**[written-voice-replication](https://github.com/aaddrick/written-voice-replication)**.
It analyzes a corpus of your writing across 25 dimensions and outputs a voice
agent, a voice skill, and a numeric profile with measurable targets.
`aaddrick-voice` is that pipeline's own worked example.

Then point `preferences.yaml` at it:

```yaml
voice:
  agent: "your-name-voice"
  is_mine: true
```

While `is_mine` is false, every skill that drafts prose warns you before it
runs. That warning is the only thing standing between you and twelve
applications sent in a stranger's voice.

## Your data stays yours

`/slushpile:onboard` writes three files into *your* directory: `profile.md`,
`preferences.yaml`, and `stories.md`. Every personal fact the pipeline uses
lives there. Nothing is hardcoded into the plugin, and the repository has a CI
gate that fails if a personal fact leaks into a skill.

That workspace will contain your full employment history, your compensation
figures, and your constraints. Keep it in a **private** repository, or in no
repository at all. The onboarding skill will say this to you and it will not
initialize one for you.

**The pipeline never submits anything.** No skill touches an application portal,
an email, or a form. It writes files. You read them and you send them.

## Honesty is the feature

This tool will tell you that a differentiator you are proud of is median. It
will tell you a role you want has a 2% conversion rate. It will occasionally
tell you not to apply.

That is the product. A pipeline that grades most applications INTERVIEW and
converts 5% of them is not producing signal, it is producing optimism, and it
will keep doing that indefinitely because nothing in it ever pushes back. The
contrarian pass, the pool anchoring, and the per-channel probabilities all exist
to make the output usable specifically when it says no.

There is a `Calibration` table in the workspace tracker for exactly this reason:
you record what the pipeline predicted and what actually happened, and the
priors get corrected by your own history rather than by anyone's confidence.

## Tune it

The nine skills and eight agents are Markdown. Fork, edit, install your copy:

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

If you change a skill, run the gates before you push. See [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

MIT. See [LICENSE](./LICENSE).
