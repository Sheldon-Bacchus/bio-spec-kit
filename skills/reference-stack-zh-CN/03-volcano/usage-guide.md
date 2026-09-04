# 火山图与 MA 图使用指南（中文审阅版）

英文原件：[reference-stack/03-volcano/usage-guide.md](../../reference-stack/03-volcano/usage-guide.md)。

## 推荐流程

1. 从冻结的完整 DE 表读取原始 p、调整后 p、未收缩/收缩 LFC 和基因 ID。
2. 预先声明颜色规则（例如 FDR、LFC 的联合门槛）以及极端值处理。
3. 生成火山图和 MA 图，导出源数据、比较名称、n、软件版本和参数。
4. 对关键基因回到完整表核对 `padj=NA`、低计数、离群和 ID 注释。

示例命令和代码以英文原件为准；中文文件不复制一套容易漂移的脚本。

