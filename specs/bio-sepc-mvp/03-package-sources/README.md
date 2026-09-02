# Package Sources

这里是这个独立项目的 preset、workflow 和 extension 源文件。它们是复制的
源包，不代表已经全部安装到某个运行环境；安装状态仍需由对应的 Spec Kit
命令和验证结果确认。

## Preset

- `preset/bio-research-mvp/`
- `preset/bioinformatics/`
- `preset/multiqc-fastqc-mvp.yml`

## Workflow

### 当前项目主 Workflow

- `workflow/bio-research-mvp/`

这是你的项目级 MVP 编排器，当前执行链是：

```text
specify → review-spec → plan → review-plan → tasks
        → multiqc-run → review-execution → record-review
```

它是一个受限的 MultiQC 执行切片，不等于完整的 S00–S13 科研主流程。

### 参考稿（不属于当前项目执行链）

- `workflow/reference-drafts/bio-research-shared-integration/`
  - PA/LUAD 差异结果的 shared-integration 场景参考稿
- `workflow/reference-drafts/bulk-rnaseq/`
  - bulk RNA-seq 的 intake、QC、pipeline、provenance、release 参考稿
- `workflow/reference-drafts/multiqc-vertical-slice.yml`
  - fixture 到验证报告的设计参考稿，原本就不是已注册 workflow
- `workflow/reference-drafts/speckit-workflow.yml`
  - 通用 Spec Kit 的 specify → plan → tasks → implement 参考稿

这些文件保留是为了比较和后续设计，不会自动接入 `bio-research-mvp`。

## Extensions

- `extensions/bio-intake/`
- `extensions/bio-integration/`
- `extensions/bio-multiqc/`
- `extensions/bio-pipeline/`
- `extensions/bio-provenance/`
- `extensions/bio-qc/`
- `extensions/bio-review/`

这些目录解决的是“源包放在哪里”的问题；是否注册、是否可执行、是否通过
科学验证，仍然是独立的状态，不能仅由文件存在推出。
