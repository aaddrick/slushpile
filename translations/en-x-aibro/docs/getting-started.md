# Getting started

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../docs/getting-started.md">English</a> ·
  <a href="../../zh-CN/docs/getting-started.md">简体中文</a> ·
  <a href="../../es/docs/getting-started.md">Español</a> ·
  <a href="../../pt-BR/docs/getting-started.md">Português (BR)</a> ·
  <a href="../../vi/docs/getting-started.md">Tiếng Việt</a> ·
  <strong>AI Bro</strong>
</p>

<!-- END GENERATED language-nav -->

Onboarding is the highest-leverage hour in this entire system.

Everything downstream reads what that hour produces. Every application for the
next three months initializes from it. Walk in cold and you get a thin substrate,
and a thin substrate does not announce itself, it just quietly caps the ceiling
on every artifact after it.

So: what to install, what to bring, where to run it.

## Getting the plugin

[INSTALL.md](../INSTALL.md) has a route per harness. Claude Code, Codex, Gemini
CLI, Cursor, and a paste-in snippet for anything else. Short version:

```bash
claude plugin marketplace add aaddrick/slushpile
claude plugin install slushpile@slushpile
```

Then, in the directory where you want your job search to live:

```
/slushpile:onboard
```

**Not in the plugin checkout.** The plugin is public code. The workspace is your
employment history. Different assets, different blast radius, different
directories. See [The workspace](workspace.md).

## Bring these to the interview

Gather first. Two of these take longer to find than the interview takes to run,
and blocking on inputs mid-interview is how a one-hour setup becomes three.

**A resume.** Any format. PDF, `.tex`, `.docx`, Markdown. Trades ten minutes of
interview for thirty seconds of parsing. A LinkedIn export works too:
`Positions.csv` and `Education.csv` carry most of the payload.

**A writing corpus.** Several thousand words of your own unedited prose, for your
voice agent. Onboarding does not analyze this itself. It routes you to
[written-voice-replication](https://github.com/aaddrick/written-voice-replication),
a separate pipeline you run once. This is the long pole. Start it before you need
it. See [Your voice agent](voice.md).

High-signal: forum and Reddit posts, blog posts, long Slack messages, emails to
colleagues, pull request descriptions, docs you wrote alone. A Reddit or Twitter
export drops straight in.

Contaminated: anything co-written, anything edited by someone else, anything
already through an LLM, anything in an institutional voice. Marketing copy and
performance reviews are the two worst inputs available. Both are already somebody
else's voice wearing your name, and the model cannot tell the difference. Garbage
in, generic out.

**Your numbers.** Budgets, headcounts, percentages, and the *before* state for
each. "Cut latency 40%" is an unusable claim until somebody knows 40% of what.
Onboarding will ask. Have the denominator.

**Your comp situation**, if you want the comp gate to do anything at all. The
recommended method needs current gross, tax, and housing cost. It runs the
arithmetic. You do not need to arrive with a number, only with the inputs.

## Requirements

**Required:** an agent that can read local files and browse the web.

**Recommended:** `pdftotext`, from `poppler-utils`.

```bash
sudo dnf install poppler-utils     # Fedora
sudo apt install poppler-utils     # Debian, Ubuntu
brew install poppler               # macOS
```

Without it the review reads your PDF as rendered. With it the review reads what
an ATS reads. Those are two different documents and only one of them decides
whether a human ever sees you. Optimize for the parser, not the renderer.

**Optional:** a LaTeX toolchain, if you use `templates/resume.tex` and
`templates/cover_letter.tex`. Every skill operates on extracted text. Nothing
requires LaTeX except those two templates.

```bash
sudo dnf install -y texlive-xetex texlive-fontspec texlive-microtype latexmk dejavu-fonts-all
sudo apt install texlive-xetex texlive-fonts-extra fonts-dejavu latexmk
brew install --cask mactex-no-gui
```

Build with `latexmk -xelatex resume.tex && latexmk -c`. Two commands: the first
builds, the second cleans. Neither does both.

The templates are set in Public Sans and IBM Plex Mono. Neither ships with TeX
Live, so both are vendored here and one command installs them:

```bash
python3 scripts/install_fonts.py            # install
python3 scripts/install_fonts.py --check    # report, change nothing
python3 scripts/install_fonts.py --uninstall
```

Seven font files into your user font directory, cache refreshed. Skipping it is a
supported path: both templates fall back to DejaVu when a family is missing, so
the documents look different and still build. Graceful degradation, on purpose.

Want your own house style? Run `/slushpile:redesign-templates`. Do not edit the
plugin checkout. The next update overwrites it and takes your work with it.

## Your first hour

```
/slushpile:onboard                          # once, in your workspace directory
/slushpile:job-board-search <company|query> # search, score, and create role folders
/slushpile:application-builder <path>       # build and review one application
```

`onboard` is an interview, not a form. It is the only stage that asks you
questions you will never be asked again.

Then start with `job-board-search` on a company you actually want, not the first
posting you find. That stage is the only one that can still talk you out of an
application for free. Highest return per minute in the pipeline, and the one
everybody is tempted to skip because it does not produce a document.

No company in mind? Describe the work instead. The same command takes
`applied AI roles within 50 miles of Martinsville, VA that fit my profile` as an
argument and resolves it into a list of companies, then puts that list in front
of you before it searches a single one of them. A list built on a misread of your
query costs you one correction instead of an hour.

[Skills](skills.md) is the full command reference.
