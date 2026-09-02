# 02 — 改造工程 Specification

**Feature**：`005-skills-nextflow-research-core`

**状态**：`APPROVED_FOR_IMPLEMENTATION_SCOPE`

**本 Feature 的一句话目标**：把“现有生信 Skills 的审计、归类与抽象、Nextflow
结构不变量提炼、科研 Research Core/preset 设计和后续量化验证准备”定义成一个
可审查、可追溯、可分阶段执行的 Spec Kit 项目。

## 1. 目标与非目标

### 1.1 目标

本工程要形成一套能够被人快速审阅、被 Agent 按契约读取、被后续运行时实现的
第一版设计材料，至少包括：

1. 官方 Spec Kit 九步在**本改造工程**中的执行边界和停止条件；
2. 13 个逻辑 Skill 的固定清点范围、来源角色和统一审计字段；
3. Nextflow/nf-core 的结构不变量、来源和向科研 Skill 契约的映射；
4. 重叠、可合并、不可替代、串联和缺失的判断规则；
5. Research Core、Bio profile/preset、Skill/component、执行层和验证层的
   所有权边界；
6. Markdown、机器契约和执行代码三种表示的分离方式；
7. 后续可量化验证的任务封装、比较条件、主指标和诊断指标；
8. 进入 `08 Implement` 前必须满足的审查门禁和具体任务。

### 1.2 非目标

本轮不得做以下事情：

- 不把 Spec Kit 九步写入或替换成目标 Skills、Consolidated Workflow 或 Bio
  runtime；
- 不删除、合并、移动、覆盖或重写现有 Skill、参考副本、中文镜像、workflow、
  preset、extension、测试或运行路径；
- 不把 13 个 Skill 自动升级成已注册、已可执行或已通过科学验证的 runtime；
- 不直接实现 Nextflow `.nf`、`node.contract.json`、wrapper、verifier 或
  preset 安装逻辑；
- 不执行真实生信 pipeline，不安装未审查的第三方 Skill，不上传项目数据；
- 不在没有固定 oracle/verifier 和比较条件的情况下运行长期 benchmark 或
  prompt/Skill 优化；
- 不用文档字段数量、LLM judge 单分或图片相似度作为科研效果的唯一证明；
- 不把 Nextflow 的语法、执行器或目录结构当成完整科研生命周期标准。

## Clarifications

### Session 2026-09-02

- Q: 是否把外部 worktree 中的两份中文总览冻结为本 Feature 的版本化输入快照？ → A: 是，复制到 `inputs/`，保留原路径、观察日期和 SHA-256；副本只作审计输入，不作运行指令。
- Q: 本轮是否严格以用户底稿的 5 个项目适配器加 8 个 reference 组件作为 13 个逻辑组件的固定分母？ → A: 是；当前 checkout 的目录差异单独记录为 source gap，不扩展或缩减逻辑分母。
- Q: Research Core、Bio profile/preset 与 evaluation protocol 的所有权如何划分？ → A: Core 拥有通用生命周期、component contract、identity/provenance、gate、verifier 接口和评估协议骨架；Bio profile/preset 拥有生物学语义、S00–S13、estimand 词汇和方法路由；具体算法与执行细节留在 Skill/Execution。
- Q: 机器可读接口是否采用 `node.contract.json` 作为 canonical 名称，并允许 public façade 关联多个 atomic module？ → A: 是；public façade 目录下使用 `node.contract.json`，可引用内部 module contract，但内部 contract 不取代 public contract。该关系必须由带版本的 `module_refs` 和端口 binding 表达；没有具体 façade fit-test 时不得宣称 façade 组合已验证。
- Q: 第一批量化评估采用什么数据和矩阵？ → A: 只使用仓库内可复核 fixture；以 A0–A3 作为四变体矩阵，MultiQC 作为 construction/smoke，shared-integration 作为 validation 参考；holdout 只在后续冻结 oracle 后使用，本轮不启动外部数据、第三方服务或长期 benchmark。

