# 转录组 Skills 合并审阅底稿：科研 Workflow 中文版

**版本**：draft-0.3（完成总览压缩与收敛决策，不改变任何运行逻辑）  
**用途**：把当前 spec-mvp/skills/ 中的项目适配器与英文 reference-stack 的 Skill 内容集中到一个 Markdown 文件，按科研 workflow 保留逐段证据；快速路由和重叠/合并/缺失判断统一见 [总览与收敛决策](../ALL-SKILLS-WORKFLOW-REFERENCE-zh-CN.md)。  
**重要状态**：这是详细合并审阅底稿，不是最终 Spec，不是新的运行时 Skill，也不是算法实现。第二步（总览）和第三步（重叠、可合并、不可替代、缺失）已在总览中完成；本文继续保留来源、方法细节和待验证证据，不直接删除或改写源文件。

## 0. 本轮到底做什么

本文件整合的是以下 13 个逻辑 Skill：

| 类型 | Skill |
|---|---|
| 项目适配器 | bulk-pa-luad、cross-branch-integration、multiqc、pathway-enrichment、wgcna-module-constraint |
| 英文参考 Skill | 01-mds、02-deg、02-deg-results、03-de-visualization、03-volcano、04-pathway-enricher、04-pathway-workflow、05-kegg |

来源关系如下：

~~~text
本机原始 Skill
  └── spec-mvp/skills/reference-stack/        英文审计副本
        └── spec-mvp/skills/reference-stack-zh-CN/  已有中文审阅镜像

上游能力 + 本项目边界
  └── spec-mvp/skills/<project-adapter>/      项目适配器
        └── .agents/skills/<project-adapter>/ 宿主发现副本

本文件
  └── 将上面 13 个逻辑 Skill 按科研数据流集中排版，并把说明性内容翻译成中文
~~~

本文件暂时遵守四条规则：

1. **先集中，再在总览中收敛**：同义段落在本文并列保留；删除、合并和不可替代判断见总览，源文件只有在后续合同和测试确认后才变更。
2. **先标来源，后提共性**：每一段保留原 Skill 名称和源文件路径，避免合并后失去出处。
3. **代码、函数名、参数名和文件名保持英文**：这样可以回到原文件核对，也避免翻译后不可执行。
4. **不把参考内容自动升级为项目合同**：参考 Skill 的建议只有在后续审查、Spec 化和 runtime 验证后，才可能成为项目规则。

### 0.1 配套入口

- [项目总览与收敛决策](../ALL-SKILLS-WORKFLOW-REFERENCE-zh-CN.md)
- [代码阅读地图](./CODE-READING-MAP-zh-CN.md)
  - [Skill 来源与翻译记录](../../SKILLS-SOURCE-AND-TRANSLATION.md)
- [项目 Skill staging README](../skills/README.md)
- [英文 reference-stack README](../skills/reference-stack/README.md)
- [中文 reference-stack README](../skills/reference-stack-zh-CN/README.md)
- [英文 workflow 顺序](../skills/reference-stack/analysis-order.md)
- [中文 workflow 顺序](../skills/reference-stack-zh-CN/analysis-order.md)
- [Skill catalog](../skills/skill-catalog.yml)
- [项目 specs、workflows、tests 和 evidence kernel](../../specs/)

### 0.2 本次清点范围与层级

本次总清点覆盖以下对象，但它们在合并稿中的职责不同：

| 对象 | 本次如何处理 | 是否作为运行时 Skill 计数 |
|---|---|---|
| .agents/skills/ | 只作为宿主发现副本核对 | 不单独计数 |
| spec-mvp/skills/ 五个项目目录 | 按项目适配器纳入 | 计为 5 个逻辑 Skill |
| spec-mvp/skills/reference-stack/ | 逐项合并英文参考内容 | 计为 8 个逻辑参考 Skill |
| spec-mvp/skills/reference-stack-zh-CN/ | 作为中文审阅/翻译镜像对照 | 不重复计数 |
| spec-mvp/skills/skill-catalog.yml | 核对 allowlist、source、libraries、phase、status | 不是 Skill runtime |
| bundles/ | 核对 bundle 提供的 preset、extension、workflow 注册 | 不是 Skill runtime |
| workflows/ 与 spec-mvp/workflows/ | 核对生命周期和执行编排 | 是 workflow，不是 Skill |
| specs/、spec-mvp/docs/、根目录中文文档 | 核对规格、证据、阅读地图和已有翻译 | 是 Spec/文档，不是 Skill |
| C:/Users/ldc/.codex/skills/ | 必要时只读核对本机原始来源 | 不自动纳入项目 |

本文件因此合并的是 13 个逻辑 Skill 的实质说明，同时把 bundle、workflow、Spec、测试和文档放在“控制面/验收面”中区分，而不是把所有目录内容混写成 Skill。

### 0.3 状态标签的读法

- **本机原始 Skill**：宿主或上游来源的原始材料，只用于来源核对。
- **英文参考副本**：reference-stack 中的英文审计副本，只供阅读和方法对照。
- **中文审阅版**：reference-stack-zh-CN 中的翻译/审阅镜像，不作为额外发现的运行时 Skill。
- **项目适配器**：spec-mvp/skills/ 下有项目边界、输入输出和 fail-closed 规则的适配层。
- **运行时**：有可执行入口、依赖、输入输出契约，并由 workflow 或测试实际接线；当前主要是 MultiQC 的 bounded vertical slice，其余需逐项确认。
- **仅设计**：存在 prose、示例或参考脚本，但尚未形成项目可调用 runtime。
- **尚未注册**：没有进入当前项目 runtime discovery/allowlist 的参考或外部能力；“有文件”不等于“已注册”。



### 0.5 统一审阅标注层：ARSSC

本合并稿从这一版开始使用一个项目内的临时名称：**ARSSC（Agent-Readable Scientific Skill Contract，Agent 可读科研 Skill 契约）**。它不是外部标准，也不是当前项目的 runtime contract；它只是把每个 Skill 已有的名称、来源、流程位置、输入、输出、方法、前置条件、硬边界和实现状态用固定键名再标一遍，便于后续比较、合并和 Spec 化。

每个 Skill 标题下的 `BEGIN_ARSSC` / `END_ARSSC` 注释遵守以下字段约定：

| 字段 | 允许的含义 |
|---|---|
| `skill_id` | 原始目录/Skill 名称；不得在合并阶段改名 |
| `display_name_zh` | 中文显示名；只是审阅标签，不替换 `skill_id` |
| `kind` | `project-adapter`、`reference-skill`、`optional-branch` |
| `primary_stage` / `secondary_stages` | 在 S00–S13 科研 Flow 中的主位置和辅助位置 |
| `source_role` | `project-adapter`、`english-reference-copy`、`local-original`、`chinese-review` |
| `source_paths` | 可回溯的原始/副本路径 |
| `registration` | `registered`、`not-registered`、`unknown` |
| `runtime_status` | `verified`、`not-verified`、`incomplete`、`reference-only` |
| `status_note_zh` | 对当前实现状态的中文解释；不得用它替代可执行测试证据 |
| `input_contract` / `output_contract` | 一行一个对象名或约束名；不是自由发挥的说明段落 |
| `core_apis` | 包、函数、CLI 或脚本入口；仅记录来源中已有内容 |
| `preconditions` | 执行前必须满足的事实或检查 |
| `hard_boundary` | 不得静默越过的科学、工程或解释边界 |

统一标注的最小语法如下。它是 Markdown 注释，不会被当作 R/Python/Bash 代码执行：

~~~text
<!-- BEGIN_ARSSC
contract_version: "0.1"
skill_id: "<原始 Skill 名称>"
display_name_zh: "<中文审阅名>"
kind: "project-adapter|reference-skill|optional-branch"
primary_stage: "Sxx"
secondary_stages: ["Sxx", "Sxx"]
source_role: "project-adapter|english-reference-copy|local-original|chinese-review"
source_paths: ["<path>"]
registration: "registered|not-registered|unknown"
runtime_status: "verified|not-verified|incomplete|reference-only"
input_contract: ["<object>"]
output_contract: ["<object>"]
core_apis: ["<package::function|CLI|script>"]
preconditions: ["<check>"]
hard_boundary: ["<must-not-cross>"]
END_ARSSC -->
~~~

阅读规则：注释里的状态不能推翻正文中的待确认项；如果注释和原始文件冲突，以原始文件和本合并稿明确的“待确认/审计问题”为准。状态 `not-verified` 不是失败结论，而是“尚未完成项目级运行验证”。

### 0.6 代码块的工程化标识

本稿保留 R、Python、Bash、PowerShell、CSV 和伪代码的原始语言标识；语言围栏只说明语法，不代表当前项目可以执行。后续若需要逐块审计，在代码围栏前加 `CODE_META` 注释，不改代码本体：

~~~text
<!-- CODE_META
code_id: "<stable-id>"
language: "r|python|bash|powershell|csv|text"
code_role: "reference-snippet|pseudocode|cli-shape|input-fixture|runtime-entrypoint"
source_path: "<source file or section>"
executable_in_current_project: false
validation_status: "not-run|passed|failed|unknown"
requires: ["<package|file|network|database>"]
input_contract: "<object or N/A>"
output_contract: "<object or N/A>"
END_CODE_META -->
~~~

当前默认规则是：没有 `CODE_META` 的代码块一律按 `reference-snippet`、`executable_in_current_project: false`、`validation_status: not-run` 解释。这样可以让正文继续保持可读，同时避免 Agent 把参考示例误当作可调用 runtime。

### 0.7 科研 Flow 与后续 Spec 抽象层

先保留两套编号，不把它们混成一套：

这套整体在项目内可暂称为 **EBAS（Evidence-First Bioinformatics Analysis Specification，证据优先生物信息学分析规格）**；如果只指六个工程抽象阶段，可写作 `EBAS-E0…E5`。这是本项目的工作名称，不声称是外部标准，也不意味着本稿已经完成 Spec 实现。

| 层 | 编号 | 作用 | 本稿是否实现 |
|---|---|---|---|
| 科研工作流层 | `S00–S13` | 描述生物信息学问题从输入到验收的真实顺序 | 是，本稿的主索引 |
| 工程/SPEC 抽象层 | `E0–E5` | 将多个 S 阶段抽象成可规格化的意图、契约、推断、整合和发布门 | 只做映射，不创建/修改 Spec |
| 单 Skill 契约层 | `ARSSC` | 描述单个 Skill 的接口、边界和状态 | 是，作为本稿的审阅注释 |

推荐的后续一一对应关系为：

| 工程层 | 覆盖的科研阶段 | 后续可承载的 SpecKit 对象 |
|---|---|---|
| `E0` 研究意图与 Claim 边界 | S00、S12 | `spec.md` 的需求、场景、成功标准和 claim boundary |
| `E1` 输入与数据契约 | S00–S02 | `data-model.md`、`contracts/`、fixture manifest |
| `E2` QC 与设计门 | S01–S04 | QC/design requirements、失败条件、验收矩阵 |
| `E3` 统计推断与结果产物 | S05–S07 | `research.md`、`plan.md`、DE/result/plot contracts |
| `E4` 解释分叉与跨分支整合 | S08–S11 | ORA/GSEA/KEGG/integration contracts 与决策规则 |
| `E5` provenance、验证与发布 | S12–S13 | `tests/`、`checklists/`、acceptance record、release claim |

`provenance` 是横切约束，不应只在 E5 最后补写；每个 S 阶段产生的对象都应带来源、版本、参数、输入快照或明确的缺失状态。以上仍只是后续规格化的骨架；本轮的删除/合并判断只落在总览的阅读入口和接口分层中，不据此删除或改写任何源 Skill。

## 1. 总 Flow：先按科研顺序放在同一张图上

~~~text
S00 输入/数据契约
    ↓
S01 样本与元数据 QC
    ↓
S02 原始数据/表达矩阵 QC
    ↓
S03 MDS/PCA 等样本诊断
    ↓
S04 设计矩阵/配对/批次/contrast
    ↓
S05 DEG 主推断
    ↓
S06 DE 结果整理
    ↓
S07 火山图 / MA / 热图
    ↓
S08 GO/KEGG 方法分叉：先判断 ORA 还是 GSEA
    ↓
S09 ID mapping / tested-gene universe
    ↓
S10 KEGG snapshot / SPIA / graphite 拓扑
    ↓
S11 跨分支整合
    ↓
S12 Claim / provenance
    ↓
S13 测试与验收

可选侧支：
S02/S03 ──→ WGCNA 模块发现与稳定性检查 ──→ S08/S09 pathway handoff

控制面（包住主 Flow，不等于生信步骤）：
constitution → specify → clarify → plan → tasks
                                           ↓
                            analyze / checklist / implement / review
~~~

### 1.1 Flow 中的输入输出关系

| 阶段 | 这一层必须回答的问题 | 主要 Skill/组件 | 典型输出 |
|---|---|---|---|
| S00 | 我拿到的是什么数据？样本单位、物种、ID、参考、问题和 estimand 是否明确？ | bulk-pa-luad 输入合同、pathway-enrichment 输入合同、bio-intake | manifest、metadata contract、未知项和允许的分析范围 |
| S01 | 样本 ID、组别、配对、批次、性状和映射是否完整？ | bulk-pa-luad、cross-branch-integration、metadata references | sample join audit、pairing audit、batch/confound audit |
| S02 | 上游工具日志或表达矩阵自身是否可用？ | multiqc、bio-qc、WGCNA 的 goodSamplesGenes | QC report、JSON、source map、表达矩阵质量摘要 |
| S03 | 样本之间的主要变异来自哪里？是否有离群、交换或批次主导？ | 01-mds、03-de-visualization 的 PCA/MDS 部分 | coordinates、distance、variance explained、loadings、样本诊断 |
| S04 | 要估计的组间效应是什么？配对、批次和 contrast 是否编码正确？ | bulk-pa-luad、02-deg、limma/edgeR references | design matrix、contrast record、可识别性和方向约定 |
| S05 | 模型、过滤、归一化、离散度和多重检验是否适用于输入？ | bulk-pa-luad、02-deg | fitted model、完整 DE 表、tested genes |
| S06 | 完整结果如何保存？padj=NA、FDR、注释、ranking、universe 如何解释？ | 02-deg-results | frozen DE table、significant list、ranking、ORA background、annotation |
| S07 | 怎样展示结果而不改变统计含义？ | 03-de-visualization、03-volcano | volcano、MA、heatmap、p-value histogram、plot parameters |
| S08 | 输入是预选 gene list 还是全量排名？应该走 ORA 还是 GSEA？ | pathway-enrichment、04-pathway-workflow、04-pathway-enricher | method decision、enrichment route、database choice |
| S09 | foreground、universe 和数据库需要什么 ID？映射损失是否可接受？ | pathway-enrichment、02-deg-results、04-pathway-workflow | mapping table、dedup rule、conversion rate、tested universe |
| S10 | KEGG 是否需要冻结？是否真的适合 SPIA/graphite 拓扑？ | 05-kegg、pathway-enrichment | KEGG ORA/GSEA、GSON snapshot、SPIA/graphite result、DB provenance |
| S11 | 两个分析分支能否比较？对应关系、ID、方向和尺度是否一致？ | cross-branch-integration | matched/unmatched、intersection、四类 direction strata、limitations |
| S12 | 当前结果能声明到哪一级？输入、命令、版本、参数和 hash 是否可追溯？ | adapter contracts、extensions、Spec/Claim 文档 | provenance、claim、review/release status |
| S13 | 结构、路由、方法、失败、重跑、独立复现和 Claim boundary 是否验收？ | tests、verifier、specs/004 fixture design | deterministic checks、human rubric、acceptance record |

## 2. S00–S06：输入、样本、原始数据、样本结构、设计与 DEG

### 2.1 项目适配器：bulk-pa-luad

<!-- BEGIN_ARSSC
contract_version: "0.1"
skill_id: "bulk-pa-luad"
display_name_zh: "PA-LUAD bulk paired DE 项目适配器"
kind: "project-adapter"
primary_stage: "S05"
secondary_stages: ["S00", "S01", "S04", "S06", "S09", "S12"]
source_role: "project-adapter"
source_paths: ["spec-mvp/skills/bulk-pa-luad/SKILL.md", ".agents/skills/bulk-pa-luad/SKILL.md"]
registration: "registered"
runtime_status: "not-verified"
status_note_zh: "项目适配器已登记；本合并稿未验证其完整 raw-count runtime。"
input_contract: ["integer_counts", "sample_metadata", "subject_pairing", "condition_levels", "contrast", "organism_namespace", "estimand_spec"]
output_contract: ["filtered_counts_manifest", "design_record", "contrast_record", "DE_result_table", "tested_gene_universe", "diagnostics", "provenance"]
core_apis: ["edgeR::DGEList", "edgeR::filterByExpr", "edgeR::normLibSizes", "edgeR::estimateDisp", "edgeR::glmQLFit", "edgeR::glmQLFTest", "limma", "stats::model.matrix"]
preconditions: ["sample_join_complete", "counts_are_integer", "pairing_is_explicit", "design_is_non_singular", "dependencies_available"]
hard_boundary: ["not_single_cell_per_cell_testing", "not_workflow_engine", "no_fabricated_positive_list"]
END_ARSSC -->

**来源文件**：spec-mvp/skills/bulk-pa-luad/SKILL.md  
**角色**：项目适配器，不是上游 edgeR 或 metadata Skill 的替代品。  
**定位**：从输入/元数据 QC 延伸到设计矩阵和 DEG 主推断。

#### 作用

为 PA-LUAD 场景提供 bulk paired differential-expression 的项目边界：

- edgeR 用于 count-model inference；
- limma 用于 paired/block continuous-data check；
- 配对 subject 必须进入设计矩阵；
- 结果必须把 signed statistics 和 tested-gene universe 交给下游。

#### 上游输入

- raw integer count matrix；
- sample metadata；
- 明确的 subject/pairing column；
- condition levels；
- contrast；
- organism/reference namespace；
- 定义 estimand 的 feature Spec。

#### 下游输出

- filtered-count manifest；
- design/contrast record；
- edgeR result table；
- 按请求生成的 paired limma result；
- diagnostics；
- 软件版本；
- input/output hashes；
- 下游 enrichment 所需的 tested-gene universe。

#### 核心包、函数和执行方式

执行入口是由宿主执行的 Rscript，而不是 Skill 文件本身：

~~~text
edgeR::DGEList
  → filterByExpr
  → normLibSizes / calcNormFactors
  → estimateDisp(robust = TRUE)
  → glmQLFit(robust = TRUE)
  → glmQLFTest
  → topTags / decideTests
~~~

配对设计的核心形状是：

~~~r
design <- model.matrix(~ subject + condition, metadata)
~~~

limma 的 paired/block 路径必须与目标 estimand 一致；不能因为 unpaired 代码更短就替换它。

#### 必须先做的决定

1. 每个 subject 是否恰好拥有要求的 condition levels；若是 repeated measures，必须显式记录。
2. counts 是否为整数；不能把 TPM、CPM、VST 或其他连续表达值送进 count model。
3. 是否在 normalization/dispersion 前使用 design-aware filterByExpr。
4. 是否使用明确的 normLibSizes(method = ...)、robust dispersion 和现代 edgeR QL test。
5. limma2 这个名字目前不能视为正式包名；在没有进一步说明前，只能按 limma paired/block 假设处理并记录。

