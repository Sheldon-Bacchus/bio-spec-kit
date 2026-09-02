# Bio-Spec Kit 总参考与改造计划

**日期**：2026-08-28  
**项目**：`E:/all-agent-workspace/codex-projects/bio-skills/bio-spec-kit`  
**状态**：已完成第一轮机制审计、Skill 资料审计、Evidence Closure Kernel MVP 和 MultiQC vertical slice；当前进入统一收敛阶段，仍不修改上游 Spec Kit 基线。

这份文件是当前可读取的相关对话、仓库内设计资料、本地 Spec Kit 源码、官方文档和已完成 MVP 实验的统一参考。它不是逐字聊天记录，而是把结论、证据、边界、决定、未决问题和后续任务集中在一个地方。

## 0. 统一阅读入口：先看这里

### 0.1 本轮整理的范围

本轮把以下几条原本分散的主线放到同一个模型中：

1. 单一 Skill 的来源、结构、触发、调用、失败和回归验证；
2. 科研设计验证，包括问题、假设、estimand、实验单位、统计和 QC；
3. 目标/标的/Claim 验证，包括证据是否支持指定范围内的主张；
4. 当前 Feature Spec 如何选择具体 Skill、方法和 runtime；
5. Spec Kit 官方的 constitution → specify → plan → tasks → implement/converge 流程；
6. Matsen walkthrough 展示的 MVP、真实执行、vertical slice 和逐级扩展；
7. `Evidence Closure Kernel` 与 `MultiQC vertical slice` 两个不同层级的 MVP；
8. 科研 Agent、Skill、Spec、Workflow 和最终产物的多维评测。

附件截图只显示 Codex 对话标题，不能作为这些对话的正文或新的项目指令。本文件只把能够从相关任务记录和当前仓库核实的内容纳入；没有正文证据的历史标题不被当作已批准需求。

### 0.2 先分清五种状态

| 状态 | 含义 | 当前例子 |
|---|---|---|
| `implemented_verified` | 已有代码、测试或真实运行证据 | MultiQC 本地 vertical slice、Evidence Kernel 本地测试 |
| `audited_adapter` | 已审计、可发现或已做薄适配，但未接通完整 runtime | `bulk-pa-luad`、`cross-branch-integration`、`pathway-enrichment`、`wgcna-module-constraint` |
| `design_reference` | 用于指导设计的讨论稿或外部案例 | `references/research-spec-kit-mvp/01–05`、Matsen walkthrough |
| `candidate_not_active` | 已有本地文件，但还未被选为默认或未完成官方运行验证 | `presets/bio-research-mvp`、`workflows/bio-research-mvp` |
| `unresolved` | 需要用户或后续实验确认，不能自动定案 | Skill 版本政策、统一状态名、目标验证的具体实例 |

不能因为一个文件存在，就把它升级成已实现；不能因为一次 demo 通过，就把整个 Bio-Spec Kit 或真实科研结论标成完成。

### 0.3 两个 MVP，不是一个 MVP

当前有两个互补的 MVP：

```text
Evidence Closure Kernel
  └─ 研究语义 MVP：Question → Observable → Validation → Claim → Provenance

MultiQC vertical slice
  └─ 执行链 MVP：fixture → Skill → wrapper → real executable → artifact → verifier
```

前者证明“研究主张如何被约束和降级”；后者证明“真实工具链如何被调用并留下可核验证据”。两者都不是完整 Research Spec Kit，也不是完整生产级生信流程。

### 0.4 总体架构

```text
用户/研究者定义问题、范围和判断边界
              ↓
Research Constitution / Bio Profile
              ↓
Feature Spec：Question、Hypothesis、Estimand、Inputs、Acceptance
              ↓
候选 Skill 与方法比较
              ↓
Plan：选定方法、runtime、参数、验证和 provenance
              ↓
Tasks：按依赖拆成可执行、可验证任务
              ↓
Skill + Extension + Workflow 调用确定性 runtime
              ↓
Run / Artifact / Manifest / Verifier
              ↓
Research Claim：supported / not_supported / inconclusive / not_evaluable
              ↓
人工复核与 release
```

核心原则：Spec 定义应该发生什么，Skill 说明某种能力如何使用，runtime 证明实际发生了什么，verifier 检查两者是否一致，人工负责人决定科学结论是否可以发布。

### 0.5 三层验证与一条执行验证

以后不要把“验证”当成一个模糊的 `true/false`。至少分为：

| 层级 | 主要问题 | 典型证据 |
|---|---|---|
| 单一 Skill 验证 | 这个 Skill 是否来源明确、能正确触发、输入输出清楚、失败会停、没有被静默改写？ | source manifest、版本/commit、hash、调用合同、负例、回归测试 |
| 科研方法验证 | 研究设计、实验单位、对照、配对、批次、统计模型、QC 和假设是否适用？ | design record、方法比较、诊断、敏感性分析、专家复核 |
| 目标/标的/Claim 验证 | 产生的 observable 和独立/正交证据是否支持指定范围内的主张？ | evidence registry、holdout/replication、decision rule、claim record |
| 真实执行验证 | 指定输入是否真的经过指定工具链产生了结果？ | command、version、exit code、stdout/stderr、artifact 内容、input/output hash |

前三层回答“是否可以相信或使用”；最后一层回答“是否真的执行过”。任何一层失败，都不能由 Agent 用一段解释文字补成通过。

本矩阵的可执行拆分见 [`spec-mvp/docs/evaluation-matrix.md`](spec-mvp/docs/evaluation-matrix.md)：其中把 FastQC/MultiQC、DEG、shared 149、GO/KEGG 分别映射到 Skill、科研方法和完整科研结果三类测试，并列出当前 MVP 缺口。

### 0.6 当前总工作顺序

```text
A. 统一文档、来源和边界
→ B. 以 MultiQC 完成第一个真实执行切片（MVP-0A）
→ C. 把已有 PA/LUAD DEG 规格化成固定输入
→ D. 用 `cross-branch-integration` 重算 shared 149（MVP-0B）
→ E. 把结果接入 manifest、verdict、Claim 和人工 gate
→ F. 在 0B 稳定后再接 offline pathway slice
→ G. 再恢复 DEG runtime、WGCNA 和更高层验证
```

这里的主线不是重新评价已经得到的科研数字，而是把“已经能跑、能重复跑”的能力变成 Feature Spec、wrapper、artifact contract 和可重跑 MVP。工具复核与 E1/E2/E3 仍然是后续门禁，但不能阻挡第一条真实 vertical slice。

## 1. 当前方向的纠正

### 1.1 不是“增加几个 Markdown Skill”

目标是创建一个面向生物信息学的新 Spec Kit process harness：

```text
Spec Kit 上游能力
        ↓
Bio-Spec Kit preset / extension / workflow / verifier
        ↓
面向生信的规格、决策、执行和验证过程
```

