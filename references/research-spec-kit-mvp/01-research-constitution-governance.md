# 01 Research Constitution 与科研治理

> 用途：Research Spec Kit 的通用科研治理参考稿。当前仅作为设计输入，不接入任何运行链路。

## 结论

`Research Constitution` 不应只是价值宣言，而应成为所有科研项目都必须遵守的治理契约：

> 什么可以被称为事实，什么可以被称为证据，什么情况下可以发布结论，以及 Agent 在不确定时必须如何停下来。

通用层负责跨领域不变量；`Bio Profile` 只负责生物信息学特有的输入、样本、参考、QC 和方法约束。Bio Profile 可以收紧通用规则，但不能放松通用科研底线。

## 一、通用科研不变量

### R-01 科研问题优先于方法

每个研究单元必须显式定义：

```yaml
question:
  question_id: Q-001
  primary_question: ""
  estimand_or_target: ""
  population_or_scope: ""
  unit_of_analysis: ""
  outcome_or_endpoint: ""
  exclusions: []
  analysis_mode: exploratory | confirmatory | descriptive | post_hoc
```

缺少主要问题、estimand、范围或主要终点时，状态必须为 `NEEDS_CLARIFICATION`，相关阶段为 `BLOCKED`。工具选择不能反向定义科学问题。

### R-02 不捏造、不静默补齐

Agent 不得：

- 编造结果、引用、样本量、方法细节或软件版本；
- 将未知信息写成事实；
- 将搜索摘要、模型记忆或自动总结当作已核验证据；
- 删除、隐藏或弱化不利结果；
- 把相关性写成因果性；
- 把“不显著”写成“等效”或“无影响”。

信息必须显式标记为：

```text
KNOWN / UNKNOWN / ASSUMPTION / CONFLICT / UNVERIFIED / N/A
```

### R-03 Claim 必须有证据链

重要 claim 至少应具有：

```yaml
claim:
  claim_id: C-001
  text: ""
  claim_type: observed | derived | interpretive | associative | predictive | causal
  scope: ""
  evidence_ids: []
  observable_ids: []
  validation_ids: []
  status: proposed | supported | not_supported | inconclusive | exploratory_only
  limitations: []
  verified_by: null
  verified_at: null
```

没有 `evidence_ids` 的 claim 不能进入发布状态；没有 `observable_ids` 或 `validation_ids` 的研究性 claim 只能标记为 `unsupported` 或 `untested`。

### R-04 证据等级约束表述强度

建议使用通用五级证据等级：

| 等级 | 含义 | 允许的最低解释强度 |
|---|---|---|
| E0 | 无证据或纯想法 | 不能作为事实发布 |
| E1 | 线索、摘要或未核验外部信息 | 仅用于发现待查证方向 |
| E2 | 有输入、代码、参数、日志和输出的计算证据 | 内部工作证据 |
| E3 | 来源、输入和 provenance 已人工核验 | 受范围限制的研究报告 claim |
| E4 | 独立重复、正交方法或多源一致 | 更高置信度，但不自动等于因果或普适 |

证据等级未知时按 E0 处理。claim 的语言强度不得超过证据等级与研究设计共同允许的范围。

### R-05 探索与验证分离

每个分析必须记录：

```yaml
analysis_mode: exploratory | confirmatory | validation | post_hoc
registered_before_execution: true | false | unknown
data_used_for_discovery: []
data_reserved_for_validation: []
post_hoc_changes: []
```

探索性信号不得自动升级为确认性、预测性或因果性结论。使用发现数据选特征、调参或选模型后，不得再把同一数据称为独立验证集。

### R-06 负结果、失败和未执行结果必须保留

统一区分：

```text
negative       分析完成但未观察到预期效应
null           结果接近零，但仍需结合精度解释
inconclusive   证据不足、功效不足或冲突未解决
failed         技术、输入、QC 或模型失败
not_run        未执行
not_applicable 设计上不适用
```

技术失败不等于生物学阴性；低功效不等于无效应；未运行不等于未发现差异。

### R-07 人工复核负责科学判断

Agent 可以整理证据、生成草稿、运行自动检查和提出候选解释，但不能替代责任研究者。以下节点必须人工复核：

- 研究问题、estimand 与设计；
- 样本身份、关键排除规则和 QC 例外；
- 主要统计模型与对照；
- claim 与 evidence 的对应关系；
- 负结果、异常和限制；
- 最终发布、外部写入和撤回。

没有人工批准时，最高状态为 `READY_FOR_REVIEW`，不得为 `RELEASED`。

### R-08 审计与不可覆盖

