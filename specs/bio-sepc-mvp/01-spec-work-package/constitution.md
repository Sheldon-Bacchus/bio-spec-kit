<!--
Feature-level constitution for the meta-project "Skills + Nextflow + Research Core".
This is a feature-level binding for this feature only. It does not replace or
modify `.specify/memory/constitution.md`. The bounded implementation scope is
approved by the user decision recorded in `review/approval.md`.
Status: APPROVED_WITH_BOUNDED_SCOPE — broader changes still require a new gate.
-->

# 01 — 改造工程 Constitution

**工程名称**：Skills 归类、Nextflow invariants 与科研 Research Core 改造

**文档角色**：本文件是这个改造工程自己的 feature-level governance draft。
仓库根目录的 `.specify/memory/constitution.md` 仍是更高层的项目宪法；本文件
只增加本工程的边界和门禁，不得降低根宪法的要求。

**当前状态**：`APPROVED_WITH_BOUNDED_SCOPE`

## 不可违反的原则

### I. Spec Kit 是执行协议，不是本轮的目标内容

本工程必须把“改造现有 Skills、提炼 Nextflow 结构不变量、设计科研 preset”
作为一个独立的 Spec Kit feature 来管理。Spec Kit 的九步描述本工程如何推进，
不等于把九步写入目标 Skill、Consolidated Workflow 或科研运行时。未经过
`01–07` 审查和明确批准，不得进入 `08 Implement`；本轮只在
`review/approval.md` 列出的路径内执行，未列路径仍受同一门禁约束。

### II. 证据、推断、提案必须分层

每个结论必须标明它属于以下哪一层：

- `FACT`：可以回到文件、源码、官方文档或可复核运行记录；
- `INFERENCE`：根据多个事实推导出的暂时判断；
- `PROPOSAL`：为了形成 Research Core 而提出的设计方案；
- `UNKNOWN`：当前材料不能决定，必须保留为缺口或澄清项。

不得把用户提供的自然语言意图、参考 Skill 的 prose、仓库中存在的文件或
第三方项目自报指标，直接写成已验证的 runtime 能力。

### III. 先定义科学语义，再判断能否合并

Skill 的重叠、可合并、不可替代和缺失判断，必须比较至少以下对象：研究问题、
estimand、输入对象、前置条件、方法/路由、输出对象、身份键、失败边界和验证
证据。仅凭目录名称、相邻位置、文字相似或都能生成一个报告，不得宣布合并。

“合并”默认只表示统一阅读入口或编排接口；删除源文件、改变所有权、合并
不同 estimand 的算法或改变运行行为，都必须作为独立任务并重新过门禁。

### IV. 接口和身份必须显式且可组合

每个候选 Skill/组件都必须能够用固定记录表达：

`component_id → upstream input → preconditions → method/estimand → route → downstream output → evidence → failure/recovery`。

输入和输出还必须在适用时注明 shape、cardinality、queue/value 语义、tuple/meta
身份、版本、引用数据和 hash。`sample_id`、`subject_id`、`branch_id`、
`contrast_id`、`reference_release` 等身份不得依靠文件名、行号或到达顺序推断。

### V. Nextflow 只提供结构先验，不取代 Spec Kit 或科研方法

本工程提炼 Nextflow/nf-core 的不变量，不把 Nextflow DSL 当成 Bio Skill 的
唯一表示，也不把它当成科研结论判定器。重点约束包括：显式端口、queue/value
区别、metadata 随 payload 传递、稳定 key 对齐、named outputs、原子节点、
可组合 subworkflow、显式路由、参数/参考与方法分离、环境与 profile 分离、
缓存/resume 身份、provenance 和测试。

### VI. 表示层分离，契约层连接

人读的 Markdown、Agent/校验器读的 JSON/YAML、Nextflow/R/Python/CLI 的执行
代码、verifier 与人工 review 记录，各自承担不同职责。它们只能通过稳定的
`component_id`、版本、输入输出契约和 provenance 关联，不得为了“统一阅读”
把三者揉成一个既不能可靠执行又不能快速审阅的文件。

