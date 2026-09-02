# Data Model（04 Plan 支持产物）

**状态**：`PROPOSAL / NOT_RUNTIME`

本文定义本次改造工程要比较和连接的对象；它不是最终的 `node.contract.json`
schema，也不授权创建运行时文件。

## 1. 状态和证据类型

### 证据状态

`FACT`、`INFERENCE`、`PROPOSAL`、`UNKNOWN`。

### 字段状态

`present`（有）、`conditional`（条件）、`absent`（无）、`pending`（待核）、
`not_applicable`（不适用）、`not_verified`（未验证）。

### 静态能力与运行状态

`node.contract.json` 是静态能力契约，只描述组件的接口、方法边界、身份和
证据要求；它不得携带某一次运行的 `execution/scientific/release` 状态。
`run-status.schema.json` 是单次运行 envelope，独占 `status.execution`、
`status.scientific`、`status.release` 三个互相独立的字段；审阅记录可以用
`execution_status` 等人读标签映射到这三个字段。
任何一个运行态字段不能由另一个字段自动推断；运行 envelope 必须通过
`contract_ref` 和 `contract_schema_version` 绑定到静态能力契约。

## 2. Entity: SourceRecord

| 字段 | 类型 | 约束 |
|---|---|---|
| `source_id` | string | 稳定、唯一 |
| `source_kind` | enum | `user_intent/local_file/official_doc/external_repo/dataset` |
| `path_or_url` | string | 可回溯；外部路径标出不可移植性 |
| `source_role` | enum | `governance/audit_input/design_reference/technical_evidence/evaluation_reference` |
| `observed_at` | date-time/date | 动态事实必须有观察时间 |
| `version_or_revision` | string/null | 未知时为 null + `unknown_reason` |
| `hash` | string/null | 可取得时记录；不能伪造 |
| `evidence_status` | enum | FACT/INFERENCE/PROPOSAL/UNKNOWN |
| `allowed_claims` | array[string] | 只能支持列出的结论 |
| `prohibited_inferences` | array[string] | 例如“有 prose ≠ runtime verified” |

## 3. Entity: SkillComponent

```text
SkillComponent
├── component_id
├── parent_component_id (optional)
├── module_refs[] (facade only)
├── kind
├── source_refs[]
├── primary_stage / secondary_stages
├── scientific_purpose
├── estimand_or_observable
├── input_ports[]
├── preconditions[]
├── routes[]
├── output_ports[]
├── identity_policy
├── evidence_refs[]
├── hard_boundary
├── failure_policy
├── runtime_status
└── merge_decision
```

### SkillComponent 字段约束

| 字段 | 必须表达的内容 |
|---|---|
| `component_id` | 不因中文翻译、镜像或内部拆分而静默改名 |
| `kind` | `project-adapter/reference/module/subworkflow/router/facade` |
| `scientific_purpose` | 研究问题或观察对象，不只写“生成报告” |
| `estimand_or_observable` | 方法输出支持什么；不支持什么 |
| `input_ports` | 上游对象、shape、cardinality、channel、identity 和约束 |
| `preconditions` | 数据、元数据、参考、依赖和门禁 |
| `routes` | 方法/数据库/方向分支如何显式选择 |
| `output_ports` | primary、diagnostics、provenance、verdict、report 的语义 |
| `identity_policy` | sample/subject/branch/contrast/reference 如何传递和对齐 |
| `evidence_refs` | 示例、测试、verifier、版本、命令和来源 |
| `hard_boundary` | 明确不能由该组件宣称、替代或拥有的责任 |
| `failure_policy` | 错误码/状态、fail closed、恢复或人工决定 |
| `runtime_status` | verified/reference-only/incomplete/not-verified |
| `merge_decision` | 仅视图合并、编排、保留独立、缺失或待定 |

## 4. Entity: Port

| 字段 | 类型 | 说明 |
|---|---|---|
| `port_id` | string | public 稳定名称 |
| `direction` | enum | `input/output`；`upstream/downstream` 是图关系，不是端口方向 |
| `channel_semantics` | enum | `queue/value/stream/unknown` |
| `shape` | enum | `path/value/tuple/table/matrix/json/report` |
| `cardinality` | enum/string | one/one-or-more/many/optional |
| `tuple_fields` | array[string] | 例如 `meta,payload` |
| `artifact_type` | string | 例如 raw counts、DE table、tested universe |
| `identity_keys` | array[string] | 引用顶层 identity.key_definitions 中的稳定 join/trace keys |
| `constraints` | array[string] | 非空、唯一、整数、namespace 等 |
| `required` | boolean | 是否为必需端口 |
| `on_missing` | enum | fail_closed/warn/block/not_applicable |