输入、方法、参数、环境、结果、claim、人工决定和例外都必须版本化。任何重跑、改阈值、改模型或改解释都产生新版本或新 run，不能覆盖历史证据。

## 二、NEEDS CLARIFICATION 与 Assumptions

### Clarification 记录

```yaml
clarification:
  id: NC-001
  question: ""
  why_it_matters: ""
  affected_artifacts: []
  options: []
  recommended_option: null
  owner: human | agent
  status: open | resolved | rejected
  resolution: ""
  resolved_by: null
  resolved_at: null
```

以下问题必须阻塞：样本或分组不明、主要 endpoint 不明、比较关系不明、方法前置条件不明、数据权限/伦理不明、证据来源冲突、结论强度超过证据范围。

### Assumption 记录

```yaml
assumption:
  id: A-001
  statement: ""
  basis: user_input | source_document | agent_inference
  confidence: high | medium | low
  impact_if_wrong: high | medium | low
  affected_artifacts: []
  verification_method: ""
  owner: human | agent
  status: proposed | accepted | rejected | verified | expired
  accepted_by: null
```

Agent 推断的内容只能是 `proposed`，不能写入 `KNOWN`。若会改变 estimand、样本排除、统计模型、参考版本或结论范围，未被人工接受前必须阻塞。

### 最小澄清原则

```text
不影响当前节点 → 记录 UNKNOWN，继续
影响当前节点但不影响后续设计 → 局部阻塞
影响设计、执行或结论 → 全局阻塞
存在冲突 → CONFLICT + ESCALATE，不由 Agent 自行裁决
```

## 三、质量门与状态

```text
INTAKE
  → DESIGN
  → EXECUTION
  → RESULT_VALIDATION
  → INTERPRETATION
  → RELEASE
```

最低质量门：

1. Intake：问题、对象、输入、权限和范围明确；
2. Design：estimand、比较、设计、统计计划和方法适用性明确；
3. Execution：输入、版本、参数、环境和日志可追溯；
4. Result：输出、QC、统计诊断、异常和失败记录完整；
5. Interpretation：claim 与证据绑定，解释不超过范围；
6. Release：provenance、负结果、审计记录和人工审批齐全。

建议状态集合：

```text
DRAFT
NEEDS_CLARIFICATION
READY_FOR_DESIGN
READY_FOR_EXECUTION
RUNNING
RESULTS_UNVERIFIED
READY_FOR_REVIEW
APPROVED_WITH_CONDITIONS
RELEASED
RECALLED
FAILED_RETRYABLE
FAILED_TERMINAL
ESCALATED
ABORTED
```

## 四、Research Constitution 与 Bio Profile 的边界

### Research Constitution 负责

- 科研诚信和 claim checking；
- 证据等级和表述强度；
- unknown、conflict、assumption 管理；
- 探索/验证分离；
- 负结果、失败和撤回；
- 验证门、人工责任和 waiver；
- provenance、审计、版本和不可覆盖；
- 研究范围、结论范围与状态转移规则。

### Bio Profile 负责

- FASTQ/BAM/CRAM/VCF/H5AD 等数据契约；
- 样本表、subject、condition、batch、replicate 和 assay 元数据；
- reference genome、annotation、gene set 和版本；
- mapping rate、测序深度、细胞比例等生信 QC；
- DESeq2、Scanpy、Nextflow、GSEA 等领域方法；
- 领域特有的阈值、输入输出和验证方式。

优先级建议：

```text
法律/伦理/数据许可
  > Research Constitution
  > Bio Profile
  > Project Constitution
  > Research Spec / Plan / Tasks
  > Agent convention
```

## 五、waiver 与不可豁免项

```yaml
waiver:
  waiver_id: W-001
  gate_id: GATE-001
  waived_requirement: ""
  reason: ""
  risk_assessment: ""
  affected_claims: []
  compensating_controls: []
  approved_by: ""
  approved_at: ""
  expires_at: ""
  follow_up_action: ""
```

`waived` 不是 `pass`。以下原则不能用 waiver 绕过：禁止捏造、claim-evidence 绑定、关键 provenance、负结果记录、人工最终责任、伦理/隐私/数据许可和审计记录。

## 六、MVP 取舍

完整 Constitution 可以很大，但 MVP 只需要先实现 6 个共性接口：

```text
ResearchQuestion
Evidence
Observable
Validation
Claim
Gate / State
```

先让一个真实研究问题能经过“问题 → 观测 → 验证 → claim”闭环，再逐步补充证据等级、人工审批、负结果、waiver 和完整审计。