#### 停止条件和不可替代边界

遇到下列情况应机器可读地停止：

- count matrix 非整数；
- metadata join 不完整；
- pairing 不明确；
- design singular；
- R 包缺失；
- 结果没有 expected tested-gene universe 或 tool version。

没有命中 DEG 是有效结果，不能把它改成 fabricated positive list。该适配器不处理 single-cell per-cell testing，也不负责 workflow-engine execution。

#### 当前状态

项目适配器已存在于 spec-mvp/skills/，并有对应 .agents/skills/ 副本；本合并稿不把它升级成已经完成的 raw-count runtime。

---

### 2.2 项目适配器：multiqc

<!-- BEGIN_ARSSC
contract_version: "0.1"
skill_id: "multiqc"
display_name_zh: "MultiQC 原始 QC 汇总适配器"
kind: "project-adapter"
primary_stage: "S02"
secondary_stages: ["S01", "S13"]
source_role: "project-adapter"
source_paths: ["spec-mvp/skills/multiqc/SKILL.md", ".agents/skills/multiqc/SKILL.md"]
registration: "registered"
runtime_status: "not-verified"
status_note_zh: "存在 bounded vertical-slice 接线线索；本合并稿未运行或验收。"
input_contract: ["upstream_QC_files", "tool_logs", "sample_source_map", "QC_policy"]
output_contract: ["multiqc_report_html", "multiqc_data", "summary_json", "source_map", "fail_warn_record"]
core_apis: ["multiqc CLI", "PowerShell wrapper", "workflow QC gate"]
preconditions: ["QC_inputs_exist", "sample_names_are_traceable", "output_directory_is_declared", "tool_versions_are_recorded"]
hard_boundary: ["report_generation_is_not_QC_interpretation", "does_not_replace_expression_matrix_QC", "does_not_silently_pass_failed_gate"]
END_ARSSC -->

**来源文件**：spec-mvp/skills/multiqc/SKILL.md  
**角色**：QC 报告生成和 workflow control adapter。  
**定位**：S02 原始数据/表达矩阵 QC；不替代 QC gate。

#### 作用

汇总上游工具已经产生的 QC 日志/指标，生成：

- 用户可以打开的 multiqc_report.html；
- 机器可读的 multiqc_data/；
- source mapping；
- wrapper verdict；
- review note；
- command/version metadata；
- output hashes。

#### 上游输入与下游输出

~~~text
upstream logs/metrics directory
  + expected sample/tool manifest
  + pinned config
  + output directory outside input tree
        ↓
project wrapper: extensions/bio-multiqc/scripts/run_multiqc.py
        ↓
MultiQC CLI
        ↓
HTML + JSON + source map + log + verdict + hashes
~~~

默认项目入口：

~~~powershell
python extensions/bio-multiqc/scripts/run_multiqc.py --input <input> --output <output> --config extensions/bio-multiqc/config/multiqc_config.yaml --multiqc-bin .venv/Scripts/multiqc.exe
~~~

#### 执行和检查顺序

1. 读取 feature spec.md，确定 expected sample/tool evidence；不能按 MultiQC 实际找到的文件临时推断 roster。
2. 用 pinned config 运行 wrapper，并保存 stdout、stderr、command、executable path 和 MultiQC version。
3. 检查 exit status、HTML、machine-readable data、source mapping、expected sample/tool marker 和 fixture-derived content marker。
4. 在机器检查之后直接审阅 HTML。
5. 把报告生成与 threshold gate、人审和 release 分开。

#### 停止条件和不可替代边界

以下情况必须停止：

- executable、input 或 config 缺失；
- 没有匹配到 intended module；
- expected sample/tool 缺失；
- machine-readable output 缺失；
- report 没有 fixture-derived evidence；
- 敏感数据启用了 AI/network summary；
- mode skip 被当作 release-ready。

MultiQC 聚合已有指标，不负责测量；报告漂亮不代表上游 QC 通过；threshold gate 必须是另外的检查。

#### 当前状态

项目适配器和 wrapper 存在，已有文档记录过 MultiQC 1.35 fixture vertical slice；本合并稿不把该历史记录当成当前环境本次执行证据。

---

### 2.3 参考 Skill：01-mds —— PCA、MDS、t-SNE、UMAP、PHATE

<!-- BEGIN_ARSSC
contract_version: "0.1"
skill_id: "01-mds"
display_name_zh: "样本降维与结构诊断"
kind: "reference-skill"
primary_stage: "S03"
secondary_stages: ["S02", "S07"]
source_role: "english-reference-copy"
source_paths: ["spec-mvp/skills/reference-stack/01-mds/SKILL.md", "spec-mvp/skills/reference-stack-zh-CN/01-mds/SKILL.md", "C:/Users/ldc/.codex/skills/dimensionality-reduction-plots/"]
registration: "not-registered"
runtime_status: "reference-only"
status_note_zh: "英文参考副本、本机来源和中文审阅镜像均存在；项目未登记专用降维 runtime。"
input_contract: ["transformed_expression_matrix", "sample_metadata", "distance_or_feature_matrix", "seed_if_stochastic"]
output_contract: ["embedding_coordinates", "distance_structure", "variance_explained", "loadings", "sample_diagnostic_plot"]
core_apis: ["DESeq2::vst", "PCAtools::pca", "limma::plotMDS", "stats::prcomp", "openTSNE", "umap", "PHATE"]
preconditions: ["raw_counts_are_transformed", "sample_metadata_join_complete", "distance_metric_is_declared", "random_seed_is_recorded_when_needed"]
hard_boundary: ["no_raw_count_PCA", "no_cluster_distance_claim_from_UMAP_or_tSNE", "no_trajectory_claim_from_2D_embedding_alone"]
END_ARSSC -->

**英文原件**：spec-mvp/skills/reference-stack/01-mds/SKILL.md  
**已有中文审阅版**：spec-mvp/skills/reference-stack-zh-CN/01-mds/SKILL.md  
**本机原始来源**：C:/Users/ldc/.codex/skills/dimensionality-reduction-plots/  
**定位**：S03 样本关系和降维诊断；不是 DEG 检验。

#### 作用和原则

选择与问题匹配的投影方法：

- PCA：线性方差、可解释载荷和方差解释率；
- t-SNE：局部邻域；
- UMAP：局部流形和部分全局结构；
- PHATE：连续转变和分支轨迹；
- classical MDS：全局欧氏距离；
- diffusion map：扩散距离和 pseudotime 支持；
- Isomap：kNN 图上的测地距离；
- force-directed/PAGA：图拓扑。

二维 embedding 会扭曲高维结构。尤其是 UMAP/t-SNE 的簇间距离、点密度和簇形状不能直接当作生物学事实。若要作轨迹 Claim，需要 RNA velocity、diffusion pseudotime、PHATE 或高维距离进行验证。

#### 方法选择表

| 方法 | 主要保留什么 | 主要参数 | 适合场景 | 主要失效边界 |
|---|---|---|---|---|
| PCA | 正交、按顺序排列的线性方差 | n_components、scaling | bulk 样本 QC、批次诊断、载荷解释 | 非线性流形；有效维度很少时的复杂结构 |
| t-SNE | 局部邻域相似性 | perplexity、learning_rate、n_iter、init | 单细胞局部簇边界 | 全局距离无意义；簇大小和随机性误导 |
| UMAP | 局部流形及部分全局关系 | n_neighbors、min_dist、spread、seed | 快速簇概览和补充投影 | 参数改变会碎裂或合并结构，仍有几何扭曲 |
| PHATE | 连续转变、分支轨迹 | knn、decay、t | 发育、分化、连续状态 | 速度较慢；不一定适合作为普通簇展示 |
| classical MDS | 全局 dissimilarity/Euclidean distance | n_components、距离矩阵 | 明确需要距离保持的场景 | 大于约 5000 个点时计算昂贵 |

#### bulk RNA-seq 首选：PCA

~~~r
library(DESeq2)
library(PCAtools)

vsd <- vst(dds, blind = FALSE)
p <- pca(assay(vsd), metadata = as.data.frame(colData(dds)))
biplot(p, colby = 'condition', shape = 'batch', lab = NULL,
       title = paste0('PCA: PC1 (', round(p$variance[1], 1), '%) vs PC2 (',
                      round(p$variance[2], 1), '%)'))
screeplot(p, components = 1:10)
plotloadings(p, components = 1, rangeRetain = 0.05)
~~~

PCA 轴必须标方差解释率。PC1/PC2 只解释很小比例时，视觉上的簇不能自动解释成稳定生物信号。

#### t-SNE 和 UMAP 的关键参数

~~~python
import openTSNE

embedding = openTSNE.TSNE(
    perplexity=30,
    n_iter=750,
    initialization='pca',
    learning_rate=X.shape[0] / 12,
    n_jobs=-1,
    random_state=42,
).fit(X)
~~~

~~~python
import umap

embedding = umap.UMAP(
    n_neighbors=30,
    min_dist=0.3,
    n_components=2,
    metric='euclidean',
    random_state=42,
).fit_transform(X)
~~~

- min_dist 主要控制簇的紧密程度，不是簇间分离度；
- n_neighbors 小会造成局部碎裂，大会让簇趋于合并；
- t-SNE perplexity 需要与样本数匹配；
- 不固定 seed 时，布局不能作为可重复图形；
- scanpy.pl.umap(save=...) 可能把文件写入 figures/ 并增加 umap 前缀，输出路径需要显式检查；
- scanpy 默认保存 DPI 150，出版图通常要明确设为 300 或更高。

#### 典型失败模式

| 现象 | 机制 | 正确处理 |
|---|---|---|
| 把 UMAP 簇间距离当生物学相似度 | UMAP 主要保持局部邻域 | 回到 PCA/高维距离或独立验证 |
| 每次运行图形变化 | 随机优化没有固定 seed | 固定 random_state/seed 并记录版本 |
| 小数据 t-SNE 碎裂 | perplexity 相对样本数过高 | 调整到与 n 匹配的范围 |
| PCA 的 PC1 只是 library size | raw counts 或变换不合适 | 先 VST/rlog 或 log+scale |
| 解释 UMAP 的细长/圆形簇 | 形状受参数和布局影响 | 只解释 cluster membership，并检查 marker |
| 把 PCA loadings 投射到 UMAP 轴 | UMAP 没有线性 loadings 语义 | 用 PCA 解释驱动基因，UMAP 只做展示 |

#### 参考阈值

- t-SNE perplexity：大样本常用 30–50；小样本需要按 n 调整；
- UMAP n_neighbors：约 15–50；
- UMAP min_dist：约 0.1–0.5；
- t-SNE Kobak–Berens learning rate：约 n / 12；
- 进入 UMAP 的 PCA 维度：常见 30–50；
- 出版 raster figure：通常至少 300 DPI；
- seed：任意固定整数，关键是可复现。

#### 当前状态

英文参考、本机原始来源和中文审阅版均存在；项目没有专门注册的 MDS/PCA runtime adapter。该 Skill 与 03-de-visualization 有功能交叉，暂不合并。

---

### 2.4 可选侧支：wgcna-module-constraint

<!-- BEGIN_ARSSC
contract_version: "0.1"
skill_id: "wgcna-module-constraint"
display_name_zh: "WGCNA 模块约束与稳定性检查侧支"
kind: "optional-branch"
primary_stage: "S03"
secondary_stages: ["S08", "S09", "S11", "S13"]
source_role: "project-adapter"
source_paths: ["spec-mvp/skills/wgcna-module-constraint/SKILL.md", ".agents/skills/wgcna-module-constraint/SKILL.md"]
registration: "registered"
runtime_status: "incomplete"
status_note_zh: "项目适配器和参考脚本存在；缺少完整 fixture、golden module、stability/preservation verifier 和 runtime。"
input_contract: ["expression_matrix", "sample_metadata", "network_parameters", "module_analysis_question"]
output_contract: ["module_assignments", "eigengenes", "hub_candidates", "constraint_sets", "stability_diagnostics"]
core_apis: ["WGCNA::goodSamplesGenes", "WGCNA module functions"]
preconditions: ["sample_size_is_adequate", "expression_scale_is_declared", "network_type_is_declared", "metadata_is_joined"]
hard_boundary: ["grey_module_is_not_biological_evidence", "coexpression_is_not_causality", "preservation_requires_diagnostic", "does_not_replace_DEG"]
END_ARSSC -->

**来源文件**：spec-mvp/skills/wgcna-module-constraint/SKILL.md  
**定位**：从 S02/S03 进入模块发现，再把满足稳定性条件的模块交给 S08/S09；不是主线必经步骤。

#### 作用

在 bulk normalized expression 上：

- 构建 signed co-expression network；
- 选择 soft power；
- 检测模块；
- 计算 module eigengenes；
- 做 module-trait association；
- 用 signed kME 定义 hub；
- 在通过 stability/preservation 规则后，形成下游模块约束 gene set。

#### 上游输入与输出

输入：

- normalized expression matrix，samples × genes；
- sample traits；
- subject/batch metadata；
- gene namespace；
- module constraint policy。

输出：

- sample/gene QC；
- signed network/soft-power record；
- module labels；
- eigengenes；
- module-trait correlations 和 p-values；
- kME hub table；
- preservation evidence（只有在确实执行时）；
- 带 provenance 的 constrained downstream gene sets。

#### 核心包和函数

~~~text
WGCNA::goodSamplesGenes
  → pickSoftThreshold(networkType = 'signed')
  → blockwiseModules(networkType = 'signed')
  → moduleEigengenes
  → cor / corPvalueStudent
  → signedKME
~~~

pickSoftThreshold 和 blockwiseModules 的 networkType 必须一致，不能一边按 signed 选 power、另一边按 unsigned 建网。

#### 前置条件和停止规则

- 样本数达到 preset 最低要求；参考 usage guide 建议可靠检测至少约 20 个样本，绝对下限约 15，但正式阈值仍需项目确认；
- 设计不奇异；
- batch 和 biology 不被静默混淆；
- outlier 处理、block size、soft power 和 network type 有记录；
- 稳定性/preservation 确实有执行的诊断。

以下情况应停止或降级为 reference-only：样本太少、设计奇异、network type 不一致、把 grey module 当作生物学证据、声称 preservation 却没有诊断、把 marginal co-expression 写成因果调控。

#### 当前状态

项目适配器和参考脚本存在；没有固定 expression fixture、golden module、stability/preservation verifier 或完整 runtime。

### 2.5 参考 Skill：02-deg —— DEG 主推断

<!-- BEGIN_ARSSC
contract_version: "0.1"
skill_id: "02-deg"
display_name_zh: "DEG 主推断参考 Skill"
kind: "reference-skill"
primary_stage: "S05"
secondary_stages: ["S04", "S06", "S07"]
source_role: "english-reference-copy"
source_paths: ["spec-mvp/skills/reference-stack/02-deg/SKILL.md", "spec-mvp/skills/reference-stack-zh-CN/02-deg/SKILL.md"]
registration: "not-registered"
runtime_status: "reference-only"
status_note_zh: "源 Skill 描述了 CLI、scripts、references 和 tests，但未被当前项目接线为统一 runtime。"
input_contract: ["expression_matrix", "group_or_design_metadata", "contrast", "method_parameters", "reproducibility_record"]
output_contract: ["complete_DE_table", "significant_gene_list", "filtered_result_table", "base_visualizations", "session_info"]
core_apis: ["limma", "DESeq2", "edgeR", "optparse", "Rscript scripts/main.R"]
preconditions: ["sample_names_match", "at_least_two_groups", "data_scale_matches_method", "design_is_identifiable", "multiple_testing_policy_is_declared"]
hard_boundary: ["group_file_is_not_full_design", "p_threshold_is_not_FDR_claim", "post_hoc_logFC_filter_is_not_effect_test", "no_fabricated_positive_result"]
END_ARSSC -->

**来源**：spec-mvp/skills/reference-stack/02-deg/SKILL.md  
**上游标识**：differential-expression-analysis；来源说明指向 AIPOCH 的 medical-research-skills。  
**在总 Flow 中的位置**：S05 DEG 主推断；它还会产生 S06 结果整理和 S07 可视化所需的基础结果。  
**当前状态**：英文参考副本；源文档描述了 CLI、scripts、references 和 tests，但本项目不把参考副本自动视为运行时 Skill，脚本、测试数据和依赖仍需单独审计。

#### 作用

针对 bulk RNA-seq 或 microarray 的两组或多组表达数据，完成输入检查、差异表达模型运行、多重检验校正、显著性筛选和基础 volcano/heatmap 输出。它明确排除 single-cell RNA-seq、methylation 和非表达数据。

在本项目总 Flow 中，本 Skill 只代表“如何从已定义的表达矩阵和比较关系得到差异结果”的主推断层；设计矩阵、配对、批次、contrast 的科学定义必须由 S04 先固定，不能因为脚本支持多个方法就把方法选择变成事后试错。

#### 上游输入

| 输入 | 约束或问题 |
|---|---|
| expression matrix | CSV；gene 为行、sample 为列；第一列为 gene ID；必须先明确是 raw counts 还是 normalized/log-scale 表达值 |
| group file | 至少包含 sample ID 与 group；sample ID 必须和表达矩阵列名一一对应 |
| contrast/design | 原始 Skill 的最小接口只写 group；复杂实验仍需补充 paired、batch、sex、subject、interaction 等设计信息 |
| 方法与阈值 | diff_method、norm_method、p_threshold、logfc_threshold；阈值须和 estimand、FDR 口径一起记录 |
| 可复现信息 | seed、R/package versions、session info、输入文件校验信息 |

示例输入：

~~~csv
"","GSM1442228","GSM1442229","GSM1442230"
"0610006L08Rik",3.438,3.237,3.265
"0610007P14Rik",6.734,7.017,6.807
~~~

~~~csv
"ID","group"
"GSM1442228","Control"
"GSM1442229","Control"
"GSM1442230","DIC"
~~~

注意：该最小 group file 不足以表达配对和批次。若研究问题需要这些变量，必须在 S04 扩展输入契约，而不是把 group file 当作完整设计矩阵。

#### 下游输出

源文档列出的文件接口包括：

| 输出 | 作用 |
|---|---|
| Diffanalysis.csv | 完整结果；典型列为 gene_id、logFC、Pvalue、Padj |
| temp/rdegs.csv | 筛选后的显著差异基因 |
| temp/Diffanalysis_filtered.csv | 带分组注释的完整结果 |
| volcano_plot.pdf | 基于显著性和 fold-change 阈值的火山图 |
| heatmap.pdf | top up/down genes 的热图 |
| session_info.txt | R 会话和包版本信息 |

进入后续层时，需要把这些脚本输出转换为明确的结果契约：比较名称、reference level、effect/LFC 列、raw p-value、adjusted p-value、tested-gene 集合、过滤规则、排序规则和 provenance。单有一个名为 Diffanalysis.csv 的文件不能保证这些字段语义一致。

#### 原始执行接口

源 Skill 给出的 CLI 形态如下；这里只作为参考接口记录，不代表本项目已经允许或已经验证该命令：

~~~bash
Rscript scripts/main.R \
  --input_file ./expression_matrix.csv \
  --group_file ./group_info.csv \
  --output_dir ./output/ \
  --diff_method limma \
  --p_threshold 0.05 \
  --logfc_threshold 0.1 \
  --seed 42
