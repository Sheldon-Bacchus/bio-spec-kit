# Project skill staging

`spec-mvp/skills/` is the auditable source tree for the first five project
skills. Long upstream material is kept under each skill's `references/` and is
read only for the selected decision. The runnable Codex discovery copies live
under `.agents/skills/` because the Codex integration discovers
`.agents/skills/<name>/SKILL.md`, not arbitrary package directories.

The five initial adapters are:

| Skill | Main role | Runtime binding | Current status |
|---|---|---|---|
| `bulk-pa-luad` | tool use + result interpretation | `Rscript`, edgeR, limma | adapter staged; runtime needs pinned R environment |
| `cross-branch-integration` | workflow control + interpretation | `Rscript` and table/matrix libraries | adapter staged; no joint model in MVP |
| `pathway-enrichment` | tool use + interpretation | `Rscript`, clusterProfiler, OrgDb/GO.db | adapter staged; GO/KEGG runtime pending |
| `wgcna-module-constraint` | tool use + interpretation | `Rscript`, WGCNA | adapter staged; stability gate pending |
| `multiqc` | tool use + workflow control | project wrapper + MultiQC 1.35 | executable path available in `.venv` |

These are project adapters, not a wholesale import of `vendor/sources/`. Their
source paths and boundaries are recorded in `skill-catalog.yml`.

## Upstream reference stack for the first transcriptomics pass

The review-only copies for the planned analysis chain are under
`spec-mvp/skills/reference-stack/`. Read them in this order:

```text
01-mds → 02-deg → 02-deg-results → 03-de-visualization/03-volcano
       → 04-pathway-workflow → 05-kegg
```

This directory is deliberately outside `.agents/skills/`: it is not runtime
discovery and does not silently add external skills to the project's allowlist.
The mapping, source paths, and boundaries are documented in its `README.md`.

For Chinese review, a parallel non-runtime mirror is available at
`spec-mvp/skills/reference-stack-zh-CN/`. It contains Chinese summaries and
decision points while preserving links to the complete English originals. It
is a translation/review backup, not an additional discovered Skill.
