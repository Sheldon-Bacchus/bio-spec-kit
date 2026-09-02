# 04 — 改造工程 Plan

**Feature**：`005-skills-nextflow-research-core`  
**状态**：`BOUNDED_SLICE_REMEDIATED / REUSABLE_CORE_NOT_GENERALIZED`  
**依据**：[spec.md](spec.md)、[constitution.md](constitution.md)、
[clarifications.md](clarifications.md)

## 0. 已冻结决策

本计划依据用户于 `2026-09-02 Asia/Shanghai` 的授权执行：

- 外部两份中文总览冻结到 `inputs/`，原路径与 SHA-256 保留在 manifest；
- 13 个逻辑组件固定为 5 个项目适配器 + 8 个 reference 组件；checkout 差异
  进入 source gap；
- Research Core 拥有通用生命周期、contract、identity/provenance、gate、
  verifier 接口和评估协议骨架；Bio profile/preset 拥有生物学语义与方法路由；
- public component contract 采用 `node.contract.json`，可引用 atomic modules；
- 第一批使用本地 fixture 的 A0–A3 protocol，实施和验证只做短时本地运行，不
  上传数据、不安装第三方服务、不启动长期 benchmark。

## 1. 推荐执行顺序

```text
冻结输入与证据角色
    ↓
官方 Spec Kit 9 步边界审计
    ↓
提取 Nextflow/nf-core invariants
    ↓
固定 13 个逻辑 Skill roster 并逐项填统一字段
    ↓
正向映射：Spec Kit 9 步 → 改造活动 → 产物/门禁
    ↓
反向抽象：13 Skills + Nextflow → Research Core v0
    ↓
定义 Core / Bio preset / Skill / Execution / Verifier 边界
    ↓
设计 fixture、oracle、指标与对照矩阵（先设计，运行权限单独冻结）
    ↓
只读一致性审计 → 用户批准 → 批准范围内 Implement → Converge
```

顺序是研究依赖，不是把九个 Spec Kit 步骤变成九个 Nextflow 节点。Spec Kit
负责本 Feature 的生命周期，Nextflow invariants 负责结构约束，13 Skills
提供经验材料，真实任务/数据集才提供外部验证。

## 2. 架构边界与数据流

```text
用户意图 / 参考材料 / 本地文件
              ↓  (source ledger)
        Feature Spec Kit artifacts
   constitution → spec ↔ clarify → plan
                    ↓ checklist → tasks → analyze
                    ↓ user approval gate
                  implement → converge

Nextflow docs + nf-core examples ─┐
13 Skill source + consolidated docs ─┼→ invariant / contract model
existing tests + candidate datasets ─┘              ↓
                                    Research Core v0 + Bio profile proposal
```

### 所有权表

| 层 | 输入 | 输出 | 明确不拥有 |
|---|---|---|---|
| Spec Kit feature | 用户目标、根 constitution、源记录 | spec/plan/tasks/gates | 领域数值计算 |
| Source ledger | 文档、源码、官方 URL、版本 | FACT/INFERENCE/PROPOSAL/UNKNOWN | 运行授权 |
| Invariant model | Nextflow/nf-core 结构证据 | invariant、失败模式、科研映射 | 具体工具选择 |
| Skill audit | 13 个组件及其源文件 | 统一字段、状态、合并判断 | 自动删除/合并 |
| Research Core | invariant + Skill 共性 + Spec 生命周期 | 跨领域契约候选 | 生信专用方法 |
| Bio profile | 生物学语义、S00–S13、estimand | Bio preset 候选 | 改写官方 Spec Kit |
| Evaluation design | 任务、数据、oracle、变体 | 评估 protocol | 没有 oracle 的分数 |

## 3. 分阶段工作

### Phase 0 — 输入冻结与范围闸门

1. 记录所有输入的路径、来源角色、观察日期和可得版本/hash。
2. 将用户请求、参考文档、官方命令模板和仓库源码分开标注。
3. 冻结 13 个逻辑 Skill 的初始 roster；中文/英文镜像只作投影。
4. 记录当前 checkout 与外部 worktree 的差异，不通过复制或猜测消除差异。

