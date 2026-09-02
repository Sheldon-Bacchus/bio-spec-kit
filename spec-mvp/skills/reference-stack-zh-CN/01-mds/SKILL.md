---
lang: zh-CN
source: ../../reference-stack/01-mds/SKILL.md
translation-status: review-translation
---

# 降维图（PCA、MDS、t-SNE、UMAP、PHATE）

本文件是 [英文 Skill 原件](../../reference-stack/01-mds/SKILL.md) 的中文审阅版。
它规定如何选择和解释高维组学数据的二维投影，重点是“图展示了什么、没有展示什么”。

## 核心原则

- bulk RNA-seq 样本 QC 通常先对 log/VST 表达做 PCA；若项目使用 classical MDS，必须把
  距离度量和算法名称写入 Spec，不能把 PCA 和 MDS 混称。
- PCA 保留线性方差，具有可解释的载荷和方差解释率；适合发现批次效应和样本离群。
- t-SNE 主要保留局部邻域；UMAP 近似流形并保留部分全局结构；PHATE/扩散图更适合连续
  过渡。它们的超参数和随机种子会改变图形。
- 二维嵌入会扭曲高维几何。簇间距离、点密度和“两个簇之间的空隙”不能自动当作生物学
  距离、细胞比例或轨迹证据。

## 选择和记录

记录输入变换（raw/log/VST）、是否缩放、距离或相似度、`n_components`、
`n_neighbors`/`perplexity`/`min_dist`、初始化方式、随机种子、软件版本和元数据颜色。
批次诊断应同时看 condition 与 batch；不要只给一张未标注的漂亮二维图。

## 项目首轮建议

1. 先使用 PCA 或合同指定的 MDS 做样本层 QC。
2. 若需要非线性图，仅作为补充展示，并以高维指标、距离矩阵或独立验证支撑结论。
3. 保存投影坐标、载荷/方差解释率、输入哈希和参数，使图可以重算。
4. 将“样本诊断通过/需复核”作为门禁，不能用降维图直接证明 DEG 或通路机制。

## 相关原件

完整算法分类、R/Python 示例和版本兼容性见 [英文 SKILL.md](../../reference-stack/01-mds/SKILL.md)；
使用提示见 [中文 usage guide](usage-guide.md)。