### VII. 未知、冲突和失败必须 fail closed

缺失信息、互相冲突的来源、未验证的依赖、没有 tested universe、身份无法对齐、
外部数据库不可追溯、敏感数据权限不清或方法路由未声明时，必须保留为
`UNKNOWN / BLOCKED / NOT_VERIFIED`，不得由 Agent 静默补全。生成 HTML、进程
退出码为 0 或文件存在，不得自动等同于科学通过或可发布。

### VIII. 量化必须面向任务结果，不把文档完整度冒充效果

后续评估必须优先测任务级正确性、验收通过率、可执行性和科学 claim 边界；
字段完整度、可追溯覆盖率、组合有效性、provenance 完整度和歧义率只能作为
诊断指标，不能单独作为“优化成功”。比较条件必须固定任务/数据、模型、工具
预算、验证器和输出要求，并保留未参与设计的 validation/holdout 案例。

### IX. 可逆、可追溯、不可偷换范围

本工程第一阶段不得删除、移动、覆盖或静默重写原始 Skill、参考材料、现有
workflow、preset、测试和运行路径。所有分类和抽象都必须保存 source path、
观察日期、版本/commit（若可得）和状态。任何新增目标修改必须有对应
`FR/SC/US`、任务 ID 和审查记录。

## 研究对象与所有权边界

| 层 | 本工程中负责什么 | 不负责什么 |
|---|---|---|
| Spec Kit | 本工程的意图、计划、任务、门禁、审查和收敛 | 不证明领域程序已经算对 |
| Nextflow invariants | 可组合计算图的结构约束 | 不定义生物学问题或人工发布结论 |
| Research Core | 跨项目共用的科研契约、路由、证据和评估抽象 | 不直接替代领域算法 |
| Bio profile/preset | 生信术语、方法边界、数据/参考语义 | 不拥有通用生命周期协议 |
| Skill/component | 一个窄能力的触发条件、方法语义和接口 | 不静默改写上游数值结果 |
| Execution layer | R/Python/CLI/Nextflow 的确定性计算和连接 | 不决定研究问题与 claim |
| Verifier/reviewer | 内容检查、机器 verdict、人工批准 | 不把警告自动升级为结论 |

## 强制门禁

1. **Evidence gate**：13 个逻辑 Skill 的来源、计数口径和现状可回溯；外部
   参考和用户意图不混成运行指令。
2. **Contract gate**：统一审计字段、Nextflow invariants 和 Research Core
   候选边界已经写明；缺失字段显式标记，不用空白掩盖。
3. **Consistency gate**：`spec.md`、`clarifications.md`、`plan.md`、
   `checklists/requirements.md`、`tasks.md`、`analysis.md` 之间没有未说明的
   目标漂移、术语漂移或任务孤儿。
4. **User approval gate**：用户明确批准 01–07 及关键澄清后，才允许创建或修改
   目标 Skills、Consolidated Workflow、preset、contract runtime 或 benchmark。
5. **Evaluation gate**：任何量化运行必须先固定案例、oracle/verifier、比较
   条件、数据权限和记录方式；本轮不以“看起来更完整”宣布通过。

## 治理

- 本文件的任何修改必须写明受影响原则、理由、迁移影响和版本变化。
- 新增或修改一个原则属于 minor 变化；改变现有原则的约束方向属于 major
  变化；措辞澄清且不改变约束属于 patch 变化。
- 用户没有确认的关键澄清必须保持 `PENDING_USER_CONFIRMATION`，不能在
  `Implement` 阶段通过默认值偷偷解决；本轮 C-001–C-005 已由授权记录明确
  决定，延期项仍保留为 `UNKNOWN/NOT_RUN`。
- 本文件批准后仍不能授权超出 `spec.md` 的目标文件；目标文件范围由
  `tasks.md` 的具体任务和用户的实施批准共同决定。

**版本**：`0.1.0`（patch：批准状态与边界文案收口，不改变约束方向）  
**创建日期**：`2026-09-02`  
**批准状态**：`本轮已由用户委托授权；范围受 review/approval.md 限定`