上游 `spec-kit` 只作为基线、来源和升级参照。当前不直接修改它的 checkout。

### 1.2 关于 AIGC 的前置说明

此前把某种 AIGC 角色表述成用户已经提出的要求，是 Assistant 自行添加的假设，不应当作为用户原话或项目硬约束保存。

本项目真正需要先解决的是：用户输入可能是不完整、乱序、相互矛盾或只包含候选方法；系统不能因此强行补全、强行执行或把默认值伪装成事实。

### 1.3 `bulk-pa-luad` 不是上游项目名

`bulk-pa-luad` 是当前项目临时使用的本地标签，不是确认过的开源项目或标准工具名称。它把疾病场景、配对设计和分析方法混在了一起。

建议后续拆为：

```text
Skill 能力：bulk-differential-expression
Preset：paired-case-control
场景：LUAD paired tumor-normal
Runtime adapter：R edgeR / limma
```

`limma2` 也不能未经确认地当成正式软件名；需要确认它是否指 `limma` 的 paired/block 设计或项目内部名称。

## 2. 三个核心的边界

### Spec Core

负责记录：

- 生物学问题和研究目标；
- estimand 或主要比较；
- 样本和实验设计；
- 输入、参考版本和数据身份；
- 用户可观察的输出；
- 验收标准；
- 已知、未知、冲突和假设；
- 当前不能继续的阻塞条件。

### Agent Skills Core

负责告诉 Agent 某种能力如何使用，包括：

- 什么时候适用；
- 前置条件；
- 需要读取哪些参考资料；
- 如何调用 wrapper 或工具；
- 哪些情况必须停止；
- 输出和验证证据是什么。

Skill 不是 runtime，也不是安全沙箱。

### Execution / Workflow Core

负责：

- 调度命令和 workflow；
- 执行 Python、R、CLI、MultiQC；
- 保存 stdout、stderr、exit code、日志和 artifacts；
- 持久化 run state；
- 执行确定性 verifier。

它独立于 Spec Core。Spec 描述“应该发生什么”，runtime 证明“实际发生了什么”。

## 3. 当前项目结构和关键位置

### 上游 Spec Kit 基线

```text
E:/all-agent-workspace/codex-projects/bio-skills/spec-kit/
```

核心 command templates：

```text
spec-kit/templates/commands/specify.md
spec-kit/templates/commands/plan.md
spec-kit/templates/commands/tasks.md
spec-kit/templates/commands/implement.md
spec-kit/templates/commands/converge.md
```

核心 templates：

```text
spec-kit/templates/spec-template.md
spec-kit/templates/plan-template.md
spec-kit/templates/tasks-template.md
spec-kit/templates/constitution-template.md
```

实现代码：

```text
spec-kit/src/specify_cli/
spec-kit/src/specify_cli/integrations/
spec-kit/src/specify_cli/presets/
spec-kit/src/specify_cli/extensions/
spec-kit/src/specify_cli/workflows/
```

Codex integration：

```text
spec-kit/src/specify_cli/integrations/codex/__init__.py
spec-kit/src/specify_cli/integrations/base.py
```

### 当前 Bio-Spec Kit 项目

```text
bio-spec-kit/
├── presets/bioinformatics/       # 当前项目 preset；下一步只改这里
├── extensions/                  # 外部工具、确定性检查和新命令
├── workflows/                   # 可暂停、可恢复、可分支的运行编排
├── bundles/                     # 以后打包 preset/extension/workflow
├── .agents/skills/              # Codex 实际发现的项目 Skill
├── spec-mvp/skills/             # Skill 审计和暂存副本
├── specs/                       # feature 级 Spec Kit artifacts
├── tests/fixtures/              # 最小可复现输入
└── vendor/sources/              # 已缓存的上游科研 Skill 源码
```

第一个 feature：

```text
bio-spec-kit/specs/002-multiqc-vertical-slice/spec.md
bio-spec-kit/specs/002-multiqc-vertical-slice/plan.md
bio-spec-kit/specs/002-multiqc-vertical-slice/tasks.md
```

实际执行 wrapper：

```text
bio-spec-kit/extensions/bio-multiqc/scripts/run_multiqc.py
```

## 4. 真实调用链：每个箭头由谁完成

```text
文件系统
  ↓ Agent harness / integration 扫描 Skill 目录
Skill discovery metadata
  ↓ harness 根据 name/description 选择或激活
SKILL.md 完整正文进入当前 context
  ↓ LLM 读取当前 Spec artifact 和 Skill instructions
模型产生 tool call
  ↓ host 执行文件、shell 或 process tool
wrapper / script 被运行
  ↓ wrapper 调用确定性 executable
Python / R / CLI / MultiQC 运行
  ↓ runtime 产生 stdout、stderr、exit code、日志和文件
artifacts / state 持久化
  ↓ host 把执行结果返回 Agent
Agent 读取并解释结果
  ↓ verifier 根据可观察证据判断是否满足验收
Spec scenario 通过或失败
```

边界：

| 对象 | 谁拥有 | 能做什么 | 不能假设它做什么 |
|---|---|---|---|
| LLM | Agent 模型 | 解释输入、提出问题、选择下一步、生成 tool call | 不能直接等于程序执行或科学证据 |
| Agent harness | Codex 等宿主 | 发现/激活 Skill，提供工具，返回结果 | 不自动保证模型理解正确 |
| Skill | 项目或上游作者 | 提供领域流程、适用条件、停止规则 | 不提供新的执行权限 |
| Tool | Host | 读写文件、启动 shell/process、搜索 | 不等于某个科研方法本身 |
| `scripts/` | Skill/Extension 文件 | 被 host 作为程序调用 | 不会自动变成新的 Tool |
| Spec artifact | 项目文件 | 持久化意图、输入输出和验收 | 不证明 runtime 真运行过 |
| Workflow runtime | Spec Kit engine | 组织步骤、条件、gate、resume 和 state | 不替代统计或生物学判断 |
| 外部 executable | R/Python/CLI/MultiQC | 做确定性计算 | 不负责理解用户的科学问题 |
| Verifier | 测试或确定性检查 | 检查内容、来源、哈希、版本和结果关系 | 不应只检查“文件存在” |

## 5. Spec Kit 原生命令的实际含义

### `specify`

默认负责创建或更新 `spec.md`。它会读取用户输入、解析 spec template，并在需要时读取 constitution；对不清楚的内容可以留下 `NEEDS CLARIFICATION`。

Bio-Spec Kit 中要把它改成“增量合并输入”：

```text
输入片段
  → 已知事实
  → 未知信息
  → 冲突信息
  → 暂定假设
  → 当前可回答部分
  → 最小阻塞问题
```

### `plan`