**输出**：`research.md` 的 source ledger、`spec.md` 的输入表、`inputs/` 冻结快照、
roster manifest。

**门禁**：任何输入如果只有路径而没有可读取内容，状态必须为 `UNKNOWN` 或
`MISSING_IN_CHECKOUT`。

### Phase 1 — 官方 Spec Kit 执行协议确认

对官方九步只确认“本 Feature 如何执行”，不把它们写成目标 runtime：

| 步骤 | 本 Feature 的活动 | 必须产生/检查 |
|---|---|---|
| 01 Constitution | 约束范围、证据、接口、失败、审批和评估边界 | feature constitution draft |
| 02 Specify | 固定问题、输入、输出、非目标、成功标准 | `spec.md` |
| 03 Clarify | 解决 roster、core 边界、contract 名称、评估矩阵等高影响歧义 | `clarifications.md` + spec 回写 |
| 04 Plan | 设计来源研究、正向映射、反向抽象和验证顺序 | `plan.md` + research/data-model/contracts 计划 |
| 05 Checklist | 检查需求完整性、可测量性、字段和门禁是否写清楚 | `checklists/requirements.md` |
| 06 Tasks | 把分析和后续修改拆成可追踪任务 | `tasks.md` |
| 07 Analyze | 只读检查以上产物是否矛盾、遗漏或目标漂移 | `analysis.md` |
| 08 Implement | 获得用户批准后按精确路径读写目标文件和运行本地 smoke | 本轮仅执行批准的 MultiQC/preset 切片 |
| 09 Converge | 依据初始 spec/plan/tasks/证据回验并追加未完成项 | 本轮在实现和子 agent 审计后执行 |

### Phase 2 — Nextflow invariant 提取

对每条候选规则建立以下记录：

```text
invariant_id
source_kind / source_path / source_url
confirmed_statement
scope_and_assumption
scientific_skill_translation
failure_mode
verification_observable
owner_layer
status: FACT | INFERENCE | PROPOSAL | UNKNOWN
```

至少覆盖：process/module 边界、channel queue/value、tuple/meta 身份、稳定 key
对齐、named `take/emit`、显式 route、atomic/composable subworkflow、
parameter/reference 分离、profile/environment、cache/resume identity、
work/publish 分离、provenance、stub/fixture/negative test、execution/scientific/
review 三态分离。

**禁止**：从一个 Nextflow 示例直接推断所有 Bio Skill 都必须使用同一 DSL；从
`exit 0` 或文件存在直接推断科学结果通过。

### Phase 3 — 13 Skill 统一审计

按 `component_id` 逐项读取源文件，使用 [spec.md](spec.md) 第 5 节的固定字段。
每个字段必须有状态值：`有 / 条件 / 无 / 待核 / 不适用 / 未验证`。

审计顺序：

1. 来源和逻辑计数；
2. scientific purpose 与 primary stage；
3. upstream input 与 preconditions；
4. method/estimand 与 route；
5. downstream output 与 identity；
6. example/test/provenance/runtime status；
7. hard boundary、failure/recovery；
8. merge decision 和 evidence。

复杂组件可以拆为内部 module，但不能因此改变原始 Skill 的逻辑计数；拆分
必须注明 `parent_component_id` 和新的所有权边界。

### Phase 4 — 正向映射

正向映射回答：**Spec Kit 每一步要求本改造工程做什么，以及它约束哪个对象。**

| Spec Kit 步骤 | 研究动作 | 产物中的对象 | 失败回路 |
|---|---|---|---|
| Constitution | 确定证据、边界、禁止行为 | feature principles/gates | 回到 Constitution |
| Specify | 定义目标和完成判据 | FR/SC/US/inputs/outputs | 回到 Specify |
| Clarify | 暴露并解决关键冲突 | clarification decisions | 回到 Specify |
| Plan | 设计阅读、抽取、映射、抽象方法 | source/invariant/audit/eval plan | 回到 Clarify/Plan |
| Checklist | 把隐含质量要求前置 | requirements-quality checks | 回到 Specify/Plan |
| Tasks | 把计划变成动作和证据 | task IDs/paths/dependencies | 回到 Plan/Tasks |
| Analyze | 检查覆盖、冲突、孤儿和偷换 | findings/report | 回到相应阶段 |
| Implement | 修改目标并运行验证 | target artifacts/evidence | 失败停机 |
| Converge | 以原始 spec 回验实际结果 | convergence/remaining tasks | 回到 Implement |

