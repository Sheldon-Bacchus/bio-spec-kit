# 07 — Analyze Report（授权后 bounded slice）

**Feature**：`005-skills-nextflow-research-core`  
**分析类型**：只读一致性与证据链审计（本报告由只读扫描完成后材料化）  
**分析日期**：`2026-09-02 Asia/Shanghai`  
**当前结论**：`REMEDIATED_BOUNDED_SLICE / REUSABLE_CORE_NOT_GENERALIZED`

本报告检查 Constitution、Spec、Clarifications、Plan、Checklist、Tasks、
contract、审计记录、评估协议和本轮实际证据之间是否一致。它不把字段齐全、
进程成功或本地 smoke 结果升级为生物学正确性、QC 通过或 human release。

## 1. 静态规模与执行状态

| 对象 | 数量/状态 | 证据与边界 |
|---|---:|---|
| Functional Requirements | 15 | `FR-001`–`FR-015`；有 `tasks.md` 需求追踪基线 |
| Success Criteria | 10 | `SC-001`–`SC-010` |
| User Stories | 5 | `US1`–`US5` |
| Clarifications | 5 resolved | `C-001`–`C-005` 已写回 `spec.md` 和 `review/approval.md` |
| Nextflow invariant evidence records | 12 | `NF-I01`–`NF-I12`；每条有 source/scope/failure/observable |
| Logical components | 13 | 5 project adapters + 8 reference components；audit/mapping 各一行 |
| Requirements checklist | 40 accepted | `review/requirements-review.md` 逐项审阅；不代表运行验收 |
| Tasks | 34 | T001-T029 的 bounded-slice记录保留；T030-T034 是本次 fresh-context remediation，T026/T028/T029 继续 `DEFERRED` |

## 2. 一致性检查结果

| 检查 | 结果 | 证据 |
|---|---|---|
| C-001 external input reproducibility | PASS | `inputs/README.md`；两份快照分别匹配 SHA-256 `B7F357A25F59693FBF647734DA30F5526D68F908A48C7984C9E81BDEF0FB1CBB` 与 `57FEB5C7185103FC58ECB2003B3C653CCE67E53427E167CE5CEF5CB72022869E` |
| C-002 denominator | PASS | `contracts/skill-audit-record.yml` 13 records、`mappings/skill-to-invariant.tsv` 13 unique rows、镜像/投影排除规则 |
| C-003 Core/Bio boundary | PASS | `contracts/core-profile-boundary.md`、preset profile contract、`spec.md` Clarifications |
| C-004 contract name/status envelope | PASS | `contracts/node-contract.schema.json`、`contracts/run-status.schema.json` 与 `contracts/multiqc/node.contract.json`；node contract 和 run-status 实例的 JSON Schema 2020-12 validation 通过 |
| C-005 evaluation boundary | PASS | `evaluation-protocol.md`、A0–A3、local construction/dev/validation/holdout 分层；不下载、不上传、不安装、不长跑 |
| Audit field completeness | PASS | 13 records 均含 `component_id`、purpose/estimand、inputs、preconditions、method、routes、outputs、identity、examples、provenance、`hard_boundary`、failure/recovery、runtime status、merge decision |
| MultiQC positive case | PASS | wrapper return `0`；artifact verifier 通过；FastQC/report/data/source/log/manifests、结构化 `research-core-status.json` 和 boundary review 均存在；执行/科学/发布状态精确为 `passed`/`not-verified`/`pending` |
| MultiQC negative case | PASS | wrapper return `2`；`failed`、`ok=false`、`release_ready=false`，错误明确指出 input directory 不存在 |
| Skill source/projection parity | PASS | `spec-mvp/skills/multiqc/SKILL.md` 与 `.agents/skills/multiqc/SKILL.md` 字节级一致，SHA-256 `CF9720051BC354F4642B275E8A731345B1D690CE7F1D4CC86F69C8F1FCC1B61F` |
| Scope control | PASS | 本轮新增/修改的路径均在 `review/approval.md`；preset 已直接声明 component→Skill→node contract→profile 绑定；工作树中其他既有 dirty changes 未清理、未重置、未顺手改写 |