~~~

参数语义：

| 参数 | 默认值 | 含义 |
|---|---:|---|
| input_file | 必填 | 表达矩阵 |
| group_file | 必填 | sample ID 与 group |
| output_dir | ./output/ | 输出目录 |
| diff_method | limma | limma、deseq2、edger、t、wilcox |
| norm_method | TMM | edgeR 路径的 TMM、RLE 或 upperquartile |
| p_threshold | 0.05 | 源脚本层面的 p-value 阈值；不能直接等同于 FDR |
| logfc_threshold | 0.1 | 源脚本层面的 logFC 筛选阈值；不能代替 TREAT 或 lfcThreshold |
| seed | 42 | 随机性控制 |

#### 方法边界

| 方法 | 源 Skill 的定位 | 进入项目时必须补充的边界 |
|---|---|---|
| limma | 线性模型与 empirical Bayes moderation；源文档推荐 normalized expression，如 FPKM/TPM | 若输入是 raw counts，应明确使用 voom/适配路径，而不是直接把 counts 当连续正态数据 |
| DESeq2 | negative binomial GLM；适合 raw counts | 需要正式 design、reference level、contrast、independent filtering、Cook's distance 和 LFC shrinkage 记录 |
| edgeR | TMM normalization、dispersion estimation 和 count model | 需要明确 DGEList、过滤、设计矩阵、QL test/contrast 以及是否使用 glmTreat |
| t-test | 简单成对参数检验 | 不能代替计数模型；需检查变换、独立性、方差和重复结构 |
| Wilcoxon | 简单成对非参数检验 | 对 ties、小样本、多重检验和协变量处理有限，不能自动解决批次或配对问题 |

#### 内置工作流与项目对接

1. **Validate Input**：检查文件存在、sample 名称匹配、每组至少有两个样本。
2. **Run Differential Expression**：选择 limma、DESeq2、edgeR、t-test 或 Wilcoxon，计算 effect/logFC、p-value，并做 Benjamini–Hochberg 校正。
3. **Filter Results**：按阈值筛选，分类为 Up、Down 或 Not significant。
4. **Generate Visualizations**：生成 volcano 和 top-gene heatmap。

对本项目而言，这四步需要拆开映射到 S04–S07：输入验证不能代替设计审计；计算 p-value 不能代替 estimand 定义；按 p-value 和 logFC 筛选不能代替 S06 对 padj、效应阈值和 tested universe 的审计；内置图不能代替 S07 的统一可视化契约。

#### 错误与停止条件

源 Skill 的错误码包括：

| 错误 | 触发 | 处理 |
|---|---|---|
| SKILL_FILE_NOT_FOUND | 输入文件不存在 | 核对路径和文件清单 |
| SKILL_SAMPLE_MISMATCH | sample 名称不匹配 | 核对 group file 与表达矩阵列名 |
| SKILL_INVALID_DATA | 少于两个 group 或每组样本不足 | 回到 S01/S04，不强行运行 |
| SKILL_FILTER_ERROR | 没有显著基因 | 先检查数据质量、设计和检验效能，再决定是否改变阈值 |
| SKILL_DEPENDENCY_MISSING | R 包缺失 | 记录环境，不能静默换方法 |

不可替代的边界：

- 只用 group 列时，不能声称已经控制 paired、batch、sex 或 subject；
- p_threshold 不能被写成 FDR 控制结论；
- logfc_threshold 的 post-hoc 筛选不能自动变成“显著且达到生物学效应”的正式检验；
- 没有显著基因不能直接归因于阈值过严，必须先检查 S01–S04 的输入、质量、设计和对比；
- 一次运行多个方法后只挑最好看的结果，会破坏 Claim/provenance。

#### 测试与实现清单（保留原参考内容）

源 Skill 声称包含以下实现项：optparse CLI、set.seed()、requireNamespace() 依赖检查、session info、临时文件清理、模块化脚本、tests/data、SKILL_* 错误码、scripts/ 和 references/ 目录。它还给出 Rscript scripts/main.R --help、样例数据运行、输出行数检查和 volcano 文件存在性检查。

在当前项目中，这些是待核对的参考验收要求，而不是已完成的项目验收。后续需要确认：

- scripts、references、tests/data 是否实际存在于当前项目；
- limma/DESeq2/edgeR 路径是否都与项目输入契约兼容；
- 输出字段是否能支持 S06、S08 和 S09；
- 失败时是否有可定位的错误证据；
- session_info 是否足以锁定运行环境。

### 2.6 参考 Skill：02-deg-results —— DE 结果整理、FDR、注释和 pathway handoff

<!-- BEGIN_ARSSC
contract_version: "0.1"
skill_id: "02-deg-results"
display_name_zh: "DE 结果整理、FDR、注释与 pathway handoff"
kind: "reference-skill"
primary_stage: "S06"
secondary_stages: ["S05", "S08", "S09", "S12"]
source_role: "english-reference-copy"
source_paths: ["spec-mvp/skills/reference-stack/02-deg-results/SKILL.md", "spec-mvp/skills/reference-stack-zh-CN/02-deg-results/SKILL.md"]
registration: "not-registered"
runtime_status: "reference-only"
status_note_zh: "方法内容较完整，但尚未由项目 adapter 封装成统一结果契约和 runtime。"
input_contract: ["fitted_DE_object", "effect_and_pvalue", "padj", "tested_gene_set", "annotation_namespace", "threshold_policy"]
output_contract: ["frozen_DE_table", "significant_lists", "ranked_vector", "annotation_table", "tested_gene_universe", "mapping_audit"]
core_apis: ["DESeq2::results", "edgeR", "IHW", "qvalue", "ashr", "AnnotationDbi::mapIds", "clusterProfiler"]
preconditions: ["fit_object_is_identified", "effect_direction_is_declared", "padj_semantics_are_known", "tested_universe_is_recoverable", "ID_namespace_is_declared"]
hard_boundary: ["padj_NA_is_not_zero", "annotation_symbol_is_not_stable_join_key", "ORA_universe_is_not_whole_genome_by_default", "does_not_recompute_S05_inference"]
END_ARSSC -->

**来源**：spec-mvp/skills/reference-stack/02-deg-results/SKILL.md  
**在总 Flow 中的位置**：S06 DE 结果整理，并向 S08–S10 提供 ranked list、显著 gene list、annotation 和 tested-gene universe。  
**当前状态**：英文参考副本；方法内容较完整，但尚未被项目 adapter 封装成统一 runtime contract。

#### 作用

从 DESeq2 或 edgeR 的已拟合对象中提取 effect、p-value 和 adjusted p-value，正确解释 padj=NA，选择与研究问题匹配的 FDR 方法，进行 gene annotation，并准备 GSEA preranked 输入或 ORA 的 tested-gene background。

核心问题不是如何导出 CSV，而是每一个基因为什么被测试、为什么通过或没有通过校正、该结果支持哪个 estimand，以及下游 pathway 使用的输入集合到底是什么。

#### padj=NA 的三种语义

padj 为 NA 不是普通缺失值。至少要区分以下三类原因，处理方式不能混用：

| 原因 | DESeq2 线索 | 统计含义 | 若确实需要保留，处理方向 |
|---|---|---|---|
| independent filtering | pvalue 有值、padj 为 NA、baseMean 低于自动阈值 | 为提高给定 alpha 下的检出数，被独立过滤排除 | results(dds, independentFiltering = FALSE) 或明确使用 filterFun = ihw 做敏感性分析 |
| Cook's distance outlier | pvalue 和 padj 都为 NA、baseMean 大于 0、通常有至少 3 个重复 | 单个样本的 Cook's distance 超过阈值 | 只有在诊断后才考虑 cooksCutoff = FALSE；不能无条件关闭 |
| 某组全零或近零 | pvalue 为 NA、baseMean 极低 | 信息不足，无法形成有效检验 | 预处理过滤或接受其不可检验状态 |

独立过滤必须和零假设下的检验统计量独立。跨样本平均表达量通常满足这一原则；用“处理组最小 count”作为事后过滤条件可能破坏独立性并膨胀 I 类错误。样本数达到一定规模时，DESeq2 还可能通过 replaceOutliers() 替换异常 count 并重新拟合；连续协变量设计下的 Cook's 过滤行为也需要单独确认。

不可替代的规则：不能对结果表直接执行 na.omit()，然后把剩下的行当成全部可解释基因。必须记录 NA 的原因、数量、受影响的 gene set 和是否做过敏感性分析。

#### FDR / 效应阈值方法分类

| 方法 | 实际控制或估计的对象 | 适用场景 | 主要边界 |
|---|---|---|---|
| BH：p.adjust(method = 'BH') 或 DESeq2 默认 BH | 固定 alpha 下的 FDR | 大多数常规 bulk DE | 需要说明测试集和依赖结构 |
| Storey q-value：qvalue::qvalue | 估计 pi0 后的 q-value | 测试数较多、零假设比例估计稳定时 | 小测试集时 pi0 估计可能不稳定 |
| IHW：results(filterFun = ihw) | 用独立协变量加权的 BH | 希望在相同 FDR 下提高 power | 协变量必须在零假设下独立，且要有足够测试数 |
| ashr lfsr / svalue | 效应方向错误的概率或其聚合控制 | 重点是方向可靠性 | lfsr/svalue 不是 padj，不可互换 |
| BY | 任意依赖下更保守的 FDR 控制 | 需要对任意依赖做保守控制时 | 通常显著牺牲 power |
| Holm / Bonferroni | FWER | 小规模确认性假设集合 | 不适合直接用于 genome-scale DE |
| TREAT / lfcThreshold | 对 abs(LFC) > tau 的假设做正式检验 | 效应大小预先定义且是核心 claim | tau 必须在看结果前设定 |

特别重要：padj < 0.05 再事后筛 abs(LFC) > 1，控制的是“非零效应”的 FDR，不等同于对“效应大于 1”的 FDR 控制。若 claim 是生物学意义上的最小 fold change，应使用 results(dds, lfcThreshold = ..., altHypothesis = 'greaterAbs') 或 edgeR 的 glmTreat()，并让方法段落与真实检验对象一致。

#### 场景决策表

| 场景 | 参考做法 | 必须记录的理由或限制 |
|---|---|---|
| 常规两组 bulk DE | DESeq2 + 默认 BH，报告 padj | 记录 design、contrast、tested set 和 alpha |
| 希望在相同 FDR 下增加 power | results(dds, filterFun = ihw) | 记录 covariate、版本、权重方法和敏感性 |
| 预先定义有意义的 fold change | lfcThreshold 或 glmTreat | 报告的是幅度假设的 FDR，而不是非零假设的 FDR |
| GSEA preranked | DESeq2 的 stat 或 shrunken LFC；edgeR 需明确 rank 构造 | 不使用仅通过显著性筛选后的子集 |
| ORA | 显著 gene list + 所有实际 tested genes 作为 background | 不能默认使用全基因组 |
| 很多 padj=NA | 先区分 independent filtering、Cook's outlier、全零 | 不能 blanket drop NA |
| 多条件 | 先用 LRT 判断任意变化，再用 pairwise Wald 获取具体效应 | LRT padj 是 omnibus 结论，LRT 的 LFC 不应被误读成某一 pairwise effect |
| 每组 n 小于等于 3 | 作为探索性结果，强调不稳定性 | 需要独立验证，不能把 gene list 当稳定事实 |
| 人/鼠混合性别 | 将 sex 作为协变量并做 sex-stratified sensitivity | 避免把性别差异误当 treatment effect |
| 原核数据 | 使用 Prokka/Bakta GFF 和 KEGG strain code | Ensembl/org.db 的 eukaryote 映射不能直接套用 |

#### 从拟合对象提取结果

DESeq2 需要明确 resultsNames(dds) 中的 coefficient 或 contrast，edgeR 需要明确 topTags() 的对象和排序方式：

~~~r
library(DESeq2)
library(dplyr)

resultsNames(dds)
res <- results(dds, name = 'condition_treated_vs_control', alpha = 0.05)
res_shrunk <- lfcShrink(dds, coef = 'condition_treated_vs_control', type = 'apeglm')

res_df <- as.data.frame(res)
res_df$gene <- rownames(res_df)
~~~

~~~r
library(edgeR)
tt <- topTags(qlf, n = Inf, sort.by = 'none')$table
tt$gene <- rownames(tt)
~~~

sort.by = 'none' 用来保留原始 gene 顺序，便于按行与 annotation 表对齐；默认按 p-value 排序时，直接按行 join 可能把注释配错。

跨工具列名不能混用：

| 工具 | effect/LFC 列 | adjusted p-value 列 |
|---|---|---|
| DESeq2 | log2FoldChange | padj |
| edgeR | logFC | FDR |
| limma topTable | logFC | adj.P.Val |
| limma topTreat | logFC | adj.P.Val；但其检验对象是 TREAT 幅度假设 |

#### IHW、q-value 与 ashr

IHW 的目的，是使用通常与检测 power 相关、但在零假设下独立的协变量进行加权。在测试数不足、协变量与 treatment 相关或协变量不能解释 power 时，不应默认 IHW 会带来收益。

~~~r
library(IHW)
res_ihw <- results(dds, filterFun = ihw, alpha = 0.05)
~~~

Storey q-value 是另一套框架，需要说明 pi0 估计：

~~~r
library(qvalue)
qv <- qvalue(res$pvalue[!is.na(res$pvalue)])
res$qvalue <- NA
res$qvalue[!is.na(res$pvalue)] <- qv$qvalues
~~~

ashr 用于估计局部错误方向概率；需要 svalue = TRUE 才会产生 svalue 列：

~~~r
res_ashr <- lfcShrink(
  dds,
  coef = 'condition_treated_vs_control',
  type = 'ashr',
  svalue = TRUE
)
res_ashr$svalue
~~~

报告时必须说清楚是 padj、qvalue、lfsr 还是 svalue；它们回答的问题不同。

#### p-value histogram 诊断

在相信 gene list 前，先画 raw p-value 的分布。理想情况下，零假设基因在 0–1 区间近似均匀，真实 signal 在 0 附近形成额外峰。

~~~r
library(ggplot2)

ggplot(res_df, aes(x = pvalue)) +
  geom_histogram(bins = 50, fill = 'steelblue', color = 'white') +
  labs(x = 'P-value', y = 'Frequency', title = 'P-value distribution') +
  theme_bw()
~~~

| 形状 | 可能含义 | 下一步 |
|---|---|---|
| 均匀背景 + 0 附近峰 | 设计与检验大体合理 | 继续做结果和残差诊断 |
| U 形、两端都高 | 隐藏 batch、未建模混杂或 dispersion misspecification | 回到 PCA/batch、design 和 dispersion |
| 0 附近缺失、1 附近高 | 过度校正、协变量过多或 dispersion 处理不当 | 检查模型复杂度和 dispersion |
| p=1 的尖峰 | 极低表达或离散计数伪影 | 检查预过滤 |
| 约 0.5 附近异常峰 | 非典型离散检验或输入问题 | 回溯数据和检验实现 |

#### 结果筛选、排序和分组

筛选条件必须显式写出，尤其是 NA 处理、tested set 和效应阈值：

~~~r
sig <- res_df |>
  dplyr::filter(!is.na(padj), padj < 0.05,
                abs(log2FoldChange) > 1, baseMean > 10) |>
  dplyr::arrange(padj)

up <- sig |> dplyr::filter(log2FoldChange > 0)
down <- sig |> dplyr::filter(log2FoldChange < 0)

n_tested <- sum(!is.na(res$padj))
n_sig <- sum(res$padj < 0.05, na.rm = TRUE)
cat(sprintf(
  'Tested: %d   Significant (padj<0.05): %d   Up: %d   Down: %d\n',
  n_tested, n_sig,
  sum(sig$log2FoldChange > 0),
  sum(sig$log2FoldChange < 0)
))
~~~

baseMean > 10 只是示例筛选，不应在没有项目理由时硬编码为普适阈值。下游要分别保留：完整结果、可检验结果、显著结果、方向子集、GSEA 全量 rank 和 ORA 的 tested background。

#### Gene annotation 与稳定 ID

优先使用本地、版本固定的 AnnotationDbi::mapIds 与 org.db；缺失时再使用 biomaRt 或 mygene。显示 symbol 不应作为主连接键，稳定的 Ensembl、Entrez 或 locus_tag 才是跨层 join 的候选键。

~~~r
library(org.Hs.eg.db)
library(AnnotationDbi)

res_df$symbol <- mapIds(
  org.Hs.eg.db,
  keys = sub('\\..*', '', res_df$gene),
  keytype = 'ENSEMBL',
  column = 'SYMBOL',
  multiVals = 'first'
)

res_df$entrez <- mapIds(
  org.Hs.eg.db,
  keys = sub('\\..*', '', res_df$gene),
  keytype = 'ENSEMBL',
  column = 'ENTREZID',
  multiVals = 'first'
)
~~~

简单去掉 Ensembl version 的正则表达式可能破坏 GENCODE 的 _PAR_Y 后缀；应采用能保留该后缀的规则并在日志中记录。HGNC symbol 可能改名，旧 symbol 可能导致下游工具静默丢基因，因此 symbol 只作为 display label 更稳妥。原核数据可从 Prokka/Bakta GFF 的 locus_tag、Name 和 product 建 annotation 表。

#### GSEA preranked 输入

GSEA 需要全量、可排序的 tested genes，不是只保留显著基因的列表。DESeq2 推荐使用 Wald statistic stat 或 shrunken LFC；edgeR 要明确使用哪一个可比的 rank 构造。

~~~r
gsea_ranks <- res_df$stat
names(gsea_ranks) <- res_df$gene
gsea_ranks <- sort(gsea_ranks[!is.na(gsea_ranks)], decreasing = TRUE)

gsea_ranks_edger <- sign(tt$logFC) * -log10(tt$PValue)
names(gsea_ranks_edger) <- rownames(tt)
gsea_ranks_edger <- sort(
  gsea_ranks_edger[is.finite(gsea_ranks_edger)],
  decreasing = TRUE
)
~~~

不要用未收缩、低 count 噪声很大的 LFC 直接作为唯一 rank，也不要先按 padj 筛选再声称做了 GSEA。

#### ORA 输入与 tested-gene universe

ORA 的显著输入可以是 padj 通过阈值的 gene list，但 background 必须是实际被测试、且能够进入该 annotation universe 的 gene set，而不是物种全基因组：

~~~r
library(clusterProfiler)

sig_entrez <- na.omit(res_df$entrez[res_df$padj < 0.05])
bg_entrez <- na.omit(res_df$entrez[!is.na(res_df$padj)])

ora <- enrichGO(
  gene = sig_entrez,
  universe = bg_entrez,
  OrgDb = org.Hs.eg.db,
  keyType = 'ENTREZID',
  ont = 'BP',
  pAdjustMethod = 'BH'
)
~~~

不传 universe 时，某些工具会默认使用该物种的所有已注释基因，包含从未进入本次检验的基因，导致 enrichment p-value 偏小。S09 必须保存 universe 的构造来源、过滤规则、ID 映射损失和版本。

#### DESeq2 与 edgeR 的 concordance

可以在相同过滤、相同设计和相同 contrast 下比较两种模型的结果：

