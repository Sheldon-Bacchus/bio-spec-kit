# Research Ledger（04 Plan 支持产物）

**状态**：`FROZEN_LEDGER / LOCAL_SLICE_IMPLEMENTING`

本文件先记录已经能确定的来源角色和研究问题；它不是目标 Skill 合同，也不把
任何参考文档的命令变成执行授权。完整的来源核验和版本/hash 冻结由 `T001`、
`T002`、`T005` 完成。

## 1. 来源分层

| source_id | 来源 | 允许支持的结论 | 当前状态 |
|---|---|---|---|
| SRC-SPECKIT-LOCAL | `.agents/skills/speckit-*`, `.specify/templates` | 本仓库采用的 Spec Kit 命令边界、产物和只读/写入约束 | `FACT / local` |
| SRC-CONSTITUTION | `.specify/memory/constitution.md` | 根项目证据、合同、provenance、QC、人审和可组合 Skill 原则 | `FACT / local` |
| SRC-SKILLS-OVERVIEW | 原始路径 `C:\Users\ldc\.codex\worktrees\7004\bio-spec-kit\spec-mvp\ALL-SKILLS-WORKFLOW-REFERENCE-zh-CN.md`；快照 `inputs/ALL-SKILLS-WORKFLOW-REFERENCE-zh-CN.md` | 13 个逻辑组件的总览、计数口径和合并判断线索 | `FACT-AS-SOURCE / frozen sha256 B7F357A25F59693FBF647734DA30F5526D68F908A48C7984C9E81BDEF0FB1CBB` |
| SRC-SKILLS-DETAIL | 原始路径 `C:\Users\ldc\.codex\worktrees\7004\bio-spec-kit\spec-mvp\docs\CONSOLIDATED-SKILLS-WORKFLOW-zh-CN.md`；快照 `inputs/CONSOLIDATED-SKILLS-WORKFLOW-zh-CN.md` | ARSSC 字段、S00–S13、输入输出和方法边界线索 | `FACT-AS-SOURCE / frozen sha256 57FEB5C7185103FC58ECB2003B3C653CCE67E53427E167CE5CEF5CB72022869E` |
| SRC-NF-DESIGN | `spec-mvp/docs/NEXTFLOW-SHAPED-SKILLS-OUTPUT-STRUCTURE-zh-CN.md` | 本项目已有的 Nextflow-shaped 设计草案 | `PROPOSAL / local` |
| SRC-NF-OFFICIAL | Nextflow Processes/Workflows/Modules/Cache and Resume 官方文档 | Nextflow 语义和执行结构的外部技术依据 | `FACT / captured 2026-09-02; URLs recorded below` |
| SRC-NFCORE | nf-core component/module/subworkflow conventions | 组件目录、meta、版本和测试的工程参考 | `FACT-AS-GUIDELINE / captured 2026-09-02; website version not pinned` |
| SRC-BIO-SKILLS | `spec-mvp/skills/` 与 `reference-stack/` | 13 个逻辑组件的源内容和当前状态 | `AUDITED / contracts/skill-audit-record.yml` |
| SRC-BENCH | `specs/004-spec-research-core/spec-fixture-design/` | fixture、hidden oracle、negative case、verifier 分离先例 | `FACT / local skeleton` |

## 2. 初步确认的结构事实

1. Spec Kit 的 lifecycle artifact 和 Skill runtime 文件拥有不同职责；本 Feature
   必须使用前者治理后者的改造。
2. 用户底稿已经把 13 个逻辑组件与文档投影区分开，但它位于外部 worktree，
   版本化和 hash 状态尚未冻结。
3. 当前 Nextflow-shaped 设计草案明确提出 `SKILL.md`、机器契约、Nextflow/
   scripts、tests/verifier/review 的分层；本 Feature 将其作为 proposal 输入。
4. 仅有 `SKILL.md` prose、目录存在或执行进程成功，不能证明一个组件有完整
   runtime contract 或科学正确性。
5. 用户希望的“快速阅读”和“Agent 可机械读取”不应强行共用同一种表示；稳定
   的 component/contract/provenance 关系比混合文件更重要。

## 3. Nextflow invariant 初步 ledger

