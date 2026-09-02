# 原始 Skill、英文备份与中文翻译的来源对照

## 结论先说

当前仓库里出现 `spec-mvp`，是因为英文副本被放在 MVP/Spec 审计项目中管理；这只是**存放位置**，
不是对上游 Skill 的改写。需要区分以下三层：

| 层级 | 位置 | 是否原始 | 是否运行时发现 |
|---|---|---:|---:|
| 本机原始 Skill | `C:/Users/ldc/.codex/skills/` | 是 | 由本机 Skill 环境管理 |
| 英文审计副本 | `spec-mvp/skills/reference-stack/` | 内容等同于复制时的原始文件 | 否 |
| 中文翻译/审阅版 | `spec-mvp/skills/reference-stack-zh-CN/` | 否，是中文整理 | 否 |
| 项目适配器 | `.agents/skills/`、`spec-mvp/skills/` 中登记的项目 Skill | 否，是本项目 Spec/MVP 适配 | 只有登记到运行时的才会发现 |

## 八个参考 Skill 的实际来源

| 分析节点 | 本机原始目录 | 英文副本 | 中文文件 |
|---|---|---|---|
| MDS/PCA/降维 | `C:/Users/ldc/.codex/skills/dimensionality-reduction-plots/` | [`01-mds`](E:/all-agent-workspace/codex-projects/bio-skills/bio-spec-kit/spec-mvp/skills/reference-stack/01-mds/) | [`01-mds`](E:/all-agent-workspace/codex-projects/bio-skills/bio-spec-kit/spec-mvp/skills/reference-stack-zh-CN/01-mds/) |
| DEG | `C:/Users/ldc/.codex/skills/differential-expression-analysis/` | [`02-deg`](E:/all-agent-workspace/codex-projects/bio-skills/bio-spec-kit/spec-mvp/skills/reference-stack/02-deg/) | [`02-deg`](E:/all-agent-workspace/codex-projects/bio-skills/bio-spec-kit/spec-mvp/skills/reference-stack-zh-CN/02-deg/) |
| DE 结果 | `C:/Users/ldc/.codex/skills/de-results/` | [`02-deg-results`](E:/all-agent-workspace/codex-projects/bio-skills/bio-spec-kit/spec-mvp/skills/reference-stack/02-deg-results/) | [`02-deg-results`](E:/all-agent-workspace/codex-projects/bio-skills/bio-spec-kit/spec-mvp/skills/reference-stack-zh-CN/02-deg-results/) |
| DE 可视化 | `C:/Users/ldc/.codex/skills/de-visualization/` | [`03-de-visualization`](E:/all-agent-workspace/codex-projects/bio-skills/bio-spec-kit/spec-mvp/skills/reference-stack/03-de-visualization/) | [`03-de-visualization`](E:/all-agent-workspace/codex-projects/bio-skills/bio-spec-kit/spec-mvp/skills/reference-stack-zh-CN/03-de-visualization/) |
| 火山图/MA | `C:/Users/ldc/.codex/skills/volcano-and-ma-plots/` | [`03-volcano`](E:/all-agent-workspace/codex-projects/bio-skills/bio-spec-kit/spec-mvp/skills/reference-stack/03-volcano/) | [`03-volcano`](E:/all-agent-workspace/codex-projects/bio-skills/bio-spec-kit/spec-mvp/skills/reference-stack-zh-CN/03-volcano/) |
| Enrichr 富集 | `C:/Users/ldc/.codex/skills/pathway-enricher/` | [`04-pathway-enricher`](E:/all-agent-workspace/codex-projects/bio-skills/bio-spec-kit/spec-mvp/skills/reference-stack/04-pathway-enricher/) | [`04-pathway-enricher`](E:/all-agent-workspace/codex-projects/bio-skills/bio-spec-kit/spec-mvp/skills/reference-stack-zh-CN/04-pathway-enricher/) |
| 表达→通路路由 | `C:/Users/ldc/.codex/skills/expression-to-pathways/` | [`04-pathway-workflow`](E:/all-agent-workspace/codex-projects/bio-skills/bio-spec-kit/spec-mvp/skills/reference-stack/04-pathway-workflow/) | [`04-pathway-workflow`](E:/all-agent-workspace/codex-projects/bio-skills/bio-spec-kit/spec-mvp/skills/reference-stack-zh-CN/04-pathway-workflow/) |
| KEGG | `C:/Users/ldc/.codex/skills/kegg-pathways/` | [`05-kegg`](E:/all-agent-workspace/codex-projects/bio-skills/bio-spec-kit/spec-mvp/skills/reference-stack/05-kegg/) | [`05-kegg`](E:/all-agent-workspace/codex-projects/bio-skills/bio-spec-kit/spec-mvp/skills/reference-stack-zh-CN/05-kegg/) |

## 原始文件入口示例

- [原始 MDS Skill](C:/Users/ldc/.codex/skills/dimensionality-reduction-plots/SKILL.md)
- [原始 DEG Skill](C:/Users/ldc/.codex/skills/differential-expression-analysis/SKILL.md)
- [原始 DE 结果 Skill](C:/Users/ldc/.codex/skills/de-results/SKILL.md)
- [原始 KEGG Skill](C:/Users/ldc/.codex/skills/kegg-pathways/SKILL.md)
- [英文审计副本入口](E:/all-agent-workspace/codex-projects/bio-skills/bio-spec-kit/spec-mvp/skills/reference-stack/README.md)
- [中文审阅入口](E:/all-agent-workspace/codex-projects/bio-skills/bio-spec-kit/spec-mvp/skills/reference-stack-zh-CN/README.md)

## 关于“翻译”的准确说明

当前 `reference-stack-zh-CN/` 是**中文审阅版**：说明性段落、方法选择、统计边界和验收重点已用中文整理，
代码块、函数名、参数、命令、文件名和 URL 保持英文。它不是把 19 个 Markdown 逐句逐字重写后的正式译本，
不能替代英文原件作精确语义核对。

因此，当前最可靠的使用方式是：

1. 用中文审阅版理解流程和 Spec 要求；
2. 用英文副本/本机原始 Skill 核对完整算法、示例和 CLI；
3. 把最终纳入运行时的内容写进项目适配器和 Spec，不修改原始 Skill。

## 为什么没有翻译插件

当前可用 Codex Skill/插件列表中没有专门的 Markdown 翻译插件；Codex 可以直接翻译 Markdown。
对科研 Skill 来说，保留原文、参数和代码，再建立带来源链接的中文镜像，比把内容交给不透明的
外部翻译服务更适合复现、审计和隐私控制。

