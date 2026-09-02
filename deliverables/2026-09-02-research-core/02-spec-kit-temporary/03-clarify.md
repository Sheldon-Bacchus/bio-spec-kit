# 03 — Clarifications 记录

**Feature**：`005-skills-nextflow-research-core`  
**状态**：`RESOLVED_BY_USER_DELEGATED_DECISION`  
**规则**：官方 `clarify` 阶段最多处理五个高影响问题；答案的 canonical
版本写回 `spec.md` 的 `## Clarifications`，本文件只保留问题、影响、提案和
决定历史，不能与 `spec.md` 形成第二套事实。

## C-001：外部总览是否冻结进当前仓库？

**问题**：用户指定的 `ALL-SKILLS-WORKFLOW-REFERENCE-zh-CN.md` 和
`CONSOLIDATED-SKILLS-WORKFLOW-zh-CN.md` 当前位于另一个 worktree。后续审计
是否应把它们复制到本 Feature 的 `inputs/` 或仓库 docs 中，作为版本化输入快照？

**影响**：不冻结会影响 source path 的可复现性；复制则会增加一份需要维护的
材料，但不会自动改变其“参考输入”角色。

**决策前提案（已由下方决定替代）**：`PENDING`。若无特别指示，采用“只读冻结副本，保留原路径和
sha256；不把副本当执行指令”的方案。

**决定**：`APPROVED`。两份原始文件复制到本 Feature 的 `inputs/`，并保留原始
worktree 路径、观察日期和 SHA-256。快照仍是 `SKILL_AUDIT_INPUT`，不获得运行
指令或科学验证地位。

## C-002：13 个逻辑 Skill 的 roster 口径

**问题**：是否严格采用用户底稿中的 5 个项目适配器 + 8 个 reference Skill，
并把中文/英文镜像和宿主发现副本排除在逻辑计数之外？当前 checkout 的目录
状态差异是否单独记录为 source gap，而不扩展 roster？

**影响**：会影响覆盖率分母、任务数量、合并判断和后续 benchmark 的 construction
集合。

**决策前提案（已由下方决定确认）**：采用底稿的 13 个逻辑组件作为本轮固定分母；checkout 差异进入
`source_status`，不静默新增或删除组件。

**决定**：`APPROVED`。本轮固定 5 个项目适配器 + 8 个 reference 组件；当前
checkout 的目录差异单独进入 source gap，不改变 13 的逻辑分母。

## C-003：Research Core 与 Bio preset 的边界

**问题**：Research Core 是否只包含跨领域生命周期/契约/评估抽象，而把生物学
术语、S00–S13、统计方法和具体路由放入 Bio profile/preset？评估协议是 core
公共能力，还是单独的 evaluation extension？

**影响**：决定最终哪些字段进入 core、哪些进入 preset，以及是否能复用于
scRNA、CADD、空间组学等其他领域。

**决策前提案（已由下方决定确认）**：Core 拥有通用生命周期、component contract、身份/provenance、
gate、verifier 接口和评估协议骨架；Bio preset 拥有生物学语义、S00–S13、
estimand 词汇和方法路由；具体算法仍由 Skill/执行层拥有。

**决定**：`APPROVED`。Core 拥有通用生命周期、component contract、身份与
provenance、gate、verifier 接口和评估协议骨架；Bio profile/preset 拥有生物学
语义、S00–S13、estimand 词汇和方法路由；算法与执行细节仍由 Skill/Execution
拥有。

## C-004：机器契约 canonical 名称与粒度

**问题**：是否采用 `node.contract.json` 作为机器可读接口的 canonical 名称，
并允许一个 public subworkflow 关联多个 atomic module contract？还是需要使用
项目已有的其他文件名/格式？

**影响**：决定 MD、JSON、Nextflow、verifier 之间的链接方式和后续 lint 规则。

**决策前提案（已由下方决定确认）**：采用 `node.contract.json`；`SKILL.md` 是人/Agent 入口，JSON
是精确端口和 gate，Nextflow 是执行连接；一个 public façade 可引用多个内部
module，但不得让内部 module 取代 public contract。

**决定**：`APPROVED`。采用 `node.contract.json`；public façade 可引用多个
atomic module contract，但内部 module 不取代 public contract。

## C-005：第一批量化案例与比较矩阵

**问题**：第一批是否采用当前已有的 BixBench/本地 fixture，还是纳入用户找到的
BioBench 数据集，或使用二者分层？比较是否固定 A0–A3 四变体，还是使用
`Spec/no-Spec × Skill/no-Skill` 的 2×2 设计？

**影响**：决定 oracle、数据许可、holdout 划分、任务级主指标和 Langfuse/
Promptfoo harness 的输入。

**决策前提案（已由下方决定替代）**：先用本地可复核 fixture 做 verifier smoke test，再用未参与
Research Core 归纳的外部/保留任务做 validation；A0–A3 是可读的候选命名，
最终矩阵待用户确认。任何数据集都不直接把外部答案当 hidden oracle。

**决定**：`APPROVED`。第一批只使用仓库内 fixture，冻结 A0–A3 四变体；MultiQC
用于 construction/smoke，shared-integration 用于 validation 参考，holdout 只在
后续 oracle 冻结后使用。本轮不使用外部数据、不安装第三方服务、不上传数据、
不启动长期 benchmark。

## Clarify 阶段门禁

- [x] 五个问题都有明确答案、延期理由或被删除的范围说明。
- [x] 答案已经写回 `spec.md`，且没有只留在聊天上下文。
- [x] 任何改变 roster、core 边界、契约名称或评估设计的答案都触发一次
      `spec.md` 和 `plan.md` 的一致性复核。
- [x] 在以上门禁通过前，不进入 08 Implement；本次用户指令已授权进入批准
      范围内的 Implement。

## 决策 provenance

- 决策来源：用户指令“你全部自行决定吧，开始执行”。
- 决策日期：`2026-09-02 Asia/Shanghai`。
- 适用范围：本 Feature 及 `spec.md` 第 13 节列出的目标路径。
- 未授权事项：其他 Skill、workflow、bundle、extension、外部数据、第三方
  服务和长期评估。
