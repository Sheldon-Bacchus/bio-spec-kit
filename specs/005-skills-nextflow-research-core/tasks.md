# 06 — Tasks

**Feature**：`005-skills-nextflow-research-core`  
**状态**：`REMEDIATION_COMPLETE / T001-T025,T027,T030-T034 COMPLETE; T026,T028,T029 DEFERRED`  
**来源**：[spec.md](spec.md)、[plan.md](plan.md)、
[checklists/requirements.md](checklists/requirements.md)

## 执行规则

- 本文件拆的是“改造工程”的工作，不是未来某个 RNA-seq 项目的科研任务。
- `T001–T021` 只产生或审查本 Feature 的证据、模型和审查产物；不得修改目标 Skills、
  Consolidated Workflow、preset 或 runtime。
- `T022` 是用户门禁。它没有完成前，所有目标修改任务必须保持阻塞。
- 每项任务必须留下可定位的证据路径；“完善文档”“继续分析”这类无边界描述
  不算可执行任务。
- `[P]` 只表示不共享写入目标且可以并行；共享 `research.md`、schema 或审计
  manifest 的任务必须串行合并。

## 执行状态约定

`[x]` 表示本轮已完成并有证据；`[ ]` 表示尚未完成或被明确授权边界阻塞。
T026 保持未完成，因为本次授权明确禁止长期/外部评估；它只能在单独授权后
运行。T027/T028 只报告本轮实际证据，不把未运行的评估写成通过。

## 需求追踪基线

| 需求 | 主要任务 |
|---|---|
| `FR-001` | `T006`, `T021`, `T022` |
| `FR-002` | `T020`, `T021`, `T022` |
| `FR-003` | `T001`, `T002`, `T005`, `T009`, `T021` |
| `FR-004` | `T003`, `T010`, `T011`, `T013` |
| `FR-005` | `T009`, `T010`, `T011` |
| `FR-006` | `T009` |
| `FR-007` | `T012`, `T023` |
| `FR-008` | `T005`, `T007`, `T013` |
| `FR-009` | `T007`, `T008`, `T024`, `T030`, `T031` |
| `FR-010` | `T014`, `T015`, `T025` |
| `FR-011` | `T006`, `T021`, `T027` |
| `FR-012` | `T013`, `T014`, `T015`, `T024` |
| `FR-013` | `T017`, `T018`, `T019`, `T026`, `T028`, `T032` |
| `FR-014` | `T001`, `T002`, `T004`, `T022`, `T023` |
| `FR-015` | `T004`, `T020`, `T022`, `T023`, `T027`, `T033`, `T034` |
| `SC-001` | `T001`, `T004`, `T016`, `T020`, `T022` |
| `SC-002` | `T003`, `T010`, `T011`, `T013` |
| `SC-003` | `T009`, `T010`, `T011`, `T013` |
| `SC-004` | `T005`, `T007`, `T008` |
| `SC-005` | `T012`, `T023`, `T027` |
| `SC-006` | `T006`, `T021`, `T022` |
| `SC-007` | `T014`, `T015`, `T025` |
| `SC-008` | `T017`, `T018`, `T019`, `T026`, `T028` |
| `SC-009` | `T020`, `T021`, `T022`, `T027` |
| `SC-010` | `T001`, `T002`, `T022`, `T023`, `T025` |

## Phase 1: Evidence and scope freeze

- [x] T001 [P] [US1] 补充并冻结 `specs/005-skills-nextflow-research-core/research.md` 的 source ledger，记录用户输入、根 constitution、官方 Spec Kit 规则、用户提供的两份底稿、Nextflow/nf-core 来源和本地 Skill 路径的 source role、状态与观察日期。
- [x] T002 [P] [US1] 在 `specs/005-skills-nextflow-research-core/research.md` 中核对当前 checkout 与外部 worktree 的路径差异，明确哪些文件可读、哪些文件为 `MISSING_IN_CHECKOUT`，不得用摘要替代原文。
- [x] T003 [P] [US2] 冻结 `specs/005-skills-nextflow-research-core/data-model.md` 中的 13 个逻辑组件 roster entity，固定 5 个项目适配器、8 个参考组件，并标出镜像/投影不重复计数规则。
- [x] T004 [US1] 为 `specs/005-skills-nextflow-research-core/clarifications.md` 的 C-001–C-005 收集用户决定；任何改变 scope、core boundary、contract name 或 evaluation matrix 的答案必须回写 `spec.md`。

