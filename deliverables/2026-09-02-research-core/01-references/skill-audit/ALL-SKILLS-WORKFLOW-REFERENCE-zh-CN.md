# Bio-Spec Kit 生信 Skills 总览与收敛决策（中文 Sketch）

> 文档角色：总览、快速路由和合并决策入口；不是运行时配置、Spec 合同或算法实现。  
> 核对范围：当前 checkout 的 `spec-mvp/skills/`、`.agents/skills/`、`extensions/`、`workflows/`、`specs/`、测试和登记文件。  
> 核对状态：本文件只读核对了文件、manifest、目录和测试定义；没有在本轮执行 R/Python/CLI、安装依赖或访问外部数据库。  
> 详细证据：[长版合并审阅底稿](./docs/CONSOLIDATED-SKILLS-WORKFLOW-zh-CN.md)。

## 0. 先给结论

### 0.1 计数口径

当前项目有 **13 个逻辑生信 Skill**：

- **5 个项目适配器**：`bulk-pa-luad`、`cross-branch-integration`、`multiqc`、`pathway-enrichment`、`wgcna-module-constraint`；
- **8 个英文参考 Skill**：`01-mds`、`02-deg`、`02-deg-results`、`03-de-visualization`、`03-volcano`、`04-pathway-enricher`、`04-pathway-workflow`、`05-kegg`。

下面这些对象不能混进 13 个生信 Skill：

| 对象 | 数量 | 正确身份 | 当前判断 |
|---|---:|---|---|
| `.agents/skills/<project-skill>` 与 `spec-mvp/skills/<project-skill>` | 5 对 | 宿主发现副本 + 项目暂存副本 | 每对只算 1 个逻辑 Skill |
| `reference-stack/` 与 `reference-stack-zh-CN/` | 8 对 | 英文参考副本 + 中文审阅镜像 | 每对只算 1 个逻辑 Skill；均非项目 runtime |
| `.agents/skills/speckit-*` | 10 | Spec Kit 控制面 Skill | 已在 Codex manifest 登记；负责 Spec 生命周期，不执行生信算法 |
| `extensions/bio-*` | 7 | Extension、wrapper、检查器和记录器 | 是执行/治理组件，不是 Skill；源包存在但当前未确认安装注册 |

当前最重要的事实：文件存在、能被目录扫描发现、已登记、可执行、科学上已验证、可以支持发布 Claim，是五个不同判断。不能由前一个判断推出后四个判断。

### 0.2 第三步已经形成的决策

1. **合并呈现和接口，不删除来源**：`03-de-visualization` 与 `03-volcano` 形成一个面向用户的 DE visualization 入口；`03-volcano` 保留为专门的 LFC/标签参考，源目录暂不删除。
2. **合并 pathway 路由，不合并算法后端**：`pathway-enrichment` 负责项目边界和统一输入输出，`04-pathway-workflow` 负责 ORA/GSEA 路由，`04-pathway-enricher` 是可选的外部 Enrichr 后端，`05-kegg` 负责 KEGG/拓扑专项。它们可以在一个入口下编排，不能压成同一个科学方法。
3. **DE 主链只统一交接合同**：`bulk-pa-luad` 是 PA/LUAD 配对场景适配器，`02-deg` 是通用模型参考，`02-deg-results` 是完整结果冻结和下游 handoff；三者相邻但不替代。
4. **QC 不做“大一统合并”**：`bio-intake`/metadata 检查、`bio-qc` 阈值判断和 `multiqc` 报告聚合失败责任不同，应串联而不是合并。
5. **WGCNA、跨分支整合和 Claim 收口保持独立**：它们分别改变估计对象、比较对象和证据/发布状态；只定义清晰的 handoff，不重写成一个大 Skill。
6. **本轮合并的是 Sketch 和接口判断**：没有移动、删除或改写任何源 Skill、Extension、workflow、算法或测试。

## 1. 一眼看懂的科研 Workflow