## 2. 用户故事与验收场景

### US1：维护者先审查“这次要做什么”

作为维护者，我希望把本次改造工程和它要处理的目标对象分开，能够在进入
实现前看到范围、原则、风险和停止条件。

**验收场景**：

1. 给定当前仓库存在 Skills、参考文档和已有 workflow，当审阅本 Feature 时，
   可以明确区分 Spec Kit 执行协议、Nextflow 参考、13 个 Skill 输入和目标输出。
2. 给定用户只批准 01–07，当执行 Agent 读取本 Feature 时，不会因为任务文件
   存在而修改任何目标 Skill 或 preset。
3. 给定一个未定义的关键选择，产物会标记 `UNKNOWN` 或
   `PENDING_USER_CONFIRMATION`，而不是使用未声明的默认值。

### US2：逐个审计 13 个逻辑 Skill

作为维护者，我希望每个 Skill 都有相同的上游输入、前置条件、方法、下游输出、
证据和边界字段，从而可以快速看出真正的重叠和缺口。

**验收场景**：

1. 给定 13 个逻辑组件，审计表能够逐个列出 `component_id`、来源角色、科研
   位置、输入、输出、方法/estimand、路由、身份、验证、provenance 和失败边界。
2. 给定某个字段在源材料中没有出现，记录显示 `无/待核`，不以空白或推测填充。
3. 给定中文镜像和英文参考副本属于同一逻辑能力，它们不会被重复计数。
4. 给定两个 Skill 文字相似但 estimand 或失败边界不同，系统会保留独立能力，
   只允许讨论接口编排或 handoff 合并。

### US3：从 Nextflow 提炼可迁移的结构规则

作为 Research Core 设计者，我希望使用 Nextflow/nf-core 已经验证过的 dataflow
结构来约束 Skill，而不是凭审美添加字段。

**验收场景**：

1. 每条 proposed invariant 都有来源、抽象解释、科研映射和失败模式。
2. 设计能够表达 queue/value、tuple/meta、稳定 key、cardinality、named
   outputs、显式 route、cache/resume identity 和 provenance。
3. 文档明确标出哪些只是 Nextflow 执行层概念，不能直接升级为科学结论或人工
   release gate。

### US4：形成 Research Core 与 Bio preset 的边界草案

作为维护者，我希望知道哪些内容属于跨领域 core，哪些内容只属于生信 profile，
哪些内容应留在具体 Skill 或执行器中。

**验收场景**：

1. 每一个拟纳入的字段或规则都有 owner 和“不负责什么”的说明。
2. `SKILL.md`、机器契约、执行代码、verifier 和 review 记录不会被合并成同一
   份既给人又给机器又给执行器的混合文件。
3. 具体 preset 的科学方法不会反向改变 Spec Kit 官方生命周期的定义。

### US5：为之后的量化比较留下可执行接口

作为评测设计者，我希望下一阶段能比较“无 Spec / 官方 Spec Kit / 改造后的
Research Core”以及“无 Skill / 有 Skill”，而不是只比较文档长短。

**验收场景**：

1. 评估设计固定相同任务、数据、模型、工具预算、输出格式和 verifier；变体只
   改变待研究的 Spec/Skill 条件。
2. 主指标是任务级正确性或验收通过率；字段完整度、追踪覆盖率、组合有效性、
   可执行性和 provenance 完整度被标为诊断指标。
3. 设计包含 construction、validation/holdout 和真实项目案例的边界，不能只
   用参与抽象的 13 个 Skill 自测。
4. Langfuse/Promptfoo 等工具只能承担 trace、版本、矩阵和 assertion 记录，
   不能替代科学 oracle 或人工 claim 审阅。

## 3. Functional Requirements

