# 工作区

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../docs/workspace.md">English</a> ·
  <strong>简体中文</strong> ·
  <a href="../../es/docs/workspace.md">Español</a> ·
  <a href="../../pt-BR/docs/workspace.md">Português (BR)</a> ·
  <a href="../../vi/docs/workspace.md">Tiếng Việt</a>
</p>

<!-- END GENERATED language-nav -->

`/slushpile:onboard` 在**你的**目录里运行，不在插件的 checkout 目录里，流水线关于你所知道的一切都住在那里。

那个目录会装着你完整的工作履历、你的薪酬数字和你的约束条件。把它放进**私有**仓库，或者干脆不放进任何仓库。初始化引导会把这话对你说一遍，而且它不会替你初始化仓库，也不会加远程地址——那是一个要刻意做出的决定，不是从某个安装步骤里继承来的。

## 初始化引导写出什么

```
profile.md          every factual claim about you
preferences.yaml    compensation, location, constraints, calibration priors
stories.md          four to eight tellable stories, with the numbers attached
job_search.md       the tracker: applications, outcomes, calibration
companies.md        one line per company ever looked at
applications/       one folder per role, created by job-board-search
```

### `profile.md`

**它不是简历。** 它是简历从中裁下来的那个池子，比你会寄出去的任何东西都长上好几倍，因为简历是一次挑选，而这是被挑选的那个东西。

里面每一个数字都带着一条基线，或者被明确标为不需要基线。"把延迟砍掉 40%"在读者知道是什么的 40% 之前都用不了，而一个没有出处的数字，正是你在面试里会被追问却答不上来的那个。来源未经核实的数字标为 `UNVERIFIED`，而不是删掉。

它会长。当一次审阅说某一节内容单薄时，`/slushpile:explore-experience` 会访谈你，并把它问出来的东西写回这里，这样下一次申请就从这里起步。

### `preferences.yaml`

机器可读的那一半。薪酬计算方式和基线、地点与搬迁约束、涉密许可与学历状态、你自称的差异化优势、你的文风智能体，以及 `calibration_priors`。

有两个字段比其余的都更能干活：

```yaml
voice:
  agent: "your-name-voice"
  is_mine: true
```

只要 `is_mine` 是 false，每一个会起草文字的技能都会在运行前警告你。见 [你的文风智能体](voice.md)。

`calibration_priors` 一开始是空的，并且一直空着，直到你在某个渠道上有五份或更多已出结果的申请。空的先验意味着智能体使用出厂默认值，并把自己的估计标注为未校准，这是正确的行为——由两个结果算出来的先验，会把评分推得比没有先验时离现实更远，而且它到手时看上去还很有实证的样子。

### `stories.md`

四到八个你真讲得出来的故事，数字都附在上面。构建器每份申请挑一个；你最终拿到的那场面试就跑在这些上面。

### `job_search.md`

跟踪表，也是流水线的长期记忆。申请、它们的结果、每家公司此前的申请，以及一个由 `/slushpile:status` 用你自己的结果重写的 `Calibration` 小节。

在一次审阅中，某家公司此前的申请历史会被申请者池分析师和唱反调者读到。此前在**更高**级别上被拒是有实质影响的：招聘方看得到整份申请人跟踪记录，而后来一次更低级别的申请，读起来就是连降数级。

### `companies.md`

你看过的每一家公司一行，这样在同一家公司做第二次搜索时，可以从第一次找到的东西起步。

## 岗位文件夹

`/slushpile:job-board-search` 为每一个熬过分档的岗位建一个文件夹：

```
applications/<Company>/<Function>/<Role>/
  job_description.md    the posting, captured verbatim
  role_analysis.md      pool position, channel EV, kill criteria, contrarian notes
  application.yaml      the record: verdicts, scores, channel used, outcome
  resume.tex            copied per role by the builder
  cover_letter.tex      copied per role by the builder
```

招聘启事是**逐字**存下来的，不做摘要。审阅期间有3个智能体直接解析那段文字，而一次转述会悄悄抹掉它们存在就是为了核对的那些确切的资格措辞。

`application.yaml` 是 `/slushpile:status` 用来构建队列、并把预测对结果做回归的那个文件。它也是有事情发生时该更新的那个文件：一封拒信、一次初筛、一次面试、一个 offer。流水线里没有别的东西能知道这些，因为流水线从不提交任何东西，也从来看不到回复。

模板是**复制进每个岗位文件夹**的，而不是留在工作区根目录。放在根目录的那份原始副本，从第一份申请偏离它的那一刻起就成了过期副本。

## 插件里永远不会有的东西

`skills/` 或 `agents/` 里没有任何东西硬编码关于你的事实。没有薪酬底线，没有地点，没有涉密许可状态，没有雇主。需要其中某一项的技能在运行时从 `preferences.yaml` 读取，而且只要有个人事实漏进插件，一道 CI 关卡就会让构建失败。

这正是工作区可移植、插件可更新的原因：你可以重装、fork 或更新 slushpile，而不用碰任何关于你自己的东西。见 [个人数据](architecture/personal-data.md)。
