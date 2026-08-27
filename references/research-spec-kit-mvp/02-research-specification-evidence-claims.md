# 02 Research Specification、Evidence 与 Scientific Claim

> 用途：定义“研究问题—证据—观测—验证—科学主张”的数据结构。当前仅作为设计输入，不接入任何运行链路。

## 结论

现有 `spec.md` 可以保留为研究规格主文档，但必须从“要做哪些分析”扩展为：

```text
Research Question
  → Hypothesis
  → Observable
  → Validation
  → Scientific Claim
```

文献证据建立背景和先验边界；本研究生成的观测回答当前问题；验证决定是否允许升级 claim。三者不能混成一个引用列表。

## 一、Research Specification 最小字段

```yaml
research_spec:
  research_spec_id: RS-Q1-001
  version: 1
  status: draft | preregistered | running | concluded

  question:
    question_id: Q-001
    text: ""
    population: ""
    comparison: ""
    outcome: ""
    estimand: ""
    question_type: comparative | descriptive | causal | predictive

  established_facts: []
  unknowns: []
  knowledge_gaps: []
  objectives: []
  hypotheses: []
  assumptions: []

  scope:
    in_scope: []
    out_of_scope: []

  observable_plan: []
  validation_plan: []
  decision_rules: []
  success_criteria: []
  failure_criteria: []
  open_issues: []
```

规则：

- `facts` 是研究开始前已经有来源支持的事实，不是运行结果；
- `unknowns` 是尚未知道的内容；
- `gaps` 解释为什么已有事实不足以回答问题；
- `hypotheses` 必须允许被数据反驳；
- 成功、失败和不确定的判定应在查看结果前固定。

## 二、Evidence / Literature artifact

建议将 evidence 作为独立 artifact，而不是散落在 spec、报告或聊天记录里：

```text
research/
├── specification.yaml
├── evidence/
│   ├── source-manifest.yaml
│   ├── evidence-records.yaml
│   ├── evidence-gaps.yaml
│   └── conflict-log.yaml
├── claims/
│   ├── claim-registry.yaml
│   ├── observable-registry.yaml
│   └── validation-registry.yaml
└── analyses/
    ├── analysis-contracts.yaml
    └── result-index.yaml
```

### Source record

```yaml
source:
  source_id: E-SRC-001
  source_type: literature_primary | dataset | guideline | method | internal
  source_uri: "DOI / PMID / accession / path"
  bibliographic_identity: ""
  version_or_access_date: ""
  content_hash_or_snapshot: null
  locator: "page / figure / table / field / line"
  verification_status: unverified | human_verified | disputed
  verified_by: null
  verified_at: null
```

不能把搜索摘要、二手引用列表或模型记忆当作已验证证据。

### Evidence record

```yaml
evidence:
  evidence_id: E-001
  source_ref: E-SRC-001
  evidence_type: literature | dataset_metadata | method_validation | internal_observation | negative
  proposition: "该证据实际支持的明确命题"
  polarity: supports | contradicts | qualifies | neutral | unresolved
  population_or_system: ""
  design_and_limitations: []
  locator: ""
  verification_status: unverified | verified | disputed
  supports: []
  contradicts: []
  does_not_establish: []
```

一条证据只能支持边界清晰的命题。引用支持的只是该命题，不是整篇文献的所有可能解释。

### Evidence gap 与冲突

```yaml
evidence_gap:
  gap_id: G-EV-001
  related_questions: [Q-001]
  missing_proposition: ""
  severity: blocking | material | minor
  consequence: ""
  closure_plan: ""
  status: open | partially_resolved | closed
```

正面证据、反面证据、间接证据和缺失证据要显式并列。文献冲突本身是研究信息，不应静默消除。

## 三、Observable、Validation 与 Claim

### Observable

Observable 必须可以从明确输入中直接计算或核验：

```yaml
observable:
  observable_id: O-001
  name: ""
  definition: ""
  unit: ""
  population: ""
  source_artifacts: []
  derivation_method: ""
  uncertainty: ""
  data_version: ""
  run_id: null
```

不能把“希望看到的生物学意义”直接当作 observable；必须先定义可测量变量、单位、分母、缺失值处理和派生规则。

### Validation

```yaml
validation:
  validation_id: V-001
  target_ids: [O-001]
  validation_type: internal | external | orthogonal | holdout | replication | sensitivity
  independent_unit: ""
  preregistered: true | false
  method: ""
  acceptance_criteria: []
  failure_criteria: []
  result_status: pending | passed | failed | inconclusive
  evidence_ids: []
```