- **FR-001**：本 Feature MUST 将“Skills 归类/抽象、Nextflow invariant 提炼、
  Research Core/preset 设计”作为一个独立的 Spec Kit 项目处理；Spec Kit
  生命周期 MUST NOT 被改写成目标 Skill 的内容。
- **FR-002**：本 Feature MUST 产出 01–07 的可审查中间产物，并明确 08 Implement
  与 09 Converge 的解锁条件；本轮 MUST NOT 进入目标实现。
- **FR-003**：每个输入材料 MUST 标注来源角色、可支持的结论、不可支持的推断、
  观察日期和版本/hash 状态；用户意图、参考 prose 和执行指令 MUST 分开。
- **FR-004**：初始清点分母 MUST 固定为 13 个逻辑组件：5 个项目适配器和 8 个
  reference 组件；中文镜像、英文副本、宿主投影、workflow、bundle 和文档
  MUST NOT 作为额外逻辑 Skill 计数。
- **FR-005**：每个逻辑组件 MUST 使用统一审计字段记录 scientific purpose、
  estimand/observable、upstream input、precondition、method、route、downstream
  output、identity、evidence、provenance、failure/recovery 和 runtime status。
- **FR-006**：统一审计字段 MUST 显式使用 `有/条件/无/待核/不适用/未验证` 状态；
  缺失信息 MUST NOT 以空白、默认值或 Agent 推测代替。
- **FR-007**：每个重叠判断 MUST 明确属于 `merge-view`、`compose-only`、
  `keep-separate`、`missing` 或 `pending`，并给出输入、estimand、身份、输出、
  失败责任和证据依据；本轮 MUST NOT 删除或合并源文件。
- **FR-008**：每条 Nextflow invariant MUST 记录 source、适用假设、科研抽象、
  失败模式、可观察验证和 owner layer，并区分 FACT、INFERENCE、PROPOSAL 和
  UNKNOWN。
- **FR-009**：候选静态 `node.contract.json` MUST 能表达 port direction、shape、
  cardinality、queue/value、tuple/meta identity、显式 route、named output、gate、
  façade/module binding 和静态 provenance 要求；关联的 `run-status.schema.json`
  MUST 表达执行/科学/发布三态，且静态 node contract 不得复制某次运行的三态值。
- **FR-010**：Research Core、Bio profile/preset、Skill/component、Execution、
  Verifier 和 Human Review MUST 各自有 owner 和禁止越界；Markdown、机器契约、
  执行代码和审查记录 MUST NOT 被合并为单一事实层。
- **FR-011**：本 Feature MUST 建立 Spec Kit 九步到改造活动、产物、门禁和失败回路
  的正向映射；该映射 MUST NOT 被解释为修改根目录 workflow 或创建九个 runtime 节点。
- **FR-012**：本 Feature MUST 建立从 Nextflow invariants 与 13 个 Skill 证据反向
  归纳 Research Core v0 的方法，并将不能表达的内容记录为 schema gap。
- **FR-013**：后续评估 protocol MUST 定义 task-level 主指标、诊断指标、构造/验证/
  holdout 划分、固定比较条件、oracle/verifier 和 trace 记录；本轮 MUST NOT 产生
  benchmark 效果分数。
- **FR-014**：在用户批准 01–07、关键澄清、目标路径和运行授权之前，本 Feature
  MUST NOT 修改 `spec-mvp/skills/`、`.agents/skills/`、`presets/`、`workflows/`、
  `bundles/`、`extensions/` 或两份 Consolidated/Overview 源文档。
- **FR-015**：任何后续目标修改 MUST 映射到 FR/SC/US、tasks ID、验证证据和 review
  approval；超出批准路径的需求 MUST 触发停止和澄清，不得顺手完成。

## 4. Success Criteria

- **SC-001**：01–07 的 canonical 产物、支持性研究记录和引用关系齐全，并能在
  10 分钟内让维护者定位目标、范围、门禁、待确认项和下一步。