默认从 `spec.md` 推导技术计划。Bio-Spec Kit 中要加入候选方法比较、适用性、前置条件、选择理由、放弃理由和替代方案。

用户先提出方法时，该方法应先标记为候选方案，而不是直接变成最终方案。

### `tasks`

默认生成按 phase 和 user story 组织的任务，并标记依赖和可并行任务。Bio-Spec Kit 需要进一步把任务表示成依赖图和状态，而不是固定线性清单。

### `implement`

默认读取 `tasks.md`、`plan.md`、`spec.md` 和相关设计文件，按任务执行。它本身是 Agent instructions，不是 R/Python/CLI 执行器。

Bio-Spec Kit 中应只执行满足依赖的 ready task；遇到缺失科学输入时进入 blocked，而不是自行发明默认值。

### `converge`

默认只检查 Spec、Plan、Tasks 和当前代码的一致性，并在发现缺口时向 `tasks.md` 追加任务。

它不能天然证明：

- MultiQC 真的运行过；
- R 模型真的拟合过；
- 输出确实受到输入影响；
- 结果文件没有被人工伪造。

这些必须由 runtime manifest、日志、内容验证和端到端测试证明。Bio-Spec Kit 后续需要新增 `bio-verify`。

## 6. 官方机制对新 process 的支持

官方文档给出的边界是：

- Preset：修改现有模板、命令和术语；
- Extension：增加新命令、新能力、新阶段、脚本和 hooks；
- Workflow：组合 command、prompt、shell、gate、if/switch、循环、fan-out/fan-in，并支持暂停恢复；
- Integration：连接具体 Agent；
- Bundle：打包已有组件，不是新的执行引擎。

默认核心命令有顺序倾向，但不是每次都必须完整跑完；`clarify`、`analyze`、部分 implement 和回到前一阶段都属于合法迭代。

官方的 `assess` 扩展尤其有参考价值：

```text
intake → research → define → shape → decide
```

它允许 `define` 直接从用户输入开始；缺少 problem 时不能 shape；证据不足时输出 `needs-clarification`，而不是强行 `go`。这提供了我们所需的“最小澄清、阻塞和回退”范式。

目前官方核心没有确认到 `escalation` 或 `proceed` 命令。Bio-Spec Kit 可以将它们定义为新命令或状态转移。

一个重要的实现细节：preset 的命令会在安装/注册时物化到当前 Agent 的命令或 Skill 目录；Agent 每次运行时不会重新解析 preset 栈。因此修改 preset 后必须重新注册/刷新有效命令并进行集成测试。

## 7. Bio-Spec Kit 的非线性状态模型

这不是固定流程，而是一个依赖关系图：

```text
用户输入或已有结果（任意顺序）
        ↓
事实分类：known / unknown / conflict / assumption
        ↓
更新 Spec decision state
        ├── 缺关键输入 → NEEDS_INPUT
        ├── 有矛盾 → ESCALATE
        ├── 有候选方法 → COMPARE
        ├── 依赖满足 → READY
        ├── 用户确认 → PROCEED
        ├── runtime 失败 → FAILED / RETRY / ABORT
        ├── 结果产生 → VERIFY
        └── 证据完整 → RELEASED
```

基本规则：

1. 用户可以先回答任意部分；系统不要求按固定顺序重述全部内容。
2. 未提及的信息保持 `unknown`，不能静默变成默认值。
3. 只有阻塞当前节点的问题才需要立即询问。
4. 方法可以先出现，但只能作为 candidate，必须经过适用性比较。
5. 结果可以先出现，但在 provenance 未验证前只能作为 untrusted evidence。
6. 不适用的分析节点不运行，并记录 `not applicable` 或 `pending`。
7. 任何跳过都要说明原因；任何例外都要记录理由和影响。

## 8. 四个分析模块和 MultiQC 的定位

### `bulk-differential-expression`

能力：设计感知的 bulk expression 差异分析。

常见 preset：

- paired case-control；
- unpaired case-control；
- batch-adjusted；
- repeated-measures 或多因素设计。

当前拟采用的 R adapter 可以使用 edgeR 作为主要 count-model 推断，并用 limma 的 paired/block 设计做敏感性分析；这不是 Skill 名字本身。

### `cross-branch-integration`

能力：比较多个分支或组学结果的身份、contrast、方向、交集和证据层级。

第一阶段只做确定性 schema、ID、contrast、方向分层和交集；暂不引入 MOFA、DIABLO、SNF 等复杂联合模型。

### `pathway-enrichment`

能力：对 feature list 或 ranked list 做 GO/KEGG/自定义 gene set 的 ORA、GSEA 或其他明确声明的方法。

必须显式记录：

- ID 类型和映射方法；
- tested universe/background；
- GO ontology；
- KEGG 或 gene-set 数据版本/日期；
- 多重检验方法；
- 输入 list 的方向和阈值。

### `wgcna-module-constraint`

能力：在样本数、性状和数据质量满足条件时，做模块结构、模块-性状关系、hub/module 约束和稳定性检查。

WGCNA 是条件性探索工具，不是所有项目默认必须执行的阶段。小样本时应停止、降级为 reference-only，或明确标记探索性。

### `MultiQC`

能力：把多样本 QC 输出汇总为用户可打开的 HTML 和 machine-readable evidence。

它是 QC evidence aggregator，不是完整 QC 结论，也不是统计分析或生物学解释器。

## 9. 横向控制层

### Situation

描述当前实际情境：assay、输入格式、样本量、配对关系、批次、缺失、参考版本、目标问题和资源限制。

### Preset

公开的一组默认选择、适用条件、禁止条件、输出契约和失败行为。Preset 不是隐藏的自动决定。

### Mistake checks

至少覆盖：

- 样本 ID、重复和实验单位错误；
- pseudoreplication；
- pairing/batch/confounding；
- reference、assembly、coordinate 或 annotation 不一致；
- gene ID 映射错误；
- contrast 或方向错误；
- tested universe 错误；
- 方法与数据不匹配；
- 结果文件和输入文件不对应；
- 把“文件存在”误判为“分析成功”。

### Exception

任何偏离 preset 的行为都记录：

```text
原默认值
偏离内容
原因
影响
批准人/确认人
重新验证方式
```

### Precision

区分：测量精度、统计精度、效应大小和区间、跨重复稳健性、计算可复现性以及生物学结论强度。它不是一个简单的 `true/false` 字段。

## 10. 第一阶段真正要改的 preset

这里要区分两个层次，避免把候选实验配置误当成已经定稿的全局配置：

- `presets/bioinformatics/` 是面向一般 Bioinformatics 项目的宽 profile，保留为长期目标，但目前还不是已经验证完成的最终默认 preset。
- `presets/bio-research-mvp/` 是隔离的候选 preset，用来验证“官方 Spec Kit 生命周期 + Research/Bio 字段”的最小闭环；它不能因为存在就自动成为全局默认。