~~~r
deseq2_sig <- rownames(subset(deseq2_res, padj < 0.05))
edger_sig <- rownames(subset(edger_tt, FDR < 0.05))

common <- intersect(deseq2_sig, edger_sig)
deseq2_only <- setdiff(deseq2_sig, edger_sig)
edger_only <- setdiff(edger_sig, deseq2_sig)

cat(sprintf(
  'DESeq2 sig: %d   edgeR sig: %d   Common: %d (%.1f%%)\n',
  length(deseq2_sig), length(edger_sig), length(common),
  100 * length(common) / min(length(deseq2_sig), length(edger_sig))
))
~~~

源 Skill 给出的经验性提示是：top 500 的 concordance 高于约 70% 时可视为较稳健，低于约 60% 时应优先检查 filtering、normalization 和 design，而不是简单归因于工具不同。该阈值只作审计提示，不是项目验收标准。

#### 典型失败模式

| 现象 | 机制 | 正确回退 |
|---|---|---|
| na.omit() 后关键基因消失 | independent filtering 或 Cook's distance | 诊断 NA 原因；只在有理由时关闭对应过滤 |
| 把 padj < 0.05 & abs(LFC) > tau 写成幅度 FDR | BH 控制的是非零效应假设 | 使用 TREAT 或 lfcThreshold |
| ORA 结果异常丰富 | 漏传 universe | 使用 post-filtering 的 tested gene IDs |
| n=3 的 gene list 在重复队列中不稳定 | 小样本下 power 和排序高度波动 | 作为 hypothesis-generating，做正交验证 |
| 混合性别但未入模 | sex 与 condition 混杂 | 加入 sex；对 chrX/chrY 结果做敏感性 |
| DESeq2 使用 FDR 列名 | 列名与 edgeR 混用 | DESeq2 用 padj，edgeR 用 FDR |
| summary(res) cutoff 与 results(alpha=) 不同 | summary 默认 alpha 可能不同 | 显式传 alpha |
| 所有 padj 都是 NA | 全部被过滤或输入数据异常 | 检查 independentFilteringResults(res)、baseMean 与输入 |
| LFC 方向相反 | reference level 未固定 | 在拟合前使用 relevel() |
| symbol mapping 低于 50% | Ensembl version、symbol rename 或物种不匹配 | 核对 release、keytype、物种和稳定 ID |

#### 不可替代的边界

- 结果整理不能反过来改变已经完成的 design/contrast；
- padj、q-value、lfsr、svalue 必须保留名称和统计语义；
- 完整结果、tested universe、显著子集、GSEA rank 不得互相冒充；
- annotation 失败率必须可见，不能把未映射 ID 静默删除；
- 任何跨工具比较都必须说明输入过滤、设计、reference level 和 ID join 是否一致；
- 小样本和 sex-confounded 结果的 claim boundary 必须在 S12 下游保留。

#### 与总 Flow 的连接

- S04 提供 design、paired/batch、contrast 和 reference level；
- S05 提供 DESeq2/edgeR/limma 等拟合结果；
- 本 Skill 在 S06 固化结果字段、过滤、FDR、annotation、GSEA rank 与 ORA universe；
- S07 使用 shrunken effect 和稳定结果生成图；
- S08–S10 只能使用本层明确标注的输入集合；
- S12 使用本层 provenance 解释“检验了谁、筛掉了谁、为什么、支持什么 claim”。
## 3. S07：火山图、MA、热图与 DE 诊断可视化

这一层不重新做统计推断，而是把 S05/S06 已经定义好的 effect、p-value、padj、表达变换和样本注释转换为诊断图或结果图。图形不能反向修改 gene set、contrast 或显著性结论；每张图都要能追溯到输入对象、过滤规则、阈值和版本。

### 3.1 参考 Skill：03-de-visualization —— DE 专用诊断和结果图

<!-- BEGIN_ARSSC
contract_version: "0.1"
skill_id: "03-de-visualization"
display_name_zh: "DE 专用诊断与结果可视化"
kind: "reference-skill"
primary_stage: "S07"
secondary_stages: ["S03", "S05", "S06", "S13"]
source_role: "english-reference-copy"
source_paths: ["spec-mvp/skills/reference-stack/03-de-visualization/SKILL.md", "spec-mvp/skills/reference-stack-zh-CN/03-de-visualization/SKILL.md"]
registration: "not-registered"
runtime_status: "reference-only"
status_note_zh: "图形和诊断规则参考；当前项目未固化为统一 runtime renderer。与 03-volcano 有待审计重叠。"
input_contract: ["DE_result_object", "transformed_expression_matrix", "sample_metadata", "contrast", "plot_policy"]
output_contract: ["dispersion_diagnostics", "pvalue_histogram", "PCA_MDS", "sample_distance_heatmap", "MA", "volcano", "DE_heatmap", "plot_parameters"]
core_apis: ["DESeq2", "edgeR", "ggplot2", "limma", "pheatmap", "matrixStats", "UpSetR"]
preconditions: ["raw_counts_are_transformed_for_dimension_reduction", "DE_semantics_are_frozen", "annotation_is_joined", "thresholds_are_recorded"]
hard_boundary: ["plot_does_not_change_inference", "raw_counts_are_not_direct_PCA_input", "visual_cluster_is_not_biological_proof", "all_plot_inputs_are_traceable"]
END_ARSSC -->

**来源**：spec-mvp/skills/reference-stack/03-de-visualization/SKILL.md  
**在总 Flow 中的位置**：S03、S05 和 S07 的交叉层；核心交付是 dispersion、p-value histogram、PCA/MDS、sample-distance heatmap、MA、volcano、top-DE heatmap、plotCounts 和多集合 UpSet。  
**当前状态**：英文参考副本；可作为图形与诊断规则的参考，但当前项目尚未把它固化为统一 runtime renderer。

#### 作用与范围

使用 DESeq2/edgeR 内置函数和轻量 ggplot2 wrapper 生成两类图：

| 类型 | 图 | 主要问题 |
|---|---|---|
| 模型/数据诊断 | dispersion/BCV、p-value histogram、PCA/MDS、sample distance heatmap | 模型是否合理、批次是否主导、样本是否一致 |
| 结果展示 | MA、volcano、top-DE heatmap、per-gene plot、UpSet | effect、显著性、样本模式和多 contrast 集合关系 |

本 Skill 不覆盖任意定制化的通用绘图体系。更丰富的 volcano/MA 定制应接到 data-visualization/volcano-and-ma-plots；PCA/UMAP/t-SNE 定制应接到 dimensionality-reduction-plots；ComplexHeatmap 等高级热图应接到 heatmaps-clustering。当前项目只登记本目录中的相关参考内容，不把这些外部名称当作已存在的项目 Skill。

#### 输入与输出

**上游输入**：

- 已拟合的 DESeq2 dds 或 edgeR y/qlf；
- S06 的完整 DE 结果与明确的 effect、p-value、padj 列；
- VST/rlog/log-CPM 等适合可视化的表达矩阵；
- condition、batch、subject、sex 等样本注释；
- 要显示的 gene set、contrast、FDR/LFC 阈值；
- 版本、变换方式、blind 参数、图形参数和 provenance。

**下游输出**：

- dispersion plot 或 BCV plot；
- raw p-value histogram；
- VST/rlog 上的 PCA 或 edgeR/limma MDS；
- sample-distance heatmap；
- unshrunken 与 shrunken LFC 对照 MA；
- shrunken LFC volcano；
- top-DE gene pattern heatmap；
- 单基因 count plot；
- 多 contrast 的 UpSet；
- 图表数据快照、图注和参数记录。

#### 图形分类与核心函数

| 图 | DESeq2/edgeR 函数 | 读图对象 |
|---|---|---|
| Dispersion | plotDispEsts(dds)、plotBCV(y) | mean-dispersion trend 和 shrinkage |
| p-value histogram | ggplot2 | null calibration、隐藏 batch、过度校正 |
| PCA/MDS | plotPCA(vsd)、plotMDS(cpm(y, log=TRUE)) | 样本聚类、批次、outlier |
| Sample distance | dist(t(assay(vsd))) + pheatmap | 组内一致性、样本交换 |
| MA | plotMA(res)、plotMD(qlf) | mean 与 LFC、归一化和低表达噪声 |
| Volcano | ggplot2 + ggrepel、EnhancedVolcano | effect 与显著性叙事 |
| Top-DE heatmap | pheatmap(assay(vsd)[sig_genes, ]) | gene pattern；必须声明 row scaling |
| Per-gene | plotCounts(dds, gene, intgroup) | 某个基因的样本级分布 |
| 多集合比较 | UpSetR::upset | 多于三个 DE gene sets 的交集结构 |

#### 最重要的语义：shrunken LFC 不会重新计算 p-value

lfcShrink() 会把低 count、标准误大的 LFC 向 0 拉回，使 effect-size 轴更诚实；它不会自动重新计算原始 Wald p-value。因此：

- shrunken LFC volcano 的 x 轴变小，并不表示显著基因数变少；
- y 轴若使用 pvalue，必须明确它是 unshrunken Wald p-value；
- 图轴应写成 shrunken log2 fold change，并在图注中说明 y 轴统计量；
- MA 图左侧低 mean 区域被压平、右侧高 mean 区域变化较小，是正常的 shrinkage 视觉特征；
- 图形展示的 effect 可以收缩，但 S06 的原始检验字段必须保留。

不能根据点云看起来更集中，就声称显著性被降低或模型重新检验过。

#### 场景决策表

| 场景 | 参考做法 | 原因 |
|---|---|---|
| 用 PCA 做无偏 QC | vst(dds, blind = TRUE) | 忽略 design，询问样本是否独立于设计而一致 |
| 已确定模型、做结果图 | vst(dds, blind = FALSE) | 使用已拟合 dispersion，允许 design 影响 |
| n 小于 30 且 library size 差异超过约 4 倍 | rlog(dds, blind = FALSE) | 小样本和强 library 差异时可作为较稳健的可视化变换 |
| n 大于 30 | vst() | rlog 成本较高 |
| sample-distance QC | vst(dds, blind = TRUE) | 检查不依赖设计的样本一致性 |
| 热图强调 gene pattern | scale = 'row' | 每个 gene 做 z-score |
| 热图强调绝对表达水平 | scale = 'none' | 避免弱表达基因被 row scaling 放大 |
| top variable genes | matrixStats::rowMads() | MAD 对单个 outlier 更稳健 |
| n=3 的 top genes | 标记为探索性 | 参考小样本 replication 风险 |
| 多于三个 DE sets | UpSet | Venn 在多集合时难以阅读 |

#### 先看 dispersion/BCV

~~~r
plotDispEsts(dds)
plotBCV(y)
~~~

| 图形模式 | 可能含义 | 处理 |
|---|---|---|
| gene-wise cloud 沿 trend 分布，final shrunken estimates 被拉向 trend | 拟合大体健康 | 继续检查 |
| fitted trend 与 gene-wise cloud 明显不匹配 | parametric trend 失败 | 比较 fitType = 'local' 或 fitType = 'mean' |
| 大量 gene-wise dispersion 远高于 trend | outlier 或隐藏 batch | 深入检查，不能只信 QL F-test |
| final estimates 全面低于 gene-wise | 可能过度 shrinkage、样本太小或 trend 过平 | 检查 useEM 和稳健超参数 |
| edgeR BCV 随 mean 单调下降 | 常见的合理趋势 | 结合设计和 outlier 继续审计 |

#### p-value histogram

~~~r
library(ggplot2)

ggplot(res_df, aes(x = pvalue)) +
  geom_histogram(bins = 50, fill = 'steelblue', color = 'white') +
  labs(x = 'P-value', y = 'Frequency', title = 'P-value distribution') +
  theme_bw()
~~~

零假设下近似均匀、0 附近有 signal 峰时较为合理；U 形可能提示隐藏 batch 或未建模 covariate；0 附近缺失且 1 附近高可能提示过度建模或错误 dispersion；p=1 尖峰常与极低 count 离散伪影有关。它是低成本 sanity check，应在相信 gene list 前执行，但本轮只保留为文档规则，不执行分析。

#### MA plot

~~~r
plotMA(res, ylim = c(-5, 5), main = 'MA plot (unshrunken)')

res_apeglm <- lfcShrink(
  dds,
  coef = 'condition_treated_vs_control',
  type = 'apeglm'
)
plotMA(res_apeglm, ylim = c(-5, 5), main = 'MA plot (apeglm-shrunken)')

plotMD(qlf, main = 'edgeR MD plot')
abline(h = c(-1, 1), col = 'blue', lty = 2)
~~~

| 模式 | 解释方向 |
|---|---|
| LFC=0 附近对称 cloud | 归一化大体合理 |
| cloud 中位数明显偏离 0 | TMM/RLE 等归一化假设可能失败 |
| 低 mean 处 funnel 变宽 | 低 count 噪声变大，通常预期 |
| 上下不对称 | 可能是真实大扰动，也可能是 normalization failure |
| 低 mean 水平离散条带 | 低 count artifact，检查预过滤 |

默认 ylim 可能把信号压扁，必须有意设置。apeglm 后左侧极端点收紧是预期效果。

#### PCA、MDS 和样本距离

不能直接对 raw counts 做 PCA：library size 会主导第一主成分；简单 log(count+1) 也未必稳定。先做 VST/rlog 或合理的 log-CPM：

~~~r
vsd <- vst(dds, blind = FALSE)
plotPCA(vsd, intgroup = c('condition', 'batch'))

pca_df <- plotPCA(
  vsd,
  intgroup = c('condition', 'batch'),
  returnData = TRUE
)
percentVar <- round(100 * attr(pca_df, 'percentVar'))

library(ggplot2)
ggplot(pca_df, aes(PC1, PC2, color = condition, shape = batch)) +
  geom_point(size = 4) +
  xlab(paste0('PC1: ', percentVar[1], '% variance')) +
  ylab(paste0('PC2: ', percentVar[2], '% variance')) +
  theme_bw()

library(limma)
plotMDS(cpm(y, log = TRUE), col = as.numeric(group), pch = 16)
~~~

blind = TRUE 适合无偏 QC；blind = FALSE 适合模型已固定后的结果展示。若 batch 分离强于 condition，应在 S04 把 batch 纳入 design；不要先用 removeBatchEffect() 改 count 再做 DE。可视化用途可以单独使用 removeBatchEffect()，但必须在图注中说明。

PCA 模式的解释：

| 模式 | 解释或动作 |
|---|---|
| PC1/PC2 按 condition 分离 | 可能存在强生物学 signal |
| 按 batch 而非 condition 分离 | batch 主导；回到 S04 加 covariate |
| 单个样本远离同组 | outlier、sample swap 或性别/污染问题；回到 QC |
| condition 出现在 PC3 以后 | effect 较弱但仍可能有 DE；结合 dispersion 和设计 |
| 两簇都无法由 metadata 解释 | 调查处理日期、lane、machine 等隐藏 covariate |

样本距离热图：

~~~r
library(pheatmap)

vsd <- vst(dds, blind = TRUE)
sd <- dist(t(assay(vsd)))
mat <- as.matrix(sd)
ann <- data.frame(
  condition = colData(dds)$condition,
  row.names = colnames(dds)
)

pheatmap(
  mat,
  annotation_col = ann,
  annotation_row = ann,
  clustering_distance_rows = sd,
  clustering_distance_cols = sd,
  color = colorRampPalette(c('white', 'steelblue'))(100),
  main = 'Sample distance (vst blind)'
)
~~~

对角线、组内距离和异常远样本都必须能被解释。row/column annotation 不完整或 sample name 不一致时，先回到 S01/S02。

#### Top-DE heatmap 与 row scaling trap

~~~r
library(pheatmap)

sig <- rownames(subset(res, padj < 0.01))[1:50]
vsd <- vst(dds, blind = FALSE)
mat <- assay(vsd)[sig, ]
mat_scaled <- t(scale(t(mat)))

ann_col <- data.frame(
  condition = colData(dds)$condition,
  batch = colData(dds)$batch,
  row.names = colnames(mat)
)

pheatmap(
  mat_scaled,
  annotation_col = ann_col,
  show_rownames = FALSE,
  clustering_distance_rows = 'correlation',
  clustering_distance_cols = 'correlation',
  color = colorRampPalette(c('blue', 'white', 'red'))(100),
  main = 'Top 50 DE genes (z-scored per gene)'
)
~~~

row scaling 适合回答“这些 gene 的变化模式是否相似”，但会销毁绝对表达量信息：均值约 6 的基因和跨样本范围 10–1000 的基因可能显示出相似色阶。QC heatmap 要观察全局 sample shift 时，使用 assay(vsd) 和 scale = 'none'；结果 heatmap 在 QC 已通过后才使用 scale = 'row'。

top-variable 选择可用 MAD：

~~~r
library(matrixStats)
vars_mad <- rowMads(assay(vsd))
top500 <- order(vars_mad, decreasing = TRUE)[1:500]
~~~

rowMads 比 rowVars 更不容易被单个异常样本支配。

#### Per-gene plot 与 UpSet

~~~r
plotCounts(dds, gene = 'GENE_NAME', intgroup = 'condition')

d <- plotCounts(
  dds,
  gene = 'GENE_NAME',
  intgroup = c('condition', 'batch'),
  returnData = TRUE
)

library(ggplot2)
ggplot(d, aes(x = condition, y = count, color = batch)) +
  geom_jitter(width = 0.1, size = 3) +
  scale_y_log10() +
  ggtitle('GENE_NAME') +
  theme_bw()
~~~

n=3 时不要依赖 boxplot 传达稳定分布；优先显示每个点。gene ID 必须和 rownames(dds) 一致，symbol 与 Ensembl 混用会导致 gene not found。

多于三个 DE sets 时用 UpSet，而不是继续增加 Venn 复杂度：

~~~r
library(UpSetR)
upset(fromList(list(
  drugA = sig_drugA,
  drugB = sig_drugB,
  drugC = sig_drugC
)))
~~~

#### 03-de-visualization 的典型失败模式

| 现象 | 机制 | 回退 |
|---|---|---|
| volcano 极端点全是 baseMean 小于 5 的 gene | 未收缩 LFC 被低 count 噪声放大 | 用 lfcShrink(type = 'apeglm') |
| ggrepel 只显示约 10 个标签 | max.overlaps 默认值静默丢弃标签 | 设置 max.overlaps = Inf |
| PCA 按 batch 分离 | batch variance 超过 condition variance | design = ~ batch + condition；不要用校正 count 做 DE |
| QC heatmap 看不出 sample shift | scale = 'row' 消去了 sample-level additive shift | QC 用 scale = 'none' |
| top variable gene 被单个样本支配 | rowVars 对极端值敏感 | 使用 rowMads |
| plotPCA 只有 PC1/PC2 | DESeq2 helper 只画前两轴 | 用 prcomp(t(assay(vsd))) 自定义轴 |
| PCA cloud 几乎塌成一点 | raw count 或错误变换 | 先做 vst/rlog |
| 所有 MA 点变红 | alpha 或 significant flag 错误 | 核对 alpha、padj 与 pvalue |
| pheatmap 有 Inf/NA | 缩放时存在零方差行 | 去除零方差行并保留记录 |
| vst 在过滤后基因很少时报错 | 默认 nsub=1000 超过可用基因数 | 调小 nsub，例如 nsub=500 |
| PDF 被 Illustrator 拖垮 | 大量点使用 vector scatter | 点层使用 rasterized = TRUE |