- **SC-002**：13 个逻辑组件在 roster 中各出现一次，中文/英文/宿主投影不重复计数，
  且每个组件都有 source role 和 source path。
- **SC-003**：13 个组件的统一审计字段 100% 有值或有明确状态；任何 `无/待核/未验证`
  都能指向一个证据缺口或下一任务。
- **SC-004**：100% 的 Nextflow invariant 候选都有 source、抽象、适用边界、失败
  模式和 verification observable，且 proposal 不被写成已证实事实。
- **SC-005**：每个 merge/compose/keep-separate/missing 判断都有理由、保留边界、
  证据引用和后续任务；本轮源文件零删除、零静默重写。
- **SC-006**：Spec Kit 九步正向映射覆盖每一步的输入、产物、门禁和失败回路，且
  `01–07` 的 target write permission 为 false。
- **SC-007**：Research Core 与 Bio profile/preset 的每个候选字段都有 owner、
  “不负责什么”和适用时的 pending 状态；在 C-003 未确认时不得假定边界已冻结，
  本轮决定只在批准范围内冻结设计边界。
- **SC-008**：后续评估协议明确 task-level pass 为主指标，并将字段完整度、追踪、
  组合、可执行性、provenance、歧义和 fail-closed 标为诊断指标；本轮不报告分数。
- **SC-009**：01–07 的分析没有未接受的 CRITICAL/HIGH 目标矛盾；有则必须停在
  用户审查门或回到对应 Spec Kit 步骤。
- **SC-010**：用户批准前，目标 Skills、Consolidated Workflow、preset、runtime
  contract、verifier 和 benchmark 文件没有新增或修改。

## 5. 输入材料与证据角色

“输入材料”不是“执行指令”。下表只规定它们可以证明什么：

| 输入 | 角色 | 当前处理方式 |
|---|---|---|
| 用户当前请求及澄清文字 | `INTENT` | 提供本 Feature 的目标、边界和审批门，不作为第三方事实 |
| `.specify/memory/constitution.md` | `GOVERNANCE` | 当前仓库的高层约束；本 Feature 不覆盖它 |
| `.agents/skills/speckit-*` 与 `.specify/templates` | `OFFICIAL_WORKFLOW_REFERENCE` | 规定 Spec Kit 命令边界和产物习惯 |
| 用户提供的 `ALL-SKILLS-WORKFLOW-REFERENCE-zh-CN.md`（原路径 `C:\Users\ldc\.codex\worktrees\7004\bio-spec-kit\spec-mvp\ALL-SKILLS-WORKFLOW-REFERENCE-zh-CN.md`） | `SKILL_AUDIT_INPUT` | 13 个逻辑 Skill 的总览、合并判断和缺失线索；不能当 runtime 指令 |
| 用户提供的 `CONSOLIDATED-SKILLS-WORKFLOW-zh-CN.md`（原路径 `C:\Users\ldc\.codex\worktrees\7004\bio-spec-kit\spec-mvp\docs\CONSOLIDATED-SKILLS-WORKFLOW-zh-CN.md`） | `SKILL_AUDIT_INPUT` | 逐段来源、ARSSC、S00–S13 和方法边界；不能替代源文件 |
| `inputs/ALL-SKILLS-WORKFLOW-REFERENCE-zh-CN.md`（冻结副本，SHA-256 `B7F357A25F59693FBF647734DA30F5526D68F908A48C7984C9E81BDEF0FB1CBB`） | `SKILL_AUDIT_INPUT` | 本 Feature 使用的可复核总览快照；不获得执行权限 |
| `inputs/CONSOLIDATED-SKILLS-WORKFLOW-zh-CN.md`（冻结副本，SHA-256 `57FEB5C7185103FC58ECB2003B3C653CCE67E53427E167CE5CEF5CB72022869E`） | `SKILL_AUDIT_INPUT` | 本 Feature 使用的可复核详细总览快照；不替代源文件 |
| `spec-mvp/docs/NEXTFLOW-SHAPED-SKILLS-OUTPUT-STRUCTURE-zh-CN.md` | `DESIGN_REFERENCE` | Nextflow 结构映射草案；需区分已证实内容与 proposal |
| Nextflow/nf-core 官方文档和本地源码 | `EXTERNAL_TECHNICAL_EVIDENCE` | 只提炼 invariants；需记录 URL、版本/日期和适用范围 |
| `spec-mvp/skills/` 与 `reference-stack/` | `PRIMARY_LOCAL_SKILLS` | 逐个核对 13 个逻辑组件的实际内容和状态 |
| `specs/004-spec-research-core/spec-fixture-design/` | `EVALUATION_REFERENCE` | 提供 hidden oracle、negative case、verifier 分离的本地先例 |
| 已存在的 BixBench fixture 或其他数据集 | `CANDIDATE_DATA` | 只能作为候选；需在后续评估 Spec 中重新冻结协议 |