```text
研究意图 / 数据身份 / manifest
        ↓  speckit-specify + speckit-clarify
输入与样本合同（bio-intake：当前为 Extension 源包）
        ↓
原始 QC 报告（multiqc） + 指标阈值 QC（bio-qc：两者职责不同）
        ↓
MDS / PCA 样本诊断（01-mds：当前仅参考）
        ↓
design / paired / batch / contrast 审计
        ↓
当前首轮 scope 的主推断路径：
  ├─ bulk DE：bulk-pa-luad 适配器 + 02-deg 方法参考
  └─ 共表达：wgcna-module-constraint（条件分支，不替代 DEG）
        ↓
冻结完整 DE / module 结果（02-deg-results 或等价统一合同）
        ├─ DE visualization：03-de-visualization + 03-volcano
        └─ pathway 路由：先选 ORA 或 GSEA
             ├─ GO/常规 pathway：pathway-enrichment + 04-pathway-workflow
             ├─ 外部 Enrichr：04-pathway-enricher（网络/隐私显式记录）
             └─ KEGG 专项：05-kegg（snapshot；SPIA/graphite 需拓扑条件）
        ↓
只对已经冻结且可比较的分支做 cross-branch-integration
        ↓
provenance / human review / Claim boundary / release
```

这不是每个项目都必须走完的直线：WGCNA、GO、KEGG、跨分支整合都是条件分支；但一旦进入某一分支，图、富集和整合都不能绕过其上游合同。

### 1.1 按意图快速选入口

| 你要做的事 | 首选入口 | 必须先锁定 | 不能直接声称 |
|---|---|---|---|
| 只要可打开的 QC 报告 | `multiqc` + `bio-multiqc` | 输入目录、parser、配置、source map | HTML 存在就等于 QC 通过 |
| PA/LUAD 配对 bulk DE | `bulk-pa-luad` → `02-deg` → `02-deg-results` | 独立实验单位、subject/pair、design、contrast、count scale | 简单两组检验可以替代配对/批次模型 |
| 样本结构和批次诊断 | `01-mds`；必要时用 `03-de-visualization` 的 PCA/MDS 部分 | 变换、距离/算法、seed、metadata | 二维距离就是生物学距离 |
| 共表达模块 | `wgcna-module-constraint` | 样本量、network type、power、稳定性 | 共表达边就是因果调控 |
| GO/KEGG 富集 | `pathway-enrichment` → `04-pathway-workflow` | foreground、tested universe、ID、物种、ORA/GSEA | 富集是同一 DE 结果的独立验证 |
| KEGG 拓扑扰动 | `05-kegg` | KEGG ID、organism、snapshot、signaling topology | 所有 KEGG map 都适合 SPIA/graphite |
| 比较两个已完成分支 | `cross-branch-integration` | stable map、namespace、尺度、方向定义 | 共享基因交集就是联合模型或因果机制 |

## 2. 13 个逻辑 Skill 索引

层缩写：`P` = project adapter，`Ref` = reference-only。状态缩写：`P-staged` = 项目适配器已写但完整 runtime 未闭环；`P-slice` = 有局部 wrapper/fixture/test 证据但只覆盖受限切片；`R-only` = 参考副本，不是 runtime。