#### 不可替代的边界

- 图不是新的 hypothesis test；图形中的颜色不能改写统计字段；
- raw counts 不能直接作为 PCA 的输入；
- shrunken LFC、unshrunken p-value、padj 轴三者必须显式标注；
- heatmap 的 scale = 'row' 与 scale = 'none' 不是审美选择，而是不同科学问题；
- removeBatchEffect() 可以服务于展示，但不能将校正后的表达值偷偷送回正式 DE；
- 小样本图应展示点和不确定性，不能用箱线图制造重复数幻觉；
- 任何图都要保留 contrast、输入结果快照、阈值、变换、annotation 和 package versions。

### 3.2 参考 Skill：03-volcano —— shrunken LFC 火山图、MA 图与标签策略

<!-- BEGIN_ARSSC
contract_version: "0.1"
skill_id: "03-volcano"
display_name_zh: "shrunken LFC 火山图、MA 图与标签策略"
kind: "reference-skill"
primary_stage: "S07"
secondary_stages: ["S05", "S06", "S13"]
source_role: "english-reference-copy"
source_paths: ["spec-mvp/skills/reference-stack/03-volcano/SKILL.md", "spec-mvp/skills/reference-stack-zh-CN/03-volcano/SKILL.md"]
registration: "not-registered"
runtime_status: "reference-only"
status_note_zh: "包含 R/Python 绘图示例和 gotchas；当前未成为统一运行时，且与 03-de-visualization 存在重叠。"
input_contract: ["DE_result", "shrunken_or_raw_LFC", "pvalue_or_padj", "baseMean", "significance_thresholds", "label_policy"]
output_contract: ["volcano_plot", "MA_plot", "label_record", "plot_audit_parameters"]
core_apis: ["DESeq2::lfcShrink", "ggplot2", "ggrepel", "EnhancedVolcano", "matplotlib"]
preconditions: ["LFC_semantics_are_declared", "y_axis_statistic_matches_threshold", "NA_Inf_pzero_are_handled", "label_policy_is_explicit"]
hard_boundary: ["shrunken_LFC_does_not_recompute_pvalue", "raw_p_and_padj_are_not_interchangeable", "plot_is_not_gene_selection_engine", "no_untracked_label_filtering"]
END_ARSSC -->

**来源**：spec-mvp/skills/reference-stack/03-volcano/SKILL.md  
**在总 Flow 中的位置**：S07；与 03-de-visualization 有重叠，先并列保留，下一阶段才审计是否合并为一个 visualization adapter。  
**当前状态**：英文参考副本；包含 ggplot2/ggrepel、EnhancedVolcano、DESeq2/edgeR、Python 绘图示例和大量 gotchas，但当前项目没有把这些示例变成统一运行时。

#### 作用和基本输入

输入是已完成 S05/S06 的 DE result，至少需要 gene、shrunken 或待收缩的 LFC、raw p-value 或 padj、baseMean、significance thresholds 和待标注 gene list。输出是：

- effect-size 与显著性关系图；
- MA 图及其诊断；
- 显著性分类和标签表；
- 图注所需的 shrinkage、p-value 轴、阈值和版本 provenance。

该 Skill 反复强调：不要用未收缩 MLE LFC 作为 volcano/MA 的主要 x 轴。2 vs 0 reads 可能产生 Inf，4 vs 1 可能给出极端 LFC，但标准误很大；低 count 极端值不能自动等于真实强 effect。

#### LFC shrinkage 方法选择

| 方法 | prior/思想 | 适用 | 重要限制 |
|---|---|---|---|
| apeglm | Cauchy heavy-tailed prior | DESeq2 默认；保留大而可靠的 effect，压低低 count 噪声 | 需要 coef；不支持 contrast 的部分调用形态 |
| ashr | mixture of normals | 需要 contrast 或希望使用 s-value | 对中等 effect 可能更激进 |
| normal | zero-centered normal | legacy reproducibility | 可能过度 shrink 大 effect，现代 vignette 不再首选 |
| unshrunken MLE | 无 prior | 不应作为 volcano/MA 主估计 | 低 count 主导尾部 |

~~~r
library(DESeq2)

dds <- DESeq(dds)

res_apeglm <- lfcShrink(
  dds,
  coef = 'condition_treated_vs_control',
  type = 'apeglm'
)

res_ashr <- lfcShrink(
  dds,
  contrast = c('condition', 'treated', 'control'),
  type = 'ashr'
)
~~~

ashr 可提供与 local false sign rate 相关的 svalue；padj 回答效应是否非零，svalue 更接近方向是否可靠，不可互换。

edgeR 已有 moderated p-values，但不会自动 shrink LFC；需要对有意义的非零效应使用 glmTreat()，并在 claim 中区分显著非零和超过效应阈值。

#### 场景决策

| 场景 | 参考方法 |
|---|---|
| bulk RNA-seq + DESeq2 | lfcShrink(type = 'apeglm')，x 轴用 shrunken LFC |
| 非默认 contrast | lfcShrink(type = 'ashr')，若接口需要 contrast |
| single-cell pseudobulk | shrunken LFC；大于约 20k gene 时考虑 raster |
| proteomics/limma/MSstats | 使用已有 moderated logFC 与 adj.P.Val |
| microarray/limma | topTable() 的 adj.P.Val 与 logFC |
| ATAC/ChIP differential peaks | 对 DESeq2/DiffBind feature 使用相同 shrinkage 逻辑 |
| 想按方向可信度排序 | ashr svalue，而不是 padj |
| 多于 6 个 comparison | 使用共享 y 轴的 faceted MA，比多个 volcano 更可读 |

#### ggplot2 + ggrepel 实现模板

下列模板保留源 Skill 的主要逻辑：先生成显著性分类，再预选标签，最后使用 combined rank；不能把所有标签交给默认布局而不检查丢失。

~~~r
library(ggplot2)
library(ggrepel)
library(dplyr)

volcano_plot <- function(
  res,
  fdr = 0.05,
  lfc_threshold = 1,
  label_genes = NULL,
  top_n = 10
) {
  res <- as.data.frame(res) |>
    tibble::rownames_to_column('gene') |>
    mutate(
      significance = case_when(
        is.na(padj) ~ 'NS',
        padj < fdr & log2FoldChange > lfc_threshold ~ 'Up',
        padj < fdr & log2FoldChange < -lfc_threshold ~ 'Down',
        TRUE ~ 'NS'
      ),
      neg_log10_p = -log10(pvalue)
    )

  if (is.null(label_genes)) {
    label_genes <- res |>
      filter(significance != 'NS') |>
      mutate(rank_score = -log10(pvalue) * abs(log2FoldChange)) |>
      arrange(desc(rank_score)) |>
      head(top_n) |>
      pull(gene)
  }

  res$label <- ifelse(res$gene %in% label_genes, res$gene, '')

  okabe_ito <- c(
    Up = '#D55E00',
    Down = '#0072B2',
    NS = '#999999'
  )

  ggplot(res, aes(log2FoldChange, neg_log10_p, color = significance)) +
    geom_point(alpha = 0.6, size = 1.3) +
    scale_color_manual(values = okabe_ito, name = NULL) +
    geom_vline(
      xintercept = c(-lfc_threshold, lfc_threshold),
      linetype = 'dashed',
      color = 'grey40',
      linewidth = 0.3
    ) +
    geom_hline(
      yintercept = -log10(fdr),
      linetype = 'dashed',
      color = 'grey40',
      linewidth = 0.3
    ) +
    geom_text_repel(
      aes(label = label),
      color = 'black',
      size = 3,
      max.overlaps = Inf,
      box.padding = 0.4,
      segment.size = 0.2,
      min.segment.length = 0
    ) +
    labs(
      x = expression(log[2]~'fold change (shrunken)'),
      y = expression(-log[10]~italic(p))
    ) +
    theme_classic(base_size = 10) +
    theme(panel.grid = element_blank())
}
~~~

设计含义：

- Okabe–Ito palette 适合色觉缺陷友好展示；
- max.overlaps = Inf 保证预选标签尽量不被默认值静默丢掉；
- -log10(fdr) 的水平线只有在 y 轴也是对应 adjusted quantity 时才有直接 FDR 语义；
- combined rank = -log10(pvalue) * abs(log2FoldChange) 同时考虑统计证据和 effect，而不是只按最小 p-value 选择 housekeeping gene；
- 需处理 pvalue=0、NA、Inf，不能让图形函数返回不可解释的坐标。

#### EnhancedVolcano 模板与三个 gotcha

~~~r
library(EnhancedVolcano)

EnhancedVolcano(
  res,
  lab = rownames(res),
  x = 'log2FoldChange',
  y = 'padj',
  pCutoff = 0.05,
  FCcutoff = 1,
  selectLab = c('TP53', 'MYC', 'BRCA1'),
  drawConnectors = TRUE,
  widthConnectors = 0.3,
  maxoverlapsConnectors = Inf,
  colAlpha = 0.6,
  pointSize = 1.5,
  labSize = 3,
  legendPosition = 'right'
)
~~~

1. selectLab 仍可能受 pCutoff 和 FCcutoff 过滤。用户点名的 gene 不通过阈值时可能不显示且没有显著警告；若必须强制标注，应使用手工 ggrepel layer。
2. y = pvalue 与 y = padj 的水平线语义不同。raw p 的水平线不是全局 FDR 阈值；若 y 轴是 padj，0.05 线才直接代表 adjusted threshold。
3. x 轴最好围绕 0 对称；不对称 x-limits 会误导方向比较。可使用 xlim = c(-X, X)，X 为最大绝对 LFC 或预先设定的可读范围。

源 Skill 还提示 EnhancedVolcano 的旧版本参数可能使用 maxoverlapsConnectors，而新版本支持 max.overlaps；版本兼容必须先查 help，不可照抄参数。

#### MA plot 与 Python 版本

MA 是 abundance-dependent variance 的诊断，能暴露 volcano 不容易显示的问题：

- 低 baseMean 聚集极端 LFC，提示 shrinkage 不足；
- 某一 LFC 的显著基因水平条带，可能提示 batch 与 treatment 混杂；
- 低 count 端上/下不对称，可能提示 library-size normalization failure；
- 大量点时使用 rasterized = TRUE，避免向量 PDF 过大。

~~~r
library(DESeq2)
plotMA(res_apeglm, alpha = 0.05, ylim = c(-5, 5))
~~~

~~~python
import matplotlib.pyplot as plt
import numpy as np

def ma_plot(res, fdr=0.05, ax=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 5))
    sig = (res['padj'] < fdr) & res['padj'].notna()
    ax.scatter(
        np.log10(res.loc[~sig, 'baseMean']),
        res.loc[~sig, 'log2FoldChange'],
        c='#999999', s=4, alpha=0.4, rasterized=True
    )
    ax.scatter(
        np.log10(res.loc[sig, 'baseMean']),
        res.loc[sig, 'log2FoldChange'],
        c='#D55E00', s=6, alpha=0.7, rasterized=True
    )
    ax.axhline(0, color='black', linewidth=0.5)
    ax.set_xlabel('log10 mean normalized count')
    ax.set_ylabel('log2 fold change (shrunken)')
    return ax
~~~

#### 03-volcano 典型失败模式和审计规则

| 现象 | 机制 | 回退 |
|---|---|---|
| top hits 全是低 count 极端 LFC | 未收缩 MLE | apeglm 或 ashr；把 unshrunken 放到补充表 |
| raw p 阈值线画在 padj 轴上 | 轴和线代表不同量 | 明确 y 轴并匹配 threshold；raw p 轴不能画固定全局 FDR 线 |
| top-N-by-p 选出 GAPDH、ACTB 等低 effect gene | p-value 与 effect 被混为一谈 | combined rank 或预先指定 gene list |
| ggrepel 只显示部分 label | max.overlaps 默认 10 | max.overlaps = Inf，且检查渲染日志 |
| 极小 p-value 把 y 轴拉到 200 | -log10 尾部压缩其他点 | coord_cartesian(ylim = c(0, 50))、sqrt transform 或断轴 |
| modern DESeq2 仍使用 normal shrinkage | 遵循旧教程 | 使用 apeglm 或 ashr，并记录版本 |
| EnhancedVolcano selectLab 缺少点名 gene | selectLab 被阈值二次过滤 | 手工 annotation layer |
| apeglm 与 ashr top hit 不一致 | prior 形状不同 | 两者都可合法；选择一个并记录依据 |
| EnhancedVolcano 比 ggplot 少点 | padj=NA 被丢弃 | 统计 NA 数；必要时将 NA padj 设为 1 仅用于绘图并注明 |
| MA 出现低 count 整数条带 | pseudocount quantization | 回查 normalization 和低 count 过滤 |
| volcano 很多显著但 MA 都在低 baseMean | 未收缩 LFC | 以 shrunken LFC 重画，结合 MA 诊断 |

操作顺序固定为：

1. x 轴是否为 shrunken LFC；
2. y 轴是 raw p 还是 padj；
3. 阈值线是否与 y 轴同一统计量；
4. label 是否按 combined rank 或预先指定；
5. 是否处理 NA、Inf、p=0 和对称坐标。

#### 保留的参考阈值

| 项目 | 参考值 | 说明 |
|---|---:|---|
| 生物学 effect convention | abs(log2FC) > 1 | 约 2-fold；细微效应可考虑 0.58，但需预先说明 |
| 默认 FDR | padj < 0.05 | BH 口径 |
| unbiased screen | padj < 0.01 | 更保守 |
| exploratory follow-up | padj < 0.10 或 0.20 | 可用于假设生成，不宜写成稳定 hits |
| s-value | 约小于 0.005 的提示 | 需依具体分析和文献解释 |
| raster threshold | 大于约 5000 points | 大散点图保持轴为 vector、点为 raster |
| ggrepel | max.overlaps = Inf | 避免默认 10 丢标签 |
| volcano y cap | -log10(p) 大于约 50 | 防止视觉压缩；保留数据而非静默删除 |

#### 不可替代的边界

- 显著与大效应必须区分；后验组合筛选不能冒充 TREAT/lfcThreshold；
- shrunken LFC 是展示/排序的更稳健 effect，不代表 p-value 被重算；
- 图中标签是展示选择，不能把未标注 gene 写成未发现；
- NA、Inf 和 p=0 的处理必须进入图形 provenance；
- 颜色分类是阈值分类，不应使用容易暗示连续显著性的渐变代替；
- 图轴、阈值、label selection 和数据版本必须能回溯到 S06。

#### 与 03-de-visualization 的重叠待审计项

这两个参考 Skill 都覆盖 shrunken LFC、volcano、MA、ggrepel、阈值、失败模式和审稿人关注点。当前先完整并列保留，不擅自删除。下一阶段要逐段比较：

- 是否保留 03-de-visualization 的诊断图全套；
- 是否把 03-volcano 的 volcano 专项模板作为同一 Skill 的子章节；
- pvalue 轴与 padj 轴规则是否统一；
- EnhancedVolcano 与手写 ggplot2 的 runtime 选择是否由项目适配器决定；
- 03-volcano 中与 S06 重复的 FDR/LFC 语义是否只保留一个权威定义。

## 4. S08–S09：GO/KEGG 方法分叉、ID mapping 与 tested-gene universe

本层是从 DE 结果进入功能解释的分叉点。顺序不能倒置：

1. 先判断输入是全量、有方向的 gene ranking，还是预先筛选的 gene list；
2. 再选择 GSEA 或 ORA；
3. 再按目标数据库要求转换 ID；
4. 对 ORA 明确定义 tested-gene universe；
5. 记录数据库、版本/日期、排序统计量、p-adjust 方法和 seed；
6. 结果先做 redundancy collapse，再进入 S10 拓扑或 S11 跨分支整合。

### 4.1 项目适配器：pathway-enrichment

<!-- BEGIN_ARSSC
contract_version: "0.1"
skill_id: "pathway-enrichment"
display_name_zh: "项目 pathway enrichment 路由适配器"
kind: "project-adapter"
primary_stage: "S08"
secondary_stages: ["S09", "S10", "S12"]
source_role: "project-adapter"
source_paths: ["spec-mvp/skills/pathway-enrichment/SKILL.md", ".agents/skills/pathway-enrichment/SKILL.md"]
registration: "registered"
runtime_status: "not-verified"
status_note_zh: "项目路由和边界已登记；底层数据库、网络接口和报告脚本是否可运行仍待核对。"
input_contract: ["DE_or_module_result", "foreground_or_ranked_vector", "tested_gene_universe", "organism", "ID_namespace", "method_decision"]
output_contract: ["GO_result", "KEGG_result", "mapping_table", "enrichment_provenance", "method_route_record"]
core_apis: ["Rscript", "clusterProfiler::bitr", "clusterProfiler::bitr_kegg", "OrgDb", "GO.db"]
preconditions: ["upstream_result_is_executed", "ORA_or_GSEA_is_decided", "ID_namespace_is_declared", "ORA_universe_exists", "database_version_or_date_is_recorded"]
hard_boundary: ["not_method_selection_by_default", "not_whole_genome_universe_by_default", "KEGG_network_is_explicit_exception", "no_silent_external_database_claim"]
END_ARSSC -->

**来源**：spec-mvp/skills/pathway-enrichment/SKILL.md  
**宿主发现副本**：.agents/skills/pathway-enrichment/SKILL.md  
**在总 Flow 中的位置**：S08 的项目入口；负责把 gene list 交给 pathway enrichment 路由。  
**当前状态**：项目适配器；存在 Skill 说明和项目边界，但不能仅凭 SKILL.md 断言所有底层数据库、网络接口和报告脚本都已在本项目可运行。

#### 作用

将 gene list 交给 pathway-enrichment 能力，覆盖 GO、KEGG、Reactome、WikiPathways 等功能富集入口。该适配器的核心价值是项目级路由、输入/输出约束和结果解释边界，不应替代 S08 的 ORA/GSEA 方法判断，也不应把外部参考数据库默认当作本地快照。

#### 上游输入

- gene list 或 DE 结果导出的 gene set；
- 物种和 gene ID 类型；
- 若走 ORA：显著 list 与 tested-gene universe；
- 若走 GSEA：全量 named decreasing ranking；
- enrichment method、数据库、阈值和 reproducibility metadata；
- 上游 contrast、过滤规则、padj/LFC 口径和 provenance。

#### 下游输出

- pathway/GO term 结果表；
- 富集方法、数据库、ID mapping 统计；
- ORA 的 universe 或 GSEA 的 ranking 说明；
- 可供可视化和 S11 整合的 term/gene/pathway 关系；
- 失败原因、空结果警告和运行 provenance。

#### 核心包、函数和前置条件

项目 catalog 指定的主要执行形态是 Rscript，核心依赖为 clusterProfiler 与适用的 OrgDb/GO.db；KEGG 网络或 snapshot 是显式例外。对应的参考函数包括：

~~~text
clusterProfiler::bitr / bitr_kegg
  → enrichGO / gseGO
  → enrichKEGG / gseKEGG
  → simplify / pairwise_termsim / setReadable
Rscript + pinned package/database versions
~~~

