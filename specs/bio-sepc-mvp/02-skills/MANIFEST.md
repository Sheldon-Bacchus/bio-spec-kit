# Skill Manifest

## 1. Spec Kit core：9 个核心阶段

这些是生成和推进 Spec Kit 生命周期的核心命令 Skill：

1. `spec-kit-core/speckit-constitution`
2. `spec-kit-core/speckit-specify`
3. `spec-kit-core/speckit-clarify`
4. `spec-kit-core/speckit-plan`
5. `spec-kit-core/speckit-tasks`
6. `spec-kit-core/speckit-analyze`
7. `spec-kit-core/speckit-checklist`
8. `spec-kit-core/speckit-implement`
9. `spec-kit-core/speckit-converge`

辅助命令 `speckit-taskstoissues` 位于
`spec-kit-auxiliary/speckit-taskstoissues`，不计入核心九阶段。

## 2. Bio logical components：13 个逻辑组件

### 5 个项目适配器

- `adapters/bulk-pa-luad`
- `adapters/cross-branch-integration`
- `adapters/multiqc`
- `adapters/pathway-enrichment`
- `adapters/wgcna-module-constraint`

### 8 个参考组件

- `reference-stack/01-mds`
- `reference-stack/02-deg`
- `reference-stack/02-deg-results`
- `reference-stack/03-de-visualization`
- `reference-stack/03-volcano`
- `reference-stack/04-pathway-enricher`
- `reference-stack/04-pathway-workflow`
- `reference-stack/05-kegg`

`reference-stack-zh-CN/` 是中文镜像，`runtime-projection/` 是 5 个项目适配器
的宿主运行时副本；两者都不增加逻辑组件分母。

## 3. Source mapping

| 独立项目层 | 原始来源 |
|---|---|
| `01-spec-work-package/` | `specs/005-skills-nextflow-research-core/` |
| `02-skills/adapters/` | `spec-mvp/skills/<adapter>/` |
| `02-skills/reference-stack/` | `spec-mvp/skills/reference-stack/` |
| `02-skills/reference-stack-zh-CN/` | `spec-mvp/skills/reference-stack-zh-CN/` |
| `02-skills/spec-kit-core/` | `.agents/skills/speckit-*`（9 个核心阶段） |
| `02-skills/spec-kit-auxiliary/` | `.agents/skills/speckit-taskstoissues/` |
| `02-skills/runtime-projection/` | `.agents/skills/<adapter>/` |
| `03-package-sources/preset/` | `presets/` 和 `spec-mvp/presets/multiqc-fastqc-mvp.yml` |
| `03-package-sources/workflow/bio-research-mvp/` | `workflows/bio-research-mvp/`；当前项目主 workflow |
| `03-package-sources/workflow/reference-drafts/` | 其他 `workflows/`、`spec-mvp/workflows/multiqc-vertical-slice.yml`、`.specify/workflows/speckit/workflow.yml`；参考稿 |
| `03-package-sources/extensions/` | `extensions/` |

## Workflow role

| 文件/目录 | 角色 | 是否属于当前项目主执行链 |
|---|---|---|
| `03-package-sources/workflow/bio-research-mvp/` | 你的项目级 MVP workflow；当前只执行受限 MultiQC slice | 是 |
| `03-package-sources/workflow/reference-drafts/bio-research-shared-integration/` | PA/LUAD DEG shared-integration 参考稿 | 否 |
| `03-package-sources/workflow/reference-drafts/bulk-rnaseq/` | bulk RNA-seq 场景生命周期参考稿 | 否 |
| `03-package-sources/workflow/reference-drafts/multiqc-vertical-slice.yml` | fixture → verified MultiQC 设计参考稿 | 否 |
| `03-package-sources/workflow/reference-drafts/speckit-workflow.yml` | 通用 Spec Kit SDD workflow 参考稿 | 否 |