这张表不能反过来证明任何 Skill 已实现；它只定义执行协议。

### Phase 5 — 反向抽象 Research Core v0

从“Nextflow invariants + 13 Skill 真实需求 + Spec Kit 生命周期约束”共同归纳，
而不是把任一来源直接当成答案。抽象过程：

1. 将所有审计字段分为科学语义、接口结构、执行证据、质量门和人工治理；
2. 识别跨组件共有且不依赖某一算法的字段；
3. 识别只属于 Bio profile 的字段（如 organism、S00–S13、ORA/GSEA、FDR、
   tested universe 等）；
4. 识别只属于具体 Skill 或执行器的字段（如 edgeR 函数、KEGG API、MultiQC
   CLI、Nextflow process body）；
5. 用未参与抽象的 representative case 做 schema fit 检查；
6. 把不能表达的内容写成 `gap`，不通过新增泛化字段掩盖冲突。

### Phase 6 — 表示层和合同草案

候选三层表示：

| 表示 | 主要读者 | 内容 | 当前阶段 |
|---|---|---|---|
| `SKILL.md` | 人和被激活的 Agent | 触发、方法边界、科学解释、失败、阅读入口 | 只设计，不改目标 |
| `node.contract.json` | Agent、路由器、verifier | 静态 capability、port、shape、cardinality、identity、route、gate、evidence、façade/module bindings | C-004 已定名；不含运行态 |
| `run-status.schema.json` | verifier、review、evaluation | 单次 run 的三态、checkout identity、manifest、command、environment 和 approval link | 与静态 capability 分离 |
| `main.nf`/scripts | 执行环境 | 真正的 process、channel、工具和 named outputs | 不在本轮实现 |

下游还要有 `tests/`、`verdict`、`provenance` 和 `review/approval`。report 是
视图，不能反向生成统计结果；人工批准不是普通 process 输出。

### Phase 7 — 量化 protocol 设计

后续评估必须先构造任务封装：

```text
case-input + task.md + environment
       + hidden-oracle/reference
       + deterministic-verifier
       + human-rubric（必要时）
       + trace/eval record
```

设计规则：

- construction 集合可包含 13 个 Skill，但最终 validation 必须包含 unseen
  Skill、unseen workflow 或真实项目案例；
- 同一 case 在比较变体间保持数据、工具、模型和预算不变；
- 每个 case/variant 的 eligibility 必须在运行前冻结；资源/权限/oracle/verifier
  缺失只能记录为显式 pre-run exclusion，不能静默改变分母；
- eligible case 的 timeout、执行错误、verifier error/fail、缺少输出、malformed
  trace 和 unsupported claim 均计为失败；不能用“未完成”从分母删除；
- A0–A3 每个 eligible case/variant 固定 3 次重复，记录稳定 seed 或
  `seed_status: unavailable`；默认 strict determinism 要求规范化输出 hash 一致，
  任一重复失败或 hash 不一致则 cell 失败；
- 先运行 oracle/verifier，再运行 Agent；
- 主指标为 task-level pass；字段/trace 指标只作诊断；
- 任何调优都只能使用 construction/dev，holdout 只用于最终比较；
- Langfuse 记录 trace、prompt/preset/version/eval run；Promptfoo 组织矩阵、
  assertions 和结果导出；不能取代领域 verifier；
- 存在敏感数据时，外部服务必须先通过数据权限门。

### Phase 8 — 批准范围内的首个实现切片

本次只实现 `multiqc` representative component：

1. 在本 Feature 内创建 `contracts/multiqc/node.contract.json`、最小 fixture
   引用、negative case、结构化 deterministic verifier 和 provenance 记录；
2. 在 `spec-mvp/skills/multiqc/SKILL.md` 及其 `.agents/skills` 投影中增加
   contract handoff，不能写入 Spec Kit 九步；
