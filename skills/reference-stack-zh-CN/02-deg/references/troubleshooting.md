# DEG 排错指南（中文审阅版）

英文原件：[references/troubleshooting.md](../../../reference-stack/02-deg/references/troubleshooting.md)。

| 错误 | 含义 | 处理 |
|---|---|---|
| `SKILL_FILE_NOT_FOUND` | 脚本或输入文件路径错误 | 先解析绝对路径并记录工作目录，不要自动猜路径 |
| `SKILL_SAMPLE_MISMATCH` | 表达矩阵和分组表的样本不一致 | 输出缺失/多余 ID，修复映射后重新运行 |
| `SKILL_FILTER_ERROR` | 过滤参数非法或过滤后没有可检验基因 | 检查阈值、ID 和输入尺度，失败应停止 |

其他常见问题包括把 TPM/FPKM 当 raw counts、重复样本 ID、组内重复不足、把 `padj=NA`
全部删除，以及把错误的 ID 类型送入 GO/KEGG。所有排错动作都要写入运行日志，不能静默
修改输入或阈值。

