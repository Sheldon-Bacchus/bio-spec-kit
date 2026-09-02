---
lang: zh-CN
source: ../../reference-stack/05-kegg/SKILL.md
translation-status: review-translation
---

# KEGG 通路、模块与拓扑富集

本文件是 [英文 Skill 原件](../../reference-stack/05-kegg/SKILL.md) 的中文审阅版。它覆盖
KEGG 的三代分析：`enrichKEGG`/`enrichMKEGG` 的 ORA、`gseKEGG` 的 GSEA，以及只对有合适
有向拓扑的信号通路定义的 SPIA/graphite 扰动分析。

## 最重要的可重复性规则

KEGG 是会变化的实时数据库，不是一个永远固定的 R 包。`enrichKEGG`、`gseKEGG` 和 SPIA
可能在调用时访问 REST API；相同代码和相同基因在不同日期可能得到不同结果。发表或基准
测试时，应使用 `gson_KEGG()` 等方式保存快照，记录访问日期、快照哈希和物种；
`use_internal_data=TRUE` 不是当前版本固定方案，而是旧的 2012 `KEGG.db`。

## ID 与物种

- 人/鼠等模式真核生物通常先转换到 Entrez，使用 `keyType='ncbi-geneid'`。
- 细菌/原核生物直接使用 KEGG locus tag，使用 `keyType='kegg'`，不要假定存在
  `org.*.eg.db`。
- 没有自身 KEGG genome 的非模式物种可映射到 KO，再进入 `organism='ko'` 的通路空间。
- 把 ENSEMBL/SYMBOL 直接送进 `enrichKEGG` 常会得到零命中；必须记录映射损失。

## 三代方法如何选

| 问题 | 方法 | 备注 |
|---|---|---|
| 预选基因列表有哪些 KEGG 通路 | ORA：`enrichKEGG`/`enrichMKEGG` | 需要 universe；模块更细但统计功效更低 |
| 全部基因有可靠排名，是否协同偏移 | GSEA：`gseKEGG` | 不设任意 DEG 截断；排名统计量和 seed 要固定 |
| 信号通路中信号沿激活/抑制边如何传播 | SPIA/graphite | 需要 signed log2FC、universe 和适用的 signaling KGML；代谢图不能随便套用 |

## 结果边界

ORA/GSEA 把通路视为基因集合；SPIA 还利用拓扑方向。三者回答不同问题，不能把一个方法
的 p 值当成另一个方法的证据。`pathview` 只是把数据叠加到图上，不是额外的显著性检验。