3. 在 `presets/bio-research-mvp/` 增加 Research Core/Bio profile contract
   绑定；不修改其他 Skill、workflow、bundle 或 extension；
4. 使用已有 `extensions/bio-multiqc` wrapper 做本地 fixture smoke，运行成功、
   scientific verdict 和 human release 三种状态分别记录。

本阶段不把 MultiQC 报告生成升级成 QC 通过，也不把本地 smoke 结果升级成
Research Core 的科学有效性结论。

## 4. 计划产物与本轮实现产物

用户已批准本 Feature 的 bounded scope；以下清单同时作为本轮的预期与实际产物
索引。实际运行证据位于 `evaluation/runs/`，未授权的长期评估不在其中：

```text
specs/005-skills-nextflow-research-core/
├── research.md                         # 来源与 invariant evidence ledger
├── data-model.md                       # Core/Bio/Skill/port/gate/eval entities
├── contracts/
│   ├── skill-audit-record.yml           # 13 Skill 审计记录形状
│   ├── node-contract.schema.json        # 机器契约候选 schema
│   ├── run-status.schema.json            # execution/scientific/release + run provenance envelope
│   ├── input-manifest.schema.json        # repository-relative input evidence
│   ├── artifact-manifest.schema.json     # repository-relative output evidence
│   ├── validate_contracts.py              # schema + cross-field contract gate
│   └── multiqc/node.contract.json         # 首个 representative contract
├── mappings/skill-to-invariant.tsv      # Skill → invariant/stage 映射
├── merge-decisions.md                   # merge/compose/keep/missing 判断
├── evaluation-protocol.md               # 本地 fixture A0–A3 protocol
├── evaluation/validate_protocol.py      # eligibility/repetition/failure protocol gate
└── quickstart.md                        # 审阅和后续验证入口
```

C-001–C-005 已批准；若实施中发现输入 hash、roster、contract 或评估边界发生
变化，必须停止并追加新的 clarification，而不是静默迁移路径。

## 5. Implement 入口条件

以下条件是进入本轮 bounded 08 Implement 的门槛；更广泛的目标修改仍需重新过门：

- [x] 用户批准 `constitution.md` 的 feature-level 原则；
- [x] `spec.md` 的 FR/SC/US 和非目标没有关键遗漏；
- [x] 五项高影响澄清已回答或有明确延期理由；
- [x] `checklists/requirements.md` 没有未解释的关键失败项；
- [x] `tasks.md` 中本轮实施任务都有来源、路径、依赖和验证证据；T026/T028 的延期已显式记录；
- [x] `analysis.md` 没有未接受的 CRITICAL/HIGH 目标矛盾；
- [x] 用户明确批准要修改的目标路径和是否开始长期评估；长期评估未批准，
      仅批准本地短时 fixture smoke；
- [x] 本轮没有把外部数据、第三方安装或运行权限默认为已批准。
- [x] 原 bounded slice 的独立子 agent 审计已记录；最终审计 verdict 为 `PASS`，
      仅关闭该 bounded local slice，T026/T028/T029 和 A-007 保持显式限制。
- [x] fresh-context remediation 的 B/S findings 已由同一套校验器、正负例和五轴
      review 重新确认；bounded slice 已修复，但 reusable Core 仍因 unseen
      validation 未运行而保持 NOT_GENERALIZED。

## 6. 失败与恢复

- 来源不可读：保留 `UNKNOWN`，补 source capture 任务；不凭摘要填充。
- 13 个 roster 不一致：回到 C-002 和 Specify，不更新分母后继续算覆盖率。
- Nextflow 规则只有示例无权威依据：标 `PROPOSAL`，不能写成 invariant gate。
- 两个 Skill 的 estimand/身份/失败边界不兼容：保留独立，允许只合并 handoff。
- 合同字段无法表达新案例：记录 schema gap，回到反向抽象，不立即加任意字段。
- 评估没有 oracle/verifier：只完成 protocol 设计，禁止输出效果分数。
- Implement 中出现超出批准路径的需求：停止，追加澄清/任务，不能顺手完成。
