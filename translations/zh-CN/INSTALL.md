# 安装

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../INSTALL.md">English</a> ·
  <strong>简体中文</strong> ·
  <a href="../es/INSTALL.md">Español</a> ·
  <a href="../pt-BR/INSTALL.md">Português (BR)</a> ·
  <a href="../vi/INSTALL.md">Tiếng Việt</a>
</p>

<!-- END GENERATED language-nav -->

slushpile 就是9个技能和8个智能体定义，全部是 Markdown。下面每一条路线，都是把同一批文件放到你的智能体会去读的地方。

**装任何东西之前先定一件事：** 你的工作区放在哪里。

插件是代码。工作区是你的从业经历、你的薪资、你的各项限制条件。它们是两回事，就该待在两个不同的目录里。插件装到你的智能体存放插件的地方；`/slushpile:onboard` 在另一个你自己保密的目录里跑。

---

## Claude Code

完整流水线。技能变成斜杠命令，8个智能体作为子智能体被调度，5个并行审阅者是真正并行跑的。

```bash
claude plugin marketplace add aaddrick/slushpile
```

```bash
claude plugin install slushpile@slushpile
```

验证：

```bash
claude plugin list
```

你应该看到 `slushpile@slushpile` 和 `enabled`。

然后开始：

```
/slushpile:onboard
```

在你希望求职工作区所在的那个目录里运行它。

### 更新

```bash
claude plugin marketplace update slushpile
```

```bash
claude plugin install slushpile@slushpile
```

### 卸载

```bash
claude plugin uninstall slushpile
```

```bash
claude plugin marketplace remove slushpile
```

这两条命令都不会碰你的工作区文件。

---

## Codex

```bash
codex plugin marketplace add aaddrick/slushpile --ref main
```

```bash
codex plugin add slushpile@slushpile
```

在 Codex 里，`/plugins` 打开插件浏览器。

Codex 会给插件技能加上插件名前缀：

```
$slushpile:onboard
```

**差别在哪。** Codex 没有子智能体调度。审阅流水线在同一个上下文里顺序跑完它的7个角色：从插件的 `agents/` 目录读一份智能体定义，代入它，把报告写完，再进入下一个。

产出的形状是一样的。有两件事会退化，值得知道是哪两件：

1. 更慢。7个角色顺序跑完，而不是5个并行审阅者再加上后面两个。
2. 5个并行审阅者本应彼此不可见。在同一个上下文里做不到，而一个已经看过初筛结论的专项审阅者，会朝着同意它的方向漂移。每份报告都完整写出来再开始下一份，技能里要求的就是这个。

---

## Gemini CLI

```bash
gemini extensions install https://github.com/aaddrick/slushpile
```

扩展把 `GEMINI.md` 指定为它的上下文文件，而那个文件会导入每一个技能和智能体定义。

然后，在你的工作区目录里：

```
Set up a slushpile workspace here.
```

Gemini 同样没有子智能体调度，所以上面那条关于顺序执行的告诫一样适用。

### 手动安装

克隆进扩展目录：

```bash
git clone https://github.com/aaddrick/slushpile ~/.gemini/extensions/slushpile
```

---

## Cursor

Cursor 从它当前打开的那个工作区里读 `.cursor/skills/` 和 `.cursor/rules/`。克隆仓库，把它们复制进你的工作区：

```bash
git clone https://github.com/aaddrick/slushpile /tmp/slushpile
```

```bash
cp -r /tmp/slushpile/.cursor/skills/slushpile <your-workspace>/.cursor/skills/
```

```bash
cp -r /tmp/slushpile/skills /tmp/slushpile/agents /tmp/slushpile/templates <your-workspace>/.slushpile/
```

Cursor 那个技能是个路由器：它指向 `.slushpile/` 下面真正的技能文件。这样流水线只留一份副本，而不是四份。

然后在 Cursor 里输入 `/slushpile`，说出你想做什么。

---

## 其他任何宿主环境

这条流水线就是带 YAML frontmatter 的纯 Markdown。任何能读文件的智能体都能跑它。

把仓库克隆到你的智能体够得着的地方：

```bash
git clone https://github.com/aaddrick/slushpile ~/.slushpile
```

然后把下面这段放进你的 `AGENTS.md`、你的系统提示词，或者你的宿主环境用来放常驻指令的任何地方：

<!-- BEGIN GENERATED harness-snippet: scripts/sync_docs.py -->

```markdown
## slushpile

A job application pipeline lives at `~/.slushpile`. When the user asks to set up
a job search, search a careers board, build an application, or review one, read
the matching skill and follow it:

- `~/.slushpile/skills/onboard/SKILL.md` — set up the workspace, once
- `~/.slushpile/skills/job-board-search/SKILL.md` — search and score roles
- `~/.slushpile/skills/explore-experience/SKILL.md` — interview for undocumented experience
- `~/.slushpile/skills/application-builder/SKILL.md` — build the resume and cover letter
- `~/.slushpile/skills/adversarial-review/SKILL.md` — run the seven-agent review
- `~/.slushpile/skills/removing-ai-tells/SKILL.md` — strip AI-authorship signals from prose
- `~/.slushpile/skills/redesign-templates/SKILL.md` — restyle the document templates
- `~/.slushpile/skills/status/SKILL.md` — report the queue and check pipeline calibration
- `~/.slushpile/skills/help/SKILL.md` — what to run next, and how to read the output

The review dispatches personas defined in `~/.slushpile/agents/`. If you cannot
dispatch subagents, adopt each definition in turn and run them sequentially,
writing each report out before starting the next.

Cover letters are written by the voice agent named in `preferences.yaml` under
`voice.agent`. A working example ships as `aaddrick-voice`; it is the plugin
author's voice, and users generate their own with
https://github.com/aaddrick/written-voice-replication

Workspace templates are in `~/.slushpile/templates/`.
```

<!-- END GENERATED harness-snippet -->

---

## 手册的其余部分

安装之后的一切都在 [docs/](docs/index.md) 里：

- [上手](docs/getting-started.md)：初始化引导之前要准备什么，以及流水线需要装什么 ——
  `pdftotext`，还有可选的 LaTeX 工具链和随仓库附带的文档字体。
- [技能](docs/skills.md)：每一条 `/slushpile:*` 命令，以及什么时候该跑它。
- [工作区](docs/workspace.md)：初始化引导写进你目录里的那些文件，以及每一个由谁来读。
- [你的文风智能体](docs/voice.md)：求职信为什么需要一个，以及怎么生成你自己的。
- [排障](docs/troubleshooting.md)。
- [架构](docs/architecture/index.md)：这条流水线为什么长成现在这个样子。