## Phase 2: Nextflow and Spec Kit evidence

- [x] T005 [P] [US3] 补全并核验 `specs/005-skills-nextflow-research-core/research.md` 的 invariant ledger，逐条记录 Nextflow/nf-core 来源、confirmed statement、假设、失败模式和可观察验证。
- [x] T006 [P] [US1] 复核并冻结 `specs/005-skills-nextflow-research-core/data-model.md` 的官方 Spec Kit 九步 entity，表达每一步的输入、产物、门禁、回路和本 Feature 的边界，不创建目标 workflow 修改。
- [x] T007 [US3] 在 `specs/005-skills-nextflow-research-core/data-model.md` 将 queue/value、tuple/meta、stable key、cardinality、named output、route、provenance 和 execution/scientific/review status 映射到候选 component contract 字段。
- [x] T008 [US3] 创建 `specs/005-skills-nextflow-research-core/contracts/node-contract.schema.json` 的候选机器契约，并在其中把 port shape、cardinality、identity、route、gate、evidence 和 status 标为可校验字段；若 C-004 改变名称，先更新任务路径再实施。

## Phase 3: 13 Skill audit and composition analysis

- [x] T009 [US2] 创建并冻结 `specs/005-skills-nextflow-research-core/contracts/skill-audit-record.yml`，为每个审计字段定义 `有/条件/无/待核/不适用/未验证` 状态枚举和 source/evidence 引用。
- [x] T010 [US2] 按 roster 顺序审计 `spec-mvp/skills/bulk-pa-luad/`、`cross-branch-integration/`、`multiqc/`、`pathway-enrichment/`、`wgcna-module-constraint/`，将每项输入、输出、方法、门禁、失败和 runtime status 写入 `data-model.md` 或其引用记录。
- [x] T011 [US2] 按 roster 顺序审计 `spec-mvp/skills/reference-stack/` 中的 8 个参考组件，区分 reference-only、not-verified 和可执行证据，不将中文镜像或宿主副本计为新组件。
- [x] T012 [US2] 依据输入、estimand、身份、输出和失败责任生成 `specs/005-skills-nextflow-research-core/merge-decisions.md`，分别标记 `merge-view`、`compose-only`、`keep-separate`、`missing` 和 `pending`，不删除或改写源 Skill。
- [x] T013 [US2] 建立 `specs/005-skills-nextflow-research-core/mappings/skill-to-invariant.tsv`，将每个逻辑组件映射到适用的 Nextflow invariant、Spec Kit stage、Bio S00–S13 stage 和缺失项，并为无法映射的项保留原因。

## Phase 4: Research Core abstraction

- [x] T014 [US3] 补全并冻结 `specs/005-skills-nextflow-research-core/data-model.md` 中的 Core、Bio profile/preset、Skill/component、Execution、Verifier 和 Review entity，记录每个 owner 与禁止越界。
- [x] T015 [US4] 在 `specs/005-skills-nextflow-research-core/contracts/core-profile-boundary.md` 说明哪些字段跨领域共用、哪些只属于 Bio profile、哪些必须留在具体算法/执行器；将 C-003 的决定写入来源位置。
- [x] T016 [US4] 修订并冻结 `specs/005-skills-nextflow-research-core/quickstart.md`，提供人类快速审阅入口、Agent 按需读取顺序、证据状态解释和 Implement 前置条件；不得把它写成目标 runtime 使用说明。

## Phase 5: Evaluation protocol design

- [x] T017 [P] [US5] 在 `specs/005-skills-nextflow-research-core/evaluation-protocol.md` 定义 case-input、environment、hidden-oracle、deterministic-verifier、human-rubric、trace record、construction/validation/holdout 和 A0–A3/2×2 候选矩阵；只写 protocol，不运行 benchmark。
- [x] T018 [US5] 为 `specs/005-skills-nextflow-research-core/evaluation-protocol.md` 定义 task-level pass rate 主指标及 traceability、composition、realizability、provenance、ambiguity、unsupported-claim、fail-closed 诊断指标，写清分母、分子和不能解释的范围。
- [x] T019 [US5] 将 Langfuse、Promptfoo 或其他记录/矩阵工具映射为可替换的 observability adapter，写明它们不能替代科学 oracle、确定性 verifier 或人工 claim review。

## Phase 6: Pre-implement gate

