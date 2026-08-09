# 智能体与模型

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../../docs/architecture/agents-and-models.md">English</a> ·
  <strong>简体中文</strong> ·
  <a href="../../../es/docs/architecture/agents-and-models.md">Español</a> ·
  <a href="../../../pt-BR/docs/architecture/agents-and-models.md">Português (BR)</a> ·
  <a href="../../../vi/docs/architecture/agents-and-models.md">Tiếng Việt</a> ·
  <a href="../../../en-x-aibro/docs/architecture/agents-and-models.md">AI Bro</a>
</p>

<!-- END GENERATED language-nav -->

## 技能负责编排。智能体只做一件事。

这是两类不同的文件，而它们之间的边界是吃力的。

技能知道流水线的事：自己处在哪个阶段、之前跑过什么、要交接给谁。智能体只知道自己那件活。
**一个知道自己处在哪个阶段的智能体，会为那个阶段做优化，而不是干自己的活**：一个被告知
自己是五个里第一个的初筛者会开始打太极，因为它看得出还有别人会来复核它的工作。

由此推出的那条推论，正是让审阅输出可比较的规则：

**有约束力的限制写在智能体定义里，不写在调度提示里。** 一个每次运行都即兴加几条约束的编排者，
产出的发现在不同申请之间无法比较，而这会摧毁整个系统赖以存在的校准数据。唱反调者的范围限制
出于这个理由放在 `agents/slushpile-contrarian.md` 里，而审阅技能被明确告知不要复述或扩展它们。

数据是例外，而且这个区分值得精确说清。`calibration_priors` 放在调度提示里，因为它改变的是
*智能体知道什么*。范围限制留在定义里，因为它们改变的是*智能体被允许说什么*。前者按设计就该
逐次运行有所不同；后者绝不可以。

## 每个智能体都声明一个模型

<!-- BEGIN GENERATED agent-table: scripts/sync_docs.py -->

| # | Agent | Model | Simulates |
|---|---|---|---|
| 1 | `slushpile-triage-screener` | sonnet | 11 seconds, F-pattern, 347 resumes already read today |
| 2 | `slushpile-requirements-analyst` | sonnet | 30 seconds, methodical, checks every qualification against evidence |
| 3 | `slushpile-ats-simulator` | sonnet | A parser. Not a reader. Structure, keywords, and years-of-experience math |
| 4 | `slushpile-fatigued-reader` | sonnet | Application #61 of 80. What annoys, what gets skimmed, what closes the tab |
| 5 | `slushpile-pool-analyst` | opus | A recruiter who knows what the queue actually looks like |
| 6 | `slushpile-hiring-manager` | opus | The person who has to justify the interview slot to their skip-level |
| 7 | `slushpile-contrarian` | opus | Whoever should have asked whether any of this was worth doing |

Plus the voice agent, `aaddrick-voice`, which the review never dispatches and
which is named in `preferences.yaml` rather than here. The first five run in
parallel and are blind to each other; the last two run in order.

<!-- END GENERATED agent-table -->

模型写在每个智能体的 frontmatter 里，而 `skills/adversarial-review/SKILL.md` 里的调度表
也为每个智能体指名了一个。两者由 `tests/test_structure.py` 互相校验：frontmatter 是宿主环境
实际据以调度的东西，而表格那一列是对它的文档化。

一个没有声明模型的智能体，会沿用会话当前跑的那个。这会无声地抹平一场刻意混用不同档次的审阅，
这也正是这个字段是必填而不是可选的原因。

这个划分不是随意的。便宜的那几个角色各自模拟一次**有界、机械**的阅读：十一秒的扫读、
一张资格核对清单、一个解析器、一个疲惫读者的恼火。这些都是被规定得很清楚的任务，
更大的模型在上面基本只增加成本。

昂贵的那几个各自都需要**估计某个不在文档里的东西**。申请者池分析师必须刻画一批并不摆在它面前的
申请者。招聘经理必须把五份报告互相掂量，并产出概率。唱反调者必须构造出「上述一切都是错的」这一
主张的最强论证。这些在小模型上会明显退化，而它们就是用户真正会据以行动的那三个的输出。

## 命名空间

每个流水线智能体都以 `slushpile-` 为前缀，这样它就不会和用户已有的某个智能体撞名。
一个已经有自己的 `contrarian` 的用户可以留着它；这条流水线的那个叫
`slushpile-contrarian`，两者永不相遇。

## 文风智能体是刻意的例外

文风智能体是本仓库里唯一一个不叫 `slushpile-*` 的智能体，也是唯一一个名字取自某个人的。

这是因为它由
[written-voice-replication](https://github.com/aaddrick/written-voice-replication)
按人逐个生成，并以其作者命名。换用自己那个的用户必须能保留那个名字，所以这个名字是在运行时
从 `preferences.yaml` 读取的，而不是硬编码在任何地方：

```yaml
voice:
  agent: "your-name-voice"
  is_mine: true
```

`agents/aaddrick-voice.md` 作为那条流水线公开的示范样例随包发布，这样在用户还没生成自己那个
之前，slushpile 就能开箱即跑。它是插件作者的文风，不是用户的，而只要 `is_mine` 还是 false，
每一个会起草文字的技能都会在运行前发出警告。那道警告是挡在用户和「以一个陌生人的文风寄出
十二份申请」之间的唯一一样东西。

它被豁免于 `scripts/check_no_pii.py` 里的身份类模式，但绝不豁免于联系方式类模式。参见
[personal-data.md](personal-data.md)。

**不要往这个仓库里再加第二个文风智能体。** 一个样例是演示；两个就是一座没人要的、
装着别人文风的图书馆。