前置条件是：上游结果已经执行；物种、ID namespace 和方向约定明确；ORA 有 tested-gene universe；GSEA 有全量 named decreasing ranking；foreground 与 universe 通过同一 mapping path 转换；GO ontology、KEGG organism/keyType、阈值和数据库版本/日期已经写入输入记录。

#### 不可替代的边界

- 不能把“有 pathway 富集”写成疾病诊断或因果证明；
- 不能用全基因组代替本次实际 tested-gene universe；
- 不能把预选 gene list 的 ORA 结果写成全量 ranking 的 GSEA；
- 不能让 pathway 适配器默默改变 DE 结果、contrast 或 gene ID；
- live database 的结果必须带查询日期或版本，不能伪装成本地可复现快照。

#### 当前状态和待确认点

这是项目适配器，不是英文 reference-stack 的逐字副本。其底层执行依赖、数据库选择、空结果处理、ID mapping 率阈值以及是否接入本项目统一报告格式，需要在后续 runtime 审计中确认。本轮只把它放入总 Flow，不执行富集。

### 4.2 参考 Skill：04-pathway-enricher —— Enrichr 多数据库 gene-set enrichment

<!-- BEGIN_ARSSC
contract_version: "0.1"
skill_id: "04-pathway-enricher"
display_name_zh: "Enrichr 多数据库 gene-set enrichment 参考"
kind: "reference-skill"
primary_stage: "S08"
secondary_stages: ["S09", "S12"]
source_role: "english-reference-copy"
source_paths: ["spec-mvp/skills/reference-stack/04-pathway-enricher/SKILL.md", "spec-mvp/skills/reference-stack-zh-CN/04-pathway-enricher/SKILL.md"]
registration: "not-registered"
runtime_status: "reference-only"
status_note_zh: "源 Skill 是 Python/REST/API 工作流参考；当前项目未将其升级为本地 runtime，且网络边界存在审计问题。"
input_contract: ["gene_list", "species", "ID_namespace", "source_DE_filter", "tested_universe_if_available"]
output_contract: ["Enrichr_tables", "enrichment_figures", "report_md", "query_metadata", "mapping_loss_record"]
core_apis: ["Python HTTP client", "Enrichr REST API", "hardcoded library set"]
preconditions: ["gene_list_is_deduplicated", "species_and_symbol_system_are_declared", "network_permission_is_explicit", "query_time_is_recorded"]
hard_boundary: ["Enrichr_library_is_not_tested_universe", "not_local_if_gene_symbols_are_POSTed", "does_not_support_unregistered_custom_database", "agent_does_not_replace_script_execution"]
END_ARSSC -->

**来源**：spec-mvp/skills/reference-stack/04-pathway-enricher/SKILL.md  
**在总 Flow 中的位置**：S08/S09 的外部 API 参考分支；接收 gene list，查询 Enrichr 六类库，生成排序表、图和 Markdown 报告。  
**当前状态**：英文参考副本；源文档描述 Python/REST/API 和报告结构，当前项目未把它自动升级为本地 runtime。

#### 作用

Pathway Enricher 是一个面向 gene-set enrichment 的专用 agent/脚本设想，输入来自 GWAS、DE 或其他 omics 的 gene list，调用 Enrichr REST API，返回 pathway/ontology 富集，并生成 bubble chart、bar chart、表格和 Markdown report。

它明确不负责 differential expression 或 variant calling。它解决的是“给定一个 list，在哪些预定义 gene set 中过度代表”，不是“从全量 DE ranking 中寻找协调变化”。

#### 触发和不触发

适合：

- 用户给出 gene list 并要求 pathway、ontology 或 biological process；
- 用户要求特定 gene set 的 bubble chart 或 enrichment plot；
- gene list 来自 GWAS hits、DE hits 或其他 omics。

不适合：

- variant analysis；
- 单基因文献检索；
- 需要严格控制 RNA-seq tested universe 的正式 ORA，除非能把背景限制、ID 和数据库版本补齐；
- 有全量 ranking 却被随意截成 list 的 GSEA 场景。

#### 输入格式

- txt/csv gene list；
- 每行一个 HGNC symbol 或逗号分隔；
- 允许以 # 开头的注释行；
- demo mode 中有一个内置的 25-gene 示例列表。

输入处理要求：去空白、去重、格式检查、物种和 symbol 体系核对。若输入来自 S06，必须额外保留 DE table、显著性筛选条件和 tested universe，不能只把 symbol 列复制出来。

#### 查询的数据库

源文档登记了六个库：

| 类型 | Enrichr library name | 源 Skill 描述 |
|---|---|---|
| KEGG | KEGG_2021_Human | 人类 KEGG |
| GO BP | GO_Biological_Process_2023 | biological process |
| GO MF | GO_Molecular_Function_2023 | molecular function |
| GO CC | GO_Cellular_Component_2023 | cellular component |
| Reactome | Reactome_2022 | reaction/pathway |
| WikiPathways | WikiPathways_2023_Human | community-curated pathways |

这些名称和年份是参考记录，不应在运行时未经确认就声称是当前数据库版本。

#### 原始工作流

1. 解析 gene symbols，去空白、去重、验证；
2. POST 到 Enrichr addList；
3. 对六个 library 逐一 GET enrichment 结果；
4. 提取 term、p-value、adjusted p-value、z-score、combined score 和 overlap genes；
5. 保留 adjusted p-value 小于 0.05 的 term；若没有通过项，可以保留全部但必须加 warning；
6. 生成 bubble chart 和每库 bar chart；
7. 输出带图和排序表的 report.md。

Enrichr 的 combined score 是其内部的 log-p 与 z-score 组合，不能直接与 clusterProfiler 的 NES、GeneRatio 或 enrichment score 互换。

#### 输出结构

源 Skill 规划的输出包括：

~~~text
output_directory/
├── report.md
├── result.json
├── tables/
│   ├── kegg_enrichment.csv
│   ├── go_bp_enrichment.csv
│   ├── go_mf_enrichment.csv
│   ├── go_cc_enrichment.csv
│   ├── reactome_enrichment.csv
│   └── wikipathways_enrichment.csv
├── figures/
│   ├── bubble_chart_kegg.png
│   ├── bubble_chart_go_bp.png
│   ├── bar_chart_summary.png
│   └── heatmap_top_pathways.png
└── reproducibility/
    ├── commands.sh
    ├── environment.yml
    └── checksums.sha256
~~~

典型 report 至少应能回答：输入基因数、实际映射/丢失数、数据库名称与版本、top terms、调整后 p-value、combined score、overlap genes、图形参数和查询时间。

#### 依赖和网络边界

源文档列出 Python 3.10+、requests >= 2.28；matplotlib、numpy、pandas 用于图和表处理。API 查询遵守约 0.5 秒的 rate limit，失败时产生 warning 而不是直接崩溃。

必须明确一个重要的审计问题：源文档一方面写“all locally, with no data leaving the machine”，另一方面又把 gene symbols POST 到公开的 Enrichr REST API。即使只发送 gene symbols、不发送患者 ID 或 genotype，数据仍然离开本机。当前先记录为待确认/审计问题，不擅自修复上游文字。

#### 不可替代的边界

- 富集是 over-representation 的统计结果，不是疾病诊断、机制证明或因果证据；
- Enrichr 的 library 不是本次 DE 的 tested universe；
- 建议将数千 gene 的输入先审查，源 Skill 提议约 500–1000 个 top significant genes，但这只是输入规模建议，不替代生物学和统计理由；
- 只支持源 Skill 明确登记的六个 hardcoded library，不能暗中查询未审计 custom database；
- API 空结果、rate limit、数据库更新和网络失败必须进入 provenance；
- agent 可以解释高层方向，脚本才负责 HTTP、统计字段、表和图生成；两者职责不能混淆。

### 4.3 参考 Skill：04-pathway-workflow —— expression-to-pathways 编排

<!-- BEGIN_ARSSC
contract_version: "0.1"
skill_id: "04-pathway-workflow"
display_name_zh: "expression-to-pathways 富集编排"
kind: "reference-skill"
primary_stage: "S08"
secondary_stages: ["S09", "S10", "S11", "S12"]
source_role: "english-reference-copy"
source_paths: ["spec-mvp/skills/reference-stack/04-pathway-workflow/SKILL.md", "spec-mvp/skills/reference-stack-zh-CN/04-pathway-workflow/SKILL.md"]
registration: "not-registered"
runtime_status: "reference-only"
status_note_zh: "主编排参考；依赖的 per-method skills 未全部登记，不能视为完整可运行 workflow。"
input_contract: ["DE_result", "significant_gene_list", "full_ranked_vector", "tested_gene_universe", "ID_mapping", "database_selection"]
output_contract: ["ORA_route", "GSEA_route", "collapsed_terms", "pathway_figures", "method_and_database_provenance"]
core_apis: ["clusterProfiler", "org.Hs.eg.db", "ReactomePA", "enrichplot"]
preconditions: ["ORA_or_GSEA_decision_is_recorded", "foreground_and_universe_share_mapping_path", "GSEA_rank_is_full_named_sorted", "database_version_is_fixed_or_dated"]
hard_boundary: ["ORA_requires_universe", "GSEA_is_not_truncated_gene_list", "method_route_is_not_post_hoc_choice", "unregistered_per_method_skill_is_not_runtime"]
END_ARSSC -->

**来源**：spec-mvp/skills/reference-stack/04-pathway-workflow/SKILL.md  
**在总 Flow 中的位置**：S08–S09 的主编排器；承接 S06 的 DE result，路由到 GO、KEGG、Reactome、WikiPathways 的 ORA/GSEA，并向 S10/S11 输出去冗余结果。  
**当前状态**：英文参考 workflow；依赖多个未在本目录中逐一展开的 per-method skills，不能直接视为可运行的完整 workflow。

#### 作用

把“DE 结果到 pathway”拆成明确阶段：

- 由输入形态决定 ORA 还是 GSEA；
- 按方法转换 gene ID；
- 对 ORA 使用可辩护的 background universe；
- 区分 local annotation 与 live database；
- 对结果做 redundancy collapse；
- 最后才画图、做多条件比较和解释。

其核心判断是：pathway 结果是以 method、universe 和 database version 为条件的 claim，不是算法自动返回的无条件发现。

#### 三代 pathway analysis 与分叉

源 Skill 保留 Khatri 2012 的三代框架：

1. **ORA**：预选 gene list 相对于背景的 over-representation；
2. **FCS/GSEA**：全量排序中 gene set 的协调变化；
3. **Pathway topology**：考虑 pathway 中节点/边关系的拓扑影响。

操作分叉：

- 如果几乎所有 measured/tested genes 都有有意义的 signed statistic，例如 DESeq2 Wald stat，使用 GSEA；
- 如果只有预选的 DE hits、co-expression module、GWAS loci 或 screen hits，使用 ORA，并定义 tested-gene universe；
- 有全量 ranking 却强行做 ORA，会丢掉协调的弱信号；
- 用全基因组做 ORA background，会把表达/检测偏差混入 enrichment。

#### 主流程

~~~text
DE results
    ↓
先判断 generation：全量 ranking → GSEA；预选 list → ORA
    ├── ORA：定义 testable-gene universe，按方法转换 ID
    │       ├── enrichGO       → GO
    │       ├── enrichKEGG     → KEGG
    │       ├── enrichPathway  → Reactome
    │       └── enrichWP       → WikiPathways
    └── GSEA：构造全量 named decreasing vector，固定 seed
            ├── gseGO
            ├── gseKEGG
            └── GSEA + msigdbr 等
    ↓
redundancy collapse + visualization
    ↓
带 universe、method、database version 的 claim/provenance
~~~

#### Stage map

| Stage | 目标 | 主要负责的细节 |
|---|---|---|
| 0 | 决定 ORA/GSEA | method selection 与输入判断 |
| 1 | 准备 list、ranking、universe | S06 的 stat、显著性、背景规则 |
| 2 | 转换 ID | OrgDb keyType、kegg-id、ENTREZ |
| 3a | ORA | list 相对 background 的 hypergeometric test |
| 3b | GSEA | 全量 ranking 的 running-sum |
| 4 | collapse + visualize | simplify、term similarity、dot/emap/GSEA 图 |

#### Stage 1：准备 list、ranked vector 和 universe

~~~r
library(clusterProfiler)
library(org.Hs.eg.db)

res <- read.csv('deseq2_results.csv', row.names = 1)

sig_genes <- rownames(
  subset(res, padj < 0.05 & abs(log2FoldChange) > 1)
)

universe_genes <- rownames(res[!is.na(res$pvalue), ])

ranked <- res$stat
names(ranked) <- rownames(res)
ranked <- sort(ranked[!is.na(ranked)], decreasing = TRUE)
~~~

要点：

- ORA list 可以是显著子集；
- universe 是进入 DE test 的 testable genes，不是 genome；
- GSEA rank 应来自全量、有方向的 statistic，首选 Wald stat；
- shrunken LFC 表经常没有 stat，不能因为表中有收缩后的 LFC 就误称其为 Wald stat；
- bare log2FC 会过度强调低 count 的不稳定基因。

#### Stage 2：按方法转换 ID

~~~r
sig_entrez <- bitr(
  sig_genes,
  fromType = 'SYMBOL',
  toType = 'ENTREZID',
  OrgDb = org.Hs.eg.db
)

bg_entrez <- bitr(
  universe_genes,
  fromType = 'SYMBOL',
  toType = 'ENTREZID',
  OrgDb = org.Hs.eg.db
)

ranked_map <- bitr(
  names(ranked),
  fromType = 'SYMBOL',
  toType = 'ENTREZID',
  OrgDb = org.Hs.eg.db
)

ranked_list <- ranked[ranked_map$SYMBOL]
names(ranked_list) <- ranked_map$ENTREZID
ranked_list <- ranked_list[!duplicated(names(ranked_list))]
ranked_list <- sort(ranked_list, decreasing = TRUE)

conv_rate <- nrow(sig_entrez) / length(sig_genes)
~~~

ID 路由：

| 方法 | 需要的 ID | 转换方向 |
|---|---|---|
| enrichGO/gseGO | OrgDb keyType：ENSEMBL、SYMBOL 或 ENTREZID | bitr |
| enrichKEGG/gseKEGG | kegg 或 ncbi-geneid | 先得到 ENTREZ；按 KEGG 规则传入 |
| enrichPathway/gsePathway | ENTREZ | bitr |
| enrichWP/gseWP | ENTREZ + organism | bitr |

转换后必须去重并重新排序，因为 remap 可能改变顺序。源 workflow 给出约 0.85 的 conversion rate 作为实用 QC 提示；低于该值应检查 ID type、物种、版本和 symbol rename，但不能把该数字直接当作普适项目验收阈值。

#### Stage 3a：ORA

~~~r
go_bp <- enrichGO(
  sig_entrez$ENTREZID,
  universe = bg_entrez$ENTREZID,
  OrgDb = org.Hs.eg.db,
  ont = 'BP',
  pAdjustMethod = 'BH',
  pvalueCutoff = 0.05,
  readable = TRUE
)

go_bp <- simplify(go_bp, cutoff = 0.7, by = 'p.adjust')

kegg <- enrichKEGG(
  sig_entrez$ENTREZID,
  universe = bg_entrez$ENTREZID,
  organism = 'hsa',
  keyType = 'ncbi-geneid',
  pvalueCutoff = 0.05
)

kegg <- setReadable(
  kegg,
  OrgDb = org.Hs.eg.db,
  keyType = 'ENTREZID'
)

library(ReactomePA)
reactome <- enrichPathway(
  sig_entrez$ENTREZID,
  universe = bg_entrez$ENTREZID,
  organism = 'human',
  pvalueCutoff = 0.05,
  readable = TRUE
)
~~~

ORA 的不可替代输入是 list + universe + ID type + database version。GO 和 Reactome 通常可以在版本固定的本地 annotation/database 下重现；KEGG 和 WikiPathways 的参考实现可能查询 live database，需要记录日期。

#### Stage 3b：GSEA

~~~r
set.seed(123)

gsea_go <- gseGO(
  ranked_list,
  OrgDb = org.Hs.eg.db,
  ont = 'BP',
  minGSSize = 10,
  maxGSSize = 500,
  pvalueCutoff = 0.05,
  verbose = FALSE
)

gsea_kegg <- gseKEGG(
  ranked_list,
  organism = 'hsa',
  minGSSize = 10,
  maxGSSize = 500,
  pvalueCutoff = 0.05,
  verbose = FALSE
)
~~~

需要固定 seed；vector 必须 named、全量、decreasing。读取 leading edge 时要报告其 gene core，而不是把一个 pathway term 当作所有成员都同等支持。

#### Stage 4：去冗余与可视化

大量 GO term 经常只是同一批基因以 DAG 关系重复出现。先用 simplify 或 pairwise_termsim，再绘图：

~~~r
library(enrichplot)

go_bp <- pairwise_termsim(go_bp)

dotplot(go_bp, showCategory = 20)
emapplot(go_bp, showCategory = 30)
gseaplot2(gsea_go, geneSetID = 1:3)
~~~

emapplot/treeplot 需要先 pairwise_termsim；cnetplot 可直接使用 geneID 关系；gseaplot2 应接收 gseaResult，不应误接 enrichResult。BP/MF/CC 应分别 simplify，不能把 ont = 'ALL' 当作一个可直接简化的单一 DAG。

#### 多条件比较

同一模型下比较多个 gene list，应使用 compareCluster，而不是比较独立运行结果的 raw p 或 -log10(p)：

~~~r
gene_clusters <- list(A = sig_A, B = sig_B, C = sig_C)

cc <- compareCluster(
  gene_clusters,
  fun = 'enrichKEGG',
  organism = 'hsa',
  universe = bg_entrez$ENTREZID
)

dotplot(cc, showCategory = 10)
~~~

对 GSEA 比较 NES；对 ORA 要注意 set size、sample size 和 universe 差异。compareCluster 漏传 universe 会静默回到默认背景，因此必须检查参数是否被转发。

#### 04-pathway-workflow 的典型失败模式

| 现象 | 机制 | 回退 |
|---|---|---|
| 没有传 universe | 分母变成物种全注释基因 | 使用实际 testable genes |
| 有完整 ranking 却跑 ORA | 二值化丢失弱而协调的信号 | 使用 GSEA |
| ENSEMBL/SYMBOL 直接给 KEGG/Reactome/WP | 数据库期待 kegg/ENTREZ | 按方法转换并检查 conversion rate |
| GSEA 没有 seed 或 vector 未排序 | permutation 不稳定或排名错误 | named decreasing vector + set.seed |
| live DB 结果没有日期 | 数据库更新后不能复现 | 记录版本/日期；必要时使用 local snapshot |
| 40 个重叠 term 被当作 40 个独立发现 | GO DAG/共享 gene 造成冗余 | simplify、pairwise_termsim、leading edge |
| shrunken LFC 表拿不到 stat | shrinkage 输出不含原始 stat | 回到 unshrunken results(dds)$stat |
| ID mapping 全空 | keyType、物种或版本不匹配 | 检查 keyType/OrgDb/organism |
| emapplot/treeplot 空白 | 未先算 pairwise_termsim | 补齐前置步骤 |

#### 参考阈值和当前状态