| ID | 候选 invariant | 科研抽象 | 失败模式 | 状态 |
|---|---|---|---|---|
| NF-I01 | process/module 具有显式输入输出边界 | Skill/component 必须有 upstream/downstream contract | 大节点无法测试或替换 | `PROPOSAL→VERIFY` |
| NF-I02 | queue 与 value 语义不同 | 样本/contrast item 与共享 reference/design 的复用语义必须区分 | 共享数据被错误消费或重复计算 | `PROPOSAL→VERIFY` |
| NF-I03 | tuple/meta 随 payload 传递 | 身份、研究、分支和 reference 不得靠文件名/行号恢复 | 输出失去 sample/subject/contrast identity | `PROPOSAL→VERIFY` |
| NF-I04 | 依据稳定 key 对齐数据流 | join/mapping 必须保留 unmatched/duplicate 审计 | 样本错配、跨分支假交集 | `PROPOSAL→VERIFY` |
| NF-I05 | named take/emit 公开组合接口 | public Skill façade 不暴露内部节点依赖 | 内部重构破坏调用方 | `PROPOSAL→VERIFY` |
| NF-I06 | route/branch 显式表达 | ORA/GSEA、GO/KEGG、edgeR/limma 等不可由隐式默认值选择 | 方法/estimand 偷换 | `PROPOSAL→VERIFY` |
| NF-I07 | profile/config 与方法分离 | 资源、容器、executor 和方法科学语义分开 | 环境差异污染结果解释 | `PROPOSAL→VERIFY` |
| NF-I08 | cache/resume 由任务身份决定 | 输入、参数、脚本、参考和环境版本进入 execution identity | 陈旧结果被错误复用 | `PROPOSAL→VERIFY` |
| NF-I09 | work/cache 与 publish/report 分离 | 计算真相、稳定 artifact、给人看的视图和 review 状态不混淆 | report 被当作统计输入或批准 | `PROPOSAL→VERIFY` |
| NF-I10 | execution/scientific/review 状态分离 | 进程成功、verifier 通过和人工发布是不同状态 | exit 0 被升级为科研结论 | `PROPOSAL→VERIFY` |
| NF-I11 | provenance 和版本是横切输出 | 每个阶段都可追踪输入、命令、版本、参数、hash | 结果无法重现或解释 | `PROPOSAL→VERIFY` |
| NF-I12 | stub、fixture、negative case 和输出断言属于组件测试 | wiring 通过不等于科学结果通过 | 只测 exit 0 的假阳性 | `PROPOSAL→VERIFY` |

## 3.1 Invariant evidence records

The table below separates a directly documented execution fact from the
research translation proposed for this project. `FACT` does not mean that every
Bio Skill already implements the invariant.