| 层 | Skill | 输入 → 输出（Sketch） | 不可越过的边界 | 当前状态 |
|---|---|---|---|---|
| P | [`bulk-pa-luad`](./skills/bulk-pa-luad/SKILL.md) | raw integer counts + metadata/pair/contrast → design audit、edgeR/limma 结果、handoff | 不处理 single-cell；不把 TPM/CPM/VST 送进 count model；不静默取消配对/阻断 | `P-staged`；raw-count runtime 未闭环 |
| P | [`cross-branch-integration`](./skills/cross-branch-integration/SKILL.md) | 已冻结的 branch tables + map/ID/方向 → matched/unmatched、intersection、四类 direction strata | 不按行号配对；不推断 namespace；交集不是 joint model/因果结论 | `P-slice`；表级 Python wrapper/test 存在，Skill metadata 的 `Rscript` 入口待统一 |
| P | [`multiqc`](./skills/multiqc/SKILL.md) | bounded QC logs + config → HTML、JSON/source map、verdict、review artifact | 只聚合，不测量阈值；`skip` 不是 release-ready；报告漂亮不等于 QC 通过 | `P-slice`；当前 checkout 无 `.venv`，本轮未重跑 |
| P | [`pathway-enrichment`](./skills/pathway-enrichment/SKILL.md) | 已执行 DE/module + foreground/rank/universe/ID → GO/KEGG 表、mapping audit、provenance | 不发明 gene list；ORA 必须有 tested universe；GSEA 必须有完整 ranking | `P-staged`；GO/KEGG runtime、snapshot、verifier 未闭环 |
| P | [`wgcna-module-constraint`](./skills/wgcna-module-constraint/SKILL.md) | normalized expression + traits + network params → modules、eigengenes、hub、stability | 不是 directed regulation；grey module 不是证据；没有稳定性不能升级为 constraint | `P-staged`；缺 fixture、golden module、preservation verifier |
| Ref | [`01-mds`](./skills/reference-stack/01-mds/SKILL.md) | 变换后的表达/距离 + metadata → PCA/MDS/UMAP 等坐标与诊断 | PCA/MDS 是样本诊断；UMAP/t-SNE 不能当线性效应或生物学距离 | `R-only` |
| Ref | [`02-deg`](./skills/reference-stack/02-deg/SKILL.md) | 表达矩阵 + design/contrast → fitted model、完整 DE 表 | group file 不是完整设计；p-value 不是 FDR；脚本默认不等于项目合同 | `R-only` |
| Ref | [`02-deg-results`](./skills/reference-stack/02-deg-results/SKILL.md) | DE fitted result → frozen table、显著列表、ranking、foreground、universe | `padj=NA` 不能用 `na.omit()` 静默抹掉；ORA 背景不能默认全基因组 | `R-only` |
| Ref | [`03-de-visualization`](./skills/reference-stack/03-de-visualization/SKILL.md) | DE object/result + transformed matrix → MA、PCA/MDS、heatmap、诊断 panel | 作图继承统计结果；不产生第二套 p 值；row scaling 必须标明 | `R-only`；与 `03-volcano` 高重叠 |
| Ref | [`03-volcano`](./skills/reference-stack/03-volcano/SKILL.md) | effect/LFC + p/padj + label rules → volcano、MA、标签表 | shrunken LFC 不重算 p-value；视觉阈值不替代正式效应检验 | `R-only`；作为 DE visualization 专项保留 |
| Ref | [`04-pathway-enricher`](./skills/reference-stack/04-pathway-enricher/SKILL.md) | gene list + Enrichr database → 外部 enrichment table/report | gene symbols 会发往外部 API；不能替代本地 universe/mapping 审计 | `R-only`；外部 API 参考 |
| Ref | [`04-pathway-workflow`](./skills/reference-stack/04-pathway-workflow/SKILL.md) | list/ranking/universe + organism → ORA/GSEA route、结果和去冗余 | ORA 与 GSEA 输入和 estimand 不同；编排 prose 不等于 runtime | `R-only`；作为 pathway router 参考 |
| Ref | [`05-kegg`](./skills/reference-stack/05-kegg/SKILL.md) | KEGG IDs + rank/effect + DB source → KEGG ORA/GSEA、snapshot、SPIA/graphite | live DB、snapshot、普通富集和拓扑推断不能混写 | `R-only`；KEGG 专项参考 |

### 2.1 参考副本的阅读规则

`reference-stack/` 是英文方法和代码来源，`reference-stack-zh-CN/` 是中文审阅镜像；两者都不自动进入 `.agents/skills/`。参考文件中的代码块、CLI 形状和“建议阈值”只有在项目合同、依赖、fixture、verifier 和 workflow 接线都成立后，才可以成为项目行为。

## 3. 第三步：重叠与合并判断

| 决策 | 关系 | 判断 | 压缩后的唯一入口/责任分层 |
|---|---|---|---|
| D1 | `03-de-visualization` ↔ `03-volcano` | **可合并（高置信，限视图/接口）** | 一个 DE visualization 入口；通用诊断由前者承载，shrunken LFC、标签和轴语义由后者保留；源文件先保留 |
| D2 | `pathway-enrichment` ↔ `04-pathway-workflow` ↔ `04-pathway-enricher` ↔ `05-kegg` | **可合并编排，不可合并科学后端** | 项目接口 → ORA/GSEA router → Enrichr 可选 backend / KEGG backend；KEGG topology 独立 gate |
| D3 | `bulk-pa-luad` ↔ `02-deg` ↔ `02-deg-results` | **不合并算法；合并 DE handoff contract** | 场景适配器负责 paired design；通用参考负责模型选择；结果层负责完整表、`padj=NA`、ranking 和 universe |
| D4 | `multiqc` ↔ `bio-qc` ↔ `bio-intake`/metadata QC | **不可合并；应串联** | intake 验证身份，bio-qc 判断指标，MultiQC 聚合报告，review 记录人工决定 |
| D5 | `wgcna-module-constraint` ↔ `pathway-enrichment` | **不可合并；只做模块 handoff** | WGCNA 生成受稳定性约束的 gene set；pathway 解释该输入，不能反向证明网络成立 |
| D6 | `cross-branch-integration` ↔ provenance/evidence kernel | **不可合并；前后相接** | integration 生成可比较对象；provenance/review/kernel 关闭证据状态和 Claim |

