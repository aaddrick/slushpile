# 技能

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../docs/skills.md">English</a> ·
  <strong>简体中文</strong> ·
  <a href="../../es/docs/skills.md">Español</a> ·
  <a href="../../pt-BR/docs/skills.md">Português (BR)</a> ·
  <a href="../../vi/docs/skills.md">Tiếng Việt</a>
</p>

<!-- END GENERATED language-nav -->

Slushpile 以9个技能的形式安装。Claude Code 把每一个暴露为 `/slushpile:<name>`；Codex 用 `$slushpile:<name>`；Gemini CLI 和其他宿主读取同样的文件，你用自然语言说出要跑哪个阶段。

其中三个是主干。另外三个会在构建一份申请材料的过程中替你调度，只有在处理不是这条流水线做出来的材料时，你才手动运行它们。最后三个是辅助性的，随时可以跑。

## 主干

### `/slushpile:onboard`

搭建工作区。摄入一份已有的简历或 LinkedIn 导出文件，就缺口对你做访谈，写出 `profile.md`、`preferences.yaml` 和 `stories.md`。检查文档工具链，搭好跟踪表，然后交接。

每个工作区跑一次，在其他一切之前。要准备什么见 [快速上手](getting-started.md)，它写出什么见 [工作区](workspace.md)。

### `/slushpile:job-board-search`

搜索一家公司的招聘页面，逐字提取每一条招聘启事，估算现实中的申请人池，做以池为基准、按渠道条件化的匹配评分，跑一遍淘汰标准，在分档列表之前先放一遍反方，并为每个存活下来的岗位建一个岗位文件夹。

**参数：** 一个公司名称。

这是流水线里回报最高的一个阶段，也是大多数工具没有的那个。它之后的每一步都要花掉一个下午；这一步只要几分钟，而且可以以"这些都不投"收场。见 [评分](architecture/scoring.md)。

### `/slushpile:application-builder`

为一个已经有职位描述和岗位分析的岗位文件夹构建针对性的简历和求职信，然后拿它们对着评审反复迭代，直到稳定下来，或者撞上三轮的上限。

**参数：** 一个岗位文件夹路径。

它自己会调度 `explore-experience`、`adversarial-review` 和 `removing-ai-tells`。它从不提交任何东西；它交给你的是做完的文件。

## 它替你跑的那三个

只有在处理不是这条流水线做出来的材料时——别处写的简历、手写的求职信——才直接运行它们中的某一个。

### `/slushpile:adversarial-review`

针对一份简历和一封求职信运行7个角色。返回每个投递渠道的结论和概率区间，把材料质量和期望值分开打分，外加一遍可以推翻其余全部结论的反方复核。

**参数：** 一个岗位文件夹路径，至少要包含一份简历和 `job_description.md`。

每个角色被展示了什么、又被刻意扣下了什么，见 [评审](architecture/the-review.md)。

### `/slushpile:explore-experience`

访谈你，挖出真实存在但没有写下来的经历，对照某个具体岗位的要求做映射，然后把它永久写进 `profile.md`。

在匹配度评估或评审指出某一节内容单薄时使用。多数时候那段经历确实是真的，只是从来没被写下来过，这也是为什么这里是一次访谈而不是一次改写。

### `/slushpile:removing-ai-tells`

剥掉那些暴露 AI 撰写痕迹的措辞、结构和用词，做法是通过全新的文风智能体实例做多轮迭代，由编排方对每一处单独改动逐条把关。

用在提交前的求职信上，或者任何必须读起来像人写的文字上。

## 随时可跑

### `/slushpile:redesign-templates`

把 `resume.tex` 和 `cover_letter.tex` 重做成你自己的样式——排版、配色、版面——同时保持 ATS 约束不变，然后证明结果仍然能编译、仍然能被抽取出来。

跑这个，而不是去改插件的 checkout 目录，那个下次更新就会被替换掉。

### `/slushpile:status`

读取工作区里每一个 `application.yaml`，报告这场求职的状态：排好序的队列、正在等你的事、已经没了动静的事，以及流水线自己的预测对实际结果的回归。把校准结论写回 `job_search.md` 和 `preferences.yaml`。

结果落地之后跑它。见 [记忆与校准](architecture/memory-and-calibration.md)。

### `/slushpile:help`

解释 slushpile 是什么、每个技能做什么、按什么顺序跑、工作区文件在哪里，以及怎么配一个文风智能体。

在你不确定该跑什么的时候跑它。
