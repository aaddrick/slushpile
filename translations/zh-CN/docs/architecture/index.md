# Slushpile 架构

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../../docs/architecture/index.md">English</a> ·
  <strong>简体中文</strong> ·
  <a href="../../../es/docs/architecture/index.md">Español</a> ·
  <a href="../../../pt-BR/docs/architecture/index.md">Português (BR)</a> ·
  <a href="../../../vi/docs/architecture/index.md">Tiếng Việt</a> ·
  <a href="../../../en-x-aibro/docs/architecture/index.md">AI Bro</a>
</p>

<!-- END GENERATED language-nav -->

Slushpile 不是一个程序。它是一组 Markdown 文件，由编码智能体读取并据此行动：
9个技能负责编排，8个智能体定义各自只做一件事，外加少量模板。没有引擎，没有运行时，
在用户自己的工作区目录之外也没有任何状态。

这一点决定了这里记录的每一个决策。这条流水线想要强制执行的规则，必须能在模型高负载下
被改写复述后依然成立，因为没有解释器来强制它。流水线所需的事实，必须存在于模型真的会
读到的文件里，因为没有数据库可供查询。

| 文件 | 内容 |
| --- | --- |
| [pipeline.md](pipeline.md) | 五张图、图例，以及每个阶段做什么。 |
| [the-review.md](the-review.md) | 审阅为什么是现在这个形状：盲审阶段、调度顺序、守门人，以及三轮上限。 |
| [scoring.md](scoring.md) | 申请者池锚定、按渠道条件化的判定、档位，以及淘汰条件。 |
| [memory-and-calibration.md](memory-and-calibration.md) | 作为持久记忆的工作区、回写路径，以及预测如何被真实结果校正。 |
| [agents-and-models.md](agents-and-models.md) | 技能与智能体的边界、每个角色对应的模型档次，以及文风智能体。 |
| [personal-data.md](personal-data.md) | 为什么插件里不得存放任何个人事实，以及强制执行这一点的关卡。 |
| [generated-surfaces.md](../../../../docs/architecture/generated-surfaces.md) | 为什么有六个界面描述这条流水线，而没有一个界面拥有某个事实。 |
| [AGENTS.md](../../../../docs/architecture/AGENTS.md) | 本目录 `CLAUDE.md` 的逐字节孪生副本，用这些约定来约束编辑行为。 |