- [x] T020 [US1] 根据 `specs/005-skills-nextflow-research-core/checklists/requirements.md` 完成维护者审阅记录；未确认的清单项必须给出缺口或延期原因。
- [x] T021 [US1] 在 `specs/005-skills-nextflow-research-core/analysis.md` 完成只读一致性分析，检查 FR/SC/US 覆盖、任务孤儿、术语漂移、来源不足、目标漂移和 constitution 冲突。
- [x] T022 [US1] 记录用户对 01–07 产物、C-001–C-005、目标修改路径和长期评估授权的明确决定到 `specs/005-skills-nextflow-research-core/review/approval.md`；没有该记录不得进入 Implement。

## Phase 7: Implement（仅在用户批准后解锁）

- [x] T023 [US2] 经批准后，按 `specs/005-skills-nextflow-research-core/merge-decisions.md` 只读修改 `spec-mvp/skills/multiqc/SKILL.md` 与 `.agents/skills/multiqc/SKILL.md`，保留 source path、状态、不可替代边界和审计证据；不得扩大到未批准路径。
- [x] T024 [US3] 经批准后，为 `contracts/multiqc/node.contract.json` 和 `evaluation/cases/multiqc-mvp/` 创建机器契约、最小 fixture、negative case、verifier，并以 `evaluation/runs/` 保存 provenance 记录；先验证接口和失败闭合，再讨论 runtime 迁移。
- [x] T025 [US4] 经批准后，按 `contracts/core-profile-boundary.md` 修改或新增 `presets/bio-research-mvp/preset.yml`、`README.md` 和 `contracts/research-core-profile.yml`，并执行 schema、source、路径和文档引用检查。
- [ ] T026 [US5] 经单独批准后，使用 `evaluation-protocol.md` 运行第一批对照实验，在 `evaluation/runs/` 保存 trace、版本、输入 hash、verifier 输出和人工 review；不得把实验结果直接回写成规则。

## Phase 8: Convergence

- [x] T027 [US1] 运行 Spec Kit `converge` 语义的只读回验：将实际产物逐项对照 `spec.md`、`plan.md`、`checklists/requirements.md` 和本文件；未完成项只能追加为新任务，不得重写历史任务。
- [ ] T028 [US5] 若评估已运行，依据 `evaluation-protocol.md` 在 `evaluation/runs/` 和 `review/` 分别报告任务级主指标、诊断指标、失败案例和 claim boundary；禁止以字段完整度或单一 judge 分数宣称 Research Core 有效。

## 任务依赖与验证证据矩阵

| Task | Depends on | Verification evidence |
|---|---|---|
| T001 | — | `research.md`, `inputs/README.md` source ledger and hashes |
| T002 | T001 | `research.md` checkout/worktree gap record |
| T003 | T001-T002 | `data-model.md`, `contracts/skill-audit-record.yml` roster count |
| T004 | — | `clarifications.md`, `spec.md` Clarifications and approval provenance |
| T005 | T001 | `research.md` invariant evidence records and source URLs |
| T006 | T001-T004 | `data-model.md` SpecStageBinding and `plan.md` forward mapping |
| T007 | T005-T006 | `data-model.md`, `contracts/node-contract.schema.json` field mapping |
| T008 | T007 | JSON parse/schema validation and candidate contract path |
| T009 | T003,T007 | `contracts/skill-audit-record.yml` required fields and status vocabulary |
| T010 | T003,T009 | five project-adapter records and source refs |
| T011 | T003,T009 | eight reference records and mirror exclusion |
| T012 | T010-T011 | `merge-decisions.md` decision/evidence/boundary/next-task table |
| T013 | T005,T010-T012 | `mappings/skill-to-invariant.tsv` has 13 unique component rows |
| T014 | T007,T009-T013 | `data-model.md` ownership entities and boundary references |
| T015 | T014 | `contracts/core-profile-boundary.md` ownership table and C-003 decision |
| T016 | T004,T015 | `quickstart.md` reading order, smoke command and gate boundary |
| T017 | T008,T013,T015 | `evaluation-protocol.md` case package, A0-A3 and local permission boundary |
| T018 | T017 | `evaluation-protocol.md` primary/diagnostic metric definitions |
| T019 | T017-T018 | `evaluation-protocol.md` observability adapter boundary |
| T020 | T004,T015-T019 | `review/requirements-review.md` item-by-item requirements-quality review |
| T021 | T020 | `analysis.md` read-only consistency report and severity counts |
| T022 | T004,T020-T021 | `review/approval.md` allowed paths and evaluation authorization |
| T023 | T012,T022 | identical MultiQC Skill source/projection and no Spec Kit lifecycle text |
| T024 | T008,T017,T022 | MultiQC contract, run-status envelope, positive/negative case, verifier and run manifests |
| T025 | T015,T022 | preset contract binding and README/preset consistency |
| T026 | T017-T019,T022 | deferred: no run permitted until separate benchmark authorization |
| T027 | T023-T025 | post-implementation spec/plan/checklist/tasks comparison |
| T028 | T026 | deferred unless an evaluation run exists; no score reported |
| T029 | T027 | A-007 follow-up: cross-platform JSON encoding compatibility requires separate approval and runtime evidence |