## 3. 覆盖、孤儿和边界审计

### 3.1 需求覆盖

`tasks.md` 的需求追踪基线为每个 FR/SC 指定任务；US1–US5 由阶段任务和
`review/requirements-review.md` 覆盖。没有发现只存在于 Spec、却没有计划动作、
任务或审计检查的 FR/SC/US。`RQ-001`–`RQ-040` 均有逐项 review；RQ-040 的
关闭条件由本报告下方的 severity 结论满足。

### 3.2 任务完整性

任务矩阵含 `T001`–`T029` 共 29 行且唯一。每条任务行有动作和路径，矩阵有依赖
与 verification evidence。当前不把以下状态误报为完成：

- `T026`：没有获得长期/外部对照实验授权，因此保持 `DEFERRED/NOT_RUN`；
- `T028`：没有评估批次，因此不报告 task-level score 或诊断分数；
- `T027`：convergence 回验已完成；最终独立子 agent 审计已通过并材料化。

这些是 C-005 的授权边界，不是隐藏失败或被伪造的通过结果。

### 3.3 目标漂移与表示分离

- `SKILL.md` 仍是人/Agent 入口，只增加 contract handoff，没有写入 Spec Kit 九步。
- JSON/YAML contract、执行 wrapper、verifier、运行 manifest 和 review note 分工明确。
- MultiQC 的 `release_ready=true` 只在本 Feature review 中解释为 artifact-ready；
  `scientific_status=not-verified` 与 `release_status=pending` 保持独立。
- Core 只拥有通用 contract/control-plane skeleton；Bio profile 拥有生物学语义、
  S00–S13 和方法路由；具体算法、执行和 human release 没有被抽走。

## 4. Findings

| ID | 类型 | 严重度 | 当前判断 | 处理/边界 |
|---|---|---|---|---|
| A-001 | resolved source gap | INFO | 外部总览已冻结为 hash-checked inputs，原路径仍保留 | `inputs/README.md`、C-001 |
| A-002 | resolved roster gap | INFO | 13 的固定分母、5+8 分类和镜像排除均可复核 | audit record、mapping、C-002 |
| A-003 | resolved ownership decision | INFO | C-003 已批准；Core/Bio/Skill/Execution/Verifier/Review/Evaluation owner 已写明 | boundary contract、preset contract |
| A-004 | resolved contract naming | INFO | `node.contract.json` 已批准并通过 schema fit；仍是 v0 design contract，不是通用科学证明 | schema、MultiQC contract、C-004 |
| A-005 | explicit evaluation limitation | INFO | unseen validation/holdout 与效果分数未运行 | C-005、T026、T028；不阻塞本地 slice，但禁止泛化结论 |
| A-006 | approval/scope gate | INFO | 目标路径和运行权限已持久化；其他 dirty files 属于进入本轮前的工作树状态 | `review/approval.md`、implementation record |
| A-007 | runtime portability observation | MEDIUM | 本地 Windows MultiQC 运行生成的 `multiqc_data.json` 用 GB18030 编码；wrapper 的兼容读取和 verifier 通过，但假定 UTF-8 的跨平台消费者仍需单独处理 | `evaluation/runs/multiqc-mvp-20260902/research-core-review.md`；不修改本次未授权的 extension wrapper |
| A-008 | initial independent audit remediation | INFO | 初次独立只读审计提出的 verifier 结构化状态、运行 status envelope、preset 直接绑定、T029 摘要和审计材料化缺口已逐项修复或记录 | `review/subagent-audit-initial-20260902.md`、`contracts/run-status.schema.json`、`evaluation/runs/multiqc-mvp-20260902/research-core-status.json` |
| A-009 | verifier boundary remediation | INFO | 第二次独立审计指出的文本 substring acceptance 已改为 HTML/JSON/log/review/error 的结构化或完整等值断言；正/负 verifier 已重新通过 | `review/subagent-audit-second-20260902.md`、`evaluation/cases/multiqc-mvp/verifier/verify_case.py` |
| A-010 | final independent audit | INFO | 最终独立只读审计 verdict 为 `PASS`，确认修复真实存在、正/负回归通过、无 CRITICAL/HIGH；bounded local implementation 可关闭 | `review/subagent-audit-final-20260902.md` |