| ID | Source | Scope/assumption | Research translation | Failure mode | Verification observable | Owner | Status |
|---|---|---|---|---|---|---|---|
| NF-I01 | [Nextflow Processes](https://docs.seqera.io/nextflow/process); [nf-core components](https://nf-co.re/docs/specifications/components/overview) | A process/module has declared inputs and outputs | Component has a narrow public boundary | Hidden side effects or untestable large node | Contract has required input/output ports and no undeclared public dependency | Core + execution | `FACT → INFERENCE` |
| NF-I02 | [Nextflow Processes](https://docs.seqera.io/nextflow/process) | Queue values are consumed; dataflow values may be reused | Shared references and per-item payloads declare different consumption semantics | Non-deterministic pairing or repeated/missing work | Port declares `queue/value` and cardinality; verifier rejects multiple queue inputs where unsupported | Core + verifier | `FACT → INFERENCE` |
| NF-I03 | [Nextflow Processes](https://docs.seqera.io/nextflow/process) | Tuple inputs can carry multiple values together | Identity metadata travels with payload | Sample/contrast identity is reconstructed from filenames or order | Contract port declares tuple fields and stable identity keys | Core + Bio profile | `FACT → INFERENCE` |
| NF-I04 | Local design plus [Nextflow Processes](https://docs.seqera.io/nextflow/process) | Joins require explicit matching keys | Scientific joins preserve unmatched/duplicate audit | Wrong sample or feature alignment | Verifier checks key uniqueness, namespace and unmatched records | Core + verifier | `INFERENCE → PROPOSAL` |
| NF-I05 | [Nextflow Processes](https://docs.seqera.io/nextflow/process); [Nextflow Workflows](https://docs.seqera.io/nextflow/workflow) | Named outputs are public references | Public façade does not depend on internal node names | Refactor breaks caller or exposes private topology | Contract `named_outputs` are stable and map to public ports | Core + execution | `FACT → INFERENCE` |
| NF-I06 | Local Skill sources and `spec-mvp/docs/NEXTFLOW-SHAPED-SKILLS-OUTPUT-STRUCTURE-zh-CN.md` | Method routes are domain declarations, not Nextflow syntax | ORA/GSEA, GO/KEGG and edgeR/limma choices are explicit | Method/estimand is silently changed by defaults | Route has selector, allowed values and estimand; missing selector blocks | Bio profile + Skill | `INFERENCE → PROPOSAL` |
| NF-I07 | [nf-core components](https://nf-co.re/docs/specifications/components/overview) | Parameters/resources and component logic can be configured separately | Environment changes are provenance, not scientific method changes | Environment drift contaminates interpretation | Provenance records config, executable, version and parameters separately | Core + execution | `FACT → INFERENCE` |
| NF-I08 | [Caching and resuming](https://docs.seqera.io/nextflow/cache-and-resume) | Cache reuse depends on task identity and outputs | Input, script, environment, params and reference versions are execution identity | Stale result is reused after semantic change | Run record lists identity inputs and artifact hashes; changed identity invalidates reuse | Execution + verifier | `FACT → INFERENCE` |
| NF-I09 | [Caching and resuming](https://docs.seqera.io/nextflow/cache-and-resume) | Work directory and published outputs have different roles | Work/cache, stable artifact, report and review are separate views | Report becomes statistical input or approval | Contract names separate output ports and review artifact | Core + review | `FACT → INFERENCE` |
| NF-I10 | Local root/feature constitutions and MultiQC wrapper | Process exit, verifier result and human approval are distinct events | Execution/scientific/release statuses cannot be inferred from one another | Exit 0 is upgraded to a scientific claim | Contract requires three status fields; negative run keeps release false/pending | Core + verifier + review | `INFERENCE → PROPOSAL` |
| NF-I11 | [Caching and resuming](https://docs.seqera.io/nextflow/cache-and-resume); [nf-core components](https://nf-co.re/docs/specifications/components/overview) | Reproducibility requires preserving task and environment context | Every stage emits source/version/param/command/hash evidence | Result cannot be reconstructed or explained | Input/artifact manifests and runtime metadata are present and hashed | Core + execution | `FACT → INFERENCE` |
| NF-I12 | [nf-core components](https://nf-co.re/docs/specifications/components/overview); local fixture design | Stub/fixture/negative checks cover wiring and failure boundaries | A component is not verified by exit 0 alone | False-positive success or silent degradation | Positive and negative verifier cases assert content, state and boundary | Verifier + review | `FACT → INFERENCE` |

The official pages were accessed on `2026-09-02 Asia/Shanghai`. They support
Nextflow/nf-core execution structure and engineering guidance; they do not
prove the scientific correctness of any Skill or the Research Core proposal.

## 4. 必须保持的研究边界

- Nextflow 官方语义需要通过官方文档/源码核验；本地设计文档只能证明“已有
  设计提案”，不能单独证明官方规范。
- 13 Skill 的共性需要从实际源内容和 representative cases 归纳；不能把上面
  12 条 invariant 直接套到每个组件而跳过审计。
- Research Core v0 是可证伪的设计假说：它必须能够描述新的、未参与构造的
  Skill/工作流，不能只在 13 个已知样例上达到形式覆盖。
- 量化结论必须绑定 task-level oracle/verifier；字段覆盖率只能告诉我们 schema
  能否容纳信息，不能证明方法有效。

## 5. 待核验的官方技术入口

以下链接是后续 source capture 的候选入口，不代表本文件已经完成版本锁定：

- [Nextflow Processes](https://docs.seqera.io/nextflow/process)
- [Nextflow Workflows](https://docs.seqera.io/nextflow/workflow)
- [Nextflow Modules](https://docs.seqera.io/nextflow/modules/)
- [Nextflow Caching and resuming](https://docs.seqera.io/nextflow/cache-and-resume)
- [nf-core component/module guidelines](https://nf-co.re/docs/guidelines/components/modules)
- [Spec Kit Quick Start](https://github.github.com/spec-kit/quickstart.html)

## 6. 研究记录状态

- [x] 对官方 Nextflow/nf-core 文档记录访问日期、URL、原文定位和适用范围；
      外部网站版本号仍保持 `UNKNOWN`，没有伪造版本。
- [x] 对 13 个组件逐项记录 source path、字段状态和当前运行证据；详见
      `contracts/skill-audit-record.yml`。
- [x] 为每条 invariant 添加 deterministic verification observable；代表性
      executable verifier 已落在 MultiQC case，其他组件仍未运行。
- [x] 记录用户对 C-001–C-005 的决定，并回写 `spec.md`。
- [ ] 产生至少一个不参与 Research Core 构造的 validation case；
      `shared-integration` 已保留为 validation reference，但尚未运行本 Feature
      的独立 verifier。