因此，“合并”在本阶段只意味着统一阅读入口、对象命名和交接接口；不意味着现在就把源目录压成一个新 Skill，也不意味着把不同 estimand 的结果拼成一个表。

## 4. 不可替代边界

```text
metadata/intake QC       ≠ 原始工具/FASTQ QC       ≠ MDS/PCA 样本结构诊断
样本诊断                 ≠ design matrix 可识别性 ≠ DEG 主推断
DEG 主推断               ≠ DE 结果冻结/注释       ≠ DE visualization
DEG                      ≠ WGCNA 共表达模块
ORA                      ≠ GSEA
普通 pathway enrichment ≠ SPIA/graphite 拓扑扰动
Enrichr live API         ≠ 本地/快照数据库结果
描述性交集               ≠ 联合统计模型           ≠ 因果整合
HTML/report 生成         ≠ QC 通过                ≠ 科学 Claim 成立
工程测试通过             ≠ 统计方法适用           ≠ 独立生物学验证
```

每个等号右侧都要求不同的输入、估计对象、失败规则或证据；不能因为它们在同一 workflow 相邻出现，就把其中一层当成另一层的充分条件。

## 5. 缺失与未闭环：先补什么

这里把“没有项目级实现”与“完全没有来源材料”分开。当前主要问题不是再盲目增加一批同名 Skill，而是把现有参考和适配器接成可验证的共同合同。

| 优先级 | 缺口 | 现有材料 | 还缺什么 |
|---|---|---|---|
| P0 | 统一输入/输出合同 | 各 Skill 分别描述 counts、metadata、design、DE、pathway | `sample/subject/pair/batch`、expression scale、design/contrast、统一 DE result、foreground/ranking/universe、mapping loss、方向和错误码 |
| P0 | Extension / workflow 接线 | `extensions/bio-*` 源包、3 个候选 workflow | 当前 `.specify/extensions.yml` 不存在，`.specify/extensions/` 只有 cache；registry 目前只登记 `speckit`，不能声称已安装可运行 |
| P1 | MDS/PCA 项目 runtime | `01-mds` 与可视化参考 | 固定变换/距离/seed、输入输出 schema、fixture、离群/批次 negative cases 和 verifier |
| P1 | raw-count DE → result freeze | `bulk-pa-luad`、`02-deg`、`02-deg-results` | 固定 R 环境、配对设计 fixture、完整结果表、`padj=NA` 原因、contrast/direction、测试和可复现 provenance |
| P1 | DE visualization 统一入口 | `03-de-visualization`、`03-volcano` | 一个 renderer contract，明确原始/收缩 LFC、p/padj、标签、row scaling 和图表数据一致性 |
| P1 | GO/KEGG runtime 与数据库固定 | `pathway-enrichment`、04 系列、`05-kegg` | ORA/GSEA router、OrgDb/GO.db 版本、KEGG access date/snapshot、mapping/universe verifier、网络策略 |
| P1 | WGCNA 稳定性闭环 | 项目适配器、R 参考脚本 | expression fixture、样本量/混杂 negative cases、golden module、preservation/stability gate |
| P1 | provenance / human review / Claim 串联 | `bio-provenance`、`bio-review`、Evidence Kernel、局部 wrapper | 全链 artifact manifest、输入 hash、命令/版本/参数、review state、claim status 和 release policy |
| P1 | 来源链闭合 | `skill-catalog.yml`、`catalogs/source-stack.yml` | catalog 声明的 `vendor/sources` 当前不存在；需要 source commit/hash 与本机原始来源的可追溯映射 |
| P2 | 全链测试和 benchmark | MultiQC/shared integration 的局部测试；reference examples/tests | MDS/DE/结果/富集/WGCNA 的项目 fixture、fail-closed tests、独立复现、no-skill/with-skill 和 no-Spec/with-Spec 对照 |

### 5.1 “缺失 Skill”应如何理解

- **不是所有缺口都要新建 Skill**：`bio-intake`、`bio-qc`、`bio-provenance`、`bio-review`、`bio-pipeline`、`bio-integration`、`bio-multiqc` 已有 Extension 源包，但不是 Skill，且当前没有安装/注册证据。
- **真正的项目化缺口**：MDS/PCA、通用 DE/result freeze、统一 DE visualization、GO/KEGG/snapshot 和 WGCNA 尚未形成完整项目 runtime；它们有参考或 staged adapter，不等于空白领域。
- **优先补横切合同**：如果先各自实现五个新入口而没有统一 sample、DE、universe、provenance 和错误语义，重叠会再次出现。