第一轮改造范围应先在隔离候选 preset 上验证，再决定哪些字段提升到宽 profile：

1. `spec-template.md`：从普通功能需求模板改成科学问题、实验设计、输入身份、未知/冲突、候选方法、验收和证据契约。
2. `commands/speckit.specify.md`：支持乱序增量输入，只追问当前阻塞项，不强行补齐。
3. `plan-template.md`：加入方法比较、适用性、替代方案、runtime 和 provenance 计划。
4. `commands/speckit.plan.md`：要求先列候选方法和未决条件，再形成可执行方案。
5. `tasks-template.md`：从固定 Setup/Foundational/User Story 改成依赖图、状态、输入输出和验证证据。
6. `commands/speckit.analyze.md`：检查科学设计、输入身份、统计方案、证据覆盖和未声明默认值。
7. 补充 `implement` 和 `converge` 的 Bio-Spec 约束，但先不修改上游基线。

第一轮不做：

- MCP；
- 动态 Skill router；
- 复杂多 Agent；
- Nextflow runtime；
- 自动自我进化；
- marketplace；
- 直接改上游 `spec-kit` checkout；
- 把四个分析模块强制串成固定顺序。

## 11. 之后的 Extension 和 Workflow 方向

Preset 解决“核心模板和命令怎么理解 Bio-Spec”。下一层才是新增命令：

```text
bio-intake
bio-clarify
bio-compare
bio-proceed
bio-escalate
bio-execute
bio-verify
```

Workflow 负责把这些命令和人工 gate 连接起来，例如：

```text
接收部分输入
  → 检查是否有阻塞问题
  → 有则暂停并提问
  → 没有则选择已满足依赖的分析节点
  → 运行真实 wrapper
  → 验证 artifacts
  → 需要时回到比较或澄清
  → 用户批准后 release
```

如果现有 workflow engine 的状态表达不够，再单独修改 Python engine 和 tests。不能先假设 Markdown 能完成状态机 enforcement。

## 12. 已完成的真实 MultiQC vertical slice

入口：

```text
tests/fixtures/multiqc/
```

Spec：

```text
specs/002-multiqc-vertical-slice/
```

项目 Skill：

```text
.agents/skills/multiqc/SKILL.md
```

真实命令：

```text
.venv/Scripts/python.exe extensions/bio-multiqc/scripts/run_multiqc.py --input tests/fixtures/multiqc --output spec-mvp/artifacts/multiqc-mvp --config extensions/bio-multiqc/config/multiqc_config.yaml --multiqc-bin ./.venv/Scripts/multiqc.exe --preset fastqc-multiqc-mvp
```

实际版本：

```text
Python 3.12.10
MultiQC 1.35
```

成功输出：

```text
spec-mvp/artifacts/multiqc-mvp/multiqc_report.html
spec-mvp/artifacts/multiqc-mvp/multiqc_report_data/multiqc_data.json
spec-mvp/artifacts/multiqc-mvp/multiqc_report_data/multiqc_sources.json
spec-mvp/artifacts/multiqc-mvp/multiqc_report_data/multiqc.log
```

最终用户报告：

[multiqc_report.html](<E:/all-agent-workspace/codex-projects/bio-skills/bio-spec-kit/spec-mvp/artifacts/multiqc-mvp/multiqc_report.html>)

真实测试覆盖：

- 干净入口运行真实 MultiQC CLI；
- 改变 fixture 后 parsed result 和 input manifest hash 改变；
- 缺失 executable 时 fail closed；
- 三个 unittest 通过；
- wrapper 不仅检查 HTML 存在，还检查 JSON、source map、log、样本名和输入值。

## 13. 前面三个只读 Agent 的有效结论

### DE 与跨分支复核

- Skill 名称不应绑定 LUAD；
- paired 设计应显式包含 subject/block；
- edgeR 作为 count-model 主分析、limma paired/block 作为敏感性分析是候选方案，不是不可替换的永久规则；
- cross-branch 第一阶段使用确定性表格契约和方向分层，不先做复杂多组学联合模型。

### Pathway 与 WGCNA 复核

- 富集分析必须区分 ORA、GSEA、universe 和 ID mapping；
- GO/KEGG 是知识来源，不是完整分析逻辑；
- WGCNA 需要样本量、性状和稳定性约束；
- hub/module 结果不能直接被解释为因果关系。

### MultiQC 与 packaging 复核

- Codex 实际 Skill 目录是 `.agents/skills/`；
- MultiQC 1.35 实际数据目录为 `multiqc_report_data/`；
- 只检查 HTML 存在不够，必须检查机器可读内容和来源；
- runtime、artifact 和 Spec 不能混成同一个对象。

## 14. Superpowers 与 Bio-Spec Kit 的关系

Superpowers 是很流行的 Agent 软件开发方法和 Skill 框架，强项包括 brainstorming、writing plans、TDD、系统调试、代码审查和完成前验证。

它适合借鉴行为纪律：

```text
先澄清
先形成方案
任务可验证
过程有检查
完成前必须验证
```

但它不是生物信息学 process，也不能替代 Spec Kit 的 artifact、preset、extension、workflow 和 runtime。Bio-Spec Kit 应以 Spec Kit 为底座，选择性吸收 Superpowers 的流程纪律，而不是整套复制。

## 15. 官方和源码参考

