# Spec Kit 改造工程压缩审阅入口

**用途**：供人和 Agent 快速判断当前 Feature 的目标、边界、结构、证据和下一道门禁。
这是按“审阅/决策”目的做的有损压缩，不替代原始文件；原始文件仍是事实来源。

**范围**：`specs/005-skills-nextflow-research-core/` 的 01–09 产物、13 个逻辑组件审计、Nextflow invariant、合同、评估 protocol、局部实现证据和 review 记录。

**当前结论**：批准范围内的 bounded local slice 与 fresh-context remediation 已收束；局部正/负例、契约/协议门和五轴 review 通过。但这不等于 13 个组件全部 runtime verified，不等于生物学有效性，不等于 human release，也没有产生 A0–A3 benchmark 分数。

## 1. 一页判定

| 问题 | 当前答案 | 权威位置 |
|---|---|---|
| 这是什么 | 用 Spec Kit 管理“Skills 审计/归类、Nextflow 结构抽象、Research Core/Bio preset 设计和量化准备”本身 | `spec.md` |
| Spec Kit 的角色 | 本改造工程的执行协议和治理门禁，不是目标 Skill/runtime 内容 | `constitution.md`、`plan.md` |
| 固定对象 | 13 个逻辑组件：5 个项目适配器 + 8 个 reference；镜像/投影不重复计数 | `spec.md`、`data-model.md` |
| 统一审计 | 每个组件都记录输入、前置、方法/estimand、route、输出、identity、证据、provenance、边界、失败恢复和 runtime 状态 | `contracts/skill-audit-record.yml` |
| Nextflow 的作用 | 提供可组合 dataflow 的结构先验；不定义生物学结论，也不改写 Spec Kit 生命周期 | `research.md` |
| Research Core 的作用 | 通用生命周期、端口、身份、provenance、gate/verifier、run-status 协议和评估骨架；静态 node 不承载单次三态 | `contracts/core-profile-boundary.md` |
| Bio preset 的作用 | 生物学术语、S00–S13、estimand 词汇、测试 universe 和方法 route | `contracts/core-profile-boundary.md` |
| 合并的含义 | 默认只合并阅读入口或 handoff；不删除源 Skill，不合并不同 estimand/所有权 | `merge-decisions.md` |
| 量化主指标 | task-level oracle/verifier 通过率；字段完整度和 trace 只作诊断 | `evaluation-protocol.md` |
| 当前局部证据 | MultiQC 正例 wrapper=0、负例 wrapper=2；verifier 通过；execution/scientific/release 保持独立 | `evaluation/runs/`、`analysis.md` |
| 仍未证明 | unseen validation/holdout、长期 benchmark、外部数据、13 个组件科学有效性 | `tasks.md`、`evaluation-protocol.md` |

## 2. Spec Kit 01–09 的实际职责

| 步骤 | 这次改造工程做什么 | 产物/门禁 | 失败回路 |
|---|---|---|---|
| 01 Constitution | 固定证据分层、科研语义优先、接口/身份、fail-closed、可逆和用户批准边界 | `constitution.md` | 回到原则或范围 |
| 02 Specify | 定义问题、输入、输出、FR/SC/US、非目标和完成条件 | `spec.md` | 回到目标定义 |
| 03 Clarify | 冻结外部输入、13 分母、Core/Bio 所有权、合同命名、第一批评估矩阵 | `clarifications.md`，并回写 `spec.md` | 回到 Specify |
| 04 Plan | 规定来源冻结、Nextflow 提取、13 项审计、正向映射、反向抽象和验证顺序 | `plan.md`、`research.md`、`data-model.md` | 回到 Clarify/Plan |
| 05 Checklist | 检查需求是否可理解、可追踪、可测量、有限界和可失败 | `checklists/requirements.md`；40 项已接受 | 回到 Specify/Plan |
| 06 Tasks | 把活动拆成有路径、依赖、证据的任务 | `tasks.md`；T001–T029 的 bounded-slice记录保留，T030–T034 追踪 fresh-context remediation，T026/T028/T029 延期 | 回到 Plan/Tasks |
| 07 Analyze | 只读检查覆盖、矛盾、孤儿、术语漂移、越权和证据不足 | `analysis.md`；无未接受 CRITICAL/HIGH | 回到对应阶段 |
| 08 Implement | 只有批准后才在精确路径做局部实现 | 已存在批准的 MultiQC/preset slice | 超范围立即停机 |
| 09 Converge | 用原始 spec/plan/checklist/tasks/证据回验实际结果，保留延期项 | `analysis.md`、`review/` | 回到 Implement 或追加任务 |

