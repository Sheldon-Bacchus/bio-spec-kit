# Skill 项目参考映射：MDS / 火山图 / KEGG

更新时间：2026-08-31

本文档只记录外部 skill 项目“可以借鉴什么”，不把外部项目的代码、分数、运行结果或公开答案直接当成本项目的 oracle。外部 skill 在本项目中暂时只作为 reference，不安装、不注册、不注入当前 Agent。

## 名称说明

- `sci-skills` 暂按两个最相关的项目理解：`SciAgent-Skills` 与 `K-Dense scientific-agent-skills`。
- `ciewio skills` 在公开检索中没有找到完全匹配的项目名；这里按最接近的生物信息学 skill 项目 `ClawBio` 记录。若你指的是另一个仓库，只需要替换该行的来源，不影响下面的测试合同设计。

## 项目对照

| 项目 | 已找到的相关内容 | MDS | 火山图 | KEGG | 本项目借鉴方式 |
|---|---|---:|---:|---:|---|
| [SciAgent-Skills](https://github.com/jaechang-hits/SciAgent-Skills) | `pydeseq2/deseq2`、`plotly-interactive-plots`、`omics-plotting`、`gseapy-gene-enrichment`、STRING/通路分析 | 未确认专门 MDS skill | 已确认有显式 Volcano 示例/绘图 skill | 已确认有通路富集/KEGG 相关路径 | 借鉴 DE→图、富集→图的输入字段和图形输出约束；不直接借用其项目自报分数 |
| [ClawBio](https://github.com/ClawBio/ClawBio) | `rnaseq`、`proteomics-de`、`diff-visualizer`、`scrna-embedding`；仓库有 skill maturity tiers | 未确认专门 MDS skill | `proteomics-de` 明确包含 Volcano 与 PCA 输出 | 当前公开目录中未确认已交付的 KEGG skill；README 将 GO/KEGG pathway 列为 wanted skill | 借鉴 `spec-only → scripted → tested → cli-registered → ci-validated → bench-validated` 的证据成熟度，不把“有 skill”当成“已验证” |
| [GPTomics/bioSkills](https://github.com/GPTomics/bioSkills) | differential-expression、ggplot2、pheatmap、clusterProfiler、ReactomePA、enrichplot、SPIA | 未确认专门 MDS skill | 有 DE 与 visualization workflow，具体 Volcano 文件需单独锁定版本后复核 | 明确覆盖 GO/KEGG/Reactome/WikiPathways 的 ORA/GSEA | 借鉴 pathway 的背景集、排序指标、冗余折叠和多条件分析要求 |
| [K-Dense Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills) | PyDESeq2、scientific visualization、数据库/通路分析，官方示例包含 KEGG 路径工作流 | 未确认专门 MDS skill | PyDESeq2/科学绘图可作为火山图流程参考 | 官方说明明确包含 KEGG/Reactome/STRING 等路径访问 | 借鉴“数据访问、分析、可视化”分层；不把其安装方式带入当前 Agent |
| [BioResearch Agent Skills](https://github.com/Alim430/bioresearch-agent) | `bioresearch-differential-expression`、`bioresearch-pathway-enrichment`、`bioresearch-agent-router` | 未确认 | 通过 DE skill 触发 Volcano | 通过 pathway-enrichment 触发 GO/KEGG | 借鉴确定性路由与执行 skill 分离，防止 Agent 因为一个大 skill 包被污染 |

## 直接可迁移的设计点

### 1. MDS：目前没有外部 skill 可直接当作合同

不要把 PCA、UMAP、t-SNE 自动当成 MDS。当前外部项目检索到的是降维或 embedding 能力，尚未找到一个可以直接锁定为“输入、参数、输出和验收规则”完整的 MDS skill。

本项目建议自建 `MDS-001`：

- 输入：经过声明的表达矩阵或距离矩阵、样本元数据、样本 ID 和分组字段。
- 输出：`mds_coordinates.tsv`、`mds_plot.png`、参数/软件版本记录。
- 确定性验证：样本数和 ID 一致；坐标行数一致；组别标签来自输入；用样本间距离或距离矩阵相关性验证，不直接比较原始 x/y 坐标。
- 原因：MDS 坐标可以发生轴翻转、旋转或尺度变化，直接逐点比较坐标会产生假阴性。
- negative cases：元数据样本缺失、重复 ID、把 raw counts 当作已规范化输入、距离矩阵非对称。

### 2. 火山图：借鉴最多的是输入字段和语义验证

本项目建议自建 `VOLCANO-001`，不以图片相似度作为唯一正确性：

- 输入字段至少固定为 `gene_id`、`log2FoldChange`、`padj`，并声明 contrast 方向。
- 输出至少包含分类表和图；分类表记录 `up/down/ns`、阈值、`-log10(padj)` 的处理方式。
- 验证阈值线、方向、显著基因计数、有限值处理、标签来源和 contrast 方向。
- negative cases：把 raw `pvalue` 当 `padj`、上下调方向反转、缺少 `padj`、无穷值/零值处理不透明。

### 3. KEGG：重点是可追溯的富集语义，而不只是画一张图

本项目建议自建 `KEGG-001`：

- 输入必须声明 organism code、gene ID namespace、up/down 集合、背景 universe、ORA 或 GSEA、显著性阈值和多重检验方法。
- 输出至少包含 enrichment table、图、ID 映射记录、数据库/快照日期和运行参数。
- 验证方向是否分开、背景集是否存在、ID namespace 是否匹配、multiple-testing 列是否真实使用、网络不可用时是否 fail closed。
- negative cases：错误物种、Entrez/Ensembl 混用、没有背景集、把上下调基因混成一个集合、在线 API 失败却输出“成功”。

## 对 `spec-fixture-design` 的落地边界

这三项属于后续 `spec-fixture-execution` 的生物科研执行案例，不应把它们混进当前 `spec-fixture-design` 的 Spec 设计判断。当前设计 bundle 只需要保存：

1. 外部参考来源和适用边界；
2. 三项本地合同的字段草案；
3. 需要自建的 negative cases；
4. hidden oracle 与 deterministic verifier 的分离规则。

外部项目的可运行 demo 可以帮助构造 fixture，但不能直接证明本项目的科研 Claim。最终报告必须分别报告单一 Skill、Clean Skill、Build Skill、LLM、Agent/Workflow 和科研 Claim，不能压成一个总分。

## 参考项目的限制

- 项目 README 中的 skill 数量、准确率或 benchmark 结果是项目方自报信息，除非有独立、可复核的 protocol、输入、oracle 和 verifier，否则不写入本项目的性能结论。
- 公开 skill 往往只证明“能够执行某个流程”，不证明输出科研上正确。
- 没有明确版本、数据库快照和参数的 KEGG 结果不可作为稳定 oracle。
- 外部 skill 不能直接写入本项目的 Agent context；先做 clean-room、build/materialization 和 contract tests，再决定是否进入对照实验。

