# DEG CLI 使用指南（中文审阅版）

英文原件：[references/cli-guide.md](../../../reference-stack/02-deg/references/cli-guide.md)。

## 必需输入

- `--input_file`：基因 × 样本表达矩阵，第一列为基因 ID。
- `--group_file`：样本 ID 与 group 的映射；样本顺序和命名必须能校验。
- `--output_dir`：结果目录。

## 常见选项

`--diff_method`（`limma`/`deseq2`/`edger`/`t`/`wilcox`）、`--norm_method`、
`--p_threshold`、`--logfc_threshold` 和 `--seed`。默认值不能被口头记忆替代；运行前读取
脚本帮助并把实际值写入 provenance。

## 输出检查

确认完整结果表、显著结果、火山图、热图、过滤日志和 `session_info.txt` 都存在；检查
输入哈希、样本匹配和至少每组两个样本的规则。任何“成功但没有结果”的运行都应判为失败。