**关键门禁**：01–07 不是九个 runtime 节点；目标 Skills、workflow、bundle、preset 和运行代码不因文档存在而自动获得修改权限。

## 3. 已冻结的五项决策

- **C-001**：两份外部中文总览复制到 `inputs/`，保留原路径、观察日期和 SHA-256；副本只是审计输入，不是运行指令。
- **C-002**：固定 13 个逻辑组件，口径是 5 个项目适配器 + 8 个 reference；checkout 差异记为 source gap。
- **C-003**：Core 负责通用协议骨架；Bio profile/preset 负责生物学语义、S00–S13、estimand 和 route；算法/执行细节留在 Skill/Execution。
- **C-004**：public machine contract 使用 `node.contract.json`；public façade 可以引用 atomic module，但内部 contract 不取代 public contract。
- **C-005**：第一批只用仓库内可复核 fixture，采用 A0–A3；MultiQC 只做 construction/smoke，shared-integration 作为 validation reference；不下载外部数据、不启用 hosted service、不长跑。

## 4. 13 个组件的最短审计地图

统一字段的完整值、状态和证据仍以 `contracts/skill-audit-record.yml` 为准；下表只保留“输入 → 输出 / 当前角色 / 关系”。

| 组件 | 输入 → 输出 | 当前角色与边界 | 关系 |
|---|---|---|---|
| `bulk-pa-luad` | counts+metadata/design → paired DE、diagnostics、tested universe | 项目适配器；不作因果结论；运行未验证 | 与 `02-deg` 仅 merge-view |
| `cross-branch-integration` | 分支结果+稳定 ID → 匹配/未匹配、交集、方向分层 | 项目适配器；不推断共同因果机制或 joint model | compose-only |
| `multiqc` | QC 输入目录+config → HTML、JSON/source map、verdict、review | 项目适配器；聚合报告不等于 QC 通过 | compose-only；本轮有局部 slice |
| `pathway-enrichment` | DE/module 的 list/rank/universe/ID → GO/KEGG 结果和 mapping audit | 项目适配器；ORA/GSEA 和 universe 必须显式 | compose-only |
| `wgcna-module-constraint` | normalized expression+traits+network params → modules/eigengenes/hubs/stability | 项目适配器；共表达不等于 directed regulation | compose-only |
| `01-mds` | 变换矩阵/距离+metadata → PCA/MDS/UMAP 等坐标和诊断 | reference；投影不等于全球生物学距离 | compose-only |
| `02-deg` | expression+design/contrast → model 和完整 DE 表 | reference；方法 route 不能替代项目适配器 | 与 `bulk-pa-luad` merge-view |
| `02-deg-results` | 已执行 DE 结果 → 过滤表、ranking、foreground/universe | reference；不重估上游 estimand，不静默丢 `NA` | compose-only |
| `03-de-visualization` | DE 结果+变换矩阵 → MA/PCA/heatmap 等图及 plot data | reference；不产生第二套统计推断 | 与结果层 compose-only |
| `03-volcano` | effect/LFC+p/padj+label rules → volcano/MA 图和标签表 | reference；shrinkage 不重算 p-value | 与 visualization compose-only |
| `04-pathway-enricher` | gene list+外部 library → enrichment table/report | reference；外部 API、隐私和 release 仍独立 | compose-only handoff |
| `04-pathway-workflow` | list/rank/universe+organism → ORA/GSEA/database route | reference router；不混淆 route/estimand | 与 04/05 系列 compose-only |
| `05-kegg` | KEGG IDs+rank/effect+organism/release → KEGG 富集/拓扑结果 | reference；KEGG snapshot/topology 不泛化到其他数据库 | 与通用 pathway keep-separate |

## 5. 结构不变量与契约骨架

### Nextflow → Research Core 的 12 条不变量

1. 节点/process/module 有窄且显式的输入输出边界。
2. 明确区分 `queue`、`value`、stream 和 cardinality。
3. `tuple/meta` 与 payload 一起传递稳定身份。
4. join/mapping 使用稳定 key，并保留 unmatched/duplicate 审计。
5. public façade 通过 named `take/emit` 或等价 public port 组合。
6. ORA/GSEA、GO/KEGG、edgeR/limma 等 route 由声明选择，不能由文件名/隐藏默认值决定。
7. 方法与资源、容器、executor、profile 分离。
8. cache/resume identity 包含输入、脚本、参数、环境和 reference 版本。
9. work/cache、primary artifact、report、review/approval 分离。
10. execution、scientific、release 三态独立。
11. provenance 横切记录来源、版本、参数、命令、环境和 hash。
12. stub/fixture/positive/negative/output assertion 都属于组件验证边界。

