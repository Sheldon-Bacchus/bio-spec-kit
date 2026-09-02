# 五个模块的第一轮设计讨论

这份讨论稿由本地上游源码审计和 3 个只读子任务汇总而来。当前只固定
边界和 contract，不把尚未安装的 R 生态工具伪装成已完成 runtime。

## 共识

- 固定绑定 skill，暂不开发动态 router。
- `SKILL.md` 负责触发边界、决策约束、preset 选择和失败策略；脚本/R/CLI
  负责确定性计算；Spec 只定义用户可观察行为。
- 上游内容保留为 `references/`，项目入口只做薄适配；来源目录不整体复制
  到默认运行时。
- 所有模块都需要输入 manifest、command、executable/version、stdout/stderr、
  exit code、输出 artifact 和内容级 verification。
- Agent 不得手工改写 p-value、FDR、NES、kME、交集表或 verification passed
  状态来满足验收。

## 模块决策表

| 模块 | 第一版定位 | executable/tool | 主要 preset | 关键例外 |
|---|---|---|---|---|
| `bulk-pa-luad` | paired bulk DE，edgeR QL 主路径，limma-voom 敏感性路径 | `Rscript`, edgeR, limma | `paired-edger-limma-default`; quality-weighted 和 v3 reproduction 后置 | pairing 不完整、非整数 counts、设计不满秩、R 包缺失 |
| `cross-branch-integration` | 确定性 branch 表对齐、gene intersection、方向分层 | Python/R 表格脚本；不自动启动 MOFA/DIABLO/SNF | `de-overlap-direction-default` | ID namespace/contrast 不一致、重复 gene、推断 sample map、无 held-out validation |
| `pathway-enrichment` | GO/KEGG ORA + 完整 rank GSEA 的受约束入口 | `Rscript`, clusterProfiler, OrgDb/GO.db | `ora-go-kegg`; `gsea-go-kegg` 后置 | ORA 无 universe、mapping 丢失不明、GSEA 无完整 rank、KEGG 未 pin |
| `wgcna-module-constraint` | bulk signed WGCNA、module-trait、kME hub、稳定性后才可作 constraint | `Rscript`, WGCNA | `wgcna-signed-bulk` | n<15、raw counts/scRNA dropout、network type 不一致、无 preservation/resampling |
| `multiqc` | fixture → wrapper → MultiQC → verified HTML/JSON | `python` wrapper → `.venv/Scripts/multiqc.exe` | `fastqc-multiqc-mvp` | executable/input/config/JSON/source map/fixture marker 缺失；敏感数据不得网络摘要 |

## `bulk-pa-luad`

`limma2` 在已缓存来源中不是包名、命令或独立 skill。目录名按用户原文保留，
正文把它解释为当前 PA-LUAD 场景下的 paired analysis；实际工具名写 `limma`。
paired 模型至少要有 `sample_id`, `subject_id`, `condition`，并将 subject 作为
blocking term，例如 `~ subject + condition`。edgeR 和 limma 必须使用同一 pairing
语义，但结果字段保持各自命名（`FDR` 与 `adj.P.Val`）。不把 FASTQ、STAR、
Salmon 或 Nextflow 塞进这个 downstream count-matrix skill。

## `cross-branch-integration`

第一版只实现可重算的表级 branch：schema/namespace/contrast validation、交集、
union、`up_up/down_down/up_down/down_up` 及单支显著分类。真正的多组学 joint
model 只有在 sample correspondence、scale、missingness、batch 和 validation
通过之后才允许增加独立 preset。它不能把“共享 gene”升级成因果结论。

## `pathway-enrichment`

默认先实现 ORA，因为 module gene list 和阈值化 DE list 都是天然 foreground；
必须显式传入 tested-gene universe。只有完整 ranked list 才走 GSEA，rank 需记录
来源（edgeR signed statistic、limma moderated t 等）和 seed。GO ontology、ID type、
mapping 数据库版本均显式写出；KEGG 是可变外部状态，必须记录 access date 或
冻结 snapshot。结果是 hypothesis generation，不是对同一 DE list 的验证。

## `wgcna-module-constraint`

只支持 normalized bulk expression 的 `wgcna-signed-bulk` preset。`pickSoftThreshold`
和 `blockwiseModules` 的 network type 必须一致，hub 用 signed kME；`grey` 不是
正常模块，scale-free R² 是 heuristic。第一版把稳定性/保存性作为“可用于约束”
的 gate，而不是看到一张漂亮 dendrogram 就放行。

## `multiqc`

这是目前唯一已接通 executable 的模块。项目 skill 只负责选择 preset、调用
现有 wrapper 和读取 verdict；MultiQC 只负责解析上游 FastQC log 并写报告，
单独的 verifier 负责确认 report data/source map/log 与 fixture 一致。MultiQC
不是 threshold gate，人工 review 和后续 workflow gate 仍归 Spec/Workflow Core。

## 下一步实现顺序

1. 以当前 MultiQC vertical slice 作为共同 artifact/provenance contract 的
   reference implementation。
2. 为 `bulk-pa-luad` 实现 R wrapper 和 paired fixture，先只交付 edgeR QL +
   limma-voom 两条路径。
3. 为 `cross-branch-integration` 实现纯表级 deterministic wrapper，接收两个
   已执行 DE 结果。
4. 为 `pathway-enrichment` 先实现 offline GO/custom-GMT ORA，再单独处理 KEGG
   snapshot 和 GSEA。
5. 最后实现 WGCNA signed bulk wrapper 和稳定性 gate，再把 module genes 交给
   pathway skill。