源 Skill 保留以下参考参数：pvalueCutoff=0.05、qvalueCutoff=0.2、BH、minGSSize=10、maxGSSize=500、simplify cutoff=0.7、conversion rate 约大于 0.85、set.seed(123)。这些是 reference defaults 或审计提示，不是已经批准的项目规格。

当前它仍是 workflow reference：依赖的 go-enrichment、gsea、kegg-pathways、reactome-pathways、wikipathways 和 enrichment-visualization 没有在本目录全部作为可运行组件登记。后续需要决定哪些依赖进入项目 runtime、哪些只保留为参考。

## 5. S10：KEGG snapshot、SPIA、graphite 与 pathview 拓扑分支

### 5.1 参考 Skill：05-kegg —— KEGG ORA、GSEA、SPIA、graphite 和 map overlay

<!-- BEGIN_ARSSC
contract_version: "0.1"
skill_id: "05-kegg"
display_name_zh: "KEGG ORA/GSEA、SPIA、graphite 与 map overlay"
kind: "reference-skill"
primary_stage: "S10"
secondary_stages: ["S08", "S09", "S12", "S13"]
source_role: "english-reference-copy"
source_paths: ["spec-mvp/skills/reference-stack/05-kegg/SKILL.md", "spec-mvp/skills/reference-stack-zh-CN/05-kegg/SKILL.md"]
registration: "not-registered"
runtime_status: "reference-only"
status_note_zh: "KEGG live DB、gson snapshot、SPIA、graphite 和 pathview 均是方法参考；当前没有已验证 topology runtime。"
input_contract: ["KEGG_compatible_IDs", "foreground_or_ranked_vector", "signed_DE_vector", "organism_code", "keyType", "database_snapshot_or_access_date"]
output_contract: ["KEGG_ORA", "KEGG_GSEA", "SPIA_result", "graphite_topology_result", "gson_snapshot", "pathview_overlay", "database_provenance"]
core_apis: ["clusterProfiler::enrichKEGG", "clusterProfiler::gseKEGG", "SPIA", "graphite", "gson", "pathview"]
preconditions: ["ID_join_is_valid", "organism_and_keyType_match", "GSEA_vector_is_full_named_sorted", "SPIA_map_is_compatible", "network_or_snapshot_policy_is_declared"]
hard_boundary: ["KEGG_is_not_static_R_package", "SPIA_requires_signed_DE_vector", "not_all_KEGG_maps_are_SPIA_compatible", "live_database_requires_date_or_snapshot"]
END_ARSSC -->

**来源**：spec-mvp/skills/reference-stack/05-kegg/SKILL.md  
**在总 Flow 中的位置**：S10；也承接 S08/S09 的 KEGG ORA/GSEA 输入。  
**当前状态**：英文参考副本；包含 clusterProfiler、gson、SPIA、graphite 和 pathview 的方法参考，不是当前项目已经验证的 topology runtime。

#### 作用

对 KEGG pathway、KEGG module 和 KEGG 的有向带符号拓扑做三代 pathway analysis：

| 代际 | 方法 | 输入 | 回答的问题 |
|---|---|---|---|
| 第一代：ORA | enrichKEGG、enrichMKEGG | gene list + universe | 哪些 pathway/module 的成员过度代表 |
| 第二代：GSEA | gseKEGG | 全量 named ranked vector | 哪些 pathway 的成员在全量排序中协调偏移 |
| 第三代：topology | SPIA、graphite + runSPIA | signed log2FC + universe + pathway graph | 结合节点位置、边方向和 effect，哪里发生了 pathway perturbation |

这里最重要的边界是：KEGG 是 live database，不是一个静态 R package。enrichKEGG、gseKEGG 和相关查询可能随 REST 数据更新而变化；正式报告必须记录 access date，最好用 gson snapshot 固定数据。

#### 输入和输出

**上游输入**：

- S06 的显著 gene list、tested universe 或全量 ranking；
- organism code，例如 hsa、mmu、rno、pae；
- KEGG 所需的 keyType 和 ID namespace；
- ORA 的 foreground + universe，或 GSEA 的 named decreasing vector；
- SPIA 的 named log2FC、all universe 和 signaling map；
- 研究问题是 membership、rank 还是 signed perturbation；
- access date、KEGG release/snapshot、package versions。

**下游输出**：

- KEGG pathway/module enrichment table；
- pvalue、p.adjust、qvalue、GeneRatio、BgRatio、Count、geneID；
- GSEA 的 NES、leading edge 和 pathway-level statistics；
- SPIA 的 pNDE、pPERT、pG、pGFdr、pGFWER、tA、Status；
- gson snapshot；
- pathview map image/PDF；
- database、ID、universe 和 topology provenance。

#### KEGG ID join 规则

KEGG 的 ID join 是此 Skill 的关键边界：

| 数据类型 | 推荐 ID/参数 | 不能做的事 |
|---|---|---|
| 人、鼠等 model eukaryote | SYMBOL/ENSEMBL 先转 ENTREZ；keyType = ncbi-geneid | 直接把 OrgDb 的 SYMBOL/ENSEMBL 传给 enrichKEGG |
| 细菌/原核 | KEGG locus tag；keyType = kegg | 强行使用 org.*.eg.db 或 Entrez identity |
| 非模式、无 KEGG genome | 映射至 KO；organism = ko | 假造一个错误的物种 code |
| UniProt/NCBI protein 输入 | bitr_kegg 转换 KEGG ID flavor | 误用 bitr 代替 KEGG conv endpoint |

检查物种可以使用 search_kegg_organism()。原核 locus tag 必须和 KEGG 对应 strain 的注释一致；重注释或换 strain 后，精确字符串 join 可能大量丢失。

示例：

~~~r
library(clusterProfiler)
library(org.Hs.eg.db)

de <- read.csv('de_results.csv')

sig_symbols <- de$gene[
  de$padj < 0.05 &
  abs(de$log2FoldChange) > 1
]

sig_entrez <- bitr(
  sig_symbols,
  fromType = 'SYMBOL',
  toType = 'ENTREZID',
  OrgDb = org.Hs.eg.db
)$ENTREZID

universe <- bitr(
  de$gene[!is.na(de$pvalue)],
  fromType = 'SYMBOL',
  toType = 'ENTREZID',
  OrgDb = org.Hs.eg.db
)$ENTREZID
~~~

不要把 symbol mapping loss 静默丢掉；foreground 和 universe 必须通过同一条 mapping path，并检查去重。

#### KEGG ORA：enrichKEGG 与 enrichMKEGG

~~~r
kk <- enrichKEGG(
  gene = sig_entrez,
  organism = 'hsa',
  keyType = 'ncbi-geneid',
  universe = universe,
  pvalueCutoff = 0.05,
  pAdjustMethod = 'BH',
  minGSSize = 10,
  maxGSSize = 500,
  qvalueCutoff = 0.2
)

kk <- setReadable(
  kk,
  OrgDb = org.Hs.eg.db,
  keyType = 'ENTREZID'
)

head(as.data.frame(kk))

mkk <- enrichMKEGG(
  gene = sig_entrez,
  organism = 'hsa',
  keyType = 'ncbi-geneid',
  universe = universe
)
~~~

enrichMKEGG 以 M-number module 为单位，集合通常更小、更稀疏：分辨率更高，但 power 也可能更低，且许多 gene 不属于 module。报告 adjusted p-value/qvalue，不要只报告 raw pvalue。KEGG 没有和 enrichGO 完全相同的 readable 参数形态；通常先做结果，再在适用的 eukaryote 场景使用 setReadable。

#### KEGG GSEA：gseKEGG

~~~r
geneList <- de$log2FoldChange
names(geneList) <- de$entrez
geneList <- sort(
  geneList[!is.na(geneList)],
  decreasing = TRUE
)

set.seed(123)

kk2 <- gseKEGG(
  geneList = geneList,
  organism = 'hsa',
  keyType = 'ncbi-geneid',
  minGSSize = 10,
  maxGSSize = 500,
  pvalueCutoff = 0.05
)
~~~

geneList 必须 named、全量、有方向并按 decreasing 排序。实际 rank metric 的选择属于 S08/S09 的 gsea 方法语义；这里负责 organism、keyType 和 KEGG database 边界。不要从被 padj 截断的 list 构造 GSEA。

#### SPIA：有符号 pathway topology

SPIA 只适合有清晰 signaling topology 的 KEGG map。它把：

- pNDE：DE gene membership 的 over-representation evidence；
- pPERT：把 log2FC 沿 KGML 的 activation/inhibition edges 传播后得到的 perturbation evidence；
- pG：二者组合后的 global probability；
- pGFdr/pGFWER：多重校正后的结果；
- tA：累计 perturbation 及其方向；
- Status：由 tA 推断的 Activated 或 Inhibited；

放在同一个 pathway-level 输出中。

~~~r
library(SPIA)

sig <- de[de$padj < 0.05, ]

map <- bitr(
  sig$gene,
  'SYMBOL',
  'ENTREZID',
  org.Hs.eg.db
)

de_vec <- setNames(
  sig$log2FoldChange[
    match(map$SYMBOL, sig$gene)
  ],
  map$ENTREZID
)

de_vec <- de_vec[!duplicated(names(de_vec))]

res <- spia(
  de = de_vec,
  all = universe,
  organism = 'hsa',
  nB = 2000,
  plots = FALSE
)
~~~

SPIA 要求 DE IDs 落在 all universe 中。源 Skill 提示如果超过约 1% 的 DE IDs 不在 all 中可能中止；该比例是实现约束/审计提示，不可跳过而继续解释。de 和 all 必须从同一 ID namespace 产生。

graphite 路由：

~~~r
library(graphite)

db <- pathways('hsapiens', 'kegg')
db <- convertIdentifiers(db, 'ENTREZID')
prepareSPIA(db, 'kegg_hsa_spia')

gr <- runSPIA(
  de = de_vec,
  all = universe,
  'kegg_hsa_spia'
)
~~~

graphite 可处理 harmonized graph、complex/family 和部分 Reactome topology；它不应被项目适配器静默调用，必须在输入、图数据库和输出解释中明确。

代际选择不可混用：

- glycolysis、TCA 等 compound-mediated metabolic map 不适合 SPIA 的 gene-to-gene signed propagation；
- metabolic membership 用 enrichKEGG 或 gseKEGG；
- broad signaling map 且有 signed effect 时才考虑 SPIA/graphite；
- SPIA 的 Activated/Inhibited 是由模型和 topology 推出的方向标签，不是实验因果证明。

#### KEGG snapshot：gson

要把 live KEGG 结果变成可复现的离线输入，源 Skill 推荐获取当前集合后写入 gson：

~~~r
library(gson)

k <- gson_KEGG('hsa')
k@accessed_date <- as.character(Sys.Date())

write.gson(
  k,
  file.path(tempdir(), 'kegg_hsa.gson')
)

k <- read.gson(
  file.path(tempdir(), 'kegg_hsa.gson')
)

kk_pinned <- enricher(
  sig_entrez,
  gson = k,
  universe = universe
)

gsea_pinned <- GSEA(
  geneList,
  gson = k
)
~~~

use_internal_data = TRUE 不是当前 KEGG release 的 pin；它可能加载过时的 2012 KEGG.db。若报告要求 reproducibility，必须区分 live query、legacy internal data 和 gson snapshot，不能把三者写成同一版本。

#### compareCluster 与 pathview

多条件比较用 pathway ID set 和统一模型，不直接比较多个独立 run 的 raw p-value：

~~~r
clusters <- list(
  up = up_entrez,
  down = down_entrez
)

ck <- compareCluster(
  geneClusters = clusters,
  fun = 'enrichKEGG',
  organism = 'hsa',
  keyType = 'ncbi-geneid'
)

ck <- setReadable(
  ck,
  OrgDb = org.Hs.eg.db,
  keyType = 'ENTREZID'
)
~~~

pathview 是 KEGG-specific map overlay，不是一般 enrichment dotplot：

~~~r
library(pathview)

vals <- setNames(de$log2FoldChange, de$entrez)

pathview(
  gene.data = vals,
  pathway.id = 'hsa04110',
  species = 'hsa',
  gene.idtype = 'entrez'
)
~~~

pathview 会下载 KGML/image、把每 gene value join 到 map 节点，并在工作目录生成图；因此同样需要网络、日期、输入快照和输出文件记录。

#### 05-kegg 典型失败模式

| 现象 | 机制 | 回退 |
|---|---|---|
| enrichKEGG 返回 0 | SYMBOL/ENSEMBL 未转 KEGG ID、organism 错或 API 不可达 | 转 ENTREZ/locus tag，核对 organism 和网络 |
| setReadable 报错 | 原核无适用 OrgDb | 跳过 setReadable，保留 raw KEGG IDs |
| live query 无法复现 | KEGG release 持续更新 | gson snapshot + access date |
| gson 传给 enrichKEGG 被拒 | enrichKEGG/gseKEGG 接口不接受该参数 | 使用 generic enricher/GSEA + gson |
| SPIA 在 glycolysis 上无意义 | metabolic map 不是清晰 signed gene graph | 改用 enrichKEGG/gseKEGG |
| SPIA 报 DE IDs 不在 all | universe 与 DE vector 不是同一 ID 空间 | 同一 mapping path 重建 |
| 细菌结果为空 | 强行用 Entrez/OrgDb，或 locus tag/strain 不匹配 | keyType = kegg、核对 strain，必要时 route to KO |
| ORA 结果过度丰富 | 漏传 universe | 使用能被调用的 tested genes |
| 不同时间路径数不同 | live database 变化 | 固定 snapshot 并记录日期 |

#### 当前状态与不可替代边界

这是 KEGG 参考 Skill，不是项目已经批准的 S10 runtime。不可替代边界如下：

- KEGG query 结果是 timestamped join，不是脱离数据库版本的生物学事实；
- ORA、GSEA 和 SPIA 分别回答 membership、rank 和 signed topology 问题；
- KEGG organism code、keyType、ID namespace 必须与输入匹配；
- SPIA 只在合适 signaling topology 上解释；
- live 数据库、gson snapshot、旧 KEGG.db 不能混为一谈；
- topology 分数不能直接提升为因果机制；
- 所有结果必须把 universe、ID mapping、database access 和 method 写入 provenance。

## 6. S11：跨分支整合

### 6.1 项目适配器：cross-branch-integration

<!-- BEGIN_ARSSC
contract_version: "0.1"
skill_id: "cross-branch-integration"
display_name_zh: "跨分支结果整合适配器"
kind: "project-adapter"
primary_stage: "S11"
secondary_stages: ["S00", "S09", "S12", "S13"]
source_role: "project-adapter"
source_paths: ["spec-mvp/skills/cross-branch-integration/SKILL.md", ".agents/skills/cross-branch-integration/SKILL.md"]
registration: "registered"
runtime_status: "not-verified"
status_note_zh: "SKILL.md 已给出输入输出和 fail-closed 条件；deterministic adapter 是否完整接线仍待核对。"
input_contract: ["branch_result_tables_or_matrices", "stable_subject_sample_map", "feature_namespace", "assembly_or_reference_release", "effect_field", "direction_rule"]
output_contract: ["matched_records", "unmatched_records", "intersection", "direction_strata", "integration_limitations", "validation_record"]
core_apis: ["deterministic Rscript", "table/matrix operations", "sample-map join", "ID harmonization"]
preconditions: ["each_branch_result_is_comparable", "subject_map_is_explicit", "namespace_is_harmonized", "direction_and_scale_are_declared", "validation_target_exists_for_predictive_claim"]
hard_boundary: ["does_not_infer_subject_map_from_results", "does_not_silently_call_joint_model", "association_is_not_causality", "predictive_claim_requires_held_out_validation"]
END_ARSSC -->

**来源**：spec-mvp/skills/cross-branch-integration/SKILL.md  
**宿主发现副本**：.agents/skills/cross-branch-integration/SKILL.md  
**源参考**：vendor/sources/bioSkills/multi-omics-integration。  
**在总 Flow 中的位置**：S11；接收不同 omics/分析分支的结果，输出可比较的交集、方向一致性和限制报告。  
**当前状态**：项目适配器；SKILL.md 已给出契约和 fail-closed 条件，实际 deterministic Rscript/adapter 是否完整可运行需后续核对。

#### 作用

当多个分支共享 subject、样本或生物学问题时，对 branch result tables/matrices 做 correspondence validation、ID harmonization、尺度审计、gene intersection 和 direction stratification。它不是每个 omics 分支的 normalization，也不是 causal integration model。

#### 上游输入

| 输入 | 必须说明 |
|---|---|
| branch result tables/matrices | 每个分支的输入、统计量、effect 字段和结果版本 |
| sample map | stable subject ID；不能用行号推断对应 |
| feature namespace | gene/protein/peak 等 ID 类型、assembly/reference release |
| branch labels | 哪一列/哪一分支属于何种 omics |
| direction convention | effect 正负与 up/down 的含义 |
| integration question | shared gene、direction concordance、subtype、latent axis 或 predictive signature |
| batch/scale metadata | 变换、尺度、缺失 view 和 batch 处理 |

#### 下游输出

- sample-map audit；
- matched/unmatched records；
- gene/feature intersection table；
- up/up、down/down、up/down、down/up direction strata；
- 各 branch 的 provenance；
- limitation report；
- integrated score（仅在有明确 validation plan 时可选）。

#### 核心包、函数和前置条件

项目 catalog 指定的执行形态是 deterministic Rscript 和表格/矩阵库；MultiAssayExperiment 只有在确实需要 joint container 时才是可选组件，不由本 Skill 自动启用。当前 SKILL.md 没有规定唯一的统计包，核心操作是 sample-map join、ID harmonization、dedup、intersection、direction stratification 和 validation record；参考脚本为 references/integration_design_diagnostic.R。

前置条件是：每个分支已产生可比较的结果表或矩阵；stable subject/sample map 已提供；feature namespace、assembly/reference release、effect field、方向规则、batch/scale 和缺失 view 已说明；若声称 predictive signature 或 integrated score，还必须有 held-out validation target。

#### 工作流

1. 先把问题分类为 shared genes、direction concordance、subtype、shared latent axis 或 predictive signature；
2. 验证 subject/sample map；保留 unmatched/missing cases，不能按 row order 对齐；
3. 用同一 reference namespace 规范 feature IDs；记录去重规则；
4. 从已执行结果表计算 intersection 与 direction strata；方向来自 signed effect 或 statistic，并记录 cutoff；
5. 若请求 joint model，先检查尺度平衡、batch identifiability、missing-view handling 和 out-of-sample validation target，再拟合。

对应关系可包括 paired、mosaic、horizontal 和 diagonal 等形态；具体选择要以上游 integration design 和 metadata 为依据，不从结果表反推 subject correspondence。

#### 方向分层

一个最小方向交集表可使用：

| branch A | branch B | 解释 |
|---|---|---|
| up | up | 同方向一致 |
| down | down | 同方向一致 |
| up | down | 方向冲突 |
| down | up | 方向冲突 |
| not called | called | 单分支证据或 power 差异，不等于反向 |

方向阈值、effect field、reference level 和 NA/未检出处理必须明确。只有交集而没有方向、sample correspondence 和 branch provenance 的结果，最多是描述性 gene overlap。

#### Fail closed

以下情况必须停止而不是给出漂亮的整合分数：

