# Getting started

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <strong>English</strong> ·
  <a href="../translations/zh-CN/docs/getting-started.md">简体中文</a> ·
  <a href="../translations/es/docs/getting-started.md">Español</a> ·
  <a href="../translations/pt-BR/docs/getting-started.md">Português (BR)</a> ·
  <a href="../translations/vi/docs/getting-started.md">Tiếng Việt</a> ·
  <a href="../translations/en-x-aibro/docs/getting-started.md">AI Bro</a>
</p>

<!-- END GENERATED language-nav -->

Everything you need before your first run: what to install, what to gather, and
where to run it.

## Getting the plugin

[INSTALL.md](../INSTALL.md) has a route per harness — Claude Code, Codex, Gemini
CLI, Cursor, and a paste-in snippet for anything else. The short version for
Claude Code:

```bash
claude plugin marketplace add VonTerraProject501c3/slushpile
claude plugin install slushpile@slushpile
```

Then, in the directory where you want your job search to live:

```
/slushpile:onboard
```

**Run it somewhere other than the plugin checkout.** The plugin is public code.
The workspace is your employment history, your compensation figures, and your
constraints. See [The workspace](workspace.md).

## What onboarding will ask you for

Worth gathering before you start, because two of these take you longer to find
than the interview takes to run.

**A resume**, in any format. PDF, `.tex`, `.docx`, Markdown. Replaces about ten
minutes of interview with thirty seconds of reading. A LinkedIn data export
works too — `Positions.csv` and `Education.csv` carry most of it.

**A writing corpus**, for your voice agent. Several thousand words of your own
unedited prose. Onboarding does not analyze this itself — it points you at
[written-voice-replication](https://github.com/aaddrick/written-voice-replication),
which is a separate pipeline you run once. Gathering the corpus is the slow
part, so start early. See [Your voice agent](voice.md).

Good sources: forum and Reddit posts, blog posts, long Slack messages, emails
to colleagues, pull request descriptions, documentation you wrote alone. A
Reddit or Twitter data export works directly.

Bad sources: anything co-written, anything edited by someone else, anything
already run through an LLM, anything in an institutional voice. Marketing copy
and performance reviews are the two worst.

**Your numbers.** Budgets, headcounts, percentages, and the *before* state for
each. "Cut latency 40%" is unusable until you know 40% of what, and onboarding
will ask.

**Your compensation situation**, if you want the compensation gate to work. For
the recommended method it needs your current gross, your tax, and your housing
cost. It does the arithmetic; you do not have to arrive with a number.

## Requirements

**Required:** an agent that can read local files and browse the web.

**Recommended:** `pdftotext` (from `poppler-utils`), so the review agents see
what an ATS sees rather than what your PDF viewer shows.

```bash
sudo dnf install poppler-utils     # Fedora
sudo apt install poppler-utils     # Debian, Ubuntu
brew install poppler               # macOS
```

**Optional:** a LaTeX toolchain, if you use `templates/resume.tex` and
`templates/cover_letter.tex`. Every skill works on extracted text and none of
them require LaTeX — only those two templates do.

```bash
sudo dnf install -y texlive-xetex texlive-fontspec texlive-microtype latexmk dejavu-fonts-all
sudo apt install texlive-xetex texlive-fonts-extra fonts-dejavu latexmk
brew install --cask mactex-no-gui
```

Build with `latexmk -xelatex resume.tex && latexmk -c`. Two commands: the first
builds, the second cleans. Neither does both.

The templates are set in Public Sans and IBM Plex Mono. Neither ships with TeX
Live, so both are vendored in this repository and one command installs them:

```bash
python3 scripts/install_fonts.py            # install
python3 scripts/install_fonts.py --check    # report, change nothing
python3 scripts/install_fonts.py --uninstall
```

It copies seven font files into your user font directory and refreshes the
cache. Nothing else runs it, and skipping it is fine: both templates fall back
to DejaVu when a family is absent, so a missing font changes how the documents
look and never whether they build.

To restyle them into something of your own, run
`/slushpile:redesign-templates` rather than editing the plugin checkout, which
the next update replaces.

## Your first hour

```
/slushpile:onboard                          # once, in your workspace directory
/slushpile:job-board-search <company|query> # search, score, and create role folders
/slushpile:application-builder <path>       # build and review one application
```

`onboard` is an interview, not a form, and it is the only stage that asks you
questions you will not be asked again. Everything after it reads what it wrote.

Start with `job-board-search` on a company you are genuinely interested in
rather than on the first role you find. The search stage is the only one that
can still talk you out of an application for free, and it is where the pipeline
returns the most per minute spent.

If you do not have a company in mind, describe what you are looking for instead
and the same command resolves it into a list — `applied AI roles within 50 miles
of Martinsville, VA that fit my profile` works as an argument. It shows you the
companies it picked before it searches any of them, so a list built on a
misread of your query costs you one correction rather than an hour.

[Skills](skills.md) is the full command reference.