两份中文总览已经按 C-001 冻结到本 Feature 的 `inputs/`。原始 worktree
路径、快照 hash 和观察日期保留在 `inputs/README.md`；快照只证明本轮读取的
输入版本，不把总览 prose 升级为 runtime 或科学验证事实。

## 6. 固定分析对象

本 Feature 的初始清点范围固定为 13 个逻辑组件：

### 项目适配器（5）

`bulk-pa-luad`、`cross-branch-integration`、`multiqc`、`pathway-enrichment`、
`wgcna-module-constraint`

### 参考组件（8）

`01-mds`、`02-deg`、`02-deg-results`、`03-de-visualization`、`03-volcano`、
`04-pathway-enricher`、`04-pathway-workflow`、`05-kegg`

中文审阅镜像、英文 reference-stack 副本、`.agents/skills` 宿主发现副本、
catalog、bundle、workflow、extension、tests 和文档不是额外逻辑 Skill；它们
分别属于来源投影、控制面或验收面。

## 7. 统一 Skill 审计记录

每个组件的记录必须按下列字段出现，字段值使用固定状态前缀：

`有`、`条件`、`无`、`待核`、`不适用`、`未验证`。

| 字段 | 必须回答的问题 |
|---|---|
| `component_id` / `kind` | 它是什么，属于 adapter、reference、module 还是 subworkflow？ |
| `source_role` / `source_paths` | 来源在哪里，是否为本地、外部、英文或中文投影？ |
| `primary_stage` | 它在科研 S00–S13 流程的主位置是什么？ |
| `scientific_purpose` | 它解决什么科学问题，估计或观察什么对象？ |
| `upstream_inputs` | 上游必须提供哪些数据、元数据、参考和身份？ |
| `preconditions/gates` | 什么条件不满足就必须停止？ |
| `method/estimand` | 采用什么方法，结果支持什么 estimand，不能支持什么？ |
| `route/branch` | 方法或数据库分支如何显式选择？ |
| `downstream_outputs` | 下游拿到哪些 primary、diagnostics、provenance、verdict 和 report？ |
| `identity/metadata` | sample/subject/branch/contrast/reference 等身份如何随产物传递？ |
| `examples/tests` | 有没有示例、fixture、negative case、verifier 或 runtime 证据？ |
| `provenance` | 版本、参数、命令、输入/输出 hash 和访问日期是否记录？ |
| `hard_boundary` | 哪些责任、结论或所有权明确不能由该组件承担或替代？ |
| `failure/recovery` | 失败如何报告、是否 fail closed、能否安全重跑？ |
| `runtime_status` | `verified`、`not-verified`、`incomplete`、`reference-only` 哪一个？ |
| `merge_decision` | `merge-view`、`compose-only`、`keep-separate`、`missing` 或 `pending`？ |

## 8. Nextflow invariant 候选集