`Port` 只描述接口可观察语义，不直接嵌入长篇算法正文或执行脚本。

### IdentityPolicy

每个静态 node contract 的 `identity.key_definitions` 必须为每个可传递身份键
声明以下最小语义：

| 字段 | 约束 |
|---|---|
| `key` | 稳定字段名；port 的 `identity_keys` 必须引用已定义的 key |
| `namespace` | key 的语义命名空间，例如 `fastqc.sample` 或 `sha256.artifact` |
| `scope` | `case/run/sample/subject/branch/contrast/reference/artifact/configuration/tool/custom` |
| `unique_within` | `case/run/artifact/component` 中的唯一性范围 |
| `required` | 是否是该身份定义的必需键；port 不得使用非 required 键 |
| `join_cardinality` | 组件边界的 `one-to-one/one-to-many/many-to-one/many-to-many/not-applicable` |
| `duplicate_policy` | `fail_closed/deduplicate_with_rule/preserve/not-applicable` |
| `unmatched_policy` | `fail_closed/drop_with_count/preserve_unmatched/not-applicable` |

`identity.transport` 描述 key 如何随 payload 传递，不能以文件名、行序或到达
顺序代替；重复和 unmatched 的行为必须显式记录。

### Provenance separation

静态 node contract 的 `provenance` 只声明来源和运行记录所需字段
（`run_record_schema` 与 `required_run_fields`），不得放入某次运行的输入 hash、
命令或环境占位文本。单次运行的 input/artifact manifest、命令、可执行版本、
参数、环境和 reference snapshot 进入 `run-status.schema.json` 的 typed
`provenance`，并以 repository-relative path 和 SHA-256 链接到实际文件。

### Facade composition

`kind: facade` 的静态 contract 必须声明一个或多个 `module_refs`。每个引用包含
atomic module 的 `component_id`、repository-relative `contract_path`、契约版本和
`module_port_id → facade_port_id` bindings。v0 linter 要求引用文件存在、版本和
component identity 一致，binding 的 direction/shape/cardinality/channel
semantics 一致，且一个公开 façade port 只绑定一个 module port。没有具体 façade
实现时，不能用 `kind: facade` 加空拓扑来假装组合能力已验证。

## 5. Entity: Invariant

| 字段 | 类型 | 说明 |
|---|---|---|
| `invariant_id` | string | `NF-Ixx` 或未来稳定 ID |
| `source_refs[]` | SourceRecord ref | 官方/本地/示例来源 |
| `statement` | string | 可审查的规范陈述 |
| `assumptions[]` | array[string] | 适用条件 |
| `research_translation` | string | 为什么适用于科研 Skill |
| `failure_modes[]` | array[string] | 不满足时的可观察失败 |
| `verification_observables[]` | array[string] | verifier 能检查什么 |
| `owner_layer` | enum | core/bio/skill/execution/verifier/review |
| `evidence_status` | enum | FACT/INFERENCE/PROPOSAL/UNKNOWN |

## 6. Entity: SpecStageBinding

| 字段 | 说明 |
|---|---|
| `stage_id` | 官方 `01–09`，不是 S00–S13 |
| `feature_activity` | 本改造工程在该步骤做什么 |
| `inputs` | 读取哪些 Spec Kit/来源材料 |
| `artifacts` | 写入哪些本 Feature 文件 |
| `gate` | 可继续的条件 |
| `rollback_target` | 失败时回到哪个步骤 |
| `target_write_allowed` | 01–07 为 false；08 由批准任务决定 |

## 7. Entity: MergeDecision

| 值 | 含义 |
|---|---|
| `merge-view` | 统一人类阅读入口，源能力仍保留 |
| `compose-only` | 只合并数据交接/编排，不合并科学方法 |
| `keep-separate` | 输入、estimand、失败责任或所有权不可替代 |
| `missing` | 需要新增能力或合同，但不是自动创建 |
| `pending` | 证据不足或用户选择未定 |

每个 decision 必须包含 `evidence_refs`、`reason`、`preserved_boundaries` 和
`next_task_ids`。

## 8. Entity: EvaluationCase

```text
EvaluationCase
├── case_id
├── task_statement
├── input_manifest
├── environment_lock
├── allowed_tools_and_budget
├── expected_observables
├── hidden_oracle_or_reference
├── deterministic_verifier
├── human_rubric (optional)
├── split: construction | dev | validation | holdout
├── variant_id
├── eligibility_record
├── repetition_policy
└── trace/evidence record
```

### 评估记录