“同一数据、同一模型、同一参数的重复运行”不能自动称为独立验证。

### Scientific Claim

```yaml
claim:
  claim_id: C-001
  question_ref: Q-001
  statement: ""
  claim_type: observed | derived | associative | predictive | causal
  scope: ""
  observable_refs: []
  validation_refs: []
  evidence_refs: []
  decision_rule_ref: DR-001
  supports: []
  does_not_support: []
  limitations: []
  status: untested | supported | not_supported | inconclusive | exploratory_only
```

推荐状态：

```text
supported       预先定义规则满足，且没有阻断性问题
not_supported   结果未满足规则或方向与假设相反
inconclusive    数据不足、功效不足或证据冲突未解决
exploratory_only 有信号但未达到确认/验证标准
not_evaluable   输入、QC 或 provenance 失败，不能评价
```

默认结论措辞应为“数据支持”“数据不支持”“结果不足以判断”“观察到探索性信号”，避免自动生成“证明了”。

## 四、ID 与可追溯链

建议 ID 永不复用：

| 对象 | 前缀 | 示例 |
|---|---|---|
| Research Spec | RS | `RS-Q1-001` |
| Question | Q | `Q-001` |
| Fact / Unknown | F / U | `F-001`, `U-001` |
| Gap | G | `G-EV-001` |
| Hypothesis | H | `H-001` |
| Assumption | ASM | `ASM-001` |
| Source / Evidence | E-SRC / E | `E-SRC-001`, `E-001` |
| Observable | O | `O-001` |
| Validation | V | `V-001` |
| Decision Rule | DR | `DR-001` |
| Claim | C | `C-Q1-001` |
| Analysis Run | RUN | `RUN-20260827-001` |

核心链：

```text
Q-001
  → H-001
  → O-001/O-002
  → V-001/V-002
  → DR-001
  → C-Q1-001
  → E-001 + internal RUN evidence
```

若研究问题或命题发生实质变化，应新建 ID，并用 `supersedes` 或 `derived_from` 记录关系。

## 五、Q1 最小闭环示例

问题：“PA 与 LUAD 是否存在共同转录响应？”不能直接使用，必须先定义“共同”：

```yaml
research_spec_id: RS-Q1-001
question:
  question_id: Q-001
  text: "在预先定义的 PA 与 LUAD 队列中，是否存在方向一致且超过预设效应阈值的共同转录响应？"
  estimand: "方向一致且经独立验证的响应基因比例及其不确定性"

hypotheses:
  - id: H-001
    statement: "共同响应超过预设零假设范围"
    falsifier: "重叠比例不超过零假设，或独立队列方向不一致"

observables:
  - id: O-001
    name: "PA gene-level effect"
    output: [gene_id, log2fc, standard_error, p_value, fdr]
  - id: O-002
    name: "LUAD gene-level effect"
    output: [gene_id, log2fc, standard_error, p_value, fdr]
  - id: O-003
    name: "cross-disease concordance"
    derived_from: [O-001, O-002]
    metrics: [sign_concordance, overlap_count, overlap_fraction, confidence_interval]

decision_rule:
  id: DR-001
  supported_if:
    - "QC 通过"
    - "预定义效应/FDR/背景集合标准通过"
    - "独立验证方向一致"
    - "敏感性分析未显示由单一批次或组织差异驱动"
  not_supported_if:
    - "重叠低于预设阈值"
    - "验证方向冲突"
  inconclusive_if:
    - "独立验证缺失"
    - "功效不足或证据冲突未解决"

claim:
  id: C-Q1-001
  statement: "在指定样本、平台和分析范围内，PA 与 LUAD 存在共同转录响应。"
  observable_refs: [O-001, O-002, O-003]
  validation_refs: [V-001, V-002, V-003]
  does_not_support: ["共同病因", "因果机制", "临床疗效"]
  status: untested
```

如果主队列有信号但没有独立验证，结果只能是 `inconclusive` 或 `exploratory_only`，不能升级为稳健 claim。

## 六、MVP 取舍

第一版不必实现完整文献数据库或复杂知识图谱。只需能可靠保存并验证：

```text
一个 Question
一个 Hypothesis
至少一个 Observable
至少一个 Validation
一个 Decision Rule
一个 Claim
以及它们之间的 ID 引用关系
```