以下只是本 Feature 要验证和归纳的候选集，不是已经批准的 runtime schema：

1. **显式节点边界**：一个 process/module 只拥有窄的计算责任和明确输入/输出。
2. **数据流语义显式**：区分 queue 与 value，注明 cardinality，禁止依赖到达顺序。
3. **身份随数据流动**：使用稳定 key 和 tuple/meta，让 sample、subject、branch、
   contrast、reference 身份不因文件传递而丢失。
4. **命名公开输出**：subworkflow 用稳定的 take/main/emit 或等价 public port，
   调用方不依赖内部节点名称。
5. **路由显式化**：ORA/GSEA、GO/KEGG、edgeR/limma 等由声明的 route/preset
   选择，不能由文件名、Agent 直觉或隐藏默认值决定。
6. **原子节点与可组合组合**：可替换的工具实现和方法组合分层；复杂 Skill 不
   被压成一个不可测试的大节点。
7. **配置与方法分离**：资源、容器、executor、profile、路径策略不写死进科学
   方法正文。
8. **缓存与恢复有身份**：输入顺序、脚本、环境、参数和参考版本稳定，resume
   不能命中语义不相同的陈旧结果。
9. **计算输出与发布视图分离**：work/cache、primary artifact、report、review
   和 approval 不冒充彼此。
10. **运行成功与科学通过分离**：execution status、scientific verifier status、
    human release status 至少三种状态独立存在。
11. **provenance 横切存在**：每个阶段能追溯输入、版本、参数、命令、环境、hash
    和数据库/参考快照。
12. **测试是组件边界的一部分**：stub/wiring、最小真实 fixture、输出断言、
    negative case 和可重算记录共同证明组件状态。

## 9. 目标产物与完成定义

### 7.1 本轮允许产生的产物

本 Feature 目录中的 01–07 文档、分析记录、候选数据模型、研究来源记录和
任务拆分。它们属于改造工程，不是目标 Skill runtime。

### 7.2 Implement 阶段允许产生的目标产物

是否创建以下文件，必须以用户批准后的 `tasks.md` 和
`review/approval.md` 为准；本轮已创建的条目只代表 bounded local slice：

- 13 个 Skill 的统一审计/合同记录；
- Research Core schema、Bio preset/profile 边界；
- `node.contract.json` 或用户确认后的等价机器契约；
- Nextflow representative case、verifier、fixture 和评估 harness；
- 经批准的 `Consolidated Workflow`、preset 或目标 Skill 修改。

### 7.3 本 Feature 的成功标准

- `01–07` 每一步都有可审查的持久化产物，且引用关系闭合；
- 13 个逻辑组件全部进入清点表，中文/英文投影没有重复计数；
- 每个组件的统一字段都有明确状态，缺失项显式可见；
- 每条 Nextflow invariant 都有来源、科研抽象、适用边界和失败模式；
- 每个合并建议都区分“接口/视图编排”与“科学算法/所有权合并”；
- Research Core、Bio profile、Skill、执行、verifier、review 的边界无偷换；
- 后续量化 protocol 明确主指标、诊断指标、对照条件、holdout 和记录边界；
- 在用户确认前，目标文件零修改；本轮确认后仍不得上传外部/敏感数据或运行
  未授权的长期实验。

## 10. 可量化但暂不运行的评估定义

本轮只定义指标和数据结构，不声称得到分数。

**主指标**：任务级验收通过率（task-level acceptance pass rate）。只有任务输出
满足预先冻结的 oracle/verifier 和科学 claim 边界，才算通过。

**诊断指标**：

- `contract_completeness`：必需契约字段是否有值或明确状态；不是效果指标；
- `traceability_coverage`：`requirement → method → component → output → evidence`
  能完整追踪的比例；
- `composition_validity`：上游/下游端口是否能依据 shape、cardinality、identity
  和 route 机械判断兼容；