每条 invariant 在 `research.md` 有 source、scope、失败模式、observable、owner 和 `FACT/INFERENCE/PROPOSAL/UNKNOWN` 状态；其中科研翻译不是 Nextflow 官方科学结论。

### 机器合同

- `node-contract.schema.json`：component kind、scientific purpose、hard boundary、method/estimand、public takes/emits、port direction/shape/cardinality/channel、identity、route、gate、named outputs、静态 provenance 要求、evidence；不含运行态。
- `run-status.schema.json`：`status.execution`、`status.scientific`、`status.release` 三个封闭状态集，互不自动推断，并携带一次运行的 typed provenance。
- `contracts/multiqc/node.contract.json`：第一个 representative public contract；通过 schema fit 不等于科学验证。
- `skill-audit-record.yml`：13 条逻辑记录，字段缺失使用 `有/条件/无/待核/不适用/未验证`，不使用空白代替不确定性。

## 6. 合并、不可替代和缺失

**允许的合并**：`merge-view` 只统一阅读入口；例如 `bulk-pa-luad` 与 `02-deg` 可以在 DE handoff 入口并列呈现，但 paired design、count model 和 reference prose 的所有权仍分开。

**主要 compose-only**：QC→分析、分支结果→整合、DE→结果冻结→可视化、模块→富集、pathway router→Enrichr/KEGG。它们共享稳定 handoff，不共享 estimand、数据库语义或 release 责任。

**必须 keep-separate**：通用 pathway enrichment 与 KEGG topology/数据库身份；普通交集与 joint model/因果整合；HTML/report 与 QC/scientific/release approval；ORA 与 GSEA；Enrichr live API 与本地/冻结数据库。

**显式缺口**：unseen scientific verifier、所有组件的 canonical S00–S13 冻结、外部 Enrichr/KEGG reproducibility snapshot、全链 runtime/benchmark。缺口不通过再造一个泛化字段静默填平。

## 7. 当前证据和限制

- 两份中文输入快照已 hash-check；原始 worktree 路径和输入角色保留在 `inputs/README.md`。
- 13 条审计记录和 13 行 invariant mapping 存在；这证明审计覆盖，不证明每个 Skill 可运行。
- MultiQC 正例：wrapper 返回 0，artifact verifier 通过；负例：不存在输入目录，wrapper 返回 2，negative verifier 通过。
- 运行 envelope 保留 `execution=passed`、`scientific=not-verified`、`release=pending`；`release_ready` 仅表示 artifact-ready 语义。
- 两个 MultiQC Skill 投影字节一致；schema、manifest、review 和正/负运行记录可追溯。
- 独立子 Agent 的既有收束记录为 `PASS`，但只覆盖原 bounded slice；本轮 fresh-context remediation 以本地校验器和五轴审查记录为准，不把旧结论扩展为 reusable-Core 通过。
- A-007：Windows 运行产生 GB18030 编码的 `multiqc_data.json`；当前 wrapper/verifier 能读，但跨平台 UTF-8 consumer 仍需另行授权处理。
- T026/T028/T029 保持 `DEFERRED/NOT_RUN`；没有 task-level 分数，也没有外部数据或长期 benchmark。

## 8. 本轮四 Skill 链

| 顺序 | Skill | 本轮职责 | 状态 |
|---|---|---|---|
| 1 | `summarization` | 按“人类快速审阅”目的压缩当前 Feature，保留决策、条件、证据位置、风险和延期 | 已安装；结构通过 |
| 2 | `review-skill` | 审计四个 Skill 的结构、scope、directive、token 和 novelty 风险 | 已安装；structural-only；有上游链接校验错误 |
| 3 | `architecture-critic` | fresh-context、只读、对 Spec/Plan/契约边界做 adversarial review；每个 finding 要有 file:line | 已安装；待子 Agent 返回 |
| 4 | `skill-forge` | 未来把批准后的审计规律蒸馏成自己的 audit-distill/audit-critic | 已安装；本轮 deferred，不自我生成 |

配置：`review-chain.yml`。原始组件保持不改；本文件只是新的审阅入口。

## 9. 下一道门禁

看 `review/skill-review-20260902.md` 和 `review/architecture-critique-20260902.md` 的 findings。若 architecture-critic 提出 blocker/红色维度，先由人决定是否修订 Spec/Plan；本轮不自动修改第三方 Skill、现有目标 Skill、preset、workflow 或 bundle。