- subject correspondence 是推断出来的而非提供的；
- ID 混合 assembly 或 namespace；
- 某分支没有可比较的 effect 字段；
- direction convention 不一致；
- batch 与 biology 完全混杂；
- 声称 integrated signature 却没有 held-out validation。

MOFA2、mixOmics、SNF 是独立 runtime component，不由该 Skill 静默调用。gene intersection 是描述性结果，不能单独证明两个分支共享 causal mechanism。

#### 当前状态和边界

该适配器已经给出输入/输出契约，但参考文档和具体 adapter 的交付边界仍需检查。后续需要确认：

- 是否真的存在 deterministic Rscript；
- 对 unmatched、duplicate、missing values 的输出格式；
- 是否支持 protein/peak 等非 gene feature；
- direction strata 的阈值和 effect convention 是否可配置；
- integrated score 是否被错误地默认启用；
- cross-branch 结果如何接入 S12 的 claim/provenance。

## 7. S12：Claim / provenance 收口

这一层不是单独的生信算法 Skill，而是把前面每层的输入、决策、证据和边界汇总成可审计 claim。已有项目适配器和 research-evidence-kernel 的存在，说明这是项目控制面的一部分；本合并稿只把接口排在这里，不改变现有实现。

### 7.1 每个结果对象应携带的最小 provenance

| 类别 | 必须记录 |
|---|---|
| 数据身份 | 输入文件路径/摘要、checksum、物种、assembly/reference release |
| 样本 | sample ID、subject ID、condition、batch、sex、paired 信息和 unmatched/removed 记录 |
| 测量层 | raw counts、normalized、VST/rlog/log-CPM 等表示 |
| 设计 | design formula、reference level、contrast、interaction、LRT/Wald/QL 等 estimand |
| 过滤 | low-count rule、independent filtering、Cook's outlier、NA 原因 |
| 统计 | effect/LFC、raw p、padj/FDR/qvalue/lfsr/svalue 的具体语义 |
| pathway 输入 | foreground、full ranking、tested universe、ID mapping loss、dedup rule |
| 方法分叉 | ORA/GSEA/topology 的选择与理由 |
| 数据库 | OrgDb/GO.db/KEGG/Reactome/WikiPathways 名称、版本或 access date |
| 图形 | plot source table、shrinkage、axis、threshold、label selection、scale |
| 跨分支 | sample map、ID namespace、direction convention、matched/unmatched |
| 环境 | R/Python 版本、package versions、seed、命令或 workflow identity |
| 限制 | 未完成、低 power、live DB、mapping loss、未验证的假设 |

### 7.2 Claim 的分层

| Claim 层级 | 可支持的表达 | 不可直接支持的表达 |
|---|---|---|
| 数据/样本 QC | 样本存在某种聚类、批次、离群或输入问题 | 仅凭 PCA 断言因果 |
| DE | 在指定 design/contrast/模型下某 gene 的 effect 与 FDR 结果 | 把 post-hoc LFC 筛选写成幅度 FDR |
| pathway ORA | 在指定 foreground/universe/database 下某 term 过度代表 | 疾病诊断、机制证明 |
| GSEA | 全量 ranking 中某 pathway 协调偏移，含 NES/leading edge | 所有 pathway gene 同等变化 |
| SPIA/topology | 指定 KEGG graph 下累计 perturbation 方向/分数 | 真实生物因果方向 |
| cross-branch | stable mapping 下的交集或方向一致性 | 共享 causal mechanism、validated predictive signature |
| 复现 | 在指定 snapshot、版本和 seed 下可复现 | live database 永久不变 |

### 7.3 当前底稿的统一对象关系

~~~text
数据/metadata
  → QC 与样本诊断
  → design/contrast
  → DE result
  → 结果整理（effect/padj/annotation/universe）
      ├─→ visualization
      ├─→ ORA
      ├─→ GSEA
      ├─→ KEGG topology
      └─→ cross-branch
  → claim + provenance
  → tests/acceptance
~~~

这张关系图只规定阅读顺序，不改变现有运行逻辑，也不意味着所有分支都必须在每个项目中执行。

## 8. S13：测试与验收

### 8.1 测试对象的区分

当前项目中的测试不是同一种东西，需要分层阅读：

| 测试对象 | 位置/来源 | 意义 |
|---|---|---|
| reference Skill 的 examples/tests | reference-stack 下的 examples、tests/data、test_pathway_enricher.py 等 | 上游参考实现或示例验证 |
| 项目适配器 references | spec-mvp/skills/<adapter>/references | 适配器使用说明、上游材料或局部脚本 |
| 项目测试 | spec-mvp/tests/test_multiqc_vertical_slice.py、test_shared_integration_mvp.py | 当前项目 vertical slice/共享整合行为 |
| evidence kernel 测试 | spec-mvp/research-evidence-kernel/tests/test_kernel.py | Claim/provenance 控制面测试 |
| workflow | spec-mvp/workflows/multiqc-vertical-slice.yml | workflow 编排，不等于 Skill 实现 |
| Spec/文档 | spec-mvp/README.md、docs、schemas | 规格和解释，不等于 executable runtime |

本轮不执行这些测试，只把它们归类到验收层。测试文件存在不等于所有 13 个逻辑 Skill 已有端到端覆盖。

### 8.2 按 Flow 的验收矩阵（待执行）

| 阶段 | 最小验收问题 | 证据 |
|---|---|---|
| S00 | 输入类型、物种、ID、样本 map、表达尺度是否明确 | contract/checksum/metadata |
| S01 | sample ID、subject ID、group、batch、sex、paired 是否一致 | metadata QC report |
| S02 | raw data/表达矩阵格式、缺失、重复、低 count 和 QC summary 是否可见 | MultiQC/矩阵 QC |
| S03 | PCA/MDS 使用的变换、blind、轴、outlier 解释是否记录 | PCA/MDS、distance matrix |
| S04 | design 是否满秩；paired/batch/contrast/reference level 是否固定 | design matrix、contrast record |
| S05 | 模型是否与 input scale 匹配；方法、过滤、seed、session 是否记录 | DE result + session info |
| S06 | 完整结果、NA 原因、tested set、FDR、annotation、GSEA rank、ORA universe 是否分开 | result tables + mapping audit |
| S07 | 图轴、shrinkage、threshold、label、heatmap scale 是否与结果语义一致 | plot data/figure metadata |
| S08 | ORA/GSEA 是否由输入形态决定，并记录理由 | method decision record |
| S09 | foreground/universe/ranking 是否同 namespace；mapping rate 和 dedup 是否可追溯 | ID audit |
| S10 | KEGG 是否记录 access date/snapshot；SPIA 是否只用于合适 signaling graph | gson/SPIA logs |
| S11 | sample map、ID、direction、batch、held-out validation 是否通过 | integration audit |
| S12 | claim 是否超出设计、统计和数据库证据边界 | evidence/provenance report |
| S13 | 测试是否覆盖正常、空结果、错误输入、mapping loss 和 fail-closed | unit/integration/acceptance logs |

### 8.3 需要保留的失败测试类型

- 缺文件、sample mismatch、少于两组或组内重复不足；
- raw counts/normalized scale 与 DE method 不匹配；
- design 奇异、contrast 不存在、reference level 方向错误；
- 所有基因 padj=NA、Cook's outlier、independent filtering；
- p-value histogram 反常；
- gene mapping 为空、重复过多、物种错误；
- ORA 缺失 universe；
- GSEA ranking 未命名、未排序、非全量；
- KEGG organism/keyType 错、API 不可达、snapshot 缺失；
- SPIA 的 DE vector 不在 all 或用于 metabolic map；
- cross-branch subject map 缺失、namespace 不一致、方向定义冲突；
- provenance 缺失但结果仍被请求用于 claim。

这些测试类型是验收设计，不代表本轮已经运行或已经通过。

## 9. 13 个逻辑 Skill 的总索引与状态

| Flow 层 | Skill | 类型 | 主要输入 | 主要输出 | 当前状态 |
|---|---|---|---|---|---|
| S00–S05 | bulk-pa-luad | 项目适配器 | counts/metadata/design/contrast | bulk DE workflow outputs | 项目适配器；执行边界需依 references 核对 |
| S01–S02 | multiqc | 项目适配器 | FastQC/原始 QC 文件 | QC report、summary、fail/warn | 项目适配器；有 vertical-slice 关联但本轮未运行 |
| S03 | 01-mds | 英文参考副本 | VST/log-CPM/样本特征 | PCA/MDS/t-SNE/UMAP/PHATE embeddings | 参考；非运行时 Skill |
| S03/S08 | wgcna-module-constraint | 项目适配器 | expression + metadata | modules、eigengenes、hub/constraint sets | 项目适配器/参考脚本；未完成完整 runtime |
| S04–S05 | 02-deg | 英文参考副本 | expression matrix + group/design | DE table、基础图、session info | 参考；源目录有脚本/测试资产，仍需项目接入审计 |
| S06 | 02-deg-results | 英文参考副本 | DESeq2/edgeR fitted result | cleaned result、annotation、rank、universe | 参考；方法完整，未封装统一 runtime |
| S07 | 03-de-visualization | 英文参考副本 | DE object/result + transformed matrix | diagnostic/result figures | 参考；与 03-volcano 重叠 |
| S07 | 03-volcano | 英文参考副本 | result + shrunken LFC/p-value/padj | volcano/MA + labels | 参考；与 03-de-visualization 重叠 |
| S08–S09 | pathway-enrichment | 项目适配器 | executed DE/module result + universe/IDs | GO/KEGG result + mapping/provenance | 项目适配器；KEGG 网络是显式例外 |
| S08–S09 | 04-pathway-enricher | 英文参考副本 | gene list | Enrichr tables/figures/report | 参考；外部 API，不是本地 runtime |
| S08–S09 | 04-pathway-workflow | 英文参考副本 | DE list/ranking/universe | ORA/GSEA routes + collapsed results | 参考 workflow；依赖未全部登记的 per-method skills |
| S10 | 05-kegg | 英文参考副本 | list/rank/log2FC + KEGG IDs/topology | KEGG ORA/GSEA/SPIA/snapshot/pathview | 参考；live DB/snapshot/topology 均待 runtime 审计 |
| S11 | cross-branch-integration | 项目适配器 | branch tables/matrices + sample map | intersection、direction strata、limitation | 项目适配器；joint model 不由其静默调用 |

### 9.1 中文审阅版不是另一套 Skill

spec-mvp/skills/reference-stack-zh-CN/ 下已有：

- 01-mds；
- 02-deg；
- 02-deg-results；
- 03-de-visualization；
- 03-volcano；
- 04-pathway-enricher；
- 04-pathway-workflow；
- 05-kegg；
- analysis-order.md 和 README.md。

它们是已有中文审阅/翻译镜像，不在上表重复计数为新的逻辑 Skill。本文件的中文正文是按总 Flow 重新组织的合并审阅底稿；英文 reference-stack 仍是逐项核对来源，中文镜像仍然保留。

### 9.2 物理目录与运行时的区分

~~~text
本机原始来源（C:/Users/ldc/.codex/skills/）
        ↓ 只读核对来源
项目 .agents/skills/
        ↓ 宿主发现副本
spec-mvp/skills/<project-adapter>/
        ↓ 项目适配器与 references
spec-mvp/skills/reference-stack/
        ↓ 英文参考副本、examples、tests、脚本
spec-mvp/skills/reference-stack-zh-CN/
        ↓ 中文审阅/翻译镜像
spec-mvp/docs/CONSOLIDATED-SKILLS-WORKFLOW-zh-CN.md
        ↓ 本次合并审阅底稿

spec-mvp/workflows/、spec-mvp/tests/、spec-mvp/research-evidence-kernel/
        ↓ 控制面/验收面；不等于 Skill runtime
~~~

判断“可运行”必须看实际脚本、依赖、输入输出契约、测试和 workflow 接线；不能只看 SKILL.md 的 prose。判断“已登记”也不能等同于“已经实现”。

### 9.3 Skill → S 阶段 → E 抽象层的统一看板

下表是后续删除、合并、补充和 Spec 化时的唯一比较入口。它只做索引，不替代各 Skill 段落中的方法细节，也不把参考 Skill 变成 runtime。

| 原始 `skill_id` | 主科研阶段 | 主工程层 | 类型/来源角色 | 当前 runtime 判断 | 下一步只允许做的事 |
|---|---|---|---|---|---|
| `bulk-pa-luad` | S05 | E3 | 项目适配器 | 未验证 | 核对脚本、依赖、设计/结果契约和测试接线 |
| `multiqc` | S02 | E2 | 项目适配器 | 未验证；有 bounded slice 线索 | 核对 QC gate、输入 source map 和验收证据 |
| `01-mds` | S03 | E2 | 英文参考副本 | 仅参考 | 审计与 `03-de-visualization` 的边界，不直接注册 |
| `wgcna-module-constraint` | S03 侧支 | E2→E4 | 项目适配器/可选侧支 | 不完整 | 补齐 stability、preservation、fixture 和 fail gate 的证据需求 |
| `02-deg` | S05 | E3 | 英文参考副本 | 仅参考 | 将 group-only 接口与 S04 design contract 做差异审计 |
| `02-deg-results` | S06 | E3→E4 | 英文参考副本 | 仅参考 | 固化 DE table、padj、annotation、ranking、universe 的唯一字段候选 |
| `03-de-visualization` | S07 | E3 | 英文参考副本 | 仅参考 | 与 `03-volcano` 做重复/互补审计 |
| `03-volcano` | S07 | E3 | 英文参考副本 | 仅参考 | 决定是否作为通用 renderer 的子集或保留专项参考 |
| `pathway-enrichment` | S08 | E4 | 项目适配器 | 未验证 | 核对 ORA/GSEA 路由、数据库和网络边界 |
| `04-pathway-enricher` | S08 | E4 | 英文参考副本 | 仅参考 | 单独审计外部 Enrichr API、网络和 universe 语义 |
| `04-pathway-workflow` | S08 | E4 | 英文参考 workflow | 仅参考 | 列出缺失的 per-method 依赖，不把编排 prose 当 runtime |
| `05-kegg` | S10 | E4 | 英文参考副本 | 仅参考 | 区分 live KEGG、snapshot、SPIA、graphite 和 pathview 的契约 |
| `cross-branch-integration` | S11 | E4 | 项目适配器 | 未验证 | 核对 subject map、namespace、方向和 deterministic adapter |

此表明确了一个关键事实：**一个科研阶段可以挂多个 Skill，一个 Skill 也可以跨多个阶段；“合并”不能靠目录名称或编号判断，必须比较输入、输出、估计对象、硬边界和验收证据。**

## 10. 收敛后的剩余审计问题（本文件只记录，不修复）

第三步的结构判断已经完成：总览给出了哪些关系可以在接口层压缩、哪些必须保留为独立方法，以及哪些能力尚未形成项目 runtime。本节只保留实现、注册、来源、数据库和验证层面的剩余问题。

### 10.1 命名与重叠（判断见总览）

- 03-de-visualization 与 03-volcano 同时覆盖 shrunken LFC、volcano、MA、ggrepel、阈值和失败模式；
- 02-deg 的基础筛选/图形输出与 02-deg-results、03-de-visualization 有边界交叉；
- 04-pathway-enricher 的 Enrichr list-based API 与 pathway-enrichment/04-pathway-workflow 的 clusterProfiler ORA/GSEA 路径并存；
- pathway-enrichment 已有项目适配器，同时 05-kegg 又定义了 KEGG 专项边界；
- cross-branch-integration 的 result integration 与 research-evidence-kernel 的 evidence aggregation 本轮保持职责独立；后续只需明确二者的 handoff interface。

### 10.2 顺序与输入缺口

- 原始 02-deg 的 group file 不能表达 paired、batch、sex、subject 和 interaction；需要由 S04 设计契约补齐；
- p_threshold、logfc_threshold 的脚本参数与 S06 的 FDR、TREAT/lfcThreshold 语义并不天然一致；
- WGCNA 可以从 S02/S03 侧支进入 S08，但模块发现的稳定性、样本数和 preservation 还没有成为完整 runtime gate；
- S10 SPIA 需要 topology-compatible signaling map，而不是所有 KEGG map；
- cross-branch 的 subject map、namespace、assembly、direction convention 是硬输入，当前不能由结果表猜；
- S13 的项目测试覆盖明显少于 13 个逻辑 Skill，需要确认哪些是 MVP 范围、哪些仅为参考。

### 10.3 状态不确定性

- reference-stack 中某些 Skill 有脚本、examples 或 tests，但这些资产是否被项目 workflow 接线，不能由目录存在直接推出；
- reference-stack-zh-CN 是中文镜像/审阅版，不应在 runtime discovery 中重复注册；
- .agents/skills 与 spec-mvp/skills 的副本关系、更新方向和冲突优先级需要后续固定；
- skill-catalog.yml 的登记项、目录实际项、workflow 使用项可能不是同一集合；
- C:/Users/ldc/.codex/skills/ 的本机原始来源只做来源核对，不把其所有条目自动纳入本项目 13 个逻辑 Skill。

### 10.4 数据库和网络

- 04-pathway-enricher 的“本地处理”表述与向公开 Enrichr API POST gene symbols 存在冲突；
- 05-kegg 的 live REST、旧 KEGG.db 和 gson snapshot 的可复现语义不同；
- pathway-enrichment adapter 允许 KEGG 网络访问，但必须有 access date/release 或 local snapshot；
- 外部数据库更新可能导致相同代码返回不同 pathway term，必须在 claim 中显式说明。

## 11. 本轮明确未做的实现动作

- 未执行任何生信分析；
- 未运行 R、Python、CLI、MultiQC、DE、ORA、GSEA、SPIA、graphite 或 pathview；
- 未运行 benchmark；
- 未修改现有算法；
- 未重写上游 Skill；
- 未新增包或依赖；
- 未改变现有 workflow、runtime 或运行逻辑；
- 未删除、移动或覆盖原有 Skill、reference、中文镜像、Spec、workflow、测试和文档；
- 未把参考 Skill 宣布为可运行 Skill；
- 未删除、移动或改写源 Skill；合并判断仅写入总览的阅读入口和接口分层；
- 未把本合并稿本身提升为最终 Spec。

## 12. 下一阶段的操作入口（收敛判断之后）

第二步和第三步已完成。下一阶段不再继续重复清点，而是把收敛判断落到共同合同、运行接线和验证证据：

1. **P0：**冻结 sample/subject/pair/batch、expression scale、design/contrast、DE result、universe/mapping、方向和 provenance 的共同 contract，并核实 registry/install 事实；
2. **P1：**用已有 MultiQC 和 shared-integration 局部切片验证 workflow、artifact、verifier 和 human-review wiring；
3. **P1：**建立受限 bulk paired DE → result freeze → ORA/GSEA vertical slice；
4. **P1：**按总览的 D1/D2 决策实现 DE visualization 统一 renderer 和 pathway router，同时保留专项后端；
5. **P1/P2：**补齐 MDS/DE/pathway/WGCNA fixture、负例、数据库 snapshot、独立复现和 Claim/release gate；
6. **最后再决定：**哪些源参考升级为 runtime，哪些继续留在 reference-only，哪些目录可以在迁移后删除。

在上述实现完成前，本文中的“待审计”“参考”“项目适配器”“未完成”仍按证据边界解释；总览负责快速决策，本文负责逐段追溯。