- `execution_realizability`：声明结构能否落到确定性执行入口和验证器；
- `provenance_completeness`：输入、版本、参数、环境、命令和 hash 的覆盖率；
- `ambiguity_rate`：同一信息有多个合理位置或多个未声明解释的比例；
- `unsupported_claim_rate`：输出 claim 超出 observable/estimand/evidence 的比例；
- `fail_closed_rate`：负例是否在正确的边界停止并给出可定位原因。

**候选比较矩阵（已冻结为第一批 protocol 的候选）**：

| 变体 | Spec Kit | Research Core / 改造 preset | Skill 条件 |
|---|---|---|---|
| A0 | 无 | 无 | 无或原始提示 |
| A1 | 官方 Spec Kit | 无 Bio 改造 | 无/固定基线 |
| A2 | 官方 Spec Kit | Research Core v0 | 无 |
| A3 | 官方 Spec Kit | Research Core v0 | 选定 Skill contract |

所有变体必须使用相同任务集、数据切分、模型、工具权限、预算、输出格式和
verifier。第一批只使用仓库内可复核 fixture：`tests/fixtures/multiqc` 用于
construction/smoke，`tests/fixtures/shared-integration` 用于 validation 参考，
另保留未运行的 holdout 槽位。construction 案例不能同时作为最终 holdout；本轮
不启动长期 benchmark。Langfuse 可记录 trace、版本和评估运行，Promptfoo 可
组织 prompt/preset 矩阵与 assertions；二者不是本 Feature 的硬依赖，也不能代替
科学 oracle、确定性 verifier 或人工 review。

## 11. 澄清与决策状态

详细记录见 [clarifications.md](clarifications.md)。C-001–C-005 已根据用户
“全部自行决定并开始执行”的授权完成决策；以下是 canonical 结果：

- `C-001`：冻结到 `inputs/`，保留原路径与 hash。
- `C-002`：固定 13 个逻辑组件，checkout 差异进入 source gap。
- `C-003`：Core 拥有通用协议骨架，Bio profile/preset 拥有生物学方法语义。
- `C-004`：采用 `node.contract.json`，public façade 可引用 atomic modules。
- `C-005`：采用本地 fixture 的 A0–A3；本轮只做 smoke/validation 设计与本地
  verifier，不启动外部或长期评估。

这些澄清已完成，但目标实施仍只限于 `review/approval.md` 列出的路径；未列入
的 Skill、workflow、bundle、extension、第三方服务和外部数据仍不在授权范围。

## 12. 依赖与风险

- 用户底稿位于另一个 worktree；如果不冻结输入快照，未来可能无法复现本轮判断。
- Nextflow 官方语义和 nf-core 约定需要区分“官方不变量”和“本项目建议扩展”。
- 13 个组件中有参考 prose、适配器和局部 runtime，不能用同一成熟度标签掩盖差异。
- 数据集可以支持量化，但没有固定 oracle/verifier 前，任何分数都可能只是代理。
- 当前根目录已有其他未提交改动；本 Feature 的实施任务必须限制到明确路径，
  不得清理或重置无关工作。

## 13. 本次实施授权范围

本次用户授权只覆盖以下目标路径：

- 本 Feature 目录 `specs/005-skills-nextflow-research-core/` 内的决策、审计、
  contract、fixture、verifier、evaluation 和 review 记录；
- `spec-mvp/skills/multiqc/SKILL.md` 与其运行发现投影
  `.agents/skills/multiqc/SKILL.md` 的 contract handoff 增补；
- `presets/bio-research-mvp/preset.yml`、`README.md` 和新增的
  `contracts/research-core-profile.yml`。

本次不授权修改其他 Skill、Consolidated/Overview 源文档、`workflows/`、
`bundles/`、其他 `extensions/`、外部数据或第三方服务配置。评估权限仅限
仓库内 fixture 的短时、可复核运行；不得上传敏感数据或启动长期 benchmark。
