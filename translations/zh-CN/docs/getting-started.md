# 上手

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../docs/getting-started.md">English</a> ·
  <strong>简体中文</strong> ·
  <a href="../../es/docs/getting-started.md">Español</a> ·
  <a href="../../pt-BR/docs/getting-started.md">Português (BR)</a> ·
  <a href="../../vi/docs/getting-started.md">Tiếng Việt</a>
</p>

<!-- END GENERATED language-nav -->

第一次运行之前你需要的一切：装什么，准备什么，在哪里跑。

## 拿到插件

[INSTALL.md](../INSTALL.md) 给每一种宿主环境都备了一条路线 —— Claude Code、Codex、Gemini
CLI、Cursor，还有给其他任何东西用的一段粘贴片段。Claude Code 的简版：

```bash
claude plugin marketplace add aaddrick/slushpile
claude plugin install slushpile@slushpile
```

然后，在你希望求职工作区所在的那个目录里：

```
/slushpile:onboard
```

**在插件签出目录以外的地方跑它。** 插件是公开代码。工作区是你的工作履历、你的薪酬数字、
你的约束条件。见 [工作区](workspace.md)。

## 初始化引导会问你什么

值得在开跑之前先备好，因为其中两项你找起来花的时间，比访谈本身跑完还长。

**一份简历**，什么格式都行。PDF、`.tex`、`.docx`、Markdown。用三十秒的阅读换掉大约十分钟的
访谈。LinkedIn 的数据导出也行 —— `Positions.csv` 和 `Education.csv` 装着其中大部分。

**一份写作语料**，给你的文风智能体用。几千字你自己写的、未经编辑的文字。初始化引导本身不
分析它 —— 它把你指向
[written-voice-replication](https://github.com/aaddrick/written-voice-replication)，
那是一条你只跑一次的独立流水线。攒语料是慢的那一部分，所以早点开始。见
[你的文风智能体](voice.md)。

好的来源：论坛和 Reddit 帖子、博客文章、长条 Slack 消息、写给同事的邮件、pull request
描述、你一个人写的文档。Reddit 或 Twitter 的数据导出可以直接用。

坏的来源：任何合写的东西、任何被别人编辑过的东西、任何已经过了一遍大模型的东西、任何用
机构口吻写的东西。营销文案和绩效评语是最糟的两种。

**你的数字。** 预算、人头数、百分比，以及每一项对应的*之前*状态。“把延迟砍了 40%”在你
知道是什么的 40% 之前都没法用，而初始化引导会问。

**你的薪酬情况**，前提是你想让薪酬门槛真的起作用。按推荐的算法，它需要你当前的税前收入、
你的税、你的住房成本。算术它来做；你不必自带一个数字过来。

## 前置要求

**必需：** 一个能读本地文件、能浏览网页的智能体。

**推荐：** `pdftotext`（来自 `poppler-utils`），这样审阅智能体看到的是 ATS 看到的东西，而
不是你的 PDF 阅读器显示的东西。

```bash
sudo dnf install poppler-utils     # Fedora
sudo apt install poppler-utils     # Debian, Ubuntu
brew install poppler               # macOS
```

**可选：** 一套 LaTeX 工具链，前提是你要用 `templates/resume.tex` 和
`templates/cover_letter.tex`。每一个技能都作用于抽取出来的文本，没有一个需要 LaTeX ——
只有那两个模板需要。

```bash
sudo dnf install -y texlive-xetex texlive-fontspec texlive-microtype latexmk dejavu-fonts-all
sudo apt install texlive-xetex texlive-fonts-extra fonts-dejavu latexmk
brew install --cask mactex-no-gui
```

用 `latexmk -xelatex resume.tex && latexmk -c` 构建。两条命令：第一条构建，第二条清理。
哪一条都不兼做另一件。

模板用 Public Sans 和 IBM Plex Mono 排版。两者都不随 TeX Live 分发，所以两者都随本仓库
附带，一条命令就能装上：

```bash
python3 scripts/install_fonts.py            # install
python3 scripts/install_fonts.py --check    # report, change nothing
python3 scripts/install_fonts.py --uninstall
```

它把七个字体文件复制进你的用户字体目录，然后刷新缓存。没有别的东西会调它，跳过也没关系：
字体族缺失时两个模板都回退到 DejaVu，所以缺一个字体只改变文档的样子，永远不改变它们能不
能构建出来。

想把它们改成你自己的样式，跑 `/slushpile:redesign-templates`，而不是去改插件签出目录 ——
下一次更新会把那里覆盖掉。

## 你的第一个小时

```
/slushpile:onboard                    # once, in your workspace directory
/slushpile:job-board-search <company> # search, score, and create role folders
/slushpile:application-builder <path> # build and review one application
```

`onboard` 是一场访谈，不是一张表单，而且它是唯一一个会问你那些以后不会再被问到的问题的
阶段。它之后的一切，读的都是它写下来的东西。

先拿 `job-board-search` 对着一家你真正感兴趣的公司跑，而不是对着你找到的第一个岗位。搜索
这一阶段是唯一还能免费劝你别投的阶段，也是这条流水线每花一分钟回报最高的地方。

[技能](skills.md) 是完整的命令参考。