- [Spec Kit 官方总览](https://github.github.io/spec-kit/)
- [Spec Kit 官方 README](https://github.com/github/spec-kit)
- [Agentic SDD 命令说明](https://github.github.io/spec-kit/reference/agentic-sdd.html)
- [Preset 机制](https://github.github.io/spec-kit/reference/presets.html)
- [Extension API](https://github.github.io/spec-kit/extensions/EXTENSION-API-REFERENCE.html)
- [Workflow 机制](https://github.github.io/spec-kit/reference/workflows.html)
- [Agent Skills specification](https://github.com/agentskills/agentskills/blob/main/docs/specification.mdx)
- [Superpowers](https://github.com/obra/superpowers)

## 16. 初始工作顺序（现已由 §24 的统一路线取代）

下面保留最初形成的工作顺序，作为决策历史；实际执行时以 §24 的阶段 A–F 为准。这样可以保留“为什么先做 preset、再做 workflow”的来路，同时避免把早期顺序误读为当前完整计划。

```text
1. 保留上游 spec-kit checkout 不动
2. 改 bio-spec-kit/presets/bioinformatics
3. 用现有 Codex integration 重新注册/验证有效命令
4. 为非线性输入、阻塞澄清和方法比较增加测试
5. 再增加 bio-specific extension commands
6. 再增加 workflow state、gate、pause/resume
7. 最后逐个接入 bulk DE、cross-branch、pathway、WGCNA
```

第一轮 preset 改造完成前，不开始重写五个生信 Skill，也不把任何方法名写死成通用架构。

## 17. 未决问题

- `limma2` 是否确实指 R `limma`，还是内部名称？
- `station` 是否指 situation/具体分析情境？
- 用户提到的“c 公司”具体是哪一个 GitHub 组织或仓库？
- Bio-Spec Kit 的第一版是否把 `proceed` 和 `escalate` 做成命令，还是只做状态？
- 哪些情形必须人工批准，哪些情形可以在 preset 范围内直接继续？
- 生信项目的最小统一输入契约是否采用 `.bio/manifest.json`、`.bio/samples.tsv` 和 reference lock？

以上未决项在没有确认前不能被假设成最终设计。

## 附录 A：对话和 Agent 复核的交接记录

本附录用于后续新对话恢复上下文。它不是新的需求来源；它只记录已经讨论过的有效结论。

### A.1 用户已经明确的边界

- 目标是创建新的 Bio-Spec Kit process，而不只是给普通 Spec Kit 项目增加几个 Markdown Skill。
- 上游 `spec-kit` checkout 先作为只读基线，暂不修改。
- 第一实际改造目标是当前项目的 `presets/bioinformatics`。
- 新对话先只讨论和分析 preset，不直接修改 preset。
- 之后才讨论 extension、workflow、状态模型和必要的 Python engine 修改。
- 暂时不做 MCP、复杂多 Agent、marketplace、动态 Skill router、自动自我进化和 Nextflow runtime。
- 用户输入可能乱序、部分提供或先给方法后给问题；系统不能强制固定顺序，也不能把未知信息静默填成默认值。

### A.2 已纠正的 Assistant 误读

- “AIGC 不负责科学决定”曾被 Assistant 错误地说成用户之前已经提出的要求；这不是用户原话，不能作为已批准的项目原则。
- `bulk-pa-luad` 不是上游开源项目名，也不是标准工具名，只是当前项目的临时标签。
- `spec.md`、`plan.md`、`tasks.md` 和 `implement/converge` 不是四个生物信息学分析阶段。
- 单独增加 `SKILL.md` 不等于改变 Spec Kit 核心流程。

### A.3 Sartre 只读 Agent 的报告摘要

Sartre 被要求只读核对本地 Spec Kit 和官方文档，没有修改文件、安装依赖或运行项目。它确认：

- Spec Kit 官方支持自定义 process；
- preset 可以改核心模板和命令；
- extension 可以增加命令、阶段、脚本和 hooks；
- workflow 可以支持 command、prompt、shell、gate、if、switch、循环、fan-out/fan-in、pause/resume；
- Codex integration 会把 Spec Kit command materialize 成 `.agents/skills/speckit-<name>/SKILL.md`；
- `implement.md` 是 Agent instructions，不是 runtime；
- `converge.md` 只能检查 Spec、Plan、Tasks 与代码的覆盖和一致性，不能独立证明 R/Python/CLI 真实运行过；
- 当前官方核心没有确认到 `escalation` 或 `proceed` 命令；这两个概念需要由 Bio-Spec Kit 新定义为命令或状态；
- `SKILL.md/scripts/` 不是新的 Tool，仍需 host 通过 shell/process 工具调用；
- workflow 的 `requires` 是声明性条件，不是 capability sandbox；shell 以本地用户权限运行。

Sartre 核对的关键上游路径：

```text
E:/all-agent-workspace/codex-projects/bio-skills/spec-kit/templates/commands/
E:/all-agent-workspace/codex-projects/bio-skills/spec-kit/src/specify_cli/
E:/all-agent-workspace/codex-projects/bio-skills/spec-kit/src/specify_cli/integrations/
E:/all-agent-workspace/codex-projects/bio-skills/spec-kit/src/specify_cli/presets/
E:/all-agent-workspace/codex-projects/bio-skills/spec-kit/src/specify_cli/extensions/
E:/all-agent-workspace/codex-projects/bio-skills/spec-kit/src/specify_cli/workflows/
```

本地上游 checkout 记录的 HEAD：

```text
c58a8487461052b4fa65e626df167521d297b184
```

### A.4 Sartre 对五个核心命令的交接结论

```text
specify：用户输入 + spec template + constitution → spec.md/checklist
plan：spec.md + constitution → plan/research/data-model/contracts/quickstart
tasks：spec.md + plan + 设计文档 → tasks.md
implement：tasks/plan/spec → Agent 调用 host tool 执行任务
converge：spec/plan/tasks + 代码 → 必要时只向 tasks.md 追加缺口
```

官方默认过程偏向顺序执行，但并不要求所有命令每次都完整执行。Bio-Spec Kit 需要把这种“可回退、可暂停、基于依赖继续”的能力从口头约定变成 preset、extension、workflow 和 verifier 的组合。

### A.5 前置三个 Agent 的交接结论

- DE 复核：Skill 应叫通用能力名；paired/block、edgeR、limma 属于 scenario、preset 或 adapter；不能绑定 LUAD。
- Integration 复核：第一阶段做 ID、contrast、方向、交集和证据分层；暂不做 MOFA、DIABLO、SNF。
- Pathway 复核：明确 ORA/GSEA、ID mapping、tested universe、GO/KEGG 版本和多重检验。
- WGCNA 复核：样本量、性状、网络类型、hub/module 约束和稳定性要成为前置条件；小样本不能默认执行。
- MultiQC 复核：真实输出数据目录是 `multiqc_report_data/`；检查内容、source map 和 log，不能只检查 HTML 文件存在。

### A.6 下一次新对话的唯一讨论主题

新对话只讨论：

```text
如何把当前 presets/bioinformatics 设计成 Bio-Spec Kit 的第一层核心改造
```

讨论内容应覆盖：

1. preset 如何覆盖 `specify`、`plan`、`tasks`、`analyze`；
2. 是否同时覆盖 `implement` 和 `converge`；
3. 如何在模板中表达 known/unknown/conflict/assumption；
4. 如何表达非线性回答和最小阻塞澄清；
5. 如何表达候选方法比较、proceed、escalate 和 exception；
6. 哪些内容必须留给 extension、workflow、runtime 或 verifier。

新对话阶段禁止：

- 修改文件；
- 运行命令；
- 修改上游 `spec-kit`；
- 先讨论具体 R/Python 实现；
- 把任何未确认的默认值写成最终规则。

## 18. 现有材料的统一归位

### 18.1 这些材料分别是什么

| 材料 | 当前性质 | 它解决的问题 | 它不代表什么 |
|---|---|---|---|
| `references/research-spec-kit-mvp/00–05` | Research/Bio 设计输入 | 治理、科研语义、设计统计、provenance、迁移边界 | 不是 OpenAI、Claude 或 Spec Kit 官方契约；当前不直接接入运行链路 |
| `specs/001-research-skills/` | Skill 调研 Feature 草稿 | 对候选 Skill 做来源、调用、评分和集成层级记录 | 不是已经批准的 Skill marketplace；当前没有完整 `tasks.md` |
| `spec-mvp/research-evidence-kernel/` | 可执行的研究语义 MVP | 用固定 fixture 证明 Question → Observable → Validation → Claim 的闭环 | 不证明真实队列、独立验证或生物学机制成立 |
| `specs/002-multiqc-vertical-slice/` | 可执行的技术 Feature Spec | 证明固定 fixture 经过真实 MultiQC 产生可核验报告 | 不等于完整 Bio workflow 或最终 QC 决策 |
| `presets/bioinformatics/` | 较宽的 Bio profile 候选 | 为生信项目提供模板、命令和领域术语 | 不应承载某一个 LUAD 项目的所有方法和默认值 |
| `presets/bio-research-mvp/` | 较窄的候选 MVP preset | 在官方 Spec Kit artifact 生命周期上增加最小科研字段 | 尚未成为默认 preset，仍需官方安装/解析/运行验证 |
| `spec-mvp/presets/multiqc-fastqc-mvp.yml` | 执行 preset | 固定 MultiQC 输入、预期值和 evidence policy | 不是通用科研 preset |
| `workflows/bio-research-mvp/` | 官方形态候选 workflow | 用 command、shell、gate 串起 specify、plan、tasks 和 MultiQC | 在本地完整注册、暂停/恢复和端到端运行前，不能称为已验证 workflow |
| `spec-mvp/workflows/multiqc-vertical-slice.yml` | 项目内部架构描述 | 清楚表达 Spec、Skill、Execution 三层 | 使用了项目自定义 step 类型，不是官方 engine 可直接执行的 workflow |
| `.agents/skills/` | Codex 实际发现目录 | 让当前 Agent 能发现和加载项目 Skill | 不等于 Skill 源码不可变仓库或科学正确性证明 |
| `spec-mvp/skills/` | 审计/暂存副本 | 保存选定 Skill 及参考资料的项目版本 | 不等于所有上游 Skill 已完成 runtime 集成 |
| `vendor/sources/` | 上游来源快照 | 保留来源、版本、commit 和审计依据 | 不应被项目命令静默改写 |

### 18.2 五个 Research 文件与 MVP 的关系

`01–05` 不是五个必须依次运行的步骤，也不是五个 Skill。它们是五类设计输入：

```text
01 Research Constitution
  → 规定科研底线、责任、证据和发布规则

02 Research Specification / Evidence / Claim
  → 定义问题、观测、验证和主张之间的语义关系

03 Research Design / Experimental Statistics
  → 规定实验单位、比较、复制、混杂、统计和验证设计

04 Open Science / Provenance
  → 规定 run、artifact、版本、hash、冻结点和可复现性

05 Spec Kit Migration / Bio Profile
  → 说明以上语义怎样映射到 Spec Kit、Bio profile、Skill 和 workflow
```

真正首先可运行的是两个小切片：

```text
Research semantics slice = Evidence Closure Kernel
Execution slice          = MultiQC vertical slice
```

因此，当前不能说五个文件已经全部进入契约；更准确的说法是：它们提供了候选规则，其中少数规则已经在两个 MVP 中得到局部实现。

## 19. Matsen walkthrough 的完整解读和可迁移事实

### 19.1 他实际走的步骤

1. **Vision**：先写目标和探索笔记，说明要构建什么、为什么构建以及可能的数据来源和规模。
2. **Constitution**：把已有 coding standards、pipeline 专家规则和项目目标合成项目原则。
3. **Specify**：根据 vision、探索笔记和 README 生成 user stories、functional requirements 和 success criteria。
4. **人工修订 Spec**：补上领域关键的 tree rooting 和 ancestor → descendant directionality。
5. **保持 Spec workflow-agnostic**：从 spec 中移除 Snakemake，把 workflow engine 的选择放到 plan 阶段。
6. **Clarify**：只提出会改变行为的高影响问题，例如 UniProt API 失败时是立即失败、重试、使用 cache 还是跳过。
7. **Plan**：让 Agent 研究 workflow engine、rooting、taxonomy、输出格式和工具 edge cases，并记录决策。
8. **Tasks**：按 setup、foundational 和 user story 拆成 49 个可执行任务，标出依赖、并行机会和每个 story 的独立验收。
9. **Analyze**：在写 code 前检查 spec、plan、tasks 和 constitution 是否矛盾或有覆盖缺口。
10. **Implement**：按任务执行真实工具链，同时根据真实工具行为修复版本、命名、参数和输出问题。
11. **MVP 验证**：先用约 100 条 sequence 跑一条完整 pipeline，检查真实输出和指标。
12. **Pilot/scale**：随后扩大数据量并转到远程执行；遇到 taxonomy bug 时创建 issue，而不是把失败结果标成成功。

### 19.2 这个案例中的 MVP

文章把 MVP 范围落在 Setup、Foundational 和第一个测试数据集 user story。它的关键不是“少做几个功能”，而是让一条完整链路在小数据上真实成立：

```text
input sequence
  → clustering
  → alignment
  → tree
  → rooting
  → ancestral reconstruction
  → parent-child extraction
  → output verification
```

这个 MVP 是 **small real system**，不是 fake prototype：工具是真的、数据变换是真的、最终结果要能被核验；只是规模、场景和 edge cases 先受到控制。

### 19.3 这个案例不应被误读为

- Agent 一次生成完整正确 pipeline；
- constitution 是一份具体方法说明；
- spec 可以代替 runtime；
- 只要输出文件存在就算成功；
- pilot 发现 bug 就说明 MVP 失败；
- 人可以完全退出，只让 Agent 自行决定科学语义。

它展示的是一种逐步收敛机制：先把目标和边界写清楚，再用小规模真实执行暴露跨工具问题，最后把问题变成新的可追踪工作。

## 20. Feature Spec 怎样根据 Skill 和具体方法落地

Feature Spec 不应把 Skill 名称直接等同于科学问题，也不应把用户提到的某个工具直接当成最终方法。正确绑定链是：

```text
研究问题 / 目标
  ↓
Feature Spec：范围、对象、比较、输入、输出、验收
  ↓
候选 Skill：检查适用条件和输入合同
  ↓
候选方法比较：方法前提、替代方案、风险和证据要求
  ↓
Plan：确认具体方法、工具、版本、参数和 runtime
  ↓
Tasks：实现、验证、provenance 和人工 review
  ↓
Skill adapter / workflow / executable
  ↓
Run artifacts + verifier
  ↓
Observable / Validation / Claim
```

对于一个具体 Feature，至少要能追溯：

```text
feature_id
→ selected_skill_id
→ source URL / commit / version / hash
→ skill preconditions
→ adapter version
→ selected method and rationale
→ executable command and version
→ input/output artifacts
→ verification rules
→ human review decision
```

因此，具体方法不是被“写进一个大 Skill”里就完成了，而是要在 Feature Spec、Plan 和运行合同之间形成可追溯关系。

## 21. Evidence Closure Kernel 的位置和当前局限

### 21.1 它证明什么

当前 MVP 可从固定输入中：

1. 检查 Question 是否完整；
2. 读取两个 effect vector；
3. 计算响应基因交集与方向一致性；
4. 检查预先设定的 threshold、overlap 和 concordance；
5. 检查独立验证状态；
6. 生成 Observable、Validation、Claim、Provenance 和 Run Manifest；
7. 在缺字段、重复 gene ID、provenance mismatch 时 fail closed。

当前状态可以区分：

```text
supported
not_supported
inconclusive
not_evaluable
failed_terminal
needs_clarification
```

即使 `claim_status=supported`，当前也不能自动 `release_ready`；还要经过人工 review。

### 21.2 它还没有证明什么

- `independent_validation` 当前主要是 fixture 中的声明值，不是真正读取独立队列或独立 run；
- `Evidence` 目前主要是 ID 引用，尚未形成完整 Evidence Registry；
- 部分 Observable 字段结构还未完全统一；
- validation 输入尚未完全纳入 run identity 和 hash 计算；
- 它没有连接真实 bulk RNA-seq、WGCNA、pathway 或空间数据；
- 它不能证明 PA/LUAD 的真实生物学机制或因果关系。

所以它是“研究结论状态的最小判定器”，不是完整科研分析系统。

## 22. 单一 Skill、科研方法、目标 Claim 的评测体系

本节是原则摘要；具体 case、oracle、负例、metamorphic test 和 E1/E2/E3 验收表见 [`spec-mvp/docs/evaluation-matrix.md`](spec-mvp/docs/evaluation-matrix.md)。

### 22.1 被评对象必须分开

| 对象 | 要回答的问题 | 不应混入的问题 |
|---|---|---|
| 单一 Skill | 是否正确触发、遵守输入/输出合同、选择正确参考、正确停止并保留来源？ | 不直接证明科学结论正确 |
| Spec 生成器 | 是否把问题、范围、未知、假设、方法候选和验收写完整？ | 不直接证明 runtime 已执行 |
| 科研设计/方法 | 实验单位、比较、统计、QC、独立验证和 claim 边界是否科学合理？ | 不以文字相似度代替专家判断 |
| Workflow/Agent | 是否按阶段、依赖、gate、retry、pause/resume 正确行动？ | 不把 `exit 0` 当科学有效 |
| Runtime/Verifier | 是否真实调用工具并验证 artifact 内容、来源、hash 和版本？ | 不替代研究者解释结果 |
| 目标/标的/Claim | 证据是否支持指定对象、范围和主张？ | 不把 supported 自动升级为因果或临床结论 |

### 22.2 测试集的必要场景

每个 Skill 或 workflow 至少要有：

- 正确适用；
- 明确不适用；
- 关键信息缺失；
- 输入顺序打乱；
- 相邻 Skill 竞争；
- 事实冲突；
- 方法前置条件不满足；
- 工具不可用或返回错误；
- 输出文件存在但内容错误；
- provenance 不一致；
- 负结果；
- 证据不足；
- 同一 fixture 重跑；
- 改变一个输入后的 metamorphic test。

### 22.3 评分方式

不能只输出一个总分。建议同时报告：

```text
触发/路由
契约遵守
澄清与安全停机
科研设计质量
工具轨迹
证据和 provenance
可复现性
Claim calibration
人工修改量
时间、token 和运行成本
```

以下情况直接属于 hard fail：

- 捏造结果、引用、版本或样本信息；
- 把 unknown 静默写成事实；
- 把技术重复当成生物学重复；
- 在证据不足时输出 supported 或 release；
- provenance 不一致仍允许发布；
- 只生成静态 artifact 却声称真实执行；
- 跳过必须的人工 gate 或篡改 verdict。

目前没有确认存在一个由 Spec Kit 官方维护、可统一比较不同 preset、workflow、模型和最终科研质量的专用 benchmark。可借鉴 SkillsBench、agent-skills-eval、Inspect AI、Agent Spec Eval、LAB-Bench 和 ScienceAgentBench 的部分设计，但 Bio-Spec Kit 仍需要自己的固定案例、隐藏验证器和领域 rubric。

## 23. 用户主导的操作模式

当前核心和底层设计不应让 Agent 自行拍板。建议把工作分成三个模式：

```text
explain-only
  Agent 只能读取、解释、指出缺失和冲突

propose-only
  Agent 可以提出候选文件、字段、diff 和方法比较，但不能应用

apply-approved
  只有用户批准明确变更范围后，Agent 才能执行修改
```

用户的工作角色是：

```text
定义问题和目标
确认关键假设、estimand、阈值和 claim boundary
批准方法和例外
审阅 MVP / pilot evidence
批准或拒绝 release
```

Agent 的工作角色是：

```text
整理输入
指出未知和冲突
解释候选方案
执行已批准的确定性任务
收集日志和 artifacts
根据规则报告状态
```

需要强调：`explain-only` 不能只依赖 prompt。Workflow 的 gate 和 prompt 不是权限沙箱；如果真的要禁止写入，host/tool 层也必须提供只读或受限运行权限。

## 24. 统一后的实施路线和验收

### Phase A：文档和边界收敛（当前）

- [x] 汇总可读取的相关对话和仓库材料；
- [x] 区分官方机制、项目自定义设计和具体 Feature；
- [x] 把两个 MVP、五类 Research 设计输入和 Skill 调研放入统一模型；
- [x] 明确工具复核暂后置；
- [ ] 确认统一状态名和 `target/Claim validation` 的正式术语；
- [ ] 确认哪些候选设计可以升级为正式 Bio Profile 规则。

### Phase B：研究语义 MVP 收敛

- [ ] 固定 Question、Observable、Validation、Evidence、Claim 的统一 schema；
- [ ] 将 validation 输入纳入完整 run identity；
- [ ] 建立最小 Evidence Registry；
- [ ] 统一 `run_status`、`claim_status`、`review_status` 和 `release_status`；
- [ ] 增加支持、阴性、不确定、不可评价、技术失败和未执行的测试；
- [ ] 明确 `supported` 只表示指定范围内规则满足。

### Phase C：官方 Spec Kit 形态验证

- [ ] 单独验证 `presets/bio-research-mvp` 的 preset schema、安装、模板解析和命令 materialization；
- [ ] 单独验证 `workflows/bio-research-mvp/workflow.yml` 的注册、参数传入、shell、gate 和 review record；
- [ ] 保留 `spec-mvp/workflows/multiqc-vertical-slice.yml` 作为架构参考，不误称官方 workflow；
- [ ] 不修改上游 Spec Kit checkout。

### Phase D：Bio preset 核心改造

- [ ] 先改 `specify + spec-template`：研究问题、未知、冲突、假设、Scope、Claim boundary；
- [ ] 再改 `plan + plan-template`：候选方法、适用性、替代方案和 provenance；
- [ ] 再改 `tasks + tasks-template`：MVP vertical slice、任务证据、依赖和 gate；
- [ ] 再改 `analyze`：科学设计、输入身份、统计、证据和默认值检查；
- [ ] 最后补 `implement/converge` 的 Bio 约束，不把它们改成生信 runtime。

### Phase E：单 Skill 与方法验证

- [ ] 为每个已选 Skill 冻结 source URL、commit、version、license、原始 hash 和规范化 hash；
- [ ] 维护 source adapter，不静默改写源 Skill；
- [ ] 为 Skill 增加输入/输出/失败/权限/版本合同；
- [ ] 先建立 `bulk-rnaseq + experimental-design` 的对照评测案例；
- [ ] 通过 negative、metamorphic、repeatability 和 artifact checks 验证。

### Phase F：具体工具和真实研究 Feature（后置）

- [ ] 完成 edgeR/limma、pathway、WGCNA、cross-branch 等工具的逐个复核；
- [ ] 以真实研究问题建立 Feature Spec，而不是把研究项目默认值写回通用 Skill；
- [ ] 增加独立/正交/holdout 的目标 Claim 验证；
- [ ] 由小数据 MVP 逐级扩展到 pilot 和 production；
- [ ] 最终由人工批准 release。

## 25. 当前不可自动定案的事项

以下内容目前必须标成 `unresolved`，不能因为已经出现在文件里就视为用户批准：

1. “标的验证”具体是 target validation、研究对象验证，还是 Claim/evidence validation 的简称；当前统一文档暂以“目标/标的/Claim 验证”并列保留。
2. Research Spec Kit 是否要作为独立产品建设，还是只作为 Bio Spec Kit 的抽象参考。
3. `Evidence Closure Kernel` 是否升级为正式 Research Core，还是继续作为 Bio MVP 内部组件。
4. `bio-research-mvp` 是否成为默认 preset，还是只作为验证用候选 preset。
5. `proceed`、`escalate` 是状态、命令，还是 workflow gate 的组合。
6. `supported`、`release_ready` 和人工批准之间的最终状态命名。
7. Skill 来源 hash 是否以原始字节为准，还是必须同时保存规范化内容 hash。
8. 哪些任务允许 Agent 自动执行，哪些任务必须用户逐项批准。
9. `specs/001-research-skills` 是继续作为调研 Feature，还是另建一个“Bio-Spec Kit 统一收敛” Feature 来承载后续正式任务。

## 26. 已启动的真实能力驱动 MVP

用户已经明确把工作重点收敛为：

```text
已有可运行能力
→ Spec 化
→ 真实输入接入
→ 可重复执行
→ artifact/provenance
→ MVP
```

因此当前已新增并实际运行：

| 项目 | 位置 | 状态 |
|---|---|---|
| shared integration Feature Spec | `specs/003-shared-integration-vertical-slice/` | Spec/Plan/Tasks 已建立 |
| 确定性 wrapper | `extensions/bio-integration/scripts/run_shared_integration.py` | 已实现 |
| Skill/extension contract | `extensions/bio-integration/` | 已建立 |
| 固定 known-answer fixture | `tests/fixtures/shared-integration/` | 已建立 |
| 自动测试 | `spec-mvp/tests/test_shared_integration_mvp.py` | 已通过 |
| 真实 PA/LUAD run | `spec-mvp/docs/shared-integration-mvp-run.md` | shared 149 与四方向集合复现 |
| Spec-driven workflow | `workflows/bio-research-shared-integration/workflow.yml` | 已建立，待官方 materialization 验证 |

真实运行得到：

```text
shared = 149
UpUp = 50
DownDown = 17
UpDown = 73
DownUp = 9
```

这条 MVP 只承诺“固定 DEG 集合的直接交集和方向分层可重算”，不把它升级成共同机制、因果关系或独立验证。下一步应在这个已稳定的 artifact contract 上接 offline frozen pathway，而不是回头重新做一轮泛化评估。

在这些问题被确认前，任何新工具、方法或 Skill 的接入只能作为候选设计或局部实验，不能自动升级为核心架构。

## 附录 B：相关对话的交接索引

下面只记录本次能够读取并确认与当前项目直接相关的对话贡献；截图中的其他标题不自动纳入。

| 对话主题 | 贡献 | 当前归位 |
|---|---|---|
| 初始 Bio-Spec Kit MVP / 本地 harness | 建立 Spec Core、Agent Skills Core、Execution Core 三层；要求真实 Skill、真实 executable、fixture、E2E 和可打开 artifact | 第 2、3、4、12 节；MultiQC MVP |
| `Evidence Closure Kernel` | 明确 Question、Observable、Validation、Claim、Provenance、Gate/State；区分 supported、inconclusive、not_evaluable | 第 0、21 节；`spec-mvp/research-evidence-kernel/` |
| Research Skill 与 Bio Skill 对照 | 选 `bulk-rnaseq + experimental-design` 作外部结构样本；明确 Research、Bio Profile、Skill、Feature 分层 | 第 18、20、22 节；`specs/001-research-skills/` |
| Bio preset 核心设计 | 先从 `specify + spec-template` 这一最早的意图边界开始，不并行改所有命令和 Skill | 第 10、24 节 |
| 科研 Agent 评测对象和框架 | 区分 Skill、Spec 生成器、Agent/Workflow、Runtime/Verifier、科研 Claim；建议 hard gate + 多维度评分 + 重复运行 | 第 0、22 节 |
| Spec Kit、Codex、Claude 与官方机制核对 | 明确 Skill、Spec Kit artifact、Research domain contract 不是同一种 contract；preset、extension、workflow、bundle 职责不同 | 第 2、6、18 节 |
| Matsen Spec-Driven Development walkthrough | 提供 vision→constitution→specify→clarify→plan→tasks→analyze→implement→MVP→pilot 的真实案例 | 第 19 节 |
| 当前对话 | 要求把单一 Skill 验证、科研验证、目标/标的验证、Spec 实例、Skill 方法绑定、MVP、vertical slice 和所有相关结果统一 | 本文件的统一入口和 Phase A |

### B.1 当前总参考的使用规则

后续新任务首先读取本文件，再根据任务范围读取相应的局部文件。新文件必须注明自己属于：

```text
official baseline
design reference
candidate contract
implemented verified
audited adapter
or unresolved proposal
```

如果一个新结论与本文件冲突，先新增 decision record 并标明来源、证据和状态，不能直接覆盖旧结论。