## 6. 当前证据能支持什么

| 证据 | 能支持 | 不能支持 |
|---|---|---|
| `.specify/integrations/codex.manifest.json` | 10 个 `speckit-*` 控制面 Skill 已登记 | 5 个生信适配器已完成正式 integration 注册 |
| `.agents/skills/` 与 `spec-mvp/skills/` 的 5 对目录 | 项目适配器的发现/暂存材料存在 | raw-count DE、GO/KEGG、WGCNA 已可直接运行 |
| `spec-mvp/tests/test_multiqc_vertical_slice.py` | MultiQC wrapper 有 3 个局部测试定义：成功、输入变化传播、缺 executable fail-closed | 当前 checkout 已配置 `.venv`，或 QC 阈值/科学 QC 已验证 |
| `spec-mvp/tests/test_shared_integration_mvp.py` | 表级整合有 4 个局部测试定义：四方向、重复 ID、方向冲突、确定性/输入传播 | 上游 DEG 正确、样本对应关系已验证、存在 joint model 或因果结论 |
| `reference-stack` 的 examples/tests | 可用于方法审计、负例和 fixture 设计 | 参考副本是项目 runtime 或 oracle |
| `extensions/` 与候选 `workflows/` | 有可执行设计和部分 wrapper | 当前已安装、已注册、依赖齐全、全链可重跑 |

当前 checkout 还缺 `.venv` 和 `vendor/sources`；`.specify/workflows/workflow-registry.json` 只登记 `speckit`。因此本 Sketch 使用“文件/设计存在”和“本轮运行通过”两套明确语言，避免把历史记录或目录结构写成运行证据。

## 7. 给人和 Agent 的最短阅读协议

1. 先看第 1 节决定路线，再看第 2 节核对 Skill 的输入、输出和状态。
2. 看到 `R-only` 时，只把它当方法参考；看到 `P-staged/P-slice` 时，还要查 wrapper、依赖、fixture、测试和 registry。
3. 看到 `bio-*` 时先问它是 Extension 还是 Skill；Extension 可以执行脚本，但不自动获得科学解释权。
4. 先冻结结果对象，再生成图、富集和跨分支比较；不要从图反推输入。
5. Quick Start 的价值是快速证明“入口—artifact—verifier—review”能闭环；它不充分证明完整分析链的统计有效性或生物学 Claim。

推荐的后续顺序：

```text
P0 统一输入/结果/provenance contract + 明确 registry/install 事实
 ↓
P1 以现有 MultiQC/shared integration 切片验证 workflow 与 review wiring
 ↓
P1 建立一个受限 bulk paired DE → result freeze → ORA/GSEA vertical slice
 ↓
P1 决定 DE visualization 的统一 renderer；再补 KEGG snapshot 与 WGCNA stability
 ↓
P2 用负例、独立复现和 benchmark 关闭“可运行”与“可发布 Claim”的差距
```

## 8. 相关入口

- 逐段来源、ARSSC 标注和完整方法边界：[CONSOLIDATED-SKILLS-WORKFLOW-zh-CN.md](./docs/CONSOLIDATED-SKILLS-WORKFLOW-zh-CN.md)
- 项目适配器说明：[skills/README.md](./skills/README.md)
- 项目 Skill 登记表：[skill-catalog.yml](./skills/skill-catalog.yml)
- 英文参考栈：[reference-stack/README.md](./skills/reference-stack/README.md)
- 中文审阅栈：[reference-stack-zh-CN/README.md](./skills/reference-stack-zh-CN/README.md)
- 参考栈执行顺序：[analysis-order.md](./skills/reference-stack/analysis-order.md)
- Spec Kit integration 登记：[codex.manifest.json](../.specify/integrations/codex.manifest.json)
- Workflow registry：[workflow-registry.json](../.specify/workflows/workflow-registry.json)
- Spec MVP 运行说明：[README.md](./README.md)
- 测试目录：[tests/](./tests/)

本文件是快速决策入口；算法、脚本、Spec、workflow 和测试的语义权威仍在各自源文件。文档中出现的命令、代码块和候选路径均是说明性材料，除非被对应 workflow/command 明确调用，否则不会自动执行。
