# 疑难排查

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../docs/troubleshooting.md">English</a> ·
  <strong>简体中文</strong> ·
  <a href="../../es/docs/troubleshooting.md">Español</a> ·
  <a href="../../pt-BR/docs/troubleshooting.md">Português (BR)</a> ·
  <a href="../../vi/docs/troubleshooting.md">Tiếng Việt</a>
</p>

<!-- END GENERATED language-nav -->

**`plugin install` 成功了，但技能没出现。** 运行 `claude plugin list`，看有没有 `enabled`。技能在会话启动时加载，所以开一个新会话，或者运行 `/clear`。

**某个技能说它找不到 `preferences.yaml`。** 你所在的目录和你做初始化引导的那个目录不是同一个。每个技能都从当前工作目录读取工作区。见 [工作区](workspace.md)。

**审阅智能体报告说简历几乎是空的。** 它们读的是抽取出来的文本，不是你渲染出来的 PDF。运行 `pdftotext yourresume.pdf -` 看看输出。如果输出是空的或者乱的，那这份简历有版面问题——多栏网格、文本框、放在页眉里的联系方式——而这是一个真实的发现，不是工具故障。ATS 看到的就是 `pdftotext` 看到的。

**求职信读起来很泛泛，或者听着像别人。** 检查 `preferences.yaml` 里的 `voice.is_mine`。如果是 false，你用的是随插件发布的示例文风，它属于插件作者。用 [written-voice-replication](https://github.com/aaddrick/written-voice-replication)
生成你自己的，再把 `voice.agent` 指过去。如果它已经是 true，那多半是语料太薄——几千字是下限。见 [你的文风智能体](voice.md)。

**每个岗位回来都因为薪酬被淘汰。** 打开 `preferences.yaml` 检查 `compensation`。用 `net_qol` 时，最常见的原因是 `current_baseline` 填的是税前数字，而不是税后再扣掉住房之后的数字，这会让每一个 offer 都显得比实际差。

**每个岗位回来都是 Tier 1。** 有东西在对着招聘启事打分，而不是对着申请者池打分。检查 `role_analysis.md` 里是不是真的有这个岗位的百分位原型，而不只是一次关键词比对——一个背后没有申请者池估计的匹配度，只是一个顶着百分位名头的关键词匹配度。见 [评分](architecture/scoring.md)。

**审阅从来不说不。** 检查唱反调者到底跑没跑：它的净结论应该出现在流水线摘要里，也应该出现在 `application.yaml` 的 `contrarian_net` 下面。它本该是自动的而不是有条件的，缺了它的审阅是一次没有证伪环节的审阅。

**校准说数据不够，但明明就够。** 下限是五份*已出结果*的申请，而一份申请只有在 `outcome.stage_reached` 被填上时，或者在投出去超过 30 天仍无回音时，才算已出结果。躺在 `application.yaml` 里、结果字段还空着的申请，算作在途，不算作被拒。`/slushpile:status` 会报告哪些记录不完整。

**一轮审阅得出的发现和上一轮一样。** 那是信号，不是 bug。在不止一轮里被标出来的问题是真的；只被标出来一次的是噪声。如果到第三轮还什么都没动，那些差距就是结构性的，流水线本该这么说出来，而不是再跑第四轮。

**流水线不会替你提交申请。** 它永远不会。没有任何技能会碰门户、邮件或表单。它写出文件；你读它们，然后你把它们寄出去。
