# 评测底层原理与 Bio-Spec MVP

> 本文是当前项目关于数据集、评分、人工评测、Skill/Spec 因果对照和前后版本比较的统一结论。这里的 “Spec/SPC/SPCAT” 均指本仓库正在建设的 Bio-Spec 体系；如果 SPCAT 是另一个同名项目，需另外核对仓库链接。

## 0. 先给结论

你的核心判断是对的：**必须先固定一组可复现的数据集和任务，再固定一个独立的评测器，最后才谈 Skill、Spec 或模型是否有效。**

但这件事不等于普通的监督学习准确率。它同时是：

1. **科学测量问题**：我们要定义“正确科学结果”是什么、允许哪些等价实现、哪些错误属于致命错误。
2. **受控实验问题**：同一任务、同一数据、同一模型、同一工具预算，只改变是否提供 Skill/Spec。
3. **随机策略评估问题**：Agent 是一个根据状态连续选择动作的随机策略，结果是轨迹和最终 artifact，而不是一次静态分类。
4. **文本程序优化问题**：如果用历史得分改写 SKILL.md 或 Spec，优化的是外部文本状态，不是模型权重；这属于黑盒、无梯度、带验证门的搜索。

因此，最重要的不是先装 Langfuse、LangSmith、Ragas、Phoenix、DSPy 或某个“全能 harness”，而是先完成：

~~~text
一个固定 Bio case
→ 一个独立 oracle/reference package
→ 一个 hidden deterministic verifier
→ C00/C01/C10/C11 四个受控条件
→ 重复运行、task-level 统计、人工盲评
→ 冻结 holdout 后才允许改写 Skill/Spec
~~~

当前仓库的技术测试已经通过一部分，但 **Skill efficacy、Spec efficacy、交互效应、完整科研正确率和完全自驾仍然没有数值证据**。这个边界不能被 93/93 的代码测试通过掩盖。详见 [FINAL-TEST-SCORE-CONCLUSION.md](FINAL-TEST-SCORE-CONCLUSION.md)。

## 1. 传统监督学习到底在测什么

### 1.1 最小数学对象

监督学习先假设有带标签样本：

~~~text
D = {(x_i, y_i)} , i = 1 ... n
模型 f_theta: x → y_hat
损失 L(y_hat, y)
风险 R(theta) = E_{(x,y)~P}[L(f_theta(x), y)]
~~~

- x 是输入；
- y 是目标标签或真值；
- f_theta 是待学习的函数；
- L 把“错多少、错在哪里、错误代价多大”编码成数值；
- 训练的目标是让经验风险低，并且对没有见过的 P 中样本仍然有效。

真正要估计的是总体风险 R，而不是训练集上的分数。训练集分数高只说明模型记住了已见样本；测试集分数才是在假设数据分布近似稳定时，对泛化风险的估计。

### 1.2 为什么必须分 train、validation、test

如果反复看 test 分数并修改模型、特征或提示词，test 就参与了决策，最后的分数会偏乐观。这就是测试集泄漏。传统做法是：

~~~text
train       用于学习参数或产生候选
validation  用于选模型、选超参数、选提示词/Skill/Spec 版本
test        只在决策冻结后使用一次或极少数次
~~~

