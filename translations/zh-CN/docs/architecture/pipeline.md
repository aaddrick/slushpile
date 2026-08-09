# 流水线，逐阶段拆解

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../../docs/architecture/pipeline.md">English</a> ·
  <strong>简体中文</strong> ·
  <a href="../../../es/docs/architecture/pipeline.md">Español</a> ·
  <a href="../../../pt-BR/docs/architecture/pipeline.md">Português (BR)</a> ·
  <a href="../../../vi/docs/architecture/pipeline.md">Tiếng Việt</a>
</p>

<!-- END GENERATED language-nav -->

## 整个循环

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../../../docs/diagrams/pipeline-overview-dark.svg">
  <img alt="Slushpile 的端到端流程。第一行从左到右：onboard，通过访谈并摄入一份简历，写出 profile、preferences 和 stories；job board search，逐字提取招聘启事，并给出申请者池锚定的匹配度评分和渠道期望值评分；application builder，产出切入角度、简历、求职信、文风过稿以及去 AI 味步骤；以及 adversarial review，7个角色，其中5个并行审阅者互相看不到彼此，按渠道各返回一个判定。builder 与 review 之间由一条双向箭头相连，箭头标注为最多三轮。流程从 review 向下落进一个蓝色方框「由你自己投出去」，其中注明没有任何技能会碰投递门户、邮件或表单。第二行从右向左读回：记录结果，然后是 status，它把流水线的预测与真实结果作回归比较，再经一条标注为先验的虚线箭头进入工作区方框，框内存放 profile.md、preferences.yaml、stories.md 和 job_search.md。另一条虚线箭头把工作区连回 onboard，标注为由 onboarding 写入、由每个阶段读取。" src="../../../../docs/diagrams/pipeline-overview-light.svg">
</picture>

主干由三条命令构成：每个工作区跑一次 `onboard`，然后按公司、按岗位分别跑
`job-board-search` 和 `application-builder`。`explore-experience`、
`adversarial-review` 和 `removing-ai-tells` 由 builder 自己调度。

底部那个循环，是简历优化器没有对应物的那部分。结果被记录下来，`status`
把流水线预测过的东西对真实发生的事做回归，校正后的先验回到
`preferences.yaml`，下一次搜索就从那里读它。参见
[memory-and-calibration.md](memory-and-calibration.md)。

## 图例

本页每张图都取自同一套类别词汇，定义在
`docs/diagrams/theme-light.d2` 和 `theme-dark.d2` 里。这两个主题文件和这张表
由 `tests/test_docs.py` 互相校验。

| 类别 | 含义 |
| --- | --- |
| `stage` | 编排技能自己执行的一个普通步骤 |
| `agent` | 一个被调度的角色：带有自己定义（在 `agents/` 中）的子智能体 |
| `gate` | 一道关卡或一个带上限的循环：运行可能在此迭代、停滞或终止 |
| `memory` | 一个持久的工作区文件，写一次，之后每个阶段都读它 |
| `human` | 唯一必须有用户参与的地方 |
| `terminal` | 该图中的终止状态 |
| `phase` | 把一起运行的若干单元框在一起的容器 |
| `flow` | 一条普通的前向边 |
| `loop` | 一条回向边：返工、重审、再来一轮 |
| `writeback` | 一条写入工作区记忆的边 |

`stage` 与 `agent` 之间的区别是最值得仔细读的一处。一个 `agent` 方框是一个子智能体，
有自己的定义和自己的上下文。在无法调度子智能体的宿主环境上，塌缩成同一个上下文的正是这些，
而这次塌缩就是完整运行与降级运行之间的全部差别。

## `/slushpile:onboard`

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../../../docs/diagrams/phase-onboard-dark.svg">
  <img alt="初始化引导的各个阶段。第一行：摄入任意格式的简历或一份 LinkedIn 导出文件；就文档填不了的空白做访谈，涉及数字的地方给出基准；profile.md，被描述为简历从中裁剪出来的那个素材池，而不是一份简历；preferences.yaml，存放薪酬计算方法和约束条件，其中 calibration_priors 留空。第二行从右向左读回：stories.md，四到八个可讲述的故事，都附上数字；一道文风智能体关卡，把用户指向属于他们自己的那个，在他们拥有之前把 is_mine 保持为 false；scaffold，写出 job_search.md 和 companies.md 并运行工具链检查；以及验证与交接，其中每一项检查都被报告，包括通过的那些。" src="../../../../docs/diagrams/phase-onboard-light.svg">
</picture>

初始化引导是一场访谈，不是一张表单。它只跑一次，之后的一切都读它写下的东西。