## 本轮执行边界

- T001-T025、T027 are the approved local design/implementation slice.
- T026 and T028 remain explicitly deferred because no long-running or external
  evaluation was authorized; this is a deliberate `NOT_RUN`, not a pass.
- T029 is an appended convergence follow-up for the observed GB18030 artifact
  encoding. It requires a separate approval before any change to the extension
  wrapper or a cross-platform compatibility run.
- No task authorizes modification outside the paths approved in `review/approval.md`.

## Phase 9: Convergence follow-up

- [ ] T029 [US3] 在另行批准且不扩大本轮范围的兼容性任务中，评估并规范
  `extensions/bio-multiqc/scripts/run_multiqc.py` 产生的 JSON 编码，补充跨平台
  consumer/verifier 证据；当前仅记录 A-007，不修改该未授权 extension。

## Convergence record

**Date**：`2026-09-02 Asia/Shanghai`  
**T027 result**：`PASS_WITH_EXPLICIT_DEFERRED_ITEMS`

只读对照已覆盖 `spec.md`、`plan.md`、`checklists/requirements.md`、本文件、
13 条审计记录、12 条 invariant、MultiQC contract、正/负例运行产物和批准路径。
未发现未接受的 CRITICAL/HIGH 矛盾；A-007 已追加为 T029，T026/T028 仍按授权
保持 `DEFERRED/NOT_RUN`。未重写历史任务或扩大批准路径。

**独立审计收束**：初次审计与第二次条件审计的发现均已在批准范围内处理并保留
记录；最终独立只读审计（Curie，`01a060a2-7f94-79a1-bbbb-128d4a23c651`）返回
`PASS`，确认 verifier、契约、范围和声明边界闭合。bounded local implementation
可关闭；T026/T028/T029 与 A-007 仍保持明确延期/限制。

## Phase 10: Fresh-context audit remediation

- [x] T030 [US3] 在 contracts/node-contract.schema.json、MultiQC node contract
  和 contracts/validate_contracts.py 中固定 static capability/run-status 分层、
  versioned facade/module references、port binding compatibility、cross-field
  direction/uniqueness/reference rules，并留下 regression self-tests。
- [x] T031 [US3] 在 run-status、input/artifact manifest schemas、当前 MultiQC
  evidence 和 Skill/preset handoff 中固定 typed provenance、repository-relative
  paths、checkout identity、manifest/file hashes 和科学/release boundary。
- [x] T032 [US3] 在 evaluation-protocol.md、evaluation/a0-a3-matrix.yml、
  construction case 和 evaluation/validate_protocol.py 中固定 pre-run
  eligibility、exclusion codes、post-run failure accounting、paired intersection、
  three repetitions、seed-unavailable 和 strict/semantic determinism policy；
  不运行 A0-A3 或生成 effect score。
- [x] T033 [US3] 在 local positive/negative verifier 与 frozen run review 中补齐
  repository-relative path resolution、manifest exactness、actual hash/size checks、
  typed status/provenance checks；保留 wrapper executor-native metadata 的风险和
  T029 延期，不修改未授权 extension。
- [x] T034 [US3] 重新执行 contract self-test、protocol gate、positive/negative
  verifier 和 five-axis review，将命令输出、deferred items 与最终 disposition
  记录到 review/remediation-20260902.md 和 analysis.md。

**T030-T034 result**：PASS_WITH_EXPLICIT_DEFERRED_ITEMS。静态/运行态 contract、
typed manifest/provenance、跨字段门、A0-A3 protocol gate、正/负 verifier 和五轴
review 均已在当前 checkout fresh rerun；unseen validation、T026/T028/T029、
scientific/release 仍按上文延期或未验证。