| 字段 | 说明 |
|---|---|
| `primary_pass` | 任务级 oracle/verifier 是否通过 |
| `traceability_coverage` | requirement→evidence 可追踪比例 |
| `composition_validity` | 端口兼容性是否可判定 |
| `execution_realizability` | 是否能落到执行入口和 verifier |
| `provenance_completeness` | provenance 必要字段覆盖 |
| `ambiguity_rate` | 未解决或多位置解释比例 |
| `unsupported_claim_rate` | 超出证据边界的 claim 比例 |
| `fail_closed` | 负例是否按预期停止 |

字段诊断分数不能替代 `primary_pass`，也不能直接证明科学结论成立。

### Evaluation eligibility and repetition

`eligible_case` 必须在 Agent 运行前依据 case manifest、输入 hash、oracle、
deterministic verifier、权限和预算字段计算。资源缺失、oracle/verifier 未冻结、
输入不可读、权限不满足或 construction/holdout 泄漏属于
`INELIGIBLE_PRE_RUN`，必须在 exclusion record 中写明原因，不能从分母静默删除。
对一个已经 eligible 的 case，超时、非零执行返回、缺少输出、verifier error、
verifier fail、malformed trace 和 unsupported claim 都是该 case 的失败，不是
排除理由。

第一批 A0–A3 protocol 固定每个 eligible case/variant 做 3 次重复。若执行器支持
seed，seed 由 `protocol_version:case_id:variant_id:replicate_index` 的稳定摘要
派生并记录；不支持时记录 `seed_status: unavailable`，不得伪造 seed。默认
`determinism: strict`：三次规范化输出 hash 必须一致且每次 verifier 通过；
任何 hash 差异或一次失败都使该 case/variant cell 不通过。若未来某 case 明确
批准 `semantic`，输出 hash 可不同，但每次必须通过同一 verifier；结果差异只能
作为 nondeterminism 诊断记录，不能隐藏失败。

`task_level_pass_rate` 的分母是预先计算且被所有比较变体共同满足的 eligible
case/variant cells，不是成功尝试数；paired A0–A3 分析使用四个变体 eligible
case 集合的交集。交集为空或少于协议最低数量时状态为
`NOT_RUN/INSUFFICIENT_ELIGIBLE_CASES`，不输出分数。

## 9. Entity: ReviewGate

| 字段 | 说明 |
|---|---|
| `gate_id` | 稳定门禁 ID |
| `stage` | Spec Kit stage 或 Bio S stage |
| `machine_verdict` | 机器可重复检查结果 |
| `human_decision` | pending/approved/rejected/waived |
| `approver` | 人工批准者；不得由 Agent 自填 |
| `reason_and_scope` | 批准、拒绝或 waiver 的原因和范围 |
| `created_at` | 时间 |
| `re_review_condition` | 何时必须重新审查 |

`ReviewGate` 是控制面记录，不能把人工批准伪装成普通 Nextflow output。

## 10. Frozen logical component roster

The logical denominator is fixed at 13. A Chinese mirror, English copy, host
projection, workflow, bundle, catalog, extension or document does not add a
logical component.

| Kind | component_id |
|---|---|
| project-adapter | `bulk-pa-luad` |
| project-adapter | `cross-branch-integration` |
| project-adapter | `multiqc` |
| project-adapter | `pathway-enrichment` |
| project-adapter | `wgcna-module-constraint` |
| reference | `01-mds` |
| reference | `02-deg` |
| reference | `02-deg-results` |
| reference | `03-de-visualization` |
| reference | `03-volcano` |
| reference | `04-pathway-enricher` |
| reference | `04-pathway-workflow` |
| reference | `05-kegg` |

The complete field-level records are in
`contracts/skill-audit-record.yml`. Each record has a value for every required
field and uses the fixed Chinese status vocabulary; uncertainty is represented
explicitly rather than by an empty value.

## 11. Spec Kit stage binding

`stage_id` is the official Spec Kit stage (`01`–`09`) and must not be confused
with the Bio profile's `S00`–`S13` vocabulary. The canonical forward mapping is
documented in `plan.md`; its implementation permission is false for `01`–`07`
and is granted only to the paths in `review/approval.md` for this run.

## 12. Contract and boundary references

- Candidate schema: `contracts/node-contract.schema.json`.
- Representative public contract: `contracts/multiqc/node.contract.json`.
- Core/Bio ownership: `contracts/core-profile-boundary.md`.
- Merge and composition decisions: `merge-decisions.md`.
- Skill-to-invariant mapping: `mappings/skill-to-invariant.tsv`.
- Local evaluation protocol: `evaluation-protocol.md`.