没有未接受的 `CRITICAL` 或 `HIGH` finding。A-007 是可定位的跨平台运行限制，
不是本轮 scientific/release 结论；在扩大运行范围前必须通过单独授权的兼容性
处理或明确的消费者契约解决。

## 5. Constitution 冲突检查

- 根 Constitution 仍是高层约束；Feature Constitution 只增加本 Feature 的边界，
  没有降低证据、provenance、QC、人审、可组合性或敏感数据要求。
- `Evidence gate`：来源、快照、13 roster、12 invariant 和运行记录均可定位。
- `Contract gate`：候选 schema、MultiQC contract、审计字段、hard boundary 和
  failure policy 已存在，缺失能力保持显式状态。
- `Consistency gate`：本报告以前的待批准文案已被批准范围文案替换；延期项仍标为
  `DEFERRED/NOT_RUN`，没有用 pending 以外的状态隐藏。
- `User approval gate`：只对 `review/approval.md` 列出的路径解锁；未授权的
  workflow、bundle、其他 Skill、extension、外部服务和长期 benchmark 未执行。
- `Evaluation gate`：正/负 local case 有 oracle/verifier 和 provenance；没有生成
  benchmark effect score，也没有把本地 smoke 写成 Research Core 有效性；最终独立
  audit 已确认 verifier 不依赖原始文本 substring 伪通过。

## 6. 结论与下一步

**结论**：原 bounded local implementation slice 和 convergence 已收束，初次与第二次
独立审计发现的问题已在原批准范围内处理，最终独立子 agent 审计已通过；本节结论
不扩展为 reusable-Core 通过。fresh-context B/S remediation 的当前状态与最终
门禁见第 7 节。不能宣称 13 个组件全部 runtime verified，不能宣称生物学有效性，
也不能报告未经运行的 A0–A3 分数。

原 bounded-slice closure 的明确边界：

1. T026/T028/T029 保持 `DEFERRED/NOT_RUN`，除非另行批准相应评估或兼容性工作；
2. 将 A-007 作为后续跨平台 runtime 兼容性工作保留，不把它静默改写成已解决；
3. 继续保留 `scientific_status=not-verified` 与 `release_status=pending`，不把
   artifact-ready 或本地 verifier 通过升级为科学或 release 结论。

## 7. Fresh-context reusable-Core remediation addendum

本节是对原 bounded-slice 分析的追加，不改写历史审计结论。fresh-context
审查重新发现并按 finding ID 处理了 B-001/B-002/B-003 与 S-001–S-004：

- B-001 由 node contract 的 versioned module_refs、facade port bindings 和
  cross-field validator 表达；实际 unseen façade runtime 仍未运行。
- B-002 由 static node contract 与 run-status envelope 分层解决；node 不再
  允许 status，运行态只在 status.execution/scientific/release 中出现。
- B-003 对冻结 run 已改为 repository-relative POSIX 路径、checkout identity、
  manifest/file hashes 和当前 checkout 解析；wrapper 生成的 executor-native
  绝对路径和 GB18030 输出仍是 T029/A-007 风险，未修改未授权 extension。
- S-001–S-003 已进入 schema 加 cross-field validator 加正/负 verifier 门；
  S-004 已进入可机器检查的 A0-A3 protocol gate，包括 eligibility、排除码、
  failure accounting、paired intersection、三次重复、seed unavailable 和
  strict hash 规则。

权威的逐项 disposition、五轴 review 和延期项见
review/remediation-20260902.md。该追加不改变以下边界：当前 MultiQC 与
shared-integration 只能作为 construction/reference material；architecture
review 的 B-003 unseen validation 保持 NOT_RUN/NOT_GENERALIZED；T026/T028/T029
继续延期；没有 A0-A3 effect score，也没有 scientific/release approval。