其中两步是关卡而非工作。文风智能体那一步拒绝自己去构建文风画像：由几份写作样本临时拼出的
画像，读起来就是模型的默认腔调套上了用户的名字，而用户会因为它看上去很完整而信任它。
这一步把 `voice.is_mine: false` 设好，并转而指向
[written-voice-replication](https://github.com/aaddrick/written-voice-replication)。
验证那一步会说明哪些检查*通过了*，而不只是哪些失败了，因为一项只报告失败的检查，
和一项根本没跑过的检查无法区分。

`calibration_priors` 是刻意留空的。一个凭空捏造的先验，是用户从未选择过的约束，
会因为他们看不见的理由悄悄杀掉一些岗位。它要么日后由真实结果填上，要么就一直空着，
而下游每一个估计值都会被标注为未校准。

## `/slushpile:job-board-search`

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../../../docs/diagrams/phase-search-dark.svg">
  <img alt="招聘板搜索的各个阶段。第一行：发现，找到招聘页 URL 并跑若干条查询，然后按职位标题做初筛；逐字捕获，按原文而非摘要的方式拿下招聘启事；申请者池估计，把还有谁会投这个岗位刻画成 p50、p75 和 p90 三个原型；以及匹配度评分，其中作为数字的是申请者池百分位，而不是关键词匹配度。第二行从右向左读回：渠道期望值矩阵，横跨冷投、内推、主动触达和被动引流，其中档位取实际可用渠道中的最优者；淘汰条件，针对薪酬、地点和涉密许可，无论通过与否都要检查并说明；一道唱反调关卡，在档位定稿之前运行，可以把某个档位降级或直接杀掉一个岗位；以及岗位文件夹，每个岗位一个，内含职位描述与分析，同时更新追踪文件和公司文件。" src="../../../../docs/diagrams/phase-search-light.svg">
</picture>

这是回报最高的阶段，也是大多数工具没有的那个阶段。下游的一切，每份申请都要花掉用户一个
下午。这个阶段只花几分钟，而且可以以「这些一个都别投」收场。

招聘启事是**逐字**捕获的。后面有3个智能体直接解析这段文本，即需求分析师、ATS 模拟器和
申请者池分析师，而一份被摘要过的启事会悄悄抹掉资格要求的原文措辞，而那正是这三者存在的
意义所在。

唱反调关卡跑在档位定稿*之前*而不是之后，因为用户已经读过的分级列表，就是他们已经认下的
分级列表。档位是什么意思、淘汰条件检查什么，参见 [scoring.md](scoring.md)。

## `/slushpile:application-builder`

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../../../docs/diagrams/phase-build-dark.svg">
  <img alt="申请构建器的各个阶段。第一行：切入角度，选定基础简历、论点、开场钩子，以及唯一值得讲的那个故事；简历，先改写再编译，读的是抽取出的文本而不是源文件；求职信，由 preferences.yaml 中指名的文风智能体撰写；以及去 AI 味，运行 removing-ai-tells，由编排者对每一处改动逐条把关。第二行从右向左读回：对抗式审阅第一轮，产出 ATS 分数、替换测试和按渠道的期望值；修复，先做机械性订正，然后是从 profile.md 中取材的深度补充；对抗式审阅第二轮，其决策关卡读取期望值最高那个渠道的判定，并通过一条标注为最多三轮的虚线回路连回修复；以及收尾，最终构建，产出 application.yaml，并更新画像和追踪文件。" src="../../../../docs/diagrams/phase-build-light.svg">
</picture>

构建器先写，然后攻击自己写出来的东西。一个被问到自己的草稿好不好的模型，会长篇大论地说好，
所以构建器从来不问，它把材料交给一场对这些材料没有利害关系的审阅。

修复的顺序很重要。机械性修复排在前面，因为它们便宜且无歧义：缺失的关键词、只写到年份的
日期、一条几乎逐字抄自招聘启事的要点。只有做完这些，它才去尝试昂贵的那一类，也就是必须
从 `profile.md` 里补足一个单薄的段落；而如果材料确实不在画像里，它会运行
`/slushpile:explore-experience`，而不是把它编出来。

**三轮是上限。** 如果到第三轮判定仍未移动，差距就是结构性的，继续编辑只是动作而非进展。
这个上限之所以存在，是因为另一种选择是一个永远能找出点什么的循环，而一场永远能找出点什么的
审阅，和一场什么也找不出的审阅无法区分。

## `/slushpile:adversarial-review`

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../../../docs/diagrams/phase-review-dark.svg">
  <img alt="对抗式审阅。先收集材料：对编译好的 PDF 跑 pdftotext，外加职位描述、岗位分析、preferences.yaml 和 job_search.md。这些材料喂进一个容器，容器里是5个并行审阅者，在同一条消息中调度，谁也看不到别人的报告：初筛者，十一秒，只看简历；需求分析师，三十秒，逐条核对每项资格要求；ATS 模拟器，是解析器而不是读者；疲惫读者，正在处理八十份中的第六十一份申请；以及申请者池分析师，问的是队列里还有谁。一条标注为五个全部返回的边通向招聘经理，它看到全部五份报告，并按渠道各产出一个判定，其中材料质量与期望值分开评分。接着是唱反调者，它看到包括招聘经理在内的一切，并可以推翻它，而且从不是可选项。再接着是守门人，它是编排者而不是一个智能体，负责剔除误报和越界的淘汰判断、重新推导净结论，并在材料发生变化时用全新实例重跑整条流水线。最后是呈现与记录，按对期望值最高那个渠道的影响排序，而不是按哪个智能体嗓门最大。" src="../../../../docs/diagrams/phase-review-light.svg">
</picture>

容器里的5个并行审阅者在同一条消息中调度，彼此看不到对方的发现。每一个只拿到它这个角色
真的会有的东西：初筛者永远不会看到求职信，因为读过求职信的筛选者就不是筛选者了。

守门人是那个编排技能，不是一个智能体。这些角色是刻意刻薄的，它们产出的东西有一部分是错的，
所以必须有什么东西对它们的输出施加判断，而那个东西不能是它们中的一员。

调度顺序、每个角色被扣下了什么、守门人被允许剔除哪些发现，都在
[the-review.md](the-review.md) 里。