交叉验证是在样本少时重复切分训练/验证，但仍应保留真正冻结的最终 test。scikit-learn 对“调参会让 test 泄漏、因此需要 validation 或交叉验证”的说明，是本项目划分 dev/validation/holdout 的直接传统依据：[scikit-learn cross-validation](https://scikit-learn.org/stable/modules/cross_validation.html)。

### 1.3 标签不是“真理”，而是测量仪器

一个标签 y 可能来自：

- 形式化规则（例如 JSON schema、数值恒等式）；
- 参考实现或参考 artifact；
- 专家标注；
- 多名专家的一致意见；
- 有误差的实验测量。

所以评测器本身也需要验证。必须问：

1. 它是否测到了目标构念，而不是容易投机的表面格式？
2. 参考答案是否唯一？如果不唯一，是否接受等价解？
3. 标签/评分者之间是否一致？
4. 错误代价是否对称？在科研中，漏掉真实信号、误报信号、物种错配、把描述性重叠写成因果机制，代价显然不同。

这就是为什么 Bio-Spec 不能只用“答案字符串相似度”或一个 LLM judge。

### 1.4 准确率只是一个聚合方式

二分类准确率：

~~~text
accuracy = (TP + TN) / (TP + TN + FP + FN)
~~~

在科研工作流中更常用的对象是：

- hard gate：关键条件是否满足；
- artifact correctness：表格、图、manifest 是否正确；
- method compliance：设计和参数是否遵守 Spec；
- evidence/provenance：结果能否追溯到输入、工具、版本和参数；
- claim calibration：结论是否超过证据边界；
- cost/latency/reliability：是否在实际预算内稳定完成。

这些维度不应过早压成一个总分。总分会把一个致命科学错误用其他格式分抵消，产生 false pass。

## 2. 从静态模型到 LLM，再到 Agent

### 2.1 LLM 仍可看成条件分布

对于文本生成，模型近似学习：

~~~text
p_theta(y | x) = Π_t p_theta(y_t | y_<t, x)
~~~

传统 NLP 可以用 exact match、F1、BLEU、困惑度等指标；但开放式科研答案往往不存在唯一字符串，因此需要结构化输出、程序检查、参考 artifact 或人工 rubric。

### 2.2 Agent 是一个序列决策系统

把 Agent 写成策略更准确：

~~~text
s_t     当前状态：任务、文件、历史轨迹、工具返回值
c       外部上下文：Skill、Spec、工具说明、预算
a_t     动作：调用工具、写文件、运行命令、询问用户、停止
T       环境转移：执行动作后产生新状态
tau     轨迹 = (s_0, a_0, s_1, ..., s_T)
pi_theta(a_t | s_t, c)   Agent 策略
V(tau, input, contract)  独立 verifier
~~~

评测的对象至少有三层：

1. **动作层**：是否选对工具、参数、输入文件和下一步。
2. **状态/Artifact 层**：是否生成正确的中间表、图、日志、manifest。
3. **Claim 层**：最终解释是否与 evidence 一致、是否合理拒绝过度结论。

Agent 的随机性来自模型采样、工具失败、文件状态、超时和路径选择。故同一 case 要重复运行；单次成功不能证明可靠性。

### 2.3 Skill 和 Spec 是“外部处理变量”

在你的实验中，模型权重应尽量固定；Skill/Spec 是外部处理：

~~~text
潜在基线能力 + treatment(Skill/Spec) + 环境
→ Agent trajectory
→ scientific artifact
→ verifier/human score
~~~

这与 A/B 实验或消融实验更接近，而不是训练一个监督分类器。Skill 是程序性知识包，Spec 是问题、约束、计划、任务、证据和 claim 边界的合同；两者会改变策略的输入，却不应改变真值评测器。

## 3. 数据集不是一个 JSONL，而是一个可测量的 case package

每个 Bio case 最少需要：

~~~text
case/
├── task.md                 # 人类可理解的研究目标与输出合同
├── data/                   # 固定输入、metadata、reference/database snapshot
├── environment/            # 容器、工具版本、资源预算
├── oracle/                 # 证明问题可解的参考解；Agent 不可见
├── verifier/               # hidden deterministic checks；Agent 不可见
├── rubric/                 # 人工盲评维度和例证
├── splits/                 # dev / validation / frozen holdout
└── manifest.json           # 版本、hash、seed、许可和 provenance
~~~

### 3.1 oracle 与 verifier 的底层区别

- **oracle/reference**：回答“至少有一条可信解法，而且参考结果是什么”。
- **verifier**：回答“这个候选输出是否满足科学合同”。它必须独立于 Agent 的实现，不能只比较一份脚本或一串文本。

若有多种正确做法，verifier 应比较可观测科学性质和不变量，而不是要求完全复刻 reference code。oracle 证明可解性，verifier 才是最终测量仪器。

### 3.2 为什么必须有 negative cases

没有故意错误输入/输出，评测器只能证明“会接受正确答案”，不能证明“会拒绝错误答案”。每个 case 至少应加入：

- 组别标签交换或 contrast 反向；
- p-value 与 adjusted p-value 混用；
- log2FC 符号或阈值错误；
- gene ID 重复、NA、物种不匹配；
- KEGG universe 缺失；
- 图和表不一致；
- 无信号数据却强行给出显著机制；
- 上游失败仍继续生成 release claim。

## 4. 外部项目各自解决哪一层

| 项目 | 真正解决的问题 | 能否替代 Bio-Spec scientific verifier |
|---|---|---|
| [BixBench](https://arxiv.org/abs/2503.00096) | 真实计算生物学任务和开放问题来源；原论文报告超过 50 个场景、近 300 个开放问题 | 不能直接替代；需要把开放答案转成结构化 artifact、oracle 和 hidden verifier |
| [BixBench3](https://arxiv.org/abs/2608.25286) | 研究规模生物信息任务，按 published artifacts 做程序化评分；20 tasks、138 artifacts | 是最接近的外部设计参考，但它主要测执行结果，不测 Spec/Skill 因果效应，也不等于独立生物学验证 |
| [SkillsBench](https://www.skillsbench.ai/skillsbench.pdf) | 把 Skill 当成一等处理变量，no-skill/curated/self-generated paired evaluation | 是你的 Skill 对照协议来源，不是 Spec Kit benchmark，也不是 KEGG/DE 真值库 |
| [SpecBench](https://github.com/WecoAI/SpecBench) | Spec-to-code 的 validation tests 与 hidden held-out tests，观察 reward-hacking gap | 可借鉴隐藏测试和反投机机制，不能替代科研 verifier |
| [Inspect AI](https://inspect.aisi.org.uk/tasks.html) | Dataset + Solver + Scorer + Sandbox + eval log 的运行抽象 | 可作 runner 参考；科学真值仍由你的 scorer 定义 |
| [HELM](https://crfm.stanford.edu/helm/latest/) | 多指标、透明、可比较的模型评测组织方式 | 可借鉴报告结构，不提供你的生物学标签 |
| [Langfuse Scores](https://langfuse.com/docs/evaluation/scores/overview) | 把 code、human、LLM judge、用户反馈统一存为 score，并挂到 trace/observation/dataset run | 是评分账本和实验观测层，不定义 scientific truth |
| [LangSmith evaluation](https://docs.langchain.com/langsmith/evaluation-concepts) | dataset example、reference output、experiment、trace 的版本比较 | 可比较不同应用版本，仍需你的 verifier |
| [Ragas metrics](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/) | faithfulness、context、tool-call、agent-goal 等通用辅助指标 | 可作辅助诊断，不能决定 DEG/KEGG 是否正确 |
| [SkillOpt](https://github.com/microsoft/SkillOpt) | 用 rollout 反馈对 SKILL.md 做有界 add/delete/replace，并以验证门接受版本 | 最接近你的 Skill 自动改写需求；它不定义科研真值 |
| [DSPy](https://arxiv.org/abs/2310.03714) | 把 LLM pipeline 表达为可优化模块图，按 metric 编译/选择提示与示例 | 适合模块化 pipeline；需要外部科研 metric |
| [GEPA](https://arxiv.org/abs/2507.19457) | 从轨迹和自然语言反思提取规则，搜索 prompt 更新和 Pareto 候选 | 适合少量 rollout 的文本演化；需要冻结 holdout 防过拟合 |
| RagaAI Catalyst / aevyra-reflex | 评测、追踪或提示词迭代的工程工具 | 这里把你说的“RZ AI/RZ Reflex”按功能映射到这类项目；名称需以你手里的确切链接再核对，不能把宣传结果当成科研证据 |

一个重要的版本陷阱：SkillsBench 论文的摘要写 86 个任务，而正文评分使用固定分母 84；官方 [v1.1 release](https://github.com/benchflow-ai/skillsbench/releases/tag/v1.1) 又固定了 87 个 native task.md 任务。你自己的 benchmark 必须冻结版本、manifest 和每个 case 的 hash，不能只写“SkillsBench 数据集”。

## 5. SkillsBench 的评分原理，及它对你的真正启发

SkillsBench 的关键不是“有一个分数”，而是：

1. 每个任务有 instruction、container environment、oracle 和 deterministic verifier。
2. 同一任务在 no Skills、curated Skills、self-generated Skills 条件下运行。
3. verifier 输出 binary pass/fail，避免把 LLM judge 的随机性当成主真值。
4. 每个 task 多次运行，先求 task-level 平均，再对任务做 macro average。
5. 同时报告绝对提升和 normalized gain，并分析负向 delta 与失败类型。

其核心计算可以写成：

~~~text
y[t,r,c] ∈ {0,1}
p[t,c] = mean_r y[t,r,c]
P[c] = mean_t p[t,c]
Delta = P[with-skill] - P[no-skill]
g = Delta / (1 - P[no-skill])
~~~

其中 t 是任务，r 是重复运行，c 是条件。必须先在任务内平均，再在任务之间平均，不能把大任务的文件数或轨迹数当权重。

g 只能作辅助指标：基线接近 1 时会出现 ceiling effect。主报告应优先使用绝对差值和任务级置信区间；SkillsBench 采用 1,000 次 percentile bootstrap，并对一部分任务做 10-run 稳定性检查。你的 MVP 可先采用 task-cluster bootstrap，随后再增加更复杂模型。

## 6. Bio-Spec 的正式 2×2 实验

四个条件必须使用同一模型、harness、输入、容器、工具版本、时间/令牌预算、输出 schema、oracle、verifier 和重复策略，唯一改变是否提供 Spec/Skill：

~~~text
C00 = no-spec    + no-skill
C01 = no-spec    + with-skill
C10 = with-spec  + no-skill
C11 = with-spec  + with-skill
~~~

主效应和交互效应：

~~~text
Skill effect without Spec = C01 - C00
Spec effect without Skill = C10 - C00
Skill effect with Spec    = C11 - C10
Spec effect with Skill    = C11 - C01
Interaction               = C11 - C10 - C01 + C00
~~~

解释：

- C01-C00 是 Skill 的边际收益，不把 Spec 的帮助混进来。
- C10-C00 是 Spec 合同/澄清/计划本身的收益，不把 Skill 的程序知识混进来。
- 交互项为正表示 Spec 使 Skill 更可用，或 Skill 使 Spec 更可执行；为负表示两者冲突、上下文过长或流程约束互相覆盖。
- no-spec 不能因缺少 spec.md 自动把 scientific score 判零。它只在 Spec-compliance 轨道上记为“未提供/未适用”；科学结果仍由同一个 verifier 判断。

## 7. 你的实际评分算法

### 7.1 首先输出一个 score vector，而非一个总分

每次 run 记录：

~~~text
scientific_pass       关键科学不变量是否全部满足（主硬门）
artifact_score        表、图、JSON、manifest 的局部正确率
method_compliance     设计、contrast、过滤、归一化和数据库版本是否符合合同
evidence_provenance   输入 hash、工具版本、参数、日志和中间结果是否可追溯
claim_boundary        是否把 descriptive 结果写成过强机制/因果结论
spec_compliance       Spec 条件下的 FR/SC→Task→Evidence 覆盖
reliability           多次运行成功率、重跑一致性、fail-closed
cost_latency          token、时间、工具调用、计算资源
failure_taxonomy      clarification、execution、method、artifact、claim、timeout 等
~~~

scientific_pass=0 的致命错误不能被其他维度的高分抵消。若为了排序必须计算 utility，应事先冻结权重，并始终同时发布完整 score vector。

### 7.2 task-level 宏平均和不确定性

对每个任务 t 和条件 c：

~~~text
y[t,r,c] = verifier 输出的 0/1
p[t,c] = 所有重复的平均
P[c] = 所有任务 p[t,c] 的平均
~~~

统计建议：

- 主要结果：paired task-level absolute delta；
- 95% CI：按 task 聚类的 bootstrap，重采样任务而不是单独打散每条轨迹；
- 条件比较：paired permutation 或 task-level bootstrap；
- task 数足够后，再用 hierarchical logistic model 分解任务难度和模型/条件效应；
- 小规模 MVP 只声明“本 case set 上的可行性和回归信号”，不声称外部泛化。

可靠性可以附加报告：

~~~text
pass@k = 1 - (1 - p)^k   # k 次中至少成功一次
pass^k = p^k             # k 次全部成功
~~~

它们不能互相替代：科研发布更关心稳定的 pass^k 和 fail-closed，而探索性使用可能关心 pass@k。

### 7.3 Skill/Spec 版本前后比较

对于候选 Skill 或 Spec 文本 h：

~~~text
S(h; D_dev)       在 dev/validation case 上的 task-level score
h' = bounded_edit(h, scored_trajectories)
accept h' 仅当：
  S(h'; D_val) > S(h; D_val) + delta
  且所有 scientific hard gate 不退化
  且成本/上下文长度不超过预算
最后只在冻结 D_holdout 上做一次最终比较
~~~

这就是 SkillOpt 思路的底层原理：把 SKILL.md 当作冻结模型外部的可训练状态，用有界文本编辑、拒绝缓冲和验证门减少自我修改的漂移。GEPA 则从轨迹反思中提炼自然语言规则，DSPy 更偏向模块化 pipeline 的 metric-driven 编译。三者都依赖同一个前提：**没有可信 verifier，优化器只是在优化评分器的漏洞。**

候选版本的接受规则应包含“无回归”：

~~~text
accept = validation_gain > delta
         AND critical_pass_new >= critical_pass_old
         AND holdout_not_touched
~~~

不要让优化器看到最终 holdout 的详细失败原因；否则它会把 holdout 变成训练集。

## 8. MDS/DMM → Volcano → KEGG 的具体 case

这是最适合你的第一条科研 vertical slice，因为每一步都有可检查的不变量：

~~~text
counts + sample metadata
→ group/contrast/replicate validation
→ filtering + normalization
→ MDS coordinates / plot data
→ DEG table (log2FC, pvalue, padj/FDR)
→ volcano data / image
→ gene-ID mapping + species + universe
→ KEGG/GO enrichment table / plot
→ evidence graph + bounded claim
~~~

verifier 不应只检查文件存在，而应检查：

- metadata 的样本、组别和 contrast 与 Spec 一致；
- duplicate、NA、ID 类型、物种和数据库版本明确；
- DEG 表的列、数值范围、log2FC 符号、p/FDR 阈值和排序正确；
- volcano 点的颜色/阈值与 DEG 表相同；
- MDS 图的坐标来自同一输入和同一参数，而非静态占位图；
- KEGG 输入 ID、背景 universe、物种、数据库版本和多重检验方法齐全；
- 图、表、manifest 和最终 claim 可以沿 artifact DAG 追溯；
- 无信号、缺 universe、物种错配或上游失败时，Agent 必须 abstain/block，而不是生成漂亮但不受支持的机制故事。

这个 verifier 需要接受数值容差和等价实现，但要拒绝“只改文件名、只生成图片、把 p-value 当 FDR、把 overlap 当机制”等投机路径。

## 9. 人工评测在整套系统中的位置

人工不是用来替代所有自动化，而是用来测量程序检查难以定义的构念，并校准自动评分器。

建议的盲评对象：

- 运行条件、模型、Skill/Spec 版本对评审者隐藏；
- 全部 borderline、machine/human discordant、critical claim 输出必评；
- 其余输出按条件分层随机抽样；
- 至少两名独立评审，记录分歧和 adjudication；
- 报告 Cohen’s kappa、Krippendorff’s alpha 或加权一致性，不只报平均分。

人工 rubric 维度：

1. 科学方法是否合理；
2. 结果解释是否由 artifact 支持；
3. claim 是否越过证据边界；
4. 是否在信息不足时澄清、阻塞或拒绝；
5. provenance 是否足以复核；
6. 输出是否清楚、可操作、可审计。

LLM-as-judge 可以用于 triage、错误分类和低成本预标注，但必须用人工盲评校准；它不应成为 DEG、KEGG 或生物学机制的唯一真值。

## 10. 对 Langfuse、LangSmith、Ragas、Phoenix 的准确定位

这些系统的共同底层原理是“记录一次运行的可观测状态，再把一个或多个 evaluator 产生的 score 绑定到 trace/span/dataset example/experiment”。例如 Langfuse 的 score 可以是 numeric、categorical、boolean 或 text，并可来自 code evaluator、LLM judge 或人工标注；LangSmith 将 dataset example、reference output、experiment 和 trace 做版本比较；Ragas 提供工具调用、faithfulness、agent goal 等通用 metric。

它们能做：

- 保存 run_id、条件、模型、Skill/Spec hash、输入输出和轨迹；
- 对同一 dataset 跑多个 experiment；
- 展示前后版本、分组、成本和失败类型；
- 调用你的 Python verifier 并保存结果；
- 管理人工 annotation queue。

它们不能自动做：

- 决定什么是正确的 DE/KEGG scientific claim；
- 判断一个图是否真正由正确数据产生；
- 证明独立队列复现或实验验证；
- 替你设计 C00/C01/C10/C11 的因果对照；
- 防止你把 test/holdout 反复用于提示词优化。

所以它们是 **ledger/observability/evaluator orchestration**，不是 benchmark truth。第一版可以不依赖它们：先用本地 JSONL/SQLite + Python verifier；稳定后再把同一 score vector 接入 Langfuse 或 Inspect。

## 11. 目前项目的硬判断

已经有：

- MultiQC 和 Evidence Closure Kernel 的局部技术 vertical slice；
- 上游脚本测试通过；
- Skill staging/discovery hash 对齐；
- 官方 Spec Kit 兼容方向、研究型 preset/extension/workflow 候选；
- 2×2 架构、三类 Bundle 和 evidence/claim 边界的设计记录。

还没有：

- 可运行的 MDS/DMM→volcano→KEGG case package；
- hidden oracle 和独立 deterministic artifact verifier；
- C00/C01/C10/C11 的实际 Agent 重复运行；
- 人工盲评数据和评分者一致性；
- Skill/Spec 前后效果的置信区间与无回归门；
- E2 独立队列复现或 E3 正交/实验验证；
- 完整的 Spec Kit component materialization；
- “完全无人值守自驾”证据。

因此当前正式状态应写成：

~~~text
technical deterministic tests: executed tests pass
scientific efficacy of Skill: not evaluated
scientific efficacy of Spec: not evaluated
Skill × Spec interaction: not evaluated
full autonomous operation: not established
release-ready scientific claim: no
~~~

## 12. 现在最应该做的顺序

### 阶段 A：先做一个科学真值闭环

只选一个小而真实的 MDS/DMM→volcano→KEGG case。完成输入 snapshot、metadata、参数、参考 artifact、oracle、hidden verifier、negative cases 和人工 rubric。此阶段不追求接入所有平台。

### 阶段 B：跑四个条件

固定模型、harness、容器、预算和 verifier，跑 C00/C01/C10/C11；每个 task 至少多次，保存 immutable run_id 和完整 provenance。先回答“Skill 和 Spec 是否真的改变科学结果”。

### 阶段 C：再接评测平台

把本地 verifier 的 score vector 和 trace 接入 Inspect 或 Langfuse/LangSmith。平台只负责运行、记录、比较和人工队列，不得把领域判断移交给平台默认 metric。

### 阶段 D：最后做 Skill/Spec 优化

在 dev/validation 上采用 SkillOpt-like bounded edit；如果要试更通用的 prompt/program 搜索，再比较 GEPA、DSPy 或 Reflex。holdout 永远只作冻结终评；每个候选版本都必须经过 hard-gate 和无回归检查。

### 阶段 E：扩大 case set 和验证层

加入不同数据规模、无信号、批次效应、物种/ID 冲突和独立数据；完成 E2，再讨论 E3。不要用更多工具名称代替更多可辨识的科学 case。

## 13. 关键项目和本地入口

### 本地

- [当前技术测试与边界](FINAL-TEST-SCORE-CONCLUSION.md)
- [总参考与历史决策](BIO-SPEC-KIT-REFERENCE.md)
- [科研 MVP 路线](SPEC-RESEARCH-MVP-ROADMAP.md)
- [评测矩阵](spec-mvp/docs/evaluation-matrix.md)
- [MultiQC vertical slice Spec](specs/002-multiqc-vertical-slice/spec.md)
- [Shared integration vertical slice Spec](specs/003-shared-integration-vertical-slice/spec.md)
- [Bio-Spec fixture 设计骨架](specs/004-spec-research-core/spec-fixture-design/README.md)
- [BixBench/SkillsBench 适配说明](specs/004-spec-research-core/spec-fixture-design/reference-package/benchmark-source-map.md)
- [SkillsBench 对照协议](specs/004-spec-research-core/spec-fixture-design/reference-package/skillsbench-reference.md)

### 外部

- [SkillsBench 论文](https://www.skillsbench.ai/skillsbench.pdf) · [v1.1 task.md release](https://github.com/benchflow-ai/skillsbench/releases/tag/v1.1)
- [BixBench 论文](https://arxiv.org/abs/2503.00096) · [BixBench3 论文](https://arxiv.org/abs/2608.25286)
- [SpecBench](https://github.com/WecoAI/SpecBench)
- [Inspect AI tasks](https://inspect.aisi.org.uk/tasks.html) · [Inspect scorers](https://inspect.aisi.org.uk/standard-scorers.html)
- [HELM](https://crfm.stanford.edu/helm/latest/)
- [Langfuse scores](https://langfuse.com/docs/evaluation/scores/overview) · [Langfuse code evaluators](https://langfuse.com/docs/evaluation/evaluation-methods/code-evaluators)
- [LangSmith evaluation concepts](https://docs.langchain.com/langsmith/evaluation-concepts)
- [Ragas metrics](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/)
- [SkillOpt paper](https://arxiv.org/abs/2605.23904) · [SkillOpt repo](https://github.com/microsoft/SkillOpt)
- [DSPy paper](https://arxiv.org/abs/2310.03714) · [GEPA paper](https://arxiv.org/abs/2507.19457)
- [scikit-learn cross-validation](https://scikit-learn.org/stable/modules/cross_validation.html)

## 14. 最终一句话

**你的 MVP 不是“把更多 Skills、harness 和评测平台装起来”，而是先建立一个能拒绝错误科学结果的固定 case + verifier，然后用同一测量仪器完成 Spec/Skill 2×2 对照和人工盲评。** 评分算法的核心是 task-level paired delta、硬科学门、重复运行和冻结 holdout；Langfuse/LangSmith/Phoenix 只负责把这些结果记录和比较起来，SkillOpt/GEPA/DSPy 才负责在有可信评分之后搜索更好的 SKILL.md/Spec。
