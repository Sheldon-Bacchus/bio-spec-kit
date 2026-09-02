# Workflow Layout

这里明确区分当前项目 workflow 和参考稿。

## 当前项目

`bio-research-mvp/` 是当前项目唯一的主 workflow。它把 Spec Kit 的
specify / plan / tasks 生命周期和一次受限的 MultiQC 执行切片连接起来，
并在执行后要求人工审查和记录批准。

## 参考稿

`reference-drafts/` 中的文件不属于当前项目的连续执行链：

- `bio-research-shared-integration/`：PA/LUAD DEG shared-integration 场景
- `bulk-rnaseq/`：bulk RNA-seq 生命周期场景
- `multiqc-vertical-slice.yml`：fixture 到验证报告的设计切片
- `speckit-workflow.yml`：通用 Spec Kit SDD 生命周期

参考稿可以提供接口、门禁和步骤设计，但不能因为存在于这个目录，就视为
当前项目已经注册、可执行或已完成科学验证。
